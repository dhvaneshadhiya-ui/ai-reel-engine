#!/usr/bin/env python3
"""Beat sheet for apple-pay-india (editorial).

Treatment split, decided from verified frames (see manifest):
  apple-ad      = live-action, survives a 9:16 crop  -> FULL-BLEED footage
  apple-support = UI mockups centred in 16:9         -> FRAMED floatcards
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402
from notation import normalise, normalise_words  # noqa: E402

SLUG = "apple-pay-india"
ROOT = Path(__file__).resolve().parent.parent
A = f"assets/{SLUG}"
C = f"{A}/clips"
OUT = ROOT / f"src/beats/{SLUG}.json"
AVATAR = f"{A}/avatar-master-169.mp4"
FACE_X = float((ROOT / f"public/{A}/face-x.txt").read_text().strip())
LOGO = json.loads((ROOT / "public/assets/logos/apple.paths.json").read_text())
MANIFEST = json.loads((ROOT / f"public/{A}/manifest.json").read_text())

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
    s = max(cw / iw, ch / ih)
    w = iw * s
    return 0.5 if w <= cw + 1 else round(max(0, min(1, (fx * w - cw / 2) / (w - cw))), 3)


FOCUS_FULL = css_pos(FACE_X, 1920, 1080, 1080, 1920)
FOCUS_SPLIT = css_pos(FACE_X, 1920, 1080, 1080, 960)


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
    ("logo",      "by october"),
    ("split",     "that its arriving"),
    ("without",   "arriving without"),
    ("howto",     "how it works"),
    ("mastercard","or mastercard"),
    ("wallet",    "apple wallet"),
    ("iphone",    "your iphone"),
    ("watch",     "apple watch"),
    ("terminal",  "contactless terminal"),
    ("thatsit",   "thats it"),
    ("face1",     "card number"),
    ("bankissue", "bank issues"),
    ("device",    "devicespecific number"),
    ("onetime",   "onetime code"),
    ("face2",     "nobody noticed"),
    ("noupi",     "not at launch"),
    ("face3",     "an oversight"),
    ("route",     "upi payments"),
    ("npci",      "from the npci"),
    ("sponsor",   "sponsor bank"),
    ("face4",     "which matters"),
    ("share",     "digital payments"),
    ("may",       "may alone"),
    ("scale",     "billion transactions"),
    ("rupees",    "trillion rupees"),
    ("notupi",    "taking on upi"),
    ("slice",     "doesnt own"),
    ("premium",   "premium credit cards"),
    ("face5",     "the real story"),
    ("tech",      "the technology"),
    ("money",     "was the money"),
    ("banks",     "biggest banks"),
    ("months",    "for months"),
    ("bps",       "basis points"),
    ("txn",       "card transaction"),
    ("counter",   "counted at 10"),
    ("face6",     "the shopkeeper"),
    ("whopays",   "already earn"),
    ("face7",     "none of this"),
    ("unconf",    "feature lists"),
    ("reporting", "this is reporting"),
    ("waiting",   "keep waiting"),
    ("interest",  "be interesting"),
    ("cta",       "qr code"),
]

def region_bounds(regions, words, total):
    """Each region ends on its own anchor PHRASE, then is divided equally
    among the visuals that belong to it.

    This is the fix for the sync failure of the first cut: an even split by
    time put every visual wherever a clock boundary fell, so the security
    spec sheet played over "not at launch" and the 85% chart over "billion
    transactions". Cuts must land on the words the visual is ABOUT, and a
    region too long for one beat is subdivided with visuals that all belong
    to that same region — never by borrowing the next region's visual.
    """
    out, prev = [], 0.0
    for k, (phrase, builders) in enumerate(regions):
        end = total if k == len(regions) - 1 else round(find(phrase) + 0.12, 2)
        n = len(builders)
        # A region can only carry as many visuals as it has time for — a
        # 0.45s beat reads as a glitch, not a cut. Drop the extras rather
        # than flash them.
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
AD, SU, W16 = "Apple", "Apple Support", 16 / 9


def hl(lines, y=0.12, theme="light", align="center"):
    return {"lines": lines, "y": y, "theme": theme, "align": align}


# ── builders: every one takes (start, duration) so a region can subdivide ────
def card(name, headline=None, sfx=None, credit=SU):
    def build(t0, d):
        sc = {"type": "floatcard", "src": f"{C}/{name}.mp4", "bg": "gradient",
              "aspect": W16, "durationSec": d, "credit": credit,
              "assetId": f"clip-{name}"}
        if headline:
            sc["headline"] = headline
        if sfx:
            sc["sfx"] = sfx
        return sc
    return build


def shot(name, zoom="in", cb=None, credit=AD, sfx=None):
    def build(t0, d):
        sc = {"type": "footage", "src": f"{C}/{name}.mp4", "durationSec": d,
              "zoomDir": zoom, "credit": credit, "assetId": f"clip-{name}"}
        if cb:
            sc["captionBottom"] = cb
        if sfx:
            sc["sfx"] = sfx
        return sc
    return build


def face(headline=None, cb=300):
    def build(t0, d):
        sc = {"type": "footage", "src": AVATAR, "durationSec": d,
              "from": round(t0, 2), "focusX": FOCUS_FULL, "captionBottom": cb}
        if headline:
            sc["headline"] = headline
        return sc
    return build


def mg(spec, sfx=None):
    def build(t0, d):
        sc = dict(spec, durationSec=d)
        if sfx:
            sc["sfx"] = sfx
        return sc
    return build


def receipt_card(label, head, accent=False, aid=None):
    def build(t0, d):
        sc = {"type": "floatcard", "src": f"{C}/receipt-bt.png", "bg": "gradient",
              "aspect": 1780 / 545, "durationSec": d, "credit": "Business Today",
              "headline": hl([
                  {"text": label, "kind": "label", "at": 0.1},
                  {"text": head, "kind": "headline", "at": 0.4, "accent": accent},
              ], y=0.11, theme="dark")}
        if aid:
            sc["assetId"] = aid
        return sc
    return build


def logo_hook(t0, d):
    return {
        "type": "logoassemble", "durationSec": d, "hideCaptions": True,
        "viewBox": LOGO["viewBox"], "paths": LOGO["paths"],
        "size": 1020, "y": 0.52, "bg": "cream", "fillOverride": "#141414",
        "label": "APPLE PAY · INDIA", "labelAt": 0.35,
        "headline": hl([{"text": "reportedly", "kind": "label", "at": 0.12}], y=0.07),
        "sfx": [dict(RISER, at=0.0), dict(IMPACT, at=0.35)],
    }


def split_hook(t0, d):
    return {
        "type": "split", "durationSec": d, "captionBottom": 1000,
        "topSrc": f"{C}/ad-contactless.mp4", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": round(t0, 2), "bottomFocusX": FOCUS_SPLIT,
        "credit": AD, "assetId": "clip-ad-contactless",
    }


SPEC_SECURITY = {
    "type": "specsheet", "bgSrc": f"{C}/ad-counter.mp4", "bgFrom": 0.0,
    "kicker": "what the terminal sees", "title": "Never your card",
    "columns": ["SENT AT TAP"],
    "rows": [
        {"label": "Your real card number", "values": ["never"]},
        {"label": "Device Account Number", "values": ["from your bank"]},
        {"label": "One-time cryptogram", "values": ["per tap"], "accent": True},
    ],
    "footnote": "source: Apple, support.apple.com/101554",
}
WC_NOUPI = {
    "type": "wordcascade", "bg": "cream", "captionTheme": "dark",
    "words": [
        {"text": "no UPI.", "style": "serif", "at": 0.12, "size": 1.6},
        {"text": "not at launch.", "style": "caps", "at": 0.8, "size": 1.15},
    ],
}
CHECKLIST_UPI = {
    "type": "checklist", "bg": "gradient", "headline": "To add UPI, Apple needs",
    "rows": [
        {"label": "Clearance from NPCI", "state": "q"},
        {"label": "A sponsor bank to route payments", "state": "q"},
    ],
}
CHART_85 = {
    "type": "chart", "kicker": "India · digital payments",
    "title": "Who owns the volume", "unit": "%", "max": 100, "bg": "black",
    "items": [
        {"label": "UPI", "value": 85, "display": "85", "sub": "of all volume",
         "highlight": True},
        {"label": "Everything else", "value": 15, "display": "15",
         "sub": "cards, wallets, netbanking"},
    ],
    "source": "NPCI data, 2026",
}
SPEC_SCALE = {
    "type": "specsheet", "kicker": "UPI · May 2026", "title": "In one month",
    "columns": ["NPCI DATA"],
    "rows": [
        {"label": "Transactions", "values": ["23.2 billion"], "accent": True},
        {"label": "Value", "values": ["Rs 29.9 trillion"]},
    ],
    "footnote": "all-time high",
}
SPEC_INOUT = {
    "type": "specsheet", "kicker": "reported launch scope", "title": "What you get",
    "columns": ["AT LAUNCH"],
    "rows": [
        {"label": "Visa credit cards", "values": ["yes"]},
        {"label": "Mastercard credit cards", "values": ["yes"]},
        {"label": "UPI", "values": ["no"], "accent": True},
    ],
    "footnote": "reported, not confirmed by Apple",
}
CHART_BPS = {
    "type": "chart", "kicker": "per credit-card transaction",
    "title": "The real hold-up", "unit": "bps", "max": 20, "bg": "black",
    "items": [
        {"label": "Apple wants", "value": 20, "display": "15-20",
         "sub": "basis points of interchange", "highlight": True},
        {"label": "Banks countered", "value": 10, "display": "10",
         "sub": "basis points"},
    ],
    "source": "Business Standard, Aug 2026",
}
SPEC_WHOPAYS = {
    "type": "specsheet", "kicker": "and the fee comes from",
    "title": "Not your pocket", "columns": ["PAYS THE FEE"],
    "rows": [
        {"label": "You", "values": ["no"]},
        {"label": "The shopkeeper", "values": ["no"]},
        {"label": "Bank interchange revenue", "values": ["yes"], "accent": True},
    ],
    "footnote": "Business Today, Aug 2026",
}
SPEC_BANKS = {
    "type": "specsheet", "kicker": "reported in discussions",
    "title": "Who Apple is talking to", "columns": ["ISSUER"],
    "rows": [
        {"label": "ICICI Bank", "values": ["in talks"]},
        {"label": "HDFC Bank", "values": ["in talks"]},
        {"label": "Axis Bank", "values": ["in talks"]},
    ],
    "footnote": "earlier Bloomberg reporting",
}
WC_UNCONF = {
    "type": "wordcascade", "bg": "cream", "captionTheme": "dark",
    "words": [
        {"text": "no date.", "style": "serif", "at": 0.1, "size": 1.35},
        {"text": "no bank list.", "style": "serif", "at": 0.7, "size": 1.3},
        {"text": "no confirmation.", "style": "caps", "at": 1.3, "size": 1.4},
    ],
}

# ── REGIONS: (anchor phrase, visuals that illustrate THAT phrase) ────────────
# The span ending on the phrase is divided among its own visuals, so a cut
# always lands on the words the visual is about.
regions = [
    ("launching in india",   [logo_hook]),
    ("by october",           [receipt_card("reported by", "Business Today")]),
    ("that its arriving",    [split_hook]),
    ("arriving without",     [shot("ad-store")]),
    ("how it works",         [card("su-logo")]),
    ("or mastercard",        [card("su-scan")]),
    ("to apple wallet",      [card("su-card"), card("su-wallet", headline=hl([
                                  {"text": "step one", "kind": "label", "at": 0.1},
                                  {"text": "card into Wallet", "kind": "headline", "at": 0.4},
                              ], y=0.11, theme="dark"))]),
    ("your iphone",          [card("su-add2", sfx=[dict(WHOOSH, at=0.0)]),
                          card("su-devices")]),
    ("apple watch",          [card("su-watch", headline=hl([
                                  {"text": "iPhone · Watch · iPad", "kind": "label", "at": 0.1},
                              ], y=0.11, theme="dark"))]),
    ("contactless terminal", [card("su-nfc")]),
    ("thats it",             [shot("ad-tap", zoom="out", cb=380,
                                   sfx=[dict(IMPACT, at=0.2)])]),
    ("real card number",     [face()]),
    ("devicespecific number", [card("su-flow"), card("su-blue")]),
    ("onetime code",         [mg(SPEC_SECURITY)]),
    ("nobody noticed",       [face()]),
    ("not at launch",        [mg(WC_NOUPI, sfx=[dict(GROUND, at=0.12)])]),
    ("an oversight",         [face()]),
    ("upi payments",         [card("su-confirm")]),
    ("from the npci",        [card("su-set2"), mg(CHECKLIST_UPI)]),
    ("that runs upi",        [card("su-approved")]),
    ("sponsor bank",         [card("su-settings")]),
    ("which matters",        [face()]),
    ("digital payments",     [card("su-hist"),
                          mg(CHART_85, sfx=[dict(GROUND, at=0.3)])]),
    ("may alone",            [shot("ad-exterior")]),
    ("billion transactions", [mg(SPEC_SCALE)]),
    ("trillion rupees",      [shot("ad-counter", zoom="out")]),
    ("taking on upi",        [mg(SPEC_INOUT)]),
    ("doesnt own",           [card("su-grocery"), card("su-multi")]),
    ("premium credit cards", [card("su-list")]),
    ("the real story",       [face()]),
    ("the technology",       [card("su-transit")]),
    ("was the money",        [shot("ad-face")]),
    ("biggest banks",        [shot("ad-cashier"), mg(SPEC_BANKS)]),
    ("for months",           [card("su-terminal")]),
    ("card transaction",     [card("su-buy"), card("su-tap")]),
    ("counted at 10",        [mg(CHART_BPS, sfx=[dict(IMPACT, at=0.3)])]),
    ("the shopkeeper",       [mg(SPEC_WHOPAYS)]),
    ("already earn",         [face()]),
    ("none of this",         [card("su-outro"), face()]),
    ("feature lists",        [mg(WC_UNCONF, sfx=[dict(GROUND, at=1.3)])]),
    ("this is reporting",    [receipt_card("still unconfirmed", "by Apple",
                                           accent=True, aid="receipt-bt")]),
    ("keep waiting",         [card("su-menu"), card("su-flow2")]),
    ("be interesting",       [shot("ad-logo", cb=420), card("su-txn")]),
    ("qr code",              [card("su-tap2"), face(headline=hl([
                                  {"text": "tap · or scan a QR", "kind": "label", "at": 0.15},
                                  {"text": "which one wins", "kind": "headline", "at": 0.5},
                                  {"text": "in India?", "kind": "headline", "at": 0.8,
                                   "accent": True},
                              ], y=0.07))]),
]

placed = region_bounds(regions, words, TOTAL)
scenes = [b(s0, round(s1 - s0, 2)) for (_, s0, s1, b) in placed]
print(f"  {len(regions)} regions -> {len(scenes)} scenes")
from collections import defaultdict
_agg, _cnt = defaultdict(float), defaultdict(int)
for (_ph, _s0, _s1, _b) in placed:
    _agg[_ph] += _s1 - _s0
    _cnt[_ph] += 1
_long = [(ph, _agg[ph], _cnt[ph]) for ph in _agg if _agg[ph] / _cnt[ph] > 2.55]
if _long:
    print("  regions needing another visual:")
    for ph, tot, n in _long:
        print(f"    {ph!r}: {tot:.2f}s over {n} visual(s) = {tot / n:.2f}s each "
              f"-> needs {int(tot // 2.5) + 1}")


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


# Display-only correction. The TTS dropped the "-er" from "countered" and
# BOTH whisper base and small hear "counted", so the slip is in the audio,
# not the transcription. Regenerating 100s of avatar for one word is not
# worth the credits: the caption and the on-screen chart both carry the
# correct word ("Banks countered"), which is the documented fix strategy.
FIX = {"counted at 10": "countered at 10", "counted": "countered"}
# Verified spellings only — taken from the sources in the manifest, never
# guessed. `notation` lives in the manifest so the canonical layer can never
# invent a product name the scout did not actually see.
CANON = MANIFEST.get("notation", {})
# normalise BEFORE chunking so notation spanning two words survives
caption_words = normalise_words(words, CANON)
captions = []
for grp in chunk(caption_words):
    text = " ".join(w[2] for w in grp)
    per = [{"t": round(w[0], 2), "text": w[2]} for w in grp]
    for a, b in FIX.items():
        text = text.replace(a, b)
        for p in per:
            p["text"] = p["text"].replace(a, b)
    text = normalise(text, CANON)
    for p in per:
        p["text"] = normalise(p["text"], CANON)
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                     "text": text, "words": [p for p in per if p["text"]]})

# music follows the placed regions, so the automation lands on the same words
R = {ph: (s0, s1) for (ph, s0, s1, _) in placed}
music = {
    "src": "music/bed-02.mp3", "from": 8.0,
    "points": [
        {"t": 0.0, "vol": 0.15},
        {"t": R["that its arriving"][1], "vol": 0.15},
        {"t": R["arriving without"][1], "vol": 0.08},      # duck for the how-to
        {"t": R["nobody noticed"][0], "vol": 0.07},
        {"t": R["not at launch"][0], "vol": 0.13},         # lift on the absence
        {"t": R["digital payments"][0], "vol": 0.10},
        {"t": R["counted at 10"][0], "vol": 0.14},         # the fee reveal
        {"t": R["none of this"][0], "vol": 0.07},          # duck under the caveat
        {"t": R["keep waiting"][0], "vol": 0.14},
        {"t": TOTAL - 0.9, "vol": 0.13},
        {"t": TOTAL, "vol": 0.02},
    ],
}

beats = {
    "id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "editorial",
    "audio": AVATAR, "music": music, "captionStyle": "word-reveal",
    "emphasis": ["UPI", "Apple", "Visa", "Mastercard", "85", "23.2", "29.9",
                 "October", "India", "NPCI", "fifteen", "twenty", "ten",
                 "basis", "points", "credit"],
    "scenes": scenes, "captions": captions,
}

total = round(sum(s["durationSec"] for s in scenes), 2)
print(f"\nscenes {total:.2f}s vs reel {TOTAL:.2f}s (delta {total - TOTAL:+.2f}s)")
face_s = sum(s["durationSec"] for s in scenes if s.get("src") == AVATAR)
print(f"scenes: {len(scenes)}, avg {total / len(scenes):.2f}s, "
      f"facecam {face_s:.1f}s = {100 * face_s / total:.0f}%")

# measure every referenced clip once so G13 can catch a beat that outruns
# its own footage
import subprocess
clip_durations = {}
for sc in scenes:
    for key in ("src", "mediaSrc", "topSrc", "bottomSrc", "bgSrc"):
        v = sc.get(key)
        if not v or "avatar-master" in str(v) or v in clip_durations:
            continue
        f = ROOT / "public" / str(v)
        if not f.exists():
            raise SystemExit(f"MISSING ASSET FILE: {f}")
        if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            continue
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(f)], capture_output=True, text=True)
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
