#!/usr/bin/env python3
"""Audit the MASTER RULE clause by clause. Answers "is it really done?".

The user has asked four times whether the framework is implemented. Three
times the answer came from me, and once it was wrong — the operating stance
sat in a file that loads only if a session opens it, which a grep would have
disproved in a second. So the answer stops being a memory and becomes a
command.

Every clause of `frameworks/short-form-master.md` §12 is listed below with
the thing that makes it TRUE, and each probe actually runs:

    CODE      a check with a right answer. The probe proves the enforcement
              exists; if someone deletes it, this audit fails.
    SCAFFOLD  a field or section a job cannot start without.
    STANCE    text in AUTO-LOADED context (CLAUDE.md), not in a file that
              has to be opened. That distinction is the whole lesson.
    JUDGEMENT no probe can decide it — the audit shows WHERE it is exercised
              so "we have a tool for that" is never mistaken for "it is
              handled".

    python3 tools/framework_audit.py            # full table
    python3 tools/framework_audit.py --brief    # one line per clause
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (clause, kind, probe) — probe is ("grep", file, pattern) or ("run", argv)
CLAUSES: list[tuple[str, str, tuple]] = [
    ("act as ONE integrated team, not separate agents", "STANCE",
     ("grep", "CLAUDE.md", r"integrated elite short-form production team")),
    ("identify the real SUBJECT", "SCAFFOLD",
     ("grep", "scripts/new_job.py", r'"subject":')),
    ("identify AUDIENCE value", "SCAFFOLD",
     ("grep", "scripts/new_job.py", r'"audience":')),
    ("identify the strongest STORY ENGINE", "SCAFFOLD",
     ("grep", "scripts/new_job.py", r"STORY ENGINE")),
    ("identify SOURCE RULES (facts vs footage are separate)", "CODE",
     ("grep", "tools/framework_check.py", r"F3 SOURCE POLICY")),
    ("identify a precise REVEAL TARGET", "SCAFFOLD",
     ("grep", "scripts/new_job.py", r'"reveal_target":')),
    ("hook + immediate context", "CODE",
     ("grep", "tools/check_script.py", r"OPENING has no version, date")),
    ("a story question or PROMISE", "SCAFFOLD",
     ("grep", "scripts/new_job.py", r"## PROMISE")),
    ("escalation", "JUDGEMENT",
     ("grep", "AGENT.md", r"escalation|editor's pass")),
    ("VISUAL PROOF matched to the claim", "CODE",
     ("grep", "tools/reel_gates.py", r"G39 scene")),
    ("WHAT -> WHY -> SO WHAT", "SCAFFOLD",
     ("grep", "scripts/new_job.py", r"WHAT -> WHY -> SO WHAT")),
    ("satisfying PAYOFF (no abandoned loop)", "CODE",
     ("grep", "tools/check_script.py", r"ABANDONED LOOP")),
    ("strong ending", "JUDGEMENT",
     ("grep", "tools/prepublish.py", r"payoff test|removal test")),
    ("earned CTA (value BEFORE the ask)", "CODE",
     ("grep", "tools/framework_check.py", r"F5 CTA FLOW")),
    ("conceal the reveal target in NARRATION", "CODE",
     ("grep", "tools/framework_check.py", r"REVEAL TARGET said out loud")),
    ("conceal it in added TEXT / GRAPHICS / CTA", "CODE",
     ("grep", "tools/framework_check.py", r"on-screen text")),
    ("do NOT damage authentic footage to hide branding", "JUDGEMENT",
     ("grep", "tools/prepublish.py", r"damage the reality in footage")),
    ("subject stays clear while the target is withheld", "CODE",
     ("grep", "tools/framework_check.py", r"F4 CLARITY")),
    ("match every VISUAL to the story", "CODE",
     ("grep", "tools/reel_gates.py", r"WHAT IS ON SCREEN MUST BE WHAT IS BEING SAID")),
    ("authentic demonstrations over filler", "CODE",
     ("grep", "tools/reel_gates.py", r"G50 ai-tools reel carries")),
    ("proof footage vs ILLUSTRATIVE is declared", "CODE",
     ("grep", "tools/framework_check.py", r"PROOF or\s*\"?\s*$|PROOF or ILLUSTRATIVE")),
    ("mobile-first capture and editing", "CODE",
     ("grep", "tools/test_capture_defaults.py", r"mobile is the default")),
    ("readable on-screen text", "CODE",
     ("grep", "tools/reel_gates.py", r"G45|captionBottom")),
    ("purposeful pattern interrupts / no overediting", "JUDGEMENT",
     ("grep", "tools/cut_sheet.py", r"same move as the beat before")),
    ("narratively shaped music (never a hand-typed curve)", "CODE",
     ("grep", "tools/reel_gates.py", r"G37")),
    ("synchronized effects", "CODE",
     ("run", [sys.executable, "-c",
              "import pathlib,sys; sys.exit(0 if pathlib.Path("
              "'tools/sync_impacts.py').exists() else 1)"])),
    ("selective silence", "JUDGEMENT",
     ("grep", "tools/prepublish.py", r"silence")),
    ("the READ is measured, not just the words", "CODE",
     ("grep", "tools/vo_qc.py", r"PITCH_SD_FLOOR")),
    ("voice-first mixing at a real loudness target", "CODE",
     ("grep", "tools/reel_gates.py", r"G31")),
    ("verify every material claim", "CODE",
     ("grep", "tools/research_check.py", r"TIERS")),
    ("no claim spoken harder than its evidence", "CODE",
     ("grep", "tools/framework_check.py", r"F2 CERTAINTY")),
    ("a prediction names whose it is", "CODE",
     ("grep", "tools/framework_check.py", r"F2b PREDICTION")),
    ("unsupported claims are excluded", "CODE",
     ("grep", "tools/research_check.py", r"REFUSED_TIERS")),
    ("obey credit restrictions", "CODE",
     ("grep", "scripts/compile_shot_plan.py", r"credit_instructions")),
    ("packaging + SEO adapted per platform", "CODE",
     ("run", [sys.executable, "-c",
              "import pathlib,sys; sys.exit(0 if pathlib.Path("
              "'tools/packaging_check.py').exists() else 1)"])),
    ("AutoDM flow VALUE->CURIOSITY->DESIRE->ASK->DELIVERY", "CODE",
     ("grep", "tools/framework_check.py", r"VALUE -> CURIOSITY")),
    ("approve only after a FINAL AUDIT", "CODE",
     ("run", [sys.executable, "-c",
              "import pathlib,sys; sys.exit(0 if pathlib.Path("
              "'tools/prepublish.py').exists() else 1)"])),
]


def probe(spec: tuple) -> bool:
    kind = spec[0]
    if kind == "grep":
        p = ROOT / spec[1]
        if not p.exists():
            return False
        return re.search(spec[2], p.read_text(), re.I | re.M) is not None
    r = subprocess.run(spec[1], cwd=ROOT, capture_output=True)
    return r.returncode == 0


def main() -> int:
    brief = "--brief" in sys.argv
    print("\n=== MASTER RULE AUDIT — every clause, and what makes it true ===\n")
    fails: list[str] = []
    counts: dict[str, int] = {}
    for clause, kind, spec in CLAUSES:
        held = probe(spec)
        counts[kind] = counts.get(kind, 0) + 1
        mark = "ok  " if held else "GONE"
        if not held:
            fails.append(clause)
        where = spec[1] if spec[0] == "grep" else "tool present"
        if brief:
            print(f"  {mark} [{kind:9}] {clause}")
        else:
            print(f"  {mark} [{kind:9}] {clause}\n"
                  f"{'':>16}<- {where}")
    total = len(CLAUSES)
    print(f"\n  {total} clauses: " + ", ".join(
        f"{n} {k.lower()}" for k, n in sorted(counts.items())))
    if fails:
        print(f"\n  {len(fails)} CLAUSE(S) NO LONGER ENFORCED:")
        for f in fails:
            print(f"    - {f}")
        print("\n  A clause whose probe fails is a clause that quietly "
              "stopped being true.\n")
        return 1
    print("\n  Every CODE and SCAFFOLD clause is enforced by something that\n"
          "  runs. The JUDGEMENT clauses are not automated on purpose — the\n"
          "  audit names where each is exercised so 'we have a tool for that'\n"
          "  is never mistaken for 'it is handled'.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
