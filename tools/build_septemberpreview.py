#!/usr/bin/env python3
"""Beat sheet for september-preview (varun-mayya, news).

Aggregate rumor roundup (user rule 2026-08-14: MacRumors never named in VO —
attribution rides on-screen credits + "rumors say"/"DigiTimes"). Cook/Ternus
transition is OFFICIAL (Apple newsroom) and stated flat.

Numbered-item serif labels (01-05) tie the roundup together. Receipt backbone
= sourceread on MOBILE captures (5 passes, never two adjacent on one png).
NEW treatments: statcard with REAL proportional bars (5.5" vs 7.8"),
uidialog x2 (Reminders Sept-1 + Calendar event invite). No annotatezoom, no
categorygrid, no endquestion, no timeline (all last reel's).
Master was surgically shortened 86.2->79.8s (user-approved line cut +
11 pause tightenings) — inside the 60-80s band, no allowLong.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402
from notation import normalise, normalise_words  # noqa: E402

SLUG = "september-preview"
ROOT = Path(__file__).resolve().parent.parent
A, C = f"assets/{SLUG}", f"assets/{SLUG}/clips"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master-169.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())
CANON = MANIFEST.get("notation", {})

raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())
words = [(w["start"], w["end"], w["word"].strip())
         for s in raw["segments"] for w in s["words"]]
merged = []
for st, en, tx in words:
    # "-suffix" fragments (hyphenated words) AND ",000"-style thousand-group
    # fragments both belong to the previous token — whisper splits "$2,000"
    # into "$2" + ",000" and a bare ",000" chip is unshippable (2026-08-14).
    if (tx.startswith("-") or re.match(r"^[.,]\d", tx)) and merged:
        p = merged[-1]
        merged[-1] = (p[0], en, p[2] + tx)
    else:
        merged.append((st, en, tx))
words = merged
TOTAL = round(words[-1][1] + 0.35, 2)
print(f"{len(words)} words, VO ends {words[-1][1]:.2f}s, reel {TOTAL:.2f}s")


def css_pos(fx, iw, ih, cw, ch):
    s = max(cw / iw, ch / ih); w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


FOCUS_FULL = css_pos(FACE_X, 1920, 1080, 1080, 1920)
FOCUS_SPLIT = css_pos(FACE_X, 1920, 1080, 1080, 960)
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
stream = [norm(w[2]) for w in words]


def find(phrase):
    t = norm(phrase).split()
    for i in range(len(stream) - len(t) + 1):
        if stream[i:i + len(t)] == t:
            return words[i + len(t) - 1][1]
    raise SystemExit(f"ANCHOR NOT FOUND: {phrase!r}")


def region_bounds(regions, total):
    out, prev = [], 0.0
    for k, (phrase, builders) in enumerate(regions):
        end = total if k == len(regions) - 1 else round(find(phrase) + 0.12, 2)
        n = len(builders)
        while n > 1 and (end - prev) / n < 0.6:
            n -= 1
        builders = builders[:n]
        step = (end - prev) / n
        for j, b in enumerate(builders):
            s0 = prev + j * step
            s1 = end if j == n - 1 else prev + (j + 1) * step
            out.append((phrase, round(s0, 2), round(s1, 2), b))
        prev = end
    return out


RISER = {"src": "sfx2/risers-01.mp3", "vol": 0.14}
IMPACT = {"src": "sfx2/impact-boom.mp3", "vol": 0.16}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.13}
CLICK = {"src": "sfx2/mouse-click-01.mp3", "vol": 0.12}
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}
hl = lambda lines, y=0.10, theme="light": {"lines": lines, "y": y,
                                           "theme": theme, "align": "center"}


def shot(name, zoom="in", headline=None, cb=None, sfx=None, infocard=None):
    def b(t0, d):
        s = {"type": "footage", "src": f"{C}/{name}.mp4", "durationSec": d,
             "zoomDir": zoom, "credit": "Apple", "assetId": f"clip-{name}"}
        if headline: s["headline"] = headline
        if cb: s["captionBottom"] = cb
        if sfx: s["sfx"] = sfx
        if infocard: s["infocard"] = infocard
        return s
    return b


def face(headline=None, cb=300, infocard=None):
    def b(t0, d):
        s = {"type": "footage", "src": AVATAR, "durationSec": d,
             "from": round(t0, 2), "focusX": FOCUS_FULL, "captionBottom": cb}
        if headline: s["headline"] = headline
        if infocard: s["infocard"] = infocard
        return s
    return b


def flo(png, aid, aspect, credit, headline=None, sfx=None):
    def b(t0, d):
        s = {"type": "floatcard", "src": f"{C}/{png}.png", "bg": "gradient",
             "aspect": aspect, "durationSec": d, "credit": credit,
             "assetId": aid}
        if headline: s["headline"] = headline
        if sfx: s["sfx"] = sfx
        return s
    return b


def mg(spec, sfx=None):
    def b(t0, d):
        s = dict(spec, durationSec=d)
        if sfx: s["sfx"] = sfx
        return s
    return b


def split_hook(t0, d):
    return {
        "type": "split", "durationSec": d, "captionBottom": 1000,
        "topSrc": f"{C}/p-rods.mp4", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": round(t0, 2),
        "bottomFocusX": FOCUS_SPLIT, "credit": "Apple",
        "assetId": "clip-p-rods", "sfx": [dict(WHOOSH, at=0.0)],
    }


def sread(png, sw, sh, aid, lines, credit="MacRumors"):
    def b(t0, d):
        return {"type": "sourceread", "durationSec": d,
                "src": f"{C}/{png}.png", "srcWidth": sw, "srcHeight": sh,
                "credit": credit, "follow": True, "lines": lines,
                "assetId": aid}
    return b


# mrs-fold 1170x1600 (grid-read)
SR_FOLD_A = sread("mrs-fold", 1170, 1640, "receipt-mrs-fold", [
    {"at": 0.2, "x": 77, "y": 300, "w": 990, "h": 50},    # first foldable...ready to
    {"at": 1.1, "x": 77, "y": 365, "w": 1000, "h": 50},   # launch. "iPhone Ultra"
])
SR_FOLD_B = sread("mrs-fold", 1170, 1640, "receipt-mrs-fold", [
    {"at": 0.2, "x": 77, "y": 428, "w": 990, "h": 50},    # ~5.5-inch...~7.8-
    {"at": 1.1, "x": 77, "y": 492, "w": 1000, "h": 50},   # inch display...4:3
])
SR_S12 = sread("mrs-s12", 1170, 500, "receipt-mrs-s12", [
    {"at": 0.2, "x": 77, "y": 220, "w": 955, "h": 50},    # faster S-series chip
    {"at": 0.9, "x": 77, "y": 410, "w": 700, "h": 50},    # battery...battery life
    {"at": 1.5, "x": 77, "y": 157, "w": 955, "h": 50},    # no design changes
])
SR_U_A = sread("mrs-ultra", 1170, 1250, "receipt-mrs-ultra", [
    {"at": 0.15, "x": 77, "y": 303, "w": 1000, "h": 48},  # DigiTimes claimed
    {"at": 0.55, "x": 77, "y": 366, "w": 965, "h": 48},   # thinner...sensing
])
SR_U_B = sread("mrs-ultra", 1170, 1250, "receipt-mrs-ultra", [
    {"at": 0.3, "x": 77, "y": 429, "w": 1015, "h": 48},   # isn't always accurate
    {"at": 1.1, "x": 77, "y": 492, "w": 690, "h": 48},    # rumors...the claim
])

SPEC_PRO = {
    "type": "specsheet", "kicker": "the flagships",
    "title": "iPhone 18 Pro · Pro Max", "columns": ["RUMORED"],
    "rows": [{"label": "Chip", "values": ["A20 Pro · 2nm"]},
             {"label": "Camera", "values": ["variable aperture"]},
             {"label": "Dynamic Island", "values": ["smaller"]},
             {"label": "New color", "values": ["Dark Cherry"], "accent": True}],
    "footnote": "MacRumors · Aug 13, 2026",
}
STAT_SCREENS = {
    "type": "statcard", "title": "iPhone Ultra — two screens",
    "rows": [{"label": "Closed", "value": "5.5″", "pct": 0.71},
             {"label": "Unfolded", "value": "7.8″", "pct": 1.0,
              "color": "#E0785A"}],
    "footnote": "MacRumors · Aug 13, 2026", "bg": "black",
}
CHECK_ULTRA = {
    "type": "checklist", "bg": "gradient", "headline": "iPhone Ultra hardware",
    "rows": [{"label": "Touch ID — not Face ID", "state": "done"},
             {"label": "Dual batteries", "state": "done"},
             {"label": "Crease-hiding hinge", "state": "done"}],
}
DIALOG_SEPT1 = {
    "type": "uidialog", "app": "Reminders",
    "title": "New CEO takes over",
    "body": "John Ternus becomes CEO · Tim Cook becomes Executive Chairman",
    "field": {"label": "Date", "value": "Mon, September 1, 2026"},
    "primary": "Remind me",
    "assetId": "receipt-ceo-hero",
}
DIALOG_EVENT = {
    "type": "uidialog", "app": "Calendar",
    "title": "Apple Event (rumored)",
    "body": "Apple Park · pre-orders the same week",
    "field": {"label": "When", "value": "Tue Sep 8 — or Wed Sep 9"},
    "primary": "Accept", "cancel": "Decline",
    "assetId": "receipt-mrs-hero",
}
CASC_NO18 = {
    "type": "wordcascade", "bg": "cream", "captionTheme": "dark",
    "words": [{"text": "NO iPhone 18", "style": "serif", "at": 0.15, "size": 1.1},
              {"text": "→ March 2027", "style": "caps", "at": 1.0,
               "size": 1.2, "accent": True}],
}
CASC_CHOICE = {
    "type": "wordcascade", "bg": "black", "captionTheme": "light",
    "words": [{"text": "the foldable?", "style": "serif", "at": 0.15, "size": 1.1},
              {"text": "OR THE PRO?", "style": "caps", "at": 1.0,
               "size": 1.25, "accent": True}],
}

HL01 = hl([{"text": "01 · iPhone 18 Pro · Pro Max", "kind": "label", "at": 0.2}])
HL02 = hl([{"text": "02 · iPhone Ultra", "kind": "label", "at": 0.2}])
HL03 = hl([{"text": "03 · Watch Series 12", "kind": "label", "at": 0.15}])
HL04 = hl([{"text": "04 · Watch Ultra 4", "kind": "label", "at": 0.15}])
HL05 = hl([{"text": "05 · A NEW BOSS", "kind": "label", "at": 0.2}])
HL_CATCH = hl([{"text": "THE CATCH?", "kind": "headline", "at": 0.35,
                "accent": True}], y=0.40)
HL_300 = hl([{"text": "UP TO", "kind": "label", "at": 0.15},
             {"text": "+$300", "kind": "headline", "at": 0.5,
              "accent": True}], y=0.40)
HL_CTA = hl([{"text": "FOLDABLE — OR PRO?", "kind": "label", "at": 0.2},
             {"text": "TELL ME BELOW", "kind": "headline", "at": 0.6,
              "accent": True}], y=0.07)
IC_2K = {"heading": "$2,000–$2,500", "body": "rumored price range", "at": 0.5}

regions = [
    ("at least",                 [split_hook]),
    ("this september",           [flo("mrs-hero", "receipt-mrs-hero",
                                      1170 / 580, "MacRumors")]),
    ("pro and pro max",          [shot("p-dust", headline=HL01)]),
    ("dark cherry color",        [shot("p-drop"),
                                  shot("p-frame", zoom="out"),
                                  mg(SPEC_PRO, sfx=[dict(IMPACT, at=0.3)])]),
    ("300 priceyear",            [shot("p-catch", headline=HL_CATCH,
                                       sfx=[dict(WHOOSH, at=0.2)]),
                                  shot("p-macro", headline=HL_300)]),
    ("the headliner",            [shot("ev-bubble", headline=HL02)]),
    ("the iphone",               [SR_FOLD_A]),
    ("basically",                [SR_FOLD_B,
                                  mg(STAT_SCREENS, sfx=[dict(CLICK, at=0.4)])]),
    ("in your pocket",           [shot("p-hand")]),
    ("instead of face id",       [face()]),
    ("and a hinge",              [mg(CHECK_ULTRA)]),
    ("and 2500",                     [shot("p-edge", zoom="out"),
                                  face(infocard=IC_2K)]),
    ("third watch",              [shot("w-trio", headline=HL03)]),
    ("faster chip",              [shot("w-sleep")]),
    ("bigger battery",           [shot("w-gold")]),
    ("same look",                [shot("w-sos")]),
    ("watch ultra 4",            [shot("w-ultra", headline=HL04),
                                  SR_U_A]),
    ("upgraded sensors",         [face()]),
    ("a single source",          [SR_U_B]),
    ("a new boss",               [face(headline=HL05),
                                  flo("ceo-hero", "receipt-ceo-hero",
                                      1170 / 1020, "Apple Newsroom",
                                      sfx=[dict(WHOOSH, at=0.0)])]),
    ("runs his first",           [flo("ceo-photo", "still-ceo-photo",
                                      1170 / 1000, "Apple Newsroom")]),
    ("officially becomes",       [flo("ceo-body", "still-ceo-body",
                                      1170 / 1000, "Apple Newsroom"),
                                  face()]),
    ("chairman on september",    [mg(DIALOG_SEPT1)]),
    ("isnt a rumor",             [flo("ceo-hero", "receipt-ceo-hero",
                                      1170 / 1020, "Apple Newsroom")]),
    ("the standard iphone",      [shot("p-stadium", zoom="out")]),
    ("moved to march",           [mg(CASC_NO18, sfx=[dict(IMPACT, at=1.0)])]),
    ("8th or 9th",               [mg(DIALOG_EVENT)]),
    ("the same week",            [shot("p-night")]),
    ("or the",                   [mg(CASC_CHOICE, sfx=[dict(IMPACT, at=1.0)])]),
    ("comments",                 [face(headline=HL_CTA)]),
]

placed = region_bounds(regions, TOTAL)
scenes = [b(s0, round(s1 - s0, 2)) for (_, s0, s1, b) in placed]
R = {}
for ph, s0, s1, _ in placed:
    a, b_ = R.get(ph, (s0, s1))
    R[ph] = (min(a, s0), max(b_, s1))
print(f"  {len(regions)} regions -> {len(scenes)} scenes")


def chunk(ws, size=3):
    out, buf = [], []
    for (s, e, w) in ws:
        buf.append((s, e, w))
        if len(buf) >= size or (re.search(r"[.,!?—:;]$", w) and len(buf) >= 2):
            out.append(buf); buf = []
    if buf: out.append(buf)
    return out


# display-only fixes for whisper mishears; timings untouched.
FIX = {"20-pro": "A20 Pro", "price-year": "pricier", "watch": "Watch",
       "dynamic": "Dynamic", "island": "Island", "dark": "Dark",
       "cherry": "Cherry"}
caption_words = normalise_words(words, CANON)
fixed = []
for s, e, t in caption_words:
    for a, b in FIX.items():
        t = re.sub(rf"(?<![\w-]){re.escape(a)}(?![\w-])", b, t, flags=re.I)
    fixed.append((s, e, t))
captions = []
for grp in chunk(fixed):
    text = normalise(" ".join(w[2] for w in grp), CANON)
    per = [{"t": round(w[0], 2), "text": normalise(w[2], CANON)} for w in grp]
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                     "text": text, "words": [p for p in per if p["text"]]})

music = {"src": "music/bed-02.mp3", "from": 8.0, "points": [
    {"t": 0.0, "vol": 0.15},
    {"t": R["pro and pro max"][0], "vol": 0.09},
    {"t": R["the headliner"][0], "vol": 0.12},
    {"t": R["instead of face id"][0], "vol": 0.08},
    {"t": R["a new boss"][0], "vol": 0.12},
    {"t": R["officially becomes"][0], "vol": 0.08},
    {"t": R["or the"][0], "vol": 0.14},
    {"t": TOTAL - 0.8, "vol": 0.10},
    {"t": TOTAL, "vol": 0.02}]}

beats = {"id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "varun",
         "format": "news",
         "audio": AVATAR, "music": music, "captionStyle": "nick-display",
         "script": (ROOT / "jobs" / SLUG / "script.md").read_text(),
         "approval": json.loads((ROOT / "jobs" / SLUG / "approval.json").read_text()),
         "emphasis": ["five", "foldable", "Ultra", "Ternus", "March",
                      "squint", "boss"],
         "scenes": scenes, "captions": captions}

total = round(sum(s["durationSec"] for s in scenes), 2)
fs = sum(s["durationSec"] for s in scenes if s.get("src") == AVATAR)
print(f"\nscenes {total:.2f}s vs reel {TOTAL:.2f}s | {len(scenes)} scenes, "
      f"avg {total / len(scenes):.2f}s | facecam {100 * fs / total:.0f}%")

clip_durations = {}
for sc in scenes:
    for k in ("src", "topSrc", "bgSrc"):
        v = sc.get(k)
        if not v or "avatar-master" in str(v) or v in clip_durations:
            continue
        f = ROOT / "public" / str(v)
        if not f.exists():
            raise SystemExit(f"MISSING ASSET: {f}")
        if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            continue
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                              "format=duration", "-of", "csv=p=0", str(f)],
                             capture_output=True, text=True)
        clip_durations[str(v)] = float(out.stdout.strip())

try:
    for w in check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST,
                         clip_durations=clip_durations):
        print(f"  warning: {w}")
    print("GATES: PASSED")
except GateError as e:
    raise SystemExit(f"GATES FAILED — beat sheet NOT written\n{e}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
