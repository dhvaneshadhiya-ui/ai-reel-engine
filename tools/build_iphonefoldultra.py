#!/usr/bin/env python3
"""Beat sheet for iphone-fold-ultra (varun-mayya, news).

ANGLE: not a spec list (september-preview already did that on 2026-08-14) but
one argument — Apple built the foldable WIDE, not tall, and Touch ID, the
missing telephoto and the 4:3 screen all fall out of that shape.

SOURCE DISCIPLINE (user rule 2026-08-17): no aggregator is NAMED in the VO —
the spec figures are spoken bare and MacRumors rides on card footnotes and the
receipts. Original claimants (Kuo / UBS / IDC) ARE named, because they are the
claim.

HONESTY: the hero footage is a non-functional DUMMY. Every dummy beat credits
"Unbox Therapy — dummy unit". The mockup seam is never paired with the crease
line (that beat is MG only), and the on-camera caliper readouts measure the
MOCKUP so they run as texture while the only thickness figure on screen is the
sourced 4.5mm. Two clips (back-cameras, bump-macro) were cut and then DELETED
on inspection: they are a REAL iPhone's camera, not the dummy's.

TREATMENTS: no specsheet (in BOTH previous reels), no sourceread/uidialog/
checklist/statcard (september-preview), no annotatezoom/timeline/categorygrid/
endquestion (iphone18-split). New here: the persistent DUMMY-UNIT credit line
and measurement-texture footage. Returning after two reels away: cream receipt
with highlight sweeps, chart with labelled bars.

Master 82.26s -> 79.62s by 4 mid-silence pause tightenings (zero credits),
inside the 60-80s band, no allowLong.
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

SLUG = "iphone-fold-ultra"
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


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


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


# ── sound: placed by ROLE, not taste (RULES.md §8, G28) ────────────────────
# transition on a cut · popup on an element entering · shutter on a still
# landing · impact on a data card · reveal on the payoff. impact-boom (2.09s)
# is deliberately NOT used: no scene here is long enough to contain it.
WHOOSH = {"src": "sfx2/whooshes-01.mp3", "vol": 0.12}   # transition, 0.89s
POP = {"src": "sfx/Pop.MP3", "vol": 0.12}               # popup,      0.18s
SHUTTER = {"src": "sfx/Camera Shutter.MP3", "vol": 0.13}  # shutter,  0.34s
CORE = {"src": "sfx/Core.MP3", "vol": 0.16}             # impact,     0.68s
REVEAL = {"src": "sfx/Magic Reveal.MP3", "vol": 0.14}   # reveal,     1.49s

hl = lambda lines, y=0.10, theme="light": {"lines": lines, "y": y,
                                           "theme": theme, "align": "center"}

# Headlines used by the floatcards above their definitions further down.
HL_TOUCHID = hl([{"text": "NO Face ID", "kind": "label", "at": 0.15},
                 {"text": "Touch ID", "kind": "headline", "at": 0.5,
                  "accent": True}], y=0.09)
HL_3000 = hl([{"text": "UP TO", "kind": "label", "at": 0.15},
              {"text": "$3,000", "kind": "headline", "at": 0.5,
               "accent": True}], y=0.09)

# Every dummy beat says so, on screen. Credit.tsx renders "Source: <text>".
DUMMY = "Unbox Therapy — dummy unit"


def shot(name, zoom="in", headline=None, cb=None, sfx=None, credit=DUMMY,
         infocard=None):
    def b(t0, d):
        s = {"type": "footage", "src": f"{C}/{name}.mp4", "durationSec": d,
             "zoomDir": zoom, "credit": credit, "assetId": f"clip-{name}"}
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


def rcpt(png, sw, sh, aid, highlights, sfx=None):
    def b(t0, d):
        s = {"type": "receipt", "src": f"{C}/{png}.png", "backdrop": "cream",
             "srcWidth": sw, "srcHeight": sh, "highlights": highlights,
             "credit": "MacRumors", "durationSec": d, "assetId": aid}
        if sfx: s["sfx"] = sfx
        return s
    return b


def flo(png, aid, aspect, headline=None, sfx=None):
    """Framed window at TRUE aspect. Used where `receipt` cannot be: the
    faceid and pricing captures are wide enough that ReceiptScene's zoom
    (Z floor 1.35) overflowed and cut their text mid-word — verified on
    rendered frames, twice, before switching (RULES.md §5)."""
    def b(t0, d):
        s = {"type": "floatcard", "src": f"{C}/{png}.png", "bg": "gradient",
             "aspect": aspect, "durationSec": d, "credit": "MacRumors",
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
        "topSrc": f"{C}/unfold-hero.mp4", "topFrom": 0.0, "topFocusX": 0.5,
        "bottomSrc": AVATAR, "bottomFrom": round(t0, 2),
        "bottomFocusX": FOCUS_SPLIT, "credit": DUMMY,
        "assetId": "clip-unfold-hero", "sfx": [dict(WHOOSH, at=0.0)],
        "kinetic": {"text": "NOT TALLER", "style": "caps", "at": 0.55,
                    "y": 0.30},
    }


# ── receipts: highlight boxes in SOURCE pixels of the cropped png ───────────
# Two passes per capture (never adjacent on the same png without a cut), so a
# receipt reads as a document being read, not a static screenshot.
RC_CREASE_A = rcpt("mr-crease", 1580, 974, "receipt-mr-crease", [
    {"at": 0.25, "x": 1065, "y": 287, "w": 166, "h": 56},  # has no
    {"at": 0.85, "x": 227, "y": 351, "w": 326, "h": 56},   # visible crease
], sfx=[dict(SHUTTER, at=0.08)])
RC_CREASE_B = rcpt("mr-crease", 1580, 974, "receipt-mr-crease", [
    {"at": 0.25, "x": 1073, "y": 509, "w": 250, "h": 58},  # "regardless
    {"at": 0.95, "x": 227, "y": 565, "w": 168, "h": 58},   # of cost,"
])
FC_FACEID_A = flo("mr-faceid", "receipt-mr-faceid", 1170 / 560,
                  sfx=[dict(SHUTTER, at=0.08)])
FC_FACEID_B = flo("mr-faceid-b", "receipt-mr-faceid-b", 1170 / 430,
                  headline=HL_TOUCHID)
FC_PRICING_A = flo("mr-pricing", "receipt-mr-pricing", 1170 / 620,
                   sfx=[dict(SHUTTER, at=0.08)])
FC_PRICING_B = flo("mr-pricing", "receipt-mr-pricing", 1170 / 620)

CHART_PRICE = {
    "type": "chart", "kicker": "nobody agrees", "title": "What it might cost",
    "bg": "black", "unit": "", "max": 3000,
    "items": [
        {"label": "UBS", "value": 2000, "display": "$1,800–$2,000"},
        {"label": "Ming-Chi Kuo", "value": 2500, "display": "$2,000–$2,500",
         "highlight": True},
        {"label": "Fubon Research", "value": 2400, "display": "$2,400"},
        {"label": "IDC", "value": 3000, "display": "$2,500 avg · $3,000 top"},
    ],
    "source": "MacRumors roundup · Aug 2026",
}

HL_NAME = hl([{"text": "APPLE'S FIRST FOLDABLE", "kind": "label", "at": 0.15},
              {"text": "iPhone Ultra", "kind": "headline", "at": 0.45},
              {"text": "expected September 2026", "kind": "subtitle",
               "at": 0.85}], y=0.34)
HL_776 = hl([{"text": "UNFOLDED", "kind": "label", "at": 0.15},
             {"text": "7.76″", "kind": "headline", "at": 0.45,
              "accent": True},
             {"text": "reported · MacRumors", "kind": "subtitle",
              "at": 0.9}], y=0.36)
HL_IPAD = hl([{"text": "A 4:3 SCREEN", "kind": "label", "at": 0.15},
              {"text": "iPad geometry", "kind": "headline", "at": 0.5,
               "accent": True}], y=0.38)
HL_549 = hl([{"text": "FOLDED", "kind": "label", "at": 0.15},
             {"text": "5.49″", "kind": "headline", "at": 0.45,
              "accent": True},
             {"text": "reported · MacRumors", "kind": "subtitle",
              "at": 0.9}], y=0.36)
HL_45 = hl([{"text": "UNFOLDED", "kind": "label", "at": 0.15},
            {"text": "4.5mm", "kind": "headline", "at": 0.45, "accent": True},
            {"text": "reported · MacRumors", "kind": "subtitle",
             "at": 0.9}], y=0.36)
HL_48MP = hl([{"text": "THE WHOLE SYSTEM", "kind": "label", "at": 0.15},
              {"text": "48MP × 2", "kind": "headline", "at": 0.5,
               "accent": True},
              {"text": "no telephoto", "kind": "subtitle", "at": 0.9}],
             y=0.36)
HL_CREASE = hl([{"text": "CREASE DEPTH", "kind": "label", "at": 0.15},
                {"text": "0.15mm", "kind": "headline", "at": 0.5,
                 "accent": True},
                {"text": "reported · MacRumors", "kind": "subtitle",
                 "at": 0.95}], y=0.36)
HL_SEPT = hl([{"text": "REPORTED EVENT DATE", "kind": "label", "at": 0.15},
              {"text": "SEPTEMBER 9", "kind": "headline", "at": 0.45,
               "accent": True}], y=0.38)
# G32: the closing headline sits mid-frame, clear of the platform's top chrome.
HL_CTA = hl([{"text": "WOULD YOU CARRY", "kind": "label", "at": 0.2},
             {"text": "A PASSPORT?", "kind": "headline", "at": 0.6,
              "accent": True}], y=0.46)

IC_DUMMY = {"heading": "DUMMY UNIT", "body": "a shape mockup — not the real device",
            "at": 0.3}

# Payoff cards. Cream keeps them clear of G12, which counts only plain BLACK
# typecards; exactly one black card is spent, on the crease figure.
def tc(text, bg="#f4f0e6", fg="#1a1712", credit=None, headline=None,
       style="serif", y=0.44, scrim=False):
    s = {"type": "typecard", "bg": bg, "fg": fg,
         "kinetic": {"text": text, "style": style, "at": 0.2, "y": y,
                     "scrim": scrim}}
    if credit: s["credit"] = credit
    if headline: s["headline"] = headline
    return s


TC_ONEDEC = tc("one decision")
TC_776 = tc("7.76 inches", credit="MacRumors")
TC_IPAD = tc("iPad geometry")
TC_549 = tc("5.49 inches", credit="MacRumors")
TC_45 = tc("4.5mm unfolded", credit="MacRumors")
TC_CREASE = tc("a 0.15mm fold", credit="MacRumors")
TC_48MP = tc("two 48MP cameras", credit="MacRumors")
TC_NOTHING = tc("nothing confirmed")
# the reel's ONE black card (G12) goes on the closing date, which also
# breaks the cream-on-cream duplicate the frame linter caught at 44 -> 45.
TC_SEPT = tc("September 9", bg="black", fg="#f5f2ea", credit="MacRumors",
             scrim=True)

# Fine anchors: the cut lands on the words the visual is ABOUT. Short regions
# keep every scene inside its G04 ceiling without inventing filler beats.
regions = [
    ("first foldable",        [split_hook]),
    ("taller iphone",         [shot("footprint-flat", zoom="out")]),
    ("shorter wider one",     [shot("size-vs-iphone")]),
    ("decision explains",     [face()]),
    ("strange about it",      [mg(TC_ONEDEC)]),
    ("the iphone ultra",      [shot("cover-hold", headline=HL_NAME,
                                    sfx=[dict(WHOOSH, at=0.0)])]),
    ("leaked dummy unit",     [shot("devices-hands", infocard=IC_DUMMY)]),
    ("shape mockup",          [shot("pair-backs", zoom="out")]),
    ("not the real thing",    [face()]),
    ("inner screen is",       [shot("unfold-hero-b", headline=HL_776)]),
    ("776 inches",            [mg(TC_776)]),
    ("4 to 3",                [shot("unfold-tilt")]),
    ("ipad geometry",         [mg(TC_IPAD)]),
    ("not phone geometry",    [shot("unfold-hands")]),
    ("folded a",              [shot("fold-cover", headline=HL_549)]),
    ("549 inch cover screen", [mg(TC_549)]),
    ("body so stabby",        [shot("flame-close")]),
    ("calling it a passport", [face()]),
    ("reportedly chasing",    [shot("profile-thin")]),
    ("45mm unfolded",         [mg(TC_45, sfx=[dict(CORE, at=0.3)])]),
    ("ever shipped",          [shot("tape-measure"), shot("caliper-wide")]),
    ("shape costs you",       [face()]),
    ("for face id",           [FC_FACEID_A]),
    ("power button",          [FC_FACEID_B]),
    ("telephoto either",      [shot("pair-stand")]),
    ("248 megapixel",         [shot("fold-back"), mg(TC_48MP)]),
    ("the whole system",      [shot("overhead-backs"), shot("pair-angled")]),
    ("crease though",         [RC_CREASE_A]),
    ("regardless of cost",    [RC_CREASE_B]),
    ("liquid metal hinge",    [shot("hinge-spine", zoom="out")]),
    ("015mm deep",            [mg(TC_CREASE, sfx=[dict(CORE, at=0.3)]),
                               face()]),
    ("anyways nobody",        [shot("unfold-hold")]),
    ("on the price",          [shot("caliper-hands")]),
    ("quo says",              [shot("cam-pair")]),
    ("2000 to 2500",          [mg(CHART_PRICE, sfx=[dict(POP, at=0.35)])]),
    ("ubs says 1800",         [FC_PRICING_A, FC_PRICING_B]),
    ("idc thinks",            [shot("caliper-edge")]),
    ("touch 3000",            [shot("face-close")]),
    ("is a leak",             [face()]),
    ("none of it",            [mg(TC_NOTHING)]),
    ("september 9th",         [mg(TC_SEPT, sfx=[dict(REVEAL, at=0.15)])]),
    ("carry a passport",      [face(headline=HL_CTA)]),
]

placed = region_bounds(regions, TOTAL)
scenes = [b(s0, round(s1 - s0, 2)) for (_, s0, s1, b) in placed]
print(f"  {len(regions)} regions -> {len(scenes)} scenes")


def chunk(ws, size=3):
    out, buf = [], []
    for (s, e, w) in ws:
        buf.append((s, e, w))
        if len(buf) >= size or (re.search(r"[.,!?—:;]$", w) and len(buf) >= 2):
            out.append(buf); buf = []
    if buf: out.append(buf)
    return out


# Display-only fixes. Timings untouched. "Quo"->"Kuo" is a SPELLING fix only:
# whisper base AND small both write "Quo", which is the homophone of the
# correct English pronunciation of Kuo, so the TTS is right (RULES.md §11).
# "conflicts"->"configs" confirmed correct in the audio by whisper `small`.
FIX = {"stabby": "stubby", "Quo": "Kuo", "conflicts": "configs"}
# Positional fixes, keyed by START TIME rather than index: normalise_words()
# can change the token count, and an index-keyed map silently lands on the
# wrong word (it wrote "two 48MP" two tokens late on the first attempt).
TIME_FIX = {}
for i, (s, e, tx) in enumerate(words):
    if tx == "4" and i + 2 < len(words) and words[i + 1][2] == "to" \
            and words[i + 2][2] == "3":
        TIME_FIX[round(s, 2)] = "4:3"
        TIME_FIX[round(words[i + 1][0], 2)] = ""
        TIME_FIX[round(words[i + 2][0], 2)] = ""
    if tx == "248":                      # whisper heard "two 48" as one token
        TIME_FIX[round(s, 2)] = "two 48MP"
    if tx.lower() == "megapixel" and i > 0 and words[i - 1][2] == "248":
        TIME_FIX[round(s, 2)] = ""

caption_words = normalise_words(words, CANON)
fixed = []
for i, (s, e, t) in enumerate(caption_words):
    if round(s, 2) in TIME_FIX:
        t = TIME_FIX[round(s, 2)]
    else:
        for a, b in FIX.items():
            t = re.sub(rf"(?<![\w-]){re.escape(a)}(?![\w-])", b, t, flags=re.I)
    fixed.append((s, e, t))

captions = []
for grp in chunk([f for f in fixed if f[2]]):
    text = normalise(" ".join(w[2] for w in grp), CANON)
    per = [{"t": round(w[0], 2), "text": normalise(w[2], CANON)} for w in grp]
    captions.append({"start": round(grp[0][0], 2), "end": round(grp[-1][1], 2),
                     "text": text, "words": [p for p in per if p["text"]]})

music = {
    "src": "music/bed-02.mp3", "from": 8.0,
    "points": [
        {"t": 0.0, "vol": 0.15},
        {"t": 9.0, "vol": 0.08},
        {"t": TOTAL * 0.68, "vol": 0.14},
        {"t": TOTAL - 0.9, "vol": 0.13},
        {"t": TOTAL, "vol": 0.02},
    ],
}

beats = {
    "id": SLUG, "fps": 30, "width": 1080, "height": 1920, "style": "varun",
    "format": "news",
    "audio": AVATAR, "music": music,
    "captionStyle": "nick-display",
    # G22: one highlight per caption beat — "shorter" and "wider" land in the
    # same chunk, so only one of them may be an emphasis word.
    "emphasis": ["7.76", "5.49", "4.5mm", "0.15mm", "48MP", "$2,000", "$2,500",
                 "$1,800", "$3,000", "wider", "passport"],
    "scenes": scenes, "captions": captions,
    "script": (ROOT / f"jobs/{SLUG}/script.md").read_text(),
    "approval": json.loads((ROOT / f"jobs/{SLUG}/approval.json").read_text()),
}

def _dur(path: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True).stdout.strip())


CLIP_DURS = {f"{C}/{f.name}": _dur(f)
             for f in sorted((ROOT / "public" / C).glob("*.mp4"))}

total = round(sum(s["durationSec"] for s in scenes), 2)
print(f"scenes {total:.2f}s vs reel {TOTAL:.2f}s (delta {total - TOTAL:+.2f}s)")

try:
    for w in check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST,
                         clip_durations=CLIP_DURS):
        print(f"  warning: {w}")
    print("GATES: PASSED")
except GateError as e:
    raise SystemExit(f"GATES FAILED — beat sheet NOT written\n{e}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(beats, indent=2, ensure_ascii=False))
print("wrote", OUT)
