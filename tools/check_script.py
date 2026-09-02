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

STRUCTURE, ADDED 2026-08-19. The checks above measure sentence SHAPE — length,
fragments, whether the viewer is addressed. They passed a script the user called
weak with "nothing to flag", because shape was never the problem: the problem
was that the script is a LIST OF FACTS rather than a story, which is what
styles/shortform-script-framework.md is about.

CALIBRATED ON A MATCHED PAIR, which is why these thresholds are not invented.
Two scripts on the SAME topic (iPhone 18 Pro), one the approved script in
jobs/iphone-18-pro/script.md and one the weak generation the user pasted:

                              approved   weak
    sentences with a bridge     53%       9%     <- the sharpest signal by far
    spec-sentence density       31%      58%
    longest run of spec lines    4        5
    curiosity / loop devices     3        1

The approved script opens "Apple's iPhone 18 Pro is expected on September 9" and
plants an open loop in its second sentence — "including one that only matters
when you have no signal" — then pays it off thirty seconds later with "Back to
that signal." The weak one opens on the framework's own Weak example and never
loops back to anything.

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


# The measurable half of "does this read like a person wrote it". The humanizer
# skill judges the rest; these are the stock constructions with near-zero
# false-positive risk in a spoken news script — drawn from its Wikipedia-derived
# signs plus the framework's own S4 filler list.
#
# CALIBRATED 2026-08-21 against every approved script in the repo (9 jobs + the
# shipped beat-sheet narrations): each phrase below fires on ZERO of them.
# Two candidates were DROPPED by that run, not by taste — "isn't just" is in the
# approved iphone-18-pro script and "the catch?" is in september-preview. A tell
# the user's own approved writing uses is not a tell, it is their voice.
AI_TELLS = [
    "not just about", "here's the thing", "here's the kicker", "the kicker",
    "let that sink in", "game-changer", "game changer", "a testament to",
    "the world of", "in today's", "seamless", "seamlessly", "elevate", "delve",
    "buckle up", "spoiler alert", "plot twist", "look no further",
    "without further ado", "dive into", "let's dive", "the best part?",
    "but that's not all", "another interesting thing", "and there's more",
    "landscape", "arguably", "crucial", "in a world where", "say goodbye to",
    "meet the new", "enter the", "revolutionary", "stunning", "sleek",
    "but here's where",
]

# HYPE MARKERS — the creator-sell register, measured off the ai-tools corpus
# (formats/ai-tools.md, 8 transcripts, 2026-08-25). The teardown adopted that
# corpus's COMPRESSION and its fused function-plus-name, and explicitly
# rejected its SELL: "Their hype markers are NOT ours. The house register is
# reporting."
#
# That rejection lived only in prose, so a future ai-tools script could carry
# "completely free" three times and nothing would say a word — exactly the
# failure mode this repo exists to prevent. Separate from AI_TELLS because
# these are not signs of a machine writing; they are signs of a SALESMAN
# writing, and a human would produce them enthusiastically.
HYPE_MARKERS = [
    "yes you heard it right", "you heard that right", "the crazy part",
    "the craziest part", "the best part is", "completely free", "100% free",
    "totally free", "for free", "insane", "insanely", "mind-blowing",
    "mind blowing", "this is huge", "trust me", "i'm not kidding",
    "no joke", "literally the best", "you won't believe", "wait till you see",
    "wait until you see", "absolute game", "blew my mind",
]


def house_tics(text: str, exclude_slug: str | None = None,
               min_n: int = 3) -> list[str]:
    """Phrases this repo has already used in another script.

    THE CHECKER WAS MANUFACTURING THE TIC (2026-08-26, user). `FORWARD` above
    is a phrase list, and NO OPEN LOOP punishes any script that does not match
    it — so every writer reaches for the same recognised words. Measured
    across the corpus when the user asked why every script sounds the same:

        "here's the"                8 scripts
        "the catch"                 4 scripts
        "the part almost nobody noticed"   3 scripts, verbatim
        "tell me in the comments"   3 scripts

    A checker that rewards specific phrasing produces house style by
    accident, and house style repeated verbatim is a tic. So this is the
    OPPOSING FORCE: the loop detector still insists a loop exists, and this
    makes reusing last reel's words cost something. You must open a loop —
    in your own words, this time.

    Same principle as STYLE-RULES' rule against repeating the previous reel's
    visual treatment, applied to language.

    Proper nouns and numbers are excluded: a subject recurring across scripts
    about the same subject is not a tic, it is the subject.
    """
    def grams(t: str) -> set[str]:
        body = " ".join(l for l in t.splitlines()
                        if l.strip() and not l.lstrip().startswith("#"))
        out: set[str] = set()
        for sent in re.split(r"(?<=[.!?])\s+", body):
            toks = sent.split()
            for n in range(min_n, min_n + 3):
                for i in range(len(toks) - n + 1):
                    g = toks[i:i + n]
                    if any(w[:1].isupper() for w in g[1:]):
                        continue                      # carries a proper noun
                    if any(any(c.isdigit() for c in w) for w in g):
                        continue
                    phrase = re.sub(r"[^a-z' ]", "", " ".join(g).lower()).strip()
                    if len(phrase.split()) >= min_n:
                        out.add(phrase)
        return out

    mine = grams(text)
    if not mine:
        return []
    seen: dict[str, set[str]] = {}
    for f in sorted((ROOT / "jobs").glob("*/script.md")):
        slug = f.parent.name
        if exclude_slug and slug == exclude_slug:
            continue
        try:
            for g in grams(f.read_text()) & mine:
                seen.setdefault(g, set()).add(slug)
        except OSError:
            continue
    # keep the LONGEST form of each overlap: "here's the part that matters"
    # rather than also reporting the four fragments inside it
    phrases = sorted(seen, key=len, reverse=True)
    kept: list[str] = []
    for ph in phrases:
        if not any(ph in longer for longer in kept):
            kept.append(ph)
    notes = []
    for ph in sorted(kept, key=lambda p: -len(seen[p]))[:6]:
        who = ", ".join(sorted(seen[ph])[:3])
        notes.append(
            f"HOUSE TIC: {ph!r} — already used in {len(seen[ph])} other "
            f"script(s) ({who}). Say it a different way; a phrase the channel "
            "reuses stops being a hook and becomes a verbal habit.")
    return notes


def sentences(text: str) -> list[str]:
    body = " ".join(l.strip() for l in text.splitlines()
                    if l.strip() and not l.lstrip().startswith(("#", ">", "<!--")))
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]


# A sentence carrying a measurement — the raw material of a spec dump.
SPEC = re.compile(r"\d+\s*(%|MP|nm|mm|GB|W|x)\b|\$\d|\b\d{2,}\b")
# Words that tie a sentence to the one before it. The framework calls these
# bridges (S9) and the "next sentence" chain (S22); measured, they are what
# separates a story from a list more reliably than anything else here.
BRIDGE = re.compile(
    r"^(and|but|so|then|that|this|those|these|which|because|back to|pair |"
    r"start with|inside|outside|now|here'?s|meanwhile|instead|yet|still)\b", re.I)
# A spec sentence earns its place by saying what the number DOES to the viewer.
CONSEQUENCE = re.compile(
    r"\b(so|which means|that means|you|your|notice|matters|in practice|enough to|"
    r"without|instead of)\b", re.I)
# FORWARD REFERENCE — a sentence that points at something it has not named yet.
# This is half of an open loop; the other half is whether anything later
# resolves it, which a phrase list cannot see.
FORWARD = re.compile(
    r"\b(only one|one of (them|these)|the most \w+ one|the one (you|i|that)|"
    r"only matters when|here'?s (the|why|what)|the part that|the catch|"
    r"what nobody|nothing to do with|what makes it different|the real (story|reason)|"
    r"but first|something \w+ have never)\b", re.I)
# NOT a loop: "three changes are coming". An ENUMERATION announces the agenda —
# it promises structure (framework S2) and withholds nothing (S10). Including it
# made the detector call a false loop on a script whose opening states its thesis
# outright and whose ending therefore restates rather than pays off. The two
# devices are different sections of the framework for a reason.
# An explicit return to something raised earlier.
CALLBACK = re.compile(
    r"\b(back to (that|the)|remember|that same|as i said|the one i (mentioned|said))\b",
    re.I)
_STOP = set("""the a an and or but so of in on for with to from that this these those
it its is are was were be been will would could may might can has have had you your
i we they he she them his her our not no as at by if then than when what which who
about into over more most one two three new now just also very really actually
# HEDGES CAN NEVER BE EVIDENCE OF A CALLBACK. framework S20 and the manifest
# exclusions REQUIRE "reportedly" / "projected" / "expected" on unreleased
# claims, so they repeat by obligation, not by design. Found 2026-08-19: the
# Explainer script's loop was being resolved by "reportedly" appearing twice —
# the right answer for a reason that would also pass a script whose promise is
# never paid off.
reportedly projected expected rumored official reports according""".split())


def open_loop(ss: list[str]) -> tuple[bool, str]:
    """Is something PROMISED early and RESOLVED later?

    WHY THIS IS NOT A PHRASE LIST (2026-08-19)
    ------------------------------------------
    The first version matched a dozen loop-shaped phrases. It reported NO OPEN
    LOOP on a draft whose second sentence was "the most useful one has nothing
    to do with the camera" — a real loop, paid off two beats later. A checker
    that misses the thing it is named after is worse than absent, and widening
    the list to cover whatever was just written is calibration by wishful
    thinking.

    So it looks for the STRUCTURE instead: a forward reference in the opening
    third, and a later sentence that resolves it — either by an explicit
    callback, or by returning to a word the promise introduced. The word has to
    be DISTINCTIVE (rare in this script), because every script repeats its own
    subject and "phone" appearing twice proves nothing.

    Validated against five scripts with hand-judged answers; see selftest().
    """
    n = len(ss)
    if n < 6:
        return True, ""
    third = max(2, n // 3)
    tail = ss[max(third, n // 2):]

    counts: dict[str, int] = {}
    for sent in ss:
        for w in re.findall(r"[a-z]{5,}", sent.lower()):
            if w not in _STOP:
                counts[w] = counts.get(w, 0) + 1

    # TRY EVERY CANDIDATE, not just the first. The first version returned on the
    # first forward-looking sentence it found, so an Explainer that says "Here's
    # the mechanism." before its real loop was judged on the throwaway and
    # reported NO OPEN LOOP with an actual loop two sentences further down.
    # A detector that stops at the first candidate is testing sentence order.
    # WITHHELD ENUMERATION — a forward reference written in the author's OWN
    # words, which a phrase list can never see (2026-08-26).
    #
    # "Four things it won't write at all." names a count and withholds the
    # items. That is a loop by structure, and FORWARD would miss it because
    # the sentence contains none of its phrases. The repo's own note above
    # warns against widening a phrase list to fit whatever was just written —
    # so this is not another phrase. It is the test the code already
    # articulates for the opposite case: "three changes are coming" is NOT a
    # loop precisely because the items follow immediately. Withheld until
    # later = loop; filled at once = agenda.
    #
    # This matters beyond one script. The phrase list was PRESCRIBING the
    # house voice — "here's the" reached 8 scripts, "the part almost nobody
    # noticed" appeared verbatim in 3 — because a script that did not use a
    # listed phrase was told it had no loop. Reading structure instead is what
    # lets every reel open its loop in its own language.
    CARDINAL = re.compile(
        r"\b(two|three|four|five|six|seven|eight|nine|ten)\s+"
        r"([a-z]{3,})\b", re.I)

    def withheld_enumeration(idx: int, sent: str) -> bool:
        m = CARDINAL.search(sent)
        if not m:
            return False
        near = " ".join(ss[idx + 1: idx + 3]).lower()
        # if the items are spelled out immediately, it is an agenda, not a loop
        return not re.search(r"\bfirst\b|\bone[:,]|\bstart with\b", near)

    unresolved: str | None = None
    for i, sent in enumerate(ss[:third]):
        if not FORWARD.search(sent) and not withheld_enumeration(i, sent):
            continue
        distinctive = {w for w in re.findall(r"[a-z]{5,}", sent.lower())
                       if w not in _STOP and counts.get(w, 0) <= 3}
        # A callback often repeats the CONSTRUCTION, not a rare noun: "the one
        # I'd care about most" -> "here's the one I'd actually want" shares no
        # distinctive word at all, only the phrase "the one i'd". Word overlap
        # alone misses every loop written that way.
        def grams(sent: str) -> set[str]:
            w = re.findall(r"[a-z']+", sent.lower())
            return {" ".join(w[j:j + 3]) for j in range(len(w) - 2)}
        promise_grams = grams(sent)
        for later in tail:
            if CALLBACK.search(later):
                return True, f"sentence {i + 1} -> callback"
            if distinctive & {w for w in re.findall(r"[a-z]{5,}", later.lower())}:
                return True, f"sentence {i + 1} -> resolved by a shared term"
            if promise_grams & grams(later):
                return True, f"sentence {i + 1} -> resolved by a repeated phrase"
        if unresolved is None:
            unresolved = (f"sentence {i + 1} promises something "
                          f"({sent[:48]!r}) and nothing later returns to it")
    return False, unresolved or "nothing in the opening third points forward"


def structure_of(slug: str) -> str | None:
    """The declared S17 shape, from jobs/<slug>/structure.md."""
    import re as _re
    p = ROOT / f"jobs/{slug}/structure.md"
    if not p.exists():
        return None
    # The scaffold new_job.py writes the heading as "## SHAPE (S17)" — the
    # section-number suffix is part of the template, so the parser has to
    # tolerate it. Without the optional group this returned None for every
    # job created by the scaffold, and the shape-specific thresholds
    # silently fell back to the generic ones (found 2026-08-22).
    m = _re.search(r"^##\s*SHAPE\s*(?:\([^)]*\))?\s*\n+\**(\w[\w -]*)",
                   p.read_text(), _re.M)
    return m.group(1).strip() if m else None


def format_of(slug: str) -> str:
    """The reel's format, so the caveat below can name it."""
    import json
    bp = ROOT / f"src/beats/{slug}.json"
    if bp.exists():
        try:
            return json.loads(bp.read_text()).get("format") or "news"
        except Exception:  # noqa: BLE001
            pass
    return "news"


def structure(ss: list[str], shape: str | None = None) -> list[str]:
    """The framework's structural failures, made countable.

    styles/shortform-script-framework.md, sections 1, 3, 7, 9 and 21.
    """
    notes: list[str] = []
    n = len(ss)
    if n < 3:
        return notes

    spec = [s for s in ss if SPEC.search(s)]
    density = len(spec) / n
    bridged = sum(1 for s in ss[1:] if BRIDGE.match(s))
    bridge_rate = bridged / (n - 1)

    longest = cur = 0
    for s in ss:
        cur = cur + 1 if SPEC.search(s) else 0
        longest = max(longest, cur)

    if bridge_rate < 0.30:
        notes.append(
            f"  BRIDGES {bridged}/{n - 1} sentences ({bridge_rate:.0%}) connect to the "
            f"one before. The approved iPhone 18 Pro script runs 53%; the weak "
            f"generation of the same story ran 9%. A sentence that starts a new "
            f"subject with no bridge reads as the next bullet, not the next beat. "
            f"(framework S9, S22)")

    if density > 0.45:
        notes.append(
            f"  SPEC DENSITY {len(spec)}/{n} sentences ({density:.0%}) carry a "
            f"measurement. Past ~45% the viewer stops hearing numbers as meaning. "
            f"(framework S21: 6 connected ideas beat 20 facts)")

    if longest >= 5:
        notes.append(
            f"  SPEC RUN {longest} sentences in a row each deliver a number — that "
            f"is the source article's order, not a story's. Ask which fact "
            f"EXPLAINS another and reorder. (framework S3)")

    # A CONSEQUENCE MAY LAND IN THE NEXT SENTENCE. "Kuo says the lens costs 50%
    # more." / "That's how much they're betting on it." is a spec followed by its
    # so-what, and the per-sentence version scored it as bare — it fired 4/5 on
    # the APPROVED script too, which is the signature of a check that is
    # over-firing rather than finding anything. Verified against both fixtures:
    # widening the window leaves the weak script's run of bare specs intact.
    idx = {id(x): i for i, x in enumerate(ss)}
    def has_so_what(sent: str) -> bool:
        i = idx[id(sent)]
        window = " ".join(ss[i:i + 2])
        return bool(CONSEQUENCE.search(window))
    bare = [s for s in spec if not has_so_what(s)]
    if spec and len(bare) / len(spec) > 0.6:
        notes.append(
            f"  WHAT WITHOUT SO WHAT {len(bare)}/{len(spec)} spec sentences never say "
            f"what the number does for the viewer. \"2nm chip\" is information; "
            f"\"faster without draining the battery\" is relevance. (framework S7)")

    has_loop, why = open_loop(ss)
    if not has_loop:
        notes.append(
            f"  NO OPEN LOOP — {why}. Nothing promised early gets paid off later, so "
            f"the ending summarises instead of arriving. The approved script plants "
            f"one in sentence two (\"only matters when you have no signal\") and "
            f"returns to it with \"Back to that signal.\" (framework S2, S10, S18)")

    # SHAPES THAT OPEN ON A QUESTION ARE NOT MISSING THEIR ANCHOR.
    # framework S17 defines Explainer as "Question -> Context -> ...", Discovery
    # as "Hook -> Context -> Mystery", Story as "Hook -> Setup", Myth-busting as
    # "Common belief -> ...". In every one the context arrives in beat TWO by
    # design. Demanding a version or date in sentence one encodes the NEWS
    # opening ("what happened") and nothing else, which is what it was
    # calibrated on. Declared in jobs/<slug>/structure.md; undeclared falls back
    # to the news-shaped check, so a script that never chose a shape is still
    # held to the stricter reading.
    QUESTION_OPENERS = {"explainer", "discovery", "story", "myth-busting",
                        "transformation", "tutorial"}
    first = ss[0]
    if (shape or "").lower() in QUESTION_OPENERS:
        pass
    elif not re.search(r"\d", first) and not re.search(
            r"\b(today|tomorrow|this week|just|now|yesterday)\b", first, re.I):
        notes.append(
            f"  OPENING has no version, date or time anchor: {first[:64]!r}. A hook "
            f"without context is confusion — the viewer should know WHICH thing and "
            f"WHEN before the claim lands. (framework S1, S16)")
    return notes


def check(text: str, shape: str | None = None) -> list[str]:
    ss = sentences(text)
    if not ss:
        return ["  no sentences found"]
    lens = [len(s.split()) for s in ss]
    words = sum(lens)
    notes: list[str] = structure(ss, shape)

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

    # 3. QUESTIONS THE VIEWER CANNOT ANSWER YET.
    #
    # Two different faults, and the user drew the line 2026-08-18: being HOOKED
    # and being CONFUSED are not the same thing.
    #
    #   "So what's inside?"  weak, but parseable — "inside" resolves to the
    #                        product we were just told about
    #   "When?"              nothing to resolve. When WHAT? The previous sentence
    #                        was about function, not timing, so the word points at
    #                        nothing. The viewer hears the ANSWER first and
    #                        reconstructs the question backwards, losing the next
    #                        sentence while they catch up.
    #
    # It is worse on mute, where the caption is one unanchored word, and it is a
    # WRITTEN device: on a page "When?" reads as a subhead, spoken it is just a
    # fragment with no typographic signal.
    stage = [s for s in ss if STAGE_DIRECTIONS.match(s.strip())]
    bare = [s for s in stage if len(s.split()) <= 2]
    soft = [s for s in stage if s not in bare]
    if bare:
        notes.append(
            f"UNANCHORED QUESTION: {', '.join(repr(s) for s in bare)} — a bare "
            "question word with no noun. The viewer cannot tell what is being "
            "asked until they have heard the answer, so they parse it backwards "
            "and lose the next line. Give it its subject ('So when do we get "
            "them?') or make it a statement that still leans in ('They are closer "
            "than you'd think.').")
    if soft:
        notes.append(
            f"STAGE DIRECTION: {', '.join(repr(s) for s in soft)} — announces "
            "structure the picture is already showing. Deletable: the sentence "
            "after it stands up alone.")

    # 4. WHEN DOES THE VIEWER ENTER? Third-person reportage is happening to
    #    other people.
    flat = " ".join(ss)
    # Strip quoted matter first. A "you" inside a quote is the SOURCE addressing
    # the viewer — Apple's ad copy saying "your world becomes savable" is not the
    # script speaking to anyone, and counting it hides a late entrance.
    #
    # The lookarounds are load-bearing (2026-09-02). Without them a straight
    # apostrophe INSIDE a word opens a quote: "Anthropic's ... map's" deleted
    # everything between two possessives, and a script that said "you" twice
    # was reported as never saying it. A quote delimiter never sits flush
    # against word characters on the inside of a word; an apostrophe always
    # does. Test: selftest()'s apostrophe case.
    unquoted = re.sub(r"(?<!\w)[\"“”'][^\"“”']{8,}[\"“”'](?!\w)", " ", flat)
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

    # 5b. AI TELLS. Stock constructions that read as generated, calibrated so
    #     that no approved script trips one (see AI_TELLS above). Advice like
    #     everything here — but a script wearing three of these is not going to
    #     "feel like a human wrote it" no matter how good its structure is.
    tells = [t for t in AI_TELLS
             if re.search(rf"\b{re.escape(t)}", low)]
    if tells:
        notes.append(
            f"AI TELL: {', '.join(repr(t) for t in tells)} — stock phrasing that "
            "reads as generated (humanizer skill / Wikipedia's signs of AI "
            "writing). Zero approved scripts use any of these. Say it the way "
            "you would say it out loud.")

    # 5c. HYPE REGISTER. We are a PUBLISHER reporting a story, not an account
    #     selling one — the line the ai-tools teardown drew when it adopted
    #     that corpus's structure. "for free" is deliberately in the list and
    #     deliberately narrow: naming a price is fine ("it's free"), selling
    #     the price is not. Advice, like everything here.
    hype = []
    for h in HYPE_MARKERS:
        if not re.search(rf"\b{re.escape(h)}", low):
            continue
        # "for Free, Pro and Max" names a plan tier. Capitalised in the
        # ORIGINAL text means it is a proper noun, not the sell register
        # (false positive found 2026-08-26 by script_doctor on its own output).
        if h == "for free" and re.search(r"\bfor Free\b", flat):
            continue
        hype.append(h)
    if hype:
        notes.append(
            f"HYPE: {', '.join(repr(h) for h in hype)} — the creator-sell "
            "register. formats/ai-tools.md took that corpus's compression and "
            "rejected its sell; the house voice reports. Say what it does and "
            "let the number carry the excitement.")

    # 5d. ABANDONED LOOP — the script navigating its own structure aloud.
    #
    # DERIVED, not guessed (2026-08-25, from the whole approved corpus): a
    # promise deferred a long way is a GOOD open loop — iphone18-colors holds
    # one for 11 sentences and never mentions it again until the payoff. What
    # no approved script does is say "back to X" after wandering away from X.
    # claude-memory-everywhere promised "the part that matters most: some of
    # it Claude refuses to write down", spent nine sentences on unrelated
    # features, then wrote "Back to what it refuses to write down." The
    # sentence is the writer admitting the detour on the record, and the
    # viewer feels it as being lost.
    #
    # Measured across 13 scripts: approved ones return to nothing detectable
    # (a forward reference or a two-sentence aside); the weak one returns 9
    # sentences. The threshold sits at 5 — past a short, obviously deliberate
    # aside, and well under the observed failure.
    NAVBACK = ("back to", "as i said", "as mentioned", "returning to",
               "like i said", "to recap")
    _stop = {"the", "a", "an", "and", "or", "but", "of", "to", "in", "it",
             "is", "was", "that", "this", "those", "these", "you", "your",
             "what", "which", "now", "some", "its", "on", "off", "by", "for",
             "they", "them", "then", "so"}

    def _content(text: str) -> set[str]:
        return {w for w in re.findall(r"[a-z']+", text.lower())
                if w not in _stop and len(w) > 2}

    for i, sentence in enumerate(ss):
        low_s = sentence.lower()
        # "going back to 2019" is a date, not a navigation
        if not any(re.search(rf"{n}(?!\s+\d)", low_s) for n in NAVBACK):
            continue
        key = _content(sentence)
        for j in range(i - 1, -1, -1):
            if len(key & _content(ss[j])) >= 2:
                if i - j >= 5:
                    notes.append(
                        f"ABANDONED LOOP: sentence {i + 1} steers back to "
                        f"something last said in sentence {j + 1} — a "
                        f"{i - j}-sentence detour, then a signpost admitting "
                        f"it ({sentence[:48]!r}). No approved script in this "
                        "repo does that. Either move the promise next to its "
                        "payoff, or cut what came between; a loop the writer "
                        "has to announce a return to was not held.")
                break

    # 5e. PAGE PUNCTUATION IN A SPOKEN SCRIPT (2026-08-26, user: "why are
    #     em-dashes getting added, even though we have the humanizer?").
    #
    # This is not a style preference, and it does not rest on the em-dash
    # being an "AI tell" — it rests on two facts:
    #
    #   1. A LISTENER CANNOT HEAR ONE. The voice renders it as a pause,
    #      exactly like the comma or full stop you could have written. It is
    #      a mark for the eye in a medium with no eye.
    #   2. IT BREAKS THE SYNTHESIS. Probed 2026-08-26: IndexTTS2 rejects
    #      em-dash, colon and semicolon outright (`unencodableText`), and 8
    #      of 13 beats failed on exactly this before `speakable()` existed.
    #
    # Measured across the corpus when the question was first asked: grok-bot
    # and apple-pay-india carry one em-dash in ~350 words, while
    # claude-eating-tokens carried SIX in 159 — one every 26 words. Both ends
    # had been approved, so the first version of this check was advice with a
    # rate attached: 1-per-60.
    #
    # THE RATE WAS THE WRONG SHAPE (2026-09-01). The user asked the SAME
    # question a second time — "if you are humanizing our script, why are
    # there em dashes in our script?" — about a draft carrying TWO in 209
    # words. That is one every 104, comfortably inside 1-per-60, so this
    # check sat silent on exactly the thing it was built to catch. A
    # threshold that passes the case that prompts the complaint is not
    # calibrated, it is decorative.
    #
    # So the count is now ZERO, and the reasoning is unchanged and does not
    # depend on taste: a listener cannot hear a dash, and the local TTS
    # rejects it outright. There is no rate at which an inaudible mark earns
    # its place in a script nobody reads. Still ADVICE per RULES.md §0 —
    # prose is craft, and it fails none of the four blocking tests.
    dashes = flat.count("\u2014") + flat.count("\u2013")
    if dashes:
        notes.append(
            f"PAGE PUNCTUATION: {dashes} em/en-dash(es) in the narration. A "
            "listener cannot hear one; it becomes whatever pause you would "
            "have written anyway, and it breaks the local TTS outright. Write "
            "the comma or the full stop you mean. Target is ZERO, not a low "
            "rate — the rate version of this check stayed silent on the draft "
            "that got asked about twice. (The humanizer skill's job is the "
            "half of this a checker cannot measure — it is a MANUAL pass and "
            "nothing runs it for you.)")

    # 6. NUMBER DENSITY — also the playbook's own rule.
    nums = len(re.findall(r"\$?\d[\d.,]*", flat))
    per = len(ss) / nums if nums else 999
    if nums and per > 3.5:
        notes.append(f"NUMBERS: one every {per:.1f} sentences. The playbook asks "
                     "for one every 2-3 — concrete numbers are what make a claim "
                     "feel reported rather than asserted.")
    return notes


# The weak generation the user pasted on 2026-08-19, kept verbatim as the
# NEGATIVE control. Its partner is the approved script in the repo. Together
# they are the only evidence that these thresholds separate anything; without
# them the numbers are just numbers, which is how the shape checks came to pass
# this exact script with "nothing to flag".
WEAK_FIXTURE = """For the first time, an iPhone lens will physically open and close.
The iPhone 18 Pro is expected on September 9, and the biggest change is one you will see in your photos.
A mechanical iris on the 48MP main lens: it opens wide in the dark, then stops down when you want the whole frame sharp.
Analyst Ming-Chi Kuo called this two years ago. He says the lens alone costs Apple about 50% more than the one in the iPhone 17 Pro.
Behind it, the A20 Pro, Apple's first 2nm chip.
Projections put it about 15% faster than the A19 Pro, on roughly 30% less power.
The Dynamic Island shrinks about 35%, because Face ID's illuminator moves under the display.
The Pro Max gets about 10% more battery, and Apple's own C2 modem finally replaces Qualcomm.
Outside, a frosted one-piece back, and a new Dark Cherry finish.
None of this is official until Apple says it on stage.
So which one actually changes how you would use the phone?"""


# The user's revision of the framework draft, 2026-08-19. Kept as a fixture
# because it is the hard case: a GOOD script with NO open loop — its thesis is
# stated in sentence two, so the ending restates rather than arrives. A loop
# detector that cannot tell this apart from the weak generation is only
# detecting quality, which is not what it claims to measure.
USER_REVISION = """Apple's iPhone 18 Pro is expected on September 9. And three rumored changes could make it much better when your phone is pushed to its limits.
Start with the camera.
The main 48MP lens could get something iPhones have never had: a mechanical iris that physically opens and closes.
Wide in a dark room. Narrow when you want more of the frame in focus.
But moving parts and heavier computation can cost battery.
That's where the A20 Pro matters — Apple's first 2nm iPhone chip, reportedly about 15% faster while using 30% less power.
Pair that with a Pro Max battery that's rumored to be about 10% bigger.
And then there's the one you'd only meet on a bad day.
Apple's C2 modem could reportedly add 5G satellite connectivity, potentially keeping you connected when there's no cellular tower nearby.
So this isn't really just a camera story.
It's a phone designed to keep going when conditions get difficult — in the dark, when the battery is running low, or when you're out of range.
None of this is official until Apple says so.
Dark room, low battery, or no bars — which one would you actually notice first?"""


def selftest() -> int:
    """The weak script must flag; the approved one on the same topic must not.

    A style checker that stops discriminating is indistinguishable from one that
    is switched off, and this file spent a day telling everyone a list of facts
    was fine.
    """
    ok = True
    weak = [n for n in structure(sentences(WEAK_FIXTURE))]
    approved_path = ROOT / "jobs/iphone-18-pro/script.md"
    approved = (structure(sentences(approved_path.read_text()))
                if approved_path.exists() else None)

    def check_(label: str, cond: bool):
        nonlocal ok
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        ok = ok and cond

    # THE LOOP DETECTOR, against five scripts judged by hand. It replaced a
    # phrase list that missed a real loop; a structural detector that cannot
    # reproduce these five is not an improvement on the list it replaced.
    # GLOB, do not hardcode. This was ROOT/"jobs/iphone-18-pro/script-v2.md"
    # until the file was renamed to iphone-18-pro-script-v2.md, at which point
    # the case reported "fixture missing" — correctly, and only because the
    # suite fails loudly on a missing control instead of skipping it.
    v2c = sorted((ROOT / "jobs/iphone-18-pro").glob("*script-v2*.md"))
    v2 = (v2c[0].read_text().split("## Narration")[1].split("---")[0]
          if v2c else None)
    loop_cases = [
        ("weak generation", WEAK_FIXTURE, False),
        ("approved script", (approved_path.read_text()
                             if approved_path.exists() else None), True),
        ("v2 framework draft", v2, True),
        ("v3 user revision", USER_REVISION, False),
    ]
    for label, text, want in loop_cases:
        if text is None:
            check_(f"loop: {label} (fixture missing)", False)
            continue
        got, _why = open_loop(sentences(text))
        check_(f"loop: {label} -> {want}", got == want)

    check_(f"weak script trips >=4 structural checks (got {len(weak)})", len(weak) >= 4)
    for want in ("BRIDGES", "SPEC DENSITY", "NO OPEN LOOP", "OPENING"):
        check_(f"weak script trips {want}", any(want in n for n in weak))
    if approved is None:
        check_("approved script present for the positive control", False)
    else:
        check_(f"approved script trips <=2 (got {len(approved)})", len(approved) <= 2)
        check_("approved script does NOT trip BRIDGES",
               not any("BRIDGES" in n for n in approved))
        check_("approved script does NOT trip NO OPEN LOOP",
               not any("NO OPEN LOOP" in n for n in approved))
    # AI TELLS: the synthetic offender must fire, and the approved script — the
    # calibration corpus's own member — must stay silent. Runs through check()
    # because the tell scan lives there, not in structure().
    import contextlib, io
    def _notes_of(text: str) -> list[str]:
        with contextlib.redirect_stdout(io.StringIO()):
            return check(text)
    telly = ("This seamless upgrade is a game-changer for the world of phones. "
             "Here's the kicker: it could elevate everything. Let that sink in. "
             "But that's not all — buckle up.")
    fired = [n for n in _notes_of(telly) if n.startswith("AI TELL")]
    check_("AI TELL fires on the synthetic offender", bool(fired))
    check_("AI TELL names multiple phrases",
           bool(fired) and fired[0].count("'") >= 6)
    if approved_path.exists():
        clean = [n for n in _notes_of(approved_path.read_text())
                 if n.startswith("AI TELL")]
        check_("AI TELL silent on the approved script", not clean)
    # HYPE: same shape. The offender is the ai-tools corpus's own sell voice,
    # which is enthusiastic HUMAN writing — so it must trip HYPE and NOT be
    # caught by the AI-tell list, or the two checks are measuring one thing.
    selly = ("Yes you heard it right — this tool is completely free. "
             "The crazy part? It's insanely good. Trust me, this is huge.")
    hype_fired = [n for n in _notes_of(selly) if n.startswith("HYPE")]
    check_("HYPE fires on the creator-sell offender", bool(hype_fired))
    check_("HYPE names multiple markers",
           bool(hype_fired) and hype_fired[0].count("'") >= 6)
    check_("the sell offender is NOT caught by the AI-tell list instead",
           not [n for n in _notes_of(selly) if n.startswith("AI TELL")])
    if approved_path.exists():
        clean = [n for n in _notes_of(approved_path.read_text())
                 if n.startswith("HYPE")]
        check_("HYPE silent on the approved script", not clean)
    # ABANDONED LOOP: the fixture is the real 2026-08-25 draft that prompted
    # the check — a promise, a nine-sentence detour, then a signpost back.
    loopy = ("Claude keeps a file on you. "
             "But here's the part that matters most: some of it Claude "
             "refuses to write down. "
             "Everything it knows is a text file under a topic. "
             "A fix only has to happen once. "
             "Correct your company's old name there. "
             "Memory stopped staying put. "
             "The subjects it leaves alone are off by default. "
             "There's a switch if you want them in. "
             "It sends a notice each time. "
             "Back to what it refuses to write down.")
    fired = [n for n in _notes_of(loopy) if n.startswith("ABANDONED LOOP")]
    check_("ABANDONED LOOP fires on the real weak draft", bool(fired))
    tight = ("Claude keeps a file on you. "
             "Back to that file in a second. "
             "First, what is in it.")
    check_("a two-sentence aside does NOT trip it",
           not [n for n in _notes_of(tight) if n.startswith("ABANDONED LOOP")])
    if approved_path.exists():
        check_("ABANDONED LOOP silent on the approved script",
               not [n for n in _notes_of(approved_path.read_text())
                    if n.startswith("ABANDONED LOOP")])
    # HOUSE TIC: a phrase lifted verbatim from another script in the repo must
    # fire; original phrasing must not. Uses the real corpus on purpose — a
    # fixture corpus would not catch the checker drifting from what shipped.
    lifted = house_tics("But here's the part that matters most about this.",
                        exclude_slug="__none__")
    check_("HOUSE TIC fires on a phrase reused from another script",
           bool(lifted))
    fresh = house_tics(
        "Quarterly forecasting collapsed into a spreadsheet nobody reconciles.",
        exclude_slug="__none__")
    check_("HOUSE TIC silent on original phrasing", not fresh)
    dashy = ("The phone ships Tuesday \u2014 and the price is the story "
             "\u2014 which nobody expected \u2014 so here we are.")
    check_("PAGE PUNCTUATION fires on a dash-dense script",
           any(n.startswith("PAGE PUNCTUATION") for n in _notes_of(dashy)))
    # THE CASE THE RATE VERSION MISSED (2026-09-01). One dash in a script this
    # long is 1-per-30 by the old arithmetic only if the script is short — so
    # this pads to well past 1-per-60 and still must fire. Without this case,
    # tightening the threshold to zero could be quietly reverted.
    sparse = ("The phone ships Tuesday and the price is the story. " * 6
              + "Nobody expected it \u2014 so here we are.")
    check_("PAGE PUNCTUATION fires on a SINGLE dash in a long script",
           any(n.startswith("PAGE PUNCTUATION") for n in _notes_of(sparse)))
    clean = ("The phone ships Tuesday. The price is the story. "
             "Nobody expected it, so here we are.")
    check_("PAGE PUNCTUATION silent when the pauses are written out",
           not any(n.startswith("PAGE PUNCTUATION") for n in _notes_of(clean)))
    # APOSTROPHES ARE NOT QUOTE MARKS (2026-09-02). The quote-stripper ran
    # before the second-person check, and a straight apostrophe inside a word
    # opened a quote it then closed at the next possessive — deleting every
    # sentence in between. A script saying "you" twice was reported as never
    # saying it, and the deletion silently reached the checks downstream too.
    apos = ("Anthropic's model shipped Tuesday and the price is the story. "
            "So if you leave an agent running, you pay less than before. "
            "The map's resolution didn't move at all.")
    check_("SECOND PERSON does not claim 'never' when 'you' sits between two possessives",
           not any("never says" in n for n in _notes_of(apos)))
    # ...and the behaviour it exists for still works: a real quoted 'you' is
    # the SOURCE addressing the viewer, not the script, so it must NOT count.
    quoted = ("The phone ships Tuesday and the price is the story. "
              "Apple's own copy reads \"your world becomes savable now\". "
              "Nobody expected it, so here we are.")
    check_("SECOND PERSON still fires when the only 'your' is inside a quote",
           any(n.startswith("SECOND PERSON") for n in _notes_of(quoted)))
    print("\n  self-test PASSED\n" if ok else "\n  self-test FAILED\n")
    return 0 if ok else 1


# framework S25 — its own definition of done. Six are measured above; the rest
# need a person, and saying WHICH is the point. A checklist that pretends to
# verify things it cannot is how "credits present" sat on a checklist for weeks
# while AnnotateZoom drew its own.
FINAL_STANDARD = [
    ("measured", "The subject is clear within the opening seconds.", "OPENING"),
    ("eye", "The opening creates curiosity without creating confusion.", None),
    ("eye", "The viewer understands why the topic matters.", None),
    ("measured", "There is a clear narrative promise.", "NO OPEN LOOP"),
    ("measured", "Information organised for storytelling, not source order.", "SPEC RUN"),
    ("measured", "Individual facts are connected logically.", "BRIDGES"),
    ("eye", "The story has progression or escalation.", None),
    ("measured", "Curiosity gaps are paid off.", "NO OPEN LOOP"),
    ("measured", "Technical information translated into practical meaning.", "WHAT WITHOUT SO WHAT"),
    ("measured", "The script does not overload the viewer.", "SPEC DENSITY"),
    ("eye", "Transitions feel natural.", None),
    ("eye", "The viewer remains oriented throughout.", None),
    ("eye", "The narration sounds natural when spoken. READ IT ALOUD.", None),
    ("eye", "Visual opportunities exist for every major beat.", None),
    ("eye", "The ending provides a genuine payoff.", None),
    ("eye", "The CTA is specific and relevant.", None),
    ("eye", "Unconfirmed information is clearly treated as such.", None),
    ("eye", "Nothing important is presented without sufficient context.", None),
    ("eye", "It feels like a story rather than an article summary.", None),
]


def checklist(text: str) -> list[str]:
    """framework S25, with the measured items already answered."""
    fired = " ".join(structure(sentences(text)))
    out = ["  framework S25 — the final quality standard", ""]
    for kind, item, marker in FINAL_STANDARD:
        if kind == "measured":
            ok = marker not in fired
            out.append(f"  [{'x' if ok else ' '}] {item}"
                       + ("" if ok else f"   <- {marker} fired"))
        else:
            out.append(f"  [ ] {item}   (your eye — nothing measures this)")
    out += ["", "  Ticked boxes are MEASURED. Empty ones are not failures — they are",
            "  the questions no tool can answer, which is most of them."]
    return out


def critic(text: str) -> list[str]:
    """Turn the framework's THREE READING TESTS into a walkable list.

    S22 (the "next sentence" test), S23 (the confused viewer) and S24 (the
    boring article) are the tests no tool can perform — they need a reader. But
    "read it as a hostile viewer" is the same instruction the frame critic pass
    gives, and that one works because it names what to look at: a contact sheet
    with every frame on it.

    This is the contact sheet for prose. Every transition, numbered, with the
    question attached. The reader still does the work; they no longer have to
    hold the whole script in their head to do it.
    """
    ss = sentences(text)
    out = ["  SCRIPT CRITIC — framework S22 / S23 / S24",
           "  Read ALOUD. At each arrow, answer out loud before moving on.", ""]
    for i in range(len(ss) - 1):
        a, b = ss[i], ss[i + 1]
        out.append(f"  {i + 1:2}. {a}")
        out.append(f"      -> does the viewer have a reason to hear: {b[:62]!r}?")
    out.append(f"  {len(ss):2}. {ss[-1]}")
    out += ["",
            "  Then the two whole-script tests:",
            "   S23  Enter as someone who knows nothing. At every point: do I know",
            "        what we are talking about, and what I am waiting to discover?",
            "   S24  Read the voiceover with no visuals. Does it sound like someone",
            "        telling you something fascinating, or like 'according to reports,",
            "        another feature, another spec'? If the second, rewrite.",
            "",
            "  Nothing here is measured. That is the point — these are the questions",
            "  the numbers cannot reach, and skipping them is how a script passes",
            "  every check and still reads like an article."]
    return out


# ---------------------------------------------------------------- calibration
#
# AI_TELLS and the structural thresholds are CALIBRATED artifacts — frozen
# snapshots of the approved-script corpus on the day they were derived. The
# corpus grows with every approval, and the failure mode of a frozen
# calibration is quiet: the day an approved script legitimately uses one of
# the 36 phrases, the checker starts flagging the user's own approved voice
# at every propose, forever, and nothing says the calibration is stale.
#
# So the calibration is now a RECORD (tools/script_calibration.json: which
# scripts, which hashes, which collisions were knowingly accepted), and
# doctor warns when reality has moved past it. Re-deriving stays human —
# --recalibrate prints the evidence and refreshes the record; removing a
# tell or accepting a collision is a judgement call with a dated comment,
# same as every calibrated number in this repo.

def _cal_path() -> Path:
    return ROOT / "tools" / "script_calibration.json"


def corpus() -> dict[str, dict]:
    """Every approved script whose approval hash still matches — the only
    scripts that count as 'the user's voice'. Uses script_approval's own
    read/hash so 'approved' here can never drift from what approve wrote.
    (Function-level import: script_approval imports this module at propose,
    so a top-level import would be circular.)"""
    import json as _json
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import script_approval as _sa
    out: dict[str, dict] = {}
    for appr in sorted((_sa.ROOT / "jobs").glob("*/approval.json")):
        slug = appr.parent.name
        try:
            spoken = _sa.read_script(slug)
        except SystemExit:
            continue
        h = _sa.sha(spoken)
        if h == _json.loads(appr.read_text()).get("sha256"):
            out[slug] = {"sha": h, "text": spoken}
    return out


def tell_collisions(corp: dict[str, dict]) -> list[tuple[str, str]]:
    """(slug, phrase) for every AI tell that fires on an APPROVED script —
    by definition not a tell but the user's voice, unless knowingly kept."""
    hits = []
    for slug, d in corp.items():
        low = d["text"].lower()
        for t in AI_TELLS:
            if re.search(rf"\b{re.escape(t)}", low):
                hits.append((slug, t))
    return hits


def recalibrate() -> int:
    import json as _json
    corp = corpus()
    cols = tell_collisions(corp)
    print(f"\n  corpus: {len(corp)} approved script(s) — "
          + ", ".join(sorted(corp)))
    if cols:
        print("\n  TELL COLLISIONS — an approved script uses a phrase the "
              "tell list calls AI:")
        for slug, t in cols:
            print(f"    {t!r} fires on {slug} — REMOVE it from AI_TELLS "
                  "(their voice, not a tell),\n      with a dated comment, "
                  "or leave it and this record accepts it knowingly.")
    print("\n  structural findings across the corpus (thresholds are advice; "
          "an approved\n  script MAY trip one deliberately — this is drift "
          "evidence, not a verdict):")
    any_notes = False
    import contextlib as _ctx, io as _io
    for slug, d in sorted(corp.items()):
        with _ctx.redirect_stdout(_io.StringIO()):   # check() prints its
            notes = check(d["text"])                 # own header line

        for n in notes:
            any_notes = True
            print(f"    {slug}: {n.split(chr(10))[0][:76]}")
    if not any_notes:
        print("    (none — every approved script measures clean)")
    _cal_path().write_text(_json.dumps({
        "calibratedAt": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).isoformat(timespec="seconds"),
        "corpus": {s: d["sha"] for s, d in corp.items()},
        "tells": len(AI_TELLS),
        "collisionsAccepted": [[s, t] for s, t in cols],
    }, indent=2))
    print(f"\n  wrote {_cal_path().name} — doctor is quiet until the corpus "
          "moves again.")
    return 0


def calibration_status() -> int:
    """0 = record matches reality. 2 = stale (doctor warns, never fails):
    the corpus changed since calibration, or a NEW tell collision exists
    that no recalibration has knowingly accepted."""
    import json as _json
    p = _cal_path()
    corp = corpus()
    if not p.exists():
        print(f"  no calibration record — {len(corp)} approved script(s), "
              "never snapshotted. Run: check_script.py --recalibrate")
        return 2
    rec = _json.loads(p.read_text())
    now = {s: d["sha"] for s, d in corp.items()}
    if now != rec.get("corpus", {}):
        gained = sorted(set(now) - set(rec.get("corpus", {})))
        print(f"  corpus moved since {rec.get('calibratedAt', '?')[:10]} "
              f"({len(rec.get('corpus', {}))} -> {len(now)} scripts"
              + (f"; new: {', '.join(gained)}" if gained else "")
              + "). Run: check_script.py --recalibrate")
        return 2
    accepted = {tuple(x) for x in rec.get("collisionsAccepted", [])}
    fresh = [c for c in tell_collisions(corp) if c not in accepted]
    if fresh:
        for slug, t in fresh:
            print(f"  AI tell {t!r} fires on APPROVED {slug} — the checker "
                  "is flagging the user's own voice. Recalibrate.")
        return 2
    print(f"  calibration current — {len(corp)} approved script(s), "
          f"{rec.get('tells')} tells, snapshotted "
          f"{rec.get('calibratedAt', '?')[:10]}")
    return 0


def main() -> None:
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--recalibrate" in sys.argv:
        sys.exit(recalibrate())
    if "--calibration" in sys.argv:
        sys.exit(calibration_status())
    if "--critic" in sys.argv:
        a = [x for x in sys.argv[1:] if not x.startswith("--")]
        src = (Path(a[0]).read_text() if a and Path(a[0]).exists()
               else (ROOT / f"jobs/{a[0]}/script.md").read_text() if a
               else sys.stdin.read())
        print("\n" + "\n".join(critic(src)) + "\n")
        return
    if "--checklist" in sys.argv:
        a = [x for x in sys.argv[1:] if not x.startswith("--")]
        src = (Path(a[0]).read_text() if a and Path(a[0]).exists()
               else (ROOT / f"jobs/{a[0]}/script.md").read_text() if a
               else sys.stdin.read())
        print("\n" + "\n".join(checklist(src)) + "\n")
        return
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fmt = "news"
    shape = None
    if "--text" in sys.argv:
        i = sys.argv.index("--text")
        text = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
    elif args:
        p = ROOT / f"jobs/{args[0]}/script.md"
        if not p.exists():
            sys.exit(f"no script at {p}")
        text = p.read_text()
        fmt = format_of(args[0])
        shape = structure_of(args[0])
    else:
        sys.exit(__doc__.split("    python3")[0].strip())

    print()
    notes = check(text, shape)
    print()
    if not notes:
        print("  nothing to flag. Read it aloud anyway — this measures shape, "
              "not whether it is any good.")
    for n in notes:
        print(f"  - {n}")
    # The thresholds were calibrated on one matched pair of NEWS scripts written
    # to one narrative shape. A Tutorial enumerates steps; a Myth-busting
    # alternates belief and evidence. Saying which shape the numbers have
    # actually seen is the difference between a measurement and a claim.
    if shape and shape.lower() not in ("news", "explainer"):
        print(f"\n  NOTE: declared structure is {shape!r}. These thresholds have only "
              f"been\n  validated against News and Explainer scripts — a {shape} "
              f"legitimately\n  has a different rhythm. Orientation, not a verdict.")
    elif not shape:
        print("\n  NOTE: no jobs/<slug>/structure.md — the narrative shape was never "
              "declared,\n  so nothing here can know what rhythm to expect. See "
              "formats/README-structure.md.")
    for _t in house_tics(text, exclude_slug=(args[0] if args else None)):
        print(f"  - {_t}")
    if fmt and fmt != "news":
        print(f"\n  NOTE: this reel's format is {fmt!r}. The structural thresholds above\n"
              "  were calibrated on a matched pair of NEWS scripts and no reel in this\n"
              "  repo has used another format, so treat them as orientation, not a\n"
              "  verdict — an enumerated list legitimately enumerates. THRESHOLDS ARE\n"
              "  NEWS-CALIBRATED.")
    print("\n  ADVICE, not rules. A script that breaks all of this and reads "
          "brilliantly\n  is a good script; the numbers are here so the choice is "
          "deliberate.")


if __name__ == "__main__":
    main()
