#!/usr/bin/env python3
"""Render a reel's cover — 1080x1920, plus the 3:4 grid tile — from its own sourced assets.

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

    python3 tools/make_thumbnail.py <slug> --frame assets/<slug>/thumb-x.png \
        --line1 "Chip prices up" --line2 "DOUBLE DIGITS"   # records cover.json
    python3 tools/make_thumbnail.py <slug>                 # re-render from it
    python3 tools/make_thumbnail.py <slug> --check         # prepublish uses this
    python3 tools/make_thumbnail.py --selftest

THE TEXT IS A PROMISE, NOT THE TITLE. The thumbnail SHOWS, the title TELLS —
repeating the title wastes the only two seconds you get. Keep each line to <= 4
words: at phone size (~120-210px wide) anything longer is a grey smear.
"""

from __future__ import annotations


# ── A STANDARD STEP AGAIN — user directive 2026-09-11 ───────────────────────
# Retired 2026-08-22 ("drop making YouTube thumbnails") and skipped by default
# from 2026-08-24; reinstated for EVERY reel on 2026-09-11, with no presenter
# face for now. The guard that refused to run is gone. What replaced it is the
# set of checks below, so the step cannot quietly produce a bad cover either.


import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_WORDS_PER_LINE = 3
# Characters, not words, are what wrap. Measured on the 104px heavy-caps
# headline: 14-character lines ("AI AGENT CHATS", "CHIP PRICES UP") sit on one
# line; 17 ("SNAPDRAGON PRICES", "DOUBLE-DIGIT HIKE") wrap to two.
# ponytail: a character budget, not a measurement of the glyphs — a line of
# W's could still wrap. Upgrade path: @remotion/layout-utils fitText.
MAX_CHARS_PER_LINE = 14
# Share of the 3:4 tile that stands out (>= 3:1) from YouTube's dark theme.
# Our cover ground measures 1.05:1 against it, so in dark mode ONLY the subject
# and the text are visible. Measured 2026-09-11: text alone 6.8%, the thinnest
# real subject shipped (WhatsApp's green ring) 23.9%, the chip 64.3%. Under
# 12% the subject has effectively vanished — a black iPhone on our ground.
FEED_DARK = (15, 15, 15)
STANDOUT_MIN = 0.12

_UNITS = ("zero one two three four five six seven eight nine ten eleven twelve "
          "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()


def _spelled(n: int) -> str | None:
    """Regex for how a script spells n (scripts write numbers as words for TTS)."""
    if n < 20:
        return _UNITS[n]
    if n < 100:
        t, u = divmod(n, 10)
        return _TENS[t - 2] + (f"[- ]{_UNITS[u]}" if u else "")
    return None


def unsourced_in(texts: list, corpus: str) -> list[str]:
    """Numbers on the cover that appear nowhere in the script or the ledger."""
    flat = corpus.lower().replace(",", "")
    bad = []
    for t in texts:
        for m in re.findall(r"\d[\d,.]*", t or ""):
            raw = m.rstrip(".,")
            d = raw.replace(",", "")
            if re.search(rf"(?<![\d.]){re.escape(d)}(?!\d)", flat):
                continue
            w = _spelled(int(d)) if d.isdigit() else None
            if w and re.search(rf"\b{w}\b", flat):
                continue
            bad.append(raw)
    return bad


def unsourced_numbers(slug: str, texts: list) -> list[str]:
    """A number on a cover is a claim with no room for its source, so it must
    already be in this reel's approved script or its claims ledger. RIGHTS-class:
    "numbers carry their source" is one of the two things besides the three
    rules that this repo lets block."""
    corpus = "".join((ROOT / "jobs" / slug / f).read_text() + "\n"
                     for f in ("script.md", "research.md")
                     if (ROOT / "jobs" / slug / f).exists())
    return unsourced_in(texts, corpus)


def not_claimed(slug: str) -> list[str]:
    """What the reel explicitly does NOT claim — shown while the words are chosen."""
    out = []
    r = ROOT / "jobs" / slug / "research.md"
    if r.exists():
        m = re.search(r"^## NOT CLAIMED\s*\n(.*?)(?=^## |\Z)", r.read_text(), re.M | re.S)
        if m:
            out += [l.strip().lstrip("-").strip() for l in m.group(1).splitlines()
                    if l.strip().startswith("-")]
    mf = ROOT / "public" / "assets" / slug / "manifest.json"
    if mf.exists():
        try:
            out += json.loads(mf.read_text()).get("explicitly_NOT_claimed", [])
        except Exception:                                       # noqa: BLE001
            pass
    return out


_LIN = [(c / 255) / 12.92 if c / 255 <= 0.03928 else ((c / 255 + 0.055) / 1.055) ** 2.4
        for c in range(256)]


def _lum(p) -> float:
    return 0.2126 * _LIN[p[0]] + 0.7152 * _LIN[p[1]] + 0.0722 * _LIN[p[2]]


def dark_feed_standout(im) -> float:
    """Fraction of the 3:4 grid tile that stands out >= 3:1 from a dark feed."""
    tile = im.convert("RGB").crop((0, 240, 1080, 1680)).resize((270, 360))
    fl = _lum(FEED_DARK)
    # tobytes, not getdata: getdata is deprecated (gone in Pillow 14) and its
    # replacement does not exist in older Pillow — another machine may have either.
    raw = tile.tobytes()
    px = [raw[i:i + 3] for i in range(0, len(raw), 3)]
    hit = sum(1 for p in px
              if (max(_lum(p), fl) + 0.05) / (min(_lum(p), fl) + 0.05) >= 3.0)
    return hit / len(px)


def check(slug: str, rec: dict) -> int:
    """prepublish: every reel has a cover, and its numbers are still sourced."""
    png = ROOT / "out" / "thumbnails" / f"{slug}-vertical.png"
    if not png.exists():
        print(f"cover MISSING — {slug}. Every reel gets one (user directive "
              f"2026-09-11). AGENT.md STEP 6, then:\n  python3 tools/"
              f"make_thumbnail.py {slug} --frame <asset> --line1 \"...\" --line2 \"...\"")
        return 1
    if rec:
        bad = unsourced_numbers(slug, [rec.get("line1"), rec.get("line2"), rec.get("brand")])
        if bad:
            print(f"cover numbers not in script.md or research.md: {bad}")
            return 1
    print(f"cover ok — {slug}" + ("" if rec else
          " (made before jobs/<slug>/cover.json existed, so its words are not re-checkable)"))
    return 0


def selftest() -> int:
    from PIL import Image
    ok = True

    def t(label, cond):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")

    t("a 14-character line fits", len("CHIP PRICES UP") <= MAX_CHARS_PER_LINE)
    t("a 17-character line is refused", len("SNAPDRAGON PRICES") > MAX_CHARS_PER_LINE)
    t("'5' is sourced by a script that says 'five'", not unsourced_in(["UP TO 5"], "Up to five."))
    t("'18' is sourced by 'eighteen billion'", not unsourced_in(["18 BILLION"], "eighteen billion"))
    t("'$720' is sourced by the ledger's '$40 to $720'", not unsourced_in(["$720"], "$40 to $720"))
    t("'1,500' matches '1500'", not unsourced_in(["1,500"], "1500 units"))
    t("an invented '20%' is caught", unsourced_in(["UP 20%"], "double digits, 2026") == ["20"])
    t("'20' is not found inside '2026'", unsourced_in(["20"], "in 2026") == ["20"])
    black = Image.new("RGB", (1080, 1920), (7, 7, 10))
    t("a cover that is all ground vanishes in a dark feed", dark_feed_standout(black) < STANDOUT_MIN)
    lit = black.copy(); lit.paste((230, 60, 40), (54, 300, 1026, 1360))
    t("a cover with a bright filled subject stands out", dark_feed_standout(lit) > STANDOUT_MIN)
    print("make_thumbnail selftest", "PASSED" if ok else "FAILED")
    return 0 if ok else 1





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
    ap.add_argument("--line1", default=None, help="white caps line (<=3 words, <=14 chars)")
    ap.add_argument("--line2", default=None,
                    help="the payoff, on the accent block (<=3 words, <=14 chars)")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if this reel has no cover (prepublish runs this)")
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
    ap.add_argument("--style", default=None)
    # Kept as a no-op: covers are a standard step again (2026-09-11), and the
    # ledger still quotes commands that carry this flag.
    ap.add_argument("--i-know-its-retired", action="store_true", help=argparse.SUPPRESS)
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = ap.parse_args()

    # THE RECORD TRAVELS. jobs/ is tracked, so jobs/<slug>/cover.json carries the
    # chosen frame and words to every machine; a re-render is `make_thumbnail.py
    # <slug>`. The frame itself lives in the gitignored public/assets/, so on a
    # new machine an OLD reel's cover needs that reel's assets fetched again.
    rec_path = ROOT / "jobs" / args.slug / "cover.json"
    rec = json.loads(rec_path.read_text()) if rec_path.exists() else {}
    if args.check:
        sys.exit(check(args.slug, rec))
    if args.line1 is None and args.line2 is None:
        if not rec:
            die(f"no --line1/--line2 and no jobs/{args.slug}/cover.json yet. "
                "AGENT.md STEP 6: pick the subject by the image ladder, take the "
                "words from research.md, then run once with --frame/--line1/--line2.")
        for k in ("line1", "line2", "brand", "frame", "at", "style", "block", "block_text"):
            if getattr(args, k) in (None, "") and rec.get(k) not in (None, ""):
                setattr(args, k, rec[k])
    elif args.line1 is None or args.line2 is None:
        die("give both --line1 and --line2")
    args.style = args.style or "editorial"

    for name, val in (("--line1", args.line1), ("--line2", args.line2)):
        if len(val.split()) > MAX_WORDS_PER_LINE:
            die(f"{name} {val!r} has {len(val.split())} words; max is "
                f"{MAX_WORDS_PER_LINE}. In a grid this is ~200px wide — a "
                f"longer line is a smear. Cut words, never shrink the type.")
        if len(val) > MAX_CHARS_PER_LINE:
            die(f"{name} {val!r} is {len(val)} characters; max is "
                f"{MAX_CHARS_PER_LINE}. At 104px heavy caps a 17-character line "
                f"wraps to two. Shorter words, never smaller type.")
    bad = unsourced_numbers(args.slug, [args.line1, args.line2, args.brand])
    if bad:
        die(f"number(s) {bad} on the cover appear nowhere in jobs/{args.slug}/"
            "script.md or research.md. A cover has no room for a source, so a "
            "number on it must already be one the reel proved.")
    nc = not_claimed(args.slug)
    if nc:
        print("  the cover must not claim (research.md / manifest):")
        for line in nc[:6]:
            print(f"    - {line[:110]}")

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

    if args.fmt == "vertical":
        from PIL import Image
        so = dark_feed_standout(Image.open(out))
        print(f"  dark feed  {so:.0%} of the 3:4 tile stands out from YouTube's dark "
              f"theme" + ("" if so >= STANDOUT_MIN else
              f"  <- UNDER {STANDOUT_MIN:.0%}: the subject vanishes in dark mode. "
              f"Brighter asset or tighter crop (AGENT.md STEP 6)."))
        rec_path.parent.mkdir(parents=True, exist_ok=True)
        rec_path.write_text(json.dumps({k: v for k, v in {
            "frame": args.frame, "at": args.at, "line1": args.line1,
            "line2": args.line2, "brand": args.brand, "style": args.style,
            "block": args.block, "block_text": args.block_text}.items()
            if v not in (None, "")}, indent=2) + "\n")
        print(f"  record jobs/{args.slug}/cover.json")

    print("\nUpload as the Reel cover / Shorts custom thumbnail.")


if __name__ == "__main__":
    main()
