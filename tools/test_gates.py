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
    LUFS_TARGET,
    RUNTIME_CEILING,
    TRUE_PEAK_CEILING,
    GateError,
    STYLE_ALIASES,
    STYLE_CANON,
    canon_caption,
    canon_style,
    check_beats,
    master_errors,
    parse_ebur128,
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

# Leading spaces ON PURPOSE: this is how whisper actually returns words
# (" Apple's"). The old clean-word fixture let a G21 bug hide for days — the
# gate stripped punctuation but not whitespace, so nothing ever matched.
VO_WORDS = [(" macOS", 0.0, 0.3), (" ships", 0.3, 0.7),
            # A word spoken OVER the specsheet (scene 4, 9.5-12.5s in the
            # baseline). G18 stopped being a flat 2.0s minimum on 2026-08-18 and
            # now asks whether the card outlasts the sentence, so the fixture
            # needs a sentence there to outlast. It ends at 12.0 — inside the
            # baseline card, so the clean sheet stays clean — and the G18 case
            # shortens the card to 1.2s so the claim outruns it.
            (" benchmark", 9.6, 12.0)]

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
def expect_gate(sheet: dict, gate: str, present: bool, label: str,
                vo_end: float | None = None) -> None:
    """Same detection semantics as expect_fail: raised OR advised both count.

    `vo_end` defaults to vo_end_of(sheet), which is derived FROM the sheet — so
    lengthening a scene moves the VO end with it and no tail is ever created.
    Any case about the tail has to pin the VO end independently (2026-08-22).
    """
    try:
        notes = check_beats(sheet,
                            vo_end=vo_end_of(sheet) if vo_end is None else vo_end,
                            manifest=MANIFEST,
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

# G01 — the tail rule is about a FROZEN PICTURE, not about silence. A final
# scene drawn by code (a CTA card typing its keyword) cannot freeze, and a
# comment-gate CTA needs a beat after the voice stops to be readable. Only
# generated scene types earn the longer tail; footage still freezes.
import copy as _copy
_tail_base = _copy.deepcopy(BASE)
_vo_end = sum(sc["durationSec"] for sc in _tail_base["scenes"]) - 0.45

_anim = _copy.deepcopy(_tail_base)
_anim["scenes"][-1] = {"type": "typecard", "durationSec":
                       _anim["scenes"][-1]["durationSec"] + 1.5,
                       "kinetic": {"text": "COMMENT APP", "style": "serif"}}
expect_gate(_anim, "G01", False,
            "G01 silent — a code-drawn final card may hold past the last word",
            vo_end=_vo_end)

_anim_far = _copy.deepcopy(_anim)
_anim_far["scenes"][-1]["durationSec"] += 2.0
expect_gate(_anim_far, "G01", True,
            "G01 fires — even an animated tail stops at 2.5s past the last word",
            vo_end=_vo_end)

# BASE ends on a `checklist`, which is itself code-drawn — so this case has to
# put a real footage scene last or it would be testing the animated branch again.
_frozen = _copy.deepcopy(_tail_base)
_frozen["scenes"][-1] = {"type": "footage",
                         "src": "assets/x/b-roll.mp4",
                         "zoomDir": "none",
                         "credit": "Acme",
                         "covers": "the last thing said",
                         "durationSec":
                         _tail_base["scenes"][-1]["durationSec"] + 1.5}
expect_gate(_frozen, "G01", True,
            "G01 fires — a FOOTAGE tail past the last word still freezes",
            vo_end=_vo_end)

_over = _at(RUNTIME_CEILING + 5)
_over.update(allowLong=True, allowLongReason="a genuinely enormous story")
expect_gate(_over, "G02", True,
            f"G02 fires — allowLong cannot pass the {RUNTIME_CEILING:.0f}s wall")


# --- G05's budget is DERIVED, and must stay tied to what it mirrors ----------
# It was a typed {"headline": 18} calibrated for Fraunces, and it went silently
# wrong the day the display face changed. Asserting the derivation here is what
# makes a future face change fail loudly instead of passing overflowing lines.
from reel_gates import LINE_MAX_CHARS as _BUDGET
_FIT_TS = (ROOT / "src/theme/fit.ts").read_text()
assert "export const ADVANCE = 0.655;" in _FIT_TS, (
    "src/theme/fit.ts ADVANCE changed — re-derive LINE_MAX_CHARS in reel_gates.py")
assert _BUDGET["headline"] == int((1080 * 0.88 - 140) / (100 * 0.655)), (
    "G05's headline budget no longer follows from the scale and the advance")
_counted("G05's char budget is derived from theme/fit.ts, not typed")


# --- G45 is a FLOOR, not a lane ---------------------------------------------
# Raising a caption to clear a face is composition and stays the author's call;
# the split hook of iphone-fold-ultra sets 1000 for exactly that reason. A gate
# that punished it would be teaching people to stop composing, which is how G21
# reached 100% false positives.
_raised = copy.deepcopy(BASE)
_raised["scenes"][1]["captionBottom"] = 1000
expect_gate(_raised, "G45", False,
            "G45 silent — a caption raised to 1000 to clear a face")

_floor = copy.deepcopy(BASE)
_floor["scenes"][1]["captionBottom"] = 500
expect_gate(_floor, "G45", False,
            "G45 silent — a caption exactly on the floor (500 = y 0.740)")
expect_gate(_floor, "G46", False,
            "G46 silent — a caption exactly on the floor is not advised against")

# The numbers both gates use are DERIVED from measurements that live elsewhere.
# Asserting them here is what stops the two copies drifting apart silently.
_ACCOUNT_ROW_Y = 0.835           # src/platformSafeArea.ts, measured off-device
assert round(1920 * (1 - _ACCOUNT_ROW_Y)) == 317, (
    "G45's platform floor no longer matches the measured account row")
_counted("G45's 317px floor still equals the measured account row at y 0.835")


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

def _footage0(sheet: dict) -> dict:
    """First `footage` scene in the sheet — the G48/G49 fields live only there,
    so a case must not land on the `split` hook or it would never fire."""
    return next(sc for sc in sheet["scenes"] if sc.get("type") == "footage")


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
    (lambda s: s.update(music=None), "G09", "no bed and no declared choice"),
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
    # The other half of the split: a SHORT card with nothing spoken over it is
    # not contradicting anything, so it advises rather than blocks. Without this
    # case the promotion would have quietly re-created the flat-minimum law it
    # was meant to replace.
    (lambda s: s["scenes"][8].update(durationSec=1.1),
     "G18a", "a short data card with no speech over it"),
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
     "G43", "a logo-build opener instead of motion at frame 0"),
    (lambda s: s["scenes"][0].__setitem__("hideCaptions", True),
     "G38", "a hook with no words on screen (mute-blind)"),
    # 2026-08-17, RULE 3: what is on screen must be what is being said.
    # scene 0 is `footage` — b-roll, so these are G44 (advice) now.
    (lambda s: s["scenes"][0].pop("covers"),
     "G44", "b-roll with no stated line"),
    (lambda s: s["scenes"][0].__setitem__("covers", "quarterly revenue guidance"),
     "G44", "b-roll claiming a line never spoken over it"),
    # A DOCUMENT on screen still blocks. It has to be scene 0: the fixture's
    # VO_WORDS covers only 0.0-0.7s, so a scene later in the timeline has no
    # speech over it and G39 correctly skips it — the first draft of this case
    # mutated the existing annotatezoom and could never fire.
    (lambda s: s["scenes"].__setitem__(0, {
        "credit": "@src", "type": "annotatezoom", "durationSec": 2.0,
        "src": "assets/x/doc.png", "srcWidth": 1080, "srcHeight": 2000,
        "focus": {"x": 40, "y": 100, "w": 900, "h": 500},
        "sfx": [{"src": "sfx/whoosh.MP3", "vol": 0.15}]}),
     "G39", "a document on screen with no stated claim"),
    # 2026-08-18, RULE 1. Both of these were in the SHIPPED iphone-fold-ultra:
    # seven scenes at 300, and the reel's own screenshot shows the caption
    # struck through the source credit.
    (lambda s: s["scenes"][1].__setitem__("captionBottom", 300),
     "G45", "a caption at y 0.844 — on Instagram's account row"),
    # 2026-08-19: credits can be turned off per reel, but never silently and
    # never as a bare switch.
    (lambda s: s.__setitem__("noCredits", {"reason": "client-supplied footage"}),
     "G47", "a reel that draws no credits says so"),
    (lambda s: s.__setitem__("noCredits", {"reason": "   "}),
     "G47", "noCredits set as a bare switch with no reason"),
    # 422 is the credit's own baseline: clear of the platform, on our credit.
    # It must ADVISE, not block — asserted here because the first draft of G45
    # blocked it, which put 183px of our own taste behind an R1 badge.
    (lambda s: s["scenes"][1].__setitem__("captionBottom", 422),
     "G46", "a caption on the credit lane but clear of the platform"),
    # 2026-08-20 — focusY + zoom, added for camera-snap cuts. G48 is RENDER:
    # each of these paints the black backdrop rather than the picture, which is
    # why it blocks. One case per failing field, since they are separate reads.
    (lambda s: _footage0(s).update(zoom=0.8),
     "G48", "zoom below 1 uncovers the canvas"),
    (lambda s: _footage0(s).update(focusY=1.4),
     "G48", "focusY outside 0..1"),
    (lambda s: _footage0(s).update(focusX=-0.2),
     "G48", "focusX outside 0..1"),
    # ADVICE, not a block: the base scale and the push multiply, so a snap that
    # meant to lock off at 1.6 drifts to 1.76. Legitimate if intended.
    (lambda s: _footage0(s).update(zoom=1.6, zoomDir="in"),
     "G49", "a locked-off zoom compounded by a push"),
]

# G50 (2026-08-25): the ai-tools evidence doctrine, measured — the corpus
# runs zero full-screen text scenes, so even one advises.
CASES.append((lambda s: (s.update(format="ai-tools"),
                         s["scenes"].__setitem__(10, {
                             "type": "typecard", "durationSec": 2.5,
                             "kinetic": {"lines": [{"text": "A CARD", "at": 0.2}]},
                             "sfx": [{"src": "sfx/Core.MP3", "vol": 0.14}]}))[0],
              "G50", "an ai-tools reel with a full-screen text card"))

# ai-tools (added 2026-08-25): CTA is constitutive — all 8 teardown reels
# carry a follow/comment gate — so declaring the format without one trips G24.
CASES.append((lambda s: s.update(format="ai-tools"),
              "G24", "ai-tools reel with no CTA scene"))

for mutate, gate, label in CASES:
    expect_fail(mutate, gate, label)

# G09 INVERTED 2026-08-22 (user directive): background music is optional, so
# `noMusic: true` ALONE — no reason — must now be silent. The old suite
# asserted the opposite; this is the negative case that keeps the inversion
# from quietly reverting in a future merge (the 2026-08-17 two-machine sync
# nearly dropped the opt-out once already).
_s = copy.deepcopy(BASE)
_s.update(music=None, noMusic=True)
try:
    _adv = check_beats(_s, vo_end=vo_end_of(_s), manifest=MANIFEST,
                       vo_words=VO_WORDS)
    _hits = [a for a in _adv if "G09" in a]
except GateError as _e:
    _hits = [a for a in (list(_e.advice) + [str(_e)]) if "G09" in str(a)]
if _hits:
    print(f"  FAIL G09 fired on a declared music-free reel: {_hits[0][:90]}")
    raise SystemExit(1)
_counted("G09 silent — noMusic:true needs no reason (music is optional)")


# ── G31, the finished master ────────────────────────────────────────────────
# The only gate that measures an ARTIFACT rather than the beat sheet, so it
# gets its own harness: check_beats never sees it, and the numbers below are
# real measurements off out/apple-pay-india-raw.mp4 (2026-08-17) rather than
# invented ones.
def expect_master_fail(integrated: float, true_peak: float, label: str) -> None:
    errs = master_errors(integrated, true_peak)
    if any("G31" in e for e in errs):
        _fired.append(("G31", label))
        _counted(f"G31 fires — {label}")
        return
    print(f"  FAIL G31 did NOT fire for {label} "
          f"(I={integrated}, TP={true_peak}); got: {errs}")
    raise SystemExit(1)


def expect_master_pass(integrated: float, true_peak: float, label: str) -> None:
    errs = master_errors(integrated, true_peak)
    if errs:
        print(f"  FAIL {label} — should have passed:\n    " +
              "\n    ".join(errs))
        raise SystemExit(1)
    _counted(label)


# This is the exact miss that was shipping: render_job.py mastered in ONE
# loudnorm pass, which undershoots by design and never applies the offset it
# has already measured.
expect_master_fail(-15.2, -1.0, "single-pass master lands 1.2 LU under target")
expect_master_fail(-12.5, -1.0, "master 1.5 LU OVER target (tolerance is both ways)")
expect_master_fail(-14.2, -0.4, "true peak over the ceiling — clips on re-encode")
expect_master_fail(float("-inf"), float("-inf"), "silent master")
# What the two-pass chain actually delivered on the same raw file.
expect_master_pass(-14.2, -1.0, "G31 silent — two-pass master at -14.2 LUFS")
expect_master_pass(LUFS_TARGET, TRUE_PEAK_CEILING,
                   "G31 silent — exactly on target, exactly at the TP ceiling")

# The parser must read the SUMMARY, never the running per-frame line, which
# carries the same label with a different (mid-file) value. Sample is real
# ffmpeg output, trimmed.
_EBUR_SAMPLE = """[Parsed_ebur128_0 @ 0x7f] t: 100.81 TARGET:-23 LUFS    M: -17.5 S: -13.7     I: -99.9 LUFS       LRA:   2.4 LU  FTPK: -37.2 dBFS  TPK:  -9.9  -9.9 dBFS
[Parsed_ebur128_0 @ 0x7f] Summary:

  Integrated loudness:
    I:         -14.2 LUFS
    Threshold: -24.7 LUFS

  Loudness range:
    LRA:         3.1 LU

  True peak:
    Peak:       -1.0 dBFS
"""
_i, _tp = parse_ebur128(_EBUR_SAMPLE)
if (_i, _tp) != (-14.2, -1.0):
    raise SystemExit(f"  FAIL parse_ebur128 read {(_i, _tp)}, want (-14.2, -1.0) "
                     "— it must read the Summary block, not a per-frame line")
_counted("parse_ebur128 reads the summary, not the running per-frame values")

# `-v error` hides loudnorm/ebur128 statistics entirely. An unreadable
# measurement must FAIL, never silently pass — that is the exact shape of the
# Pillow bug this repo was rebuilt around.
try:
    parse_ebur128("ffmpeg version 8.0\nframe= 3025 fps=1163\n")
except GateError as _e:
    if "G31" not in str(_e):
        raise SystemExit(f"  FAIL empty ebur128 output raised without G31: {_e}")
    _counted("G31 fires — ffmpeg output carried no ebur128 summary to read")
else:
    raise SystemExit("  FAIL parse_ebur128 accepted output with no summary — "
                     "an unreadable measurement must never pass as clean")

# ---- G41 / G42: capture provenance and source tier ------------------------
# These need a MUTATED MANIFEST rather than a mutated sheet, because the facts
# live with the asset, not the scene. Same block-vs-advise assertion as
# expect_fail, so a gate cannot quietly change which side it is on.
def expect_manifest(man: dict, gate: str, label: str, want_text: str = "") -> None:
    sheet = copy.deepcopy(BASE)
    try:
        notes = check_beats(sheet, vo_end=vo_end_of(sheet), manifest=man,
                            vo_words=VO_WORDS)
    except GateError as e:
        hit = [gate in str(e), any(gate in a for a in e.advice)]
        if hit[0]:
            if gate not in BLOCKING_RULES:
                print(f"  FAIL {gate} blocked but is not in BLOCKING_RULES ({label})")
                raise SystemExit(1)
            if want_text and want_text not in str(e):
                print(f"  FAIL {gate} fired without {want_text!r} ({label})")
                raise SystemExit(1)
            _fired.append((gate, label)); _counted(f"{gate} blocks — {label}"); return
        if hit[1] and gate not in BLOCKING_RULES:
            _fired.append((gate, label)); _counted(f"{gate} advises — {label}"); return
        print(f"  FAIL {gate} did not fire for {label}; got:\n{e}")
        raise SystemExit(1)
    if any(gate in n for n in notes):
        if gate in BLOCKING_RULES:
            print(f"  FAIL {gate} is in BLOCKING_RULES but only advised ({label})")
            raise SystemExit(1)
        if want_text and not any(want_text in n for n in notes):
            print(f"  FAIL {gate} advised without {want_text!r} ({label})")
            raise SystemExit(1)
        _fired.append((gate, label)); _counted(f"{gate} advises — {label}"); return
    print(f"  FAIL {gate} did NOT detect {label}")
    raise SystemExit(1)


expect_manifest(
    {"assets": [{"id": "clip-b", "tier": "official",
                 "capture": {"mobile": False, "viewport": {"width": 1200},
                             "desktopReason": None}},
                {"id": "clip-banned"}],
     "banned_assets": ["clip-banned"]},
    "G41", "a desktop capture with no recorded reason")

# No tier at all — a legitimate desktop capture, but nothing recorded about
# WHERE it came from. (The first draft of this case gave the asset a tier and
# then expected the "records no tier" message, which of course never came.)
expect_manifest(
    {"assets": [{"id": "clip-b",
                 "capture": {"mobile": False, "viewport": {"width": 1200},
                             "desktopReason": "spec table has no mobile layout"}},
                {"id": "clip-banned"}],
     "banned_assets": ["clip-banned"]},
    "G42", "a source with no tier recorded", want_text="record no tier")

expect_manifest(
    {"assets": [{"id": "clip-b", "tier": "fallback",
                 "capture": {"mobile": True, "desktopReason": None}},
                {"id": "clip-banned"}],
     "banned_assets": ["clip-banned"]},
    "G42", "a fallback-tier source", want_text="fallback")


# The suite printed "every gate fires on its violation" while G13 and G16 had
# no failing case at all (found 2026-08-17). Uniqueness of ids was asserted;
# COVERAGE never was. Assert the claim the last line makes.
# Collect declared ids from the COMMENT convention *and* from every id the
# module actually emits. The comment-only scan depended on a house style: adding
# "# G41 (Rule 2) + G42 (advice) — ..." made BOTH ids invisible to coverage, so
# they needed no test case and the suite still claimed full coverage. A gate must
# not be able to hide by writing its comment differently.
_declared = set(re.findall(r'^\s*# (G\d\d) — ', _src, re.M))
_declared |= set(re.findall(r'["\']\s*(G\d\d) ', _src))
_declared |= set(re.findall(r'f"(G\d\d) ', _src))
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
