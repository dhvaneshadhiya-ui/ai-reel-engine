#!/usr/bin/env python3
"""Generate the two motion-graphic scene ASSETS iphone-18-pro needs.

WHY THIS EXISTS: the iGeeksBlog framework (rule 11) requires that when the VO
says the aperture opens and closes, the viewer SEES it open and close — same for
the Dynamic Island shrinking. Neither motion exists in the component library and
RULES section 10 forbids extending the engine for one reel, so these are built as
standalone MP4 scene assets and referenced from the beat sheet like any footage.
Every gate then still applies to the finished reel.

Palette is pulled from the editorial tokens, not invented:
  black #0a0a0a · cream #f4f0e6 · accent #FFD84D
"""
import math, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public/assets/iphone-18-pro"
TMP = Path("/private/tmp/claude-501/-Users-dhvaneshadhiya-Movies-ai-reel-engine/ce288be2-42e5-48b2-9912-6a9d5e942734/scratchpad/mg")
W, H, FPS = 1080, 1920, 30
BLACK = (10, 10, 10); CREAM = (244, 240, 230); ACCENT = (255, 216, 77)
BLADE = (46, 46, 48); BLADE_HI = (86, 86, 90)


def ease(t):                      # smootherstep
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def iris_frame(open_frac):
    """open_frac 1.0 = wide open, 0.18 = stopped down."""
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, int(H * 0.42)
    R = 452                                   # plate radius
    r = 54 + (R - 80) * open_frac             # aperture radius
    theta = (1 - open_frac) * 0.55            # blades rotate as they close

    # light coming through the opening: concentric amber falloff
    for k in range(26, 0, -1):
        rr = r * k / 26
        f = k / 26
        col = (int(ACCENT[0] * (1 - f * .45)), int(ACCENT[1] * (1 - f * .5)), int(ACCENT[2] * (1 - f * .25)))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)

    # blades: an N-gon hole punched through a metal plate
    N = 8
    verts = [(cx + r * math.cos(2 * math.pi * i / N + theta),
              cy + r * math.sin(2 * math.pi * i / N + theta)) for i in range(N)]
    BIG = 900
    for i in range(N):
        a, b = verts[i], verts[(i + 1) % N]
        fa = (cx + (a[0] - cx) * BIG / max(r, 1), cy + (a[1] - cy) * BIG / max(r, 1))
        fb = (cx + (b[0] - cx) * BIG / max(r, 1), cy + (b[1] - cy) * BIG / max(r, 1))
        shade = BLADE if i % 2 == 0 else BLADE_HI
        d.polygon([a, b, fb, fa], fill=shade)
        d.line([a, fa], fill=(20, 20, 22), width=3)

    # mask the plate to a disc, then a machined rim
    arr = np.array(img)
    yy, xx = np.mgrid[0:H, 0:W]
    outside = (xx - cx) ** 2 + (yy - cy) ** 2 > R ** 2
    arr[outside] = BLACK
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(120, 120, 124), width=9)
    d.ellipse([cx - R + 13, cy - R + 13, cx + R - 13, cy + R - 13], outline=(28, 28, 30), width=3)
    return img


SF = "/System/Library/Fonts/SFNS.ttf"       # SF Pro - RULES section 6 allows no other family


def island_frame(t):
    """t 0->1 : the pill shrinks 20.76mm -> 13.49mm, shown as a DETAIL view so
    the change is legible on a phone. A ghost outline holds the original width
    so the shrink is a comparison, not a memory test."""
    from PIL import ImageFont
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    PPMM = 30.0
    cy = int(H * 0.40)
    d.rounded_rectangle([-160, cy - 470, W + 160, cy + 780], radius=120,
                        fill=(26, 26, 29), outline=(110, 110, 116), width=6)
    d.rounded_rectangle([-140, cy - 452, W + 140, cy + 762], radius=104, fill=(17, 17, 19))
    e = ease(t)
    w_mm = 20.76 + (13.49 - 20.76) * e
    ph = 8.6 * PPMM
    py = cy - 120
    gw = 20.76 * PPMM
    d.rounded_rectangle([W/2 - gw/2, py, W/2 + gw/2, py + ph], radius=ph/2,
                        outline=(92, 92, 98), width=3)
    pw = w_mm * PPMM
    d.rounded_rectangle([W/2 - pw/2, py, W/2 + pw/2, py + ph], radius=ph/2,
                        fill=(0, 0, 0), outline=(150, 150, 156), width=3)
    ly = py + ph + 96
    d.line([W/2 - pw/2, ly, W/2 + pw/2, ly], fill=ACCENT, width=7)
    for sx in (W/2 - pw/2, W/2 + pw/2):
        d.line([sx, ly - 26, sx, ly + 26], fill=ACCENT, width=7)
    font = ImageFont.truetype(SF, 96)
    txt = "%.2fmm" % w_mm
    bb = d.textbbox((0, 0), txt, font=font)
    d.text((W/2 - (bb[2]-bb[0])/2, ly + 54), txt, font=font, fill=ACCENT)
    if e > 0.985:
        f2 = ImageFont.truetype(SF, 76)
        t2 = u"\u2212 35%"
        b2 = d.textbbox((0, 0), t2, font=f2)
        d.text((W/2 - (b2[2]-b2[0])/2, ly + 186), t2, font=f2, fill=CREAM)
    return img, w_mm




def encode(frames_dir, name, n):
    out = OUT / name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS),
                    "-i", str(frames_dir / "f%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                    "-r", str(FPS), str(out)], check=True)
    print(f"  wrote {out.name}  {n} frames  {n/FPS:.2f}s")


def build_iris(seconds=4.6):
    n = int(seconds * FPS); dd = TMP / "iris"; dd.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / (n - 1)
        # wide open -> stop down -> open again, so "opens and closes" is literal
        if t < 0.40:   f = 1.0 - 0.82 * ease(t / 0.40)
        elif t < 0.62: f = 0.18
        else:          f = 0.18 + 0.82 * ease((t - 0.62) / 0.38)
        iris_frame(f).save(dd / f"f{i:04d}.png")
    encode(dd, "mg-aperture-iris.mp4", n)




def build_island(seconds=4.6):
    n = int(seconds * FPS); dd = TMP / "island"; dd.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        t = i / (n - 1)
        p = 0.0 if t < 0.06 else (1.0 if t > 0.42 else (t - 0.06) / 0.36)
        img, _ = island_frame(p)
        img.save(dd / f"f{i:04d}.png")
    encode(dd, "mg-island-shrink.mp4", n)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_iris(); build_island()
