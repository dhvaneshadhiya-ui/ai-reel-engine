#!/usr/bin/env python3
"""made-by-google-26 — Everything announced at Made by Google 2026.

Built per scripts/made-by-google-26.md (user-approved 2026-08-13).
allowLong: user explicitly asked for an ~2-minute reel; master is 135.2s
after pause-tightening (15 jump cuts in silence, none under a facecam beat).
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

SLUG = "made-by-google-26"

ROOT = Path(__file__).resolve().parent.parent
A = f"assets/{SLUG}"
C = f"{A}/clips"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master-169.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())
CANON = MANIFEST.get("notation", {})
SCRIPT = (ROOT / f"jobs/{SLUG}/script.md").read_text().strip()
APPROVAL = json.loads((ROOT / f"jobs/{SLUG}/approval.json").read_text())

# ── voiceover is the master clock ───────────────────────────────────────────
raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())
words = [(w["start"], w["end"], w["word"].strip())
         for s in raw["segments"] for w in s["words"]]

merged = []
for st, en, tx in words:
    if (tx.startswith("-") or tx.startswith(".")) and merged:
        p = merged[-1]
        merged[-1] = (p[0], en, p[2] + tx)
    else:
        merged.append((st, en, tx))
words = merged

# "3.5 times" -> "3.5x", "120 times" -> "120x", "three times" -> "3x"
# (display only; timings keep the pair's span)
merged2, skip = [], False
for i, (st, en, tx) in enumerate(words):
    if skip:
        skip = False
        continue
    nxt = words[i + 1] if i + 1 < len(words) else None
    base = tx.rstrip(".,!?")
    if nxt and nxt[2].rstrip(".,!?").lower() == "times" and \
            re.fullmatch(r"(\d+(\.\d+)?|three)", base, re.I):
        num = "3" if base.lower() == "three" else base
        tail = nxt[2][len(nxt[2].rstrip(".,!?")):]
        merged2.append((st, nxt[1], f"{num}x{tail}"))
        skip = True
    else:
        merged2.append((st, en, tx))
words = merged2

TOTAL = round(words[-1][1] + 0.35, 2)
print(f"{len(words)} words, VO ends {words[-1][1]:.2f}s, reel {TOTAL:.2f}s")

# former master jump-cut points — no facecam scene may SPAN one
CUTS = [12.83, 33.11, 41.89, 50.09, 58.79, 66.81, 74.39, 80.29, 87.57,
        92.45, 95.57, 97.81, 102.01, 110.59, 117.31]


def css_pos(fx, iw, ih, cw, ch):
    s = max(cw / iw, ch / ih)
    w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


FOCUS_FULL = css_pos(FACE_X, 1920, 1080, 1080, 1920)
FOCUS_SPLIT = css_pos(FACE_X, 1920, 1080, 1080, 960)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


stream_all = [norm(w[2]) for w in words]
IDX = [i for i, s in enumerate(stream_all) if s]        # skip "%" -> "" tokens
stream = [stream_all[i] for i in IDX]


def find(phrase, after=0.0):
    t = norm(phrase).split()
    for i in range(len(stream) - len(t) + 1):
        if stream[i:i + len(t)] == t:
            e = words[IDX[i + len(t) - 1]][1]
            if e > after + 0.05:
                return e
    raise SystemExit(f"ANCHOR NOT FOUND after {after:.1f}s: {phrase!r}")


anchors = [
    ("hook",       "google just refreshed every"),
    ("hardware",   "single piece of hardware it makes"),
    ("fourpix",    "four new pixels a new watch"),
    ("trackera",   "and a 29 tracker"),
    ("trackerb",   "with a billion android phones behind it"),
    ("mbg26",      "this is made by google 2026"),
    ("matters",    "everything that actually matters in two minutes"),
    ("p11pricea",  "the pixel 11 is"),
    ("p11priceb",  "899 now"),
    ("cambar",     "with a camera bar thats 40  thinner"),
    ("sensora",    "behind the glass is a new"),
    ("sensorb",    "48 megapixel sensor"),
    ("light",      "pulling in 56  more light"),
    ("displaya",   "the pro and pro xl push"),
    ("displayb",   "a 3600nit display"),
    ("zoom120",    "and pro zoom hits 120x"),
    ("lookat",     "just look at this"),
    ("charges",    "the pro xl also charges"),
    ("battery",    "15 hours of battery in 15 minutes"),
    ("foldlighta", "the pixel 11 pro fold"),
    ("foldlightb", "is nearly 10  lighter"),
    ("foldthin",   "almost a millimeter thinner"),
    ("durable",    "and 3x more durable"),
    ("cracka",     "google says the new back"),
    ("crackb",     "is nearly impossible to crack"),
    ("bridge",     "heres the part almost nobody noticed"),
    ("tensor",     "all of it runs on tensor g6"),
    ("compute",    "50  more ai compute"),
    ("faster",     "so gemini runs 35x faster"),
    ("energy",     "on 35x less energy"),
    ("titanintro", "and the new titan m3 chip"),
    ("titan",      "is hardened against quantum computer attacks"),
    ("decade",     "google is planning a decade ahead"),
    ("watch5",     "pixel watch 5 is 20  faster"),
    ("gpsa",       "tracks gps routes"),
    ("gpsb",       "twice as accurately and its"),
    ("insulin",    "the only watch tracking insulin resistance trends"),
    ("breathing",  "it can even detect a breathing emergency"),
    ("help",       "and call for help on its own"),
    ("tagintro",   "then the pixel tag"),
    ("tagspecs",   "29 stainless steel a oneyear"),
    ("tagfindsa",  "battery and it finds your"),
    ("tagfindsb",  "stuff through over a billion android devices"),
    ("airtag",     "the air tag finally has a real fight"),
    ("asla",       "the camera now translates"),
    ("aslb",       "american sign language live"),
    ("watchthis",  "just watch this magic capture"),
    ("frames",     "picks your best shot from around 500 frames"),
    ("rambler",    "and rambler turns your voice rambles"),
    ("cleantext",  "into clean text"),
    ("catch",      "now the catch"),
    ("pricebump",  "every single phone got a 100 price bump"),
    ("budsa",      "this year and pixel buds pro 2"),
    ("budsb",      "only got a new color anyways"),
    ("updates",    "every phone gets 7 years of updates"),
    ("gigs",       "and starts at 256 gigs"),
    ("aug20",      "they hit shelves august 20th"),
    ("nov11",      "the tag lands november 11th"),
    ("quantuma",   "so a quantum proof phone"),
    ("quantumb",   "and a 29 tracker"),
    ("iphone",     "is that enough to pull you off your iphone"),
    ("comments",   "tell me in the comments"),
]

# per-anchor end-pad overrides (default 0.12) — used to keep a beat inside its
# pacing ceiling or to align a facecam boundary onto a master jump-cut point
PAD = {"displaya": -0.05, "displayb": -0.05, "energy": 0.30, "tensor": -0.05, "faster": -0.15}

bounds, prev = [], 0.0
for name, ph in anchors:
    e = round(find(ph, after=prev) + PAD.get(name, 0.12), 2)
    bounds.append((name, prev, e))
    prev = e
bounds[-1] = (bounds[-1][0], bounds[-1][1], TOTAL)
B = {n: (s, e) for n, s, e in bounds}
for n, s, e in bounds:
    print(f"  {n:10s} {s:6.2f}-{e:6.2f} ({e - s:.2f}s)")


def dur(n):
    return round(B[n][1] - B[n][0], 2)


def face_spans_cut(n):
    s, e = B[n]
    return [c for c in CUTS if s + 0.05 < c < e - 0.05]


FACE_BEATS = ["matters", "durable", "cracka", "crackb", "titanintro",
              "decade", "airtag", "catch", "quantuma", "quantumb",
              "iphone", "comments"]
for fb in FACE_BEATS:
    bad = face_spans_cut(fb)
    if bad:
        print(f"  !! facecam beat {fb} spans master cut at {bad}")

RISER = {"src": "sfx2/risers-01.mp3", "vol": 0.15}
IMPACT = {"src": "sfx2/impact-boom.mp3", "vol": 0.16}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.14}
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}
CLICK = {"src": "sfx2/mouse-click-01.mp3", "vol": 0.12}

CRED = "Made by Google"
CRED_BLOG = "Source: blog.google"


def face(n, zoom="in", **kw):
    s = {"type": "footage", "src": AVATAR, "durationSec": dur(n),
         "from": B[n][0], "focusX": FOCUS_FULL, "zoomDir": zoom}
    s.update(kw)
    return s


def clip(n, name, aid, zoom="in", **kw):
    s = {"type": "footage", "src": f"{C}/{name}.mp4", "durationSec": dur(n),
         "zoomDir": zoom, "credit": CRED, "assetId": aid}
    s.update(kw)
    return s


def card(n, name, aid, aspect, **kw):
    s = {"type": "floatcard", "src": f"{C}/{name}.mp4", "durationSec": dur(n),
         "bg": "gradient", "aspect": aspect, "credit": CRED, "assetId": aid}
    s.update(kw)
    return s


scenes: list[dict] = [
    # HOOK — split: family lineup top / face bottom
    {"type": "split", "durationSec": dur("hook"),
     "topSrc": f"{C}/c-fam.mp4", "topFrom": 0.0, "topFocusX": 0.5,
     "bottomSrc": AVATAR, "bottomFrom": 0.0, "bottomFocusX": FOCUS_SPLIT,
     "credit": CRED, "assetId": "family-lineup",
     "captionBottom": 1000, "sfx": [RISER]},
    clip("hardware", "v-recycled", "recycled-slide", zoom="out", **{"from": 5.0}),
    card("fourpix", "c-colors", "lineup-colors-slide", 900 / 485),
    clip("trackera", "v-tagkeys", "tag-keys-table"),
    card("trackerb", "c-tagfind2", "tag-find-ui", 16 / 9),
    clip("mbg26", "v-droplab", "durability-lab", zoom="out",
         kinetic={"text": "MADE BY GOOGLE 2026", "style": "caps", "at": 0.25, "y": 0.24},
         sfx=[IMPACT]),
    face("matters", zoom="in"),
    clip("p11pricea", "v-p11pro", "p11pro-coral-render"),
    clip("p11priceb", "v-p11pro2", "p11pro-coral-render", zoom="out"),
    clip("cambar", "v-cambar", "camera-bar-macro"),
    clip("sensora", "v-xray2", "teardown-xray", zoom="out"),
    clip("sensorb", "v-xray", "teardown-xray"),
    {"type": "specsheet", "durationSec": dur("light"),
     "kicker": "Pixel 11", "title": "New main sensor",
     "rows": [{"label": "MAIN SENSOR", "value": "48MP"},
              {"label": "LIGHT SENSITIVITY", "value": "+56%", "accent": True}],
     "footnote": "Source: blog.google"},
    clip("displaya", "v-p11front2", "p11-front-pink"),
    clip("displayb", "v-p11front", "p11-front-pink", zoom="out"),
    card("zoom120", "c-zoom120", "zoom-120x-slide", 860 / 520),
    clip("lookat", "v-zoomcity", "zoom-city-demo", captionBottom=260, sfx=[WHOOSH]),
    card("charges", "c-battery", "battery-slide", 940 / 545, **{"from": 3.0}),
    {"type": "statcard", "durationSec": dur("battery"),
     "title": "Pro XL · WIRED CHARGING", "bg": "black",
     "rows": [{"label": "TIME PLUGGED IN", "value": "15 min", "pct": 0.2},
              {"label": "BATTERY GAINED", "value": "15 hr", "pct": 0.92}],
     "footnote": "Source: blog.google"},
    clip("foldlighta", "v-foldstand", "fold-standing"),
    clip("foldlightb", "v-foldhinge", "fold-hinge-macro", zoom="out", **{"from": 0.6}),
    clip("foldthin", "v-foldedge", "fold-hinge-macro"),
    face("durable", zoom="in"),
    face("cracka", zoom="out"),
    face("crackb", zoom="in"),
    {"type": "wordcascade", "durationSec": dur("bridge"), "bg": "cream",
     "words": [{"text": "the part", "style": "caps", "at": 0.2},
               {"text": "NOBODY", "style": "caps", "at": 0.7, "size": 1.5, "accent": True},
               {"text": "noticed", "style": "caps", "at": 1.2}]},
    clip("tensor", "v-tensor", "tensor-g6-macro"),
    clip("compute", "v-tensor2", "tensor-g6-macro", zoom="out"),
    {"type": "chart", "durationSec": dur("faster"),
     "kicker": "Tensor G6 · ON-DEVICE AI", "title": "Gemini Nano, uncorked",
     "bg": "black", "unit": "x",
     "items": [{"label": "AI SPEED", "value": 3.5, "display": "3.5x faster", "highlight": True},
               {"label": "TENSOR G5", "value": 1, "display": "1x",
                "sub": "previous chip"}],
     "source": "blog.google"},
    {"type": "specsheet", "durationSec": dur("energy"),
     "kicker": "EFFICIENCY", "title": "Energy per AI task",
     "rows": [{"label": "Tensor G5", "value": "3.5 units"},
              {"label": "Tensor G6", "value": "1 unit", "accent": True}],
     "footnote": "Source: blog.google"},
    face("titanintro", zoom="in"),
    {"type": "specsheet", "durationSec": dur("titan"),
     "kicker": "SECURITY", "title": "Titan M3",
     "rows": [{"label": "THREAT MODEL", "value": "quantum attacks"},
              {"label": "DEFENSE", "value": "post-quantum crypto", "accent": True},
              {"label": "SECURE BOOT", "value": "yes"}],
     "footnote": "Source: blog.google"},
    face("decade", zoom="out"),
    clip("watch5", "v-watchfilm", "watch-film", **{"from": 1.2}),
    card("gpsa", "c-gpsslide", "gps-route-aerial", 16 / 9),
    card("gpsb", "c-gpsaerial", "gps-route-aerial", 1160 / 720),
    card("insulin", "c-insulin", "watch-insulin-card", 16 / 9),
    card("breathing", "c-breathing", "breathing-emergency", 1240 / 640),
    clip("help", "v-wrist", "watch-wrist-demo", zoom="out", **{"from": 1.5}),
    card("tagintro", "c-tagmacro", "tag-macro", 1150 / 560, sfx=[CLICK]),
    {"type": "specsheet", "durationSec": dur("tagspecs"),
     "kicker": "Pixel Tag", "title": "The $29 tracker",
     "rows": [{"label": "PRICE", "value": "$29", "accent": True},
              {"label": "BODY", "value": "stainless · IP67"},
              {"label": "BATTERY", "value": "1 yr, replaceable"}],
     "footnote": "Source: blog.google"},
    card("tagfindsa", "c-tagfind", "tag-find-ui", 16 / 9),
    {"type": "statcard", "durationSec": dur("tagfindsb"),
     "title": "Find Hub network", "bg": "black",
     "rows": [{"label": "ANDROID DEVICES", "value": "1,000,000,000+", "pct": 1.0,
               "color": "#FFD84D"}],
     "footnote": "Source: blog.google"},
    face("airtag", zoom="in"),
    card("asla", "c-asl", "asl-demo", 880 / 420),
    card("aslb", "c-asl2", "asl-demo", 880 / 420, bg="black"),
    card("watchthis", "c-asl4", "asl-demo", 880 / 420, bg="cream", captionBottom=260),
    {"type": "chart", "durationSec": dur("frames"),
     "kicker": "Magic Capture", "title": "Frames, not luck",
     "bg": "cream",
     "items": [{"label": "FRAMES ANALYZED", "value": 500, "display": "~500"},
               {"label": "SHOTS YOU KEEP", "value": 18, "display": "1", "highlight": True}],
     "source": "9to5Google"},
    {"type": "wordcascade", "durationSec": dur("rambler"), "bg": "black",
     "words": [{"text": "so um basically", "style": "caps", "at": 0.15},
               {"text": "like i was saying", "style": "caps", "at": 0.55},
               {"text": "Rambler", "style": "caps", "at": 1.15, "size": 1.6, "accent": True}]},
    {"type": "promptcard", "durationSec": dur("cleantext"),
     "app": "Gboard", "headline": "CLEAN TEXT",
     "promptText": "Dinner at 7 works — see you there.",
     "bg": "gradient"},
    face("catch", zoom="in"),
    {"type": "priceladder", "durationSec": dur("pricebump"),
     "kicker": "THE CATCH", "title": "Every price, up $100",
     "badge": "+$100", "bg": "black", "stagger": 0.45,
     "rows": [{"label": "Pixel 11", "oldPrice": "$799", "newPrice": "$899"},
              {"label": "Pixel 11 Pro", "oldPrice": "$999", "newPrice": "$1,099"},
              {"label": "Pro XL", "oldPrice": "$1,199", "newPrice": "$1,299"},
              {"label": "Pro Fold", "oldPrice": "$1,799", "newPrice": "$1,899"}],
     "footnote": "Source: blog.google · TechCrunch", "sfx": [GROUND]},
    card("budsa", "c-buds", "buds-slides", 1030 / 545),
    card("budsb", "c-buds2", "buds-slides", 1030 / 545),
    {"type": "checklist", "durationSec": dur("updates"), "bg": "cream",
     "headline": "Every Pixel 11",
     "rows": [{"label": "7 years of updates", "state": "done"},
              {"label": "6 months Google AI Pro (Pro)", "state": "done"}]},
    {"type": "statcard", "durationSec": dur("gigs"),
     "title": "BASE STORAGE", "bg": "black",
     "rows": [{"label": "Pixel 10", "value": "128GB", "pct": 0.5},
              {"label": "Pixel 11", "value": "256GB", "pct": 1.0, "color": "#FFD84D"}],
     "footnote": "Source: blog.google"},
    {"type": "annotatezoom", "durationSec": dur("aug20"),
     "src": f"{A}/receipt-p11-price.png", "srcWidth": 1170, "srcHeight": 1520,
     "bg": "cream", "assetId": "receipt-p11-price", "credit": CRED_BLOG,
     "focus": {"x": 40, "y": 1030, "w": 1080, "h": 380},
     "annotations": [
         {"kind": "underline", "at": 0.5, "x": 905, "y": 1105, "w": 185, "h": 60},
         {"kind": "underline", "at": 1.2, "x": 310, "y": 1320, "w": 260, "h": 62}]},
    {"type": "annotatezoom", "durationSec": dur("nov11"),
     "src": f"{A}/receipt-tag-price.png", "srcWidth": 1170, "srcHeight": 930,
     "bg": "black", "assetId": "receipt-tag-price", "credit": CRED_BLOG,
     "focus": {"x": 40, "y": 400, "w": 1080, "h": 200},
     "annotations": [
         {"kind": "circle", "at": 0.4, "x": 720, "y": 415, "w": 110, "h": 75},
         {"kind": "underline", "at": 1.0, "x": 835, "y": 500, "w": 280, "h": 60}]},
    face("quantuma", zoom="in", sfx=[{"src": "sfx2/risers-01.mp3", "vol": 0.13}]),
    face("quantumb", zoom="out"),
    face("iphone", zoom="in"),
    face("comments", zoom="out"),
]


# ── captions ────────────────────────────────────────────────────────────────
caption_words = normalise_words(words, CANON)


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


FIX = {}

captions = []
for grp in chunk(caption_words):
    text = " ".join(w[2] for w in grp)
    per = [{"t": round(w[0], 2), "text": w[2]} for w in grp]
    for a, b in FIX.items():
        text = text.replace(a, b)
        for p in per:
            p["text"] = p["text"].replace(a, b)
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                     "text": text, "words": [p for p in per if p["text"]]})

music = {
    "src": "music/bed-02.mp3", "from": 8.0,
    "points": [
        {"t": 0.0, "vol": 0.15},
        {"t": B["mbg26"][0], "vol": 0.09},
        {"t": B["lookat"][0], "vol": 0.14},
        {"t": B["charges"][0], "vol": 0.08},
        {"t": B["bridge"][0], "vol": 0.12},
        {"t": B["watch5"][0], "vol": 0.08},
        {"t": B["watchthis"][0], "vol": 0.13},
        {"t": B["catch"][0], "vol": 0.10},
        {"t": B["quantuma"][0], "vol": 0.14},
        {"t": TOTAL - 0.8, "vol": 0.10},
        {"t": TOTAL, "vol": 0.02},
    ],
}

beats = {
    "id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "varun",
    "format": "news", "allowLong": True,
    "allowLongReason": MANIFEST["allowLongReason"],
    "script": SCRIPT, "approval": APPROVAL,
    "audio": AVATAR, "music": music,
    "captionStyle": "nick-display",
    "emphasis": ["$29", "$899", "40%", "56%", "48", "3,600-nit", "120x", "15",
                 "10%", "3x", "G6", "3.5x", "Titan", "quantum", "20%",
                 "insulin", "breathing", "billion", "500", "Rambler", "$100",
                 "7", "256", "August", "November", "iPhone"],
    "scenes": scenes, "captions": captions,
}

total = round(sum(s["durationSec"] for s in scenes), 2)
print(f"\nscenes {total:.2f}s vs reel {TOTAL:.2f}s (delta {total - TOTAL:+.2f}s)")

clip_durations = {}
for sc in scenes:
    for key in ("src", "topSrc"):
        src = sc.get(key)
        if src and src.endswith(".mp4") and "avatar-master" not in src:
            p = ROOT / "public" / src
            if p.exists() and src not in clip_durations:
                d = float(subprocess.check_output(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=nw=1:nk=1", str(p)]).strip())
                clip_durations[src] = d

try:
    for w in check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST,
                         clip_durations=clip_durations, vo_words=[(t, s_, e_) for s_, e_, t in caption_words]):
        print(f"  warning: {w}")
    print("GATES: PASSED")
except GateError as e:
    raise SystemExit(f"GATES FAILED — beat sheet NOT written\n{e}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
