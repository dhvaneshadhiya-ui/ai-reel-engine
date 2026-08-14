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

### STEP 0 — Load context
1. Read `STYLE-RULES.md`. Its rules override this file.
2. Pick the style pack in `styles/`. It defines the LOOK and the script voice.
   This file defines the PROCESS.
3. Check the pack's *treatment history* — never repeat the previous reel's
   visual treatment for the same kind of information.

### STEP 1a — ASSET SCOUT (before writing a single script line)
Verify the story (web search — topics are usually newer than your training
data), then hunt visuals and write `public/assets/<slug>/manifest.json`:

```jsonc
{
  "topic": "...",
  "verified_facts": ["fact — source url", "..."],
  "assets": [
    { "id": "clip-demo",
      "kind": "footage|receipt|brand|still",
      "source": "yt:VIDEO_ID @t120-128 | url",
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

**Verify every candidate by extracting frames and looking at them.** Write the
`shows` field from what you actually see, never from what you assume. A thin
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

### STEP 2 — Voice + face
Generate one continuous avatar master from the final script (see
`references/heygen.md`). Store as `public/assets/<slug>/avatar-master.mp4`.
Extract a 16k mono wav → whisper with word timestamps →
`public/assets/<slug>/vo.json`.

Fix mishears (product names, numbers) in the build script's CORRECT/FIX map —
**display text only, keep the original timings.**

### STEP 3 — Cut the assets
Cut only what the beat map binds, at the noted timestamps and crops. If you
discover a problem while cutting (the shot drifted, chrome is visible), update
the manifest *and* the beat map **before** building — not after rendering.

### STEP 4 — Build, register, render
```bash
cp tools/build_template.py tools/build_<slug>.py   # then fill it in
python3 tools/build_<slug>.py             # runs the GATES, writes src/beats/<slug>.json
python3 scripts/register_beats.py         # regenerates the composition index
npx remotion render <slug> out/<slug>-raw.mp4 --concurrency=2 --timeout=120000
ffmpeg -y -i out/<slug>-raw.mp4 -af "loudnorm=I=-14:TP=-1.2:LRA=7" -c:v copy out/<slug>-final.mp4
```
The build script calls `reel_gates.check_beats()`, which **raises** on any
mechanical rule violation — runtime band, pacing ceilings, headline line
lengths, facecam share, clip reuse, SFX count, manifest provenance. A failing
sheet is never written, so it cannot reach the renderer.

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
| "delayRender timed out" | Default render concurrency | `--concurrency=2 --timeout=120000` |
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
