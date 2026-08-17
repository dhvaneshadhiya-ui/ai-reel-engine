#!/usr/bin/env python3
"""TEMPLATE — copy to tools/build_<slug>.py and fill in.

    cp tools/build_template.py tools/build_myreel.py

The structure below is not optional decoration: the anchor lookup, the scene
sum, and the gate call are what keep visuals on the spoken word and stop a
rule-breaking sheet from ever reaching the renderer. `tools/build_seedance25.py`
is a worked example.

Read RULES.md first.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402

SLUG = "CHANGEME"

ROOT = Path(__file__).resolve().parent.parent
A = f"assets/{SLUG}"
C = f"{A}/clips"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master-169.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())

# ── voiceover is the master clock ───────────────────────────────────────────
raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())
words = [(w["start"], w["end"], w["word"].strip())
         for s in raw["segments"] for w in s["words"]]

# whisper splits hyphenated words into a token + a "-suffix" token, AND
# numbers into a token + a "[.,]digit" fragment ("$2"+",000", "7"+".8").
# Merge both or a caption chip reads a bare fragment. UNIVERSAL — keep this
# loop (gate G30 refuses a sheet that missed it).
merged = []
for st, en, tx in words:
    if (tx.startswith("-") or re.match(r"^[.,]\d", tx)) and merged:
        p = merged[-1]
        merged[-1] = (p[0], en, p[2] + tx)
    else:
        merged.append((st, en, tx))
words = merged

TOTAL = round(words[-1][1] + 0.35, 2)   # reel ends <=0.4s after the last word
print(f"{len(words)} words, VO ends {words[-1][1]:.2f}s, reel {TOTAL:.2f}s")


def css_pos(fx, iw, ih, cw, ch):
    """face-x (fraction of source width) → CSS objectPosition for a crop."""
    s = max(cw / iw, ch / ih)
    w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


FOCUS_FULL = css_pos(FACE_X, 1920, 1080, 1080, 1920)
FOCUS_SPLIT = css_pos(FACE_X, 1920, 1080, 1080, 960)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


stream = [norm(w[2]) for w in words]


def find(phrase):
    """End time of a verbatim phrase. Cuts anchor to WORDS, never timestamps."""
    t = norm(phrase).split()
    for i in range(len(stream) - len(t) + 1):
        if stream[i:i + len(t)] == t:
            return words[i + len(t) - 1][1]
    raise SystemExit(f"ANCHOR NOT FOUND: {phrase!r}")


# One anchor per beat, in order. The phrase is the LAST words that beat covers,
# copied verbatim from the whisper transcript (not the written script — they
# differ). ~40-45 beats for a 90s reel; see RULES.md §4 for the ceilings.
anchors = [
    ("hook",  "CHANGEME"),
    # ("beat2", "..."),
]

bounds, prev = [], 0.0
for name, ph in anchors:
    e = round(find(ph) + 0.12, 2)
    bounds.append((name, prev, e))
    prev = e
bounds[-1] = (bounds[-1][0], bounds[-1][1], TOTAL)   # last beat absorbs the tail
B = {n: (s, e) for n, s, e in bounds}
for n, s, e in bounds:
    print(f"  {n:10s} {s:6.2f}-{e:6.2f} ({e - s:.2f}s)")


def dur(n):
    return round(B[n][1] - B[n][0], 2)


# ── sound: 6-9 cues total, ordinary cuts silent (RULES.md §8) ───────────────
RISER = {"src": "sfx2/risers-01.mp3", "vol": 0.15}
IMPACT = {"src": "sfx2/impact-boom.mp3", "vol": 0.16}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.14}
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}


def hl(lines, y=0.12, theme="light", align="center"):
    """Headline spec. Line limits are enforced by G05: label 30, headline 18."""
    return {"lines": lines, "y": y, "theme": theme, "align": align}


CREDIT = "@CHANGEME"

scenes: list[dict] = [
    # Every scene: durationSec=dur("<anchor>"), plus assetId for anything that
    # came from the manifest so provenance is checkable (G11).
]


# ── captions: per-word reveal for word-reveal captions ──────────────────────────────
def chunk(ws, size=3):
    out, buf = [], []
    for (s, e, w) in ws:
        buf.append((s, e, w))
        if len(buf) >= size or (re.search(r"[.,!?—:;]$", w) and len(buf) >= 2):
            out.append(buf)
            buf = []
    if buf:
        out.append(buf)
    return out


# Display-only fixes for whisper mishears. NEVER touch the timings — and
# confirm with whisper `small` on the slice before assuming the TTS was wrong.
FIX = {}

captions = []
for grp in chunk(words):
    text = " ".join(w[2] for w in grp)
    per = [{"t": round(w[0], 2), "text": w[2]} for w in grp]
    for a, b in FIX.items():
        text = text.replace(a, b)
        for p in per:
            p["text"] = p["text"].replace(a, b)
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                     "text": text, "words": [p for p in per if p["text"]]})

# ── music: automated, never flat (G09) ──────────────────────────────────────
music = {
    "src": "music/bed-02.mp3", "from": 8.0,
    "points": [
        # DO NOT SHIP THESE. They are a placeholder so the sheet is valid while
        # you build; G37 blocks a render until the curve is DERIVED from the
        # voice:   python3 tools/duck_music.py <slug> --write
        # Hardcoded clock times cannot hear the VO. Measured on six shipped
        # reels, they ducked by +0.003 and three were inverted (music LOUDER
        # under the voice than in the pauses).
        {"t": 0.0, "vol": 0.15},                 # full at the hook
        {"t": 8.0, "vol": 0.08},                 # duck through explanation
        {"t": TOTAL * 0.7, "vol": 0.14},         # rise at the reveal
        {"t": TOTAL - 0.9, "vol": 0.13},
        {"t": TOTAL, "vol": 0.02},               # fade
    ],
}

beats = {
    "id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "editorial",
    "audio": AVATAR, "music": music,
    "captionStyle": "word-reveal",
    "emphasis": [],          # numbers/brands — drives the accent keyword
    "scenes": scenes, "captions": captions,
}

total = round(sum(s["durationSec"] for s in scenes), 2)
print(f"\nscenes {total:.2f}s vs reel {TOTAL:.2f}s (delta {total - TOTAL:+.2f}s)")

try:
    for w in check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST):
        print(f"  warning: {w}")
    print("GATES: PASSED")
except GateError as e:
    raise SystemExit(f"GATES FAILED — beat sheet NOT written\n{e}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
