# Formats

**A format is not a style.** Two different axes:

- **`styles/`** — the LOOK: type, palette, caption treatment, audio mix.
  (`varun-mayya`, `nick-saraev`)
- **`formats/`** — the GENRE: what the reel is *doing*, and therefore its
  physics — runtime band, hook ceiling, facecam share, SFX band, whether a
  CTA is mandatory, and any structural rules.

A reel picks ONE of each. `varun-mayya` × `comparison` is a valid pairing, so
is `nick-saraev` × `top5`.

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
{ "id": "my-reel", "format": "top5", "style": "nick-saraev", ... }
```

Omitting `format` means `news`, so every older sheet keeps working.
Gate **G23** rejects a format with no profile.

## Adding a new format

1. **Tear down 8-12 reference reels** of the genre — contact sheets, whisper
   transcripts, loudness, cut rhythm. This is how `varun-mayya` (11 reels) and
   `nick-saraev` (12 reels) were built, and it is why their numbers hold.
2. Add the profile to `FORMATS` with a `_derived` string naming the source.
3. Add a self-test to `tools/test_gates.py`: one POSITIVE case that builds
   clean, plus a negative for each rule the format adds.
4. Write `formats/<name>.md` — structure and script skeleton, no numbers.

**If you cannot measure it, inherit and SAY SO** — see `comparison.md`. Never
invent a plausible-looking band; a guessed number blocks good work and passes
bad work, and nobody can tell which.
