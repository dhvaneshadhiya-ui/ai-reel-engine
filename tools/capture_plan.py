#!/usr/bin/env python3
"""Turn a list of URLs into a capture plan, so `capture.mjs batch` has something
to eat that nobody had to hand-write.

WHY
---
Batching the capture tool is only a saving if the PLAN is cheaper than the
captures it replaces. A batch that requires hand-written JSON moves the work
rather than removing it.

    python3 tools/capture_plan.py <slug> urls.txt          # -> plan on stdout
    python3 tools/capture_plan.py <slug> urls.txt --write  # -> jobs/<slug>/capture-plan.json

`urls.txt` is one line per capture, in the form the scouting actually produces:

    https://www.macrumors.com/2026/08/06/iphone-18-pro/   mr-hero        official
    https://9to5mac.com/2026/08/17/iphone-18-pro/         9to5-features  reliable
    https://example.com/wide-dashboard                    dash  fallback  desktop:no mobile layout

Columns after the URL: output name, tier, then optional `desktop:<reason>`.
Everything else — viewport, scale, the mobile default — comes from capture.mjs.

TIER IS REQUIRED HERE, deliberately. Rule 2 says sources are scouted on mobile
first and G41 blocks a desktop capture with no recorded reason; G42 counts how
well-sourced a reel is. Measured 2026-08-19: 229 assets in this repo carry a
`shows` description and only 18 carry a tier — the per-item metadata that costs
attention is the metadata that gets dropped. A batch tool that made tier
optional would finish that job.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIERS = {"official", "reliable", "fallback"}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug, src = args[0], Path(args[1])

    plan, problems = [], []
    for n, raw in enumerate(src.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # SPLIT ONLY THE FIRST THREE. A desktop reason is a sentence, and
        # splitting the whole line on whitespace truncated it to its first word
        # — "wide" instead of "wide dashboard has no mobile layout". G41 would
        # then have passed on a reason that says nothing, which is worse than
        # blocking, because it looks like the rule was satisfied.
        parts = line.split(None, 3)
        if len(parts) < 3:
            problems.append(f"  line {n}: need at least URL, name, tier — got {len(parts)}")
            continue
        url, name, tier = parts[0], parts[1], parts[2]
        rest = [parts[3]] if len(parts) > 3 else []
        if tier not in TIERS:
            problems.append(f"  line {n}: tier {tier!r} is not one of {sorted(TIERS)}")
            continue
        item = {
            "url": url,
            "out": f"public/assets/{slug}/{name}.png",
            "tier": tier,
        }
        for extra in rest:
            if extra.startswith("desktop:"):
                item["mobile"] = False
                item["desktopReason"] = extra.split(":", 1)[1] or ""
                if not item["desktopReason"]:
                    problems.append(f"  line {n}: desktop: with no reason (G41 blocks it)")
        plan.append(item)

    if problems:
        print("\n  plan NOT written:\n" + "\n".join(problems) + "\n")
        sys.exit(1)

    out = json.dumps(plan, indent=2) + "\n"
    if "--write" in sys.argv:
        dest = ROOT / f"jobs/{slug}/capture-plan.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out)
        print(f"\n  {len(plan)} capture(s) -> {dest}")
        print(f"  node tools/capture.mjs batch {dest} --workers 4\n")
    else:
        print(out)


if __name__ == "__main__":
    main()
