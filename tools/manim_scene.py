#!/usr/bin/env python3
"""
manim_scene.py — render brand-themed mechanism diagrams via Manim CE.

Usage:
  python3 tools/manim_scene.py <template> --style varun|nick --bg cream|black \
      --out <path.mp4> [--args '<JSON>']

Templates:
  fanout    {"center": "Fable 5", "children": ["Kimi K2.7", "GLM 5.2", ...]}
  pipeline  {"stages": ["script", "voice", "avatar", "render"]}
  versus    {"left": "...", "right": "...", "winner": "left"|"right"|null}

Output: 1920x1080 @ 30fps mp4 (16:9 card — the reel engine can card-frame it
or full-bleed-crop it). Clips run ~4-5s.

See tools/MANIM.md for details.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Template bodies. Each takes (scene, args) — scene is a ReelScene with
# scene.ctx already set. They are called from the generated scene file.
# --------------------------------------------------------------------------


def _ease_pop():
    from manim import rate_functions

    return rate_functions.ease_out_back


def build_fanout(scene, args: dict):
    """Center node fans out to N children: center pops, arrows draw with
    stagger, children spring in."""
    import numpy as np
    from manim import (
        AnimationGroup,
        Create,
        FadeIn,
        LEFT,
        RIGHT,
        LaggedStart,
    )

    from manim_theme import make_arrow, make_node

    ctx = scene.ctx
    center_label = str(args.get("center", "core"))
    children = [str(c) for c in args.get("children", ["a", "b", "c"])][:7]
    n = len(children)

    center = make_node(
        center_label, ctx, accent=True, serif=True, font_size=40,
        pad_x=0.7, pad_y=0.42, min_w=2.6,
    )
    center.move_to(LEFT * 3.6)

    # children stacked on the right, vertically centered
    child_nodes = [
        make_node(c, ctx, font_size=27, pad_x=0.5, pad_y=0.3, min_w=2.4)
        for c in children
    ]
    total_h = sum(cn.height for cn in child_nodes)
    gap = min(0.55, max(0.28, (6.8 - total_h) / max(n - 1, 1))) if n > 1 else 0
    span = total_h + gap * (n - 1)
    y = span / 2
    for cn in child_nodes:
        cn.move_to(RIGHT * 3.4 + np.array([0, y - cn.height / 2, 0]))
        y -= cn.height + gap

    arrows = []
    for cn in child_nodes:
        start = center.get_edge_center(RIGHT) + RIGHT * 0.18
        end = cn.get_edge_center(LEFT) + LEFT * 0.18
        arrows.append(make_arrow(start, end, ctx))

    # 1) center pops in with spring
    scene.play(FadeIn(center, scale=0.6), rate_func=_ease_pop(), run_time=0.6)
    scene.wait(0.15)
    # 2) arrows draw outward, staggered; 3) children pop as arrows land
    scene.play(
        LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.18),
        LaggedStart(
            *[
                AnimationGroup(FadeIn(cn, scale=0.6, rate_func=_ease_pop()))
                for cn in child_nodes
            ],
            lag_ratio=0.18,
        ),
        run_time=1.6,
    )
    scene.wait(1.4)


def build_pipeline(scene, args: dict):
    """Left-to-right stages connected by drawing arrows; each stage lights
    up in sequence."""
    from manim import (
        Create,
        FadeIn,
        LEFT,
        RIGHT,
        VGroup,
    )

    from manim_theme import make_arrow, make_node, sans_text

    ctx = scene.ctx
    stages = [str(s) for s in args.get("stages", ["in", "process", "out"])][:6]
    n = len(stages)

    font_size = 30 if n <= 4 else 25
    nodes = [
        make_node(s, ctx, font_size=font_size, pad_x=0.5, pad_y=0.36, min_w=1.9)
        for s in stages
    ]
    row = VGroup(*nodes).arrange(RIGHT, buff=1.05)
    if row.width > 12.6:
        row.scale_to_fit_width(12.6)
    row.move_to([0, 0, 0])

    arrows = [
        make_arrow(
            nodes[i].get_edge_center(RIGHT) + RIGHT * 0.14,
            nodes[i + 1].get_edge_center(LEFT) + LEFT * 0.14,
            ctx,
        )
        for i in range(n - 1)
    ]

    # step numbers above each stage, tiny + muted
    steps = []
    for i, node in enumerate(nodes):
        t = sans_text(f"0{i + 1}", ctx, size=17)
        t.set_opacity(0.45)
        t.next_to(node, direction=[0, 1, 0], buff=0.28)
        steps.append(t)

    # stages appear one by one, arrow drawing between each
    for i, node in enumerate(nodes):
        scene.play(
            FadeIn(node, scale=0.65),
            FadeIn(steps[i]),
            rate_func=_ease_pop(),
            run_time=0.42,
        )
        if i < n - 1:
            scene.play(Create(arrows[i]), run_time=0.3)

    # light-up pass: each stage flashes the accent in sequence;
    # the final stage keeps the accent (the "output")
    for i, node in enumerate(nodes):
        box = node[0]
        scene.play(box.animate.set_fill(ctx.accent), run_time=0.16)
        if i < n - 1:
            scene.play(box.animate.set_fill(ctx.node_fill), run_time=0.22)
    scene.wait(1.0)


def build_versus(scene, args: dict):
    """Two nodes slam in from the sides, serif VS between, winner ring."""
    from manim import (
        Create,
        FadeIn,
        LEFT,
        RIGHT,
        RoundedRectangle,
        rate_functions,
    )

    from manim_theme import STROKE_W, make_node, serif_text

    ctx = scene.ctx
    left_label = str(args.get("left", "A"))
    right_label = str(args.get("right", "B"))
    winner = args.get("winner")  # "left" | "right" | None

    left = make_node(
        left_label, ctx, serif=True, font_size=42, pad_x=0.75, pad_y=0.5, min_w=3.4
    )
    right = make_node(
        right_label, ctx, serif=True, font_size=42, pad_x=0.75, pad_y=0.5, min_w=3.4
    )
    left.move_to(LEFT * 3.9)
    right.move_to(RIGHT * 3.9)

    vs = serif_text("vs", ctx, size=120, italic=True, color=ctx.accent)
    vs.move_to([0, 0, 0])

    # slam in from off-screen
    left.shift(LEFT * 6)
    right.shift(RIGHT * 6)
    scene.play(
        left.animate.shift(RIGHT * 6),
        right.animate.shift(LEFT * 6),
        rate_func=rate_functions.ease_out_expo,
        run_time=0.55,
    )
    scene.play(
        FadeIn(vs, scale=0.4), rate_func=rate_functions.ease_out_back, run_time=0.5
    )
    scene.wait(0.5)

    if winner in ("left", "right"):
        target = left if winner == "left" else right
        ring = RoundedRectangle(
            corner_radius=0.34,
            width=target.width + 0.5,
            height=target.height + 0.5,
            stroke_color=ctx.accent,
            stroke_width=STROKE_W + 2.5,
            fill_opacity=0,
        ).move_to(target)
        scene.play(
            Create(ring),
            target.animate(rate_func=rate_functions.there_and_back).scale(1.06),
            run_time=0.9,
        )
    scene.wait(1.2)


TEMPLATES = {
    "fanout": build_fanout,
    "pipeline": build_pipeline,
    "versus": build_versus,
}

# --------------------------------------------------------------------------
# CLI — generates a scene file and shells out to manim
# --------------------------------------------------------------------------

_GEN_TEMPLATE = '''\
import json
import sys

sys.path.insert(0, {tools_dir!r})

from manim_theme import ReelScene
import manim_scene as _templates


class Diagram(ReelScene):
    REEL_STYLE = {style!r}
    REEL_BG = {bg!r}

    def construct(self):
        _templates.TEMPLATES[{template!r}](self, json.loads({args_json!r}))
'''


def render(template: str, style: str, bg: str, out: str, args: dict) -> str:
    if template not in TEMPLATES:
        raise SystemExit(
            f"unknown template '{template}' (choose from {', '.join(TEMPLATES)})"
        )
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    workdir = tempfile.mkdtemp(prefix="manim-reel-")
    scene_path = os.path.join(workdir, "generated_scene.py")
    with open(scene_path, "w") as f:
        f.write(
            _GEN_TEMPLATE.format(
                tools_dir=TOOLS_DIR,
                style=style,
                bg=bg,
                template=template,
                args_json=json.dumps(args),
            )
        )

    env = dict(os.environ)
    env["PATH"] = env.get("PATH", "") + os.pathsep + "/opt/homebrew/bin"

    cmd = [
        sys.executable,
        "-m",
        "manim",
        "render",
        "-qh",
        "--fps",
        "30",
        "--resolution",
        "1920,1080",
        "--format",
        "mp4",
        "--media_dir",
        os.path.join(workdir, "media"),
        "--disable_caching",
        scene_path,
        "Diagram",
    ]
    proc = subprocess.run(cmd, env=env, cwd=workdir)
    if proc.returncode != 0:
        raise SystemExit(f"manim render failed (exit {proc.returncode})")

    candidates = glob.glob(
        os.path.join(workdir, "media", "videos", "**", "*.mp4"), recursive=True
    )
    # ignore partial movie files
    candidates = [c for c in candidates if "partial_movie_files" not in c]
    if not candidates:
        raise SystemExit("manim produced no mp4 output")
    shutil.move(max(candidates, key=os.path.getmtime), out)
    shutil.rmtree(workdir, ignore_errors=True)
    return out


def main():
    p = argparse.ArgumentParser(
        description="Render a brand-themed Manim mechanism diagram."
    )
    p.add_argument("template", choices=sorted(TEMPLATES))
    p.add_argument("--style", choices=["varun", "nick"], default="varun")
    p.add_argument("--bg", choices=["cream", "black"], default="cream")
    p.add_argument("--out", required=True, help="output .mp4 path")
    p.add_argument("--args", default="{}", help="JSON template arguments")
    ns = p.parse_args()

    try:
        args = json.loads(ns.args)
    except json.JSONDecodeError as e:
        raise SystemExit(f"--args is not valid JSON: {e}")

    out = render(ns.template, ns.style, ns.bg, ns.out, args)
    print(out)


if __name__ == "__main__":
    main()
