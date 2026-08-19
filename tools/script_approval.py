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


def cmd_propose(slug: str) -> None:
    spoken = read_script(slug)
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
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from check_script import check as _prose, checklist as _list  # noqa: E402
        print("\nPROSE (advice — style is craft, none of this blocks):")
        for _n in _prose(spoken) or ["  nothing to flag"]:
            print(f"  - {_n}" if not _n.startswith("  ") else _n)
        # framework S25 at the ONE moment the script can still change. The
        # measured half is answered; the rest is what the approver is for.
        print()
        for _n in _list(spoken):
            print(_n)
    except Exception as _e:  # noqa: BLE001
        print(f"\n  (prose check unavailable: {_e})")

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


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("propose", "approve", "check"):
        sys.exit("usage: python3 tools/script_approval.py "
                 "propose|approve|check <slug>")
    {"propose": cmd_propose, "approve": cmd_approve,
     "check": cmd_check}[sys.argv[1]](sys.argv[2])


if __name__ == "__main__":
    main()
