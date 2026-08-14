# Manim mechanism animations

Brand-themed diagram clips for "mechanism" beats — how a system works:
model fan-outs, pipelines/data flow, head-to-head comparisons. Rendered with
Manim Community Edition, themed to the reel style packs (mirrors
`src/theme/tokens.ts` exactly), and dropped into the reel as footage clips.

Clips are **16:9 @ 1920x1080, 30fps, ~4-5s** — card-frame them like any other
footage clip, or full-bleed-crop into the 1080x1920 canvas.

## Usage

```bash
python3 tools/manim_scene.py <template> --style varun|nick --bg cream|black \
    --out <path.mp4> [--args '<JSON>']
```

Examples (these are the verified sample commands):

```bash
# model fan-out, varun cream
python3 tools/manim_scene.py fanout --style varun --bg cream \
  --out out/dev-manim/fanout-varun-cream.mp4 \
  --args '{"center": "Fable 5", "children": ["Kimi K2.7", "GLM 5.2", "Qwen 4", "DeepSeek V4"]}'

# pipeline, nick cream
python3 tools/manim_scene.py pipeline --style nick --bg cream \
  --out out/dev-manim/pipeline-nick-cream.mp4 \
  --args '{"stages": ["script", "voice", "avatar", "render"]}'

# versus, nick black
python3 tools/manim_scene.py versus --style nick --bg black \
  --out out/dev-manim/versus-nick-black.mp4 \
  --args '{"left": "Claude Code", "right": "Cursor", "winner": "left"}'
```

To use in a reel, render into `public/assets/<slug>/` and reference the mp4 as
a footage scene like any other clip.

## Templates — when to use which

| Template   | Use for | Args |
|------------|---------|------|
| `fanout`   | One thing producing/spawning/routing to many: a lab shipping N models, a router hitting N providers, one tool feeding N outputs. Center node pops in (accent fill, serif italic), arrows draw outward with stagger, children spring in. | `{"center": str, "children": [str, ...]}` (max 7 children) |
| `pipeline` | Sequential mechanisms: how something is built step by step, data flow, "here's the automation". Stages pop in left→right with drawing arrows, then each stage flashes the accent in sequence; the final stage keeps the accent. | `{"stages": [str, ...]}` (max 6 stages; 3-5 reads best) |
| `versus`   | Head-to-head comparisons, benchmark beats, "X just beat Y". Nodes slam in from the sides, big serif italic accent "vs", then an accent ring draws around the winner. | `{"left": str, "right": str, "winner": "left"\|"right"\|null}` |

Rules of thumb:
- Keep labels short (1-3 words) — these are glanceable diagrams, not slides.
- Match `--style`/`--bg` to the surrounding beat so the clip cuts in natively.
- Accent is used sparingly by design (one accent element per diagram). Don't
  ask for more; that's the brand.

## Theming

`tools/manim_theme.py` is the single source of truth, mirroring
`src/theme/tokens.ts`:

- **varun** — cream `#f4f0e6` / black `#0a0a0a`, ink `#141414`
  (`#f5f2ea` on dark), accent yellow `#FFD84D`
- **nick** — cream `#efe9dc` / black `#0d0d0d`, ink `#181512`
  (`#f2ede3` on dark), accent terracotta `#E0785A`

Type: real **Fraunces** (converted from `public/fonts/*.woff2` into
`tools/fonts/*.ttf`, registered via manimpango at import; falls back to
Georgia if the TTFs are missing) for display words, Helvetica Neue for labels.
Strokes are thin (3.0), nodes are rounded white/panel cards — never default
Manim blue-on-black.

Building a new template: subclass `ReelScene` (sets brand background and
exposes `self.ctx`), and use `make_node`, `make_arrow`, `serif_text`,
`sans_text`, `accent_underline`. Note `make_node` sets `z_index` so labels
survive animating the box alone — keep that pattern.

## Install (macOS, no Homebrew additions)

Verified working on this machine (Python 3.13 from python.org, arm64,
Manim CE v0.20.1). pycairo has no macOS wheel, so it builds from source; it
needs a pkg-config binary and cairo. Homebrew cairo was already present but
`pkg-config` was not — the PyPI `pkgconf` wheel covers that without brew.
macOS lacks `.pc` files for zlib/bzip2/expat, so stub ones are created.

```bash
pip3 install pkgconf                       # ships a pkgconf/pkg-config binary

# stub .pc files for libs macOS provides natively
mkdir -p /tmp/pc
printf 'Name: zlib\nDescription: z\nVersion: 1.2.12\nLibs: -lz\nCflags:\n'   > /tmp/pc/zlib.pc
printf 'Name: bzip2\nDescription: bz\nVersion: 1.0.8\nLibs: -lbz2\nCflags:\n' > /tmp/pc/bzip2.pc
printf 'Name: expat\nDescription: ex\nVersion: 2.5.0\nLibs: -lexpat\nCflags:\n' > /tmp/pc/expat.pc

# the python shim 'pkg-config' can be flaky; point builds at the real binary
export PKG_CONFIG="$(python3 -c 'import pkgconf,os;print(os.path.join(os.path.dirname(pkgconf.__file__),".bin","pkgconf"))')"
export PKG_CONFIG_PATH=/opt/homebrew/lib/pkgconfig:/opt/homebrew/share/pkgconfig:/tmp/pc

pip3 install pycairo
pip3 install manim
python3 -m manim --version   # Manim Community v0.20.1
```

These env vars are only needed while pip-building pycairo — rendering needs
nothing beyond `ffmpeg` on PATH (`tools/manim_scene.py` appends
`/opt/homebrew/bin` defensively).

Font conversion (already done, only needed if `tools/fonts/` is deleted):

```bash
pip3 install fonttools brotli
python3 - <<'EOF'
from fontTools.ttLib import TTFont
for n in ("Fraunces-400", "Fraunces-600", "Fraunces-Italic"):
    f = TTFont(f"public/fonts/{n}.woff2"); f.flavor = None
    f.save(f"tools/fonts/{n}.ttf")
EOF
```
