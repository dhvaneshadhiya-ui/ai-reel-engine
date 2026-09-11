#!/usr/bin/env python3
"""Render a YouTube thumbnail from a reel's own frames. 1280x720, free, on-brand.

WHY NOT A GENERATOR
-------------------
Every off-the-shelf thumbnail skill wraps a paid image model and returns an AI
illustration. Our reels are sourced reporting: the strongest possible thumbnail
asset is a REAL FRAME from the reel — the Apple Newsroom card, the spec sheet,
the stat — not an invented picture of the thing. Rendering through Remotion also
means the thumbnail pulls the same theme tokens as the reel, so it cannot drift
off-brand, and it is reproducible and diffable like everything else here.

WHAT THIS DOES
--------------
1. pulls a frame from the finished master (or any -t timestamp)
2. writes it into public/assets/<slug>/ so Remotion can staticFile() it
3. renders src/Thumbnail.tsx as a still, passing the promise text as props
4. can emit BOTH layout variants for the A/B test the brief prescribes

    python3 tools/make_thumbnail.py <slug> --at 55 \
        --lines "Tim Cook's last|keynote is in|three weeks" \
        --accent "last" --kicker "Apple · September"

    python3 tools/make_thumbnail.py <slug> --at 55 --lines "..." --both

THE TEXT IS A PROMISE, NOT THE TITLE. The thumbnail SHOWS, the title TELLS —
repeating the title wastes the only two seconds you get. Keep each line to <= 4
words: at phone size (~120-210px wide) anything longer is a grey smear.
"""

from __future__ import annotations


# ── RETIRED, user directive 2026-08-22 ──────────────────────────────────────
# "Drop making YouTube thumbnails." The pipeline no longer produces them; the
# renderer below is kept intact so the decision is reversible by deleting this
# guard, and the guard exists because a retired step that only lives in prose
# gets un-retired by the next session that never read the prose.
import sys as _sys
if __name__ == "__main__" and "--i-know-its-retired" not in _sys.argv:
    _sys.exit("RETIRED (user directive 2026-08-22): the pipeline no longer "
              "makes YouTube thumbnails.\nSee STYLE-RULES.md. To run anyway "
              "(e.g. the user reversed the call): --i-know-its-retired")


import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_WORDS_PER_LINE = 3


def die(msg: str) -> None:
    sys.exit(f"make_thumbnail: {msg}")


def find_master(slug: str) -> Path | None:
    """The finished render, else the avatar master, else nothing."""
    for cand in (
        ROOT / "out" / f"{slug}.mp4",
        ROOT / "out" / slug / f"{slug}.mp4",
        ROOT / "public/assets" / slug / "avatar-master.mp4",
    ):
        if cand.exists():
            return cand
    return None


def grab_frame(video: Path, at: float, dest: Path) -> None:
    if not shutil.which("ffmpeg"):
        die("ffmpeg not on PATH")
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", str(at), "-i", str(video),
         "-frames:v", "1", str(dest)],
        capture_output=True, text=True,
    )
    if r.returncode != 0 or not dest.exists():
        die(f"could not grab a frame at {at}s from {video}:\n{r.stderr.strip()}")


def render_still(props: dict, out_png: Path, comp: str = "thumbnail") -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["npx", "remotion", "still", "src/index.ts", comp, str(out_png),
         "--props", json.dumps(props)],
        cwd=ROOT, capture_output=True, text=True,
    )
    if r.returncode != 0 or not out_png.exists():
        die(f"remotion still failed:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--line1", required=True, help="white caps line (<=3 words)")
    ap.add_argument("--line2", required=True,
                    help="the payoff, on the accent block (<=3 words)")
    ap.add_argument("--brand", default="",
                    help="subject wordmark at the top, e.g. APPLE")
    ap.add_argument("--block", default="", help="block colour, e.g. '#E8112D'")
    ap.add_argument("--block-text", default="", help="text colour on the block")
    ap.add_argument("--format", default="vertical",
                    choices=["vertical", "wide"], dest="fmt")
    ap.add_argument("--at", type=float, default=None,
                    help="seconds into the master to grab the frame from")
    ap.add_argument("--frame", default=None,
                    help="use this image instead of grabbing one (path under public/)")
    ap.add_argument("--style", default="editorial")
    # The retirement guard at the top of this file reads sys.argv directly, so
    # argparse has to know the flag exists or it rejects it as unrecognized —
    # which made the documented escape hatch impossible to actually use.
    # Found 2026-09-10 the first time anyone tried to reverse the call.
    ap.add_argument("--i-know-its-retired", action="store_true",
                    help="run despite the 2026-08-22 retirement")
    args = ap.parse_args()

    for name, val in (("--line1", args.line1), ("--line2", args.line2)):
        if len(val.split()) > MAX_WORDS_PER_LINE:
            die(f"{name} {val!r} has {len(val.split())} words; max is "
                f"{MAX_WORDS_PER_LINE}. In a grid this is ~200px wide — a "
                f"longer line is a smear. Cut words, never shrink the type.")

    # The reel's asset folder is gitignored, so on a FRESH CLONE it does not
    # exist — and every write below (a grabbed frame, an enlarged PNG, a sized
    # SVG) went there, so the first cover made on another machine crashed with
    # FileNotFoundError. Found 2026-09-11 by cloning from GitHub and running
    # the tool, the day after "everything is pushed" had been said.
    (ROOT / "public" / "assets" / args.slug).mkdir(parents=True, exist_ok=True)

    # frame: supplied, or pulled from the master
    if args.frame:
        frame_rel = args.frame
        if not (ROOT / "public" / frame_rel).exists():
            die(f"no such frame: public/{frame_rel}")
    elif args.at is not None:
        master = find_master(args.slug)
        if master is None:
            die(f"no master found for {args.slug!r} — looked in out/ and "
                f"public/assets/{args.slug}/avatar-master.mp4. "
                f"Pass --frame <path under public/> instead.")
        frame_rel = f"assets/{args.slug}/thumb-frame.png"
        grab_frame(master, args.at, ROOT / "public" / frame_rel)
        print(f"  frame  {master.name} @ {args.at}s -> public/{frame_rel}")
    else:
        frame_rel = ""
        print("  frame  none (solid background)")

    # ENLARGE A SMALL FRAME SO IT FILLS ITS BOX (2026-09-11). Thumbnail.tsx
    # only CAPS the image (maxWidth/maxHeight), which keeps the radius and the
    # shadow on the picture itself but never scales UP — so a tightly cropped
    # subject, which is the correct crop, landed small: a 760px chip sat 760px
    # wide in a 972px box. Enlarging here, to at least the largest box either
    # layout can offer (the full 1080 width x the 1440 3:4 safe area), means the
    # cap always binds and the subject always fills. LANCZOS, and only ever up.
    # AN SVG IS ENLARGED BY SAYING SO, NOT BY RESAMPLING (2026-09-11).
    # get_logo.mjs only ever writes SVG, and PIL cannot open one — so the
    # enlarge step below CRASHED on the official logo that ladder rung 6 fetches.
    # The WhatsApp cover only worked because a throwaway script outside the repo
    # turned the SVG into a PNG first, which meant another machine could not make
    # it. A vector needs no rasteriser: give its root element a width and height
    # big enough for the cap to bind, and the browser draws it at that size, sharp.
    if frame_rel.lower().endswith(".svg"):
        import re
        svg = (ROOT / "public" / frame_rel).read_text()
        vb = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', svg)
        if not vb:
            die(f"{frame_rel} has no viewBox, so its size cannot be derived")
        vw, vh = float(vb.group(1)), float(vb.group(2))
        k = max(1080 / vw, 1440 / vh)
        root = re.search(r"<svg\b[^>]*>", svg).group(0)
        sized = re.sub(r'\s(width|height)="[^"]*"', "", root)
        sized = sized.replace("<svg", f'<svg width="{vw * k:.0f}" height="{vh * k:.0f}"', 1)
        fit_rel = f"assets/{args.slug}/thumb-frame-fit.svg"
        (ROOT / "public" / fit_rel).write_text(svg.replace(root, sized, 1))
        print(f"  frame  vector sized to {vw * k:.0f}x{vh * k:.0f} -> public/{fit_rel}")
        frame_rel = fit_rel
    elif frame_rel:
        from PIL import Image
        src_img = ROOT / "public" / frame_rel
        with Image.open(src_img) as im:
            k = max(1.0, 1080 / im.width, 1440 / im.height)
            if k > 1.0:
                fit_rel = f"assets/{args.slug}/thumb-frame-fit.png"
                im.resize((round(im.width * k), round(im.height * k)),
                          Image.LANCZOS).save(ROOT / "public" / fit_rel)
                print(f"  frame  enlarged x{k:.2f} to fill its box -> public/{fit_rel}")
                frame_rel = fit_rel

    props = {
        "brand": args.brand,
        "frameSrc": frame_rel,
        "line1": args.line1,
        "line2": args.line2,
        "style": args.style,
        "blockColor": args.block,
        "blockText": args.block_text,
        "format": args.fmt,
    }
    outdir = ROOT / "out" / "thumbnails"
    comp = "thumbnail" if args.fmt == "vertical" else "thumbnail-wide"
    out = outdir / f"{args.slug}-{args.fmt}.png"
    render_still(props, out, comp)
    dims = "1080x1920" if args.fmt == "vertical" else "1280x720"
    print(f"  wrote  {out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB, {dims})")

    # The check that matters: a profile grid CENTRE-CROPS a 9:16 cover, so
    # preview exactly that crop. Anything unreadable here is invisible where
    # people actually browse.
    #
    # 3:4, NOT 1:1, since 2026-09-11. Instagram moved its profile grid to 3:4
    # tiles (1080x1440) in January 2025; this preview kept cropping a square,
    # so it showed LESS than viewers see and the cover was judged on the wrong
    # picture. Kept in step with GRID_H in src/Thumbnail.tsx.
    if args.fmt == "vertical" and shutil.which("ffmpeg"):
        grid = outdir / f"{args.slug}-grid.png"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(out),
             "-vf", "crop=1080:1440:0:240,scale=300:400", str(grid)],
            check=False)
        if grid.exists():
            print(f"  wrote  {grid.relative_to(ROOT)}  (centre 3:4 crop — how the "
                  f"Instagram profile grid shows it)")

    print("\nUpload as the Reel cover / Shorts custom thumbnail.")


if __name__ == "__main__":
    main()
