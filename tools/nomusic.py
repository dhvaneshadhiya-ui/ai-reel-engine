#!/usr/bin/env python3
"""Derive a reel's music-free sibling, and prove it has not drifted.

WHY
---
Three `-nomusic` sheets exist as SEPARATE FILES, each hand-emitted by its build
script. Measured 2026-08-18:

    ios27-tiers-nomusic          identical apart from `id`   (a pure duplicate)
    september-preview-nomusic    12 scenes differ
    iphone-fold-ultra-nomusic    36 scenes differ

The last one drifted the same day: every fix applied to the parent — the caption
lane, the twin receipts, the paced timings, the SFX calibration — went to
`iphone-fold-ultra.json` and none of them reached its sibling, because the
sibling is a stored document rather than a derivation. A second copy of a thing
is a second thing to forget.

A music-free variant is not a different reel. It is the same reel with the bed
removed, which is a FUNCTION of the parent:

    python3 tools/nomusic.py <slug>            # would it change? (drift report)
    python3 tools/nomusic.py <slug> --write    # regenerate from the parent

ADVICE, and deliberately not wired into render_job. Regenerating a sibling
silently during a render would overwrite whatever a person had deliberately
changed in it — and the whole reason these drifted is that nobody was told.
This makes the difference visible and the regeneration explicit.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEATS = ROOT / "src/beats"


def derive(parent: dict, slug: str) -> dict:
    """The parent with a SILENT bed. Everything else travels unchanged.

    THE CONVENTION HAD DRIFTED TOO, which is its own small lesson: two of the
    three siblings swap `music.src` for music/silence.mp3 and keep the volume
    automation, and the third drops the music block entirely and sets
    `noMusic: true`. Three files, two conventions, no note anywhere saying which
    was intended.

    The silence bed wins because it is the one with a recorded reason —
    tools/build_ios27tiers.py:33 says "The volume automation is kept identical
    so G09 still fires on a flat bed; only the audio file is silent." Dropping
    the block instead means the gate that checks the ducking curve has nothing
    to check, so the variant is no longer testing what its parent tests.
    """
    child = json.loads(json.dumps(parent))          # deep copy
    child["id"] = f"{slug}-nomusic"
    if isinstance(child.get("music"), dict):
        child["music"]["src"] = "music/silence.mp3"
    child["noMusic"] = True
    child["noMusicReason"] = (
        "derived from the parent by tools/nomusic.py — do not hand-edit; "
        "re-run that tool instead")
    return child


def diff(a: dict, b: dict) -> list[str]:
    out = []
    sa, sb = a.get("scenes", []), b.get("scenes", [])
    if len(sa) != len(sb):
        out.append(f"scene count {len(sb)} -> {len(sa)}")
    else:
        n = sum(1 for x, y in zip(sa, sb) if x != y)
        if n:
            out.append(f"{n} of {len(sa)} scene(s) differ")
    for k in sorted(set(a) | set(b)):
        if k in ("scenes", "noMusicReason"):
            continue
        if a.get(k) != b.get(k):
            out.append(f"key {k!r} differs")
    return out


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug, write = args[0].replace("-nomusic", ""), "--write" in sys.argv

    parent_path = BEATS / f"{slug}.json"
    if not parent_path.exists():
        sys.exit(f"no parent sheet at {parent_path}")
    child_path = BEATS / f"{slug}-nomusic.json"

    want = derive(json.loads(parent_path.read_text()), slug)
    have = json.loads(child_path.read_text()) if child_path.exists() else None

    if have is None:
        print(f"\n  {slug}-nomusic does not exist yet")
    else:
        d = diff(want, have)
        if not d:
            print(f"\n  {slug}-nomusic is in sync with its parent")
            return
        print(f"\n  {slug}-nomusic has DRIFTED from its parent:")
        for line in d:
            print(f"    {line}")

    if write:
        child_path.write_text(json.dumps(want, indent=2) + "\n")
        print(f"\n  regenerated {child_path.name} from {parent_path.name}\n")
    else:
        print("\n  (--write to regenerate it from the parent)\n")


if __name__ == "__main__":
    main()
