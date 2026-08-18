#!/usr/bin/env python3
"""Turn an iPhone screen recording into a reel-ready clip, without leaking your life.

WHY THIS AND NOT THE SIMULATOR
------------------------------
The fix-it / how-to format needs device UI on screen. The iOS Simulator was the
plan, but it needs a full Xcode install (this Mac has only Command Line Tools),
and Apple's SDK licence scopes the Simulator to developing and testing apps —
publishing its output as editorial content is at best unsettled. A recording of
your OWN device has no such question, needs nothing installed, and shows the real
OS: a real Face ID prompt, a real carrier, real behaviour.

THE PART THAT MATTERS IS THE PRIVACY SCRUB
------------------------------------------
A screen recording carries your carrier, the exact time, your battery level, your
Wi-Fi network name, and any notification that happens to land mid-take. Publishing
that to a few hundred thousand people leaks real detail about you. So the scrub is
not optional here and it is not silent: it prints what it covered, writes a
before/after frame, and tells you to look at them.

    python3 tools/ingest_screencap.py <in.mov>                 # probe only
    python3 tools/ingest_screencap.py <in.mov> --out clip.mp4  # normalise + scrub
    ... --status-frac 0.055     # the top band to cover, as a fraction of height
    ... --keep-status           # DON'T scrub (you have already checked it)
    ... --trim 4.5:9.0          # seconds, in:out

GEOMETRY IS MEASURED, NOT ASSUMED. Devices differ (886x1920, 1170x2532,
1179x2556, 1206x2622) and so does where iOS puts the status bar. This reads the
file and reports; it never hardcodes a device.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

FRAME_W, FRAME_H = 1080, 1920      # the only output shape we ship

# The status bar sits in the top ~5% on every modern iPhone, but the exact
# fraction moves with the notch/island. Default is deliberately generous.
DEFAULT_STATUS_FRAC = 0.055


def probe(p: Path) -> dict:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate,codec_name",
         "-show_entries", "format=duration", "-of", "json", str(p)],
        capture_output=True, text=True)
    d = json.loads(r.stdout or "{}")
    st = (d.get("streams") or [{}])[0]
    num, _, den = (st.get("r_frame_rate") or "0/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 0.0
    return {"w": st.get("width"), "h": st.get("height"), "fps": fps,
            "codec": st.get("codec_name"),
            "dur": float((d.get("format") or {}).get("duration") or 0)}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    src = Path(args[0])
    if not src.exists():
        sys.exit(f"no such file: {src}")
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not on PATH")

    def flag(name: str, default=None):
        for a in sys.argv[1:]:
            if a.startswith(f"--{name}="):
                return a.split("=", 1)[1]
        if f"--{name}" in sys.argv[1:]:
            i = sys.argv[1:].index(f"--{name}")
            rest = sys.argv[1:][i + 1:]
            if rest and not rest[0].startswith("--"):
                return rest[0]
            return True
        return default

    info = probe(src)
    w, h = info["w"], info["h"]
    if not w or not h:
        sys.exit(f"could not read a video stream from {src}")

    print(f"\n  {src.name}")
    print(f"    {w}x{h}  {info['fps']:.0f}fps  {info['dur']:.1f}s  {info['codec']}")
    if h <= w:
        print("    LANDSCAPE — a phone screen recording should be portrait. "
              "Check you exported the right file.")
    if w % 2 or h % 2:
        print(f"    ODD DIMENSION ({w}x{h}) — libx264 cannot encode this "
              "directly; it will be padded to even. iPhone 15 Pro records at "
              "1179 wide, which hits exactly this.")

    src_ar, out_ar = w / h, FRAME_W / FRAME_H
    print(f"    aspect {src_ar:.3f} vs reel {out_ar:.3f} — "
          + ("taller than the frame: it will be fit to width with bars, "
             "or crop it yourself first"
             if src_ar < out_ar else
             "wider than the frame: it will be fit to width"))

    status_frac = float(flag("status-frac", DEFAULT_STATUS_FRAC))
    band = int(round(h * status_frac))
    print(f"    status band to cover: top {band}px ({status_frac:.1%} of height)")

    out = flag("out")
    if not out:
        print("\n  probe only. Pass --out <file.mp4> to normalise and scrub.")
        print("  LOOK AT THE FIRST FRAME before publishing: carrier, clock, "
              "battery,\n  Wi-Fi name and any notification banner all live in a "
              "screen recording.\n")
        return

    out = Path(out)
    keep = bool(flag("keep-status", False))
    trim = flag("trim")
    pre = []
    if trim and ":" in str(trim):
        a, _, b = str(trim).partition(":")
        pre = ["-ss", a, "-to", b]

    # GEOMETRY. A phone records at ~19.5:9 (0.46) and a reel is 9:16 (0.56), so
    # the source is TALLER than the frame: fitting to width overflows the height
    # and `pad` refuses ("padded dimensions cannot be smaller than input"). The
    # first draft of this did exactly that and died on the first real file.
    #
    # So fit to width and CROP the surplus height — which is also the better
    # scrub: cropping the status bar away removes those pixels entirely, where a
    # black box merely covers them and leaves a bar across the top of the shot.
    scale_f = FRAME_W / w
    scaled_h = int(round(h * scale_f / 2) * 2)
    scaled_band = int(round(band * scale_f))
    vf = [f"scale={FRAME_W}:-2"]

    if scaled_h >= FRAME_H:
        # start the crop below the status bar when scrubbing, else at the top,
        # and never run off the bottom of the scaled image
        top = scaled_band if not keep else 0
        top = max(0, min(top, scaled_h - FRAME_H))
        vf.append(f"crop={FRAME_W}:{FRAME_H}:0:{top}")
        how = (f"cropped {FRAME_W}x{FRAME_H} from y={top}"
               + (f" (status bar removed, not covered)" if not keep and top else ""))
        lost = scaled_h - FRAME_H - top
        if lost > 0:
            how += f"; {lost}px dropped from the bottom"
    else:
        # shorter than the frame: pad, and cover the band since it is still there
        if not keep:
            vf.append(f"drawbox=x=0:y=0:w={FRAME_W}:h={scaled_band}:"
                      "color=black:t=fill")
        vf.append(f"pad={FRAME_W}:{FRAME_H}:(ow-iw)/2:(oh-ih)/2:color=black")
        how = f"padded to {FRAME_W}x{FRAME_H}" + ("" if keep else "; status band covered")
    print(f"    plan: scale to {FRAME_W}x{scaled_h}, then {how}")
    cmd = (["ffmpeg", "-v", "error", "-y"] + pre + ["-i", str(src),
            "-vf", ",".join(vf), "-c:v", "libx264", "-crf", "18",
            "-pix_fmt", "yuv420p", "-an", str(out)])
    print("\n  + " + " ".join(cmd[:14]) + " ...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{r.stderr[-800:]}")

    got = probe(out)
    print(f"  wrote {out}  {got['w']}x{got['h']}  {got['dur']:.1f}s")

    # before/after stills, because a scrub you have not LOOKED at is a hope
    for label, path, at in (("before", src, 0.3), ("after", out, 0.3)):
        still = out.with_name(f"{out.stem}-{label}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(at),
                        "-i", str(path), "-frames:v", "1", str(still)],
                       capture_output=True)
        print(f"  {label}: {still}")
    if keep:
        print("\n  --keep-status: the status bar was NOT covered. You are "
              "publishing your\n  carrier, clock and battery. Say that was "
              "deliberate.")
    else:
        print("\n  Status band covered. NOW COMPARE THE TWO STILLS. The band is "
              "a fixed\n  top strip — it does NOT catch a notification that "
              "lands mid-recording, or\n  a Wi-Fi name inside a Settings row. "
              "Those are yours to spot.")


if __name__ == "__main__":
    main()
