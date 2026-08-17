#!/usr/bin/env python3
"""The SFX catalogue: what each cue IS, and where it is allowed to go.

WHY THIS EXISTS
---------------
2026-08-13: the user supplied two reference videos and asked the system to use
the sound library "whenever and wherever they fit". Those videos are not reels
to imitate statistically — they are TUTORIALS that state the mapping out loud:

    "Use WHOOSH to zoom in or out."
    "Use POP or CLICK for pop-ups."
    "Use RISER to add suspense."
    "Use CAMERA SHUTTER for transitions."
    "Use MAGIC REVEAL to reveal stuff."
    (ref B, same structure) "...to grab attention / to build suspense / to make
    a transition feel smoother / to reveal something unexpected / to make the
    statement more important / to make the statement more comedic."

Every `role` below comes from those lines. Every acoustic number was MEASURED
off the file itself (duration, attack, spectral centroid start->end, low-band
share), not read off the filename — which is how we know `Riser.MP3` really
does peak at the END with a rising centroid, and `Whoosh (Reversed)` is
front-loaded and must therefore START BEFORE the cut it serves.

    python3 tools/sfx_library.py            # print the catalogue
    python3 tools/sfx_library.py --check    # verify every file is present
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SFX_DIR = ROOT / "public"

# roles, straight from the reference videos
TRANSITION = "transition"   # "make a transition feel smoother"
POPUP = "popup"             # "use pop or click for pop-ups"
SUSPENSE = "suspense"       # "use riser to add suspense"
REVEAL = "reveal"           # "to reveal something unexpected"
IMPACT = "impact"           # "to make the statement more important"
SHUTTER = "shutter"         # "use camera shutter for transitions"
COMEDIC = "comedic"         # "to make the statement more comedic"

CATALOGUE: dict[str, dict] = {
    # ── transitions: ride the CUT ───────────────────────────────────────────
    "sfx/whoosh.MP3": dict(
        role=TRANSITION, dur=0.63, low=0.59, lead=0.10,
        note="Centroid falls 1257->535: a downward whoosh. General cut cover."),
    "sfx2/whooshes-01.mp3": dict(
        role=TRANSITION, dur=0.89, low=0.13, lead=0.12,
        note="Centroid RISES 5153->7348 — bright, lifts into the next shot. "
             "Good going into a bigger/brighter scene."),
    "sfx/Whoosh (Reversed).MP3": dict(
        role=TRANSITION, dur=0.42, low=0.64, lead=0.42,
        note="REVERSED: energy builds to the very end, so it must START a full "
             "duration BEFORE the cut or the effect is lost. lead == dur."),
    "sfx/Camera Shutter.MP3": dict(
        role=SHUTTER, dur=0.34, low=0.00, lead=0.05,
        note="Snap. For a hard transition or a screenshot/still landing."),

    # ── pop-ups: an element APPEARS ─────────────────────────────────────────
    "sfx/Pop.MP3": dict(
        role=POPUP, dur=0.18, low=0.01, lead=0.03,
        note="Fastest attack in the library (48 ms). Element entrances."),
    "sfx/Click.MP3": dict(
        role=POPUP, dur=0.29, low=0.01, lead=0.03,
        note="Bright (centroid 8154). UI-flavoured tap."),
    "sfx2/mouse-click-01.mp3": dict(
        role=POPUP, dur=0.37, low=0.01, lead=0.03,
        note="Literal mouse click — use only when a cursor/UI is on screen."),

    # ── suspense: promises a payoff ─────────────────────────────────────────
    "sfx/Riser.MP3": dict(
        role=SUSPENSE, dur=1.49, low=0.26, lead=1.49,
        note="Attack at 1.43s of 1.49s — it PEAKS AT THE END, centroid rising "
             "2142->3658. Must land its peak ON the payoff, so it starts a "
             "full duration earlier."),
    "sfx2/risers-01.mp3": dict(
        role=SUSPENSE, dur=6.19, low=0.24, lead=6.19,
        note="6.2s. Long-form build — only for a hook or a major reveal, never "
             "mid-list. Starts a very long way before its payoff."),

    # ── reveal: the payoff itself ───────────────────────────────────────────
    "sfx/Magic Reveal.MP3": dict(
        role=REVEAL, dur=1.49, low=0.00, lead=0.08,
        note="Bright sparkle, no low end (centroid 4041->5280). Lands ON the "
             "thing being revealed."),

    # ── impact: 'this statement matters' ────────────────────────────────────
    "sfx2/impact-boom.mp3": dict(
        role=IMPACT, dur=2.09, low=0.86, lead=0.06,
        note="86% low-band — the heaviest hit. Reserve for the single biggest "
             "number or claim in the reel."),
    "sfx/Core.MP3": dict(
        role=IMPACT, dur=0.68, low=0.64, lead=0.05,
        note="Short deep hit. The everyday 'this matters' punctuation."),
    "sfx2/ground-impact-352053.mp3": dict(
        role=IMPACT, dur=1.44, low=0.25, lead=0.08,
        note="Impact with a bright rising tail — reads as an arrival."),

    # ── comedic: REGISTER-GATED, see COMEDIC_OK ─────────────────────────────
    "sfx/Vine Boom.MP3": dict(
        role=COMEDIC, dur=1.31, low=0.66, lead=0.05,
        note="Meme boom. Instantly recognisable as a joke."),
    "sfx/Among Us.MP3": dict(
        role=COMEDIC, dur=2.95, low=0.38, lead=0.05,
        note="Meme sting."),
    "sfx/faah.MP3": dict(
        role=COMEDIC, dur=1.12, low=0.03, lead=0.05,
        note="Vocal meme sting."),
}

# WHERE EACH ROLE BELONGS — the scene-level rule.
# A cue whose role does not fit the beat it sits on is noise, however good the
# sound is.
ROLE_FITS = {
    TRANSITION: "a CUT between two scenes — place at the scene's start",
    SHUTTER: "a hard cut, a screenshot landing, or a still snapping into place",
    POPUP: "an element entering: a headline line, a list row, a card appearing",
    SUSPENSE: "the beat BEFORE a reveal — it must resolve into one",
    REVEAL: "the payoff itself: the answer, the number, the product",
    IMPACT: "a data card or the single biggest claim in the reel",
    COMEDIC: "a punchline — never a factual claim",
}

# Comedic stings undercut a news claim. iGeeksBlog reels are reporting, so
# these are blocked wherever the reel is presenting itself as reporting.
COMEDIC_OK_FORMATS = {"top5"}          # tips/roundups may joke
COMEDIC_BLOCKED_TONES = {"serious"}

# Roles that are punctuation, not texture: at most this many per reel.
ROLE_MAX = {IMPACT: 3, SUSPENSE: 2, REVEAL: 2, COMEDIC: 1, SHUTTER: 3}


def role_of(src: str) -> str | None:
    e = CATALOGUE.get(src)
    return e["role"] if e else None


def missing_files() -> list[str]:
    return [s for s in CATALOGUE if not (SFX_DIR / s).exists()]


def main() -> None:
    miss = missing_files()
    if "--check" in sys.argv:
        if miss:
            sys.exit("MISSING SFX FILES:\n  " + "\n  ".join(miss))
        print(f"sfx library ok — {len(CATALOGUE)} cues, all present.")
        return
    by_role: dict[str, list[str]] = {}
    for src, e in CATALOGUE.items():
        by_role.setdefault(e["role"], []).append(src)
    for role, srcs in by_role.items():
        print(f"\n{role.upper()}  — {ROLE_FITS[role]}")
        for s in srcs:
            e = CATALOGUE[s]
            flag = "" if (SFX_DIR / s).exists() else "   [MISSING]"
            print(f"  {s:34} {e['dur']:.2f}s  lead {e['lead']:.2f}s{flag}")
            print(f"      {e['note']}")
    if miss:
        print(f"\n{len(miss)} file(s) missing — run with --check to fail loudly.")


if __name__ == "__main__":
    main()
