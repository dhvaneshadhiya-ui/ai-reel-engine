#!/usr/bin/env python3
"""Derive the music volume curve from where the voice ACTUALLY is.

WHY THIS EXISTS
---------------
Music level was five hardcoded clock times:

    {"t": 0.0, "vol": 0.15}      # full at the hook
    {"t": 8.0, "vol": 0.08}      # duck through explanation
    {"t": TOTAL*0.7, "vol": 0.14}
    ...

Those numbers cannot see the voice. If the VO happens to pause at 8s the bed
ducks under silence; if it is mid-sentence at 0.7*TOTAL the bed swells over the
line. It was a guess dressed as an edit.

CLAUDE.md has said since 2026-08-16 that `hyperframes-audio` does this properly
("voiceover carve") and is worth borrowing. It was never wired in — zero lines of
this repo reference it — and it could not be dropped in anyway: the carve is
data attributes read by HyperFrames' own player at playback, not a Remotion
volume callback. The technique transfers, the code does not.

We can do better than a generic carve regardless. A carve has to INFER speech
from a waveform; we already hold whisper word timings for every reel, so the
speech intervals are known exactly.

    python3 tools/duck_music.py <slug>            # print the curve
    python3 tools/duck_music.py <slug> --write     # patch it into the beat sheet
    python3 tools/duck_music.py <slug> --compare   # against the current curve

THE ONE MUSICAL JUDGEMENT: do not lift the bed in every gap between words, or it
pumps on every breath and sounds broken. Only real pauses (>= MIN_GAP) open up.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OPEN_VOL = 0.150   # bed alone — hook, pauses, tail
DUCK_VOL = 0.055   # bed under speech; low enough that consonants stay crisp
ATTACK = 0.18      # duck DOWN fast: late attack lets a word start on loud music
RELEASE = 0.34     # come UP slow: fast release pumps audibly between phrases
MIN_GAP = 0.45     # a gap shorter than this stays ducked
TAIL_FADE = 0.9    # fade to near-silence over the last of the reel


def words_of(slug: str) -> list[tuple[float, float]]:
    p = ROOT / f"public/assets/{slug}/vo.json"
    if not p.exists():
        sys.exit(f"no word timings at {p} — the voice stage has not run")
    d = json.loads(p.read_text())
    ws = [(float(w["start"]), float(w["end"]))
          for s in d.get("segments", []) for w in s.get("words", [])]
    if not ws:
        sys.exit(f"{p} has no word-level timings")
    return sorted(ws)


def speech_spans(words: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Merge words into speech runs, splitting only on a real pause."""
    spans: list[list[float]] = []
    for st, en in words:
        if spans and st - spans[-1][1] < MIN_GAP:
            spans[-1][1] = max(spans[-1][1], en)
        else:
            spans.append([st, en])
    return [(a, b) for a, b in spans]


def curve(slug: str, total: float) -> list[dict]:
    spans = speech_spans(words_of(slug))
    pts: list[tuple[float, float]] = [(0.0, OPEN_VOL)]

    for st, en in spans:
        # ramp down into the phrase, ramp up after it
        pts.append((max(0.0, st - ATTACK), OPEN_VOL))
        pts.append((st, DUCK_VOL))
        pts.append((en, DUCK_VOL))
        pts.append((min(total, en + RELEASE), OPEN_VOL))

    pts.append((max(0.0, total - TAIL_FADE), OPEN_VOL))
    pts.append((total, 0.02))

    # keep it monotonic in t and drop points that collide after clamping
    pts.sort(key=lambda p: p[0])
    out: list[dict] = []
    for t, v in pts:
        if out and abs(t - out[-1]["t"]) < 0.02:
            # same instant: the later value wins, so a duck is never skipped
            out[-1]["vol"] = min(out[-1]["vol"], v)
            continue
        out.append({"t": round(t, 3), "vol": round(v, 4)})
    return out


def vol_at(pts: list[dict], t: float) -> float:
    """Same interpolation Reel.tsx does, so a check measures what renders."""
    if t <= pts[0]["t"]:
        return pts[0]["vol"]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if a["t"] <= t < b["t"]:
            k = (t - a["t"]) / (b["t"] - a["t"])
            return a["vol"] + k * (b["vol"] - a["vol"])
    return pts[-1]["vol"]


def score(slug: str, pts: list[dict], total: float) -> tuple[float, float]:
    """(mean level under speech, mean level in real pauses). Lower/higher = better."""
    spans = speech_spans(words_of(slug))
    step = 0.05
    sp, ga = [], []
    t = 0.0
    while t < total:
        inside = any(a <= t <= b for a, b in spans)
        (sp if inside else ga).append(vol_at(pts, t))
        t += step
    mean = lambda xs: sum(xs) / len(xs) if xs else 0.0
    return mean(sp), mean(ga)


def beats_path(slug: str) -> Path:
    p = ROOT / f"src/beats/{slug}.json"
    if not p.exists():
        sys.exit(f"no beat sheet at {p}")
    return p


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("THE ONE MUSICAL")[0].strip())
    slug = args[0]
    bp = beats_path(slug)
    doc = json.loads(bp.read_text())
    total = sum(s["durationSec"] for s in doc["scenes"])
    new = curve(slug, total)

    print(f"\n  {slug}: {total:.1f}s, {len(speech_spans(words_of(slug)))} speech "
          f"runs -> {len(new)} volume points")
    ns, ng = score(slug, new, total)
    print(f"  derived   under speech {ns:.3f}   in pauses {ng:.3f}")

    if "--compare" in sys.argv:
        cur = (doc.get("music") or {}).get("points")
        if cur:
            os_, og = score(slug, cur, total)
            print(f"  current   under speech {os_:.3f}   in pauses {og:.3f}"
                  f"   ({len(cur)} points)")
            print(f"\n  separation: derived {og - ns:+.3f}, "
                  f"current {og - os_:+.3f}"
                  "  (bigger = the bed actually gets out of the way)")
        else:
            print("  current   no music block to compare")

    if "--write" in sys.argv:
        if "music" not in doc:
            sys.exit("no music block in the beat sheet — nothing to patch")
        doc["music"]["points"] = new
        doc["music"]["derivedFrom"] = "vo.json word timings (tools/duck_music.py)"
        bp.write_text(json.dumps(doc, indent=2) + "\n")
        print(f"\n  written to {bp.relative_to(ROOT)}")
    else:
        print("\n  (--write to patch the beat sheet)")


if __name__ == "__main__":
    main()
