#!/usr/bin/env python3
"""Self-test for reel_gates: prove every gate actually fires.

A gate that never triggers is worse than no gate — it buys false confidence.
This takes a known-good beat sheet, mutates it one rule at a time, and asserts
the matching gate id appears in the raised error.

    python3 tools/test_gates.py
"""
from __future__ import annotations

import copy
import hashlib
import re
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import check_beats, GateError  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def good() -> dict:
    """A minimal sheet that passes every gate."""
    face = "assets/x/avatar-master-169.mp4"
    scenes = [
        {"type": "logoassemble", "durationSec": 2.0,
         "sfx": [{"src": "sfx/whoosh.MP3", "vol": 0.15},
                 {"src": "sfx/Camera Shutter.MP3", "vol": 0.16}]},
        {"credit": "@src", "type": "split", "durationSec": 2.5, "topSrc": "assets/x/clips/a.mp4",
         "bottomSrc": face},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/b.mp4",
         "assetId": "clip-b", "sfx": [{"src": "sfx2/whooshes-01.mp3", "vol": 0.12}]},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/c.mp4",
         "sfx": [{"src": "sfx2/whooshes-01.mp3", "vol": 0.12}]},
        {"type": "specsheet", "footnote": "src", "durationSec": 3.0,
         "sfx": [{"src": "sfx/Core.MP3", "vol": 0.14}]},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/d.mp4",
         "sfx": [{"src": "sfx2/whooshes-01.mp3", "vol": 0.12}]},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/e.mp4",
         },
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/f.mp4",
         "sfx": [{"src": "sfx/whoosh.MP3", "vol": 0.16}]},
        {"type": "chart", "source": "src", "durationSec": 3.0,
         "sfx": [{"src": "sfx/Core.MP3", "vol": 0.14}]},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/g.mp4"},
        {"type": "wordcascade", "durationSec": 2.5, "bg": "cream"},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/h.mp4"},
        # facecam block ~14% of a 65s runtime
        {"type": "footage", "durationSec": 2.5, "src": face},
        {"type": "footage", "durationSec": 2.5, "src": face},
        {"type": "footage", "durationSec": 2.5, "src": face},
        {"type": "footage", "durationSec": 2.4, "src": face,
         "headline": {"lines": [
             {"text": "30 sec · one pass · with sound", "kind": "label", "at": 0.1},
             {"text": "would you hand it", "kind": "headline", "at": 0.5},
         ], "y": 0.07}},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/i.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/j.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/k.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/l.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/m.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.5, "src": "assets/x/clips/n.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.6, "src": "assets/x/clips/o.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.6, "src": "assets/x/clips/p.mp4"},
        {"credit": "@src", "type": "footage", "durationSec": 2.6, "src": "assets/x/clips/q.mp4"},
        {"type": "settingspane", "durationSec": 3.0, "title": "Cellular",
         "focus": "0.0", "focusAt": 0.5,
         "groups": [{"rows": [
             {"label": "Cellular Data", "toggle": True, "on": True,
              "flipAt": 1.2},
             {"label": "Personal Hotspot", "value": "Off"}]}]},
        {"credit": "@src", "type": "annotatezoom", "durationSec": 2.5,
         "src": "assets/x/ui.png", "srcWidth": 2560, "srcHeight": 1440,
         "focus": {"x": 900, "y": 500, "w": 700, "h": 420}},
        {"credit": "@src", "type": "sourceread", "durationSec": 2.5,
         "src": "assets/x/src.png", "srcWidth": 1080, "srcHeight": 2340,
         "lines": [{"at": 0.2, "x": 40, "y": 200, "w": 900, "h": 60}]},
        {"type": "checklist", "durationSec": 2.5, "stagger": 0.5,
         "sfx": [{"src": "sfx/Pop.MP3", "vol": 0.12}],
         "rows": [{"label": "macOS", "state": "done"},
                  {"label": "Free Grok", "state": "no"},
                  {"label": "Android", "state": "q"}]},
    ]
    return {
        "id": "selftest", "fps": 30, "width": 1080, "height": 1920,
        "captionStyle": "nick-display",
        "tone": "warm", "avatarRegister": "warm",
        "emphasis": ["30"],
        "captions": [{"start": 0, "end": 1, "text": "macOS ships"}],
        "script": SCRIPT,
        "approval": {"sha256": SCRIPT_SHA, "approvedAt": "2026-08-12T00:00:00+00:00"},
        "music": {"src": "music/bed-02.mp3",
                  "points": [{"t": 0, "vol": 0.15}, {"t": 60, "vol": 0.02}]},
        "scenes": scenes,
    }


SCRIPT = "macOS ships today and that changes the maths."
SCRIPT_SHA = hashlib.sha256(" ".join(SCRIPT.split()).encode()).hexdigest()

VO_WORDS = [("macOS", 0.0, 0.3), ("ships", 0.3, 0.7)]

MANIFEST = {"assets": [{"id": "clip-b"}, {"id": "clip-banned"}],
            "banned_assets": ["clip-banned"]}


def pane(sheet: dict) -> dict:
    """The baseline's settingspane scene, found by type."""
    return next(s for s in sheet["scenes"] if s["type"] == "settingspane")


def chk(sheet: dict) -> dict:
    """The baseline's checklist scene, found by type so inserts can't shift it."""
    return next(s for s in sheet["scenes"] if s["type"] == "checklist")


def vo_end_of(sheet: dict) -> float:
    """VO end that satisfies G01 exactly for this sheet."""
    return round(sum(s["durationSec"] for s in sheet["scenes"]) - 0.35, 2)


def expect_pass(sheet: dict, label: str) -> None:
    try:
        check_beats(sheet, vo_end=vo_end_of(sheet), manifest=MANIFEST,
                    vo_words=VO_WORDS)
        print(f"  ok   {label}")
    except GateError as e:
        print(f"  FAIL {label} — should have passed:\n{e}")
        raise SystemExit(1)


def expect_fail(mutate, gate: str, label: str) -> None:
    sheet = copy.deepcopy(BASE)
    vo = vo_end_of(sheet)          # capture BEFORE mutation where relevant
    mutate(sheet)
    try:
        check_beats(sheet, vo_end=vo, manifest=MANIFEST,
                    vo_words=VO_WORDS)
    except GateError as e:
        if gate in str(e):
            print(f"  ok   {gate} fires — {label}")
            return
        print(f"  FAIL {gate} did not fire for {label}; got:\n{e}")
        raise SystemExit(1)
    print(f"  FAIL {gate} did NOT fire for {label} (no error raised)")
    raise SystemExit(1)


BASE = good()


def top5(sheet: dict) -> dict:
    """The baseline re-cut as a top5 reel: shorter, quieter cues, with a CTA."""
    s = copy.deepcopy(sheet)
    s["format"] = "top5"
    # trim to the 26-48s band
    s["scenes"] = s["scenes"][:14]
    for sc in s["scenes"]:
        for c in (sc.get("sfx") or []):
            c["vol"] = 0.08                      # nick's pops are quieter
    s["scenes"].append({"type": "commentcta", "durationSec": 2.0})
    return s


def comparison(sheet: dict) -> dict:
    """The baseline re-cut as a balanced, labelled comparison reel."""
    s = copy.deepcopy(sheet)
    s["format"] = "comparison"
    s["sides"] = ["iPhone 18", "iPhone 17"]
    face = "assets/x/avatar-master-169.mp4"
    # three labelled compare scenes + an even single-sided split
    s["scenes"][2] = {"credit": "@src", "type": "comparesplit", "durationSec": 2.5,
                      "leftSrc": "assets/x/clips/b.mp4",
                      "rightSrc": "assets/x/clips/c.mp4",
                      "leftLabel": "iPhone 18", "rightLabel": "iPhone 17",
                      "side": "both",
                      "sfx": [{"src": "sfx2/whooshes-01.mp3", "vol": 0.12}]}
    for sc in s["scenes"]:
        if sc["type"] == "footage" and face not in str(sc.get("src", "")):
            sc.setdefault("side", "a")
    # even the two sides up
    singles = [sc for sc in s["scenes"] if sc.get("side") in ("a", "b")]
    for i, sc in enumerate(singles):
        sc["side"] = "a" if i % 2 == 0 else "b"
    s["scenes"].append({"type": "endquestion", "durationSec": 2.0})
    return s


# A duplicate gate ID silently makes two rules indistinguishable in output and
# in these tests — on 2026-08-14 a new gate was numbered G30 when G30 already
# existed, and the suite still went green.
_src = (Path(__file__).resolve().parent / "reel_gates.py").read_text()
_ids = re.findall(r'^\s*# (G\d\d) — ', _src, re.M)
_dupes = {i for i in _ids if _ids.count(i) > 1}
if _dupes:
    raise SystemExit(f"  FAIL duplicate gate id(s): {sorted(_dupes)}")
print(f"  ok   {len(_ids)} gate ids, all unique")

print("=== reel_gates self-test ===")
expect_pass(BASE, "baseline sheet passes cleanly")
expect_pass(top5(BASE), "top5 profile: 26-48s + quiet cues + CTA passes")
expect_pass(comparison(BASE), "comparison profile: labelled, balanced, 3+ compares")

_neutral = copy.deepcopy(BASE)
_neutral.update(tone="serious", avatarRegister="neutral")
expect_pass(_neutral, "G19: a neutral twin may deliver a serious script")

TOP5 = top5(BASE)
CMP = comparison(BASE)

CASES = [
    (lambda s: s["scenes"][-1].update(durationSec=9.0), "G01", "tail runs past the VO"),
    (lambda s: s["scenes"].__setitem__(slice(3, None), []), "G02", "runtime under 60s"),
    (lambda s: s["scenes"][0].update(durationSec=3.0), "G03", "hook held 3s"),
    (lambda s: s["scenes"][4].update(durationSec=4.0), "G04", "specsheet over 3.3s"),
    (lambda s: s["scenes"][4].update(type="priceladder", title="X",
        rows=[{"label": "A", "oldPrice": "$1", "newPrice": "$2"}],
        durationSec=4.0), "G04", "priceladder over 3.3s (building class)"),
    (lambda s: s["scenes"][15]["headline"]["lines"][0].update(
        text="thirty seconds. one pass. with sound."), "G05", "label 37 chars"),
    (lambda s: [sc.update(src="assets/x/avatar-master-169.mp4")
                for sc in s["scenes"][:12] if sc["type"] == "footage"],
     "G06", "facecam over 20%"),
    (lambda s: s["scenes"][3].update(src="assets/x/clips/b.mp4"), "G07", "clip reused"),
    (lambda s: [sc.pop("sfx", None) for sc in s["scenes"][:6]],
     "G08", "too few SFX cues"),
    (lambda s: [sc.update(sfx=[{"src": "sfx/Pop.MP3", "vol": 0.13}])
                for sc in s["scenes"]], "G08", "a cue on every cut"),
    (lambda s: s["scenes"][2]["sfx"][0].update(vol=0.45), "G08", "SFX too loud"),
    # ── SFX placement (G28) ──────────────────────────────────────────────
    (lambda s: s["scenes"][2]["sfx"][0].update(src="sfx/Whoosh-typo.MP3"),
     "G28", "SFX filename not in the catalogue (would render silent)"),
    (lambda s: s["scenes"][2]["sfx"][0].update(src="sfx/Magic Reveal.MP3"),
     "G28", "reveal cue on a plain footage beat"),
    (lambda s: s["scenes"][4]["sfx"][0].update(src="sfx/Vine Boom.MP3"),
     "G28", "comedic sting in a news reel"),
    # scene 9 is followed by wordcascade + plain footage — nothing to pay off
    (lambda s: s["scenes"][9].__setitem__(
        "sfx", [{"src": "sfx2/risers-01.mp3", "vol": 0.15}]),
     "G28", "riser with no payoff in the next 3 beats"),
    (lambda s: s.update(music=None), "G09", "no music bed"),
    (lambda s: s["music"].update(points=[{"t": 0, "vol": 0.1},
                                         {"t": 60, "vol": 0.1}]), "G09", "flat bed"),
    (lambda s: s.update(emphasis=[]), "G10", "empty emphasis"),
    (lambda s: s["scenes"][2].update(assetId="clip-nope"), "G11", "unknown assetId"),
    (lambda s: s["scenes"][2].update(assetId="clip-banned"), "G11", "banned assetId"),
    (lambda s: s["scenes"].insert(1, {"credit": "@src", "type": "footage",
        "durationSec": 2.5, "src": "assets/x/clips/zz1.mp4"}) or
               s["scenes"].insert(1, {"credit": "@src", "type": "footage",
        "durationSec": 2.5, "src": "assets/x/clips/zz2.mp4"}),
     "G17", "presenter appears after 5s"),
    (lambda s: s["scenes"][4].update(durationSec=1.2) or
               s["scenes"][-1].update(durationSec=s["scenes"][-1]["durationSec"] + 1.8),
     "G18", "data card vanishes mid-claim"),
    (lambda s: s["scenes"][-1].update(headline={"lines": [
        {"text": "TELL ME BELOW", "kind": "headline", "at": 0.3}], "y": 0.07}),
     "G32", "outro caption stranded at the top of the frame"),
    (lambda s: [c.update(src="sfx/whoosh.MP3")
                for sc in s["scenes"] for c in (sc.get("sfx") or [])],
     "G33", "the whole reel scored with one sound"),
    (lambda s: pane(s).update(focusAt=3.0), "G25", "settings spotlight never lands"),
    (lambda s: pane(s)["groups"][0]["rows"][0].update(flipAt=2.9),
     "G25", "settings toggle never flips"),
    (lambda s: pane(s).update(groups=[]), "G25", "settings pane with no rows"),
    (lambda s: s.pop("approval"), "G27", "script never approved"),
    (lambda s: s.update(script=SCRIPT + " Also, buy my course."),
     "G27", "script edited after approval"),
    (lambda s: s.pop("script"), "G27", "sheet carries no script"),
    # ── comparison structure ─────────────────────────────────────────────
    (lambda s: s.clear() or s.update(copy.deepcopy(CMP)) or s.pop("sides"),
     "G26", "comparison with no declared sides"),
    (lambda s: s.clear() or s.update(copy.deepcopy(CMP)) or
               [sc.__setitem__("side", "a") for sc in s["scenes"]
                if sc.get("side") == "b"],
     "G26", "one product hogs the screen time"),
    (lambda s: s.clear() or s.update(copy.deepcopy(CMP)) or
               next(sc for sc in s["scenes"]
                    if sc["type"] == "comparesplit").pop("rightLabel"),
     "G26", "unlabelled comparison split"),
    (lambda s: s.clear() or s.update(copy.deepcopy(CMP)) or
               s.__setitem__("scenes", [sc for sc in s["scenes"]
                                        if sc["type"] not in
                                        ("comparesplit", "specsheet", "chart")]),
     "G26", "a 'comparison' that never compares"),
    # ── format profiles ──────────────────────────────────────────────────
    (lambda s: s.update(format="how-to"), "G23", "format with no measured profile"),
    (lambda s: s.update(format="top5"), "G02",
     "news-length reel declared as top5 (over the 48s ceiling)"),
    (lambda s: TOP5.__setitem__("scenes", TOP5["scenes"][:-1]) if False else
               s.clear() or s.update(copy.deepcopy(TOP5)) or
               s.__setitem__("scenes", s["scenes"][:-1]),
     "G24", "top5 reel with no CTA"),
    (lambda s: s.clear() or s.update(copy.deepcopy(TOP5)) or
               [c.update(vol=0.15) for sc in s["scenes"] for c in (sc.get("sfx") or [])],
     "G08", "varun-loud SFX in a top5 reel"),
    (lambda s: next(x for x in s["scenes"] if x["type"] == "annotatezoom")
               .pop("focus"),
     "G29", "wide desktop capture fitted whole instead of cropped"),
    (lambda s: next(x for x in s["scenes"] if x["type"] == "sourceread")
               .update(srcWidth=1200, srcHeight=900),
     "G29", "desktop capture in a sourceread"),
    (lambda s: next(x for x in s["scenes"] if x["type"] == "sourceread")
               .update(srcWidth=540, srcHeight=1170),
     "G29", "mobile capture at too low a scale"),
    (lambda s: chk(s).update(stagger=1.4),
     "G20", "last list row never lands"),
    (lambda s: chk(s).update(rows=[]), "G20", "empty checklist"),
    (lambda s: s.update(allowLong=True), "G02", "allowLong with no reason"),
    (lambda s: s.update(captions=[{"start": 0, "end": 1, "text": "Windows ships"}]),
     "G21", "caption word never spoken"),
    (lambda s: s.update(emphasis=["macOS", "ships"]),
     "G22", "two highlights in one beat"),
    (lambda s: s.update(captions=[{"start": 0, "end": 1,
                                   "text": "Pegatron T, one of"}]),
     "G34", "orphan single-letter TTS artifact in a caption"),
    (lambda s: s.update(captions=[{"start": 0, "end": 1,
                                   "text": "between $2 ,000 and"}]),
     "G30", "orphan numeric fragment in a caption"),
    (lambda s: s.update(avatarRegister="serious"),
     "G19", "serious face on a warm script"),
    (lambda s: s.update(avatarRegister="neutral"),
     "G19", "neutral face cannot sell a warm script"),
    (lambda s: s.update(tone="serious"),
     "G19", "serious script on the smiling look"),
    (lambda s: s.pop("avatarRegister", None),
     "G19", "tone declared with no look register"),
    (lambda s: s.update(tone="wry"), "G19", "unknown tone"),
    (lambda s: s["scenes"][2].pop("credit", None) or
               s["scenes"][2].update(credit=""), "G14", "borrowed footage with no credit"),
    (lambda s: s["scenes"][4].pop("footnote", None) or
               s["scenes"][4].update(source="", footnote=""), "G15", "data card with no source"),
    (lambda s: s["scenes"].__setitem__(10, {"type": "typecard", "durationSec": 2.5,
                                            "bg": "black"}) or
               s["scenes"].__setitem__(11, {"type": "typecard", "durationSec": 2.5,
                                            "bg": "black"}), "G12", "two black typecards"),
]

for mutate, gate, label in CASES:
    expect_fail(mutate, gate, label)

print(f"\nall {len(CASES) + 1} checks passed — every gate fires on its violation.")
