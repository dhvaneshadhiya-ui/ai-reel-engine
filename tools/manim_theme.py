"""
manim_theme.py — brand theming for Manim mechanism animations.

Mirrors src/theme/tokens.ts exactly. Two style packs:
  varun : cream #f4f0e6 / black #0a0a0a, ink #141414, accent yellow  #FFD84D
  nick  : cream #efe9dc / black #0d0d0d, ink #181512, accent terracotta #E0785A

Aesthetic rules (keep it editorial, never default-Manim):
  - thin elegant strokes (2.5-3.5), rounded nodes, generous whitespace
  - Fraunces serif for display words, sans (Helvetica Neue) for labels
  - accent color used sparingly: one highlight, one ring, one underline

Clips render 16:9 @ 1920x1080 30fps so the reel engine can card-frame them
or crop full-bleed into the 1080x1920 canvas.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import manimpango
from manim import (
    VGroup,
    Text,
    RoundedRectangle,
    Line,
    Scene,
    config,
    Arrow,
    CubicBezier,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

# ---------------------------------------------------------------- fonts

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
_FONT_DIR = os.path.join(_TOOLS_DIR, "fonts")

_FRAUNCES_OK = False
for _f in ("Fraunces-400.ttf", "Fraunces-600.ttf", "Fraunces-Italic.ttf"):
    _p = os.path.join(_FONT_DIR, _f)
    if os.path.exists(_p):
        try:
            _FRAUNCES_OK = manimpango.register_font(_p) or _FRAUNCES_OK
        except Exception:
            pass

SERIF = "Fraunces" if _FRAUNCES_OK else "Georgia"
SANS = "Helvetica Neue"

# ---------------------------------------------------------------- palettes


@dataclass(frozen=True)
class Palette:
    id: str
    cream: str
    black: str
    white: str
    accent: str
    ink: str
    ink_on_dark: str


PALETTES: dict[str, Palette] = {
    "varun": Palette(
        id="varun",
        cream="#f4f0e6",
        black="#0a0a0a",
        white="#ffffff",
        accent="#FFD84D",
        ink="#141414",
        ink_on_dark="#f5f2ea",
    ),
    "nick": Palette(
        id="nick",
        cream="#efe9dc",
        black="#0d0d0d",
        white="#ffffff",
        accent="#E0785A",
        ink="#181512",
        ink_on_dark="#f2ede3",
    ),
}


@dataclass(frozen=True)
class ThemeCtx:
    """Resolved palette for a (style, bg) combination."""

    palette: Palette
    bg_mode: str  # "cream" | "black"

    @property
    def bg(self) -> str:
        return self.palette.cream if self.bg_mode == "cream" else self.palette.black

    @property
    def ink(self) -> str:
        return self.palette.ink if self.bg_mode == "cream" else self.palette.ink_on_dark

    @property
    def accent(self) -> str:
        return self.palette.accent

    @property
    def node_fill(self) -> str:
        # white cards on cream; slightly-lifted panel on black
        if self.bg_mode == "cream":
            return self.palette.white
        return "#1a1a1a" if self.palette.id == "varun" else "#1d1916"

    @property
    def muted(self) -> str:
        return self.ink  # used with opacity by callers


def theme(style: str = "varun", bg: str = "cream") -> ThemeCtx:
    if style not in PALETTES:
        raise ValueError(f"unknown style '{style}' (use varun|nick)")
    if bg not in ("cream", "black"):
        raise ValueError(f"unknown bg '{bg}' (use cream|black)")
    return ThemeCtx(palette=PALETTES[style], bg_mode=bg)


# ---------------------------------------------------------------- helpers

STROKE_W = 3.0  # thin, elegant


def serif_text(
    s: str,
    ctx: ThemeCtx,
    size: float = 48,
    italic: bool = True,
    weight: str = "MEDIUM",
    color: str | None = None,
) -> Text:
    """Editorial display text — Fraunces, usually italic."""
    return Text(
        s,
        font=SERIF,
        slant="ITALIC" if italic else "NORMAL",
        weight=weight,
        font_size=size,
        color=color or ctx.ink,
    )


def sans_text(
    s: str,
    ctx: ThemeCtx,
    size: float = 30,
    weight: str = "MEDIUM",
    color: str | None = None,
) -> Text:
    """Small utilitarian labels."""
    return Text(
        s, font=SANS, weight=weight, font_size=size, color=color or ctx.ink
    )


def make_node(
    label: str,
    ctx: ThemeCtx,
    accent: bool = False,
    serif: bool = False,
    font_size: float = 30,
    pad_x: float = 0.55,
    pad_y: float = 0.34,
    corner: float = 0.22,
    min_w: float = 0.0,
) -> VGroup:
    """Rounded editorial node: thin ink outline, white/panel fill, label.

    accent=True fills the pill with the brand accent (use on ONE node max).
    """
    if serif:
        txt = serif_text(label, ctx, size=font_size, italic=True)
    else:
        txt = sans_text(label, ctx, size=font_size)
    if accent:
        # accent fill always takes near-black ink for contrast
        txt.set_color(PALETTES[ctx.palette.id].ink)

    w = max(txt.width + 2 * pad_x, min_w)
    h = txt.height + 2 * pad_y
    box = RoundedRectangle(
        corner_radius=min(corner, h / 2 - 0.01),
        width=w,
        height=h,
        stroke_color=ctx.ink,
        stroke_width=STROKE_W,
        fill_color=ctx.accent if accent else ctx.node_fill,
        fill_opacity=1.0,
    )
    txt.move_to(box.get_center())
    # keep the label above the box even when the box is animated later
    # (playing an animation on the box alone re-adds it on top otherwise)
    box.set_z_index(0)
    txt.set_z_index(1)
    return VGroup(box, txt)


def make_arrow(
    start,
    end,
    ctx: ThemeCtx,
    accent: bool = False,
    stroke: float = STROKE_W,
) -> VGroup:
    """Thin line with a small open chevron tip (not manim's fat triangle)."""
    import numpy as np

    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    color = ctx.accent if accent else ctx.ink
    line = Line(start, end, stroke_color=color, stroke_width=stroke)
    # chevron tip
    direction = end - start
    n = np.linalg.norm(direction)
    if n > 1e-6:
        u = direction / n
        perp = np.array([-u[1], u[0], 0.0])
        tip_len = 0.16
        a = end - u * tip_len + perp * tip_len * 0.66
        b = end - u * tip_len - perp * tip_len * 0.66
        chev = VGroup(
            Line(a, end, stroke_color=color, stroke_width=stroke),
            Line(b, end, stroke_color=color, stroke_width=stroke),
        )
        return VGroup(line, chev)
    return VGroup(line)


def accent_underline(mobj, ctx: ThemeCtx, buff: float = 0.12, stroke: float = 5.0) -> Line:
    """Short accent underline beneath a text mobject (sparing accent usage)."""
    left = mobj.get_corner(DOWN + LEFT) + DOWN * buff
    right = mobj.get_corner(DOWN + RIGHT) + DOWN * buff
    return Line(left, right, stroke_color=ctx.accent, stroke_width=stroke)


# ---------------------------------------------------------------- scene base


class ReelScene(Scene):
    """Themed base scene: brand background, 16:9 @ 1920x1080, 30fps.

    Subclasses read self.ctx (ThemeCtx). Style/bg are injected by the CLI via
    class attributes REEL_STYLE / REEL_BG before render.
    """

    REEL_STYLE = "varun"
    REEL_BG = "cream"

    def setup(self):
        self.ctx = theme(self.REEL_STYLE, self.REEL_BG)
        self.camera.background_color = self.ctx.bg


def apply_render_config():
    """1920x1080 @ 30fps — call before rendering if not using CLI flags."""
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 30
