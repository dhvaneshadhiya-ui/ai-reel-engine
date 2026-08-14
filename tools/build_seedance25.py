#!/usr/bin/env python3
"""Beat sheet for seedance-25 (varun-mayya).

Every scene binds to an id in public/assets/seedance-25/manifest.json or to an
MG component. Scene durations are anchored to whisper word timings so cuts
land on the spoken word, and the scene sum is forced to equal the VO length.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
A = "assets/seedance-25"
C = f"{A}/clips"
OUT = ROOT / "src/beats/seedance-25.json"
AVATAR = f"{A}/avatar-master-169.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
LOGO = json.loads((ROOT / "public/assets/logos/tiktok.paths.json").read_text())

raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())
words = [(w["start"], w["end"], w["word"].strip())
         for s in raw["segments"] for w in s["words"]]

# merge whisper's hyphen fragments ("re" + "-staff") — universal rule
merged = []
for st, en, tx in words:
    if tx.startswith("-") and merged:
        p = merged[-1]
        merged[-1] = (p[0], en, p[2] + tx)
    else:
        merged.append((st, en, tx))
words = merged

TOTAL = round(words[-1][1] + 0.35, 2)   # reel ends <=0.4s after final word
print(f"{len(words)} words, VO ends {words[-1][1]:.2f}s, reel {TOTAL:.2f}s")


def css_pos(fx, iw, ih, cw, ch):
    s = max(cw / iw, ch / ih)
    w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


FOCUS_FULL = css_pos(FACE_X, 1920, 1080, 1080, 1920)
FOCUS_SPLIT = css_pos(FACE_X, 1920, 1080, 1080, 960)
print(f"face-x {FACE_X} -> focus full {FOCUS_FULL}, split {FOCUS_SPLIT}")


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
    ("hook",      "owns tiktok"),
    ("jelly",     "generates 30 seconds"),
    ("porthole",  "its own soundtrack"),
    ("glass",     "single pass"),
    ("keynote",   "seedense 2 5"),
    ("timeline",  "last friday"),
    ("cap15",     "at 15 seconds"),
    ("spec1",     "around 10"),
    ("forest",    "one runs 30"),
    ("clouds",    "then extends"),
    ("face1",     "nobody noticed"),
    ("refsfan",   "in one job"),
    ("spec2",     "10 audio tracks"),
    ("ballroom",  "three clips"),
    ("face2",     "real unlock"),
    ("reddress",  "to the beat"),
    ("lipen",     "syncs the lips"),
    ("compare",   "dozen languages"),
    ("lipjp",     "same shot"),
    ("face3",     "benchmark number"),
    ("cascade",   "they chose"),
    ("debris",    "one pass with sound"),
    ("arch",      "whole ad"),
    ("cta",       "clients brief"),
]

bounds, prev = [], 0.0
for name, ph in anchors:
    e = round(find(ph) + 0.12, 2)
    bounds.append((name, prev, e))
    prev = e
bounds[-1] = (bounds[-1][0], bounds[-1][1], TOTAL)
B = {n: (s, e) for n, s, e in bounds}
for n, s, e in bounds:
    flag = "  <-- LONG" if (e - s) > 2.7 and n not in ("porthole",) else ""
    print(f"  {n:9s} {s:6.2f}-{e:6.2f} ({e - s:.2f}s){flag}")


def dur(n):
    return round(B[n][1] - B[n][0], 2)


RISER = {"src": "sfx2/risers-01.mp3", "vol": 0.15}
IMPACT = {"src": "sfx2/impact-boom.mp3", "vol": 0.16}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.14}
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}


def hl(lines, y=0.12, theme="light", align="center"):
    return {"lines": lines, "y": y, "theme": theme, "align": align}


CREDIT = "@Reel Rook · Volcano Engine FORCE 2026"

scenes = [
    {   # 1 hook — the household-recognisable mark, animated, on cream.
        # NOT BrandHook: its title is fixed at 188px with no auto-fit, and
        # "SEEDANCE 2.5" overflows 1080px, clipping the mark off-frame and
        # cutting the word at both edges. STYLE-RULES forbids changing the
        # engine to make a reel work, so the treatment changes instead.
        "type": "logoassemble", "durationSec": dur("hook"), "hideCaptions": True,
        "viewBox": LOGO["viewBox"], "paths": LOGO["paths"],
        # mark runs LARGE: at size 620 the frame linted 74% flat, over the
        # 55% hook ceiling. The ledger also wants the subject brand to be the
        # centre of attraction, so the fix is a bigger mark, not filler type.
        "size": 1000, "y": 0.51, "bg": "cream",
        "fillOverride": "#FF0050",
        "label": "BYTEDANCE", "labelAt": 0.3,
        # the top band would otherwise sit empty — hard fail in the first 2s
        # (STYLE-RULES 2026-08-04). This also completes the sound-off test:
        # TikTok's owner → Seedance 2.5, in one frame.
        "headline": hl([
            {"text": "SEEDANCE 2.5", "kind": "headline", "at": 0.12, "accent": True},
        ], y=0.07),
        "sfx": [dict(RISER, at=0.0), dict(IMPACT, at=0.3)],
    },
    {   # 2 split hook — face on screen at 1.3s (rule: face by second 2)
        "type": "split", "durationSec": dur("jelly"), "captionBottom": 1000,
        "topSrc": f"{C}/jellyfish.mp4", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": 0.0, "bottomFocusX": FOCUS_SPLIT,
        # no headline here: the hook card above already names the product, and
        # repeating it back-to-back is redundant. Chips carry this beat.
        "credit": CREDIT, "assetId": "clip-jellyfish",
    },
    {   # 3 porthole — payoff frame, plays clean (rule 7)
        "type": "footage", "src": f"{C}/porthole-girl.mp4", "durationSec": dur("porthole"),
        "zoomDir": "out", "captionBottom": 300, "assetId": "clip-porthole-girl",
    },
    {   # 4 stained glass — still inside the SAME continuous 30s generation
        "type": "footage", "src": f"{C}/stained-glass.mp4", "durationSec": dur("glass"),
        "zoomDir": "in", "assetId": "clip-stained-glass",
    },
    {   # 5 keynote slide — framed 16:9, never full-bleed (rule 3)
        # cropped to 1920x648 (aspect 2.963): the source frame carried the
        # creator's PiP webcam at x 89-357 / y 714-960 — cropping the bottom
        # band removes it while keeping every line of slide text uncut.
        "type": "floatcard", "src": f"{C}/keynote-slide.jpg", "bg": "gradient",
        "aspect": 2.963,
        "durationSec": dur("keynote"), "credit": "Volcano Engine FORCE 2026",
        "assetId": "card-keynote",
        "headline": hl([
            {"text": "ByteDance", "kind": "label", "at": 0.12},
            {"text": "Seedance 2.5", "kind": "headline", "at": 0.45, "accent": True},
        ], y=0.11, theme="dark"),
        "sfx": [dict(WHOOSH, at=0.0)],
    },
    {   # 6 timeline — announced -> shipped -> API, all sourced dates
        "type": "timeline", "durationSec": dur("timeline"),
        "kicker": "2026", "title": "Shipped in stages",
        "bgSrc": f"{C}/paramedics.mp4", "bgFrom": 0.0,
        "items": [
            {"date": "Jun 23", "name": "Announced", "sub": "Volcano Engine FORCE", "at": 0.12, "minor": True},
            {"date": "Jul 31", "name": "Creator apps", "sub": "Jimeng · Doubao", "at": 0.62},
            {"date": "Aug 7", "name": "Developer API", "sub": "public", "at": 1.12, "accent": "#FFD84D"},
        ],
        "sfx": [dict(GROUND, at=1.12)],
    },
    {   # 7 the doubling, as animated bars with count-ups
        "type": "chart", "durationSec": dur("cap15"),
        "kicker": "one generation", "title": "How long a clip",
        "unit": "sec", "max": 30, "bg": "black",
        "items": [
            {"label": "Seedance 2.0", "value": 15, "display": "15", "sub": "previous"},
            {"label": "Seedance 2.5", "value": 30, "display": "30", "sub": "now", "highlight": True},
        ],
        "source": "ByteDance launch specs",
    },
    {   # 8 spec sheet — competitor comparison WITH UNITS (rule 6)
        "type": "specsheet", "durationSec": dur("spec1"),
        "bgSrc": f"{C}/debris-bw.mp4", "bgFrom": 0.0,
        "kicker": "one generation", "title": "How long a clip",
        "columns": ["MAX LENGTH", "NATIVE AUDIO"],
        "rows": [
            {"label": "Seedance 2.0", "values": ["15 sec", "yes"]},
            {"label": "Gemini Omni Flash", "values": ["~10 sec", "yes"]},
            {"label": "Seedance 2.5", "values": ["30 sec", "yes"], "accent": True},
        ],
        # no cue: scenes 05-07 are three data screens in a row and a cue on
        # each reads as busy. The timeline's Aug-7 landing carries the block.
        "footnote": "ByteDance launch specs · the-decoder, Aug 2026",
    },
    {   # 6 forest stream
        "type": "footage", "src": f"{C}/forest-stream.mp4", "durationSec": dur("forest"),
        "zoomDir": "in", "assetId": "clip-forest-stream",
    },
    {   # 7 clouds -> window montage
        "type": "footage", "src": f"{C}/clouds-plane.mp4", "durationSec": dur("clouds"),
        "zoomDir": "out", "assetId": "clip-clouds-plane",
    },
    {   # 8 facecam — the bridge
        "type": "footage", "src": AVATAR, "durationSec": dur("face1"),
        "from": B["face1"][0], "focusX": FOCUS_FULL, "captionBottom": 300,
    },
    {   # 9 the reference fan, in the real UI
        "type": "footage", "src": f"{C}/refs-fan.mp4", "durationSec": dur("refsfan"),
        "zoomDir": "in", "credit": CREDIT, "assetId": "clip-refs-fan",
        "sfx": [dict(WHOOSH, at=0.0)],
    },
    {   # 10 spec sheet — references per job, 2.0 vs 2.5
        "type": "specsheet", "durationSec": dur("spec2"),
        "bgSrc": f"{C}/champagne.mp4", "bgFrom": 0.0,
        "kicker": "references accepted", "title": "In a single job",
        "columns": ["2.0", "2.5"],
        "rows": [
            {"label": "Images", "values": ["9", "30"]},
            {"label": "Video clips", "values": ["3", "10"]},
            {"label": "Audio tracks", "values": ["0", "10"], "accent": True},
        ],
        "footnote": "50 references total · morphic.com",
        "sfx": [dict(IMPACT, at=1.1)],
    },
    {   # 11 the result those references produced
        "type": "footage", "src": f"{C}/ballroom-group.mp4", "durationSec": dur("ballroom"),
        "zoomDir": "in", "credit": CREDIT, "assetId": "clip-ballroom-group",
    },
    {   # 12 facecam pop — the opinion
        "type": "footage", "src": AVATAR, "durationSec": dur("face2"),
        "from": B["face2"][0], "focusX": FOCUS_FULL, "captionBottom": 300,
    },
    {   # 13 dance cut on the music
        "type": "footage", "src": f"{C}/red-dress.mp4", "durationSec": dur("reddress"),
        "zoomDir": "out", "credit": CREDIT, "assetId": "clip-red-dress",
    },
    {   # 14 english lip-sync
        "type": "footage", "src": f"{C}/lipsync-en.mp4", "durationSec": dur("lipen"),
        "zoomDir": "in", "captionBottom": 560, "assetId": "clip-lipsync-en",
    },
    {   # 15 NEW TREATMENT — same shot, two languages, side by side
        "type": "comparesplit", "durationSec": dur("compare"),
        "leftSrc": f"{C}/lipsync-en.mp4", "rightSrc": f"{C}/lipsync-jp.mp4",
        "leftLabel": "ENGLISH", "rightLabel": "日本語",
        "topText": "ONE SHOT",
        "finalText": "SAME TAKE → NEW VOICE, NEW LIPS",
        "sfx": [dict(GROUND, at=0.2)],
    },
    {   # 16 japanese lip-sync
        "type": "footage", "src": f"{C}/lipsync-jp.mp4", "durationSec": dur("lipjp"),
        "zoomDir": "out", "captionBottom": 560, "assetId": "clip-lipsync-jp",
    },
    {   # 17 facecam — the honesty beat is an on-camera opinion (astra rule)
        "type": "footage", "src": AVATAR, "durationSec": dur("face3"),
        "from": B["face3"][0], "focusX": FOCUS_FULL, "captionBottom": 300,
    },
    {   # 18 what is NOT known
        "type": "wordcascade", "bg": "cream", "durationSec": dur("cascade"),
        "captionTheme": "dark",
        "words": [
            {"text": "no published benchmark.", "style": "serif", "at": 0.15},
            {"text": "no third-party eval.", "style": "serif", "at": 0.95, "size": 0.95},
            {"text": "not yet.", "style": "caps", "at": 1.7, "size": 1.1},
        ],
        "sfx": [dict(GROUND, at=1.7)],
    },
    {   # 21 spectacle — one pass, with sound
        "type": "footage", "src": f"{C}/debris-bw.mp4", "durationSec": dur("debris"),
        "zoomDir": "in", "credit": CREDIT, "assetId": "clip-debris-bw",
    },
    {   # 22 the architectural viz — this one already looks like a commercial
        "type": "footage", "src": f"{C}/arch-aerial.mp4", "durationSec": dur("arch"),
        "zoomDir": "out", "credit": CREDIT, "assetId": "clip-arch-aerial",
    },
    {   # 23 CTA
        "type": "footage", "src": AVATAR, "durationSec": dur("cta"),
        "from": B["cta"][0], "focusX": FOCUS_FULL,
        # OUTRO TYPE (user note 2026-08-11): the label is 46px uppercase with
        # letterSpacing 2 — anything past ~30 characters wraps and orphans a
        # word ("...WITH / SOUND."). Keep it to one line, and split the
        # question so the payoff half carries the accent colour instead of
        # sitting as one flat white block.
        "headline": hl([
            {"text": "30 sec · one pass · with sound", "kind": "label", "at": 0.15},
            {"text": "would you hand it", "kind": "headline", "at": 0.55},
            {"text": "a client's brief?", "kind": "headline", "at": 0.85, "accent": True},
        ], y=0.07),
        "sfx": [dict(IMPACT, at=0.6)],
    },
]

# ---------------------------------------------------------------- captions
FIX = {
    "Seedense": "Seedance", "seedense": "Seedance",
    "bite dance": "ByteDance", "Bite dance": "ByteDance",
    "bite": "ByteDance", "dance": "",          # only ever appears as the pair
    "2 .5": "2.5",
}


def chunk(ws, size=3):
    out, buf = [], []
    for (s, e, w) in ws:
        buf.append((s, e, w))
        end_of_clause = re.search(r"[.,!?—:;]$", w)
        if len(buf) >= size or (end_of_clause and len(buf) >= 2):
            out.append(buf)
            buf = []
    if buf:
        out.append(buf)
    return out


captions = []
for grp in chunk(words):
    text = " ".join(w[2] for w in grp)
    per = [{"t": round(w[0], 2), "text": w[2]} for w in grp]
    # display-only corrections; timings untouched
    if "bite" in text.lower() and "dance" in text.lower():
        text = re.sub(r"[Bb]ite\s+dance", "ByteDance", text)
        for i, p in enumerate(per):
            if p["text"].lower() == "bite":
                p["text"] = "ByteDance"
            elif p["text"].lower() == "dance" and i and per[i - 1]["text"] == "ByteDance":
                p["text"] = ""
    text = text.replace("Seedense", "Seedance").replace("2 .5", "2.5")
    for p in per:
        p["text"] = p["text"].replace("Seedense", "Seedance").replace("2 .5", "2.5")
    per = [p for p in per if p["text"]]
    captions.append({
        "start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
        "text": text, "words": per,
    })

# ------------------------------------------------------------------- music
music = {
    "src": "music/bed-02.mp3", "from": 8.0,
    "points": [
        {"t": 0.0, "vol": 0.15},
        {"t": B["hook"][1], "vol": 0.15},
        {"t": B["hook"][1] + 0.7, "vol": 0.08},          # duck for explanation
        {"t": B["face1"][0], "vol": 0.07},
        {"t": B["refsfan"][0], "vol": 0.10},
        {"t": B["reddress"][0], "vol": 0.14},            # rise into the reveal
        {"t": B["lipjp"][1], "vol": 0.13},
        {"t": B["face3"][0], "vol": 0.07},               # duck under the honesty beat
        {"t": B["debris"][0], "vol": 0.15},              # up for the close
        {"t": TOTAL - 0.9, "vol": 0.13},
        {"t": TOTAL, "vol": 0.02},
    ],
}

beats = {
    "id": "seedance-25", "fps": 30, "width": 1080, "height": 1920,
    "style": "varun",
    "audio": AVATAR,
    "music": music,
    "captionStyle": "nick-display",
    "emphasis": ["TikTok", "ByteDance", "Seedance", "2.5", "30", "50", "15",
                 "10", "nine", "three", "dozen", "benchmark", "seconds"],
    "scenes": scenes, "captions": captions,
}

total_scenes = sum(s["durationSec"] for s in scenes)
print(f"\nscenes {total_scenes:.2f}s vs reel {TOTAL:.2f}s  (delta {total_scenes - TOTAL:+.2f}s)")
assert abs(total_scenes - TOTAL) < 0.02, "scenes must sum to the audio length"
longest = max(scenes, key=lambda s: s["durationSec"])
print(f"scenes: {len(scenes)}, avg {total_scenes / len(scenes):.2f}s, "
      f"longest {longest['durationSec']:.2f}s ({longest['type']})")
face = sum(s["durationSec"] for s in scenes if s.get("src") == AVATAR)
print(f"facecam {face:.2f}s = {100 * face / TOTAL:.0f}% of runtime (target 10-20%)")

# ── BLOCKING GATES ──────────────────────────────────────────────────────────
# Every mechanical rule from STYLE-RULES.md, enforced as code. This raises
# rather than prints: a violated rule must stop the build, not scroll past.
# allow_short=True because this reel predates the 2026-08-11 1-2 minute rule.
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())
try:
    for w in check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST,
                         allow_short=True):
        print(f"  warning: {w}")
    print("GATES: PASSED")
except GateError as e:
    raise SystemExit(f"GATES FAILED — beat sheet NOT written\n{e}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
