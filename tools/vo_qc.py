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

    print(f"\n=== VO QC — {label} ===\n")
    print(f"  pitch variation   {sd:5.2f} semitones   "
          f"(measured creator band 3.74-6.63, floor {PITCH_SD_FLOOR})")
    print(f"  pitch range       {rng:5.1f} semitones   "
          f"(references 11.6-17.4, floor {PITCH_RANGE_FLOOR})")
    print(f"  median pitch      {np.median(f0):5.0f} Hz")

    findings = []
    if sd < PITCH_SD_FLOOR:
        findings.append(
            f"FLAT READ: {sd:.2f} semitones of pitch movement, under the "
            f"{PITCH_SD_FLOOR} floor taken from the flattest real creator "
            "reference (3.74). This is the 'no energy, no emotion' the user "
            "hears. Raise expressiveness at generation (lower stability, "
            "higher style) — do not fix it in the mix.")
    if rng < PITCH_RANGE_FLOOR:
        findings.append(
            f"NARROW RANGE: {rng:.1f} semitones between the read's high and "
            "low. Even a calm delivery moves more than this.")

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
