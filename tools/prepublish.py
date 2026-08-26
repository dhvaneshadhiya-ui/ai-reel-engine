#!/usr/bin/env python3
"""The framework's §11 pre-publish audit, as one command.

`frameworks/short-form-master.md` ends with an instruction, not a suggestion:
*"Approve only when facts, clarity, retention, visuals, audio, platform fit,
CTA, reveal handling, and overall coherence pass a final audit."* Every piece
of that audit existed here in some tool or other; the AUDIT did not. Nothing
gathered them, so "it passed" meant "nobody found anything", which is not the
same sentence.

Two halves, and the split is the honest part:

  MEASURED   — run now, pass or fail, no opinion involved.
  JUDGEMENT  — printed as questions, because a machine cannot answer them and
               pretending otherwise is how taste ends up wearing a rule's
               badge (the G18 lesson). They are the framework's own story
               tests and coherence checks, asked out loud so the answer is
               deliberate.

    python3 tools/prepublish.py <slug>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MEASURED = [
    ("facts + reveal + source policy", "tools/framework_check.py", []),
    ("claim ledger", "tools/research_check.py", []),
    ("script approval is fresh", "tools/script_approval.py", ["check"]),
    ("gates (render + rights + the three rules)", "tools/reel_gates.py", []),
    ("packaging limits", "tools/packaging_check.py", []),
]

# The framework's §11 items no tool can answer. Phrased as the question, not
# as a checkbox, so a yes has to be earned.
JUDGEMENT = [
    ("STORY", "Could a first-time viewer explain the subject, the point, and "
              "the current story question? (confused-viewer test)"),
    ("STORY", "Does this sound like a spoken story, or an article read "
              "aloud? (boring-article test)"),
    ("STORY", "Did every promise and open loop get a useful answer? "
              "(payoff test)"),
    ("STORY", "Can any sentence or shot disappear without loss? Then it "
              "should. (removal test)"),
    ("RETENTION", "Does every shot earn the next moment, and does the "
                  "escalation add proof or stakes rather than more facts?"),
    ("VISUAL", "Is every claim on screen at the moment it is spoken, and is "
               "proof footage distinguishable from illustration?"),
    ("VISUAL", "Could a silent viewer follow the essential story?"),
    ("AUDIO", "Is the voice always intelligible on a phone speaker, and is "
              "any silence intentional rather than an error?"),
    ("CTA", "Is the ask earned by value already delivered, and does the "
            "delivery contain exactly what was promised?"),
    ("REVEAL", "Has authentic footage been left alone? The rule is hide the "
               "identity in NARRATION, never damage the reality in footage to "
               "hide incidental branding."),
    ("REVEAL", "If branding is naturally visible, does the promised reveal "
               "still mean anything — or should the offer be redefined?"),
    ("COHERENCE", "Do research, story, edit, audio and CTA read as ONE "
                  "decision — or as departments that never spoke?"),
]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.split("    python3")[0].strip())
        return 1
    slug = sys.argv[1]
    print(f"\n=== PRE-PUBLISH AUDIT — {slug} ===\n")
    print("-- measured --")
    failed: list[str] = []
    for label, tool, extra in MEASURED:
        path = ROOT / tool
        if not path.exists():
            print(f"  skip  {label} (no {tool})")
            continue
        cmd = [sys.executable, str(path)] + extra + [slug]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        if r.returncode == 0:
            print(f"  ok    {label}")
        else:
            failed.append(label)
            tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
            print(f"  FAIL  {label}")
            for line in tail[-3:]:
                print(f"          {line.strip()[:96]}")

    if any("packaging" in f for f in failed):
        print("\n  SKILL CUE: packaging is written with the `social` and "
              "`caption-and-hashtags`\n  skills (and `youtube-seo` for the "
              "Shorts title/description). Nothing\n  invokes them — naming "
              "them here is the trigger.")

    print("\n-- judgement (answer these; nothing here can) --")
    group = None
    for g, q in JUDGEMENT:
        if g != group:
            print(f"\n  [{g}]")
            group = g
        print(f"    - {q}")

    print()
    if failed:
        print(f"  NOT READY — {len(failed)} measured check(s) failed: "
              f"{', '.join(failed)}\n")
        return 1
    print("  Measured checks pass. The judgement list is the actual gate —\n"
          "  the framework approves on the whole experience, not the parts.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
