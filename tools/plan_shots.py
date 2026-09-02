#!/usr/bin/env python3
"""Turn an approved script into a shot plan — one shot per clause, phrase-anchored.

WHY THIS EXISTS
---------------
The user has asked for this since the September teardown: "We must have scouted
sources according the script and try to show the exact same thing in the video
whenever possible... first attempt would be to find the exact thing being said,
and if not available then relevant ones."

The machinery was already here and unused. `scripts/compile_shot_plan.py` has
supported PHRASE-ANCHORED shots (`start_phrase` resolved against the whisper word
timings) the whole time, yet every jobs/*/shot-plan.json holds 0 shots — the reels
were hand-assembled by bespoke tools/build_<slug>.py scripts instead. So the
pipeline had the right idea and never ran it.

THE ORDER MATTERS. Planning the shot from the SCRIPT first, then scouting an
asset to satisfy it, is what makes Rule 3 provable rather than asserted:

  script clause  ->  what the visual must show  ->  scout an asset  ->  covers
                     (the brief)                    (official first)   (free)

`covers` then falls out of `start_phrase` at compile time and is not circular,
because the phrase existed before anyone went looking for footage. Compare with
inferring `covers` from whatever words happen to overlap a finished scene, which
is the trap tools/link_shots.py exists to avoid.

    python3 tools/plan_shots.py <slug>              # print the plan
    python3 tools/plan_shots.py <slug> --write      # write jobs/<slug>/shot-plan.json

SEARCH TIERS, in order, per the user's rule 2026-08-14:
  official   the maker's own page, newsroom, spec sheet, keynote
  reliable   an established outlet with a named reporter — upcoming products are
             often NOT on official sources, so this is expected, not a failure
  fallback   merely relevant. Recorded so it can be counted and argued with.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from textsplit import sentences as _split_sentences  # noqa: E402

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STOP = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "for",
    "with", "from", "by", "as", "is", "are", "was", "were", "be", "it", "its",
    "this", "that", "these", "those", "so", "if", "not", "no", "you", "your",
    "we", "our", "they", "their", "will", "would", "can", "just", "also",
    "more", "very", "one", "up", "out", "about", "into", "all", "what", "how",
    "here", "there", "then", "than", "keep", "keeps", "calling", "everything",
    "strange", "explains", "decision",
}

ANCHOR_WORDS = 4        # words in a start_phrase — enough to be unique
MIN_CLAUSE_WORDS = 4    # shorter than this is not its own shot


def clauses(script: str) -> list[str]:
    """Split into shot-sized units: sentences, then long ones at their comma."""
    out: list[str] = []
    for sent in _split_sentences(script):
        sent = sent.strip()
        if not sent:
            continue
        if len(sent.split()) > 14 and "," in sent:
            head, _, tail = sent.partition(",")
            for part in (head, tail):
                if len(part.split()) >= MIN_CLAUSE_WORDS:
                    out.append(part.strip(" ,"))
                elif out:
                    out[-1] = f"{out[-1]}, {part.strip(' ,')}"
        else:
            out.append(sent)
    return [c for c in out if len(c.split()) >= 2]


def anchor_of(clause: str) -> str:
    return " ".join(clause.split()[:ANCHOR_WORDS])


def brief_of(clause: str) -> list[str]:
    """The concrete things a visual for this clause must contain."""
    words = re.sub(r"[^\w\s.%\"$-]", " ", clause).split()
    keep: list[str] = []
    for w in words:
        bare = w.strip(".,;:!?\"'").lower()
        if not bare:
            continue
        if any(c.isdigit() for c in bare) or bare not in STOP and len(bare) > 3:
            keep.append(w.strip(".,;:!?"))
    seen, out = set(), []
    for w in keep:
        k = w.lower()
        if k not in seen:
            seen.add(k)
            out.append(w)
    return out[:6]


def normalise(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", s.lower().replace("’", "'"))


def resolvable(anchor: str, vo_words: list[str]) -> bool:
    """Would compile_shot_plan find this phrase in the actual voice track?

    Checked HERE because a plan whose anchors do not resolve is a plan that
    cannot compile, and finding that out at compile time wastes the trip.
    """
    needle = normalise(anchor)
    if not needle:
        return False
    hay = [w for word in vo_words for w in normalise(word)]
    return any(hay[i:i + len(needle)] == needle
               for i in range(len(hay) - len(needle) + 1))


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug = args[0]
    write = "--write" in sys.argv

    script_p = ROOT / f"jobs/{slug}/script.md"
    if not script_p.exists():
        sys.exit(f"no script at {script_p}")
    # APPROVAL IS A PRECONDITION FOR --write, not a docstring claim
    # (2026-08-26, user: "why does it build the shot plan before getting
    # approval of the script?").
    #
    # This file has always SAID "turn an approved script into a shot plan"
    # and only ever checked that the file existed. Every shot here is
    # PHRASE-ANCHORED to exact wording, so a shot plan written before
    # approval is invalidated by the first word the user changes — which is
    # precisely the "repair the broken anchors" work that then looks like
    # progress. Planning against unapproved words is not early work, it is
    # work that has to be redone.
    #
    # Reading the plan without --write stays open: seeing the clause
    # breakdown is often HOW you decide the script is ready.
    if write:
        import hashlib
        appr_p = ROOT / f"jobs/{slug}/approval.json"
        if not appr_p.exists():
            sys.exit(
                f"REFUSING to write a shot plan for {slug!r}: the script is "
                "not approved.\n"
                "  Every shot here anchors to exact wording, so this file "
                "would be invalidated by the first edit.\n"
                "  Approve first:  python3 tools/script_approval.py propose "
                f"{slug}   (then approve)\n"
                "  Or read the breakdown without writing: drop --write.")
        try:
            appr = json.loads(appr_p.read_text())
            # HASH THE SAME BYTES script_approval DOES (2026-09-01). This
            # used to sha256 the WHOLE file, while script_approval.py hashes
            # only the SPOKEN lines — it strips markdown headings, quotes and
            # comments first. The two agreed for every reel so far purely
            # because no script.md had ever carried a heading. The first one
            # that did was refused here with a hash the user had genuinely
            # approved. Two functions guarding one guarantee must read the
            # same input, or the guard is right by convention rather than by
            # construction.
            from script_approval import read_script, sha
            live = sha(read_script(slug))
            if appr.get("sha256") and appr["sha256"] != live:
                sys.exit(
                    f"REFUSING: {slug!r} was approved at "
                    f"{appr['sha256'][:8]} but script.md now hashes "
                    f"{live[:8]}. The anchors would be written against words "
                    "nobody approved. Re-propose and re-approve.")
        except (ValueError, KeyError):
            pass
    vo_p = ROOT / f"public/assets/{slug}/vo.json"
    vo_words: list[str] = []
    if vo_p.exists():
        # READ THE SHAPE THE PIPELINE ACTUALLY WRITES (2026-09-01). This used
        # to reach only for raw Whisper's `segments[].words[]`, while
        # ingest_avatar.py — the tool that writes this file — emits the
        # flattened {"words": [...]}. So the anchor check silently found ZERO
        # words on every reel ingested that way and printed "no vo.json yet",
        # which reads as "not generated yet" rather than "I cannot read it".
        # A check that cannot run is worse than one that fails: it is invisible.
        # compile_shot_plan.load_words already tolerates both; reuse it rather
        # than keeping a third opinion about the format.
        sys.path.insert(0, str(ROOT / "scripts"))
        from compile_shot_plan import load_words
        vo_words = [w["text"] for w in load_words(vo_p)]

    cl = clauses(script_p.read_text())
    shots, unresolved = [], []
    for i, c in enumerate(cl):
        anchor = anchor_of(c)
        ok = resolvable(anchor, vo_words) if vo_words else None
        if ok is False:
            unresolved.append((i, anchor))
        shots.append({
            "start_phrase": anchor,
            "line": c,
            "needs": brief_of(c),
            "tier": None,          # scout fills: official | reliable | fallback
            "asset_id": None,      # scout fills, must exist in the manifest
            "scene": {},           # chosen once the asset is known
        })

    print(f"\n  {slug}: {len(cl)} clause(s) -> {len(shots)} shot(s)")
    if vo_words:
        print(f"  anchors checked against {len(vo_words)} spoken words: "
              f"{len(shots) - len(unresolved)} resolve, {len(unresolved)} do not")
    else:
        print("  no vo.json yet — anchors NOT verified, they may fail to compile")
    print()
    for i, s in enumerate(shots[:14]):
        mark = "  " if (i, s["start_phrase"]) not in unresolved else "!!"
        print(f"  {mark} {i:02d} {s['start_phrase']!r}")
        print(f"        needs: {', '.join(s['needs']) or '(nothing concrete)'}")
    if len(shots) > 14:
        print(f"  ... and {len(shots) - 14} more")

    if unresolved:
        print(f"\n  {len(unresolved)} anchor(s) are NOT in the voice track — the "
              "script was edited\n  after the VO was generated, or the read "
              "differed. These will fail to\n  compile; fix the phrase or "
              "re-cut the anchor:")
        for i, a in unresolved[:8]:
            print(f"    shot {i:02d} {a!r}")

    if write:
        out_p = ROOT / f"jobs/{slug}/shot-plan.json"
        existing = json.loads(out_p.read_text()) if out_p.exists() else {}
        if existing.get("shots"):
            sys.exit(f"{out_p.relative_to(ROOT)} already has "
                     f"{len(existing['shots'])} shot(s) — refusing to overwrite "
                     "scouting work. Move it aside first.")
        existing["shots"] = shots
        existing.setdefault("emphasis", [])
        existing.setdefault("caption_corrections", {})
        out_p.write_text(json.dumps(existing, indent=2) + "\n")
        print(f"\n  wrote {len(shots)} shot(s) to {out_p.relative_to(ROOT)}")
        print("  Each carries the LINE it must illustrate and a `needs` brief. "
              "Scout in tier\n  order and record which tier you got: official, "
              "then reliable, then fallback.")
    else:
        print("\n  (--write to save the plan)")


if __name__ == "__main__":
    main()
