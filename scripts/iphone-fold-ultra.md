# iphone-fold-ultra — script + beat map

**Format:** news · **Style:** varun-mayya · **Tone:** neutral · **Target:** ~66s (179 words @ 2.7 wps; delivery range 65-76s)
**Presenter:** digital twin `f55b0b7c` (neutral register — G19 ok for a neutral script)

## The angle

The September roundup already listed this device's specs. This reel does not
re-list them. It asks the question the spec list skips: **why is it shaped like
that?** Apple did not build a taller iPhone that folds — it built a squat, wide,
passport-shaped one, and Touch ID, the missing telephoto and the 4:3 screen all
fall out of that single decision. A leaked dummy unit is the only reason anyone
knows how strange it is in the hand, so the dummy carries the reel as footage.

## Narration

(as approved in `jobs/iphone-fold-ultra/script.md`)

## Beat map

Every beat resolves to a manifest asset id or an MG spec. Times are nominal —
the build anchors each cut to the voiceover word timings.

| # | ~s | Line / fragment | Visual |
|---|---|---|---|
| 1 | 2.0 | "Apple's first foldable isn't a taller iPhone." | **split** — top `clip-unfold-hero` (the open reveal) / bottom facecam. Kinetic serif "NOT TALLER". HOOK, ≤2.0s (G03) |
| 2 | 2.4 | "It's a shorter, wider one." | `clip-size-vs-iphone` full-bleed — dummy beside a normal iPhone, the whole argument in one frame. Serif caps "SHORTER. WIDER." |
| 3 | 2.5 | "And that one decision explains everything strange about it." | FACECAM pop (opinion line) |
| 4 | 2.3 | "It's the iPhone Ultra." | MG:`HeadlineBuild` — label "APPLE'S FIRST FOLDABLE" / headline "iPhone Ultra" / subtitle "expected September 2026" |
| 5 | 2.6 | "This is a leaked dummy unit —" | `clip-fold-cover` + persistent corner chip **"DUMMY UNIT · not the real device"** (honesty, per manifest) |
| 6 | 2.5 | "a shape mockup, not the real thing." | `clip-footprint-flat`, credit "Unbox Therapy" |
| 7 | 2.7 | "Unfolded, the inner screen is 7.76 inches, 4:3." | `clip-unfold-hold` w/ serif overlay **7.76" · 4:3** + footnote "reported · MacRumors" (credit on screen, not in the line) |
| 8 | 2.6 | "That's iPad geometry, not phone geometry." | MG:**`comparesplit`** (NEW TREATMENT) — left "EVERY OTHER FOLDABLE / tall + narrow", right "iPhone Ultra / short + wide", banner swaps to "4:3 — iPad geometry" |
| 9 | 2.6 | "Folded, a 5.49-inch cover screen" | `clip-fold-cover` (2nd distinct region) w/ serif **5.49"** |
| 10 | 2.5 | "on a body so stubby" | `clip-unfold-hero` (2nd distinct region) |
| 11 | 2.4 | "people keep calling it a passport." | FACECAM pop |
| 12 | 2.7 | "Apple's reportedly chasing 4.5 millimetres unfolded —" | `clip-profile-thin` w/ serif **4.5mm** + footnote "rumored · MacRumors" |
| 13 | 2.5 | "the thinnest thing it has ever shipped." | `clip-caliper-edge` (texture — readout never claimed as spec) |
| 14 | 2.4 | "Here's what that shape costs you." | FACECAM pop (mechanism turn) |
| 15 | 2.9 | "No depth for Face ID, so Touch ID moves to the power button." | **`receipt`** `receipt-mr-faceid` — cream MacRumors card, highlight sweeps onto "Touch ID" (treatment absent from the last two reels) |
| 16 | 2.6 | "No room for a telephoto either —" | `clip-back-cameras` macro full-bleed, serif "TWO LENSES" |
| 17 | 2.7 | "two 48-megapixel cameras, and that's the whole system." | `clip-bump-macro` w/ serif **48MP × 2** + "no telephoto" |
| 18 | 2.9 | "The crease, though, Apple chased regardless of cost." | **`receipt`** `receipt-mr-crease` — highlight sweep onto the quoted phrase "regardless of cost" |
| 19 | 2.5 | "A liquid metal hinge," | `clip-apple-metal` (Apple material footage, credited; illustrative — labelled, not claimed as the hinge) |
| 20 | 2.6 | "and a fold under 0.15 millimetres deep." | MG:`statcard` — **0.15mm** crease depth, footnote "reported · MacRumors". *No dummy footage here* (banned pairing, per manifest) |
| 21 | 2.4 | "Anyways, nobody agrees on the price." | FACECAM pop (act break) |
| 22 | 3.1 | "Kuo says 2,000 to 2,500 dollars. UBS says 1,800." | MG:**`chart`** — labelled bars: Kuo $2,000–2,500 · UBS $1,800–2,000 · Fubon $2,400 · IDC $2,500 avg → $3,000 max. Source footnote "MacRumors roundup" (G15). Bar labels match the names spoken |
| 23 | 2.6 | "IDC thinks some configs touch 3,000." | `receipt-mr-pricing` — the analyst paragraph as the receipt; the $3,000 lands on the last words (G18) |
| 24 | 2.6 | "And every number there is a leak." | FACECAM (honesty beat) |
| 25 | 2.5 | "Apple has confirmed none of it." | `clip-apple-exploded` (dark Apple internals render) w/ serif "NOTHING CONFIRMED" |
| 26 | 2.2 | "September 9th." | MG:`HeadlineBuild` — "SEPTEMBER 9" / "reported event date" |
| 27 | 2.6 | "Would you carry a passport?" | FACECAM close on the question (CTA — question type, one only) |

**Facecam beats:** 3, 11, 14, 21, 24, 27 → ≈ 15.0s of ~68s = **22%**, in 2.4–2.6s
pops, never one block. That is over the G06 ceiling of 20%, so the build drops
one pop (beat 14 folds into the `receipt` at 15) or trims each by ~0.3s —
resolved against the real word timings, not guessed here.

**Clip reuse:** `clip-unfold-hero`, `clip-fold-cover` and `clip-size-vs-iphone`
each carry two beats — G07 requires a DISTINCT region per beat, so each second
use is cut from a different part of its window, not replayed.

## New / avoided treatments (variety rule)

- **NEW this reel:** `comparesplit` carrying the shape argument (tall+narrow vs
  short+wide); the persistent **DUMMY UNIT** honesty chip; caliper-measurement
  texture footage.
- **Returning but absent from the last two reels:** cream `receipt` with
  highlight sweeps, `chart` with labelled bars, `statcard`.
- **Deliberately avoided** (september-preview used them): `sourceread` ×5,
  `uidialog`, `checklist`, proportional-bar `statcard` spine, numbered serif
  item labels. **Also avoided** (iphone18-split): `annotatezoom`, `timeline`,
  `categorygrid`, `endquestion`.
- **`specsheet` dropped entirely** — it appeared in BOTH previous reels.
- No plain black typecard (G12).

## Honesty guards carried into the build

1. Every dummy beat carries the **DUMMY UNIT** chip + "Unbox Therapy" credit.
2. The mockup seam is **never** paired with a crease line (beat 22 is MG only).
3. Caliper readouts are texture; the only thickness number on screen is the
   sourced **4.5mm**, footnoted.
4. Apple keynote footage (beats 21, 27) is illustrative and credited "Apple" —
   never captioned as the foldable's own hardware.
5. Beats 26–27 are the honesty beat; attribution appears on every figure card.
