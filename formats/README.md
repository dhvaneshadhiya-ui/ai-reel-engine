# Formats

**A format is not a style.** Two different axes:

- **`styles/`** — the LOOK: type, palette, caption treatment, audio mix.
  (`editorial`, `utility`)
- **`formats/`** — the GENRE: what the reel is *doing*, and therefore its
  physics — runtime band, hook ceiling, facecam share, SFX band, whether a
  CTA is mandatory, and any structural rules.

A reel picks ONE of each. `editorial` × `comparison` is a valid pairing, so
is `utility` × `top5`.

## The numbers live in code, not here

    python3 tools/reel_gates.py --formats

That prints the live table straight from `FORMATS` in `tools/reel_gates.py`,
plus where each number came from. **These docs deliberately do not restate the
numbers.** On 2026-08-12 four separate stale-prose drifts were found in one
session — the skill said `avatar_v`, RULES said 60-120s, the style pack said
speed 1.2, and doctor was checking a length range the gates had already
changed. Every one was a doc quoting a number that had moved. Print, never
copy.

## Declaring a format

```json
{ "id": "my-reel", "format": "top5", "style": "utility", ... }
```

Omitting `format` means `news`, so every older sheet keeps working.
Gate **G23** rejects a format with no profile.

## Adding a new format

1. **Tear down 8-12 reference reels** of the genre — contact sheets, whisper
   transcripts, loudness, cut rhythm. This is how `editorial` (11 reels) and
   `utility` (12 reels) were built, and it is why their numbers hold.
2. Add the profile to `FORMATS` with a `_derived` string naming the source.
3. Add a self-test to `tools/test_gates.py`: one POSITIVE case that builds
   clean, plus a negative for each rule the format adds.
4. Write `formats/<name>.md` — structure and script skeleton, no numbers.

**If you cannot measure it, inherit and SAY SO** — see `comparison.md`. Never
invent a plausible-looking band; a guessed number blocks good work and passes
bad work, and nobody can tell which.


## Runtime is chosen from the topic

A format's `runtime` band is the **default**, measured from real reels — what a
reel should be unless the story argues otherwise. It is not a cap.

- Inside the band: nothing to do.
- Past it: set `allowLong: true` **and** `allowLongReason: "<one line>"`. G02
  rejects the flag without the reason, because it is an argument, not a switch.
- **180s is the wall.** `allowLong` cannot pass `RUNTIME_CEILING` in
  `tools/reel_gates.py` (user rule 2026-08-16). Past that, split the topic
  across two reels.

The ceiling is USER-SET, not derived from a teardown — unlike the bands. It is
the **platform** limit: Instagram Reels and YouTube Shorts both allow 3 minutes.
That means the ceiling no longer supplies any editorial brake, and
`allowLongReason` is the only one left between the band and the wall. Write it
like it matters.

**Known scaling gap.** G08 wants 6-9 SFX cues regardless of runtime. Measured
across the seven shipped reels that is 1 cue per 12.1s on average; at 180s the
same rule permits 1 per 20-30s. The count was derived on 60-80s reels, so past
the band it means something it was never measured to mean. Re-derive it as a
per-minute density before shipping anything near the wall.
