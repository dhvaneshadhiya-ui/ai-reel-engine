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

        # FALSE CORROBORATION, both shapes — advisory, never a refusal.
        # (a) "multi" off two articles on ONE domain
        (job / "research.md").write_text(RESEARCH.replace(
            "SRC: https://9to5mac.com/2026/08/10/iphone-18-pro/",
            "SRC: https://www.macrumors.com/2026/08/10/other-piece/"))
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
        rev = json.loads(rev_p.read_text())
        ok("multi-tier on one domain ADVISES",
           any("one outlet" in a for a in rev.get("research_advice", [])))
        # (b) two domains, but every SRC traces VIA the same leaker
        shared_via = RESEARCH.replace(
            "  SRC: https://www.macrumors.com/guide/iphone-18-pro/\n"
            "  SRC: https://9to5mac.com/2026/08/10/iphone-18-pro/",
            "  SRC: https://www.macrumors.com/guide/iphone-18-pro/\n"
            "  VIA: Fixed Focus Digital\n"
            "  SRC: https://9to5mac.com/2026/08/10/iphone-18-pro/\n"
            "  VIA: Fixed Focus Digital")
        (job / "research.md").write_text(shared_via)
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
        rev = json.loads(rev_p.read_text())
        ok("multi-tier with one shared VIA ADVISES (one source, two domains)",
           any("dressed as many" in a for a in rev.get("research_advice", [])))
        # (c) distinct VIAs = genuine corroboration, no advisory
        (job / "research.md").write_text(shared_via.replace(
            "  VIA: Fixed Focus Digital\n"
            "  SRC: https://9to5mac.com/2026/08/10/iphone-18-pro/\n"
            "  VIA: Fixed Focus Digital",
            "  VIA: Fixed Focus Digital\n"
            "  SRC: https://9to5mac.com/2026/08/10/iphone-18-pro/\n"
            "  VIA: Instant Digital"))
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
        rev = json.loads(rev_p.read_text())
        ok("distinct VIAs stay silent (genuine corroboration)",
           not any("dressed as many" in a
                   for a in rev.get("research_advice", [])))
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

        # 8b. The rehearsal advisory (2026-08-21) — printed by `check`, the
        # documented last command before generation, because that is the one
        # moment it can still save credits. Advice: check must still exit 0.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sa.cmd_check("selftest")
        ok("check ADVISES when the reel was never rehearsed",
           "NOT REHEARSED" in buf.getvalue())
        reh = tmp / "_sources" / "selftest" / "rehearsal"
        reh.mkdir(parents=True)
        (reh / "rehearsal-vo.wav").write_bytes(b"x")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sa.cmd_check("selftest")
        ok("check is quiet once rehearsal artifacts exist",
           "NOT REHEARSED" not in buf.getvalue())
    finally:
        sa.ROOT = REAL_ROOT

    # 9. Calibration staleness — the ⑤ mechanism. Runs against a THROWAWAY
    # corpus by repointing BOTH module ROOTs (corpus() reads approvals via
    # script_approval, the record lives under check_script.ROOT).
    cs_root = check_script.ROOT
    tmp2 = Path(tempfile.mkdtemp(prefix="calibration-selftest-"))
    (tmp2 / "tools").mkdir()
    check_script.ROOT = tmp2
    sa.ROOT = tmp2
    try:
        def approve_job(slug, text):
            j = tmp2 / "jobs" / slug
            j.mkdir(parents=True, exist_ok=True)
            (j / "script.md").write_text(text)
            (j / "approval.json").write_text(json.dumps(
                {"sha256": sa.sha(text)}))
        approve_job("one", "Apple ships a thing. You will notice it.")
        ok("status stale with no record",
           check_script.calibration_status() == 2)
        with contextlib.redirect_stdout(io.StringIO()):
            check_script.recalibrate()
        ok("status current after recalibrate",
           check_script.calibration_status() == 0)
        approve_job("two", "A second approved script. It says plain things.")
        ok("corpus growth turns status stale",
           check_script.calibration_status() == 2)
        with contextlib.redirect_stdout(io.StringIO()):
            check_script.recalibrate()
        # an approved script that uses a tell = the checker flagging the
        # user's own voice. Status must warn until a recalibration
        # knowingly accepts it — and go quiet after.
        approve_job("two", "This seamless upgrade is a plain thing.")
        ok("tell collision on an approved script turns status stale",
           check_script.calibration_status() == 2)
        with contextlib.redirect_stdout(io.StringIO()):
            check_script.recalibrate()
        ok("an ACCEPTED collision is quiet (recorded, not nagged)",
           check_script.calibration_status() == 0)
    finally:
        check_script.ROOT = cs_root
        sa.ROOT = REAL_ROOT

    # 10. render_job's draft plumbing (2026-08-21) — dry-run only, since a
    # real render needs footage. The invariant that matters: a draft can
    # never become a deliverable (renders to -draft.mp4, skips the master),
    # a partial render is draft-only, and the normal path is untouched.
    import subprocess
    rj = str(REAL_ROOT / "scripts/render_job.py")
    out = subprocess.run(
        [sys.executable, rj, "september-preview", "--dry-run", "--draft"],
        capture_output=True, text=True, cwd=REAL_ROOT).stdout
    ok("draft renders to -draft.mp4 at half scale",
       "-draft.mp4" in out and "--scale=0.5" in out)
    ok("draft skips the loudness master and the lint",
       "loudnorm" not in out and "lint_frames.py" not in out)
    full = subprocess.run(
        [sys.executable, rj, "september-preview", "--dry-run"],
        capture_output=True, text=True, cwd=REAL_ROOT).stdout
    ok("the full pipeline still masters and lints",
       "loudnorm" in full and "lint_frames.py" in full
       and "-final.mp4" in full)
    part = subprocess.run(
        [sys.executable, rj, "september-preview", "--dry-run",
         "--frames", "1-10"],
        capture_output=True, text=True, cwd=REAL_ROOT)
    ok("--frames without --draft refuses (no partial deliverables)",
       part.returncode != 0 and "partial" in (part.stderr + part.stdout))

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
