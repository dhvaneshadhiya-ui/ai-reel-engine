#!/usr/bin/env python3
"""Measure how much of a focused screenshot region falls OUTSIDE the frame.

WHY THIS EXISTS
---------------
Published reels were cutting captured article text off BOTH edges — viewers on
Instagram and YouTube could not read the left or right of the source we were
pointing at. The video is a correct 1080x1920, so nothing was cropping it; the
crop was baked in by the renderer.

Cause: `AnnotateZoom` and `ReceiptScene` both compute `fit`, the zoom at which
the padded focus region fits the frame, and then override it with a MINIMUM zoom
(1.15 and 1.35). When the focus is nearly as wide as the capture, `fit` lands
BELOW 1.0 — the camera needs to pull back — and the floor forces it to push in
instead. The focused text is then wider than the frame and is sliced
symmetrically.

This replicates each component's zoom arithmetic in isolation and reports the
overflow in SOURCE pixels per side, so the damage is a number instead of an
impression.

    python3 tools/check_safe_area.py              # every beats file
    python3 tools/check_safe_area.py ios27-tiers  # one

Exit 1 if any scene overflows. Keep it that way: this is the check, and a check
that cannot fail is not a check.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEATS = ROOT / "src/beats"

# Frame is authoritative; beats files carry it but default to the house format.
DEF_W, DEF_H = 1080, 1920

# Mirrors AnnotateZoom.tsx / ReceiptScene.tsx. If either component changes its
# geometry, change it here in the same commit — a drifted model measures nothing.
GEOM = {
    # component      cardFrac  fitW   fitH   minZ   maxZ  pad  push
    "annotatezoom": (0.90, 0.86, 0.58, 1.15, 2.40, 46, 0.05),
    "receipt":      (0.86, 0.88, 0.55, 1.35, 2.20, 40, 0.06),
}

# Allow a hair of bleed: a rounded card corner may clip a pixel of background
# without touching a glyph. Beyond this a character is being eaten.
TOL_SRC_PX = 2.0


# Mirrors src/safeArea.ts. Keep the two in step; a drifted copy measures nothing.
SAFE_W = 0.96


def overflow(kind: str, src_w: int, src_h: int,
             fx: float, fy: float, fw: float, fh: float,
             frame_w: int, legacy: bool = False) -> tuple[float, float, float]:
    """(per-side overflow in SOURCE px, chosen zoom, the zoom that would fit).

    `legacy=True` models the PRE-FIX arithmetic, where the aesthetic minimum
    zoom overrode the fit. It exists as a positive control: this tool must still
    be able to detect the bug it was written for, or a green run proves nothing.
    """
    card_frac, fit_w, fit_h, min_z, max_z, pad, push = GEOM[kind]

    card_w = frame_w * card_frac
    card_h = (src_h / src_w) * card_w
    s = card_w / src_w                     # source px -> card px

    uw = (fw + 2 * pad) * s                # padded focus, card px
    uh = (fh + 2 * pad) * s

    fit = min((card_w * fit_w) / uw, (card_h * fit_h) / uh)

    # The zoom at which the padded focus exactly spans the frame's safe width.
    z_fits = (frame_w * SAFE_W) / uw

    floored = max(min_z, min(max_z, fit))
    if legacy:
        # PRE-FIX: floor wins, nothing caps it, push-in added on top.
        z = floored + push
    else:
        # FIXED: the ceiling beats the floor, and is re-applied AFTER the
        # push-in — a ceiling applied before the push-in is not a ceiling.
        z = min(min(floored, z_fits) + push, z_fits)

    on_screen = uw * z
    over_total = max(0.0, on_screen - frame_w)
    per_side_src = (over_total / 2) / (s * z) if z else 0.0
    return per_side_src, z, z_fits


def scenes_of(doc: dict) -> list[dict]:
    return doc.get("scenes", []) if isinstance(doc, dict) else doc


def check(path: Path, legacy: bool = False) -> list[str]:
    doc = json.loads(path.read_text())
    frame_w = int(doc.get("width", DEF_W))
    bad: list[str] = []
    rows: list[tuple] = []

    for i, sc in enumerate(scenes_of(doc)):
        kind = sc.get("kind") or sc.get("type")
        if kind not in GEOM:
            continue
        sw, sh = sc.get("srcWidth"), sc.get("srcHeight")
        if not sw or not sh:
            continue

        # focus: explicit, else union of highlights/annotations, else whole page
        f = sc.get("focus")
        if isinstance(f, dict) and {"x", "y", "w", "h"} <= set(f):
            fx, fy, fw, fh = f["x"], f["y"], f["w"], f["h"]
        else:
            marks = sc.get("annotations") or sc.get("highlights") or []
            marks = [m for m in marks if all(k in m for k in ("x", "y", "w", "h"))]
            if marks:
                x0 = min(m["x"] for m in marks)
                y0 = min(m["y"] for m in marks)
                fx, fy = x0, y0
                fw = max(m["x"] + m["w"] for m in marks) - x0
                fh = max(m["y"] + m["h"] for m in marks) - y0
            else:
                # no focus and no marks: the component shows the page unzoomed,
                # which is the one safe case. Nothing to check.
                continue

        per_side, z, z_fits = overflow(kind, sw, sh, fx, fy, fw, fh,
                                       frame_w, legacy)
        rows.append((i, kind, sw, fw, per_side, z, z_fits))
        if per_side > TOL_SRC_PX:
            bad.append(
                f"  scene {i:2} {kind:13} focus w={fw:>5} of src {sw}  "
                f"CUT {per_side:5.0f} src px per side   "
                f"zoom {z:.2f} but only {z_fits:.2f} fits")

    if rows:
        worst = max(r[4] for r in rows)
        print(f"{path.name}: {len(rows)} focused scene(s), "
              f"{len(bad)} overflowing, worst {worst:.0f} src px per side")
        for line in bad:
            print(line)
    return bad


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--legacy"]
    legacy = "--legacy" in sys.argv[1:]
    files = ([BEATS / f"{a}.json" for a in args] if args
             else sorted(BEATS.glob("*.json")))
    files = [f for f in files if f.exists()]
    if not files:
        sys.exit("no beats files found")

    if legacy:
        print("MODELLING THE PRE-FIX RENDERER (positive control)\n")

    total = 0
    for f in files:
        total += len(check(f, legacy))
    print()
    if total:
        sys.exit(f"{total} scene(s) cut the focused text off the frame edge.")
    print("all focused scenes keep their focus region inside the frame.")
    if not legacy:
        print("Positive control: `--legacy` must FAIL here. If it passes, this "
              "tool has stopped being able to see the bug.")


if __name__ == "__main__":
    main()
