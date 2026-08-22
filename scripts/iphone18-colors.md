# iphone18-colors — script + beat map

format: news · style: editorial · avatar: digital twin f55b0b7c (neutral) · 214 words
delivered **70.04s** at 2.97 wps — inside the 60-80s news band.
approval sha256 `c35d4242…` — narration lives in `jobs/iphone18-colors/script.md`.

STRUCTURE: **Discovery** (`jobs/iphone18-colors/structure.md`), written before the
first sentence. Hook+context -> mystery (nobody agrees on the shade) -> investigation
(it has a published Pantone code) -> reveal (Pantone files it Red-Purple: a plum) ->
widen to the lineup -> the Ultra contrast -> implication -> CTA that re-asks the
opening question.

OPEN LOOP: planted beat 03 ("here's the catch"), deferred beat 04 ("but first"),
paid off beat 16 ("that most expensive iPhone").

RULE-3 CONSTRAINTS FROM THE MANIFEST:
- Every swatch is an **approximate sRGB rendering of a published Pantone code**,
  labelled as such on screen. It is never Apple's finish.
- The iPhone Ultra chips are drawn as **outlines**. Its two shades come from photos
  of camera protectors; no code was published, so there is no value to fill them
  with. Filling them would be inventing data.
- The four-up render appears ONLY under "every render you've seen leans red", where
  the render is the SUBJECT of the line — never as evidence of the phone.
- De-emphasis is a lift, never a blend: fading a chip toward cream changes its hue,
  which on this reel misstates the one thing being claimed.

| # | dur | narration | visual | sfx |
|---|---|---|---|---|
| 00 | 3.24s | "Apple's iPhone 18 Pro has a new signature color." | `split` — chip-cherry | — |
| 01 | 3.42s | "It's called Dark Cherry — and nobody agrees what it looks like." | `footage` — chip-cherry | Camera Shutter.MP3 |
| 02 | 3.40s | "Which is odd, because we know its exact Pantone code." | `footage` — avatar (facecam) | — |
| 03 | 4.86s | "And here's the catch: Apple's most expensive iPhone ever doesn't get it." | `wordcascade` — chip-cherry | — |
| 04 | 2.34s | "But first — what color is this actually?" | `typecard` — chip-cherry | — |
| 05 | 2.16s | "Every render you've seen leans red." | `receipt` — renders-four | Camera Shutter.MP3 |
| 06 | 3.10s | "But the leaker who detailed it says those are wrong." | `receipt` — 9to5-head | — |
| 07 | 1.22s | "It's purple-tinged." | `wordcascade` — chip-cherry | Core.MP3 |
| 08 | 4.84s | "And the reports pin it to one number: Pantone 6076." | `sourceread` — mr-bullets | Riser.MP3 |
| 09 | 1.92s | "Pantone files that under Red-Purple." | `annotatezoom` — pantone-6076 | Magic Reveal.MP3 |
| 10 | 2.26s | "In plain terms: a dark plum." | `footage` — chip-cherry-tight | — |
| 11 | 2.42s | "So if you're picturing a rich red iPhone" | `footage` — avatar (facecam) | — |
| 12 | 3.20s | "the real one is quieter and browner than you expect." | `receipt` — simtray | Core.MP3 |
| 13 | 2.56s | "It's still the only risk in the lineup: Silver" | `footage` — chip-lineup | — |
| 14 | 1.44s | "Dark Gray, and a Light Blue." | `footage` — chip-lineup-b | — |
| 15 | 3.22s | "And reports don't even agree Dark Gray survives." | `receipt` — mr-caution | — |
| 16 | 2.70s | "Now — that most expensive iPhone." | `footage` — avatar (facecam) | — |
| 17 | 2.82s | "The foldable iPhone Ultra reportedly gets two." | `receipt` — mr-ultra-head | Camera Shutter.MP3 |
| 18 | 1.34s | "Silver, and a dark blue." | `footage` — chip-ultra | — |
| 19 | 2.76s | "Both from leaked camera protectors, not the phone." | `footage` — avatar (facecam) | — |
| 20 | 1.44s | "A bold color is a bet." | `footage` — avatar (facecam) | — |
| 21 | 4.16s | "Sell millions and a miss gets absorbed — but at a reported two thousand dollars and up" | `footage` — chip-gap | — |
| 22 | 1.22s | "it's just unsold stock." | `footage` — chip-gap | whoosh.MP3 |
| 23 | 2.00s | "So the risk goes where the volume is." | `footage` — avatar (facecam) | — |
| 24 | 3.44s | "None of it's confirmed — and lighting changes how any color reads." | `wordcascade` — chip-cherry | Core.MP3 |
| 25 | 1.66s | "So — plum, not red." | `footage` — chip-cherry | — |
| 26 | 0.90s | "Still the one you'd pick?" | `footage` — chip-cherry-tight | — |

## Sound

9 cues, placed by ROLE against `ROLE_FIT_TYPES` (G40): 3 shutter, 3 impact,
1 suspense, 1 reveal, 1 transition. The Riser on beat 08 starts 1.49s before the
cut so it PEAKS on the Red-Purple reveal in beat 09, which resolves it.

Music bed ducked from the voice by `tools/duck_music.py` — 38 derived points,
0.066 under speech, 0.106 in pauses. Never hand-written (G37).

## Sources

Pantone (official) · MacRumors · 9to5Mac · Sonny Dickson via MacRumors.
Full provenance and the honesty exclusions: `public/assets/iphone18-colors/manifest.json`.
