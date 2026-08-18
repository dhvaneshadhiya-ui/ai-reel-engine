#!/usr/bin/env python3
"""Measure a script's PROSE, not its facts.

WHY THIS EXISTS
---------------
styles/editorial-script-playbook.md line 57 already says:

    "Short declaratives, ~8-14 words, ONE idea each. Then occasionally one long
     spec sentence deliberately PACKED with numbers (the 'spec dump')."

The AirPods script — the best one this pipeline has produced — has ZERO sentences
over 20 words. The rule was written, read, and skipped, which is the same thing
that happened to script approval, to the credit position, and to the mobile
capture rule. Prose guidance does not survive contact with a deadline. So this
measures what the playbook asks for and prints the numbers.

    python3 tools/check_script.py <slug>
    python3 tools/check_script.py --text "..."

EVERYTHING HERE IS ADVICE. Style is craft, and the constitution leaves craft to
the author: only the three standing rules may block a render. A script that
breaks every guideline below and reads brilliantly is a good script — the numbers
exist so the choice is deliberate rather than accidental.
"""
from __future__ import annotations

import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LONG_SENTENCE = 18       # the playbook's "occasionally one long sentence"
FRAGMENT = 4             # words or fewer reads as a full-stop fragment
YOU_BY = 0.40            # the viewer should be addressed in the first 40%

# Section headers read aloud. They announce structure the picture is already
# showing, and they cost a beat each.
STAGE_DIRECTIONS = re.compile(
    r"^(so\s+)?(what|why|how|when|where|who)('s|\s+is|\s+are|\s+do|\s+does)?"
    r"[^?]{0,18}\?$", re.I)

# Business-speak in an otherwise plain script. Each one has a plainer twin.
HEDGES = {
    "north of": "more than",
    "sit at": "cost",
    "sits at": "costs",
    "in terms of": "(cut it)",
    "when it comes to": "(cut it)",
    "leverage": "use",
    "utilise": "use",
    "utilize": "use",
    "a number of": "some",
    "at this point in time": "now",
    "going forward": "(cut it)",
    "reach out": "ask",
    "deep dive": "look",
}


def sentences(text: str) -> list[str]:
    body = " ".join(l.strip() for l in text.splitlines()
                    if l.strip() and not l.lstrip().startswith(("#", ">", "<!--")))
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]


def check(text: str) -> list[str]:
    ss = sentences(text)
    if not ss:
        return ["  no sentences found"]
    lens = [len(s.split()) for s in ss]
    words = sum(lens)
    notes: list[str] = []

    print(f"  {len(ss)} sentences · {words} words · mean {statistics.mean(lens):.1f}"
          f" · median {statistics.median(lens)} · longest {max(lens)}")

    # 1. ONE GEAR. Short sentences land because something longer preceded them.
    longs = [n for n in lens if n >= LONG_SENTENCE]
    if len(longs) < 2 and len(ss) > 8:
        # ONE long sentence in twenty is not a gear change, it is an outlier —
        # and on the script that prompted this check, the single longest sentence
        # was a QUOTE, not a written one. Ask for two before calling it variation.
        notes.append(
            f"CADENCE: only {len(longs)} sentence reaches {LONG_SENTENCE} words "
            f"(longest {max(lens)}). The playbook asks for 'occasionally one long "
            "spec sentence' — with everything short, nothing reads as short. "
            "Nothing to push against.")
    elif len(longs) > len(ss) * 0.25:
        notes.append(f"CADENCE: {len(longs)} of {len(ss)} sentences are long. "
                     "The short ones stop being punctuation.")

    # 2. THE SAME MOVE, OVER AND OVER. A medium sentence closed by a fragment is
    #    a strong device; used six times it is a tic the ear predicts.
    shape = sum(1 for a, b in zip(lens, lens[1:]) if a >= 6 and b <= FRAGMENT)
    if shape >= 4:
        notes.append(
            f"SHAPE: the 'statement, then a {FRAGMENT}-word fragment' move "
            f"appears {shape} times. By the third the ear predicts it and the "
            "fragments stop landing as emphasis.")

    # 3. STAGE DIRECTIONS. "So what's inside?" announces a section.
    stage = [s for s in ss if STAGE_DIRECTIONS.match(s.strip())]
    if stage:
        notes.append(
            f"STAGE DIRECTIONS: {len(stage)} — {', '.join(repr(s) for s in stage[:3])}. "
            "These announce structure the visual is already showing. Delete them; "
            "the sentence after each one stands up alone.")

    # 4. WHEN DOES THE VIEWER ENTER? Third-person reportage is happening to
    #    other people.
    flat = " ".join(ss)
    # Strip quoted matter first. A "you" inside a quote is the SOURCE addressing
    # the viewer — Apple's ad copy saying "your world becomes savable" is not the
    # script speaking to anyone, and counting it hides a late entrance.
    unquoted = re.sub(r"[\"“”'][^\"“”']{8,}[\"“”']", " ", flat)
    unquoted = re.sub(r":\s*[a-z][^.!?]*", " ", unquoted)   # "Siri answers: ..."
    m = re.search(r"\byou\b|\byour\b|\byou're\b|\byou'll\b", unquoted, re.I)
    if not m:
        notes.append("SECOND PERSON: the script never says 'you'. It is reportage "
                     "about a company, not something happening to the viewer.")
    else:
        at = len(unquoted[:m.start()].split()) / max(1, words)
        if at > YOU_BY:
            notes.append(
                f"SECOND PERSON: the first 'you' arrives {at:.0%} of the way in. "
                "Until then the viewer is watching something happen to other "
                "people. Move one 'you' into the opening.")

    # 5. DICTION. Business-speak beside plain writing reads as a seam.
    low = flat.lower()
    hits = [(h, p) for h, p in HEDGES.items() if re.search(rf"\b{re.escape(h)}\b", low)]
    if hits:
        notes.append("DICTION: " + "; ".join(f"{h!r} -> {p}" for h, p in hits))

    # 6. NUMBER DENSITY — also the playbook's own rule.
    nums = len(re.findall(r"\$?\d[\d.,]*", flat))
    per = len(ss) / nums if nums else 999
    if nums and per > 3.5:
        notes.append(f"NUMBERS: one every {per:.1f} sentences. The playbook asks "
                     "for one every 2-3 — concrete numbers are what make a claim "
                     "feel reported rather than asserted.")
    return notes


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--text" in sys.argv:
        i = sys.argv.index("--text")
        text = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
    elif args:
        p = ROOT / f"jobs/{args[0]}/script.md"
        if not p.exists():
            sys.exit(f"no script at {p}")
        text = p.read_text()
    else:
        sys.exit(__doc__.split("    python3")[0].strip())

    print()
    notes = check(text)
    print()
    if not notes:
        print("  nothing to flag. Read it aloud anyway — this measures shape, "
              "not whether it is any good.")
    for n in notes:
        print(f"  - {n}")
    print("\n  ADVICE, not rules. A script that breaks all of this and reads "
          "brilliantly\n  is a good script; the numbers are here so the choice is "
          "deliberate.")


if __name__ == "__main__":
    main()
