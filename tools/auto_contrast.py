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

CAPTIONS TOO, added 2026-08-18. The headline got a measurement in the morning
and the caption — which is on screen for the ENTIRE reel rather than for one
beat — kept its hand-typed `captionTheme`, which nobody ever typed. So
iphone-fold-ultra shipped the word "iPhone," in white, over a white phone on a
white table, at 0:03. Same defect, same fix, one band lower.
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
    cap_changed = 0
    cursor = 0.0
    with tempfile.TemporaryDirectory() as td:
        for i, sc in enumerate(scenes):
            start = cursor
            cursor += sc.get("durationSec", 0)
            hl = sc.get("headline")
            hl = hl if isinstance(hl, dict) else None
            # A caption is burned in for the whole reel, so EVERY media scene
            # needs the caption band sampled — not only the ones carrying a
            # headline, which is all the old loop looked at.
            if hl is None and sc.get("hideCaptions"):
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

            # A STILL HAS NO 0.4s TO SEEK TO (2026-09-02).
            #
            # This seeked 0.4s into every source. On a video that lands mid-shot;
            # on a PNG it seeks past the end of a one-frame stream, ffmpeg exits
            # 0 having written nothing, and the scene was reported as "could not
            # read a frame, skipped". Silently — so a tool built to replace a
            # hand-typed flag with a measurement was blind to every still-image
            # backdrop, which is precisely where the typed flag is most likely
            # to be wrong.
            #
            # Found on claude-fable-5-1, whose HOOK is a split over a still: the
            # one frame the user complained about first was the one frame this
            # never measured.
            is_still = f.suffix.lower() in (
                ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff")
            at = 0.0 if is_still else (
                float(sc.get("from", 0) or 0)
                + min(0.4, sc.get("durationSec", 1) / 2))
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

            def band_luminance(ycen: float, half: float):
                """Mean luminance of a frame band, mapped onto this panel."""
                fy0, fy1 = max(0.0, ycen - half), min(1.0, ycen + half)
                sy0 = min(1.0, max(0.0, (fy0 - y_off) * y_scale))
                sy1 = min(1.0, max(0.0, (fy1 - y_off) * y_scale))
                if sy1 <= sy0:
                    return None
                return luminance(px, int(W * 0.06), int(H * sy0),
                                 int(W * 0.94),
                                 max(int(H * sy1), int(H * sy0) + 2))

            if hl is not None:
                ycen = float(hl.get("y", 0.5))
                lum = band_luminance(ycen, 0.055)
                if lum is None:
                    print(f"  scene {i:02d} — headline sits outside this panel, skipped")
                else:
                    want = "dark" if lum > BRIGHT else "light"
                    have = str(hl.get("theme") or "light")
                    mark = "  " if want == have else "->"
                    near = (" (borderline — the scrim is carrying it)"
                            if abs(lum - BRIGHT) < UNSURE else "")
                    print(f"  {mark} scene {i:02d} {kind:8} headline y={ycen:.2f}  "
                          f"luminance {lum:.2f}  ink should be {want.upper():5} "
                          f"(sheet says {have}){near}")
                    if want != have:
                        changed += 1
                        if write:
                            if want == "dark":
                                hl["theme"] = "dark"
                            else:
                                hl.pop("theme", None)

            # --- the caption band ---------------------------------------------
            # Captions sit on ONE line for the whole reel now (bottom 500 of
            # 1920, y 0.74 at the baseline), so the band is fixed rather than
            # per-scene. A scene that raises its caption to clear a face gets
            # sampled where it actually lands.
            if not sc.get("hideCaptions"):
                cb = sc.get("captionBottom")
                cb = 500 if cb is None else max(int(cb), 500)
                cap_y = 1.0 - (cb + 60) / 1920.0   # 60px up: the ink, not the baseline
                clum = band_luminance(cap_y, 0.045)
                if clum is not None:
                    cwant = "dark" if clum > BRIGHT else "light"
                    chave = str(sc.get("captionTheme") or "light")
                    cmark = "  " if cwant == chave else "->"
                    print(f"  {cmark} scene {i:02d} {kind:8} caption  y={cap_y:.2f}  "
                          f"luminance {clum:.2f}  ink should be {cwant.upper():5} "
                          f"(sheet says {chave})")
                    if cwant != chave:
                        cap_changed += 1
                        if write:
                            if cwant == "dark":
                                sc["captionTheme"] = "dark"
                            else:
                                sc.pop("captionTheme", None)

    if write and (changed or cap_changed):
        bp.write_text(json.dumps(doc, indent=2) + "\n")
        print(f"\n  set `theme` on {changed} headline(s) and `captionTheme` on "
              f"{cap_changed} scene(s) from the pixels")
    else:
        print(f"\n  {changed} headline(s) and {cap_changed} caption(s) disagree "
              "with the footage"
              + ("" if not (changed or cap_changed) else "  (--write to fix)"))

    # --check MAKES THIS A LINT (2026-09-02, RULES.md's middle category).
    #
    # Report mode is right about one thing and wrong about the consequence.
    # Right: silently rewriting a sheet the user approved under G27 during a
    # render is an edit, not a measurement, and it should never happen. Wrong:
    # that is an argument against WRITING, not against REFUSING. A measurement
    # nobody has to act on is a measurement nobody acts on — 30 headline and
    # caption ink choices across this repo disagree with the pixels behind
    # them, against 58 that agree, and every one of them shipped.
    #
    # claude-fable-5-1's hook is the case that matters: light ink measured
    # against luminance 0.98, near-white. That forced the legibility scrim to
    # 46% black over a white document, which is the grey band across the first
    # frame of the reel. Fix the ink and the band has nothing to do.
    if "--check" in sys.argv and (changed or cap_changed):
        sys.exit(
            f"\n  INK DISAGREES WITH THE PIXELS — {changed} headline(s), "
            f"{cap_changed} caption(s).\n"
            "  Light type on a bright frame is illegible on a phone on mute, "
            "and it drags\n  a heavy scrim in behind it to compensate. Fix "
            "`theme` / `captionTheme` on the\n  sheet, or re-run with --write "
            "and re-approve. This refuses; it does not edit.\n")


if __name__ == "__main__":
    main()
