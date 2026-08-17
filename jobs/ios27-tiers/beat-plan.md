# ios27-tiers — beat plan (v3, as built)

**The spoken narration lives in `script.md` and NOTHING ELSE does** —
`script_approval.py` hashes that file as the words to be spoken and
`rehearse_vo.py` counts every word in it. v1 put this beat table inside
`script.md` and the rehearsal counted 1572 words instead of 331.

**Format:** news · **Style:** editorial · **Tone:** serious
**Approved:** 254 words, hash `4eefbe517fb09f7c`, 2026-08-17
**Runtime:** 92–108s (`allowLong`, reason in the build script)
**Credits:** ~31–36 of the 39 available. The 331-word v2 needed ~42–45 and was
refused: `AVATAR_IV_VIDEO_GENERATION_OUT_OF_CREDIT`. See the ledger entry.

## What the trim removed (user's choice, 2026-08-17)

- the DMA mechanism sentence (29 words)
- the Mac / Vision Pro platform split (21 words)
- the China line (11 words)

Plus ~17 words of prose tightening that removed no fact. The EU section is now
a single line — "Unless you're in Europe. Siri AI won't ship in the EU at
launch." — carried by two visuals on Apple's own Newsroom page.

## Component correctness — checked against the source, not assumed

`FootageScene` and `FloatingCard` both render a Remotion `<Video>`. A PNG handed
to either renders **black**. Only three scene types take an `<Img>`:
`split` (branches on file extension), `receipt`, and `annotatezoom`. Every still
in this reel therefore goes through one of those three. Found before the first
render, not after.

Two MG specs were also wrong against `src/types.ts` and would have rendered
empty: `wordcascade` takes `words[{text,style,at}]` (not `lines`), and `chart`
takes `items[{label,value,display}]` + `source` (not `rows`/`footnote`).

## Beats as built

| # | Line / fragment | Visual | Type |
|---|---|---|---|
| 1 | "…back to 2019" | `hook-ios27` glass "27" / face | `split` ≤2.0s |
| 2 | "…gets iOS 27" | `compat-noai` — Apple's device list | `receipt` |
| 3 | "…reading about" | avatar + "ALMOST NONE" | facecam |
| 4 | "…with the new iPhones" | `macrumors-lede`, underline "the update arrives in September" | `annotatezoom` |
| 5 | "…zero devices" | DEVICES / DROPPED: / **ZERO** | `wordcascade` |
| 6 | "…same list as iOS 26" | `compat-noai` zoomed to the 11-series, underline the SE row | `annotatezoom` |
| 7 | "…three different phones" | avatar | facecam |
| 8 | *(tier reveal)* | FULL SIRI AI / STANDARD / NO AI | `categorygrid` |
| 9 | "…and iPhone Air" | `note-tier` — Apple's footnote, two underlines (the three phones wrap across two lines, so a single box would also cover the iPad clause) | `annotatezoom` |
| 10 | "…standard Apple Intelligence" | STANDARD TIER rows, source Apple | `specsheet` |
| 11 | "…not the whole assistant" | `glass-lockscreen` — Apple's Siri orb | `receipt` |
| 12 | "…no Apple Intelligence at all" | 15 · 14 · 13 · 12 · 11 · SE → **NO APPLE INTELLIGENCE** | `wordcascade` |
| 13 | "…one model year" | avatar | facecam |
| 14 | "…iPhone 15 is out" | iPhone 15 Pro IN / iPhone 15 OUT | `categorygrid` |
| 15 | "…genuinely rebuilt" | avatar | facecam |
| 16 | "…behind Gemini" | `gemini-diagram` — Apple's APPLE FOUNDATION MODELS radial | `receipt` |
| 17 | "…handles your data" | co-developed / on-device + PCC / Google: none | `specsheet` |
| 18 | "…in the EU at launch" | `apple-dma` receipt, then underline the headline "delayed in EU" | `receipt` + `annotatezoom` |
| 19 | "…story is underneath" | avatar | facecam |
| 20 | "…Liquid Glass slider" | **`settingspane`** Settings › Appearance, spotlight "Liquid Glass" — **NEW TREATMENT** | MG |
| 21 | "…two options" | `note-glass` — Apple's own "ultraclear to fully tinted", underlined | `annotatezoom` |
| 22 | "…30% faster" | 30% / 70% / 80%, footnote Apple | `statcard` |
| 23 | "…iPhone 11 Pro Max" | `note-testing` — **circle on "iPhone 11 Pro Max"** | `annotatezoom` |
| 24 | "…iOS 26 stalled" | avatar | facecam |
| 25 | "…had 127 days" | iOS 26 74% (150d) · iOS 18 76% (127d) · iOS 17 76% (139d) | `chart` |
| 26 | "…removed the variable" | iOS 26 CUT 3 PHONES / **iOS 27 CUTS NONE** | `wordcascade` |
| 27 | "…iPhone land in" | avatar, closing headline y=0.46 (G32) | facecam |

7 facecam beats. Honesty beat is 22–23 and it cuts *toward* the old phones.
Loop: beat 5 opens "zero devices dropped", beat 26 closes it.

## Annotation coordinates — every one verified on pixels

Each was overlaid as a drawbox and looked at. Two were wrong on the first pass:

- `note-testing` circle took **three** passes to land on "iPhone 11 Pro Max"
  (line 2, x 112–428). The first attempt sat on line 3.
- `macrumors-lede` underline originally hit "including the second-generation
  iPhone SE" instead of "the update arrives in September".
- `apple-dma` underline was moved off the macOS/visionOS subhead and onto the
  headline — that subhead's content was cut from the script, so pointing at it
  would raise a claim the VO no longer makes.

## Sound (9 cues, 7 distinct files, 5 roles)

| Beat | Cue | Role |
|---|---|---|
| 1 | sfx/Riser.MP3 @0.2 | suspense → resolves on beat 2 |
| 2 | ground-impact | impact |
| 5 | Pop | popup |
| 9 | Magic Reveal | reveal |
| 14 | whooshes-01 | transition |
| 18 | sfx/Riser.MP3 | suspense |
| 20 | Pop | popup |
| 23 | impact-boom | impact — the biggest claim |
| 25 | Core | impact |

`sfx2/risers-01.mp3` was dropped: 6.19s with a 6.19s lead cannot peak inside a
~1.7s hook, so it would have outrun its beat (G28).

## Treatment check

- **NEW:** `settingspane` — built 2026-08-12, never shipped until now.
- september-preview (previous reel) used sourceread ×5, uidialog ×2, numbered
  01–05 serif labels, proportional-bar statcard. **None reused.**
- `priceladder` (made-by-google-26) not used. No black typecard (G12).
