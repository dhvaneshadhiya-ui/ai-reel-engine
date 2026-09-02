# AGENT.md — operating manual for the AI Reel Engine

You are the director of an automated reel factory. **Input:** a topic or short
script from the user. **Output:** a finished vertical reel (1080×1920, 30fps,
mastered to −14 LUFS) with an AI presenter, sourced footage, motion graphics,
captions, SFX and music — rendered entirely as code, with zero manual editing.

**Read `RULES.md` first** — the short, current, binding rule set, which marks
each rule as gate-enforced, lint-enforced, or eyes-only. Then this file (the
PROCESS), `PIPELINE.md` (technical spec), and the style pack in `styles/`.
`STYLE-RULES.md` is the dated ledger behind RULES.md — go there for why a rule
exists, and to append new feedback.

Before starting: `python3 scripts/doctor.py`. It fails loudly on a missing
dependency instead of letting a safety check silently skip — which is exactly
how the frame linter's pixel checks sat disabled for weeks.

---

## 1. The mental model (read this twice)

A reel is a **beat sheet**: one JSON file listing timed *scenes*. A library of
~34 React components renders those scenes. A build script generates the beat
sheet by anchoring every scene cut to the **voiceover's word timings**.

**The voiceover is the master clock.** Visuals are cut to spoken words, never
the reverse. Scenes must sum *exactly* to the audio duration.

```
topic ──▶ SCOUT assets ──▶ manifest.json
      ──▶ DIRECT script + shot plan (every beat bound to a real asset)
      ──▶ VOICE + FACE (HeyGen) ──▶ whisper word timings
      ──▶ build beat sheet ──▶ register ──▶ render ──▶ master ──▶ CRITIC pass
```

### The one rule that matters most

> **Never script a claim you cannot show.**

Source the footage **first**, then write to it. The expensive failure mode is
writing a beautiful script about three demos you have no footage of, then
papering over the gap with text cards. If an asset doesn't exist, either
re-scout for it specifically, or **rewrite the line** to something you can show.

---

## 2. Order of operations (do not reorder)

### STEP -1 — WHERE THE TOPIC COMES FROM (added 2026-08-27)

Every other stage of this pipeline had a tool, a gate and a self-test. Topic
selection had a habit: reels got picked off whatever news was in front of
someone, and nothing ever read what the audience was actually asking.

A scheduled task (`daily-reel-ideas`) runs each morning and writes
`jobs/_ideas/<YYYY-MM-DD>.md` — a shortlist that has already passed:

```bash
python3 tools/idea_scout.py --brief          # what the researcher must know
python3 tools/idea_scout.py --check <file>   # whether what came back is usable
```

`--brief` hands over every subject already made (so a repeat cannot be
suggested), the formats with their measured bands, and the output contract.
`--check` refuses a shortlist unless every idea carries a real STORY ENGINE
(believed X -> discovers Y -> matters because Z), **two independent source
domains**, a known format, and no overlap with an existing reel.

**AUDIENCE lines are language, never evidence.** The watering-hole sources
(App Store 1-3 star reviews, YouTube and Instagram comments, topic subreddits)
tell you what people are confused about and in whose words. `--check` counts
them separately from `SRC:` and REFUSES an idea supported only by them. A
forum quote shapes the angle and the hook; it never becomes a claim.

**LANE B RUNS HERE, NOT IN THE CLOUD (measured 2026-08-31).** The routine's
sandbox blocks essentially all outbound web traffic — `curl` and `WebFetch`
both 403 at the egress proxy, including hn.algolia.com, reddit.com,
itunes.apple.com RSS and every news domain tested. Only `WebSearch` works
there, because it runs server-side. So the morning shortlist is Lane A
(what moved) plus whatever demand signal search snippets reveal.

The audience pass happens on THIS machine, on the ONE topic you picked —
which is better targeting anyway than shallow mining across five candidates.
Confirmed reachable from here:

| source | status | what it gives |
|---|---|---|
| `hn.algolia.com/api/v1/search?query=<q>&tags=comment` | **works** | verbatim comments with author + date |
| WebSearch on "<topic> reddit / complaints / why does" | works | the question people keep asking |
| reddit.com (any path) | **blocked here too** | — |
| itunes.apple.com RSS | returns feed metadata, no reviews | — |

Findings go into `research.md` as AUDIENCE lines: verbatim quote, platform,
url, date. **They are LANGUAGE, not evidence** — they shape the angle, the
hook and the vocabulary, and they never become a TIER, a SRC or a spoken
claim.

Pick one, then `scripts/new_job.py <slug>` and continue at STEP 0. The SRC
lines are a head start, not the research — `research.md` still has to be
filled properly.

### STEP 0 — Load context
0. Read `frameworks/short-form-master.md` and answer its §2 brief fields in
   `jobs/<slug>/brief.json`: **subject**, **reveal_target** (the precise
   identity withheld for a DM, or `none`), **source_policy** (facts and
   footage are separate categories). `new_job.py` scaffolds all three, and
   `script_approval.py propose` refuses on a leak, a claim spoken harder
   than its evidence, or a source-policy violation.
   Then state the STORY ENGINE in one sentence before writing anything:
   *a viewer who believes/experiences X discovers Y, which matters because
   Z.* If you cannot fill it, there is no reel yet — only material.
1. Read `STYLE-RULES.md`. Its rules override this file.
2. Pick the style pack in `styles/`. It defines the LOOK and the script voice.
   This file defines the PROCESS.
3. Check the pack's *treatment history* — never repeat the previous reel's
   visual treatment for the same kind of information.

### STEP 0.5 — RESEARCH (the ledger, before a source is captured)

**This step had no number until 2026-08-27.** It was one parenthetical inside
STEP 1a — "verify the story (web search)" — even though the ledger it produces
is a BLOCKING precondition of `propose`. A stage that gates the pipeline and
is named nowhere in the order of operations is the definition of a step that
gets skipped. The user asked where research happens; the honest answer was
that the manual did not say.

It runs FIRST, before scouting, for a practical reason: you cannot capture a
source until you know which claim it proves and where that claim was
published. Fill `jobs/<slug>/research.md` (scaffolded by `new_job.py`) AS you
research, never afterwards from memory:

- every load-bearing claim gets a **CLAIM**, a **TIER**
  (official/multi/single/disputed), a **SRC** url you actually fetched, the
  **SPOKEN** words of the script that carry it, and a **VIA** naming the
  ultimate source;
- a dated **## SEARCHED** log of the queries you actually ran.

`tools/research_check.py` refuses a ledger that is missing, still a template,
carries no claims, has no search log, or names SPOKEN words the script never
says. `propose` runs it and stops on any of those.

**References the user hands you are INPUTS, not sourcing.** They tell you the
angle; they do not discharge this step. The dated search log exists precisely
so a reel cannot be built out of whatever arrived in the prompt, and a topic
with no references given changes nothing about what the ledger must contain.
Two independent source DOMAINS minimum, or write `ONE-SOURCE-OK: <why>` — and
independence is judged on VIAs, so two outlets quoting one leaker is one
source. `fact-check-workflow` is cued here, while a claim is still a claim and
the fix is verification rather than a rewrite.

### STEP 1a — ASSET SCOUT (before writing a single script line)
The story is already verified in STEP 0.5 and its claims are in the ledger;
this step hunts the VISUALS that prove them. Write
`public/assets/<slug>/manifest.json`:

```jsonc
{
  "topic": "...",
  // verified_facts is SUPERSEDED for claims: the authoritative record is
  // jobs/<slug>/research.md (CLAIM/TIER/SPOKEN/SRC), which propose enforces.
  // The manifest stays the truth about ASSETS.
  "assets": [
    { "id": "clip-demo",
      "kind": "footage|receipt|brand|still",
      "source": "yt:VIDEO_ID @t120-128 | url",
      // asset tier = PROVENANCE (official|reliable|fallback) — G42 counts it,
      // capture_plan refuses a line without it. Distinct axis from the
      // research ledger's claim tier (official|multi|single|disputed),
      // which is CORROBORATION.
      "tier": "official|reliable|fallback",
      "shows": "what is LITERALLY on screen — written only after you looked at extracted frames",
      "quality": "clean|has-chrome|busy",
      "credit": "@handle | channel",
      "crop": "608:1080:X:0 notes" }
  ],
  "mg_always_available": "SpecSheet, XPost, HeadlineBuild, receipt, CategoryGrid, Carousel, Checklist, HCompare, wordcascade, statcard, ..."
}
```

Scout order: official channels/keynotes → creator demo compilations (credit
them) → screenshot receipts (headless Chrome) → brand marks.

**Your own device is a source.** `python3 tools/ingest_screencap.py` turns an
iPhone screen recording into a reel-ready clip and scrubs the personal data
out of it (the privacy pass is the point of the tool). Use it when the story
needs real OS behaviour — a real Face ID prompt, a real carrier, a real
setting being toggled — which the Simulator cannot license and a stock clip
cannot prove. It was written, tested, and then mentioned in no document for
weeks; found by `wiring_audit.py` on 2026-08-26.

**Verify every candidate by extracting frames and looking at them.** Write the
`shows` field from what you actually see, never from what you assume.
`python3 tools/scout_sheet.py <slug>` makes the look one file per clip — a
timestamped contact sheet of every candidate under `_sources/` and
`public/assets/` for the job. The looking and the writing stay yours. A thin
manifest is a valid outcome — it just means a more graphics-led reel.

Two vocabularies, and the distinction is the whole game:
- **Footage is scarce** and must be verified. Use it for proof and spectacle.
- **Graphics are infinite** and always available. Use them for numbers,
  comparisons, and mechanisms.

### STEP 1b — SCRIPT DIRECTOR
Load the style pack's script rules + the manifest. Write `scripts/<slug>.md`
containing the script **and** a beat map where every beat carries:

```
visual: <manifest asset id>   OR   visual: MG:<component + concrete spec>
```

A beat whose visual is neither is **illegal**. Fix it on paper: re-scout with a
specific request (max 1–2 loops), or rewrite the line.

**Validation gate:** before generating anything, re-read the beat map and
confirm every visual id resolves. Fixing this on paper costs seconds; fixing it
after voice + avatar generation costs credits and an hour.

### STEP 1c — THE CRAFT LOOP (write -> measure -> rewrite)

```bash
python3 tools/script_doctor.py <slug>        # or --file draft.md --slug <s>
```

ONE call: prose shape, house tics, the framework's reveal/certainty/source
rules, and the runtime prediction. A good script takes several passes — that
is the job, not a defect. What was a defect is that each pass used to cost
four or five separate commands, which is where "twenty minutes for a script"
went (2026-08-26).

Expect 3-5 passes. If the first draft measures clean, be suspicious rather
than pleased.

**THE LAST PASS IS THE HUMANIZER, AND IT IS NOT OPTIONAL.** When the script
measures clean and hits its word budget, run the `humanizer` skill over the
WHOLE script — not the lines the checker flagged. What it fixes is rhythm and
whether a sentence sounds like a person said it, which is precisely what
`script_doctor` cannot see; a script with zero measurable tells can still read
like a machine wrote it. Feed it our own shipped scripts as a voice sample (a
sample outranks its own style rules), and hold it to its own clause: no fact,
name, number, date or citation that is not already in the source text. Then:

```bash
python3 tools/script_approval.py humanized <slug>   # records the pass
```

`propose` refuses without that record, and refuses again if you edit a word
afterwards — the pass no longer covers the words you are showing. Never run
it AFTER approval: G27 hashes the approved narration, so a post-approval
rewrite correctly stops the build.

**A shot plan is NOT part of this loop.** `plan_shots.py --write` now refuses
until the script is approved and hash-fresh: every shot anchors to exact
wording, so a plan written against unapproved words is invalidated by the
first edit. Reading the clause breakdown (no `--write`) is fine and often how
you decide the script is ready.

### STEP 1.5 — Rehearse the VO for free, FIRST

```bash
python3 tools/rehearse_vo.py <slug>      # local, no credits, no API key
```

Synthesises a throwaway VO with chatterbox, whisper-times it, and checks
everything that only exists once a VO exists: that every `start_phrase` /
`end_phrase` in the shot plan actually resolves (a miss kills
`compile_shot_plan.py`), and which words the read mangles (feed those to
`caption_corrections`).

Do this BEFORE step 2. Generation costs credits and **freezes the audio**, so a
phrase anchor discovered afterwards costs a second generation. Exits non-zero if
any anchor is missing.

It prints a runtime prediction from the **measured** 2.5–2.7 wps, and prints the
synthetic audio's own duration marked as *not* the predictor — chatterbox's
speaking rate is not the twin's, and swapping a measured number for an
unmeasured one is what G23 flags (as advice — the discipline is yours). Artifacts land in
`_sources/<slug>/rehearsal/`, never `public/` (Remotion re-copies all of
`public/` on every render).

### STEP 2 — Voice + face — THE VOICE IS GENERATED OUTSIDE HEYGEN

**Changed 2026-08-27. HeyGen no longer speaks; it only moves the mouth.**

Measured, on the same cloned voice, same avatar, same words: **2.14 semitones
of pitch movement through HeyGen's TTS, 3.60 through ElevenLabs v3 with audio
tags.** Speaker similarity between them is 0.998 — the same voice — against
different-speaker controls at 0.959 and 0.964. 3.60 is the only read this repo
has ever measured above the 3.5 creator floor. Every HeyGen-side lever moved it
by 0.01, because uploaded audio bypasses TTS and tags placed in the API
`script` field are stripped before the voice ever sees them.

**1. Emit the tagged script.** Tags never go in `script.md` — G27 hashes that
as the approved narration and G21 checks captions against it.

```bash
python3 tools/vo_tagged.py <slug>        # -> jobs/<slug>/script-tagged.txt
```

Same words as the approved script, positional tags from `vo_direct`'s own
registers. Only documented ElevenLabs tags are emitted; an unrecognised tag is
spoken aloud or silently dropped.

**2. Generate it — no manual step (ElevenLabs MCP, connected 2026-08-27).**
`creative_generate_speech` with `model_id: eleven_v3` and the voice id in
`config.json` (`voice.elevenLabsVoiceId`). Poll
`creative_get_flow_run_status`, download the mp3 from `media[].url`.

Verified: tags are ACTED, not spoken — the transcript comes back clean, with
no `[curious]` audible. 3.17 semitones against HeyGen's 2.14 on identical
words, speaker similarity 0.991.

**The API exposes no stability control**, where the web UI does. A hand-made
175-second take measured 3.60 and this 9.6-second one 3.17 — length, emotional
range and stability all differ, so do not conclude the API is worse without
separating them. If a read comes back flatter than wanted, the web UI with
Creative stability is still available and `vo_external.py` takes its file
just the same.

**3. Prepare it.**

```bash
python3 tools/vo_external.py <slug> <downloaded.mp3>
```

Re-encodes with metadata stripped — **the ElevenLabs download as-is is REFUSED
by the upload** ("Stored file type not supported: application/octet-stream")
even though it is a valid mp3 — and checks the pace against the measured band.

**4. Upload and lip-sync.** `create_asset_upload` → PUT the bytes with the
returned headers unchanged → `complete_asset_upload` →
`create_video_from_avatar` with **`audioAssetId`**, never `script`/`voiceId`
(they are mutually exclusive). Store as
`public/assets/<slug>/avatar-master.mp4`.

Verified end to end: expressiveness survives the render (3.40 in → 3.31 out),
duration is preserved to 16ms, and the avatar gestures normally.

**G53 is what replaces the guarantee this costs us.** With TTS the audio was
synthesised FROM the approved script and could not diverge. An uploaded file
can, so the whisper transcript must now match the approved script at ≥0.70 —
threshold derived from real reels (legitimate 0.885–1.000, a different reel's
audio 0.013–0.110).

**Kick the generation, then go straight to STEP 3 while it renders** — the
two share no data, so the queue wait is either hidden behind asset cutting
or sat through doing nothing. `script_approval.py check` will remind you to
rehearse first (STEP 1.5) if `_sources/<slug>/rehearsal/` is empty.
Extract a 16k mono wav → whisper with word timestamps →
`public/assets/<slug>/vo.json`.

Fix mishears (product names, numbers) in the build script's CORRECT/FIX map —
**display text only, keep the original timings.**

### STEP 3 — Cut the assets
Cut only what the beat map binds, at the noted timestamps and crops. If you
discover a problem while cutting (the shot drifted, chrome is visible), update
the manifest *and* the beat map **before** building — not after rendering.

### STEP 3.9 — THE PRE-PUBLISH AUDIT (framework §11)

```bash
python3 tools/prepublish.py <slug>
```

The framework's closing instruction is *"approve only when facts, clarity,
retention, visuals, audio, platform fit, CTA, reveal handling, and overall
coherence pass a final audit."* Every piece of that existed in some tool; the
AUDIT did not, so "it passed" meant "nobody found anything".

It prints two halves and the split is the point: **measured** checks run and
fail, **judgement** items print as questions — the confused-viewer,
boring-article, payoff and removal tests, plus coherence. A machine cannot
answer those, and pretending it can is how taste ends up wearing a rule's
badge. Answer them out loud before shipping.

### STEP 4 — Build, register, render

**Preferred: compile the shot plan.** Each shot is anchored to the phrase it
illustrates, so `covers` is written for you and Rule 3 (G39) is satisfied by
construction — the phrase existed before anyone went looking for footage.

```bash
python3 tools/plan_shots.py <slug> --write   # script -> one shot per clause
# scout to satisfy each line, then fill asset_id + scene per shot
python3 scripts/compile_shot_plan.py <slug>  # writes src/beats/<slug>.json
python3 scripts/register_beats.py            # regenerates the composition index
python3 scripts/render_job.py <slug>         # render + TWO-PASS master + G31
```

**When the footage is ONE long screen recording**, do not cut it by hand. The
shot plan already knows how long every beat runs — it is anchored to spoken
phrases and the whisper timings — so only the *which moment goes where*
decision needs a person:

```bash
python3 tools/cut_clips.py --scan _sources/<slug>/<recording>.mov
# read out/<recording>-scan/scan-sheet.jpg, write the moments you chose into
# jobs/<slug>/clip-map.json  ->  {"shots": {"<shot index>": <seconds>}}
python3 tools/cut_clips.py --cut <slug> _sources/<slug>/<recording>.mov
```

It cuts each beat to the exact length its line needs, and REFUSES any clip that
would come out shorter than its beat — a short clip freezes on its last frame,
which is a blocking RENDER fault. A shot with no entry in the map is skipped,
never guessed: matching a moment to a line is a judgement about content, and
scene detection cannot make it. chatgpt-stickers' 18 clips were cut by hand
before this existed.

Then declare the assets `"surface": "screen"` in the manifest so the compiler
frames them as a phone rather than full-bleed (see **Surface** below).

**Fallback: a bespoke build script**, for a reel whose structure the shot plan
cannot express. You then owe `covers` by hand (`tools/link_shots.py <slug>`
justifies what it can from the manifest and refuses to guess the rest).

### Surface — what is the viewer looking at?

Every manifest asset may declare `surface`, and it decides the framing:

| surface | means | treatment |
|---|---|---|
| `screen` | a device UI recording | `deviceframe` — "go do this on your phone" |
| `graphic` | full-frame designed art | full bleed — "look at this" |
| `world` | real-world footage | full bleed — "look at this" |

A `screen` asset in a plain `footage` shot is **forced** into
`deviceframe(phone)` at compile. Write `"fullBleed": true` on the scene to
opt out deliberately.

**It is declared because it cannot be measured.** The obvious guess — 1080x1920
means a phone screen recording — is wrong: 8 of this repo's 32 exactly-1080x1920
clips are `iphone18-colors`' Pantone chip graphics, and a bezel around a colour
swatch lies about what is on screen. A document you want READ is neither: that
is `sourceread` / `receipt`, full bleed, because a bezel only shrinks the words.

```bash
cp tools/build_template.py tools/build_<slug>.py   # then fill it in
python3 tools/build_<slug>.py                      # writes src/beats/<slug>.json
```

**Master through `render_job.py`, never a bare ffmpeg line.** This section used
to end with `ffmpeg -af "loudnorm=I=-14:TP=-1.2:LRA=7"`, which is a SINGLE pass:
loudnorm is adaptive and converges toward the target without reaching it, so it
lands roughly 1 LU short and G31 rejects the result. `render_job.py` measures
first, then applies the measured values.

`check_beats()` raises only on the rules in `BLOCKING_RULES` — the three
standing rules, plus render correctness and rights. Runtime length, pacing,
headline lengths, facecam share, clip reuse and SFX count are **advice** now:
they print with their evidence and stop nothing. (This paragraph claimed the
opposite until 2026-08-17.)

The concurrency/timeout flags are required — the default hits "delayRender
timed out" on reels with many video sources plus two audio tracks.

### STEP 5 — CRITIC pass (mandatory before delivering)
```bash
cp out/<slug>-final.mp4 out/<slug>.mp4 && python3 tools/lint_frames.py <slug>
```
This now **exits non-zero** on a hard flag (pacing, clip reuse, edge-cropped
text, near-duplicate scenes, hook dead space). `--soft` overrides it — and if
you use it, say so when you hand the reel over.

Then extract a frame strip across all beats and review it **as a hostile
viewer**. The linter catches geometry; only you catch meaning:

- Does each frame show what the voiceover claims *at that second*?
- **Any screen that needs explaining is a failure.**
- Crops centred? Captions clear of the face and of any baked-in text?
- Every number carrying its unit/label?
- No app chrome (browser tabs, sidebars) anywhere?
- Integrated loudness ≈ −14 to −15 LUFS?

Fix, re-render, re-verify. Only then deliver.

---

### STEP 6 — Cover (Reels + Shorts) — SKIPPED BY DEFAULT (user directive, 2026-08-24)

**Do not run this step for a reel unless the user asks for a cover on that
specific one.** Standing rule, not per-video: no thumbnail/cover generation
going forward. The tool and the spec below stay documented for the rare
explicit request.

```bash
python3 tools/make_thumbnail.py <slug> \
    --frame "assets/<slug>/thumb-subject.png" \
    --brand "APPLE" --line1 "TIM COOK'S" --line2 "LAST KEYNOTE"
```

**1080x1920, vertical.** Our reels are vertical; a 16:9 cover was the first
version of this and was wrong (rejected 2026-08-17). `--format wide` still
exists for any surface that wants a wide still.

**The centre 1:1 crop is the whole game.** A profile grid centre-crops a 9:16
cover, so read-critical content lives in y = 420..1500 and the rest is bleed.
The tool always writes `<slug>-grid.png` alongside — that is how the grid
actually shows it. **Judge the grid file, not the full-height one.**

The look: near-black ground, ALL-CAPS heavy sans, subject in the middle, and a
two-line headline whose SECOND line sits on a solid accent block. The block is
the payoff and the loudest thing in frame. Default block is the style accent
(editorial yellow); `--block "#E8112D" --block-text "#ffffff"` for the red
convention. Yellow is more differentiated in a feed that is mostly red, and
black-on-yellow carries a higher contrast ratio than white-on-red.

Hard limit: **3 words per line**, enforced. At ~200px a longer line is a smear;
cut words, never shrink the type.

**No presenter face.** The reference creators anchor on their own face; we are a
publication, so the anchor is the SUBJECT.

**Choose the frame for its SHAPE, not its content.** At 200px a dense text card
is just a bright rectangle — it reads as "a document" and nothing more. A
product render, a device, one huge number: those still read. Crop the subject
out of the reel frame first rather than passing the whole 9:16.

## 3. The beat-sheet contract

`src/types.ts` is the source of truth. Shape:

```jsonc
{
  "id": "my-reel", "fps": 30, "width": 1080, "height": 1920,
  "audio": "assets/<slug>/avatar-master.mp4",
  "music": { "src": "music/bed-184.mp3", "from": 32.0,
             "points": [{"t":0.0,"vol":0.15}, {"t":6.0,"vol":0.08}] },
  "captionStyle": "chip-small",
  "emphasis": ["a phrase", "42"],
  "scenes": [ ... ],
  "captions": [ {"start":0.0,"end":0.6,"text":"two or three words"} ]
}
```

Every scene shares: `durationSec` (required), `sfx?`, `captionBottom?` (push
captions off faces/seams), `headline?` (editorial serif overlay usable on *any*
scene type).

Key scene types — full table in `PIPELINE.md` §3:

| type | use |
|---|---|
| `footage` | full-bleed clip (b-roll or presenter) |
| `split` | hook: footage top / face bottom |
| `receipt` | screenshot proof; zooms + sweeps highlights onto exact phrases |
| `floatcard` | **framed 16:9 window** — how you show any app/document recording |
| `specsheet` | dark comparison table with column headers + units |
| `wordcascade` | words stacking in sequence |
| `hcompare` / `comparesplit` | before/after comparisons |
| `statcard`, `checklist`, `categorygrid`, `carousel`, `xpost` | structured MG |

---

## 3b. THE EDITOR'S PASS — do this before every render

Added 2026-08-25, user directive: *"think of yourself as a years-experienced
video editor who is also expert in editing for reels and shorts, and edit as
per the need of the topic and script."*

The gates prove a reel is not BROKEN. They cannot tell you it is not EDITED.
A sheet where every beat carries the same `zoomDir: "in"` passes everything
and still watches like a slideshow — which is exactly what claude-eating-
tokens was until this pass.

So after compiling and before rendering, print the cut and read it:

```bash
python3 tools/cut_sheet.py <slug>      # every beat: time, duration, motion
```

Then ask these five questions and CHANGE something for each one that fails.
None of them is a threshold; they are the questions an editor asks.

1. **Does any two adjacent beats move the same way?** Two shots that both
   push in read as one long shot with a glitch. Give one of them a different
   job: establish wide, then hold tight. Same asset, two moves, is a CUT.
2. **Where is the longest shot, and what time does it sit at?** A long hold
   early is confidence; the same hold at 40s is a dropped viewer. Split it
   on its own second clause — most sentences have one.
3. **Does the motion fight the asset?** A recording that already scrolls
   does not want a push on top; that is two motions arguing. A static
   oversized asset wants the opposite: let it travel (`slide`), optionally
   with a slow push for depth (`zoom` + `slide` compose — the slide reads
   the content, the push keeps it alive).
   **And check what the asset can afford.** A mobile capture is 1080 wide —
   exactly the frame — so scale on it crops words off BOTH edges. A `zoom:
   1.5` meant to make a README claim readable chopped that claim in half
   (2026-08-25). Frame a full-width capture by choosing its SLICE (`focusY`)
   and its MOMENT (`from`), at 1:1. Save scale for assets genuinely wider
   than the frame. Compile prints an advisory when a zoom exceeds what the
   source can afford.
4. **Does the shape follow the story?** A myth-buster should SLOW at its
   turn and ACCELERATE through its fixes. Compare the beat durations either
   side of the pivot; if they are the same, the edit is not telling the
   story the script is telling.
5. **Is every frame doing the job its line asks for?** A tool being NAMED
   wants the tool visible; a claim being PROVED wants the sentence readable.
   That decides zoom-vs-hold more reliably than any preference.

Record what you changed and why in the STYLE-RULES entry for the reel. The
next editor (you, in a month) needs the reasoning, not the values.

---

## 4. Non-negotiable visual rules (learned the hard way)

1. **Never open on a document, browser, file bin, black screen or loading
   spinner.** Open on the strongest shot of the payoff, full-bleed.
2. **Show what was built, not text about what was built.** If you're tempted to
   render a tweet as a text card, you're missing footage — go get it.
3. **App/document recordings go in framed `floatcard`s, never full-bleed.**
   Blowing a 16:9 document up to fill 9:16 produces cropped walls of text.
4. **No flat empty backdrops.** A small asset on a black field is dead space —
   `receipt` fills the frame with a blurred copy of itself behind the card.
5. **Crop out all app chrome** — browser tabs, sidebars, PiP webcams. One stray
   tab reads as a mistake.
6. **Every number on screen carries its unit or label.** "9.5 · 3¢" means
   nothing; "QUALITY /10" + "COST / RUN" column headers mean everything.
7. **Let the payoff breathe.** The money shot plays clean — no captions, no
   graphics over it, music up.
8. **Nothing static.** Punch-in on every cut, alternating zoom directions;
   no unchanged screen holds longer than ~1.5s (except the payoff).
9. **The face appears early** (usually a split hook) and returns for opinions —
   roughly 10–20% of runtime, not throughout.
10. **Sound:** music bed always, volume-automated (full at hook → duck through
    explanation → rise at the reveal → up at CTA → fade). 6–9 sparse SFX cues,
    ordinary cuts silent. Master to −14 LUFS.

---

## 5. Failure modes to avoid

| Symptom | Root cause | Fix |
|---|---|---|
| Text cards standing in for demos | Scripted before scouting | Rewrite script to available footage |
| Walls of cut-off text | Full-bleeding a 16:9 document | Framed `floatcard` |
| Large dead black areas | Small asset on flat backdrop | Blurred self-fill behind card |
| Ghost sidebars / stray tabs | Crop bounds too wide | Re-crop to artifact bounds only |
| Meaningless numbers | Missing units | Add column headers/labels |
| Tail drift / audio desync | Scenes don't sum to audio | Enforce the sum in the build script |
| "delayRender timed out" | Default render concurrency | `--concurrency=6 --timeout=120000` |
| Fonts 404 in render | Raw `/fonts/...` URL | Use `staticFile("fonts/...")` |
| Misframed face | Vertical avatar auto-crop | Generate wide, crop with a measured face-x |

---

## 6. Setup

- **Node** ≥ 18, then `npm install`
- **Python 3**, **ffmpeg/ffprobe**, **yt-dlp** on PATH
- `pip install openai-whisper` (word timings; `base` model is enough)
- Headless Chrome (screenshot receipts)
- A HeyGen account (or any avatar/TTS provider) — put **your own** avatar and
  voice IDs in `config.json` (copy `config.example.json`)
- Optional: `pip install gradio_client` for the voice-clone path

Nothing in this repo contains credentials. Never write API keys, tokens or
presigned URLs into project files or logs.

---

## 7. Extending the engine

To add a new scene type:
1. Add it to the `Scene` union in `src/types.ts`
2. Create `src/components/<Name>.tsx`
3. Add a `case` in `SceneSwitch` inside `src/Reel.tsx`

When the user gives feedback, append it to `STYLE-RULES.md` as
*raw note → root cause → distilled rule*, then apply it. The ledger is what
makes the system improve instead of repeating mistakes.

---

## 8. Credit and honesty

- Keep an `@credit` on screen for third-party footage.
- Every factual claim needs a receipt. No receipt → make it an on-camera
  opinion, or cut it.
- If research contradicts the user's premise, **say so and correct it** rather
  than repeating a checkable falsehood. A corrected beat usually makes a
  stronger reel than the myth did.
