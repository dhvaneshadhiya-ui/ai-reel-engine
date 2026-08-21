#!/usr/bin/env python3
"""Script approval — a BLOCKING step, not a good intention.

WHY THIS EXISTS
---------------
On 2026-08-12 the user said: "Our System never shows me the script and if it
is okay or I want any changes. It must first take approval of the script."

They were right. Script approval had been written as PROSE in CLAUDE.md,
RULES.md and the news-reel skill — and this repo's founding observation is
that prose rules get skipped while code rules get enforced. So approval is now
a hash-checked artifact:

    python3 tools/script_approval.py propose <slug>   # show it, ask questions
    python3 tools/script_approval.py approve <slug>   # record the user's YES
    python3 tools/script_approval.py check   <slug>   # exits 1 if not approved

`check` runs BEFORE the avatar is generated (generation costs credits and
freezes the audio) and again inside render_job.py. Gate G27 re-checks the hash
against the narration stored in the beat sheet, so editing a word AFTER
approval invalidates it — silently shipping an unapproved edit is impossible.

Layout per reel:
    jobs/<slug>/script.md      the narration, exactly as it will be spoken
    jobs/<slug>/questions.md   open questions for the user (optional)
    jobs/<slug>/approval.json  written only by `approve`
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WPS = 2.7          # words/sec — CENTER of the measured range (see below)
WPS_MIN, WPS_MAX = 2.35, 2.75
# 2026-08-13: the old 3.2 was never measured. 2026-08-14: FIVE masters now —
# grok-bot 2.69, apple-pay-india 2.72, iphone18-split 2.55,
# september-preview 2.36 (pause-heavy punctuation runs slow: colons, dashes
# and rhetorical questions are runtime). The voice VARIES, so the check
# blocks on the SLOWEST pace: a script only passes if it fits the band even
# at 2.35 wps. Band words for 60-80s: 141-188 safe (188 = 80x2.35).


def paths(slug: str) -> tuple[Path, Path, Path]:
    # A DERIVATIVE sheet ("<slug>-nomusic", the sanctioned music-free export)
    # speaks the SAME approved narration — it differs only in the music block,
    # and G27 re-hashes that narration off the sheet either way. It therefore
    # resolves to the parent's approval record rather than demanding a second
    # yes for words the user already approved.
    for suffix in ("-nomusic",):
        if slug.endswith(suffix):
            parent = slug[: -len(suffix)]
            if (ROOT / "jobs" / parent / "approval.json").exists():
                slug = parent
            break
    d = ROOT / "jobs" / slug
    return d / "script.md", d / "questions.md", d / "approval.json"


def normalise(text: str) -> str:
    """Hash the WORDS, not the whitespace — reflowing a paragraph is not an
    edit, changing a word is."""
    return " ".join(text.split())


def sha(text: str) -> str:
    return hashlib.sha256(normalise(text).encode()).hexdigest()


def read_script(slug: str) -> str:
    script_p, _, _ = paths(slug)
    if not script_p.exists():
        sys.exit(f"no script at {script_p} — write the narration there first.")
    body = script_p.read_text()
    # strip markdown headings/comments so the hash covers spoken words only
    spoken = "\n".join(l for l in body.splitlines()
                       if l.strip() and not l.lstrip().startswith(("#", ">", "<!--")))
    if not spoken.strip():
        sys.exit(f"{script_p} has no narration lines.")
    return spoken


# framework S17's ten shapes — structure.md must name the one it chose.
SHAPES = ("discovery", "news", "product announcement", "explainer", "tutorial",
          "comparison", "story", "list", "myth-busting", "transformation")


def review_path(slug: str) -> Path:
    """jobs/<slug>/review.json — written by propose, demanded by approve.
    Rides the same -nomusic parent resolution as the approval record."""
    return paths(slug)[2].with_name("review.json")


def structure_problems(slug: str) -> list[str]:
    """Why jobs/<slug>/structure.md is not yet a decision. Empty = it is.
    Split out of require_structure so showrunner's stage display and the
    refusal share one definition — a scaffolded template must not read as
    'structure chosen' anywhere."""
    st_p = paths(slug)[2].with_name("structure.md")
    if not st_p.exists():
        return ["missing"]
    body = st_p.read_text()
    out = []
    if re.search(r"<[a-z][^>\n]{3,}>", body):
        out.append("unfilled <placeholders>")
    if not any(s in body.lower() for s in SHAPES):
        out.append("no S17 shape named")
    return out


def require_structure(slug: str) -> Path:
    """The framework's one non-negotiable ORDER: shape before sentences.

    ADDED 2026-08-21, the third time a weak first draft reached the user.
    The framework was in the repo, named by the skill, the formats and this
    repo's own README-structure.md — and the draft still opened on the S16
    failure verbatim, because reading is optional and nothing blocked. Same
    arc as approval itself in the docstring above: prose for a day, then code.

    The check is deliberately shallow — file exists, placeholders filled, a
    S17 shape named. Whether the structure is any GOOD stays the author's
    craft; what can no longer happen is a script drafted with no structure
    decision at all.
    """
    st_p = paths(slug)[2].with_name("structure.md")
    probs = structure_problems(slug)
    if "missing" in probs:
        sys.exit(
            f"NO STRUCTURE DECLARED — {slug}\n"
            f"  missing {st_p}\n"
            "  The framework (styles/shortform-script-framework.md S17) chooses\n"
            "  the narrative shape BEFORE the first sentence — none of promise,\n"
            "  loop or escalation can be retrofitted by editing lines afterwards\n"
            "  (formats/README-structure.md). scripts/new_job.py scaffolds this\n"
            "  file; fill it in, then draft, then propose.")
    if "unfilled <placeholders>" in probs:
        sys.exit(
            f"STRUCTURE STILL A TEMPLATE — {slug}\n"
            f"  {st_p} has unfilled <placeholders>.\n"
            "  Decide the shape, the promise and the loop before drafting —\n"
            "  that is the writing, not paperwork around it.")
    if probs:
        sys.exit(
            f"STRUCTURE NAMES NO SHAPE — {slug}\n"
            f"  {st_p} must name one of framework S17's shapes:\n"
            f"  {', '.join(SHAPES)}.")
    return st_p


def cmd_propose(slug: str) -> None:
    st_p = require_structure(slug)
    spoken = read_script(slug)
    # The research ledger — hardened 2026-08-21, one day after structure, for
    # the same reason and with the same split: a ledger that is structurally
    # dishonest (missing, template, unsourced claim, SPOKEN words nobody says)
    # refuses; judgement calls (unhedged single-source, one domain) advise.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from research_check import check_research  # noqa: E402
    research_errors, research_advice = check_research(
        slug, spoken, root=ROOT)
    if research_errors:
        sys.exit("RESEARCH LEDGER REFUSED — " + slug + "\n  "
                 + "\n  ".join(research_errors)
                 + "\n  Fix jobs/" + slug + "/research.md, then propose again.")
    _, q_p, _ = paths(slug)
    words = len(spoken.split())
    secs = words / WPS
    print("=" * 68)
    print(f"SCRIPT FOR APPROVAL — {slug}")
    print("=" * 68)
    print(spoken)
    print("-" * 68)
    print(f"{words} words  ->  ~{secs:.0f}s at speed 1.05 (measured {WPS} wps)")
    print(f"sha256: {sha(spoken)[:16]}")
    # 2026-08-13: BLOCK out-of-band scripts at propose time — the cheap
    # moment. A 242-word script sailed through at "~76s" under the old 3.2
    # wps constant and rendered 93.5s; gate G02 only catches that AFTER the
    # avatar is generated and the credits are spent. Band: 60-80s (news).
    # Deliberate long-form needs "allowLong" in the questions file, which
    # forces the length to be one of the questions the user answers.
    # Band comes from the reel's declared FORMAT (manifest.json "format",
    # default news) via reel_gates.FORMATS — a top5 script is 26-48s, not
    # 60-80s (bug caught 2026-08-13 before the first top5 reel).
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
    from reel_gates import FORMATS
    fmt = "news"
    man_p = ROOT / "public" / "assets" / slug / "manifest.json"
    if man_p.exists():
        try:
            fmt = json.loads(man_p.read_text()).get("format", "news")
        except Exception:
            pass
    band_lo, band_hi = FORMATS.get(fmt, FORMATS["news"])["runtime"]
    slow, fast = words / WPS_MIN, words / WPS_MAX
    print(f"delivery range: {fast:.0f}-{slow:.0f}s at measured "
          f"{WPS_MIN}-{WPS_MAX} wps")
    q_text = q_p.read_text() if q_p.exists() else ""
    # Block when the SLOWEST measured pace overshoots the band, or the
    # fastest undershoots it — the voice varies 2.36-2.72 wps across real
    # masters, so a point estimate is not safe (2026-08-14).
    # ADVISORY since 2026-08-17, not a block.
    #
    # The constitution says only three rules are law — Reels/Shorts format,
    # mobile-first scouting, picture matches words — and runtime is explicitly
    # judgement: "If a longer reel serves the story, make it longer." That change
    # landed in reel_gates.py and NEVER PROPAGATED HERE, so the length band kept
    # hard-blocking at the approval step while the same band merely advised at
    # the gate. Found by trying to record the approval for two reels that had
    # already SHIPPED at ~100s: the tool refused to let the user approve a script
    # the audience has already watched.
    #
    # It still says its piece, loudly, because the measurement is real and a
    # 130s news reel usually is too long. It just no longer refuses.
    if (slow > band_hi * 1.02 or fast < band_lo * 0.95) \
            and "allowLong" not in q_text:
        print(f"\n  LENGTH ADVICE: {words} words could run "
                 f"{fast:.0f}-{slow:.0f}s — outside the {band_lo:.0f}-"
                 f"{band_hi:.0f}s band for format {fmt!r} at the voice's "
                 f"measured pace range. Safe budget: "
                 f"{int(band_lo*WPS_MAX)}-{int(band_hi*WPS_MIN)} words. "
                 "Trim it if the story does not need the room. Runtime is "
                 "judgement, not a rule — this is advice, and approval is "
                 "still yours to give.")
    # Prose measurement, printed where the script is actually being read. The
    # playbook's cadence rule existed for weeks and was skipped every time,
    # because nobody re-reads a style guide at the moment they approve.
    findings: list[str] | None = None
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from check_script import check as _prose, checklist as _list  # noqa: E402
        findings = _prose(spoken) or []
        print("\nPROSE (advice — style is craft, none of this blocks):")
        for _n in findings or ["  nothing to flag"]:
            print(f"  - {_n}" if not _n.startswith("  ") else _n)
        # framework S25 at the ONE moment the script can still change. The
        # measured half is answered; the rest is what the approver is for.
        print()
        for _n in _list(spoken):
            print(_n)
    except Exception as _e:  # noqa: BLE001
        print(f"\n  (prose check unavailable: {_e})")

    # The review RECORD. approve refuses without one whose hash matches the
    # current script, so "the user approved it" now provably means "the user
    # was shown THIS script, with these findings, and said yes to that" —
    # the same RIGHTS territory as G27, one step earlier. The findings stay
    # advice; what stops being possible is approving a script nobody proposed,
    # or quietly editing between the showing and the yes.
    if research_advice:
        print("\nRESEARCH (advice — sourcing depth is judgement, "
              "none of this blocks):")
        for _a in research_advice:
            print(f"  - {_a}")
    review_path(slug).write_text(json.dumps({
        "script_sha256": sha(spoken),
        "structure_sha256": sha(st_p.read_text()),
        "findings": findings,
        "research_advice": research_advice,
        "proposedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }, indent=2))

    if q_p.exists():
        print("\nQUESTIONS THAT NEED AN ANSWER BEFORE WE BUILD:")
        print(q_p.read_text().rstrip())
    else:
        print("\nNo open questions recorded. If anything about this script is a "
              "judgement call, write it to:")
        print(f"  {q_p}")
    print("\nNOTHING IS GENERATED UNTIL THE USER SAYS YES.")
    print(f"On their approval:  python3 tools/script_approval.py approve {slug}")


def cmd_approve(slug: str) -> None:
    spoken = read_script(slug)
    _, _, appr_p = paths(slug)
    # An approval must sit on a propose of the SAME words. Without this, the
    # 2026-08-21 path stays open: draft in chat, approve from chat, and the
    # structure gate plus every printed finding is bypassed because propose
    # simply never ran.
    rev_p = review_path(slug)
    if not rev_p.exists():
        sys.exit(
            f"NEVER PROPOSED — {slug}\n"
            f"  no {rev_p}\n"
            "  Approval records that the user saw THIS script with its "
            "findings.\n  Run propose first:\n"
            f"    python3 tools/script_approval.py propose {slug}")
    rev = json.loads(rev_p.read_text())
    if rev.get("script_sha256") != sha(spoken):
        sys.exit(
            f"SCRIPT CHANGED SINCE IT WAS PROPOSED — {slug}\n"
            f"  proposed {rev.get('script_sha256', '')[:16]} at "
            f"{rev.get('proposedAt')}\n"
            f"  current  {sha(spoken)[:16]}\n"
            "  The user would be approving words they were never shown. "
            "Propose again.")
    appr_p.parent.mkdir(parents=True, exist_ok=True)
    rec = {
        "sha256": sha(spoken),
        "approvedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "words": len(spoken.split()),
        "_note": "Written only after the user approved the script in chat. "
                 "Editing the script invalidates this — the hash stops "
                 "matching and G27 blocks the build.",
    }
    appr_p.write_text(json.dumps(rec, indent=2))
    print(f"approved: {slug} ({rec['words']} words, {rec['sha256'][:16]})")


def cmd_check(slug: str) -> None:
    spoken = read_script(slug)
    _, _, appr_p = paths(slug)
    if not appr_p.exists():
        sys.exit(
            f"SCRIPT NOT APPROVED — {slug}\n"
            f"  no {appr_p}\n"
            "  Show the user the script and the beat plan, ask any open "
            "questions, and wait for an explicit yes:\n"
            f"    python3 tools/script_approval.py propose {slug}\n"
            "  Do NOT generate the avatar before this passes — generation "
            "costs credits and freezes the audio.")
    rec = json.loads(appr_p.read_text())
    if rec.get("sha256") != sha(spoken):
        sys.exit(
            f"SCRIPT CHANGED SINCE APPROVAL — {slug}\n"
            f"  approved {rec.get('sha256', '')[:16]} at "
            f"{rec.get('approvedAt')}\n"
            f"  current  {sha(spoken)[:16]}\n"
            "  The user approved a different script. Show them what changed "
            "and get approval again.")
    print(f"script approved — {slug} ({rec['words']} words, "
          f"{rec['approvedAt']})")
    # REHEARSAL ADVISORY — printed here because `check` is the documented
    # last command before the avatar is generated, which is the one moment
    # this information can still save money. A broken phrase anchor found
    # AFTER generation costs credits and the queue wait a second time;
    # rehearse_vo.py finds it for free. ADVICE, never a block: the
    # constitution reserves blocking for the three rules, render
    # correctness and rights — prudence about spend is judgement.
    # (Same slug resolution as everything else: a -nomusic sibling shares
    # its parent's rehearsal.)
    base = slug
    for suffix in ("-nomusic",):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
    reh = ROOT / "_sources" / base / "rehearsal"
    if not (reh.exists() and any(reh.iterdir())):
        print(f"\n  NOT REHEARSED — no artifacts under {reh}.\n"
              "  Generation freezes the audio; a phrase anchor that does not "
              "resolve is only\n  discoverable against a VO, and discovering "
              "it after generation costs credits\n  plus the queue wait. The "
              "rehearsal costs nothing:\n"
              f"    python3 tools/rehearse_vo.py {base}\n"
              "  Advice, not a block — but say so out loud if you generate "
              "without it.")


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("propose", "approve", "check"):
        sys.exit("usage: python3 tools/script_approval.py "
                 "propose|approve|check <slug>")
    {"propose": cmd_propose, "approve": cmd_approve,
     "check": cmd_check}[sys.argv[1]](sys.argv[2])


if __name__ == "__main__":
    main()
