#!/usr/bin/env python3
"""Render REAL command output as a self-animating terminal page for capture.

WHY THIS EXISTS
---------------
The ai-tools format's evidence unit is a windowed recording of the tool
running (formats/ai-tools.md). For BROWSER tools, capture.mjs records the
real page. For CLI tools there is no browser to point at — and screen-
recording a live terminal needs macOS permissions and unrepeatable takes.

So: run the real command, keep its REAL output, and play it back inside a
styled terminal window that capture.mjs can record deterministically —
typing the command, then revealing the genuine output line by line. The
utility pack already sanctions exactly this class of treatment ("UI dialog
recreations — pixel-perfect, clean, real, credible"); the honesty line is
that the DATA is the machine's own, and the manifest `shows` says
"recreation playing back real <tool> output". Rule 3 holds because nothing
on screen claims to be anything it is not.

    python3 tools/terminal_page.py --cmd "npx ccusage monthly" \\
        --body _sources/<slug>/ccusage-monthly.txt \\
        --out /tmp/term.html [--title "you@mac: ~"] [--highlight "Total"]
        [--no-type]           # output pre-revealed (for hero/hold shots)
        [--cols 120]          # wraps the window to the content

Then record it:
    node tools/capture.mjs record "file:///tmp/term.html" --out clip.webm \\
        --duration 9 --width 1280 --height 800 --scale 2
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
  html,body {{ margin:0; padding:0; background:{canvas}; height:100%; }}
  body {{ display:flex; align-items:center; justify-content:center; }}
  .win {{ width:{winw}px; background:#1a1b23; border-radius:{radius}px;
         box-shadow:0 24px 70px rgba(0,0,0,.5); overflow:hidden;
         font-family:"SF Mono",Menlo,monospace; }}
  .bar {{ height:{barh}px; background:#2a2b35; display:flex; align-items:center;
         padding:0 {barpad}px; gap:{dotgap}px; }}
  .dot {{ width:{dot}px; height:{dot}px; border-radius:50%; }}
  .title {{ color:#9a9ba5; font-size:{titlef}px; margin-left:12px; }}
  pre {{ margin:0; padding:{prepad}px {prepadx}px; font-size:{font}px;
        line-height:1.5; color:#d6d7de; white-space:pre; overflow:hidden; }}
  .prompt {{ color:#5bd6a2; }}
  .cmd {{ color:#fff; }}
  .hl {{ background:rgba(37,99,235,.35); color:#fff; border-radius:3px; }}
  .cursor {{ display:inline-block; width:{caret}px; height:{careth}px;
            background:#d6d7de; vertical-align:text-bottom;
            animation:blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
</style></head><body>
<div class="win"><div class="bar">
  <div class="dot" style="background:#ff5f57"></div>
  <div class="dot" style="background:#febc2e"></div>
  <div class="dot" style="background:#28c840"></div>
  <div class="title">{title}</div></div>
<pre id="t"><span class="prompt">➜ </span><span class="cmd" id="c"></span><span class="cursor" id="k"></span><span id="o"></span></pre>
</div>
<script>
  const CMD = {cmd_js};
  const LINES = {lines_js};
  const TYPE = {type_js};
  const c = document.getElementById("c"), o = document.getElementById("o"),
        k = document.getElementById("k");
  function esc(s) {{ return s; }}   // lines are pre-escaped server-side
  let li = 0;
  function reveal() {{
    if (li >= LINES.length) {{ k.remove(); return; }}
    o.insertAdjacentHTML("beforeend", "\\n" + LINES[li++]);
    setTimeout(reveal, 42);
  }}
  if (TYPE) {{
    let ci = 0;
    (function typeCmd() {{
      if (ci < CMD.length) {{ c.textContent += CMD[ci++]; setTimeout(typeCmd, 46); }}
      else setTimeout(reveal, 420);
    }})();
  }} else {{ c.textContent = CMD; LINES.forEach(l =>
      o.insertAdjacentHTML("beforeend", "\\n" + l)); k.remove(); }}
</script></body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--body", required=True, help="file with the REAL output")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="dhvanesh@mac — zsh")
    ap.add_argument("--highlight", action="append", default=[],
                    help="substring(s) to highlight wherever they appear")
    ap.add_argument("--no-type", action="store_true")
    ap.add_argument("--width", type=int, default=1180,
                    help="terminal window px width")
    ap.add_argument("--fit", type=int, metavar="VIEWPORT_PX",
                    help="size the window AND its type to fill a viewport of "
                         "this CSS width (use the recorder's --width). The "
                         "monospace column is measured from the longest line, "
                         "so nothing clips — a fixed 13.5px font silently cut "
                         "'66%% of window' off a mobile recreation on "
                         "2026-08-25.")
    a = ap.parse_args()

    raw = Path(a.body).read_text().rstrip("\n").splitlines()
    lines = []
    for ln in raw:
        e = html.escape(ln)
        for h in a.highlight:
            eh = html.escape(h)
            if eh in e:
                e = e.replace(eh, f'<span class="hl">{eh}</span>')
        lines.append(e)

    # TYPE SIZE FROM THE CONTENT, not a constant. SF Mono's advance width is
    # 0.6em, so the longest line decides how big the type can be inside the
    # window — and the window decides how much of the frame the evidence owns.
    font, winw = 13.5, a.width
    if a.fit:
        winw = int(a.fit * 0.94)
        widest = max((len(ln) for ln in raw), default=1)
        widest = max(widest, len(a.cmd) + 3)
        pad = max(10, int(a.fit * 0.035))
        font = round((winw - 2 * pad) / (widest * 0.6), 1)
        prepad, prepadx = int(font * 1.3), pad
    else:
        prepad, prepadx = 18, 20
    scale = font / 13.5
    Path(a.out).write_text(PAGE.format(
        canvas="#101014", winw=winw, title=html.escape(a.title),
        font=font, prepad=prepad, prepadx=prepadx,
        radius=max(10, int(10 * scale)), barh=max(28, int(30 * scale)),
        barpad=max(10, int(12 * scale)), dot=max(9, int(11 * scale)),
        dotgap=max(6, int(7 * scale)), titlef=max(10, round(11 * scale, 1)),
        caret=max(5, int(6 * scale)), careth=max(11, int(13 * scale)),
        cmd_js=json.dumps(a.cmd), lines_js=json.dumps(lines),
        type_js="true" if not a.no_type else "false"))
    secs = (0 if a.no_type else len(a.cmd) * 0.046 + 0.42) + len(lines) * 0.042
    print(f"wrote {a.out}  ({len(lines)} lines, font {font}px, window {winw}px; "
          f"animation ~{secs:.1f}s — record with duration >= {secs + 1.5:.0f}s)")
    if a.fit:
        # NATURAL HEIGHT, so the recorder crops the canvas to the evidence.
        # A terminal centred in a 9:16 viewport is a small band in a sea of
        # dark — the /clear before/after "undersold its own drama" (user,
        # 2026-08-25). Record at this height and the window IS the frame;
        # the scene (floatcard/footage) then decides how it sits in 9:16.
        bar = max(28, int(30 * scale))
        body = (len(lines) + 1) * 1.5 * font + 2 * prepad
        # EVEN css px: h264 refuses odd pixel dimensions, and every recorder
        # scale we use is a whole number, so an odd CSS height becomes an odd
        # physical height and the mp4 conform dies (2026-08-25).
        nat = int(bar + body + a.fit * 0.06)
        print(f"  natural viewport for this content: "
              f"--width {a.fit} --height {nat + (nat % 2)}")


if __name__ == "__main__":
    main()
