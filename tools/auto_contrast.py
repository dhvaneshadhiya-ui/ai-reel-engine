#!/usr/bin/env python3
"""Choose headline ink from the PIXELS behind it, not from a typed flag.

WHY
---
`headline.theme` is hand-typed. Someone writes "dark" meaning dark ink, and
nothing ever checks it against the footage. On the airpods hook that produced
black type over a bright window — and, because the scrim used to be gated on the
same flag, no scrim and no shadow either.

Every other guess in this pipeline has been replaced by a measurement:

    music ducking   <- whisper word timings, not five clock times
    sfx gain        <- the file's measured peak, not a flat 0.14
    status crop     <- the measured Dynamic Island, not a 5.5% guess
    covers          <- the phrase the shot was planned from

This is the same move for contrast. Sample the frame the headline will sit on,
measure its luminance, and pick the ink that survives it.

    python3 tools/auto_contrast.py <slug>            # report
    python3 tools/auto_contrast.py <slug> --write    # set `theme` from the pixels

HANDLES `footage` and `split`, which is where headlines actually live. Anything
else is reported and skipped rather than guessed at — a wrong sample is worse
than no sample, because it looks authoritative.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAME_W, FRAME_H = 1080, 1920
# Above this mean luminance the background is "bright" and wants dark ink.
BRIGHT = 0.55
# Inside this margin either way, neither ink is comfortable and the scrim is
# doing all the work — worth saying rather than silently picking one.
UNSURE = 0.08


def luminance(px, x0, y0, x1, y1, step=4) -> float:
    tot = n = 0
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            r, g, b = px[x, y][:3]
            tot += 0.2126 * r + 0.7152 * g + 0.0722 * b
            n += 1
    return (tot / n / 255) if n else 0.5


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug = args[0]
    write = "--write" in sys.argv
    try:
        from PIL import Image
    except ImportError:
        sys.exit("needs Pillow")

    bp = ROOT / f"src/beats/{slug}.json"
    if not bp.exists():
        sys.exit(f"no beat sheet at {bp}")
    doc = json.loads(bp.read_text())
    scenes = doc.get("scenes", [])

    changed = 0
    cursor = 0.0
    with tempfile.TemporaryDirectory() as td:
        for i, sc in enumerate(scenes):
            start = cursor
            cursor += sc.get("durationSec", 0)
            hl = sc.get("headline")
            if not isinstance(hl, dict):
                continue

            kind = sc.get("type")
            # Which media is under the type, and how the frame maps onto it.
            if kind == "footage":
                src, y_scale, y_off = sc.get("src"), 1.0, 0.0
            elif kind == "split":
                # top panel fills the upper half, so frame-y 0..0.5 -> source 0..1
                src, y_scale, y_off = sc.get("topSrc"), 2.0, 0.0
            else:
                print(f"  scene {i:02d} ({kind}) — not footage/split, skipped "
                      "rather than guessed")
                continue
            if not src:
                continue
            f = ROOT / "public" / str(src)
            if not f.exists():
                print(f"  scene {i:02d} — media missing on disk, skipped")
                continue

            at = float(sc.get("from", 0)) + min(0.4, sc.get("durationSec", 1) / 2)
            shot = Path(td) / f"{i}.png"
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(at),
                                "-i", str(f), "-frames:v", "1", str(shot)],
                               capture_output=True, text=True)
            if r.returncode != 0 or not shot.exists():
                print(f"  scene {i:02d} — could not read a frame, skipped")
                continue

            im = Image.open(shot).convert("RGB")
            W, H = im.size
            px = im.load()

            # the band the headline occupies, in FRAME fractions, mapped to source
            ycen = float(hl.get("y", 0.5))
            half = 0.055
            fy0, fy1 = max(0.0, ycen - half), min(1.0, ycen + half)
            sy0 = min(1.0, max(0.0, (fy0 - y_off) * y_scale))
            sy1 = min(1.0, max(0.0, (fy1 - y_off) * y_scale))
            if sy1 <= sy0:
                print(f"  scene {i:02d} — headline sits outside this panel, skipped")
                continue
            lum = luminance(px, int(W * 0.06), int(H * sy0),
                            int(W * 0.94), max(int(H * sy1), int(H * sy0) + 2))

            want = "dark" if lum > BRIGHT else "light"
            have = str(hl.get("theme") or "light")
            mark = "  " if want == have else "->"
            near = " (borderline — the scrim is carrying it)" if abs(lum - BRIGHT) < UNSURE else ""
            print(f"  {mark} scene {i:02d} {kind:8} y={ycen:.2f}  "
                  f"luminance {lum:.2f}  ink should be {want.upper():5} "
                  f"(sheet says {have}){near}")
            if want != have:
                changed += 1
                if write:
                    if want == "dark":
                        hl["theme"] = "dark"
                    else:
                        hl.pop("theme", None)

    if write and changed:
        bp.write_text(json.dumps(doc, indent=2) + "\n")
        print(f"\n  set `theme` on {changed} headline(s) from the pixels")
    else:
        print(f"\n  {changed} headline(s) disagree with the footage"
              + ("" if not changed else "  (--write to fix)"))


if __name__ == "__main__":
    main()
