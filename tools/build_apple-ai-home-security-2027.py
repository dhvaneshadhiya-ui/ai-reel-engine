#!/usr/bin/env python3
"""Beat sheet for apple-ai-home-security-2027 (editorial, format=news).

Single-source rumor story (Bloomberg/Gurman via MacRumors), so the visuals
lean on: the actual mobile receipts of that reporting, Apple's own newsroom
page for the Ternus-CEO fact, AppleInsider's 2024 router-abandonment report,
and motion graphics for the mechanism/timeline/logic beats that have no
photographable subject (the camera doesn't exist yet).

Anchors are placed by hand rather than via even-split, so every held layout
lands under its RULES.md 2c cap: motion (footage/split) <=2.9s, timeline
<=3.3s, every other card (receipt/checklist/wordcascade) <=2.6s.

noCredits is set (RULES.md 2c, gate G47) per user directive 2026-09-07 —
no on-screen "Source: X" labels. `credit` stays on every scene for G14
provenance bookkeeping; only the drawn label is suppressed.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402
from reelkit import Reel  # noqa: E402

SLUG = "apple-ai-home-security-2027"
ROOT = Path(__file__).resolve().parent.parent
A = f"assets/{SLUG}"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())

raw = json.loads((ROOT / f"public/{A}/vo.json").read_text())
words = [(w["start"], w["end"], w["word"].strip()) for w in raw["words"]]
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


CRED = ""  # noCredits reel — nothing drawn, but keep per-scene `credit` for G14
kit = Reel(slug=SLUG, avatar=AVATAR, clips=A, credit=CRED, focus_x=FOCUS_FULL)

hl = lambda lines, y=0.10, theme="light": {"lines": lines, "y": y, "theme": theme,
                                            "align": "center"}
WHOOSH = {"src": "sfx/whoosh.MP3", "vol": 0.13}
SHUTTER = {"src": "sfx/Camera Shutter.MP3", "vol": 0.14}
REVEAL = {"src": "sfx/Magic Reveal.MP3", "vol": 0.15}
GROUND = {"src": "sfx2/ground-impact-352053.mp3", "vol": 0.13}


# DUPLICATE-frame guard: consecutive face() beats are the same continuous
# clip cut back to back, so the frame-lint's ahash compare sees near-
# identical mid-frames unless the crop SCALE actually differs at the
# midpoint. zoomDir alone does not do this: FootageScene interpolates
# [base, base*1.1] for "in" and [base*1.1, base] for "out", and both curves
# cross the exact same value (base*1.05) at the midpoint — confirmed on the
# first render, headline text alone didn't move enough pixels either.
#
# A counter incremented inside zface() calls was tried and is WRONG: two
# beats (hook_face, face_built) are separate top-level functions whose
# zface() call only runs when the scene-building comprehension invokes
# them, which happens AFTER every inline zface() call in the BEATS list
# has already incremented the counter — so their parity has no relation to
# their actual neighbours. Confirmed on the second render: scenes 2-3-4-5
# still flagged despite the counter "alternating". Fixed below by assigning
# zoom from each scene's REAL index in the final `scenes` list, after every
# builder has run — position-based, not call-order-based.
def zface(headline=None, **extra):
    return kit.face(headline=headline, **extra)


def hook_face(t0, d):
    return zface(headline=hl([{"text": "SEPTEMBER 4, 2026", "kind": "label", "at": 0.1},
                               {"text": "REPORTEDLY", "kind": "headline", "at": 0.4,
                                "accent": True}], y=0.06),
                  sfx=[dict(WHOOSH, at=0.05)])(t0, d)


def hook_receipt(t0, d):
    s = kit.doc("receipt-macrumors-headline-crop.png", "receipt-macrumors-headline",
                credit="MacRumors", covers="Apple's next security camera",
                highlights=[{"at": 0.15, "x": 90, "y": 0, "w": 900, "h": 730}])(t0, d)
    return s


def face_built(t0, d):
    return zface(headline=hl([{"text": "BUILT TO NOT RECORD YOU", "kind": "headline",
                                "at": 0.15, "accent": True}], y=0.14))(t0, d)


CHECK_PLAN = {
    "type": "checklist", "bg": "gradient", "headline": "THE PLAN (REPORTEDLY)",
    "rows": [
        {"label": "Home security camera", "state": "done"},
        {"label": "Monitoring service", "state": "done"},
        {"label": "Folds into Apple One?", "state": "q"},
    ],
}
WC_LOGIC = {
    "type": "wordcascade", "bg": "cream", "captionTheme": "dark",
    "words": [{"text": "less footage. less to leak.", "style": "serif", "at": 0.1, "size": 1.05}],
}
WC_HAPPENED = {
    "type": "wordcascade", "bg": "black", "captionTheme": "light",
    "words": [{"text": "something happened.", "style": "caps", "at": 0.1, "size": 1.2,
               "accent": True}],
}
TL_SLIP = {
    "type": "timeline", "kicker": "ALREADY SLIPPED TWICE", "title": "THE HOME CAMERA",
    "items": [
        {"date": "2025", "name": "first expected", "at": 0.15, "minor": True},
        {"date": "LATE 2026", "name": "then this", "at": 0.9, "minor": True},
        {"date": "2027", "name": "now the target", "at": 1.7, "accent": "#FFD84D"},
    ],
    "footnote": "AppleInsider reporting history, Sept 4 2026",
}

# (end phrase, single builder) — hand-anchored, see module docstring.
BEATS = [
    ("Bloomberg reported", hook_face),
    ("security camera", hook_receipt),
    ("not record you", face_built),

    ("the trade", zface()),
    ("center of it", zface()),

    ("new CEO", zface()),
    ("targeting 2027", kit.doc("receipt-ceo-headline-crop.png", "receipt-ceo-headline",
                               credit="Apple Newsroom",
                               covers="John Ternus, targeting 2027",
                               highlights=[{"at": 0.15, "x": 90, "y": 0, "w": 900, "h": 980}],
                               sfx=[dict(SHUTTER, at=0.05)])),

    ("it's expected", zface()),
    ("watch the room", kit.doc("receipt-macrumors-mechanism-crop.png",
                                "receipt-macrumors-mechanism", credit="MacRumors",
                                covers="use on-device AI to watch the room")),

    ("a timestamp", zface(headline=hl([{"text": "JUST A TIMESTAMP", "kind": "headline",
                                         "at": 0.2, "accent": True}], y=0.14))),
    ("something move", zface()),

    ("video feed", zface()),

    ("something happened", zface()),
    ("right here right now", kit.mg(WC_HAPPENED, sfx=[dict(GROUND, at=0.1)])),

    ("plug into a new", zface()),
    ("home security service", zface()),

    ("fold into apple", kit.mg(CHECK_PLAN, sfx=[dict(REVEAL, at=0.1)])),

    ("logic is simple", zface()),
    ("footage stored", zface()),
    ("can ever leak", kit.mg(WC_LOGIC)),
    ("into a lawsuit", zface()),
    ("somewhere it shouldn't", zface()),

    ("slipped twice", zface()),
    ("from 2025", zface()),
    ("now 2027", kit.mg(TL_SLIP, sfx=[dict(GROUND, at=0.3)])),

    ("same company that reportedly", zface()),
    ("smart routers", kit.doc("receipt-router-headline-crop.png", "receipt-router-headline",
                               credit="AppleInsider",
                               covers="walked away from HomeKit's smart routers")),

    ("the whole pitch", zface(headline=hl([{"text": "THE TRADE", "kind": "headline",
                                             "at": 0.2, "accent": True}], y=0.14))),

    ("barely watch you", zface(headline=hl([
        {"text": "THIS CAMERA", "kind": "label", "at": 0.15},
        {"text": "BARELY WATCHES", "kind": "headline", "at": 0.45},
    ], y=0.07))),
    ("on the market", zface()),
    ("sells you the opposite", zface(headline=hl([
        {"text": "EVERYONE RECORDS", "kind": "headline", "at": 0.1, "accent": True},
    ], y=0.14))),

    ("security to you", zface()),
    ("actually watch", zface(headline=hl([
        {"text": "IS THAT STILL", "kind": "label", "at": 0.15},
        {"text": "SECURITY?", "kind": "headline", "at": 0.5, "accent": True},
    ], y=0.14))),
]

regions = [(phrase, [builder]) for phrase, builder in BEATS]
placed = region_bounds(regions, TOTAL)
scenes = [b(s0, round(s1 - s0, 2)) for (_, s0, s1, b) in placed]

# Position-based zoom alternation (see zface() note above for why a
# call-order counter can't do this correctly). Every footage scene whose
# src is the avatar gets a zoom keyed to its OWN index in the final list —
# guaranteed different from its immediate neighbour regardless of which
# builder produced it or when.
_ZOOM_BASES = [1.0, 1.12]
for i, sc in enumerate(scenes):
    if sc.get("type") == "footage" and sc.get("src") == AVATAR:
        sc["zoomDir"] = "in"
        sc["zoom"] = _ZOOM_BASES[i % 2]

print(f"  {len(regions)} beats -> {len(scenes)} scenes")
for ph, s0, s1, b in placed:
    d = s1 - s0
    if d > 3.3 or d < 0.3:
        print(f"    CHECK: {ph!r} {d:.2f}s")


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


SCRIPT_TEXT = (ROOT / f"jobs/{SLUG}/script.md").read_text().strip()
APPROVAL = json.loads((ROOT / f"jobs/{SLUG}/approval.json").read_text())

captions = []
for grp in chunk(words):
    text = " ".join(w[2] for w in grp)
    per = [{"t": round(w[0], 2), "text": w[2]} for w in grp]
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                      "text": text, "words": per})

beats = {
    "id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "editorial",
    "format": "news",
    "audio": AVATAR, "captionStyle": "nick-display", "noMusic": True,
    "noMusicReason": "brief.json set music:false; a skeptical single-source "
                     "reel reads better VO-only, no bed underneath receipts.",
    "script": SCRIPT_TEXT,
    "approval": {"sha256": APPROVAL["sha256"], "approvedAt": APPROVAL["approvedAt"]},
    "noCredits": {
        "reason": "user directive, 2026-09-07 session: no on-screen source "
                  "labels for this reel."
    },
    "emphasis": ["Bloomberg", "Ternus", "2027", "AI", "2025", "2026",
                 "HomeKit", "lawsuit", "Apple"],
    "scenes": scenes, "captions": captions,
}

total = round(sum(s["durationSec"] for s in scenes), 2)
fs = sum(s["durationSec"] for s in scenes if s.get("src") == AVATAR
         or s.get("bottomSrc") == AVATAR)
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
