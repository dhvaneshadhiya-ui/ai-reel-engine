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
import json
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


# A stage whose artifact new_job.py SCAFFOLDS cannot use exists() as its done
# test — the file is born, the work is not. Found 2026-08-21, the day the
# scaffolds landed and three stages lit up green on an empty job. The done
# tests below share their definitions with the tools that enforce them.

def _structure_done(slug: str) -> bool:
    sys.path.insert(0, str(_p("tools")))
    from script_approval import structure_problems  # noqa: E402
    return _p(f"jobs/{slug}/structure.md").exists() \
        and not structure_problems(slug)


def _research_done(slug: str) -> bool:
    """Structural half only — SPOKEN is verified against the script at
    propose, which may not exist yet at this stage."""
    sys.path.insert(0, str(_p("tools")))
    from research_check import check_research  # noqa: E402
    errors, _ = check_research(slug, None)
    return not errors


def _scouted(slug: str) -> bool:
    """new_job scaffolds an EMPTY manifest, so existence proves nothing.
    Done = at least one asset recorded, or a deliberate thin-manifest call
    recorded as `"thin": "<why>"` (AGENT.md: a thin manifest is a valid
    outcome — it just means a graphics-led reel; valid decisions get
    written down)."""
    p = _p(f"public/assets/{slug}/manifest.json")
    if not p.exists():
        return False
    try:
        m = json.loads(p.read_text())
    except Exception:
        return False
    return bool(m.get("assets") or m.get("items") or m.get("thin"))


def steps(slug: str) -> list[dict]:
    """The pipeline, in order. `auto` is a command safe to run unattended."""
    return [
        dict(key="goal",
             label="ONE goal chosen (save / share / follow / lead)",
             done=_p(f"jobs/{slug}/goal.md").exists(),
             auto=None,
             skills=["going-viral         pick the goal; it dictates emotion + mechanic"],
             human="Pick ONE goal and write it to "
                   f"jobs/{slug}/goal.md with the emotion and mechanic it "
                   "implies:\n"
                   "        SAVE   relief + fear-of-forgetting -> a finite "
                   "numbered system, depth in the caption\n"
                   "        SHARE  awe / indignation / status -> result first, "
                   "then how; must make the SENDER look early\n"
                   "        FOLLOW FOMO + aspiration -> show the gap, a real "
                   "climbing number, a recognisable look\n"
                   "        LEAD   greed + curiosity -> a named free "
                   "deliverable behind a keyword\n"
                   "      This comes FIRST, before scouting: the goal decides "
                   "what evidence is worth finding."),
        dict(key="research",
             label="Research ledger started (claims tiered + sourced)",
             done=_research_done(slug),
             auto=None,
             skills=["fact-check-workflow  verify each claim BEFORE it becomes a beat"],
             human=f"Fill jobs/{slug}/research.md AS YOU RESEARCH, not after:\n"
                   "        - CLAIM: <the claim>  /  TIER: official|multi|"
                   "single|disputed\n"
                   "          SPOKEN: (filled at script time)  /  SRC: <url "
                   "you actually fetched>\n"
                   "        plus a dated line in ## SEARCHED per query.\n"
                   "      Two independent source domains minimum, or write "
                   "ONE-SOURCE-OK: <why>.\n"
                   "      propose verifies SPOKEN against the script later; "
                   "this stage is the\n      structural half "
                   f"(python3 tools/research_check.py {slug})."),
        dict(key="scout",
             skills=["fact-check-workflow  verify each claim BEFORE it becomes a beat",
                     "ffmpeg-ytdlp        yt-dlp to pull source video/subtitles, ffmpeg to cut clips"],
             label="Assets scouted and manifest written",
             done=_scouted(slug),
             auto=None,
             human="Plan the shots from the approved script FIRST "
                   f"(python3 tools/plan_shots.py {slug}), then scout to satisfy "
                   "each line. Capture on MOBILE and RECORD WHERE IT CAME FROM:\n"
                   "        node tools/capture.mjs screenshot <url> --out <f.png> "
                   "--tier official|reliable|fallback\n"
                   "        --desktop needs --desktop-reason \"<why mobile could "
                   "not show it>\" (G41 blocks without it)\n"
                   "      One glance per candidate first: python3 "
                   f"tools/scout_sheet.py {slug}\n"
                   "      (a labeled contact sheet per clip — write `shows` "
                   "from the SHEET, not the filename).\n"
                   "      Write a `shows` description concrete enough to prove "
                   "the script link later — it is\n      what lets "
                   "tools/link_shots.py justify a `covers` phrase, and thin "
                   "`shows` text is why\n      grok-bot could only justify 4 of "
                   "39 while iphone-fold-ultra managed 11 of 30.\n"
                   f"      Then write public/assets/{slug}/manifest.json with "
                   "credits and tiers. See AGENT.md STEP 1a."),
        dict(key="structure",
             label="Narrative structure + open loop chosen",
             done=_structure_done(slug),
             auto=None,
             skills=["shortform-script-framework  S17 shapes, S2/S10 the loop"],
             human="Write jobs/" + slug + "/structure.md BEFORE the first "
                   "sentence. Three things, none retrofittable:\n"
                   "        SHAPE   one of framework S17 — Discovery / News / "
                   "Product announcement /\n"
                   "                Explainer / Tutorial / Comparison / Story / "
                   "List / Myth-busting /\n"
                   "                Transformation — or one you invent for this "
                   "topic. This is NOT\n"
                   "                the `format` field: format is the runtime "
                   "envelope, shape is the\n"
                   "                telling. See formats/README-structure.md.\n"
                   "        PROMISE what the viewer is told they will get (S2)\n"
                   "        LOOP    what is withheld early and paid off later "
                   "(S10), and WHERE\n"
                   "                it pays off. An enumeration is not a loop — "
                   "'three changes are\n"
                   "                coming' announces the agenda and withholds "
                   "nothing.\n"
                   "      Escalation (S6) follows from the shape; name which "
                   "progression you are using."),
        dict(key="script",
             skills=["news-reel           owns structure; formats/<format>.md is the shape",
                     "shortform-script-framework  READ FIRST — styles/. Structure",
                     "                    and open loop are chosen before sentence one",
                     "viral-hook-writer   the first 2 seconds only — pair it with",
                     "                    framework S1/S16 or it writes a hook with",
                     "                    no context, which is what shipped 2026-08-19",
                     "humanizer           LAST pass, SCOPED — see SKILL.md 2a. Three of",
                     "                    its patterns collide with S20 hedging, the",
                     "                    playbook's hook devices, and the payoff triad"],
             label="Narration written",
             done=_p(f"jobs/{slug}/script.md").exists(),
             auto=None,
             human=f"Write the narration to jobs/{slug}/script.md using "
                   "formats/<format>.md for structure and the style pack for "
                   f"voice. Put judgement calls in jobs/{slug}/questions.md.\n"
                   f"      Then measure the prose: python3 tools/check_script.py {slug}\n"
                   "      (cadence, repeated shapes, stage-direction questions, "
                   "when 'you' first appears,\n      business-speak, number "
                   "density — advice, never blocking)"),
        dict(key="approval",
             skills=["(none — this is the user's decision, not a skill's)"],
             label="Script approved by the user",
             done=_approved(slug),
             auto=None,
             stops=True,
             human=f"python3 tools/script_approval.py propose {slug}\n"
                   "      Show the user the script AND the beat plan, ask the "
                   "open questions, wait for an explicit yes, then:\n"
                   f"      python3 tools/script_approval.py approve {slug}"),
        dict(key="voice",
             skills=["(none — HeyGen MCP + tools/voice_clone.py to rehearse pace free)"],
             label="Voice + avatar master generated",
             done=_p(f"public/assets/{slug}/vo.json").exists(),
             auto=None,
             stops=True,
             human="Generate the avatar (HeyGen, native 9:16 @1080p) and the "
                   "whisper word timings. THIS SPENDS CREDITS — check the "
                   "balance first, and never run it on an unapproved script."),
        dict(key="beats",
             skills=["remotion-markup     animation/effects; frame-driven, never CSS transitions",
                     "remotion-captions   caption timing and display",
                     "remotion-docs       look up an API instead of guessing"],
             label="Beat sheet built",
             done=_p(f"src/beats/{slug}.json").exists(),
             auto=None,
             human="PREFERRED — compile the shot plan, which anchors every "
                   "scene to the phrase it\n      illustrates, so `covers` is "
                   "written for you and G39 is satisfied by construction:\n"
                   f"        python3 scripts/compile_shot_plan.py {slug}\n"
                   "      FALLBACK — a bespoke script, for a reel the shot plan "
                   "cannot express. You then\n      owe `covers` by hand "
                   f"(tools/link_shots.py {slug} justifies what it can):\n"
                   f"        cp tools/build_template.py tools/build_{slug}.py\n"
                   "      Either way the sheet must carry `script` and "
                   "`approval` for G27."),
        dict(key="register",
             skills=["(none — deterministic)"],
             label="Beat sheet registered with Remotion",
             done=_p("src/generatedBeatSheets.ts").exists()
                  and slug in _p("src/generatedBeatSheets.ts").read_text(),
             auto=[sys.executable, str(_p("scripts/register_beats.py"))]),
        dict(key="gates",
             skills=["(none — gates are code and are not advisory)"],
             label="All gates pass",
             done=_gates_pass(slug),
             auto=[sys.executable, str(_p("tools/reel_gates.py")), slug],
             human="Fix what the gates report. They are not advisory."),
        dict(key="render",
             skills=["remotion-render      export settings",
                     "ffmpeg-ytdlp         mastering; two-pass loudnorm, measure the result"],
             label="Rendered and mastered",
             done=_p(f"out/{slug}-final.mp4").exists(),
             auto=[sys.executable, str(_p("scripts/render_job.py")), slug]),
        dict(key="qc",
             skills=["reel-analyzer        watch the master back and find what went wrong",
                     "ffmpeg-ytdlp         pull frames to inspect"],
             label="Frame lint clean",
             done=False,   # always re-run; it is cheap and catches regressions
             auto=[sys.executable, str(_p("tools/lint_frames.py")), slug]),
        dict(key="packaging",
             skills=["social               titles, captions, cadence (Instagram 5 hashtags)",
                     "youtube-seo          YouTube title/description/tags",
                     "thumbnail-design     the thumbnail BRIEF (we render it ourselves)",
                     "content-repurposer   spin the reel into other platforms afterwards"],
             label="Title, caption, hashtags, alt text",
             done=_p(f"jobs/{slug}/packaging.md").exists(),
             auto=None,
             human="Use the `social` skill. Hashtags per platform limits "
                   "(Instagram 5), hashtags in the FIRST COMMENT, and include "
                   "ALT TEXT. Then: python3 tools/packaging_check.py " + slug),
        # POST-PUBLISH, and the only stage that feeds numbers BACK into the
        # system. Every FORMATS number so far came from teardowns of other
        # people's reels; this is where our own start to accumulate.
        dict(key="retention",
             skills=["(none — YouTube Studio and one command)"],
             label="Retention ingested (post-publish; wait ~72h of views)",
             done=_p(f"jobs/{slug}/performance.json").exists(),
             auto=None,
             human="After the reel has aged ~72h on YouTube:\n"
                   "        Studio -> Analytics -> Advanced mode -> Audience "
                   "retention -> Export -> CSV\n"
                   f"        python3 tools/retention_ingest.py {slug} "
                   "--csv <export.csv> --duration <published s> --views <n>\n"
                   "      It joins the curve to this reel's beat timeline: "
                   "which scene TYPES bleed\n      viewers, what got "
                   "replayed. Across reels: retention_ingest.py --aggregate.\n"
                   "      Instagram has no per-second export — note its "
                   "aggregate numbers in packaging.md."),
    ]


def _stamp(slug: str, st: list[dict]) -> dict:
    """Record when each stage first showed as done, and report the gaps.

    NOTHING HAS EVER MEASURED THIS. Asked on 2026-08-19 why a reel takes two
    hours, the honest answer was an inference from artifact counts — 8 build
    scripts, 22-51 assets per reel, 7 render cycles — not a measurement. The
    machine half is timed to the second (a still is 3.3s, a render is ~8min);
    the human half, which is 7 of the 12 stages, has never been timed at all.

    So `showrunner status` now stamps the first moment each stage reads done
    into jobs/<slug>/timing.json. It costs nothing, it cannot be gamed by
    memory, and after one reel it replaces every estimate in this file with a
    number.
    """
    import datetime as _dt
    f = _p(f"jobs/{slug}/timing.json")
    rec = json.loads(f.read_text()) if f.exists() else {}
    changed = False
    for step in st:
        if step["done"] and step["key"] not in rec:
            rec[step["key"]] = _dt.datetime.now().astimezone().isoformat(timespec="seconds")
            changed = True
    if changed and f.parent.exists():
        f.write_text(json.dumps(rec, indent=2) + "\n")
    return rec


def _elapsed(rec: dict, st: list[dict]) -> None:
    import datetime as _dt
    done = [(s["key"], rec[s["key"]]) for s in st if s["key"] in rec]
    if len(done) < 2:
        return
    print("  stage timings (first seen done — a floor, not a stopwatch):")
    prev = None
    for key, iso in done:
        t = _dt.datetime.fromisoformat(iso)
        gap = f"{(t - prev).total_seconds() / 60:6.0f} min" if prev else "     —"
        print(f"    {key:12} {gap}")
        prev = t
    total = (_dt.datetime.fromisoformat(done[-1][1])
             - _dt.datetime.fromisoformat(done[0][1])).total_seconds() / 60
    print(f"    {'TOTAL':12} {total:6.0f} min across {len(done)} stages\n")


def cmd_status(slug: str) -> None:
    st = steps(slug)
    rec = _stamp(slug, st)
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
    _elapsed(rec, st)
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
        # Naming the skill HERE is the point: a stage-to-skill map in a doc gets
        # skipped, the same way the script-approval rule got skipped while it was
        # only prose. Say it at the moment it is needed.
        for line in s.get("skills", []):
            print(f"      skill: {line}")
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
