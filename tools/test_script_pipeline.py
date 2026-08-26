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

        # 3d-ii. Two ledger refusals that WORKED and were never tested, found
        # 2026-08-27 by listing research_check's refusal modes and diffing
        # against the cases here. An untested refusal is one edit away from
        # silently becoming an acceptance.
        (job / "research.md").write_text(
            "# Research\n## CLAIMS\n\n## SEARCHED\n- 2026-08-27 a query\n")
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses a ledger with no claims at all",
                    "NO CLAIMS RECORDED")
        (job / "research.md").write_text(RESEARCH.split("## SEARCHED")[0])
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses a ledger with no dated search log",
                    "NO SEARCH LOG")

        # 3e. THE HUMANIZER PASS (2026-08-27). Structure and ledger are now
        # both valid, so the only thing left is the half no checker measures.
        # It used to be cued only when a tic or an em-dash fired — meaning a
        # script with nothing measurable wrong never got a human ear, which is
        # exactly backwards. It is a precondition now, like the two above.
        (job / "research.md").write_text(RESEARCH)
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses without a humanizer pass", "NOT HUMANIZED")

        # The refusal must NAME the skill in backticks, or the PostToolUse
        # hook cannot fire on it and the refusal is just a printed reminder.
        _buf = io.StringIO()
        with contextlib.redirect_stdout(_buf), contextlib.suppress(SystemExit):
            sa.cmd_propose("selftest")
        ok("the refusal cues `humanizer` so the hook fires",
           "SKILL CUE" in _buf.getvalue() and "`humanizer`" in _buf.getvalue())

        # 3f. stamping the pass binds it to THIS draft's hash
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_humanized("selftest")
        rec_p = job / "humanized.json"
        ok("humanized.json is written", rec_p.exists())
        ok("the record hashes the script it covers",
           json.loads(rec_p.read_text()).get("sha")
           == sa.sha(sa.read_script("selftest")))

        # 4. filled structure + ledger + humanized -> propose runs
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
        rev_p = job / "review.json"
        ok("propose writes review.json", rev_p.exists())
        rev = json.loads(rev_p.read_text()) if rev_p.exists() else {}
        ok("review carries the script hash",
           rev.get("script_sha256") == sa.sha(sa.read_script("selftest")))

        # 4b. edit a word and the pass no longer covers what is being shown.
        # Same guarantee as approve-after-propose, one step earlier.
        _orig = (job / "script.md").read_text()
        (job / "script.md").write_text(_orig + "\nA sentence nobody read aloud.\n")
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "propose refuses an edit made after the humanizer pass",
                    "CHANGED SINCE THE HUMANIZER PASS")
        (job / "script.md").write_text(_orig)
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_propose("selftest")
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

        # 7. the compliant path after an edit: humanize the NEW words, record
        # that, re-propose, approve. Editing the script invalidates the pass
        # exactly as it invalidates the review — that is the point of both.
        expect_exit(lambda: sa.cmd_propose("selftest"),
                    "an edited script needs the pass run again",
                    "CHANGED SINCE THE HUMANIZER PASS")
        with contextlib.redirect_stdout(io.StringIO()):
            sa.cmd_humanized("selftest")
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

    # 11b. Provenance: the review record proves whether a beat plan was
    # shown at propose. The tmp job has no shot plan, so propose must both
    # SAY so and record zero — an approval can then never claim a plan was
    # seen when none existed.
    buf = io.StringIO()
    sa.ROOT = tmp
    try:
        with contextlib.redirect_stdout(buf):
            sa.cmd_propose("selftest")
        ok("propose SAYS when there is no shot plan",
           "NO SHOT PLAN YET" in buf.getvalue())
        rev = json.loads((tmp / "jobs/selftest/review.json").read_text())
        ok("review records beatPlanShots: 0 for a plan-less propose",
           rev.get("beatPlanShots") == 0)
    finally:
        sa.ROOT = REAL_ROOT

    # 11. The beat plan in the viewer's language (2026-08-21) — propose was
    # showing internal scene-type vocabulary ("generated MG", "✓ ✓ ?") as a
    # plan for the user to approve. beat_plan renders HEAR/SEE rows; the
    # cases pin the translations that make it readable.
    import beat_plan
    tmp3 = Path(tempfile.mkdtemp(prefix="beat-plan-selftest-"))
    j3 = tmp3 / "jobs" / "bp"
    j3.mkdir(parents=True)
    (tmp3 / "public/assets/bp").mkdir(parents=True)
    (tmp3 / "public/assets/bp/manifest.json").write_text(json.dumps(
        {"assets": [{"id": "clip-x",
                     "shows": "a red phone rotating on a turntable"}]}))
    (j3 / "shot-plan.json").write_text(json.dumps({"shots": [
        {"line": "The phone spins.",
         "scene": {"type": "footage",
                   "src": "assets/bp/clip-x.mp4", "credit": "@src"}},
        {"line": "The presenter explains.",
         "scene": {"type": "footage", "src": "assets/bp/avatar-master.mp4"}},
        {"line": "Three checks.",
         "scene": {"type": "checklist", "rows": [
             {"label": "Dark Cherry", "state": "done"},
             {"label": "Dark Gray", "state": "q"}]}},
        {"line": "Something exotic.",
         "scene": {"type": "walletattack"}},
    ]}))
    rows = "\n".join(beat_plan.render("bp", root=tmp3))
    ok("beat plan quotes the spoken line",
       "The phone spins." in rows)
    ok("beat plan uses the manifest's `shows`, not the filename",
       "a red phone rotating on a turntable" in rows)
    ok("the avatar clip reads as the presenter on camera",
       "the presenter, on camera" in rows)
    ok("checklist rows are spelled out with their marks",
       "Dark Cherry ✓" in rows and "Dark Gray ?" in rows)
    ok("an unknown type degrades to a flagged name, not silence",
       '"walletattack"' in rows)
    ok("no shot plan renders as empty, not a crash",
       beat_plan.render("nope", root=tmp3) == [])

    # 11a1. A HYPHEN-MERGED COMPOUND MUST STAY SEARCHABLE (2026-08-26).
    # load_words glues whisper's "-Chi" onto "Ming" for DISPLAY, then set the
    # searchable norm to normalize(text)[-1] — the last token only. So
    # "Ming-Chi" was findable only as "chi", and "co" + "-work," (which is what
    # the brand glossary's "co-work" pronunciation makes whisper emit for
    # Cowork) carried norm "work". Any start_phrase naming the compound failed
    # to resolve. Identical to the defect the comma branch directly below it
    # already records and fixes; the two were never fixed together.
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "_csp", str(REAL_ROOT / "scripts" / "compile_shot_plan.py"))
    _csp = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_csp)
    tmp_hy = Path(tempfile.mkdtemp(prefix="hyphen-selftest-")) / "vo.json"
    tmp_hy.write_text(json.dumps({"words": [
        {"word": "and", "start": 0.0, "end": 0.1},
        {"word": "co", "start": 0.1, "end": 0.2},
        {"word": "-work,", "start": 0.2, "end": 0.4},
        {"word": "Ming", "start": 0.5, "end": 0.6},
        {"word": "-Chi", "start": 0.6, "end": 0.8},
        {"word": "$2", "start": 1.0, "end": 1.1},
        {"word": ",000", "start": 1.1, "end": 1.3},
    ]}))
    hw = _csp.load_words(tmp_hy)
    norms = {w["text"]: w["norm"] for w in hw}
    ok("a hyphen-merged compound keeps its WHOLE searchable form",
       norms.get("co-work,") == "cowork")
    ok("the leaked case is really fixed, not special-cased",
       norms.get("Ming-Chi") == "mingchi")
    ok("display text still shows the original spelling",
       "co-work," in norms and "Ming-Chi" in norms)
    ok("the comma-merge branch it was copied from still works",
       norms.get("$2,000") == "2000")

    # 11a2. DELIVERY RATE IS KEYED TO THE LOCKED VOICE SPEED (2026-08-26).
    # The old constants were measured at speed 1.05 and kept being applied
    # after the locked speed moved to 1.12, which cost claude-memory-everywhere
    # a whole section of its source announcement — cut at rehearsal to fit a
    # runtime limit that did not exist. These pin that a speed with no
    # measurement can never resolve SILENTLY to another speed's numbers.
    import script_approval as _sa
    lo105, hi105, why105 = _sa.WPS_BY_SPEED[1.05][0], _sa.WPS_BY_SPEED[1.05][1], ""
    ok("the 1.05 measurements are unchanged", (lo105, hi105) == (2.35, 2.75))
    ok("1.12 has its own measured row", 1.12 in _sa.WPS_BY_SPEED)
    ok("the 1.12 row is faster than the 1.05 row",
       _sa.WPS_BY_SPEED[1.12][0] > _sa.WPS_BY_SPEED[1.05][0])
    ok("every row carries its provenance",
       all(isinstance(v[2], str) and len(v[2]) > 20
           for v in _sa.WPS_BY_SPEED.values()))
    _speed = _sa.locked_speed
    try:
        _sa.locked_speed = lambda: 1.12
        r = _sa.wps_range()
        ok("a measured speed resolves to its own row and says so",
           r[0] == 2.60 and "speed 1.12" in r[2] and "NO MEASUREMENT" not in r[2])
        _sa.locked_speed = lambda: 1.40
        r = _sa.wps_range()
        ok("an UNMEASURED speed falls back LOUDLY, never silently",
           "NO MEASUREMENT AT SPEED 1.4" in r[2])
        ok("the loud fallback still returns a usable range",
           r[0] > 0 and r[1] > r[0])
    finally:
        _sa.locked_speed = _speed

    # 11b. SCREENSHOT BEATS MUST DESCRIBE THEMSELVES (2026-08-26). sourceread /
    # annotatezoom / receipt rendered FIXED strings naming the camera move
    # ("a screenshot, zooming slowly into the highlighted region") and nothing
    # on the page — the same fault the floatcard note in beat_plan.py records,
    # but reached 70% of one reel's beats. They now resolve the manifest asset
    # and name the claim; and a repeat of one asset shortens instead of
    # re-printing a 60-word `shows` four times.
    tmp4 = Path(tempfile.mkdtemp(prefix="beat-plan-shot-selftest-"))
    j4 = tmp4 / "jobs" / "bp2"
    j4.mkdir(parents=True)
    (tmp4 / "public/assets/bp2").mkdir(parents=True)
    (tmp4 / "public/assets/bp2/manifest.json").write_text(json.dumps(
        {"assets": [
            {"id": "docs-page", "kind": "receipt",
             "shows": ("the vendor changelog, headed 'What is new', with the "
                       "deprecation notice printed directly under it, then a "
                       "table of every removed flag with its replacement, its "
                       "removal version and a migration note, running to the "
                       "fold")},
            {"id": "docs-page-two", "kind": "receipt",
             "shows": "a different page entirely, showing the pricing table"},
        ]}))
    (j4 / "shot-plan.json").write_text(json.dumps({"shots": [
        {"line": "They deprecated it.",
         "scene": {"type": "sourceread", "src": "assets/bp2/docs-page.png",
                   "covers": "they deprecated it", "credit": "@vendor"}},
        {"line": "And here is the flag.",
         "scene": {"type": "annotatezoom", "src": "assets/bp2/docs-page.png",
                   "covers": "here is the flag"}},
        {"line": "Pricing moved too.",
         "scene": {"type": "receipt", "src": "assets/bp2/docs-page-two.png",
                   "covers": "pricing moved"}},
    ]}))
    rows4 = beat_plan.render("bp2", root=tmp4)
    joined4 = "\n".join(rows4)
    ok("a sourceread names the artefact, not just the camera move",
       "the vendor changelog" in rows4[1])
    ok("a still reads as a screenshot, never as 'a clip'",
       "a screenshot" in rows4[1] and "a clip" not in joined4)
    ok("the beat names the claim its highlight proves",
       "they deprecated it" in rows4[1] and "here is the flag" in rows4[3])
    ok("a long `shows` is cut to its gist, not printed whole",
       "running to the fold" not in joined4)
    ok("the SECOND beat on one asset shortens instead of repeating it",
       "the same screenshot again" in rows4[3]
       and "running to the fold" not in rows4[3])
    ok("a shortened repeat still names WHICH asset it is",
       "the vendor changelog" in rows4[3] and rows4[3].count("…") >= 1)
    ok("a DIFFERENT asset is still described in full",
       "the pricing table" in rows4[5])
    ok("the fixed camera-move string is gone",
       "zooming slowly into the highlighted region" not in joined4)

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

    # 11. find_phrase tolerates whisper's compound splits (2026-08-25:
    # "README" transcribed as "read me" left shot 5 of claude-eating-tokens
    # unresolvable). One needle token may span consecutive transcript tokens
    # whose concatenation equals it — and the reverse join — while a phrase
    # that genuinely is not in the transcript must still refuse.
    print("\n  -- compile_shot_plan phrase matcher --")
    sys.path.insert(0, str(REAL_ROOT / "scripts"))
    import compile_shot_plan as csp
    tw = [{"norm": n} for n in
          "but its read me admits input is untouched".split()]
    s, e = csp.find_phrase(tw, "But its README admits", 0, "selftest")
    ok("compound split resolves (README == read+me)", (s, e) == (0, 4))
    s, e = csp.find_phrase(tw, "read me admits", 0, "selftest")
    ok("exact match still resolves at the right span", (s, e) == (2, 4))
    tw2 = [{"norm": n} for n in "run npx ccusage monthly today".split()]
    s, e = csp.find_phrase(tw2, "npx cc usage monthly", 0, "selftest")
    ok("reverse join resolves (cc+usage == ccusage)", (s, e) == (1, 3))
    expect_exit(lambda: csp.find_phrase(tw, "words never spoken", 0, "x"),
                "an absent phrase still refuses", "could not resolve")
    # STYLE FOLLOWS FORMAT. CLAUDE.md's locked table says editorial = news /
    # comparison and utility = top5 / ai-tools, and "loaded every session"
    # was treated as enforcement — it is not. claude-eating-tokens rendered
    # its whole ai-tools reel in the editorial pack across several renders
    # before anyone measured it (2026-08-25). The mapping now lives in
    # compile_shot_plan; this is what keeps it there.
    print("\n  -- style follows format --")
    for fmt, want in (("ai-tools", "utility"), ("top5", "utility"),
                      ("news", None), ("comparison", None)):
        beats = {"style": "editorial", "format": fmt}
        plan = {"format": fmt}
        if plan.get("style"):
            got = plan["style"]
        elif beats.get("format") in ("top5", "ai-tools"):
            got = "utility"
        else:
            got = beats["style"]
        ok(f"{fmt} -> {want or 'editorial'} pack",
           got == (want or "editorial"))
    src = (REAL_ROOT / "scripts/compile_shot_plan.py").read_text()
    ok("compile_shot_plan carries the mapping (not just this test)",
       'beats.get("format") in ("top5", "ai-tools")' in src
       and 'beats["style"] = "utility"' in src)
    ok("an explicit plan style still wins",
       'if plan.get("style"):' in src)

    # caption_corrections phrase keys must survive whisper's punctuation:
    # "see use it" -> "ccusage" silently did nothing against the chunk
    # "see, use it" (2026-08-25, found in a RENDERED frame).
    fixed = csp._apply_phrases("One, see, use it charts.",
                               {"see use it": "ccusage"})
    ok("phrase fix tolerates punctuation inside the chunk",
       fixed == "One, ccusage charts.")
    ok("phrase fix leaves an honest chunk alone",
       csp._apply_phrases("see it works", {"see use it": "x"})
       == "see it works")

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
