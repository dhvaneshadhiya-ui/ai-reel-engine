#!/usr/bin/env python3
"""Land the sound effect on the frame the picture lands.

WHY
---
Asked 2026-08-18: "how about adding the similar effects to the text (headlines)
similar to sound effects when they are in the video."

Measured on iphone-fold-ultra before building anything:

    8 SFX cues   6 scenes with headlines   1 scene carries both
    that one scene: whoosh at 0.00s, headline lands at 0.15 / 0.45 / 0.85

So not a single sound in the reel fired on a picture event. That is why the
effects read as background texture rather than as production — a whoosh over
nothing is a noise, and the identical whoosh on the frame a claim arrives is an
accent the viewer cannot explain but can feel.

src/theme/impact.ts gives text a transient envelope. This closes the other half:
it moves each SFX cue onto the nearest headline landing, and reports the cues
that have no picture event to attach to.

    python3 tools/sync_impacts.py <slug>            # what is out of sync
    python3 tools/sync_impacts.py <slug> --write    # move the cues

WHAT IT WILL NOT DO
-------------------
It never ADDS a sound. Choosing that a beat wants a shutter rather than a pop is
taste, and the tool has no way to be right about it — it would just distribute
noise evenly and call that craft. It only aligns cues that somebody already
decided to place. Cues with no headline within the window are listed so the
choice stays a person's.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# How far a cue may be moved to meet a line. Beyond this the cue is not a
# mistimed accent, it is punctuating something else — a cut, a reveal, a card —
# and dragging it onto the headline would break whatever it was actually for.
WINDOW = 0.55


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug, write = args[0], "--write" in sys.argv

    bp = ROOT / f"src/beats/{slug}.json"
    if not bp.exists():
        sys.exit(f"no beat sheet at {bp}")
    doc = json.loads(bp.read_text())
    scenes = doc.get("scenes", [])

    moved = orphan = paired = 0
    hl_no_sfx: list[int] = []

    for i, sc in enumerate(scenes):
        cues = sc.get("sfx") or []
        hl = sc.get("headline")
        lines = hl.get("lines", []) if isinstance(hl, dict) else []
        lands = sorted({round(float(l["at"]), 3) for l in lines if "at" in l})

        if lands and not cues:
            hl_no_sfx.append(i)
        if not cues:
            continue
        if not lands:
            for c in cues:
                print(f"     scene {i:02d} {Path(c['src']).name:22} at "
                      f"{float(c.get('at', 0)):.2f}s — no headline in this scene, "
                      f"left alone")
                orphan += 1
            continue

        # any cue with no line to meet becomes a standalone impact, so the
        # picture still acknowledges a sound the viewer definitely hears
        extra: list[float] = []
        for c in cues:
            at = float(c.get("at", 0))
            near = min(lands, key=lambda L: abs(L - at))
            delta = near - at
            if abs(delta) > WINDOW:
                print(f"     scene {i:02d} {Path(c['src']).name:22} at {at:.2f}s "
                      f"— nearest landing {near:.2f}s is {abs(delta):.2f}s away "
                      f"(> {WINDOW}); punctuating something else, left alone")
                extra.append(at)
                orphan += 1
                continue
            if abs(delta) < 0.017:            # already inside one frame
                paired += 1
                continue
            print(f"  -> scene {i:02d} {Path(c['src']).name:22} {at:.2f}s "
                  f"-> {near:.2f}s  (moves {abs(delta) * 1000:.0f}ms onto the "
                  f"{'first' if near == lands[0] else 'landing of a'} line)")
            moved += 1
            if write:
                c["at"] = near
            paired += 1

        if write and extra and isinstance(hl, dict):
            hl["impacts"] = sorted(set(extra))

    if hl_no_sfx:
        print(f"\n  {len(hl_no_sfx)} scene(s) land a headline with NO sound at "
              f"all: {hl_no_sfx}")
        print("  Not fixed here — picking WHICH effect a beat wants is taste, "
              "and a tool\n  that spreads noise evenly would be making that "
              "choice badly. The text\n  still gets its own visual transient "
              "(src/theme/impact.ts).")

    print(f"\n  {paired} cue(s) now land with a line, {moved} moved, "
          f"{orphan} left where they were")
    if write and moved:
        bp.write_text(json.dumps(doc, indent=2) + "\n")
        print(f"  wrote {bp.name}")
    elif moved:
        print("  (--write to apply)")


if __name__ == "__main__":
    main()
