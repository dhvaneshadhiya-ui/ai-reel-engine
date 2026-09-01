# Reel feedback ledger — the dated history

> **Read [`RULES.md`](RULES.md) first.** It is the short, deduplicated,
> CURRENT rule set, and it says which rules are enforced by code
> (`tools/reel_gates.py`, `tools/lint_frames.py`) versus which need your eyes.
>
> This file is the **append-only ledger behind it**: what happened, on what
> date, and why each rule exists. It contains superseded entries by design —
> when the two disagree, RULES.md wins.
>
> **New feedback goes HERE** as *raw note → root cause → distilled rule*, then
> the rule graduates into RULES.md (with a gate + a case in
> `tools/test_gates.py` if it can be measured).

STRUCTURE: universal rules apply to every style; style-specific taste rules
and treatment history live in styles/<name>.md. Entries below dated per reel.
Styles available: varun-mayya (default), nick-saraev.

## 2026-08-14 — september-preview (Apple September event roundup)

### Retro (session close, 2026-08-14)

WENT RIGHT — keep doing:
- The critic toolchain caught every shipped-quality defect before delivery:
  A/B window verification killed 5 bad cuts pre-render, the sync table
  caught the ",000" caption fragments, the contact sheet confirmed labels,
  receipts and CTA. Nothing was caught by the user that we missed.
- Surgical audio editing is now a proven pattern (2 reels): sentence cuts
  and pause-tightening at silence boundaries fix length and TTS flubs for
  0 credits, verified by re-whisper. The 86.2->79.8s trim was inaudible.
- The propose-time length gate did its job on the top5 draft (caught 133
  words at ~49s vs the 26-48 band BEFORE generation).
- User feedback loop worked: format flip (top5->news), no-outlet-name rule
  and CTA rule were absorbed mid-build with zero credit waste.
- Packaging (social skill) and a no-music variant shipped same-session; the
  silent-bed variant sheet is the sanctioned mechanism for music-free
  exports (music block present and automated, bed = music/silence.mp3,
  disclosed to the user; the canonical reel keeps its bed).

CODIFIED THIS RETRO (now enforced):
- G30: orphan numeric caption fragment (",000"/".5") raises + self-test;
  the [.,-]digit merge loop is in build_template.py so new builds inherit.
- script_approval now estimates a RANGE (2.35-2.75 wps) and blocks when the
  SLOWEST measured pace overshoots the band. Safe news budget: 141-188
  words. september-preview's 203 words would have been blocked at propose.

RULES FOR THE NEXT REEL (EYE/workflow):
- Name probe frames with sequential indexes (q1..qN), NEVER raw timestamps
  — "b112.5.jpg" sorts before "b112.jpg" and that lexicographic trap
  produced a wrong shot map twice this session.
- Count needed footage slots from the region table BEFORE cutting and scout
  ~30% spare clips; this reel needed 4 rounds of clip-slot juggling because
  scripting outran the shot list.
- Prefer long single-shot product films over recap/montage sources: every
  montage cut here needed boundary surgery (~1s shot changes, baked-in
  display text, black flash frames).
- Punctuation is runtime: colons, dashes and rhetorical questions dropped
  this voice to 2.36 wps. Write punchy punctuation, budget for it.
- LEGACY NOTE: src/beats/iphone18-split.json (shipped 2026-08-13) fails the
  newer impact-cap rule (4 impact-role cues). Shipped reels are not
  retro-edited; if it is ever re-rendered, downgrade one cue first.

- **The voice's pace VARIES more than one measurement suggested: 2.36 wps on
  this master** (vs 2.55-2.72 on the previous three). A 203-word approved
  script ran 86.2s. FIX WITHOUT RE-RECORD: user approved cutting one
  editorial sentence + tightening 11 inter-sentence pauses to ~0.18s —
  surgical multi-cut brought the master to 79.8s, inside the band, splice
  inaudible (verified by re-whisper). RULE: plan scripts to the SLOWEST
  measured pace (2.4 wps ≈ 55s/80s = 132-192 words), and treat pause-heavy
  punctuation (colons, dashes, rhetorical questions) as runtime.
- **Whisper splits "$2,000" into "$2"+",000" and "5.5" into "5"+".5" — a
  bare ",000" or ".5" caption chip shipped to the first render.** RULE: the
  caption merge loop must join tokens starting with "-" AND `[.,]digit`
  into the previous token (timings kept). Fixed in build_septemberpreview;
  copy into every new build script alongside the hyphen merge.
- **User content rules (2026-08-14, binding for future reels):** (1) don't
  name the aggregator outlet in VO for non-exclusive stories — attribution
  lives in on-screen credits and "rumors say"/named-analyst mentions;
  (2) comment-gate CTAs don't fit news-preview topics — use the question
  CTA; (3) roundup topics get the news/varun treatment at ~60-80s, not
  top5, when the user wants per-item detail.
- **G29 (mobile capture) fired on two receipt crops that were technically
  landscape (wide-short paragraph crops).** RULE: crop receipts TALLER than
  wide even when the passage is short — include the section header.
- **The 1s-cut montage lesson generalizes:** five separate cut windows
  failed first/last-frame verification this reel (sort-order misread,
  +1.8s systematic offset, baked-in display text, black flash frames).
  The A/B check caught every one before render. It stays mandatory.

## 2026-08-13 — iphone18-split (Pegatron / split iPhone 18 launch)

### Retro (what to carry into the next reel)

WENT RIGHT — keep doing:
- Scout-before-script held: every beat was bound to a frame-verified asset,
  zero missing-footage scrambles, and the manifest's banned-timestamps list
  caught Watch/AirPods frames twice before they shipped.
- The critic pass caught three real defects the gates cannot see (payoff
  serif landing a scene early, receipt text too small, a cut opening on the
  wrong shot) — the sync table found the drift, the contact sheet found the
  rest. Both remain mandatory.
- Surgical audio cut + re-whisper fixed a TTS flub for 0 credits.
- Fix-the-engine-not-the-reel: stale validate_job.py rules were corrected in
  code instead of being bypassed.

CODIFIED FROM THIS REEL (now enforced, not prose):
- G28 orphan single-letter caption token (TTS artifact) + self-test.
- script_approval.py: WPS=2.7 measured; propose now EXITS 1 outside the
  60-80s band unless questions.md argues 'allowLong' to the user.
- Word budgets corrected to 160-215 in playbook / style pack / news format /
  config / skill.

NEXT REEL — do differently:
- Write to 160-215 words from the first draft; the propose gate will refuse
  anything else.
- Verify the START and END frame of every cut window, not one mid-frame.
- Capture text receipts at mobile width from the start.
- Treatments now used and not to be repeated next: categorygrid as launch
  waves, endquestion CTA card, 3-stop timeline rail, Pegatron-style photo
  floatcard pairs, "TWICE A YEAR"-style serif payoff over splash footage.

- **The word budget was fiction: approved 242-word script rendered 93.5s,
  17% over the 60-80s band.** ROOT: the "3.2 words/sec at speed 1.05"
  constant was never measured. Three real masters on this voice: grok-bot
  2.69 wps, apple-pay-india 2.72, iphone18-split 2.55.
  RULES: (1) `script_approval.py` WPS constant is now 2.7 — the propose
  step warns BEFORE credits are spent. (2) 60-80s = **160-215 words** on
  this voice; the playbook's 220-300 figure overshoots by ~30%.
  (3) This reel shipped at 93.2s under `allowLong` with the measured-pace
  reason on the sheet rather than cutting user-approved sentences without
  sign-off; a trim + re-record was offered at delivery.
- **TTS spoke a stray "T" after "Pegatron —"** (confirmed by base AND small
  whisper on the isolated slice, both hearing "Pegatron T"). ROOT: an
  em-dash straight after a proper noun can synthesize a consonant tail.
  RULE: scan the transcript for one-letter tokens after names; a 0.3s
  surgical cut of the master (video+audio, re-whisper afterwards) fixes it
  for free when the avatar is off-screen at that beat.
- **Desktop-width article capture = unreadable annotatezoom.** The 1000px
  MacRumors capture zoomed out to tiny text with 47-49% dead space in all
  three mr-body receipts. ROOT: the sourceread mobile-width rule applies to
  EVERY text receipt, not just sourceread.
  RULE: capture articles for annotatezoom at ~390px CSS, scale 3; grid the
  crop and read annotation coords off the grid.
- **A verified frame at one instant does not validate a cut window.** The
  event film's recap montage flickers products at ~1s (t134 AirPods, t135.5
  pastel fan, t136 Watch Ultra, t137 trio); ev-splash cut at t22 opened on
  the PRECEDING glass-rig shot before the phone appeared at t23.
  RULE: verify the START and END frames of every cut window, not one
  mid-frame; treat end-of-film recap montages as banned by default.
- **`scripts/validate_job.py` was still enforcing pre-2026-07-30 rules**
  (chip-lg captions, legacy manifest `items` schema) and blocked a
  gate-clean render. FIXED in code: it now reads the locked captionStyle
  from config.json and accepts the `assets` manifest schema. When a
  validator and a gate disagree, the gate (with its self-test) is the
  authority — but fix the validator, don't bypass it.

## 2026-08-12 — grok-bot USER FEEDBACK (8 items, all fixed forward)

User: "don't work on the same video again, just learn from it." Fixes landed in
the engine so the next reel inherits them.

1. **Avatar invented PENS in its hands** mid-gesture (~1:36). avatar_iv adds
   props unless forbidden. FIX: motionPrompt now says "hands hold nothing — no
   pen, no phone, no papers, no props". Scan the contact sheet for objects in
   the hands.
2. **Checklist rows ran flush to the frame edge.** FIX (Checklist.tsx): the
   column is width-capped at 860 and centred inside 96px side padding, so items
   sit in a proper margin however long the longest label is.
3. **Outro caption at the very top edge and plain.** FIX: outro type belongs at
   or just below CENTRE (y ~0.42-0.50). y=0.07 is for overlays on footage, not
   the closing card. RULES.md updated.
4. **Presenter appeared ~9s in.** The region structure put three opening
   visuals plus a receipt ahead of the split hook. NEW GATE G17: the presenter
   must be on screen within 5s, or the build fails.
5. **Footage credit was a bare unexplained name floating mid-field.** FIX
   (FloatingCard.tsx): renders "Source: X" (unless already prefixed), pinned
   directly under the card's bottom-left corner and left-aligned to the card.
6. **Motion graphics vanished before the VO finished the claim.** NEW GATE
   G18: a chart/specsheet/timeline/statcard must hold >=2.0s. The underlying
   discipline: anchor a data card's region on the LAST word of its claim, not
   the first.
7. **Expression was a fixed smile regardless of content.** FIX: motionPrompt
   now names the expression per section — neutral explaining, raised brows on
   the surprising figure, serious on the caveat, warm on the close.
8. **Wordcascade read flat.** FIX (WordCascade.tsx): per-word `accent` flag
   renders the punchline line in the accent colour (#C2410C on cream, #FFD84D
   on dark) for contrast. Also replaced Georgia with SF Pro — it had been
   breaching the SF-Pro-only rule since before this session.

Gate count now 18, self-test 21 cases, all firing.

## 2026-08-12 — grok-bot (first reel on the gesturing avatar + first sourceread)

- Avatar master measured **7.19 motion** on look 0aa05d6e via avatar_iv +
  expressiveness:high + motionPrompt — vs 0.48 for the same look on avatar_v.
  The gesture problem is fixed; hands are visible and moving through every
  facecam beat.
- **First production use of `sourceread`.** x.ai's announcement is the textbook
  YES case: official, text-dense, portrait after a mobile-width capture, and
  the VO quotes the lede verbatim so the marker tracks the exact words. Used
  twice — the lede, and a tint-shifted single-line sweep on the EARLY BETA
  badge. Captured at 400px CSS / scale 3 per the rule.
- **Cloudflare blocked the demo film on x.ai's CDN and it was NOT circumvented**
  (bot-detection bypass is off-limits). The same film is posted by @bot on X
  and yt-dlp fetches it normally — at 3840x2160, better than the site copy.
  RULE: when a CDN blocks, look for an official mirror the normal tools can
  reach; do not engineer around the block.
- LINTER FIX (real false positive): the DUPLICATE check hashed the FULL frame,
  so any two consecutive floatcards read as identical because they share the
  gradient surround by design. It now hashes the centre 72% — the content —
  and the two false pairs cleared while genuine ones still fire. Also added
  `sourceread` to the DESIGNED set for dead space; it is a typographic card,
  not footage, and was being held to the 30% footage threshold.
- Tier-1 source, so per the sourcing policy the claims are stated flat and
  attributed once ("x.ai · Aug 11"). Qualifying language is ~2% of runtime,
  inside the <=3% budget — versus 10% on apple-pay-india.

## 2026-08-12 — AVATAR SELECTION IS NOW MEASURED, AND PER-REEL

User: "use avatar 0aa05d6e as of now with gestures" + "it would be great if we
can change the avatar video to video and decide which avatar we want to use."

- The requested look is the one that measured FROZEN (0.48) on avatar_v. It is
  rescued by `avatar_iv` + `expressiveness:high` + `motionPrompt`: **6.01** —
  the highest of anything measured, above even the black hoodie's 5.32 on
  avatar_v. So the user can have the look they want AND gestures; the cost is
  Avatar V on that look.
- RULE: **the engine is a property of the LOOK, decided by measurement.**
  `expressiveness` is avatar_iv only; `motionPrompt` needs a digital twin on
  avatar_v. Some looks gesture natively on avatar_v (48d4076); some need the
  avatar_iv path (0aa05d6e). Store the winning engine alongside the look in
  `config.avatarRegistry` and never pick by preference.
- The 2026-08-11 "Avatar V always" lock is therefore SUPERSEDED by "whatever
  the measurement says for that look" — the user's real priority was gestures,
  and Avatar V was a proxy for it that turned out to be the wrong lever.
- TOOLING: `tools/measure_avatar.py` — `score` (measure), `--register`,
  `list` (registry, best-moving first), `use <id>` (switch default; refuses a
  frozen look). Per-reel override: `"avatar": "<id>"` in the reel manifest.

## 2026-08-12 — AVATAR GESTURES: measured, and my diagnosis was wrong twice

User: "the Avatar is hardly having any gestures, no hand movement" — then sent
a prior video from another project where the same account DOES gesture.

- **My first diagnosis was wrong.** I claimed the group lacked a `digital_twin`
  so Avatar V rendered from a still image. But the gesture video uses look
  `48d407621ae64e4ba7dcfb63635f45e8` — a `photo_avatar` in the SAME Dhvanesh
  group, which has no twin, and it gestures. I had over-generalised one API
  error ("motion_prompt requires a reference look") into "no motion is
  possible", and skipped the clause where a photo avatar falls back to
  *curated public studio looks* as its animation reference.
  I sent the user off to record a 15s Digital Twin they did not need. Do not
  ship a confident causal claim off a single error message.

- **The measurement.** Three 6.3s clips, identical script, mean frame-to-frame
  luminance delta in the hand region (lower 560px):

  | look | engine | mean | peak |
  |---|---|---|---|
  | 0aa05d6e blue hoodie | avatar_v, no prompt | **0.54** | 0.98 |
  | 48d4076 black hoodie | avatar_v, no prompt | **3.46** | 7.16 |
  | 48d4076 black hoodie | avatar_iv + expressiveness:high + motionPrompt | **6.74** | 17.25 |

- **RULE: the LOOK is the dominant variable, worth ~6.4x. The engine/prompt
  path is worth a further ~2x.** Two looks of the same person, same engine,
  same parameters, differ by more than six times in movement. Pick the look by
  measuring, not by how the still photo reads — the blue-hoodie still looks
  perfectly good and animates almost not at all.
  PROCEDURE for a new look: render one ~6s clip, crop the hand region, take the
  mean consecutive-frame delta. Under ~1.0 is a frozen presenter; 3+ moves.

- Avatar V stays locked (user rule). `expressiveness` is avatar_iv ONLY
  (rejected on avatar_v) and `motionPrompt` needs a twin on avatar_v — so on
  Avatar V the gestures have to come from the look, which is exactly what the
  measurement says they do.

## 2026-08-11 — SOURCE READ-ALONG + NOTATION (user, binding)

**1. New scene type `sourceread` — the source document, highlighted live.**
Reference supplied by the user (highlightscreenshot.mp4): a long-form article
full-bleed in portrait, with a mint marker sweeping the exact sentence as the
voice-over reaches it, highlights ACCUMULATING so the frame shows how far the
read has got. Built as `src/components/SourceRead.tsx`. Marker uses
`mixBlendMode: multiply` so the words stay readable THROUGH it — a solid fill
would cover the very text being proved. `follow: true` scrolls a page taller
than the frame to keep the active line at ~58%.

WHEN TO USE IT — this is judgement, and the wrong call makes a wall of small
text, which the engine already has rules against:
  - YES: a text-dense, portrait-friendly artefact (article body, paper,
    filing, changelog, docs page) where the VO closely tracks the passage AND
    the claim is load-bearing enough to be worth proving on screen.
  - NO: a wide screenshot (`floatcard`), an image-led page, a passage the VO
    only loosely paraphrases, or a claim nobody would dispute.
  - CAPTURE AT MOBILE WIDTH (~390-400 CSS px, scale 3). A desktop capture
    gives a 2.5:1+ text column that cannot work in 9:16; a mobile capture
    wraps the same prose into a tall narrow column that does.
  - Verified in practice: the Business Today news page was a BAD fit (short,
    ad-broken, wide) while Apple's own support page was a good one (long,
    ad-free prose). Same session, same topic — the artefact decides, not the
    story.

**2. Standard visual notation for every number on screen.**
"Normalize all numbers, model names, money, dates, percentages, units,
versions, and technical terms into standard visual notation." Built as
`tools/notation.py`, ENFORCED by G16 across captions AND authored card text.
Two layers, because only one of them is allowed to invent:
  - LAYER 1 mechanical (always safe): joins whisper's split decimals
    ("23 .2" -> 23.2), attaches % ("85 %" -> 85%), moves currency to its
    symbol ("30 trillion rupees" -> ₹30 trillion), makes ranges ("15 to 20"
    -> 15-20), multipliers ("three point five times" -> 3.5x). It only
    re-renders digits that were already spoken; it cannot introduce a fact.
  - LAYER 2 canonical (per-reel, VERIFIED): product names and official
    capitalisation come from a `notation` map in that reel's manifest.json —
    spellings the scout actually saw. There is deliberately NO global product
    dictionary, because the user's rule is "use official capitalisation
    exactly as verified in the source material; do not invent punctuation,
    model versions, prices, or abbreviations". A global guess table would
    happily invent `GPT-5.4` for a source that wrote `GPT 5.4`.

  TWO TRAPS, both hit and both fixed:
  - **Normalise BEFORE chunking, not after.** Notation spans word boundaries
    and the caption chunker cuts straight through it: "nearly 30 trillion" /
    "rupees." and "It wants 15" / "to 20 basis" shipped un-normalised because
    each chunk could not see the other half. `normalise_words()` merges at
    token level while the words are still adjacent, keeping the first token's
    start time.
  - **A bare "one" is an article, not a datum.** The first pass turned the
    spec-sheet title "In one month" into "In 1 month". Spelled cardinals now
    convert only when a unit follows AND the value is not a bare 1 — unless a
    scale word follows, so "one billion tokens" -> "1 billion tokens" still
    works. Over-normalising is its own failure mode.

## 2026-08-11 — SOURCING POLICY (user, binding — supersedes the hedging habit)

- **"Most news about Apple or any company is sort of rumour, and many turn out
  true. We rely on trusted sources and/or who reported it. We have to make the
  video no matter what the topic is, using our system. We can give credit to
  the sources we use."**
  ROOT CAUSE of the correction: on apple-pay-india I treated "unconfirmed" as a
  risk to be managed with volume. Measured: **10.1s of a 100.8s reel (10%) was
  spent qualifying**, and beats 46-49 were 8.2 CONSECUTIVE seconds making the
  same point three ways — a facecam caveat, a three-line wordcascade of
  negations, and a receipt card reading "this is reporting" — on top of
  "reportedly" in the hook, a "STILL UNCONFIRMED by Apple" card, and "Reported"
  on the thumbnail. That is not rigour, it is a tic, and it signals the channel
  does not trust its own sourcing.

  **THE POLICY:**
  1. **Sourcing quality is a FRAMING DIAL, never a gate.** It changes HOW a
     claim is said, never WHETHER the video gets made. The pipeline does not
     refuse or stall on a topic because it is pre-announcement.
  2. **Attribution replaces hedging.** Name who reported it — once, clearly,
     early — then state the substance with confidence. One attribution beat
     does the work that three caveat beats were doing badly.
  3. **Credit every source we use, on screen.** ENFORCED: G14 (borrowed
     footage carries `credit`) and G15 (any card showing a number carries
     `source`/`footnote`). Both have self-test cases. G15 immediately caught a
     "who pays the fee" spec sheet shipping with no attribution.
  4. Budget: aim for **<=3% of runtime** on qualifying language, not 10%.

  **The tiers (how loud the attribution is, not whether we publish):**
  official -> state flat; named reporting with a track record (Bloomberg /
  Gurman, Reuters, Business Standard citing people familiar) -> attribute once
  then state directly, this is journalism not rumour; track-record analyst
  (Kuo) -> attribute + flag as forecast; aggregator recycling a tier-2 story ->
  never cite, go to the original; anonymous account with no history -> can
  still cover it, framed as "X claims", credited. **No source at all is not a
  rumour, it is absent** — there is nobody to credit, so there is nothing to
  put on screen (this is what killed "supports offline payments").

- **Weight claims by TYPE, not just by source.** Inside ONE sourced article the
  details are not equally solid, and most coverage gets this backwards:
  - **Mechanisms and specific figures are the firmest** — "15-20 bps vs 10"
    came FROM the sourcing; that granularity is what insiders actually know.
  - **Dates are the softest** — "by October" is a target and targets slip.
  Lead on the mechanism, treat the date lightly. The mechanism is the durable
  claim; the date is the one that ages badly.

## 2026-08-11 — apple-pay-india v1 → v2 (USER FEEDBACK: visuals out of sync)

- **"What's going on the screen doesn't look in sync with the script and what
  the creator is saying."** Correct, and the cause was a fix I made for a
  different problem. To clear the G04 pacing ceilings I replaced semantic
  anchors with an EVEN TIME SPLIT, but left the visuals in a fixed order — so
  each visual landed wherever a clock boundary fell, not where its content was
  spoken. The data cards drifted 2-3 beats late: the security spec sheet played
  over "not at launch", the 85% chart over "billion transactions", the
  interchange chart over "doesn't come from you".
  ROOT CAUSE: pacing and sync were treated as one problem with one lever.
  They are two constraints and need two mechanisms.
  RULE (universal, blocking): **cuts anchor to the words the visual is ABOUT.**
  Never distribute beats by clock time. When a region is too long for one
  visual, subdivide it with MORE VISUALS THAT BELONG TO THAT SAME REGION —
  never by borrowing the neighbouring region's visual. `region_bounds()` in
  `tools/build_applepay.py` is the reference implementation: each anchor phrase
  owns a list of visuals and its span is divided among them.
  COROLLARIES:
  - Put a region's most SPECIFIC visual LAST in its list, so the card carrying
    the number lands on the words saying the number ("Who owns the volume"
    lands on "of India's digital payments", not on "which matters because").
  - A region can only carry as many visuals as it has time for. `region_bounds`
    now drops extras rather than emitting a sub-0.6s flash (one Apple Watch
    beat came out at 0.45s and read as a glitch).
  - Budget: 100s at ~1.8s/beat is ~56 beats, needing ~35 distinct clips plus
    ~10 MG cards. Scout for that BEFORE scripting; the shortfall is what
    pushed v1 into borrowing visuals across regions in the first place.
- **VERIFY SYNC EXPLICITLY, it is not visible on a contact sheet.** A sheet
  shows plausible frames in a plausible order and hides drift completely. Print
  a table of `scene -> time window -> the caption words spoken in that window`
  and read it. That table is what exposed all ten mismatches in seconds, after
  the sheet had looked fine to me twice.
- Two `[DUPLICATE]` flags were real: `su-nfc` next to `su-terminal` (two
  contactless glyphs back to back) and two consecutive facecam beats, which
  read as one long block against the facecam-in-pops rule. The linter caught
  both; trust it over the eye on near-identical frames.
- Mastering: single-pass AND two-pass `loudnorm` both landed -15.2 LUFS because
  the true-peak ceiling was binding (input LRA 4.0, so linear gain hit TP
  before it hit target). A light `acompressor` + `alimiter` BEFORE `loudnorm`
  got it to -14.6 LUFS / -1.1 dBTP. Use that chain when loudnorm undershoots.

## 2026-08-11 — apple-pay-india (first reel built under the gates)

The gates and the frame linter caught four things the eye missed. All four are
now enforced, not written down.

- **NEW GATE G13: a clip must be at least as long as the beat that plays it.**
  A short clip does not fail loudly — it runs past its own end and the frame
  holds, or spills into whatever the SOURCE cut to next. Here a 1.65s clip on a
  2.3s beat dragged the Apple ad's next title card into frame with its text
  cropped ("ount on Apple Pa"). Invisible in logs; caught on the contact sheet.
  Cut every clip with headroom above the pacing ceiling (>=2.8s).
- **Hand-picked semantic anchors produce unusable pacing on a long reel.**
  On a 100s / 44-beat reel they gave spans from 0.72s to 4.28s — ten broke G04
  while the short ones wasted beats. FIX: `even_bounds()` in
  `tools/build_applepay.py` splits the VO into equal spans, snapping to word
  ends and preferring clause endings, with a hard 2.55s ceiling so no span can
  break pacing whatever scene type it becomes. Copy that function; do not
  hand-place 40+ anchors.
- **A very wide screenshot cannot use the `receipt` treatment.** ReceiptScene
  zooms to the union of its highlights with a Z floor of 1.35, so a 3.27:1
  artifact overflows the 1080 frame and cuts the headline mid-word ("e Pay is
  coming to India..."). RULE: artifacts wider than ~2.5:1 go in a `floatcard`
  at their true aspect, framed whole, with a display headline above. Reserve
  `receipt` (with its zoom+sweep) for artifacts nearer portrait.
- **UI footage vs live-action decides the treatment, and it is checkable on
  frames.** The Apple ad is photographic and survived a 9:16 centre crop; the
  Apple Support video is device mockups centred in 16:9 and a 9:16 crop cut
  card numbers and menu labels mid-word. Same topic, same session, opposite
  treatments. Always test-crop one frame per source before cutting the batch.

Process notes:
- The brief's bullet list contained a claim ("supports offline payments") that
  NO source supported. It was cut and recorded in the manifest's
  `explicitly_NOT_claimed`. A second bullet ("UPI yet to be confirmed") was
  weaker than the reporting, which says UPI is absent at launch AND why — that
  absence became the reel's spine. Always re-verify a supplied bullet list;
  the correction usually makes the stronger reel.
- TTS dropped the "-er" from "countered" and BOTH whisper base and small heard
  "counted", so the slip was in the audio, not the transcription. Rather than
  regenerate 100s of avatar for one word, the caption FIX map and the on-screen
  chart both carry the correct word. Documented, not hidden.

## 2026-08-11 — seedance-25 v1 → v2 (USER FEEDBACK — all binding)

Reel was approved ("looks amazing, almost everything is perfect") with five
corrections. These override every earlier entry they touch.

- **"We need to slow down the speed a little bit."** v1 ran HeyGen voice
  speed 1.2 (the 2026-07-23 PUBG-pace preference).
  RULE: default voice speed is **1.05** for all reels, both styles. This
  SUPERSEDES the 2026-07-23 "default all new reels to speed 1.2" entry — that
  line is dead. Set in `config.json.avatar.voiceSpeed`. Delivery at 1.05 is
  ~3.2 words/sec; use that to convert a target runtime into a word count.
- **"Video length must be between 1-2 minutes based on the topic and script."**
  v1 was 47.6s.
  RULE: every reel runs **60-120s**, and the length is CHOSEN FROM THE TOPIC —
  how much the story actually has to say — not padded to hit a number. A thin
  story gets 60s; a dense launch with several verified mechanisms earns 120s.
  This supersedes every earlier 26-48s / ~42s / ~56s target. Enforced in
  `scripts/new_job.py` (clamp now 60-120) and `config.json.defaults`.
  Consequence to plan for: a 90s reel needs ~40-45 beats and roughly twice the
  scouted footage — budget the scout accordingly instead of stretching shots.
- **"Need to improve caption style in the outro."** The outro label read
  "THIRTY SECONDS. ONE PASS. WITH SOUND." — 37 characters at the label's fixed
  46px uppercase + letterSpacing 2, which overflows 1080px, wraps, and orphans
  "SOUND." on its own line. The question below it was one flat white block.
  RULES (universal, all display type):
  - A `label` line is **≤30 characters** — it does not auto-fit and a wrap
    orphans a word. Use "·" separators to compress ("30 sec · one pass · with
    sound"). Count the characters before shipping.
  - The closing question SPLITS across two `headline` lines with the payoff
    half carrying `accent: true`, so the outro has the same two-voice
    hierarchy as the captions instead of one even block.
  - A 3-line outro block anchors at **y ≈ 0.07**, not 0.10 — at 0.10 the last
    line grazes the presenter's hairline. Verify on the actual last frame.
- **"Make sure to choose Avatar V."** Already correct in v1 — but lock it in:
  RULE: `engine: {"type": "avatar_v"}` on every `create_video_from_avatar`
  call. Never `avatar_iv`/`avatar_iii`. GOTCHA: the API rejects `motionPrompt`
  together with `avatar_v` when the avatar's group has no digital twin
  ("motion_prompt requires a reference look"). The fix is to DROP
  `motionPrompt` — never downgrade the engine to keep the prompt.
- **The `news-reel` skill pointed at the wrong repo.** It targeted
  `~/AI Videos/reel-engine` and described that engine's `pipeline/make.mjs`
  workflow, which does not exist here.
  RULE: the skill now points at `/Users/dhvaneshadhiya/Movies/ai-reel-engine`
  and documents THIS pipeline (build_<slug>.py → register_beats → remotion
  render → loudnorm → lint). Two engines exist; never mix their commands.

## 2026-08-11 — seedance-25 (engine defects found during the critic pass)

Not user feedback — four blocking defects caught by the mandatory frame review.
All four were invisible in render logs; only extracted frames exposed them.

- **BrandHook overflows on long product names.** `titleSize` is hardcoded
  188px (with mark) / 232px (without) with `whiteSpace: pre` and no auto-fit.
  A 12-char title ("SEEDANCE 2.5") ran ~1250px wide in a 1080px frame: the
  word was clipped at BOTH edges and the flex row pushed the brand mark
  entirely off-frame, so the logo silently never appeared.
  RULE: BrandHook's `title` is limited to **~6 uppercase characters with a
  mark, ~7 without**. Longer subject names do NOT get BrandHook — use
  `logoassemble` (household mark, animated) for the first beat and a `split`
  for the next so the face still lands by second 2. Never widen the engine to
  fit a name; the treatment changes, not the component.
- **A module-scope `loadFont()` blocks EVERY composition.** `InstaCTA.tsx`
  called `loadFont({family:"Fraunces"})` at import time; Root imports it, so
  its `delayRender` ran on unrelated reels and killed the render ~3 frames in
  with a font timeout. It was also dead code — the SF-Pro-only rule already
  points every theme serif token at the SF Pro stack. Removed.
  RULE: never call `loadFont()` at module scope in a file Root imports. If a
  render dies on "Loading font …", look for a font load in a composition the
  reel does not even use.
- **Screen-recording sources hide a PiP webcam in stills too.** The scout
  correctly measured the creator PiP at x 89-357 / y 714-960 and every 9:16
  video crop cleared it — but the keynote STILL was extracted as a full
  1920x1080 frame and shipped the PiP straight into a floatcard.
  RULE: the PiP-exclusion crop applies to **stills as well as clips**. When a
  wide slide must keep all its text, crop the BOTTOM band away (here
  1920x648, aspect 2.963) rather than the side — cropping the side cut the
  slide's own wordmark mid-word, which is its own hard fail.
- **zsh `$VAR` inside `-filter_complex`/`-vf` silently empties** (already
  logged 2026-07-27 for filtergraphs) — it bit again on a `drawtext` label
  built from a shell var. Inline the whole filter, and keep `text='…'`
  single-quoted *inside* the double-quoted `-vf`.

Process notes that worked and should be repeated:
- Whisper `base` misspelling a product name is NOT evidence of a TTS
  mispronunciation. `base` wrote "Seedense" and "bite dance"; re-running
  whisper **small** on the two 2s slices returned "C-Dance" and "Bite Dance"
  — both phonetically correct, so no regeneration was needed. Always confirm
  a suspected mispronunciation on a slice with a bigger model before spending
  credits on a re-record.
- Data screens that BUILD (specsheet rows, chart bars, timeline items landing
  in sequence) are the documented exemption to the 2s pacing rule and were
  gated at 3.3s; pure footage at 2.9s; every other card at 2.6s. The build
  script now enforces this itself and refuses to be "OK" without it.
- Claims the sources do NOT support get written into the manifest as an
  explicit `explicitly_NOT_claimed` block with the banned source timestamps.
  Here: Seedance 2.5's 4K. The on-stage 4K cards belong to Seedance **2.0**;
  frames 563s/566-602s were banned from the reel to stop a plausible-looking
  but unsupported claim leaking in via b-roll.

## 2026-08-06 — qwen-max v1 → v2 (voice default + brand recognition)

- **"I wanted to use vibe voice"** — v1 shipped with HeyGen TTS per the
  2026-07-29 canonical policy. User re-confirmed VibeVoice as their preference.
  RULE: VibeVoice (voice-sample-ref clone) is the DEFAULT voice for all reels again;
  HeyGen native TTS is the FALLBACK (Space down / quota). This supersedes the
  2026-07-29 "HeyGen TTS default" line. Avatar = audio-driven avatar_iv from
  the VibeVoice track.
- **"Throughout the reel focus on branding elements recognizable by viewers —
  Alibaba original logo, Jack Ma's photo — people know these so they instantly
  relate; showing them ANIMATED in the beginning helps a lot"** — v1 led with
  the Qwen sub-brand (mark + wordmark films), which most viewers don't know.
  RULES (universal):
  - Every reel anchors on the most HOUSEHOLD-RECOGNIZABLE brand assets: the
    parent company's official logo in its brand colors, and, when the story is
    company-scale, the famous founder/CEO's face (properly licensed photo,
    credited). Recognition beats abstraction — a sub-brand mark supports, never
    replaces, the household brand.
  - These anchors appear ANIMATED inside the first 2-3 seconds (draw-on/
    assemble/pan-zoom photo card), and brand touches recur through the reel
    (logo on charts/cards, brand color accents), not just at the hook.

## GOVERNING RULE (2026-07-23, read before EVERY reel — no exceptions)

- EVERY reel is built in exactly ONE of two styles: varun-mayya or nick-saraev,
  strictly per that style pack. Never invent a third look.
- If the user names a style, use it. If the user names NO style, DEFAULT to
  varun-mayya.
- A REFERENCE REEL the user gives supplies the TOPIC (and which of the two
  styles best fits) ONLY. NEVER copy the reference's visual style, layout,
  fonts, or effects — rebuild the topic in our varun or nick pack. The ONLY
  exception is if the user EXPLICITLY says "use these visuals / copy this look".
- VOICE is the ONLY thing that changed with VibeVoice. Visuals, scene grammar,
  sound design, captions, pacing, treatment history — all unchanged, still
  driven entirely by the two style packs and the universal rules here.

## UNIVERSAL PACING RULE (2026-07-31 — BLOCKING, applies to BOTH styles)

User (angry, repeated feedback): "the first frame with face at bottom and a
different block on top shouldn't be there for more than 2 seconds… we can't
afford static screens for more than 2 seconds. Instagram retention is low —
keep showing people something new." google-15 held its hook layout 6.4s.

- NO layout/composition persists longer than ~2s. This includes the hook
  split/BrandHook (face visible by s1, gone or replaced by s2), typecards,
  logo beats, charts, annotatezoom holds, any designed card.
- "It animates internally" is NOT an exemption for held layouts — micro
  -motion (push-ins, springs, count-ups, camera ease) does not count as a
  scene change. Only genuinely moving FOOTAGE/screen-recordings may run
  2.5-4s, and even those target a cut every 2-2.5s when the VO allows.
- Long VO sentences get SPLIT across 2-3 distinct visuals, always.
- ENFORCEMENT: tools/lint_frames.py flags scene 0 if >2.2s and any
  non-footage scene >2.6s ([PACING] flags). A build with PACING flags on the
  hook does not ship.

## UNIVERSAL DENSITY + INTENSITY RULES (2026-07-31 — BLOCKING, both styles)

User: "why are you limiting yourself to limited footage? content is limitless
on the internet… when I say 'brand's whole social campaign' you show one
boring screen — nothing matching the intensity of the words." Plus a
meaningless filler frame (dark mid-scroll page section) shipped unverified.

- ASSET DENSITY: every tool/claim gets MULTIPLE visuals — the scout gathers
  3-5 usable shots per subject (official videos are long: mine several
  segments, punch-in crops of 4K sources count as extra shots; credited
  creator demos allowed). One-clip-per-tool beats are BANNED. Long beats
  (>2.5s) become 2-3 rapid sub-shots.
- INTENSITY MATCHING: the visual must match the SCALE of the words. Plural/
  totalizing words ("whole campaign", "everything", "15 tools", "unlimited")
  demand plural visuals: walls/grids of creatives, rapid montages, stacked
  results — never a single static screen. Say-big show-big.
- ONE CLIP PER BEAT: a source clip may carry only ONE footage beat in a reel.
  Reusing the same shot at a different `from` offset still reads as "same
  footage again and again" (india-claude v1: 6 clips across 11 beats). Cut a
  DISTINCT shot for every slot — a 3-5 min aerial/demo source holds 15-20
  separable locations; mine them. ENFORCED: lint_frames.py [CLIP REUSE] flag,
  blocking.
- EVERY scene's source range is frame-verified AT ITS EXACT in/out points
  before it enters the beat sheet. "It's from the right page" is not
  verification — the pomelli-scroll filler fail. No unverified filler, ever.

Every entry: date, reel, the raw feedback, root cause, distilled rule.
Rules here override SKILL.md. Never repeat a mistake recorded here.

## 2026-07-29 — grok-voice v1 → v2 (hook composition)

- **"Black text overlapping the dark background in the first 3 seconds; the
  first-3s visuals aren't pleasing"** — hook split put dark serif headline
  over the number-provisioning clip's dark/orange gradient regions.
  RULE (hardens the existing legibility rule): the HOOK headline never sits
  on footage at all — hook display type goes on a CLEAN light/cream field.
  Legibility check at the landing frame is BLOCKING for the hook beat.
- **"The subject brand (xAI) must be LARGE — it's the center of attraction."**
  User supplied Nick's hook frame as the target composition: giant brand/
  product name on cream, the tool's real screen in a floating window under
  it, one italic serif line, face in a rounded bottom card.
  ENGINE: new `brandhook` scene (BrandHook.tsx, theme-aware) = title (huge
  serif brand name) + subtitle caps + framed media window (video) + italic
  serif line + rounded facecam card. USE THIS as the default varun/nick hook
  for product-launch reels; chips auto-hidden (hideCaptions default in beat).
- Liked: SFX selection and overall visuals — keep the current sound recipe.
- Process: avatar + VO reuse across visual revisions (no regeneration needed
  when only scene composition changes).
- **v5 → v6: "captions are boring and not large enough — I want Nick's
  caption style"** — measured teardown of Nick's caption system across the 12
  reference reels (2026-07-30): BIG free-floating text (~66-86px at 1080w),
  NO pill by default, deep soft drop shadow carries legibility; TWO VOICES
  mixed inside one phrase — connective words italic, the KEY word lands
  HEAVIER + BIGGER; words accumulate as spoken (per-word reveal, not
  chip-swap); keyword gets an accent color; pill only as fallback over busy
  footage. ENGINE (permanent): captionStyle "nick-display" in CaptionChips —
  per-word reveal times in beats captions[].words, emphasis list drives the
  heavy+accent keyword, per-scene `captionTheme: dark` flips white→ink over
  cream fields (accent shifts to amber #E8A200 on light bg so it never
  blends), phrases hold through VO pauses (+0.9s cap). SF Pro Italic plays
  the italic voice per the SF-Pro-only rule. DEFAULT for all reels;
  chip modes remain as legacy fallback.
- **v3 → v4: "use SF Pro only, all type"** — the brand font is SF Pro
  (Display), every variation (weight/italic) at the director's discretion.
  ENGINE (permanent): theme `serif` tokens for BOTH styles now point to the
  SF Pro stack; HeadlineBuild/KineticType hardcoded Fraunces removed; display
  weights bumped (800 headlines) since SF Pro reads lighter than a serif.
  RULE: no Fraunces/Georgia/serif families in any reel — SF Pro
  everywhere (chips were already SF Pro).
- **v3 → v4: "too much empty white space around the framed screens — Nick
  fills it with large text"** (user pointed at 3-22s framed cards + 25s
  receipts; praised the chart's title block at 34s as the model).
  RULE: every framed-card scene (floatcard / deviceframe / annotatezoom)
  carries a BIG display headline in the empty field above the card (label +
  headline kinds, y≈0.10, theme dark on cream) — 2-5 punchy words stating the
  beat's claim, NOT verbatim VO (≤1 shared significant word keeps the karaoke
  chips alive; duplicating numbers like "80+ voices · 25 languages" is the
  exception where chips auto-hide). White space is a canvas, never blank.
- **v2 → v3: "text is getting cut in the browser windows (multiple screens)"**
  — DeviceFrame's browser media area was hardcoded 940x1050 (portrait);
  16:9 clips under objectFit:cover lost ~half their width ("ue_refund",
  "Thank y"). ENGINE FIX (permanent): media area now follows the source
  aspect — VIDEO sources default to a 16:9 window (full frame, zero crop),
  page screenshots keep the tall reading pane; `mediaAspect` prop overrides.
  RULE: a framed clip must show its FULL source frame — if a device window
  and its media have different aspects, the WINDOW adapts, never the media.

## 2026-07-22 — indiaai-gpu v1 → v2

- **"My face is not in the center"** — root cause: HeyGen 9:16 auto-crop.
  HISTORICAL RULE (superseded by the 2026-07-29 connector policy below):
  generate avatar 16:9 + crop ourselves with measured face-x.
- **"Varun's first 2 seconds include the face"** — RULE: hook is always a
  split screen (footage top / facecam bottom) or full facecam. Face visible
  by second 2, always.
- **"Captions bigger + styled"** — RULE: 56px+, extra-bold, solid black pill.
- **"Key pointers highlighted"** — RULE: numbers/prices/brands in yellow
  #FFD84D at 1.22em inside chips (emphasis list in beat sheet).
- **"Static screens feel dead"** — RULE: every scene moves (punch-in on cut,
  receipts open zoomed near the highlight and settle, alternating zoomDir).
- **Liked**: minister/launch-event footage, official b-roll. Keep sourcing
  real event footage for government/company stories.

## 2026-07-22 — indiaai-gpu v2 → v3 (Varun-style audio rebuild)

- **"The audio is shit, sound effects are pathetic"** — root cause: whoosh on
  every cut at ~5 LU under voice, no music bed. Demucs analysis of Varun's
  reels: bed always present ~15 LU under voice with energy curve (hook full →
  duck mid → rise at reveal/CTA); SFX sparse (riser into hook, 2-4 impacts at
  act breaks, pops on highlights) and deep/cinematic, not zippy.
  VARUN-PACK RULES (Nick levels are defined in `styles/nick-saraev.md`):
  - Music bed in every reel, volume-automated (0.07-0.16), never flat.
  - Max 6-9 SFX cues per reel; silent ordinary cuts.
  - SFX vols 0.11-0.18; hook-vs-voice energy delta ≤ +4 dB.
  - Master the final file to -14 LUFS (loudnorm), verify with ebur128.
- **"Captions cover the face in the beginning"** — RULE: split-hook scenes set
  captionBottom≈1000 (seam); any facecam scene must keep chips off the face.

## 2026-07-22 — kimi-india (noted, no re-render requested)

- **"The screen you're showing doesn't match what I'm talking about"** — hook
  top showed a macOS Finder recreation while VO said "a frontier AI model goes
  up for free download". Topically adjacent ≠ visually matching.
  RULE: the hook visual must LITERALLY depict the hook line — the product's
  recognizable UI/logo, the announcement itself, or the named subject. A
  generic demo clip fails even if it came from the right ecosystem. Test:
  would a viewer with the sound off name the subject from the hook frame?
- **"FREE FRONTIER AI is white and overlapping with the white background"** —
  white caps type sat over a white Finder window.
  RULE: display type must be legibility-checked against its actual backdrop
  in the verification pass (extract the frame AT the type's landing moment).
  Engine now draws a dark radial scrim behind KineticType over footage, but
  still prefer footage moments with dark/quiet regions at the type position.
- **"You used the same black-screen-with-text frame in both reels — find new
  ways to present information in every reel"** — the plain black serif
  typecard appeared in indiaai-gpu (₹67 vs ₹330, ₹/$) AND kimi-india
  (Hindi·Tamil·Kannada, ₹/$).
  RULES:
  - Never reuse a scene treatment the previous reel used for the same kind of
    information, unless the user has explicitly blessed it as a template.
  - Plain black typecard = fallback of last resort, max once per reel.
  - Prefer varied treatments per reel: type over footage (scrim handles
    legibility), brand-matched cards in the subject's design language (Varun
    does Kimi-dark / Apple-white / Nothing dot-matrix), stat/comparison
    layouts, type inside receipts, split text+footage.
  - Log each reel's treatments in the "Treatment history" list below and
    check it before building the next beat sheet.

## 2026-07-28 — emergent v1 → v2 (retention pacing teardown)

- **"Face should be there in the beginning for only 2 seconds, then change the
  screen, and keep changing screens every 2-3 seconds — Instagram retention is
  very low."** — v1 held the split hook (face on screen) for 7.2s and had a
  6.0s facecam take + 4.4s single floatcard mid-reel.
  RULES (varun style, all future reels):
  - Hook split (face visible) lasts ~2s MAX; the rest of the hook line gets its
    own visuals.
  - NO scene longer than ~3s unless it animates internally (specsheet rows,
    receipt highlight sweeps); target average visual change every 2-2.5s.
  - Long VO beats (personal takes, CTAs) get SPLIT across 2-3 distinct visuals
    even when the voice is one continuous thought.
  - Facecam returns mid-reel in 1.5-3s pops, never one long block.
- **"I never asked you to use the kleo reel or anything from it."** — I cloned
  kleo's build script + treatment flow and cited it in the delivery summary.
  RULE: engine components are shared, but each reel's treatment choices must be
  derived fresh from ITS manifest — never presented or reasoned as "like the
  previous reel". Never name other reels in user-facing summaries.

## Treatment history (check before every new reel)

- indiaai-gpu: split hook, cream receipts w/ highlights, BLACK TYPECARD x2,
  full-bleed footage w/ caps + serif overlays, facecam.
- kimi-india: split hook, cream receipts w/ highlights, BLACK TYPECARD x2,
  full-bleed footage w/ serif overlay, facecam.
- ibm-rehiring: split hook (IBM building top / face bottom), full-bleed
  footage w/ caps overlay, CREAM typecards x2 (new — replaced black), facecam
  bridges, cream receipts w/ highlights (Toms + Forbes). No black typecard. ✓
- model-wave: split serif hook (Kimi 3D-world / face), dark editorial receipt
  (digitalapplied) w/ headline + composed clean stat-row crops, Kimi dark brand
  spec-card AS footage, spec overlays over build footage, NEW TimelineCascade
  (dated brand cards on a rail — Qwen 72h triple), statcard price bars (TTS ⅓,
  $9→$7.50), cream Anthropic receipt w/ half-price highlight, dark SpecSheet
  (clay accent, SOTA badge) over ink-blot brand motion, facecam pops, serif CTA
  over Anthropic grid film. No black typecard. VibeVoice (2 surgical VO cuts —
  see rule below).
- seedance-25: logoassemble hook (TikTok mark, pink on cream) → split hook
  (jellyfish / face, serif product name), full-bleed generation footage,
  wide-band keynote floatcard (aspect 2.963), NEW dated `timeline` on a
  paramedics bed, NEW `chart` with count-up bars (15→30 sec), two specsheets
  with column headers + units, NEW `comparesplit` carrying a LANGUAGE PAIR
  (English / 日本語, same source shot), cream wordcascade for the honesty
  beat, facecam pops (18%). No black typecard. No BrandHook (see defect
  above). HeyGen TTS on the cloned voice, speed 1.2.
- grok-bot: logoassemble hook (Grok mark on cream), split hook, NEW
  `sourceread` read-along on the official announcement (x2 — lede + badge),
  16 framed 16:9 floatcards for the launch film's UI shots, full-bleed
  live-action, pricing chart, two checklists, two specsheets, cream
  wordcascade of open questions, facecam 14% WITH gestures.
- apple-pay-india: logoassemble hook (Apple mark on cream), split hook,
  full-bleed live-action ad footage, 17 framed 16:9 floatcards for UI,
  NEW checklist for regulatory preconditions, two charts (share + the bps
  fight), three specsheets with units, two cream wordcascades, wide
  screenshot as a floatcard (not a receipt), facecam 19%.
- ios27-tiers: split hook (Liquid Glass "27" / face), NEW `settingspane`
  (first ship), Apple's own device list as receipt + 3 annotated regions, TWO
  tall portrait footnote receipts each mined for 3 focus rects, Apple Siri-orb
  lock screen, Apple Foundation Models radial, Apple Newsroom DMA receipt x3
  framings, categorygrid x4, specsheet x3, statcard, chart (74/76% with both
  day counts), cascades x5, facecam 15.4%. 50 scenes / 104.7s allowLong.
- → next reel must introduce at least one new treatment and avoid the plain
  black typecard entirely. Already used and not to be repeated next:
  `settingspane` for a settings feature, and the tall-receipt-mined-for-three-
  regions annotatezoom run. Already used and not to be repeated next: the
  language-pair comparesplit and the count-up duration chart.


## 2026-07-23 — ibm-rehiring (varun style, natural-audio test)

- UNIVERSAL: whisper splits hyphenated words into a token + a "-suffix" token
  ("re-staff"->"re","-staff"; "entry-level"->"entry","-level"). Caption
  builders MUST merge any token starting with "-" into the previous token
  before chunking, else a chip reads a bare fragment ("re"). Merge loop now in
  build_ibm.py — copy it into every new build script.
- UNIVERSAL: render reels with `--concurrency=2 --timeout=120000`. Default 4x
  hits "delayRender timed out" when a reel reuses the avatar master at many
  offsets + b-roll + 2 audio tracks (single frames render fine → parallel
  load, not content). Also keep public/ lean (move raw .mkv/.webm to
  _sources/, delete diagnostic PNGs) — Remotion copies all of public/.
- **"whenever you highlight text, zoom in on that part too — at 0:24 there's
  a lot of words on screen"** — receipts showed the whole page so highlighted
  phrases got lost. ReceiptScene now does a STEADY per-scene focus: frames the
  union of that scene's highlights big + centered (fit ~88% width / ~55%
  height, Z clamp 1.35-2.2) and HOLDS it the whole scene with a gentle
  push-in (earlier per-highlight keyframes wrongly RELEASED the zoom mid-scene
  — don't do that). Highlight boxes still sweep on at their cue. UNIVERSAL,
  applies to both styles. (Speed later set to 1.2 — see pace-preference entry
  below; this reel's 1.05 is superseded.)
- Audio naturalness: speed 1.05 (was 1.15-1.2) reads far more human; the
  speed-up was the main "sounds AI" tell. Well-known acronyms (IBM/HR/AI) read
  fluid in TTS; only niche ones (PUBG) need phonetic spelling. create_speech
  audio-only endpoint needs a separate 'api' credit pool the Creator plan
  lacks — cheapest pronunciation test is a short 720p avatar clip.

## 2026-07-23 — pace preference (applies to all upcoming reels)

- **"use the same pace we used for the pubg reel for upcoming videos"** — PUBG
  ran at HeyGen speed 1.2. RULE: default all new reels (both styles) to
  speed 1.2, overriding the earlier 1.05 natural-audio experiment. User
  prefers the punchier pace over maximum naturalness.

## POD reel — "the result is shit" (major structural teardown)

- **NEVER open on a document / browser / file bin / black / loading screen.**
  Open on the STRONGEST shot of the finished result (the AI ad hero frame),
  full-bleed 9:16, push-in + impact. v1 opened on the business-plan doc — hard
  fail. RULE: cold-open on the payoff, then rewind to the process.
- **Rebuild tiny source UI as big motion graphics.** Do not expect the viewer to
  read a screen recording. AI category lists → 2x2 CategoryGrid cards with a
  select animation (fade others 20%, centre, scale 125%, cyan outline, ✓).
  Design gallery → numbered (01-05) Carousel that swipes and lands on the winner
  with SELECTED ✓. Prompts → clean full-screen PromptCard with the spoken
  keywords highlighted in cyan pills, + shimmer loader cards.
- **Let the result breathe.** The 7s payoff ad plays clean — no captions, no MG,
  no "better direction" graphic over the product; music raised. Save the
  design-vs-ad comparison + BETTER DIRECTION → BETTER OUTPUT + "WOULD YOU RUN
  THIS AD?" for AFTER the clean watch.
- **Source-F extraction:** the AI ad lived inside the screen recording. The
  clean copy (no player chrome, no facecam PiP) is only in the "reveal" window —
  crop=606:1080:985:0 from ad.webm t≈16.4-24 (=exact 9:16). The player-playback
  copy has controls + PiP baked in; don't use it.
- New reusable components: PromptCard, CategoryGrid, Carousel, Checklist,
  CompareSplit (src/components/). Beat builder: tools/build_pod2.py.
- **Audio caveat:** VibeVoice ZeroGPU reserves a fixed 90s block per call, so a
  short line can't be generated when <90s quota remains (resets ~daily). Reused
  existing vo-A/vo-B; the exact "40 seconds earlier / didn't exist" hook line is
  a pending 2-min swap once quota resets.

## POD reel v3 — "too slow, tighten to 36-38s" (pace revision)

- **Reel length = audio length.** Faster visual cuts alone don't shorten a reel;
  the VO track sets the floor. To speed up WITHOUT re-recording: tools/tighten_vo.py
  rebuilds the VO from word timings — caps every inter-word pause at 0.11s and
  applies a pitch-preserved atempo. Emits matching word-time JSON so captions stay
  synced (no whisper neede/available). 1.20x + pause-cap took 47s -> 39s naturally.
- **Decouple visual pacing from VO anchoring for J-cuts.** v3 uses FIXED per-scene
  durations (not VO-end anchors) so the design reveal can run 5s while the next VO
  sentence starts underneath. Captions track the VO independently.
- New components: DesignReveal (full-screen sequential, numbered, winner held +
  SELECTED ✓), HCompare (horizontal top-design/bottom-ad, cyan matching boxes +
  connecting line, sequential banners), EndQuestion (ad freeze + YES/NO, avatar
  region reserved). Builder: tools/build_pod3.py.
- **Give the payoff room:** most static screens <=1.5s, but reallocate ~5s to the
  design reveal (the winner gets ~2x hold) and keep the 7s ad clean.
- **Continuity note:** the clean full-frame section-F ad wears "JUGAAD EXPERT"
  while the selected design is "JUGAAD ZINDABAD" (the ZINDABAD ad only exists with
  player chrome). User locked both assets, so the compare boxes are thematic, not
  pixel-identical.
- STILL PENDING (same two unlocks): new opening line "This product advertisement
  didn't exist 40 seconds ago" + HeyGen avatar hook/ending. Layouts are built for
  a clean drop-in.

## 2026-07-27 — nightborne v1 → v2 (film-over-black cards)

- **"Instead of black background, play movie scenes behind the text"** — applies
  to SpecSheet, title cards, credits/names screens. RULES:
  - SpecSheet now takes bgSrc/bgFrom: film footage behind a top-dark gradient
    scrim (0.34→0.82). Never ship a solid-black spec screen when footage exists.
  - Real credit text (titles, cast walls, production cards) gets COMPOSITED over
    footage: crop the white-on-black text region from the source, lumakey the
    black away, overlay on a darkened (eq brightness -0.10..-0.22) 9:16 crop of a
    DARK scene. Never retype real people's names — reuse the film's own pixels.
  - ffmpeg gotcha: `blend=screen` on 10-bit VP9 gives magenta chroma; use
    format=yuv420p + lumakey + overlay instead.
  - zsh gotcha: $VAR expansion inside -filter_complex silently emptied → "No
    such filter: ''" AND the old output file survives (looks like the change
    "didn't take"). Inline the full filtergraph in single quotes.
  - Pick TEXT BEDS by darkness: explosions/night scenes carry white credits;
    white lab coats kill them. Keep the bed scene distinct from other beats
    (don't reuse the finale shot). Watch caption-chip vs composited-text
    collisions — set captionBottom to clear the wordmark.

## 2026-07-29 — model-wave (VibeVoice date flub, process rule)

- VibeVoice mispronounced a spoken DATE ("July 17th" → "July 7th" + a garbled
  artifact phrase) — caught only because whisper was cross-checked at 3 model
  sizes on the suspect slice. RULES:
  - After generating VO, whisper-check every NUMBER and DATE in the transcript
    against the script before rendering the avatar-driven master; re-verify
    suspicious slices with whisper small/medium.
  - Fix strategy when the face is OFF-SCREEN at the flub: surgically cut the
    span from BOTH streams of the avatar master (identical trim windows), then
    re-whisper the trimmed master for caption timings. Prefer cutting a
    dispensable spoken phrase over regenerating (dates can live on-screen).
  - Caption FIX maps operate on CHIP text (post-chunking) — multi-word fixes
    must be written per-chip; verify the fix landed in the beats JSON, not
    just the FIX dict.

## 2026-07-29 — kimi-k3 full review ("visuals too basic" — composition teardown)

User compared the kimi-k3 render against Nick Saraev's 12 reference reels
frame-by-frame. The gap was NOT assets — it was compositing rules. Five root
causes, each now a UNIVERSAL rule + engine fix:

- **ONE TEXT SYSTEM AT A TIME.** kimi-k3 showed "a first-person shooter that
  actually plays" in big serif AND "shooter that actually" in the karaoke chip
  simultaneously — same words twice. ENGINE FIX (permanent): Reel.tsx now
  auto-hides CaptionChips during typecard/wordcascade scenes and any scene with
  a kinetic overlay (`hideCaptions` per-scene override exists; explicit `false`
  forces chips back on). RULE: display type and karaoke chips never co-exist;
  headline overlays may run with chips ONLY when their words differ from the
  concurrent VO.
- **Display type never sits on busy content.** Big serif was stamped over game
  footage and over a white card ("run it yourself" white-on-white, eyebrow line
  overlapping the logo card). The references CUT to a dedicated designed card
  (cream/black, one phrase, push-in) instead. RULE: every beat is exactly one
  of (a) face + chips, (b) full-bleed footage + chips only, (c) designed card
  with no chips. Type-over-footage only via KineticType's scrim on a QUIET
  region, verified at the landing frame.
- **Highlights must never obscure data.** The Arena receipt's highlight used a
  white difference-blend box that inverted the Kimi row into a black bar —
  hiding the exact data being highlighted. ENGINE FIX (permanent):
  ReceiptScene dark backdrops now draw a stroked accent box + faint tint
  around the region (cream keeps yellow multiply marker). RULE: highlight goes
  AROUND data (stroke/underline), never over it.
- **Screenshots are never full-bleed raw.** The Arena chart ran full-bleed,
  low-res, cropped mid-letter ("ontend Code Arena"), with a blurred smear
  filling the top half. RULE: capture receipts at deviceScaleFactor 2-3,
  always card-framed (rounded + shadow on styled fill), zoom via transform to
  the region of interest so edges never cut words. Frame edges must not crop
  text mid-word — check in critic pass (lint tool flags it).
- **No per-scene palette drift.** Green game world → navy chart → black cards
  read as unrelated slides. RULE: every scene pulls bg/accent/type from the
  active style pack's tokens only (varun: cream/black + yellow #FFD84D accent,
  Fraunces serif; nick: cream/black + orange, per pack). Screenshot card
  backdrops included.
- **NEW TOOL (mandatory in STEP 6): `tools/lint_frames.py <slug>`** — extracts
  labeled per-scene stills + contact sheets into out/<slug>-lint/ and
  auto-flags dead space >30%, near-duplicate consecutive scenes, edge-cropped
  text, and double-text risks. Run it BEFORE the vision critic pass; review
  its sheets against the checklist it prints.

## 2026-07-28 — kleo/kimi v2 (dark space + walls of text)

- **"Too much dark space, we can't keep it dark"** — ReceiptScene floated a
  small card on flat black. FIX (component-level, permanent): ReceiptScene now
  renders a blurred, enlarged copy of the receipt itself as a full-frame fill
  behind the card (cream: bright blur; black: darkened blur). No scene should
  ever show flat empty backdrop around a small asset.
- **"Wall of text, getting cut, unprofessional"** — blowing up document/app UI
  to full-bleed 9:16 turns it into cropped text walls. RULE: screen-recordings
  of documents/apps are shown as FRAMED 16:9 floatcards (bg gradient) with the
  serif headline above — never full-bleed unless the content is visual (games,
  film, product motion). Crop the window region (excluding any presenter PiP)
  at its native aspect.
- Receipt crops must contain ONLY the artifact: re-check edges for leftover
  app chrome (kimi arena had residual X-sidebar pixels at x<560).

## 2026-07-29 — canonical automated presenter policy

- The connected HeyGen video connector requires an explicit `9:16` aspect for
  portrait reels. This supersedes the older unconditional 16:9 instruction
  above for calls made through that connector. Always inspect a calibration
  frame; if the automatic framing is poor, show the portrait master with
  `contain`/fit or in a split/card treatment instead of cropping out the face.
- Native HeyGen TTS with the configured creator voice is the default because it
  produces the most reliable lip sync. VibeVoice is opt-in only.
- The canonical file is `public/assets/<slug>/avatar-master.mp4`.
- For Nick-style reels, the universal 6–9 SFX cap wins: place tiny clicks/pops
  only on meaningful landings and leave ordinary cuts silent.
- Production order is scout/manifest first, then script and shot plan, then
  presenter generation. Do not generate paid media before the story has
  verified visual coverage.

## 2026-08-04 — astra v1 → v2 (diagram crop, washed statcard, hook dead space)

- **"From :10 to :13 I can see arrows but not the whole diagram — it's
  getting cut"** — the 16:9 manim fanout ran full-bleed in the 9:16 frame,
  cover-crop ate the diagram's sides. RULE (universal): a 16:9 mechanism/
  diagram render NEVER runs full-bleed in a portrait reel — frame it
  (floatcard/deviceframe, full source frame visible) with a display headline
  filling the field above, or regenerate the diagram at 9:16. Wide diagrams
  are composition-critical; footage-style cover-crop only suits photographic
  b-roll where the subject survives a center crop.
- **"Screen at 0:34 — I get the price but the background is pathetic"** —
  StatCard floated a small white card on flat cream; read washed-out/empty.
  RULE (nick style): money/comparison beats use the full-frame `chart`
  treatment (brand-styled, animated bars + count-ups, title block) or a
  statcard placed over a rich field with a display headline — never a lone
  small card on an empty page-colored background.
- **"Screen around :39 doesn't make sense with what I'm speaking"** — an
  abstract chalk-triangle filler carried the "when someone tells you AI only
  remixes… remember" take. RULE: opinion/take/address-the-viewer lines are
  FACECAM beats (or the claim's receipt) — never decorative filler. If no
  face exists yet, use the receipt of the claim being countered, not
  unrelated texture.
- **"OpenAI logo with huge blank space under it — use large captions to
  cover it"** (reference: Nick hook = logo + tool window + big italic serif
  + face card, every band filled) — the v1 logoassemble hook left the lower
  60% empty with small chips. RULE (hardens BrandHook default): hook and any
  logo beat must fill the vertical: mark + window/media + LARGE display
  caption + face card. If a band would sit empty, put big type in it —
  blank space in the first 2s is a hard fail.
- **v2 → v3: "first 2-3 seconds look like a still screen — use OpenAI's
  official logo, animate it, things should be moving, add text animations"**
  — BrandHook's springs all settled by ~0.7s and the window held a static
  screenshot. ENGINE (permanent, BrandHook.tsx): official brand mark (svgl
  paths) draw-on stroke → fill with spin settle + perpetual slow rotation;
  per-letter title stagger; subtitle tracking-in; serif line pops word-by-
  word (numbers auto-accent amber) + underline sweep; window gets continuous
  push-in and, for still images, a slow pan. RULE (universal): in any hook
  scene the motion must NEVER fully settle — stagger entrances across the
  full beat and give every still asset a continuous camera move; brand marks
  are ANIMATED (draw/assemble), never pasted static.
- Process: HeyGen connector appeared mid-session → avatar generated
  audio-driven from the existing VibeVoice track (16:9 1080p, face-x 0.43),
  dropped into brandhook hook + "remember" take + CTA without touching VO or
  captions. HAS_FACE branch in build_astra.py keeps both variants buildable.

## 2026-08-03 — oss-alt v1 → v2 (tool-name montage + tail trim)

- **"When you start saying tool names (Claude Code, Cursor…) just show their
  animated logos or dashboards"** — v1 cut to each tool's alternatives-page
  scroll during the name montage; at 0.4-0.8s per name those read as walls of
  text. RULE: when the VO merely NAMES tools in rapid succession, show the
  brand MARK (logoassemble) or a recognizable dashboard hero — never a
  text-heavy page. Results-page footage belongs to the beats that talk about
  the results themselves. svgl note: gradient (`url(#…)`) fills strip out —
  drop those layers and keep solid+white paths (canva = purple circle + C);
  tint `currentColor` marks with theme ink or cream per bg.
- **"When you finish speaking the reel goes on while the face is still — cut
  that out"** — v1 held the CTA end-card 1.5s past VO end, freezing the
  avatar's last frame behind it. RULE: reel ends ≤0.3-0.4s after the final
  spoken word; land the end-card BEFORE the VO ends (shift dropAt earlier),
  never hold on a frozen face. Avatar master ends ~0.2s after VO — any scene
  time past that is a freeze.

## 2026-08-12 — feedback #1 and #7 verified by probe, not by assertion

Method note first: both of these were shipped last round as "prompt-side,
unverified." HeyGen Pro (436 credits) makes a ~3-credit probe cheap enough
that **no prompt-side claim gets recorded as fixed until a clip proves it.**
That is the rule going forward — probe, then write the ledger entry.

- **#1 props in hands — FIXED, verified.** Probe `be34b663` (11.5s), sampled
  every 0.4s = 28 frames, hand region cropped and tiled. Every frame bare
  hands: open palms, clasped, counting. The explicit ban ("hands hold nothing
  at any point — no pen, no phone, no papers, no props of any kind") holds.
  RULE: that sentence stays verbatim in every motionPrompt. Verify it the
  same way — a hand-region crop strip at ≤0.5s spacing, not the contact
  sheet, which is too coarse to catch a pen (the 1:36 pen was invisible in
  the grok-bot sheet).
- **#7 expression tracks the script — NOT FIXED by prompting.** Same probe,
  three registers in one 11.5s script. Face read: 1.4s figure → smiling;
  5.0s "does not explain credential handling" → smiling with crinkled eyes;
  **7.4s "or permission scope" → broad open-mouth grin, the most cheerful
  frame in the clip on the most serious line**; 10.6s closing question →
  neutral. Near-inverted. `motionPrompt` steers the HANDS but does not steer
  the FACE. `expressiveness` is one dial for the whole generation, so a
  per-section instruction inside the prompt has nothing to bind to.
  CONSEQUENCE: expression is a SEGMENTATION problem, not a prompting problem
  — see below.

### Why #7 is not a prompting problem — the two probes

- Probe B `5492c2c0`, same caveat sentence, `expressiveness: low`, motionPrompt
  saying "no smiling at any point, brows slightly drawn, mouth neutral":
  **still smiling**, and motion collapsed 6.90 → **1.02 (stiff)**.
  FINDING: `expressiveness` is a MOVEMENT-AMPLITUDE dial, not an emotional
  register. Turning it down costs the gestures and buys nothing on the face.
  RULE: never lower expressiveness to chase a serious face — it trades away
  the one thing that was working.
- Root cause, from the asset itself: look `0aa05d6e` is named
  **"Smiling podcaster in blue hoodie"**, `avatar_type: photo_avatar`. A photo
  avatar is a deformation of ONE still image; if that still is a smile, every
  frame is a smile. There is no neutral face in the model to reach. No prompt
  and no dial can add one.
  RULE (general): for a photo avatar, **the source photo's expression is the
  floor.** Check `get_avatar_look().name` / preview before adopting a look —
  a look whose auto-generated name begins "Smiling" cannot carry a caveat.

### What actually works: the look IS the expression control

- Probe C `31699b25`, same caveat sentence, look `7123b3d0` (neutral source
  still), `expressiveness: high`: **level brows, no grin, mouth neutral except
  for speech — and motion 2.97, still gesturing.** Same person, same voice.
  PROVEN: register is selected by LOOK, not by prompt or dial.
- REGISTRY now carries `register` per look: `0aa05d6e` = **warm**,
  `7123b3d0` = **serious**, `48d4076` = unmeasured (do not use where tone
  matters). Enforced by **G19**: a sheet declaring `tone` must carry a
  matching `avatarRegister`, so a caveat script can no longer ship on the
  smiling face. Four self-test cases.
- CONSTRAINT: the two looks differ in wardrobe AND background (blue hoodie /
  dark acoustic panels vs grey sweater / blue-green desk). Checked all 21
  looks in the group — there is no wardrobe-matched neutral twin. So the rule
  is ONE LOOK PER REEL, chosen by the reel's dominant register. Do not cut
  between registers inside a reel; it reads as two different shoots.
- Within a reel, the tone the face cannot carry is carried by the channels we
  DO control: caption weight and colour, music bed level, SFX choice, palette,
  and word choice. The face is one channel of several, not the only one.
- OPEN, and now correctly diagnosed: true per-sentence expression needs a
  DIGITAL TWIN driven by real footage. That is the one thing a twin genuinely
  buys. NOTE the earlier error — a twin was previously claimed necessary for
  GESTURES, and measurement disproved that. Do not re-open the twin question
  for anything except expression range.

## 2026-08-12 (2) — bullet marks, story length, caption truth, render gate

- **"Why is there a question icon in the bulleting"** — root cause was the
  TYPE, not the component: `rows[].state` allowed only `done | q`, so an
  EXCLUSION list ("Who does NOT get it": Free Grok / Standard SuperGrok /
  Cursor Pro) had no way to say "excluded" and fell back to `q`. A "?" tells
  the viewer WE DO NOT KNOW — a weaker and different claim than "these are
  excluded", so the screen contradicted the script. FIX: added `state: "no"`
  (rust ✗). RULE: `q` means genuinely unconfirmed, NEVER "excluded".
- Checklist.tsx rebuilt: marks are now stroked SVG paths that draw on with the
  row (no typed "?"/"✓" glyphs, no font dependency, consistent stroke weight);
  each row sits on a soft plate so labels stay legible over the gradient on a
  phone; headline + rows are ONE flow-centred column, so the group is optically
  centred instead of the headline pinning to the top with a dead gap below.
  Emphasis pulse now only applies when a list MIXES states — highlighting every
  row highlights nothing.
- **[GATE] G20 — every list row must land AND be readable.** Found by maths,
  not by eye: grok-bot scene 49 held 5 rows at stagger 0.55 in a 2.04s scene,
  so the last row entered at 2.45s — **the "iOS" row never appeared at all,
  while the voiceover was already saying "Linux, and iOS."** The gate requires
  `0.25 + (n-1)*stagger + 0.6s <= durationSec` and prints the stagger that
  would fit.
- **[GATE] G02 retuned 60-120s -> 60-80s** (user: aim 60-80 unless the story
  genuinely needs longer). Longer is still possible but must be ARGUED:
  `allowLong` is only accepted with a one-line `allowLongReason`.
- **[GATE] G03 hook 2.2s -> 2.0s** (user: the tension/surprise/consequence
  lands in the first 2 seconds, not a generic product announcement).
- **[GATE] G21 — captions are verified against the NARRATION, not the script.**
  Captions get written from the script, but the render uses the generated voice
  track; edit the script after the voice is made and the captions silently
  drift. G21 checks every caption word against the whisper transcript.
- **[GATE] G22 — one highlight per beat.** Highlighting three words in a
  four-word chunk highlights nothing. Caught 'Grok Bot, and it' double-marking.
- **[GATE] FINAL QUALITY GATE — render_job.py now runs doctor + reel_gates
  before `remotion render`.** Until today it ran validate + tsc and went
  straight to render, so a sheet could fail every gate and still produce an
  mp4. Verified: the pipeline exits 1 and never reaches the renderer.
- **[PROCESS] The script is approved before any avatar video is generated.**
  Generation costs credits and locks the audio; a script change afterwards is
  a re-render. Show the full narration + the beat-by-beat visual plan, get a
  yes, then generate.

Running the new gates over the shipped grok-bot sheet surfaced 5 real defects
(G02 runtime, G17 late presenter, G18 short data card, G20 vanishing row, G22
double highlight) — none of which the contact sheet showed.

## 2026-08-12 (3) — style/format split, and the state of style support

- **USER DECISION: `nick-saraev` stays as-is for tips/top-5.** Do not re-derive
  it. It was built 2026-07-24 from a 12-reel teardown and is fit for purpose.
- Style was only HALF-WIRED and the two halves contradicted each other:
  `scripts/validate_job.py` hard-required `brief.style == "nick-saraev"` while
  `config.json` defaulted to `varun-mayya`, so the job path rejected every reel
  actually shipped. (`jobs/` is empty — all three reels were built directly by
  `tools/build_<slug>.py`, which is why render_job stopped at validate.)
  FIXED: a style is valid if it has a pack in `styles/`.
- FOUR spellings of the same field were in use: `varun` (beat sheets),
  `varun-mayya` (config), `nick-saraev` (validate_job), `nick`
  (compile_shot_plan). CANONICAL = the style pack filename. Beat sheets
  migrated to `varun-mayya`.
- **`config.defaults.lengthRangeSeconds` was still [60,120] and `doctor.py` was
  CHECKING for [60,120]** — so doctor passed green while gate G02 enforced
  60-80. doctor now imports RUNTIME_MIN/RUNTIME_MAX from reel_gates, so the
  two can never disagree again. This was the 4th stale-prose drift found in
  one session (avatar_v in the skill, 60-120 in RULES, 1.2 speed in the style
  pack, this).
- ARCHITECTURE for multi-genre: **style (look) and format (genre) are separate
  axes.** Style = type/palette/captions/audio mix. Format = news, explainer,
  comparison, how-to, top-5 — and FORMAT is what changes the gate physics
  (runtime band, hook ceiling, facecam share, SFX count). Today every tunable
  is a module constant tuned to varun-mayya news reels, which is why a
  nick-saraev tips reel (native 26-48s) would FAIL G02's 60s floor. Gate
  tunables must move into per-format profiles before a second genre ships.
- Numbers for a new format are DERIVED FROM REFERENCE REELS, never invented —
  that is how varun-mayya (11 reels) and nick-saraev (12 reels) were built.

## 2026-08-12 (4) — format profiles shipped; top5 is live

- `tools/reel_gates.py` now carries **FORMATS**, a per-genre profile table.
  STYLE (look) and FORMAT (genre) are finally separate: a sheet declares
  `"format"`, and the runtime band, hook ceiling, facecam share, SFX count and
  SFX volume all resolve from that profile. Omitting it means `news`, so every
  existing sheet keeps working. Module-level constants for facecam/SFX were
  DELETED — leaving them was how a news-tuned number silently governed a genre
  it had never been measured on.
- **`top5` profile derived entirely from `styles/nick-saraev.md` v2** (12-reel
  teardown, 2026-07-24), which the user approved as-is on 2026-08-12. Nothing
  invented: runtime **26-48s**, SFX **6-9 pops at 0.06-0.10** ("ordinary cuts
  stay silent"), **comment-gate CTA required**. Three of those CONFLICTED with
  the news gates — a top5 reel would have failed G02 (60s floor) and G08
  (0.10-0.19 volume band) before this change.
- One honest gap recorded in the profile itself: **facecam share is inherited
  from `news`, not measured for top5.** It was derived as a general retention
  rule rather than a genre rule. Measure it on the first top5 reel and tighten.
- **[GATE] G23** — unknown format is blocked outright, with the message "add a
  profile derived from a real teardown; do not guess the numbers". This is the
  guard that stops the next genre being unblocked by invention.
- **[GATE] G24** — a format whose profile sets `requires_cta` must contain a
  CTA scene. For top5 the comment-gate CTA is a defining property, not a
  garnish.
- Self-tests: 34 checks, including a positive case (a real top5 sheet passes)
  and four negatives (unmeasured format, news-length reel declared top5, top5
  without a CTA, varun-loud SFX in a top5 reel).

## 2026-08-12 (5) — `settingspane`: rendered iOS Settings for how-to/fix-it

- **Xcode is NOT installed on this machine** — only Command Line Tools, so
  `xcrun simctl` does not exist and there are no simulators. Installing it is
  a ~7-10 GB download plus `sudo xcode-select -s`, which needs the user's
  password. NOT a blocker, because the simulator was the wrong tool anyway:
  Simulator Settings is missing whole panes (Cellular, Face ID), which are
  exactly the ones iGeeksBlog's biggest fix-it articles are about.
- **DECISION: build the pane, don't capture it.** Same precedent as `terminal`
  ("replaces real terminal screen-recs — crisper + reusable") and `chart`
  ("never ship a raw chart screenshot again"). A rendered pane is reusable,
  animatable, pin-sharp at 1080x1920, and needs no Xcode.
- `src/components/SettingsPane.tsx` — nav bar with back chevron, grouped rows
  with iOS separators/footers, icon tiles, real iOS switches that FLIP on cue
  (`flipAt`), and a row spotlight (`focus`/`focusAt`). Light and dark
  appearance. Verified by render, both appearances.
- LIMIT recorded in the component: it is a faithful RECREATION, not a capture.
  **The user will supply real device screen recordings** for panes we cannot
  rebuild honestly — those go in `deviceframe`.
- **[GATE] G25** — a pane's cues must LAND: spotlight `focusAt + 0.35s` and
  every `flipAt + 0.35s` must fit inside the scene, and a pane must have rows.
  Same failure class as G20 (an animation scheduled past the end of its scene
  simply never happens). `settingspane` joins BUILDING_TYPES, so its ceiling
  is 3.3s rather than the 2.6s card limit — the spotlight lands after entry.

### Regression caught, and a correction to the 2026-08-12 (3) entry

Canonicalising the beat sheets' `style` from `"varun"` to `"varun-mayya"`
**broke every reel**: `src/theme/tokens.ts` keys THEMES by a SHORT runtime id
(`StyleId = "varun" | "nick"`), which is a deliberate separate namespace from
the style-pack filenames — not a fourth "spelling" as that entry claimed.
Renders died with `Cannot read properties of undefined (reading 'accent')`.
FIXED with `resolveStyle()`: accepts either id, falls back to `varun` with a
console warning, and never hands `undefined` to a component.

LESSON: that canonicalisation was a data change shipped WITHOUT rendering a
single frame. Gates and tsc both passed — neither can catch a runtime theme
lookup. **Any change to a field the renderer reads must be proved with a still
render before it is called done.**

## 2026-08-12 (6) — `comparison` format: structure gated, timing NOT faked

- Third profile added. **Its timings are INHERITED from `news` and labelled as
  inherited, because there is no comparison teardown in `styles/`.** Every
  timing value is deliberately identical to news rather than nudged, so nobody
  can later mistake them for derived numbers. `_derived` says so in the
  profile itself. Re-derive from 3-5 real comparison reels before trusting the
  band.
- What IS specific to the genre is STRUCTURAL, and needs no measurement —
  **[GATE] G26**:
  - the sheet declares `sides: ["A", "B"]`, named as they appear on screen;
  - at least **3** compare scenes (comparesplit / hcompare / specsheet / chart
    / strikeswap) — fewer is a review of one product that mentions the other;
  - **balance**: single-sided screen time must sit within **40-60%** per side.
    Scenes carry `side: "a" | "b" | "both"` (new field on SceneBase). A
    comparison that gives one product 80% of the screen is an ad, and the gate
    says so by name: "as cut this reads as an ad for 'X'";
  - every `comparesplit`/`hcompare` must carry BOTH labels — an unlabelled
    split is two videos playing next to each other, not a comparison.
  - If no scene is tagged, balance is reported as a WARNING, not a pass — the
    absence of tags must not read as evidence of fairness.
- Self-tests now 41 checks: three positive (news, top5, comparison all build
  clean) and four new negatives (no sides, one product hogging the screen,
  unlabelled split, a "comparison" with nothing to compare).

PRINCIPLE CONFIRMED: when a genre had a real teardown (top5 <- nick-saraev)
the numbers came from it; when it did not (comparison) the numbers were
inherited WITH DISCLOSURE and only the derivable rules were gated. Guessing a
plausible-looking band would have been the easy path and the wrong one — G23
exists to make that refusal the default.

## 2026-08-12 (7) — formats made visible, and numbers de-duplicated

- User asked "did you create new styles for each format?" — reasonable, since
  `styles/` still held three files. Answer: no, and correctly so — a format is
  not a style. But the question exposed a REAL gap: `news` had
  varun-mayya.md + the script playbook, `top5` had nick-saraev.md, and
  **`comparison` had no prose home at all.** Its structure was gated (G26) but
  nothing told a fresh session how to WRITE one.
- NEW `formats/` directory: `README.md` (the two-axis model + how to add a
  genre), `news.md`, `top5.md`, `comparison.md` (structure, scene vocabulary,
  script skeleton, and each one's honest measured-vs-inherited status).
- **`python3 tools/reel_gates.py --formats`** prints the live profile table
  plus every `_derived` provenance string. The format docs deliberately DO NOT
  restate the numbers, and CLAUDE.md's hand-written format table was deleted.
  RULE: **print the numbers, never copy them.** Four stale-prose drifts were
  found in this one session and every single one was a doc quoting a number
  that had since moved — including, on this very edit, CLAUDE.md still saying
  "34 checks" and "news 60-80s, top5 26-48s" minutes after both changed.

## 2026-08-12 (8) — script approval is now a GATE, not a good intention

- **USER: "Our System never shows me the script and if it is okay or I want any
  changes. It must first take approval of the script and ask relevant question
  and go ahead after my approval."** They were right, and the failure is
  self-inflicted: script approval had been written as PROSE in CLAUDE.md,
  RULES.md and the news-reel skill on 2026-08-12, and this repo's founding
  observation is that *prose rules get skipped while code rules get enforced*.
  I gated everyone else's rules and left my own as a comment.
- `tools/script_approval.py` — `propose` / `approve` / `check`:
  - `propose` prints the narration, word count, estimated runtime at speed
    1.05, and the open questions from `jobs/<slug>/questions.md`, ending with
    "NOTHING IS GENERATED UNTIL THE USER SAYS YES";
  - `approve` records a sha256 of the spoken words (whitespace-normalised, so
    reflowing is not an edit but changing a word is);
  - `check` exits 1 with instructions when unapproved OR when the script has
    changed since approval.
- **[GATE] G27** — the beat sheet must carry `script` (the narration) and a
  matching `approval.sha256`. Approving one script and generating a different
  one is now impossible.
- Wired into `scripts/render_job.py` alongside doctor + reel_gates, so an
  unapproved script cannot reach an mp4 by any route.
- VERIFIED end to end, not asserted: check before approval exits 1; propose
  prints; approve records; check passes; changing ONE word ("October" ->
  "November") flips it back to exit 1 with both hashes shown.
- Self-tests now 44: three new negatives (never approved, edited after
  approval, sheet carries no script).

LESSON, and it is the same one for the fourth time today: **if a rule matters,
it is code with a self-test. If it is only prose, assume it will be skipped —
including by me.**

## 2026-08-12 (9) — personal-model training set (the real fix for #7)

- HeyGen offers "Train your personal model" from 10-30+ images (60 credits,
  10-15 min). This is the genuine fix for feedback #7 (fixed smile), because a
  trained model is NOT a deformation of one still.
- **THE TRAP, and it is the whole ballgame: the training set becomes the
  expression range.** The existing look library is almost entirely smiling
  ("Smiling podcaster…", "Smiling man…", "Smiling host…"). Training on those
  produces a better-MOVING avatar that still grins on the caveat — the same
  defect measured on 2026-08-12, just more expensive.
- `references/avatar-training-shotlist.md` — 30 shots as a full matrix
  (angle x framing x expression x hands). **12 of 30 are deliberately
  non-smiling** (Block A: neutral, concerned, skeptical, unimpressed, warning,
  weighing). Blocks B/C/D cover warm, reaction and angle coverage. Every shot
  carries the permanent prop ban and the 16:9 centred-subject framing the
  9:16 crop needs.
- AFTER training, do not trust the preview: measure motion with
  `tools/measure_avatar.py`, then spend ~3 credits on a 7s three-register probe
  and read a face-crop strip at <=0.5s spacing — the exact method that proved
  the current avatar's smile was immovable.
- IF the trained model holds a real range it could collapse the warm/serious
  PAIR into one avatar and relax G19's one-look-per-reel constraint. IF it does
  not, the two-look system stands. Record which, either way.

## 2026-08-13 — made-by-google-26 (first ~2-min reel; priceladder ships)

- USER REQUEST overrode the 60-80s band: "a reel of almost two minutes"
  (2026-08-13). Built with `allowLong` + written reason. LESSON ON LENGTH
  BUDGETING: the playbook's "220-300 words → 60-80s" assumes ~200 wpm
  delivered, but the HeyGen voice at speed 1.05 measured **~148 wpm**
  (335 words → 140.1s raw). RULE: budget scripts at ~2.5 words/sec for this
  voice until re-measured; a 2-minute ask is ~300 words, not ~385.
- **Pause-tightening a HeyGen master is safe and cheap**: 17 inter-sentence
  gaps >0.5s totalled 10.5s; 15 were jump-cut (video+audio together, cuts at
  mid-silence) taking 140.1s → 135.2s with zero credits. The 2 gaps under
  facecam beats (hook, CTA) were left uncut, and every cut point was recorded
  so no facecam beat spans one — a jump ON the face is visible, a jump under
  b-roll is not. Cut points live in the build script's CUTS list.
- **NEW component `priceladder`** (types.ts + Reel.tsx + BUILDING_TYPES +
  test_gates case): prop-driven rows, old price struck through → new price
  springs in + delta chip. Built because StrikeSwap is hardcoded ("PAID
  TOOLS") and the honesty beat needed 4 rows of real prices. Reusable.
- **lint_frames.py had a latent bug**: DESIGNED set read
  `"promptcard" "settingspane"` (missing comma → one concatenated string), so
  BOTH types were held to the 30% footage dead-space limit instead of 70%.
  Fixed + priceladder added. A promptcard had been flagged at 74% because of
  this — check the literal set contents when a lint class looks wrong.
- **Keynote stage-wide shots are a trap**: a slide-region crop verified on one
  frame breaks when the broadcast cuts to another camera mid-window
  (c-tagmacro, c-foldrig, c-gpsslide all drifted). RULE: verify a stage-slide
  crop at BOTH ends of the window, and prefer the full-frame slide moments
  (cameras hold ~3-6s) over cropping wide shots.
- **Clip heads lie**: three cuts started 1-5s before the product shot (recycled
  flat-lay, watch film, wrist demo) and leaked stage presenters into the reel;
  caught only on the contact sheet. RULE: after cutting, check the FIRST
  second of every clip, not just the mid frame — or set `from` in the scene.
- yt-dlp on this network: section downloads crawl at ~10 MB/min sequentially;
  `-N 8` (concurrent fragments) made the same section land in under a minute.
  `--force-keyframes-at-cuts` made ffmpeg exit 8 on merge — drop it; exact
  boundaries don't matter since sub-clips are re-cut precisely anyway.
- whisper artifacts handled in-build: "%"-tokens ("40 %"), split decimals
  ("3 .5"), and "times"→"x" pairs are merged BEFORE captioning, so captions
  read 40% / 3.5x / 120x (G16) while timings stay untouched.

### Treatment history — made-by-google-26
- split hook (family-lineup slide / face), NO logoassemble (3-reel streak
  broken deliberately), caps kinetic "MADE BY GOOGLE 2026" over drop-test lab
  footage, 20 keynote footage/floatcard windows (product films, 120x zoom
  demo, fold hinge/edge macros, Tensor G6 die, watch film, breathing-emergency
  watch face, Daniel Durant ASL live demo x3 distinct shots), specsheets x4
  (sensor / energy / Titan M3 / $29 tag), charts x2 (Gemini speed, Magic
  Capture 500 frames), statcards x3 (15hr/15min charging, Find Hub 1B devices,
  256GB storage), cream + black wordcascades (bridge, Rambler), promptcard
  (clean text), NEW `priceladder` for the $100 price-hike honesty beat,
  annotatezoom receipts x2 (blog.google pricing paragraphs, underline on
  "August 20" / circle $29 + underline "November 11"), facecam ~17% in 8 pops.
- Used here, avoid repeating next reel: priceladder for a price beat,
  caps-kinetic-over-lab-footage title card, three-window live-demo trio.

## 2026-08-13 — digital twin #1: the concept works, this twin does not

Twin `8e49c9d1` ("Dhvanesh -- 55", `avatar_type: digital_twin`) tested on the
IDENTICAL three-register probe used for every avatar, so results compare
directly. Cost ~337 credits (436 -> 92 remaining, resets 2026-08-22).

**THE GOOD NEWS, and it is the answer to feedback #7:** a digital twin BREAKS
the fixed-smile problem. The face stays neutral and level through the caveat.
No photo avatar can do that at any `expressiveness` — proven 2026-08-12. The
twin route is right; this twin is not.

**Why it is unusable for reels (all measured, none assumed):**
1. **Branding burned in** — "iGeeksBlog" lower-third + social icons in **19 of
   19** sampled frames, plus a SUBSCRIBE button. Permanent, and it collides
   with our own captions and source credits.
2. **1280x640 @ 25fps, 2:1 aspect** (source preview 1440x720, also 2:1). We
   need 1080x1920 @ 30fps. A 9:16 crop off a 640px-high source is 360x640 —
   about a 3x upscale.
3. **Hands out of frame.** Head-and-shoulders framing, motion **1.71 (stiff)**,
   under the 2.5 gesture threshold. No `motionPrompt` can gesture with hands
   that were never filmed.

ROOT CAUSE of all three: **it was trained on a PUBLISHED, EDITED video rather
than raw camera footage.**

- `references/digital-twin-recording-spec.md` written: raw footage only, 16:9
  1080p+ (never 2:1), 30fps, waist-up with hands visible and empty, 2-5 min
  covering all three registers, then measure before registering.
- Registered in `avatarRegistry` with `USABLE: false` and the full reason, so
  no future session picks it by accident.
- **`avatar_v` + `motionPrompt` is now accepted** — the API allows it once the
  group contains a digital twin, which was exactly the blocker that forced
  `avatar_iv` on 2026-08-11. Test both engines on the retrained twin.

LESSON: measure the SOURCE before paying to train on it. Resolution, aspect,
frame rate, framing and burned-in graphics are all checkable in one ffprobe
plus one frame, and every one of them was fatal here.

## 2026-08-13 (2) — digital twin #2 WORKS, and native 9:16 unlocked

Twin `f55b0b7c` ("Dhvanesh -- 59"), same three-register probe as every other
avatar so results compare directly.

**Free source checks first** (the discipline that twin #1 taught): preview is
16:9 1280x720 @30fps, motion 3.71, no watermark, hands in frame. Only then
spent credits. Every one of those was a defect in twin #1.

**Measured on the render (probe d5006da2, avatar_v + motionPrompt):**
- motion **4.41 (gestures)** vs twin #1's 1.71 (stiff)
- hands **bare in 30/30** sampled frames, varied gestures, no props
- face **level through the caveat, no grin** — feedback #7 is genuinely solved
  by a twin; no photo avatar can do this at any `expressiveness`
- same blue-hoodie studio as the shipped reels → no wardrobe break
- REGISTER is neutral-dominant: it does not grin at bad news, but it did not
  visibly warm on the closing question either. Recorded as "neutral", NOT as a
  proven warm-to-serious range.

**BIG PIPELINE FIND — `resolution` and `aspectRatio` were never being set.**
Renders defaulted to 720p 16:9 and we cropped+upscaled ~2.7x to 1080x1920. The
API takes `resolution: '4k'|'1080p'|'720p'` and `aspectRatio: '9:16'`, and
digital twins are 4K-eligible (photo avatars never were — which is why the old
"4K is impossible" note was true then and is wrong now).
VERIFIED (probe 768387f5): `aspectRatio 9:16` + `resolution 1080p` +
`fit cover` renders **NATIVE 1080x1920** with good framing — face upper-third,
hands visible in the lower third. No crop, no upscale.
- USE native 9:16 for full-frame facecam beats.
- KEEP 16:9 for `split` scenes, where the avatar fills half the frame and the
  wider source is what you actually want.

**OPEN: both renders came back 25fps** while the project is 30fps. The source
preview is 30fps, so it is the render. Conform on ingest, or hunt a parameter.

Credits: 92 -> 80 across three probes (~12). Resets 2026-08-22.

LESSON: the free source checks cost nothing and would have saved ~337 credits
on twin #1. They are now the first step in
`references/digital-twin-recording-spec.md`.

## 2026-08-13 (3) — digital twin is now the DEFAULT presenter

User instruction: make `f55b0b7c` the default. Three coordinated changes, not
just the id:

1. `avatar.avatarId` -> `f55b0b7c…`, `avatar.engine` -> `avatar_v` (doctor
   enforces that engine matches the avatarRegistry entry, and the twin was
   MEASURED on avatar_v).
2. **`avatar.expressiveness` DELETED.** The API rejects `expressiveness`
   alongside `engine.type: "avatar_v"` — it is Avatar IV + photo avatar only.
   Leaving the old `"high"` in place would have failed every single request.
   This is the kind of coupling that a bare id swap silently breaks.
3. **G19 now uses a compatibility map, not equality.** The twin's register is
   `neutral`, and under the old strict check a `serious` script on a `neutral`
   presenter would have been BLOCKED — wrongly, because not grinning at bad
   news is exactly what the gate wants. New rule:
   - `serious` accepts `{serious, neutral}`
   - `warm` accepts `{warm}` only — a level face cannot sell warmth, and this
     twin has never been proven to warm up.
   47 self-test checks, including a new positive (neutral twin delivers a
   serious script) and a new negative (neutral cannot deliver warm).

The photo avatars stay registered as fallbacks. `0aa05d6e` (warm) is now the
ONLY proven option for a genuinely warm reel until the twin is probed for it.

Also recorded in `avatar._render_note`: always send `resolution` and
`aspectRatio`. They were unset for every reel shipped so far, which is why the
masters were 720p and cropped+upscaled ~2.7x.

## 2026-08-13 (4) — sound design became a gate, from the user's two references

The user supplied two reference videos and the expanded `public/sfx/` library
(17 files) and asked the system to use them "whenever and wherever they fit".

**METHOD NOTE — my first analysis was wrong and I discarded it.** I ran
high-band spectral-flux onset detection on both refs and got 322-340 "cues per
minute" at a 0.17s median gap. That is the rate of SPEECH SYLLABLES — plosives
and sibilants are broadband and sit above 4 kHz. Building placement rules on
that would have been building on noise. Re-ran with whisper word timings as a
speech mask, which is when the real content surfaced.

**The refs are not reels to imitate — they are TUTORIALS that state the
mapping.** Whisper recovered it verbatim: "Use WHOOSH to zoom in or out. Use
POP or CLICK for pop-ups. Use RISER to add suspense. Use CAMERA SHUTTER for
transitions. Use MAGIC REVEAL to reveal stuff." The second ref gives six
purposes with the sound played in the gap after each "Use".

- `tools/sfx_library.py` — 16 cues, each with MEASURED properties (duration,
  attack, spectral centroid start->end, low-band share) and a role taken from
  the refs. Measurement mattered: it proved `Riser.MP3` peaks at 1.43s of
  1.49s with a rising centroid (a true riser), `Whoosh (Reversed)` is 64%
  low-band and front-loaded (so `lead == dur` — it must start a full length
  before the cut), and `impact-boom` is 86% low-band.
- **[GATE] G28** — file must be catalogued AND on disk; role must fit the beat
  type; a cue may not outrun its scene; a riser must resolve into a reveal or
  impact within its own beat or the next 3; per-role caps (impact 3, shutter 3,
  suspense 2, reveal 2, comedic 1); comedic stings only in `top5` and never at
  serious tone.
- **THE SILENT-CUE BUG: nothing validated `sfx.src` at all.** A typo'd
  filename rendered silent while still counting toward G08's 6-9 budget — a
  reel could pass the sound gate with no sound in it.
- TWO RULES CORRECTED after running against real reels, because the rule was
  too narrow rather than the reels wrong: `impact` is now allowed on hook
  scenes (a brand mark LANDING is a statement landing — all three shipped reels
  chose that independently), and a riser's payoff may share its own beat.
- Shipped reels now show 5-6 `impact` cues each, some on plain footage, one
  2.09s cue on a 0.96s scene. CAUSE: the old `public/sfx2/` library had only
  five files and NO pop, shutter or reveal — so `impact-boom` became the
  general-purpose cut sound. The new library is what makes correct placement
  possible. Not fixing those reels; the rule applies forward.

51 self-test checks.

## 2026-08-13 (5) — source pages are captured on MOBILE

User: "How about making our system scout sources on mobile view as we make
videos in shorts and reels format?" Correct, and it was a real defect —
`tools/capture.mjs` defaulted to **1200x900 with a desktop user-agent** while
every reel this engine ships is 9:16.

MEASURED on the same live page (igeeksblog.com/best-iphone-ipad-ai-apps/):
- mobile default -> **1080x2340**, fills the whole 1080x1920 frame, headline
  readable at arm's length, room left to pan;
- `--desktop` -> 3600x2700, which fits to **1080x810 — 42% of the frame
  height** — body text unreadable, and an ad banner cutting across it.

CHANGES:
- `capture.mjs` now defaults to **360x780 @ scale 3 = 1080x2340** with an
  iPhone user-agent AND `isMobile: true` + `hasTouch: true`. The `isMobile`
  flag is the part that matters: it makes Chromium honour the page's
  meta-viewport, which is what actually triggers the mobile LAYOUT — a narrow
  window alone does not.
- `--desktop` opts out, for pages with no mobile layout, wide dashboards, or
  genuine side-by-side comparisons.
- **[GATE] G29** — a `sourceread` may not use a landscape capture, and may not
  use one under 1000px wide (it would upscale into the 1080 frame). The scene
  already declares `srcWidth`/`srcHeight`, so this is checkable without
  touching disk.

53 self-test checks.

NOTE for whoever adds the next fixture: appending the new `sourceread` scene
MID-LIST broke the top5 fixture's facecam share, because that helper slices
`scenes[:14]`. Append test scenes at the TAIL. Second time this exact mistake
has been made in one session.

## 2026-08-13 (6) — desktop capture is allowed, but must be cropped and moved

User: mobile by default, "however, make sure that when it is not feasible to
scout from mobile view, do it from desktop. We may use various effects like
zoom in, crop, slide-in… to fit in our reels." Reference: YouTube short
`q4_-y67JGCU` — 96s, 1080x1920, 41 cuts (~2.3s/shot, matching our own pacing).

MEASURED off the reference, frame strips at 2 fps:
- **Articles are mobile, full-bleed, with a PROGRESSIVE HIGHLIGHT.** The
  Anthropic/EU-AI-Act support page starts wide, pushes in, and an orange
  highlight extends phrase by phrase in time with the narration ("Claude
  models" -> "…launched in the EU on or after August 2, 2026 will support" ->
  the full sentence). That is exactly our `sourceread`, which already fits to
  frame width, follow-scrolls the active line to ~58% down frame, and applies
  a slow zoom.
- **Desktop UIs are CROPPED, not fitted.** The wide Claude desktop app is
  cropped to the composer box, scaled until the text reads, and the crop
  window PANS — the "Evening" header visibly drifts across frames. It is never
  letterboxed.
- **Live interactions are RECORDED, not screenshotted.** The same shot shows
  typing land word by word ("Add" -> "Add punctuation," -> "Add punctuation,
  fix grammar"). A still cannot carry that.

WE ALREADY HAD THE COMPONENTS — `annotatezoom` eases from wide into an explicit
`focus` rect, `deviceframe` push-ins, `sourceread` fits-to-width and
follow-scrolls. What was missing was the POLICY and its enforcement.

- `references/source-capture-policy.md` — when to use mobile vs desktop, the
  obligation that comes with desktop, and a treatment table by source type.
- **[GATE] G29b** — an `annotatezoom` with a LANDSCAPE source and neither
  `focus` nor annotations is blocked: the camera would settle on the union of
  nothing, i.e. the whole wide page, i.e. a letterbox at 1080x608 in a
  1080x1920 frame.

54 self-test checks.

## 2026-08-14 — three advisory skills installed, five explicitly denied

Evaluated `Ootto-AI/claude-content-skills` (13 skills). Read each candidate's
frontmatter and body BEFORE installing, because a skill's text instructs the
agent — trusting a README summary would have been the same mistake as trusting
a filename.

INSTALLED as REAL directories in `.claude/skills/` (not symlinks, so they
travel with the repo to a cloud/team checkout):
- **`reel-analyzer`** — teardown of a reference reel. Fills the gap G23 creates:
  every new FORMAT needs a real teardown. Takes a local file or URL, no Apify.
- **`content-repurposer`** — one long source -> 5+ reel concepts. Lands on the
  strategic finding from the igeeksblog.com research: the evergreen "best X"
  and fix-it libraries are the durable opportunity; news dies in 48 hours.
- **`viral-hook-writer`** — 10 ranked hook candidates. G03 caps the hook and
  demands it open on real tension, but nothing GENERATED candidates.

DENIED, with reasons recorded in CLAUDE.md: `content-factory` (a parallel
end-to-end pipeline — 30-45s scripts, its own Remotion render, Instagram
publishing via Composio, auto-DM lead loop; it would hijack "make a reel",
bypass every gate, and act outward on the brand account), `reel-builder`
(assembles outside the beat-sheet contract), `caption-hashtags` (redundant with
`social`, whose platform limits we already corrected), `ai-brain` (Obsidian
vault dependency; STYLE-RULES.md is better — in-repo, dated, gate-enforced),
`comment-responder` (automated public replies and DMs on the brand account).

THREE THINGS READING THE FILES CAUGHT, now neutralised in CLAUDE.md:
1. `reel-analyzer` ends with "Next: feed the teardown into reel-scripter ->
   reel-builder" — i.e. the installed skill instructs the agent to use two
   DENIED skills. Explicitly countermanded.
2. Both `content-repurposer` and `viral-hook-writer` carry "Obsidian memory
   tips" that would introduce a vault dependency. Ignored by rule.
3. Their length/structure defaults conflict with our measured bands —
   `content-repurposer` prescribes a 3-beat hook/value/CTA outline,
   `viral-hook-writer` caps hooks at 12 words. Ours come from
   `formats/<format>.md` and `reel_gates.py --formats`.

STANDING CONSTRAINT: these skills ADVISE, they never BUILD. Output lands in our
files (`formats/*.md`, `FORMATS`, `jobs/<slug>/script.md`) and passes our gates.
And `reel-analyzer`'s "pacing assessment" is an ESTIMATE — every number that
reaches a FORMATS profile must still be measured with ffmpeg/ffprobe, exactly
as the comparison profile's timings have NOT been.

## 2026-08-14 (2) — re-review of four Ootto skills after user pushback

The user challenged four exclusions. Two of my calls had been made off the
README summary rather than the file — the same shortcut I refused to take on
the three I did install. Read all four in full. One reversal, two confirmations
with harder evidence, one idea I should have engaged with.

**REVERSED — `going-viral` is now INSTALLED.** My "overlaps social" dismissal
was wrong; it is a substantive strategy layer. Adopt: Frame 0 IS the hook
(biggest element already on screen AND moving, >=40% of frame, legible on mute);
order motion -> lock -> claim with the claim landing **1.2-1.6s** (sharper than
our G03, which only caps the hook at 2.0s); no fade-from-black or title card;
nothing static; re-hook at ~4s/9s/15s; one CTA; every opened loop must close.
NOTE: "nothing static — every element keeps a low-amplitude idle motion"
INDEPENDENTLY CONVERGES with the BrandHook rule we derived ourselves on
2026-08-11 ("motion must NEVER fully settle"). Two separate derivations landing
on the same rule is corroboration.
REJECT for news/comparison: manufactured indignation, engineered outrage,
comment-keyword -> auto-DM funnels. We are a publisher, not a lead-gen account.
The comment gate stays legitimate in `top5`, where nick-saraev prescribes it.

**CONFIRMED — `caption-and-hashtags` stays out, now on a checkable fact.** It
prescribes "HASHTAGS — 12-15". `social/references/platform-limits.md` says
Instagram max is **5 (official, since Aug 2025)**, recommended 3-5, and
exceeding the cap gets them ignored. Installing it would reinstate the exact
error corrected earlier in this session. STOLE TWO IDEAS: an ALT TEXT line
(accessibility — genuinely missing from our packaging), and hashtags in the
FIRST COMMENT plus a reply-sparking question rather than in the caption.

**CONFIRMED, MUCH MORE STRONGLY — `agent-reach` must NOT be installed.** The
user asked me to check its scraping behaviour. Findings: vendored from a third
party (Panniantong/Agent-Reach), predominantly Chinese-language and aimed at
Chinese platforms; requires binaries we lack (`agent-reach`, `mcporter`,
`opencli`, `rdt-cli`, `twitter-cli`, `bili-cli`); **Reddit — the one capability
wanted — has NO zero-config path and requires a logged-in session, with setup
described as "the user only needs to provide cookies"**; its description is a
hijack directive ("MUST USE when the user shares any URL", "do not invent your
own approach") that would override WebSearch/WebFetch/yt-dlp on every research
task; and it solicits its own updates via a pasted URL. Everything zero-config
in it we already have and used today.

**`content-factory`: the INSTALL verdict stands, but the IDEA is good and I
skipped it.** The skill hardcodes Apify + Composio + its own Remotion +
Instagram autopost + 30-45s scripts + 3x/day. Installing it is a second
pipeline that bypasses 29 gates. BUT the user's actual point — "we can think of
and turn our own system working like this" — is right: an ORCHESTRATOR over OUR
own steps is valuable and absent. Proposed, not yet built. Note 3x/day is
impossible here regardless: 80 HeyGen credits is about two reels.

## 2026-08-14 (3) — showrunner built; caption skill installed with its number capped

**`tools/showrunner.py`** — the orchestrator idea from `content-factory`,
applied to OUR steps. `status` / `next` / `run` over ten artifacts, from
manifest to packaging. It AUTOMATES the deterministic steps (register, gates,
render+master, lint) and HALTS at the two that must not be automated.
VERIFIED both stops, not asserted:
- with a script and no approval -> "HALTED — Script approved by the user …
  the showrunner will not cross this line";
- with approval but no voice -> "HALTED — Voice + avatar master generated …
  THIS SPENDS CREDITS".
It never publishes. Deliberately NOT content-factory's "3x a day": 80 HeyGen
credits is about two reels, and unattended posting cannot coexist with a
blocking human approval gate.
Run against grok-bot it correctly reports the script/approval steps as NOT done
— that reel predates the approval convention, and the tool says so rather than
pretending otherwise.

**`caption-and-hashtags` INSTALLED**, reversing the previous entry, at the
user's call: "we can keep the HASHTAGS limit to 5." Its structure (caption /
first comment / ALT TEXT) is useful; only its "12-15 hashtags" was wrong.
**`tools/packaging_check.py`** makes the cap code rather than a note — it reads
`jobs/<slug>/packaging.md` and enforces Instagram 5 / YouTube 15, the 3-5
recommendation, caption and title lengths, ALT TEXT on every post, and rejects
hashtags sitting in the caption instead of the first comment. Verified failing
(12 tags, no alt text) and passing (4 tags + alt text).

PATTERN, again: the fix for a skill carrying one wrong number is not to refuse
the skill — it is to take the useful part and put the number under a gate.

## 2026-08-14 (4) — september-preview post-mortem

The reel PASSED all gates and still shipped visible defects. That is the
headline: the gates approved it, so the gates were wrong, not the operator.

**MEASURED, not guessed:**
- 38 scenes, 79.7s, 1080x1920 @30fps. Gates: PASSED.
- Credits: 25 scenes carry one; the 6 without are all `avatar-master`, which is
  correct. So nothing was missing — the RENDERING was inconsistent.
- SFX: 7 cues but only **3 distinct files**, all from the old 5-file `sfx2/`
  library. 13 of the 16 catalogued cues unused — no pop, no riser, no reveal,
  no shutter. Cue levels measured +2 to +4 dB over programme, so they are
  audible; the palette is the problem, not the mix.
- Avatar master is **1920x1080 @25fps** — generated 16:9 and cropped, NOT the
  native 9:16 1080p that was added to config on 2026-08-13.

**TWO DEFECTS WERE REGRESSIONS OF INSTRUCTIONS ALREADY GIVEN.** Both were
recorded in this ledger as prose and never became code:
1. "Source: X, left-aligned under the footage" (2026-08-12) was applied to
   FloatingCard ONLY. FootageScene / SplitScene / ReceiptScene kept a bare
   centred name at 85% white. The same reel shows a bold "Source: MacRumors"
   on an article card and a faint centred "Apple" under a video.
2. "Outro caption centre or slightly below" (2026-08-12) — the closing headline
   shipped at **y=0.07**, the top of the frame.

FIXES:
- `src/components/Credit.tsx` — ONE treatment, imported by FootageScene,
  SplitScene and ReceiptScene. `creditLabel()` adds the "Source: " prefix
  unless the credit already starts with source/credit/@.
- **[GATE] G32** — the last headline, if it falls in the closing fifth of the
  reel, must sit at y >= 0.45.
- **[GATE] G33** — at least 4 DISTINCT sfx files, and at least 2 distinct
  roles. G08 counted cues; counting cues does not measure sound design.

**TWO DUPLICATE GATE IDs FOUND — one of them mine, minutes old.** I numbered
the outro gate G30 when G30 (orphan numeric fragment) already existed, and the
suite still went green. Adding a uniqueness assertion then exposed a SECOND,
older collision: G28 was both "orphan single-letter caption token" and the SFX
placement gate. Renumbered the orphan-token gate to G34 (the SFX gate is
referenced in RULES.md, the skill and the published manual).
`test_gates.py` now asserts every `# Gnn — ` header is unique BEFORE running
any case. 33 ids, all unique. 57 checks.

LESSON, and it is the same one again: **the prose-vs-code rule applies to this
ledger too.** Feedback that became a gate (props ban, presenter by 5s, data
card dwell) has held. Feedback left as prose (credit styling, outro position)
regressed within two days. A ledger entry is a note to nobody unless it also
becomes a check.

## 2026-08-14 (5) — voice engine identified, ink-circle captions, Remotion skills

**VOICE (#1) — the cause is found and it is fixable.** The reel sounded flat
because we have only ever sent `speed`. The API also takes
`voiceSettings.engine_settings`, and a probe CONFIRMED the voice
`bb79e839` ("iGeeks Blog") is **ElevenLabs-backed** — the request was accepted
with `engine_type: "elevenlabs"`, which the API rejects on a mismatched voice.
That unlocks the two controls that actually govern delivery:
- **stability** — LOW means more emotional variation between sentences; HIGH
  is the flat, consistent read we have been shipping. Probed at **0.35**.
- **style** — stylistic exaggeration. Probed at **0.45**.
- plus `similarity_boost` 0.75 and `use_speaker_boost`.
Probe `e1fd4471` in flight. **Config is NOT changed until the probe is heard** —
the same discipline that stopped three earlier avatar claims being wrong.

**CAPTIONS (#8) — `ink-circle` added**, measured off the user's reference
(instagram.com/reels/Db_Xf3tAuzH, 1080x1920 @30fps, 23.5s):
- near-black sentence-case text, weight 800, at **y ~0.65** of frame height
  (measured: text band centred at 856/1920 in one frame, caption band ~1240);
- exactly ONE accent word per line in coral **#d86c48** (sampled off the frame,
  not guessed);
- a **hand-drawn ellipse** looping that word — irregular, and overshooting
  where the stroke crosses itself, like a real marker. Implemented as an SVG
  path drawn on with strokeDashoffset.
- The line **BUILDS word by word and STAYS**, rather than replacing itself.
It differs from `nick-display` on every axis (ink vs white, sentence case vs
caps, upright vs italic, building vs replacing) so it is a genuine second
system, not a variant. G10 now accepts either.

**REMOTION (#9) — the official skills are installed**: `npx skills add
remotion-dev/skills` -> 12 skills including `remotion-markup` (animation and
effects), `remotion-captions` (timing/sync) and `remotion-docs` (search the
docs and fetch any page as markdown). First thing learned from `remotion-markup`
and worth checking our components against: **CSS `transition` / `animation` and
Tailwind animation classes DO NOT RENDER** — animation must be driven by
`useCurrentFrame()` + `interpolate()`, with `Easing.bezier()` / `Easing.spring()`
for timing. That is a correctness rule, not a style preference.

### Voice probe RESULT — settings accepted, effect NOT proven

Probe `e1fd4471` vs the september-preview VO, measured rather than judged:

| | expressive (0.35/0.45) | september-preview |
|---|---|---|
| loudness sd | 5.11 dB | 4.78 dB |
| loudness range | 20.3 dB | 21.5 dB |
| pitch sd | 301.6 cents | 281.3 cents |
| pitch p10-p90 | 495 cents | **589 cents** |

**The settings did not produce a measurably more expressive read**, and on
pitch spread the OLD take is wider. The API accepted `engine_type:
"elevenlabs"` — which does confirm the voice is ElevenLabs-backed — but
accepting a parameter is not the same as it changing the output. DO NOT
change config on this evidence; the honest status is "available, unproven".

Likelier causes of the flat read, in order:
1. **The SCRIPT.** Prosody follows text. A run of uniform declaratives reads
   flat at any stability setting. The reference reels vary sentence length,
   interrupt themselves, and ask questions mid-flow.
2. `get_voice` reports **`support_pause: true`** for this voice — explicit
   pause/break markup is an untried lever that acts on pacing directly.
3. HeyGen may not forward engine_settings to a cloned voice at all.

NEXT, and cheap: generate the SAME sentence twice — once as written, once
rewritten with varied structure and explicit pauses — and measure both. That
isolates script from settings, which this probe did not.

## 2026-08-14 (6) — the voice lever is the SCRIPT, and it is measured

Two takes of the SAME facts through `create_speech` (audio only — a voice test
does not need avatar credits), identical voice and speed, script as the only
variable:

| | A · flat declaratives | B · varied + SSML pauses | delta |
|---|---|---|---|
| pitch sd | 161.6 cents | **207.4 cents** | **+28%** |
| pitch p10-p90 | 292 cents | **380 cents** | **+30%** |
| silence share | 26% | **38%** | +11.6 pts |

Compare the engine-settings probe from earlier the same day: stability 0.35 /
style 0.45 moved pitch sd by +20 cents and made the spread NARROWER than the
flat reel. **Script structure moves prosody 2-4x more than the engine settings
did, and in the right direction.**

WHAT MAKES B WORK — write these into scripts, not into config:
- fragments and one-word sentences ("Five.") next to long ones;
- a question mid-flow ("But the one everyone is waiting for?");
- a repetition for emphasis ("...three hundred dollars. Three hundred.");
- explicit `<break time="0.35s"/>` — this voice reports `support_pause: true`,
  and `create_speech` accepts `inputType: "ssml"`.

**CONSEQUENCE FOR THE WORD BUDGET.** Pauses cost runtime: A ran 2.89 words/sec,
B ran **2.53**. The approval estimator uses a flat 2.7. A pause-rich 70s script
is therefore ~180 words, not ~190 — and the more expressive the script, the
fewer words fit. Worth splitting WPS by whether the script carries breaks.

## Remotion skills — two live bugs fixed, one PROVEN by render

1. **`SourceRead` follow-scroll never rendered.** It delegated smoothing to a
   CSS `transition`, which Remotion does not render, over an
   `interpolate(frame, [0,1], [offsetY, offsetY])` that interpolated a value to
   ITSELF — a no-op. The comment promised a glide the code never produced; the
   scroll hard-jumped. Now eased in frame-space over 0.45s.
   **VERIFIED BY RENDER, not asserted:** a scrollable test scene (1080x2340
   page in a 1920 frame) measured **-16, -9, -4, -1, 0 px** per 3-frame step
   across a line change — a decelerating ease-out. The first attempt at proof
   used september-preview scene 09, which is 1170x1640 -> pageH 1514 in a 1920
   frame and therefore NOT scrollable; zero motion there was correct and proved
   nothing. Build the test that can actually show the thing.
2. **`PromptCard`** carried a dead `transition: "all .2s"`.
`tools/lint_frames.py` now scans for CSS `transition` / `animation` /
`@keyframes` in `src/**/*.tsx`. Codebase currently clean.

NOTE: september-preview's source captures are 1170x1640 — neither the desktop
default nor our 1080x2340 mobile spec. G29 passes them (portrait, >=1000px
wide) but they are shorter than the frame, so `follow` can never engage.

## 2026-08-14 (7) — portability verified by simulating a fresh machine

User asked whether the folder can simply be copied to another MacBook. Tested
rather than reasoned about: rsynced the repo minus the regenerable and
per-reel bulk into a clean directory and ran `doctor.py` there.

RESULT: **11 MB, 465 files.** All 20 skills present, **no broken symlinks**,
config valid, avatar registry intact, sfx catalogue complete, all 57 gate
self-tests passing. Doctor failed on exactly ONE thing — `node_modules` — which
is correct and is what `npm install` is for.

FIXED FIRST, because it WOULD have broken: `.claude/skills/{news-reel, social,
video}` were **absolute symlinks** into `~/Faceless YouTube Channel/`. On any
other machine those resolve to nothing and the pipeline skill silently
disappears. Replaced with real directories inside the repo, which is now the
canonical copy. The Remotion skills were already relative symlinks
(`../../.agents/skills/...`) and survive a copy untouched.

ALSO VERIFIED: `setup.sh`'s whisper URL. The sha256 in the URL path segment
matches the local `base.pt` byte-for-byte — I had written that URL from memory,
and a wrong one would have failed only on the new machine, which is the worst
place to find out.

CAVEAT recorded in CLAUDE.md: the test ran on THIS machine, so ffmpeg/node/
whisper/yt-dlp resolved because they are installed here. On a genuinely new Mac
those are missing; setup.sh installs all but ffmpeg, and doctor names whatever
is left. The HeyGen connector is client-side and does not travel.

## 2026-08-16 — styles are named for what they ARE, not who they came from

**Rule.** A style id describes the style, the way a format id describes the
genre. `editorial` and `utility`, not `varun-mayya` and `nick-saraev`. The
caption treatment follows the same rule: `word-reveal`, not `nick-display`.

| was | now | what it is |
|---|---|---|
| `varun-mayya` / `varun` | **`editorial`** | tech-news reporting: claim -> receipt -> demo -> take |
| `nick-saraev` / `nick` | **`utility`** | tips and tools: designed artifacts, comment-gate CTA |
| `nick-display` | **`word-reveal`** | per-word caption reveal, emphasis drives the accent |
| `varun-script-playbook.md` | **`editorial-script-playbook.md`** | the WORDS for editorial |

**Why.** The creator names were a research artifact — they recorded whose reels
we tore down, which mattered while deriving the numbers and stopped mattering
once the numbers were in `FORMATS`. They cost us on two axes. They said nothing
about when to reach for a style, so the choice had to be memorised rather than
read. And they sat beside `news` / `top5` / `comparison`, which are named
correctly, so the two axes looked like different kinds of thing when they are
not. The teardown provenance is not lost: it stays in the pack headers and in
`_derived` on each `FORMATS` profile, which is where provenance belongs.

**Legacy ids resolve forever.** Seven reels were published carrying
`varun`/`varun-mayya`/`nick`/`nick-display`. `STYLE_ALIASES` and
`CAPTION_ALIASES` in `tools/reel_gates.py` are the single source of truth;
`validate_job.py` imports them rather than keeping a copy, and
`src/theme/tokens.ts` and `tools/manim_theme.py` mirror them for their runtimes.
Rewriting a shipped beat sheet to satisfy a rename is the retro-fixing RULES.md
forbids. Do NOT add entries — a new style gets a canonical name, not an alias.

**What the rename uncovered.** Three producers were stamping values their own
validators rejected, all the same shape — the checker was fixed, the producer
was not:

- `compile_shot_plan.py` wrote `captionStyle: "chip-lg"`, retired 2026-07-30 and
  rejected by both `validate_job.py` and G10. **The generic new-reel path had
  been dead**, and nobody noticed because all seven reels were built by bespoke
  `tools/build_*.py` scripts that set the value themselves.
- `compile_shot_plan.py` also wrote `style: "nick"`, and `new_job.py` wrote
  `style: "nick-saraev"`, while `config.json` defaulted to the editorial pack.
- All three now read `config.json`, per the standing rule that locked settings
  live there and never inline in a build script.

**And the self-test was under-reporting.** The total was `len(CASES) + 1`, which
counted only the failure cases — adding a passing case did not move the number.
It printed 57 while running 61. Now every assertion increments a counter: **64**.

**Rule going forward.** A new style pack is named for its editorial function.
If the name would only make sense to someone who watched the reference reels,
it is the wrong name.

## 2026-08-16 (2) — runtime is chosen from the topic, and 120s is the wall

**Rule.** A format's `runtime` band is the DEFAULT, not a cap. When the topic
earns more time, set `allowLong: true` + `allowLongReason: "<one line>"`.
**`RUNTIME_CEILING = 120s` is absolute** — `allowLong` cannot pass it.

**Why.** The bands are measured and worth keeping as the default: 60-80s for
news came out of an 11-reel teardown, 26-48s for top5 out of twelve. But a band
derived from someone else's reels should not decide how long OUR story needs to
be when the story is genuinely bigger. Padding to reach a floor and amputating
to meet a ceiling are the same error in opposite directions.

**What was actually missing.** `allowLong` already existed and already demanded
a written reason — so topic-driven runtime was the design all along. What it did
not have was a **ceiling**. Set the flag with any reason string and a "reel"
could run ten minutes: an unbounded opt-out of the one gate that keeps these
things short form. That hole existed from the day the flag was added and nothing
caught it, because a gate with an escape hatch reads as governed.

`allowLong` was also **never declared in `src/types.ts`** — enforced by the gate,
invisible to the type. Both fixed.

**The ceiling is USER-SET, not derived** — recorded plainly so nobody later
mistakes 120 for a measured number the way the comparison timings almost were.
Reels and Shorts both allow 3 minutes, so the platform is not what binds here;
retention is. The reason line exists to make the author say out loud what the
viewer gets for the extra time.

**Tests.** Three assertions, written against G02 specifically rather than a
whole clean sheet — making BASE legitimately 100s means repeating scenes, which
trips G06/G07/G08 for reasons unrelated to runtime, and a test that fails for
the wrong reason is worse than no test:

- 100s news with no `allowLong` -> G02 fires
- 100s with `allowLong` + reason -> G02 silent
- 125s with `allowLong` + reason -> G02 fires on the wall

Suite: 64 -> **67 checks**.

## 2026-08-16 (3) — the ceiling is the PLATFORM limit: 180s

**Revises (2) the same day.** `RUNTIME_CEILING` 120s -> **180s**, per the user:
Instagram Reels and YouTube Shorts both allow up to 3 minutes, so the wall
should be the platform's, not a number we picked.

**What this changes, and it is not nothing.** At 120s the ceiling still carried
an editorial opinion — it said "past this it stops being short form" in our
voice. At 180s it says only "past this the platform refuses the upload". The
ceiling has stopped being a brake. **`allowLongReason` is now the only editorial
brake between the measured band and the wall**, which makes that one line the
load-bearing part of the rule rather than a formality. A reason that would not
survive being read aloud to a viewer is not a reason.

The bands are untouched and still measured: news 60-80s, top5 26-48s. The
default is unchanged; only the outer limit moved.

**Known scaling gap, recorded rather than quietly inherited.** G08 asks for 6-9
SFX cues *no matter how long the reel is*. Measured on what we have actually
shipped:

| reel | runtime | cues | density |
|---|---|---|---|
| seedance-25 | 47.6s | 9 | 1 per 5.3s |
| september-preview | 79.6s | 7 | 1 per 11.4s |
| iphone18-split | 93.1s | 8 | 1 per 11.6s |
| apple-pay-india | 100.8s | 8 | 1 per 12.6s |
| grok-bot | 106.8s | 8 | 1 per 13.4s |
| made-by-google-26 | 135.2s | 6 | 1 per 22.5s |

Mean across all seven: **1 cue per 12.1s**. At 180s the same 6-9 rule permits 1
per 20-30s — sparser than every reel we have made except the one that already
ran longest. The number was derived on 60-80s reels; stretched to 180s it
silently stops meaning "sparse but present" and starts meaning "nearly absent".

**Do not fix this by guessing a bigger count.** Re-derive G08 as a per-minute
density from a real teardown, the way every other number here was derived. Until
then, anything past ~120s should be treated as carrying an unmeasured sound
rule. Same class of debt as the comparison timings, and recorded the same way.

## 2026-08-17 — the credit ceiling is a SCRIPT CONSTRAINT, and nothing checks it

ios27-tiers reached the generation step with everything else green — doctor,
67 gate self-tests, story verified from primary sources, 9 assets cropped and
verified on frame, script approved (hash `a23c17909555a633`) — and then HeyGen
refused it: `AVATAR_IV_VIDEO_GENERATION_OUT_OF_CREDIT`, 39 premium credits
remaining against the ~42 a 123-132s master needs at the measured ~0.34
credits/sec. Three credits short, after all the work that assumed it would run.

ROOT CAUSE: **runtime is priced, and the price is invisible to every check we
have.** G02 asks whether a runtime is editorially allowed (band, or `allowLong`
+ reason). Nothing asks whether it is affordable. `allowLong` therefore reads as
"the user approved the length" when it also means "this now costs ~40% more
credits than a band-compliant reel". The longer the approved script, the larger
the unhedged bet.

Sharpest form: **an approved script is a purchase order.** `script_approval.py`
already computes words and a delivery range, so it already knows the credit
cost; it just never says it.

RULE (prose today, and prose is exactly what this ledger says gets skipped):
- Before `approve`, state the credit cost of the runtime alongside the seconds,
  and check it against the balance. `propose` prints "331 words -> 123-132s";
  it should also print "~42-45 credits, balance 39 -> SHORT BY 3".
- `allowLong` must carry its credit delta in the reason, not just an editorial
  argument. A 125s reel is ~14 credits more than an 80s one — a third of a
  monthly cycle's headroom at 436/month.
- The balance cannot live in `doctor.py`: the HeyGen connector is configured in
  the Claude client, not the repo, so no repo tool holds a key. The check has to
  happen at the point where an agent CAN call the API — the approval step.

NOT YET CODE, so treat it as unenforced: making this a gate needs the balance
passed into `script_approval.py` by the agent that can read it. Until then it is
the operator's job, which the 2026-08-14 (4) entry warns is where rules go to
die.

Credits reset 2026-08-22T09:06Z. The reel is complete up to the master and
blocked only on generation.

## 2026-08-17 (2) — ios27-tiers: the linter passed a reel with 14 broken scenes

The reel passed doctor, all 67 gate self-tests, `check_beats`, `validate_job`
AND `lint_frames.py` ("no blocking flags") — and 14 of its 50 scenes were
defective. Every defect was caught by reading frames, none by automation. Same
headline as 2026-08-14 (4): the gates approved it, so the gates were wrong.

**DEFECT 1 — every underline was a strike-through, which inverts the meaning.**
`AnnotateZoom` draws the bar at `a.y + a.h + barH*0.6` — BELOW the region you
pass. I passed `h` as the LINE PITCH, so "below line 1" landed exactly on line
2. On Apple's device list the accent bar struck through "iPhone 14 Pro Max"
while the VO was about "iPhone 15"; on the tier footnote it struck through
"iPhone Air, iPad models with M4…", dragging in the iPad clause the beat was
written to exclude.
RULE: **`h` is the GLYPH height (~0.6 x line pitch), never the pitch.** The bar
then lands in the inter-line gap. RULES.md already said "highlights go around
data, never over it" — it never said how the component computes that.

**DEFECT 2 — a wide source makes AnnotateZoom 50-84% dead space.**
`cardW = width*0.9; cardH = (srcHeight/srcWidth)*cardW`. The card inherits the
SOURCE aspect, so a 942x205 footnote crop (4.6:1) becomes a thin horizontal
band floating in a 1920-tall frame of blurred fill. Measured: 4.6:1 -> ~16%
frame fill.
RULE: **feed `annotatezoom` a PORTRAIT source (<=1:1.4) and let `focus` move the
camera between paragraphs.** Do not crop one thin strip per quote. Crop ONE tall
page region and mine it for 2-3 focus rects — that is also a different shot each
time, so it satisfies the variety rule instead of fighting it. Five thin crops
collapsed into two 1080x2280 receipts here. RULES.md carried the >2.5:1 warning
for `receipt` only; it applies at least as hard to `annotatezoom`.

**DEFECT 3 — page chrome rendered on screen, and dodging it did not work.**
Apple's local nav (`Overview / iOS / macOS / iPad`) is STICKY and overlays the
footnote block. Starting the focus rect below it was not enough: the camera
zooms wider than the focus rect, so the bar came into frame anyway.
RULE: **kill chrome AT CAPTURE, never by framing around it.** In the capture
script, hide every `position: fixed|sticky` element before screenshotting. On
apple.com that removed 5 elements and did NOT reflow the page, so measured
coordinates survived.

**AND THE SAME MISTAKE REPEATED ONE RENDER LATER**, which is why this is stated
twice. After fixing Apple's sticky nav I left 9to5Mac's "Discover more"
related-links widget in the 9to5-notes asset, reasoning that no `focus` rect
pointed at it. It rendered on screen anyway: **AnnotateZoom's visible window is
larger than the focus rect** — the card is positioned by the focus centre, and
whatever else falls inside the 1080x1920 viewport comes with it. A focus rect is
not a crop.
SHARPEST FORM: **if chrome is anywhere in the asset, assume it will be on
screen.** Cut it out of the file (here: 1080x2280 -> 1080x1055) or hide it at
capture. Never rely on where the camera is pointed.

**A PNG in `footage` or `floatcard` renders BLACK.** Both render a Remotion
`<Video>`. Only `split` (branches on file extension), `receipt` and
`annotatezoom` take an `<Img>`. Caught before the first render, but only by
reading the component — nothing warns.

**Two MG specs were silently wrong against `src/types.ts`:** `wordcascade` takes
`words:[{text,style,at}]` (not `lines`), `chart` takes `items[]` + `source` (not
`rows`/`footnote`). Both would have rendered EMPTY and no gate checks MG shape
against the type union.

**A stale-asset race produced a clean-looking render of the wrong file.**
The corrected capture landed at 12:58:13; the render had finished at 12:56:07.
The beat sheet was right, the PNG on disk was right, the MP4 was wrong, and
nothing flagged it.
RULE: after replacing any asset, **compare the asset mtime against the output
mtime before believing a frame**. `ls -la` on both is cheap; a re-render is not.

NOW CODE, with self-tests (suite went 67 -> 69 checks):
- **G35** rejects a PNG `src` on `footage`/`floatcard` (the black-frame bug).
- **G36** rejects an `annotatezoom` source wider than **2.5:1**. NOTE ON THAT
  NUMBER: I first set it to 1.45 and `test_gates.py` immediately caught me —
  1.45 rejects the baseline sheet's 16:9 source, a shape that shipped fine on
  iphone18-split and made-by-google-26. I had only MEASURED failures at 2.6:1
  and above, so the threshold is the 2.5:1 wide-artifact line RULES.md already
  sets for `receipt`. G23 discipline applies to gate thresholds too, and the
  suite enforced it on me within a minute.

STILL PROSE, so treat as unenforced:
- a gate validating MG scene shape against the `Scene` union — `wordcascade`
  took `lines` instead of `words[]` and `chart` took `rows` instead of `items[]`;
  both would have rendered EMPTY and nothing checks MG shape against the union.
- a lint check that output mtime > every referenced asset mtime.
- a check that no `position: fixed|sticky` element survived into a capture.

## 2026-08-17 — the self-test claimed coverage it did not have

**Rule.** `test_gates.py` now asserts that **every declared gate id has a
failing case**, and fails naming the gaps.

**Why.** The suite's last line reads *"every gate fires on its violation."* That
was not true. It asserted gate ids were UNIQUE and never asserted they were
COVERED, so **G13** (a clip shorter than the beat that plays it) and **G16**
(standard visual notation) had no failing case at all — two gates sitting in the
build with nothing proving they still work, behind a green line saying they did.

Exactly the failure this suite exists to prevent, one level up: the gates check
the reel, and nothing was checking the gates.

Both now have cases. G13 needed its own helper because it reads `clip_durations`,
which the shared `expect_fail` does not pass — that missing parameter is likely
why it was skipped originally.

**The coverage check was itself verified** by injecting a `# G99 — ` header with
no test and confirming the suite fails naming G99. A check that cannot fail is
decoration.

**Also corrected: the counts in the docs were wrong.** 35 gate ids, not 33; 72
checks, not 67. The earlier figures were read off stale output and repeated into
MIGRATION.md — the same prose-drift this repo keeps finding. The numbers now
come from a live run.

| | was documented | actual |
|---|---|---|
| gate ids | 33 | **35** |
| self-tests | 67 | **72** |

## 2026-08-17 — two-machine merge, and two real bugs in the sync procedure

Applied Mac 2's bundle to Mac 1. Did NOT follow §6.2 literally, because
following it would have destroyed work.

**THE HISTORIES WERE UNRELATED.** Mac 2 was set up from the tar.gz archive and
then `git init`ed independently, so its root (`1ca11f1`) shares no ancestor with
Mac 1's (`136b4b6`). `git merge-base` returned nothing.

**BUG 1 IN §6.2 — the guard checked the wrong thing.** It ran
`git status --porcelain` and stopped only on UNCOMMITTED edits. That was clean.
Meanwhile Mac 1 held six local COMMITS the bundle had never seen, including the
entire `iphone-fold-ultra` reel (12 files) and the G09 `noMusic` opt-out.
`reset --hard` would have deleted all of it and reported success. The check that
matters is `git log --oneline HEAD --not sync/main`, and it was absent.

**BUG 2 — `git merge FETCH_HEAD` silently no-ops.** `git fetch sync` writes the
tip to `refs/remotes/sync/main` and marks `.git/FETCH_HEAD` **`not-for-merge`**.
`reset --hard FETCH_HEAD` works (reset reads the SHA), but `merge FETCH_HEAD`
prints "Already up to date" and changes NOTHING. I hit exactly this: the merge
appeared to succeed with zero conflicts, which contradicted the merge-base
result and was the tell. Merge `sync/main`, never `FETCH_HEAD`.

**RESOLUTION.** Pushed Mac 1 to GitHub first plus a `pre-sync-2026-08-17` tag,
so the pre-merge state is recoverable. Then merged with
`--allow-unrelated-histories`: 50 conflicts, resolved by taking sync/main
wholesale (strictly ahead — 35 gates, editorial/utility rename, 180s ceiling,
coverage assertion, Apple-Silicon ffmpeg finding, .zshenv fix) and re-applying
Mac 1's one unique gate change, the G09 noMusic opt-out, plus a self-test case
for it that sync did not have.

**VERIFIED AFTER, NOT ASSUMED:** 35 gate ids all unique; coverage says all 35
have a failing case; **73 self-tests pass**; skills 29, sfx 16, scene types 42 —
matching the §1.2 baseline exactly; tsc clean; doctor ok with the two expected
§6.3 warnings (manim, chatterbox venv); iphone-fold-ultra present and
re-registered in generatedBeatSheets.

LESSON: a sync procedure whose safety check cannot see the thing it is meant to
protect is not a safety check. The same class as the earlier
`gh api contents/<path>` test that reported five excluded directories as
PRESENT — a verification that cannot fail is not a verification.

## 2026-08-17 (2) — second sync, and the payoff for merging instead of resetting

Applied Mac 2's second bundle. **Zero conflicts, where the first sync had 50.**

The reason is the previous decision: because that sync was a MERGE and not a
`reset --hard`, Mac 2's tip (`5e9a6cf`) is inside this history — so this time
`git merge-base` found it and the merge was ordinary. Resetting would have
thrown that ancestry away and left every future sync fighting 50 conflicts
again. The corrected §6.2 checks worked exactly as written: (a) one uncommitted
edit, committed first; (b) 8 local commits the bundle lacked; (c) merge-base
present -> merge, not reset.

**VERIFIED THAT BOTH SIDES SURVIVED THE AUTO-MERGE**, rather than trusting
"0 conflicts" to mean "nothing lost". `MIGRATION.md` had changed on both sides:
this machine's two §6.2 bug fixes (local-commits check, FETCH_HEAD
not-for-merge warning) AND Mac 2's `install_global_skills.sh` reference are all
present. A clean auto-merge can still silently drop one side's intent.

One false alarm worth recording: `git ls-files | grep iphone-fold-ultra` showed
11 files where 12 were expected, which read as a deleted build script. The file
is `tools/build_iphonefoldultra.py` — no hyphens — so the hyphenated grep missed
it. **The pattern, not the repo, was wrong.** Check the search before believing
the absence.

**GLOBAL SKILLS NOW INSTALLED HERE.** `tools/install_global_skills.sh` (from the
bundle) installed all five — find-skills, humanizer, fact-check-workflow,
youtube-seo, thumbnail-design — and verified each on disk. They had never
existed on this machine: §6.3 says they cannot travel in git, and that was true
rather than theoretical.

**FULL INVENTORY, both machines now level:**
- 29 in-repo skills: 12 Remotion, 9 HyperFrames (`hyperframes-*` + `media-use`),
  8 pipeline/advisory. 8 real directories, 21 relative symlinks, **0 broken**.
- 5 global skills in `~/.agents/skills`.
- 35 gates, all ids unique, coverage complete, **73 self-tests pass**.
- sfx 16, scene types 42, tsc clean, doctor ok with the two expected §6.3
  warnings (manim, chatterbox).

## 2026-08-17 (3) — chatterbox installed, and it was broken until fixed

User asked to install `resemble-ai/chatterbox` "as a skill" to clone the
avatar's voice. **It is not a skill** — it is Resemble AI's Python TTS library
(MIT). Our own §6.3 already listed it as a per-machine install; doctor had been
warning about it since the merge.

**THE VENV HAZARD IS REAL, now proven rather than warned about:**
chatterbox-tts pins **torch 2.6.0**; the system runs **2.13.0** under whisper.
Installed into `~/.venvs/chatterbox`, both survive — verified after the install
that system torch was still 2.13.0 and whisper still imports. A system-wide
install would have dragged torch back seven minor versions and broken the
transcription the whole edit anchors to.

**IT DID NOT WORK OUT OF THE BOX.** First generation died with
`'NoneType' object is not callable` at `perth.PerthImplicitWatermarker()`.
Root cause: `perth/perth_net/__init__.py` does
`from pkg_resources import resource_filename`, **setuptools 81+ removed
pkg_resources**, and the venv had 84.0.0 — so perth's submodule import failed
SILENTLY, leaving the class as `None`. Fixed by pinning `setuptools<81` in the
venv (80.10.2), which RESTORES the watermarker rather than bypassing it. Do not
"fix" this by skipping the watermarker: it is the provenance mechanism.

**CLONE QUALITY, MEASURED:** reference (real HeyGen VO) median f0 **170.2 Hz**,
clone **170.2 Hz** — a **0-cent** difference, pitch sd 268 vs 240 cents. Same
speaker. The clone took.

**WATERMARK VERIFIED BOTH WAYS:** `cloned.wav` -> perth score **1.0**,
`reference.wav` -> **0.0**. So chatterbox rehearsal audio is always
distinguishable from real VO. It is NOT a substitute for the shipped voice.

**PACE DIFFERS AND MUST BE CALIBRATED:** the clone ran **3.11 wps** against
HeyGen's measured 2.35-2.75. A raw chatterbox duration is therefore NOT a
HeyGen prediction. `tools/voice_clone.py calibrate` measures the ratio against
real masters (first 40 words of each, compared to HeyGen's own word timings) and
`speak` applies it and prints the basis. Uncalibrated, it says so.

**`tools/voice_clone.py`** — `ref` / `speak` / `calibrate`. The point is that
the approval gate blocks on the SLOWEST plausible pace, so borderline scripts
get rejected that would have been fine; a free local rehearsal narrows that.

**DOCTOR HARDENED.** It only checked that the venv DIRECTORY existed — which it
did, while chatterbox was entirely broken. It now runs a probe in the venv
asserting `perth.PerthImplicitWatermarker is not None`, the exact thing that was
silently missing. Same class as the absent Pillow and the `.zshrc` PATH: the
tool is installed, the check just never looked at it.

## 2026-08-18 — airpods-camera (Apple's camera AirPods demo found in macOS 26.7 RC)

**RAW NOTE (user, mid-build):** "Apple never confirms or announce until unless
their official events or press release. So you should not worry about official
Apple announcement, just follow the news (rumors and leaks)."

**ROOT CAUSE:** the script spent a beat saying "But Apple has announced none of
this." Apple announces nothing before an event or a press release, so that
sentence is a tautology dressed as diligence — it costs runtime and signals we
do not trust our own sourcing. Same failure class as apple-pay-india v1's 10%
hedging budget (2026-08-11), reached from the opposite direction: not hedging a
weak source, but disclaiming a strong one.

**DISTILLED RULE:** never spend a beat telling the viewer that Apple (or any
company that only confirms at events) has not confirmed something. Report the
leak, credit who reported it, move on. The honesty beat still belongs in the
reel — make it an OBSERVATION about the evidence, not a disclaimer about its
absence. Here it became "in Apple's own video, you never once see the camera",
which is stronger reporting than the disclaimer it replaced.

**SECOND USER NOTE:** "use demonstration video instead of ad". ROOT CAUSE: I
called the file an "ad" three times. MacRumors and Macworld both call it a demo
/ instructional video; "ad" was my characterisation and it was the only
interpretive word in an otherwise fully sourced script. RULE: when outlets have
a word for the artefact, use THEIR word. A synonym that upgrades the claim is a
claim.

### Findings from this build

- **The two enforcers disagree about pacing, and the linter is the stale one.**
  `reel_gates.py` classifies G04 (held-layout ceilings) as ADVICE, per the
  2026-08-17 constitution: only the three rules plus RENDER and RIGHTS block.
  `tools/lint_frames.py` still treats [PACING] as a HARD flag and exits 1. So a
  sheet that passes the authority fails the linter on a rule the authority
  demoted. Shipped with `--soft` and declared. **Someone should reconcile
  lint_frames' hard-flag list with BLOCKING_RULES** — a check that blocks on
  taste is exactly what the restructure removed from reel_gates.
- **G13 does not fire from the CLI.** `reel_gates.py <slug>` never populates
  `clip_durations`, so the gate that catches "clip shorter than its beat"
  silently passes. Six of six footage beats outran their clips on the first
  compile and the gates said nothing; it was caught by probing every clip by
  hand. This is a RENDER-category rule (a short clip freezes on its last
  frame), so it should not depend on the caller.
- **`compile_shot_plan.py --force` does not exist.** The overwrite guard tells
  you to re-run with `--force`, but the flag was never registered with argparse,
  so it errors. The only way past is deleting the sheet by hand — the exact
  destructive act the guard exists to prevent.
- **The compiler's caption source is wrong.** It splits "Apple's" into
  `apple` + `s` so phrase anchors can match, then builds captions from those
  split tokens — rendering "apple s own." and tripping G34/G21. Captions must
  come from the ORIGINAL whisper words. Handled here by
  `tools/finalize_airpods_camera.py`; worth moving into the compiler.
- **Whisper mishears are not mispronunciations, twice over.** The full-pass
  transcript read "warns" as "wants" and "MacRumors Aaron Perris" as "Mac
  rumors are in Paris". Re-running `small` on the isolated 2s slices returned
  "warns" correctly, and biasing with `--initial_prompt` returned the name
  correctly — proving the audio was right both times. **No credits were spent
  on a re-record.** The rule works; use it before assuming the voice is wrong.
- **A shot plan built on estimated word timings will not fit the footage.**
  The first plan needed 18.2s of footage from a 13.2s source. Splitting long
  beats across more visuals brought it to 12.1s against 10.5s usable, closed
  with a 1.0-1.25x slowdown baked into the clips with `setpts`. Do the footage
  BUDGET before cutting: sum the beats, compare to the usable source, and only
  then choose windows.
- **`-t` after `-i` truncates a slowed clip back to the source length.** With
  `setpts`, the trim must be an INPUT option (`-ss X -t LEN -i src`) or ffmpeg
  cuts the stretched output back down and the slowdown silently does nothing.
- **PriceLadder is for a price CHANGE, not a price COMPARISON.** Given one
  current price and "costs more", it struck through $249 on both rows, which
  reads as a price cut that never happened. A component whose animation asserts
  something the data does not is a factual error, not a styling choice. Used a
  specsheet instead.
- **A built `uidialog` invents UI.** Rendering Apple's alert string in a dialog
  added Cancel/OK buttons no source describes, and read as 78% dead space
  besides. Replaced with a credited crop of MacRumors' own paragraph. Build UI
  only when the whole dialog is known.
- **Dead space is what the dark MG components do at 1080x1920 with 2 rows.**
  Six scenes flagged 75-83% flat. Fixed by giving `specsheet`/`timeline` a
  `bgSrc` bed (a darkened, heavily-slowed plate of the source footage) and
  giving `wordcascade` a `bottomSrc` facecam. Both fill the frame without
  inventing content. `bottomSrc` does NOT count toward G06 facecam share.

### Treatment history

- airpods-camera (Apple's camera AirPods demo, found in macOS 26.7 RC): split
  hook (Apple's OWN 2160x3840 vertical demo top / face bottom) with serif
  headline build APPLE'S OWN DEMO -> NEVER ANNOUNCED; SIX distinct shots mined
  from ONE 13.1s source (establishing loft, walk-in, the raise, the held book,
  a 1.25x punch-in on the AirPod in-ear, a defocused outro plate), each cut to
  its beat with a 1.0-1.25x `setpts` slowdown; NEW `sourceread` on the
  @aaronp613 post (X app chrome cropped off the top); MacRumors receipts x3 as
  SEPARATE CROPS of one full-page capture (headline+lede block, the Siri-quote
  paragraph, the hair-alert paragraph) rather than one page mined for regions;
  specsheets x3 (B790 / infrared-not-a-lens / the price) all on a darkened
  slowed-footage `bgSrc` bed; timeline (SEP 2026 B790); cascades x3 (macOS
  Tahoe 26.7 + release candidate / NO PHOTOS + NO RECORDING on cream / AirPods
  Pro 4 or AirPods Ultra), two of them with facecam bottoms; endquestion over
  the defocused plate. Facecam 21% in 8 pops. Digital twin, avatar_v, native
  1080x1920. 25 scenes / 72.9s / -14.0 LUFS.
- Used here, avoid repeating next reel: the `bgSrc` darkened-slowed-plate bed
  behind data cards, the one-source-mined-into-six-shots structure, and the
  cascade-with-facecam-bottom.
- NOT used (available again): categorygrid, statcard, chart, annotatezoom,
  settingspane, uidialog, priceladder, logoassemble, black typecard, hcompare,
  comparesplit, checklist, xpost, floatcard.

### 2026-08-18 — airpods-camera v2 (user feedback after first delivery)

**RAW NOTE (user):** "1. Caption overlaps the credit (source across the video)
2. Background music is too low. Let's remove background music from this video.
However, use the sound effects."

**FIX 1 — CAPTIONS vs CREDITS. This was systemic, not a one-off.**
ROOT CAUSE: `Credit.tsx` sits at `CREDIT_Y` 0.78 = **422px** up from the
bottom. `CaptionChips` defaults to **400px** up. The two are 22px apart, so the
caption chip lands on the credit on EVERY credited scene of EVERY reel — not
just this one. It shipped because a contact sheet at 150px wide does not
resolve a 22px offset; it was only visible on a full-res crop of the credit
band.

**DISTILLED RULE:** a scene that renders a `credit` must set `captionBottom`.
Push captions **UP** (520 works: chips occupy 520-584, clear of the credit's
422-482), never DOWN. `captionBottom: 300` looks like it works and is a Rule 1
violation — 300px up is y 0.844, and Instagram's account row is measured at
y 0.835, so it puts the caption under the platform's own chrome.

On `receipt` and `sourceread` scenes, set `captionBottom: 6000` (hidden)
instead: the highlighted source text IS the sentence being spoken, so a chip
repeating it breaks "one text system at a time" (RULES section 6) as well as
colliding with the credit.

**This deserves a gate.** Both numbers are known at build time — a scene with a
`credit` and a `captionBottom` inside [credit-60, credit+60] is checkable, and
so is a `captionBottom` below the account row at y 0.835.

**FIX 2 — MUSIC OFF, SFX KEPT.** Set `noMusic` + `noMusicReason` on the sheet
(G09's documented escape hatch, same shape as G02's `allowLong`) and drop the
`music` key. The 9 SFX cues are untouched. VERIFIED BY MEASUREMENT, not by
assertion: speech gaps read **-57.0 dB RMS** (a bed sits near -28), while the
sampled cues read -10.6 to -18.9 dB — at or above the -17.3 dB speech
reference. Master still lands -14.0 LUFS.

**`scripts/validate_job.py` did not know about `noMusic` and hard-failed.**
Same staleness as its opening-scene check: `reel_gates.py` added the hatch on
2026-08-17 and this second, older validator was never updated, so a sheet that
PASSED the authority failed here on a rule the authority already allows an
argued exception to. Taught validate_job the same contract, reason string still
mandatory, and checked both failure modes still bite (no music + no hatch
fails; hatch with an empty reason fails). **Rule: when reel_gates grows an
escape hatch, validate_job needs it too — two enforcers, one contract.**

**PROCESS NOTE, and this one nearly shipped a wrong claim.** After the music
change I measured loudness and pulled frames — and reported them — from a file
that had NOT been re-rendered: `render_job.py` had aborted at validate_job, so
`out/*-final.mp4` was 20 minutes stale. **Always check the output file's mtime
against the clock before reading anything off it.** A render that fails early
leaves a plausible, complete, WRONG artifact sitting exactly where the fresh
one belongs.

## 2026-08-19 — iphone-18-pro (iPhone 18 Pro feature roundup, 72.5s)

First reel built to the user's **iGeeksBlog narrative framework** (supplied
mid-session, after a first script was written and rejected). The framework's
rule 1 — *never open with an isolated fact* — killed the original hook ("For the
first time, an iPhone lens will physically open and close"), which was a good
sentence and a bad opening: it named a mechanism before naming the product.

**DISTILLED RULE — context before fact, promise before detail.** Beat 1 answers
*what are we talking about and why now*; the curiosity gap is planted in the
same breath and PAID OFF later. Here: "…including one that only matters when you
have no signal" (0:08) → "Back to that signal." (0:49) → 5G via satellite. The
user's own retention ladder is the acceptance test, not the word count.

**The design beat moved because of that ladder.** v2 put the colours/back
between the satellite payoff and the conclusion — a colour fact interrupting the
climax. Folding it INTO the conclusion ("…even the frosted back it's wrapped in")
turned a seventh feature into the evidence for "this isn't just a camera
upgrade", and gave the supplied mockup its strongest placement.

### Six engine bugs the CONTACT SHEET found that no gate did

1. **Every "%" was dropped from captions.** whisper emits `%` as its own token;
   `normalize()` returns `[]` for it, so the caption loop `continue`d and threw
   it away — shipping "shrink about 35", "reportedly 15", "on 30". Numbers
   without units, against standard notation, on five separate cards. FIXED in
   `compile_shot_plan.py`: a punctuation-only token now glues onto the word
   before it. **Every past reel with a percentage has this defect.**
2. **Possessives split into an orphan chip.** "Apple's" normalises to
   `["apple","s"]` and each token was emitted separately → a caption chip
   reading just `s`. G34 caught it (it is the same class as the `,000` and
   `Pegatron T` cases). Fixed generally: contraction tails re-merge and the
   ORIGINAL spelling is restored for display.
3. **`-Chi` shipped as "Ming -Chi".** The hyphen-merge loop documented for
   `build_template.py` was never inherited by `compile_shot_plan.py`.
4. **Multi-word `caption_corrections` silently did nothing.** The key normaliser
   stripped every non-alphanumeric, so `"dark cherry"` became `"darkcherry"` and
   matched no token and no chunk. Now keeps interior spaces and applies phrase
   keys to the chunk text — which is also why `"dark"` alone must NEVER be
   mapped: this script says "in the dark" 20s earlier.
5. **`floatcard` renders `<OffthreadVideo>` — a still gives it ONE frame.** G35
   blocked it before render (it would have crashed). Stills for a floatcard must
   be cut to mp4; doing so also satisfies "nothing static".
6. **`EndQuestion` hardcodes YES / NO chips.** It was built for "WOULD YOU RUN
   THIS AD?". "Which one would make you upgrade?" cannot be answered yes/no, so
   the buttons contradicted the question. **RULE: `endquestion` is only for a
   binary question.** Anything else is a closing plate + kinetic type.

### A generated MG clip must COMPLETE inside the beat that plays it
The Dynamic Island clip animated 20.76mm → 13.49mm over 0.22–0.78 of a 4.6s
file, finishing at 3.59s — but the beat was 2.58s. The viewer watched it stop
near 17mm while the very next card claimed 13.49mm. Nothing flagged it; the clip
was long enough to avoid a freeze, so it looked correct everywhere except on the
frames. **RULE: time a generated animation to the BEAT, then leave tail; check
the last frame the beat actually reaches, not the last frame of the file.**

### loudnorm can overshoot its own true-peak target
`linear=true` applies ONE fixed gain, so a peaky master asked for TP −1.2 and
landed **−0.9**, over G31's −1.0 ceiling. Target moved to −1.5 and an
`alimiter=limit=0.83` added AFTER loudnorm as a hard ceiling in
`render_job.py` — the remedy RULES §11 already prescribed. General, not per-reel.

### G20 vs the pacing cap — a real conflict, resolved by component choice
A `checklist` is row-timed: G20 (blocking, R1) demands it be held long enough for
the last row to land (~1.95s + stagger), while the card pacing cap is 2.6s. At
3.28s it satisfied G20 and failed the linter; split to 1.46s it satisfied the
linter and failed G20. **A `specsheet` carries the same content under the 3.3s
BUILDING cap** — the fix was the component, not an override.

### Phrase anchors: avoid apostrophes, hyphens and proper nouns
`rehearse_vo --tts` reported 7 anchor misses, then a DIFFERENT 2 on a re-run —
chatterbox is non-deterministic, so chasing 18/18 against a randomly-mangled
synthetic transcript is chasing noise. What matters: an anchor is a BUILD-time
lookup, not audio, so a real miss costs nothing to fix after generation. Anchor
on plain words. And note the caption merges above CHANGE the matching stream —
fixing "Ming -Chi" merged `ming`+`chi`, which broke the anchor `"Analyst Ming"`.

### Pronounce-check a spec by WORD DURATION, not by whisper's text
`2nm` was the one real TTS risk (september-preview spelled it "2 nanometers").
whisper normalises numerals either way, so its transcript proves nothing. A ~3
credit probe measured the word at **1.16s** — nearly double "Apple's" (0.68s) and
consistent with a 5-syllable "two nanometer", not a 3-syllable "two-en-em".
Approved script shipped unchanged. **RULE: to test a spec's pronunciation,
measure the token's duration against a known neighbour.**

Related: that probe sentence ran ~1.8 wps and would have predicted ~100s for the
reel. The real master came back **72.49s (2.50 wps)**. A number-dense sentence is
a worst case, not a pace — never extrapolate runtime from one probe line.

### Derivative sheets and the two-enforcers rule (third time for validate_job)
`<slug>-nomusic` is the sanctioned music-free export, but `validate_job.py` AND
`script_approval.py` both resolved brief/script/manifest/approval against the
DERIVATIVE slug — demanding a duplicate job folder and a second copy of every
asset under `public/`. Both now fall back to the parent slug. This is the third
logged instance of `validate_job` being stale against a contract `reel_gates`
already accepted. **When a sheet variant becomes legal, every enforcer that
reads a path by slug needs to know.**

### Treatment history

- iphone-18-pro (iPhone 18 Pro feature roundup): split hook on a STILL pair
  (MacRumors mockup cropped tight to two camera plateaus, 1125x1000 so it fills
  the top half with no upscale) over facecam; **two generated MG clips** built
  with PIL+ffmpeg as scene assets, not engine components — an 8-blade aperture
  iris opening and closing, and the Dynamic Island shrinking 20.76mm → 13.49mm
  against a ghost outline of its original width; `hcompare` of two frames pulled
  FROM that iris clip; categorygrid used three ways (the promise map, the same
  map recalled with DISPLAY lit, and a two-state WIDE OPEN / STOPPED DOWN card);
  statcard x4; specsheet x4; wordcascade x6 on black; MacRumors receipt under
  "if the reports hold"; floatcard x3 on Ken-Burns mp4s of the mockup; closing
  plate = blurred-fill cherry phone + kinetic question (NOT endquestion).
  34 scenes / 72.49s / −14.0 LUFS / TP −1.6 / facecam 18.4% / 9 SFX cues.
- Used here, avoid repeating next reel: the generated-iris/island MG pair, the
  categorygrid-as-promise-map-then-callback device, and the blurred-fill closing
  plate.
- NOT used (available again): timeline, sourceread, annotatezoom, uidialog,
  settingspane, priceladder, logoassemble, chart, carousel, xpost, comparesplit,
  black typecard, checklist, designreveal.

### 2026-08-19 (2) — packaging, and a thumbnail composition that had never run

`--format wide` on `tools/make_thumbnail.py` produced a **black 1280x720 frame**
with a faint ghost of the image. No error, exit 0, plausible file size. Root
cause: in `Thumbnail.tsx`'s `Wide`, the radial-gradient backdrop is an
`<AbsoluteFill>` (position: absolute) while the two content columns were
`position: static` — and a POSITIONED element paints above a static one in the
same stacking context, so the gradient covered the text and the image. Fixed by
making both columns `position: relative`.

**It had never shown because no reel had ever generated a wide thumbnail** —
`out/thumbnails/` held only `-vertical` and `-grid` files. A code path with no
output is not a working code path; it is an untested one. Same shape as the
`[SKIP] PIL not installed` lesson: silence read as success.

**RULE: a Short's cover is the VERTICAL file, judged on `-grid.png`.** The 1280x720
is for the YouTube video page, not the Short. Generate both, look at both.

**Packaging counts, enforced not remembered:** Instagram 5 hashtags (it ignores
all of them past 5), YouTube 3-5 shipped against a 15 cap, hashtags in the FIRST
COMMENT never the caption, ALT TEXT on every platform.
`tools/packaging_check.py` is the authority.

**The manifest's honesty constraints bind the COPY too, not just the reel.** The
same five bans were carried into both captions: no "Apple announced/confirmed",
the ~10% battery is Pro Max ONLY (the smaller Pro is reported near flat), no
price, September 9 is expected not confirmed, and no f-stop range because the
reports disagree. A caption is where an unhedged claim is most likely to leak
back in, because it is written last and gated least.

## 2026-08-20 — camera-snap framing: `focusY`, `zoom`, and why one of the two gates advises

Added `focusY` and `zoom` to the `footage` scene so a locked-off talking head can
be re-framed BETWEEN cuts: consecutive scenes on one avatar clip, each a
different `focusX`/`focusY`/`zoom`, `zoomDir: "none"`, cutting on vo.json word
onsets. `from` carries the trim forward so lip sync never breaks. Before this,
framing could move sideways only, and only at a fixed 1.1x push.

**The idea came from evaluating a third-party skill we did NOT install**
(`kinetic-multicam`). Its route was to send the avatar master through Seedance
video-to-video — a second synthesis pass over a digital twin of a real face, a
second paid platform, and a text-prompt handoff outside `render_job.py`. The
technique underneath it — camera snaps timed to breath boundaries — was worth
having; the delivery mechanism was not. Taking the idea and leaving the vendor
cost two fields and two gates.

**`zoom` is the BASE the push runs from, not a replacement for it.** So a sheet
with no `zoom` renders byte-identical to before (base 1 -> 1 to 1.1). That
compatibility is the whole reason it was built this way rather than as a new
scene type.

**G48 blocks; G49 advises. The split is the point.** Both were written the same
afternoon, and only one earned a block:

- **G48 (RENDER, blocking)** — `zoom < 1`, or a focus outside 0..1. Below 1 the
  scaled layer stops covering the canvas; a focus past the slack `cover` gives
  it pushes the image off an edge. Both paint the black backdrop. The bounds are
  not a chosen number — they are exactly where the frame stops being covered,
  which is the same category as G35, a still in a video slot rendering black.
- **G49 (advice)** — `zoom` set together with a `zoomDir` push, so the scale
  compounds to `zoom * 1.1`. Easy to hit by accident, because `zoomDir` defaults
  to `"in"` when omitted and the field was added for locked-off snaps. But
  wanting a push FROM a tight base is a legitimate choice, so it asks the
  question instead of refusing the render.

Had G49 been given a ceiling — "no zoom above 2.0x" — that would have been taste
wearing a rule's badge, the exact fault the G18 note records. There is no
defensible maximum without the source resolution, and the beat sheet does not
carry it for footage.

**`focusX` had never been validated.** It has existed since the footage variant
did, and nothing checked its range; G48 covers it now because it fails the same
way. All 101 focus values across the 14 shipped sheets were in range, so nothing
was silently broken — but nothing would have caught it either.

**Still unproven: how it LOOKS.** A 16:9 master cropped to 9:16 has finite
headroom, and a hard snap can clip the face or push it under
`platformSafeArea.ts`. That is an [EYE] question no gate answers. Check it with
`tools/preflight_stills.py` (one frame per scene, ~36s) before committing a reel
to the treatment. It could not be checked on the machine this was written on —
a fresh clone with no footage.

## 2026-08-21 — script writing, enforced: the third weak draft was the last unforced one

The iphone18-colors first draft opened "Apple's new iPhone red isn't red" —
the framework's S16 failure verbatim, a paradox with no premise — and reached
the user raw. Same class as 2026-08-19, which is the second time, which is why
this entry is about ENFORCEMENT and not about writing advice. The framework
(`styles/shortform-script-framework.md`) was in the repo, named by the skill,
the formats and README-structure.md; `check_script.py` was calibrated and
FLAGS that exact opening. Everything existed. Nothing blocked. Prose for the
third time, then code:

- **`new_job.py` scaffolds `jobs/<slug>/structure.md`** — the S17
  shape-before-sentences decision, plus PROMISE, OPEN LOOP, WHAT->WHY->SO
  WHAT, WHAT WAS CUT, and SOURCES (two independent minimum, or say why one; a
  one-source brief is how thin scripts start). A file that exists gets
  filled; a file that must be remembered does not.
- **`script_approval.py propose` refuses** without structure.md, with unfilled
  placeholders, or with no S17 shape named. On success it writes
  `review.json`: the script hash, the structure hash, and the prose findings
  the user is being shown.
- **`approve` refuses** without a review whose hash matches the current
  script. "The user approved it" now provably means "the user saw THIS
  script, with these findings" — RIGHTS territory, same family as G27, one
  step earlier. The findings themselves stay advice; the constitution's craft
  line is untouched.
- **`check_script.py` gained the AI-tell scan** — the measurable half of
  "feels human". 36 phrases, CALIBRATED: every candidate firing on any of the
  9 approved scripts was dropped ("isn't just" is in approved iphone-18-pro;
  "the catch?" is in september-preview — a tell the user's own approved
  writing uses is their voice, not a tell). The unmeasurable half stays with
  the humanizer pass, step 5 of the binding order in the news-reel skill.
- **Self-test:** `tools/test_script_pipeline.py`, run by doctor — every
  refusal above has a failing case, per the founding rule.

**Registry search, documented verdict (user asked):** searched skills.sh for
script/storytelling/retention skills. Top hit `jackyshen-gen-short-video-script`
(2.5K installs) is a Hook->Content->CTA fill-in template — template-shaped
scripting is the framework's own S3 failure mode, so installing it would
codify the exact weakness being fixed. Nothing installed; what this repo has
(framework + calibrated checker + humanizer) is stronger than anything found.

**Cleanup in the same pass:** `references/writing-block-2.0.md` deleted — it
was byte-identical to the tracked `styles/shortform-script-framework.md`, and
two copies of a canonical text is how drift starts. The legacy
`scripts/<slug>.md` beat-map scaffold in new_job.py is gone too: nothing reads
that file, and the one it scaffolded for iphone18-colors sat unfilled in
scripts/ while the real work happened in jobs/. The news-reel skill also
stopped hardcoding one machine's absolute path as "the engine".

## 2026-08-21 (2) — research hardened the way scouting was: a ledger, refused when dishonest

Scouting got its discipline from a measurement — 229 assets carried `shows`,
18 carried a tier, so capture_plan made tier REQUIRED. Research had less than
that: `verified_facts` in the manifest is a convention no code reads, the
fact-check skill is advisory (in this repo's history: skipped), and the
iphone18-colors first draft was scripted off ONE source. Same recipe applied:

- **`jobs/<slug>/research.md`** (scaffolded by new_job.py): a claims ledger —
  CLAIM / TIER (official·multi·single·disputed) / SPOKEN / SRC — plus a dated
  SEARCHED log. The SPOKEN field is the `covers` discipline applied to
  research: the ledger names the exact script words each claim rides on, and
  `tools/research_check.py` verifies those words exist in the script. A
  ledger describing words nobody says is fiction wearing a record's badge.
- **REFUSED at propose** (the G41 half): missing/template ledger, a claim
  with no SRC url or invalid TIER, a SPOKEN phrase absent from the script,
  an empty search log.
- **ADVICE, never blocks** (the G42 half): a single/disputed claim spoken
  unhedged (framework S20's own vocabulary — reportedly/leaked/says/…), and
  fewer than two source domains without an `ONE-SOURCE-OK:` line. Sourcing
  depth is judgement; the record of it is not.
- **A known edge, kept on purpose:** "None of it's confirmed" trips the
  unhedged-advice because "confirmed" is NOT in the hedge list — adding it
  would silence "Apple confirmed X" spoken off one source, which is the
  exact sentence the check exists for. The advisory costs a glance; the
  blind spot would cost the rule.
- Self-tests in `tools/test_script_pipeline.py` (doctor runs them); the live
  example is jobs/iphone18-colors/research.md, written from sources fetched
  the same session.

What this cannot do, recorded so nobody oversells it: verify a search
happened, that a URL says what the ledger claims, or that a fact is true.
It verifies the record exists, is internally consistent, and matches the
script it describes. The last inch of research quality stays judgement —
same as the writing.

## 2026-08-21 (3) — the fresh-job path audited: three born-done stages and a manifest the blocking gate could not see

"Make research and scouting work at their best for all upcoming videos" meant
auditing the path every future reel actually takes — new_job.py -> showrunner
-> propose — instead of adding more machinery. Four defects, all fixed and
proven with a scaffold-to-propose dry run that left no trace:

- **new_job scaffolded `manifest.items` — the LEGACY key.** G11, a BLOCKING
  gate, resolves assetIds against `manifest["assets"]` only. Every fresh job
  started life invisible to the gate that protects it. Now scaffolds
  `assets`.
- **Born-done stages.** Scaffolding structure.md/research.md (yesterday's
  fix) defeated showrunner's `exists()` done-tests — three stages lit green
  on an empty job, and "Assets scouted" was done the moment new_job created
  the empty manifest. Done now means the WORK: structure filled and naming a
  shape (shared definition with propose via `structure_problems`), ledger
  structurally valid (`check_research(script_text=None)`), manifest carrying
  >=1 asset or a recorded `"thin": "<why>"` decision.
- **No research stage in the pipeline display.** Added between goal and
  scout, with the structural-only contract stated: the ledger starts at
  research time, SPOKEN fills at script time, propose verifies the join.
- **AGENT.md's manifest template taught a shape without `tier`** — the
  18/229 lesson, still being taught. Template now carries it, and names the
  two tier axes so they stop being conflated: asset tier is PROVENANCE
  (official/reliable/fallback, G42), claim tier is CORROBORATION
  (official/multi/single/disputed, research_check).

Two test-fixture lessons from the same pass, kept because they are the
checker teaching its own tests: a hedge one clause away legitimately covers
(the +/-12-word window), so an advisory case must isolate its claim from a
neighbour's hedge; and parse_ledger reads claims only inside `## CLAIMS`, so
a claim appended after `## SEARCHED` silently does not exist — the case
failed on its own fixture, which is exactly the failure mode the suite
exists to catch.

## 2026-08-21 (4) — the retention loop: our own reels finally feed the numbers

Every number in FORMATS came from teardowns of OTHER people's reels, because
at the time that was the only data there was. Published reels are the ground
truth nobody was using — and this pipeline holds an advantage no teardown
has: the beat sheet knows what is on screen at every frame.

**`tools/retention_ingest.py`** joins a published reel's retention curve to
its beat timeline and writes `jobs/<slug>/performance.json`:

- Input is the YouTube Studio "Audience retention" CSV export (zero setup)
  or the Analytics API rows (`elapsedVideoTimeRatio` ×
  `audienceWatchRatio`, 100 points/video). v1 does NOT do OAuth — the join
  is the value, fetching is commodity. Instagram exposes no per-second
  retention at all; its aggregates get noted by hand in packaging.md.
- Output: per-scene watch-in/watch-out, pp lost per on-screen second,
  ranked per-TYPE bleed table, worst single scenes, and REPLAY upticks
  (audienceWatchRatio rising means people rewound — on a spec card that is
  a compliment, not an anomaly). `--aggregate` sums across every ingested
  reel.
- Honest limits, in the tool's own docstring: the beat sheet is the
  PRE-pace-cut timeline, so a pace-cut reel gets a proportional scale and a
  loud APPROXIMATE warning (>2% mismatch); 100 points ≈ 0.75s resolution;
  under ~500 views the curve is noise and it says so.

**The ritual is a showrunner stage** ("Retention ingested, post-publish,
wait ~72h"), because a ritual that lives in memory is a ritual that stops.
Selftest (9 checks — parsers, join math, scale warning, noise warning,
replay attribution) runs inside doctor.

**FORMATS re-derivation stays a HUMAN step.** One curve is an anecdote; the
tool prints exactly that, every run. Numbers move into reel_gates.FORMATS
only via a dated entry here, after --aggregate shows several reels
agreeing — G23 applied to our own output, not around it.

## 2026-08-21 (5) — VIA: corroboration is the source count, not the domain count

The claims ledger shipped with a hole its own first live use exposed: TIER
"multi" measured DOMAINS, and the aggregator economy makes domains cheap.
Two shapes of false corroboration, both advisory in research_check now, both
found in real data the day the field existed:

- **Domain-level.** Two articles from one outlet counted as "multi" — the
  live iphone18-colors ledger did this on THREE claims (two MacRumors
  pieces each). Fires as advice: add a second outlet or downgrade.
- **Source-level.** Different outlets all citing the same ultimate origin.
  MacRumors and PhoneArena both quoting Fixed Focus Digital is one Weibo
  leaker dressed as two domains. Recorded with `VIA:` lines (one per
  independent origin, optional); a multi-tier claim whose SRCs share one
  VIA fires as advice. Distinct VIAs stay silent — that is what genuine
  corroboration looks like.

VIA is OPTIONAL, deliberately: requiring it would have refused every
existing ledger the day it landed, and absence-nagging on every multi claim
would teach people to fill it with noise. The tier is only as verifiable as
the VIAs behind it, and the check says so exactly when it matters — when a
claim wears "multi" it cannot demonstrate. Three failing cases in
tools/test_script_pipeline.py (16 checks now), doctor-run.

## 2026-08-21 — iphone18-colors: a colour reel, and the master that never hit its ceiling

### THE MASTER BUG THAT SURVIVED THREE FIXES — it was the AAC encoder

G31 kept failing on true peak. The two notes above this one both "fixed" it by
moving a number, and both shipped over the ceiling. Splitting the chain finally
showed why:

    PCM out of loudnorm + limiter ....... -1.9 dBFS true peak   (clean)
    the SAME audio encoded to AAC 192k .. -0.3 dBFS true peak   (over)

**The overshoot is added by the lossy encode, after every filter has run.** So
no limiter setting can hold the delivered file under the ceiling — and worse,
tightening the limiter made it WORSE, because harder limiting sharpens
transients and raises inter-sample peaks:

    limit 0.85 -> -0.6 dBFS    limit 0.63 -> -2.9 dBFS  (passes)
    limit 0.72 -> -0.6 dBFS    limit 0.56 -> -4.1 dBFS  (too quiet)

Oversampling the limiter (4x, then back to 48k) is now in the chain because it
is correct, but it is NOT what fixed this. **The master has to carry headroom
THROUGH the encode.** RULE: when a delivered-file measurement disagrees with a
filter setting, measure the file at each stage before touching the setting
again. Three notes in this ledger moved a number without doing that.

### THE SCRIPT ON DISK WAS NOT THE SCRIPT THAT WAS APPROVED

Mid-build, `jobs/iphone18-colors/script.md` was found to be a different script
from the approved one — carrying dates ("leaked back in April", "dummy units in
May, a SIM tray in June") and a launch implication ("until next month") that
were never written here, never sourced, and never shown to the user. Its
`research.md` matched that other script and cited URLs this session never
fetched. **G27 blocked the build.** That gate is the only reason it did not ship.

Two rules come out of it:

1. **Do not reconstruct an approved script from memory to make a hash match.**
   Trying candidate texts until one matches an approval record is manufacturing
   consent — it is the exact failure G27 exists to prevent. The recovery is
   `git show <commit>:jobs/<slug>/script.md`, which matched `c35d4242…` byte for
   byte on the first try.
2. **The audio is the other witness.** Diffing `vo.json` against the restored
   script left only known whisper artefacts, which proved the generated master
   was the approved narration and that no credits had been wasted.

### FOUR BUGS IN THE GENERIC COMPILE PATH — all found in one reel

`scripts/compile_shot_plan.py` had never been exercised by a reel with a
possessive in a start_phrase. Each is fixed with the failure recorded inline:

- **`find_phrase` could not match any possessive.** The transcript merges
  "Apple's" to one token (`apples`); the needle split it (`apple`,`s`). The
  transcript half was fixed when G34 was added, the needle half was not.
- **`,000` was not merged like `.8`**, so captions read `$2 ,000` (G30).
- **Caption corrections collected punctuation from ANYWHERE in the token**, so a
  hyphen-merged word came back as `purple-tinged-`. Trailing-only now.
- **The sheet never carried `script`/`approval`**, so EVERY reel compiled by
  this path failed G27. The bespoke `build_<slug>.py` scripts set it themselves,
  which hid it — the same shape as the two earlier notes about `validate_job`
  being stale against a contract `reel_gates` already accepted.

Also: the compiler ended the video at the last WORD, leaving trailing silence
uncovered (70.04s of scenes against a 70.44s master). The final beat now holds
through it.

### A GENERATED CLIP MUST FINISH INSIDE THE BEAT IT IS CUT TO

`chip-ultra` landed its second chip at 0.70s and its caveat at 1.5s, on a 1.34s
beat: the shot showed a half-built card for its whole duration, and the honesty
line ("no code published") never appeared at all. `chip-lineup` had the same
fault — four chips landing over 2.3s on a 2.6s beat left half the frame empty at
the midpoint (57% dead space). **When you generate a scene asset, read its
animation against the beat's DURATION, not against how it looks played alone.**

### THE PLATFORM BAND APPLIES TO GENERATED CLIPS TOO

All three original chip clips put content below y=1498, where
`src/platformSafeArea.ts` says Instagram draws its own UI. The worst case was
`chip-gap`'s caveat — the one line whose entire job is to stop a viewer reading
outline chips as real colours — sitting under the account row. Nothing checks a
generated MP4's interior; the safe floor is an [EYE] rule for anything we draw
ourselves.

### THE SPLIT COVER-CROPS ITS SOURCE — measure the window, do not guess it

The hook's `topSrc` is not shown whole. Two rendered probes gave
`composite ≈ (source − 500) × 0.52`, i.e. only a band of the source is visible,
so a full-frame chip design was first sliced through the letters of its own
label and then, over-corrected, had its code strip fall below the seam. A clip
destined for a `split` needs composing for that window specifically.

### ONE TEXT SYSTEM — a footage scene whose SOURCE contains type must say so

`hideCaptions` defaults true for typecard/wordcascade and for any scene carrying
a `kinetic`, because the engine can see those. It cannot see type baked into an
MP4, so the karaoke chips printed straight through "A DARK PLUM" and
"DARK CHERRY". Set `hideCaptions: true` on any footage beat whose clip carries
its own display type.

### DE-EMPHASIS ON A COLOUR REEL IS A LIFT, NEVER A BLEND

`chip-lineup-b` first dimmed the un-named chips by blending toward cream. That
turned Dark Cherry into a light mauve — misstating the exact thing the reel
spends 70 seconds establishing. The named chips are lifted and underlined
instead, and every swatch stays its published value. **Any treatment that alters
a hue is off-limits on a reel whose claim IS the hue.**

### Treatment history — iphone18-colors

- iphone18-colors (every iPhone 18 Pro / Ultra colour rumour): **NEW — Pantone
  chip motion graphics generated with PIL+ffmpeg** (8 clips: hook plate, hero
  chip, punched-in chip, 4-up lineup, lineup with two named chips lifted and
  underlined, Pro-vs-Ultra count card, Ultra-only card, closing plate), each
  labelled `APPROX sRGB OF THE PUBLISHED CODE`; **the Ultra's chips drawn as
  OUTLINES** because no code was published for them, captioned "no code
  published"; Pantone's own colour-finder page as an official-tier `receipt`
  with the "Color Family: Red-Purple" row highlighted — the reel's whole
  argument settled by the source; MacRumors' four-up render used ONLY under
  "every render you've seen leans red", labelled FAN RENDERS, where the render
  is the subject and not evidence; `sourceread` on the MacRumors bullet list;
  receipts on the leaked SIM tray (its own "alleged" caption highlighted as the
  hedge), the 9to5Mac leaker headline, the MacRumors "could be dropped before
  launch" caution, and the Ultra headline; two cream wordcascades; facecam 21%.
  27 scenes / 70.5s / −14.4 LUFS / TP −2.9 / 9 SFX cues.
- Used here, avoid repeating next reel: the Pantone-chip family as the primary
  motion-graphic system and the official-spec-page-as-receipt move (Pantone).

### THE OUTLINE-CHIP DEVICE FAILED, AND IT FAILED AS A PICTURE

The Ultra's two shades have no published code, so they were drawn as EMPTY
OUTLINE chips to say precisely that. The reasoning was written into the
manifest and into this ledger, and it was still wrong: on screen two blank
boxes read as a BROKEN RENDER, not as honesty. The user's first note on the
finished cut was "iPhone Ultra colors are not appearing, just blank".

**A caveat that needs a caption to explain it is not working as a picture.**
The shades are now filled with labelled approximations and the caveat lives in
the chip's own label ("APPROX", "no Pantone code published"), where it is read
as information rather than as a fault. RULE: an absence can be *stated*, but it
cannot be *drawn as nothing* — the viewer has no way to tell your deliberate
blank from a bug.

### HIDING CAPTIONS TO FIX A COLLISION SILENCED A THIRD OF THE REEL

`hideCaptions: true` went onto nine chip beats because the karaoke chips printed
through type baked into the clips. It fixed the collision and created a worse
one: with the receipts already at `captionBottom: 6000` (the repo's convention),
captions were absent for most of the runtime — on reels watched on mute.

The fix is a LANE, not a switch. `BANDS.caption` is [0.62, 0.74] and
`captionFloorPx` puts the lowest legal caption at `bottom: 499`, so a caption
occupies roughly y 1320-1420. Every generated clip now finishes above a
`CONTENT_MAX` of 1300 and the captions are back on with `captionBottom: 500`.
RULE: when generated artwork and captions collide, move the ARTWORK — a caption
lane is fixed by the platform, and turning captions off is paying for a layout
mistake with the mute viewer's comprehension.
- NOT used (available again): timeline, uidialog, categorygrid, statcard,
  chart, specsheet, checklist, comparesplit, endquestion, logoassemble.

## 2026-08-21 (6) — scout contact sheets: the look, made one file

The scout rule was always the honest one — extract frames and LOOK, write
`shows` from what you saw — and always [EYE] and slow, which is the recipe
for a rule that gets skipped. Thin `shows` text is why grok-bot could
justify only 4 of 39 covers phrases while iphone-fold-ultra managed 11 of
30: the description quality IS the Rule 3 evidence chain.

**`tools/scout_sheet.py`** makes the look one file per candidate: 24 frames
evenly spaced across the clip, timestamp burned on each tile (PressStart2P,
shipped in public/fonts so it works on any machine), tiled into a single
JPG. Takes a file, a directory, or a job slug (sheets everything under
`_sources/` and `public/assets/` for the job). Sub-second clips get fewer
frames instead of an error.

Two design points worth the ink:

- **It automates the scrubbing, not the seeing.** The scout still looks and
  still writes; the tool's closing line says exactly that — write `shows`
  from the SHEET, not the filename, and not from what the source claimed.
  Same division of labour as preflight_stills at the other end.
- **It degrades instead of failing.** Timestamps need drawtext, the filter
  ffmpeg-full was installed for. On a plain build the tool produces
  UNLABELED sheets and says so loudly — a sheet without timestamps still
  beats no sheet. The selftest asserts drawtext WORKS, which makes doctor's
  scout-sheet block a live probe of the ffmpeg-full capability: a plain
  ffmpeg would pass every PATH check and fail exactly here.

Verified by looking, not by exit code: a 12s vertical synthetic clip
sheeted 6x4 with legible corner timestamps 0.2s-11.8s. Named in the
showrunner scout stage and AGENT.md STEP 1a.

## 2026-08-21 (7) — hook experiments: vary on purpose, measure before ruling

The avatar master is the expensive frozen half of a reel; the cold open's
VISUAL treatment is just Remotion, and re-renders are free. So hooks are
now an experiment with a ledger instead of a habit:

- **The treatment label is DERIVED, never declared.**
  `retention_ingest.hook_treatment()` reads the first 2.5s of the beat
  sheet (scene types + kinetic/headline/infocard/locked flags) into a
  stable string — `split+kinetic > footage`. A hand-written label would
  drift from what actually renders; a derived one cannot. Recorded in
  every performance.json ingest.
- **`retention_ingest.py --hooks`** is the experiment view: every reel's
  derived treatment (tried), joined to hook watch @2s and pp lost 0-3s
  (measured, filling in as reels publish). Named in the showrunner
  structure stage, where the open gets designed.
- **First run of the table already taught something:** 7 of 11 reels open
  on a split, and logoassemble opens appear three times despite
  going-viral's own no-logo-build warning. The variation discipline was
  prose; now it has a scoreboard.
- **Within-reel A/B was cut on purpose.** YouTube cannot A/B the video
  (Test & Compare covers thumbnails only), and cross-platform splits
  confound audience with treatment. Across-reel variation measured by the
  retention loop is the honest experiment available.
- **DATA BEFORE RULES, stated where it will be read:** the table's own
  footer says no hook gate exists and none gets written until several
  reels share a treatment and their curves agree — and then the finding
  lands here first, dated, like every measured number before it.

## 2026-08-21 (8) — calibration is a record now, not a memory

AI_TELLS and check_script's prose thresholds are frozen snapshots of the
approved-script corpus on the day they were derived (9 scripts, this
morning). The corpus grows with every approval, and a frozen calibration
fails QUIETLY: the day an approved script legitimately uses one of the 36
phrases, the checker starts flagging the user's own approved voice at every
propose — forever, with nothing saying the list is stale. That is the exact
inverse of the "isn't just"/"the catch?" lesson that built the list.

- **`tools/script_calibration.json`** records what the calibration was run
  against: each approved script's hash (approval-matching only — an edited
  script is not the user's voice), the tell count, and any collisions
  knowingly accepted.
- **`check_script.py --calibration`** compares the record to reality; exits
  2 when the corpus moved or a NEW tell fires on an approved script.
  **Doctor runs it as a WARN, never a FAIL** — a grown corpus is progress,
  not breakage, but a checker flagging the user's own voice must not stay
  silent about it.
- **`--recalibrate`** prints the evidence — tell collisions with the
  remove-or-accept instruction, structural findings per approved script —
  and refreshes the record. REMOVING a tell stays a human edit with a dated
  comment; a collision left in place is recorded as accepted and stops
  nagging. Same shape as FORMATS re-derivation: the tool gathers, the
  human rules.
- The bootstrap run's structural sweep doubled as history: pre-framework
  approved scripts (apple-pay-india, ios27-tiers) trip NO OPEN LOOP and
  SPEC RUN — the checks correctly date which scripts predate the story
  standard. Drift evidence, not verdicts; thresholds stay advice.

Five failing cases in test_script_pipeline (21 checks now), doctor-run.

## 2026-08-21 — the nomusic clone reported green on checks it never ran

`iphone18-colors-nomusic` (music bed dropped, SFX kept) came back
**"GATES PASSED (PARTIAL)"**. The word PARTIAL was carrying the whole warning:
`reel_gates` resolves `vo.json` and the manifest by SLUG, found neither under
the derivative, and skipped every check that compares the PICTURE against the
WORDS — the blocking ones included. A clone can therefore look green on Rule 3
while never having been tested against it.

This is the **third** enforcer to need the parent fallback. The ledger already
records it for `validate_job.py` and `script_approval.py`, and already states
the rule: *when a sheet variant becomes legal, every enforcer that reads a path
by slug needs to know.* It was written down and still missed, because the
partial verdict reads like a pass at a glance.

RULE: **a qualified pass is a fail until the qualifier is gone.** If a gate run
says PARTIAL, find out which checks were skipped before believing the colour.

### Verifying a music-free export — measure it, do not trust the flag

`noMusic: true` proves the sheet asked for it, not that the delivered file
obeyed. Measured mean volume in matched windows of both masters:

    window                with music   no music
    speech gap, no sfx      -22.8 dB    -26.1 dB
    speech gap, no sfx      -25.9 dB    -33.1 dB
    speech gap, no sfx      -25.6 dB    -34.4 dB
    SFX Magic Reveal        -14.9 dB    -15.1 dB
    SFX Camera Shutter      -17.0 dB    -17.1 dB
    SFX whoosh              -15.1 dB    -15.1 dB
    SFX Core                -10.1 dB    -10.0 dB

The pauses drop 3-9 dB (the bed is gone; what remains is VO room tone) while
every SFX window matches within 0.2 dB (the cues are untouched). That is the
claim "music removed, effects kept" actually evidenced, and it takes one script.

`volumedetect` writes its report at INFO level, so `-v error` silences the very
line you are measuring — it returns nothing and reads as a failed probe.

## 2026-08-21 (9) — render speed: measured levers, a draft lane, and one benchmark refused

"Speed up the process" starts with the honest map of where a reel's time
goes, because most of it is not the render:

    research -> script -> approval   agent + human, the true bulk
    HeyGen generation                external queue, minutes, unfixable
    whisper vo.json                  ~1 min
    build + gates                    seconds
    RENDER                           ~165s for a 135s reel (measured)
    master + lint                    ~1 min

The render was ALREADY optimized by measurement: concurrency 2 -> 6 took a
full reel from ~390s to 165s (2026-08-19, 8-core machine), and
preflight_stills exists precisely because seven-render sessions were being
triggered by defects visible in one frame. What was missing was an
ITERATION lane:

- **`render_job.py --draft`** — half scale, crf 28, renders to -draft.mp4,
  skips doctor/master/G31/lint/measurements, KEEPS approval + gates (the
  law applies to drafts; delivery QC re-runs on the final anyway). A draft
  can never become a deliverable: -final.mp4 only exists through the full
  pipeline.
- **`--draft --frames A-B`** — re-render just the fixed scene's frames.
  Refused without --draft: a partial final is a corrupt deliverable.
- **`--concurrency N`** — the measured 6 came from the OLD 8-core machine;
  this one has 10 cores. Re-measure on the first REAL render and record
  here, per the invocation comment's own instruction.

**A synthetic benchmark was considered and REFUSED.** No footage lives on
this machine yet, and an MG-only scratch composition would measure a
workload real reels do not have — their render cost is dominated by
OffthreadVideo decoding 30+ clips. Numbers from a fake workload would be
worse than no numbers (G23). The draft lane's actual speedup gets measured
on the first real reel, and lands here dated.

The bigger wall-clock saving is procedural and free: kick HeyGen
generation, then cut assets during the wait (AGENT steps 2 and 3 have no
data dependency); rehearse with chatterbox BEFORE generating so a broken
phrase anchor never costs a second generation; preflight stills before any
full render. The machine time after the avatar arrives is ~5 minutes —
everything larger than that is process, and the process levers already
exist.

## 2026-08-21 (10) — the procedural savings, made structural

The speed entry above ended with "the process levers already exist" — three
bullets of prose advice, each tagged "the discipline is using it". That
phrase is this repo's oldest alarm: calibrate_sfx existed and nothing
called it; the framework was named everywhere and skipped. Advice that
lives in a paragraph is advice that dies under a deadline. So each lever
now fires at the moment its decision happens:

- **Rehearse-before-generating** is an advisory inside
  `script_approval.py check` — the documented LAST command before the
  avatar is generated, the one moment the reminder can still save credits.
  No rehearsal artifacts under `_sources/<slug>/rehearsal/` prints NOT
  REHEARSED with the cost stated (credits + the queue wait, twice) and the
  free alternative named. Advice, never a block: prudence about spend is
  judgement, and the constitution keeps blocking for the three rules,
  render correctness and rights. But generating without it now requires
  saying so out loud.
- **Cut-while-it-renders** lives in the showrunner avatar stage and
  AGENT.md STEP 2, at the exact line that says to generate: kick the
  generation, then go straight to asset cutting — the two share no data,
  so the queue wait is hidden or it is wasted.
- **Preflight stills** needed nothing: already wired into render_job
  before every full render. The lesson generalises the other way — the
  reason it never got skipped is precisely that it does not depend on
  anyone remembering it.

Two standing cases in test_script_pipeline (27 checks): the advisory fires
on an un-rehearsed job and goes quiet once rehearsal artifacts exist.

## 2026-08-21 (11) — the beat plan is shown in the viewer's language

The user was asked to approve a beat table reading "chip with label
withheld / generated MG" and "✓ ✓ ?" — the pipeline's internal vocabulary,
meaningful to the session that wrote it, opaque to the person consenting.
Approval is informed consent on script AND plan; a plan the approver cannot
picture makes half that consent hollow.

**`tools/beat_plan.py`** renders the shot plan as HEAR/SEE rows — the
spoken line, then what is literally on screen, built from the plan's own
content: the manifest's `shows` text instead of filenames, the avatar clip
as "the presenter, on camera", checklist rows spelled out with their marks
("Dark Cherry ✓, Dark Gray ?"), cascade words and headlines quoted. Scene
types survive only as trailing [tags] for the builder. An unknown type
degrades to a flagged name, never silence. `propose` prints it
automatically; with no shot plan it says the plan must still be shown in
viewer's terms.

The closing line of the render is the rule itself: **if a SEE line is not
understandable, the plan is not ready to approve.** Six cases in
test_script_pipeline (33 checks), doctor-run.

## 2026-08-21 (12) — the approval record proves what was SHOWN, both halves

review.json carried the script hash — proof of which WORDS the user saw —
but nothing recorded whether a beat plan was shown beside them. Now it
carries `beatPlanShots`: the number of HEAR/SEE rows rendered at propose
(zero when no shot plan existed, and propose says so out loud). An approval
can no longer silently claim the plan half of informed consent. Also fixed
in passing: voice_clone.py's stale "torch 2.6.0 pin" note, which had hidden
the real torch 2.13 / torchcodec save issue for a day.

## 2026-08-22 (13) — a VO-only reel, and the four tools that assumed a face

First reel built with **no presenter at all**: narration over first-party
product footage, at the user's choice. Nothing in the constitution requires
a face — facecam share is ADVICE (G06/G17) — but four tools had the avatar
baked in as an assumption, and each failed in a way that looked like a
different bug:

- `compile_shot_plan.py` hardcoded `audio` to `avatar-master.mp4`, so a reel
  whose audio is a bare voice track had no way through the generic path —
  even though the beat-sheet contract already documents audio as "the
  video's audio OR a wav". The shot plan may now name its own `audio`.
- Its `media_info()` insists on a video stream because it also returns the
  width/height the avatar's face framing needs. An audio-only track returned
  `None`, so the trailing-silence extension silently never ran and the scene
  total came out 0.23s short of the audio. Added `duration_of()`.
- `validate_job.py` **blocked** on "opening scene must visibly include the
  presenter" — the same property `reel_gates` treats as advice. Two tools
  disagreeing about whether a presenter is optional. Now: blocks only when
  the reel HAS a presenter and the opening hides them.
- `duck_music.py` and `reel_gates.py --master` both read `vo.json` as
  whisper's `segments` shape only, while `load_words` has always accepted the
  flat `{"words": [...]}` form. A TTS that returns its own word timings
  produces the flat form, and both died on it — one with a bare `KeyError`.

**Distilled rule: an assumption held by four tools and no gate is not a
rule, it is a habit.** When a build legitimately departs from the usual
shape, the tools that block should be exactly the ones a gate classifies as
blocking. Everything else advises.

Also fixed: `compile_shot_plan` never emitted `format`, so every reel built
on the generic path was judged with **news** physics whatever it declared —
a top5 reel silently measured against the 60-80s band. `format`,
`noCredits`, `sides`, `allowLong`/`allowLongReason` and `captionStyle` are
now pass-throughs. `rehearse_vo.py` had the same defect and now reads the
manifest. And `check_script.py` could not parse the heading its own
scaffold writes (`## SHAPE (S17)` vs a bare `## SHAPE`), so every scaffolded
job silently fell back to generic thresholds.

## 2026-08-22 (14) — focusX is object-position, not the window centre

Every off-centre framing in this reel was verified on a real extracted
frame before it went in the plan — and every one of them still came out
wrong, pulled toward the middle. The scouting crops used
`crop=608:1080:centre*1920-304`, i.e. focusX as the window CENTRE. Remotion
passes focusX to CSS `object-position`, where it is a fraction of the
**overflow**: the window's left edge in source pixels is
`focusX * (1920 - 608)`. The two agree only at 0.5, which is why nothing
looked broken in testing and the hook lost the iPhone in the render.

    focusX_remotion = (centre * 1920 - 304) / 1312

**Distilled rule: verifying a frame proves the CONTENT, not the framing.**
A crop test is only evidence if it uses the renderer's own geometry. Check
an off-centre focusX against the rendered output, never against a
hand-rolled ffmpeg crop.

## 2026-08-22 (15) — OCR is a screen, not a proof

The brand restriction forbade the product name anywhere on screen. A
tesseract sweep (4fps, 467 frames) over the seven official source clips
found the wordmark in two of them — and MISSED a six-second title card in
the hero montage where the name sits in small italic script under the
title. A manual frame review caught it.

Every subsequent name-safe window in the manifest carries `nameSafe`, and
the finished render is audited twice: OCR at two page-segmentation modes on
2x-upscaled frames, AND a full visual sweep of every frame at 5fps. The
visual sweep is what caught three defects OCR cannot see:

- a clip opening on the vendor's red promo card under the word "gestures"
- a clip opening on the Mac's text composer under "a touch control surface"
- a named YouTube creator's face filling the Mac screen for ~3s, inside
  first-party footage — the sourcing rule was satisfied and the intent was
  not

**Distilled rule: a text detector answers "is this string present". It does
not answer "is this frame right".** Only the second question is the one the
critic pass exists to ask, and only eyes answer it.

### Treatments used (do not repeat next reel for the same kind of info)
- hook: wide two-device desk shot + `headline` label/headline build
- feature labels: `chip` kinetic at y 0.70, one per feature beat
- requirements: `specsheet` dark card, 3 rows, one accent row
- payoff: return to the OPENING shot, zoomed out, headline echoing the hook
- CTA: `commentcta` (now keyword-parameterised) over the opening desk shot

## 2026-08-22 (16) — five features listed beat three features shown, and why

User feedback on the first cut: "the current mobile-view clips show fragments
of the concept — icons, websites, emoji, gestures — but rarely make the app's
capability immediately legible on a phone screen." Correct, and the cause was
a treatment decision, not a scouting one.

Tight 9:16 crops of this footage are *beautiful* and *uninformative*. The
capability lives in the RELATIONSHIP — finger moves here, Mac changes there —
and a 608px-wide window of a 1920px frame holds the iPhone or the Mac screen,
never both. Every feature became two shots (cause, then effect), and two
shots separated in time do not read as cause and effect at 3 words/second.

**Distilled rule: when the claim is a relationship, the frame has to hold
both ends of it.** Five capabilities named in narration lose to three
demonstrated in one shot each. Cut the other two.

The treatment that made it work is `floatcard` with the new `bg:"blur"`: the
whole 16:9 frame, never re-cropped, on a field made from the shot's own
colour. It is the documented answer for wide material in a vertical frame
(references/source-capture-policy.md says crop and move, *or* card it) and
the user's "desktop/native view where the Mac action and the iPhone trigger
can be seen together" is exactly the G41 recorded-reason case.

Two things this exposed:

- A `split` of the SAME clip at two focus points looked obvious on paper and
  read as a duplicated image, because both halves come from one 16:9 frame
  and overlap. Rejected after previewing it, not after rendering it.
- A 16:9 card centred in 9:16 leaves ~70% dead space. Flat cream read as
  empty; the blurred-self background fills it and the linter's dead-space
  rule stops applying.

### The labels that deleted the captions

The first pass labelled each card with what the beat did — "TAP ONCE → THE
MAC APP OPENS" over "Tap once to open the apps you use every day" — and the
captions silently vanished for 40% of the runtime. Reel.tsx `autoHide` drops
the caption chips when a scene's headline shares two or more spoken words
with the VO under it: ONE TEXT SYSTEM, working exactly as designed.

**Distilled rule: an on-screen label must ADD a word, not repeat one.** The
tags became LAUNCH / AUTOMATE / GESTURES — a category each, ≤1 shared word,
captions intact. If a label and the narration say the same thing, one of
them is decoration.

### The tail rule was about a face, not about silence

G01 refused any cut running more than 0.45s past the last spoken word. Its
own message says why: "frozen face". But this reel's last scene is a
comment-gate CTA drawn entirely in code, and it needs a beat after the voice
stops for a viewer to read what to comment — the payoff card was being cut
mid-animation. G01 now allows 2.5s when the final scene is a generated type
and still 0.45s for footage, which genuinely does freeze. Three cases in
test_gates (108 checks) pin both branches.

The self-test harness needed fixing first: `expect_gate` derived `vo_end`
from the sheet, so lengthening a scene moved the VO end with it and no tail
could ever be constructed. Any tail case has to pin the VO end independently.

### Treatments used (do not repeat next reel for the same kind of info)
- hook: wide two-device desk, full-bleed, three-line `headline` build
- feature demo: `floatcard` + `bg:"blur"`, one-word category tag above
- requirements: `specsheet` dark card, 3 rows, one accent row
- payoff: return to the OPENING shot, zoomed out, headline echoing the hook
- CTA: `commentcta`, keyword-parameterised, over the opening desk shot
- captions: `chip-lg` (per-reel override of the locked word-reveal)

## 2026-08-22 (17) — the CTA that appeared twice, and the line nobody spoke

Two user notes on the v2 cut, both about the same 5 seconds.

**"Comment App appears twice at the last with two different style."** True.
`CommentCta` shows the keyword three times by design: typed into a comment
field, then on a big card reading COMMENT THIS WORD, then a closing display
COMMENT "APP" in a different treatment. On the short beat it originally had,
the third never rendered and nobody noticed. Give the scene the room it
actually needs and the redundancy appears.

**Distilled rule: a component's full animation is part of its contract.** If
a beat is too short to play it, the bug is hidden, not absent — and lengthening
the beat later surfaces a design fault that was always there. Added
`showFinal` (default true, so shipped reels are untouched); this reel ends on
the "link sent" notification instead.

**"Voiceover skips saying Want the App."** Also true, and worse than a skip:
the words were only ever ON SCREEN. `CommentCta` draws its own question,
which made the CTA look complete in every frame check while the narration
went straight to "Comment app". Nothing caught it, because every gate that
compares picture to words checks that the PICTURE is justified by the
speech — never that a promise made in the picture is spoken at all.

**Distilled rule: a component that draws its own copy is writing script the
script does not contain.** When a scene has built-in text, check it against
the narration by hand; Rule 3's gates only run in one direction.

The CTA is now spoken in full, the scene starts on "Want the app?" so the
drawn question lands under those words, and speed came down 1.15 -> 1.10
after the user said the read was not clear. 90 words, 33.7s.

One mechanical note worth keeping: G18 kept firing as the specsheet boundary
moved word by word, because the boundary word starts exactly where the card
ends and 3dp rounding puts it 1ms INSIDE. Move a scene boundary a whole word,
not to the edge of one.

## 2026-08-22 (18) — energy is pause structure, not speed

Shipped a voiceover the user called "completely flat, slow and low energy".
Self-inflicted: an earlier note said the read "doesn't sound clearly", and the
session answered it by lowering speed 1.15 -> 1.10. Wrong lever, and the
clarity complaint had actually been about a skipped line and a spelled-out
word, both already fixed by then. The `speed` dial got moved twice in opposite
directions with no way to check either.

Measuring four takes answered it immediately:

| take | voiced | longest pause | pitch var | wps |
|---|---|---|---|---|
| 1.15 plain | 69% | 0.59s | 2.02 st | 3.18 |
| 1.10 plain | 64% | 0.88s | 2.12 st | 2.67 |
| 1.15 SSML + breaks | 67% | 0.78s | 2.15 st | 2.87 |
| 1.20 plain | 71% | 0.49s | 2.04 st | 3.48 |

**Pitch variation is identical across all four.** The take that sounded
lifeless has the same inflection as the one that did not. What it has is DEAD
AIR — nearly double the pauses, with 0.8-0.9s gaps landing mid-thought ("Add a
shortcut … and", "one button … You can").

**Distilled rule: perceived energy in a TTS read is the pause structure. Judge
a take by `voiced %` and `longest pause`, not by the speed number.**

Two things that fall out of it:

- **SSML `<break>` ADDS to the engine's own sentence pause, it does not
  replace it.** Tested at 0.12-0.22s and the resulting gaps measured
  0.38-0.66s, making the read 5s longer. To tighten, remove sentence
  boundaries or raise speed — never add breaks.
- **`<emphasis>` parses and costs nothing** (tags are consumed, not spoken),
  but moved pitch variation 2.02 -> 2.15 st, which is noise. Not the lever.

`tools/voice_energy.py` does the measurement — pitch variation in semitones,
loudness dynamics, voiced fraction and the pause histogram, from numpy alone.
Compare VO-ONLY files: on a finished master the music bed fills every gap and
the pause numbers stop meaning anything (the shipped master reads 0 pauses).

## 2026-08-22 (19) — the CTA broke because of WHERE it sat, not how fast it was

The user: "Voice over for Call to action at last is completely fucked up."
Measured, and they were describing something real. In the 1.20 take, across
the closing line:

    Comment 0.30s rms 0.111 | and 0.08s 0.035 | we'll 0.18s 0.037
    send 0.22s 0.045 | the 0.42s 0.045 | exact 0.28s 0.035 | one 0.10s 0.025

Energy falls to a THIRD after "Comment", "one / in / your" are swallowed at
0.06-0.10s, and the filler word "the" stretches to 0.42s — four times its own
length two seconds earlier. The engine runs out of breath at the end of a long
paragraph.

The proof it is position and not speed: generate that identical line at an even
FASTER 1.30, but as its OWN utterance, and the decay halves — 66% -> 32% — with
"app" becoming the LOUDEST word in the line instead of a swallowed one.

**Distilled rule: generate the VO in SECTIONS. A call to action is a separate
utterance and must be synthesised as one.** Body and CTA want opposite
settings anyway — the body wants speed for energy, the CTA wants to be
understood — and one global `speed` cannot serve both. Shipped: body 1.30,
CTA 1.15, joined with a 0.40s beat.

Two smaller findings from the same pass, both counter-intuitive enough to
write down:

- **Punctuation edits do not buy energy.** Removing mid-sentence commas made
  the read 1.6s LONGER (the engine redistributed into bigger sentence pauses);
  joining sentences with commas also made it longer. Five body takes, all
  64-65% voiced. Speed is the only lever that moved it: 1.30 gave the highest
  pitch variation of any take measured (2.59 st) as well as the fastest rate.
- **`silenceremove` is not a tail trim.** `stop_periods=-1` strips EVERY
  silence, including the pauses between phrases, clipping them all to the
  `stop_duration` stub — it took 3.5s out of the middle of a body take and
  would have desynced every hand-written word timing. To trim a tail, cut to a
  known timestamp.

Also worth keeping: the API folds a word's FOLLOWING pause into that word's
end timestamp. A word that looks stretched to 0.78s is often ~0.2s of speech
and 0.58s of silence — check the tail RMS before believing the duration.

## 2026-08-22 (20) — "zoomed out" is what a wide shot looks like full-bleed

User on the finished cut: "first 10 seconds visuals seen completely zoomed
out... same thing right from 0:27. Everything else is good." Precisely the
full-bleed beats, and precisely not the floatcard demos between them.

The cause is not the framing being wrong — the geometry was correct. It is
that a WIDE ESTABLISHING SHOT played full-bleed puts the subject in a corner.
In these shots the iPhone is one small object on a desk with a lamp, an
ornament and a laptop; a 9:16 crop keeps all of that and the phone stays
small. The floatcards read fine because the card IS the subject and the eye
has nowhere else to go.

**Distilled rule: full-bleed needs a shot whose subject already fills it. A
wide shot used full-bleed must be PUSHED IN — `zoom` 1.4-1.6 with focusX on
the subject — or it reads as distant no matter how correct the crop is.**

Three things worth carrying:

- The push has a ceiling set by the FOOTAGE, not by taste. apps-wide contains
  its own aggressive dolly, so the same `zoom` that frames the phone nicely at
  the clip's start is a single giant app icon 2s later. Check a scene's
  framing at BOTH ends of the span it actually plays, not at one frame.
- One of these beats had no subject at all: the clip cut for "but once it's
  set up" was a Mac dock close-up with no iPhone anywhere in it. Pushing in
  would not have saved it; it needed different footage. Check what is in the
  frame before deciding the frame is too wide.
- **`commentcta` takes no `zoom`**, so its backdrop cannot be pushed in from
  the sheet. Pre-crop it to 1080x1920 instead. Doing that also caught the old
  backdrop being 2.40s under a 3.74s scene — it had been freezing for the
  tail, which nothing flags because the scene type is not `footage` and G13
  only measures those.

## 2026-08-22 — two user directives: music is optional, thumbnails are dropped

**1. Background music is OPTIONAL per reel; SFX stay the default.** G09
inverted: the 2026-08-17 design treated a music-free reel as an argued
exception (noMusic + a mandatory written reason); it is now a first-class
choice. What survives is the gate's original 2026-07-22 purpose — a reel
that FORGOT its bed must be distinguishable from a chosen VO-only cut — so
`noMusic: true` still declares the choice, reason accepted but not
demanded. Plumbed end to end: `new_job.py --no-music` → shot-plan
`noMusic` → compile skips the default bed and stamps the sheet → G09
silent. SFX untouched (G08/G28/G40). Suite: the old "noMusic without
reason fires" case became its inverse — a declared music-free reel must
stay SILENT — so a future merge cannot quietly restore the old law
(108 gate checks).

**2. YouTube thumbnails are DROPPED.** `tools/make_thumbnail.py` refuses
with a dated pointer here (`--i-know-its-retired` overrides, for the day
the call reverses; the Remotion renderer and `Thumbnail.tsx` stay in code
for the same reason). The `thumbnail-design` global skill is removed from
the installer and this machine — doctor reads the installer's list, so its
count self-updates to 5. Every doc mention updated (CLAUDE.md, MIGRATION,
showrunner packaging stage). The 2026-08-19 thumbnail entries above are
superseded by this one; the ledger keeps them because it is append-only.

## 2026-08-24 — no-music-by-default graduates from a per-video call to a standing rule, and covers stop by default

Two separate user directives, given directly (not discovered mid-build), both
now recorded in RULES.md §8 rather than left to live only in this chat.

**Music.** The question had a paper trail already. `airpods-camera`
(2026-08-18) dropped its bed on request, and the session that shipped it
wrote down explicitly: *"I logged that as a per-video call, not a standing
rule."* `iphone18-colors-nomusic` (2026-08-21) shipped a VO-only derivative
alongside its scored parent for the same reason. The in-flight `iphone-18-pro`
job was sitting on an open question asking exactly this — *"Say the word and
I'll ship it `noMusic` + SFX only, same as the last one"* — when the user said
it today: **no background music on any upcoming reel, use SFX fully instead.**
That resolves `jobs/iphone-18-pro/questions.md` Q1 and every future job's
version of it.

Mechanically nothing new had to be built. G09 (`tools/reel_gates.py`) and
`validate_job.py` have accepted `noMusic: true` + `noMusicReason` since
2026-08-17 — the escape hatch just flips from rare exception to default.
`scripts/compile_shot_plan.py`'s generic path used to auto-build a bed
whenever a plan didn't say otherwise; that default now emits `noMusic` +
a standing reason instead, and a plan opts back into a bed explicitly with
`"music": true` or its own object. **SFX takes over the job the bed was
doing** — run the top of G08's range (9 cues, not 6) and draw from the full
16-cue catalogue rather than repeating the same 2-3. The measured 6-9
ceiling itself is NOT raised without a fresh teardown; "use all the SFX" is
variety and generosity within that range, not a request to blow past it.

**Covers.** Second, unrelated directive: stop generating the 9:16
Reels/Shorts cover (`tools/make_thumbnail.py`, AGENT.md STEP 6) for every
reel. It was never gated — no RULES.md line, no G-number — purely a
workflow step, so the only fix needed was marking it SKIPPED BY DEFAULT in
AGENT.md. Runs again only if the user asks for a cover on a specific reel.

## 2026-08-24 — reconciliation: two sessions implemented the music directive at once

The two entries above are BOTH real: the same user directive reached two
parallel sessions, one built default-with-declared-opt-out, the other built
no-bed-by-default. Merged 2026-08-24, converging on the second reading —
the user's "however, sound effects will be used by default" implies the bed
is not — with the first session's G09 loosening kept (a declaration needs
no argued reason). Final semantics live in RULES.md; compile stamps the
declaration automatically, so the default path needs nothing from anyone.

## 2026-08-25 — ios27-beta7: first reel built end-to-end under the no-music
standing rule, and two real text collisions the gates could not see

First reel scripted, scouted, generated and rendered since the 2026-08-24
no-music-by-default rule landed — confirms the mechanics work as designed:
`build_ios27beta7.py` set `noMusic: True` + a one-line reason and never
touched a `music` object; `compile_shot_plan.py`'s auto-fallback was not
needed since this reel used a bespoke build script (the shot-plan path is
still preferred when the material fits it — this one did not, see below).
9 SFX cues drawn from 5 of the library's 6 roles (transition, shutter x3,
impact x2, suspense, reveal x2) — the "top of the range, full catalogue"
instruction followed literally rather than repeating the same 2-3 cues.

**Scope discipline, stated up front and held.** The topic (iOS 27 beta 7)
sits one reel away from the published `ios27-tiers` (Siri AI / device
tiers). `structure.md` recorded the exclusion BEFORE scripting — no Siri AI,
no device tiers, scoped purely to what beta 7 itself is (a stability pass,
proven with three consumer-relevant bugs pulled from Apple's own release
notes) — and the research ledger's `explicitly_NOT_claimed` repeated it.
Worth naming as a pattern: the treatment-history check this file already
asks for is about VISUALS; this is the same discipline one level up, on the
STORY itself, and it deserves the same explicit pre-declaration.

**FloatingCard renders `<OffthreadVideo>` only — a PNG handed to it is a
black frame, not a coincidence.** `build_ios27tiers.py`'s docstring already
said so in a comment; this session re-derived it the hard way by reading
`FloatingCard.tsx` line by line before trusting the comment. Four scraped
release-notes crops (aspect 1.95:1 to 3.88:1, all over RULES.md's 2.5:1
`receipt`-overflow line, so `floatcard` was the only legal home) were
silent-looped into 4s MP4s with `ffmpeg -loop 1 -i x.png -t 4 -vf
"format=yuv420p,pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -pix_fmt
yuv420p x.mp4` — the `pad` is required because libx264 refuses an odd
dimension (885px source crops are common; refuse the temptation to
special-case width, just pad every conversion). **Distilled rule: before
handing a still to ANY scene type, check whether it imports `Img` or only
`OffthreadVideo`/`Video` — `split`, `receipt`, `sourceread`, `annotatezoom`
take stills directly; `floatcard` and `footage` do not, ever.**

**Two text-on-text collisions that every gate passed clean — found only by
pulling actual frames, exactly as RULES.md §11 says to.** `check_beats()`,
`validate_job.py` and `lint_frames.py`'s AUTO FLAGS all passed this reel
with zero blocking errors on both defects:

1. The hook's `kinetic` "BETA 7" card defaulted to `y: 0.14` (Kinetic's
   own default region), which is exactly where `src-hero.png`'s own
   headline ("iOS & iPadOS 27 Beta 7 Release Notes") sits — the kinetic
   text landed printed directly on top of the words it was echoing,
   unreadable. Fixed by measuring the source image's actual empty band
   (the white space between the tagline and the seam) and pointing `y`
   there (0.42) instead of trusting the component default. **A `kinetic`
   default `y` is tuned for a footage/avatar background, not for a
   text-dense screenshot behind it — always eyeball the actual source
   image before accepting the default.**
2. A `floatcard` built from a TALL composite (three stacked outlet
   receipts, aspect 0.545, 72% of frame height, vertically centred) pushed
   the default caption position (`captionBottom` unset → ~y 0.71) into the
   middle of the card, printing the caption word "says" directly across
   the Macworld headline. No gate checks whether a card's own footprint
   overlaps the caption band — `captionBottom` exists precisely for this
   and is scene-level (`SceneBase`, not `split`-only, despite every prior
   use of it being on a `split` hook), so the fix was one field:
   `captionBottom: 1750` to park captions in the card's TOP gap. **The
   bottom gap was NOT a safe alternative** — this card's own bottom edge
   already sits at y 0.86, past the platform account-row line (y 0.835,
   `platformSafeArea.ts`), so any caption placed further down would have
   been a real G45 violation, not just a taste problem. **Distilled rule:
   any card occupying more than ~60% of frame height needs its
   `captionBottom` chosen by hand, and the choice must check BOTH gaps
   against the platform safe floor, not just whichever one looks bigger
   in a still.**

**Four typecards, one script — G12 didn't fire, and it should have made me
look harder, not accept the pass.** The gate checks `bg in (None,
"black")`; this build used `bg: "#0a0a0a"` on all four (a deliberate
near-black, not the literal string), which is a hex-string loophole in the
letter of G12 while violating its entire point — four visually-identical
black cards in one 78s reel. Caught on the contact sheet, not by any gate.
Fixed by alternating two of the four to `bg: "#f2ecdf"` (the `TINT.sand`
cream, matching `FloatingCard`'s cream) — not by filing a G12 fix, though
one is owed (`bg` should be normalised/canonicalised before the equality
check, the same class of gap as `STYLE_ALIASES` exists for style ids).

### Treatment history — ios27-beta7

- ios27-beta7 (iOS 27 beta 7 — stability-pass story, deliberately NOT the
  Siri AI/tiers story already told): split hook (Apple's own beta-7
  release-notes page / face, kinetic "BETA 7" card), TWO sourceread passes
  on the same official hero receipt (headline region, then a second
  region for "release notes read like a fix list"), FOUR floatcards built
  from official release-notes text crops converted to silent MP4 loops
  (alarm/Clock, Camera Portrait blur, Siri voice revert, Dictation
  toggle — each floatcard's duration spans BOTH the lead-in clause and the
  claim, not the claim alone), ONE floatcard built from a 3-outlet
  composite receipt (9to5Mac + MacRumors + Macworld mastheads and
  headlines, all dated the same day, stitched with PIL into one portrait
  image), alternating cream/black typecards (2 of each) for the
  "no features / seven betas / shipped broken / closing countdown" beats,
  facecam 19.2% (within the news 10-20% band, four beats: stakes line,
  bridge, opinion line, pivot line — all direct-address). No music
  (noMusic + reason, standing rule). No CTA (format news, CTA optional,
  argued in `questions.md` and confirmed at approval).
- → next reel must introduce at least one new treatment. Already used and
  not to be repeated as the SAME shape next: a multi-source composite
  receipt built by stitching separate mobile captures with PIL (borrow the
  TECHNIQUE for a different multi-source claim, but the specific "three
  outlet mastheads stacked vertically" layout is now used); converting a
  release-notes text crop straight into a silent floatcard loop for a
  sequence of parallel bug-fix beats.

## 2026-08-25 — the ai-tools format: an 8-reel measured teardown, and the blend

The engine's first non-Apple genre, built the G23 way. Corpus: 5 Badar Munir
YouTube shorts (26.5-48.6s · 1.6-5.4 s/cut · 217 wpm · ~60% on camera) and
3 Nick Saraev Instagram reels (34.7-39.4s · 1.4-4.9 s/cut · 237 wpm ·
bookend face ~20%), pulled with yt-dlp, measured with ffprobe/scene-detect/
whisper, frames read via scout_sheet. Two sub-rhythms in both corpora:
tool-LIST reels cut at 1.4-1.7s, single-story walkthroughs at 4-5s.

**The blend (user decision): Saraev's skeleton, Badar's evidence.** Face
bookends the reel — Badar's ~60% on-camera presence leans on a live human
and was deliberately not asked of a HeyGen twin. The evidence doctrine is
the format's own reading of Rule 3: *a named tool is on screen, running or
being itself, while it is named* — its real page, real output, a real
terminal. A README screenshot is evidence only for a claim ABOUT the
README. Full-screen text cards standing in for demos are this format's
logo-build anti-pattern: claude-eating-tokens v1 had six in fourteen beats
and is the reel that forced the format to exist.

**Runtime derived for OUR voice, not copied (user kept the pace).** The
corpus speaks 217-237 wpm; the twin is locked at 2.35-2.75 wps. Corpus word
counts mapped through our pace give the 40-60s band. sfx inherited from
news, unmeasured — the comparison-format precedent, marked as such.

**Recordable evidence is the genre's unfair advantage:** for Claude-topic
reels the artifacts are our own machine's real output (ccusage, claude-hud,
/clear) — tier official, zero rights friction. Record, don't screenshot.

## 2026-08-25 (2) — the observation study: how the ai-tools corpus scouts, animates, and writes

The user picked 9 specific shorts (5 Badar, 4 Saraev YT — the four that his
recent-uploads listing had hidden, all tool-format, one Anthropic-sponsored
with a burned disclosure line). All pulled, 8 transcribed, 5 frame-read via
scout_sheet. Findings live in formats/ai-tools.md "Observation study"; the
three that changed our plans:

1. **Recordings are WINDOWED, not full-bleed** — every demo in the corpus is
   a card with a live cursor floating on a canvas. claude-eating-tokens'
   four terminal/chart recordings moved from `footage` to `floatcard`.
2. **The naming moment has a grammar**: plain-function sentence fused to the
   name, the name lands on a designed logo/wordmark card (Badar sets
   "CLAUDE CODE" in chunky pixel type — our Press Start 2P is already that
   voice), then the real artifact. Meme/stock b-roll is legal exactly once,
   at the hook.
3. **Their hype register is not ours.** "Yes you heard it right / the crazy
   part / completely free ×3" sell; we report. We take the compression and
   the fused naming, leave the hype — and if a reel is ever sponsored, the
   disclosure line burns on screen like Saraev's.

## 2026-08-25 (3) — the study adapted: no third style, a live cursor, and the first recorded asset

Three decisions from the user's "how do we adapt this":

1. **No third style pack** — RULES.md locks the count at two, and the
   genre's look is this repo's own Saraev lineage anyway. The ai-tools
   FORMAT renders under `utility` (mapping in CLAUDE.md locked settings);
   the look vocabulary landed as an addendum in styles/utility.md.
2. **capture.mjs record paints a VISIBLE CURSOR now** (+ click ring; on by
   default, --no-cursor reverts). The recorder had eased mouse choreography
   since day one but page.mouse renders nothing — every recording to date
   had invisible clicks, and the observation study found the live cursor is
   load-bearing in the genre. Proven same-day on the real caveman repo:
   public/assets/claude-eating-tokens/caveman-page.webm, the reel's first
   scouted asset, manifest entry with honest `shows` (the take over-scrolls
   — re-record dwelling on the README; take-craft note in utility.md).
3. **HyperFrames pilot authorized, scene-scoped** — one designed animated
   card for the cost-split beat, our palette, judged by gates and preflight
   against StatCard. Verdict to be recorded here.

## 2026-08-25 (4) — the script approved, and the doctrine made mechanical

The user approved the claude-eating-tokens script with all three carried
advisories accepted in writing: runtime to 68s at the slow end (ship as-is,
pause-tighten after generation), the loop-detector override, and their own
real usage numbers on screen. Approval 341019be.

And the last prose-only piece of the ai-tools doctrine became a gate:
**G50 (advice)** — an ai-tools sheet carrying any full-screen text scene
(typecard/wordcascade) advises, because the 9-reel corpus's measured number
is ZERO: its text moments are chips over moving evidence. v1's six-cards-in-
fourteen-beats can now never happen silently again. Deliberate exceptions
override with a reason, which is why it advises rather than blocks.

## 2026-08-25 — claude-eating-tokens scout session: the evidence stack for ai-tools

The format's first real scout produced the doctrine's proof case. Every
evidence asset is a RECORDING or a verified receipt; zero full-screen text
cards (G50 satisfied by construction):

- **Terminal recreations carry REAL data.** `tools/terminal_page.py` (new)
  plays back a command's genuine output inside a styled terminal that
  `capture.mjs` records deterministically — typed command, line-by-line
  reveal, `--highlight`. Honesty line: the DATA is the machine's own
  (`_sources/<slug>/` keeps the raw capture), and the manifest `shows` says
  "recreation playing back real output". Sanctioned by the utility pack's
  UIDialog precedent. Used for ccusage (real August table: 661,554,294
  tokens, $585.82, cache-read 647,936,100 vs output 1,879,404 — the reel's
  thesis proven on its maker's own bill) and /clear (66% → 1% at real
  session scale).
- **Repo pages are recorded with a live cursor** (capture.mjs now injects a
  44px cursor + click ring by default; `--no-cursor` for recreations, where
  a stray idle cursor otherwise photobombs the corner). Take-craft in
  `styles/utility.md`: dwell where the claim lives — the caveman take holds
  the About line "cuts 65% of tokens" through the opening 3s before
  scrolling.
- **A README screenshot is evidence only for a claim ABOUT the README.**
  The caveman "Honest number warning" callout is captured verbatim as a
  still because the script's claim IS that the README admits the catch.
  (First attempt captured the full 48,561px README — unusable; crop to the
  claim, don't capture the page.)
- **HyperFrames pilot deferred:** the designed-artifact slot was beaten by
  a real recording of the same fact. Queue it for a beat no real artifact
  can show.

## 2026-08-25 — tool names must go through the pronunciation glossary

The first claude-eating-tokens master spoke "ccusage" as roughly "accusate"
(whisper base heard "secluded", medium heard "accusate" — two models agree
the audio was wrong, and the beat exists to NAME that tool). Written-form
names — lowercase CLI tools, hyphenated repo names — are exactly what a TTS
guesses at. Fix, verified by a ~3-credit probe before the ~20-credit regen:
HeyGen brand glossary `262b0154…` (config.json `avatar.brandGlossaryId`),
ccusage -> "see-see-usage", claude-hud -> "Claude hudd". Glossary affects
audio only; captions keep the written form. RULE: before any generation,
scan the script for written-form names and add each to the glossary; send
`brandGlossaryId` on every create call. Note: rehearse_vo's TTS pass was
skipped for RAM this session — its anchor pass cannot catch pronunciation,
which is precisely the class of defect that cost a regeneration here.

## 2026-08-25 — first ai-tools review round: seven user notes, each made structural

The user reviewed the first claude-eating-tokens master. Every note is now a
rule or a mechanism, not a memory:

1. **No credit chip when the frame names itself.** A recorded page showing
   its masthead/URL, a terminal showing its command — the chip repeats the
   pixels ("Source: Claude Docs" under the Claude Docs masthead). Scene flag
   `creditOnScreen: true` (G14 honours it, negative test in the suite).
   CROPS that strip the chrome keep their credit.
2. **A sourceread must highlight the sentence, not the region.** The first
   pass put the sweep on a breadcrumb (y=300 was guessed, not measured).
   Rects are measured from the capture, one per spoken claim, timed with
   `at`. The component's follow-scroll only moves when there are >=2 lines.
3. **Record responsive sites at REAL mobile.** capture.mjs record used a
   width*scale viewport + CSS zoom — media queries saw 1080px, so GitHub
   rendered its desktop breakpoint mangled into 360px. Now: real 360x780
   viewport, deviceScaleFactor 3, Playwright screenshot scale:"device"
   (raw CDP ignores DPR and had been saving 360x780 files labelled 1080).
4. **Floatcards declare the clip's true aspect** — the default 16:9 +
   objectFit:cover was silently cropping the 2:1 terminal tables.
5. **Voice pace/energy is probed, then locked.** 1.05 read slow and flat;
   probe before every full generation when the setting changes.
6. **ai-tools CTA is the keyword variant** (`commentcta` `variant:
   "keyword"`): verb-first pop over the face, no simulated comment UI. The
   gate mock stays the top5 default.
7. **Captions: auto_contrast --write is part of the compile sequence** (the
   4 white-page scenes now carry captionTheme) and `emphasis` is REQUIRED
   authoring — an empty list means no accent word anywhere, which is how the
   locked "one highlight per beat" shipped as all-white captions.

## 2026-08-25 — review round 2: the four remaining notes, all made structural

Watched the render frame by frame, named four defects, fixed each as a rule:

1. **A recording's `from` must point at the moment the claim is visible.**
   The claude-hud beat said "a live meter in your status line" while playing
   the repo header — the status-line demo only appeared at the clip's tail.
   Scouting a recording now means noting WHEN the proof is on screen, and
   the shot sets `from` to it (`from: 4.6` here). A clip is not evidence
   because it contains the proof somewhere.
2. **No single card holds the 4–9s drop-off zone alone.** The cream docs
   page ran 7.58s across the exact window where viewers leave. Split into
   two visuals: the sourceread keeps its highlight, then a live-cursor
   scroll of the SAME page lands on "How the cache is organized" — whose
   text ("the model doesn't remember anything between requests, so Claude
   Code re-sends the full context") states the script's claim verbatim.
   Same source, different treatment, motion where it was static.
3. **A recreation is cropped to its content, never centred in dead space.**
   `terminal_page.py --fit <viewport>` sizes the window AND its type from
   the longest line (monospace is 0.6em, so this is arithmetic, not taste)
   and prints the NATURAL VIEWPORT HEIGHT to record at. The /clear
   before/after went from a small band in a dark 9:16 field to a card that
   fills its own frame. A fixed 13.5px font had also been clipping
   "66% of window" off the mobile version.
4. **A scene that spells the spoken line out in display type suppresses the
   caption.** `Reel.tsx` already did this for headlines; `commentcta`'s own
   keyword/question were invisible to it, so "COMMENT CLAUDE" at 200px sat
   over a caption reading "Comment Claude I'll".

**A generated page must declare a viewport.** The first `--fit` recreation
still rendered tiny: with no `<meta name="viewport">`, mobile Chromium lays
a page out at 980px and scales it to the device — so a window sized to 94%
of 360 CSS px arrived on screen at a third of the frame. Same family as the
GitHub-breakpoint bug, and now asserted by the capture-contract suite. Any
HTML this repo generates for capture carries the tag.

**Frame a recording on its proof, not on its page.** The claude-hud beat at
full width put the caption on the README's Install body text; `zoom 1.55 +
focusY 0.30` makes the status-line demo own the frame and the caption land
on quiet pixels.

**And the capture contract became a suite.** `tools/test_capture_defaults.py`
(run by doctor) asserts capture.mjs's six load-bearing defaults — cursor on,
`--no-cursor` boolean, mobile default, real viewport, device-scale frames,
even physical dimensions. Every one of those was a rule stated in prose, and
two of them had silently broken and shipped a whole scout session. The
"code, not habit" claim is now checked rather than believed.

## 2026-08-25 — auditing the "all upcoming videos" table against its own standard

The table claims "verified permanent, not promised". Audited row by row,
asking only: *what code stops a future session from skipping this?*

| Row | Verdict |
|---|---|
| Format physics | REAL — `FORMATS["ai-tools"]` measured, G23/G24 with failing cases |
| Evidence doctrine (G50) | REAL — present, absent from `BLOCKING_RULES` (advises), self-tested |
| Live-cursor recordings | REAL **as of today** — `tools/test_capture_defaults.py`, run by doctor |
| The look | PARTIAL -> now REAL where measurable (style mapping + G52) |
| Script grammar + hype | **WAS PROSE** -> now `HYPE_MARKERS` in check_script |
| Style mapping | **WAS FALSE** -> now enforced in compile + tested |
| HyperFrames pilot | prose, correctly — a per-reel judgement call |

Two rows did not hold:

- **"Script grammar + hype exclusion — read-order + check_script at propose"
  was not true.** `check_script` had no knowledge of the hype register; the
  rejection of the corpus's sell voice lived only in `formats/ai-tools.md`.
  A future ai-tools script could carry "completely free" three times and
  nothing would say a word. Now `HYPE_MARKERS` (23 markers, measured off the
  same 8 transcripts) with its own self-test — and the offender fixture is
  *enthusiastic human writing*, asserted NOT to be caught by `AI_TELLS`, so
  the two checks stay distinct instead of quietly measuring one thing.
- **"Style mapping — CLAUDE.md locked settings — loaded every session" was
  false, and this reel is the proof.** claude-eating-tokens rendered in the
  editorial pack across several renders while the locked table said
  ai-tools -> utility. A document loaded every session is not enforcement;
  it is a document. The mapping now lives in `compile_shot_plan.py` and the
  pipeline suite asserts both the mapping and its presence in that file.

**New: G52 (advice)** — an ai-tools reel closing on the simulated
comment-field mock. All 9 corpus reels close on a verb-first keyword pop
over the presenter; the mock is the top5 pack's comment-gate and read wrong
on a reporting reel.

The lesson is the repo's own founding one, arriving again: *"loaded every
session", "the skill's binding read-order" and "the build session reads it"
are all the same sentence — someone will read a file — and that sentence is
what the gates exist to replace.*

## 2026-08-25 — three treatments measured off user-supplied reference shorts

The user named three shorts and three problems. Every number below came from
a frame of those reels, not from taste (G23 discipline applied to look, not
just timing). Assets in `scratchpad/refs`, measurements reproducible.

**1. CAPTIONS — a plate, and smaller (ref vIAH9SaCNvo).** Measured: 40px cap
height in its 720-wide frame = **60px at our 1080**, uniform, on a
translucent dark rounded plate that hugs the line. Two findings:
- Our BASE size was already close (57px cap). The visible problem was the
  missing plate — we carried an 8-direction contour ring instead, which
  thickens every glyph over a bright page and still loses to busy content.
- Our EMPHASIS ran 1.3x (73px cap) — bigger than the reference's whole line,
  and it changed the line height mid-sentence. The reference carries emphasis
  on COLOUR at a uniform size. Ours is now 0.88 of the role with a 1.14 step.
- Plate alpha measured 0.30-0.50 across two samples; set 0.62 over dark
  grounds and 0.55 over bright, because a 0.40 plate on a terminal page is
  dark-on-dark and provides no separation (found by eye on the first plated
  render — the number the reference gave was for a plate over MIXED ground).
- The plate is sized for the WHOLE chunk from the start (unrevealed words
  hold their slot) — a plate that grows a word at a time jitters.

**2. OVERSIZED FOOTAGE TRAVELS (refs GQfEc8FHA48, fR8AkVkuM18).** Wide desktop
captures are fitted to the frame and moved sideways; tall pages and posters
scroll vertically. New `slide: "up"|"down"|"left"|"right"` + `slideSpan` on
footage, eased, implemented on objectPosition so `cover` still governs the
fit and the travel is exactly the asset's overflow.
**Do not stack it on a recording that already scrolls** — our mobile page
recordings carry their own scripted scroll, and a slide on top is two
motions fighting. It is for assets whose content is static: this reel's
3000x1520 ccusage table, which as a card rendered at a third scale and now
plays full-bleed with its columns legible.

**3. CTA (ref fR8AkVkuM18).** Measured: one word, neon **rgb(226,254,14)**,
cap height 150px (font ~207) at 1080x1920, centred at **67% of frame
height**, PERSISTING while the ordinary captions keep running above it. No
"COMMENT" label stacked over it, no question card, no simulated comment
field. Our first keyword variant stacked a label and suppressed captions,
which turned the closing beat into a title card. Now only the single caption
chunk that would print the keyword twice is dropped, and compile defaults
`captionBottom: 880` on a keyword CTA so the caption clears the keyword —
without it they render through each other.

All six numbers are asserted by `tools/test_capture_defaults.py` (13 checks,
run by doctor): a measured treatment that lives only in a component can drift
back to taste in one edit.

## 2026-08-25 — the EDITOR'S PASS becomes a step (user directive)

*"Think of yourself as a years-experienced video editor... and edit as per
the need of the topic, script."* The gates prove a reel is not BROKEN; they
cannot tell you it is not EDITED. claude-eating-tokens passed every gate
with sixteen beats that nearly all carried the same `zoomDir: "in"` — a
slideshow with a green light.

New step in AGENT.md §3b, with `tools/cut_sheet.py` to make the cut legible:
every beat's duration and motion side by side, in order, plus the places an
edit usually needs a decision (adjacent beats moving identically, the
longest beat sitting late, beats declaring no movement at all). It asserts
nothing — the five questions are in the manual, and the answers are
judgement.

What the pass changed on this reel, and why:

- **Two caveman shots that both pushed in** -> the first ESTABLISHES (wide,
  push), the second LANDS THE CLAIM (held at 1.5x on the About line, where
  "cuts 65% of tokens" is readable). Same asset, two moves, is a cut.
- **A push on a recording that already scrolls** -> held and cropped tighter
  (1.14x). Two motions arguing is worse than one.
- **The 6.9s ponytail shot at 40s**, the longest in the reel and sitting
  where attention is thinnest -> split on its own second clause ("it checks
  the standard library first"), the second half framed on the README's
  "~54% less code". Longest beat is now 5.62s and it sits at 21s, which is
  the reel's TURN — a hold there is confidence, not drift.
- **Two annotatezooms back to back** -> the second is a `sourceread`,
  because its line is a sentence being proved and that is the treatment
  built for reading a sentence.
- **The pivot line held dead still** — cut_sheet caught it on its first run,
  three minutes after being written. "These three cut the expensive half" is
  the hinge of the script; it now pushes in gently.
- **zoom + slide compose** (user, same message): the wide table slides to
  read its columns AND pushes 1.06x for depth. The slide reads; the push
  keeps it alive.
- **Captions down again** to 0.78 of the role (from 0.88). Stated as
  judgement, not measurement: the reference's 60px cap is its line height,
  but our plate makes the block read heavier, so matching its cap made ours
  look bigger than it. The eye is the instrument for type size on a phone.

**Same-session correction: scale cuts text on a frame-width capture.** The
editor's pass set `zoom: 1.5` on the caveman beat to make its README claim
readable, and the render showed the opposite — a mobile capture is 1080 wide,
exactly the frame, so the scale pushed half of every line off both edges.
Four beats had it. A full-width capture is framed by SLICE (`focusY`) and
MOMENT (`from`) at 1:1; scale is for assets wider than the frame. Compile now
prints an advisory with the asset's real width, and AGENT.md §3b question 3
carries the reasoning. Worth noting the sequence: the editorial judgement was
right (that claim should be readable), the mechanism was wrong, and only
looking at the rendered frame told the difference.

## 2026-08-25 — the short-form master framework installed as the standard

User supplied `frameworks/short-form-master.md` and asked for it in action.
It is now read-order item 0 in CLAUDE.md: the STANDARD this repo builds to.
Where it and RULES.md disagree, RULES.md wins — the gates encode failures we
have actually had, and a framework cannot overrule evidence.

**Most of it is judgement and stays a document** — story engine, escalation,
pattern interrupts, information density, the editor's eye. Wiring judgement
into a gate is how taste ends up wearing a rule's badge (the G18 lesson).

**Three of its rules are not judgement.** They have a right answer, they fail
silently, and each is a promise to the viewer rather than a matter of taste,
so they are code: `tools/framework_check.py`, run by
`script_approval.py propose` (a leak is caught BEFORE the user is asked to
approve the words) and self-tested by doctor.

- **F1 REVEAL TARGET.** A campaign that withholds an identity for a DM must
  not disclose it in narration, on-screen text, or CTA/packaging copy — and
  clues that COMBINE are a disclosure, so the check fires when every word of
  the target appears across a surface. Leaking it spends the delivery and
  makes the CTA a lie. **F4** is its other half: with a target withheld, the
  SUBJECT must still be spoken, or curiosity has become confusion.
- **F2 CERTAINTY.** "Never convert uncertain information into certainty."
  The research ledger already recorded each claim's strength; nothing checked
  that the SPOKEN words matched it. A `single`- or `disputed`-tier claim
  carrying "will / confirmed / guaranteed" with no qualifier now fails.
- **F3 SOURCE POLICY.** Research sources and footage sources are separate
  categories and a restriction on one does not imply the other — the
  framework is explicit, and the check honours it: `official-footage-only`
  lets third-party RESEARCH through while refusing third-party MEDIA.

Scaffolded so they cannot be forgotten: `new_job.py` writes `subject`,
`reveal_target` and `source_policy` into every brief, and structure.md now
opens with the STORY ENGINE sentence (§4A) — *a viewer who believes X
discovers Y, which matters because Z*. If it cannot be filled there is no
reel yet, only material.

**Applied to claude-eating-tokens, and it changed two things:**
1. `reveal_target: none`, recorded WITH ITS REASONING — the reel names every
   tool it recommends, so nothing is withheld and the CTA delivers links for
   four already-named tools. That is honest but it is also weaker curiosity
   than the framework's §6 flow can produce, and writing it down makes the
   trade a known choice rather than an oversight.
2. Every asset now declares **proof** or **illustrative**. The one that
   changed hands: `term-clear` is ILLUSTRATIVE — its figures are at this
   machine's real session scale but the transcript is a recreation, not a
   captured session. The ccusage terminals stay PROOF: the DATA is real
   output (kept in `_sources/`), only the chrome is styled. That distinction
   is the quiet way a sourced reel becomes untrue, and it now has a field.

## 2026-08-26 — "our system still generates very poor scripts": the diagnosis

User pasted the claude-memory-everywhere draft. Ran it through our own
`check_script` first, before defending anything: it reported a NUMBERS note
and nothing else. The user was right, and the checker was the reason.

**What was actually wrong with that draft**, read as a writer:
its structure.md was excellent — it declared the story engine, chose
misconception -> reality -> proof -> limit -> consequence, and said in as many
words "not the four-section feature list the announcement itself is organised
as." Then the script was that feature list. **The plan was right and the
writing ignored it, and nothing in the pipeline noticed.**

The visible symptom was one sentence: *"Back to what it refuses to write
down."* The draft promised that payoff in sentence 4, spent nine sentences on
unrelated features, then wrote a signpost admitting the detour. A viewer
feels that as being lost.

**New check: ABANDONED LOOP** — derived, not invented. Measured the promise ->
navigation-back distance across all 13 scripts in the repo:

| script | navigates back to | detour |
|---|---|---|
| iphone18-colors (approved) | — (holds a loop 11 sentences, never signposts) | none |
| claude-eating-tokens (approved) | short aside | 2 |
| iphone-18-pro (approved) | forward reference | none |
| **claude-memory-everywhere** | **sentence 4** | **9** |

So a long deferral is a GOOD loop; what no approved script does is announce a
return after wandering. Threshold 5 — past a deliberate aside, well under the
observed failure. Fires on the real draft, silent on every approved script and
on a two-sentence aside. `"going back to 2019"` is excluded: a date is not a
navigation.

**And the craft loop itself was missing.** The rewrite took five passes, each
one driven by the checker's own output: v1 traded the abandoned loop for NO
loop; v2 fixed bridges but broke cadence; v3 planted a loop the payoff never
echoed (the detector wants a DISTINCTIVE word returned, which is also what
makes a callback ring); v4 landed the callback but ran 232 words, 84-99s
against a 60-80s band; v5 trimmed to 194. That is the loop that was never
being run — writing, measuring, rewriting — and it is now written down as the
expected number of passes, not a sign something went wrong.

Rewrite lives at `jobs/claude-memory-everywhere/script-rewrite.md` — NOT over
the other session's `script.md`, which is unapproved and theirs to merge.

## 2026-08-26 — three root causes behind "every script sounds the same"

User: *"Why does it follow the same structure instead of considering the
topic? Every script says 'here's the part that matters most.' Why does it
build the shot plan before approval? And it took twenty minutes."*

**1. THE CHECKER WAS WRITING THE HOUSE TIC.** `check_script`'s NO OPEN LOOP
test matched a phrase list (`FORWARD`), so a script that did not use a listed
phrase was told it had no loop — and every writer, human or model, reached
for the listed words. Measured across the corpus:

| phrase | scripts |
|---|---|
| `here's the` | 8 |
| `the catch` | 4 |
| `the part almost nobody noticed` (verbatim) | 3 |
| `tell me in the comments` | 3 |

Two fixes, opposing forces:
- **`house_tics()`** flags any 3-5 word rhetorical phrase already used in
  another script (proper nouns and numbers excluded — a subject recurring
  across scripts about that subject is the subject, not a tic). Reported by
  `propose`, so reuse costs something.
- **`open_loop` now reads STRUCTURE, not vocabulary**: a withheld
  enumeration ("Four things it won't write at all") is a loop when the items
  arrive later, and an agenda when they arrive at once — which is the exact
  test the code already applied to "three changes are coming". All five
  hand-judged cases still pass.
  Together: you must open a loop, and you may not open it in last reel's
  words. The rewrite of claude-memory-everywhere failed the tic check on my
  own first draft ("the part that matters"), which is how I know it works.

**2. THE SHOT PLAN WAS BUILT BEFORE APPROVAL.** `plan_shots.py` has always
SAID "turn an approved script into a shot plan" and only ever checked that
the file existed. Every shot is phrase-anchored, so a plan written before
approval is invalidated by the first word changed — and the repair then looks
like progress. `--write` now refuses without `approval.json`, and refuses
again if the script has drifted from the approved hash. Reading without
`--write` stays open, because that is often how you decide it is ready.

**3. TWENTY MINUTES WAS ROUND TRIPS, NOT THINKING.** Each rewrite pass cost
four or five commands. `tools/script_doctor.py` runs all of them in one call
(0.12s). The craft loop itself — 3-5 passes — is correct and stays; it is now
documented in AGENT.md §1c as the expected shape of the work rather than a
sign something went wrong.

Bonus catch: script_doctor's first run flagged `for Free, Pro and Max` as the
sell phrase "for free". A plan tier is a proper noun; the marker is narrowed.

## 2026-08-26 — framework implementation audit: three gaps found and closed

Asked to confirm the framework was really implemented, so I audited its 12
sections against what code actually enforces rather than asserting it was
done. Three gaps were real.

**1. §2 brief — 4 of 14 fields.** subject, reveal_target, source_policy and
cta_keyword were scaffolded; audience, platform, goal, core_value,
desired_action, target_duration, tone, footage_constraints,
credit_instructions and deliverables were not. Each one DECIDES something
downstream (platform decides packaging; tone decides diction; credit
instructions decide whether a chip is drawn at all), so a brief missing ten
of them is a brief that gets answered by default. `new_job.py` now writes all
fourteen, each with the decision it drives noted beside it.

**2. §3 claim taxonomy — two classes had no word.** Ours was
official/multi/single/disputed, which covers CORROBORATION only. The
framework's six classes add **Prediction or Analysis** (a forecast is not a
report, and §3.6 requires naming whose it is) and **Unsupported** — the one
class §3.5 says must be excluded. Now: `prediction` is a valid tier and
**F2b** fails a forecast whose spoken words never say whose it is;
`unsupported` is REFUSED by research_check with the framework's own remedy
(narrow it, attribute it, reframe, or cut — §3.14: adding "reportedly" to an
unsupported claim does not make it publishable).

**3. §11 had no audit.** The pre-publish checklist existed as prose across a
dozen tools. `tools/prepublish.py` runs the measured half — framework check,
claim ledger, approval freshness, gates, packaging — and prints the
judgement half as QUESTIONS: the confused-viewer, boring-article, payoff and
removal tests, plus retention, visual, audio, CTA and coherence. The split is
deliberate: a machine cannot answer whether this reads as one creative
decision, and a checkbox that pretends otherwise is worse than the question.

It earned itself immediately: first run on claude-eating-tokens reported the
reel is rendered and **has no packaging.md** — true, and nothing else had
said so.

## 2026-08-26 — mac-mini-m6-m5pro: `annotatezoom.focus` is SOURCE PIXELS, not a fraction

**RAW NOTE.** Every receipt in the first render came back as a near-blank
cream card — a tiny caption and credit chip floating over flat background,
zero source text visible. `lint_frames.py` correctly flagged 82-90% dead
space on eight scenes and the render still passed every gate, because no
gate inspects rendered pixels.

**ROOT CAUSE.** `AnnotateZoomProps.focus` is typed `{x,y,w,h}` in **source
pixels** (`src/components/AnnotateZoom.tsx`), not the 0-1 fraction used
elsewhere in this codebase (`topFocusX`/`bottomFocusX` on `split`, CSS
`objectPosition`). I wrote fractional values (`{x:0.5, y:0.72, w:0.85,
h:0.18}`) by analogy with those other props. On a 1080x2340 source that
focus rect is a ~1x1 pixel box near the top-left corner — the camera
"settles" on a single pixel, which upscales to a flat, near-uniform colour
field. `srcWidth`/`srcHeight` are also required props I had left unset
entirely; nothing defaults them, and nothing in `compile_shot_plan.py`
back-fills them from the actual image file.

**Two lessons, not one:**
1. **A component-local prop name that LOOKS like a pattern used elsewhere
   is not evidence it follows that pattern.** `focus` reads exactly like
   `topFocusX`/`face-x.txt` (both fractions of frame width) but is
   documented, in the same file, as "region in SOURCE pixels" — the
   docstring was right there and unread.
2. **A broken visual can pass every mechanical gate.** G39 checks that the
   *spoken words* match a scene's declared `covers` claim; nothing checks
   that the *pixels* match the claim. The only thing that caught this was
   pulling actual full-resolution frames and looking — exactly what
   RULES.md's critic-pass step says to do, and exactly what gets skipped
   under time pressure once the pipeline says "GATES PASSED".

**DISTILLED RULE.** Before trusting any scene-prop shape, read the
component's own TypeScript interface, not a sibling prop's convention —
and after the first real render of any new receipt/annotatezoom asset,
pull an actual full-resolution frame (not just the lint thumbnail sheet)
before treating a green gate run as "done". Whole-page mobile captures
(1080x2340 or taller) need their focus rect measured on a pixel grid
(`ImageDraw` gridlines every 200px, as used for `face-x.txt`) — eyeballing
proportions on a scaled-down preview is not precise enough at this scale.

**Also fixed in the same pass:** four pairs of back-to-back scenes reusing
one static image with no visual change (`split`/`annotatezoom` clauses of
one sentence each getting their own scene) — `lint_frames.py`'s
`[DUPLICATE]` check is hard-blocking regardless of gate classification.
Fix was to MERGE the clauses into one scene per continuous visual, not to
force artificial variation between them — a sentence spoken over one held
image is one beat, not two.

### Treatment history — mac-mini-m6-m5pro

- mac-mini-m6-m5pro (Apple's Mac mini M6/M5 Pro refresh, framed as the
  price-hike-vs-specs argument rather than a flat feature rundown, per
  user direction): split hook (Apple's own mac-mini product page — "mini"
  wordmark over the real device photo, "From $899" — / face); NEW
  `priceladder` use for a genuine TWO-HOP price change ($599 to $699 in
  June, $699 to $899 in August — two real rows, not one row overstating a
  single jump); five official Apple Newsroom receipts (M6 2nm/cores,
  M6 AI-performance paragraph, M5 Pro cores, M5 Pro memory/bandwidth,
  pricing-and-availability, pre-order/Srouji-quote) plus one Macworld
  headline receipt for the price-hike claim itself (Apple never states its
  own price history, so that claim is carried by outlet reporting,
  credited on screen); honesty beat on the unchanged 256GB base storage;
  closing take reordered to land AFTER the availability beat, not before,
  so the reel ends on the payoff line rather than trailing into logistics.
  No music (standing rule), no CTA (user directive, dropped after the
  first review pass — the reel closes on the facecam take instead).
  9 SFX cues across 5 roles (transition/popup/impact/shutter/reveal).
  18 scenes / 75.4s / facecam 26.5% (above the news 10-20% band — accepted
  deliberately: the honesty beat + closing take is one continuous
  direct-address run and splitting it for a percentage would have hurt the
  ending more than the percentage helps). −14.5 LUFS, TP −3.9 dBFS.
- → next reel must introduce at least one new treatment. Already used and
  not to be repeated as the SAME shape next: `priceladder` for a
  multi-hop price change (the technique is reusable, the exact "two
  strikethrough rows, dated" layout is now used); a single Newsroom
  paragraph mined for 2-3 separate annotatezoom regions across consecutive
  clauses of one sentence.

## 2026-08-26 — a stale constant cost a reel a whole section of its source

The engine predicted this reel's runtime with a words-per-second band measured
at voiceSpeed **1.05**. The locked speed has been **1.12** since 2026-08-25.
Nobody re-measured, and nothing in the pipeline could notice, because the
constant's own comment said "measured at the locked 1.05" — accurate, and
therefore invisible, since the label lives in the source and the decision
happens at the propose prompt.

**What it cost, measured not guessed.** The first master delivered 199 script
words in 67.50s = **2.95 wps** against a predicted 72-85s. Thirty-six words of
headroom existed. At the rehearsal stage that phantom overrun had already
caused a named section of Anthropic's announcement — "Memory updates as you
chat" — to be cut from the script, and the cut was written up in questions.md
as a deliberate editorial trade. It was not a trade. It was arithmetic from the
wrong voice.

**Distilled rule: a measured number must carry the CONDITIONS it was measured
under, in a form the code can check — not in a comment.** `WPS_BY_SPEED` is
now keyed by speed, each row carries its provenance, and a speed with no
measurement resolves LOUDLY (`NO MEASUREMENT AT SPEED x`) instead of silently
borrowing another speed's numbers. The per-reel `measuredWps` hatch had existed
since 2026-08-22 for exactly this and went unused, because nobody knew the
default had gone stale underneath them. An escape hatch does not help when the
thing you would escape looks correct.

Second-order note worth keeping: the 1.12 row is TWO masters (2.61 and 2.95)
and is marked THIN in the table. Two points spanning 0.34 wps is not a band, it
is a hint. Do not tighten it until there are four.

## 2026-08-26 — whisper disagreeing with the script is evidence, but only when it survives priming

RULES §11 says a whisper `base` misspelling is not proof of mispronunciation.
This reel found the other half of that rule.

Three deltas against the approved script. **"Cowork" heard as "call work"** was
`base` being wrong: `medium` heard "co-work" cleanly at both instances, and the
brand-glossary entry added before generating had done its job. **"25" heard as
"25th"** is the TTS reading a date correctly and needs a caption correction,
not a re-record. **"leaves alone" heard as "lives alone"** survived `base`,
`small` at two window sizes, and `medium` — and flipped to "leaves" only when
whisper was primed with a sentence containing the word.

**Distilled rule: escalate the model AND test the prior.** A transcription that
holds across model sizes is evidence about the audio; one that flips under
priming is evidence about the language model. Run both before spending credits
— and prefer rewording to re-recording, because a word the synthesiser fumbles
once will fumble again. "leaves alone" became "stays out of": same meaning,
unambiguous vowel.

## 2026-08-26 — the approval beat plan named the camera move, not the frame

`beat_plan.py` exists so the user approves a plan they can picture. Its
`sourceread`, `annotatezoom` and `receipt` rows rendered FIXED strings — "a
screenshot, zooming slowly into the highlighted region" — which describes the
CAMERA and nothing on the page. On this reel 18 of 26 beats were one of those
three types, so 70% of the plan said nothing about what was being approved.

Same fault the file's own floatcard note recorded on 2026-08-22 ("describes the
CONTAINER and not one thing inside it"), reintroduced in three sibling types.
They now resolve the manifest asset, name the artefact by what it IS (a still
says "a screenshot", never "a clip"), and print the claim the highlight proves.

Two things learned while fixing it, both now tested: a `shows` field is written
for the BUILDER and runs 60 words, which is unreadable inline, so it is cut to
its gist; and one asset used across four beats printed itself four times, so
repeats shorten — but a shortened repeat must still name WHICH asset, because
"the same screenshot again" identifies nothing once a plan interleaves two.

## 2026-08-26 — simulate the crop before the render, not after

Every `annotatezoom` frame was composited in PIL — crop, fit, blur-fill,
annotations drawn — and looked at, before anything was rendered. It caught four
defects that no gate and no beat plan could:

- a focus rect that sliced the highlighted row's "Meal Planning" into
  "Planning". The HIGHLIGHTED row in that screenshot is inset further left than
  its siblings, which is invisible until something crops it.
- three rects that were 15:1 and 8:1 ribbons, filling **4-8% of frame height**.
  In-bounds, geometrically valid, and nearly empty frames.
- two rects ending mid-text-line, slicing glyphs horizontally.

**Distilled rule: `focus` is in SOURCE pixels and every intuition about it is
wrong.** A rect can be in bounds, land on the right words, and still render as
a ribbon or a mid-word cut. The simulation is ~20 lines and runs in a second;
the render is minutes. Do it first. The same pass also settled a judgement
call by eye — beat 17's three candidate framings were composited side by side,
and the two "tighter, more legible" options turned out to be a 7% ribbon and a
left-edge mid-word cut.

## 2026-08-26 — the framework's own lesson, applied to the framework

User asked a third time whether the master rule was really in force. It was
not, and the reason is the one this repo was built around:

**The operating stance was in a FILE, not in CONTEXT.** `CLAUDE.md` loads
automatically at the start of every session. `frameworks/short-form-master.md`
was read-order item 0 — which still means *a session has to open it*. I had
put the standard exactly where "loaded every session" had already failed
twice before (the style mapping; the capture defaults), and then reported it
as implemented. Grep settled it: zero occurrences of the master rule in
auto-loaded context.

Fixed: §12 now sits verbatim in CLAUDE.md, above the machine-facing sections,
with the split stated — what is CODE (framework_check, prepublish) and what
is YOU (the story, the escalation, the edit, the ending, which no gate will
catch you skipping).

**Two more clauses were prose.** Both are named in the user's own rule:

- **The AutoDM flow** (VALUE → CURIOSITY → DESIRE → ASK → DELIVERY) was
  checked by nothing. Now **F5**: the ask must not land in the opening third
  (an ask before value is an advertisement with a story attached), it must
  say what the viewer RECEIVES, and a brief whose goal is comment/follow but
  whose script never asks for anything fails.
- **`credit_instructions`** was scaffolded the same day and read by nothing —
  a field nobody reads is a decision nobody made. It now sets `noCredits`
  with the brief as the recorded reason, so G47 still refuses a silent
  switch-off, and provenance stays in the manifest either way.

And `prepublish.py` gained the framework's own reveal-handling questions:
has authentic footage been left alone, and if branding is naturally visible,
does the promised reveal still mean anything.

The pattern worth keeping: **every time I said "it's implemented", the thing
that made it true was a grep, not a memory.**

## 2026-08-26 — the master rule gets an audit, so the answer stops being mine

Fourth time asked whether the framework is implemented. Three of those
answers came from me and one was wrong — the operating stance was sitting in
a file that loads only when opened, which a single grep would have disproved.
An answer that depends on my memory is worth what my memory is worth.

`tools/framework_audit.py` lists every clause of §12 with the thing that
makes it true, and RUNS each probe. 36 clauses:

| kind | n | meaning |
|---|---|---|
| CODE | 24 | a check with a right answer; delete it and the audit fails |
| SCAFFOLD | 6 | a field or section a job cannot start without |
| STANCE | 1 | text in AUTO-LOADED context, not a file that must be opened |
| JUDGEMENT | 5 | no probe can decide it — the audit names WHERE it is exercised |

The judgement rows are the important design decision. Escalation, a strong
ending, pattern interrupts, selective silence, and leaving authentic footage
alone cannot be settled by a machine. Listing them as "ok" with a pointer to
where they are exercised keeps them visible WITHOUT pretending they are
automated — the alternative is a green checkmark that means nothing, which is
how taste ends up wearing a rule's badge.

It earned itself on the first run by failing a clause: the
"do not damage authentic footage" probe spanned a Python string break and
matched nothing. The clause was fine; the PROBE was wrong — which is exactly
the failure an audit is supposed to surface, and the reason each probe greps
a real fragment rather than trusting a filename.

doctor runs it, so a clause that quietly stops being enforced fails the first
command of the session instead of waiting to be asked a fifth time.

## 2026-08-26 — annotatezoom fits the SOURCE, so a `focus` inside a big sheet renders small

The reel's UI evidence is three official Anthropic screenshots at 2048x1152.
Ten beats framed regions of them with `annotatezoom` + `focus`. Every one
rendered as a **small card adrift on a near-empty cream field** — eleven
DEAD SPACE flags, and two adjacent beats hashed as near-identical and blocked
the lint.

The cause is that annotatezoom fits the SOURCE image and then settles toward
the focus, so a 900x880 region inside a 2048x1152 sheet is drawn at the sheet's
scale, not the region's. A PIL simulation had predicted 55% fill; the render
gave about 20%. **The simulation was modelling the wrong component.**

Two fixes, and the second only exists because of the first:

1. **Bake the crop into its own asset** and point the beat at that, with
   `focus` = the whole image. Now the component fits the region itself. The
   topic-name column went from 36% to 61% of frame height.
2. **Then set the field by measured brightness.** Baking removed the orange
   margin, so annotatezoom's blurred-self fill became WHITE — a white card on a
   white field. Every baked crop is now measured (`mean > 170` -> `bg: "black"`),
   which put the white cards on the dark editorial field and took DEAD SPACE
   from eleven flags to two.

**Distilled rule: a simulation is evidence about the simulation.** It caught
four real defects before the first render and then confidently mispredicted the
fill, because it modelled the geometry and not the component. Simulate to find
crops that are wrong; render to find out how they look.

### Treatment history — claude-memory-everywhere

- claude-memory-everywhere (Anthropic memory announcement — a news reel built
  almost entirely on FIRST-PARTY evidence, which is new here: three official
  product screenshots embedded in the announcement plus a mobile capture of the
  post itself, no third-party footage at all): split hook (baked PORTRAIT crop
  of the Topics file list above the presenter, NO display type — see below),
  `receipt` on the post masthead with the highlight landing on "August 25,
  2026", NINE `sourceread` read-alongs across four different regions of one
  mobile capture (highlights accumulate forward down the page, never
  backwards), EIGHT `annotatezoom` beats on BAKED crops of the official
  screenshots on a `bg: "black"` field with box/underline marks timed to
  vo.json onsets, `wordcascade` for the five sensitive categories with
  `bottomSrc` facecam filling the 1.68s before the first word is spoken,
  `checklist` with all four rows in the `no` state ("NEVER STORED") for the
  refused list, four facecam beats (opening promise, the take, the loop plant,
  the close), 8 SFX, no music, no CTA.
- **The hook carries NO display type, deliberately.** Two passes proved it
  should not: the type landed across the topic rows and was unreadable, and
  because ONE TEXT SYSTEM saw the headline speak the narration's words it
  suppressed the caption chips — so the frame carried two texts, one illegible
  and one missing. Removing the headline gives the chips back, and the chips
  name the brand on mute, which is what the headline was there to do.
- -> next reel must introduce at least one new treatment. Already used and not
  to be repeated as the SAME shape next: a `checklist` whose rows are ALL `no`
  as the payoff of a withheld-list loop; `wordcascade` + `bottomSrc` to cover
  the gap before its first spoken word; baked focus-crops on `bg: "black"` as
  the general answer to a wide UI screenshot in a 9:16 frame (borrow the
  TECHNIQUE freely — it is now the documented default — but not the specific
  "white card on black, box on the control" composition three times running).

## 2026-08-26 — "the voiceover is flat": measured, and it is the CLONE

User: *"Voiceover is still so flat, no energy, no emotion... the way it starts,
like the creator is fumbling."* Correct on both counts, and both are now
numbers rather than impressions.

**FLAT — measured against the user's own reference reels.** Pitch standard
deviation in semitones, same estimator on all four:

| clip | pitch sd | range |
|---|---|---|
| creator reference #1 | 3.74 | 11.6 |
| creator reference #2 | 5.00 | 16.3 |
| creator reference #3 | 6.63 | 17.4 |
| **our shipped master** | **2.83** | **9.1** |

**FUMBLING — it is inverted stress.** In the flagged opening, `"the"` is held
0.34s while `"reading"` — the word carrying the meaning — gets 0.28s; then
"why the top" rushes past at 0.14s each. Function words longer than the
content words beside them is a reader who does not know which word matters.
Three instances in the reel.

**THE CAUSE IS THE CLONE, and settings do not touch it.** Two avatar probes
(stability 0.42→0.28 + style 0.35→0.62; and eleven_v3 at style 0.70) came
back at 2.02 and 2.74 against a 2.83 baseline — one WORSE, one unchanged.
Then the decisive test, TTS only, same text, same speed, only the voice
different:

    our clone "iGeeks Blog"    1.86 semitones   range  4.6
    HeyGen stock voice "Shaun" 3.27 semitones   range 10.6

A clone reproduces the expressiveness of its training audio. The source read
was level, so the clone is level, and no stability/style value invents range
that was never recorded. **Do not spend more credits tuning this clone** —
recorded in `config.json` so a future session does not repeat the experiment.

**What is now in place:**
- `tools/vo_qc.py` measures the READ — pitch variation, pitch range, stress
  inversion — with the 3.5-semitone floor taken from the flattest real
  creator, not invented. Every check in this repo looked at the script;
  nothing had ever listened to what came back.
- It runs inside `avatar_handoff prepare`, so a flat read is caught where the
  VO first exists — before a frame is rendered against it.
- The master-rule audit gained a clause for it: *the READ is measured, not
  just the words.*
- `references/voice-clone-recording-spec.md` says what to record to fix it,
  and sets the acceptance test: a new clone ships only if it clears 3.5.

**The honest limit:** nothing here fixes the current reel's read. The fix
needs new source recordings from the user, which is the one step no tool can
do.

## 2026-08-26 — Soniqo / IndexTTS2 evaluated for emotion control: measured verdict

User asked whether soniqo.audio could add emotion, tempo and pause control to
the voiceover. Installed it (`brew install speech`, homebrew-core, on-device,
Apple Silicon) and measured rather than speculated.

**It does have the controls**: `--indextts2-emotion` (10 presets or an 8-value
vector), `--indextts2-emotion-weight`, `--indextts2-speaking-rate` (0.5-1.5),
`--indextts2-max-pause`, and `--indextts2-emotion-audio` — a SEPARATE emotion
reference from the voice sample. Cloning needs 5-30s, not minutes. Runs
locally: no per-use cost, no queue.

**Measured, same voice sample and same line throughout:**

| synthesis | pitch sd | identity vs his reference |
|---|---|---|
| HeyGen clone (what ships today) | 1.86 | 0.976 |
| Soniqo, neutral | 2.25 | **0.984** |
| Soniqo, `--emotion happy` | 2.43 | 0.936 |
| Soniqo, emotion transferred from an expressive sample | 2.75 | 0.957 |
| Soniqo, `--emotion eager` / `excited` | **2.99** | 0.952 |
| *control: a genuinely different speaker* | 3.27 | *0.924* |
| *target: the user's own creator references* | *3.74-6.63* | — |

**Two findings, and the second is the one that matters.**

1. Emotion control is real: 1.86 -> 2.99 is a **61% increase** in pitch
   movement. But it still lands **below the 3.5 floor** taken from the
   flattest real creator. It narrows the gap; it does not close it.
2. **Expression is being bought with identity.** Neutral scores 0.984 —
   better than the HeyGen clone itself. Every emotion preset moves it toward
   the different-speaker control: eager 0.952, happy 0.936, against 0.924 for
   a different person entirely. The more emotion asked for, the less it is
   his voice.

**The reason is the reference, and it invalidates nothing but explains
everything: the 20-second sample was extracted from the existing FLAT clone's
own output.** So the test cloned a flat voice and then asked it for energy.
The emotion presets were fighting the source, which is exactly why they cost
identity to make progress.

**Therefore the recording script is still the fix, not the workaround.** With
genuinely expressive source audio, the emotion controls would be adding to a
voice that already moves rather than dragging one that does not. The correct
sequence is: record -> re-clone -> measure -> only then decide whether emotion
control is needed on top.

**Identity caveat RESOLVED, favourably:** a 20-second reference preserved
identity BETTER than the full HeyGen clone (0.984 vs 0.976). Short reference
length is not a risk here.

**Licence caveat RESOLVED, with a named risk:** IndexTTS2 ships under the
**bilibili Model Use License** (not Apache 2.0, despite its HuggingFace card
— the inconsistency is itself a smell). §2.1 grants royalty-free use; §2.2
requires a separate licence only above 100M MAU or RMB 1B revenue, so
commercial use at this scale is permitted. Governed by PRC law, Shanghai
arbitration. **CosyVoice, in the same CLI, is true Apache 2.0** and is the
clean fallback if that matters more than the finer controls.

New tool: `tools/voice_similarity.py` — MFCC fingerprint cosine similarity,
which is how every number in the identity column above was produced. Its own
output insists on a different-speaker CONTROL, because an absolute similarity
score has no units worth trusting.

**Second attempt, using the HeyGen voice ID directly as the clone source
(2026-08-26).** The first reference had been extracted from a RENDERED reel,
so it carried mp4 encoding and the loudness master; a clean 44.1kHz sample
straight from `create_speech` should have been strictly better. It was worse
on both axes:

| clone source | source's own pitch sd | output pitch sd | identity |
|---|---|---|---|
| slice of the rendered reel | 3.13 | **2.99** | 0.952 |
| raw TTS from the voice ID | 1.92 | 2.79 | **0.922** |
| *different-speaker control* | — | 3.27 | *0.924* |

**The reference's own expressiveness is both the ceiling AND the identity
anchor.** Cloning from the flatter source produced a flatter read whose
identity score fell BELOW the different-speaker control — i.e. it stopped
sounding like him at all while still not gaining energy.

Two independent attempts now put the ceiling at ~3.0 against a 3.5 floor, and
both used a reference derived from the flat clone. There is no configuration
of engine, emotion preset, or reference cleanliness that fixes this, because
the range was never in the source. **Only a real expressive recording moves
the ceiling** (`references/voice-clone-script.md`).

Correction to an earlier note: `--clean-reference` (Sidon restoration) is
**not wired for indextts2** — it applies to qwen3/cosyvoice/voxcpm2/f5/higgs/
indic-mio. Cleaning a phone recording before cloning therefore means either
using one of those engines or running the restoration as a separate pass.

**Was Soniqo implemented as documented? No — three deviations, corrected
2026-08-26.** Checked my own usage against their stated spec rather than
defending it:

1. **"No heavy compression"** — the reference that produced the best number
   (2.99) was a slice of the RENDERED MASTER, i.e. after `loudnorm` + a
   limiter. Directly against their spec, and the good score was partly an
   artefact of it. Fixed by cutting the reference from
   `avatar-master-raw-v3.mp4` — the avatar render BEFORE our mastering.
2. **Never used two of the three controls.** Their own example passes
   `--indextts2-speaking-rate 1.35` and `--indextts2-max-pause 0.05`. I had
   only ever set `--indextts2-emotion` — while telling the user the toolkit
   offered tempo and pause control.
3. **Never tested CosyVoice**, the Apache-2.0 engine, which their docs say
   *"Always pass the transcript... skipping it costs accuracy and produces
   mid-utterance drifts."* Now tested with the reference's real transcript.

**Doing it properly changed the answer on identity, not on the ceiling:**

| configuration | pitch sd | identity |
|---|---|---|
| HeyGen clone (ships today) | 1.86 | 0.981 |
| Soniqo, non-compliant compressed reference | 2.99 | 0.950 |
| **Soniqo per spec** (pre-master, 16k, all three controls) | 2.54 | **0.973** |
| **CosyVoice per spec**, with transcript | **3.00** | 0.954 |
| *control — a different person* | *3.27* | *0.938* |

Per-spec configuration bought a large identity gain (0.950 -> 0.973 against a
0.938 control) at a small expression cost. CosyVoice reaches 3.00 — the best
expression of any run — and carries the clean Apache-2.0 licence, but sits
closer to the control on identity.

**The ceiling did not move.** Every correctly-configured run lands 2.5-3.0
against a 3.5 floor, because all of them clone the same flat source. Doing it
by the book improved fidelity and confirmed the diagnosis.

## 2026-08-26 — per-beat voice direction: built, measured, and it did NOT work

User's real goal, stated plainly: *"the idea is not going with a particular
version. The idea is adapt the tempo, energy and emotions as and when
required across the video."* Correct instinct — the framework already demands
exactly this of music (hook / stable pulse / build / accent / release / CTA)
and said nothing about voice because nobody had wired it.

Built `tools/vo_direct.py`: seven registers (hook, context, build, turn,
proof, payoff, cta), each with its own emotion, tempo and trailing silence,
one voice reference throughout, assembled into a single VO. A line can be
tagged `[turn]`; untagged lines get a register from their position in the arc.

**Result: 2.81 semitones — no better than the 2.83 that already ships, and
below the 3.00 of a single well-chosen setting.** Range 9.8, still under the
10.0 floor. Identity held well (0.965 vs 0.938 control), and runtime landed
at 57.4s against the master's 58.6s.

**Why it failed is the useful part.** Directed registers DO land — probed on
one line, IndexTTS2 gives hook 204Hz / turn 241Hz / payoff 202Hz, a real 3.0
semitones of intentional spread. But stitching differently-directed beats
does not raise the measure, because pitch sd is computed over the WHOLE file
and each beat is internally flat. Splicing flat pieces at different pitches
produces steps, not movement. **A voice that changes register between
sentences is still monotone inside them**, and inside is where a listener
hears energy.

So per-beat direction is worth keeping — it is the right architecture, it
costs nothing at runtime, and it will matter once the source has range — but
it is NOT a substitute for an expressive clone. Nothing measured today beat
3.00 against a 3.5 floor.

**Two real bugs found on the way, both of which would have poisoned every
future run silently:**

1. **`synth()` treated a pre-existing file as success.** A failed beat kept
   the previous run's audio and reported `ok`, so a "directed" VO assembled
   from 5 new beats and 8 stale ones from a DIFFERENT ENGINE measured 3.45
   and looked like a win. It now deletes the target first and prints the
   engine's own error.
2. **IndexTTS2's tokenizer rejects our house punctuation.** Proved by probe,
   not inferred: `"One: see it works"` is rejected, `"One, see it works"` is
   accepted; `"A test; another clause"` is rejected. Em-dash, colon and
   semicolon all fail with `unencodableText` — and this repo's script style
   uses all three constantly. `speakable()` maps them to commas, which is
   what they mean out loud. Without it, 8 of 13 beats failed.

**The fumble is fixable in the SCRIPT, today, with the voice we already
have.** Same words, same clone, same speed — the shipped hook as one compound
sentence ("...mostly the reading, not the writing — here's why the top fix
barely helps") versus three short ones ("...mostly the reading. Not the
writing. And the top fix barely helps."):

| | stress inversions | word-duration spread |
|---|---|---|
| one compound sentence | 1 (`'the'` 0.34s > `'reading'` 0.28s) | 0.26s |
| three short sentences | **0** | **0.38s (+46%)** |

A long compound line gives a TTS no clear stress target, so it lands weight on
whatever it meets — which is what the user heard as "the creator is fumbling".
Short declaratives hand it one idea per sentence and one obvious word to hit.
This costs nothing, needs no re-clone and no new engine, and it is the ONE
voice improvement available immediately.

**Decision for the next reel: keep the HeyGen voice.** Nothing measured beats
it enough to justify the trade — the best alternative (CosyVoice, 3.00 vs
2.83, +6%) is inaudible against a 3.5 floor and costs identity (0.954 against
0.981, with a stranger at 0.938). Switching would also add local synthesis,
concatenation seams, an untested HeyGen lip-sync path and re-derived anchors,
for a gain nobody would hear. Write shorter hook sentences instead, and
revisit the whole question once the re-clone exists.

## 2026-08-26 — the short-sentence hook, and a caption bug it exposed

**The rewrite worked for its stated purpose.** Hook split from one 16-word
compound sentence into three (7 / 3 / 8 words), regenerated, and the stress
inversion is GONE in the real audio: `'the'` 0.14s against `'reading'` 0.30s,
where the shipped version had `'the'` 0.34s > `'reading'` 0.28s. The fumble
the user heard was a script problem, and the script fixed it.

**With an honest cost:** overall pitch variation fell 2.83 -> 2.22. Short
declaratives give three small intonation arcs where a long sentence gives one
big one. The opening no longer stumbles; the read is marginally more even.
Worth it for the specific complaint, and it changes nothing about the clone
being the real ceiling.

**Keeping the open loop nearly got lost.** The first rewrite —
"...mostly the reading. Not the writing. And the top fix barely helps." —
reads well and KILLED the loop: the original's "here's why ... barely helps"
was a promise paid off thirty seconds later at "that's why it barely helps."
Dropping "here's why" turned a promise into a statement and the ending would
have summarised instead of arriving. Caught by `open_loop`, fixed by keeping
both halves inside the short sentences.

**And it exposed a caption bug that would have shipped a broken reel.**
Multi-word `caption_corrections` were applied to the CHUNK text AFTER words
are grouped three at a time. That works only while a phrase happens to sit
inside one chunk. The new read re-chunked as `"see it, CC"` / `"usage
charts, it"`, so `"cc usage" -> "ccusage"` matched nothing and **three of the
four tool names vanished from the captions of a reel whose whole job is
naming those tools** — silently, with every gate green.

Fixed at the word level: a matching run now collapses into ONE caption word
spanning the run's timing, so a name cannot be split by any future chunk
boundary. Same failure shape as the anchor matcher's compound splits — an
arbitrary grouping deciding what counts as adjacent. Regenerating a voice
moves every boundary, so this would have recurred on every re-render.

## 2026-08-26 — "is our script actually being humanized?" No. It never was.

User asked why em-dashes keep appearing in scripts when the repo has a
humanizer skill installed. Checked instead of answering: **every occurrence
of `humanizer` in this repo's code is a comment.** `check_script.py` mentions
it in a docstring, `showrunner.py` prints its name in a stage list,
`doctor.py` refers to it in passing. Nothing has ever invoked it. CLAUDE.md
said "run it after the word budget and before propose" — and that sentence
was the entire mechanism.

The em-dashes are the visible symptom, measured across the corpus:

| script | em-dashes | words | one every |
|---|---|---|---|
| claude-eating-tokens | 6 | 159 | **26 words** |
| iphone18-split | 7 | 242 | 35 |
| september-preview | 6 | 196 | 33 |
| grok-bot | 1 | 355 | 355 |
| apple-pay-india | 1 | 339 | 339 |

**New check: PAGE PUNCTUATION**, and it does NOT rest on the em-dash being an
"AI tell". It rests on two facts about this medium:

1. **A listener cannot hear one.** The voice renders it as a pause — exactly
   the comma or full stop that could have been written. It is a mark for the
   eye, in a medium with no eye.
2. **It breaks the synthesis.** Probed: IndexTTS2 rejects em-dash, colon and
   semicolon outright, and 8 of 13 beats failed on precisely this.

Threshold 1-per-60 words, sitting between the corpus's clean end (~1 per 350)
and its dense end (1 per 26). Advice, with a self-test both ways.

**And the docs now say what is true.** CLAUDE.md records that nothing runs
the pass, and `propose` prints a line at the last moment before approval
saying so. A skill that is installed, documented, and never executed is
indistinguishable from one that was never installed — except that it lets
everyone believe the work was done.

## 2026-08-26 — full engine audit: is everything wired, and does it fire?

User asked for a thorough pass over the whole engine, with the emphasis on
things "getting auto-triggered at the right time". Given how many
documented-but-never-executed capabilities turned up today, the audit had to
be mechanical rather than a read-through.

**`tools/wiring_audit.py`** puts every tool in exactly one bucket:

| bucket | n | meaning |
|---|---|---|
| AUTO | 55 | another program executes it |
| MANUAL | 14 | a human runs it, and a doc names it |
| LEGACY | 10 | one-off per-reel scripts, inert by design |
| **ORPHAN** | **0** | nothing runs it, nothing mentions it |

It found exactly ONE genuine orphan: **`ingest_screencap.py`** — a working
tool that turns an iPhone screen recording into a reel-ready clip and scrubs
the personal data out of it, mentioned in no document, so nobody would ever
reach for it. Now written into AGENT.md's scout step, where a real OS
demonstration is the thing you want. The legacy bucket exists so those ten
inert build scripts cannot hide the next real one.

Doctor runs the wiring audit every session.

**SKILLS CANNOT BE AUTO-INVOKED — only cued.** No code can execute a skill,
so "auto-trigger" means naming the skill at the exact moment its need
appears. A moment stated in a document is NOT a trigger: the humanizer had
one in CLAUDE.md for weeks and never ran once. Cues now fire off findings:

- `script_doctor` -> `viral-hook-writer` / `going-viral` when the hook or the
  loop is what failed; `humanizer` on a tic, an AI tell or page punctuation;
  `fact-check-workflow` when a claim is spoken harder than its evidence.
- `prepublish` -> `social` / `caption-and-hashtags` / `youtube-seo` when
  packaging is missing.
- `propose` -> `humanizer`, at the last moment before approval.

**Everything green, verified rather than assumed:** 115 gate checks, 66
script-pipeline checks, 13 capture defaults, 37 master-rule clauses,
framework and check_script self-tests, TypeScript clean, doctor ok.

**Two of my own test harnesses lied during this audit**, both from zsh not
word-splitting an unquoted variable: the first orphan sweep reported all 79
tools orphaned, and a suite loop reported two self-tests failing at exit=2
when both pass. Neither was a repo defect. Recorded because a broken CHECK
reads exactly like a broken SYSTEM, and the reflex has to be to verify the
harness before reporting the finding.

**One real open item:** claude-eating-tokens is rendered but has no
`packaging.md`, so `prepublish` correctly refuses it. That is the last step
before it can be posted.

## 2026-08-26 — hooks: skills now fire without anyone remembering

The user caught a real walk-back. Earlier in the day I said skills
auto-trigger; by the audit I had redefined "auto" as "a tool prints a line
naming the skill, and the agent notices." That is not a trigger, it is a
reminder, and this repo's whole history says reminders get skipped.

**What was actually missing: `.claude/settings.json` did not exist.** No hooks,
project-level or user-level, had ever been configured. Claude Code has a real
mechanism for running something at a defined moment and injecting the result
as an instruction, and the engine had never used it. That is the gap, and it
is now closed:

| Hook | Fires on | Makes automatic |
|---|---|---|
| `session_start.py` | SessionStart | `doctor.py` — the "first two commands" prose rule |
| `reel_precedence.py` | UserPromptSubmit | `news-reel` precedence + the anti-hijack rule |
| `skill_cue.py` | PostToolUse (Bash) | reads our `SKILL CUE:` lines, names the skill as an instruction |
| `guard_bypass.py` | PreToolUse (Bash) | denies direct remotion render, HyperFrames pipeline cmds, hard-reset/force-push |

**Proof, not assertion:** `skill_cue` fired live in the session that wrote it,
on a real `prepublish` run, and correctly pulled `social`,
`caption-and-hashtags` and `youtube-seo` off wrapped lines. Hooks load without
a session restart.

**The guards bit their own author three times, all the same bug.**
`guard_bypass` blocked the commit writing its own test (the test quotes the
commands it blocks); `skill_cue` fired on a `sed` that was only DISPLAYING a
cue; `guard_bypass` then blocked the CLAUDE.md section documenting itself,
because a markdown table's pipes and backticks split into flawless fake
commands. One lesson: **text about a command is not a command.** Matching is
positional now, heredoc bodies are data, and inspection commands cannot raise
a cue. Every one of those three incidents is a case in `tools/test_hooks.py`.

**Guarding the guard.** 55 checks in `test_hooks.py`, run by doctor;
`wiring_audit.py` now fails if a hook script is not named in settings.json,
because an unwired hook removes a trigger while looking exactly like nothing
is wrong — the identical failure shape as the tools it was built to find.

## 2026-08-26 — second full audit: the hooks themselves were broken

Asked to verify the whole engine again. The session's own SessionStart hook
reported "doctor timed out (>110s)" for a check that takes 15 seconds, which
was the first finding and the worst one.

**1. INFINITE RECURSION in the preflight (shipped, live).** doctor runs
`test_hooks.py`, which exercises `session_start.py`, which runs doctor. Each
layer only ended on a nested timeout. It was invisible when the hook was
written because doctor was wired to the suite in the same commit as the suite
was wired to the hook. Fixed with an inherited env guard
(`AIRE_PREFLIGHT_RUNNING`): the nested copy reports instead of recursing.
Real preflight now 14.2s. The guard is tested, not trusted — and the test
runs UNDER the guard so it cannot re-enter doctor either.

**Lesson: a hook that calls the thing that tests the hook is a cycle, and no
individual review of either file shows it.** Only running the real entry point
does.

**2. The precedence hook fired on maintenance prompts.** The repo is NAMED
"AI Reel Engine", so "go through our entire AI Reel Engine" tripped the reel
matcher. Tightened, and the test corpus is now REAL prompts from this
project's history — nine production, eight maintenance. Tightening it
immediately exposed the opposite bug: `script` did not match "scripts" and
`caption` did not match "captions", so two genuine production requests
("our system still generates very poor scripts") had been missing the brief
all along. A filter is only as good as the corpus you test it against.

**3. Two self-tests existed that nothing ran.** `check_frame_contract` and
`notation` both had working `--selftest` flags that no program called — found
by listing every selftest in the repo and diffing against doctor's calls.
Both now run; `wiring_audit` fails on any future one, so coverage that never
executes cannot look like coverage.

**4. Four skills had no trigger; two needed one.** `reel-analyzer` now cues
off G23 (an unmeasured format is exactly what that skill is for), and
`ffmpeg-ytdlp` cues off a FAILING ffmpeg/yt-dlp command — the failure happens
inside ffmpeg, so no tool of ours could print a cue for it. `content-repurposer`
and `find-skills` are user-initiated and correctly have none.

**5. DOC/CODE DRIFT — docs promised enforcement the code never performed.**
CLAUDE.md: "Gate G23 rejects an unmeasured format outright." RULES.md:
"Unknown format = G23 blocks." G23 is ADVICE and always was; the constitution
only lets the three rules, RENDER and RIGHTS block. **A doc that promises a
block the code does not perform is worse than no doc — it is exactly how a
rule gets trusted instead of checked.** Both corrected, AGENT.md too, and
`wiring_audit` now scans the binding docs for the claim automatically.
STYLE-RULES is deliberately excluded: it is an append-only dated ledger, so
its old entries are records of what was true then.

**State of the material, separate from the system:** 9 of 21 beat sheets are
blocked, 85 of their 94 violations being G45 — captions sitting under
Instagram's account row. Every one was last modified 2026-08-18, before that
overlay was measured. The gates are working; the old sheets are stale. They
are shipped reels, so they were left alone rather than rewritten.

## 2026-08-27 — the humanizer was cued CONDITIONALLY, which is backwards

The user, reading the audit report's trigger table: *"humanizer skill only
triggers if there are em-dashes in the script? actually entire script must be
humanized."* Correct, and the fix is a rule change, not a wording change.

**What was wrong.** `script_doctor` cued `humanizer` only when something
MEASURABLE fired — a house tic, an AI tell, page punctuation. And
`script_approval propose` printed a HUMANIZER reminder with **no backticks**,
so the PostToolUse hook could not fire on it at all: the "last stop before
approval" note was a printed line nobody was required to act on, which is the
exact thing hooks exist to replace.

**Why conditional is the wrong shape.** The humanizer's job is rhythm and
whether a sentence sounds like a person said it. That is, by definition, the
half a checker cannot measure. Firing it only when the checker DOES measure
something means the scripts that most need a human ear — the ones that look
clean — are the ones that never get one. A clean measurement is not the same
as sounding human.

**What it is now.** A third precondition of `propose`, sitting beside
structure.md and research.md, and hash-bound the way approval is:

```bash
python3 tools/script_approval.py humanized <slug>
```

- `propose` refuses without the record: `NOT HUMANIZED`.
- It refuses again if a word changed since: `SCRIPT CHANGED SINCE THE
  HUMANIZER PASS`. The pass no longer covers the words being shown — the same
  guarantee as approve-after-propose, one step earlier.
- **The refusal IS the trigger**: it prints the cue with the skill in
  backticks, so the hook injects it as an instruction at the moment of refusal.
- `script_doctor` now cues it on EVERY run, with different wording when
  nothing measurable fired — *"which is not the same as sounding like a
  person."*

**Two ordering bugs found while wiring it, both worth keeping.** The check
was first placed before the research ledger check, so three ledger cases
started failing with a humanizer message — a refusal naming the wrong cause
is worse than no refusal. And it was briefly inside the prose section's
best-effort `try/except`, where an unrelated ImportError would have silently
skipped it. **A precondition that an exception can skip is not a
precondition.** It now sits last of the three, outside the try.

`test_script_pipeline` is 72 checks (was 66): the refusal, the backticked
cue, the record's hash binding, the staleness refusal, and the compliant
path after an edit (humanize the new words, re-record, propose, approve).

## 2026-08-27 — auditing the two stages the report had skipped

The user, reading the audit report: *"There is nothing written about research
and scouting in the report."* Correct — it covered the trigger machinery and
the suites, and said nothing about two whole pipeline stages. Audited both
properly rather than writing them up from memory.

**RESEARCH — one real gap.** `research_check` has four refusal modes. The
suite tested two of them plus the SPOKEN cross-check; **`NO CLAIMS RECORDED`
and `NO SEARCH LOG` were never tested.** Both work — probed directly, both
refuse — but an untested refusal is one edit away from silently becoming an
acceptance, which is the whole reason this repo tests its refusals rather
than its successes. Both are now cases in `test_script_pipeline` (74 checks,
was 72).

**RESEARCH — a missing trigger at the right moment.** `fact-check-workflow`
was cued only by `script_doctor`, on a claim SPOKEN harder than its evidence.
By then the sentence already exists and the fix is a rewrite. The cheaper
moment is when `propose` reports thin sourcing — one source, or one domain
wearing two names — because the claim is still a claim. Cued there now.

**SCOUTING — nothing wrong, which is worth recording.** All ten
sourcing/scouting gates BLOCK, and every one carries at least one case in
`test_gates`: G29 mobile-first capture (3 cases), G41 desktop needs a
recorded reason (1), G39 every scene carries the line it illustrates (5),
G14 credit (3), G15 numbers carry their source (1), G45 caption safe area
(3), G48 framing (3), G35/G11/G13 render integrity (4 between them).
`capture.mjs` defaults hold at 13 checks, including the two that had silently
broken and shipped a whole scout session. `scout_sheet` self-tests.

Rule 2 and Rule 3 are the two constitution rules these enforce, and both are
enforced in code rather than remembered — which is the answer to "is scouting
covered": yes, and here is the evidence rather than the assurance.

## 2026-08-27 — "at what stage do you do research?" had no answer in the manual

The user asked where research sits, and guessed correctly: right after the
topic, before anything else. Checking rather than confirming from memory
turned up four documentation defects, one of them a stage with no number.

**1. RESEARCH WAS NOT A STEP.** `AGENT.md` runs STEP 0 -> 1a -> 1b -> 1c ...
and research appeared exactly three times in the whole file: twice as a field
reference inside STEP 1a (ASSET SCOUT), once as a general principle. The
ledger it produces is a BLOCKING precondition of `propose`. **A stage that
gates the pipeline and is named nowhere in the order of operations is the
definition of a step that gets skipped.** Now `STEP 0.5 — RESEARCH`, placed
before the scout, because you cannot capture a source until you know which
claim it proves.

**2. The skill carried two orderings that never met.** `news-reel` says
"Research first, and it leaves a LEDGER" in its writing order, and "1 — Scout
BEFORE scripting" in its order of operations, with nothing reconciling them.
Both are correct; the full sequence is research -> scout -> script, and it is
now stated.

**3. The skill's propose preconditions were a step behind.** It named only
`structure.md`. There are three: structure, research, and the recorded
humanizer pass.

**4. The humanizer section said the pass runs "not on the whole script".**
Read fairly, that licenses running it over flagged lines only — the exact
thing the user objected to. The section's REASONING is right and measured
(three of humanizer's patterns would strip the hedging G14/G15 and framework
S20 require), but it conflated two different scopes. Split explicitly now:

> **INPUT is wholesale** — the entire script, every time, measured or not.
> **OUTPUT is selective** — reject the three named patterns on sight.

**The pattern across all four:** every one is a doc that was true when
written and drifted as the code moved, and none would have been found by
running anything. `wiring_audit` catches a doc claiming a gate blocks when it
does not; it cannot catch a stage nobody wrote down. That class still needs a
person to ask "where does X happen?" — which is what the user did.

**And a note on the answer itself:** references the user supplies are INPUTS,
not sourcing. The dated `## SEARCHED` log is mandatory precisely so a reel
cannot be assembled out of whatever arrived in the prompt, and a topic given
with no references changes nothing about what the ledger must contain.
## 2026-08-27 — apple-surprise-and-shine: whisper writes spoken "AM"/"PM" as an orphan ".m." token, and it is not a TTS defect

RAW NOTE: gate G34 blocked the render on `'.m. Pacific, Steve' carries an
orphan single-letter token '.m.'`. The script says "10 AM Pacific" — whisper
tokenized it as `"a"` then `".m."`, and the two landed in DIFFERENT caption
chunks ("now. 10 a" / ".m. Pacific, Steve"), so no chunk-level phrase
correction could ever bridge them.

ROOT CAUSE, and the thing worth writing down: my first instinct was to treat
this like the "Pegatron T" case (2026-08-13) — a stray TTS sound, fix by
cutting the master and re-whispering. It was NOT. Isolated whisper on the
2.3s slice, run at BOTH `base`/`small` AND `medium`, transcribed the SAME
audio as `"9 to 5 Mac"` / `"10 a.m. Pacific"` cleanly every time. The
smaller-model mis-hearing I chased first (`"925 Mac"`) across THREE HeyGen
probe regenerations was itself a false positive of exactly the kind this
skill already warns about ("a misspelling from whisper base is NOT proof of
a mispronunciation") — I just hadn't yet hit the case where the SAME
false-positive shape (an isolated short clip transcribing worse than the
full-context original) also produces a gate-blocking artifact, which made it
look load-bearing enough to chase. Two lessons compound into one: (1) always
re-verify an isolated-slice transcription against the ORIGINAL full-context
audio before spending credits on a fix, and (2) a confirmed orphan-token
GATE is not by itself proof the audio is wrong — verify with the same
isolated-medium-model check before concluding "cut it from the master."

DISTILLED RULE: `scripts/compile_shot_plan.py` now merges a lone `"a"`/`"p"`
token followed by a `".m."`-shaped token into one `"AM"`/`"PM"` caption word,
the same class of fix as the existing hyphen-prefix and leading-punct+digit
merges — general, not a per-reel patch, with a self-test in
`tools/test_script_pipeline.py` (3 cases: AM merges, PM merges, an ordinary
`"a"` with nothing after it is left alone). Any future reel that states a
time this way inherits the fix for free.

TREATMENT HISTORY (apple-surprise-and-shine, so the next Apple-event reel
does not repeat it): hook = pure facecam, no card (2 sentences, ~8s — no
split/BrandHook this time). `receipt` (not `floatcard`) used TWICE on real
stills with no highlights, for a gentle ken-burns push-in on a photo —
`floatcard` cannot play a still at all (G35: it renders via
`<OffthreadVideo>`). `specsheet` used three times for confirmed-facts /
expected-products / historical-comparison tables, no `statcard` and no
`comparesplit`. One `wordcascade` stinger, two plain black `typecard`s
(over G12's max-1 advice — the mid-reel one and the closing date card serve
different jobs, judged worth it). Deliberately did NOT reuse
`september-preview`'s `floatcard` treatment on the same Cook/Ternus official
photo, or its `receipt`+`annotatezoom`-on-deviceframe treatment for the
foldable-rumor beat.


## 2026-08-27 — HeyGen exposes ElevenLabs V3 and we were never asking for it

The user sent two HeyGen UI screenshots showing a **Voice Engine** dropdown set
to **ElevenLabs V3**, a Stability slider, and audio tags (`[curious]`,
`[excited]`, `[pause]`) sitting inside one of our own scripts.

**Checked what our pipeline actually sends: `voiceId` and `speed: 1.12`.
Nothing else.** No engine, no model, no stability, no style. HeyGen therefore
picks the default model for that voice, and there is no reason to think that
default is v3.

The API has supported this the whole time:

```
voiceSettings.engine_settings = {
  engine_type: "elevenlabs",
  model: "eleven_v3" | "eleven_multilingual_v2" | "eleven_turbo_v2_5"
       | "eleven_flash_v2_5",
  stability, style, similarity_boost, use_speaker_boost
}
```

with one constraint that decodes the whole UI: **"When using eleven_v3,
stability must be 0, 0.5, or 1"** — exactly the Creative / Natural / Robust
presets in ElevenLabs' own docs.

**This casts doubt on a conclusion recorded earlier today.** We measured the
clone at 1.86 semitones, concluded the CLONE was flat and that HeyGen had
topped out, and recorded a decision to keep HeyGen while treating Soniqo as a
future re-clone rig. But the user's own v3 generations of a different script
measured 3.22 and 3.41 — nearly double — on ElevenLabs. If the flatness was
the MODEL rather than the voice, that conclusion was wrong about its cause.
Probe running: identical words, same voice, control vs eleven_v3 @ 0.5 vs
eleven_v3 @ 0 with tags, all measured by `vo_qc`.

**Design constraint decided before any config change: TAGS DO NOT GO IN
`script.md`.** G27 hashes the approved narration and G21 verifies captions
against it, so markup in the script would mean the user approves `[curious]`
as if it were words, and the caption check would compare against words nobody
speaks. Tags are DELIVERY, like voiceSpeed — they belong in the beat sheet and
are injected into the HeyGen payload at generation. `tools/vo_direct.py`
already holds per-beat registers and is the right home.

**HeyGen's "Enhance voice" toggle stays OFF.** It inserts tags automatically:
the delivery stops being reproducible, and a tool starts editing text the user
approved.

### The probe result — the hypothesis was WRONG (2026-08-27)

Three avatar generations, identical words, same voice
(`bb79e839`), same avatar, same speed 1.12, measured by `vo_qc`:

| | condition | pitch sd | range | median | secs |
|---|---|---|---|---|---|
| A | control — what we send today | **2.14** | 6.7 | 168 | 10.2 |
| B | + `eleven_v3` @ stability 0.5 | **2.15** | 7.1 | 168 | 9.4 |
| C | + `eleven_v3` @ stability 0 + audio tags | **2.15** | 5.8 | 167 | 10.8 |

**No difference. +0.01 semitones.** Sending `engine_settings` with
`model: eleven_v3` through the API changes nothing measurable, and the audio
tags were **stripped, not spoken** — whisper transcribes all three
identically, with no `[curious]` audible. So the tags reached HeyGen and were
discarded before the TTS ever saw them.

**The request was NOT rejected**, even though the schema says "the request is
rejected if the voice_id is not compatible with the selected engine". So
either the validation does not fire, or the voice is eligible and the setting
is silently dropped on this path. Either way the API accepted a parameter and
did nothing with it, which is the worst of the three possibilities: it looks
like it worked.

**What this does and does not settle.** It settles that the API route does not
deliver the UI's behaviour. It does NOT settle that v3 cannot help — the
user's own ElevenLabs generations of a different script measured 3.22 and 3.41,
and their HeyGen UI has V3 selected with a stability slider. The gap is now
API-vs-UI, not v3-vs-not-v3.

**A confound worth checking first: the account holds THREE private voices all
named "iGeeks Blog"** — `9c7efdaf`, `bb79e839` (ours, listed gender *female*),
and `faaffee3`. Our config points at one of them and the UI may be tuning
another. A same-named voice is exactly the kind of thing that gets picked in a
dropdown and never reconciled with a config file.

**Earlier conclusion stands for now, with a footnote.** Today's record said the
CLONE is flat and HeyGen has topped out. This probe supports that rather than
overturning it: 2.14 through the API with every expressiveness lever we can
reach. The open question is whether the UI path reaches a lever the API does
not.

**Next step is one click for the user, not more credits from us:** generate
this exact sentence in the HeyGen UI with ElevenLabs V3 selected, download it,
and measure. If it lands near 3.4 the fix is the path, not the voice.

### The lever was the VOICE, not the model — and today's earlier conclusion was wrong (2026-08-27)

Five generations, identical words, same avatar, same speed, one variable each:

| | condition | pitch sd | range | median | w/s |
|---|---|---|---|---|---|
| A | `bb79e839` iGeeks Blog — **what we ship** | **2.14** | 6.7 | 168 | 2.65 |
| B | same voice + `eleven_v3` @ stability 0.5 | 2.15 | 7.1 | 168 | 2.87 |
| C | same voice + `eleven_v3` @ 0 + audio tags | 2.15 | 5.8 | 167 | 2.51 |
| D | `9ce667b7` "Dhvanesh -- 59" | 3.21 | 10.0 | 136 | 4.07 |
| **E** | **`fae1de1f` "Dhvanesh"** | **3.51** | 10.3 | 150 | 3.29 |

**E clears the 3.5 floor.** +64% over the voice we ship, from changing one
field. Every engine-level lever moved the number by 0.01; the voice moved it
by 1.37.

**CORRECTION — this repo recorded the wrong conclusion earlier today.** The
record said the CLONE is flat, that settings/engines/references/per-beat
direction all top out around 3.0 against a 3.5 floor, and that the answer was
to keep HeyGen and hold Soniqo as a future re-clone rig. That was measured on
**one voice** and generalised to the provider. The correct statement is
narrower and much more useful: **the particular voice we selected is flat, and
another voice already sitting in the same account clears the floor on the same
provider, same avatar, same API path.**

The failure was not the measurement. It was the SCOPE of the conclusion — one
sample, generalised to "HeyGen has topped out". The account held six private
voices; five were never measured until asked to check which of three
same-named voices the UI used.

**Also settled by the same run:** the account has THREE voices named "iGeeks
Blog" (2.06 / 3.00 / 1.79 on previews) and we were on the best of those three,
so the duplicate-name theory was dead — but the two `Dhvanesh`-named voices
were never in that comparison at all.

**Previews overstate. Do not tune off them.** `bb79e839` previews at 3.00 and
generates at 2.14. Predictions from preview minus that 0.86 gap put D at ~2.42
and E at ~2.51; both actually came in ~0.8-1.0 HIGHER. The gap is not a
constant, so a preview ranks candidates and nothing more.

**NOT CHANGED IN CONFIG, DELIBERATELY.** E is acoustically distinguishable
from the shipping voice — 0.945 against probe A, where two independent
different-speaker controls sit at 0.959 and 0.964, and median pitch is 150 Hz
vs 168 Hz. That may mean "a different voice", or it may mean "the user's ACTUAL
voice, versus a brand clone that was never him" — note `bb79e839` is named
"iGeeks Blog" and the API lists it as gender *female*, while `fae1de1f` is
named "Dhvanesh". **A number cannot settle whose voice this is. The user
listens and decides**, and the config changes only after that.

Pace is not an objection: E runs 3.29 w/s at speed 1.12, and our band is
2.35-2.75. That is the `speed` parameter, roughly 0.85 instead of 1.12.

### DECISION: the voice stays `bb79e839`. The user chose it by ear. (2026-08-27)

Having measured five generations and found `fae1de1f` "Dhvanesh" clearing the
3.5 floor at 3.51 against our shipping voice's 2.14, the user listened to all
three and **chose the voice we already ship**.

**That decision stands and is not to be relitigated by measurement.** Whose
voice this channel has is an identity question, and a pitch statistic has no
standing to answer it. A future session reading the probe table above will see
that E is +64% more expressive and be tempted to "fix" the config. Do not.
It was offered, listened to, and declined.

**What the probe was still worth:** it killed three wrong theories — that the
model was the lever (eleven_v3 moved it 0.01), that audio tags were the lever
(stripped, not spoken), and that we were pointed at the wrong one of three
same-named voices (we were on the best of them). And it corrected a
provider-level conclusion that had been generalised from a single sample.

**Speed: NOT changed, because nothing measurable is wrong.** The user asked to
"fix the speed", but that instruction was premised on switching to the
Dhvanesh voice, which runs 3.29 w/s. On the chosen voice at the locked speed
of 1.12, probe A measures **2.65 w/s** — inside our measured band of
2.35-2.75. Changing a setting that is in band would be motion, not work. Said
so and left it.

**CONSEQUENCE TO WATCH — `vo_qc` will now flag every reel FLAT, forever.** Its
floor is 3.5 and the chosen voice generates 2.14. A check that fires on every
single run and is correctly ignored every single time is worse than no check:
it trains the reader to skim past the one time it means something. This needs
resolving — either the floor is wrong for a deliberately-chosen voice, or the
advisory needs to carry the decision. Not fixed unilaterally, because
weakening a check to make a warning go away is exactly the move this repo
exists to prevent.

### The VO alarm is now calibrated to OUR corpus, not the creator band (2026-08-27)

Chosen by the user over retiring the check. The problem: with the voice
deliberately kept at ~2.4 semitones and the floor at 3.5, `vo_qc` would have
flagged FLAT on every reel forever. **A check that fires every run and is
correctly ignored every run is worse than no check — it teaches the reader to
skim past the one time it means something.**

**What changed:** the ALARM is derived from our own shipped reads
(`voice_calibration.json`, written by `vo_qc.py --recalibrate`, n=3, alarm
2.02 pitch / 5.6 range). **What did NOT change:** the creator band is still
printed on every single run, along with the gap to it. We do not get to stop
knowing we sit below real creators; we stop treating a settled choice as a
fresh defect.

**Both measures had to move.** Calibrating pitch alone would have left NARROW
RANGE firing on everything instead (our reads run 6.7-9.8 against a 10.0
floor) — fixing one permanent alarm and leaving the other is not a fix, it
just changes which line gets ignored.

**THIS CHANGE IS SHAPED EXACTLY LIKE A DISHONEST ONE.** Lowering a threshold
until the red light turns green is the move this repo exists to prevent. The
only thing separating the two is whether the check can still fail, so
`tools/test_vo_qc.py` (15 checks, run by doctor) asserts BOTH halves:

- a read at our own mean stays quiet, and
- **a genuinely flat read STILL alarms** — synthesised at 0.8 semitones below
  the floor, and the alarm must fire.
- the floor sits below every shipped read (or it fires forever) and above 0.5
  (or it can never fire), and is not silently back at 3.5.
- the creator band and the gap are still in the output.

A calibration that cannot fail is not a calibration, it is a deletion.

**Doctor warns while n < 5** — the threshold is PROVISIONAL on three reads and
should be re-derived as reels ship. It also warns when the corpus moves,
mirroring the script calibration.

**One display bug found and fixed on the way:** the recalibration listing
printed only `<parent>/<name>`, so `public/assets/x/vo.wav` and
`_sources/x/vo.wav` rendered identically — which sent this session's own
verification to a path that did not exist. Repo-relative paths now.

## 2026-08-27 — the voice was never flat. HEYGEN'S TTS WAS.

The user generated a read in ElevenLabs v3 with audio tags and asked for a
system that produces our own voiceover and lip-syncs it with HeyGen. Measuring
their file settles the entire day's investigation:

| | pitch sd | range | median | identity vs shipped |
|---|---|---|---|---|
| HeyGen TTS, our voice (probe A) | 2.14 | 6.7 | 168 | — (this IS it) |
| HeyGen + eleven_v3 + tags (probe C) | 2.15 | 5.8 | 167 | — |
| user's ElevenLabs_v3.mp3 | **3.60** | **12.3** | 170 | **0.998** |
| creator floor | 3.50 | 11.6 | | different speakers: 0.959, 0.964 |

**Same voice — 0.998 similarity, the highest measured all day, against two
independent different-speaker controls at 0.959 and 0.964. And it clears the
3.5 floor**, the first thing this session that has, with range inside the
reference band.

**So the conclusion recorded twice today was wrong both times.** First it said
the CLONE is flat and HeyGen had topped out (one voice, generalised to a
provider). Then the probe corrected it to "the voice we picked is flat, a
different voice clears the floor" — also wrong, because it kept assuming the
voice determines the read. It does not. **The same voice reads at 2.14 through
HeyGen's TTS and 3.60 through ElevenLabs v3.** The variable was never the
voice; it was who renders it.

Worth naming the pattern: three conclusions, each corrected by widening what
was measured. The measurements were right every time. The inference from them
kept outrunning the evidence.

### The audio-driven path WORKS — verified end to end

`references/heygen.md` documented this flow for months in prose and nothing
ever ran it. Ran it:

- **Upload refuses the ElevenLabs MP3 as downloaded** — "Stored file type not
  supported: application/octet-stream", twice, with two upload methods, on a
  file `file(1)` calls audio/mpeg and ffprobe decodes fine. An ffmpeg
  re-encode with `-map_metadata -1` uploads and completes first try. Now in
  `tools/vo_external.py` so it is never rediscovered.
- **Expressiveness survives the render**: 3.40 in -> 3.31 out (-2.6%).
- **Duration is preserved to 16ms** (58.514 -> 58.498), so HeyGen is not
  time-stretching the audio.
- **The avatar animates and gestures normally** on the frames sampled.

With uploaded audio HeyGen does lip-sync ONLY. `voiceId`, `voiceSpeed`,
`engine_settings` and Enhance voice all stop applying — which is why none of
the engine experiments mattered and why this one does.

### No ElevenLabs MCP is connected to this session

The user linked ElevenLabs' MCP announcement. It is not connected here. What
IS available is a third-party proxy (Higgsfield `generate_audio` with
`variant: elevenlabs`) that draws on ITS voice library, not the user's
ElevenLabs account — so it cannot reach the voice they built. Direct
generation needs the ElevenLabs connector added in the Claude client.

Until then the division is: **the user generates the read, the agent does
everything else.** That is one manual step in exchange for the only voice
we have measured above the floor.

## 2026-08-27 — the pipeline now generates its own voice; HeyGen only lip-syncs

Made the external-VO flow the default, on the measurement that the SAME voice
reads at 2.14 semitones through HeyGen's TTS and 3.60 through ElevenLabs v3
with tags (0.998 speaker similarity; different-speaker controls 0.959/0.964).
3.60 is the only read this repo has measured above the 3.5 creator floor.

**The new STEP 2:**

1. `vo_tagged.py <slug>` — emits `script-tagged.txt` from the APPROVED script.
   Same words, positional tags from `vo_direct`'s existing registers, only
   documented ElevenLabs tags. Tags never enter `script.md`: G27 hashes that
   as the approved narration and G21 checks captions against it.
2. The user generates it in ElevenLabs (Natural stability first; **Robust
   ignores tags by design**).
3. `vo_external.py <slug> <file.mp3>` — re-encodes with metadata stripped and
   checks pace. **Not optional**: the download as-is is refused by the upload.
4. Upload → `create_video_from_avatar` with `audioAssetId`, never
   `script`/`voiceId`.

**WHAT THIS COSTS, AND THE GATE THAT PAYS FOR IT.** With HeyGen TTS the audio
was synthesised FROM the sheet's script, so "what he says" and "what was
approved" matched *by construction* and no gate was needed. An uploaded file
has no such guarantee: the wrong take, an older draft, or another reel's
audio can reach the render with a perfectly valid G27 hash on the sheet.
**G27 proves the TEXT was approved; G53 now proves the AUDIO says it.**

**G53's floor is derived, not chosen.** Every reel on disk, script vs its OWN
audio: 1.000 / 0.962 / 0.948 / 0.885. The 0.885 is entirely whisper artefacts
("bill"/"bell", "100 000" for "a hundred thousand"), not drift. The same
scripts against a DIFFERENT reel's audio: 0.013-0.110. Floor set at 0.70, in
the empty middle, with margin on both sides.

**Adding G53 immediately failed the clean baseline fixture**, because
`VO_WORDS` in test_gates was a three-word stub against an eight-word script —
fine for years while nothing compared the two. **A stub fixture is not a
smaller version of reality; it is a different thing that happens to pass.**
The fixture now carries the whole script, and the failing case is an approved
script whose audio says something else, with the approval hash updated so G27
stays satisfied and G53 is the only thing standing in the way.

**Verified end to end before any of this was written:** upload → lip-sync
render, expressiveness 3.40 → 3.31, duration preserved to 16ms, avatar
gesturing normally.

**Reversible on purpose.** `voice.mode: "heygen-tts"` in config.json goes back,
and `avatar.voiceId` / `voiceSpeed` are left in place and correct for it.

**wiring_audit caught two omissions in the same hour it took to build this** —
`vo_external` and then `vo_tagged` both landed with self-tests doctor did not
run, and `vo_tagged` sat as an ORPHAN until AGENT.md named it. The rule I
added this morning has now caught its own author three times.

### ElevenLabs MCP connected — the manual step is gone (2026-08-27)

The user connected the hosted ElevenLabs MCP (`https://api.elevenlabs.io/v1/mcp`,
OAuth). It is not limited to agent management as its docs implied:
`creative_generate_speech` takes `model_id: eleven_v3` and a workspace voice
id, so the agent can now generate the read itself.

Verified on the same sentence as the six HeyGen probes, voice
`5dh6l1ILwXHgGBApxztn`:

| | pitch | range | median | length |
|---|---|---|---|---|
| HeyGen TTS (what we shipped) | 2.14 | 6.7 | 168 | 10.2s |
| HeyGen + eleven_v3 + tags | 2.15 | 5.8 | 167 | 10.8s |
| **ElevenLabs MCP, v3 + tags** | **3.17** | 10.8 | 163 | 9.6s |
| user's hand-made take | 3.60 | 12.3 | 170 | 175s |

**+48% over HeyGen on identical words, and the TAGS ARE ACTED, NOT SPOKEN** —
the transcript comes back clean with no `[curious]` audible, which is exactly
what failed when the same tags were sent through HeyGen's `script` field.
Speaker similarity 0.991 against different-speaker controls at 0.959/0.964.

**Do NOT read 3.17 vs 3.60 as "the API is worse."** Three things differ at
once: length (9.6s vs 175s — a short clip has less room to move), emotional
range (three news sentences vs a demo script that swings through a hundred
states), and stability (**the MCP exposes no stability parameter; the web UI
does**). Untangle those before concluding anything. The web UI remains
available and `vo_external.py` accepts its file identically.

**Cost, so it is not a surprise:** ~190 credits for 9.6s, so a 70s reel runs
roughly 1,400 credits.

**A duplicate voice named "Dhvanesh" exists** (`kjnHU2BEEUxL4teU1fAg`). The id
in config is the one the user named. Same trap as the three "iGeeks Blog"
voices on the HeyGen side — a name is not an identifier.

## 2026-08-27 — apple-surprise-and-shine: first reel through the external-voice flow

End to end on the new pipeline. It worked, and it found four things.

**The flow, as run:** `vo_tagged` -> `creative_generate_speech` (eleven_v3,
voice `5dh6l1ILwXHgGBApxztn`) -> `vo_external` -> HeyGen asset upload ->
`create_video_from_avatar` with `audioAssetId` -> `ingest_avatar` ->
`compile_shot_plan` -> gates -> render. **HeyGen never spoke a word.**

70.4s VO, 3.25 semitones (vs 2.14 from HeyGen's TTS on this voice), master
70.5s at -14.53 LUFS, gates passed, frame-lint clean.

**G53 earned its place on its first real run.** Pre-checked the VO against the
approved script before spending the avatar render: **0.955**, every difference
a whisper artefact ("fifteen"/"15", "onstage"/"on stage", "10 am"/"10am"), no
drift. The gate that replaced the by-construction guarantee did its job.

### Four faults found, all in the INHERITED sheet or my own edits

**1. A credit named the wrong source.** Scene 01 credited "Apple" for a
MacRumors page. That is a RIGHTS error, not a typo — we credit the source we
actually used.

**2. Geometry written against a different capture.** The shot plan carried
`srcHeight` 533 / 695 / 475 for images that are 920 / 1940 / 1440, and an
`annotatezoom` focus rect pointing at y=480 — which on the real capture is the
Newsroom nav bar, not the headline. **A rect is meaningless without the file
it was measured on.** Re-measured all three.

**3. MY OWN G18 FIX INTRODUCED A LIP-SYNC DRIFT, AND NO GATE CAUGHT IT.**
Fixing "the card vanishes before the sentence ends" by shortening the NEXT
scene left a footage scene starting at 56.43s while still seeking `from`
56.08s — 0.35s of drift for the rest of the reel. Gates passed. G01 passed.
It surfaced only because the `[DUPLICATE]` flag made me look at those scenes
at all. **A fix that moves a boundary must move `from` with it**, and there is
currently no check that a footage scene's `from` matches its timeline start.
That check is worth adding.

**4. The hook was 7.1s of talking head** — and the two rules that guard it
disagree in a productive way. `lint_frames` blocks a hook layout over 2.0s;
`validate_job` requires the presenter visible in the opening scene. A receipt
opener satisfied one and failed the other. The answer was already written in
RULES.md — *"Face on screen by second 2 — usually a split hook"* — and the
split (invite receipt above, presenter below, "APPLE CONFIRMS / SEPTEMBER 9")
satisfies both plus the sound-off test that 7 seconds of a man talking fails
outright.

### Treatment history (do not repeat next reel)

split hook (receipt over presenter) · annotatezoom on a press release
headline · CONFIRMED specsheet vs EXPECTED-NOT-CONFIRMED specsheet as an
honesty pair · wordcascade "NOT ONE PRODUCT NAMED" · comparison table
"WHO'S SHIPPED A FOLD" · kinetic serif date card outro.

### Left honestly unfixed

- **Pace 2.90 w/s against a 2.35-2.75 band.** `creative_generate_speech`
  exposes no speed parameter; the web UI does. Runtime still lands at 70.5s,
  inside the 60-80s band.
- **Outro typecard is 76% dead space** (limit 70%) — advisory.
- **The hook headline overlaps the receipt's own text.** Readable, not clean.
- **No packaging yet** — caption, hashtags, first comment, alt text.

## 2026-08-31 — apple-pencil-iphone-ultra: fast VO, and a lint bug worth naming

Single-source Gurman scoop (Apple tested and shelved a foldable-iPhone
stylus). Built end to end on the external-voice flow; three issues, all
worth recording.

**1. ElevenLabs v3 read this script at 3.45 w/s, not the 2.35-2.75 band —
and `[pause]` tags plus one-sentence-per-paragraph moved it to only 3.38.**
Two full-price regenerations (~2,580 credits, ~$45) for a ~0.07 w/s
improvement. **The lever this pipeline documents for pacing doesn't reliably
work on this voice/script combination** — logged so the next reel doesn't
re-spend credits re-discovering it. User chose to accept the fast take
(advisory-only, G02 runtime band still cleared at 61s) rather than fall back
to HeyGen's flatter TTS or risk an untested atempo time-stretch.

**2. `plan_shots.py`'s clause-level auto-split plus per-clause identical
scenes is a DUPLICATE-flag factory.** Binding two or three adjacent clauses
to the SAME still image (because they're one sentence, one visual) produces
back-to-back scenes whose mid-frames hash near-identical — `[DUPLICATE]` is
HARD_ALWAYS in `lint_frames.py` regardless of BLOCKING_RULES. **The fix is
structural, not cosmetic: merge same-visual adjacent shots into ONE shot
before compiling**, every time a sentence spans multiple clauses bound to one
asset. Seven merges did it here (20 shots -> 12). Worth teaching
`plan_shots.py` to warn about this at write-time rather than finding out
after a full render.

**3. `annotatezoom` on a short, wide screenshot (not a big source image)
makes dead space WORSE, not better.** Splitting a 1080x620 receipt into two
310px-tall focus rects to show "scroll from paragraph 1 to paragraph 2"
produced 37-43% dead space (limit 30%) — the wide-aspect focus rect, scaled
to fill canvas WIDTH, left more vertical letterbox than the full image would
have. **`receipt` (full image, no focus rect) is the right type for a short
screenshot; `annotatezoom` is for zooming into a region of a LARGE source.**
Switched back to `receipt` with both paragraphs in one merged shot — fixed
the dead space AND the duplicate-scene problem in the same edit.

**4. `[EDGE TEXT]` false-fired on a receipt with a blurred ambient
backdrop.** The heuristic measures pixel variance in an 8px strip at the
frame's L/R edges — it can't tell "cropped word" from "the app's own blurred
backdrop-fill texture is naturally noisy at the edges." Verified by hand:
ran the exact regex/variance check against the actual frame, and by eye
against the rendered still — no cropped text, just backdrop noise crossing
the score-34 threshold. Overridden with `--soft`, disclosed here and to the
user. Not something a per-reel fix should chase; the false-positive risk is
systemic to any receipt scene sitting on the app's blurred background, not
specific to this asset.

**5. Split hook, again — same fix as apple-surprise-and-shine, independently
re-derived before reading that entry.** A receipt-only hook (headline image,
no presenter) fails `validate_job.py`'s "opening scene must visibly include
the presenter" the moment the reel HAS a presenter elsewhere. `split` (image
top / avatar bottom) satisfies that, the sound-off test, AND reads better on
frame 0 per G43. **This is now confirmed twice: image-led hook material on
this pipeline should default to `split`, not a bare `receipt`, whenever a
presenter exists.**

### Treatment history (do not repeat next reel)

split hook (real product-render screenshot over presenter, not an official
invite) · receipt (not annotatezoom) on a short two-paragraph screenshot,
BOTH paragraphs in one shot · annotatezoom used only on a real product photo
(Apple Pencil Pro) with an on-screen "shown for scale, not the prototype"
disclaimer · reused an official asset (Sept 9 invite art) VERBATIM from a
prior job's `public/assets/` instead of re-capturing — new for this
pipeline, since every prior reel re-scouted per slug even for the same
event.

### Left honestly unfixed

- **Facecam 34% of runtime** (band 10-20% for `news`) — a side effect of
  merging clause-pairs into single facecam shots; each merged shot now spans
  more spoken time. Advisory only (G06 not in BLOCKING_RULES).
- **Every held-layout PACING flag** (scene 0 hook 7.2s down to a scene at
  9.9s) — all trace to the same fast VO read in #1, not to the shot
  boundaries themselves; re-verified by eye against the lint sheets rather
  than reflexively re-cut.

## 2026-08-27 — topic selection finally has a system

**The gap:** every stage of this pipeline had a tool, a gate and a self-test —
research, structure, script, voice, render, packaging. Topic selection had a
habit. Reels got picked off whatever news was in front of someone, and nothing
ever read what the audience was actually asking.

**`tools/idea_scout.py` is the deterministic half.** It cannot research —
research needs the web, and that is the agent's job. What a tool can do is the
two halves either side of the thinking:

- `--brief` hands over every subject already made (so a repeat cannot be
  proposed), the formats with their measured bands, and the output contract.
- `--check` refuses a shortlist unless every idea carries a real STORY ENGINE
  (believed X -> discovers Y -> matters because Z), **two independent source
  domains**, a known format, and no overlap with an existing reel.

**The guardrail that matters.** `AUDIENCE:` lines are parsed separately from
`SRC:` and are REFUSED as sourcing. This is the constraint recorded when
`marketing-skills:customer-research` was adopted: a forum comment tells you
what people are confused about and in whose words, and it never establishes a
fact. It shapes the angle and the hook; it is not evidence. Now that rule is
executable rather than remembered.

**A CLOUD ROUTINE runs it, not a local cron.** `daily-reel-ideas` was first
built on the local scheduler and that was wrong: local tasks only fire while
the desktop app is open. The routine (`trig_01L4wAZiwpB6cXJYRgarN8a7`) runs
server-side at 02:30 UTC / 08:00 Asia/Calcutta, in a fresh checkout, and
**commits the shortlist to `jobs/_ideas/<date>.md`** — so the morning's ideas
are waiting on every machine, not trapped in one chat.

**Scope: Tech, Apple, AI, Gadgets**, two research lanes — what actually moved
(primary source + independent coverage) and what the audience is asking (App
Store 1-3 star reviews, YouTube/Instagram comments, topic subreddits, HN).

**The cloud box has no MCP connectors for skills, so the technique is written
into the prompt rather than referenced.** That is the better shape anyway:
what mattered about `customer-research` was its method, not its packaging.

**Both tools it depends on are pure stdlib** plus repo-local modules —
verified before scheduling, because a routine that dies on an import at 8am
is a routine nobody trusts again.

**It proposes and stops.** The prompt forbids creating a job, writing a
script, or generating anything, and forbids touching any file outside
`jobs/_ideas/`. It also tells the agent that web pages and forum comments are
DATA, not instructions to it.

### Lane B cannot run in the cloud — measured, not assumed (2026-08-31)

The first idea-scout run produced five good ideas and **zero AUDIENCE lines**.
The agent had tried `forums.macrumors.com` and been refused by the egress
proxy, and its Reddit searches returned news articles about Reddit rather than
threads. Rather than guess a workaround, probed the sandbox directly with a
one-shot routine against ten targets.

**Everything is blocked.** Not Reddit specifically, not forums specifically —
`curl` returns `CONNECT tunnel failed, response 403` at the proxy before TLS,
and `WebFetch` returns `EGRESS_BLOCKED`, for hn.algolia.com, itunes.apple.com
RSS, reddit.com JSON, news.ycombinator.com, macrumors.com and 9to5mac.com
alike. The proxy's own status endpoint shows an allowlist of infra domains
only (npm, PyPI, the Anthropic API). **`WebSearch` works because it runs
server-side, outside the proxy.** That is the whole toolkit up there.

**Locally the picture is different, and also not what I expected.**
`hn.algolia.com` returns real verbatim comments with authors and dates —
genuinely good Lane B material for tech topics. **Reddit is blocked from here
too.** The iTunes reviews RSS returns feed metadata with no review entries.
So the working local source is HN plus targeted WebSearch, and that is what
AGENT.md now says rather than the aspirational list.

**The fix is a SPLIT, and it is better than the original design.** The cloud
routine does Lane A daily. The audience pass happens on the user's machine,
on the ONE topic they picked — deep on one subject beats shallow across five.

**The routine prompt now states the network reality up front**, because the
first run burned several turns discovering it. It also carries an explicit
NEVER FABRICATE A QUOTE rule: an invented AUDIENCE line would enter the
pipeline looking sourced, which is worse than an empty field.

## 2026-09-01 — ios-27-beta-8: no source screenshot of the feature, so say so with a card

Beta-8-as-checkpoint roundup ("what's actually new in iOS 27, now that it's
basically done"), not a beta-8-specific changelog — corroborated across
macrumors/9to5mac/osxdaily/appleinsider/ioshacker that the visible features
(Siri AI, Liquid Glass slider, Visual Intelligence in Camera) shipped across
the WHOLE cycle and beta 8 itself added nothing new; the script says that
honestly ("Beta eight itself is reportedly quiet, though") instead of
implying beta 8 introduced them.

**No screenshot of the actual new Siri UI, the transparency slider, or
Visual Intelligence-in-Camera exists anywhere (beta not installed on a
capture device).** Rather than reuse an unrelated Apple hero image and
imply it shows the feature, those three beats used a plain `specsheet`
motion-graphic card (title + kicker + rows + footnote naming the sources) —
honest about what it is (an explainer card, not a screenshot) and G15-
compliant (every specsheet needs a `source`/`footnote`, found the hard way
when the first pass shipped without one). Worth being a named pattern: when
the visual doesn't exist, build the honest card instead of stretching an
unrelated real image to stand in for it.

**A receipt crop with NO margin below its last line of text clips that
line when the scene zooms — even before the highlight animation starts.**
Two receipts (Apple dev-notes at 1080x700, OSXDaily at 1080x1250) both hard-
failed `[EDGE TEXT]` in `lint_frames.py`, and inspecting the actual frames
(not just trusting the flag) showed two DIFFERENT failure shapes: the short
700px crop clipped the LAST paragraph line at the bottom because there was
no whitespace margin past it; the tall 1250px crop clipped the HEADLINE at
the TOP because it started flush at the headline with zero margin above.
The one receipt that rendered perfectly (MacRumors, 1080x930) had generous
whitespace on both ends — a colored banner above, blank margin below the
last line before the credit tag. Fix: **re-crop every receipt to ~930px
tall with real margin on both ends, matching the size of the one that
already works**, not by guessing new highlight-box coordinates against a
tight source image. Confirmed by re-cropping both from fresh captures and
re-rendering: both flags cleared with no highlight-box changes needed
beyond adjusting for the new coordinates.

**`[EDGE TEXT]` false-fired a second time, independently, on a receipt with
a blurred colored backdrop** — same root cause as apple-pencil-iphone-
ultra's #4 (the edge-pixel-variance heuristic can't tell a cropped word from
the app's own blurred-gradient backdrop texture). Verified by eye against
the actual frame (fully intact card, nothing cropped) before overriding with
`--soft`, disclosed here. Two independent hits on the same false-positive
class in two different reels is worth the heuristic maintainer knowing, not
just re-verifying and moving on each time.

**Tiering: "3 outlets" is not automatically `multi`.** `research_check.py`
correctly downgraded 6 of this reel's claims from `multi` (3 domains) to
`official`, because the reel's own VIA field said the same thing for all
three: "Apple's own feature, relayed by the outlet" — a fact about Apple's
own shipped product, independently observed in a beta anyone can install,
is `official`, not `multi` dressed in three mastheads. `multi` should mean
independent ORIGINS, not independent repeaters of one origin — matches the
Weibo-leaker VIA discipline already in RULES.md, just not applied to a
first-party feature claim before.

**ElevenLabs v3 read this script at 3.31 w/s again** (206 words / 62.3s,
outside the 2.35-2.75 w/s band, same as apple-pencil-iphone-ultra) — third
time this exact model+voice combination has overshot on this pipeline.
Runtime still cleared the 60-80s news band (62.3s), so accepted without a
regeneration, per the precedent that a second full-price take buys ~0.1 w/s
at best. Worth promoting from a per-reel note to an assumption: **budget
this voice at ~3.3 w/s, not 2.6 w/s, when sizing a script for a target
runtime**, rather than re-discovering the gap every time.

### Treatment history (do not repeat next reel)

split hook (real headline receipt over presenter) · `specsheet` motion-
graphic cards (dark, footnoted) for three feature explainers with no real
screenshot to show · `categorygrid` (3 colored cards) for a performance
grab-bag · plain `receipt` (headline + margin, no annotatezoom) for three
press screenshots and one official Apple page.

### Left honestly unfixed

- **Every G04 PACING advisory fired** (9 of 11 scenes held longer than
  their type's typical band; average scene 5.66s vs the 2.5s guideline) —
  a genuinely coarser cut rhythm than editorial style's usual "visual
  change every 2-3s", accepted for a script this information-dense with
  only 4 real source images and no per-clause b-roll. Splitting every
  merged clause into its own visual was the alternative; not done here.
- **Facecam 25% of runtime** (band 10%-20% for `news`) — three facecam
  beats (an app-explainer beat, the hedge/honesty beat, the closing take)
  in an 11-beat, 62s reel. Advisory only (G06 not in BLOCKING_RULES).
- **Scenes 4/5 (specsheet), 7/8 (receipt) and 9/10 (footage) each repeat
  their treatment back-to-back** (render_job.py's own validator flags
  this) — content-driven (two Siri-adjacent feature cards, two press
  screenshots, two facecam beats in sequence at the close) rather than a
  variety failure, but worth varying treatment more on the next reel that
  has this many same-type beats in a row.


## 2026-09-01 — the em-dash check was asked about twice, so the rate went to zero

**Raw note.** User, reading the qualcomm-chip-hike draft: *"If you are
humanizing our script, why are there em dashes in our script?"* The draft
carried two in 209 words.

**Root cause, and it is not the writing.** `check_script.py` has had a PAGE
PUNCTUATION check since 2026-08-26, added in answer to this same question the
FIRST time the user asked it. It was built as advice with a rate: fire past
one dash every 60 words. Two in 209 is one every 104. **The check stayed
silent on the exact draft that produced the complaint** — and it would have
stayed silent on the previous draft too, at one every 209. A threshold that
passes the case which prompts the question is not calibrated, it is
decorative, and the gap let a second identical conversation happen five days
later.

The 1-per-60 number was derived honestly (approved scripts sat at both ends of
it), but it answered the wrong question. It measured *how often*, when the
reason for the rule has no frequency term in it at all:

1. **A listener cannot hear a dash.** It renders as whatever pause a comma or
   full stop would have produced. It is a mark for the eye, in a medium with
   no eye.
2. **It breaks the synthesis.** Probed 2026-08-26: IndexTTS2 rejects em-dash,
   colon and semicolon outright.

Neither of those gets better at a lower rate. So the threshold is now **zero**,
and `PAGE PUNCTUATION fires on a SINGLE dash in a long script` is a new case in
`check_script.py --selftest` — without it, the tightening could be reverted to a
rate by anyone who reads the old comment and not this entry.

**Distilled rule: NO em or en dashes in narration. Write the comma or the full
stop you mean.** Still ADVICE per RULES.md §0 — prose is craft and this fails
all four blocking tests. It just no longer stays quiet.

**What it cost, honestly.** Re-scanned the corpus after the change:
apple-surprise-and-shine, claude-eating-tokens, iphone18-split and
september-preview now all flag. Those reels shipped and were approved; the
flag is retrospective advice, not a verdict on them.

**The second lesson, which is the older one in this repo.** The humanizer skill
was run on this script, and it did not remove these — because its own §14 says
the dash ban lifts when *the writer's sample uses them*, and the approved
scripts I fed it as the voice sample carry up to seven each. The sample taught
it the habit. When a skill's rule is conditional on the corpus, a corpus with
the defect in it will keep the defect. The checker has to hold that line, not
the skill.

### Treatment history (do not repeat next reel)

split hook with LIVE FOOTAGE on top (Snapdragon chip in circuitry) rather than
the screenshot the previous two reels used · animated three-bar cost card
(double digits vs 58-63% vs 400%+), each bar carrying its own source line ·
two-row landing card whose rows arrive on the words that name them
("Qualcomm's margins" / "your phone price") · closing question card over
product footage.


## 2026-09-01 — qualcomm-chip-hike: three silent checks, and a component contract nobody wrote down

Snapdragon price rise, 63.1s, -14.5 LUFS, gates green, lint clean.

**1. THREE CHECKS WERE SILENT, AND TWO HAD ALWAYS BEEN.** All the same shape:
a guard that could not run, reading as a guard that passed.

- `plan_shots.py` refused an approved script because it sha256'd the WHOLE
  script.md while `script_approval.py` hashes only the SPOKEN lines. They had
  agreed on every prior reel purely because no script.md had ever carried a
  markdown heading. Fixed by importing the shared function.
- `plan_shots.py` read `segments[].words[]` from vo.json, while
  `ingest_avatar.py` — the tool that WRITES vo.json — emits `{"words": [...]}`.
  So the anchor check found zero words on every reel ever built and printed
  "no vo.json yet", which reads as "not generated" rather than "cannot parse".
  Turned on, it immediately caught 4 unresolvable anchors on this reel.
- `check_script.py`'s PAGE PUNCTUATION fired only past one em-dash per 60
  words. The user asked "why are there em dashes in our script?" for the
  SECOND time about a draft at one per 104. Threshold is now zero.

**The distilled rule: a check that cannot run is worse than a check that
fails.** Two of these printed a cheerful line while doing nothing. When two
tools guard one guarantee, they must read the same bytes — pin it in a
self-test, not in a convention.

**2. DRAM READ AS "drum".** whisper base AND small both transcribed "drum",
which per RULES section 11 rules out a transcriber artefact — it was the
audio. HeyGen's brand glossary used to catch this class of thing; moving the
voice to ElevenLabs silently removed it, because a glossary only applies to
audio HeyGen synthesises, never to an upload. `vo_tagged.py` now carries
`PRONOUNCE`, applied only to `script-tagged.txt`. Probed before spending:
16.8s / ~243 credits compared D-RAM, DEE-ram and D.R.A.M. — all transcribe as
DRAM and all run 0.60-0.66s, so none spells the letters out.

**3. StatCard's label column is 220px with `whiteSpace: nowrap`, and nothing
says so anywhere.** A 45-character row label overflowed its box and ran under
the bar — the pink bar appeared to be drawn through the words. Read off
`17-statcard-mid.png`; invisible in every log. The fix was the LABELS, not the
component (RULES section 10). Working sizes: statcard row label <= ~14 chars,
value <= ~9 chars, detail goes in the footnote. `HeadlineBuild` already has
G05 for exactly this class of limit; **StatCard and SpecSheet do not, and
should.**

**4. A `wordcascade` rendered as a completely black frame.** Caught by
[DEAD SPACE] 95% and confirmed on the still. Not diagnosed — the beat was
replaced by letting the 9to5Google receipt carry the sentence, which was the
better edit anyway: its headline literally prints the words "double digits",
so the highlight moves from the headline to the phrase as it is spoken.
**Diagnosed the same day — see the G54 entry below.** It was TWO bugs, not
one, and the diagnosis was done twice in parallel: once here and once in a
spun-off session, which found strictly more (unknown `style` falls through
to browser-default 16px; `pixel` has a 46px base, not 100) and split the
physical bound from the corpus band the way G48/G49 do. That branch was
merged and this session's narrower G54 was reverted in its favour.
**The reusable lesson is about the split, not the bug:** a spun-off session
on a well-specified prompt is not automatically the duplicate — check its
commits before assuming, which is not what happened here first time.

**5. A source's own title cards leak into b-roll two ways.** Scene-detect at
threshold 0.3 misses slow dissolves, so a "single shot" by that measure held
three different framings; and a clip verified at its mid frame ran into a
"Learns your home" title at 1.4s. Both were caught by checking 9:16 centre
crops at 3 points per candidate before cutting. **Where two good phone shots
were each too short for their beat, CUTTING THEM TOGETHER into one clip file
was the answer** — one beat, one asset id, a hard cut inside it. New here.

### Treatment history (do not repeat next reel)

split hook with LIVE FOOTAGE on top (Snapdragon chip in circuitry) rather than
the screenshot the previous two reels used - checklist "ACROSS THE BOARD" with
rows landing on the words that name them - animated bar card built across
THREE beats, one bar arriving per claim, each with its own source line -
two-row "TWO CLOCKS" specsheet whose second row is the payoff - endquestion
(BUY NOW / WAIT) over the same chip the reel opened on, as a bookend -
two short b-roll shots concatenated into one clip file to cover one beat.

### Left honestly unfixed

- **Pace 3.25 w/s against the 2.35-2.75 band.** Same finding as
  apple-pencil-iphone-ultra, whose entry records two regenerations for a
  0.07 w/s gain. Not re-spent. Runtime still lands at 63.1s, inside the band.
- **G04 held-layout advisories on 8 card scenes** (2.6-3.7s vs a 2.6s cap).
  Every one of them has content ARRIVING during the hold — a highlight moving,
  a bar growing, a row landing — which is the distinction the rule itself
  draws. Accepted deliberately, not inherited.
- **[DEAD SPACE] on the wafer and die-grid shots (73%, 39%).** Inherent to
  footage of a wafer against black. Soft flag, left as shot.
- **Facecam 20%**, at the top of the 10-20% band.

## 2026-09-01 — G54: a `wordcascade` scene that cannot render (qualcomm-chip-hike)

**Raw note.** Scene 03 of the qualcomm reel rendered an entirely empty frame.
`lint_frames.py` caught it — "[DEAD SPACE] scene 03 (wordcascade): 95% of frame
is flat/empty" — and the reel shipped by REPLACING the beat, so the bug stayed
live for the next reel that reached for wordcascade.

    {"type": "wordcascade", "bg": "#0b0d10", "words": [
       {"text": "DOUBLE", "style": "caps",     "at": 0.06, "size": 150},
       {"text": "DIGITS", "style": "gradient", "at": 0.42, "size": 150},
       {"text": "from today", "style": "serif", "at": 0.95, "size": 64}]}

**The component was right; the scene object was malformed, on two counts, and
each one produces a blank frame ON ITS OWN.** Both were confirmed by rendering
stills of a probe sheet rather than reasoning from the source, because the
component reads as though either one alone would be survivable:

1. **`bg` is a NAME, not a colour.** `BGS` in `WordCascade.tsx` is a three-key
   lookup (cream / black / white). `BGS["#0b0d10"]` is `undefined`, so nothing
   is painted — and the very next line, `dark = bg !== "black"`, comes back
   TRUE, so the ink is `#111111`. Black type on an unpainted (black) frame.
   Frame 8 of the probe render: uniform near-black.
2. **`size` is a MULTIPLIER (default 1), not pixels.** The component computes
   `100 * size` px. `150` renders a 15000px glyph: one letter swallows the
   1080x1920 canvas. Frame 50 of the probe: a flat field of accent yellow —
   the inside of the "D".

The two suspects that were NOT the bug: `at` is already seconds (the component
multiplies by fps), and `gradient` is a valid style. `mascot` and `bottomSrc`
are genuinely optional.

**Gate G54, RENDER-blocking** — the same category as G35 (a still in a video
slot) and G48 (framing that exposes backdrop): it is a black frame, not taste.
It refuses an unknown `bg`, an unknown `style` (which falls through
`wordStyle`'s default branch to browser-default 16px with no font family),
missing/empty `words`, a non-positive `size`, and an `at` at or past the end of
its own beat (the frames-vs-seconds slip: the word is never drawn).

**The blocking bound on `size` is PHYSICAL, not the corpus band.** It fires when
`base_px * size` exceeds the canvas height — a line taller than the frame cannot
be a word on screen, only a flat field. The corpus band (0.6-1.6 across all 102
wordcascade words on disk) is taste, so it advises as **G54a**. Same split as
G48/G49: what stops the frame rendering blocks; what merely looks unlike
anything shipped is a note.

**The fixture proved the gate before the reel did.** `test_gates.py`'s baseline
sheet had carried `{"type": "wordcascade", "durationSec": 2.5, "bg": "cream"}`
with **no `words` key at all** since it was written — a scene that draws an empty
stack for its whole beat, sitting inside the sheet whose job is to pass every
gate. It has words now.

**The component also got a two-line hardening**, deliberately narrow: resolve
the bg KEY first, then derive both the background and `dark` from it, so an
unknown key can never again disagree with itself. G54 stops a bad beat sheet at
build time, but Remotion Studio and `npx remotion still` run no gates, and a
blank preview is how this got mistaken for a component bug in the first place.

**This was a KNOWN open item, written down and left as prose.** 2026-08-17
listed under STILL PROSE: *"a gate validating MG scene shape against the `Scene`
union — `wordcascade` took `lines` instead of `words[]` … both would have
rendered EMPTY and nothing checks MG shape against the union."* Two weeks later
a wordcascade rendered empty for a different field on the same scene type. G54
closes it for `wordcascade` only; `chart`, `specsheet` and `statcard` still have
no shape gate, and the honest reading of this entry is that the next one will
be found the same way.

## 2026-09-01 — G55 + G20 widened: the other three MG cards, and a shipped defect

Finishing what G54 started, and what 2026-08-17 wrote down and left as prose.
`chart`, `specsheet` and `statcard` now have a shape gate. Every entry was read
off the component, and each one either kills the render or draws the wrong
thing silently:

| what | what it does |
|---|---|
| chart with no `title` | `title.length > 26 ? 76 : 88` throws — the render dies |
| `rows`/`items` absent | `.map` / `.slice` on undefined. This is the `rows`-instead-of-`items` slip from 2026-08-17, exactly |
| chart `value` not a number | `Math.max(...)` goes NaN, `width: NaN%`, and `.toLocaleString()` throws on undefined |
| more than 8 chart items | `items.slice(0, 8)`. The 9th is not small, it is absent, while the voice still names it |
| `statcard` `pct` above 1 | clamped to a full bar — see below |
| `specsheet` `bgSrc` still | `<OffthreadVideo>`, one frame, "No frame found at position N". G35 on a field G35 never looked at |

**`bg` is only ADVICE here, and that is not an oversight.** ChartScene and
StatCard branch on `bg === "black"` and fall back to cream, so an unknown value
renders a readable cream card. WordCascade's `BGS` is a LOOKUP, which is why the
identical mistake there is a black frame and blocks under G54. Same field name,
different physics, different classification.

**iphone-18-pro SHIPPED FOUR STATCARDS WITH FLAT BARS.** `pct` is a fraction and
StatCard does `Math.max(0, Math.min(1, pct))`. Scenes 12, 16, 20 and 23 were
written on a 0-100 scale, so:

    {"label": "iPhone 17 Pro", "pct": 66}    ->  clamped to 1  ->  full bar
    {"label": "iPhone 18 Pro", "pct": 100}   ->  clamped to 1  ->  full bar

Rendered both to be sure rather than asserting it from the source (the G35
lesson): the two bars are **pixel-identical**, one pink and one purple, running
the full width of the track. The comparison the card exists to make was erased,
and the value text beside it still says "7-element lens" vs "about +50%". Same
class as G54's `size: 150` and G48's focus outside 0..1 — a scale misread that
the component silently absorbs.

**The four scenes are LEFT AS SHIPPED.** The reel is published; editing the beat
sheet now would make it describe something other than what was rendered, and
this ledger's value is that it records what happened. G55 blocks a re-render of
that sheet, which is the correct outcome — anyone re-rendering it must fix the
bars first, and the gate message names the number to write.

**G20 was only ever enforced on `checklist`, though its own text claims every
list row.** It now covers `specsheet`, `statcard` and `chart` too, with each
component's stagger read out of its source, not chosen. And it split, the way
G18/G18a did:

- **G20 (blocks)** — the last row never finishes. For a chart or a statcard
  "finishes" includes the bar's fill, because the value COUNTS UP during it: cut
  mid-fill and the number on screen is not the number.
- **G20a (advice)** — it finishes, but with less than `ROW_DWELL` (0.6s) left to
  read. That number is flat readability, and CLAUDE.md's warning applies to it:
  a number is not a rule. Measured before splitting, it rejects **five shipped
  scenes** whose rows all plainly land — apple-pay-india 27/43, ios27-tiers 42,
  iphone-18-pro 12/16, at 0.16-0.42s of dwell. Blocking a re-render of those
  would be taste wearing a rule's badge.

**The fixture was the third empty MG scene.** After `wordcascade`, `specsheet`
and `chart` in `test_gates.py`'s baseline also carried no rows and no items —
three cards drawing a title over an empty box, inside the sheet whose job is to
pass every gate. Nothing in the suite could have caught them, because until
today nothing checked that an MG card had anything in it.

## 2026-09-01 — the zoom WAS working. The receipt fallback was the dead half.

User: "we adapted zoom and scrolling effects to apply whenever possible, I
think our system is not adapting these." Traced it before touching anything,
and the first read of the data was wrong in a useful way.

**Counting `zoomDir` in the beat sheets says 330/809 scenes have motion, and
the two newest reels look terrible (1/13, 2/12). That count is misleading.**
`FootageScene` reads `scene.zoomDir ?? "in"` — absence means a 1.1x push, so
every bare footage scene already moves. The sheets are not the source of truth
for motion; the components are.

**The real dead spot: `receipt` with no `highlights`.** ReceiptScene does a
genuine focus pull — zoom onto the highlight cluster as it fires — but only
when highlights exist. With none it fell back to
`1.0 + interpolate(..., [0.02, 0.06])`: **a 4% push, the flattest move in the
codebase**, on the one scene type that holds a full-page screenshot for 6-9s.

**And 42 of 74 receipts across every reel have no highlights**, because
`compile_shot_plan.py` has never set them. So the fallback was not an edge
case — it was the treatment for most screenshots we ship. The reels with 0
missing (iphone18-colors, qualcomm-chip-hike, airpods-camera) are the
hand-built ones.

**Fix, at the component so every caller gets it:** the fallback now pushes
0 -> 0.10, **matched to FootageScene's existing 1.1x house push** rather than
a newly invented number. One constant, one file, every past and future reel.
Verified by re-rendering apple-surprise-and-shine and diffing the receipt
scene's first and last frame.

**Pinned:** two rows in `test_capture_defaults.py` — the receipt fallback must
stay >=9%, and FootageScene must still be 1.1x so the two cannot silently
drift apart. Confirmed the check FAILS when the old value is restored.

**Cued, not inferred:** `compile_shot_plan` now prints an ADVICE when a
receipt has no highlights, naming the covered line. The rect cannot be
computed here — knowing where on the page the claim sits needs someone to look
at the image, which is what the scout step is for. A generic push is the
floor; a pull to the claim is the goal.

### Found and NOT fixed: 26 of 30 card components are entry-only

`SpecSheet`, `TypeCard`, `WordCascade`, `Checklist`, `StatCard`, `HCompare`,
`Carousel`, `CategoryGrid` and the rest animate IN and then hold perfectly
still for the rest of the beat. CLAUDE.md already carries the rule from
`going-viral`: *"Nothing static — every element keeps a low-amplitude idle
motion."* It is not implemented in the components.

Left alone deliberately: a shared idle-drift wrapper across 26 components is a
real build with real layout risk, and it is not what was asked for. Recorded
here so it is a decision rather than an oversight.
## 2026-09-01 — the sweep: G56, and G35 was never about `footage`

Third and last pass on MG scene shape. G54 closed `wordcascade` after it cost a
beat, G55 closed the three cards, and this closes the remaining thirty-odd
scene types **before** they cost anything — which is the first time in this
repo a defect class has been shut ahead of the reel that would have found it.

**G35 was mis-scoped from the day it was written, and the scope was the bug.**
It reads "a still in `footage` or `floatcard` renders black", so it grew a
scene-type list. But the RULE has nothing to do with those two types: it is
that **a slot which does not branch on the file extension cannot take the other
kind of file**. Scanning every component for `isVideo(...)` found the real
count — **21 one-sided media slots**, of which G35 was watching two and G55 a
third (specsheet `bgSrc`, found the hard way six weeks later and moved into G35
here, because one rule belongs in one place).

The mirror was never checked at all. An `<Img>` handed an mp4 does not crash —
it draws **nothing**, quietly, which is the same failure as every other entry
in this ledger. Six still-only slots plus three inside lists now refuse a video.

Safe slots are deliberately absent from both tables: `brandhook.mediaSrc`,
`comparesplit.src`, `deviceframe.src`, `endquestion.src`, `hcompare.bottomSrc`,
`split.topSrc/bottomSrc`, `xpost.bgSrc/media` all do
`isVideo(src) ? <OffthreadVideo/> : <Img/>` and handle either kind.

**G56 — the list is absent, or empty.** Thirteen scene types do
`scene.<field>.map(...)` with no guard, so an absent field throws and the
render dies; an empty one draws the chrome around nothing. Plus three smaller
classes read off the same components: a fixed slot count that silently drops
the rest (`toolstack` and `stackwindows` both render `slice(0, 5)`, the same
defect as chart's `slice(0, 8)`), an index that selects nothing (`designreveal.
selectIndex`, `desktopmockup.selected`), and a `typecard` with no
`kinetic.text` — which does not crash, because TypeCard reads
`scene.kinetic?.text ?? ""`, it just lays out the empty string and renders an
empty field. That is G54's blank frame with different spelling.

**Where the union and the component disagree, the COMPONENT wins.** `promptcard`
marks `lines` optional and guards it (`scene.lines ? ... : ...`), so it is not
in the table. `typecard` marks `kinetic` required and the component defaults it,
so the gate has to be the thing that makes the union true of a JSON beat sheet.
The table is what renders, not what is declared.

**The tables are a claim about source code, so the suite re-derives them.**
Fourteen of the scene types named in the media tables appear in NO shipped reel
— nothing on this machine would have noticed if a component were later taught
to branch, and the gate would have gone on refusing a file the component had
learned to handle. `test_gates.py` now reads `Reel.tsx`'s dispatch, finds each
component, and fails if a slot the table calls one-sided contains
`isVideo(<field>)`, or if a branching slot is listed as one-sided. Verified by
temporarily teaching `ReceiptScene` to branch: the suite failed, as it should.
This is the `wiring_audit` idea applied to a lookup table — a table that
describes other code has to be checked against that code, or it is a comment.

**The corpus says the classification is right, not merely quiet.** Ten table
rows are exercised by 545 real scenes across every shipped reel, and none
fires. The other eleven rest on the source-drift check above, which is stated
here rather than implied.

**Nothing new blocks a shipped reel.** The only blocking hit anywhere in the
library is still iphone-18-pro's `pct` scale, disclosed in the entry above.
**The fixture was carrying the bug.** `tools/test_gates.py`'s known-good sheet
had a `wordcascade` with no `words` at all — the exact defect, sitting in the
file whose job is to be correct, invisible until a gate existed to look.

## 2026-09-01 — G56: the same land-check for typecard and kinetic overlays

G55 generalised the same day it landed. `wordcascade` turned out not to be
special: `Reel.tsx` suppresses the caption chips for a **`typecard`** and for
**any scene carrying a `kinetic` overlay** under the identical "one text system
at a time" rule. In all three cases the scene's own display type is the only
words on screen, so type that never lands leaves the beat with none — and for
the 70-85% watching on mute, a beat that says nothing.

**TypeCard is the worse of the two.** Its `bg` defaults to `theme.black`, so a
card whose first line never lands is the same uniform black frame the G55 probe
reproduced. A kinetic overlay sits over footage, so the picture survives and
only the words are lost.

**THE CONTRACTS, READ OFF THE COMPONENTS, NOT REMEMBERED.**

- `KineticType.tsx`: `startFrame = (kinetic.at ?? 0.15) * fps`, `null` before it.
- `TypeCard.tsx`: per line, `start = kinetic.ats?.[claim] ?? at + li * 0.11`.

`ats` is indexed by CLAIM (the `\n`-separated units) while `li` is the LINE
index, and lines are chosen by TypeCard's own ink search. **The gate does not
reimplement that search.** So the LAST landing is exact when `ats` is given and
is `at` plus an unknown ≤0.11s-per-line stagger otherwise — under-reporting the
dwell slightly rather than inventing a layout it cannot see. The FIRST landing
is exact either way (`li = 0`), which is what the blocking half rests on. Where
a check cannot be exact, say which half is exact and rest the law on that half.

**CALIBRATED ON WHAT SHIPPED**, the G23 discipline: 26 typecards and 11 kinetic
overlays on disk. **None** trips the blocking half. Exactly **one** trips the
dwell advice — a deliberate 0.68s flash card on qualcomm-chip-hike — which is
the same evidence that made G55a advisory, arriving independently.

**DISTILLED RULE (now covering all three): a scene that suppresses the captions
has no fallback layer, so its own type landing is a guarantee, not a pacing
preference.** G56 blocks four shapes — no text, no `kinetic` block at all on a
typecard, a first line that never lands, and a named `ats` claim that never
lands while the voice says it. G56a advises the too-tight-to-read case.

**Two more fixtures were carrying the defect.** The G12 case built two
typecards with no `kinetic` at all, and the G50 case used an invented
`{"lines": [...]}` shape that the `Kinetic` type has never had. Both were
invisible until a gate existed to look — the third time in two days that the
known-good sheet turned out to contain the thing being gated.

---

## 2026-09-01 — chatgpt-stickers (ai-tools, 56.7s)

First reel built entirely on USER-SUPPLIED screen recordings rather than
scouted third-party footage. Three lessons, all of which cost time here and
will not next time.

**RAW NOTE — the press was wrong and our own footage proved it.** Every
outlet that names a style count for ChatGPT's sticker picker says 18. The app
shows 19; the last row holds one orphan tile, which is what an odd count
looks like in a two-column grid. The entry path was also wrong in coverage
(sidebar -> Images -> Stickers) versus the shipped build (plus menu ->
Plugins -> Create image -> Stickers).
**ROOT CAUSE.** Both numbers came from outlets that did not open the app.
`research.md` already models this: VIA "own testing" is a first-class origin.
**DISTILLED RULE.** When the reel's own footage IS the primary source,
count/read the thing on screen before writing a single number, and record the
disagreement in the ledger rather than quietly siding with the press.

**RAW NOTE — the VO came back 2.87 w/s, outside the 2.35-2.75 band, and the
correct fix cost nothing.** Rather than regenerate (~973 credits), whisper
word timings were measured on two SHIPPED masters:
claude-eating-tokens 3.50 w/s SPEAKING with 21% gaps, iphone18-colors 3.63
with 18%. Ours spoke at 3.60 with 20% — in family. Only the pause budget was
short.
**ROOT CAUSE.** The band is words / TOTAL runtime, so it conflates speaking
rate with pause budget. A read can be perfectly in-voice and still miss it.
**DISTILLED RULE.** Before regenerating a VO for pace, split the measurement:
if SPEAKING w/s matches shipped masters, the fix is pauses, not a re-record.
Extend sentence boundaries with room tone lifted from the read's own longest
gap — never digital silence (audible dropout against a live noise floor) and
never time-stretch (moves pitch, which is the whole reason we render at
ElevenLabs). 13 boundaries x 215ms took 53.92s -> 56.72s, 2.73 w/s.
`vo_external.py` should grow this measurement; today it only prints the
overall figure.

**RAW NOTE — `ingest_avatar.py` silently overwrote a hand-corrected
vo.json, and its schema differs from raw whisper output.** Whisper hears
"nineteen" as "19", which broke the shot-9 phrase anchor exactly as
`rehearse_vo` predicted. The token was corrected, then ingest re-ran whisper
and threw the correction away — and the regenerated file is `{"words": [...]}`
where raw whisper is `{"segments": [{"words": [...]}]}`, so the re-fix script
failed silently on a KeyError until the shape was checked.
**DISTILLED RULE.** Correct vo.json AFTER `ingest_avatar.py`, never before,
and write transcript patches against the shape actually on disk. A spoken
number that whisper renders as digits will break its anchor every time —
`rehearse_vo` catches it for free and was right here.

**TREATMENT HISTORY (do not repeat next reel).** Cold-open split on the
finished artifact with a two-line HeadlineBuild; screen-recording walkthrough
carrying 18 of 22 beats; statcard for a rules trio; face bookends only at
open, attribution and CTA (3 of 22 beats).

**ACCEPTED ADVISORIES, disclosed.** Hook held 2.2s against the 2.0s advisory
(the sentence takes 2.2s to say and the audio is frozen post-approval);
scene 03 dead space 31% vs 30%; six scenes over the 2.9s single-visual
ceiling, which the ai-tools playbook itself expects of walkthroughs
("walkthroughs 4-5s/cut"). No blocking gate was overridden and `--soft` was
not used.


## 2026-09-01 — two spun-off sessions, and the three ways that went wrong

Three sessions ran against this repo at once: this one, plus two spun off to
fix things it had found. Every problem below is about the SPLIT, not the code.

**1. I called a spun-off session a duplicate without reading its commits.**
Twice. Both times it had found MORE than I had. Its wordcascade gate also
caught an unknown `style` (falls through `wordStyle`'s default to browser
16px), used the real per-style base px (`pixel` is 46, not 100), and split the
physical bound from the corpus band the way G48/G49 do. The second session's
label-budget gate MEASURED glyph advances with canvas `measureText` in
headless chromium — the same engine Remotion renders in — where I would have
typed a number. **Check `git log main..<branch>` before writing one off.** An
hour of my work was reverted because I did not.

**2. Independent numbering collides, and a Python dict hides it.** Both
sessions numbered from G54 up, for different checks. The raw cherry-pick left
TWO `"G56"` keys in `BLOCKING_RULES` — and a duplicate key silently keeps the
last, so the land-check would have lost its classification and quietly become
advisory with nobody choosing that. Renumbered to G57/G58; the suite now
asserts no id is registered twice. **A gate id is a shared namespace and
nothing was allocating it.**

**3. Sessions sharing one working tree will eat each other's staged work.**
A fourth session (chatgpt-stickers) ran `git add -A && git commit` on main
while G58 sat staged here, and swept it into its own commit. The code is
correct and on main; the history says something else. Worktrees prevented this
between the two spun-off sessions and would have prevented it here too.
**If more than one session may touch main, they need worktrees or they need to
not use `git add -A`.**

**What the merged gates immediately found.** `iphone-18-pro`, published, has
statcard rows with `pct` 66 / 100 / 65 / 70 where `pct` is a 0..1 fraction.
The component clamps, so every bar rendered FULL WIDTH and a two-row card drew
two identical bars whatever its numbers said. That reel's charts have always
been meaningless and no check saw it until G55. `apple-surprise-and-shine`
fails G18 by 0.28s, which is pre-existing and minor. **Neither is a false
positive; both are reels that shipped with the defect.**

### Idle motion: one wrapper, not 26 component edits (2026-09-01)

26 of 30 card components animated IN and then held perfectly still. The rule
was already written — CLAUDE.md carries `going-viral`'s *"nothing static,
every element keeps a low-amplitude idle motion"* — and was implemented
nowhere.

**Fixed at the single dispatch point.** Every scene routes through
`SceneSwitch` in `Reel.tsx`, so the switch body became `SceneBody` and
`SceneSwitch` now wraps it in `IdleMotion`: `translateY(-6px * t)` and
`scale(1 -> 1.02)` across the beat. One file, one wrapper, all 26 card types.

**Scale goes UP only** — the same reason G48 blocks a footage `zoom` below 1:
scaling down pulls the card's own edge into frame.

**`MOVES_ITSELF` excludes the eight types that animate themselves** —
footage, receipt, sourceread, annotatezoom, deviceframe, terminal, chart,
split. Stacking a second transform on FootageScene's 1.1x push or
ReceiptScene's focus pull would fight the move the scene is already making
rather than add to it.

**Verified, not assumed:** two `remotion still` frames 3.1s apart inside
claude-eating-tokens' statcard — previously byte-identical, now a mean pixel
delta of 4.49 across the card region.

### And a merge that had to be repaired first

`tools/reel_gates.py` was found carrying **committed conflict markers** — the
gates file, syntactically broken, with `test_gates` unable to import it. A
parallel session had been landing G55/G56/G57/G58 while this one worked.

The cause was an **ID collision**: two independent lines of work both claimed
`G56` — "a scene whose list is absent or empty draws nothing" and "display
type that never lands". The parallel session had already re-IDed the
land-check to **G58**, so the repair was to keep their block whole rather than
to pick a winner. 162 gate checks pass.

**Lesson worth keeping: a recompile discards hand edits to a beat sheet.**
Re-running `compile_shot_plan` to test the new receipt advisory wiped the
manual G18 timing fixes, the split hook and the merged facecam scenes from
apple-surprise-and-shine. The shot plan is the source of truth; anything fixed
only on the sheet is temporary.

### G18's boundary was wrong, not the reel (2026-09-01)

apple-surprise-and-shine failed G18 twice. Fixed it by hand on the sheet, then
a recompile threw the fix away — which is how the real bug surfaced.

**Measured instead of guessed.** Scene 7 ends at a cumulative
`44.260000000000005`; the next word starts at exactly `44.26`. G18 selects
`start <= a < end`, so `44.26 < 44.260000000000005` is **True** and the NEXT
scene's opening word was charged to the outgoing card — whose own end then
looked 0.28s short.

Scene ends are a **cumulative sum of rounded durations**, and phrase-anchored
compilation puts every cut on a word onset **by design**. So this was a
systemic false positive firing on correct reels, not a fault in any sheet.

**Fix:** one frame of slack on the upper bound (`a < end - 0.04`), symmetric
with the +0.04 already allowed on `claim_end`. A word beginning inside a
card's final frame belongs to the next beat.

**The test almost wasn't a test.** The first fixture summed to exactly 1.1 with
no drift and passed with the bug restored — a check that cannot fail. No
two-term sum of round durations reproduces it either (real sheets need eight
3-decimal ones). So the drift is now set explicitly with `+ 1e-12`, which IS
the condition, and the case was confirmed to FAIL when the old bound is put
back.

**Also reverted:** a change to `compile_shot_plan` made on the first, wrong
hypothesis (that whisper word timings overlap). They do not — "Mac." ends at
44.04, "Meaning," starts at 44.26. It fired zero times and was deleted.

### And the reel's own fixes moved to the shot plan

The split hook and the three-into-one facecam merge now live in
`shot-plan.json`, not the sheet, so a recompile keeps them. The plan is the
source of truth; anything fixed only on the sheet is temporary. `compile`
refusing to overwrite without `--force` is what caught this — a good guard.

Rendered: 13 scenes, 70.5s, -14.53 LUFS, gates pass, frame-lint clean.
Receipt scenes now measurably move (mean pixel delta 8.78 and 19.12 between
their first and last seconds, previously a 4% nudge).

**Left as advice:** the split hook runs 2.08s against the 2.0s guideline. G03
is advisory by the constitution, and 0.08s did not justify another compile and
render cycle.

**Hook tightened (2026-09-01):** anchor moved from "out to reveal" (2.08s) to
"walking out to" (1.76s), so the split hook is inside the 2.0s guideline
rather than 0.08s over. In the shot plan, so a recompile keeps it. Re-rendered:
70.5s, -14.53 LUFS, gates pass, frame-lint clean, no HARD LIMIT flag.

## 2026-09-01 — second motion audit: what the sweep found

Full pass over the engine after the motion work, plus a re-render of
qualcomm-chip-hike to carry the fixes.

**Everything green:** 163 gate checks, 81 script-pipeline, 73 hook, 15 VO, 15
capture defaults, 37 framework clauses, 0 orphans, doctor ok.

**Beat sheets: 15 pass / 11 blocked -> 17 pass / 9 blocked** after the two
fixes below. The remaining 9 are all pre-2026-08-18 material blocked on G45
(85 of the 94 violations) — captions under Instagram's account row, measured
after those reels shipped. New reels cannot ship it because G45 blocks, so
this is stale content, not an engine fault.

**G55 is catching REAL defects, not false-positiving.** 14 hits, all one root
cause: `pct=66` and `pct=100` on statcard rows where the component wants a
0..1 fraction. It clamps, so every row past 1 draws an IDENTICAL full bar —
the chart says nothing while looking fine. Confined to iphone-18-pro and its
nomusic twin, hand-authored, and **not generated by any tool**, so new reels
were never at risk. Divided by 100; that reel now passes.

Worth noting against the G18 case earlier today: a gate firing 14 times is not
by itself evidence of a false positive. G18's 2 hits were a bug in the gate;
G55's 14 were a bug in the data. The way to tell them apart is to read one.

**The VO alarm had silently re-derived from n=1.** `voice_calibration.json`
said n=1 while `corpus_wavs()` found 3 — the file had regressed to a single
sample, which makes a "flat for us" threshold nearly meaningless. Doctor's
standing warning is what surfaced it. Recalibrated to n=3.

**qualcomm-chip-hike re-rendered** — 63.1s, -14.58 LUFS, gates pass,
frame-lint clean. 8 card scenes newly carry idle motion; verified by frame
diff (checklist 7.56, statcard 7.87, statcard 4.58 mean delta between their
first and last second, previously frozen). Its 6 receipts already carried
highlights, so the receipt push changed nothing there — it is one of the
hand-built reels, which is exactly why it had no gaps to fix.

### G45 cleared on the 9 stale sheets (2026-09-01)

85 captions across 9 sheets sat below the 317px floor — under Instagram's own
account row, where the platform paints over the words. Two values only: 205
(40 scenes) and 300 (45). All pre-2026-08-18, written before that overlay was
measured.

**Raised to 500, not to 317.** 317 is the bare minimum that satisfies G45; 500
also clears G46, our own credit lane, and is the single most common value
across healthy reels (32 uses). Same principle as the receipt push earlier
today: reuse the house number rather than pick the value that just scrapes
past the gate.

**15 pass / 11 blocked this morning -> 25 pass / 1 blocked.**

**NOT VISUALLY VERIFIED, and that matters.** None of the 9 have footage on this
machine (`public/assets/` is excluded from git by design), so this is a
gate-level verdict only. Raising a caption 200-300px could in principle land
it against a headline or card in a scene nobody can render here. If any of
these is ever re-cut, look at the frames.

**seedance-25 stays blocked, deliberately.** Its remaining gates are RIGHTS,
not geometry: G27 (no approved narration on the sheet) and G14 (five borrowed
clips with no `credit`). There is no `jobs/seedance-25`, no `_sources` entry
and no manifest — **nothing anywhere records where that footage came from.**
Inventing an attribution to clear a rights gate is worse than leaving the reel
blocked, which is the whole reason G14 exists. It needs the person who
scouted it.

## 2026-09-01 — third sweep: two false leads rejected, one real gap closed

Went looking for what is broken. Most of the engine is genuinely healthy, and
the honest result of an audit is sometimes "this is fine" — so what follows is
what was CHECKED, not a list of invented work.

**Clean:** no scene type declared without a `SceneSwitch` case (either
direction), no component file nothing imports, 13 SFX cues all present on
disk, no missing music beds, format doc numbers match `FORMATS` in code,
smoke test passes, 163 gate checks, 25/26 beat sheets passing.

### Two things that LOOKED like defects and were not

**The black final frame.** The contact sheet ends on a pure black tile. It is
the tile grid padding — 11x6 = 66 cells for a 63-frame sheet. The real last
frame measures 79.2 mean luma. Nearly filed as a defect.

**"Footage scenes are letterboxed."** Three footage scenes flagged 34-73% dead
space, all four sources 1920x1080 landscape in a 1080x1920 frame — and a
fitted 16:9 clip occupies ~32% of a 9:16 frame, leaving ~68% black, which
matches the measured 73% almost exactly. A compelling story. `FootageScene`
sets `objectFit: "cover"`, so there is no letterboxing: that is dark wafer
footage reading as flat to a variance metric. **The arithmetic agreeing with a
hypothesis is not evidence for it.**

### The real gap, and it was mine

The receipt push got a check the day it was written. **The `IdleMotion`
wrapper did not** — delete it and every card silently freezes again with every
suite still green. Exactly the unguarded shape the receipt check exists to
prevent, in work written the same hour.

Two rows added to `test_capture_defaults`: the wrapper must be present, and
`MOVES_ITSELF` must still exclude footage and receipt so idle motion never
stacks on a scene that already moves. Confirmed to fail when the wrapper is
removed.

**Also verified my own change is safe rather than assuming it:** the 2% scale
could in principle clip type at the frame edge, and `[EDGE TEXT]` is a hard
lint flag. Neither rendered reel trips it.

## 2026-09-01 — chatgpt-stickers: a screen recording is not b-roll

The user gave the system 18 phone screen recordings and got back a reel with
two complaints: no real iPhone mockup, and footage that "appears zoomed and
doesn't fit to screen". Both were true, and neither was a taste call.

### The zoom was a default doing its job in the wrong place

`FootageScene` defaults to `zoomDir ?? "in"` — a 1.1x push. That is right for
b-roll, where a slow move keeps a static shot alive. It is wrong for a
recording already delivered at exactly 1080x1920: the push cuts ~10% off every
edge, and the first casualty is the header. Proved by stacking the source
frame against the rendered frame — "Create an image" sliced in half on a clip
that had fit the frame perfectly. `compile_shot_plan` now forces `zoomDir:
"none"` on any exact-1080x1920 footage source. Forced, not advised: the whole
point of a UI recording is to see the UI, and the crop is invisible in a beat
sheet.

### The mockup existed and had never been used

`DeviceFrame` with `kind: "phone"` had been in the codebase the whole time.
Its geometry was hardcoded at `cardW=470, mediaH=922`, so the phone occupied
48% of frame height with the content side-cropped and the notch sitting over
the app header. Rebuilt from an aspect-driven width — 940 wide, height derived
from the media — putting the device at 86% of frame height with nothing
cropped. The notch is suppressed over video sources, where it covered content
it was only ever meant to decorate.

### Then the fix for the first thing broke the second

The 17 converted device shots were pinned to `zoomDir: "none"` by carrying the
footage rule straight across. **The two rules are opposite.** A device push
scales the phone CARD, which has no crop window, so it cannot cut the UI — and
a frozen card makes consecutive shots of one screen render as identical
frames. The frame linter caught it as `[DUPLICATE] 15 -> 16` and was right.
`compile_shot_plan` now releases a deviceframe pinned to `none`, and
`test_capture_defaults` pins both halves — confirmed to fail when either is
removed.

### The duplicate was also editorial, and motion could not fix it

Restoring the push did not clear the flag, because the two shots showed the
same screen state. "This is where it stops people" is the pivot into the
3-sticker rule, and the rule is the statcard — so the line now lands on the
reveal it introduces instead of on a third copy of the same grid. Rule 3, and
one fewer shot.

### G57 measured a defect instead of fixing it

The statcard's bars painted through all three labels. This had already
happened on qualcomm-chip-hike, and the response had been G57 — a character
budget derived from StatCard's fixed 220px `nowrap` column. **The column was
the defect, not the copy.** Every honest label ("Minimum to export", "One
ChatGPT generation") blew the 15-character budget, so the gate fired on every
row of every card and, being ADVICE, changed nothing — and the bars painted
through the words anyway. A flex item does not clip.

StatCard's rows are now a 3-column grid, `minmax(0, max-content) minmax(140px,
1fr) max-content`. A label cannot overlap a bar at any length. G57 is
re-derived from what actually constrains the layout now — the room the label
has before the bar hits its 140px floor, 36 characters — and `test_gates`
pins that `nowrap` has not come back, because ADVICE alone did not stop this
once already.

**The lesson worth keeping: when a gate fires on every single case, the gate
is describing a broken component, not bad copy.**

### A tool crash that only appears on some reels

`lint_frames` built its contact sheet with `tile={cols}x{rows}` and did not
pad the frame list, so 6 stills into a 4x2 grid made ffmpeg exit non-zero and
took the whole render with it — after the render had already succeeded. Padded
with the last still.

## 2026-09-01 — the hook, the message that lied, and the video nobody was reading

### A hook can only be tightened where the silence is

`chatgpt-stickers` held its opening split for 2.16s. The hook LINE ends at
1.50s — the remaining 0.66s was a pause in the read, spent on one frozen
layout at the exact moment a viewer decides whether to stay. The anchor could
not move: 2.16s is when the next word is spoken.

So the hook was split on its own payoff word. "Those aren't downloaded" holds
the split (1.06s), then a hard cut to the phone mockup as "stickers." lands —
1.06s, inside `going-viral`'s 1.2-1.6s claim window — and the pause is now
covered by a scale-up instead of a freeze. **Where a hook runs long because of
a pause, the fix is a second visual inside it, not a shorter line.**

### A lint message that asserted a rule the constitution had abolished

The linter printed `HARD LIMIT 2.0s (user rule, blocking)` on the hook and
`(blocking)` on clip reuse. Neither blocks. The 2026-08-22 reclassification had
already fixed the VERDICT — it derives from `BLOCKING_RULES` — but the message
text was typed by hand, so nothing kept the two in sync, and for nine days the
linter told the reader a hard limit existed that the constitution explicitly
does not have ("no hook length you must respect").

Severity is now printed from the same lookup that sets the exit code, so every
flag reads `[advice]` or `[BLOCKS]` and a message cannot contradict the
verdict. Proved by temporarily adding G03 to `BLOCKING_RULES`: the same flag
flips to `[BLOCKS]` and the exit code follows. `test_gates` now fails if any
flag message contains the word "blocking" at all.

**The rule: a check may not assert its own severity. Severity has one home.**

### Four renders were "verified" against a 44-minute-old video

`lint_frames` defaulted to `out/<slug>.mp4` — a file that exists only because
the `news-reel` skill tells a human to `cp out/<slug>-final.mp4` onto it first.
The copy is a ritual, and a skipped ritual is silent. After the first copy,
every re-render updated `-final.mp4` and every lint kept reading the original.

It produced a false conclusion that survived three fixes: a `[DUPLICATE]` on
the tightened hook that the current cut did not have, and — worse — a
"restoring the push did not clear the flag" that was read entirely off the old
video. The device-push conclusion happened to be right for other reasons, but
the evidence for it was worthless.

The linter now prefers `-final.mp4` and **refuses any video older than the beat
sheet it is being checked against**, because preferring the right file only
fixes the copy: editing beats and linting without re-rendering reads the
previous cut and calls it a result.

**Evidence read from a stale artifact is worse than no evidence, because it
looks like a result.** Every "I verified it" in this repo is only as good as
the freshness of the thing that was read.
