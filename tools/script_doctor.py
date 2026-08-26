#!/usr/bin/env python3
"""Every script check, in ONE call. The craft loop's inner loop.

WHY: writing a script well takes several passes — write, measure, rewrite.
That is not a defect, it is the job. What WAS a defect is that each pass cost
four or five separate commands (prose shape, house tics, the framework's
reveal/certainty rules, the research ledger, runtime), so a five-pass rewrite
was twenty-plus round trips and the better part of twenty minutes (user,
2026-08-26). The measuring, not the writing, was the slow part.

One command, one verdict, so a pass costs one round trip:

    python3 tools/script_doctor.py <slug>
    python3 tools/script_doctor.py --file draft.md [--slug <for-corpus-compare>]

Nothing here is new enforcement — it is the existing checks, batched. propose
still runs its own copies; this is for the drafting loop BEFORE propose.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

WPS_LO, WPS_HI = 2.35, 2.75          # measured house pace


def main() -> int:
    argv = sys.argv[1:]
    slug = None
    text = None
    if "--file" in argv:
        text = Path(argv[argv.index("--file") + 1]).read_text()
        if "--slug" in argv:
            slug = argv[argv.index("--slug") + 1]
    else:
        args = [a for a in argv if not a.startswith("--")]
        if not args:
            print(__doc__.split("    python3")[0].strip())
            return 1
        slug = args[0]
        p = ROOT / f"jobs/{slug}/script.md"
        if not p.exists():
            print(f"no script at {p}")
            return 1
        text = p.read_text()

    import check_script

    words = len(text.split())
    print(f"\n=== script doctor{' — ' + slug if slug else ''} ===")
    print(f"  {words} words -> {words/WPS_HI:.0f}-{words/WPS_LO:.0f}s "
          f"at the measured 2.35-2.75 wps")

    findings: list[str] = []
    findings += check_script.check(text) or []
    findings += check_script.house_tics(text, exclude_slug=slug)

    # the framework's three mechanical rules need the job on disk
    if slug and (ROOT / "jobs" / slug).exists():
        r = subprocess.run(
            [sys.executable, str(ROOT / "tools/framework_check.py"), slug],
            capture_output=True, text=True)
        for line in r.stdout.splitlines():
            s = line.strip()
            if s.startswith(("FAIL", "note")):
                findings.append(s)

    if findings:
        print()
        for f in findings:
            print(f"  - {f}")
    else:
        print("\n  nothing to flag on shape, tics, reveal handling or "
              "certainty.")
    # SKILL CUES — a skill cannot be invoked by code, so the next best thing
    # is naming it at the exact moment its finding appears. The humanizer had
    # a stated moment in CLAUDE.md for weeks and still never ran once
    # (2026-08-26); a cue attached to the finding is what a doc line was not.
    blob = " ".join(findings).lower()
    cues = []
    if "no open loop" in blob or "opening" in blob:
        cues.append("`viral-hook-writer` for hook candidates, `going-viral` "
                    "for the loop//payoff structure above it")
    if "house tic" in blob or "ai tell" in blob or "page punctuation" in blob:
        cues.append("`humanizer` — the pass nothing runs for you")
    if "f2 certainty" in blob or "f2b" in blob:
        cues.append("`fact-check-workflow` before that claim becomes a beat")
    for c in cues:
        print(f"  SKILL CUE: {c}")
    print("\n  Read it aloud. These measure shape, not whether it is good.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
