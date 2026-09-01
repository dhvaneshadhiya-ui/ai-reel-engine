#!/usr/bin/env python3
"""Blocking gates for a reel beat sheet.

WHY THIS EXISTS
---------------
STYLE-RULES.md is 600+ lines of prose. Prose rules get skipped — the pacing
"rule" printed a FAIL for weeks without ever failing a build, and the frame
linter silently disabled its own pixel checks because Pillow was missing and
nobody read the [SKIP] line.

So: every rule that can be checked mechanically lives HERE, as code that
raises. Rules that genuinely need eyes stay in RULES.md marked [EYE].

Usage from a build script, after `scenes` and `beats` are assembled:

    from reel_gates import check_beats, GateError
    check_beats(beats, vo_end=words[-1][1], manifest=MANIFEST)   # raises

Or standalone against an already-built sheet:

    python3 tools/reel_gates.py seedance-25
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notation import normalise, violations  # noqa: E402
from sfx_library import (CATALOGUE as SFX_CAT, ROLE_FITS, ROLE_MAX,  # noqa: E402
                         COMEDIC_OK_FORMATS, COMEDIC_BLOCKED_TONES, SFX_DIR)

ROOT = Path(__file__).resolve().parent.parent


class GateError(Exception):
    """A blocking rule was violated. The build must not continue.

    Carries `advice` — the non-blocking findings from the same run. Without this
    a blocking error DISCARDED every piece of craft advice computed alongside it,
    so the author fixed one hard rule, re-ran, and only then saw the notes. Worse,
    the self-test could not see an advisory gate whose case also tripped a
    blocking one, and would have reported it as dead.
    """

    def __init__(self, message: str, advice: list[str] | None = None) -> None:
        super().__init__(message)
        self.advice = advice or []


# ── tunables, every one traceable to a dated ledger entry ────────────────────
# ── FORMAT PROFILES ─────────────────────────────────────────────────────────
# STYLE (the look: type, palette, captions, audio mix) and FORMAT (the genre:
# news, top5, comparison...) are separate axes. Format is what changes the
# PHYSICS, so the tunables below are per-format. A sheet declares
# `"format": "<name>"`; omitting it means "news" so every existing sheet keeps
# working.
#
# EVERY number here is derived from a measured teardown, never invented — the
# same discipline that produced the style packs. `_derived` records the source.
FORMATS: dict[str, dict] = {
    "news": {
        "runtime": (60.0, 80.0),
        "hook_max": 2.0,
        "face": (0.10, 0.20),
        "sfx": (6, 9),
        "sfx_vol": (0.10, 0.19),
        "requires_cta": False,
        "_derived": "styles/editorial.md — 11-reel teardown 2026-07-22; "
                    "runtime + hook set by user rules 2026-08-12.",
    },
    "top5": {
        # Tips / roundups / 'top 5' / free-tool reels.
        "runtime": (26.0, 48.0),
        "hook_max": 2.0,
        "face": (0.10, 0.20),
        "sfx": (6, 9),
        "sfx_vol": (0.06, 0.10),
        "requires_cta": True,
        "_derived": "styles/utility.md v2 — 12-reel teardown 2026-07-24 "
                    "(full-res crops + 8fps motion bursts). Runtime '26-48s', "
                    "SFX 'tiny click/pops vols .06-.10, ordinary cuts silent', "
                    "'comment-gate CTA' are all measured properties of that "
                    "pack, approved as-is by the user 2026-08-12. face share "
                    "is INHERITED from news: it was derived as a general "
                    "retention rule, not a genre rule, and has not been "
                    "measured separately for this format — measure it on the "
                    "first top5 reel and tighten this if it disagrees.",
    },
    "ai-tools": {
        # AI / Claude / automation tool reels — the 2026-08-25 expansion. The
        # BLEND, chosen by the user: Saraev's SKELETON (face bookends the reel
        # — hook and CTA — evidence owns the middle) with Badar Munir's
        # EVIDENCE DOCTRINE (a named tool is ON SCREEN, running or being
        # itself, while it is named: its real page, its real output, a real
        # terminal — never a README screenshot standing in for a demo).
        #
        # RUNTIME IS DERIVED FOR OUR VOICE, not copied from the corpus. The
        # corpus runs 26.5-48.6s at a measured 217-237 wpm; our twin is
        # locked at 2.35-2.75 wps (~162 wpm, user kept the pace 2026-08-25).
        # Corpus word counts (~95-176 words, median ~130-155) spoken at OUR
        # pace land 40-66s; the band takes the working middle. A single-tool
        # short sits at the bottom, a 3-tool list at the top.
        "runtime": (40.0, 60.0),
        "hook_max": 2.0,          # corpus hooks land the PROBLEM by ~2s,
                                  # artifact already on frame 0
        "face": (0.10, 0.25),     # bookend style, measured on Saraev IG
                                  # (~20%: hook + one mid beat + CTA)
        "sfx": (6, 9),            # INHERITED from news — not measurable from
        "sfx_vol": (0.10, 0.19),  # stills; re-derive on the first shipped reel
        "requires_cta": True,     # follow/comment gate is constitutive: all 8
                                  # corpus reels carry one
        "_derived": "8-reel teardown 2026-08-25 (STYLE-RULES entry of that "
                    "date): 5x Badar Munir YT shorts (26.5-48.6s, 1.6-5.4 "
                    "s/cut, 217 wpm, ~60%% face) + 3x Saraev IG (34.7-39.4s, "
                    "1.4-4.9 s/cut, 237 wpm, bookend face ~20%%), measured "
                    "with ffprobe/scene-detect/whisper, frames read via "
                    "scout_sheet. Runtime mapped through OUR measured "
                    "2.35-2.75 wps. sfx band inherited from news, unmeasured.",
    },
    "comparison": {
        # "iPhone 18 vs 17", "Grok vs ChatGPT". Spikes at launch moments.
        # TIMING IS INHERITED FROM `news`, NOT MEASURED. There is no comparison
        # teardown in styles/ — and rather than fabricate numbers that would
        # LOOK derived, every timing value here is deliberately identical to
        # news and marked as such. What this format DOES add is structural
        # (G26): a comparison must actually compare, name both sides, and stay
        # balanced. Those rules follow from what the genre IS and need no
        # measurement. Measure the timings on the first 3-5 comparison reels
        # and split this profile off properly then.
        "runtime": (60.0, 80.0),
        "hook_max": 2.0,
        "face": (0.10, 0.20),
        "sfx": (6, 9),
        "sfx_vol": (0.10, 0.19),
        "requires_cta": True,
        "_derived": "INHERITED from news (editorial 11-reel teardown) — NOT "
                    "measured for this genre. Only the structural rules in "
                    "G26 are specific to comparison. Do not present these "
                    "timings as derived; tighten them from a real teardown.",
    },
}
DEFAULT_FORMAT = "news"

# ---------------------------------------------------------------- style names
# Renamed 2026-08-16: style ids describe the STYLE, not its creator, so they
# read like the format vocabulary (news / top5 / comparison).
#   editorial = tech-news reporting  (was varun-mayya / varun)
#   utility   = tips and tools       (was nick-saraev / nick)
#   word-reveal = per-word caption reveal (was nick-display)
#
# THIS MODULE IS THE SINGLE SOURCE OF TRUTH for the mapping — validate_job.py
# imports it rather than keeping a second copy, because two copies drift.
# The legacy ids are accepted forever: seven reels were published carrying
# them, and re-writing a shipped beat sheet to satisfy a rename is exactly the
# retro-fixing RULES.md forbids. Do NOT add new entries — a new style gets a
# canonical name, not an alias.
STYLE_CANON = ("editorial", "utility")
STYLE_ALIASES = {
    "varun": "editorial",
    "varun-mayya": "editorial",
    "nick": "utility",
    "nick-saraev": "utility",
}
CAPTION_ALIASES = {"nick-display": "word-reveal"}


def canon_style(value: str | None) -> str | None:
    """Canonical style id for a beat sheet / brief value."""
    if value is None:
        return None
    return STYLE_ALIASES.get(value, value)


def canon_caption(value: str | None) -> str | None:
    """Canonical caption treatment for a beat sheet value."""
    if value is None:
        return None
    return CAPTION_ALIASES.get(value, value)


# Scenes that put the two sides in front of the viewer together.
COMPARE_TYPES = {"comparesplit", "hcompare", "specsheet", "chart", "strikeswap"}
COMPARE_MIN = 3          # fewer than this and it is a review, not a comparison
BALANCE = (0.40, 0.60)   # single-sided screen time share per side

# Module-level aliases = the news profile, so importers (scripts/doctor.py)
# and any older call site keep working.
RUNTIME_MIN, RUNTIME_MAX = FORMATS["news"]["runtime"]
HOOK_MAX = FORMATS["news"]["hook_max"]

# Absolute wall = the PLATFORM limit (user rule 2026-08-16, revised same day
# from 120s: "Instagram Reels and YouTube Shorts both allow up to 3 minutes,
# so our cap should be 3 minutes").
#
# The per-format `runtime` band stays the DEFAULT and stays measured — it is
# what a reel should be unless the topic argues otherwise. `allowLong` is the
# argument, and it already required a written `allowLongReason`. What it did
# NOT have was a ceiling: set the flag with any reason string and a "reel"
# could run ten minutes, which is not a judgement call, it is an unbounded
# opt-out of the one gate that keeps these things short.
#
# 180s is USER-SET, not derived from a teardown — recorded as such so nobody
# later mistakes it for a measured number. It is now the PLATFORM ceiling
# rather than an editorial one, which means the only editorial brake left
# between the band and the wall is `allowLongReason`. Write it like it matters.
#
# CAVEAT — rules that count instead of measuring density do not scale with it.
# G08 wants 6-9 SFX cues no matter how long the reel is: ~1 per 10s at the
# 60-80s band, ~1 per 25s at 180s. The number was measured on 60-80s reels, so
# past the band it quietly means something it was never measured to mean.
# Re-derive G08 as a per-minute density before shipping anything near 180s.
RUNTIME_CEILING = 180.0
ROW_DWELL = 0.6      # a list row must be readable, not merely present
DUR_MAX = {                                # 2026-07-28 / 2026-07-31
    "motion": 2.9,      # footage / split / video-backed cards
    "building": 3.3,    # specsheet | chart | timeline — content lands in sequence
    "card": 2.6,        # everything else: a held layout
}
# NOTE: facecam share, SFX count and SFX volume are PER-FORMAT — see FORMATS.
# They used to be module constants here; that is exactly how a news-tuned
# number silently governs a genre it was never measured on.
TAIL_MAX = 0.45
FACE_BY = 5.0        # user rule 2026-08-12: presenter on screen by 5s
DATA_MIN = 2.0       # a card carrying a claim must outlast the claim                            # 2026-08-03 oss-alt tail-trim rule

# HeadlineBuild.tsx renders these at fixed sizes with NO auto-fit, so an
# over-long line wraps and orphans a word (user note 2026-08-11).
# Limits measured against the 1080px frame at the component's real font sizes.
# DERIVED from the type scale and the measured advance, not typed. These were
# {"label": 30, "headline": 18, "subtitle": 26} — calibrated for Fraunces, and
# silently wrong from the moment the display face became Space Grotesk on
# 2026-08-18: the real headline budget fell to ~14 characters while the gate
# kept passing 18, so six headlines already in the library overflow the frame
# with a clean build. Mirrors src/theme/fit.ts ADVANCE; test_gates.py asserts
# the two agree.
_ADVANCE = 0.655                 # src/theme/fit.ts
_BOX_W = 1080 * (1 - 2 * 0.06) - 140     # safe width, centred block padding
_SIZE = {"label": 36, "subtitle": 60, "headline": 100}   # src/theme/type.ts
LINE_MAX_CHARS = {
    k: int(_BOX_W / (v * _ADVANCE)) for k, v in _SIZE.items()
}

AZ_ASPECT_MAX = 2.5    # G36. NOT a fresh measurement: it is the SAME wide-
                       # artifact line RULES.md already sets for `receipt`
                       # ("wider than ~2.5:1 goes in a floatcard"). Every
                       # source measured broken on ios27-tiers exceeded it
                       # (2.6, 3.1, 4.6:1); 16:9 sources have shipped fine on
                       # iphone18-split and made-by-google-26, so gating
                       # tighter than 2.5 would reject working precedent.
# ---------------------------------------------------------------------------
# WHAT MAY BLOCK A RENDER, AND UNDER WHICH RULE
#
# Read the long note at the end of check_beats first. In short: the pipeline used
# to enforce 37 rules, most of them numbers taken from teardowns. Those numbers
# were real, but taste is not law, and a gate that refuses to render a good video
# because it runs 84 seconds instead of 80 is doing harm. Only these block.
# ---------------------------------------------------------------------------
BLOCKING_RULES: dict[str, str] = {
    # RULE 1 — the output is an Instagram Reel / YouTube Short.
    "G01": "R1 audio and scenes must stay in sync or the tail drifts",
    "G20": "R1 a row that never lands is unreadable on a phone",
    "G25": "R1 a cue that never lands is unreadable on a phone",
    "G30": "R3 a split number makes the caption say what he did not",
    "G32": "R1 the outro must clear the platform's own chrome",
    "G34": "R1 an orphaned single letter is unreadable",
    "G38": "R1 70-85% watch on mute, so the hook must carry words",
    # G31 is RULE 1, not taste. Instagram and YouTube both normalise loudness,
    # so a master 2 LU under target plays audibly quieter than everything around
    # it in the feed — a platform-specific defect, the same category as content
    # hidden under the platform's own chrome. The +/-1.0 LU tolerance was derived
    # by measurement (two-pass lands ~0.5 LU short), not chosen; widen it if it
    # ever rejects a master that sounds right.
    "G31": "R1 platforms normalise loudness, so the master must hit the target",
    # G46 is deliberately NOT here. A caption riding our own credit lane is our
    # layout colliding with our layout — craft, not the Reels/Shorts rule. See
    # the split note at the gate itself.
    "G45": "R1 a caption under the account row is painted over by the platform",
    # RULE 2 — sources are scouted on mobile view first.
    "G29": "R2 sources are captured on mobile view first",
    "G41": "R2 a desktop capture needs a recorded reason",
    # RULE 3 — what is on screen matches what the creator says.
    #
    # G18 PROMOTED 2026-08-18, on the condition this note set: it now measures
    # the claim's real length from word timings instead of asserting a flat 2.0s.
    # A card that ends while the sentence explaining it is still being spoken
    # contradicts what the viewer is hearing, which is Rule 3. The flat minimum
    # survives as G18a — ADVICE — for cards with no speech over them at all,
    # where there is no claim to outlast and the number is only taste.
    "G18": "R3 a card must outlast the sentence it illustrates",
    "G21": "R3 captions must be words that were actually spoken",
    "G39": "R3 every scene must carry the script line it illustrates",
    # RENDER — not opinion. These produce black frames or crash.
    "G11": "RENDER an assetId that is not in the manifest cannot resolve",
    "G13": "RENDER a clip shorter than its beat freezes or blacks out",
    "G28": "RENDER a missing SFX file",
    "G35": "RENDER a still in a video slot renders black",
    # G48 is RENDER, not framing taste: below 1 the layer stops covering the
    # canvas, and a focus outside 0..1 pushes past the slack `cover` gives it.
    # Both paint the black backdrop. G49 — the zoom/zoomDir compounding note —
    # is deliberately NOT here: wanting a push from a tight base is a real
    # choice, so it asks the question instead of refusing the render.
    "G48": "RENDER framing that exposes the backdrop renders black bars",
    # G51 (2026-08-25): scene JSON is invisible to tsc (the registry casts it),
    # so a scene can ship without the one array its component `.map()`s over —
    # claude-eating-tokens' statcard carried an invented stat/unit shape and
    # crashed remotion at frame 538, AFTER every other gate had passed.
    "G51": "RENDER a scene missing the array its component maps over crashes",
    # G54 (2026-09-01): wordcascade's `size` is a MULTIPLIER on a 100px base,
    # not a pixel value. Authored as `size: 150` it asks for 15,000px type on a
    # 1920px frame, and what renders is the flat interior of one glyph — a
    # frame with no legible content, which lint reads as 95% dead space and a
    # human reads as "the beat is broken". Proven by rendering it. RENDER for
    # the same reason as G35: nothing downstream can recover it, and the
    # threshold is a ratio of the platform's own frame to the component's base,
    # not a number anyone picked.
    "G54": "RENDER type larger than the frame renders as one blank glyph",
    # RIGHTS — attribution, and the user's control over their own work.
    "G14": "RIGHTS we credit the sources we use",
    "G15": "RIGHTS a stated number carries where it came from",
    "G27": "RIGHTS the user approved THIS script",
    "G53": "RIGHTS the voice says the script the user approved",
}


# G53 floor. Derived 2026-08-27 from every reel on disk: legitimate
# script-vs-own-audio scores 0.885-1.000, a different reel's audio scores
# 0.013-0.110. 0.70 sits in the empty gap between the two bands.
VO_SCRIPT_MATCH_FLOOR = 0.70


def _norm_words(s: str) -> str:
    """Lowercase, strip punctuation, collapse space — so a `covers` phrase can be
    matched against spoken words without tripping over commas or casing."""
    import re as _re
    return _re.sub(r"\s+", " ", _re.sub(r"[^\w\s]", " ", s.lower())).strip()


def _shows_source(sc: dict) -> bool:
    """True when the scene puts BORROWED material on screen.

    The presenter's own avatar footage is not evidence, so it never needs to
    declare what line it illustrates.
    """
    src = str(sc.get("src") or sc.get("topSrc") or "")
    if "avatar" in src.lower():
        return False
    return bool(sc.get("assetId")) or (
        src.startswith("assets/") and not src.endswith("avatar-master.mp4"))


def _partition(errors: list[str]) -> tuple[list[str], list[str]]:
    """Split findings into blocking and advisory by their gate id.

    Default is ADVICE. A check has to be named in BLOCKING_RULES to stop a
    render, so forgetting to classify a new gate makes it advisory — the safe
    direction — instead of silently adding a new law.
    """
    block, advise = [], []
    for e in errors:
        gid = e.split(" ", 1)[0].strip()
        if gid in BLOCKING_RULES:
            block.append(f"{e}\n      [{BLOCKING_RULES[gid]}]")
        else:
            advise.append(f"ADVICE {e}")
    return block, advise


MOTION_TYPES = {"footage", "split"}
BUILDING_TYPES = {"specsheet", "chart", "timeline", "settingspane", "priceladder"}
VIDEO_EXT = (".mp4", ".webm", ".mov")


def _is_motion(sc: dict) -> bool:
    if sc["type"] in MOTION_TYPES:
        return True
    src = str(sc.get("src") or sc.get("mediaSrc") or "")
    return sc["type"] in ("floatcard", "deviceframe") and src.endswith(VIDEO_EXT)


def _dur_class(sc: dict) -> str:
    if _is_motion(sc):
        return "motion"
    if sc["type"] in BUILDING_TYPES:
        return "building"
    return "card"


def check_beats(beats: dict, vo_end: float | None = None,
                manifest: dict | None = None,
                allow_short: bool = False,
                clip_durations: dict[str, float] | None = None,
                vo_words: list | None = None) -> list[str]:
    """Run every mechanical gate. Raises GateError listing ALL failures.

    Returns the list of non-blocking warnings.
    `allow_short` exempts the 60-120s runtime rule (legacy sheets only).
    """
    errors: list[str] = []
    warnings: list[str] = []
    scenes = beats["scenes"]

    # G23 — the sheet's format must be one we have measured numbers for.
    fmt_name = beats.get("format", DEFAULT_FORMAT)
    prof = FORMATS.get(fmt_name)
    if prof is None:
        errors.append(
            f"G23 unknown format {fmt_name!r} — known: {sorted(FORMATS)}. "
            "Add a profile to FORMATS derived from a real teardown before "
            "shipping a new genre; do not guess the numbers. "
            "SKILL CUE: the teardown is what the `reel-analyzer` skill does — "
            "feed it 3-5 reference reels of the genre. Take its STRUCTURE; "
            "measure the NUMBERS yourself with ffprobe and scene detection, "
            "because its pacing read is an estimate and G23 exists to stop "
            "guessed bands.")
        prof = FORMATS[DEFAULT_FORMAT]
    RT_MIN, RT_MAX = prof["runtime"]
    HK_MAX = prof["hook_max"]
    FC_MIN, FC_MAX = prof["face"]
    SX_MIN, SX_MAX = prof["sfx"]
    SXV_MIN, SXV_MAX = prof["sfx_vol"]
    total = round(sum(s["durationSec"] for s in scenes), 2)

    # G01 — scenes must sum to the audio, or the tail drifts out of sync
    if vo_end is not None:
        # THE DEFECT IS A FROZEN PICTURE, NOT A SILENT TAIL (2026-08-22).
        #
        # The gate's own message names it: "frozen face". It exists because an
        # avatar clip held past its last word sits there staring. A tail whose
        # final scene is DRAWN BY CODE cannot freeze — a CTA card is still
        # typing its keyword and landing its notification — and a comment-gate
        # CTA genuinely needs a beat after the voice stops for the viewer to
        # read what to comment. Blocking that forced the CTA payoff to be cut
        # off mid-animation on the first VO-only reel.
        #
        # Narrow on purpose: only generated scene types earn the longer tail.
        # A `footage` or `split` scene held past its clip DOES freeze, and G13
        # is about clip length, not this. Everything else still gets TAIL_MAX.
        ANIMATED_TAIL = {"commentcta", "typecard", "endquestion", "logobeat",
                         "specsheet", "statcard", "wordcascade", "checklist"}
        last_type = str(scenes[-1].get("type", "")) if scenes else ""
        tail_max = 2.5 if last_type in ANIMATED_TAIL else TAIL_MAX
        reel_end = vo_end + tail_max
        if total > reel_end + 0.01:
            errors.append(
                f"G01 tail freeze: scenes total {total:.2f}s but VO ends at "
                f"{vo_end:.2f}s — a reel may not run more than {tail_max}s past "
                f"the last spoken word (frozen face). Final scene is "
                f"{last_type!r}.")
        if total < vo_end - 0.01:
            errors.append(
                f"G01 audio truncated: scenes total {total:.2f}s < VO "
                f"{vo_end:.2f}s — the voiceover would be cut off.")

    # G02 — runtime band
    long_ok = bool(beats.get("allowLong"))
    if long_ok and not str(beats.get("allowLongReason") or "").strip():
        errors.append(
            "G02 allowLong is set with no `allowLongReason` — running past "
            f"{RUNTIME_MAX:.0f}s has to be argued for in one line, not just "
            "switched on.")
    if not allow_short:
        if total < RT_MIN:
            errors.append(
                f"G02 runtime {total:.1f}s under {RT_MIN:.0f}s for format "
                f"{fmt_name!r}.")
        elif total > RT_MAX and not long_ok:
            errors.append(
                f"G02 runtime {total:.1f}s over {RT_MAX:.0f}s for format "
                f"{fmt_name!r}. Cut every sentence that does not change the "
                "viewer's understanding. If the story genuinely needs longer, "
                "set allowLong + allowLongReason.")
    # The ceiling binds even with allowLong, and even with --allow-short:
    # allowLong is permission to argue past the measured band, not permission
    # to leave short form. Nothing enforced this before 2026-08-16.
    if total > RUNTIME_CEILING:
        errors.append(
            f"G02 runtime {total:.1f}s over the {RUNTIME_CEILING:.0f}s hard "
            f"ceiling (format {fmt_name!r}). allowLong cannot pass this — it "
            "buys room to argue past the measured band, not an exit from "
            "short form. Split the topic across two reels.")

    # G03 — the hook may not hold
    if scenes and scenes[0]["durationSec"] > HK_MAX:
        errors.append(
            f"G03 hook held {scenes[0]['durationSec']:.2f}s > {HK_MAX}s "
            f"({scenes[0]['type']}) — Instagram retention rule 2026-07-31.")

    # G04 — per-type held-layout ceilings
    for i, sc in enumerate(scenes):
        cls = _dur_class(sc)
        lim = DUR_MAX[cls]
        if sc["durationSec"] > lim:
            errors.append(
                f"G04 scene {i:02d} ({sc['type']}, {cls}) held "
                f"{sc['durationSec']:.2f}s > {lim}s — split the VO across 2-3 "
                "distinct visuals.")

    # G05 — a display line longer than the frame comfortably holds. ADVICE.
    #
    # DEMOTED FROM BLOCKING 2026-08-18. Its stated reason was "HeadlineBuild has
    # no auto-fit; this wraps and orphans a word" — a RENDER defect, which is
    # why it blocked. HeadlineBuild now shrinks to fit (src/theme/fit.ts), so
    # the render is correct at any length and the defect no longer exists.
    #
    # What is left is real but is taste: a claim that has been shrunk to 62% of
    # display size still fits, still reads, and is probably too wordy for a
    # hook. That is a judgement about copy, not a fact about Reels, so it
    # advises. Per RULES.md section 0, test (3): if the renderer fixes it, the
    # frame is already right and the check is a lint, not a law.
    for i, sc in enumerate(scenes):
        hl = sc.get("headline")
        if not isinstance(hl, dict):
            continue
        for ln in hl.get("lines", []):
            kind = ln.get("kind", "headline")
            limit = LINE_MAX_CHARS.get(kind, 18)
            for part in str(ln.get("text", "")).split("\n"):
                if len(part) > limit:
                    errors.append(
                        f"G05 scene {i:02d} {kind} line is {len(part)} chars "
                        f"(comfortable max {limit} at this face and size): "
                        f"{part!r} — it renders, because HeadlineBuild shrinks "
                        f"to fit, but it lands smaller than the scale intends. "
                        f"Shorter copy reads better than smaller type.")

    # G06 — facecam share of runtime
    avatar_scenes = [s for s in scenes
                     if "avatar-master" in str(s.get("src") or "")]
    face = sum(s["durationSec"] for s in avatar_scenes)
    share = face / total if total else 0
    if not (FC_MIN <= share <= FC_MAX):
        errors.append(
            f"G06 facecam {share:.0%} of runtime, outside "
            f"{FC_MIN:.0%}-{FC_MAX:.0%} for format {fmt_name!r}.")

    # G07 — one source clip may carry only one footage beat
    used = Counter()
    for sc in scenes:
        src = str(sc.get("src") or "")
        if sc["type"] == "footage" and src and "avatar-master" not in src:
            used[src] += 1
    for src, n in used.items():
        if n > 1:
            errors.append(
                f"G07 clip reuse: {src.split('/')[-1]} carries {n} footage "
                "beats — cut a DISTINCT shot for every slot (rule 2026-07-31).")

    # G08 — sound design: sparse, and never louder than the band
    cues = [c for s in scenes for c in (s.get("sfx") or [])]
    if not (SX_MIN <= len(cues) <= SX_MAX):
        errors.append(
            f"G08 {len(cues)} SFX cues, outside {SX_MIN}-{SX_MAX} — ordinary "
            "cuts stay silent (rule 2026-07-22).")
    for c in cues:
        v = c.get("vol")
        if v is not None and not (SXV_MIN <= v <= SXV_MAX):
            errors.append(
                f"G08 SFX {c.get('src')} vol {v} outside "
                f"{SXV_MIN}-{SXV_MAX} for format {fmt_name!r}.")

    # G09 — background music is OPTIONAL; the CHOICE is what gets declared.
    #
    # INVERTED 2026-08-22 by user directive: "make it optional to make video
    # without background music; sound effects stay the default." The
    # 2026-08-17 design treated a music-free reel as an argued EXCEPTION
    # (noMusic + a written noMusicReason); it is now a first-class choice and
    # the reason is accepted but no longer demanded. What survives is the
    # original 2026-07-22 problem this gate was born for: a reel that FORGOT
    # its bed must still be distinguishable from a chosen VO-only cut — so a
    # sheet with neither `music` nor `noMusic: true` still advises. SFX are a
    # separate layer (G08/G28/G40) and remain the default, untouched.
    no_music = bool(beats.get("noMusic"))
    music = beats.get("music")
    if not music and not no_music:
        errors.append("G09 no music bed and no `noMusic: true` — background "
                      "music is OPTIONAL (user directive 2026-08-22), but the "
                      "choice is declared: set noMusic so a forgotten bed can "
                      "be told apart from a chosen VO-only cut.")
    elif music and len({p["vol"] for p in music.get("points", [])}) < 2:
        errors.append("G09 music bed is flat — volume must be automated "
                      "(hook full → duck → rise at the reveal → fade).")

    # G10 — production caption treatment
    PROD_CAPTIONS = {"word-reveal", "ink-circle"}
    if canon_caption(beats.get("captionStyle")) not in PROD_CAPTIONS:
        warnings.append(
            f"G10 captionStyle is {beats.get('captionStyle')!r}; "
            f"production treatments are {sorted(PROD_CAPTIONS)} (2026-07-29).")
    if not beats.get("emphasis"):
        errors.append("G10 empty `emphasis` — it drives the accent keyword in "
                      "word-reveal captions.")
    if not beats.get("captions"):
        errors.append("G10 no captions array.")

    # G11 — provenance: every assetId must exist in the manifest
    if manifest:
        known = {a["id"] for a in manifest.get("assets", [])}
        banned = set(manifest.get("banned_assets", []))
        for i, sc in enumerate(scenes):
            aid = sc.get("assetId")
            if aid and aid not in known:
                errors.append(
                    f"G11 scene {i:02d} assetId {aid!r} is not in the "
                    "manifest — every visual must be a scouted, verified asset.")
            if aid and aid in banned:
                errors.append(
                    f"G11 scene {i:02d} uses BANNED asset {aid!r} — the "
                    "manifest bans it because it would imply an unsupported "
                    "claim.")

    # G13 — a clip must be at least as long as the beat that plays it.
    # A short clip does not fail loudly: it runs past its own end and the
    # frame holds or spills into whatever the source cut to next. On
    # apple-pay-india a 1.65s clip on a 2.3s beat dragged the ad's next title
    # card into frame with its text cropped — invisible in logs, caught only
    # on the contact sheet.
    if clip_durations:
        for i, sc in enumerate(scenes):
            for key in ("src", "mediaSrc", "topSrc", "bottomSrc", "bgSrc",
                        "leftSrc", "rightSrc"):
                src = sc.get(key)
                if not src or "avatar-master" in str(src):
                    continue
                have = clip_durations.get(str(src))
                if have is None:
                    continue
                start = float(sc.get("from") or sc.get(f"{key[:-3]}From") or 0)
                need = start + sc["durationSec"]
                if have + 0.02 < need:
                    errors.append(
                        f"G13 scene {i:02d} ({sc['type']}) plays "
                        f"{str(src).split('/')[-1]} for {sc['durationSec']:.2f}s "
                        f"from {start:.2f}s but the clip is only {have:.2f}s — "
                        "re-cut it longer or shorten the beat.")

    # G17 — THE PRESENTER MUST APPEAR IN THE FIRST 5 SECONDS (user 2026-08-12).
    # On grok-bot the region structure pushed the split hook to ~9s: three
    # opening visuals, then a receipt, THEN the face. A viewer should meet the
    # human almost immediately.
    face_at = None
    t = 0.0
    for sc in scenes:
        srcs = [str(sc.get(k) or "") for k in ("src", "bottomSrc")]
        if any("avatar-master" in v for v in srcs):
            face_at = t
            break
        t += sc["durationSec"]
    if face_at is None:
        errors.append("G17 the presenter never appears.")
    elif face_at > FACE_BY:
        errors.append(
            f"G17 presenter first appears at {face_at:.1f}s — must be on screen "
            f"by {FACE_BY:.0f}s. Move the split hook earlier or shorten the "
            "opening block.")

    # G18 — a card that states a claim must not vanish mid-sentence (user
    # 2026-08-12 #6: "motion graphics disappear before the creator finishes").
    #
    # NOW MEASURED, not assumed (2026-08-18). The rule had been a flat
    # `durationSec < 2.0`, and the note in BLOCKING_RULES explained why that
    # could not be law: "a 1.6s card over a 1.4s claim satisfies Rule 3 and a
    # 2.1s card over a 3s claim breaks it". A fixed number cannot tell those
    # apart, because the thing it is really about — the SENTENCE — was never in
    # the check.
    #
    # With word timings the real question is answerable: does the card outlast
    # the speech that runs under it? That is Rule 3 exactly — what is on screen
    # matching what is being said — so when the measurement is available this
    # blocks, and where it is not (no vo_words) it falls back to the flat
    # minimum as ADVICE, which is all a guess was ever worth.
    _wt: list[tuple[str, float, float]] = []
    for x in (vo_words or []):
        if isinstance(x, (list, tuple)) and len(x) >= 3:
            try:
                _wt.append((str(x[0]), float(x[1]), float(x[2])))
            except (TypeError, ValueError):
                pass
    _cursor = 0.0
    for i, sc in enumerate(scenes):
        start = _cursor
        _cursor += sc["durationSec"]
        end = _cursor
        if sc["type"] not in ("specsheet", "chart", "timeline", "statcard"):
            continue
        # The claim is the speech that STARTS while this card is up. A word that
        # began before the card appeared belongs to the previous beat.
        spoken = [(a, b) for _, a, b in _wt if start <= a < end]
        if spoken:
            claim_end = max(b for _, b in spoken)
            if claim_end > end + 0.04:      # ~1 frame of tolerance at 30fps
                errors.append(
                    f"G18 scene {i:02d} ({sc['type']}) ends at {end:.2f}s but the "
                    f"sentence it illustrates runs to {claim_end:.2f}s — the card "
                    f"vanishes {claim_end - end:.2f}s before the creator finishes "
                    f"saying it. Hold it to the LAST word of the claim.")
        elif sc["durationSec"] < DATA_MIN:
            # nothing spoken over it, so there is no claim to outlast; the flat
            # minimum is taste and says so
            errors.append(
                f"G18a scene {i:02d} ({sc['type']}) holds only "
                f"{sc['durationSec']:.2f}s with no speech over it — under "
                f"{DATA_MIN}s a data card is hard to read at all. Judgement, not "
                "a rule: nothing is being contradicted, it is just quick.")

    # G19 — THE PRESENTER'S FACE MUST MATCH THE REEL'S REGISTER (2026-08-12).
    # Measured: a photo avatar's expression is fixed by its source still, so
    # the ONLY lever is which look you pick. Look 0aa05d6e is a permanent
    # smile; running a caveat-heavy script on it grins through the bad news
    # (probe be34b663 — widest grin landed on "does not explain credential
    # handling"). expressiveness cannot rescue it: at `low` it still smiled
    # and motion fell 6.90 -> 1.02. So the sheet declares its tone and the
    # build must have selected a look registered for that tone.
    # A neutral-register presenter is ACCEPTABLE for a serious script — it
    # does not grin at bad news, which is the whole failure G19 exists to stop.
    # It is NOT acceptable for a warm script: a level face cannot sell warmth,
    # and twin f55b0b7c has never been proven to warm up (2026-08-13).
    REGISTER_OK = {"serious": {"serious", "neutral"}, "warm": {"warm"}}
    tone = beats.get("tone")
    if tone is not None:
        if tone not in ("warm", "serious"):
            errors.append(
                f"G19 tone {tone!r} is not one of warm/serious.")
        else:
            got = beats.get("avatarRegister")
            if not got:
                errors.append(
                    f"G19 sheet declares tone {tone!r} but no `avatarRegister` "
                    "— set it from config.avatarRegistry[<lookId>].register so "
                    "the face is checked against the script.")
            elif got not in REGISTER_OK[tone]:
                errors.append(
                    f"G19 tone is {tone!r} but the selected look is registered "
                    f"{got!r}. A {got} face cannot deliver a {tone} script — "
                    f"acceptable registers for {tone!r}: "
                    f"{sorted(REGISTER_OK[tone])}. Switch the look "
                    "(tools/measure_avatar.py use <lookId>), not the prompt. "
                    "Prompting the face does nothing.")

    # G20 — EVERY LIST ROW MUST LAND AND BE READABLE (2026-08-12).
    # Checklist.tsx staggers rows at 0.25 + i*stagger. On grok-bot scene 49 a
    # 5-row list with stagger 0.55 put the last row at 2.45s inside a 2.04s
    # scene: the "iOS" row NEVER APPEARED, while the voiceover was already
    # saying "Linux, and iOS". A contact sheet cannot show this — only maths.
    for i, sc in enumerate(scenes):
        if sc["type"] != "checklist":
            continue
        rows = sc.get("rows") or []
        if not rows:
            errors.append(f"G20 scene {i:02d} checklist has no rows.")
            continue
        stagger = sc.get("stagger", 0.55)
        last_at = 0.25 + (len(rows) - 1) * stagger
        need = last_at + ROW_DWELL
        if need > sc["durationSec"] + 0.01:
            fits = round(
                (sc["durationSec"] - ROW_DWELL - 0.25) / max(len(rows) - 1, 1), 2)
            errors.append(
                f"G20 scene {i:02d} checklist: last of {len(rows)} rows enters "
                f"at {last_at:.2f}s and needs {need:.2f}s to read, but the "
                f"scene is {sc['durationSec']:.2f}s — the final row(s) never "
                f"land. Use stagger <= {max(fits, 0.05):.2f}, drop rows, or "
                "hold the scene longer.")

    # G21 — CAPTIONS MUST MATCH THE NARRATION THAT WAS ACTUALLY SPOKEN
    # (user rule 2026-08-12: "verify captions against the final narration
    # before render"). Captions are written from the script, but the render
    # uses the GENERATED voice track — if the script was edited after the
    # voice was made, captions silently drift from the audio.
    if vo_words:
        # .strip() FIRST for whitespace: whisper returns words with a LEADING
        # SPACE (" Apple's"), and strip(punctuation) does not remove it.
        raw = [w.strip().lower().strip(".,!?:;\"'—-") for w, *_ in
               (x if isinstance(x, (list, tuple)) else (x,) for x in vo_words)]
        raw = [w for w in raw if w]
        spoken = set(raw)
        # Whisper is NOT ground truth for what was said, and this gate treated it
        # as if it were. Measured across the library on 2026-08-17, every single
        # one of its 20 hits was a transcription artifact, not a caption defect:
        #
        #   hyphen splits   "device-specific" transcribed as "device" "-specific"
        #                   also one-time, hold-up, always-on, pre-orders, Ming-Chi
        #   name mishears   Kuo->"Quo", Seedance->"Seedense", ByteDance->"bite
        #                   dance", stubby->"stabby", configs->"conflicts"
        #   number mishears "two 48-megapixel" heard as "248 megapixel"
        #
        # A gate at 100% false positives is worse than none: it trains people to
        # skip the output. The repo already knew whisper mishears — that is what
        # `caption_corrections` is for. So compare with the tolerance the medium
        # actually needs, and keep the case this exists for: captions written
        # against a DIFFERENT script, which show up as words with no plausible
        # match anywhere near them in time.
        joined = {a + b for a, b in zip(raw, raw[1:])}          # "bite dance"
        spoken |= joined
        squashed = {w.replace("-", "").replace("'", "") for w in spoken}

        def close(a: str, b: str) -> bool:
            """Cheap edit-distance<=2 for same-ish length words."""
            if abs(len(a) - len(b)) > 2:
                return False
            # The prefix/suffix guard is a speed trick, and for a SHORT word it
            # is the whole word — so "kuo" vs "quo" (distance 1, a classic
            # proper-noun mishear) was rejected before the distance was even
            # computed. Skip the guard when there is nothing to guard.
            if len(a) > 4 and a[:3] != b[:3] and a[-3:] != b[-3:]:
                return False
            prev = list(range(len(b) + 1))
            for i, ca in enumerate(a, 1):
                cur = [i]
                for j, cb in enumerate(b, 1):
                    cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                                   prev[j - 1] + (ca != cb)))
                prev = cur
            return prev[-1] <= 2

        missing = []
        for cap in (beats.get("captions") or []):
            for tok in str(cap.get("text", "")).split():
                k = tok.lower().strip(".,!?:;\"'—-")
                if not k or any(c.isdigit() for c in k):
                    continue
                flat = k.replace("-", "").replace("'", "")
                if k in spoken or flat in squashed:
                    continue
                if any(close(flat, s) for s in squashed if abs(len(s) - len(flat)) <= 2):
                    continue
                # Whisper also RUNS WORDS TOGETHER: "Free Grok" comes back as
                # "FreeGROK", so each caption word is a substring of one spoken
                # token. Only for words long enough that containment means
                # something.
                if len(flat) >= 4 and any(flat in s for s in squashed):
                    continue
                missing.append(tok)
        # BLOCK ON THE RATE, NOT ON A WORD. The failure this gate exists for —
        # captions written against a script that was edited after the voice was
        # made — is SYSTEMIC: most words stop matching at once. An isolated miss
        # is a mishear whisper could not spell, and blocking a render for one of
        # those is how a gate teaches people to ignore it. Measured: the whole
        # library sits at ~1-3 stray words per reel out of 150-250 tokens, while
        # a genuinely different script misses nearly everything.
        total_tok = sum(len(str(c.get("text", "")).split())
                        for c in (beats.get("captions") or [])) or 1
        rate = len(set(missing)) / total_tok
        if missing and (rate > 0.05 or len(set(missing)) >= 8):
            uniq = sorted(set(missing))[:8]
            errors.append(
                f"G21 {len(set(missing))} of {total_tok} caption word(s) "
                f"({rate:.0%}) have no match in the "
                f"narration: {uniq} — not a mishear, not a hyphen split: no "
                "similar word is spoken anywhere. The captions were written "
                "against a different script than the voice track. Re-derive them "
                "from the whisper transcript.")

    # G22 — ONE HIGHLIGHT PER BEAT (user rule 2026-08-12). Highlighting three
    # words in a four-word chunk highlights nothing.
    emph = {e.lower() for e in (beats.get("emphasis") or [])}
    if emph:
        for cap in (beats.get("captions") or []):
            toks = [w.lower().strip(".,!?:;\"'—-")
                    for w in str(cap.get("text", "")).split()]
            hits = [w for w in toks if w in emph]
            if len(hits) > 1:
                errors.append(
                    f"G22 caption {str(cap.get('text'))!r} highlights "
                    f"{len(hits)} words {hits} — one key word, number or "
                    "phrase per beat.")
                break

    # G34 — ORPHAN SINGLE-LETTER CAPTION TOKEN (2026-08-13, iphone18-split).
    # The TTS synthesized an audible stray "T" after "Pegatron —" and whisper
    # faithfully transcribed it. A lone letter that is not "a"/"I" in a
    # caption is almost always a TTS artifact or an unmerged whisper
    # fragment; it must be surgically cut from the master (then re-whisper),
    # never shipped or silently display-fixed while the audio still says it.
    for cap in (beats.get("captions") or []):
        for tok in str(cap.get("text", "")).split():
            k = tok.strip(".,!?:;\"'\u2014-")
            if len(k) == 1 and k.isalpha() and k.lower() not in ("a", "i"):
                errors.append(
                    f"G34 caption {str(cap.get('text'))!r} carries an orphan "
                    f"single-letter token {tok!r} — probable TTS artifact "
                    "(cf. 'Pegatron T', 2026-08-13). Cut it from the master "
                    "and re-run whisper; do not display-fix audio.")
                break
        else:
            continue
        break

    # G30 — ORPHAN NUMERIC FRAGMENT IN A CAPTION (2026-08-14,
    # september-preview). Whisper splits "$2,000" into "$2"+",000" and "7.8"
    # into "7"+".8"; if the build script's merge loop misses the [.,]digit
    # case, a bare ",000" or ".5" chip ships. The merge belongs in the build
    # (see build_template.py); this gate makes forgetting it impossible.
    import re as _re
    for cap in (beats.get("captions") or []):
        for tok in str(cap.get("text", "")).split():
            if _re.match(r"^[.,]\d", tok):
                errors.append(
                    f"G30 caption {str(cap.get('text'))!r} carries an orphan "
                    f"numeric fragment {tok!r} — merge [.,]digit tokens into "
                    "the previous token before chunking (see the merge loop "
                    "in tools/build_template.py).")
                break
        else:
            continue
        break

    # G24 — formats that are DEFINED by their call to action must carry one.
    # the utility teardown lists the comment-gate CTA as a defining property
    # of the tips/top-5 format, not a garnish: the reel exists to convert.
    if prof.get("requires_cta"):
        CTA_TYPES = {"commentcta", "endquestion", "instacta"}
        has_cta = any(sc["type"] in CTA_TYPES for sc in scenes) or any(
            sc.get("cta") for sc in scenes)
        if not has_cta:
            errors.append(
                f"G24 format {fmt_name!r} requires a call to action — add a "
                f"{sorted(CTA_TYPES)} scene. The comment-gate CTA is a "
                "defining property of this format (styles/utility.md).")

    # G25 — a settings pane's cues must LAND. Same failure as G20: an
    # animation scheduled past the end of its scene simply never happens, and
    # the viewer is told to look at a row that never highlights.
    CUE_TAIL = 0.35          # spotlight/flip transition length
    for i, sc in enumerate(scenes):
        if sc["type"] != "settingspane":
            continue
        dur = sc["durationSec"]
        if sc.get("focus"):
            land = sc.get("focusAt", 0.5) + CUE_TAIL
            if land > dur + 0.01:
                errors.append(
                    f"G25 scene {i:02d} settingspane spotlights row "
                    f"{sc['focus']!r} at {sc.get('focusAt', 0.5):.2f}s but the "
                    f"scene is {dur:.2f}s — the highlight never lands.")
        for gi, grp in enumerate(sc.get("groups") or []):
            for ri, row in enumerate(grp.get("rows") or []):
                fa = row.get("flipAt")
                if fa is not None and fa + CUE_TAIL > dur + 0.01:
                    errors.append(
                        f"G25 scene {i:02d} settingspane row {gi}.{ri} "
                        f"({row.get('label')!r}) flips at {fa:.2f}s but the "
                        f"scene is {dur:.2f}s — the toggle never moves.")
        # a pane nobody can read is decoration
        rows = sum(len(g.get("rows") or []) for g in (sc.get("groups") or []))
        if rows == 0:
            errors.append(f"G25 scene {i:02d} settingspane has no rows.")

    # G26 — A COMPARISON MUST ACTUALLY COMPARE, AND MUST BE FAIR.
    # Structural, not stylistic: these follow from what the genre is.
    if fmt_name == "comparison":
        sides = beats.get("sides")
        if not (isinstance(sides, list) and len(sides) == 2
                and all(str(s).strip() for s in sides)):
            errors.append(
                "G26 a comparison reel must declare `sides: [\"A\", \"B\"]` — "
                "the two things being compared, named as they appear on "
                "screen.")
        n_cmp = sum(1 for sc in scenes if sc["type"] in COMPARE_TYPES)
        if n_cmp < COMPARE_MIN:
            errors.append(
                f"G26 only {n_cmp} comparison scene(s) ({sorted(COMPARE_TYPES)}) "
                f"— a comparison needs at least {COMPARE_MIN}. Fewer than that "
                "is a review of one product with the other mentioned.")
        a = sum(sc["durationSec"] for sc in scenes if sc.get("side") == "a")
        b = sum(sc["durationSec"] for sc in scenes if sc.get("side") == "b")
        if a + b > 0:
            share = a / (a + b)
            if not (BALANCE[0] <= share <= BALANCE[1]):
                lead = (sides or ["A", "B"])[0 if share > 0.5 else 1]
                errors.append(
                    f"G26 unbalanced: side A holds {share:.0%} of the "
                    f"single-sided screen time ({a:.1f}s vs {b:.1f}s), outside "
                    f"{BALANCE[0]:.0%}-{BALANCE[1]:.0%}. As cut this reads as "
                    f"an ad for {lead!r}, not a comparison. Tag scenes with "
                    "`side` and even them up.")
        else:
            warnings.append(
                "G26 no scene carries `side` — balance could not be checked. "
                "Tag single-product beats \"a\"/\"b\" so the cut is provable.")
        # the viewer must be able to tell which side is which
        for i, sc in enumerate(scenes):
            if sc["type"] == "comparesplit" and not (
                    sc.get("leftLabel") and sc.get("rightLabel")):
                errors.append(
                    f"G26 scene {i:02d} comparesplit is missing leftLabel/"
                    "rightLabel — an unlabelled split is two videos, not a "
                    "comparison.")
            if sc["type"] == "hcompare" and not (
                    sc.get("topLabel") and sc.get("bottomLabel")):
                errors.append(
                    f"G26 scene {i:02d} hcompare is missing topLabel/"
                    "bottomLabel.")

    # G53 — THE AUDIO MUST SAY THE APPROVED SCRIPT (2026-08-27).
    #
    # Until today the voice was SYNTHESISED FROM the sheet's script, so "what
    # he says" and "what was approved" matched by construction and no gate was
    # needed. The external-VO flow removes that: the read is generated in
    # ElevenLabs, outside everything this repo enforces, and then uploaded.
    # Nothing structural stops the wrong take, an older draft, or a file from
    # a different reel reaching the render with a valid G27 hash on the sheet.
    # G27 proves the TEXT was approved. G53 proves the AUDIO says it.
    #
    # THRESHOLD IS MEASURED, NOT INVENTED (G23 discipline). Every reel on this
    # machine with both a script and word timings, script vs its OWN audio:
    #
    #     iphone-third-interface    1.000
    #     iphone18-colors           0.962
    #     claude-memory-everywhere  0.948
    #     claude-eating-tokens      0.885   <- lowest legitimate
    #
    # The 0.885 is entirely whisper artefacts — "bill"/"bell", "100 000" for
    # "a hundred thousand", "summarise"/"summarize" — not drift. The same
    # scripts against a DIFFERENT reel's audio score 0.013 to 0.110. So the
    # legitimate band starts at 0.885 and the wrong-audio band tops out at
    # 0.110; 0.70 sits in the empty middle with margin on both sides.
    if vo_words and beats.get("script"):
        import difflib as _dl
        _script = _norm_words(str(beats["script"])).split()
        _spoken = _norm_words(" ".join(
            (x[0] if isinstance(x, (list, tuple)) else str(x))
            for x in vo_words)).split()
        if _script and _spoken:
            _ratio = _dl.SequenceMatcher(None, _script, _spoken).ratio()
            if _ratio < VO_SCRIPT_MATCH_FLOOR:
                _diff = []
                for _t, _i1, _i2, _j1, _j2 in _dl.SequenceMatcher(
                        None, _script, _spoken).get_opcodes():
                    if _t != "equal" and len(_diff) < 3:
                        _diff.append(
                            f"script {' '.join(_script[_i1:_i2])!r} -> "
                            f"heard {' '.join(_spoken[_j1:_j2])!r}")
                errors.append(
                    f"G53 the voice track does not say the approved script "
                    f"— {_ratio:.2f} match against a {VO_SCRIPT_MATCH_FLOOR} "
                    f"floor (real reels score 0.885-1.00; a different reel's "
                    f"audio scores under 0.11). "
                    + ("; ".join(_diff) if _diff else "")
                    + " Either the wrong audio file is in place, or the "
                    "script was edited after the read was generated. "
                    "Re-generate the voice from the approved words.")

    # G27 — THE USER APPROVED *THIS* SCRIPT (user rule 2026-08-12).
    # The sheet carries the narration it was built from plus the approval
    # hash recorded by tools/script_approval.py. Editing a word after the
    # user said yes changes the hash and stops the build — you cannot ship an
    # unapproved edit by accident, and you cannot approve a script and then
    # quietly generate a different one.
    script = beats.get("script")
    appr = beats.get("approval") or {}
    if not script or not str(script).strip():
        errors.append(
            "G27 the sheet carries no `script` — store the narration that was "
            "approved, so approval can be checked against what actually ships.")
    elif not appr.get("sha256"):
        errors.append(
            "G27 no `approval` on the sheet. Show the user the script and the "
            "beat plan, ask any open questions, wait for an explicit yes, then "
            "`python3 tools/script_approval.py approve <slug>` and copy the "
            "record onto the sheet. NOTHING is generated before this.")
    else:
        got = hashlib.sha256(
            " ".join(str(script).split()).encode()).hexdigest()
        if got != appr["sha256"]:
            errors.append(
                f"G27 the script changed after approval — approved "
                f"{appr['sha256'][:16]} at {appr.get('approvedAt')}, sheet now "
                f"has {got[:16]}. Show the user what changed and re-approve.")

    # G28 — SFX MUST EXIST, AND MUST FIT THE BEAT THEY SIT ON (2026-08-13).
    # Derived from the user's two reference videos, which state the mapping
    # outright ("use whoosh to zoom in or out", "use pop or click for
    # pop-ups", "use riser to add suspense", "use camera shutter for
    # transitions", "use magic reveal to reveal stuff").
    #
    # Until today NOTHING checked the src at all: a typo'd filename produced a
    # SILENT cue that still counted toward G08's 6-9 budget, so a reel could
    # pass the sound gate with no sound.
    ROLE_FIT_TYPES = {
        "transition": None,          # any scene — it rides the cut
        "shutter": None,
        "popup": {"checklist", "specsheet", "chart", "timeline", "categorygrid",
                  "toolstack", "carousel", "statcard", "settingspane",
                  "notifstack", "uidialog", "desktopmockup", "priceladder"},
        "suspense": None,            # position-checked below, not type-checked
        "reveal": {"logoassemble", "brandhook", "logobeat", "wordcascade",
                   "typecard", "floatcard", "deviceframe", "annotatezoom",
                   "designreveal", "strikeswap", "problemsolved"},
        "impact": {"specsheet", "chart", "statcard", "receipt", "timeline",
                   "wordcascade", "typecard", "annotatezoom", "priceladder",
                   # a brand mark or hook LANDING is a statement landing —
                   # all three shipped reels chose this independently
                   "logoassemble", "brandhook", "logobeat", "osshook"},
        "comedic": None,
    }
    role_counts: Counter = Counter()
    for i, sc in enumerate(scenes):
        for c in (sc.get("sfx") or []):
            src = str(c.get("src") or "")
            entry = SFX_CAT.get(src)
            if entry is None:
                errors.append(
                    f"G28 scene {i:02d} uses SFX {src!r}, which is not in the "
                    "catalogue — an unknown cue renders SILENT while still "
                    "counting toward the G08 budget. See "
                    "`python3 tools/sfx_library.py`.")
                continue
            if not (SFX_DIR / src).exists():
                errors.append(
                    f"G28 scene {i:02d} SFX file is missing on disk: {src}")
                continue
            role = entry["role"]
            role_counts[role] += 1
            allowed = ROLE_FIT_TYPES.get(role)
            if allowed is not None and sc["type"] not in allowed:
                errors.append(
                    f"G40 scene {i:02d} ({sc['type']}) carries a {role!r} cue "
                    f"({src}) — {role} belongs on {ROLE_FITS[role]}. "
                    "A cue on the wrong beat is noise, however good the sound.")
            # a cue longer than the beat it sits on bleeds into the next one
            if entry["dur"] > sc["durationSec"] + 0.35 and role != "suspense":
                errors.append(
                    f"G40 scene {i:02d} SFX {src} runs {entry['dur']:.2f}s on a "
                    f"{sc['durationSec']:.2f}s scene — it bleeds into the next "
                    "beat. Pick a shorter cue.")
            # comedic stings undercut reporting
            if role == "comedic":
                if fmt_name not in COMEDIC_OK_FORMATS:
                    errors.append(
                        f"G40 scene {i:02d} uses a comedic sting ({src}) in a "
                        f"{fmt_name!r} reel. Allowed formats: "
                        f"{sorted(COMEDIC_OK_FORMATS)} — a meme boom under a "
                        "factual claim reads as a joke about the claim.")
                if beats.get("tone") in COMEDIC_BLOCKED_TONES:
                    errors.append(
                        f"G40 scene {i:02d} uses a comedic sting ({src}) in a "
                        "serious-tone reel.")

    # a riser PROMISES a payoff — it must be followed by a reveal or impact
    for i, sc in enumerate(scenes):
        for c in (sc.get("sfx") or []):
            e = SFX_CAT.get(str(c.get("src") or ""))
            if not e or e["role"] != "suspense":
                continue
            nxt = scenes[i: i + 4]        # payoff may share the beat
            paid = any(
                SFX_CAT.get(str(cc.get("src") or ""), {}).get("role")
                in ("reveal", "impact")
                for s2 in nxt for cc in (s2.get("sfx") or []))
            if not paid:
                errors.append(
                    f"G40 scene {i:02d} builds suspense ({c.get('src')}) with "
                    "no payoff in the next 3 beats — a riser that does not "
                    "resolve into a reveal or an impact is a broken promise.")

    for role, cap in ROLE_MAX.items():
        if role_counts.get(role, 0) > cap:
            errors.append(
                f"G40 {role_counts[role]} {role!r} cues, max {cap} per reel — "
                "punctuation stops being punctuation when it repeats.")

    # G29 — SOURCE PAGES ARE CAPTURED ON MOBILE (user rule 2026-08-13).
    # Every reel is 9:16. A desktop capture (1200x900) forced into a 1080x1920
    # frame fits to 1080x810 — 42% of the frame height — and the body text is
    # unreadable on a phone. A mobile capture at 360x780 @3 lands at 1080x2340:
    # native width, type already sized for a hand, room to pan.
    # `tools/capture.mjs` now defaults to mobile; this catches a stale or
    # hand-made desktop asset sneaking in.
    for i, sc in enumerate(scenes):
        if sc["type"] != "sourceread":
            continue
        sw, sh = sc.get("srcWidth"), sc.get("srcHeight")
        if not sw or not sh:
            errors.append(
                f"G29 scene {i:02d} sourceread is missing srcWidth/srcHeight — "
                "the component needs them to place highlights.")
            continue
        if sh <= sw:
            errors.append(
                f"G29 scene {i:02d} sourceread uses a {sw}x{sh} LANDSCAPE "
                "capture. Source pages are captured on mobile: "
                "`node tools/capture.mjs screenshot <url> --out <f>.png` "
                "(mobile is the default, 1080x2340). A desktop grab fits to "
                "1080x810 in a 9:16 frame and the text is unreadable.")
        elif sw < 1000:
            errors.append(
                f"G29 scene {i:02d} sourceread capture is only {sw}px wide — "
                "it will upscale into the 1080px frame. Capture at "
                "--scale 3 (360x780 @3 = 1080x2340).")

    # G29b — A DESKTOP (landscape) CAPTURE IS ALLOWED, BUT IT MUST BE CROPPED
    # AND MOVED, NEVER FITTED WHOLE (user rule 2026-08-13).
    # Some sources cannot be shot on mobile: software UIs, dashboards, wide
    # comparisons, pages with no mobile layout. Reference short q4_-y67JGCU
    # handles exactly this — the wide Claude desktop app is CROPPED to the
    # composer region, scaled until the text reads, and the crop window pans
    # slowly. It is never letterboxed into the 9:16 frame.
    # `annotatezoom` is our component for that: it eases from wide into an
    # explicit `focus` rect. Without `focus` it settles on the union of the
    # annotations — which, on a wide capture with no annotations, is the whole
    # page, i.e. a letterbox.
    for i, sc in enumerate(scenes):
        if sc["type"] != "annotatezoom":
            continue
        sw, sh = sc.get("srcWidth"), sc.get("srcHeight")
        if not sw or not sh:
            continue
        if sw > sh and not sc.get("focus"):
            has_ann = bool(sc.get("annotations"))
            if not has_ann:
                errors.append(
                    f"G29 scene {i:02d} annotatezoom uses a {sw}x{sh} LANDSCAPE "
                    "capture with no `focus` rect and no annotations — the "
                    "camera would settle on the whole wide page, which "
                    "letterboxes into 9:16. Declare `focus` on the region that "
                    "actually matters, so the shot crops in and reads.")

    # G32 — THE OUTRO MUST SIT WHERE PEOPLE READ IT (user rule, twice).
    # Asked for on 2026-08-12 ("outro caption should be centre / slightly
    # below") and STILL shipped at y=0.07 on september-preview, because it was
    # only ever written down. A headline in the closing stretch of the reel is
    # the CTA; at the top of the frame it competes with nothing and gets
    # missed, and on Instagram the top band is where the UI chrome sits.
    # Was 0.45 — an arbitrary "mid-frame or just below". The RULE is only that
    # the outro must clear the platform's own furniture: Instagram's top header
    # sits at y 0.100 and its account row at y 0.835 (src/platformSafeArea.ts).
    # Anything inside that window is a composition choice, not a violation.
    OUTRO_Y_MIN, OUTRO_Y_MAX = 0.12, 0.80
    with_head = [(i, sc) for i, sc in enumerate(scenes)
                 if isinstance(sc.get("headline"), dict)]
    if with_head:
        li, lsc = with_head[-1]
        start = sum(s["durationSec"] for s in scenes[:li])
        if total and start >= total * 0.80:          # in the closing fifth
            y = lsc["headline"].get("y")
            if y is None or y < OUTRO_Y_MIN or y > OUTRO_Y_MAX:
                errors.append(
                    f"G32 the closing headline (scene {li:02d}, at "
                    f"{start:.1f}s of {total:.1f}s) sits at y={y} — put it "
                    f"inside y {OUTRO_Y_MIN}-{OUTRO_Y_MAX}, clear of "
                    "Instagram's top header (0.100) and its account row "
                    "(0.835). Where it goes inside that window is your call.")

    # G33 — SOUND MUST BE DESIGNED, NOT JUST PRESENT (2026-08-14).
    # september-preview passed G08 with 7 cues that were only THREE distinct
    # files, all from the old 5-file library: two whooshes, an impact, a click.
    # Nothing popped, nothing built, nothing revealed. Counting cues does not
    # measure sound design; variety and role coverage do.
    SFX_MIN_DISTINCT = 4
    all_cues = [str(c.get("src") or "") for s in scenes for c in (s.get("sfx") or [])]
    if all_cues:
        distinct = {c for c in all_cues if c}
        if len(distinct) < SFX_MIN_DISTINCT:
            errors.append(
                f"G33 only {len(distinct)} distinct SFX file(s) across "
                f"{len(all_cues)} cues — a reel needs at least "
                f"{SFX_MIN_DISTINCT}. Repeating two sounds reads as an accident, "
                "not a sound design. See `python3 tools/sfx_library.py`.")
        roles = {SFX_CAT[c]["role"] for c in distinct if c in SFX_CAT}
        if len(roles) < 2:
            errors.append(
                f"G33 every cue is the same role ({sorted(roles)}) — use the "
                "palette: transition on cuts, popup when an element enters, "
                "impact on the biggest claim.")

    # G14 — WE CREDIT THE SOURCES WE USE (user policy 2026-08-11).
    # Every borrowed frame names where it came from, on screen. This is what
    # replaces hedging: we do not qualify a claim to death, we say who
    # reported it. Avatar scenes are ours and need no credit.
    CREDIT_TYPES = {"footage", "floatcard", "split", "receipt", "comparesplit",
                    "hcompare", "deviceframe", "annotatezoom"}
    for i, sc in enumerate(scenes):
        if sc["type"] not in CREDIT_TYPES:
            continue
        srcs = [str(sc.get(k) or "") for k in ("src", "topSrc", "leftSrc")]
        if any("avatar-master" in v for v in srcs):
            continue
        # creditOnScreen (user directive 2026-08-25): when the SOURCE'S OWN
        # IDENTITY is visible inside the frame — a recorded page showing its
        # masthead or URL, a terminal showing the command being run — a credit
        # chip repeats what the pixels already say and reads as clutter. The
        # flag is a per-scene declaration that the scout LOOKED and the
        # identity is in frame; a crop that strips the chrome must keep its
        # credit. The rule stays: every borrowed frame names its source on
        # screen — this only recognises frames that name it themselves.
        if sc.get("creditOnScreen") is True:
            continue
        if not str(sc.get("credit") or "").strip():
            errors.append(
                f"G14 scene {i:02d} ({sc['type']}) borrows footage with no "
                "`credit` — every third-party frame names its source on screen.")

    # G15 — every card that states a NUMBER carries where the number came from.
    # A data card without a source is an assertion; with one it is reporting.
    for i, sc in enumerate(scenes):
        if sc["type"] not in ("specsheet", "chart", "timeline", "statcard"):
            continue
        attribution = (str(sc.get("source") or "") + str(sc.get("footnote") or "")).strip()
        if not attribution:
            errors.append(
                f"G15 scene {i:02d} ({sc['type']}) shows data with no `source` "
                "or `footnote` — name who reported the number.")

    # G16 — STANDARD VISUAL NOTATION (user rule 2026-08-11). Every number,
    # money figure, percentage, unit and version appears on screen in normal
    # form. Whisper emits "23 .2" and "85 %"; spoken text says "thirty
    # trillion rupees". None of that belongs on a frame.
    canon = (manifest or {}).get("notation") or {}
    for c in beats.get("captions", []):
        v = violations(c.get("text", ""), canon)
        if v:
            errors.append(
                f"G16 caption {c.get('text')!r} is not in standard notation "
                f"({', '.join(v)}) -> should read "
                f"{normalise(c.get('text', ''), canon)!r}")
    # authored card text is held to the same standard
    for i, sc in enumerate(scenes):
        texts = []
        for r in sc.get("rows", []) or []:
            texts += [str(r.get("label") or "")] + [str(x) for x in (r.get("values") or [])]
        for it in sc.get("items", []) or []:
            texts += [str(it.get("label") or ""), str(it.get("display") or ""),
                      str(it.get("sub") or "")]
        for w in sc.get("words", []) or []:
            texts.append(str(w.get("text") or ""))
        hl = sc.get("headline")
        if isinstance(hl, dict):
            texts += [str(l.get("text") or "") for l in hl.get("lines", [])]
        texts += [str(sc.get(k) or "") for k in ("title", "kicker", "footnote", "source")]
        for t in texts:
            if t and violations(t, canon):
                errors.append(
                    f"G16 scene {i:02d} text {t!r} is not in standard notation "
                    f"-> {normalise(t, canon)!r}")

    # G35 — A STILL IN `footage` OR `floatcard` RENDERS BLACK (2026-08-17,
    # ios27-tiers). FootageScene and FloatingCard both render a Remotion
    # <OffthreadVideo>. Only `split` (which branches on file extension),
    # `receipt` and `annotatezoom` take an <Img>.
    #
    # CORRECTED 2026-08-17 by actually rendering the offenders. This said "a
    # still renders BLACK", which was asserted from reading the components and
    # never checked. The truth is worse and stranger:
    #
    #   iphone-fold-ultra scene 23   renders PERFECTLY — card, text, credit
    #   september-preview scene 01   kills the render outright:
    #     "Compositor error: No frame found at position 40 ... mrs-hero.png"
    #
    # ffmpeg decodes a PNG as a ONE-FRAME video, so OffthreadVideo succeeds at
    # position 0 and fails at every later position. Whether a given scene works
    # depends on which frame is requested, which is why these shipped: the reels
    # rendered once and looked fine. It is a position-dependent hard failure,
    # not a visual defect — the worst kind, because it passes until it doesn't.
    #
    # I nearly "fixed" 16 correctly-rendering scenes on the strength of the old
    # wording, and nearly deleted the gate on the strength of the first render.
    # Both would have been wrong.
    STILL_EXT = (".png", ".jpg", ".jpeg", ".webp", ".avif")
    for i, sc in enumerate(scenes):
        if sc["type"] not in ("footage", "floatcard"):
            continue
        for key in ("src", "mediaSrc"):
            v = str(sc.get(key) or "").lower()
            if v.endswith(STILL_EXT):
                errors.append(
                    f"G35 scene {i:02d} ({sc['type']}) plays a STILL "
                    f"{str(sc.get(key)).split('/')[-1]!r} — {sc['type']} renders "
                    "an <OffthreadVideo>, and a still gives it exactly ONE "
                    "frame. Asking for any later position KILLS THE RENDER: "
                    "\"Compositor error: No frame found at position N\". Use "
                    "receipt or annotatezoom for a still, or cut it to an mp4.")

    # G36 — A WIDE SOURCE TURNS `annotatezoom` INTO DEAD SPACE (2026-08-17,
    # ios27-tiers). AnnotateZoom sizes its card as
    #   cardW = width*0.9; cardH = (srcHeight/srcWidth)*cardW
    # so the card inherits the SOURCE aspect. A 942x205 footnote strip (4.6:1)
    # becomes a thin horizontal band in a 1920-tall frame: measured ~16% frame
    # fill, i.e. ~84% blurred dead space, against a 30% ceiling. The fix is a
    # PORTRAIT source mined for several `focus` rects, not one strip per quote.
    for i, sc in enumerate(scenes):
        if sc["type"] != "annotatezoom":
            continue
        sw, sh = sc.get("srcWidth"), sc.get("srcHeight")
        if not sw or not sh:
            continue
        aspect = sw / sh
        if aspect > AZ_ASPECT_MAX:
            fill = min(1.0, (sh / sw) * 0.9 / (1920 / 1080))
            errors.append(
                f"G36 scene {i:02d} annotatezoom source is {sw}x{sh} "
                f"({aspect:.2f}:1, over {AZ_ASPECT_MAX}:1) — the card inherits "
                f"the source aspect, so it fills only ~{fill * 100:.0f}% of the "
                "frame and the rest is blurred fill. Crop ONE TALL page region "
                "and move the camera with `focus` instead of cropping a strip "
                "per quote.")

    # G12 — the plain black typecard is a last resort, max once
    black_cards = sum(1 for s in scenes
                      if s["type"] == "typecard" and s.get("bg") in (None, "black"))
    if black_cards > 1:
        errors.append(
            f"G12 {black_cards} plain black typecards — max 1 per reel, and "
            "it is a fallback of last resort (rule 2026-07-22).")

    # G37 — A MUSIC BED THAT CANNOT HEAR THE VOICE (2026-08-17).
    # Volume was five hardcoded clock times. Measured across six shipped reels,
    # the bed sat at 0.118 under speech and 0.120 in the pauses — separation
    # +0.003 — and on THREE of them the separation was NEGATIVE: the music was
    # louder under the voice than in the gaps. It was a guess dressed as an edit.
    # tools/duck_music.py derives the curve from whisper word timings, which we
    # already hold, and stamps `derivedFrom`. Deriving it took separation to
    # +0.031..+0.062. A hand-written curve is now a blocking error, because the
    # hand-written ones were measurably wrong every single time.
    music = beats.get("music")
    if music:
        pts = music.get("points") or []
        if not music.get("derivedFrom"):
            errors.append(
                f"G37 music.points is hand-written ({len(pts)} points) — derive "
                f"it from the voice: python3 tools/duck_music.py {beats.get('id', '<slug>')} "
                "--write. Hardcoded clock times cannot hear the VO; measured "
                "across six reels they ducked by +0.003, and three were inverted.")
        elif len(pts) < 8:
            errors.append(
                f"G37 music.points claims to be derived but has only {len(pts)} "
                "points — a real duck curve has 4 per speech run. Re-run "
                "tools/duck_music.py.")

    # G38 — FRAME ZERO MUST CARRY MOTION AND SOMETHING LEGIBLE ON MUTE.
    # From the `going-viral` skill, which is research-grounded (Berger & Milkman:
    # sharing tracks AROUSAL, not positivity) and states it plainly: "Frame 0 IS
    # the hook. The biggest element is already on screen AND moving... legible on
    # mute (70-85% watch sound-off). No fade-from-black, no slow logo build, no
    # title card."
    #
    # Audited 2026-08-17: eight reels open on `split` (two live sources — right),
    # but THREE open on `logoassemble` with `hideCaptions: true` — a logo drawing
    # itself with no words on screen. That is the exact anti-pattern, and it
    # shipped three times because the rule lived in a skill nobody was told to
    # read at this stage.
    #
    # This DOES newly fail those three sheets. That is the point: they are the
    # bug, not the precedent worth protecting.
    if scenes:
        s0 = scenes[0]
        if s0["type"] not in MOTION_TYPES and s0["type"] not in BUILDING_TYPES:
            # G43, NOT G38 — split 2026-08-17. "Open on motion, never a logo
            # build" is going-viral's craft advice and it is good advice, but it
            # is TASTE: a short brand mark is a legitimate channel signature, and
            # the constitution says only the three rules are law. Bundling it
            # with the mute-legibility check meant a judgement call blocked three
            # reels under Rule 1's badge — the same mistake as G28 and G41.
            errors.append(
                f"G43 the hook (scene 00) is `{s0['type']}` — going-viral says "
                "frame 0 should already be MOVING and show the subject, not a "
                "mark that assembles. Advice, not law: a brand opener is a "
                "choice, and this one costs you the first ~2s of attention.")
        if s0.get("hideCaptions"):
            errors.append(
                "G38 the hook (scene 00) sets hideCaptions — 70-85% of viewers "
                "watch on mute, so a hook with no words on screen says nothing. "
                "Show the claim.")

    # G51 — THE ARRAY THE COMPONENT MAPS OVER MUST EXIST (RENDER, 2026-08-25).
    # The registry imports scene JSON with a cast, so TypeScript never checks
    # it; a statcard authored with an invented stat/unit shape passed tsc,
    # validate_job and every gate, then crashed remotion at frame 538 with
    # "Cannot read properties of undefined (reading 'map')". Mirror each
    # component's hard `.map()` contract here — fields with defaults are the
    # component's business, fields it maps over unconditionally are ours.
    MAPPED_FIELDS = {"statcard": "rows", "sourceread": "lines"}
    for i, sc in enumerate(scenes):
        field = MAPPED_FIELDS.get(sc.get("type", ""))
        if field is None:
            continue
        rows = sc.get(field)
        if not isinstance(rows, list) or not rows:
            errors.append(
                f"G51 scene {i:02d} ({sc['type']}) has no {field!r} — the "
                f"component maps over it unconditionally, so the render "
                f"crashes. Author the scene in the component's real shape "
                f"(see src/types.ts / a shipped {sc['type']}).")

    # G54 — WORDCASCADE `size` IS A MULTIPLIER, AND NOTHING SAID SO (RENDER,
    # 2026-09-01). WordCascade computes `fontSize: 100 * size`, so `size: 150`
    # is 15,000px on a 1920px frame. The qualcomm-chip-hike draft shipped that
    # to a render: the frame filled with the inside of a single letter, and the
    # only thing that noticed was a soft [DEAD SPACE] lint flag that is easy to
    # walk past. src/types.ts documents it as "relative size multiplier
    # (default 1)"; the ceiling below is where 100 * size passes the frame
    # height, with generous slack — the largest deliberate use in this repo is
    # about 2.5, so a real scene never comes near it.
    FRAME_H = 1920
    MAX_MULT = FRAME_H / 100.0          # 19.2 — type taller than the frame
    for i, sc in enumerate(scenes):
        if sc.get("type") != "wordcascade":
            continue
        for w in sc.get("words", []):
            mult = w.get("size", 1)
            if isinstance(mult, (int, float)) and mult >= MAX_MULT:
                errors.append(
                    f"G54 scene {i:02d} (wordcascade) word {w.get('text','')!r} "
                    f"has size {mult} — that is a MULTIPLIER on a 100px base, "
                    f"so it asks for {int(100 * mult)}px type on a {FRAME_H}px "
                    f"frame. What renders is the inside of one glyph. Use a "
                    f"multiplier (1 = 100px; about 1.5 for a headline word).")

    # G39 — WHAT IS ON SCREEN MUST BE WHAT IS BEING SAID (user rule 2026-08-17:
    # "what we see on the video should match as much as possible with what
    # creator says").
    #
    # This is the rule the engine has been missing since the September teardown,
    # where the user wrote: "We must have scouted sources according the script and
    # try to show the exact same thing in the video whenever possible." It stayed
    # prose for five days.
    #
    # A gate cannot judge whether a picture means what a sentence means. What it
    # CAN do is refuse the case where nobody ever stated the link: every scene
    # that puts a SOURCE on screen must name the phrase it illustrates, and that
    # phrase must actually be spoken WHILE the scene is up. That turns "show the
    # same thing" from an intention into something with a right answer.
    #
    # The presenter's own footage is exempt — the avatar is not evidence.
    # SCOPE, set by the user 2026-08-17 after measuring what this actually
    # demanded: 154 scenes, of which only 14 put a DOCUMENT on screen and 140
    # were b-roll cutaways — 88 of those sitting under a sentence FRAGMENT.
    # "covers: 'cameras, and that's'" cannot fail meaningfully; it is
    # box-ticking, and box-ticking teaches people to ignore the output (see G21,
    # which reached 100% false positives before anyone noticed).
    #
    # So a source used as PROOF must name the claim it proves — that is Rule 3
    # with teeth. B-roll gets G44, advisory, because the real risk there is a
    # clip sitting against the wrong sentence, which is worth flagging and not
    # worth blocking.
    EVIDENCE_TYPES = {"receipt", "sourceread", "annotatezoom"}
    if vo_words:
        wt: list[tuple[str, float, float]] = []
        for x in vo_words:
            if isinstance(x, (list, tuple)) and len(x) >= 3:
                try:
                    wt.append((str(x[0]), float(x[1]), float(x[2])))
                except (TypeError, ValueError):
                    pass
        if wt:
            cursor = 0.0
            for i, sc in enumerate(scenes):
                start = cursor
                cursor += sc["durationSec"]
                end = cursor
                if not _shows_source(sc):
                    continue
                spoken = " ".join(w for w, a, b in wt if b > start and a < end)
                if not _norm_words(spoken):
                    # Nothing is being said over this beat — a held image or a
                    # deliberate musical pause. There is no line to match, so
                    # demanding one would make a legitimate beat unfixable.
                    continue
                covers = str(sc.get("covers") or "").strip()
                evidence = sc["type"] in EVIDENCE_TYPES
                if not covers:
                    if evidence:
                        errors.append(
                            f"G39 scene {i:02d} ({sc['type']}) puts a DOCUMENT on "
                            f"screen but never says WHICH line it proves. Add "
                            f"`covers` — the phrase this visual proves. Spoken "
                            f"over it: {_norm_words(spoken)[:64]!r}")
                    else:
                        errors.append(
                            f"G44 scene {i:02d} ({sc['type']}) is b-roll with no "
                            f"stated line. Worth checking it is not sitting "
                            f"against the wrong sentence — spoken over it: "
                            f"{_norm_words(spoken)[:56]!r}")
                elif _norm_words(covers) not in _norm_words(spoken):
                    # Whisper is NOT ground truth for what was said (G21's
                    # lesson, measured at 100% false positives). The caption
                    # stream in the same window has caption_corrections
                    # applied — the declared record of what the voice
                    # actually says where whisper miswrote it ("re-reads" ->
                    # "reads", "agent's" -> "agents", both 2026-08-25). A
                    # `covers` found there is spoken; only fail when BOTH
                    # streams miss it.
                    cap_spoken = " ".join(
                        str(c.get("text", "")) for c in
                        (beats.get("captions") or [])
                        if isinstance(c, dict)
                        and float(c.get("end", 0)) > start
                        and float(c.get("start", 0)) < end)
                    if _norm_words(covers) in _norm_words(cap_spoken):
                        continue
                    errors.append(
                        f"{'G39' if evidence else 'G44'} scene {i:02d} "
                        f"({sc['type']}) claims to cover "
                        f"{covers!r}, but those words are not spoken while it is "
                        f"on screen ({start:.1f}-{end:.1f}s says "
                        f"{_norm_words(spoken)[:64]!r}) — move the scene to the "
                        "line it illustrates, or point it at what is actually "
                        "being said.")

    # G47 — CREDITS SUPPRESSED FOR THIS REEL. Advice, and loud.
    #
    # The user can turn on-screen credits off per video (RULES.md 2c). The flag
    # carries its own reason — `noCredits: {reason}` — so it cannot be set as a
    # bare switch, the same shape as allowLong + allowLongReason and the capture
    # tool's --desktop-reason.
    #
    # This does NOT block: it is the user's call, stated at topic time. What it
    # refuses to do is happen quietly. A reel that ships with no attribution on
    # screen should say so in the one place somebody reads before rendering.
    nc = beats.get("noCredits")
    if nc:
        reason = (nc or {}).get("reason", "") if isinstance(nc, dict) else ""
        n_sources = len({(sc.get("credit") or "").strip()
                         for sc in scenes if sc.get("credit")})
        if not reason.strip():
            errors.append(
                "G47 noCredits is set with no reason. It takes `{\"reason\": "
                "\"...\"}` — the flag is an argument, not a switch.")
        else:
            errors.append(
                f"G47 this reel draws NO source credits on screen ({n_sources} "
                f"source(s) still recorded in the sheet). Reason: {reason!r}. "
                f"The manifest and G14 are unaffected; the licence terms of any "
                f"borrowed material are not — check them separately.")

    # G45 (RULE 1, blocking) + G46 (craft, advice) — WHERE A CAPTION MAY SIT.
    #
    # SPLIT 2026-08-18, the day after G45 was written, because as first written
    # it was the exact defect this whole restructure exists to delete.
    #
    # It blocked every caption below bottom 500 (y 0.740) with the reason "under
    # the platform's own UI". But the platform's own UI is MEASURED, and it
    # starts at y 0.835 — Instagram's account row, per src/platformSafeArea.ts.
    # A caption at y 0.78 is not under anything Instagram draws. It is sitting
    # on OUR source credit, which is our layout, our choice, and taste.
    #
    # So 183px of that band was craft wearing an R1 badge — the same fault the
    # G18 note describes ("a fixed number wearing an R3 badge"), committed by
    # the same hand that wrote the note. The user's constitution is that ONLY
    # "we are making videos for Reels and Shorts" may block. Being covered by
    # Instagram's chrome is that rule. Colliding with our own credit is not.
    #
    # G45 now blocks ONLY at the measured furniture. Everything above it is
    # G46, advice — and src/platformSafeArea.ts still clamps at render time, so
    # the frame is correct either way. The difference is that a person, not a
    # gate, decides whether a caption riding the credit lane is wrong here.
    #
    # 317 = round(1920 * (1 - 0.835)): the caption's LOWEST ink must stay above
    # the account row. 500 = platformSafeArea.captionFloorPx(1920). Both are
    # asserted in tools/test_gates.py so neither can drift from its source.
    PLATFORM_FLOOR = 317
    CAPTION_FLOOR = 500
    for i, sc in enumerate(scenes):
        cb = sc.get("captionBottom")
        if cb is None or sc.get("hideCaptions"):
            continue
        cb = int(cb)
        y = 1 - cb / 1920
        if cb < PLATFORM_FLOOR:
            errors.append(
                f"G45 scene {i:02d} sets captionBottom {cb} (y {y:.3f}) — under "
                f"Instagram's own account row (measured y 0.835). The platform "
                f"paints over this; the words cannot be read on either app. "
                f"Raise it above {PLATFORM_FLOOR}, or drop the field.")
        elif cb < CAPTION_FLOOR:
            errors.append(
                f"G46 scene {i:02d} sets captionBottom {cb} (y {y:.3f}) — clear "
                f"of the platform, but inside our own credit lane (floor "
                f"{CAPTION_FLOOR}, y 0.740). The renderer clamps it, so the "
                f"frame is fine; worth deciding on purpose rather than "
                f"inheriting the clamp.")

    # G41 (Rule 2, blocking) + G42 (tier, advice) — WHERE EACH SOURCE CAME
    # FROM, AND HOW IT WAS CAPTURED.
    #
    # TWO IDS ON PURPOSE. One id carrying both a blocking claim and an
    # advisory one is the G28 mistake: taste ends up blocking under a
    # borrowed badge, and classification cannot separate them.
    #
    # Two rules meet here, and they are deliberately split between blocking and
    # advice because they are different KINDS of claim.
    #
    # RULE 2 is blocking, and this is the first time it is actually CHECKED
    # rather than inferred. G29 guesses "was this mobile?" from the image aspect,
    # which cannot tell a real 360x780 render from a tall crop of a desktop page.
    # tools/capture.mjs now writes a provenance sidecar at capture time, so a
    # desktop capture is a recorded fact — and one taken without a stated reason
    # is a Rule 2 violation, not a matter of opinion.
    #
    # TIER is advice. "Official beats reliable beats merely-relevant" is real
    # editorial craft, but an unannounced product is usually NOT on an official
    # source, so a reel leaning on reliable outlets is normal work, not a defect.
    # It gets counted and reported, and the author decides.
    if manifest:
        assets = manifest.get("assets") or manifest.get("items") or []
        by_id = {str(a.get("id")): a for a in assets if a.get("id")}
        used = [str(sc.get("assetId")) for sc in scenes if sc.get("assetId")]
        tiers: dict[str, int] = {}
        untiered: list[str] = []
        for aid in dict.fromkeys(used):
            a = by_id.get(aid) or {}
            cap = a.get("capture") or {}
            tier = a.get("tier") or cap.get("tier")
            if tier:
                tiers[tier] = tiers.get(tier, 0) + 1
            else:
                untiered.append(aid)
            if cap and cap.get("mobile") is False and not cap.get("desktopReason"):
                errors.append(
                    f"G41 asset {aid!r} was captured on DESKTOP with no reason "
                    f"recorded ({cap.get('viewport')}) — sources are scouted on "
                    "mobile view first; if mobile genuinely could not show it, "
                    "say so with --desktop-reason.")
        if tiers.get("fallback"):
            errors.append(
                f"G42 {tiers['fallback']} source(s) are tier 'fallback' — merely "
                "relevant, not the thing being said. Try official, then a named "
                "reporter at an established outlet, before settling.")
        if untiered:
            errors.append(
                f"G42 {len(untiered)} source(s) record no tier "
                f"({', '.join(untiered[:5])}{'...' if len(untiered) > 5 else ''}) "
                "— capture with --tier so how well-sourced the reel is can be "
                "counted instead of guessed.")

    # G48 — RENDER: framing that exposes frame the source cannot fill.
    #
    # ADDED 2026-08-20 with `focusY` and `zoom`, for camera-snap cuts. Both
    # failures here paint the black backdrop, which is the same category as G35
    # (a still in a video slot renders black) — not taste:
    #
    #   zoom < 1        scales the layer BELOW the canvas, so the backdrop shows
    #                   around it. `scale(0.8)` is a 9:16 reel with black bars.
    #   focus outside   objectPosition past 0..1 pushes the image beyond the
    #   0..1            slack `cover` gives it, exposing the backdrop at an edge.
    #
    # The bounds are not a chosen number — they are where the frame stops being
    # covered. That is why this one blocks and the compounding check below does
    # not. focusX was never validated before; it is checked here for the same
    # reason, since it fails the same way.
    for i, sc in enumerate(scenes):
        if sc.get("type") != "footage":
            continue
        for field in ("focusX", "focusY"):
            v = sc.get(field)
            if v is None:
                continue
            if not isinstance(v, (int, float)) or not (0.0 <= float(v) <= 1.0):
                errors.append(
                    f"G48 scene {i:02d} sets {field}={v!r} — outside 0..1, so "
                    f"the frame is pushed past what `cover` can fill and the "
                    f"black backdrop shows at an edge. 0 = flush left/top, "
                    f"0.5 = centred, 1 = flush right/bottom.")
        z = sc.get("zoom")
        if z is not None:
            if not isinstance(z, (int, float)) or float(z) < 1.0:
                errors.append(
                    f"G48 scene {i:02d} sets zoom={z!r} — below 1 the scaled "
                    f"layer no longer covers the canvas and renders with black "
                    f"bars. 1 = fill, above 1 = punch in.")

    # G49 — the locked-off scale and the Ken Burns push COMPOUND.
    #
    # Advice, deliberately. `zoom` is the base the push runs from, so
    # `zoom: 1.6` with the default `zoomDir: "in"` ends at 1.76x, not 1.6x —
    # easy to hit by accident when `zoom` was added for locked-off snaps and
    # `zoomDir` defaults to "in" when omitted. Wanting a push FROM a tight base
    # is legitimate, so this cannot block; it only asks whether it was meant.
    for i, sc in enumerate(scenes):
        if sc.get("type") != "footage" or sc.get("zoom") is None:
            continue
        z = sc.get("zoom")
        if not isinstance(z, (int, float)) or float(z) < 1.0:
            continue                      # already a G48 failure; do not pile on
        dir_ = sc.get("zoomDir", "in")
        if dir_ != "none":
            errors.append(
                f"G49 scene {i:02d} sets zoom={z} AND zoomDir={dir_!r}, so the "
                f"scale compounds to {float(z) * 1.1:.2f}x by the "
                f"{'end' if dir_ == 'in' else 'start'} of the beat. For a "
                f"locked-off snap set zoomDir: \"none\"; if the push is meant, "
                f"this is only a note.")

    # G50 — ai-tools: text cards standing in for demos. ADVICE.
    #
    # The format's evidence doctrine (formats/ai-tools.md): a named tool is on
    # screen, running or being itself, while it is named. The 9-reel corpus
    # (2026-08-25 observation study) contains ZERO full-screen text-only
    # scenes — every "text moment" is a chip or label over something moving.
    # claude-eating-tokens v1 had SIX in fourteen beats, and is the reel that
    # forced the format to exist. The threshold is the corpus's own number
    # (zero), so even one advises; craft can override with a reason, which is
    # why this is advice and not law.
    if fmt_name == "ai-tools":
        texty = [i for i, sc in enumerate(scenes)
                 if sc.get("type") in ("typecard", "wordcascade")]
        if texty:
            errors.append(
                f"G50 ai-tools reel carries {len(texty)} full-screen text "
                f"scene(s) (scenes {', '.join(f'{i:02d}' for i in texty[:5])})"
                " — the 9-reel corpus runs ZERO: its text moments are chips "
                "over moving evidence. Show the tool, not a card about the "
                "tool (formats/ai-tools.md). Deliberate exceptions welcome — "
                "with a reason in questions.md.")

        # G52 — ai-tools: the CTA is a KEYWORD POP, not a simulated comment
        # box. ADVICE. Measured in the same observation study: all 9 corpus
        # reels close on one verb-first word in huge type over the presenter
        # (INSTALL / COMMENT / FOLLOW / SETUP); none draws a fake comment
        # field. The mock is the top5 pack's comment-gate, and it read wrong
        # on a reporting reel (user, 2026-08-25). Advice because a reel that
        # genuinely wants the gate should be able to take it.
        gates = [i for i, sc in enumerate(scenes)
                 if sc.get("type") == "commentcta"
                 and sc.get("variant", "gate") != "keyword"]
        if gates:
            errors.append(
                f"G52 ai-tools CTA scene(s) {', '.join(f'{i:02d}' for i in gates)}"
                " draw the simulated comment field. The corpus closes on a "
                "verb-first keyword pop over the face — set `variant: "
                "\"keyword\"` (formats/ai-tools.md). The gate mock is the "
                "top5 pack's treatment.")

    # ---- THE ONLY THINGS ALLOWED TO BLOCK A RENDER -------------------------
    #
    # Directive, 2026-08-17: "Nothing should be hardcoded, behind the gates and
    # rules except we are making videos for Instagram Reels and YouTube Shorts."
    # Plus two more: sources are scouted on MOBILE view first, and what is on
    # screen must match what the creator says.
    #
    # Everything else — runtime length, hook duration, facecam share, sound
    # density, how many highlights a beat carries, whether a genre "needs" a CTA
    # — is CRAFT JUDGEMENT and is now advice. It still gets computed and printed,
    # with the evidence that produced it, because the measurements were real and
    # throwing them away would be throwing away the teardowns behind them. It
    # just no longer refuses to render.
    #
    # A gate earns BLOCKING status only by belonging to one of these five:
    #   RULE 1  the output is an Instagram Reel / YouTube Short
    #   RULE 2  sources are captured on mobile first
    #   RULE 3  the picture matches the words
    #   RENDER  it does not technically work (black frames, missing files)
    #   RIGHTS  attribution and the user's own approval
    #
    # Anything not listed here is advice by DEFAULT — the safe direction. A new
    # gate has to argue its way onto this list rather than land here by accident.
    blocking, advice = _partition(errors)
    warnings = advice + warnings

    if blocking:
        msg = (f"{len(blocking)} blocking violation(s) — these are the only "
               f"rules that stop a render:\n  - " + "\n  - ".join(blocking))
        if advice:
            msg += (f"\n\n  {len(advice)} advisory note(s) from the same run — "
                    "judgement, not law:\n  - " + "\n  - ".join(advice))
        raise GateError(msg, advice=warnings)
    return warnings


# ─────────────────────────────────────────────────────────────────────────────
# THE FINISHED MASTER
#
# Every gate above reads the beat sheet — a statement of INTENT. This one reads
# the artifact, because the mastering step is where intent and result routinely
# disagree and nothing was checking.
# ─────────────────────────────────────────────────────────────────────────────

LUFS_TARGET = -14.0        # Instagram / YouTube / Spotify normalisation target
LUFS_TOL = 1.0             # two-pass lands ~0.5 LU short; ~1 LU is normal
TRUE_PEAK_CEILING = -1.0   # dBFS. RULES.md master spec is TP -1.0 to -1.2.
                           # MEASURED CAVEAT (2026-08-17): a real master asking
                           # loudnorm for TP=-1.2 came back at exactly -1.0
                           # after AAC encode — lossy encoding moves peaks, so
                           # the headroom here is ZERO, not 0.2 dB. If this
                           # trips on a clean reel, lower the loudnorm TP in
                           # render_job.py; do NOT loosen the ceiling, which is
                           # the number the platform actually applies.

_EBUR_I = re.compile(r"^\s*I:\s*(-?[\d.]+|-inf)\s*LUFS", re.M)
_EBUR_TP = re.compile(r"^\s*Peak:\s*(-?[\d.]+|-inf)\s*dBFS", re.M)


def parse_ebur128(text: str) -> tuple[float, float]:
    """Integrated loudness (LUFS) and true peak (dBFS) from an ebur128 summary.

    Both patterns anchor on the SUMMARY block's indented labels. The per-frame
    lines carry the same numbers under different labels (`t: ... I: ... TPK:`)
    but are prefixed with `[Parsed_ebur128_0 @ ...]`, so they cannot match.
    The last match wins in case a chain ever emits two summaries.
    """
    i_hits = _EBUR_I.findall(text)
    tp_hits = _EBUR_TP.findall(text)
    if not i_hits or not tp_hits:
        raise GateError(
            "G31 could not read an ebur128 summary from ffmpeg's output. A "
            "check that cannot fail is not a check: treat this as a FAILURE, "
            "not a skip. Most likely cause is `-v error`, which hides filter "
            "statistics — the measurement needs `-hide_banner -nostats`.")
    return float(i_hits[-1]), float(tp_hits[-1])


# G31 — THE DELIVERED MASTER MUST ACTUALLY HIT -14 LUFS (2026-08-17).
# Declared as a comment in this exact shape on purpose: test_gates.py scrapes
# `# G\d\d — ` out of this file to build the list of gates it then demands a
# failing case for. A gate documented only in a docstring is invisible to that
# coverage assertion, i.e. untested while looking tested.
def master_errors(integrated: float, true_peak: float) -> list[str]:
    """Blocking loudness checks on a finished master.

    Pure, so the self-test can exercise it without rendering anything.

    WHY: `loudnorm` is adaptive and streaming, so a SINGLE pass ends carrying a
    residual offset it never applies — it undershoots its own target and says
    nothing. render_job.py ran exactly that chain from the day it was written.

    Measured 2026-08-17 on out/apple-pay-india-raw.mp4 (100.8s full mix,
    target I=-14):

        single pass  -15.2 LUFS   1.2 LU short   <- outside this tolerance
        two pass     -14.2 LUFS   0.2 LU short

    and pass 1 of the single-pass chain reported the miss ITSELF as
    `target_offset=1.18`, which is precisely what it then failed to apply.
    Two LU quieter than target is not cosmetic: platform normalisation leaves
    the reel quieter than everything around it in the feed.

    The gate does NOT read loudnorm's own report. It re-measures the finished
    file with ebur128 — measure the artifact, never the filter that produced
    it — because a chain that lies about its output would otherwise pass by
    quoting itself.
    """
    errors: list[str] = []
    gap = integrated - LUFS_TARGET
    if abs(gap) > LUFS_TOL:
        errors.append(
            f"G31 master is {integrated:.1f} LUFS, {abs(gap):.1f} LU "
            f"{'over' if gap > 0 else 'under'} the {LUFS_TARGET:.0f} LUFS "
            f"target (tolerance ±{LUFS_TOL:.1f} LU). A single loudnorm pass "
            "undershoots by design — master with the TWO-pass chain in "
            "scripts/render_job.py, which feeds pass 1's measured_* values "
            "and offset back into pass 2.")
    if true_peak > TRUE_PEAK_CEILING:
        errors.append(
            f"G31 master true peak is {true_peak:+.1f} dBFS, over the "
            f"{TRUE_PEAK_CEILING:+.1f} dBFS ceiling — it will clip on lossy "
            "re-encode. Lower the loudnorm TP target.")
    return errors


def check_master(path: Path) -> tuple[float, float]:
    """Measure a finished master with ebur128 and raise on a G31 violation."""
    path = Path(path)
    if not path.exists():
        raise GateError(f"G31 no master to measure at {path}")
    # `-v error` would HIDE the filter's summary and this would silently read
    # nothing. `-hide_banner -nostats` keeps the statistics and drops the noise.
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True)
    integrated, true_peak = parse_ebur128(proc.stderr)
    # Route through the SAME classification as every other check. This function
    # was written in a worktree before BLOCKING_RULES existed and raised
    # directly, which meant G31 blocked unconditionally while everything else
    # declared its status — one authority is the whole point, and an exception
    # that quietly opts out of it is how the old 37-rule sprawl happened.
    blocking, advice = _partition(master_errors(integrated, true_peak))
    for note in advice:
        print(f"  warning: {note}")
    if blocking:
        raise GateError(
            f"{len(blocking)} blocking violation(s):\n  - "
            + "\n  - ".join(blocking), advice=advice)
    return integrated, true_peak


def print_formats() -> None:
    """Single source of truth for the per-format numbers.

    Docs must PRINT this rather than restate it — four separate stale-prose
    drifts were found on 2026-08-12 alone, every one a doc quoting a number
    that had since moved.
    """
    w = max(len(k) for k in FORMATS)
    print(f"{'format'.ljust(w)}  runtime    hook   facecam  sfx   sfx-vol"
          "      cta")
    for name, pr in FORMATS.items():
        rt = f"{pr['runtime'][0]:.0f}-{pr['runtime'][1]:.0f}s"
        fc = f"{pr['face'][0]:.0%}-{pr['face'][1]:.0%}"
        sx = f"{pr['sfx'][0]}-{pr['sfx'][1]}"
        sv = f"{pr['sfx_vol'][0]}-{pr['sfx_vol'][1]}"
        print(f"{name.ljust(w)}  {rt:<9}  {pr['hook_max']:.1f}s   {fc:<7}  "
              f"{sx:<4}  {sv:<11}  "
              f"{'required' if pr['requires_cta'] else 'optional'}")
    print()
    for name, pr in FORMATS.items():
        print(f"{name}: {pr['_derived']}\n")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--formats":
        print_formats()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "--master":
        if len(sys.argv) < 3:
            sys.exit("usage: python3 tools/reel_gates.py --master <file>")
        path = Path(sys.argv[2])
        try:
            integrated, true_peak = check_master(path)
        except GateError as e:
            print(f"GATES FAILED — {path.name}\n{e}")
            sys.exit(1)
        print(f"G31 PASSED — {path.name}: {integrated:.1f} LUFS "
              f"(target {LUFS_TARGET:.0f} ±{LUFS_TOL:.1f}), "
              f"true peak {true_peak:+.1f} dBFS")
        return
    if len(sys.argv) < 2:
        sys.exit("usage: python3 tools/reel_gates.py <slug> [--allow-short]\n"
                 "       python3 tools/reel_gates.py --master <file>\n"
                 "       python3 tools/reel_gates.py --formats")
    slug = sys.argv[1]
    allow_short = "--allow-short" in sys.argv
    beats_path = ROOT / f"src/beats/{slug}.json"
    if not beats_path.exists():
        sys.exit(f"missing beats: {beats_path}")
    beats = json.loads(beats_path.read_text())

    # A DERIVATIVE sheet ("<slug>-nomusic", the sanctioned music-free export)
    # shares the parent's assets — only the music track differs. Resolving the
    # manifest and vo.json against the DERIVATIVE slug found neither, and the
    # run degraded to "GATES PASSED (PARTIAL)" with every Rule 3 check skipped:
    # a clone reporting green on checks it never ran.
    # This is the THIRD enforcer to need the parent fallback; the ledger already
    # records it for validate_job.py and script_approval.py, with the note that
    # when a sheet variant becomes legal every enforcer that reads a path by
    # slug needs to know. Added 2026-08-21.
    asset_slug = slug
    for _suffix in ("-nomusic",):
        if slug.endswith(_suffix):
            _parent = slug[: -len(_suffix)]
            if (ROOT / f"public/assets/{_parent}/vo.json").exists():
                asset_slug = _parent
            break

    man_path = ROOT / f"public/assets/{asset_slug}/manifest.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else None

    vo_end = None
    vo_words: list[tuple[str, float, float]] | None = None
    vo_path = ROOT / f"public/assets/{asset_slug}/vo.json"
    if vo_path.exists():
        raw = json.loads(vo_path.read_text())
        # ACCEPT BOTH vo.json SHAPES, the way compile_shot_plan.load_words does.
        # This read raw["segments"] only, so a vo.json in the flat {"words":[...]}
        # form — which load_words has always accepted, and which a TTS that
        # returns its own word timings produces directly — crashed the one entry
        # point anybody runs, with a bare KeyError. Two tools reading the same
        # file disagreed on its contract (found 2026-08-22).
        if isinstance(raw.get("words"), list):
            ws = raw["words"]
        elif isinstance(raw.get("segments"), list):
            ws = [w for s in raw["segments"] for w in s["words"]]
        else:
            raise SystemExit(
                f"{vo_path} has neither a 'words' nor a 'segments' list")
        vo_end = ws[-1]["end"]
        # THIS LINE WAS MISSING (found 2026-08-17). The CLI read vo.json, pulled
        # the words out, and used them ONLY for vo_end — so `vo_words` was never
        # passed and BOTH Rule 3 gates were dead in the one entry point anybody
        # actually runs: G21 (captions must be words that were spoken, a user
        # rule since 2026-08-12) and G39 (a source must carry the line it
        # illustrates). The gates existed, had self-tests, and passed them,
        # because the self-test passes vo_words and the CLI did not.
        #
        # Same failure as the missing Pillow, the invisible PATH, and the guard
        # that could not see local commits: a check that cannot reach its data.
        # It is the one worth checking twice, because it always looks green.
        vo_words = [(w["word"], float(w["start"]), float(w["end"])) for w in ws]

    try:
        warnings = check_beats(beats, vo_end=vo_end, manifest=manifest,
                               allow_short=allow_short, vo_words=vo_words)
    except GateError as e:
        print(f"GATES FAILED — {slug}\n{e}")
        sys.exit(1)

    # A PASS with no word timings is not the same verdict as a PASS with them,
    # and until 2026-08-19 it printed identically. On a fresh clone —
    # public/assets/ is excluded from git by design — made-by-google-26 reported
    # 10 findings and exit 0 where the same commit with footage reported 36,
    # because every word-level check simply did not run. One of them, G18, is
    # BLOCKING: a clone could pass a reel this repo would refuse.
    #
    # The comment forty lines up already names this exact failure and calls it
    # "the one worth checking twice, because it always looks green" — it was
    # written about vo_words never being PASSED, and the neighbouring case of
    # vo_words being ABSENT was left silent. So: say so. Not a failure — a clone
    # legitimately has no footage, and checking a beat sheet without it is a
    # supported workflow — but never a verdict that looks complete.
    if vo_words is None:
        print(f"GATES PASSED (PARTIAL) — {slug}")
        print(f"  no word timings: {vo_path.relative_to(ROOT)} is absent, so "
              f"every check that compares the PICTURE against the WORDS "
              f"(Rule 3) was skipped, blocking ones included.")
        print("  This verdict covers the beat sheet only. Re-run where the "
              "reel's footage lives before trusting it.")
    else:
        print(f"GATES PASSED — {slug}")
    for w in warnings:
        print(f"  warning: {w}")


if __name__ == "__main__":
    main()
