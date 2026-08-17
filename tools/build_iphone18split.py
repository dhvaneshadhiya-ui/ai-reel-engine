#!/usr/bin/env python3
"""Beat sheet for iphone18-split (editorial, news).

Pegatron's Aug 12 earnings call (via Economic Daily News / MacRumors +
AppleInsider) — supplier-tier sourcing, so claims are attributed once
(Pegatron / MacRumors / Kuo) then stated with confidence.

allowLong: the approved 242-word script delivers at this voice's measured
~2.6 wps (grok-bot 2.69, apple-pay-india 2.72), running 93.2s. The docs'
3.2 wps constant is wrong for this voice — logged in STYLE-RULES.md.
Cutting approved sentences without user sign-off was the worse option.

Treatments: split serif hook, Pegatron photo floatcards, annotatezoom
receipts (AppleInsider headline + byline; MacRumors body x3 regions + hero),
NEW categorygrid (two launch waves), timeline 3-stop rail (2019->2025->2027),
wordcascade (spring lineup), specsheet (parts crunch), NEW endquestion CTA.
No black typecard. No sourceread (grok-bot's). No logoassemble hook
(apple-pay-india's).
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

SLUG = "iphone18-split"
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
    if tx.startswith("-") and merged:
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
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}
hl = lambda lines, y=0.12, theme="light": {"lines": lines, "y": y,
                                           "theme": theme, "align": "center"}


def shot(name, zoom="in", headline=None, cb=None, sfx=None, hide=False):
    def b(t0, d):
        s = {"type": "footage", "src": f"{C}/{name}.mp4", "durationSec": d,
             "zoomDir": zoom, "credit": "Apple", "assetId": f"clip-{name}"}
        if headline: s["headline"] = headline
        if cb: s["captionBottom"] = cb
        if sfx: s["sfx"] = sfx
        if hide: s["hideCaptions"] = True
        return s
    return b


def face(headline=None, cb=300):
    def b(t0, d):
        s = {"type": "footage", "src": AVATAR, "durationSec": d,
             "from": round(t0, 2), "focusX": FOCUS_FULL, "captionBottom": cb}
        if headline: s["headline"] = headline
        return s
    return b


def flo(png, aid, aspect, credit, sfx=None):
    def b(t0, d):
        s = {"type": "floatcard", "src": f"{C}/{png}.png", "bg": "gradient",
             "aspect": aspect, "durationSec": d, "credit": credit,
             "assetId": aid}
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
        "topSrc": f"{C}/pro-camera.mp4", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": round(t0, 2),
        "bottomFocusX": FOCUS_SPLIT, "credit": "Apple",
        "assetId": "clip-pro-camera", "sfx": [dict(RISER, at=0.0)],
    }


def az(src, sw, sh, credit, aid, focus, annos, bg="cream", sfx=None):
    def b(t0, d):
        s = {"type": "annotatezoom", "durationSec": d, "src": f"{C}/{src}.png",
             "srcWidth": sw, "srcHeight": sh, "credit": credit, "bg": bg,
             "focus": focus, "annotations": annos, "assetId": aid}
        if sfx: s["sfx"] = sfx
        return s
    return b


AZ_AI = az("ai-hero", 2588, 2138, "AppleInsider", "receipt-ai-hero",
           {"x": 15, "y": 40, "w": 2320, "h": 480},
           [{"kind": "underline", "at": 0.5, "x": 20, "y": 90, "w": 2280, "h": 250}])
AZ_AI_BYLINE = az("ai-hero", 2588, 2138, "AppleInsider", "receipt-ai-hero",
                  {"x": 15, "y": 40, "w": 2320, "h": 560},
                  [{"kind": "circle", "at": 0.9, "x": 480, "y": 470, "w": 660, "h": 90}])
# mr-body is a MOBILE-width capture (390px CSS, scale 3) — the same rule as
# sourceread: a desktop-width column zooms out to unreadable in 9:16.
AZ_BODY_FOLD = az("mr-body", 1170, 1600, "MacRumors", "receipt-mr-body",
                  {"x": 20, "y": 150, "w": 1130, "h": 500},
                  [{"kind": "circle", "at": 0.8, "x": 140, "y": 415, "w": 580, "h": 75},
                   {"kind": "underline", "at": 1.6, "x": 190, "y": 555, "w": 420, "h": 55}])
AZ_BODY_STREAK = az("mr-body", 1170, 1600, "MacRumors", "receipt-mr-body",
                    {"x": 20, "y": 640, "w": 1130, "h": 400},
                    [{"kind": "underline", "at": 0.5, "x": 76, "y": 680, "w": 990, "h": 52},
                     {"kind": "circle", "at": 1.4, "x": 695, "y": 920, "w": 230, "h": 64}])
AZ_BODY_KUO = az("mr-body", 1170, 1600, "MacRumors", "receipt-mr-body",
                 {"x": 20, "y": 1100, "w": 1130, "h": 480},
                 [{"kind": "circle", "at": 0.8, "x": 225, "y": 1295, "w": 320, "h": 70},
                  {"kind": "underline", "at": 1.5, "x": 780, "y": 1370, "w": 280, "h": 50}])
AZ_HERO = az("mr-hero", 1820, 1420, "MacRumors", "receipt-mr-hero",
             {"x": 0, "y": 0, "w": 1820, "h": 720},
             [{"kind": "underline", "at": 0.5, "x": 45, "y": 26, "w": 1310, "h": 66}],
             sfx=[dict(WHOOSH, at=0.0)])

GRID_WAVES = {
    "type": "categorygrid", "bg": "gradient",
    "headline": "ONE LAUNCH, SPLIT IN TWO",
    "cards": [{"label": "SEPTEMBER 2026", "sub": "18 Pro · Pro Max · “Ultra”"},
              {"label": "MARCH 2027", "sub": "iPhone 18 · 18e · Air 2"}],
}
WC_SPRING = {
    "type": "wordcascade", "bg": "cream", "captionTheme": "dark",
    "words": [{"text": "iPhone 18", "style": "serif", "at": 0.1, "size": 1.1},
              {"text": "iPhone 18e", "style": "serif", "at": 0.75, "size": 1.1},
              {"text": "iPhone Air 2", "style": "caps", "at": 1.4,
               "size": 1.2, "accent": True}],
}
TL_STREAK = {
    "type": "timeline", "title": "7 Septembers straight",
    "kicker": "the standard iPhone",
    "footnote": "MacRumors · Aug 12, 2026",
    "items": [
        {"date": "2019", "name": "iPhone 11", "sub": "September", "at": 0.2},
        {"date": "2025", "name": "iPhone 17", "sub": "September", "at": 0.85},
        {"date": "2027", "name": "iPhone 18", "sub": "March — the break",
         "accent": "MOVED", "at": 1.5},
    ],
}
SPEC_2028 = {
    "type": "specsheet", "kicker": "Pegatron, on the same call",
    "title": "The parts crunch", "columns": ["OUTLOOK"],
    "rows": [{"label": "Semiconductors", "values": ["tight into 2028"]},
             {"label": "Memory (RAM)", "values": ["tight into 2028"],
              "accent": True}],
    "footnote": "Pegatron, via AppleInsider · Aug 12, 2026",
}
END_Q = {
    "type": "endquestion", "src": f"{C}/pro-lineup-still.jpg",
    "question": "Wait till March — or buy the Pro?", "bg": "gradient",
    "assetId": "still-pro-lineup",
}

HL_NOPHONE = hl([{"text": "THIS SEPTEMBER", "kind": "label", "at": 0.15},
                 {"text": "NO iPhone 18", "kind": "headline", "at": 0.5,
                  "accent": True}], y=0.10)
HL_WAVE1 = hl([{"text": "WAVE 1 · September 2026", "kind": "label",
                "at": 0.2}], y=0.09)
HL_PROMAX = hl([{"text": "18 PRO · PRO MAX", "kind": "label", "at": 0.2}], y=0.09)
HL_WAVE2 = hl([{"text": "WAVE 2 · March 2027", "kind": "label", "at": 0.2}], y=0.09)
HL_PROONLY = hl([{"text": "September 2026", "kind": "label", "at": 0.1},
                 {"text": "PRO-ONLY", "kind": "headline", "at": 0.45,
                  "accent": True}], y=0.10)
HL_DATES = hl([{"text": "IN EVERY LEAK", "kind": "label", "at": 0.15},
               {"text": "DATES ARE THE", "kind": "headline", "at": 0.45},
               {"text": "SOFTEST DETAIL", "kind": "headline", "at": 0.7,
                "accent": True}], y=0.40)
HL_TWICE = hl([{"text": "TWICE A YEAR", "kind": "headline", "at": 0.6,
                "accent": True}], y=0.42)
HL_CTA = hl([{"text": "MARCH — OR THE PRO?", "kind": "label", "at": 0.2},
             {"text": "TELL ME BELOW", "kind": "headline", "at": 0.6,
              "accent": True}], y=0.07)

regions = [
    ("apple just skipped the iphone", [split_hook]),
    ("this september",           [shot("pro-molten", headline=HL_NOPHONE,
                                       sfx=[dict(IMPACT, at=0.4)]),
                                  shot("ev-macro", zoom="out")]),
    ("earnings call",            [face(),
                                  flo("pegatron-building", "still-pegatron-building",
                                      1792 / 1330, "AppleInsider"),
                                  AZ_AI]),
    ("splitting the iphone",     [mg(GRID_WAVES, sfx=[dict(WHOOSH, at=0.0)])]),
    ("pro the 18 pro max",       [shot("pro-lineup"),
                                  shot("pro-trio-backs", zoom="out",
                                       headline=HL_WAVE1),
                                  shot("pro-profile", headline=HL_PROMAX)]),
    ("the iphone ultra",         [face(), AZ_BODY_FOLD]),
    ("wave 2 march 2027",        [shot("ev-fan", headline=HL_WAVE2)]),
    ("the iphone air 2",         [mg(WC_SPRING), shot("air-thin")]),
    ("seven generations straight", [shot("ev-blue", zoom="out"),
                                    AZ_BODY_STREAK,
                                    mg(TL_STREAK, sfx=[dict(GROUND, at=0.2)])]),
    ("pure premium show",        [shot("pro-unibody", headline=HL_PROONLY),
                                  shot("ev-title", zoom="out")]),
    ("apples fattest margins",   [face()]),
    ("entire holiday quarter",   [shot("pro-neon")]),
    ("component shortages",      [flo("pegatron-gate", "still-pegatron-gate",
                                      1000 / 630, "AppleInsider"),
                                  shot("pro-chips")]),
    ("into 2028",                [shot("pro-wafer", zoom="out"),
                                  mg(SPEC_2028, sfx=[dict(IMPACT, at=0.3)])]),
    ("parts are scarce",         [face()]),
    ("iphones fighting",         [shot("air-internals")]),
    ("at once",                  [shot("pro-glass", zoom="out")]),
    ("has been building",        [AZ_HERO]),
    ("spring 2027",              [face(), AZ_BODY_KUO]),
    ("said it out",              [shot("air-mood", zoom="out"), AZ_AI_BYLINE]),
    ("apple hasnt confirmed",    [face()]),
    ("dates are always",         [shot("pro-rain", headline=HL_DATES, cb=1500)]),
    ("if it sticks",             [shot("pro-machine", zoom="out")]),
    ("a twice a year event",     [shot("ev-splash", headline=HL_TWICE,
                                       hide=True, sfx=[dict(IMPACT, at=0.2)])]),
    ("comments",                 [shot("air-fingertip",
                                       sfx=[dict(RISER, at=0.3)]),
                                  mg(END_Q),
                                  face(headline=HL_CTA)]),
]

placed = region_bounds(regions, TOTAL)
scenes = [b(s0, round(s1 - s0, 2)) for (_, s0, s1, b) in placed]
R = {}
for ph, s0, s1, _ in placed:
    a, b_ = R.get(ph, (s0, s1))
    R[ph] = (min(a, s0), max(b_, s1))
print(f"  {len(regions)} regions -> {len(scenes)} scenes")

# ── captions ────────────────────────────────────────────────────────────────


def chunk(ws, size=3):
    out, buf = [], []
    for (s, e, w) in ws:
        buf.append((s, e, w))
        if len(buf) >= size or (re.search(r"[.,!?—:;]$", w) and len(buf) >= 2):
            out.append(buf); buf = []
    if buf: out.append(buf)
    return out


# display-only fixes; timings untouched. Verified with whisper small:
# voice says "Ming-Chi Kuo" correctly; base writes "Mingchi Quo".
FIX = {"Mingchi": "Ming-Chi", "Quo": "Kuo"}
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
    {"t": R["earnings call"][0], "vol": 0.09},
    {"t": R["seven generations straight"][0], "vol": 0.07},
    {"t": R["into 2028"][0], "vol": 0.10},
    {"t": R["has been building"][0], "vol": 0.08},
    {"t": R["a twice a year event"][0], "vol": 0.14},
    {"t": R["comments"][0], "vol": 0.13},
    {"t": TOTAL - 0.8, "vol": 0.10},
    {"t": TOTAL, "vol": 0.02}]}

beats = {"id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "editorial",
         "format": "news",
         "audio": AVATAR, "music": music, "captionStyle": "word-reveal",
         "script": (ROOT / "jobs" / SLUG / "script.md").read_text(),
         "approval": json.loads((ROOT / "jobs" / SLUG / "approval.json").read_text()),
         "allowLong": True,
         "allowLongReason": (
             "Approved 242-word script (hash 02bc3f9e56c5c17c) delivers at this "
             "voice's measured ~2.6 wps (grok-bot 2.69, apple-pay-india 2.72 on "
             "the same voice), running 93.2s. The 3.2 wps planning constant in "
             "the docs is wrong for this voice; word budgets re-derived in "
             "STYLE-RULES.md 2026-08-13. Cutting approved sentences without "
             "user sign-off was rejected; user offered a trim+re-record."),
         "emphasis": ["skipped", "Pegatron", "two", "Ultra", "2027", "18e",
                      "margins", "2028", "six"],
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
