#!/usr/bin/env python3
"""Assert capture.mjs's CAPTURE CONTRACT — the defaults reels depend on.

Every one of these is a rule the engine states somewhere as prose and then
relies on capture.mjs to honour silently. Prose rots: on 2026-08-25 the
recorder was emulating mobile with a zoomed viewport (media queries saw
1080px, so GitHub served its DESKTOP breakpoint squeezed into 360 CSS px)
and its frame grab ignored deviceScaleFactor entirely — files logged as
"1080x2340" were really 360x780. Both had shipped a whole scout session.
Neither could have survived a check that looked at the code.

Run by doctor. Adding a default here is cheaper than re-scouting a reel.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "capture.mjs"

CHECKS: list[tuple[str, str, str]] = [
    # (label, regex that MUST match, why it matters)
    ("cursor is ON by default",
     r'const showCursor = !flags\["no-cursor"\]',
     "the ai-tools evidence grammar is a live cursor (formats/ai-tools.md); "
     "an opt-IN cursor means every recording quietly ships without one"),
    ("--no-cursor is a boolean flag",
     r'boolFlags = new Set\(\[[^\]]*"no-cursor"',
     "a value-taking --no-cursor swallows the NEXT flag: it ate --tier and "
     "four recordings failed silently (2026-08-25)"),
    ("mobile is the default",
     r"const MOBILE = !flags\.desktop",
     "RULE 2 — sources are scouted on mobile view first"),
    ("record() uses a REAL viewport, never a zoom trick",
     r"viewport: \{ width: opts\.width, height: opts\.height \},\s*"
     r"deviceScaleFactor: S,",
     "a width*scale viewport + CSS zoom makes responsive sites serve their "
     "desktop breakpoint into a phone-width frame"),
    ("frames are captured at device scale",
     r'page\.screenshot\(\{[^}]*scale: "device"',
     "raw CDP Page.captureScreenshot ignores deviceScaleFactor and writes "
     "CSS-pixel frames — 360x780 files labelled 1080x2340"),
    ("physical dimensions are forced even",
     r"if \(\(opts\[dim\] \* S\) % 2 !== 0\)",
     "VP9 accepts odd sizes and h264 refuses them, so the failure lands at "
     "the mp4 conform, one step from its cause"),
]


def run() -> int:
    if not SRC.exists():
        print(f"  FAIL capture.mjs not found at {SRC}")
        return 1
    src = SRC.read_text()
    failed = False
    for label, pattern, why in CHECKS:
        if re.search(pattern, src):
            print(f"  ok   {label}")
        else:
            failed = True
            print(f"  FAIL {label}\n       {why}")
    print(f"\n{len(CHECKS)} capture defaults checked — "
          f"{'all hold' if not failed else 'A DEFAULT CHANGED'}.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
