#!/usr/bin/env python3
"""Build the beat sheet for ios27-tiers.

Anchors bind every cut to SPOKEN WORDS; each region is divided among its
visuals (most specific LAST); check_beats() raises before anything is written.

Two things learned the hard way while writing this, recorded so the next build
does not repeat them:

1. FootageScene and FloatingCard both render a Remotion <Video>. A PNG handed to
   either renders BLACK. Only `split` (which branches on file extension),
   `receipt` and `annotatezoom` take an <Img>. Every still below goes through
   one of those three.
2. 27 anchors over 104s averages 3.9s a region, and the G04 ceilings are 2.9s
   motion / 3.3s building / 2.6s card. Long regions are split across 2-4
   DISTINCT visuals — mostly by mining one receipt for several annotated
   regions, which is a different shot each time, not a reuse.

allowLong is set with a written reason (G02).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402

SLUG = "ios27-tiers"

ROOT = Path(__file__).resolve().parent.parent
A = f"assets/{SLUG}"
C = f"{A}/clips"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())

# ── voiceover is the master clock ───────────────────────────────────────────
raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())
words = [(w["start"], w["end"], w["word"].strip())
         for s in raw["segments"] for w in s["words"]]

# whisper splits hyphenated words, number fragments AND percent signs into
# separate tokens ("30" + "%"). Merge, or a caption chip reads a bare fragment
# and G16/G30 refuse the sheet.
merged = []
for st, en, tx in words:
    if (tx.startswith("-") or tx.startswith("%")
            or re.match(r"^[.,]\d", tx)) and merged:
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


# native 9:16 master (1080x1920): no horizontal crop happens, so both resolve
# to 0.5 — kept as a measurement rather than a hardcoded constant.
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


# ── sound (G08 6-9 cues, G33 >=4 files & >=2 roles, G28 role fits the beat) ──
# sfx2/risers-01.mp3 is deliberately unused: 6.19s with a 6.19s lead cannot
# peak inside a ~2.3s hook, so it would outrun its beat.
RISER = {"src": "sfx/Riser.MP3", "vol": 0.14}            # suspense, 1.49s lead
IMPACT_B = {"src": "sfx2/impact-boom.mp3", "vol": 0.17}  # the biggest claim
CORE = {"src": "sfx/Core.MP3", "vol": 0.15}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.15}
POP = {"src": "sfx/Pop.MP3", "vol": 0.13}
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}
MAGIC = {"src": "sfx/Magic Reveal.MP3", "vol": 0.15}     # the payoff itself


def hl(lines, y=0.10, theme="light", align="center"):
    """G05 line limits: label 30, headline 18, subtitle 26 — no auto-fit."""
    return {"lines": [{"text": t, "kind": k, "at": a} for t, k, a in lines],
            "y": y, "theme": theme, "align": align}


# ── scene builders ──────────────────────────────────────────────────────────
def face(headline=None, cb=320):
    def b(t0, d):
        s = {"type": "footage", "src": AVATAR, "durationSec": d,
             "from": round(t0, 2), "focusX": FOCUS_FULL, "captionBottom": cb}
        if headline:
            s["headline"] = headline
        return s
    return b


def rec(png, aid, sw, sh, credit, backdrop="cream", sfx=None):
    def b(t0, d):
        s = {"type": "receipt", "durationSec": d, "src": f"{C}/{png}.png",
             "srcWidth": sw, "srcHeight": sh, "backdrop": backdrop,
             "credit": credit, "assetId": aid}
        if sfx:
            s["sfx"] = sfx
        return s
    return b


def az(png, aid, sw, sh, credit, focus, annos, bg="cream", sfx=None, cb=205):
    def b(t0, d):
        s = {"type": "annotatezoom", "durationSec": d, "src": f"{C}/{png}.png",
             "srcWidth": sw, "srcHeight": sh, "credit": credit, "bg": bg,
             "captionBottom": cb,
             "focus": focus, "annotations": annos, "assetId": aid}
        if sfx:
            s["sfx"] = sfx
        return s
    return b


def mg(spec, sfx=None):
    def b(t0, d):
        s = dict(spec, durationSec=d)
        if sfx:
            s["sfx"] = sfx
        return s
    return b


def split_hook(t0, d):
    return {
        "type": "split", "durationSec": d, "captionBottom": 1000,
        "topSrc": f"{C}/hook-ios27.png", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": round(t0, 2),
        "bottomFocusX": FOCUS_SPLIT, "credit": "MacRumors",
        "assetId": "hook-ios27", "sfx": [dict(RISER, at=0.0)],
    }


def ul(at, x, y, w, h):
    return {"kind": "underline", "at": at, "x": x, "y": y, "w": w, "h": h}


def circ(at, x, y, w, h):
    return {"kind": "circle", "at": at, "x": x, "y": y, "w": w, "h": h}


# ── MG specs ────────────────────────────────────────────────────────────────
CASCADE_ALMOST = {
    "type": "wordcascade", "bg": "cream",
    "words": [
        {"text": "SUPPORTED", "style": "caps", "at": 0.15},
        {"text": "ISN'T THE SAME AS", "style": "caps", "at": 0.55},
        {"text": "SUPPORTED", "style": "caps", "at": 0.95, "size": 1.4,
         "accent": True},
    ],
}
CASCADE_ZERO = {
    "type": "wordcascade", "bg": "cream",
    "words": [
        {"text": "DEVICES", "style": "caps", "at": 0.12},
        {"text": "DROPPED:", "style": "caps", "at": 0.5},
        {"text": "ZERO", "style": "caps", "at": 0.9, "size": 1.6,
         "accent": True},
    ],
}
GRID_TIERS = {
    "type": "categorygrid", "bg": "gradient",
    "headline": "ONE UPDATE, THREE PHONES",
    "cards": [
        {"label": "EVERYTHING", "sub": "17 Pro · 17 Pro Max · Air"},
        {"label": "STANDARD", "sub": "16 line · 15 Pro"},
        {"label": "NO AI", "sub": "15 and older · SE"},
    ],
}
SPEC_STANDARD = {
    "type": "specsheet", "kicker": "the middle tier",
    "title": "Standard Apple Intelligence", "columns": ["GETS"],
    "rows": [
        {"label": "iPhone 16 line", "values": ["incl. 16e"]},
        {"label": "iPhone 15 Pro", "values": ["Pro · Pro Max"]},
        {"label": "Siri", "values": ["new look only"], "accent": True},
    ],
    "footnote": "Source: Apple — apple.com/os/ios",
}
CASCADE_NOAI = {
    "type": "wordcascade", "bg": "black",
    "words": [
        {"text": "15 · 14 · 13 · 12 · 11 · SE", "style": "caps", "at": 0.12},
        {"text": "NO Apple Intelligence", "style": "caps", "at": 0.7,
         "size": 1.2, "accent": True},
    ],
}
GRID_INOUT = {
    "type": "categorygrid", "bg": "black",
    "headline": "SAME YEAR, SAME NAME",
    "cards": [
        {"label": "iPhone 15 Pro", "sub": "IN — Apple Intelligence"},
        {"label": "iPhone 15", "sub": "OUT — no AI"},
    ],
    "selectIndex": 1, "selectAt": 0.9,
}
SPEC_PRIVACY = {
    "type": "specsheet", "kicker": "where it actually runs",
    "title": "Apple Foundation Models", "columns": ["iOS 27"],
    "rows": [
        {"label": "Co-developed with", "values": ["Google · Gemini"]},
        {"label": "Runs", "values": ["on-device + PCC"]},
        {"label": "Google data access", "values": ["none"], "accent": True},
    ],
    "footnote": "Source: MacRumors, Jun 8 2026",
}
GRID_GLASS = {
    "type": "categorygrid", "bg": "gradient",
    "headline": "LIQUID GLASS CONTROL",
    "cards": [
        {"label": "iOS 26", "sub": "Clear or Tinted — two options"},
        {"label": "iOS 27", "sub": "continuous slider"},
    ],
    "selectIndex": 1, "selectAt": 1.0,
}
PANE_GLASS = {
    "type": "settingspane", "title": "Appearance", "back": "Settings",
    "appearance": "light",
    "groups": [
        {"header": "APPEARANCE",
         "rows": [
             {"label": "Automatic", "toggle": True, "on": True},
             {"label": "Light"},
             {"label": "Dark"},
         ]},
        {"header": "LIQUID GLASS",
         "rows": [
             {"label": "Liquid Glass", "value": "Ultraclear",
              "tint": "#0aa9c2", "glyph": "◎", "chevron": True},
             {"label": "Tint", "value": "Off"},
         ],
         "footer": "Ultraclear to fully tinted, with a live preview."},
    ],
    "focus": "1.0", "focusAt": 0.6,
}
STAT_FASTER = {
    "type": "statcard", "title": "iOS 27 — Apple's own numbers",
    "titleRight": "vs iOS 26.4.2",
    "rows": [
        {"label": "App launches", "value": "up to 30% faster", "pct": 0.30},
        {"label": "Photos load", "value": "up to 70% faster", "pct": 0.70},
        {"label": "AirDrop", "value": "up to 80% faster", "pct": 0.80,
         "color": "#2fb98a"},
    ],
    "bg": "black", "footnote": "Source: Apple — apple.com/os/ios",
}
CASCADE_FASTER = {
    "type": "wordcascade", "bg": "cream",
    "words": [
        {"text": "FASTER — BUT", "style": "caps", "at": 0.15},
        {"text": "ON WHICH PHONE?", "style": "caps", "at": 0.7, "size": 1.35,
         "accent": True},
    ],
}
CHART_ADOPT = {
    "type": "chart", "bg": "black", "unit": "%",
    "kicker": "% OF iPHONES FROM THE LAST 4 YEARS",
    "title": "Adoption, at different ages",
    "items": [
        {"label": "iOS 26", "value": 74, "display": "74%", "sub": "150 days",
         "highlight": True},
        {"label": "iOS 18", "value": 76, "display": "76%", "sub": "127 days"},
        {"label": "iOS 17", "value": 76, "display": "76%", "sub": "139 days"},
    ],
    "source": "Apple via 9to5Mac, Feb 13 2026",
}
SPEC_ADOPT = {
    "type": "specsheet", "kicker": "not a like-for-like loss",
    "title": "Why iOS 26 trailed", "columns": ["FACTOR"],
    "rows": [
        {"label": "Measured at", "values": ["150 days vs 127"]},
        {"label": "Models dropped", "values": ["3 vs 0"], "accent": True},
        {"label": "iOS 18 supported", "values": ["same as iOS 17"]},
    ],
    "footnote": "Source: 9to5Mac, Feb 13 2026",
}
CASCADE_DROPPED = {
    "type": "wordcascade", "bg": "cream",
    "words": [
        {"text": "iOS 26 CUT 3 PHONES", "style": "caps", "at": 0.12},
        {"text": "iOS 27 CUTS NONE", "style": "caps", "at": 0.7, "size": 1.3,
         "accent": True},
    ],
}
GRID_DROPPED = {
    "type": "categorygrid", "bg": "gradient",
    "headline": "THE REMOVED VARIABLE",
    "cards": [
        {"label": "iOS 26", "sub": "XS · XS Max · XR cut"},
        {"label": "iOS 27", "sub": "nothing cut"},
    ],
    "selectIndex": 1, "selectAt": 0.9,
}

# ── regions: (anchor, [builders]) — most SPECIFIC visual LAST ───────────────
REGIONS = [
    # hook -------------------------------------------------------------------
    # anchored on "back to" (1.40s) rather than "2019" (2.20s): G03 caps the
    # FIRST scene at 2.0s and the longer anchor made it 2.32s.
    ("back to", [split_hook]),
    ("gets iOS 27", [face(), rec("compat-noai", "compat-noai", 750, 1450,
                                 "Apple", sfx=[dict(GROUND, at=0.0)])]),
    ("reading about", [face(), mg(CASCADE_ALMOST)]),
    # zero devices dropped ---------------------------------------------------
    ("with the new iPhones", [az("macrumors-lede", "macrumors-lede", 1020, 1420,
                                 "MacRumors",
                                 {"x": 20, "y": 380, "w": 980, "h": 420},
                                 [ul(0.6, 45, 722, 690, 40)])]),
    ("zero devices", [mg(CASCADE_ZERO, sfx=[dict(MAGIC, at=0.55)])]),
    ("same list as iOS 26",
     [az("compat-noai", "compat-noai", 750, 1450, "Apple",
         {"x": 10, "y": 10, "w": 730, "h": 430}, [ul(0.55, 22, 20, 200, 40)]),
      az("compat-noai", "compat-noai", 750, 1450, "Apple",
         {"x": 10, "y": 1010, "w": 730, "h": 430},
         [ul(0.55, 22, 1352, 700, 40)])]),
    # the three tiers --------------------------------------------------------
    ("three different phones", [face()]),
    ("the full Siri AI", [mg(GRID_TIERS, sfx=[dict(POP, at=0.08)])]),
    ("and iPhone Air",
     [az("apple-notes", "apple-notes", 1080, 2280, "Apple",
         {"x": 60, "y": 180, "w": 1000, "h": 250},
         [ul(0.45, 100, 191, 778, 26)]),
      az("apple-notes", "apple-notes", 1080, 2280, "Apple",
         {"x": 60, "y": 205, "w": 700, "h": 190},
         [ul(0.5, 100, 239, 128, 26)], sfx=[dict(MAGIC, at=0.3)])]),
    ("standard Apple Intelligence",
     [(mg(SPEC_STANDARD), 0.54),
      az("apple-notes", "apple-notes", 1080, 2280, "Apple",
         {"x": 60, "y": 440, "w": 1000, "h": 260},
         [ul(0.5, 100, 549, 705, 26)])]),
    ("not the whole assistant", [rec("glass-lockscreen", "glass-lockscreen",
                                     1600, 960, "Apple", backdrop="black")]),
    ("no Apple Intelligence at all",
     [az("compat-noai", "compat-noai", 750, 1450, "Apple",
         {"x": 10, "y": 430, "w": 730, "h": 430}, []),
      mg(CASCADE_NOAI)]),
    # the sharpest cut in the lineup ----------------------------------------
    ("one model year", [face()]),
    ("iPhone 15 is out",
     [mg(GRID_INOUT, sfx=[dict(WHOOSH, at=0.0)]),
      az("compat-noai", "compat-noai", 750, 1450, "Apple",
         {"x": 10, "y": 10, "w": 730, "h": 300}, [circ(0.5, 20, 12, 230, 56)])]),
    # Gemini, stated correctly ----------------------------------------------
    ("genuinely rebuilt", [face(), rec("gemini-lede", "gemini-lede", 1020, 880,
                                       "MacRumors")]),
    ("behind Gemini",
     [az("gemini-lede", "gemini-lede", 1020, 880, "MacRumors",
         {"x": 20, "y": 440, "w": 980, "h": 400}, [ul(0.55, 45, 728, 880, 44)]),
      rec("gemini-diagram", "gemini-diagram", 924, 520, "Apple via MacRumors")]),
    ("handles your data",
     [mg(SPEC_PRIVACY),
      az("note-pcc", "note-pcc", 984, 560, "MacRumors",
         {"x": 15, "y": 10, "w": 950, "h": 200}, [ul(0.5, 25, 64, 700, 35)]),
      az("gemini-diagram", "gemini-diagram", 924, 520, "Apple via MacRumors",
         {"x": 300, "y": 150, "w": 330, "h": 250}, [])]),
    # the regional gap -------------------------------------------------------
    ("in the EU at launch",
     [rec("apple-dma", "apple-dma", 1080, 2340, "Apple Newsroom"),
      az("apple-dma", "apple-dma", 1080, 2340, "Apple Newsroom",
         {"x": 40, "y": 440, "w": 1000, "h": 620}, [ul(0.5, 60, 680, 760, 85)]),
      az("apple-dma", "apple-dma", 1080, 2340, "Apple Newsroom",
         {"x": 40, "y": 1660, "w": 1000, "h": 300},
         [ul(0.5, 60, 1726, 900, 36)])]),
    # what everyone actually gets -------------------------------------------
    ("story is underneath", [face()]),
    ("Liquid Glass slider", [mg(PANE_GLASS)]),
    ("two options",
     [mg(GRID_GLASS),
      az("note-glass", "note-glass", 828, 600, "Apple",
         {"x": 20, "y": 380, "w": 790, "h": 230},
         [ul(0.6, 60, 408, 690, 36)]),
      az("note-glass", "note-glass", 828, 600, "Apple",
         {"x": 20, "y": 440, "w": 790, "h": 160},
         [ul(0.6, 60, 487, 580, 36)])]),
    ("30% faster", [(mg(STAT_FASTER), 0.54), mg(CASCADE_FASTER)]),
    ("iPhone 11 Pro Max",
     [az("apple-notes", "apple-notes", 1080, 2280, "Apple",
         {"x": 60, "y": 1810, "w": 1000, "h": 320},
         [circ(0.55, 165, 1858, 300, 50)], sfx=[dict(IMPACT_B, at=0.5)]),
      az("apple-notes", "apple-notes", 1080, 2280, "Apple",
         {"x": 60, "y": 1880, "w": 1000, "h": 260},
         [ul(0.5, 442, 1919, 376, 24)])]),
    # adoption — closes the loop opened by "zero devices dropped" -----------
    ("iOS 26 stalled",
     [face(),
      az("9to5-notes", "9to5-notes", 1080, 1055, "9to5Mac",
         {"x": 30, "y": 810, "w": 1020, "h": 230},
         [ul(0.5, 48, 901, 944, 26)])]),
    ("had 127 days",
     [mg(CHART_ADOPT, sfx=[dict(CORE, at=0.1)]),
      rec("note-adopt", "note-adopt", 1044, 402, "9to5Mac"),
      mg(SPEC_ADOPT),
      az("9to5-notes", "9to5-notes", 1080, 1055, "9to5Mac",
         {"x": 30, "y": 480, "w": 1020, "h": 280},
         [ul(0.5, 48, 636, 522, 26)])]),
    ("removed the variable",
     [mg(CASCADE_DROPPED), mg(GRID_DROPPED),
      az("9to5-notes", "9to5-notes", 1080, 1055, "9to5Mac",
         {"x": 30, "y": 190, "w": 1020, "h": 280},
         [ul(0.5, 48, 348, 590, 26)])]),
    ("iPhone land in", [face(hl([("WHICH TIER IS", "headline", 0.25),
                                 ("YOUR iPHONE?", "headline", 0.7)], y=0.46))]),
]

# ── divide each region among its visuals ───────────────────────────────────
bounds, prev = [], 0.0
for phrase, builders in REGIONS:
    e = round(find(phrase) + 0.12, 2)
    bounds.append((phrase, builders, prev, e))
    prev = e
_p, _b, _s, _ = bounds[-1]
bounds[-1] = (_p, _b, _s, TOTAL)

scenes: list[dict] = []
for phrase, builders, s, e in bounds:
    span = round(e - s, 2)
    n = len(builders)
    # a builder may be (fn, weight); weights let a data card clear the 2.0s
    # G18 floor without pushing its neighbour under the 0.6s glitch floor.
    fns = [b[0] if isinstance(b, tuple) else b for b in builders]
    wts = [b[1] if isinstance(b, tuple) else None for b in builders]
    free = 1.0 - sum(w for w in wts if w)
    n_auto = sum(1 for w in wts if w is None)
    wts = [w if w else (free / n_auto if n_auto else 0) for w in wts]
    t = s
    for i, mk in enumerate(fns):
        d = round(span - (t - s), 2) if i == n - 1 else round(span * wts[i], 2)
        scenes.append(mk(t, d))
        t = round(t + d, 2)
    print(f"  {phrase[:30]:32s} {s:6.2f}-{e:6.2f} ({span:5.2f}s) /{n}")

# ── caption display fixes (timings never touched) ──────────────────────────
# whisper `base` heard "app launches" as "Apple launches" at 75.64s. VERIFIED
# with whisper `small` on the 73.6-77.8s slice: "And Apple says app launches are
# up to 30% faster." The AUDIO IS CORRECT — display-only fix (RULES.md 11).
# "Apple" cannot be replaced globally: the reel says it legitimately six other
# times. Keyed on TIME instead, as are two "in" mishears.
TIME_FIX = [
    (75.24, "Apple", "app"),
    (39.96, "N,", "in,"),
    (27.06, "in", "and"),
]
for _i, (_st, _en, _tx) in enumerate(words):
    for _t, _from, _to in TIME_FIX:
        if abs(_st - _t) < 0.15 and _tx == _from:
            words[_i] = (_st, _en, _to)
            print(f"  caption fix @{_st:.2f}s {_from!r} -> {_to!r}")

# Proper nouns whisper lower-cased, plus a hallucinated currency symbol on
# "iOS 18". Safe as plain string fixes — none collides with another word.
FIX = {"$18": "18", "intelligence": "Intelligence", "liquid": "Liquid",
       "glass": "Glass", "settings": "Settings", "appearance": "Appearance",
       "private": "Private", "cloud": "Cloud", "compute": "Compute"}


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


captions = []
for grp in chunk(words):
    text = " ".join(w[2] for w in grp)
    per = [{"t": round(w[0], 2), "text": w[2]} for w in grp]
    for a, b in FIX.items():
        text = text.replace(a, b)
        for q in per:
            q["text"] = q["text"].replace(a, b)
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                     "text": text, "words": [q for q in per if q["text"]]})

# ── music: automated, never flat (G09) ─────────────────────────────────────
# bed-184.mp3 from the style pack does not exist on this machine; every shipped
# reel uses bed-02.mp3 from=8.0, which is 118.0s — enough for a 104.7s reel.
music = {
    "src": "music/bed-02.mp3", "from": 8.0,
    "points": [
        {"t": 0.0, "vol": 0.15},                  # full at the hook
        {"t": 7.5, "vol": 0.08},                  # duck through the tiers
        {"t": round(TOTAL * 0.45, 2), "vol": 0.10},
        {"t": round(TOTAL * 0.72, 2), "vol": 0.14},   # rise into the payoff
        {"t": round(TOTAL - 6.0, 2), "vol": 0.15},
        {"t": round(TOTAL - 0.8, 2), "vol": 0.13},
        {"t": TOTAL, "vol": 0.02},                # fade
    ],
}

beats = {
    "id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "editorial",
    "format": "news", "tone": "serious",
    # config.avatarRegistry["f55b0b7c..."].register — a serious script
    # accepts a serious OR neutral presenter (G19).
    "avatarRegister": "neutral",
    "script": (ROOT / f"jobs/{SLUG}/script.md").read_text().strip(),
    "approval": json.loads(
        (ROOT / f"jobs/{SLUG}/approval.json").read_text()),
    "allowLong": True,
    "allowLongReason": (
        "User-approved 2026-08-17. Keeps the three-tier device split, the EU "
        "regulatory gap, the Gemini architecture correction and the iOS 26 "
        "adoption comparison that closes the loop opened by 'zero devices "
        "dropped'. Each carries its own receipt and its own number; none is "
        "padding. 254 approved words at the measured 2.4-2.7 wps cannot fit the "
        "60-80s news band; the master came back 104.65s. Well inside the 180s "
        "platform ceiling, and already trimmed once from 331 words."
    ),
    "audio": AVATAR, "music": music,
    "captionStyle": "word-reveal",
    "emphasis": ["2019", "zero", "three", "17", "15", "30%", "74%", "76%",
                 "150", "127", "none", "11"],
    "scenes": scenes, "captions": captions,
}

total = round(sum(s["durationSec"] for s in scenes), 2)
face_t = round(sum(s["durationSec"] for s in scenes
                   if "avatar-master" in str(s.get("src") or "")), 2)
print(f"\nscenes {total:.2f}s vs reel {TOTAL:.2f}s (delta {total - TOTAL:+.2f}s)")
print(f"{len(scenes)} scenes | facecam {face_t:.2f}s = "
      f"{100 * face_t / total:.1f}% | "
      f"{sum(len(s.get('sfx') or []) for s in scenes)} sfx cues")

try:
    for w in check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST):
        print(f"  warning: {w}")
    print("GATES: PASSED")
except GateError as e:
    raise SystemExit(f"GATES FAILED — beat sheet NOT written\n{e}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
