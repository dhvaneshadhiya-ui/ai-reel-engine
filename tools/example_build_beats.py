#!/usr/bin/env python3
"""Beat sheet for kleo (varun-mayya, VibeVoice) — Cameron Trew nerve story.
First reel through the Scout->Director pipeline: every beat pre-bound in
scripts/kleo.md to manifest assets or MG specs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = "assets/kleo"
C = f"{A}/clips"
OUT = ROOT / "src/beats/kleo.json"
AVATAR = f"{A}/avatar-master-169.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())

raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())["words"]
words = [(w["start"], w["end"], w["word"].strip()) for w in raw]
TOTAL = round(words[-1][1] + 0.3, 2)
print(f"{len(words)} words, {TOTAL}s")


def css_pos(fx, iw, ih, cw, ch):
    s = max(cw / iw, ch / ih); w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


FOCUS_FULL = css_pos(FACE_X, 1920, 1080, 1080, 1920)
FOCUS_SPLIT = css_pos(FACE_X, 1920, 1080, 1080, 960)


def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def find(phrase):
    t = norm(phrase).split(); stream = [norm(w[2]) for w in words]
    for i in range(len(stream) - len(t) + 1):
        if stream[i:i+len(t)] == t:
            return words[i+len(t)-1][1]
    raise SystemExit(f"NOT FOUND: {phrase!r}")


anchors = [
    ("hook1",   "childhood bedroom"),
    ("hook2",   "62 000 a month"),
    ("nameit",  "linkedin posts"),
    ("cnd",     "season desist"),
    ("rebuild", "cloud code"),
    ("pricing", "in 4 days"),
    ("wrong",   "gets wrong"),
    ("distrib", "was a distribution"),
    ("honest",  "one engineer"),
    ("helped",  "they helped"),
    ("credit",  "bet on himself"),
    ("nerve",   "never did"),
    ("cta",     "yourselves"),
]
bounds, prev = [], 0.0
for name, ph in anchors:
    e = round(find(ph) + 0.12, 2); bounds.append((name, prev, e)); prev = e
bounds[-1] = (bounds[-1][0], bounds[-1][1], TOTAL)
B = {n: (s, e) for n, s, e in bounds}
for n, s, e in bounds: print(f"{n:8s} {s:6.2f}-{e:6.2f} ({e-s:.2f}s)")
dur = lambda n: round(B[n][1] - B[n][0], 2)

RISER = {"src": "sfx2/riser-sweep.wav", "vol": 0.16}
IMPACT = {"src": "sfx2/impact-deep.mp3", "vol": 0.17}
IMPACTB = {"src": "sfx2/impact-cool.mp3", "vol": 0.18}
SLIDE = {"src": "sfx2/tech-slide.mp3", "vol": 0.12}
POPS = {"src": "sfx2/pops.mp3", "vol": 0.13}


def hl(lines, y=0.12, theme="light", align="center"):
    return {"lines": lines, "y": y, "theme": theme, "align": align}


scenes = [
    {  # hook1 — London towers / face + serif build
        "type": "split", "durationSec": dur("hook1"), "captionBottom": 1000,
        "topSrc": f"{C}/canary-hook.mp4", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": 0.0, "bottomFocusX": FOCUS_SPLIT,
        "headline": hl([
            {"text": "a senior engineer in London", "kind": "label", "at": 0.2},
            {"text": "traded his flat for his\nchildhood bedroom", "kind": "headline", "at": 0.75},
        ], y=0.33),
        "sfx": [dict(RISER, at=0.0), dict(IMPACT, at=0.75)],
    },
    {  # hook2 — the $62k receipt
        "type": "receipt", "durationSec": dur("hook2"), "backdrop": "black",
        "src": f"{C}/ih-receipt.png", "srcWidth": 1100, "srcHeight": 640,
        "credit": "Indie Hackers",
        "highlights": [
            {"at": 0.1, "x": 28, "y": 140, "w": 350, "h": 100},
            {"at": 1.0, "x": 28, "y": 515, "w": 260, "h": 75},
        ],
        "sfx": [dict(SLIDE, at=0.0), dict(POPS, at=1.0)],
    },
    {  # nameit — kleo.so hero (clean, branded)
        "type": "receipt", "durationSec": dur("nameit"), "backdrop": "black",
        "src": f"{C}/kleo-hero.png", "srcWidth": 1100, "srcHeight": 730,
        "credit": "kleo.so",
        "highlights": [
            {"at": 0.15, "x": 420, "y": 90, "w": 265, "h": 50},
            {"at": 1.2, "x": 170, "y": 140, "w": 770, "h": 140},
        ],
        "sfx": [dict(SLIDE, at=0.0), dict(POPS, at=1.2)],
    },
    {  # cnd — 60k users -> cease & desist
        "type": "wordcascade", "bg": "cream", "durationSec": dur("cnd"),
        "words": [
            {"text": "60,000 users.", "style": "serif", "at": 0.2},
            {"text": "then:", "style": "caps", "at": 1.1, "size": 0.7},
            {"text": "a cease & desist.", "style": "serif", "at": 1.6, "size": 1.15},
        ],
        "sfx": [dict(POPS, at=0.2), dict(IMPACTB, at=1.6)],
    },
    {  # rebuild — Kleo app in a framed window card
        "type": "floatcard", "src": f"{C}/kleo-card1.mp4", "bg": "gradient",
        "durationSec": dur("rebuild"), "credit": "kleo.so",
        "headline": hl([
            {"text": "rebuilt from scratch —", "kind": "label", "at": 0.15},
            {"text": "in 4 weeks", "kind": "headline", "at": 0.55},
        ], y=0.13, theme="dark"),
        "sfx": [dict(SLIDE, at=0.0)],
    },
    {  # pricing — spec sheet with UNITS
        "type": "specsheet", "durationSec": dur("pricing"),
        "bgSrc": f"{C}/canary-nerve.mp4",
        "kicker": "beta launch", "title": "Sold out",
        "columns": ["Price /mo", "Spots", "Sold in"],
        "rows": [
            {"label": "Beta 1", "values": ["$59", "500", "4 days"], "accent": True},
            {"label": "Beta 2", "values": ["$79", "500", "9 days"]},
            {"label": "Standard", "values": ["$99", "—", "live"]},
        ],
        "footnote": "source: Indie Hackers interview",
        "sfx": [dict(SLIDE, at=0.0), dict(POPS, at=0.6), dict(IMPACTB, at=1.3)],
    },
    {  # wrong — facecam bridge
        "type": "footage", "src": AVATAR, "durationSec": dur("wrong"),
        "from": B["wrong"][0], "focusX": FOCUS_FULL,
    },
    {  # distrib — the honesty numbers, black cascade
        "type": "wordcascade", "bg": "black", "durationSec": dur("distrib"),
        "words": [
            {"text": "he wasn't solo.", "style": "serif", "at": 0.2},
            {"text": "3 co-founders.", "style": "caps", "at": 1.2, "size": 0.9},
            {"text": "480,000 followers.", "style": "caps", "at": 2.1, "size": 0.9},
        ],
        "sfx": [dict(POPS, at=0.2), dict(POPS, at=1.2), dict(IMPACTB, at=2.1)],
    },
    {  # honest — facecam + infocard (the one-engineer point)
        "type": "footage", "src": AVATAR, "durationSec": dur("honest"),
        "from": B["honest"][0], "focusX": FOCUS_FULL,
        "infocard": {"heading": "The code?", "body": "Every single line — one engineer.", "at": 0.3},
    },
    {  # helped — the generated post, framed
        "type": "floatcard", "src": f"{C}/kleo-card2.mp4", "bg": "gradient",
        "durationSec": dur("helped"),
        "headline": hl([
            {"text": "credit the AI tools —", "kind": "label", "at": 0.15},
            {"text": "sure, they helped", "kind": "subtitle", "at": 0.6, "accent": True},
        ], y=0.13, theme="dark"),
        "sfx": [dict(POPS, at=0.1)],
    },
    {  # credit — facecam (the bedroom line, pure)
        "type": "footage", "src": AVATAR, "durationSec": dur("credit"),
        "from": B["credit"][0], "focusX": FOCUS_FULL,
    },
    {  # nerve — serif reveal over dusk London
        "type": "footage", "src": f"{C}/canary-nerve.mp4", "durationSec": dur("nerve"),
        "zoomDir": "in",
        "headline": hl([
            {"text": "the tools got cheap.", "kind": "label", "at": 0.15},
            {"text": "the nerve\nnever did", "kind": "headline", "at": 0.6},
        ], y=0.38),
        "sfx": [dict(IMPACT, at=0.6)],
    },
    {  # cta — facecam + serif
        "type": "footage", "src": AVATAR, "durationSec": dur("cta"),
        "from": B["cta"][0], "focusX": FOCUS_FULL,
        "headline": hl([
            {"text": "would you move back home", "kind": "label", "at": 0.15},
            {"text": "to bet on yourself?", "kind": "headline", "at": 0.5},
        ], y=0.10),
    },
]


def chunk_caps(ws):
    caps, chunk, cs = [], [], None
    for (s, e, w) in ws:
        if cs is None: cs = s
        chunk.append(w)
        if len(chunk) >= 3 or (re.search(r"[.,!?—:;]$", w) and len(chunk) >= 2):
            caps.append({"start": round(cs, 2), "end": round(e, 2), "text": " ".join(chunk)})
            chunk, cs = [], None
    if chunk: caps.append({"start": round(cs, 2), "end": round(ws[-1][1], 2), "text": " ".join(chunk)})
    return caps


captions = chunk_caps(words)
FIX = {"Cameron True": "Cameron Trew", "Cleo": "Kleo", "and AI tool": "an AI tool",
       "season desist": "cease-and-desist", "Cloud Code": "Claude Code",
       "So it's sold out": "Sold out", "That was a distribution": "That was the distribution",
       "yourselves?": "yourself?", "62 ,000": "62,000", "60 ,000": "60,000",
       "co -founders": "co-founders", "$62 ,000": "$62,000"}
for c in captions:
    for a, b in FIX.items():
        c["text"] = c["text"].replace(a, b)

music = {
    "src": "music/bed-184.mp3", "from": 32.0,
    "points": [
        {"t": 0.0, "vol": 0.15}, {"t": B["hook1"][1], "vol": 0.15},
        {"t": B["hook1"][1] + 0.6, "vol": 0.08},
        {"t": B["pricing"][0], "vol": 0.10}, {"t": B["pricing"][1], "vol": 0.10},
        {"t": B["honest"][0], "vol": 0.07},
        {"t": B["nerve"][0], "vol": 0.14}, {"t": B["nerve"][1], "vol": 0.14},
        {"t": B["cta"][0], "vol": 0.10},
        {"t": TOTAL - 0.8, "vol": 0.12}, {"t": TOTAL, "vol": 0.02},
    ],
}
beats = {
    "id": "kleo", "fps": 30, "width": 1080, "height": 1920,
    "audio": AVATAR, "music": music, "captionStyle": "chip-small",
    "emphasis": ["$62,000", "62,000", "90 days", "Kleo", "60,000", "4 weeks",
                 "$59", "500", "4 days", "one engineer", "nerve", "Cameron Trew"],
    "scenes": scenes, "captions": captions,
}
print(f"scenes {sum(s['durationSec'] for s in scenes):.2f}s vs audio {TOTAL:.2f}s")
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
