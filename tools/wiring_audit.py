#!/usr/bin/env python3
"""Is every tool actually WIRED, or just present?

WHY: this repo keeps discovering capabilities that exist, are documented, and
have never once executed — the humanizer pass (2026-08-26), the style
mapping, the capture defaults, the framework stance. Each was found by
accident. A tool nobody calls and nobody is told to call is indistinguishable
from a tool that was never written, except that it lets everyone believe the
work is being done.

Every tool lands in exactly one bucket:

  AUTO     another program executes it — a subprocess call or an import.
  MANUAL   a human or agent runs it, and a doc SAYS SO by name. Legitimate,
           but only when the instruction actually exists somewhere.
  ORPHAN   nothing runs it and nothing tells anyone to. These are the bugs.

    python3 tools/wiring_audit.py [--verbose]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE_DIRS = ["tools", "scripts"]
DOCS = ["CLAUDE.md", "AGENT.md", "RULES.md", "PIPELINE.md", "MIGRATION.md",
        "README.md", "STYLE-RULES.md"]
# Runnable by a person by design; not pipeline stages.
ENTRYPOINTS = {"doctor.py", "showrunner.py", "new_job.py", "render_job.py",
               "smoke_test.py", "reelkit.py", "wiring_audit.py"}
# LEGACY: one-off scripts kept as the record of a SHIPPED reel, or a
# migration that has already run. They are supposed to be inert. Naming them
# is what stops "12 orphans" from becoming background noise that hides a real
# gap — the exact way the humanizer stayed invisible.
LEGACY_PATTERNS = (
    r"^build_",          # per-reel bespoke builders, superseded by compile_shot_plan
    r"^finalize_",       # per-reel finishing passes
    r"^example_",        # documentation samples
    r"^migrate_",        # one-time migrations, already applied
    r"^gen_chips_", r"^make_mg_", r"^fix_still_",   # one-reel asset helpers
)


def main() -> int:
    verbose = "--verbose" in sys.argv
    files = sorted(p for d in CODE_DIRS for p in (ROOT / d).glob("*.py"))
    # every byte of code + docs, once
    code_blob = {p: p.read_text(errors="ignore") for p in files}
    for extra in ROOT.glob("*.sh"):
        code_blob[extra] = extra.read_text(errors="ignore")
    docs_blob = "\n".join((ROOT / d).read_text(errors="ignore")
                          for d in DOCS if (ROOT / d).exists())

    # DOC/CODE DRIFT (2026-08-26). CLAUDE.md said "Gate G23 rejects an
    # unmeasured format outright" and RULES.md said "Unknown format = G23
    # blocks". G23 is ADVICE and always was — the constitution only lets the
    # three rules, RENDER and RIGHTS block. A doc that promises enforcement
    # the code does not perform is worse than no doc: it is why a rule gets
    # trusted instead of checked. STYLE-RULES is excluded on purpose — it is
    # an append-only dated ledger, so its old entries are records of what was
    # true then, not live claims.
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import reel_gates as _rg
        blocking = set(_rg.BLOCKING_RULES)
        every_gate = set(re.findall(r"\bG\d{2}\b",
                                   (ROOT / "tools/reel_gates.py").read_text()))
    except Exception:                                      # noqa: BLE001
        blocking, every_gate = set(), set()
    # The verb must sit right after the gate id, so "G48 blocks; G49 advises"
    # and "never one long block. [GATE:G06]" are not mistaken for claims.
    CLAIM = re.compile(r"\b(G\d{2})\b[^.;\n]{0,24}?"
                       r"\b(blocks?|rejects?|refuses?|stops?)\b", re.I)
    NEGATED = re.compile(r"\b(cannot|can not|never|does not|doesn't|"
                         r"no longer|not)\b", re.I)
    drift = []
    for doc in ("CLAUDE.md", "RULES.md", "AGENT.md", "PIPELINE.md"):
        f = ROOT / doc
        if not f.exists():
            continue
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            for m in CLAIM.finditer(line):
                gate = m.group(1)
                # "G23 advises (it cannot block)" is a correct sentence, not a
                # false claim. Skip a negated verb.
                if NEGATED.search(m.group(0)):
                    continue
                if gate in every_gate and gate not in blocking:
                    drift.append((doc, n, gate, line.strip()[:88]))

    # SELF-TESTS NOBODY RUNS (2026-08-26). check_frame_contract and notation
    # each had a working --selftest that no program called, found only by
    # listing every selftest and diffing against doctor. A self-test nobody
    # runs is identical to no self-test, while looking like coverage.
    doctor_txt = (ROOT / "scripts" / "doctor.py").read_text(errors="ignore")
    selftests, unrun = [], []
    for p_ in files:
        if p_.name.startswith("test_"):
            continue                       # these ARE suites; AUTO covers them
        if '"--selftest"' not in code_blob[p_]:
            continue
        selftests.append(p_.name)
        if p_.stem not in doctor_txt:
            unrun.append(p_.name)

    # HOOKS (2026-08-26). A hook script that settings.json does not name is
    # exactly the bug this tool exists for, one folder over: present,
    # plausible, never executed. And a hook is the only thing here that can
    # fire a SKILL, so an unwired one silently removes a trigger.
    hooks_dir = ROOT / ".claude" / "hooks"
    settings_f = ROOT / ".claude" / "settings.json"
    settings_txt = settings_f.read_text(errors="ignore") if settings_f.exists() else ""
    unwired = [h.name for h in sorted(hooks_dir.glob("*.py"))
               if h.name not in settings_txt] if hooks_dir.exists() else []
    hook_count = len(list(hooks_dir.glob("*.py"))) if hooks_dir.exists() else 0

    auto, manual, orphan, legacy = [], [], [], []
    for p in files:
        name = p.name
        stem = p.stem
        if name.startswith("__"):
            continue
        called = False
        for other, text in code_blob.items():
            if other == p:
                continue
            if name in text or re.search(rf"\b(import|from)\s+{stem}\b", text):
                called = True
                break
        documented = re.search(rf"\b{re.escape(stem)}(\.py)?\b", docs_blob)
        if called:
            auto.append(name)
        elif name in ENTRYPOINTS or documented:
            manual.append(name)
        elif any(re.match(pat, name) for pat in LEGACY_PATTERNS):
            legacy.append(name)
        else:
            orphan.append(name)

    print(f"\n=== WIRING AUDIT — {len(files)} tools ===\n")
    print(f"  AUTO   {len(auto):3}  executed by other code")
    print(f"  MANUAL {len(manual):3}  run by hand, and a doc names them")
    print(f"  LEGACY {len(legacy):3}  one-off/shipped-reel scripts, inert by design")
    print(f"  ORPHAN {len(orphan):3}  nothing runs them, nothing mentions them")
    if verbose:
        for label, group in (("AUTO", auto), ("MANUAL", manual)):
            print(f"\n  -- {label} --")
            for n in group:
                print(f"     {n}")
    print(f"\n  DOCS   {len(blocking):3}  gates block; binding docs checked "
          f"for false 'this blocks' claims")
    if drift:
        print("\n  DOC/CODE DRIFT — a doc promises enforcement the code "
              "does not perform:")
        for doc, n, gate, line in drift:
            print(f"     {doc}:{n}  {gate} is ADVICE — {line}")
        print()
        return 1

    print(f"\n  SELFTEST {len(selftests):3}  tools with a --selftest, "
          f"{len(selftests) - len(unrun)} of them run by doctor")
    if unrun:
        print("\n  SELF-TESTS NOBODY RUNS — coverage that never executes:")
        for n in unrun:
            print(f"     {n}")
        print()
        return 1

    print(f"\n  HOOKS  {hook_count:3}  in .claude/hooks, "
          f"{hook_count - len(unwired)} wired into settings.json")
    if unwired:
        print("\n  UNWIRED HOOKS — present but never fired:")
        for n in unwired:
            print(f"     {n}")
        print()
        return 1

    if orphan:
        print("\n  ORPHANS — each is either dead code or a silent gap:")
        for n in orphan:
            print(f"     {n}")
        print()
        return 1
    print("\n  Every tool is either executed by the pipeline or named in a\n"
          "  document that tells a person to run it.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
