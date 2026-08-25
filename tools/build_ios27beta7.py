#!/usr/bin/env python3
"""Build the beat sheet for ios27-beta7.

Anchors bind every cut to SPOKEN WORDS (from whisper's actual transcript,
which is not always the written script verbatim — e.g. "Beta 7" not "Beta
seven"). Every region is divided among its visuals; check_beats() raises
before anything is written.

Story: beta 7 is a stability/bug-fix pass, not a feature drop. Visual spine:
the hook is Apple's own release-notes page (split with the presenter), then
each of the three consumer-relevant fixes gets its own official-text receipt
(converted from PNG to a silent MP4 loop — FloatingCard renders OffthreadVideo
only, so a PNG handed to it renders black), then a 3-outlet corroboration
composite for "every outlet says the same thing", closing on a typecard that
counts down to release.

noMusic is the default now (2026-08-24 standing rule) — SFX carries the sound,
run at the top of the range (9 cues).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402

SLUG = "ios27-beta7"

ROOT = Path(__file__).resolve().parent.parent
A = f"assets/{SLUG}"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())

# The approved narration, read straight from the approved file — never
# retyped — so G27 checks the sheet against what the user actually said yes
# to, not a hand-copied paraphrase of it.
SCRIPT = " ".join(
    line.strip()
    for line in (ROOT / f"jobs/{SLUG}/script.md").read_text().splitlines()
    if line.strip()
)

APPLE_CREDIT = "Source: Apple Developer"
PRESS_CREDIT = "Sources: 9to5Mac, MacRumors, Macworld"

# ── voiceover is the master clock ───────────────────────────────────────────
raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())
words = [(w["start"], w["end"], w["word"].strip())
         for s in raw["segments"] for w in s["words"]]

merged = []
for st, en, tx in words:
    if (tx.startswith("-") or re.match(r"^[.,]\d", tx)) and merged:
        p = merged[-1]
        merged[-1] = (p[0], en, p[2] + tx)
    else:
        merged.append((st, en, tx))
words = merged

TOTAL = round(words[-1][1] + 0.35, 2)
print(f"{len(words)} words, VO ends {words[-1][1]:.2f}s, reel {TOTAL:.2f}s")


def css_pos(fx, iw, ih, cw, ch):
    s = max(cw / iw, ch / ih)
    w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


# native 9:16 master (1080x1920): no horizontal crop happens either way, so
# both resolve to 0.5 — kept as a measurement, not a hardcoded constant.
FOCUS_FULL = css_pos(FACE_X, 1080, 1920, 1080, 1920)
FOCUS_SPLIT = css_pos(FACE_X, 1080, 1920, 1080, 960)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


stream = [norm(w[2]) for w in words]


def find(phrase):
    t = norm(phrase).split()
    for i in range(len(stream) - len(t) + 1):
        if stream[i:i + len(t)] == t:
            return words[i + len(t) - 1][1]
    raise SystemExit(f"ANCHOR NOT FOUND: {phrase!r}")


anchors = [
    ("hook",        "beta 7 just landed"),
    ("stakes",      "ships to your phone next month"),
    ("cadence",     "one week after beta 6"),
    ("pattern",     "actually inside"),
    ("nofeat",      "already announced"),
    ("fixlist",     "not a feature list"),
    ("alarm-lead",  "take the alarm bug"),
    ("alarm-fix",   "unlocking your phone fixed"),
    ("camera-lead", "or portrait mode"),
    ("camera-fix",  "also fixed"),
    ("siri-lead",   "even the new siri voice"),
    ("siri-fix",    "overheated patched"),
    ("dict-lead",   "and dictations"),
    ("dict-fix",    "keyboard settings"),
    ("thepoint",    "exactly the point"),
    ("sevenbetas",  "adding features anymore"),
    ("shippedbroken", "shipped broken in september"),
    ("corroborate", "weeks from release"),
    ("itstheseven", "it's the 7"),
    ("closer",      "27"),
]

bounds, prev = [], 0.0
for name, ph in anchors:
    e = round(find(ph) + 0.12, 2)
    bounds.append((name, prev, e))
    prev = e
bounds[-1] = (bounds[-1][0], bounds[-1][1], TOTAL)
B = {n: (s, e) for n, s, e in bounds}
for n, s, e in bounds:
    print(f"  {n:14s} {s:6.2f}-{e:6.2f} ({e - s:.2f}s)")


def dur(n):
    return round(B[n][1] - B[n][0], 2)


def start(n):
    return B[n][0]


# ── sound: top of the range (9 cues), no music bed (RULES.md 2026-08-24) ────
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.14}
SHUTTER = {"src": "sfx/Camera Shutter.MP3", "vol": 0.15}
CORE = {"src": "sfx/Core.MP3", "vol": 0.16}
RISER = {"src": "sfx/Riser.MP3", "vol": 0.13}
REVEAL = {"src": "sfx/Magic Reveal.MP3", "vol": 0.15}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.16}

FOOTAGE = lambda name, zoom_dir, credit=None: {
    "type": "footage", "durationSec": dur(name), "src": AVATAR,
    "from": round(start(name), 2), "zoomDir": zoom_dir, "focusX": FOCUS_FULL,
    **({"credit": credit} if credit else {}),
}

scenes: list[dict] = [
    # 1 — HOOK: Apple's own beta-7 page split with the presenter. Mute-test
    # (G38) satisfied by the kinetic "BETA 7" card.
    {
        "type": "split", "durationSec": dur("hook"), "captionBottom": 1000,
        "topSrc": f"{A}/src-hero.png", "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": 0.0, "bottomFocusX": FOCUS_SPLIT,
        # y 0.42 lands in the clear white space below the page's own tagline
        # ("Update your apps...") and above the seam — 0.14 sat directly on
        # top of the "Beta 7 Release Notes" headline it was supposed to
        # echo, an unreadable text-on-text collision.
        "kinetic": {"text": "BETA 7", "style": "caps", "at": 0.05, "y": 0.42},
        "credit": APPLE_CREDIT, "assetId": "src-hero",
        "covers": "beta 7 just landed",
        "sfx": [dict(WHOOSH, at=0.0)],
    },
    # 2 — stakes line, direct address
    FOOTAGE("stakes", "out"),
    # 3 — the official page itself: this is where beta 7 lives
    {
        "type": "sourceread", "durationSec": dur("cadence"),
        "src": f"{A}/src-hero.png", "srcWidth": 1080, "srcHeight": 1750,
        "credit": APPLE_CREDIT, "follow": False, "assetId": "src-hero",
        "covers": "one week after beta 6",
        "lines": [
            {"at": 0.1, "x": 68, "y": 632, "w": 944, "h": 220},
        ],
        "sfx": [dict(SHUTTER, at=0.0)],
    },
    # 4 — bridge
    FOOTAGE("pattern", "in"),
    # 5 — the thesis, stated flat — a card, not facecam (G06 facecam budget)
    {
        "type": "typecard", "durationSec": dur("nofeat"),
        "kinetic": {
            "text": "NO NEW FEATURES.\nJUST FIXES.", "style": "caps",
            "ats": [0.1, round(dur("nofeat") * 0.5, 2)],
        },
        "bg": "#f2ecdf", "fg": "#141414",
        "sfx": [dict(CORE, at=0.0)],
    },
    # 6 — back to the source: "release notes read like a fix list"
    {
        "type": "sourceread", "durationSec": dur("fixlist"),
        "src": f"{A}/src-hero.png", "srcWidth": 1080, "srcHeight": 1750,
        "credit": APPLE_CREDIT, "follow": False, "assetId": "src-hero",
        "covers": "release notes read like a fixed list",
        "lines": [
            {"at": 0.1, "x": 68, "y": 890, "w": 950, "h": 220},
        ],
    },
    # 7 — fix 1: the alarm bug — card spans the lead-in clause too (G18: a
    # card must outlast the sentence it illustrates)
    {
        "type": "floatcard", "durationSec": dur("alarm-lead") + dur("alarm-fix"),
        "src": f"{A}/src-clock-fix.mp4", "aspect": 886 / 304,
        "bg": "cream", "credit": APPLE_CREDIT, "assetId": "src-clock-fix",
        "covers": "couldn't stop a ringing alarm without unlocking your phone",
        "sfx": [dict(SHUTTER, at=0.0)],
    },
    # 8 — fix 2: Portrait mode blur
    {
        "type": "floatcard", "durationSec": dur("camera-lead") + dur("camera-fix"),
        "src": f"{A}/src-camera-fix.mp4", "aspect": 886 / 228,
        "bg": "cream", "credit": APPLE_CREDIT, "assetId": "src-camera-fix",
        "covers": "the blur was rendering wrong on photos",
        "sfx": [dict(SHUTTER, at=0.0)],
    },
    # 9 — fix 3: Siri voice reverting
    {
        "type": "floatcard", "durationSec": dur("siri-lead") + dur("siri-fix"),
        "src": f"{A}/src-siri-voice.mp4", "aspect": 886 / 378,
        "bg": "cream", "credit": APPLE_CREDIT, "assetId": "src-siri-voice",
        "covers": "reverting to the old one whenever your phone overheated",
    },
    # 10 — dictation: the one "new feature" that IS in the notes
    {
        "type": "floatcard", "durationSec": dur("dict-lead") + dur("dict-fix"),
        "src": f"{A}/src-dictation-fix.mp4", "aspect": 886 / 454,
        "bg": "cream", "credit": APPLE_CREDIT, "assetId": "src-dictation-fix",
        "covers": "a toggle waiting in keyboard settings",
    },
    # 11 — the opinion line
    FOOTAGE("thepoint", "in"),
    # 12 — SEVEN BETAS. ZERO NEW FEATURES.
    {
        "type": "typecard", "durationSec": dur("sevenbetas"),
        "kinetic": {
            "text": "SEVEN BETAS.\nZERO NEW FEATURES.", "style": "caps",
            "ats": [0.1, round(dur("sevenbetas") * 0.55, 2)],
        },
        "bg": "#0a0a0a", "fg": "#ffffff",
    },
    # 13 — the consequence — card, not facecam (G06 budget); riser leads into
    # the corroboration payoff next, timed to peak exactly as it lands.
    {
        "type": "typecard", "durationSec": dur("shippedbroken"),
        "kinetic": {
            "text": "WOULD'VE SHIPPED BROKEN.", "style": "caps", "at": 0.15,
        },
        "bg": "#f2ecdf", "fg": "#141414",
        "sfx": [dict(RISER, at=round(max(0.0, dur("shippedbroken") - 1.49), 2))],
    },
    # 14 — the corroboration payoff: 3 outlets, same day, same story
    {
        "type": "floatcard", "durationSec": dur("corroborate"),
        "src": f"{A}/src-corroboration.mp4", "aspect": 1056 / 1936,
        "bg": "cream", "credit": PRESS_CREDIT, "assetId": "src-corroboration",
        "covers": "every outlet watching this cycle says the same thing",
        # this card is tall (72% of frame height) and centred, so the default
        # caption position (y~0.71) lands mid-card, on top of the Macworld
        # headline. Move captions into the clear gap above the card instead —
        # the gap below it is past the platform's own account-row line
        # (y 0.835) and unsafe for captions there (G45).
        "captionBottom": 1750,
        "sfx": [dict(REVEAL, at=0.0)],
    },
    # 15 — the pivot / reveal line, direct address
    FOOTAGE("itstheseven", "in"),
    # 16 — closing countdown, callback to the hook's BETA 7 card
    {
        "type": "typecard", "durationSec": dur("closer"),
        "kinetic": {
            "text": "ONE MORE BETA.\nTHEN THE RC.\nTHEN... iOS 27.",
            "style": "caps",
            "ats": [0.1, 2.7, 4.7],
        },
        "bg": "#0a0a0a", "fg": "#ffffff",
        "sfx": [dict(GROUND, at=2.7)],
    },
]

# ── captions: per-word reveal ────────────────────────────────────────────────
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


# Display-only fixes for whisper mishears/normalisation. Timings untouched.
FIX = {
    "Beta 7": "Beta 7",
    "7's": "7's",
}

captions = []
for grp in chunk(words):
    text = " ".join(w[2] for w in grp)
    per = [{"t": round(w[0], 2), "text": w[2]} for w in grp]
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                     "text": text, "words": [p for p in per if p["text"]]})

beats = {
    "id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "editorial",
    "format": "news",
    "audio": AVATAR,
    "noMusic": True,
    "noMusicReason": ("Standing rule 2026-08-24: no music bed by default. "
                       "SFX (9 cues, top of the news band) carries the sound "
                       "for this reel; nothing about this topic asked for a "
                       "bed back."),
    "captionStyle": "word-reveal",
    "emphasis": ["Beta 7", "fixed", "Siri", "dictation", "seven", "iOS 27"],
    "scenes": scenes, "captions": captions,
    "script": SCRIPT,
    "approval": {
        "sha256": "dd59fef1aace3191e42b7e140a3674beab0398f2ba2030514322324c99c01860",
        "approvedAt": "2026-08-25T04:52:52+00:00",
    },
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
