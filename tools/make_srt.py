#!/usr/bin/env python3
"""Write a YouTube caption file (SRT) for a long-form video.

The WORDS come from the approved script and the TIMES from whisper. Whisper's own
text is not caption-grade: on ios27-settings-longform it heard "worth" as "word",
"sitting" as "setting" and wrote "eleven" as "11". So the script's words are
aligned to whisper's timings (difflib on normalised tokens); a script word with no
matched whisper word takes its time from its neighbours.

    python3 tools/make_srt.py <slug>          # -> out/<slug>.srt
    python3 tools/make_srt.py --demo

A cue is at most 2 lines of 42 characters and 6 seconds, and breaks after a
sentence end.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_CHARS, MAX_SECS = 84, 6.0


def norm(w: str) -> str:
    return re.sub(r"[^\w]", "", w.lower())


def align(script_words: list[str], heard: list[dict]) -> list[tuple[str, float, float]]:
    """(script word, start, end) for every script word."""
    a = [norm(w) for w in script_words]
    b = [norm(h["word"]) for h in heard]
    times: list[tuple[float, float] | None] = [None] * len(a)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            h = heard[blk.b + k]
            times[blk.a + k] = (h["start"], h["end"])
    # fill gaps by spreading them between the known neighbours
    i = 0
    while i < len(times):
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(times) and times[j] is None:
            j += 1
        t0 = times[i - 1][1] if i > 0 else 0.0
        t1 = times[j][0] if j < len(times) else (heard[-1]["end"] if heard else t0)
        step = (t1 - t0) / (j - i + 1)
        for k in range(i, j):
            times[k] = (t0 + step * (k - i), t0 + step * (k - i + 1))
        i = j
    return [(w, t[0], t[1]) for w, t in zip(script_words, times)]


def cues(words: list[tuple[str, float, float]]) -> list[tuple[float, float, str]]:
    out, cur = [], []
    for w in words:
        cur.append(w)
        text = " ".join(x[0] for x in cur)
        if (w[0].endswith((".", "?", "!")) or len(text) > MAX_CHARS - 10
                or cur[-1][2] - cur[0][1] > MAX_SECS):
            out.append((cur[0][1], cur[-1][2], text))
            cur = []
    if cur:
        out.append((cur[0][1], cur[-1][2], " ".join(x[0] for x in cur)))
    return out


def wrap(text: str) -> str:
    if len(text) <= 42:
        return text
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best[0]:
            best = (score, a + "\n" + b)
    return best[1]


def ts(s: float) -> str:
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def srt(cs: list[tuple[float, float, str]]) -> str:
    return "\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{wrap(t)}\n" for i, (a, b, t) in enumerate(cs, 1))


def demo() -> int:
    heard = [{"word": w, "start": i * 0.5, "end": i * 0.5 + 0.4}
             for i, w in enumerate("It is word changing 11 back.".split())]
    got = align("It is worth changing eleven back.".split(), heard)
    assert [w for w, *_ in got] == "It is worth changing eleven back.".split(), got
    assert all(b >= a for _, a, b in got), "times must not run backwards"
    assert got[2][1] > got[1][1] and got[4][1] > got[3][1], "unmatched words keep their order in time"
    assert ts(3661.5) == "01:01:01,500"
    assert "\n" in wrap("x" * 30 + " " + "y" * 30), "long lines wrap"
    print("make_srt self-check passed — script words kept, whisper times used, gaps filled in order")
    return 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        raise SystemExit(demo())
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    slug = sys.argv[1]
    script = (ROOT / "jobs" / slug / "script.md").read_text().split()
    heard = json.loads((ROOT / "public/assets" / slug / "vo.json").read_text())
    heard = heard["words"] if isinstance(heard, dict) else heard
    out = ROOT / "out" / f"{slug}.srt"
    out.parent.mkdir(exist_ok=True)
    cs = cues(align(script, heard))
    out.write_text(srt(cs))
    print(f"  {len(cs)} cues -> {out.relative_to(ROOT)}")
