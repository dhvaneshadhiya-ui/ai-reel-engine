#!/usr/bin/env python3
"""Prove the calibrated VO alarm still detects a flat read.

WHY THIS EXISTS: on 2026-08-27 the alarm floor was lowered from the creator
band (3.5) to a corpus-derived one (~2.0), because the user deliberately chose
a voice that reads at ~2.4 and the old floor fired on every reel forever. That
is a legitimate change and also EXACTLY what an illegitimate one looks like —
lowering a bar until the red light goes green.

The difference has to be demonstrable, so this suite asserts both halves:
the alarm stays quiet on reads we actually ship, AND it still fires on a read
that is genuinely flat. A calibration that cannot fail is not a calibration,
it is a deletion.
"""
from __future__ import annotations

import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

fails, checks = [], 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global checks
    checks += 1
    if not cond:
        fails.append(f"{label}: {detail}")


def synth(path: Path, semitone_sd: float, seconds: float = 6.0) -> None:
    """A voiced tone whose pitch wanders by a known amount. Not speech —
    the estimator only ever sees f0, so a controlled f0 is the honest
    fixture: it lets us state the expressiveness we are testing."""
    sr, base = 16000, 150.0
    n = int(sr * seconds)
    rng = np.random.default_rng(7)
    # one pitch value per 100ms, smoothed, scaled to the target spread
    steps = rng.normal(0, 1, int(seconds * 10))
    steps = np.convolve(steps, np.ones(3) / 3, mode="same")
    steps = steps / (steps.std() or 1) * semitone_sd
    f0 = base * 2 ** (np.repeat(steps, sr // 10)[:n] / 12)
    phase = np.cumsum(2 * np.pi * f0 / sr)
    sig = 0.5 * np.sin(phase) + 0.2 * np.sin(2 * phase)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((sig * 32767).astype(np.int16).tobytes())


def run(wav: Path) -> str:
    return subprocess.run([sys.executable, str(ROOT / "tools/vo_qc.py"),
                           "--wav", str(wav)], capture_output=True,
                          text=True, cwd=ROOT).stdout


def main() -> int:
    cal_p = ROOT / "voice_calibration.json"
    check("calibration exists", cal_p.exists(),
          "run: python3 tools/vo_qc.py --recalibrate")
    if not cal_p.exists():
        print(f"vo_qc self-test FAILED ({len(fails)} of {checks})")
        return 1
    cal = json.loads(cal_p.read_text())

    for key in ("n", "mean", "floor", "range_floor", "samples"):
        check(f"calibration records {key}", key in cal)
    check("calibration names its voice",
          cal.get("voice_id") == "bb79e8390b4340ce8793ea5f123dbba7")

    # THE HALF THAT MATTERS: the floor must sit BELOW everything we ship (or
    # it fires forever) and ABOVE zero (or it can never fire at all).
    shipped = list(cal["samples"].values())
    check("floor is under every shipped read",
          cal["floor"] <= min(shipped),
          f"floor {cal['floor']} vs flattest shipped {min(shipped)}")
    check("floor is not vacuous", cal["floor"] > 0.5, str(cal["floor"]))
    check("floor is not silently back at the creator band",
          cal["floor"] < 3.5)

    tmp = Path(subprocess.run(["mktemp", "-d"], capture_output=True,
                              text=True).stdout.strip())

    # 1. a read at our own mean must stay quiet
    ok_wav = tmp / "ours.wav"
    synth(ok_wav, cal["mean"])
    out = run(ok_wav)
    check("a typical read for us does NOT alarm",
          "FLAT FOR US" not in out, out[-200:])

    # 2. a genuinely flat read MUST still alarm — this is the whole point
    flat_wav = tmp / "flat.wav"
    synth(flat_wav, max(cal["floor"] - 0.8, 0.3))
    out = run(flat_wav)
    check("a genuinely flat read STILL alarms", "FLAT FOR US" in out,
          f"alarm did not fire at {max(cal['floor'] - 0.8, 0.3):.2f} "
          f"semitones (floor {cal['floor']})")

    # 3. the creator gap must remain VISIBLE — we do not get to stop knowing
    out = run(ok_wav)
    check("the creator band is still printed", "3.74-6.63" in out)
    check("the creator gap is still reported", "vs creators" in out)
    check("provisional sample size is disclosed",
          ("PROVISIONAL" in out) == (cal["n"] < 5))

    if fails:
        print(f"vo_qc self-test FAILED ({len(fails)} of {checks})")
        for f in fails:
            print(f"  - {f}")
        return 1
    print(f"vo_qc self-test PASSED — {checks} checks "
          f"(alarm calibrated to n={cal['n']}, still fires below "
          f"{cal['floor']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
