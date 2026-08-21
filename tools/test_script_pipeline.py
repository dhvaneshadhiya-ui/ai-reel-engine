#!/usr/bin/env python3
"""Self-test for the script pipeline's MECHANICAL rules.

Covers the enforcement added 2026-08-21 — the third time a weak first draft
reached the user while every piece of guidance sat unread:

  1. propose refuses a job with no structure.md            (framework S17)
  2. propose refuses a structure.md that is still template
  3. propose refuses a structure.md naming no S17 shape
  4. propose, on success, writes review.json with the script's hash
  5. approve refuses when propose never ran
  6. approve refuses when the script changed after propose
  7. approve succeeds on a fresh propose
  8. check_script's own selftest (structure thresholds + AI tells)

Every rule here is a gate with a failing case, per CLAUDE.md. The suite runs
against a THROWAWAY job in a temp dir by repointing script_approval.ROOT —
nothing under jobs/ is touched.

    python3 tools/test_script_pipeline.py
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_script  # noqa: E402
import script_approval as sa  # noqa: E402

REAL_ROOT = sa.ROOT
CHECKS = 0
FAILED = False


def ok(label: str, cond: bool) -> None:
    global CHECKS, FAILED
    CHECKS += 1
    print(f"  {'ok  ' if cond else 'FAIL'} {label}")
    FAILED = FAILED or not cond


def expect_exit(fn, label: str, want_text: str) -> None:
    """The command must sys.exit with a message containing want_text."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn()
    except SystemExit as e:
        msg = str(e)
        ok(f"{label} (mentions {want_text!r})", want_text in msg)
        return
    ok(f"{label} — DID NOT REFUSE", False)


SCRIPT = ("Apple's iPhone 18 Pro is expected on September 9. And one rumored "
          "change only matters when you have no signal. Start with the shape "
          "of it. You will notice the difference on a bad day.")

STRUCTURE = """# Structure — selftest
## SHAPE (S17)
Discovery — there is a real mystery in the material.
## PROMISE (S2)
The viewer learns what the change is and when it lands.
## OPEN LOOP (S10)
Planted: sentence two. Paid off: the ending returns to it.
## SOURCES
MacRumors guide; Ming-Chi Kuo note.
"""


RESEARCH = """# Research — selftest

## CLAIMS

- CLAIM: the iPhone 18 Pro is expected in September
  TIER: multi
  SPOKEN: "is expected on September 9"
  SRC: https://www.macrumors.com/guide/iphone-18-pro/
  SRC: https://9to5mac.com/2026/08/10/iphone-18-pro/

- CLAIM: one rumored change only matters with no signal
  TIER: single
  SPOKEN: "only matters when you have no signal"
  SRC: https://www.macrumors.com/guide/iphone-18-pro/

## SEARCHED

- 2026-08-21  "iphone 18 pro september"  (freshness re-check)
"""


def run() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="script-pipeline-selftest-"))
    job = tmp / "jobs" / "selftest"
    job.mkdir(parents=True)
    sa.ROOT = tmp
    try:
        (job / "script.md").write_text(SCRIPT)

        # 1. no structure.md at all
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses with no structure.md", "NO STRUCTURE")

        # 2. structure.md still a template
        (job / "structure.md").write_text(
            "# Structure\n## SHAPE (S17)\nDiscovery\n"
            "## PROMISE\n<what the viewer gets>\n")
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses unfilled placeholders", "TEMPLATE")

        # 3. no S17 shape named
        (job / "structure.md").write_text(
            "# Structure\nA promise and a loop, but no shape word.\n")
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses when no shape is named", "NO SHAPE")

        # 3b. structure is fine but there is no research ledger.
        # The ledger rule shipped without a case here, so the suite failed on
        # its own fixture instead of on a violation — doctor went red for a
        # missing test file, not a broken rule. Added 2026-08-21.
        (job / "structure.md").write_text(STRUCTURE)
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses with no research.md", "NO RESEARCH LEDGER")

        # 3c. ledger still a template
        (job / "research.md").write_text(
            "# Research\n## CLAIMS\n- CLAIM: <the claim>\n  TIER: multi\n"
            "  SPOKEN: \"x\"\n  SRC: https://a.com\n## SEARCHED\n- 2026 q\n")
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses a template ledger", "TEMPLATE")

        # 3d. SPOKEN words the script never says — a ledger describing a
        # script that does not exist is fiction wearing a record's badge
        (job / "research.md").write_text(RESEARCH.replace(
            '"is expected on September 9"', '"ships worldwide tomorrow"'))
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses SPOKEN words not in the script",
                    "not in the script")

        # 4. filled structure + ledger -> propose runs and records the review
        (job / "research.md").write_text(RESEARCH)
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
        rev_p = job / "review.json"
        ok("propose writes review.json", rev_p.exists())
        rev = json.loads(rev_p.read_text()) if rev_p.exists() else {}
        ok("review carries the script hash",
           rev.get("script_sha256") == sa.sha(sa.read_script("selftest")))
        # An UNHEDGED single-source claim must ADVISE (recorded in the
        # review) while propose still succeeds — advice, never a block.
        # The claim sits at the script's tail, clear of the opening's
        # "expected": the hedge window is +/-12 words on purpose (a hedge
        # one clause away covers — "None of it's official ..."), so a test
        # claim adjacent to someone else's hedge would never fire.
        # INSERTED before ## SEARCHED, not appended: parse_ledger only reads
        # claims inside the CLAIMS section, and the first draft of this case
        # appended after the section boundary — the claim silently did not
        # exist and the case failed on its own fixture.
        (job / "research.md").write_text(RESEARCH.replace("## SEARCHED", """\
- CLAIM: you will notice this on a bad day
  TIER: single
  SPOKEN: "notice the difference on a bad day"
  SRC: https://www.macrumors.com/guide/iphone-18-pro/

## SEARCHED"""))
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
        rev = json.loads(rev_p.read_text())
        ok("unhedged single-source claim ADVISES, does not refuse",
           any("UNHEDGED" in a for a in rev.get("research_advice", [])))
        (job / "research.md").write_text(RESEARCH)   # restore

        # 5. approve without a propose (fresh job, no review)
        job2 = tmp / "jobs" / "never-proposed"
        job2.mkdir()
        (job2 / "script.md").write_text(SCRIPT)
        (job2 / "structure.md").write_text(STRUCTURE)
        (job2 / "research.md").write_text(RESEARCH)
        expect_exit(lambda: sa.cmd_approve("never-proposed"),
                    "approve refuses when propose never ran", "NEVER PROPOSED")

        # 6. script edited after propose -> stale review
        (job / "script.md").write_text(SCRIPT + " One extra sentence.")
        expect_exit(lambda: sa.cmd_approve("selftest"),
                    "approve refuses a script edited after propose",
                    "CHANGED SINCE IT WAS PROPOSED")

        # 7. re-propose, then approve — the compliant path stays open
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
            sa.cmd_approve("selftest")
        ok("approve succeeds on a fresh propose",
           (job / "approval.json").exists())
    finally:
        sa.ROOT = REAL_ROOT

    # 8. check_script's own selftest — structure thresholds + AI tells.
    print("\n  -- check_script selftest --")
    rc = check_script.selftest()
    ok("check_script selftest passes", rc == 0)

    print(f"\nall {CHECKS} checks "
          f"{'passed' if not FAILED else 'DID NOT pass'} — the script "
          "pipeline's mechanical rules each refuse their violation.")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(run())
