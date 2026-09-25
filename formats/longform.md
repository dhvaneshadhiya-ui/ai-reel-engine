# Format: longform (landscape YouTube explainer)

**Status: MEASURED on five in-format references, and WIRED into `FORMATS`
(2026-09-25).** Print the live numbers with `python3 tools/reel_gates.py --formats`;
this file is the working, not the source of truth.
Teardown run 2026-09-25, first on four candidates picked from metadata (three of
which turned out to be the wrong form) and then on five that were frame-verified
first. Measured (`tools/measure_video.py`, scene detection at 0.15, YouTube caption
tracks, publisher chapter lists, contact sheets read by eye at 1 frame / 10s, presenter share via Apple Vision).
Every number below came from a file on this machine, not from an impression.

## How to run it again

```bash
python3 tools/measure_video.py <file.mp4> [more.mp4 ...] [--threshold 0.15]
```

Downloads first (`yt-dlp -f "bv*[height<=480]..." --write-auto-subs --write-info-json`),
into `_sources/_teardown-longform/`. The tool prints cut rhythm, speech rate and
chapter lengths per video plus a pooled median. `--faces` measures presenter share
with Apple's Vision framework (a face at least 10% of frame height, one frame every
10s), so that number is measured too; layout still has to be read off a contact sheet
(`fps=1/10,tile=10x8`).

## What was measured — IN-FORMAT references (voice-led, screen-carried)

Face share is measured with Apple Vision; every one of these sits at or under 19%.

| reference | runtime | hard cuts | s/cut p50 | p75 | longest hold | w/s | chapters | chapter p50 | face |
|---|---|---|---|---|---|---|---|---|---|
| ThioJoe, hidden iOS 27 features | 503s | 22 | 7.5s | 30.7s | 88s | 3.64 | 25 | 18s | 12% |
| MacMost, 10 password app tips | 696s | 36 | 16.1s | 23.7s | 80s | 3.09 | 12 | 46s | 19% |
| MacMost, 10 Split View tips | 658s | 74 | 4.2s | 14.9s | 43s | 3.02 | 13 | 43s | 6% |
| Kevin Stratvert, Google Flow | 554s | 72 | 2.5s | 10.4s | 77s | 3.44 | 8 | 48s | 13% |
| ScreenCastsONLINE, DockDoor | 550s | 16 | 13.4s | 54.0s | 231s | 3.22 | 0 | — | 0% |

**Spread:** runtime 503-696s (median 554) · shot p50 2.5-16.1s (median 7.5) ·
p75 10.4-54.0s (median 23.7) · 3.02-3.64 w/s (median 3.22) · face 0-19% (median 12).

Two of the five are the same channel in the same series, which is the point: MacMost
repeats this form, and the numbers hold across both (face 19% and 6%, w/s 3.09 and
3.02). The channel also runs a SECOND format — its "N new features in macOS" videos
cut to a full-frame talking head between items — so the form is a property of the
series, not the channel.

## The earlier candidates — kept as the contrast

These were picked from metadata and mostly are NOT this format. They stay here because
they are what the bands are being held against.

### Out-of-format, measured anyway

| reference | runtime | hard cuts | s/cut p50 | p75 | longest hold | w/s | chapters | chapter p50 | face share (measured) |
|---|---|---|---|---|---|---|---|---|---|
| Brandon Butch, iOS 27 first 12 things | 723s | 34 | 15.3s | 30.3s | 81.6s | 3.89 | 20 | 26s | 6% |
| ThioJoe, Hidden new features in iOS 27 | 503s | 22 | 7.5s | 30.7s | 88.2s | 3.64 | 25 | 18s | **12%** |
| Hayls World, iOS 27 everything new | 501s | 93 | 4.2s | 7.2s | 20.6s | 3.00 | 0 | — | 68% |
| Apple Explained, Apple's trade-in program | 529s | 180 | 2.6s | 3.6s | 14.3s | 3.45 | 0 | — | 62% |

Pooled median: runtime 516s, shot p50 5.9s, shot p75 18.8s, 3.55 w/s.

## Three findings that change the plan

1. **Only ONE of the four is the format we are building.** The shortlist was picked
   from metadata, and three of four style calls were wrong when the frames were
   actually read: Butch is an overhead shot of hands holding a real iPhone for twelve
   minutes (no face, and not reproducible here — we have no device rig); Hayls World
   and Apple Explained are both presenter-led at roughly 60% face. **ThioJoe is the
   only measured reference that matches voice-led, screen-carried, face at the
   bookends** — title card at 0s, iPhone screen recordings on a branded background,
   presenter appearing for a few seconds at a time, presenter close.
2. **In long form the unit of change is not the cut.** Screen-carried references show
   FEWER hard cuts (22 in 503s) than the b-roll documentary (180 in 529s), because the
   motion happens inside the screen recording. Our short-form pacing gate (G04, 1.7s
   static max) measures the wrong thing here: the rule must be "something on screen
   changes every N seconds", not "cut every N seconds".
3. **Long form is spoken FASTER than our reels.** Every reference sits at 3.00-3.89
   w/s where our measured reel band is 2.35-2.75. A long-form read at reel pace would
   run noticeably slow.

## The profile, derived

- **Runtime 500-700s** (8:20-11:40), default target **555s (~9:15)** — the measured
  median. Every in-format reference sits inside this.
- **Speech 2.9-3.2 w/s.** References run 3.02-3.64 (median 3.22); our reels run
  2.35-2.75. The band sits at the bottom of the references on purpose: our voice is a
  clone with measured-flat delivery, and pace cannot stand in for expression.
- **Chapter every 20-50s**, 8-25 of them, published as timestamps. ThioJoe is the dense
  end (25 chapters, 18s each), Stratvert the loose end (8 chapters, 48s).
- **Face 8-15%**, and never more than 19%. Open, close, and a short cutaway roughly
  every 90s. One reference (a pure screencast) carries 0% and still over-performs its
  channel by 37x, so the face is optional in this format — the voice is not.
- **Something changes on screen every 4-8s** (p50 of the three busiest references:
  2.5, 4.2, 7.5). This is NOT a cut rule: the two calmest references hold a single
  screen for 13-16s at a time while the cursor works inside it. Hard cuts range 16 to
  74 per video for the same runtime.
- **Longest single hold <= 60s**, except a deliberate demo. The pure screencast holds
  one screen for 231s, which is the format's outer edge and not a target.
- **Narration is continuous.** At 10s resolution every reference speaks in every
  bucket — none leaves a ten-second hole. (Caveat: that resolution cannot see the
  sentence-level pauses our own reels rely on.)

## What the gap taught (closed 2026-09-25)

The first four references were chosen from titles, descriptions and chapter lists.
Reading the frames overturned three of the four style calls. The second sweep verified
the form on sampled frames BEFORE the shortlist was handed over, and all five survived
measurement. Six further candidates were rejected on frames first, among them a 9to5Mac
video whose presenter is on screen for its whole runtime and a MacRumors video shot as
overhead hands holding a phone.

**Rule for the next format: verify the form on frames before the reference list is
written down, not after.**

## Wired into the gates, 2026-09-25

- **G02** reads a per-format `ceiling` (longform 900s) instead of the global 180s
  wall. A negative test asserts a 560s cut passes, because every positive test
  would still have passed with the format unusable.
- **G03** takes the 10s cold open from the profile's `hook_max`.
- **G04** switches to "something changed": `change_max` 8.0s and `hold_max` 60.0s,
  instead of the cut-derived short-form ceilings.
- **G06** takes the 0-19% face band.
- **G08** asserts NOTHING and says so — the 6-9 count is a 60-80s rule and was not
  re-measured for nine minutes. A rescaled number would read as evidence.
- **G70** takes a `proof_window` of 4-20s instead of 2-5s.

A 560s longform sheet now passes with three advisories, all correct: no measured
SFX band, no presenter declared, and (before the window moved) the short-form
proof rule. Nothing blocks.

## What this format still needs from the engine

- A per-format runtime ceiling (G02 is a flat 180s today).
- A 16:9 layout pass on the handful of scene types this format actually uses.
- A "something changed" pacing measure to replace the cut-based one.
- An SRT sidecar instead of burned word-reveal captions.
- Chapters in the packaging file, and a 16:9 cover.

## Sources

Measured from local copies in `_sources/_teardown-longform/` (not committed).
Metadata (views, dates, durations) from each video's own YouTube page, 2026-09-25.
