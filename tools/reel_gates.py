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
LINE_MAX_CHARS = {"label": 30, "headline": 18, "subtitle": 26}

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
    "G05": "R1 display type must fit the phone frame, not wrap and orphan",
    "G20": "R1 a row that never lands is unreadable on a phone",
    "G25": "R1 a cue that never lands is unreadable on a phone",
    "G30": "R1 an orphaned number fragment is unreadable",
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
    # RULE 2 — sources are scouted on mobile view first.
    "G29": "R2 sources are captured on mobile view first",
    # RULE 3 — what is on screen matches what the creator says.
    #
    # G18 is NOT here on purpose. Its principle is Rule 3 — a card must outlast
    # the sentence it illustrates — but the CHECK is a flat 2.0s minimum, which
    # is taste, not the rule: a 1.6s card over a 1.4s claim satisfies Rule 3 and
    # a 2.1s card over a 3s claim breaks it. A fixed number wearing an R3 badge
    # is exactly the thing this restructure exists to delete. Promote it back to
    # blocking once it measures the claim's real length from word timings.
    "G21": "R3 captions must be words that were actually spoken",
    "G39": "R3 every scene must carry the script line it illustrates",
    # RENDER — not opinion. These produce black frames or crash.
    "G11": "RENDER an assetId that is not in the manifest cannot resolve",
    "G13": "RENDER a clip shorter than its beat freezes or blacks out",
    "G28": "RENDER a missing SFX file",
    "G35": "RENDER a still in a video slot renders black",
    # RIGHTS — attribution, and the user's control over their own work.
    "G14": "RIGHTS we credit the sources we use",
    "G15": "RIGHTS a stated number carries where it came from",
    "G27": "RIGHTS the user approved THIS script",
}


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
            "shipping a new genre; do not guess the numbers.")
        prof = FORMATS[DEFAULT_FORMAT]
    RT_MIN, RT_MAX = prof["runtime"]
    HK_MAX = prof["hook_max"]
    FC_MIN, FC_MAX = prof["face"]
    SX_MIN, SX_MAX = prof["sfx"]
    SXV_MIN, SXV_MAX = prof["sfx_vol"]
    total = round(sum(s["durationSec"] for s in scenes), 2)

    # G01 — scenes must sum to the audio, or the tail drifts out of sync
    if vo_end is not None:
        reel_end = vo_end + TAIL_MAX
        if total > reel_end + 0.01:
            errors.append(
                f"G01 tail freeze: scenes total {total:.2f}s but VO ends at "
                f"{vo_end:.2f}s — a reel may not run more than {TAIL_MAX}s past "
                "the last spoken word (frozen face).")
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

    # G05 — display type does not auto-fit; long lines wrap and orphan a word
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
                        f"(max {limit}): {part!r} — HeadlineBuild has no "
                        "auto-fit; this wraps and orphans a word.")

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

    # G09 — music bed present and automated, never flat
    #
    # 2026-08-17: added `noMusic`, the same shape as G02's allowLong, because a
    # VO-only cut is a legitimate DERIVATIVE of a finished reel (accessibility,
    # a client's own bed, a broadcaster who strips audio anyway) rather than a
    # reel that forgot its music. It has to be argued for in one line so it
    # cannot be flipped on to silence a complaint — which is the whole reason
    # the escape hatch is a written reason and not a bare boolean.
    # Re-applied 2026-08-17 after the two-machine merge: sync/main did not have
    # it, and taking sync wholesale would have dropped the VO-only cut.
    no_music = bool(beats.get("noMusic"))
    if no_music and not str(beats.get("noMusicReason") or "").strip():
        errors.append(
            "G09 noMusic is set with no `noMusicReason` — shipping a reel with "
            "no bed has to be argued for in one line, not just switched on.")
    music = beats.get("music")
    if not music and not no_music:
        errors.append("G09 no music bed — every reel carries one (2026-07-22). "
                      "A deliberate VO-only cut sets noMusic + noMusicReason.")
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
    for i, sc in enumerate(scenes):
        if sc["type"] in ("specsheet", "chart", "timeline", "statcard") \
                and sc["durationSec"] < DATA_MIN:
            errors.append(
                f"G18 scene {i:02d} ({sc['type']}) holds only "
                f"{sc['durationSec']:.2f}s — a data card needs >={DATA_MIN}s so it "
                "outlasts the sentence it illustrates. Anchor its region on the "
                "LAST word of the claim, not the first.")

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
        # SPACE (" Apple's"), and strip(punctuation) does not remove it, so every
        # entry in this set carried a space and no caption token could ever match.
        # G21 therefore flagged every alphabetic word in every reel. It went
        # unnoticed because the CLI never passed vo_words (see the note at the
        # bottom of this file) and because the self-test fixture used clean words
        # that did not look like real whisper output.
        spoken = {w.strip().lower().strip(".,!?:;\"'—-") for w, *_ in
                  (x if isinstance(x, (list, tuple)) else (x,) for x in vo_words)}
        spoken.discard("")
        missing = []
        for cap in (beats.get("captions") or []):
            for tok in str(cap.get("text", "")).split():
                k = tok.lower().strip(".,!?:;\"'—-")
                if not k:
                    continue
                # A token carrying a DIGIT is exempt, because the user's own
                # notation rule requires captions to normalise what the voice
                # says: the VO speaks "twenty nine dollars" and the caption must
                # read "$29". The old test exempted only a bare `isdigit()`
                # token, so every normalised form failed — "$29", "10%", "120x",
                # "11th", '7.76"'. That reported 217 "defects" on one reel, all
                # of them the notation rule working correctly, which made the
                # gate worse than useless: it drowned the case it exists for.
                #
                # What it still catches, which is the real target: ALPHABETIC
                # caption words that were never spoken, i.e. captions written
                # against a script that was edited after the voice was made.
                if any(c.isdigit() for c in k):
                    continue
                if k not in spoken:
                    missing.append(tok)
        if missing:
            uniq = sorted(set(missing))[:8]
            errors.append(
                f"G21 {len(set(missing))} caption word(s) are not in the "
                f"narration: {uniq} — the captions were written against a "
                "different script than the voice track that will be rendered. "
                "Re-derive captions from the whisper transcript. (Numerals and "
                "normalised forms like '$29' or '10%' are exempt by design.)")

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
    # <Video>; handed a PNG they produce nothing at all. Only `split` (which
    # branches on file extension), `receipt` and `annotatezoom` take an <Img>.
    # Caught by reading the components, not by any check — six scenes were
    # already wired this way.
    STILL_EXT = (".png", ".jpg", ".jpeg", ".webp", ".avif")
    for i, sc in enumerate(scenes):
        if sc["type"] not in ("footage", "floatcard"):
            continue
        for key in ("src", "mediaSrc"):
            v = str(sc.get(key) or "").lower()
            if v.endswith(STILL_EXT):
                errors.append(
                    f"G35 scene {i:02d} ({sc['type']}) plays a STILL "
                    f"{str(sc.get(key)).split('/')[-1]!r} — {sc['type']} renders a "
                    "<Video> and a still renders BLACK. Use receipt or "
                    "annotatezoom for a PNG, or cut the still to an mp4.")

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
            errors.append(
                f"G38 the hook (scene 00) is `{s0['type']}` — frame 0 needs a "
                "moving element, not a card that assembles. Open on `split` or "
                "`footage` and let the claim land on top.")
        if s0.get("hideCaptions"):
            errors.append(
                "G38 the hook (scene 00) sets hideCaptions — 70-85% of viewers "
                "watch on mute, so a hook with no words on screen says nothing. "
                "Show the claim.")

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
                if not covers:
                    errors.append(
                        f"G39 scene {i:02d} ({sc['type']}) puts a source on "
                        f"screen but never says WHICH line it illustrates. Add "
                        f"`covers` — the phrase this visual proves. Spoken over "
                        f"it: {_norm_words(spoken)[:72]!r}")
                elif _norm_words(covers) not in _norm_words(spoken):
                    errors.append(
                        f"G39 scene {i:02d} ({sc['type']}) claims to cover "
                        f"{covers!r}, but those words are not spoken while it is "
                        f"on screen ({start:.1f}-{end:.1f}s says "
                        f"{_norm_words(spoken)[:64]!r}) — move the scene to the "
                        "line it illustrates, or point it at what is actually "
                        "being said.")

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

    man_path = ROOT / f"public/assets/{slug}/manifest.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else None

    vo_end = None
    vo_words: list[tuple[str, float, float]] | None = None
    vo_path = ROOT / f"public/assets/{slug}/vo.json"
    if vo_path.exists():
        raw = json.loads(vo_path.read_text())
        ws = [w for s in raw["segments"] for w in s["words"]]
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
    print(f"GATES PASSED — {slug}")
    for w in warnings:
        print(f"  warning: {w}")


if __name__ == "__main__":
    main()
