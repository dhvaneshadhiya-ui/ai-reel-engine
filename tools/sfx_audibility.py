#!/usr/bin/env python3
"""Can a viewer actually HEAR each sound effect? Measured from stems, not the mix.

WHY STEMS
---------
Every reel carries 6-9 SFX cues, calibrated since 2026-08-18 to land at the same
effective peak — and nothing had ever checked that any of them is audible over
the voice. Two attempts on 2026-09-11 to answer that from the FINAL MIX failed:
whisper's word timings run 193 of 225 word pairs back to back, so "the cue sits
inside a word" meant nothing; and subtracting the voice from the mix aligned at
r ~0.85, which leaks enough voice that plain speech with no cue nearby scored as
high as the cues did. The control proved the method could not tell a sound
effect from the leak.

So this renders the SAME timeline twice, audio only — `stem: "sfx"` (only the
sound effects) and `stem: "rest"` (everything else: voice, music) — using the
switch in src/Reel.tsx. The two line up by construction. Each cue is then read
against whatever is playing under it, at that exact moment. Both stems are
pre-master; the two-pass master applies one gain to both, so the ratio holds.

Idea from video-talkcraft's sfx_check (PolyForm Noncommercial — not copied;
this is our own implementation). Its thresholds are BORROWED from its calibration
on its own good and bad reels, and are not yet calibrated on ours:

    MISSING   effect peak < -45 dBFS in the window — the cue renders silent
    UNMASKED  what is under it is quiet (< -40 dBFS RMS) and the effect peaks
              >= -38 dBFS — it lands in a pause; it will be heard
    AUDIBLE   effect peak >= the RMS under it minus 6 dB — audible over speech
    MASKED    anything else — buried; it might as well not be there

    python3 tools/sfx_audibility.py <slug>           # render stems, measure
    python3 tools/sfx_audibility.py <slug> --reuse   # measure existing stems
    python3 tools/sfx_audibility.py --selftest

Exits 1 only for a MISSING cue: an effect that makes no sound is a render fault.
MASKED is advice — how loud a whoosh should be is craft, under the constitution.
"""
from __future__ import annotations

import array
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
WIN = 0.35              # seconds read after each cue's start
PRESENT = -45.0         # dBFS peak: below this the cue is not in the render
QUIET = -40.0           # dBFS RMS of what is under the cue: a pause
UNMASK = -38.0          # dBFS peak an effect needs to be heard in a pause
MARGIN = 6.0            # dB below the RMS under it an effect may peak and still be heard


def _db(v: float) -> float:
    return 20 * math.log10(v) if v > 1e-9 else -120.0


def peak_db(x) -> float:
    return _db(max((abs(s) for s in x), default=0.0))


def rms_db(x) -> float:
    n = len(x)
    return _db(math.sqrt(sum(s * s for s in x) / n)) if n else -120.0


def classify(sfx, rest) -> tuple[str, float, float]:
    """(verdict, effect peak dBFS, RMS under it dBFS) for one cue window."""
    sp, rr = peak_db(sfx), rms_db(rest)
    if sp < PRESENT:
        return "MISSING", sp, rr
    if rr < QUIET and sp >= UNMASK:
        return "UNMASKED", sp, rr
    if sp >= rr - MARGIN:
        return "AUDIBLE", sp, rr
    return "MASKED", sp, rr


def cues(slug: str) -> list[tuple[float, str]]:
    """Absolute cue times from the beat sheet: scene start + the cue's `at`."""
    b = json.loads((ROOT / "src" / "beats" / f"{slug}.json").read_text())
    t, out = 0.0, []
    for sc in b["scenes"]:
        for c in (sc.get("sfx") or []):
            out.append((t + float(c.get("at") or 0), str(c.get("src", "")).split("/")[-1]))
        t += float(sc["durationSec"])
    return out


def decode(path: Path) -> array.array:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    a = array.array("f")
    a.frombytes(raw)
    return a


def render_stem(slug: str, stem: str, out: Path) -> None:
    """Audio-only render of one stem. Not a deliverable, so it does not go
    through render_job.py's gates — it changes nothing that ships."""
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["npx", "remotion", "render", "src/index.ts", slug, str(out),
                        "--codec=wav", "--props", json.dumps({"stem": stem}),
                        "--timeout=120000"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0 or not out.exists():
        sys.exit(f"stem render failed ({stem}):\n{r.stderr[-1200:]}")


def measure(slug: str, reuse: bool) -> int:
    d = ROOT / "out" / "stems"
    sfx_p, rest_p = d / f"{slug}-sfx.wav", d / f"{slug}-rest.wav"
    if not (reuse and sfx_p.exists() and rest_p.exists()):
        print(f"  rendering stems for {slug} (audio only) ...")
        render_stem(slug, "sfx", sfx_p)
        render_stem(slug, "rest", rest_p)
    sfx, rest = decode(sfx_p), decode(rest_p)
    rows = []
    print(f"\n  {'at':>7}  {'cue':24} {'effect pk':>10} {'under it':>9}  verdict")
    for t, name in cues(slug):
        a, b = int(t * SR), int((t + WIN) * SR)
        v, sp, rr = classify(sfx[a:b], rest[a:b])
        rows.append(v)
        print(f"  {t:6.2f}s  {name[:24]:24} {sp:8.1f}dB {rr:7.1f}dB  {v}")
    n = len(rows)
    counts = {k: rows.count(k) for k in ("UNMASKED", "AUDIBLE", "MASKED", "MISSING")}
    print("\n  " + ", ".join(f"{k} {v}" for k, v in counts.items()) + f"  (of {n})")
    if counts["MASKED"] * 2 > n:
        print("  ADVICE: most cues are buried under the voice. Move them into the "
              "pauses, or raise them — thresholds are talkcraft's, not yet ours.")
    return 1 if counts["MISSING"] else 0


def selftest() -> int:
    ok = True

    def t(label, cond):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")

    n = int(WIN * SR)
    silence = [0.0] * n
    tone = lambda amp: [amp * math.sin(2 * math.pi * 200 * i / SR) for i in range(n)]
    click = lambda amp: [amp if i < 200 else 0.0 for i in range(n)]
    t("an effect in a pause is UNMASKED", classify(click(0.5), silence)[0] == "UNMASKED")
    t("an effect at speech level is AUDIBLE", classify(click(0.2), tone(0.14))[0] == "AUDIBLE")
    t("a faint effect under loud speech is MASKED", classify(click(0.03), tone(0.45))[0] == "MASKED")
    t("a cue that renders silent is MISSING", classify(silence, tone(0.1))[0] == "MISSING")
    t("dB of full scale is 0", abs(peak_db([1.0])) < 1e-9)
    print("sfx_audibility selftest", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main() -> None:
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if not a or a[0].startswith("-"):
        sys.exit(__doc__.strip().splitlines()[0] +
                 "\n  usage: sfx_audibility.py <slug> [--reuse] | --selftest")
    sys.exit(measure(a[0], "--reuse" in a))


if __name__ == "__main__":
    main()
