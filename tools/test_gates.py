#!/usr/bin/env python3
"""Self-test for reel_gates: prove every check detects its violation, and that
each one blocks or advises exactly as classified.

A check that never triggers is worse than none — it buys false confidence. This
takes a known-good beat sheet, mutates it one rule at a time, and asserts the
matching id turns up.

Since 2026-08-17 only three standing rules (plus render correctness and rights)
may BLOCK; everything else is advice. So each case asserts two things: the check
detected the violation, and its block-or-advise behaviour matches BLOCKING_RULES.
A gate that quietly promoted itself to blocking now fails the suite.

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
from reel_gates import (  # noqa: E402
    BLOCKING_RULES,
    CAPTION_ALIASES,
    RUNTIME_CEILING,
    GateError,
    STYLE_ALIASES,
    STYLE_CANON,
    canon_caption,
    canon_style,
    check_beats,
)

ROOT = Path(__file__).resolve().parent.parent


def good() -> dict:
    """A minimal sheet that passes every gate."""
    face = "assets/x/avatar-master-169.mp4"
    scenes = [
        # G38: the hook opens on MOTION with words on screen. This fixture used
        # to open on `logoassemble` — the same logo-build anti-pattern three
        # shipped reels had, which is why the baseline failed the moment the
        # gate existed.
        # Duration stays 2.0: the fixture timeline is measured off it, and
        # shortening it moved every later cue and broke the G17 case.
        # `footage`, NOT `split`: a split carries the face, and putting the
        # presenter at 0s made G17 ("presenter appears after 5s") unfireable.
        {"credit": "@src", "type": "footage", "durationSec": 2.0,
         "src": "assets/x/clips/hook.mp4",
         # G39: a scene that shows a SOURCE must name the line it illustrates,
         # and those words must be spoken while it is on screen.
         "covers": "macOS ships",
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
        "captionStyle": "word-reveal",
        "tone": "warm", "avatarRegister": "warm",
        "emphasis": ["30"],
        "captions": [{"start": 0, "end": 1, "text": "macOS ships"}],
        "script": SCRIPT,
        "approval": {"sha256": SCRIPT_SHA, "approvedAt": "2026-08-12T00:00:00+00:00"},
        # A DERIVED curve (G37): the shape tools/duck_music.py emits — open in
        # the gaps, ducked under each speech run, 4 points per run. The old
        # two-point fixture was itself an example of the bug G37 now blocks.
        "music": {"src": "music/bed-02.mp3",
                  "derivedFrom": "vo.json word timings (tools/duck_music.py)",
                  "points": [{"t": 0, "vol": 0.15},
                             {"t": 1.8, "vol": 0.15}, {"t": 2.0, "vol": 0.055},
                             {"t": 9.0, "vol": 0.055}, {"t": 9.34, "vol": 0.15},
                             {"t": 20.0, "vol": 0.15}, {"t": 20.2, "vol": 0.055},
                             {"t": 40.0, "vol": 0.055}, {"t": 40.34, "vol": 0.15},
                             {"t": 59.1, "vol": 0.15}, {"t": 60, "vol": 0.02}]},
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


# Every assertion increments this. The old total was `len(CASES) + 1`, which
# silently ignored the expect_pass cases and the gate-id check — adding a pass
# case did not move the number, so the suite under-reported its own coverage
# (noticed 2026-08-16 while adding the style-rename checks).
CHECKS = 0
_fired: list[tuple[str, str]] = []


def _counted(label: str) -> None:
    global CHECKS
    CHECKS += 1
    print(f"  ok   {label}")


def expect_pass(sheet: dict, label: str) -> None:
    try:
        check_beats(sheet, vo_end=vo_end_of(sheet), manifest=MANIFEST,
                    vo_words=VO_WORDS)
        _counted(label)
    except GateError as e:
        print(f"  FAIL {label} — should have passed:\n{e}")
        raise SystemExit(1)


def expect_fail(mutate, gate: str, label: str) -> None:
    """Assert the check DETECTS its violation.

    Since 2026-08-17 only the three standing rules (plus render correctness and
    rights) block a render; every other finding is advice. So "fires" now means
    the gate id appears EITHER in the raised error OR in the returned advice —
    detection is what is being tested, and whether it blocks is asserted
    separately against BLOCKING_RULES. Without this split the suite would have
    reported the advisory checks as dead the moment they stopped raising, and the
    obvious "fix" would have been to delete them.
    """
    sheet = copy.deepcopy(BASE)
    vo = vo_end_of(sheet)          # capture BEFORE mutation where relevant
    mutate(sheet)
    try:
        notes = check_beats(sheet, vo_end=vo, manifest=MANIFEST,
                            vo_words=VO_WORDS)
    except GateError as e:
        if gate in str(e) and gate in BLOCKING_RULES:
            pass
        elif any(gate in a for a in e.advice) and gate not in BLOCKING_RULES:
            # detected as advice, while something ELSE blocked this sheet
            _fired.append((gate, label))
            _counted(f"{gate} advises — {label}")
            return
        if gate in str(e):
            if gate not in BLOCKING_RULES:
                print(f"  FAIL {gate} BLOCKED a render but is not in "
                      f"BLOCKING_RULES ({label})")
                raise SystemExit(1)
            _fired.append((gate, label))
            _counted(f"{gate} blocks — {label}")
            return
        print(f"  FAIL {gate} did not fire for {label}; got:\n{e}")
        raise SystemExit(1)
    if any(gate in n for n in notes):
        if gate in BLOCKING_RULES:
            print(f"  FAIL {gate} is in BLOCKING_RULES but only advised "
                  f"({label})")
            raise SystemExit(1)
        _fired.append((gate, label))
        _counted(f"{gate} advises — {label}")
        return
    print(f"  FAIL {gate} did NOT detect {label} (no error, no advice)")
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
            c["vol"] = 0.08                      # utility pops are quieter
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
_counted(f"{len(_ids)} gate ids, all unique")

print("=== reel_gates self-test ===")
expect_pass(BASE, "baseline sheet passes cleanly")
expect_pass(top5(BASE), "top5 profile: 26-48s + quiet cues + CTA passes")
expect_pass(comparison(BASE), "comparison profile: labelled, balanced, 3+ compares")

_neutral = copy.deepcopy(BASE)
_neutral.update(tone="serious", avatarRegister="neutral")
expect_pass(_neutral, "G19: a neutral twin may deliver a serious script")

# --- style / caption RENAME (2026-08-16) ---------------------------------
# Ids describe the style, not its creator. The legacy creator ids must keep
# resolving forever: seven reels were published carrying them, and rewriting a
# shipped beat sheet to satisfy a rename is the retro-fixing RULES.md forbids.
for _legacy_id, _want in STYLE_ALIASES.items():
    if canon_style(_legacy_id) != _want:
        raise SystemExit(f"  FAIL style alias {_legacy_id!r} -> "
                         f"{canon_style(_legacy_id)!r}, expected {_want!r}")
for _legacy_id, _want in CAPTION_ALIASES.items():
    if canon_caption(_legacy_id) != _want:
        raise SystemExit(f"  FAIL caption alias {_legacy_id!r} -> "
                         f"{canon_caption(_legacy_id)!r}, expected {_want!r}")
# Canonical ids must be fixed points, or a second canonicalise would move them.
for _canon in STYLE_CANON:
    if canon_style(_canon) != _canon:
        raise SystemExit(f"  FAIL canonical style {_canon!r} is not idempotent")
if canon_caption("word-reveal") != "word-reveal":
    raise SystemExit("  FAIL canonical caption 'word-reveal' is not idempotent")
# An alias must never point at another alias (one hop only).
for _target in {**STYLE_ALIASES, **CAPTION_ALIASES}.values():
    if _target in STYLE_ALIASES or _target in CAPTION_ALIASES:
        raise SystemExit(f"  FAIL alias chain: {_target!r} is itself an alias")
_counted(f"{len(STYLE_ALIASES) + len(CAPTION_ALIASES)} legacy style/caption "
         f"ids resolve to canonical names")

_legacy_caps = copy.deepcopy(BASE)
_legacy_caps["captionStyle"] = "nick-display"
expect_pass(_legacy_caps, "G10: legacy 'nick-display' still passes as word-reveal")

_legacy_style = copy.deepcopy(BASE)
_legacy_style["style"] = "varun-mayya"
expect_pass(_legacy_style, "legacy style id 'varun-mayya' still passes")

# --- G02 runtime is topic-driven, but walled (user rule 2026-08-16) ---------
# The measured band is the DEFAULT; `allowLong` + a written reason buys room
# past it; RUNTIME_CEILING is the wall allowLong cannot pass.
#
# These assert on G02 SPECIFICALLY rather than on a whole clean sheet: making
# BASE legitimately 100s means repeating scenes, which trips G06/G07/G08 for
# reasons unrelated to runtime. A pass-the-whole-sheet test would be testing
# the fixture, not the rule.
def expect_gate(sheet: dict, gate: str, present: bool, label: str) -> None:
    """Same detection semantics as expect_fail: raised OR advised both count."""
    try:
        notes = check_beats(sheet, vo_end=vo_end_of(sheet), manifest=MANIFEST,
                            vo_words=VO_WORDS)
        fired = any(gate in n for n in notes)
    except GateError as e:
        fired = gate in str(e) or any(gate in a for a in e.advice)
    if fired is present:
        _counted(label)
        return
    print(f"  FAIL {label} — {gate} {'did not fire' if present else 'fired'}")
    raise SystemExit(1)


def _at(seconds: float) -> dict:
    """BASE with its last scene grown so the sheet totals `seconds`."""
    sheet = copy.deepcopy(BASE)
    sheet["scenes"][-1]["durationSec"] += seconds - sum(
        sc["durationSec"] for sc in sheet["scenes"])
    return sheet


expect_gate(_at(100.0), "G02", True,
            "G02 fires — 100s news reel with no allowLong")

_argued = _at(100.0)
_argued.update(allowLong=True,
               allowLongReason="three rulings, each needing its own receipt")
expect_gate(_argued, "G02", False,
            "G02 silent — 100s is allowed once the topic is argued for")

_over = _at(RUNTIME_CEILING + 5)
_over.update(allowLong=True, allowLongReason="a genuinely enormous story")
expect_gate(_over, "G02", True,
            f"G02 fires — allowLong cannot pass the {RUNTIME_CEILING:.0f}s wall")


# --- G13 needs clip_durations, which the shared expect_fail does not pass ---
def expect_fail_with_clips(sheet: dict, clips: dict, gate: str, label: str) -> None:
    try:
        check_beats(sheet, vo_end=vo_end_of(sheet), manifest=MANIFEST,
                    vo_words=VO_WORDS, clip_durations=clips)
    except GateError as e:
        if gate in str(e):
            _fired.append((gate, label))
            _counted(f"{gate} fires — {label}")
            return
        print(f"  FAIL {gate} did not fire for {label}; got:\n{e}")
        raise SystemExit(1)
    print(f"  FAIL {gate} did not fire for {label} (no error raised)")
    raise SystemExit(1)


_short_clip = copy.deepcopy(BASE)
_first_footage = next(
    sc for sc in _short_clip["scenes"] if sc.get("src") and "avatar-master" not in str(sc["src"])
)
expect_fail_with_clips(
    _short_clip,
    {_first_footage["src"]: _first_footage["durationSec"] - 0.6},
    "G13",
    "clip shorter than the beat that plays it")

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
     "G40", "reveal cue on a plain footage beat"),
    (lambda s: s["scenes"][4]["sfx"][0].update(src="sfx/Vine Boom.MP3"),
     "G40", "comedic sting in a news reel"),
    # scene 9 is followed by wordcascade + plain footage — nothing to pay off
    (lambda s: s["scenes"][9].__setitem__(
        "sfx", [{"src": "sfx2/risers-01.mp3", "vol": 0.15}]),
     "G40", "riser with no payoff in the next 3 beats"),
    (lambda s: s.update(music=None), "G09", "no music bed"),
    (lambda s: s.update(music=None, noMusic=True),
     "G09", "noMusic switched on with no written reason"),
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
     "G08", "editorial-loud SFX in a top5 reel"),
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
    (lambda s: s["captions"].append(
        {"start": 1, "end": 2, "text": "it costs 85 % more"}),
     "G16", "caption not in standard notation ('85 %')"),
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
    # 2026-08-17, ios27-tiers: both of these shipped into a render that passed
    # every existing gate AND the frame linter.
    (lambda s: s["scenes"].__setitem__(2, dict(s["scenes"][2], type="footage",
                                               src="assets/x/clips/still.png")),
     "G35", "a still handed to `footage` (renders black)"),
    (lambda s: s["scenes"].__setitem__(3, {
        "type": "annotatezoom", "durationSec": 2.2,
        "src": "assets/x/clips/strip.png", "srcWidth": 942, "srcHeight": 205,
        "credit": "Apple", "assetId": "receipt-x",
        "focus": {"x": 20, "y": 5, "w": 900, "h": 195},
        "annotations": [{"kind": "underline", "at": 0.5,
                         "x": 30, "y": 40, "w": 700, "h": 26}]}),
     "G36", "a 4.6:1 strip in annotatezoom (84% dead space)"),
    # 2026-08-17: the hand-written music curve. Every shipped reel had one, and
    # every one of them was measurably not ducking.
    (lambda s: s.__setitem__("music", {"src": "music/bed-02.mp3", "from": 0.0,
                                       "points": [{"t": 0.0, "vol": 0.15},
                                                  {"t": 8.0, "vol": 0.08},
                                                  {"t": 40.0, "vol": 0.14}]}),
     "G37", "a hand-written music curve (no derivedFrom)"),
    (lambda s: s.__setitem__("music", {"src": "music/bed-02.mp3", "from": 0.0,
                                       "derivedFrom": "vo.json word timings",
                                       "points": [{"t": 0.0, "vol": 0.15},
                                                  {"t": 40.0, "vol": 0.05}]}),
     "G37", "a curve CLAIMING to be derived but with 2 points"),
    # 2026-08-17, from the going-viral skill. Three shipped reels opened this way.
    (lambda s: s["scenes"].__setitem__(0, {"type": "logoassemble",
                                           "durationSec": 1.9,
                                           "viewBox": "0 0 1024 1024",
                                           "paths": [{"d": "M0 0"}], "size": 500}),
     "G38", "a logo-build opener instead of motion at frame 0"),
    (lambda s: s["scenes"][0].__setitem__("hideCaptions", True),
     "G38", "a hook with no words on screen (mute-blind)"),
    # 2026-08-17, RULE 3: what is on screen must be what is being said.
    (lambda s: s["scenes"][0].pop("covers"),
     "G39", "a source on screen with no stated line"),
    (lambda s: s["scenes"][0].__setitem__("covers", "quarterly revenue guidance"),
     "G39", "a source claiming a line that is never spoken over it"),
]

for mutate, gate, label in CASES:
    expect_fail(mutate, gate, label)

# The suite printed "every gate fires on its violation" while G13 and G16 had
# no failing case at all (found 2026-08-17). Uniqueness of ids was asserted;
# COVERAGE never was. Assert the claim the last line makes.
_declared = set(re.findall(r'^\s*# (G\d\d) — ', _src, re.M))
_covered = {g for g, _l in _fired}
_gap = sorted(_declared - _covered)
if _gap:
    raise SystemExit(
        f"  FAIL {len(_gap)} gate(s) have no failing case: {_gap}\n"
        f"  Every mechanical rule is a gate WITH a self-test (CLAUDE.md). A gate\n"
        f"  that never fires in the suite is untested, and this line would\n"
        f"  otherwise claim it was.")
_counted(f"coverage: all {len(_declared)} gate ids have a failing case")

print(f"\nall {CHECKS} checks passed — every check detects its violation, "
      "and blocks or advises exactly as BLOCKING_RULES classifies it.")
