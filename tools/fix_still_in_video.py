#!/usr/bin/env python3
"""Convert a still wired into a video slot (G35) into a `receipt` scene.

WHY
---
`footage` and `floatcard` render an <OffthreadVideo>. ffmpeg decodes a PNG as a
ONE-FRAME video, so the component succeeds at position 0 and fails at every later
position with:

    Compositor error: No frame found at position N ... foo.png

Whether a given scene works depends on which frame is asked for, which is why
these shipped — the reels rendered once and looked fine. It is a
position-dependent hard failure, not a visual defect.

`receipt` renders an <Img>, needs `srcWidth`/`srcHeight`, and does a gentle
ken-burns on a themed backdrop. It is the honest home for a still.

    python3 tools/fix_still_in_video.py            # report every offender
    python3 tools/fix_still_in_video.py --write    # convert them

WHAT IT WILL NOT DO: guess a size. If the file is missing, or Pillow cannot read
it, the scene is reported and LEFT ALONE — a receipt with wrong dimensions
misplaces every highlight drawn on it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STILL_EXT = (".png", ".jpg", ".jpeg", ".webp", ".avif")
VIDEO_SLOTS = ("footage", "floatcard")

# `floatcard` keys that mean nothing to `receipt` and would just be noise.
DROP = {"aspect", "bg", "zoomDir", "from", "mediaAspect"}
# Wider than this and the receipt card leaves a lot of empty frame. Reported,
# not refused: a wide card that RENDERS beats a scene that kills the render.
WIDE = 2.5


def dims(p: Path):
    try:
        from PIL import Image
    except ImportError:
        return None
    if not p.exists():
        return None
    try:
        with Image.open(p) as im:
            return im.width, im.height
    except Exception:  # noqa: BLE001 - unreadable is unreadable
        return None


def main() -> None:
    write = "--write" in sys.argv
    changed_files, converted, skipped, wide = 0, 0, [], []

    for bp in sorted((ROOT / "src/beats").glob("*.json")):
        doc = json.loads(bp.read_text())
        scenes = doc.get("scenes") or []
        touched = False
        for i, sc in enumerate(scenes):
            if sc.get("type") not in VIDEO_SLOTS:
                continue
            src = str(sc.get("src") or "")
            if not src.lower().endswith(STILL_EXT):
                continue
            wh = dims(ROOT / "public" / src)
            if not wh:
                skipped.append(f"{bp.stem} scene {i:02d} — cannot read "
                               f"public/{src}; left as-is")
                continue
            w, h = wh
            ratio = w / h
            note = ""
            if ratio > WIDE:
                wide.append(f"{bp.stem} scene {i:02d} {Path(src).name} "
                            f"{w}x{h} = {ratio:.1f}:1")
                note = "  (wide)"
            print(f"  {bp.stem:20} scene {i:02d}  {sc['type']:10} -> receipt  "
                  f"{Path(src).name[:26]:28} {w}x{h}{note}")
            converted += 1
            touched = True
            if write:
                for k in list(sc):
                    if k in DROP:
                        del sc[k]
                sc["type"] = "receipt"
                sc["srcWidth"] = w
                sc["srcHeight"] = h
                sc.setdefault("backdrop", "cream")
        if touched and write:
            bp.write_text(json.dumps(doc, indent=2) + "\n")
            changed_files += 1

    print()
    if skipped:
        print(f"  {len(skipped)} LEFT ALONE (no reliable size — a receipt with "
              "wrong dimensions misplaces every highlight):")
        for s in skipped:
            print(f"    {s}")
        print()
    if wide:
        print(f"  {len(wide)} are wider than {WIDE}:1 and will leave empty frame "
              "as a receipt.\n  Converted anyway — a wide card that renders beats "
              "a scene that kills the render.\n  Crop them or cut them to mp4 if "
              "the space bothers you:")
        for s in wide:
            print(f"    {s}")
        print()
    print(f"  {converted} scene(s) {'converted' if write else 'to convert'}"
          f"{f' across {changed_files} beat sheet(s)' if write else ''}")
    if not write:
        print("  (--write to apply)")


if __name__ == "__main__":
    main()
