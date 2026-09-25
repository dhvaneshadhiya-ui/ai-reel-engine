# Format: longform (landscape YouTube explainer)

**Status: NUMBERS PARTLY MEASURED, NOT YET A PROFILE.** Teardown run 2026-09-25 on
four references (`tools/measure_video.py`, scene detection at 0.15, YouTube caption
tracks, publisher chapter lists, contact sheets read by eye at 1 frame / 10s).
Do not copy these into `FORMATS` until the gap named at the bottom is closed.

## How to run it again

```bash
python3 tools/measure_video.py <file.mp4> [more.mp4 ...] [--threshold 0.15]
```

Downloads first (`yt-dlp -f "bv*[height<=480]..." --write-auto-subs --write-info-json`),
into `_sources/_teardown-longform/`. The tool prints cut rhythm, speech rate and
chapter lengths per video plus a pooled median; face share and layout come from a
contact sheet read by eye, because no tool here measures those.

## What was measured

| reference | runtime | hard cuts | s/cut p50 | p75 | longest hold | w/s | chapters | chapter p50 | face share (read) |
|---|---|---|---|---|---|---|---|---|---|
| Brandon Butch, iOS 27 first 12 things | 723s | 34 | 15.3s | 30.3s | 81.6s | 3.89 | 20 | 26s | ~0% |
| ThioJoe, Hidden new features in iOS 27 | 503s | 22 | 7.5s | 30.7s | 88.2s | 3.64 | 25 | 18s | **~12%** |
| Hayls World, iOS 27 everything new | 501s | 93 | 4.2s | 7.2s | 20.6s | 3.00 | 0 | — | ~60% |
| Apple Explained, Apple's trade-in program | 529s | 180 | 2.6s | 3.6s | 14.3s | 3.45 | 0 | — | ~60% |

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

## Draft bands (hold until the gap closes)

- **Runtime** 480-660s (8-11 min); the four references cluster 501-723s.
- **Speech** 2.9-3.2 w/s. Below the references deliberately: our voice is a clone with
  measured-flat delivery, and speed cannot substitute for expression.
- **Beat / chapter** 18-30s, 12-25 chapters, published as timestamps.
- **Face share** 8-15%: open, close, and a short cutaway roughly every 90s (ThioJoe).
- **On-screen change** every 4-8s (references' shot p50 4.2-7.5s), longest single
  hold <= 30s (p75 ~30s on both screen-carried references).
- **Cold open** states the question in the first two sentences; the strongest item
  lands by ~0:10 (Butch's chapter list puts it there, and it is his best video of the
  year by 9.6x his median).

## The gap

One in-format reference is not a teardown. Two or three more screen-carried,
low-face, landscape explainers must be measured the same way before these bands go
into `FORMATS` — that is the G23 discipline, and today's session is the reason it
exists: the metadata-based style calls were wrong three times out of four.

## What this format needs from the engine

- A per-format runtime ceiling (G02 is a flat 180s today).
- A 16:9 layout pass on the handful of scene types this format actually uses.
- A "something changed" pacing measure to replace the cut-based one.
- An SRT sidecar instead of burned word-reveal captions.
- Chapters in the packaging file, and a 16:9 cover.

## Sources

Measured from local copies in `_sources/_teardown-longform/` (not committed).
Metadata (views, dates, durations) from each video's own YouTube page, 2026-09-25.
