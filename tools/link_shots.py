#!/usr/bin/env python3
"""Link every source scene to the line it illustrates — Rule 3, authorable.

WHY THIS IS NOT A FILL-IN-THE-BLANKS SCRIPT
-------------------------------------------
G39 requires each scene showing a scouted source to declare `covers`: the phrase
that visual proves. A tool that picked any phrase from the words spoken during
the scene would make the gate CIRCULAR — the check would pass by construction and
verify nothing beyond "some words were said here".

So the link is only ever asserted from EVIDENCE ON BOTH SIDES:

  what the asset shows   manifest `shows`, written when the asset was scouted
  what the creator says  whisper word timings for that scene's window

A `covers` phrase is proposed only where those two share a concrete term. That is
real evidence that the picture matches the words. Where they share nothing, the
tool says so and leaves it for a human — because "no overlap" is itself the most
interesting result: it usually means the shot is sitting against the wrong line.

    python3 tools/link_shots.py <slug>           # report, writes nothing
    python3 tools/link_shots.py <slug> --write   # fill only the justified ones
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Words that co-occur in any two English sentences and prove nothing about a match.
STOP = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "for",
    "with", "from", "by", "as", "is", "are", "was", "were", "be", "been", "it",
    "its", "this", "that", "these", "those", "there", "here", "then", "than",
    "so", "if", "not", "no", "yes", "you", "your", "we", "our", "they", "their",
    "he", "she", "his", "her", "i", "me", "my", "will", "would", "can", "could",
    "just", "also", "more", "most", "very", "one", "two", "up", "out", "about",
    "into", "over", "all", "both", "each", "which", "who", "what", "when",
    "how", "why", "now", "new", "shows", "showing", "seen", "verified", "clean",
    "frame", "screen", "camera", "hands", "holding", "held", "against",
    "backdrop", "distinct", "region", "head", "tail",
}


def norm(s: str) -> list[str]:
    return [w for w in re.sub(r"[^\w\s]", " ", s.lower()).split() if w]


def content(s: str) -> set[str]:
    return {w for w in norm(s) if w not in STOP and len(w) > 2}


def load(slug: str):
    beats_p = ROOT / f"src/beats/{slug}.json"
    vo_p = ROOT / f"public/assets/{slug}/vo.json"
    man_p = ROOT / f"public/assets/{slug}/manifest.json"
    if not beats_p.exists():
        sys.exit(f"no beat sheet at {beats_p}")
    if not vo_p.exists():
        sys.exit(f"no word timings at {vo_p} — the voice stage has not run, so "
                 "there is nothing to match against")
    beats = json.loads(beats_p.read_text())
    vo = json.loads(vo_p.read_text())
    words = [(w["word"].strip(), float(w["start"]), float(w["end"]))
             for s in vo.get("segments", []) for w in s.get("words", [])]
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    shows = {a.get("id"): a.get("shows", "") for a in man.get("assets", [])}
    return beats_p, beats, words, shows


def shows_source(sc: dict) -> bool:
    """Mirrors reel_gates._shows_source: borrowed material, not the presenter."""
    src = str(sc.get("src") or sc.get("topSrc") or "")
    if "avatar" in src.lower():
        return False
    return bool(sc.get("assetId")) or (
        src.startswith("assets/") and not src.endswith("avatar-master.mp4"))


def phrase_around(words: list[tuple[str, float, float]], lo: float, hi: float,
                  anchor: str, span: int = 4) -> str:
    """The shortest natural phrase inside the window containing `anchor`."""
    inwin = [w for w, a, b in words if b > lo and a < hi]
    low = [w.lower().strip(".,!?:;\"'") for w in inwin]
    if anchor not in low:
        return " ".join(inwin[:span])
    i = low.index(anchor)
    start = max(0, i - 1)
    return " ".join(inwin[start:start + span]).strip(" .,!?;:")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug = args[0]
    write = "--write" in sys.argv

    beats_p, beats, words, shows = load(slug)
    scenes = beats["scenes"]

    linked, needs_human, already = 0, [], 0
    cursor = 0.0
    for i, sc in enumerate(scenes):
        lo = cursor
        cursor += sc["durationSec"]
        hi = cursor
        if not shows_source(sc):
            continue
        spoken = " ".join(w for w, a, b in words if b > lo and a < hi)
        if not norm(spoken):
            continue                      # silent beat; G39 skips these too
        if str(sc.get("covers") or "").strip():
            already += 1
            continue

        desc = shows.get(sc.get("assetId"), "")
        overlap = content(desc) & content(spoken)

        if overlap:
            anchor = sorted(overlap, key=lambda w: (-len(w), w))[0]
            cand = phrase_around(words, lo, hi, anchor)
            print(f"  scene {i:02d} {sc['type']:13} {lo:6.1f}-{hi:5.1f}s  "
                  f"LINK on {anchor!r}")
            print(f"        asset shows : {desc[:76]}")
            print(f"        voice says  : {spoken[:76]}")
            print(f"        covers      : {cand!r}")
            if write:
                sc["covers"] = cand
            linked += 1
        else:
            needs_human.append((i, sc, lo, hi, desc, spoken))

    if needs_human:
        print(f"\n  {len(needs_human)} scene(s) where the asset's own description "
              "and the narration share NOTHING.")
        print("  This is the interesting case: usually the shot is against the "
              "wrong line, or\n  the manifest `shows` was written too vaguely to "
              "prove anything. Decide by hand.\n")
        for i, sc, lo, hi, desc, spoken in needs_human[:12]:
            print(f"  scene {i:02d} {sc['type']:13} {lo:6.1f}-{hi:5.1f}s "
                  f"{sc.get('assetId') or sc.get('src','')[-28:]}")
            print(f"        asset shows : {(desc or '(no manifest entry)')[:76]}")
            print(f"        voice says  : {spoken[:76]}")
        if len(needs_human) > 12:
            print(f"  ... and {len(needs_human) - 12} more")

    print(f"\n  {already} already linked · {linked} justified by both sides · "
          f"{len(needs_human)} need a human")
    if write and linked:
        beats_p.write_text(json.dumps(beats, indent=2) + "\n")
        print(f"  wrote {linked} `covers` to {beats_p.relative_to(ROOT)}")
        print("  The unjustified ones were LEFT EMPTY on purpose — filling them "
              "from the\n  transcript alone would make G39 pass without proving "
              "anything.")
    elif not write:
        print("  (--write fills only the justified ones)")


if __name__ == "__main__":
    main()
