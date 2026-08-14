# Sound design — what goes where

Derived 2026-08-13 from two reference videos the user supplied. They are not
reels to imitate — they are **tutorials that state the mapping out loud**:

> "Use WHOOSH to zoom in or out. Use POP or CLICK for pop-ups. Use RISER to
> add suspense. Use CAMERA SHUTTER for transitions. Use MAGIC REVEAL to
> reveal stuff."
> — and the second: "…to grab attention / to build suspense / to make a
> transition feel smoother / to reveal something unexpected / to make the
> statement more important / to make the statement more comedic."

Every acoustic number in `tools/sfx_library.py` was MEASURED off the file
(duration, attack, spectral centroid start→end, low-band share), not inferred
from the filename.

    python3 tools/sfx_library.py           # the catalogue, grouped by role
    python3 tools/sfx_library.py --check   # fail if any file is missing

## The six roles

| Role | Says | Goes on |
|---|---|---|
| `transition` | "this is a cut" | the first frame of a new scene |
| `shutter` | "snap" | a hard cut, a screenshot or still landing |
| `popup` | "something appeared" | a headline line, list row, card entering |
| `suspense` | "something is coming" | the beat **before** a reveal |
| `reveal` | "here it is" | the payoff itself |
| `impact` | "this matters" | a data card, or the biggest claim in the reel |
| `comedic` | "this is a joke" | a punchline — **never** a factual claim |

## The rules that BLOCK (gate G28)

1. **The file must be in the catalogue and on disk.** Before today nothing
   checked this: a typo'd filename rendered SILENT while still counting toward
   G08's 6–9 budget, so a reel could pass the sound gate with no sound.
2. **The role must fit the beat.** A `reveal` sparkle on plain footage, or an
   `impact` boom on a checklist, is noise however good the sound is.
3. **A cue may not outrun its beat.** `impact-boom` is 2.09s; on a 0.96s scene
   it bleeds into the next shot.
4. **A riser must resolve.** A `suspense` cue with no `reveal` or `impact`
   within its own beat or the next three is a broken promise.
5. **Caps per reel** — `impact` 3, `shutter` 3, `suspense` 2, `reveal` 2,
   `comedic` 1. Punctuation stops being punctuation when it repeats.
6. **Comedic stings are register-gated.** Allowed only in `top5`, never in a
   `serious`-tone reel. A meme boom under a factual claim reads as a joke
   about the claim — and these are iGeeksBlog news reels.

## Lead time — the part that is easy to get wrong

A cue is placed so its PEAK lands on the moment, which means most cues start
slightly BEFORE it. `lead` in the catalogue is that offset.

- `Whoosh (Reversed)` has **lead == duration (0.42s)**: its energy builds to
  the very end, so it must start a full length before the cut or the effect is
  simply lost.
- `Riser.MP3` peaks at 1.43s of 1.49s — it starts a **full 1.49s** before the
  payoff.
- `risers-01.mp3` is **6.19s**: hooks and major reveals only, never mid-list.
- Pops and clicks are near-instant (48–150 ms attack) and sit on the frame.

## Why the shipped reels look wrong under this gate

grok-bot, apple-pay-india and seedance-25 each carry **5–6 `impact` cues**,
some on plain footage, one 2.09s cue on a 0.96s scene. That is not
carelessness: the old library (`public/sfx2/`) held only five files — two
impacts, a whoosh, a riser, a click. **There was no pop, no shutter, no
reveal**, so `impact-boom` became the general-purpose cut sound. The expanded
`public/sfx/` library is what makes correct placement possible.

Fix them only if those reels are ever re-cut; the rule applies from the next
reel forward.
