#!/usr/bin/env python3
"""Normalise spoken text into standard visual notation for on-screen display.

USER RULE 2026-08-11: every number, model name, money figure, date,
percentage, unit, version and technical term appears on screen in standard
notation — "ninety eight point seven percent" reads as `98.7%`, not as words,
and not as whisper's `98 .7 %`.

    "iPhone seventeen"          -> iPhone 17
    "GPT five point four"       -> GPT-5.4        (canonical map only)
    "fifty million lines"       -> 50M lines
    "ninety eight point seven percent" -> 98.7%
    "three point five times"    -> 3.5x
    "June twenty second twenty twenty six" -> June 22, 2026

DESIGN — two layers, because one of them is allowed to invent and the other
is not:

  LAYER 1 (mechanical, ALWAYS SAFE). Re-renders what was already spoken:
  joins whisper's split decimals, attaches %, moves currency to its symbol,
  turns number ranges into en dashes. It cannot introduce a fact — every
  digit it writes was already in the transcript.

  LAYER 2 (canonical, PER-REEL, VERIFIED). Product names, model versions and
  official capitalisation come from a `notation` map in that reel's
  manifest.json — spellings the scout actually saw in the source. There is
  deliberately NO global product dictionary: the user's rule is "use official
  capitalisation exactly as verified in the source material; do not invent
  punctuation, model versions, prices, or abbreviations". A global guess table
  would invent `GPT-5.4` for a source that wrote `GPT 5.4`.

Spoken cardinals become digits ONLY next to a unit or scale word, so ordinary
prose survives: "One honest caveat" stays, "fifteen to twenty basis points"
becomes "15-20 basis points".
"""
from __future__ import annotations

import re

UNITS = (r"percent|per ?cent|%|billion|million|trillion|thousand|lakh|crore|"
         r"basis points?|bps|seconds?|minutes?|hours?|days?|weeks?|months?|"
         r"years?|times|x|rupees?|dollars?|cents?|gigabytes?|megabytes?|"
         r"terabytes?|gb|mb|tb|kb|watts?|hertz|hz|pixels?|px|tokens?|lines?|"
         r"parameters?|frames?|fps|inches|inch|mm|cm|km|kg|degrees?")

ONES = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
        "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
        "seventy": 70, "eighty": 80, "ninety": 90}

CURRENCY = {"rupees": "₹", "rupee": "₹", "dollars": "$", "dollar": "$",
            "euros": "€", "euro": "€", "pounds": "£", "pound": "£"}


def _words_to_int(text: str):
    """'twenty three' -> 23. Returns None if the phrase is not a plain number."""
    toks = re.split(r"[\s-]+", text.strip().lower())
    if not toks:
        return None
    total = 0
    for t in toks:
        if t in ONES:
            total += ONES[t]
        elif t in TENS:
            total += TENS[t]
        elif t == "hundred":
            total = (total or 1) * 100
        else:
            return None
    return total


def _spelled_to_digits(s: str) -> str:
    """Spelled cardinals -> digits, ONLY when the numeric phrase ends in a unit.

    The phrase may span "point" and "to" connectors, so
    "ninety eight point seven percent" and "fifteen to twenty basis points"
    both convert; bare prose ("One honest caveat") never does because no unit
    follows it.
    """
    word = r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|" \
           r"twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|" \
           r"nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|" \
           r"hundred)"
    part = rf"(?:\d+(?:\.\d+)?|(?:{word}[\s-]*)+)"
    phrase = rf"\b({part}(?:\s*(?:point|to)\s*{part})*)(?=\s*({UNITS})\b)"
    SCALE = ("billion", "million", "trillion", "thousand", "lakh", "crore")

    def to_num(chunk: str):
        chunk = chunk.strip()
        if re.fullmatch(r"\d+(?:\.\d+)?", chunk):
            return chunk
        n = _words_to_int(chunk)
        return None if n is None else str(n)

    def sub(m):
        full = m.group(1)
        raw = full.rstrip()
        tail = full[len(raw):]          # keep the original spacing EXACTLY,
        # otherwise "3.5x" normalises to "3.5 x" and the function stops being
        # idempotent (the gate compares normalise(x) == x).
        if re.search(r"\bto\b", raw, re.I):
            parts = re.split(r"\s*\bto\b\s*", raw, maxsplit=1, flags=re.I)
            a, b = to_num(parts[0]), to_num(parts[1])
            return f"{a}-{b}{tail}" if a and b else m.group(0)
        if re.search(r"\bpoint\b", raw, re.I):
            nums = [to_num(x) for x in re.split(r"\s*\bpoint\b\s*", raw, flags=re.I)]
            return ".".join(nums) + tail if all(nums) else m.group(0)
        v = to_num(raw)
        # A bare "one" is an article, not a datum: "In one month" must not
        # become "In 1 month", and "one-time code" must stay. But "one
        # billion" IS data, so keep the conversion when a SCALE word follows.
        if v == "1" and (m.group(2) or "").lower() not in SCALE:
            return m.group(0)
        return f"{v}{tail}" if v else m.group(0)

    return re.sub(phrase, sub, s, flags=re.I)


def normalise(text: str, canonical: dict[str, str] | None = None) -> str:
    """Return `text` in standard visual notation. Idempotent."""
    s = text

    # ── layer 1: mechanical repairs ─────────────────────────────────────────
    s = re.sub(r"(\d)\s+\.\s*(\d)", r"\1.\2", s)          # 23 .2   -> 23.2
    s = re.sub(r"(\d)\s+,\s*(\d{3})\b", r"\1,\2", s)      # 1 ,000  -> 1,000
    s = re.sub(r"(\d)\s+%", r"\1%", s)                     # 85 %    -> 85%
    s = re.sub(r"([$₹€£])\s+(\d)", r"\1\2", s)   # $ 5 -> $5

    # spoken "X point Y" between digits -> decimal
    s = re.sub(r"\b(\d+)\s+point\s+(\d+)\b", r"\1.\2", s, flags=re.I)

    s = _spelled_to_digits(s)

    # "N percent" -> "N%"
    s = re.sub(r"\b(\d+(?:\.\d+)?)\s*per ?cent\b", r"\1%", s, flags=re.I)

    # "N rupees/dollars" -> symbol prefix, keeping any scale word: 30 trillion
    # rupees -> Rs30 trillion is wrong, so the scale word stays attached.
    def money(m):
        n, scale, unit = m.group(1), (m.group(2) or "").strip(), m.group(3).lower()
        sym = CURRENCY[unit]
        return f"{sym}{n}{(' ' + scale) if scale else ''}"
    s = re.sub(rf"\b(\d+(?:[\d,.]*\d)?)\s*(billion|million|trillion|thousand|lakh|crore)?\s*"
               rf"({'|'.join(CURRENCY)})\b", money, s, flags=re.I)

    # "N times" as a multiplier -> Nx
    s = re.sub(r"\b(\d+(?:\.\d+)?)\s*times\b", r"\1x", s, flags=re.I)

    # numeric range -> en dash (only digit-to-digit)
    s = re.sub(r"\b(\d+(?:\.\d+)?)\s+to\s+(\d+(?:\.\d+)?)\b", r"\1-\2", s)

    # tidy spacing artefacts whisper leaves behind
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    s = re.sub(r"[ \t]{2,}", " ", s)

    # ── layer 2: canonical, verified spellings only ─────────────────────────
    for spoken, official in (canonical or {}).items():
        s = re.sub(rf"(?<![\w-])({re.escape(spoken)})(?![\w-])", official, s,
                   flags=re.I)
    return s


def normalise_words(words, canonical=None):
    """Normalise a whisper word list BEFORE it is chunked into captions.

    Notation spans word boundaries — "30 trillion rupees" and "15 to 20" — and
    a caption chunker will happily cut straight through them. Normalising each
    chunk afterwards then cannot see the other half, so `nearly 30 trillion` /
    `rupees.` shipped with no currency symbol. Merging here, while the tokens
    are still adjacent, keeps the first token's start time and the last
    token's end time.

    Input/return: [(start, end, text), ...]
    """
    scale = ("billion", "million", "trillion", "thousand", "lakh", "crore")
    out = list(words)
    i = 0
    merged = []
    while i < len(out):
        s0, e0, t0 = out[i]
        nxt = lambda k: out[i + k][2].strip() if i + k < len(out) else ""
        low = lambda k: nxt(k).lower().strip(".,;:!?")
        num = re.fullmatch(r"\d+(?:[.,]\d+)?", t0.strip())

        # N [scale] <currency>  ->  ₹N [scale]
        if num:
            for span, sc_word in ((2, low(1)), (1, None)):
                unit = low(span)
                if unit in CURRENCY and (sc_word in scale or span == 1):
                    sym = CURRENCY[unit]
                    tail = out[i + span][2]
                    punct = "".join(ch for ch in tail if ch in ".,;:!?")
                    body = f"{sym}{t0.strip()}" + (f" {sc_word}" if span == 2 else "")
                    merged.append((s0, out[i + span][1], body + punct))
                    i += span + 1
                    break
            else:
                pass
            if merged and merged[-1][0] == s0:
                continue

        # N to M (followed by a unit) -> N-M
        if num and low(1) == "to" and re.fullmatch(r"\d+(?:\.\d+)?", low(2) or "x"):
            merged.append((s0, out[i + 2][1], f"{t0.strip()}-{nxt(2)}"))
            i += 3
            continue

        # N + % / percent -> N%
        if num and low(1) in ("%", "percent", "per cent"):
            punct = "".join(ch for ch in nxt(1) if ch in ".,;:!?")
            merged.append((s0, out[i + 1][1], f"{t0.strip()}%{punct}"))
            i += 2
            continue

        merged.append((s0, e0, t0))
        i += 1
    return [(a, b, normalise(c, canonical)) for a, b, c in merged]


def violations(text: str, canonical: dict[str, str] | None = None) -> list[str]:
    """Human-readable reasons `text` is not in standard notation."""
    out = []
    if re.search(r"\d\s+\.\d", text):
        out.append("split decimal")
    if re.search(r"\d\s+%", text):
        out.append("detached %")
    if re.search(r"[$₹€£]\s+\d", text):
        out.append("detached currency symbol")
    if re.search(rf"\b\d+(?:\.\d+)?\s*({'|'.join(CURRENCY)})\b", text, re.I):
        out.append("currency as a word")
    if re.search(r"\b\d+(?:\.\d+)?\s*per ?cent\b", text, re.I):
        out.append("percent as a word")
    if re.search(r"\b\d+\s+point\s+\d+\b", text, re.I):
        out.append("decimal as 'point'")
    if normalise(text, canonical) != text:
        out.append("not in normal form")
    return out


if __name__ == "__main__":
    CASES = [
        ("alone, 23 .2", "alone, 23.2"),
        ("about 85 %", "about 85%"),
        ("nearly 30 trillion rupees.", "nearly ₹30 trillion."),
        ("ninety eight point seven percent", "98.7%"),
        ("three point five times", "3.5x"),
        ("fifteen to twenty basis points", "15-20 basis points"),
        ("fifty million lines", "50 million lines"),
        ("One honest caveat.", "One honest caveat."),      # prose survives
        ("one-time code.", "one-time code."),              # compound survives
        ("It wants 15 to 20 basis points", "It wants 15-20 basis points"),
        ("In one month", "In one month"),           # article, not a datum
        ("one billion tokens", "1 billion tokens"),  # scale word -> data
        ("two million lines", "2 million lines"),
    ]
    ok = True
    for src, want in CASES:
        got = normalise(src)
        flag = "ok  " if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"  {flag} {src!r} -> {got!r}" + ("" if got == want else f"  (want {want!r})"))
    # idempotence: normalising twice must equal normalising once
    for src, _ in CASES:
        once = normalise(src)
        if normalise(once) != once:
            print(f"  FAIL not idempotent: {src!r}")
            ok = False
    print("\nnotation self-test:", "passed" if ok else "FAILED")
    raise SystemExit(0 if ok else 1)
