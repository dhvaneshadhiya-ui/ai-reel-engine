# Style pack: editorial (DEFAULT)

> Renamed 2026-08-16 from `varun-mayya`. Style ids now describe the style,
> not its creator, so they read like formats do. Tech-news reporting:
> claim -> receipt -> demo -> take. Legacy ids (`varun-mayya`, `varun`)
> still resolve — see `STYLE_ALIASES` in `tools/reel_gates.py`.

Derived from forensic analysis of 11 reels (2026-07-22): contact sheets,
whisper transcripts, demucs stem separation, loudness measurement.

## Script voice
- DEEP script DNA lives in styles/editorial-script-playbook.md (hook taxonomy,
  6-act skeleton, connectives, honesty beat, CTA menu, binding rules) —
  the Script Director MUST load it alongside this pack.
- **160-215 words → 60-80s at speed 1.05** (user rules 2026-08-11 speed and
  2026-08-12 length; ~162 wpm MEASURED across three masters, 2026-08-13).
  Gate G02 blocks anything under 60s or over 80s, so write to this budget
  BEFORE building the beat sheet. script_approval.py now refuses to propose
  an out-of-band script.
  SUPERSEDED: '220-300 words' — assumed an unmeasured 3.2 wps and produced
  a 93.5s reel from a 242-word approved script.
  SUPERSEDED: '150-175 words → 45-55s at speed 1.2' (2026-07-23) — that
  target now lands under the 60s floor and fails the build.
- Hook = concrete shock stat/claim, first sentence, no throat-clearing:
  "X just dropped/discovered/revealed…", "X is in federal court right now"
- Short sentences, one idea each. "Anyways," as section pivot.
- Structure: hook → mechanism/context (2-3 beats) → "here's the part almost
  nobody noticed" bridge → biggest reveal → first-person founder take →
  CTA/prediction ("that excuse just got an expiry date") or comment-bait Q.
- Every factual claim gets a receipt; no receipt → facecam line or cut it.

## Scene grammar
- Split hook: footage top / facecam bottom, face on screen by second 2,
  captionBottom 1000. Hook footage must literally depict the hook line.
- Credibility loop: claim → receipt (highlight sweeps synced to VO) → demo →
  take. Receipts on cream or black card, drift + open-zoom near highlight.
- Talking head 10-20% total: hook bottom, bridge, personal take.
- Five b-roll classes: official press footage (credited @channel), screenshot
  receipts, concept motion graphics, AI-generated b-roll, community demo
  clips. Visual change every 2-3s, punch-in on every cut, alternating
  zoomDir, nothing static.
- Type: SF PRO ONLY (user brand rule 2026-07-29 — no serif families).
  SF Pro Display: Black/800 for display headlines, Bold caps for labels,
  Heavy Italic for accent lines; graphics adopt the SUBJECT's brand language
  when possible (Apple white / Kimi dark / Nothing dot-matrix).

## Captions (word-reveal — DEFAULT since 2026-07-30, user-mandated)
- captionStyle "word-reveal": BIG free-floating SF Pro text, NO pill.
  Connective words SF Pro Italic 700 @66px; emphasis keywords (numbers,
  prices, brands, verbs of value) SF Pro 900 @86px in accent. Words
  accumulate per-word as spoken; phrases hold through pauses (+0.9s cap).
  Deep soft shadow for legibility. Per-scene captionTheme:"dark" over cream
  card fields (ink text, amber #E8A200 accent) — captions must NEVER blend
  with the background. bottom 400 default / per-scene captionBottom.
- Emphasis list = single spoken tokens (match whisper words exactly).
- Legacy chip modes (chip-small/chip-lg) exist as fallback over busy footage
  only.

## Sound (measured: music+SFX layer ≈ -29 LUFS vs -14 mix = 15 LU under voice)
- Music bed ALWAYS, volume-automated 0.07-0.16: full at hook, duck through
  explanation, rise at reveal, up at CTA, fade out last 0.8s.
  Default track: music/bed-184.mp3 from=32 ("Vastness") for tech/serious.
- SFX 6-9 cues max, vols 0.11-0.18: riser under hook + impact on hook type
  land, tech-slide + pops on receipt highlights, one deep impact per major
  reveal, riser tail into CTA. Ordinary cuts are SILENT.
- Hook-vs-voice energy delta +1.5 to +4 dB. Master to -14 LUFS
  (loudnorm I=-14:TP=-1.2:LRA=7); target LRA ≈ 2.5-3.

## ENGINE CAPABILITIES v3 (2026-07-29 — theme-aware, USE THESE)

Beat sheets may set `"style": "editorial"` (default). New scene types (wired into
the scene union) + overlays — all pull the editorial tokens (cream #f4f0e6,
yellow #FFD84D accent, Fraunces serif) automatically:

- `chart` — brand-styled animated leaderboard/benchmark (staggered bar fills,
  count-ups, accent highlight row + serif badge). REPLACES raw leaderboard/
  table screenshots — never ship a raw chart screenshot again.
- `deviceframe` — screenshot/screen-rec in macOS browser chrome or iPhone
  frame, blurred-self bg fill, push-in. For app/site demos.
- `terminal` — RENDERED macOS terminal (typed commands, ✓/✗ lines, blinking
  prompt). Crisper than real terminal screen-recs and fully directable.
- `annotatezoom` — premium receipt treatment: card + camera-ease to the focus
  region + hand-drawn accent annotations (box/underline/circle/arrow) drawing
  on at cues. Prefer over plain `receipt` when calling out specific phrases.
- overlays on ANY scene: `sprites` (pixel mascot garnish) and `burst` (seeded
  confetti/sparks for milestone beats — max 1 per reel).
- `logoassemble` — brand-logo assembly hook (reference: Google dots→G):
  the logo's SVG paths fly in staggered + spring-settle into the mark, with
  optional count-up label beneath ("15 NEW TOOLS"). Fetch any brand SVG free
  via `node tools/get_logo.mjs <name> [--index n]` (svgl.app; check the match
  list, monochrome fallback = simple-icons); paths embed into the beat, no
  runtime fetch. Use as the pre-hook logo beat or a tool-intro punctuation.
- mechanism beats: `python3 tools/manim_scene.py fanout|pipeline|versus
  --style editorial --bg cream|black --out public/assets/<slug>/mg-<name>.mp4` →
  use as a footage scene (see tools/MANIM.md).

## Treatment history (append after each reel; never repeat consecutive)
- indiaai-gpu: split hook, cream receipts w/ highlights, black typecard x2,
  full-bleed footage w/ caps + serif overlays, facecam.
- kimi-india: split hook, cream receipts w/ highlights, black typecard x2,
  full-bleed footage w/ serif overlay, facecam.
- BAN in effect: plain black typecard (user called out repetition) — next
  editorial-style reel must use new treatments (type over footage, brand-matched
  cards, stat layouts, type inside receipts).
- record-skill (Anthropic "Record a Skill"): split hook (real Record-a-Skill UI
  top / avatar bottom), SEJ receipt w/ highlight sweep, official Anthropic Cowork
  b-roll (task prompt → autonomous build → analytics result) + the real feature UI
  (menu → dialog → saved) as full-bleed footage w/ caps, cream SERIF typecard +
  wordcascade for the "it broke" turn (NOT black typecard — ban respected),
  facecam take w/ infocard, serif reveal. HeyGen voice (VibeVoice quota out).

- iphone18-split (Apple skips iPhone 18 this year): split serif hook (17 Pro
  camera macro / face), Pegatron factory PHOTO floatcards x2 (building, gate)
  as supply-chain proof, annotatezoom on a MOBILE-width MacRumors capture x3
  regions (circle foldable "iPhone Ultra", underline 11->17 September streak,
  circle Ming-Chi Kuo) + MacRumors hero + AppleInsider headline/byline, NEW
  categorygrid as the two launch waves, timeline 3-stop rail (2019->2025->
  2027 MOVED accent), cream wordcascade (18/18e/Air 2), dark specsheet "The
  parts crunch" (Pegatron via AppleInsider footnote), NEW endquestion CTA
  card over the trio still, serif payoffs over molten/splash footage
  ("NO iPhone 18", "TWICE A YEAR"), facecam 17%. HeyGen avatar_iv master
  93.2s (allowLong, measured 2.55 wps), one 0.3s surgical audio cut.
  No black typecard, no sourceread, no logoassemble.

- september-preview (Sept 2026 event roundup): split hook (iPhone-amid-rods
  neon), numbered serif item labels 01-05 as the roundup spine, MacRumors
  mobile receipts as floatcard + FIVE sourceread passes (foldable x2, Ultra-4
  DigiTimes caveat x2 — "site isn't always accurate" underlined on screen),
  dark specsheet (18 Pro rumored rows), NEW statcard with REAL proportional
  bars (5.5" vs 7.8" screens), checklist (Ultra hardware), NEW uidialog x2
  (Reminders "New CEO takes over Sep 1", Calendar "Apple Event (rumored)
  Sep 8-9"), Apple Newsroom official floatcards (headline, Cook+Ternus
  photo, body para; headline re-shown on "isn't a rumor" as an earned
  receipt), serif punches ("THE CATCH?" over rugby dive pun, "+$300"),
  infocard "$2,000-$2,500" on face, cascades x2 (NO iPhone 18 -> March 2027;
  foldable? OR THE PRO?), face CTA. Facecam 19%. No annotatezoom /
  categorygrid / endquestion / timeline (all previous reel's). Master
  surgically shortened 86.2->79.8s.

- ios27-tiers (iOS 27's three-tier split): split hook (Liquid Glass "27" icon
  on cream / face), NEW `settingspane` (Settings > Appearance, spotlight on the
  "Liquid Glass" row — component built 2026-08-12, first ship), Apple's OWN
  device list as a full-frame receipt + 3 annotated regions (underline the
  "iPhone 15" row, the SE row, circle the 15 row), TWO TALL PORTRAIT footnote
  receipts mined for multiple focus rects (apple-notes 1080x2280 -> tier list /
  Apple Intelligence list / the iPhone 11 Pro Max testing footnote;
  9to5-notes 1080x2280 -> slower-pace conclusion / dropped-3-models / same-
  models-as-iOS-17), Apple official Siri-orb lock screen as a receipt, Apple's
  APPLE FOUNDATION MODELS radial diagram as a receipt, Apple Newsroom DMA
  headline receipt + annotated headline + annotated body, categorygrids x4
  (three tiers / 15-vs-15-Pro IN-OUT / Liquid Glass two-options-vs-slider /
  the removed variable), specsheets x3 (standard tier / Apple Foundation Models
  privacy / why iOS 26 trailed), statcard (30-70-80% with Apple footnote),
  chart (74% vs 76% with BOTH day counts on screen), cascades x5, facecam 15.4%
  in 7 pops. 50 scenes / 104.7s (allowLong). Digital twin, motion 5.68.
  No black typecard, no sourceread, no uidialog, no priceladder, no logoassemble.
- Used here, avoid repeating next reel: `settingspane` for a settings feature,
  the tall-footnote-receipt-mined-for-3-regions treatment, and the
  two-options-vs-continuous categorygrid.

## 2026-07-26 — premium bar (from a Varun reference reel, Codex Micro)
Reference showed the pack executed at a higher bar. RULES going forward:
- TITLES = editorial serif that BUILDS line-by-line (label → bold headline →
  italic subtitle), grey→ink colour reveal. Component: HeadlineBuild (Fraunces
  400/600 upright + italic). Reserve blocky condensed CAPS for rare punch only —
  serif is the default title voice now.
- FOOTAGE-FORWARD: lead with the most cinematic official footage FULL-BLEED and
  let it breathe; titles overlay it. Don't lean on cropped UI screenshots or MG
  cards as the backbone.
- SPEC-SHEET MG for "what it is / how it works": dark field, serif title, a few
  label→value rows revealing in sequence, ONE row in brand accent. Component:
  SpecSheet. (Replaces flat black typecards.)
- CAPTIONS: restrained — chip-small (38px) not the 56px sans. Footage does the
  talking; captions support, not shout.
- Match the SUBJECT's brand: Anthropic = cream + clay #d97757 accent + serif.
- record-skill treatment: split serif hook over Anthropic footage, SEJ receipt,
  real Record-a-Skill UI full-bleed w/ serif labels, black SpecSheet, cream serif
  card + wordcascade for the turn, facecam takes, serif CTA.
- nightborne (Blomkamp AI film): split serif hook (clone-army film shot / face),
  film-as-receipt motif — NIGHTBORNE title card, FEATURING cast wall (32 people)
  and A BARLEY STUDIOS PRODUCTION card as black floatcards; dark SpecSheet
  (Seedance 2.0 accent row); Kotaku roast receipt on black; serif-over-footage
  reveals (red cockpit "generated", night helis "a test", action "workstation");
  cream serif wordcascade (a crew/a location/months); wired-face finale.
  HeyGen voice. Premium serif register throughout.
- kimi-k3 (why it's viral + what people built): VibeVoice audio (clone) driving
  HeyGen avatar. Serif hook over a real Kimi 3D-world build; LMArena #1 leaderboard
  receipt; NEW XPost component = faithful credited tweet cards (real @handle + text
  + a giant serif STAT: "2 prompts" @kirillk_web3, "< $1" @soya_da_yoot, "27 min"
  @Fried_rice) over darkened real build footage; benchmark SpecSheet (Kimi K3
  9.5·3¢ accent vs Fable 5 7.5·38¢) attributed @CommandCodeAI; model-access footage
  for "open weights"; serif reveal. Honesty rule: card text = real claim, credited;
  never present other footage AS a specific person's exact build.
- kimi-k3 FEEDBACK (v1→v2): "why show text tweets? show what's BUILT." + "screens
  don't make sense." ROOT: I wrote the VO around 3 named X demos I had no footage
  of, so I fell back to messy tweet screen-grabs (X sidebar visible) + text cards.
  FIX: rewrote the VO to feature builds I had CLEAN footage of, regenerated
  VibeVoice+avatar, went full-bleed on real builds (3D world, FPS, Blender models
  showing Kimi $0.20 vs Fable $3.23), clean #1 leaderboard, benchmark SpecSheet.
  RULE: never script a claim you can't SHOW; footage-first, then write to it.
  Crop OUT app chrome (browser tabs, X sidebar) — a stray tab reads as a mistake.
- emergent (Bengaluru $130M unicorn + India talent): split serif hook (golden-hour
  Bengaluru drone / face, "BENGALURU -> $130,000,000 -> not San Francisco" build);
  emergent.sh live homepage receipt (tagline highlight); zoomed real prompt-box
  floatcard; Emergent's own mascot-agents promo full-bleed; NEW treatment = CNBC-TV18
  TV-graphic floatcards as proof ($1.5Bn Up-5x, 12M apps/70% bullets, production-ready
  bullet, founder Mukund Jha full-frame for "the building is happening here");
  TechCrunch green-hero receipt; FPJ 16%-talent receipt (composed clean card);
  India SpecSheet w/ units over blurred blr footage (16% accent); investor infocard
  on honesty beat; serif CTA over Bengaluru dusk ("quietly dissolving under your
  feet"). VibeVoice audio. No black typecard.
- model-wave (7 models / 7 days release week + Opus 5): split serif hook over
  Kimi 3D-world build; digitalapplied dark editorial receipt (headline zoom +
  composed clean stat-row crops for 5/7 and 3-vendor-claim cards); Kimi dark
  brand card AS spec footage; caps/serif spec overlay over FPS build footage;
  NEW TimelineCascade component (dated brand release cards sliding onto a
  vertical rail — Qwen's 72-hour triple); statcard price bars (TTS ⅓ ElevenLabs,
  Gemini $9→$7.50); Anthropic cream receipt w/ "half the price" highlight; dark
  SpecSheet w/ clay accent + SOTA badge over Anthropic ink-blot film; facecam
  act-break pops; serif CTA over Anthropic grid film. VibeVoice. SpecSheet
  hard-coded WINNER chip replaced by per-row optional `badge`.
- grok-voice (xAI Voice Agent Builder): split serif hook (number provisioning
  top / face), official @Grok launch-video clips as FRAMED cards (floatcard
  cream: create/number/wordmark/voices; deviceframe browser x.ai/voice:
  typing/kb/refund — framed-UI rule enforced, zero full-bleed UI crops), NEW
  manim pipeline floatcard (4-meter old stack), NEW annotatezoom receipts on
  the official post (underlines on "every hop adds cost", circle on $0.05/min
  + underline $0.01/min), NEW chart scene ($/min all-in: Grok $0.06 ★ vs
  ElevenLabs ~$0.08 vs OpenAI ~$0.10+, sourced), deviceframe scroll of the
  announcement, serif reveal over endcard ("expired July 1st"), facecam pops
  (mech setup, honesty, CTA). HeyGen TTS (VibeVoice quota out). Captured via
  tools/capture.mjs (3x receipts + scroll recording). No black typecard.
- india-claude (India = Claude's #2 market): FIRST editorial reel with the giant
  "#2" BrandHook (numeral instead of a brand name) over the real INR pricing
  page; TechCrunch green hero card as an annotatezoom receipt (underline on
  "biggest market after the US"); the 5.8% body-quote receipt (circle on the
  number + underline on "second-largest market"); NEW chart use for a social
  stat (ADP daily-AI-use: India 41% highlighted vs Nigeria 39 / Vietnam 36 /
  global 20); Anthropic INR pricing tiers zoomed with a circle on ₹2,000; 4K
  Bengaluru aerials (clouds/metro/dense city/sunset/L&T corridor) carrying the
  "we were downstream" personal beats; closer on an illuminated Indian flag at
  night. 25 scenes / 46s — zero pacing violations. VibeVoice with one sentence
  surgically cut (ChatGPT/OpenAI pronunciation flub, quota exhausted).
- kleo (Cameron Trew nerve story): FIRST reel through the Scout->Director
  pipeline — manifest written + every beat bound before scripting, zero
  missing-footage scramble. Absurd-image hook (33rd-floor flat -> childhood
  bedroom) over Canary Wharf drone + face; $62k Indie Hackers receipt; real Kleo
  app footage (credited @Kleo); "60,000 users -> cease & desist" cream cascade;
  Sold-out SpecSheet w/ column units ($59/500/4 days); honesty beat corrected the
  user's "solo" premise -> "he wasn't solo, 480k followers, one engineer" black
  cascade + infocard; "the tools got cheap / the nerve never did" serif over dusk
  London; VibeVoice audio. Emotional/founder story, not a product launch.
- made-by-google-26 (~2:15, allowLong per user request): split hook
  (family-lineup slide / face) — logoassemble streak broken; caps kinetic
  "MADE BY GOOGLE 2026" over drop-test lab as the title card; NEW
  `priceladder` ($799→$899 struck-through ladder x4 rows) for the price-hike
  honesty beat; specsheets x4, charts x2, statcards x3, cream+black
  wordcascades, promptcard, annotatezoom receipts x2 (blog.google pricing);
  Daniel Durant ASL live demo as a 3-shot floatcard run; facecam ~17% in 8
  pops. HeyGen voice measured ~148 wpm — budget 2.5 w/s. Ledger 2026-08-13.
- mac-mini-m6-m5pro (Mac mini M6/M5 Pro, framed as price-hike-vs-specs):
  split hook (Apple's own mac-mini page, real device + "From $899" / face);
  `priceladder` reused for a genuine two-hop price change ($599→$699→$899,
  two dated rows — see STYLE-RULES 2026-08-26 for why one row would have
  overstated it); five Apple Newsroom receipts + one Macworld headline
  receipt for the (outlet-reported, not Apple-stated) price-hike claim;
  honesty beat on unchanged 256GB storage; closing take moved AFTER the
  availability beat so the reel ends on payoff, not logistics. No music,
  no CTA (dropped post-review). 18 scenes / 75.4s / facecam 26.5% (news
  band exceeded deliberately — see STYLE-RULES). **Distilled the same
  session: `AnnotateZoom.focus` is SOURCE PIXELS, not a 0-1 fraction like
  `topFocusX` — read the component's own prop interface before reusing a
  sibling prop's convention, and pull a full-resolution frame after the
  first render of any new receipt before trusting a green gate run.**
