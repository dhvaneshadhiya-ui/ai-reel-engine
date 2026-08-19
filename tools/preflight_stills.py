#!/usr/bin/env python3
"""Render one frame per scene and check them BEFORE the full render.

WHY (measured 2026-08-19, after a reel took ~2 hours)
------------------------------------------------------
The cost of a reel is not the render. It is the NUMBER of renders.

    one still, via remotion                3.3s
    one full render + master + lint      ~8min   (2283 frames)

iphone-fold-ultra was rendered SEVEN times in one session. Two died in preflight
and five completed, so roughly 40 minutes went into rendering the same reel over
and over, plus the wait between each. Every re-render was triggered by a defect
found AFTER the render finished:

    caption printed through the source credit     (found by eye, on the frame)
    captions white on white footage               (auto_contrast, unwired)
    receipt sliced mid-word at both edges         (found by eye, on the frame)
    two identical scenes back to back             (lint_frames, post-render)
    typecards 88-90% empty                        (lint_frames, post-render)

EVERY ONE of those is visible in a single still. None of them needed 2283
frames, an audio master, or eight minutes to discover. They were found late for
one structural reason: tools/lint_frames.py extracts its frames FROM THE
FINISHED VIDEO, so linting could not happen until rendering had.

This renders the same frames straight from Remotion instead — one per scene, at
the same midpoint lint_frames uses, into the same directory with the same
names. The existing checks then run against them unchanged.

    python3 tools/preflight_stills.py <slug>              # all scenes
    python3 tools/preflight_stills.py <slug> --scenes 3,7 # just these
    python3 tools/preflight_stills.py <slug> --types      # one per scene TYPE

`--types` is the fast pass: one frame per distinct scene type catches every
component-level defect (contrast, credit position, dead space, edge overflow)
in a fraction of the time, because those defects live in the COMPONENT, not in
the individual scene. Use it while iterating; use the full pass before render.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug = args[0]

    beats = json.loads((ROOT / f"src/beats/{slug}.json").read_text())
    scenes = beats["scenes"]
    fps = beats.get("fps", 30)

    only = None
    if "--scenes" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--scenes") + 1].split(",")}

    # midpoint of each scene, the same frame lint_frames samples
    picks: list[tuple[int, str, int]] = []
    cursor = 0.0
    seen_types: set[str] = set()
    for i, s in enumerate(scenes):
        mid = cursor + s["durationSec"] / 2
        cursor += s["durationSec"]
        if only is not None and i not in only:
            continue
        if "--types" in sys.argv:
            if s["type"] in seen_types:
                continue
            seen_types.add(s["type"])
        picks.append((i, s["type"], round(mid * fps)))

    out = ROOT / f"out/{slug}-lint"
    out.mkdir(parents=True, exist_ok=True)

    print(f"\n  {len(picks)} still(s) from {len(scenes)} scenes "
          f"({'one per type' if '--types' in sys.argv else 'one per scene'})\n")
    # IN PARALLEL. Each `remotion still` is a separate process that reuses the
    # cached bundle, so they do not contend for it. Measured 2026-08-19: the
    # render itself went 2.4x faster at concurrency 6 on this 8-core machine;
    # stills are the same shape of work. Capped at 4 so the preflight cannot
    # starve an interactive session.
    from concurrent.futures import ThreadPoolExecutor

    def one(job):
        i, typ, frame = job
        dest = out / f"{i:02d}-{typ}-mid.png"
        r = subprocess.run(
            ["npx", "remotion", "still", "src/index.ts", slug, str(dest),
             f"--frame={frame}", "--timeout=120000"],
            cwd=ROOT, capture_output=True, text=True)
        return i, typ, frame, r.returncode, (r.stderr or r.stdout)

    t0 = time.time()
    made = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i, typ, frame, rc, err in pool.map(one, picks):
            if rc != 0:
                print(f"  FAILED scene {i:02d} ({typ}) at frame {frame}")
                tail = err.strip().splitlines()
                print("    " + (tail[-1][:100] if tail else "no output"))
                continue
            made += 1
            print(f"  {i:02d} {typ:14} frame {frame:5}  ok")

    dt = time.time() - t0
    total_frames = round(sum(s["durationSec"] for s in scenes) * fps)
    print(f"\n  {made} still(s) in {dt:.0f}s.")
    print(f"  The full render is {total_frames} frames; this sampled {made}.")
    print(f"\n  Now run the checks that do not need a video:")
    print(f"    python3 tools/lint_frames.py {slug} --from-stills")
    print(f"    python3 tools/check_frame_contract.py {slug}")
    print(f"    python3 tools/auto_contrast.py {slug}\n")


if __name__ == "__main__":
    main()
