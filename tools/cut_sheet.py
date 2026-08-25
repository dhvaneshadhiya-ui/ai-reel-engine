#!/usr/bin/env python3
"""Print a reel's CUT — every beat with its duration and its motion.

The gates answer "is this broken?". This answers "is this edited?", which is
a different question and the one nobody was asking: a sheet where sixteen
beats all carry `zoomDir: "in"` passes every gate in the repo and still
watches like a slideshow. That was claude-eating-tokens on 2026-08-25 until
someone read the cut instead of the gate output.

It computes nothing you could not read out of the JSON — the point is that
it puts duration and motion side by side, in order, so the RHYTHM is visible.
The five questions to ask of it are in AGENT.md §3b (the editor's pass).

    python3 tools/cut_sheet.py <slug>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOTION_KEYS = ("zoomDir", "zoom", "slide", "slideSpan", "focusX", "focusY",
               "from")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: cut_sheet.py <slug>")
        return 1
    slug = sys.argv[1]
    path = ROOT / f"src/beats/{slug}.json"
    if not path.exists():
        print(f"no beat sheet at {path} — compile first")
        return 1
    beats = json.loads(path.read_text())
    scenes = beats.get("scenes", [])
    caps = beats.get("captions", [])

    def line_at(start: float, end: float) -> str:
        words = [c.get("text", "") for c in caps
                 if float(c.get("end", 0)) > start
                 and float(c.get("start", 0)) < end]
        return " ".join(words)[:60]

    print(f"\n=== CUT — {slug} ({len(scenes)} beats, "
          f"{sum(s['durationSec'] for s in scenes):.1f}s) ===\n")
    print(f"{'#':>3} {'in':>6} {'dur':>6}  {'type':<13} {'motion':<38} line")
    cursor = 0.0
    prev_motion = None
    flags: list[str] = []
    for i, sc in enumerate(scenes):
        dur = float(sc["durationSec"])
        motion = " ".join(f"{k}={sc[k]}" for k in MOTION_KEYS if k in sc)
        mark = ""
        # adjacent beats that move identically read as one shot with a glitch
        if motion and motion == prev_motion:
            mark = "  <- same move as the beat before"
            flags.append(f"beats {i-1:02d}/{i:02d} carry identical motion")
        print(f"{i:3} {cursor:6.1f} {dur:6.2f}  {sc['type']:<13} "
              f"{(motion or '(none declared)'):<38} {line_at(cursor, cursor+dur)}{mark}")
        prev_motion = motion
        cursor += dur

    durs = [float(s["durationSec"]) for s in scenes]
    longest = max(durs)
    at = sum(durs[:durs.index(longest)])
    print(f"\n  longest beat {longest:.2f}s at {at:.1f}s "
          f"| mean {sum(durs)/len(durs):.2f}s | median "
          f"{sorted(durs)[len(durs)//2]:.2f}s")
    if at > sum(durs) * 0.5 and longest > 5:
        flags.append(f"the longest beat ({longest:.1f}s) sits in the second "
                     f"half, at {at:.0f}s — where attention is thinnest")
    still = [i for i, s in enumerate(scenes)
             if s.get("zoomDir") == "none" and "slide" not in s
             and "zoom" not in s]
    if still:
        flags.append(f"beats {still} declare no movement at all")
    print()
    for f in flags:
        print(f"  ASK: {f}")
    print("\n  AGENT.md §3b has the five questions. None of these is a rule —")
    print("  they are the places an edit usually needs a decision.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
