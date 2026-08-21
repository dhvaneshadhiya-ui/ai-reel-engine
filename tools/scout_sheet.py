#!/usr/bin/env python3
"""One glance per candidate clip — the scout's eye, made cheap.

WHY THIS EXISTS
---------------
AGENT.md's scout rule is the honest one: "Verify every candidate by
extracting frames and LOOKING at them. Write `shows` from what you actually
see, never from what you assume." It is also [EYE] and slow, which in this
repo's history is the recipe for a rule that gets skipped — thin `shows`
text is why grok-bot could only justify 4 of 39 covers phrases while
iphone-fold-ultra managed 11 of 30.

This makes the look one file: a labeled contact sheet per candidate clip —
N frames evenly spaced across the whole clip, timestamped, tiled into a
single JPG. The scout still does the looking and the writing; they no
longer do the scrubbing. Same move preflight_stills.py made for render QC,
pointed at the other end of the pipeline.

    python3 tools/scout_sheet.py <clip.mp4>            # one sheet
    python3 tools/scout_sheet.py <dir>                 # every video inside
    python3 tools/scout_sheet.py <slug>                # _sources + public
                                                       #   assets for the job
    python3 tools/scout_sheet.py --selftest

Sheets land next to their source as `<name>.sheet.jpg` (or under --out).
Options: --frames N (default 24) · --cols N (default 6) · --out DIR.

Timestamps are burned with drawtext — the filter ffmpeg-full was installed
for. On a build without it the tool still produces the sheet, unlabeled,
and says so loudly rather than failing: a sheet without timestamps still
beats no sheet.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FRAMES, COLS, TILE_W = 24, 6, 320
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi"}

FONTS = [ROOT / "public/fonts/PressStart2P.ttf",          # ships with the repo
         Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
         Path("/System/Library/Fonts/Helvetica.ttc")]


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path: Path) -> dict | None:
    r = _run(["ffprobe", "-v", "error", "-print_format", "json",
              "-show_format", "-show_streams", str(path)])
    if r.returncode != 0:
        return None
    d = json.loads(r.stdout)
    vs = next((s for s in d.get("streams", [])
               if s.get("codec_type") == "video"), None)
    if not vs:
        return None
    dur = float(d.get("format", {}).get("duration") or
                vs.get("duration") or 0)
    return dict(duration=dur, width=vs.get("width"), height=vs.get("height"))


def _font() -> Path | None:
    return next((f for f in FONTS if f.exists()), None)


_warned_label = False


def sheet(src: Path, out: Path, frames: int = FRAMES,
          cols: int = COLS) -> dict | None:
    """Extract, label, tile. Returns probe info on success."""
    global _warned_label
    info = probe(src)
    if info is None or info["duration"] <= 0:
        print(f"  skip  {src.name} — no readable video stream")
        return None
    dur = info["duration"]
    n = max(2, min(frames, int(dur * 10) or 2))   # a 0.4s clip gets 4 frames
    ts = [(i + 0.5) * dur / n for i in range(n)]
    font = _font()
    with tempfile.TemporaryDirectory(prefix="scout-sheet-") as td:
        for i, t in enumerate(ts):
            label = f"{t:.1f}s"
            vf = f"scale={TILE_W}:-2"
            if font:
                vf += (f",drawtext=fontfile='{font}':text='{label}'"
                       ":fontsize=13:fontcolor=white:box=1"
                       ":boxcolor=black@0.55:boxborderw=4:x=6:y=6")
            r = _run(["ffmpeg", "-v", "error", "-y",
                      "-ss", f"{min(t, dur * 0.999):.3f}", "-i", str(src),
                      "-frames:v", "1", "-vf", vf,
                      f"{td}/f{i:03d}.png"])
            if r.returncode != 0 and font:
                # drawtext unavailable (plain ffmpeg build) — degrade, once,
                # loudly. An unlabeled sheet still beats no sheet.
                if not _warned_label:
                    print("  ! drawtext failed — sheets will be UNLABELED. "
                          "brew install ffmpeg-full restores timestamps.")
                    _warned_label = True
                font = None
                r = _run(["ffmpeg", "-v", "error", "-y",
                          "-ss", f"{min(t, dur * 0.999):.3f}", "-i", str(src),
                          "-frames:v", "1", "-vf", f"scale={TILE_W}:-2",
                          f"{td}/f{i:03d}.png"])
            if r.returncode != 0:
                print(f"  skip  {src.name} — frame extract failed at {t:.1f}s")
                return None
        rows = math.ceil(n / cols)
        r = _run(["ffmpeg", "-v", "error", "-y", "-framerate", "1",
                  "-i", f"{td}/f%03d.png",
                  "-vf", f"tile={cols}x{rows}:padding=2:color=black",
                  "-frames:v", "1", str(out)])
        if r.returncode != 0:
            print(f"  FAIL tiling {src.name}: {r.stderr.strip()[:120]}")
            return None
    print(f"  sheet {out}  ({dur:.1f}s · {info['width']}x{info['height']} "
          f"· {n} frames)")
    return info


def collect(target: str) -> list[Path]:
    p = Path(target)
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(q for q in p.rglob("*")
                      if q.suffix.lower() in VIDEO_EXT
                      and ".sheet." not in q.name)
    # a slug: raw candidates first, then what the reel already uses
    if (ROOT / "jobs" / target).exists():
        vids = []
        for base in (ROOT / "_sources/assets" / target,
                     ROOT / "_sources" / target,
                     ROOT / "public/assets" / target):
            if base.exists():
                vids += [q for q in base.rglob("*")
                         if q.suffix.lower() in VIDEO_EXT
                         and ".sheet." not in q.name]
        return sorted(set(vids))
    sys.exit(f"{target!r} is not a file, a directory, or a job slug.")


def selftest() -> int:
    """Prove the whole chain on synthetic clips — including the machine's
    drawtext capability, which is exactly what ffmpeg-full was installed
    for and exactly what a plain build silently lacks."""
    ok = True

    def check(label, cond):
        nonlocal ok
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        ok = ok and cond

    with tempfile.TemporaryDirectory(prefix="scout-selftest-") as td:
        clip = Path(td) / "t.mp4"
        r = _run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                  "-i", "testsrc=duration=3:size=320x240:rate=10",
                  str(clip)])
        check("synthetic clip encodes", r.returncode == 0)
        out = Path(td) / "t.sheet.jpg"
        info = sheet(clip, out)
        check("sheet produced", info is not None and out.exists())
        pi = probe(out) if out.exists() else None
        check("sheet is a valid image of tiled width",
              pi is not None and pi["width"] >= TILE_W * 2)
        # drawtext is a CAPABILITY, not a requirement — plain ffmpeg still
        # produces useful (unlabeled) sheets, and a missing nice-to-have must
        # not fail doctor and thereby block renders (render_job runs doctor).
        # Exit 2 = "works, unlabeled"; doctor reports it as a warn.
        unlabeled = _warned_label or _font() is None
        short = Path(td) / "s.mp4"
        _run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
              "-i", "testsrc=duration=0.4:size=160x120:rate=10", str(short)])
        check("sub-second clip still sheets",
              sheet(short, Path(td) / "s.sheet.jpg") is not None)
    if ok and unlabeled:
        print("\n  scout sheet selftest PASSED — but sheets are UNLABELED "
              "(no drawtext/font).\n  brew install ffmpeg-full restores "
              "timestamps.\n")
        return 2
    print("\n  scout sheet selftest " + ("PASSED" if ok else "FAILED") + "\n")
    return 0 if ok else 1


def main() -> None:
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())

    def opt(name, cast=str, default=None):
        if name in argv:
            i = argv.index(name)
            if i + 1 < len(argv):
                return cast(argv[i + 1])
        return default

    frames = opt("--frames", int, FRAMES)
    cols = opt("--cols", int, COLS)
    out_dir = opt("--out", Path)
    vids = collect(args[0])
    if not vids:
        sys.exit(f"no video files found under {args[0]!r}")
    made = 0
    for v in vids:
        out = (out_dir / f"{v.stem}.sheet.jpg") if out_dir \
            else v.with_suffix("").with_name(v.stem + ".sheet.jpg")
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
        if sheet(v, out, frames, cols):
            made += 1
    print(f"\n  {made}/{len(vids)} sheet(s). Now LOOK, then write `shows` "
          "from what is on the sheet —\n  not from the filename, and not "
          "from what the source claimed it was.")


if __name__ == "__main__":
    main()
