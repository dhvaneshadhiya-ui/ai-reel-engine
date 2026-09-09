#!/usr/bin/env python3
"""Beat sheet for meta-muse-ai-agent (editorial, format=news).

Meta's own Sept 8 2026 launch, headlined "the world's first personal AI
agent." Visuals: the two real mobile receipts we could capture (Meta's own
press-release headline, the ai.meta.com/muse product page), facecam +
headline-overlay for everything the fast ElevenLabs read (3.15 w/s, 204
words / 64.86s) makes too short to hold a full MG card under its own G04
cap, and two short MG cards (a specsheet row for the Secure VM claim, a
statcard for the FTC fine) placed only where the anchor math leaves enough
room under the "building" (3.3s) / "card" (2.6s) ceilings.

Every anchor is hand-picked for UNIQUENESS against the whole whisper
stream — several phrases repeat ("personal AI agent" twice, "Meta" four
times, "24-7" twice) and find() always returns the first match, so a short
anchor for a LATER beat would silently re-bind to the EARLIER occurrence.
See the anchors list below for the disambiguating context kept on each one.

Whisper heard "haggles your build down" (confidence 0.54, vs 0.97+ on
every neighbouring word) where the script says "bill down" — confirmed on
TWO independent whisper-small passes (STYLE-RULES' own DRAM precedent: two
consistent low-confidence reads across passes means the word is genuinely
ambiguous in the audio, not a transcriber fluke). Not a re-record: one
borderline word among 204, fixed as a caption_corrections-style display
override at build time (ingest_avatar.py's own rule — a mishear is a
caption problem, never a reason to touch timings).
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

SLUG = "meta-muse-ai-agent"
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

# whisper mis-heard "bill" as "build" at ~15.78-16.0s (0.54 confidence vs
# 0.97+ neighbours, confirmed twice). Caption display only — vo.json timing
# is untouched, this only changes what the caption chip shows.
for i, (st, en, tx) in enumerate(words):
    if tx.rstrip(".,") == "build" and 15.5 < st < 16.1:
        words[i] = (st, en, "bill")
        break

CAPTION_CORRECTIONS = {"build": "bill"}  # display-only, recorded for the ledger


def css_pos(fx, iw, ih, cw, ch):
    s = max(cw / iw, ch / ih)
    w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


# Native 9:16 avatar master (1080x1920) into a 1080x1920 canvas: scaled
# width already equals canvas width, so css_pos always returns 0.5 — this
# is confirmed by the formula, not assumed. face-x.txt (0.487) is kept for
# the record; it has no effect on a source that already matches the canvas.
FOCUS_FULL = css_pos(FACE_X, 1080, 1920, 1080, 1920)

norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
stream = [norm(w[2]) for w in words]


def find(phrase):
    t = norm(phrase).split()
    for i in range(len(stream) - len(t) + 1):
        if stream[i:i + len(t)] == t:
            return words[i + len(t) - 1][1]
    raise SystemExit(f"ANCHOR NOT FOUND: {phrase!r}")


def region_bounds(regions, total):
    """buffer defaults to 0.12s of breathing room after the anchor word; pass
    0.0 for a beat immediately followed by a CONTIGUOUS next word (no gap),
    where the default buffer would push past the next word's own start and
    make G18 think this card is still up while that word is spoken."""
    out, prev = [], 0.0
    for k, region in enumerate(regions):
        phrase, builder = region[0], region[1]
        buf = region[2] if len(region) > 2 else 0.12
        end = total if k == len(regions) - 1 else round(find(phrase) + buf, 2)
        out.append((phrase, prev, end, builder))
        prev = end
    return out


CRED = ""
kit = Reel(slug=SLUG, avatar=AVATAR, clips=A, credit=CRED, focus_x=FOCUS_FULL)

hl = lambda lines, y=0.10, theme="light": {"lines": lines, "y": y, "theme": theme,
                                            "align": "center"}
SHUTTER = {"src": "sfx/Camera Shutter.MP3", "vol": 0.14}
WHOOSH = {"src": "sfx/whoosh.MP3", "vol": 0.13}
POP = {"src": "sfx/Pop.MP3", "vol": 0.15}
IMPACT = {"src": "sfx/Core.MP3", "vol": 0.17}


def zface(headline=None, **extra):
    return kit.face(headline=headline, **extra)


# --- the real mobile receipts -----------------------------------------------
HEADLINE_PNG = "receipt-press-headline-crop.png"
PRODUCT_PNG = "receipt-muse-product-page-crop.png"   # 1080x2100 — tall enough for G59

# highlight rect for the whole headline block (source px, 1080x1350)
HEADLINE_BOX = {"x": 20, "y": 610, "w": 1040, "h": 480}
# TIGHT per-icon boxes inside the 1080x2100 product-page crop. Each is
# ~180x150 — small enough against the 928px-wide card to clear the 1.35x
# zoom floor (a wide highlight, like the original 960px-wide HERO/ICON
# boxes, computed `fit` under 1.35 and never zoomed past the floor, leaving
# no headroom for the caption chip below the card — frame-lint EDGE TEXT on
# scenes 07/08 and DUPLICATE on 09->10, since two adjacent beats shared one
# wide box on the identical image). A tight box forces a real ~2.1x push-in,
# and each beat targets a DIFFERENT icon, so all four cuts read as visibly
# distinct receipts of the same verified page rather than one static hold.
ICON_ENVELOPE = {"x": 650, "y": 1800, "w": 180, "h": 150}   # "emails people"
ICON_CARD = {"x": 270, "y": 1615, "w": 180, "h": 150}       # "haggles your bill"
ICON_SALMON = {"x": 95, "y": 1615, "w": 180, "h": 150}      # "a recipe you saved"
ICON_CART = {"x": 280, "y": 1800, "w": 180, "h": 150}       # "into a grocery list"


def receipt(covers, highlight_at=0.1, box=HEADLINE_BOX, credit="Meta Newsroom",
            aid="receipt-press-headline", sfx=None):
    return kit.doc(HEADLINE_PNG, aid, credit=credit,
                    highlights=[dict(box, at=highlight_at)],
                    covers=covers, sfx=sfx)


def icon_receipt(covers, box, sfx=None):
    return kit.doc(PRODUCT_PNG, "receipt-muse-product-page",
                    credit="Meta / ai.meta.com",
                    highlights=[dict(box, at=0.05)], covers=covers, sfx=sfx)


SPEC_VM = {
    "type": "specsheet", "kicker": "META'S OWN CLAIM", "title": "WHERE MUSE RUNS",
    "rows": [{"label": "Runs in", "value": "Secure VM", "accent": True}],
    "footnote": "Source: about.fb.com, Sept 2026",
}
STAT_FTC = {
    "type": "statcard", "title": "META'S PRIVACY RECORD", "titleRight": "2019",
    "rows": [{"label": "FTC penalty", "value": "$5B", "pct": 1.0,
              "color": "#E4572E"}],
    "footnote": "Source: FTC.gov",
}
SPEC_PRICE = {
    "type": "specsheet", "kicker": "LAUNCHING NOW", "title": "MUSE PRICING",
    "rows": [
        {"label": "Power", "value": "$20/mo"},
        {"label": "Maximum", "value": "$100/mo", "accent": True},
    ],
    "footnote": "Source: about.fb.com, Sept 2026",
}

# (anchor phrase — the LAST words of the beat, exactly as WHISPER heard
# them — builder). Anchors are chosen long enough to be unique against the
# whole stream; see module docstring for the collisions this avoids.
BEATS = [
    ("new ai", zface(headline=hl(
        [{"text": "SEPT 8, 2026", "kind": "label", "at": 0.1}], y=0.06))),
    ("the worlds", receipt("agent the world's", box=HEADLINE_BOX,
                            sfx=[dict(SHUTTER, at=0.05)])),
    ("first personal ai agent", receipt(
        "first personal AI agent", highlight_at=0.05,
        box={"x": 20, "y": 630, "w": 1040, "h": 300})),

    ("bigger than that", zface(headline=hl(
        [{"text": "THE CATCH", "kind": "headline", "at": 0.15, "accent": True}],
        y=0.14))),

    ("says itll", zface()),
    ("dont have to", zface(headline=hl(
        [{"text": "ZUCKERBERG, ON X", "kind": "label", "at": 0.1},
         {"text": "WORKS 24/7", "kind": "headline", "at": 0.4, "accent": True}],
        y=0.07))),

    ("chat back", zface()),

    # Receipt's push-in is hard-capped near ~1.16x (cardFits = 1/0.86,
    # ReceiptScene.tsx) REGARDLESS of how tight the highlight box is — a
    # constant of the 86%-width card, not something a tighter box can beat.
    # So a run of same-image receipt beats close together in the grid reads
    # as near-identical (frame-lint DUPLICATE, 08->09 on the first attempt).
    # Fix: alternate receipt/facecam so no two receipt beats are ever
    # adjacent, rather than chasing zoom math the component doesn't support.
    ("books your flights", icon_receipt(
        "it emails people books your flights", ICON_ENVELOPE,
        sfx=[dict(WHOOSH, at=0.05)])),
    ("haggles your bill down", zface(headline=hl(
        [{"text": "HAGGLES YOUR BILL", "kind": "label", "at": 0.1}], y=0.14))),
    ("saved off instagram", icon_receipt(
        "turn a recipe you saved off Instagram", ICON_SALMON)),
    ("into a grocery list", zface(headline=hl(
        [{"text": "GROCERY LIST", "kind": "label", "at": 0.1}], y=0.14))),

    ("access to your accounts", zface()),

    ("own secure computer", kit.mg(SPEC_VM, covers="Muse runs inside its own secure computer",
                                    sfx=[dict(WHOOSH, at=0.05)])),

    ("rest of the internet", zface(headline=hl(
        [{"text": "WALLED OFF", "kind": "headline", "at": 0.15, "accent": True}],
        y=0.14))),
    ("called sentinel", zface(headline=hl(
        [{"text": "SENTINEL WATCHDOG", "kind": "label", "at": 0.1}], y=0.14))),
    ("leaves that computer", zface()),
    ("never even sees", zface(headline=hl(
        [{"text": "META SAYS:", "kind": "label", "at": 0.1}], y=0.14))),
    ("or your card", zface(headline=hl(
        [{"text": "NO PASSWORD. NO CARD.", "kind": "label", "at": 0.1,
          "accent": True}], y=0.14))),

    ("catch muse isnt", zface(headline=hl(
        [{"text": "THE CATCH", "kind": "headline", "at": 0.15, "accent": True}],
        y=0.14), sfx=[dict(WHOOSH, at=0.05)])),
    ("the first personal ai agent", zface()),
    ("shipped agents", zface()),
    ("before meta did", zface()),
    ("and anthropic", zface(headline=hl(
        [{"text": "GOOGLE · OPENAI", "kind": "label", "at": 0.15},
         {"text": "AMAZON · ANTHROPIC", "kind": "label", "at": 1.3}], y=0.14))),

    ("fined the same", zface(headline=hl(
        [{"text": "META'S OWN RECORD", "kind": "label", "at": 0.15}], y=0.14))),
    ("5 billion", kit.mg(STAT_FTC, covers="company 5 billion",
                          sfx=[dict(IMPACT, at=0.05)]), 0.0),
    ("handled peoples data", zface()),

    ("us only", zface(headline=hl(
        [{"text": "US ONLY", "kind": "headline", "at": 0.15, "accent": True}],
        y=0.14))),
    ("the web", zface()),
    ("to start", zface()),
    ("want more", zface()),
    ("100 a month", kit.mg(SPEC_PRICE, covers="thats 20 or 100 a month",
                            sfx=[dict(POP, at=0.05)])),

    ("muse work 247", zface()),
    ("your behalf", zface()),

    ("holding the keys", zface()),
]

regions = list(BEATS)
placed = region_bounds(regions, TOTAL)
scenes = [b(s0, round(s1 - s0, 2)) for (_, s0, s1, b) in placed]

_ZOOM_BASES = [1.0, 1.12]
for i, sc in enumerate(scenes):
    if sc.get("type") == "footage" and sc.get("src") == AVATAR:
        sc["zoomDir"] = "in"
        sc["zoom"] = _ZOOM_BASES[i % 2]

print(f"  {len(regions)} beats -> {len(scenes)} scenes")
for ph, s0, s1, b in placed:
    d = s1 - s0
    if d > 3.3 or d < 0.25:
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
    "audio": AVATAR, "captionStyle": "word-reveal", "noMusic": True,
    "noMusicReason": "brief.json set music:false — voice + SFX only, per the "
                     "2026-08-24 standing default; a skeptical editorial "
                     "piece needs no bed under the receipts.",
    "script": SCRIPT_TEXT,
    "approval": {"sha256": APPROVAL["sha256"], "approvedAt": APPROVAL["approvedAt"]},
    "captionCorrections": CAPTION_CORRECTIONS,
    "emphasis": ["Meta", "Muse", "24/7", "Google", "OpenAI", "Amazon",
                 "Anthropic", "$5,000,000,000", "$20", "$100"],
    "scenes": scenes, "captions": captions,
}

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

vo_words_for_gate = [(w[2], w[0], w[1]) for w in words]

try:
    for w in check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST,
                          clip_durations=clip_durations, vo_words=vo_words_for_gate):
        print(f"  warning: {w}")
    print("GATES: PASSED")
except GateError as e:
    raise SystemExit(f"GATES FAILED — beat sheet NOT written\n{e}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
