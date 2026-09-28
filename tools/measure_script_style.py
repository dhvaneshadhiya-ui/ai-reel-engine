#!/usr/bin/env python3
"""Measure how a reference video is WRITTEN, from its caption track.

The longform teardown measured pacing and face share and never looked at the
prose. The first pilot script came back with deck-style chapter labels on screen
and a structure nobody in the references uses, which is what an unmeasured half
of a format produces (user, 2026-09-25).

    python3 tools/measure_script_style.py <file.en.vtt | jobs/<slug>/script.md> [...]

Reports, per reference: words, sentence length, question rate, second-person
density, imperative openings, and the transition words that actually carry the
turns. `--open` prints the first 40 seconds verbatim, which is where a long-form
video wins or loses the viewer.

Self-check: python3 tools/measure_script_style.py --demo
"""
from __future__ import annotations

import re
import statistics as st
import sys
from pathlib import Path

TURNS = ("so", "now", "but", "and", "then", "which", "because", "here's", "that's",
         "if", "when", "once", "next", "first", "second", "finally", "also", "plus")


def vtt_text(path: Path) -> tuple[str, list[tuple[float, str]]]:
    rows, seen, t = [], set(), None
    for line in path.read_text(errors="ignore").splitlines():
        m = re.match(r"(\d\d):(\d\d):(\d\d)\.(\d+)\s+-->", line)
        if m:
            h, mnt, s, ms = (int(x) for x in m.groups())
            t = h * 3600 + mnt * 60 + s + ms / 1000
            continue
        s = re.sub(r"<[^>]+>", "", line).strip()
        if t is not None and s and not s.startswith(("WEBVTT", "Kind:", "Language:")):
            if s not in seen:
                seen.add(s)
                rows.append((t, s))
    return " ".join(s for _, s in rows), rows


def sentences(text: str) -> list[str]:
    # auto-captions carry no punctuation, so split on the turn words that start
    # a new clause as well as on any punctuation that did survive
    parts = re.split(r"(?<=[.!?])\s+", text)
    out: list[str] = []
    for p in parts:
        if len(p.split()) <= 45:
            out.append(p)
            continue
        words, cur = p.split(), []
        for w in words:
            if cur and w.lower().strip(",") in ("so", "but", "and then", "now") and len(cur) > 6:
                out.append(" ".join(cur)); cur = []
            cur.append(w)
        if cur:
            out.append(" ".join(cur))
    return [s for s in out if s.strip()]


def measure(path: Path) -> dict:
    # a .md is one of OUR scripts: same measurements, so the draft can be held
    # against the references instead of against taste
    if path.suffix == ".md":
        text = re.sub(r"\s+", " ", path.read_text()).strip()
        rows = [(0.0, text)]
    else:
        text, rows = vtt_text(path)
    words = text.split()
    sents = sentences(text)
    lens = [len(s.split()) for s in sents]
    low = text.lower()
    you = len(re.findall(r"\b(you|your|you're|you'll|yourself)\b", low))
    i_me = len(re.findall(r"\b(i|i'm|i've|my|me)\b", low))
    qs = len(re.findall(r"\?", text)) or sum(
        1 for s in sents if re.match(r"^(what|why|how|when|where|which|who|is|are|do|does|did|can|should|would)\b", s.lower()))
    turns = {w: len(re.findall(rf"\b{re.escape(w)}\b", low)) for w in TURNS}
    top = sorted(turns.items(), key=lambda kv: -kv[1])[:5]
    return {
        "name": path.stem.replace(".en", ""), "words": len(words),
        "sent": len(sents), "mean": st.mean(lens) if lens else 0,
        "median": st.median(lens) if lens else 0,
        "long_share": sum(1 for L in lens if L > 25) / max(1, len(lens)),
        "you_per_100": 100 * you / max(1, len(words)),
        "i_per_100": 100 * i_me / max(1, len(words)),
        "q_per_min": qs, "turns": top, "rows": rows,
    }


def report(rows: list[dict], show_open: bool) -> None:
    print(f"\n{'reference':<18}{'words':>7}{'sent':>6}{'mean':>7}{'med':>6}{'>25w':>7}"
          f"{'you/100':>9}{'I/100':>7}{'Qs':>5}  top turns")
    for r in rows:
        turns = ", ".join(f"{w}x{n}" for w, n in r["turns"] if n)
        print(f"{r['name']:<18}{r['words']:>7}{r['sent']:>6}{r['mean']:>7.1f}{r['median']:>6.0f}"
              f"{r['long_share']*100:>6.0f}%{r['you_per_100']:>9.1f}{r['i_per_100']:>7.1f}"
              f"{r['q_per_min']:>5}  {turns}")
    if len(rows) > 1:
        p = lambda k: st.median([r[k] for r in rows])
        print(f"\n  POOLED MEDIAN  {p('mean'):.1f} words/sentence · {p('long_share')*100:.0f}% over 25 "
              f"· you {p('you_per_100'):.1f}/100 · I {p('i_per_100'):.1f}/100")
    if show_open:
        for r in rows:
            first = " ".join(s for t, s in r["rows"] if t <= 40)
            print(f"\n--- {r['name']}, first 40s ---\n{first[:700]}")


def demo() -> int:
    s = sentences("this is short. " + " ".join(["word"] * 60) + " so here is another clause")
    assert len(s) >= 2, s
    assert all(len(x.split()) <= 62 for x in s)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        v = Path(td) / "x.en.vtt"
        v.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nyou can see this\n\n"
                     "00:00:03.000 --> 00:00:05.000\nyou can see this\n\n"
                     "00:00:05.000 --> 00:00:07.000\nso I changed it\n")
        m = measure(v)
        assert m["words"] == 8, m["words"]
        assert m["you_per_100"] > 10, m
    print("measure_script_style self-check passed — captions de-duplicated, pronouns counted")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--demo" in args:
        raise SystemExit(demo())
    show = "--open" in args
    args = [a for a in args if a != "--open"]
    if not args:
        raise SystemExit(__doc__)
    report([measure(Path(a)) for a in args], show)
