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
  .win {{ width:{winw}px; background:#1a1b23; border-radius:14px;
         box-shadow:0 24px 70px rgba(0,0,0,.5); overflow:hidden;
         font-family:"SF Mono",Menlo,monospace; }}
  .bar {{ height:38px; background:#2a2b35; display:flex; align-items:center;
         padding:0 14px; gap:8px; }}
  .dot {{ width:13px; height:13px; border-radius:50%; }}
  .title {{ color:#9a9ba5; font-size:13px; margin-left:12px; }}
  pre {{ margin:0; padding:18px 20px; font-size:13.5px; line-height:1.42;
        color:#d6d7de; white-space:pre; overflow:hidden; }}
  .prompt {{ color:#5bd6a2; }}
  .cmd {{ color:#fff; }}
  .hl {{ background:rgba(37,99,235,.35); color:#fff; border-radius:3px; }}
  .cursor {{ display:inline-block; width:8px; height:16px; background:#d6d7de;
            vertical-align:text-bottom; animation:blink 1s steps(1) infinite; }}
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

    Path(a.out).write_text(PAGE.format(
        canvas="#101014", winw=a.width, title=html.escape(a.title),
        cmd_js=json.dumps(a.cmd), lines_js=json.dumps(lines),
        type_js="true" if not a.no_type else "false"))
    secs = (0 if a.no_type else len(a.cmd) * 0.046 + 0.42) + len(lines) * 0.042
    print(f"wrote {a.out}  ({len(lines)} lines; animation ~{secs:.1f}s — "
          f"record with duration >= {secs + 1.5:.0f}s)")


if __name__ == "__main__":
    main()
