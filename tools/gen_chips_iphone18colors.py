#!/usr/bin/env python3
"""Generate the Pantone-chip motion assets for iphone18-colors.

WHY CHIPS AND NOT RENDERS
-------------------------
Every "iPhone 18 Pro in Dark Cherry" image in circulation is a fan render or a
dummy model, and this reel's central claim is that those renders have the shade
wrong. A render on screen would contradict the narration.

A Pantone chip is the honest object: it renders a PUBLISHED CODE, and every
chip carries "APPROX sRGB" so nobody reads it as Apple's finish.

The iPhone Ultra chips are drawn as OUTLINES, not fills. Its two colours come
from photographs of third-party camera protectors — there is no published code,
so there is no value to fill them with. Filling them would be inventing data.
"""
import subprocess, pathlib, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
OUT = pathlib.Path("public/assets/iphone18-colors")
TMP = pathlib.Path("/private/tmp/claude-501/-Users-dhvanesh-AI-Reel-Engine/4e4d284d-33e5-47c7-ab71-052c73be5c2d/scratchpad/chips")
CREAM, INK, MUTED = (244, 240, 230), (20, 20, 22), (120, 116, 108)

F = "/System/Library/Fonts/Supplemental/%s"
def font(name, size): return ImageFont.truetype(F % name, size)
BOLD, REG, BLACK = "Arial Bold.ttf", "Arial.ttf", "Arial Black.ttf"

# PUBLISHED codes only. Sources in public/assets/iphone18-colors/manifest.json.
PRO = [
    ("#442C43", "6076 C", "DARK CHERRY"),
    ("#8FACD9", "2121 C", "LIGHT BLUE"),
    ("#25282A", "426 C",  "DARK GRAY"),
    ("#D0D3D4", "427 C",  "SILVER"),
]
ULTRA = [("SILVER", ""), ("DARK BLUE", "")]

def rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def ease(t): return 1 - (1 - t) ** 3

def center(d, txt, f, y, fill, w=W):
    b = d.textbbox((0, 0), txt, font=f)
    d.text(((w - (b[2] - b[0])) / 2 - b[0], y), txt, font=f, fill=fill)

def chip(d, x, y, w, h, color, code, name, alpha=1.0, outline=False):
    """One Pantone chip: colour block + white footer strip carrying the code."""
    foot = int(h * 0.26)
    if outline:
        d.rounded_rectangle([x, y, x + w, y + h], 10, outline=MUTED, width=4)
        d.line([x, y + h - foot, x + w, y + h - foot], fill=MUTED, width=3)
    else:
        d.rounded_rectangle([x, y, x + w, y + h], 10, fill=color)
        d.rectangle([x, y + h - foot, x + w, y + h], fill=(252, 252, 250))
        d.rounded_rectangle([x, y, x + w, y + h], 10, outline=(214, 210, 200), width=2)
    fs = max(13, int(foot * 0.20))
    d.text((x + 16, y + h - foot + int(foot * 0.16)), "PANTONE®",
           font=font(REG, fs), fill=MUTED if not outline else MUTED)
    d.text((x + 16, y + h - foot + int(foot * 0.46)),
           code if code else "NO CODE PUBLISHED",
           font=font(BOLD, int(fs * (1.5 if code else 1.0))), fill=INK if code else MUTED)
    if name:
        d.text((x, y + h + 14), name, font=font(BOLD, 30), fill=INK)

def encode(frames_dir, out, n):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS),
                    "-i", str(frames_dir / "%04d.png"), "-frames:v", str(n),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                    str(out)], check=True)
    print("  wrote", out)

def render(name, secs, painter):
    d = TMP / name; d.mkdir(parents=True, exist_ok=True)
    n = int(secs * FPS)
    for i in range(n):
        im = Image.new("RGB", (W, H), CREAM)
        painter(ImageDraw.Draw(im), i / FPS, im)
        im.save(d / f"{i+1:04d}.png")
    encode(d, OUT / f"{name}.mp4", n)

# ---------------------------------------------------------------- chip-cherry
def cherry(d, t, im):
    drift = math.sin(t * 0.9) * 6           # never fully settles
    a = ease(min(1, t / 0.5))
    cw, ch = 640, 800
    x, y = (W - cw) // 2, int(360 + (1 - a) * 60 + drift)
    chip(d, x, y, cw, ch, rgb("#442C43"), "6076 C", "")
    center(d, "DARK CHERRY", font(BLACK, 76), y + ch + 60, INK)
    if t > 1.1:
        center(d, "APPROX sRGB OF THE PUBLISHED CODE", font(REG, 27),
               y + ch + 160, MUTED)

# ---------------------------------------------------------------- chip-lineup
# EVERY layout here is bounded by SAFE_FLOOR. Below y 0.78 the platform draws
# its own account row and caption over ours (src/platformSafeArea.ts), so a
# chip label down there is a label nobody sees.
def lineup(d, t, im):
    center(d, "THE PRO LINEUP", font(BLACK, 58), 250, INK)
    cw, ch, gap = 430, 440, 40
    x0 = (W - (cw * 2 + gap)) // 2
    for i, (hexv, code, nm) in enumerate(PRO):
        at = 0.15 if i == 0 else 0.5 + (i - 1) * 0.9   # cherry already known
        if t < at: continue
        a = ease(min(1, (t - at) / 0.45))
        col, row = i % 2, i // 2
        x = x0 + col * (cw + gap)
        y = 360 + row * (ch + 100) + int((1 - a) * 40) + int(math.sin(t * .8 + i) * 4)
        chip(d, x, y, cw, ch, rgb(hexv), code, nm)   # deepest label ~1394

# ------------------------------------------------------------------- chip-gap
def gap(d, t, im):
    cw, ch = 290, 300
    center(d, "iPHONE 18 PRO", font(BLACK, 48), 240, INK)
    for i, (hexv, code, _) in enumerate(PRO):
        a = ease(min(1, max(0, (t - 0.1 - i * .12) / .4)))
        if a <= 0: continue
        x = 70 + (i % 4) * 233
        chip(d, x, 320 + int((1 - a) * 30), 210, 230, rgb(hexv), code, "")
    d.text((70, 570), "FOUR", font=font(BLACK, 92), fill=INK)

    if t > 1.5:
        a = ease(min(1, (t - 1.5) / .5))
        center(d, "iPHONE ULTRA", font(BLACK, 48), 745, INK)
        for i, (nm, _) in enumerate(ULTRA):
            x = 195 + i * 400
            y = 820 + int((1 - a) * 30) + int(math.sin(t * .8 + i) * 4)
            chip(d, x, y, cw, ch, None, "", nm, outline=True)
        d.text((195, 1195), "TWO", font=font(BLACK, 92), fill=INK)
        if t > 2.6:
            # the honesty line — MUST stay above the platform band
            center(d, "shades known from leaked accessories", font(REG, 27), 1330, MUTED)
            center(d, "no code published", font(BOLD, 27), 1375, MUTED)

for nm, secs, fn in (("chip-cherry", 6.0, cherry),
                     ("chip-lineup", 6.5, lineup),
                     ("chip-gap", 6.0, gap)):
    print("rendering", nm)
    render(nm, secs, fn)
