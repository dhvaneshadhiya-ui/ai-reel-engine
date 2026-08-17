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
    args = ap.parse_args()

    for name, val in (("--line1", args.line1), ("--line2", args.line2)):
        if len(val.split()) > MAX_WORDS_PER_LINE:
            die(f"{name} {val!r} has {len(val.split())} words; max is "
                f"{MAX_WORDS_PER_LINE}. In a grid this is ~200px wide — a "
                f"longer line is a smear. Cut words, never shrink the type.")

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
    # preview the centre square. Anything unreadable here is invisible where
    # people actually browse.
    if args.fmt == "vertical" and shutil.which("ffmpeg"):
        grid = outdir / f"{args.slug}-grid.png"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(out),
             "-vf", "crop=1080:1080:0:420,scale=400:400", str(grid)],
            check=False)
        if grid.exists():
            print(f"  wrote  {grid.relative_to(ROOT)}  (centre 1:1 crop — how the "
                  f"profile grid shows it)")

    print("\nUpload as the Reel cover / Shorts custom thumbnail.")


if __name__ == "__main__":
    main()
