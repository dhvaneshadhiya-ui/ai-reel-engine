#!/usr/bin/env python3
"""Beat sheet for grok-bot (editorial).

Source is x.ai's own launch film (via the @bot X post) plus the announcement
page. Tier-1 official source, so per RULES.md the claims are stated flat and
attributed once — no stacked hedging.

Treatment split, verified on frames: the film's UI/overlay shots lose their
copy to a 9:16 crop, so they run as framed 16:9 floatcards; the live-action
people shots survive a centre crop and run full-bleed.
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

SLUG = "grok-bot"
ROOT = Path(__file__).resolve().parent.parent
A, C = f"assets/{SLUG}", f"assets/{SLUG}/clips"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master-169.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
LOGO = json.loads((ROOT / "public/assets/logos/grok.paths.json").read_text())
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
    """Each region ends on the phrase its visuals are ABOUT, then divides that
    span among its own visuals (never the neighbour's). See RULES.md §4."""
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


RISER = {"src": "sfx2/risers-01.mp3", "vol": 0.15}
IMPACT = {"src": "sfx2/impact-boom.mp3", "vol": 0.16}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.14}
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}
CRED, W16 = "SpaceXAI", 16 / 9
hl = lambda lines, y=0.12, theme="light": {"lines": lines, "y": y, "theme": theme,
                                           "align": "center"}


def card(name, headline=None, sfx=None):
    def b(t0, d):
        s = {"type": "floatcard", "src": f"{C}/{name}.mp4", "bg": "gradient",
             "aspect": W16, "durationSec": d, "credit": CRED,
             "assetId": f"clip-{name}"}
        if headline: s["headline"] = headline
        if sfx: s["sfx"] = sfx
        return s
    return b


def shot(name, zoom="in", cb=None, sfx=None):
    def b(t0, d):
        s = {"type": "footage", "src": f"{C}/{name}.mp4", "durationSec": d,
             "zoomDir": zoom, "credit": CRED, "assetId": f"clip-{name}"}
        if cb: s["captionBottom"] = cb
        if sfx: s["sfx"] = sfx
        return s
    return b


def face(headline=None, cb=300):
    def b(t0, d):
        s = {"type": "footage", "src": AVATAR, "durationSec": d,
             "from": round(t0, 2), "focusX": FOCUS_FULL, "captionBottom": cb}
        if headline: s["headline"] = headline
        return s
    return b


def mg(spec, sfx=None):
    def b(t0, d):
        s = dict(spec, durationSec=d)
        if sfx: s["sfx"] = sfx
        return s
    return b


def page(label, head, accent=False, aid=None, src="src-hero"):
    def b(t0, d):
        s = {"type": "floatcard", "src": f"{C}/{src}.png", "bg": "gradient",
             "aspect": 1200 / 1500 if src == "src-hero" else 1200 / 1560,
             "durationSec": d, "credit": "x.ai",
             "headline": hl([{"text": label, "kind": "label", "at": 0.1},
                             {"text": head, "kind": "headline", "at": 0.4,
                              "accent": accent}], y=0.09, theme="dark")}
        if aid: s["assetId"] = aid
        return s
    return b


def readalong(t0, d):
    """The official lede, marked as the VO says it. Text-dense, portrait,
    VO tracks it verbatim — the documented YES case for sourceread."""
    return {
        "type": "sourceread", "durationSec": d,
        "src": f"{C}/src-hero.png", "srcWidth": 1200, "srcHeight": 1500,
        "credit": "x.ai — the official announcement", "follow": False,
        "lines": [
            {"at": 0.15, "x": 57, "y": 628, "w": 1080, "h": 54},
            {"at": 0.95, "x": 57, "y": 713, "w": 1055, "h": 54},
            {"at": 1.70, "x": 57, "y": 798, "w": 890, "h": 54},
        ],
        "assetId": "src-hero",
    }


def beta_badge(t0, d):
    return {
        "type": "sourceread", "durationSec": d,
        "src": f"{C}/src-hero.png", "srcWidth": 1200, "srcHeight": 1500,
        "credit": "x.ai", "follow": False, "tint": "#FFD2A8",
        "lines": [{"at": 0.2, "x": 845, "y": 462, "w": 232, "h": 66}],
    }


def logo_hook(t0, d):
    return {
        "type": "logoassemble", "durationSec": d, "hideCaptions": True,
        "viewBox": LOGO["viewBox"], "paths": LOGO["paths"],
        "size": 1050, "y": 0.51, "bg": "cream", "fillOverride": "#141414",
        "label": "GROK BOT · SPACEXAI", "labelAt": 0.35,
        "headline": hl([{"text": "early beta", "kind": "label", "at": 0.12}], y=0.07),
        "sfx": [dict(RISER, at=0.0), dict(IMPACT, at=0.35)],
    }


def split_hook(t0, d):
    return {
        "type": "split", "durationSec": d, "captionBottom": 1000,
        "topSrc": f"{C}/v-office.mp4", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": round(t0, 2), "bottomFocusX": FOCUS_SPLIT,
        "credit": CRED, "assetId": "clip-v-office",
    }


SPEC_HOW = {
    "type": "specsheet", "bgSrc": f"{C}/v-wide.mp4", "bgFrom": 0.0,
    "kicker": "how it reaches your tools", "title": "No API required",
    "columns": ["GROK BOT"],
    "rows": [{"label": "Formal API", "values": ["not needed"]},
             {"label": "MCP connector", "values": ["not needed"]},
             {"label": "Signs in and drives the UI", "values": ["yes"], "accent": True}],
    "footnote": "x.ai, Aug 11, 2026",
}
CHART_PRICE = {
    "type": "chart", "kicker": "monthly, per user", "title": "The way in",
    "unit": "$", "max": 300, "bg": "black",
    "items": [{"label": "SuperGrok Heavy", "value": 300, "display": "300",
               "sub": "SpaceXAI's own tier"},
              {"label": "Cursor Ultra", "value": 200, "display": "200", "sub": "per month"},
              {"label": "Cursor Premium Teams", "value": 120, "display": "120",
               "sub": "per seat", "highlight": True}],
    "source": "implicator.ai · VentureBeat",
}
SPEC_CURSOR = {
    "type": "specsheet", "kicker": "the cheapest door", "title": "It runs on Cursor",
    "columns": ["ROLE"],
    "rows": [{"label": "Lowest price tier", "values": ["Cursor Teams"]},
             {"label": "Signs you in", "values": ["Cursor auth"], "accent": True}],
    "footnote": "kingy.ai",
}
CHECK_ELIGIBLE = {
    "type": "checklist", "bg": "gradient", "headline": "Who does NOT get it",
    "rows": [{"label": "Free Grok", "state": "no"},
             {"label": "Standard SuperGrok", "state": "no"},
             {"label": "Cursor Pro", "state": "no"}],
}
WC_UNKNOWN = {
    "type": "wordcascade", "bg": "cream", "captionTheme": "dark",
    "words": [{"text": "credential handling?", "style": "serif", "at": 0.1, "size": 1.15},
              {"text": "permission scope?", "style": "serif", "at": 0.85, "size": 1.1},
              {"text": "audit records?", "style": "caps", "at": 1.6, "size": 1.2}],
}
CHECK_PLATFORMS = {
    "type": "checklist", "bg": "gradient", "headline": "Where it runs today",
    "rows": [{"label": "macOS", "state": "done"}, {"label": "Windows", "state": "done"},
             {"label": "Linux", "state": "done"}, {"label": "iOS", "state": "done"},
             {"label": "Android — coming soon", "state": "q"}],
}

regions = [
    ("do the work",        [logo_hook, card("w-hired"), card("w-icons")]),
    ("live yesterday",     [page("reported", "x.ai · Aug 11", aid="src-hero"),
                        card("w-list")]),
    ("official line",      [split_hook]),
    ("alwayson agents",    [readalong]),
    ("keep working 247",   [card("w-meet", sfx=[dict(WHOOSH, at=0.0)]), shot("v-people"),
                        card("w-ui4")]),
    ("computer is real",   [face()]),
    ("in the cloud",       [card("w-code", sfx=[dict(WHOOSH, at=0.0)]), card("w-ui1")]),
    ("close your laptop",  [shot("v-desk", zoom="out")]),
    ("actually matters",   [face()]),
    ("no mcp",             [card("w-ui2"), card("w-ui5"),
                        mg(SPEC_HOW, sfx=[dict(GROUND, at=0.3)])]),
    ("person would",       [card("w-ui3"), card("w-ui6")]),
    ("like a colleague",   [shot("v-woman")]),
    ("things done",        [shot("v-wide")]),
    ("itself next time",   [card("w-teach"), card("w-emails"), shot("v-desk2")]),
    ("specialists underneath", [card("w-phone"), shot("v-talk")]),
    ("judgment calls",     [card("w-chat"), card("w-bots")]),
    ("nobody noticed",     [face()]),
    ("actually get in",    [shot("v-pair")]),
    ("300 a month",        [mg(CHART_PRICE, sfx=[dict(IMPACT, at=0.3)])]),
    ("120 per seat",       [card("w-charts"), shot("v-guy"), card("w-draft"),
                        card("w-tasks")]),
    ("signs you in",       [card("w-brand"), mg(SPEC_CURSOR), shot("v-sofa"), face()]),
    ("does not either",    [mg(CHECK_ELIGIBLE), shot("v-ipad")]),
    ("early beta",         [beta_badge, page("the badge on the page", "EARLY BETA", accent=True, src="src-body")]),
    ("logins to",          [face()]),
    ("audit records",      [mg(WC_UNKNOWN, sfx=[dict(GROUND, at=1.6)]), shot("v-team2"), face()]),
    ("android is coming",  [card("w-laptop"),
                        mg(CHECK_PLATFORMS, sfx=[dict(GROUND, at=0.3)]),
                        card("w-end")]),
    ("your passwords",     [shot("v-women"), face(headline=hl([
        {"text": "it signs in as you", "kind": "label", "at": 0.15},
        {"text": "would you hand it", "kind": "headline", "at": 0.5},
        {"text": "your passwords?", "kind": "headline", "at": 0.8, "accent": True},
    ], y=0.07))]),
]

placed = region_bounds(regions, TOTAL)
scenes = [b(s0, round(s1 - s0, 2)) for (_, s0, s1, b) in placed]
R = {ph: (s0, s1) for (ph, s0, s1, _) in placed}
print(f"  {len(regions)} regions -> {len(scenes)} scenes")
long = [(ph, e - s) for ph, s, e, _ in placed if e - s > 2.55]
for ph, d in long:
    print(f"    long: {ph!r} {d:.2f}s")


def chunk(ws, size=3):
    out, buf = [], []
    for (s, e, w) in ws:
        buf.append((s, e, w))
        if len(buf) >= size or (re.search(r"[.,!?—:;]$", w) and len(buf) >= 2):
            out.append(buf); buf = []
    if buf: out.append(buf)
    return out


# display-only fixes for whisper mishears; timings untouched
FIX = {"bought": "Bot", "chief of staff bought": "chief of staff Bot",
       "24 -7": "24/7", "24-7": "24/7"}
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
    {"t": R["official line"][1], "vol": 0.15},
    {"t": R["alwayson agents"][1], "vol": 0.08},
    {"t": R["nobody noticed"][0], "vol": 0.07},
    {"t": R["300 a month"][0], "vol": 0.14},
    {"t": R["does not either"][1], "vol": 0.09},
    {"t": R["audit records"][0], "vol": 0.13},
    {"t": TOTAL - 0.9, "vol": 0.13}, {"t": TOTAL, "vol": 0.02}]}

beats = {"id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "editorial",
         "audio": AVATAR, "music": music, "captionStyle": "word-reveal",
         "emphasis": ["Grok", "Bot", "Bots", "SpaceXAI", "Cursor", "MCP", "API",
                      "300", "200", "120", "beta", "macOS", "iOS", "24/7"],
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
