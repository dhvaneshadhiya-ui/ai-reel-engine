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
# The Ultra's two shades have NO published Pantone code — they were read off
# photographs of third-party camera protectors. They were drawn as empty
# outlines at first, to say exactly that. On screen it read as a broken render,
# not as honesty: a viewer sees two blank boxes and assumes the video failed.
# So they are FILLED with approximations and the caveat is carried in the label
# instead, where it is read as information rather than as a fault.
#   silver    — "a classic silver and white model"
#   dark blue — "an indigo option similar to the iPhone Air's Deep Blue finish"
#               (MacRumors, 2026-08-09)
ULTRA = [("#D3D5D6", "SILVER"), ("#1E2A3F", "DARK BLUE")]

# CAPTION LANE. Captions were switched off on every chip beat because the
# karaoke chips printed through the artwork — which silenced roughly a third of
# the reel for a mute viewer. The artwork now ends above CONTENT_MAX and the
# band below it is left empty for the caption, so both can coexist.
CONTENT_MAX = 1300

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



# ---------------------------------------------------------------------------
# PAINTERS. Every layout finishes above CONTENT_MAX (1300) so the caption lane
# below it stays clear, and above the platform floor at 1498 either way.
# ---------------------------------------------------------------------------

def cherry(d, t, im):
    drift = math.sin(t * 0.9) * 6            # never fully settles
    a = ease(min(1, t / 0.5))
    cw, ch = 700, 820
    x, y = (W - cw) // 2, int(240 + (1 - a) * 55 + drift)
    chip(d, x, y, cw, ch, rgb("#442C43"), "6076 C", "")
    center(d, "DARK CHERRY", font(BLACK, 78), y + ch + 50, INK)
    if t > 1.1:
        center(d, "APPROX sRGB OF THE PUBLISHED CODE", font(REG, 26),
               y + ch + 160, MUTED)


def cherry_tight(d, t, im):
    drift = math.sin(t * 0.8) * 5
    a = ease(min(1, t / 0.4))
    cw, ch = 820, 890
    x, y = (W - cw) // 2, int(210 + (1 - a) * 30 + drift)
    chip(d, x, y, cw, ch, rgb("#442C43"), "6076 C", "")
    center(d, "A DARK PLUM", font(BLACK, 74), y + ch + 45, INK)
    center(d, "NOT A RED", font(REG, 32), y + ch + 145, MUTED)


def _grid(d, t, lift=None):
    center(d, "THE PRO LINEUP", font(BLACK, 54), 218, INK)
    cw, ch, gap = 470, 390, 34
    x0 = (W - (cw * 2 + gap)) // 2
    for i, (hexv, code, nm) in enumerate(PRO):
        at = 0.10 + i * 0.30
        if lift is None and t < at:
            continue
        a = 1.0 if lift is not None else ease(min(1, (t - at) / 0.45))
        col, row = i % 2, i // 2
        x = x0 + col * (cw + gap)
        y = 330 + row * (ch + 80) + int((1 - a) * 40) + int(math.sin(t * .8 + i) * 4)
        if lift is not None and i in lift and t >= lift[i]:
            y -= int(16 * ease(min(1, (t - lift[i]) / 0.4)))
        chip(d, x, y, cw, ch, rgb(hexv), code, nm)
        if lift is not None and i in lift and t >= lift[i]:
            d.rectangle([x, y + ch + 50, x + cw, y + ch + 56], fill=INK)


def lineup(d, t, im):
    _grid(d, t)


def lineup_b(d, t, im):
    # Dark Gray, then Light Blue — the two the line actually names.
    # De-emphasis is a LIFT, never a blend: fading the others toward cream
    # turned Dark Cherry into a mauve, which misstates the reel's whole claim.
    _grid(d, t, lift={2: 0.20, 1: 1.00})


def gap(d, t, im):
    """Four filled Pro chips against the Ultra's two. The count sits on the
    SAME LINE as its heading — a numeral in the same column as a chip label
    will always fight it."""
    def bank(y0, title, count):
        d.text((55, y0), title, font=font(BLACK, 50), fill=INK)
        cnt = font(BLACK, 82)
        b = d.textbbox((0, 0), count, font=cnt)
        d.text((W - 55 - (b[2] - b[0]), y0 - 24), count, font=cnt, fill=INK)

    bank(230, "iPHONE 18 PRO", "FOUR")
    for i, (hexv, code, _) in enumerate(PRO):
        a = ease(min(1, max(0, (t - 0.1 - i * .12) / .4)))
        if a <= 0: continue
        chip(d, 55 + i * 248, 348 + int((1 - a) * 26), 235, 250, rgb(hexv), code, "")

    if t > 1.5:
        a = ease(min(1, (t - 1.5) / .5))
        bank(700, "iPHONE ULTRA", "TWO")
        for i, (hexv, nm) in enumerate(ULTRA):
            chip(d, 150 + i * 450, 818 + int((1 - a) * 26) + int(math.sin(t * .8 + i) * 4),
                 330, 280, rgb(hexv), "APPROX", nm)
        if t > 2.6:
            center(d, "Ultra shades approximate — no Pantone code published",
                   font(REG, 26), 1235, MUTED)


def ultra_only(d, t, im):
    center(d, "iPHONE ULTRA", font(BLACK, 68), 240, INK)
    cw, ch = 400, 520
    for i, (hexv, nm) in enumerate(ULTRA):
        at = 0.10 + i * 0.32
        if t < at: continue
        a = ease(min(1, (t - at) / 0.35))
        x = 105 + i * 470
        y = 360 + int((1 - a) * 34) + int(math.sin(t * .8 + i) * 5)
        chip(d, x, y, cw, ch, rgb(hexv), "APPROX", nm)
    if t > 0.85:
        center(d, "shades read off leaked camera protectors", font(REG, 30), 1000, MUTED)
        center(d, "no Pantone code published", font(BOLD, 30), 1050, MUTED)


def hook_chip(d, t, im):
    """The SPLIT cover-crops its source: measured against two rendered probes,
    composite = (source - 500) * 0.52, so the chip must sit between source
    y 890 (below the headline block) and y 1400 (above the seam)."""
    drift = math.sin(t * 0.9) * 5
    a = ease(min(1, t / 0.45))
    cw, ch = 700, 490
    x, y = (W - cw) // 2, int(900 + (1 - a) * 30 + drift)
    chip(d, x, y, cw, ch, rgb("#442C43"), "6076 C", "")


def end_chip(d, t, im):
    drift = math.sin(t * 0.8) * 5
    a = ease(min(1, t / 0.4))
    cw, ch = 640, 680
    x, y = (W - cw) // 2, int(320 + (1 - a) * 28 + drift)
    chip(d, x, y, cw, ch, rgb("#442C43"), "6076 C", "")
    center(d, "A DARK PLUM", font(BLACK, 70), y + ch + 45, INK)
    center(d, "NOT A RED", font(REG, 32), y + ch + 140, MUTED)
    if t > 0.25:
        b = ease(min(1, (t - 0.25) / 0.4))
        center(d, "STILL THE ONE?", font(BLACK, 70), int(212 - (1 - b) * 16), INK)


for nm, secs, fn in (("chip-cherry", 6.0, cherry),
                     ("chip-lineup", 6.5, lineup),
                     ("chip-gap", 6.0, gap),
                     ("chip-cherry-tight", 5.0, cherry_tight),
                     ("chip-ultra", 5.0, ultra_only),
                     ("chip-lineup-b", 5.0, lineup_b),
                     ("chip-hook", 5.0, hook_chip),
                     ("chip-end", 4.0, end_chip)):
    print("rendering", nm)
    render(nm, secs, fn)
