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
TERM = Path(__file__).resolve().parent / "terminal_page.py"

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


RENDER_SRC = {
    "Reel.tsx": Path(__file__).resolve().parent.parent / "src/Reel.tsx",
    "ReceiptScene.tsx": Path(__file__).resolve().parent.parent
                        / "src/components/ReceiptScene.tsx",
    "CaptionChips.tsx": Path(__file__).resolve().parent.parent
                        / "src/components/CaptionChips.tsx",
    "OssAlt.tsx": Path(__file__).resolve().parent.parent
                  / "src/components/OssAlt.tsx",
    "FootageScene.tsx": Path(__file__).resolve().parent.parent
                        / "src/components/FootageScene.tsx",
}

# The three treatments measured off the user's reference shorts on 2026-08-25.
# Each is a NUMBER taken from a real frame, so each can silently drift back to
# taste in a later edit — which is precisely what a check is for.
REF_CHECKS: list[tuple[str, str, str, str]] = [
    # IDLE MOTION (2026-09-01). 26 of 30 card components animate in and then
    # hold still, against `going-viral`'s "nothing static" rule. One wrapper at
    # the SceneSwitch dispatch point fixes all of them — and nothing failed if
    # it were deleted, which is the same unguarded shape as the 4% receipt push
    # it was written alongside.
    ("Reel.tsx", "card scenes are wrapped in idle motion",
     r"IdleMotion",
     "without the wrapper every card component animates in and then freezes "
     "for the rest of the beat"),
    ("Reel.tsx", "self-moving scene types are excluded from idle motion",
     r"MOVES_ITSELF[\s\S]{0,200}\"footage\"[\s\S]{0,120}\"receipt\"",
     "stacking idle motion on FootageScene's 1.1x push or ReceiptScene's "
     "focus pull fights the move the scene already makes"),
    # MOTION DEFAULTS ARE RULES TOO (2026-09-01). A receipt with no
    # `highlights` falls back to a ken-burns push, and 57% of receipts across
    # the reels have none — so this constant IS the treatment for most
    # screenshots, not an edge case. It sat at 4% (0.02 -> 0.06) and read as a
    # still on a page held 6-9s.
    ("ReceiptScene.tsx", "receipt fallback push is visible, not a 4% nudge",
     r"\[0\.0, 0\.1\]",
     "a full-page screenshot held 6-9s at a 4% push reads as a still; this is "
     "matched to FootageScene's 1.1x house push, not a new invented number"),
    ("FootageScene.tsx", "footage still pushes 1.1x (what receipt is matched to)",
     r"base \* 1\.1",
     "if the footage push changes, ReceiptScene's fallback must be re-matched "
     "or the two silently drift apart"),
    ("CaptionChips.tsx", "captions sit on a translucent plate",
     r"background: PLATE",
     "reference vIAH9SaCNvo sets its caption on a translucent dark plate; "
     "without a ground the type needs a heavy contour and still loses "
     "against busy footage"),
    ("CaptionChips.tsx", "caption type is the tuned 0.78 of the role",
     r"SIZE\.caption \* 0\.78",
     "the reference measures a 60px cap height at 1080 wide; ours ran 78 "
     "with a 1.3x emphasis step, so every accent word beat its whole line"),
    ("CaptionChips.tsx", "emphasis is a small step, not a size jump",
     r"0\.78 \* 1\.12",
     "the reference carries emphasis on COLOUR at a uniform size"),
    ("OssAlt.tsx", "CTA keyword is the measured neon",
     r"rgb\(226,254,14\)",
     "sampled from fR8AkVkuM18's final frames"),
    ("OssAlt.tsx", "CTA keyword is the measured size",
     r"fontSize: 207",
     "cap height 150px at 1080x1920 in the reference"),
    ("FootageScene.tsx", "oversized footage can travel instead of cropping",
     r'slide === "left"',
     "a static cover-crop throws most of an oversized asset away; the "
     "reference travels across it"),
]


TERM_CHECKS: list[tuple[str, str, str]] = [
    ("generated pages declare a viewport",
     r'<meta name="viewport" content="width=device-width',
     "without it mobile Chromium lays the page out at 980px and scales it "
     "down — a 94%-wide terminal rendered at a third of the frame and the "
     "recreation looked tiny (2026-08-25)"),
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
    term = TERM.read_text() if TERM.exists() else ""
    for label, pattern, why in TERM_CHECKS:
        if re.search(pattern, term):
            print(f"  ok   {label}")
        else:
            failed = True
            print(f"  FAIL {label}\n       {why}")
    for fname, label, pattern, why in REF_CHECKS:
        path = RENDER_SRC[fname]
        text = path.read_text() if path.exists() else ""
        if re.search(pattern, text):
            print(f"  ok   {label}")
        else:
            failed = True
            print(f"  FAIL {label} ({fname})\n       {why}")
    print(f"\n{len(CHECKS) + len(TERM_CHECKS) + len(REF_CHECKS)} defaults checked — "
          f"{'all hold' if not failed else 'A DEFAULT CHANGED'}.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
