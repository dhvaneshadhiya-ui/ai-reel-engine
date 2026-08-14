# Style pack: nick-saraev  (v2 — deep re-teardown 2026-07-24)

WHY v2: v1 was built from low-res thumbnails and came out shallow. This pass
used full-res detail crops + 8fps motion bursts of all 12 reels. The quality gap
was NOT the concept — it was execution: captions, real designed graphics, and
MOTION. Fix those and we match him.

## Content & script (unchanged, was right)
- Utility/tool-tips, "top 5", free-hacks. "Free" is the magnet word.
- 26-48s, ~230 wpm. Comment-gate CTA ("comment WORD, I'll DM the link").
- Hook = "You can now X for free" / "You don't need to pay for X anymore" /
  "X just dropped Y — completely free" / "here are the top 5 Y you need".
- Structure: hook → what it is (1 line) → HOW (numbered: First/Then/Next) → CTA.

## THE QUALITY GAPS (what to actually fix)

### 1. CAPTIONS — his are a whole system, ours were flat chips
His text has FIVE distinct treatments, all clean SF Pro:
  a. **Chip captions**: dark pill rgba(0,0,0,.82), radius ~10, WHITE BOLD ~46-52px
     (bigger than our 38px!), 1-3 words, centered lower-mid. Subtle soft edge.
  b. **Big single-word beats**: one word ("five", "website") huge (~90px) bold,
     centered mid-frame on the clean bg — a punctuation moment.
  c. **File-selection labels**: filename on a BLUE (#2563EB) selection highlight,
     exactly like a highlighted desktop file (e.g. "brand-guidelines.zip").
  d. **Info cards**: bold HEADING (~54px) + 1-2 lines of body (~34px regular) on a
     dark gradient scrim over the facecam. Real hierarchy, not a caption.
  e. Serif + pixel display (see 3).
→ HISTORICAL ENGINE NOTE (superseded by `chip-lg` below): enlarge the compact
caption treatment to ~48px bold; add caption variants "big-word",
  "file-select" (blue), and "info-card" (heading+body scrim).

### 2. GRAPHICS — real designed artifacts, not flat cards
  - **Desktop / Finder mockups**: numbered arrows (1-2-3-4-5 in a handwritten-ish
    accent) pointing at real file icons (PDF, .md, folder, .zip) on cream.
  - **UI dialog recreations**: pixel-perfect app dialogs (NVIDIA "Generate API
    Key", VS Code editor, provider settings) — clean, real, credible.
  - **Stat / budget cards**: titled card ("Free-Tier Budget 1.4B") with rows +
    COLORED PROGRESS BARS (each provider a bar), soft shadow on cream/black.
  - Screen recordings of the actual tool in a rounded window.
→ ENGINE: new scenes — StatCard (rows + animated bars), DesktopMockup (icons +
  numbered arrows), UIDialog (styled recreation), keep FloatingCard for screen-recs.

### 3. MOTION — the biggest miss. His stuff MOVES; ours popped and froze.
From the 8fps bursts:
  - **Stat-card bars FILL** left-to-right, row by row, over ~0.8-1.0s (staggered).
  - **Pixel logo ANIMATES**: the Claude-Code starburst SPINS, and a vertical beam
    DRAWS downward beneath it.
  - **Serif reveals word-by-word** ("TO 1.6" → "TO 1.6 BILLION") with ease-out +
    slight scale, not a hard pop.
  - Cards SLIDE + settle with a soft spring; elements stagger in, never all-at-once.
→ ENGINE: animate bar widths (interpolate + stagger), animate the pixel logo
  (rotate + draw a beam via strokeDashoffset), refine WordCascade easing to
  ease-out-cubic with per-word stagger + subtle scale.

### 4. TYPE — his serif is high-end editorial, not Georgia
  - Display serif italic looks like **PP Editorial New Italic** (high contrast,
    elegant) — get that font (or closest free: "Newsreader" italic is decent).
  - Pixel = Press Start 2P (we have it) but used sparingly + animated.
  - Body/caption = SF Pro (system) — we have it.
→ ENGINE: add the editorial serif @font-face (data-URI); route "serif" style to it.

## Sound (v1 was ~right, keep)
Bed ~20 LU under voice (rhythmic lofi w/ drums, near-flat). Use 6–9 tiny
click/pops on the most meaningful word/element landings (vols .06-.10), with
ordinary cuts silent. No risers/bass drops.
public/sfx-nick + music/bed-726.

## Captions default = "chip-lg" (NEW): SF Pro, 48px, weight 800, white on
rgba(0,0,0,.82) pill radius 11, plus the 4 variants above per beat.

## v2 COMPONENTS — ALL BUILT & VERIFIED (2026-07-24)
- captionStyle "chip-lg" = 50px/800 SF Pro, pill rgba(0,0,0,.82), radius 12,
  inset edge. DEFAULT for nick reels. (chip-small still exists for tiny.)
- statcard scene: title + titleRight + rows[{label,value,pct,color}] + footnote;
  bars FILL staggered row-by-row (his signature). bg cream|black.
- logobeat mark:"starburst" = animated spinning pixel star + drawing beam +
  pixel text (Press Start 2P). markColor sets the star color.
- serif = Fraunces italic (public/fonts/Fraunces-Italic.woff2, loaded in
  WordCascade; used by WordCascade + KineticType). Premium editorial, not Georgia.
- footage.infocard {heading, body, at} = Nick info-card overlay (bold heading +
  body on dark top-scrim over facecam).
- desktopmockup scene: files[{name,kind:pdf|md|folder|zip}] + selected index →
  file icons w/ numbered Fraunces arrows, blue selection highlight on `selected`.
- uidialog scene: app/title/body/field/select/primary/cancel → clean app-modal
  recreation (NVIDIA-style green primary).
Test harness: src/beats/test-nick2.json (renders all six). Verified out/test-nick2.
NEXT: rebuild the Ideogram reel (Nick's own = Video-4582) on v2, compare side by
side. Build DesktopMockup/UIDialog into reels only when the topic calls for it.

## v3 ENGINE CAPABILITIES (2026-07-29 — theme-aware, USE THESE)

Beat sheets set `"style": "nick"` → every themed component switches to the
nick tokens automatically (cream #efe9dc, terracotta #E0785A accent, Fraunces
serif). New scene types + overlays (all in src/components/, wired into the
scene union):

- `chart` — brand-styled animated leaderboard/benchmark (bars fill staggered,
  count-ups, highlight row gets accent + serif badge). REPLACES raw
  leaderboard/table screenshots — never ship a raw chart screenshot again.
- `deviceframe` — screenshot/screen-rec inside macOS browser chrome (URL pill)
  or iPhone frame, blurred-self bg, push-in. For app/site demos.
- `terminal` — RENDERED macOS terminal with per-char typing, ✓/✗ output lines,
  trailing prompt. Replaces real terminal screen-recs (crisper + reusable).
- `annotatezoom` — the premium receipt treatment: card + camera-ease to focus
  + hand-drawn accent annotations (box/underline/circle/arrow) that draw on at
  cues. Prefer over plain `receipt` when specific phrases must be called out.
- overlays on ANY scene: `sprites` (animated pixel mascot — bob/hop/spin/walk;
  sample at public/assets/dev/mascot.png) and `burst` (seeded confetti/sparks
  for milestone/celebration beats — use sparingly, 1 per reel max).
- `logoassemble` — brand-logo assembly hook (reference: Google dots→G):
  the logo's SVG paths fly in staggered + spring-settle into the mark, with
  optional count-up label beneath ("15 NEW TOOLS"). Fetch any brand SVG free
  via `node tools/get_logo.mjs <name> [--index n]` (svgl.app; check the match
  list, monochrome fallback = simple-icons); paths embed into the beat, no
  runtime fetch. Use as the pre-hook logo beat or a tool-intro punctuation.
- mechanism beats: `python3 tools/manim_scene.py fanout|pipeline|versus
  --style nick --bg cream|black --out public/assets/<slug>/mg-<name>.mp4`
  → use as a footage scene. Brand-themed diagram animation (see tools/MANIM.md).

## Treatment history
- pubg-fable, ideogram (v4582 IS Nick's Ideogram reel — same one) used v1 pack:
  flat chips, static cards. Re-do future nick reels on v2 once components land.
- google-15 (5 of Google's 15 free AI tools — Pomelli/Stitch/Opal/Antigravity/
  Mixboard): FIRST nick reel on the v3 engine. BrandHook hook (giant "Google" +
  Pomelli campaign posters in window + serif + face card), numbered tool system
  (HeadlineBuild label "TOOL 0X · FREE" / bold name / italic tagline) over
  official-video floatcards (all @Google channels: Pomelli walkthrough, Stitch
  GfD, Opal GfD, Antigravity welcome), Mixboard = annotatezoom hero + browser
  deviceframe scroll, nick-display captions (ink on cream, amber keywords),
  confetti burst on "comment GOOGLE", bed-726 flat + sfx-nick pops. VibeVoice.
  Zero treatments repeated from google-free-ai-tools (no ToolStack/mockup/
  checklist/grids/wordcascade).
- google-free-ai-tools: official-product split hook, five-card paper ToolStack,
  presenter limit card, source-ingest desktop mockup, screenshot receipt zooms,
  prompt-to-app card, browser device frames, prompt-to-UI-to-code grid, Jules
  checklist plus daily-limit card, Flow model grid plus free-credit card, and
  cream WordCascade CTA. No generative b-roll; every product claim is paired
  with official Google or product documentation.
- astra (OpenAI Astra / ten proofs, comment-gate ASTRA, 45s, VibeVoice,
  FACE-LIGHT v1 — HeyGen connector absent in the session; avatar = v2 drop-in
  for hook/CTA): logoassemble OpenAI mark hook ("OPENAI · ASTRA"),
  annotatezoom receipts (vibemathed Gromov 1999/27y/Solved cascade, GitHub
  lean files, openai.com results w/ "$2,000 at Sol API rates"), NEW pdf
  page-flip montage (249-page manuscript at 13fps in portrait floatcard),
  official OpenAI chalk-animation window cropped from 4K coverage (credited
  OpenAI · via @TuringPost; ramsey/fanout/spherepack/triangle/annotate
  segments), manim fanout mechanism, compact 10-row Checklist (new
  stagger/compact props), cream typecard "CLOSED ALL TEN." (new kinetic
  scrim:false), deviceframe browser gh-repo, NEW lean-verify terminal
  (lake build ✓✓ 10/10), statcard THE BILL ($2,000/$200 bars), XPost MG
  (Bubeck, credited) over chalk bg, black+cream wordcascades, confetti CTA.
  No BrandHook (needs face), no black typecard, zero google-15/oss-alt
  treatment repeats.
- qwen-max v2 (SHIPPED — VibeVoice natural pace 49.75s, audio-driven avatar_iv
  16:9 face-x 0.43; brand-recognition rules applied): hook = BrandHook giant
  "Alibaba" + ANIMATED orange (#FF6A00) Alibaba smiley-'a' mark (new markColor
  prop) + Qwen glass-logo film window + face card; Jack Ma Ken Burns photo beat
  (WEF Davos, CC BY 2.0, orange tie + MA nameplate) at second 2; orange Alibaba
  logoassemble "OPEN WEIGHTS" punctuation before the HF deviceframe; closer =
  animated Qwen lockup from the 16-days film tail. VibeVoice hallucinated the
  CTA line + garbled "Qwen 3.8 Max" on first pass — regenerated those two
  sentences with phonetic respelling (Kwen) and spliced at word boundaries;
  whisper FIX map covers Ali Baba→Alibaba, it's quote→it scored, KWN→QWEN.
- qwen-max v1 (superseded by v2 — HeyGen TTS @1.2 + avatar_v; script
  hooks/retention per Aryan Anurag frameworks — excitement+outcome hook,
  expectation-payoff, forward flow): BrandHook (giant "Qwen 3.8" + official glass-logo film window + face
  card), official-wordmark nature footage (beach/mountain), logoassemble Qwen
  mark punctuation, floatcards over Alibaba Cloud launch-film vignettes
  (chips/protein/finance) + 16-day autonomous-coding film (editor timelapse,
  127-PRs board, app montage), black wordcascade benchmark card, big-serif
  "IT SCORED 86.6" cream wordcascade, chart x2 (bench leaderboard cream w/
  Qwen badge; API pricing black, no badge), facecam pops, deviceframe HF org
  page, terminal 27B download, annotatezoom Dataconomy claim (underlines),
  NEW manim VERSUS framed card ("FRONTIER LABS vs YOUR MACHINE"), facecam
  infocard CTA + confetti, punched-in official "Is Live Now" endcard.
  Number-duplicating scenes hide chips (one text system). No black typecard.
- oss-alt (OpenAlternative — "stop paying for AI tools", comment-gate OPEN,
  user-supplied storyboard): VibeVoice + audio-driven avatar_iv. 11 NEW bespoke
  scenes in src/components/OssAlt.tsx: osshook (STOP PAYING over facecam),
  notifstack (5 payment cards + wallet drain + red strike), strikeswap
  (PAID→OPEN-SOURCE on near-black), searchspotlight (real site footage + cyan
  outline + cursor dot + tick labels), stackwindows (5 mini browser windows
  zoom-out), problemsolved (red/cyan compare → check), walletattack (notif
  chips jump wallet on "attacking"), forkcustomize, selfhost, checkoutblock
  (UPGRADE $20/mo blocked by cyan card → trash), commentcta (type OPEN → grow
  → DM "Link sent ✓"). Real phone-shaped captures of openalternative.co (site
  identity hidden for the comment gate), light theme = cream-adjacent. Accent
  system: cyan #0aa9c2 (open/free) vs red #e0244a (paid) on nick tokens.
  Synth SFX (ffmpeg): pitched ding ×5, cash-reverse, keys, unlock, chime.
