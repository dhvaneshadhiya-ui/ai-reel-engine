# News-Reel Pipeline — full handoff

Topic / post / pointers **in** → finished vertical reel (1080×1920, 30fps, mastered)
**out**, with the creator's AI face + voice, official sourced footage, motion
graphics, SFX + music, rendered as code. Zero manual video editing.

This document is self-contained: an agent with this repo + the prerequisites
below can reproduce the reels. It is the source of truth; `SKILL.md` is the
short playbook, the `styles/*.md` packs define the LOOK, `FEEDBACK.md` is the
learned-rules ledger.

---

## 0. What the pipeline is

A **Remotion** (React-video-as-code) project. Every reel is a **beat sheet**
(one JSON file) that lists timed **scenes**; a library of ~22 scene
**components** renders them; a Python **build script** generates the beat sheet
by anchoring scene cuts to the **voiceover's word timings** (from whisper). The
voiceover is the master clock — visuals are cut to the spoken words.

Flow per reel:

```
topic ──▶ scout claims + official ASSETS ──▶ manifest
      ──▶ script + giveaway + phrase-anchored shot plan
      ──▶ native HeyGen VOICE + FACE ──▶ whisper word-timings
      ──▶ compile_shot_plan.py ─writes─▶ src/beats/<slug>.json
      ──▶ register_beats.py ──▶ remotion render ──▶ master to -14 LUFS
      ──▶ verify (frame strip) ──▶ deliver
```

---

## 0b. Scout → Director flow (2026-07-28 upgrade)

The topic (or short script) is ALWAYS user-provided. Before ANY scripting:
1. **ASSET SCOUT** — verify the story, hunt visuals, and write
   `public/assets/<slug>/manifest.json`: per asset `{id, kind, source, shows
   (verified by looking at frames), quality, credit, crop}` + the always-
   available MG component list. Thin manifest = more MG/facecam-led reel.
2. **SCRIPT DIRECTOR** — loads the requested style pack (for Nick reels,
   `styles/nick-saraev.md`) + the manifest; writes script + beat map where
   EVERY beat binds to a manifest id or an MG spec. Beats with unresolvable visuals are illegal:
   re-scout (specific request, max 1-2 loops) or rewrite the line.
3. Validation gate before generating anything; CRITIC pass after render
   reviews the frame strip against the beat map.
Root lesson (kimi-k3): never script a claim you can't show — footage first,
then write to it.

## 1. Prerequisites

- **Node** ≥ 18, `npm install` in the repo (Remotion 4.0.501, React 18).
- **Python 3**, **ffmpeg/ffprobe**, **yt-dlp** on PATH.
- **openai-whisper** (`pip install openai-whisper`, needs torch) for word
  timings. Model `base` is enough.
- **gradio_client** only when explicitly using the optional VibeVoice path.
- **Headless Chrome** for screenshot receipts (macOS path in §6).
- **API access** (see §4):
  - HeyGen MCP/API — default native TTS + avatar.
  - VibeVoice HF Space — optional voice clone; community-run, with a daily GPU
    quota.
  - (optional) Higgsfield — AI b-roll generation.

Render always with reliability flags (§7):
`npx remotion render <slug> out/<slug>.mp4 --concurrency=2 --timeout=120000`

---

## 2. Repository layout

```
news-reels/
  package.json  tsconfig.json  remotion.config.ts
  src/
    index.ts            # registerRoot
    Root.tsx            # registers every beat sheet as a <Composition> — ADD NEW REELS HERE
    Reel.tsx            # the player: SceneSwitch + PunchIn + music/sfx + captions + headline overlay
    types.ts            # THE CONTRACT — BeatSheet + every Scene type (read this first)
    components/         # one file per scene type (see §8)
    beats/<slug>.json   # generated beat sheets (the reels)
  tools/
    build_<slug>.py     # per-reel beat-sheet builders (copy one as a template)
    tighten_vo.py       # remove VO dead-air + tempo, whisper-free re-timing
    gen_pod_vo.py       # VibeVoice generation example (gradio_client)
  styles/
    varun-mayya.md      # DEFAULT style pack (voice, scene grammar, captions, sound, treatment history)
    nick-saraev.md      # 2nd style pack
  public/
    fonts/  Fraunces-400/600/Italic.woff2, PressStart2P.ttf
    sfx2/   varun SFX (impact-deep/cool, tech-slide, pops, riser-sweep.wav, whoosh-stutter)
    sfx-nick/ nick SFX (word-pop, soft-click, bubble, card-slide)
    music/  bed-140/184/726.mp3 (+ spec pngs)
    assets/<slug>/  per-reel: avatar-master.mp4, vo*.json/wav, clips/, face-x.txt
  _sources/           # raw yt-dlp downloads (kept OUT of public/ so Remotion doesn't copy them)
  FEEDBACK.md         # learned rules ledger — READ FIRST, append after every review
  SKILL.md            # short playbook
  PIPELINE.md         # this file
```

Keep `public/` lean: after cutting clips, move raw downloads to `_sources/` and
delete diagnostic PNGs — Remotion copies ALL of `public/` on every render.

---

## 3. The beat-sheet schema (the contract — `src/types.ts`)

```jsonc
{
  "id": "record-skill", "fps": 30, "width": 1080, "height": 1920,
  "audio": "assets/<slug>/avatar-master.mp4",   // VO master track (video's audio or a wav)
  "music": { "src": "music/bed-184.mp3", "from": 32.0,
             "points": [ {"t":0.0,"vol":0.15}, {"t":6.0,"vol":0.08}, ... ] },  // volume automation
  "captionStyle": "chip-small",   // "sans"(56px) | "chip-small"(38px, restrained) | "chip-lg" | "mono"
  "emphasis": ["Record a Skill","Pro","Max"],  // substrings shown yellow #FFD84D in caption chips
  "scenes": [ /* see below */ ],
  "captions": [ {"start":0.0,"end":0.6,"text":"two or three words"}, ... ]  // absolute seconds
}
```

**Every scene** shares `SceneBase`: `durationSec` (required), `sfx?` (array of
`{src, at?, vol?}` seconds-into-scene), `captionBottom?` (px from frame bottom;
push captions off the face/seam — e.g. 1000 on split hooks, 6000 to hide),
`headline?` (editorial serif overlay, see below). Scenes SUM exactly to the
audio duration.

**Scene types** (`type` field selects the component):

| type | key fields | use |
|---|---|---|
| `footage` | `src, from?, zoomDir(in/out/none), focusX?, kinetic?, credit?, infocard?{heading,body,at}` | full-bleed clip (b-roll or facecam) |
| `split` | `topSrc, topFrom?, topFocusX?, bottomSrc, bottomFrom?, bottomFocusX?, kinetic?` | hook: footage top / face bottom |
| `receipt` | `src, srcWidth, srcHeight, backdrop(cream/black), highlights[{at,x,y,w,h}], credit?` | screenshot proof; zooms to highlight |
| `typecard` | `kinetic{text,style}, bg?, fg?` | full-screen statement card |
| `wordcascade` | `words[{text,style(serif/caps/pixel/gradient),at,size?}], bg?, mascot?, bottomSrc?` | words stacking in sequence |
| `promptcard` | `promptText, highlights[], headline?, subtext?, loaders?(n), lines?[], app?, bg?` | AI-prompt UI card, keyword highlights |
| `categorygrid` | `cards[{label,sub?}], headline?, selectIndex?, selectAt?` | 2×2 cards + select-one animation |
| `carousel` | `items[{src}], selectIndex, headline?` | swipe through cards, land on winner |
| `designreveal` | `items[{src}], selectIndex` | full-screen sequential reveal, winner held |
| `checklist` | `rows[{label,state(done/q)}], headline?` | ✓/✓/? status list, ? enlarged |
| `comparesplit` | `leftSrc, rightSrc, leftLabel?, rightLabel?, topText?, midText?, finalText?, question?` | vertical L/R compare, banners |
| `hcompare` | `topSrc, bottomSrc, topLabel?, bottomLabel?, topFrac?, messages[]` | horizontal top/bottom compare, cyan match boxes |
| `specsheet` | `title, kicker?, rows[{label,value,accent?}], footnote?` | dark spec card, 1 accent row (premium MG) |
| `statcard` | `title, titleRight?, rows[{label,value,pct,color?}], footnote?, bg?` | animated bar stats |
| `desktopmockup` | `files[{name,kind}], selected?, bg?` | fake desktop with file icons |
| `uidialog` | `app?, title, body?, field?, select?, primary?, cancel?` | fake app dialog |
| `logobeat` | `src?/text?, mark?(starburst), markColor?, pixel?, bg?, label?` | animated logo/mark beat |
| `floatcard` | `src, from?, bg?(black/cream/gradient), kinetic?, credit?` | 16:9 screen recording in a floating card |
| `endquestion` | `src, question` | closing ad-freeze + YES/NO |

**`kinetic`** (`{text, style, at?, y?}`): on-scene type. `style`:
`caps`(condensed black), `serif`(Fraunces italic), `chip`. Prefer **serif** for
titles (premium); caps for rare punch.

**`headline`** (premium editorial title that BUILDS line-by-line — the signature
hook treatment): `{ lines:[{text, kind(label/headline/subtitle), at, accent?}],
y?, align?, theme? }`. `label`=small upright serif, `headline`=large bold serif
with grey→ink reveal, `subtitle`=italic serif. Set `theme:"dark"` over light
footage. Rendered as an overlay by `Reel.tsx`, so ANY scene can carry one.

---

## 4. Production constants (creator = the creator)

- HeyGen avatar (digital twin): **`<YOUR_HEYGEN_AVATAR_ID>`**
- HeyGen voice (English clone "creator"): **`<YOUR_HEYGEN_VOICE_ID>`**
- Generate one continuous avatar master at **1080p, engine avatar_v, speed
  1.2**. Follow the active connector's aspect-ratio schema (`9:16` for portrait
  requests) and inspect a calibration frame before committing the edit.
- **face-x** = face-centre fraction on a mid avatar frame (≈0.41 here) →
  `public/assets/<slug>/face-x.txt`. `css_pos()` in the build script converts it
  per container (full-frame vs split half). Measure with a `drawgrid` overlay.
- Reel output: **1080×1920, 30fps**. Length per style pack (varun 38–55s).

### Voice + face generation

**Optional voice = VibeVoice** clone (only when explicitly chosen):
```python
from gradio_client import Client, handle_file
c = Client("vibingvoice/vibe-voice-custom-voices")
res = c.predict(text=SCRIPT, speaker1_audio_path=handle_file(REF),
                speaker2_audio_path=None, speaker3_audio_path=None, speaker4_audio_path=None,
                seed=42, diffusion_steps=24, cfg_scale=1.3, use_sampling=False,
                temperature=0.95, top_p=0.95, max_words_per_chunk=250,
                api_name="/generate_speech_gradio")   # returns a wav path
# REF = clean ~18s sample of the real voice: _private/voice/voice-ref.wav
```
VibeVoice reserves a **fixed 90s GPU block per call**; if <90s daily quota
remains it fails until reset (~daily). No local whisper needed for timings if you
reconstruct them (see `tools/tighten_vo.py`).

**Face** (audio-driven avatar): convert VO→mp3, upload to HeyGen
(`create_asset_upload` → PUT to presigned S3 → `complete_asset_upload`), then
`create_video_from_avatar(avatarId, audioAssetId, connector-compliant aspect,
1080p)` — no script/voice (audio-driven `avatar_iv`). Download →
`avatar-master.mp4`. For a portrait reel, explicitly use the connector's
required `9:16` value and inspect a calibration frame before production.

**Default: native HeyGen TTS** — one call does face+voice together and gives
the most reliable lip sync:
```
create_video_from_avatar(avatarId=b4b3…, script=SCRIPT,
  voiceId=<YOUR_HEYGEN_VOICE_ID>, aspectRatio="9:16", resolution="1080p",
  engine={"type":"avatar_v"}, voiceSettings={"speed":1.2})
```
Poll `get_video(id)` until `completed`, download `video_url` →
`avatar-master.mp4`.

**Word timings:** extract 16k mono wav from the avatar, then
```python
import whisper; m=whisper.load_model("base")
r=m.transcribe("vo16.wav", word_timestamps=True, language="en")
# save [{start,end,word}] → public/assets/<slug>/vo.json
```
Fix whisper mishears (e.g. "cloud"→"Claude") in the build script's CORRECT/FIX
maps — **display text only, keep the timings.**

---

## 5. The build-script pattern (`tools/build_<slug>.py`)

Copy an existing one (`build_record_skill.py` is the current best template).
It:
1. Loads `public/assets/<slug>/vo.json` word timings.
2. `css_pos(face_x, iw, ih, cw, ch)` → objectPosition fraction for face framing.
3. `find(phrase)` → the whisper end-time of an anchor phrase; each beat ends on
   its anchor so cuts land on spoken words. Scenes then SUM to the audio.
   (Alternatively, fixed per-scene durations for tight pacing — see
   `build_pod3.py` — with captions still driven by the VO.)
4. Builds the `scenes` list (choose components per §3, per the style pack).
5. Chunks captions to 2–4 words; applies the emphasis + mishear-fix maps.
6. Sets the `music` volume-automation points (full at hook → duck → rise at
   reveal → up at CTA → fade).
7. Writes `src/beats/<slug>.json` and prints `scenes Xs vs audio Ys` (must match).

Then **register** the reel in `src/Root.tsx` (import the json, add to the
`sheets` array).

---

## 6. Asset sourcing (source-first, verify-always)

- **Footage**: `yt-dlp "ytsearchN:…"`, prefer official channels, keep `@credit`
  on screen. Download HD: `--extractor-args
  "youtube:player_client=default,android" -f "bv*[height>=720]+ba/b"`. Scan with
  fps-tiled contact sheets, then cut 9:16:
  `crop=608:1080:X:0,scale=1080:1920` (from 1080p; scale 4K→1920 first). Center
  `X` on the subject. **Verify every clip with a frame strip; re-cut misses.**
- **Receipts**: headless Chrome —
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new
  --disable-gpu --hide-scrollbars --virtual-time-budget=20000
  --window-size=1100,1500 --screenshot=out.png URL`. Crop to a clean column;
  READ the screenshot and record exact highlight rects (never guess). x.com
  blocks headless — pull tweet frames from 4K YouTube screen-recordings.
- **AI b-roll** (optional): Higgsfield (soul still → Kling image-to-video).

Contact sheet without ImageMagick font issues:
`ffmpeg -i in.mp4 -vf "fps=1/2,scale=220:391,tile=6x4:padding=4:color=white" -frames:v 1 out.png`

---

## 7. Render · master · verify

```bash
npx remotion render <slug> out/<slug>-raw.mp4 --concurrency=2 --timeout=120000
ffmpeg -y -i out/<slug>-raw.mp4 -af "loudnorm=I=-14:TP=-1.2:LRA=7" -c:v copy out/<slug>-final.mp4
```
- `--concurrency=2 --timeout=120000` avoids "delayRender timed out" on reels with
  many OffthreadVideo sources + 2 audio tracks (default 4× hits it; single frames
  render fine, so it's parallel load, not content).
- **Verify (mandatory before delivery):** frame strip across all beats
  (script↔visual match, crops centered, captions off the face, credits present);
  zoom-check each receipt highlight sits on its text; check kinetic/headline
  legibility on its backdrop; confirm integrated loudness ≈ −14 to −15 LUFS
  (`ffmpeg -i final.mp4 -af ebur128 -f null -`).

Probe a single frame fast: `npx remotion still <slug> out.png --frame=N`.

---

## 8. Component catalog (`src/components/`)

Renderers: `FootageScene, SplitScene, ReceiptScene, TypeCard, WordCascade,
PromptCard, CategoryGrid, Carousel, DesignReveal, Checklist, CompareSplit,
HCompare, SpecSheet, StatCard, DesktopMockup, UIDialog, LogoBeat, FloatingCard,
EndQuestion, KineticType (on-scene type), HeadlineBuild (serif title overlay),
CaptionChips (caption bar)`. Add a new scene type by: add it to the `Scene`
union in `types.ts`, write `components/<Name>.tsx`, add a `case` in
`Reel.tsx`'s `SceneSwitch`.

---

## 9. Style packs & self-improvement

- **Pick a style FIRST** (`styles/varun-mayya.md` default, or `nick-saraev.md`
  if named). The pack defines script voice, scene grammar, caption spec, sound
  recipe, and a **treatment history** — never repeat the previous reel's
  treatment for the same info type. A reference reel the user gives supplies the
  TOPIC/style only, **not** visuals (unless they say "use these visuals").
- **Read `FEEDBACK.md` FIRST** every reel — its rules override everything. After
  each user review, append: raw note → root cause → distilled RULE (filed under
  the style or universal). Universal process rules → `SKILL.md`; style taste →
  the pack; treatment → the pack's history.

Current premium bar (2026-07): editorial **serif headlines** (HeadlineBuild),
**footage-forward** full-bleed, and **SpecSheet** for "what/how". Caption and
palette rules come from the active pack: Nick uses `chip-lg` plus
cream/black/orange; Varun uses restrained `chip-small`. Music bed always,
volume-automated; 6–9 sparse SFX; master −14 LUFS.

---

## 10. Gotchas (learned)

- Scenes MUST sum to the audio length or the tail drifts.
- Render with `--concurrency=2 --timeout=120000` (see §7).
- Fonts: load via `staticFile("fonts/…")` in `loadFont`, not a raw `/fonts/…`
  URL (404s in render).
- HeyGen: request the connector-required explicit `9:16` portrait aspect,
  inspect a calibration frame, and use fit/split treatment if the crop is poor.
- VibeVoice is opt-in only and reserves a 90s GPU block per call.
- Whisper mishears: fix in the CORRECT/FIX display maps, keep timings.
- Keep `public/` lean (it's copied every render); raw downloads → `_sources/`.
- Avoid modern CSS the render Chromium may lack (used rgba interp, not
  `color-mix`).

---

## 11. Quickstart for a fresh agent

1. `npm install`; ensure ffmpeg, yt-dlp, and whisper. VibeVoice's
   `gradio_client` is optional.
2. Read `FEEDBACK.md` + the chosen `styles/*.md`.
3. Initialize the job; scout official assets and complete `manifest.json`.
4. Write `scripts/<slug>.md`, the real giveaway, and phrase-anchored
   `jobs/<slug>/shot-plan.json`.
5. Generate native HeyGen face+voice → `avatar-master.mp4`; inspect the
   calibration frame and Whisper to `vo.json`.
6. Run `compile_shot_plan.py`, which writes `src/beats/<slug>.json`.
7. Run `register_beats.py`; no manual `Root.tsx` edit is needed.
8. Run `render_job.py` → master → lint → verify. Deliver and log feedback.
```
```
