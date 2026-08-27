#!/usr/bin/env python3
"""Measure the READ, not the words. Catches a flat or fumbling voiceover.

WHY THIS EXISTS
---------------
Every check in this repo looked at the SCRIPT — shape, tics, claims, loops —
and nothing ever listened to what came back from the voice. So a read the
user described as "flat, no energy, no emotion" shipped through a green
pipeline (2026-08-26). The words were fine. The performance was not, and
nothing was measuring performance.

THE BAND IS MEASURED, NOT INVENTED (G23 discipline). Three real creator
shorts the user supplied as references, analysed with the same estimator:

    reference #1   pitch sd 3.74 semitones   range 11.6
    reference #2   pitch sd 5.00             range 16.3
    reference #3   pitch sd 6.63             range 17.4
    ------------------------------------------------------
    our master     pitch sd 2.83             range  9.1     <- half the movement

Pitch standard deviation in semitones is the standard correlate of vocal
expressiveness: a monotone read clusters near its median, an engaged one
moves. 3.5 is the floor because the flattest real creator sits at 3.74 and
ours at 2.83 — the gap between them is the thing the user can hear.

STRESS INVERSION is the second measure, and it is what "fumbling" actually
is. In the flagged opening, "the" was held 0.34s while "reading" — the word
carrying the meaning — got 0.28s, and then "why the top" rushed by at 0.14s
each. Function words longer than the content words beside them is a reader
who does not know which word matters.

    python3 tools/vo_qc.py <slug>
    python3 tools/vo_qc.py --wav path.wav [--json path/vo.json]
"""
from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

PITCH_SD_FLOOR = 3.5          # flattest real creator = 3.74; ours was 2.83
PITCH_RANGE_FLOOR = 10.0      # p95-p5 semitones; references 11.6-17.4
CALIBRATION = ROOT / "voice_calibration.json"

# WHY THIS GREW A CALIBRATION (2026-08-27)
# ----------------------------------------
# The 3.5 floor is real and stays visible: it is where the flattest measured
# creator sits. But on 2026-08-27 the user listened to five generations —
# including one that cleared 3.5 — and DELIBERATELY kept the voice that reads
# at ~2.4. Whose voice the channel has is an identity decision, not a
# statistic's call.
#
# That turned the floor into a permanent alarm: it would fire on every reel,
# forever, and be correctly ignored every time. A check that is always ignored
# is worse than no check, because it teaches the reader to skim past the one
# run that matters.
#
# So the ALARM is now calibrated to our own corpus — it fires when a read is
# unusually flat FOR US — while the creator band is still PRINTED on every
# run. We do not get to stop knowing we sit below it. What we stop doing is
# treating a settled decision as a fresh defect.
#
# This is the same pattern as check_script's calibration, deliberately: the
# threshold is DERIVED from shipped work, recorded with its sample count, and
# recalibrated by an explicit command rather than edited by hand.


def load_calibration() -> dict | None:
    try:
        c = json.loads(CALIBRATION.read_text())
        return c if c.get("floor") else None
    except Exception:                                          # noqa: BLE001
        return None


def corpus_wavs() -> list[Path]:
    seen, out = set(), []
    for pat in ("_sources/*/vo.wav", "_sources/*/vo-directed.wav",
                "public/assets/*/vo.wav"):
        for w in sorted(ROOT.glob(pat)):
            if w.stat().st_size > 0 and w.resolve() not in seen:
                seen.add(w.resolve())
                out.append(w)
    return out


def measure(wav: Path) -> tuple[float, float] | None:
    f0 = f0_track(wav)
    if len(f0) < 50:
        return None
    st = 12 * np.log2(f0 / np.median(f0))
    st = st[np.abs(st) < 12]
    return float(st.std()), float(np.percentile(st, 95) - np.percentile(st, 5))


def recalibrate() -> int:
    """Derive the alarm threshold from what this voice actually ships."""
    rows = []
    for w in corpus_wavs():
        m = measure(w)
        if m:
            rel = str(w.relative_to(ROOT))
            rows.append((rel, m[0], m[1]))
            print(f"    {rel:<48} sd {m[0]:5.2f}  range {m[1]:5.1f}")
    if not rows:
        print("\n  no VO audio found to calibrate against.")
        return 1
    sds = [r[1] for r in rows]
    rngs = [r[2] for r in rows]
    mean = sum(sds) / len(sds)
    sd = (sum((x - mean) ** 2 for x in sds) / (len(sds) - 1)) ** 0.5 \
        if len(sds) > 1 else 0.0
    # 1.5 SD below our own mean = "unusually flat for us". Never set the floor
    # ABOVE the flattest thing we have already shipped, or history fails
    # retroactively and the alarm is back to firing on everything.
    floor = min(mean - 1.5 * sd, min(sds)) if len(sds) > 1 else min(sds) * 0.9
    # Same treatment for RANGE. Our reads run 6.7-9.8 against a 10.0 floor, so
    # leaving it uncalibrated would just move which line gets ignored daily.
    rmean = sum(rngs) / len(rngs)
    rsd = (sum((x - rmean) ** 2 for x in rngs) / (len(rngs) - 1)) ** 0.5 \
        if len(rngs) > 1 else 0.0
    rfloor = min(rmean - 1.5 * rsd, min(rngs)) if len(rngs) > 1 \
        else min(rngs) * 0.9
    CALIBRATION.write_text(json.dumps({
        "voice_id": "bb79e8390b4340ce8793ea5f123dbba7",
        "n": len(sds), "mean": round(mean, 3), "sd": round(sd, 3),
        "floor": round(floor, 3),
        "range_mean": round(rmean, 3), "range_floor": round(rfloor, 3),
        "samples": {r[0]: round(r[1], 2) for r in rows},
        "_why": "Alarm threshold derived from our own shipped reads. The 3.5 "
                "creator floor is still printed every run; this is what FIRES. "
                "See tools/vo_qc.py header and STYLE-RULES 2026-08-27.",
    }, indent=2) + "\n")
    tag = "  (PROVISIONAL — under 5 samples)" if len(sds) < 5 else ""
    print(f"\n  n={len(sds)}  pitch mean={mean:.2f} -> alarm {floor:.2f}   "
          f"range mean={rmean:.1f} -> alarm {rfloor:.1f}{tag}")
    print(f"  wrote {CALIBRATION.name}\n")
    return 0


FUNCTION = {"the", "a", "an", "of", "to", "in", "is", "it", "and", "or",
            "that", "this", "for", "on", "at", "as", "but", "so", "your",
            "you", "its", "was", "are", "be", "by", "with", "from"}


def f0_track(wav: Path) -> np.ndarray:
    w = wave.open(str(wav))
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    a = a.astype(float) / 32768.0
    win, hop = int(sr * 0.040), int(sr * 0.020)
    lo, hi = int(sr / 300), int(sr / 70)
    out = []
    for i in range(0, len(a) - win, hop):
        x = a[i:i + win]
        if np.sqrt((x ** 2).mean()) < 0.01:
            continue
        x = x - x.mean()
        c = np.correlate(x, x, "full")[win - 1:]
        if c[0] <= 0:
            continue
        seg = c[lo:hi]
        if not len(seg):
            continue
        p = int(np.argmax(seg)) + lo
        if c[p] / c[0] < 0.35:
            continue
        out.append(sr / p)
    return np.array(out)


def stress_inversions(vo_json: Path) -> list[tuple[str, str, float, float]]:
    """Function words held LONGER than the content word next to them."""
    data = json.loads(vo_json.read_text())
    ws = [w for s in data.get("segments", []) for w in s.get("words", [])]
    bad = []
    for i, w in enumerate(ws[:-1]):
        a, b = w, ws[i + 1]
        ta = str(a.get("word", "")).strip().strip(".,!?;:").lower()
        tb = str(b.get("word", "")).strip().strip(".,!?;:").lower()
        da = float(a["end"]) - float(a["start"])
        db = float(b["end"]) - float(b["start"])
        if ta in FUNCTION and tb not in FUNCTION and len(tb) > 3 and da > db * 1.15:
            bad.append((ta, tb, da, db))
    return bad


def main() -> int:
    argv = sys.argv[1:]
    if "--recalibrate" in argv:
        return recalibrate()
    if "--calibration" in argv:
        c = load_calibration()
        print(f"  {c}" if c else "  no calibration — run --recalibrate")
        return 0
    if not argv:
        print(__doc__.split("    python3")[0].strip())
        return 1
    if "--wav" in argv:
        wav = Path(argv[argv.index("--wav") + 1])
        vj = Path(argv[argv.index("--json") + 1]) if "--json" in argv else None
        label = wav.stem
    else:
        slug = argv[0]
        wav = ROOT / f"public/assets/{slug}/vo.wav"
        vj = ROOT / f"public/assets/{slug}/vo.json"
        label = slug
        if not wav.exists():
            print(f"no vo.wav for {slug} — run avatar_handoff prepare first")
            return 1

    f0 = f0_track(wav)
    if len(f0) < 50:
        print("  not enough voiced audio to measure")
        return 1
    st = 12 * np.log2(f0 / np.median(f0))
    st = st[np.abs(st) < 12]
    sd = float(st.std())
    rng = float(np.percentile(st, 95) - np.percentile(st, 5))

    cal = load_calibration()
    alarm = cal["floor"] if cal else PITCH_SD_FLOOR

    print(f"\n=== VO QC — {label} ===\n")
    print(f"  pitch variation   {sd:5.2f} semitones   "
          f"(measured creator band 3.74-6.63)")
    print(f"  pitch range       {rng:5.1f} semitones   "
          f"(references 11.6-17.4)")
    print(f"  median pitch      {np.median(f0):5.0f} Hz")
    if cal:
        prov = " PROVISIONAL," if cal["n"] < 5 else ""
        print(f"  our own baseline  {cal['mean']:5.2f} mean over {cal['n']} "
              f"shipped read(s) —{prov} alarm fires under {alarm:.2f}")
        # The creator gap stays VISIBLE even though it no longer alarms. The
        # voice was chosen deliberately (2026-08-27); that is a decision, not
        # a defect. We still do not get to stop knowing where we sit.
        print(f"  vs creators       {PITCH_SD_FLOOR - sd:+5.2f} to the 3.5 "
              "floor — a settled choice of voice, not a per-reel defect")

    findings = []
    if sd < alarm:
        findings.append(
            f"FLAT FOR US: {sd:.2f} semitones, under this voice's own "
            f"{alarm:.2f} alarm floor derived from "
            f"{cal['n'] if cal else 0} shipped read(s). Not the creator-band "
            "gap — that is a known, chosen difference. This read is flat "
            "even by our own standard, so something went wrong in THIS "
            "generation. Re-generate before spending avatar credits.")
    ralarm = cal["range_floor"] if cal and cal.get("range_floor") \
        else PITCH_RANGE_FLOOR
    if rng < ralarm:
        findings.append(
            f"NARROW RANGE FOR US: {rng:.1f} semitones between this read's "
            f"high and low, under our own {ralarm:.1f}. The reference band is "
            "11.6-17.4 and we have never been near it — this fires because "
            "the read is narrow even by our standard.")

    if vj and vj.exists():
        inv = stress_inversions(vj)
        if len(inv) >= 3:
            ex = "; ".join(f"{a!r} ({da:.2f}s) held longer than {b!r} ({db:.2f}s)"
                           for a, b, da, db in inv[:3])
            findings.append(
                f"STRESS INVERSION x{len(inv)}: function words held longer "
                f"than the content words beside them — {ex}. This is what "
                "'fumbling' sounds like: the reader does not know which word "
                "carries the meaning. Shorten the sentence or move the key "
                "word off a weak beat.")

    print()
    for f in findings:
        print(f"  - {f}\n")
    if not findings:
        print("  the read moves. Nothing to flag.\n")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
