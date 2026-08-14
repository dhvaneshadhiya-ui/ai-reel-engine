#!/usr/bin/env python3
"""Showrunner — walks ONE reel through the pipeline, and stops where it must.

WHY THIS EXISTS
---------------
2026-08-14: every reel so far was produced by walking the steps by hand, which
means the order lived in someone's head. `Ootto-AI/claude-content-skills`
ships a `content-factory` orchestrator; we did not install it (it renders and
posts through its own stack, bypassing all 29 gates) — but the IDEA was right
and we had no equivalent.

This is that idea over OUR steps. It is deliberately NOT "one command that
posts 3x a day":

  * it AUTOMATES the deterministic steps (register, gates, render, master, lint)
  * it STOPS at the steps that need a human or spend money, and prints the
    exact command to continue
  * it never publishes anything, anywhere

    python3 tools/showrunner.py status <slug>    # where is this reel?
    python3 tools/showrunner.py next   <slug>    # the single next action
    python3 tools/showrunner.py run    <slug>    # advance until a stop

THE ONE INVARIANT: `run` will not cross the script-approval line, and will not
generate an avatar. Those cost credits, freeze the audio, or need your yes.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OK, PENDING, STOP = "done", "todo", "stop"


def _p(*parts) -> Path:
    return ROOT.joinpath(*parts)


def _approved(slug: str) -> bool:
    """True only if an approval exists AND still matches the script."""
    r = subprocess.run([sys.executable, str(_p("tools/script_approval.py")),
                        "check", slug], capture_output=True, text=True)
    return r.returncode == 0


def _gates_pass(slug: str) -> bool:
    if not _p(f"src/beats/{slug}.json").exists():
        return False
    r = subprocess.run([sys.executable, str(_p("tools/reel_gates.py")), slug],
                       capture_output=True, text=True)
    return r.returncode == 0


def steps(slug: str) -> list[dict]:
    """The pipeline, in order. `auto` is a command safe to run unattended."""
    return [
        dict(key="scout",
             label="Assets scouted and manifest written",
             done=_p(f"public/assets/{slug}/manifest.json").exists(),
             auto=None,
             human="Research the story, capture sources on MOBILE "
                   "(tools/capture.mjs), cut clips, and write "
                   f"public/assets/{slug}/manifest.json with credits. "
                   "See AGENT.md STEP 1a."),
        dict(key="script",
             label="Narration written",
             done=_p(f"jobs/{slug}/script.md").exists(),
             auto=None,
             human=f"Write the narration to jobs/{slug}/script.md using "
                   "formats/<format>.md for structure and the style pack for "
                   f"voice. Put judgement calls in jobs/{slug}/questions.md."),
        dict(key="approval",
             label="Script approved by the user",
             done=_approved(slug),
             auto=None,
             stops=True,
             human=f"python3 tools/script_approval.py propose {slug}\n"
                   "      Show the user the script AND the beat plan, ask the "
                   "open questions, wait for an explicit yes, then:\n"
                   f"      python3 tools/script_approval.py approve {slug}"),
        dict(key="voice",
             label="Voice + avatar master generated",
             done=_p(f"public/assets/{slug}/vo.json").exists(),
             auto=None,
             stops=True,
             human="Generate the avatar (HeyGen, native 9:16 @1080p) and the "
                   "whisper word timings. THIS SPENDS CREDITS — check the "
                   "balance first, and never run it on an unapproved script."),
        dict(key="beats",
             label="Beat sheet built",
             done=_p(f"src/beats/{slug}.json").exists(),
             auto=None,
             human=f"Build the beat sheet (tools/build_{slug}.py, modelled on "
                   "tools/build_template.py). It must carry `script` and "
                   "`approval` for G27."),
        dict(key="register",
             label="Beat sheet registered with Remotion",
             done=_p("src/generatedBeatSheets.ts").exists()
                  and slug in _p("src/generatedBeatSheets.ts").read_text(),
             auto=[sys.executable, str(_p("scripts/register_beats.py"))]),
        dict(key="gates",
             label="All gates pass",
             done=_gates_pass(slug),
             auto=[sys.executable, str(_p("tools/reel_gates.py")), slug],
             human="Fix what the gates report. They are not advisory."),
        dict(key="render",
             label="Rendered and mastered",
             done=_p(f"out/{slug}-final.mp4").exists(),
             auto=[sys.executable, str(_p("scripts/render_job.py")), slug]),
        dict(key="qc",
             label="Frame lint clean",
             done=False,   # always re-run; it is cheap and catches regressions
             auto=[sys.executable, str(_p("tools/lint_frames.py")), slug]),
        dict(key="packaging",
             label="Title, caption, hashtags, alt text",
             done=_p(f"jobs/{slug}/packaging.md").exists(),
             auto=None,
             human="Use the `social` skill. Hashtags per platform limits "
                   "(Instagram 5), hashtags in the FIRST COMMENT, and include "
                   "ALT TEXT. Then: python3 tools/packaging_check.py " + slug),
    ]


def cmd_status(slug: str) -> None:
    st = steps(slug)
    print(f"\n  REEL: {slug}\n")
    nxt = None
    for s in st:
        if s["done"]:
            mark, tail = "  [x]", ""
        elif nxt is None:
            nxt = s
            mark = "  [ ]" if not s.get("stops") else "  [!]"
            tail = "   <- next" + ("  (STOPS HERE)" if s.get("stops") else "")
        else:
            mark, tail = "  [ ]", ""
        print(f"{mark} {s['label']}{tail}")
    print()
    if nxt is None:
        print("  Everything done. Deliver the master and the packaging.\n")
    return


def cmd_next(slug: str) -> None:
    for s in steps(slug):
        if s["done"]:
            continue
        print(f"\n  NEXT — {s['label']}\n")
        if s["auto"]:
            print("      " + " ".join(str(x) for x in s["auto"]))
        else:
            print("      " + s.get("human", "(manual step)"))
        print()
        return
    print("\n  Nothing left.\n")


def cmd_run(slug: str) -> None:
    """Advance through the deterministic steps; halt at anything else."""
    while True:
        pending = [s for s in steps(slug) if not s["done"]]
        if not pending:
            print("\n  Pipeline complete.\n")
            return
        s = pending[0]
        if s["auto"] is None:
            print(f"\n  HALTED — {s['label']}")
            if s.get("stops"):
                print("  This step needs YOU. The showrunner will not cross "
                      "this line:\n  approval is a human decision, and "
                      "generation spends credits.")
            print("\n      " + s.get("human", "(manual step)") + "\n")
            return
        print(f"\n  -> {s['label']}")
        r = subprocess.run(s["auto"], cwd=ROOT)
        if r.returncode != 0:
            print(f"\n  FAILED at: {s['label']}")
            if s.get("human"):
                print("      " + s["human"])
            print()
            sys.exit(1)
        # qc is the terminal step and never marks itself done
        if s["key"] == "qc":
            print("\n  Pipeline complete through QC.\n")
            return


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("status", "next", "run"):
        sys.exit("usage: python3 tools/showrunner.py status|next|run <slug>")
    {"status": cmd_status, "next": cmd_next, "run": cmd_run}[sys.argv[1]](sys.argv[2])


if __name__ == "__main__":
    main()
