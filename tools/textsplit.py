#!/usr/bin/env python3
"""Sentence splitting that knows an abbreviation from a full stop.

WHY THIS EXISTS (2026-09-02)
----------------------------
Four tools carried the same line — `re.split(r"(?<=[.!?])\\s+", body)` — and
all four broke on the same input. `claude-fable-5-1` opens:

    This AI was so powerful, the U.S. Government literally banned foreign
    nationals from using it.

Every one of them cut it after "the U.S.", so:

  * `vo_tagged.py` emitted "the U.S." as its own line, which is a hard pause
    mid-phrase in the ElevenLabs read — on a ~1,250-credit render.
  * `plan_shots.py` opened a shot on the orphan "Government literally
    banned...", so the cut landed mid-noun-phrase.
  * `check_script.py` measured a 5-word sentence that nobody says, which moves
    the cadence and bridge numbers it advises on.

The failure is one bug in four copies, so the fix is one function they all
import rather than four regexes that drift. Same reason `reel_gates` is
imported rather than re-implemented per build script.

Self-test: `python3 tools/textsplit.py --selftest` (run by doctor).
"""

from __future__ import annotations

import re

# Abbreviations whose trailing period is NOT a sentence end. Kept deliberately
# short: every entry is one we have actually written or would plausibly write
# in a news script. A long list of honorifics we never use is dead weight, and
# each entry is a chance to swallow a real sentence boundary.
_ABBR = (
    r"U\.S|U\.K|E\.U|U\.N|"          # the ones that actually bit us
    r"Dr|Mr|Mrs|Ms|Jr|Sr|St|Prof|"
    r"Inc|Ltd|Co|Corp|"
    r"vs|etc|e\.g|i\.e|approx|"
    r"a\.m|p\.m|No|Fig|Vol|Est"
)
# A private-use sentinel: it cannot occur in a script, so masking is reversible.
_DOT = "\x00"


def sentences(text: str, *, strip_headers: bool = True) -> list[str]:
    """Split prose into sentences, leaving abbreviations intact.

    `strip_headers` drops blank lines and the markdown prefixes every caller
    already skipped by hand: headings, block quotes and HTML comments.
    """
    lines = text.splitlines()
    if strip_headers:
        lines = [ln for ln in lines
                 if ln.strip() and not ln.lstrip().startswith(("#", ">", "<!--"))]

    # A LINE BREAK IS A HARD BOUNDARY, and taking it first is what makes the
    # abbreviation mask safe. Masking alone cannot decide "in the U.S. Nobody
    # noticed" — the period is both an abbreviation's and a sentence's, and no
    # regex recovers that. In this repo scripts are authored one sentence per
    # line, so the author has already answered it; we just have to read the
    # answer instead of guessing.
    # ponytail: same-line "...the U.S. Nobody..." still joins. Put the second
    # sentence on its own line (which script.md already does) or teach this a
    # real tokenizer if a script ever genuinely needs it mid-line.
    out: list[str] = []
    for ln in lines:
        # Mask the period that ENDS a known abbreviation, split, then restore.
        # A lookbehind cannot do this: Python requires fixed width, and "U.S"
        # and "approx" are not the same length.
        masked = re.sub(rf"\b({_ABBR})\.", rf"\1{_DOT}", ln)
        for part in re.split(r"(?<=[.!?])\s+", masked):
            part = part.replace(_DOT, ".").strip()
            if part:
                out.append(part)
    return out


def selftest() -> int:
    ok = True

    def check(label: str, cond: bool) -> None:
        nonlocal ok
        if not cond:
            ok = False
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")

    # THE CASE THAT PAID FOR THIS FILE. Both halves must stay in one sentence.
    got = sentences(
        "This AI was so powerful, the U.S. Government literally banned foreign "
        "nationals from using it.\nAnd now, Anthropic just dropped its 5.1 upgrade."
    )
    check("'the U.S. Government' is not split", len(got) == 2)
    check("the abbreviation survives intact", "U.S. Government" in got[0])

    got = sentences("When Mythos first launched, the U.S. Treasury Secretary called a meeting.")
    check("'the U.S. Treasury' is one sentence", len(got) == 1)

    # It must still split ordinary sentences, including one ENDING in an
    # abbreviation — the case a naive mask would swallow.
    check("ordinary sentences still split",
          len(sentences("One. Two. Three.")) == 3)
    # A sentence ENDING in an abbreviation is genuinely ambiguous mid-line, so
    # the line break is what resolves it — and script.md is written that way.
    check("a sentence ending in an abbreviation splits across lines",
          len(sentences("They shipped it in the U.S.\nNobody noticed.")) == 2)
    check("the known ceiling is what we think it is (same line stays joined)",
          len(sentences("They shipped it in the U.S. Nobody noticed.")) == 1)
    check("question and exclamation still split",
          len(sentences("Why? Because it did! Then it stopped.")) == 3)
    check("headings and blanks are dropped",
          sentences("# Title\n\nOne sentence here.") == ["One sentence here."])
    check("no sentinel leaks into the output",
          all("\x00" not in s for s in sentences("The U.S. and the U.K. agreed.")))

    print("\n  self-test PASSED\n" if ok else "\n  self-test FAILED\n")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys

    raise SystemExit(selftest() if "--selftest" in sys.argv else selftest())
