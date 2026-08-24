# RULES — the binding checklist

**Read this before every reel. It is the current, deduplicated truth.**
`STYLE-RULES.md` is the dated ledger behind it — go there for *why* a rule
exists, or to append new feedback. When the two disagree, this file wins,
because the ledger is append-only and contains superseded entries by design.

Every rule below is tagged with how it is enforced:

| Tag | Meaning |
|---|---|
| **[GATE:Gxx]** | `tools/reel_gates.py` — **raises and stops the build**. Cannot be skipped. |
| **[LINT]** | `tools/lint_frames.py` — **exits non-zero** on a hard flag. `--soft` overrides, and you must say so when handing over. |
| **[EYE]** | No automation exists. You are the only check. These are where reels actually go wrong. |

Adding a rule? If it can be measured, add a gate and a case in
`tools/test_gates.py` — prose rules get skipped. That is the lesson of
2026-08-11, when a pacing "rule" printed FAIL for weeks without failing
anything and the linter's pixel checks sat disabled behind an unread
`[SKIP] PIL not installed`.

---

## 0. WHAT MAY BLOCK — the classification test

**User instruction, 2026-08-18: "Make sure that everything we develop further
remains advice unless it is genuinely required to be a blocking gate or
hardcoded."**

A new check is **ADVICE by default**. `_partition()` in `tools/reel_gates.py`
already enforces this mechanically — a gate id absent from `BLOCKING_RULES`
cannot stop a render — so the failure mode is not "forgot to classify", it is
**classifying something as blocking that isn't**.

Before adding an id to `BLOCKING_RULES`, it must pass all four:

1. **It restates one of the three standing rules, or render-correctness, or
   rights.** R1 Reels/Shorts · R2 mobile-first scouting · R3 picture matches
   words · RENDER produces a black frame or a crash · RIGHTS attribution and
   the user's approval. Nothing else is law.
2. **Its threshold is a MEASUREMENT of something outside us**, not a number we
   picked. Instagram's account row at y 0.835 is a fact about Instagram.
   "Captions look better above y 0.74" is a fact about our taste.
3. **A violation is unfixable downstream.** If the renderer clamps it, the
   frame is already correct and the gate is a lint, not a law.
4. **It fails a real case in `tools/test_gates.py`, AND a legitimate
   neighbouring case stays silent.** A gate with no negative test will
   eventually block good work — that is how G21 reached 100% false positives.

**Worked example — the one that failed this test.** G45 was added 2026-08-18
blocking every caption below y 0.740 as "under the platform's own UI". It
passed (1), (3) and (4), and failed (2): the platform's UI starts at y 0.835,
so 183px of the band was our own credit lane — craft wearing an R1 badge, the
exact fault the G18 note warns about. Split the next day into **G45**
(blocking, at the measured 0.835) and **G46** (advice, our credit lane).

The same test applies to CONSTANTS. A number inside an advisory tool or a
component is craft and may be typed — but prefer deriving it, and say in a
comment what it was derived from. A number that decides whether a render
happens must be traceable to a measurement.

---

## 1. Locked user settings

| Setting | Value | Enforced |
|---|---|---|
| Runtime | per FORMAT (`--formats`), chosen from the topic, never padded. Past the band: `allowLong` + a written `allowLongReason`. **Hard ceiling 180s** (platform limit) — allowLong cannot pass it | [GATE:G02] |
| Voice speed | **1.05** | `config.json` [EYE] |
| HeyGen engine | **per-look, by measurement** — see `avatarRegistry` | `config.json` [EYE] |
| Caption style | **`word-reveal`** (was `nick-display`) | [GATE:G10] |
| Style pack | `editorial` default, else `utility`. Never invent a third. | [EYE] |
| Master | **−14 LUFS**, TP −1.2 | [EYE] |

**Source capture [GATE]:** web sources are captured on MOBILE —
`node tools/capture.mjs screenshot <url> --out <f>.png` defaults to
360x780 @3 = 1080x2340 with an iPhone UA and `isMobile`. G29 blocks a
landscape capture in a `sourceread`, or one under 1000px wide. `--desktop` for software UIs, dashboards, wide comparisons and pages with no
mobile layout — and a desktop capture must then be CROPPED to a `focus` region
and given motion (`annotatezoom`), never fitted whole. G29 blocks a landscape
`annotatezoom` with no focus. See `references/source-capture-policy.md`.

**Sound [GATE]:** every SFX cue must be in `tools/sfx_library.py`, exist on
disk, and its ROLE must fit the beat (G28) — transition on a cut, popup on an
element entering, suspense before a reveal, reveal on the payoff, impact on a
data card or the biggest claim. Caps per reel: impact 3, shutter 3, suspense 2,
reveal 2, comedic 1. Comedic stings only in `top5`, never serious tone. A cue
may not outrun its beat; a riser must resolve. See
`references/sfx-placement.md`. Count and volume stay with G08.

**Format [GATE]:** the beat sheet declares `format` (`news` | `top5` | `comparison`); it
selects the runtime band, hook ceiling, facecam share and SFX band from
`FORMATS` in reel_gates. Unknown format = G23 blocks. `top5` and `comparison` require a CTA scene (G24); `comparison` must also
declare its two `sides`, carry 3+ compare scenes, label every split and stay
balanced 40-60% (G26). Numbers come from teardowns, never from guesses.

**Script approval [GATE-BY-PROCESS]:** the narration and beat plan are shown
to the user and approved BEFORE any avatar video is generated. Generation
costs credits and freezes the audio; changing a word afterwards is a
re-render. [EYE]
Since 2026-08-21 the process has teeth upstream: `propose` exits non-zero
without a filled `jobs/<slug>/structure.md` (shape before sentences) AND a
valid `jobs/<slug>/research.md` — the claims ledger, where every load-bearing
claim carries a TIER, a SRC url, optionally the VIA (ultimate source) each
SRC traces to, and the SPOKEN words that carry it, verified to exist in
the script. `approve` exits non-zero unless the current script
hash-matches the last propose. [LINT — `tools/research_check.py`, run inside
`script_approval.py`; self-test `tools/test_script_pipeline.py`]
A single/disputed-tier claim spoken unhedged prints as advice (framework
S20), never blocks — sourcing depth is judgement, the record of it is not.

**Story [GATE]:** runtime per format (G02; `allowLong` + `allowLongReason` to
exceed the band, hard-capped at 180s).
Hook <= 2.0s and it opens on the actual tension, surprise or consequence —
never a generic product announcement (G03). Every sentence must change the
viewer's understanding; if it does not, cut it. [EYE for the cut, GATE for
the length]

**Pause-tightening a long master [EYE]:** jump-cutting video+audio together
at mid-silence recovers ~4-5% runtime for zero credits. Record every cut
point in the build script and never let a facecam beat SPAN one — a jump on
the face is visible, a jump under b-roll is not (made-by-google-26:
140.1s → 135.2s, 15 cuts).

**Captions [GATE]:** verified against the final narration, not the script
(G21). One highlight per beat (G22). Standard notation (G16). Official
product spelling and capitalization exactly as the source uses it.

**Design system [EYE]:** one series look — SF Pro, the registered palette
(#0aa9c2 / #2fb98a / #C2410C accents), word-reveal captions, the same chart
and transition vocabulary. Do not introduce a new hue or a new type family
for a single scene. Every important visual must be readable on a phone.

**Budget (HeyGen Pro, from 2026-08-12):** 436 credits/cycle, ~1 per 3s of
avatar, ~36 per 107s reel — about 12 reels. Script changes are affordable now,
so a weak script gets redone rather than patched. **Probe prompt-side changes
with a ~7s clip (~3 credits) before committing to a full generation.** [EYE]

`motionPrompt` is rejected by the API alongside `avatar_v` when the avatar's
group has no digital twin. **Drop the motion prompt — never downgrade the
engine.**

**Choose the presenter by MEASUREMENT, never by preference or by how the still
photo reads.** `python3 tools/measure_avatar.py score <clip.mp4>` returns the
mean frame-to-frame delta in the hand region: **<1.0 frozen (do not ship),
1.0-2.5 stiff, 3+ gestures.** Register it, then `use <lookId>` to switch, or
put `"avatar": "<lookId>"` in a reel's manifest to override for one video.

Measured so far: blue hoodie `0aa05d6e` = **0.48 on avatar_v (frozen)** but
**6.01 on avatar_iv + expressiveness:high + motionPrompt**; black hoodie
`48d4076` = **5.32 on avatar_v alone**. The engine that gestures is therefore a
property OF THE LOOK — `expressiveness` is avatar_iv only, and `motionPrompt`
needs a digital twin on avatar_v. Store the winning engine with the look.

**Gestures come from the LOOK first, the engine second — and no Digital Twin
is required.** Measured on identical 6.3s clips (mean frame-to-frame delta in
the hand region): look `0aa05d6e` = 0.54, look `48d4076` = 3.46 on the SAME
engine and params — **6.4x from the look alone**. Adding
`avatar_iv` + `expressiveness:high` + `motionPrompt` reaches 6.74, but that
trades away Avatar V, so we take the look.
**Before adopting any new look, measure it:** render ~6s, crop the hand
region, take the mean consecutive-frame delta. Under ~1.0 is a frozen
presenter; 3+ moves. A still photo that looks great can animate almost not at
all. [EYE]

## 2. Order of operations

1. Verify the story (web search — topics are newer than training data).
2. **Scout footage and write the manifest BEFORE any script line.**
3. Script + beat map, every beat bound to a manifest id or an MG spec.
4. Avatar master → whisper word timings → face-x.
5. Build (gates run here) → register → render → master.
6. Frame lint → **read every frame** → fix → re-verify.
7. Append to `STYLE-RULES.md` + treatment history.

**The one rule that matters most: never script a claim you cannot show.**
Source the footage first, then write to it. [EYE]

## 2b. Scripting — the story standard

`styles/shortform-script-framework.md` is the standard a script is written to.
Read it before writing, not after. Its one sentence, if you read nothing else:

> **The goal is not to summarize information.**

The failure it exists to prevent has a name and a shape — a source article
turned into ordered facts, each true, none connected. It is not a shape you
notice while writing; you notice it when the reel is cut and every beat lands
the same way. [EYE]

Four of its sections are now MEASURED by `tools/check_script.py`, which prints
at approval time — where a script can still be changed. [LINT, advice]

| Framework | Measured as | Weak / approved |
|---|---|---|
| §9, §22 transitions | sentences that bridge to the one before | 9% / 53% |
| §21 density | sentences carrying a measurement | 58% / 31% |
| §3 no bullet lists | longest run of consecutive spec lines | 5 / 4 |
| §7 what → so what | spec lines that never say what the number does | 71% / 80% |
| §2, §10 open loops | a promise in the first third, paid off later | none / two |
| §1, §16 hook vs context | opening carries a version, date or time anchor | no / yes |

Those numbers are a MATCHED PAIR — the same story (iPhone 18 Pro) written twice,
once well and once as a list. The thresholds sit between the two, which is the
only reason to believe them. `check_script.py --selftest` asserts the separation
still holds; if it ever stops, the checker has stopped meaning anything.

Everything here is ADVICE, per section 0: prose is craft, and a script that
breaks all of it and reads brilliantly is a good script.

## 2c. Credits on screen (user decision 2026-08-19)

**Once per source, short label.** The first scene to use a source draws its
credit; later scenes from the same source draw nothing. The drawn label stops at
the first em dash: `Unbox Therapy — dummy unit` renders as `Source: Unbox
Therapy`. [LINT — `tools/check_assumptions.py`]

Measured before the change: iphone-fold-ultra drew a credit on 76% of its
runtime, `Unbox Therapy — dummy unit` 24 times and `MacRumors` 12. It never
flickered — the label does not animate and sits at a fixed position — it simply
never left. After: two credits in the whole reel, at 0.8s and 18.2s.

**The beat sheet keeps `credit` on every scene.** Only the DRAWING is
deduplicated. G14 reads the sheet, and stripping credits there would lose which
asset came from where.

**Every component goes through `<Credit>`.** Four did not, and each silently
opted out of both rules by drawing its own label — FloatingCard reimplemented
the whole thing to anchor attribution under its card (Credit takes a `top`
prop now, so the placement survives), and SpecSheet, StatCard and PriceLadder
called it `footnote`. Attribution has three spellings in this repo — `credit`,
`source`, `footnote` — and a rule that only knows one of them is a rule that
holds for some components.

**What this costs, recorded honestly.** On iphone-fold-ultra the stripped
suffix was the only place the word "dummy" appeared in 46 scenes. The manifest
asks for "a DUMMY UNIT label AND the Unbox Therapy credit"; the label was never
built. Nothing on screen now tells a viewer that footage is a non-functional
mockup. The fix the manifest already specifies is the LABEL on one dummy beat —
not the suffix back on every credit.

## 3. Truth and provenance

- Every figure comes from the manifest's `verified_facts`, with unit and
  source url. No figure enters the script any other way. [EYE]
- Claims the sources do **not** support go in `explicitly_NOT_claimed`, with
  the **banned source timestamps**, so they cannot leak back in as b-roll.
  Banned asset ids are refused at build time. [GATE:G11]
- Every `assetId` in the beat sheet must exist in the manifest. [GATE:G11]
- Write an asset's `shows` field **only after looking at extracted frames**.
  Never from what you assume is there. [EYE]
- If research contradicts the premise, say so and correct it. A corrected
  beat beats a checkable falsehood. [EYE]
- **Credit every source we use, on screen.** Borrowed footage carries
  `credit`; any card showing a number carries `source`/`footnote`.
  [GATE:G14] [GATE:G15]

### Sourcing: attribute, don't hedge (user policy 2026-08-11)

Source quality is a **framing dial, never a gate** — it changes how a claim is
said, never whether the video gets made. Most tech news is sourced reporting,
and a lot of it turns out true.

- **Name who reported it once, early — then state the substance with
  confidence.** One attribution beat replaces three caveat beats. [EYE]
- Budget **<=3% of runtime** on qualifying language. apple-pay-india v1 spent
  10%, including 8.2 consecutive seconds saying "unconfirmed" three ways —
  that reads as not trusting your own sourcing. [EYE]
- Loudness of attribution by tier: official → state flat · named reporting
  with a track record → attribute once, then direct · analyst → attribute +
  "forecast" · aggregator → never cite, go to the original · anonymous account
  → cover it framed as "X claims", credited. [EYE]
- **No source at all is not a rumour, it is absent.** Nobody to credit means
  nothing to put on screen. [EYE]
- **Weight by claim type, not just source.** Specific figures and mechanisms
  are the firmest part of a report; DATES are the softest. Lead on the
  mechanism. Most coverage does the reverse. [EYE]

## 4. Pacing

- Hook ≤ **2.2s**. [GATE:G03] [LINT]
- Held layouts: motion (footage/split/video-backed card) ≤ **2.9s**;
  building data screens (specsheet/chart/timeline, content landing in
  sequence) ≤ **3.3s**; every other card ≤ **2.6s**. [GATE:G04] [LINT]
- "It animates internally" is **not** an exemption for a static layout.
  Micro-motion — push-ins, springs, count-ups — does not count. Only genuine
  content change does. [EYE]
- Long VO sentences split across 2–3 distinct visuals, always. [EYE]
- Scenes sum exactly to the audio; reel ends ≤0.4s after the last spoken
  word, never on a frozen face. [GATE:G01]
- One source clip carries **one** footage beat. Mine a long source for
  distinct shots. [GATE:G07] [LINT]
- **Cut every clip longer than the beat that plays it** (>=2.8s). A short
  clip silently spills into whatever the source cut to next. [GATE:G13]
- **Cuts anchor to the words the visual is ABOUT — never to clock time.**
  Each anchor phrase owns a list of visuals; its span is divided among them.
  A region too long for one visual gets MORE VISUALS FROM THAT REGION, never
  the neighbour's. Reference: `region_bounds()` in `tools/build_applepay.py`.
  Distributing beats evenly by time silently destroys sync. [EYE]
- Put a region's most SPECIFIC visual LAST, so the card carrying the number
  lands on the words saying the number. [EYE]
- A region carries only as many visuals as it has time for; never emit a
  sub-0.6s beat — it reads as a glitch, not a cut. [EYE]

## 5. Composition

- **Never open on** a document, browser, file bin, black screen or spinner.
  Open on the strongest shot of the payoff. [EYE]
- The hook must pass the **sound-off test**: could a viewer name the subject
  from the frame alone? Anchor on the most household-recognisable brand
  (parent company, not a sub-brand nobody knows), animated, in brand colour.
  [EYE]
- **No empty bands in the first 2s.** [LINT: HOOK DEAD SPACE, hard, >55%]
- Designed cards may read up to 70% flat; footage and small-asset-on-field
  30%. [LINT, soft]
- App/document recordings go in framed `floatcard`s, **never full-bleed**.
  A 16:9 diagram never runs full-bleed in a portrait frame. [EYE]
- Crop out **all** app chrome — tabs, sidebars, PiP webcams. **This applies to
  stills as well as clips**; a still extracted full-frame from a screen
  recording carries the PiP straight through. [EYE]
- Frame edges must not cut text mid-word. When a wide slide must keep its
  text, crop the **bottom band**, not the side. [LINT: EDGE TEXT, hard]
- Artifacts wider than ~2.5:1 go in a `floatcard` at their true aspect, NOT
  `receipt` — ReceiptScene's zoom (Z floor 1.35) overflows the frame and
  cuts them mid-word. [EYE]
- Test-crop ONE frame per source before cutting a batch: live-action usually
  survives a 9:16 crop, centred UI mockups never do. [EYE]
- Every number on screen carries its unit or column header. [EYE]
- **Nothing touches the frame edge.** Lists/checklists sit in a width-capped
  centred column with >=96px side margin. [EYE]
- **A data card must outlast the sentence it illustrates** — anchor its region
  on the LAST word of the claim, never the first. [GATE:G18]
- **Credits read "Source: X"**, sit directly under the card, left-aligned to
  the card edge. A bare name floating in the field reads as a stray word. [EYE]
- **Outro type sits at or just below centre (y ~0.42-0.50), never the top
  edge.** The 0.07 anchor is for overlays on footage, not for the closing
  card. [EYE]
- **`sourceread` — the source document with the spoken sentence highlighted
  live.** Use when the artefact is text-dense and portrait-friendly, the VO
  closely tracks the passage, and the claim is worth proving. NOT for wide
  screenshots (use `floatcard`), image-led pages, loose paraphrase, or
  uncontested claims. **Capture the page at mobile width (~390px CSS, scale
  3)** — a desktop capture is too wide a column for 9:16. [EYE]
- Highlights go **around** data (stroke/underline), never over it. [EYE]
- No flat empty backdrop behind a small asset — fill with a blurred copy. [EYE]
- Let the payoff breathe: the money shot plays clean, no captions, music up. [EYE]
- Nothing static: punch-in on every cut, alternating zoom direction. [EYE]

## 6. Type and captions

- **One text system at a time.** Display type and karaoke chips never speak the
  same words. A headline may run with chips only if the words differ. [EYE]
- Display type never sits on busy content. Over footage, only via a scrim on a
  quiet region — verified at the type's **landing frame**. [EYE]
- `HeadlineBuild` has **no auto-fit**. Line limits: `label` ≤30 chars,
  `headline` ≤18, `subtitle` ≤26. Over that it wraps and orphans a word.
  [GATE:G05]
- A 3-line outro block anchors at **y ≈ 0.07**; at 0.10 the last line grazes
  the presenter's hairline. [EYE]
- Closing question splits across two `headline` lines, the payoff half
  carrying `accent: true`. [EYE]
- Captions clear of the face and of any baked-in subtitle in the footage. [EYE]
- SF Pro only. No Fraunces/Georgia/serif families. [EYE]

### Standard visual notation (user rule 2026-08-11)

Every number, model name, money figure, date, percentage, unit, version and
technical term appears on screen in standard notation. [GATE:G16]

- `98.7%` not "ninety eight point seven percent" and not whisper's `98 .7 %`;
  `₹30 trillion` not "30 trillion rupees"; `15-20` not "15 to 20"; `3.5x` not
  "three point five times". Handled by `tools/notation.py`. [GATE:G16]
- **Normalise BEFORE chunking captions** (`normalise_words`) — notation spans
  word boundaries and the chunker cuts through it. [EYE]
- Product names come from the manifest's `notation` map — **verified spellings
  only, never a global guess table.** Do not invent punctuation, model
  versions, prices or abbreviations. [EYE]
- Don't over-normalise: a bare "one" is an article ("In one month"), not a
  datum. [EYE]

## 7. Presenter

- **On screen within the first 5 seconds.** [GATE:G17]
- **Motion prompt must ban props.** avatar_iv invents objects — a pen appeared
  mid-gesture on grok-bot. State "hands hold nothing: no pen, no phone, no
  papers". Scan the contact sheet for objects in the hands. [EYE]
- **Direct the expression per script section** (neutral explaining, raised brows
  on the surprising figure, serious on the caveat, warm on the close) or it
  holds one fixed smile the whole way through. [EYE]

- Face on screen **by second 2** — usually a split hook. [EYE]
- Facecam **10–20%** of runtime, returning in 1.5–3s pops, never one long
  block. [GATE:G06]
- Opinion / take / address-the-viewer lines are facecam beats — never
  decorative filler. [EYE]

## 8. Sound

- Background music is OPTIONAL per reel (user directive 2026-08-22).
  When present: volume-automated, never flat — full at the hook →
  duck under VO → rise at the reveal → fade. When absent: declare
  `noMusic: true` so a forgotten bed is distinguishable from a chosen
  VO-only cut; no reason required. SFX remain the default sound layer
  (G08/G28/G40 unchanged). [G09, advice]
- **6–9 SFX cues**, vols 0.10–0.19. Ordinary cuts stay silent. [GATE:G08]
- Master to −14 LUFS, verify with `ebur128`. [EYE]

## 9. Variety

- Never reuse the previous reel's treatment for the same kind of information.
  Check the treatment history in `STYLE-RULES.md` first, and log this reel's
  treatments after. [EYE]
- Plain black typecard: fallback of last resort, **max one per reel**.
  [GATE:G12]

## 10. Engine discipline

- **Never modify the engine to make one reel work.** If a reel seems to need
  it, the plan is wrong. BrandHook could not fit a 12-character product name —
  the correct fix was a different treatment, not a wider component.
- Never call `loadFont()` at module scope in a file `Root.tsx` imports; its
  `delayRender` runs on **every** composition and times out unrelated renders.
- Keep raw downloads in `<repo>/_sources/<slug>/`, never under `public/` —
  Remotion copies all of `public/` on every render.
- Render with `--concurrency=2 --timeout=120000`.
- zsh: inline the whole filtergraph. `$VAR` inside `-vf`/`-filter_complex`
  silently empties, and the stale output file survives so it looks like the
  change "didn't take".

## 11. Verification

- Whisper `base` misspelling a product name is **not** evidence of
  mispronunciation. Re-run whisper `small` on the 2s slice before spending
  credits on a re-record. Check every number and date against the script. [EYE]
- Run `python3 scripts/doctor.py` before a session — it fails loudly on a
  missing dependency instead of letting a check silently skip.
- Run `python3 tools/test_gates.py` after touching `reel_gates.py`. A gate
  that never fires is worse than no gate.
- **Check the FIRST second of every cut clip, not just the mid frame.** Cut
  clips open on the previous broadcast shot (stage presenters, the prior
  product) — five clips leaked this way on made-by-google-26. The linter now
  prints **[HEAD DRIFT]** (soft) when a motion scene's start frame diverges
  sharply from its mid frame; on a real leak, trim with `from` or re-cut. [LINT]
- **Verify a stage-slide crop at BOTH ends of its window** — broadcast
  cameras cut mid-window, and a crop verified on one frame drifts onto
  presenters or the wall. Prefer the full-frame slide moments (cameras hold
  them ~3-6s). [EYE]
- **Read every frame of the contact sheet as a hostile viewer.** Asset errors
  are invisible in logs. This is still where most defects are caught. [EYE]
- **Print the sync table before delivering** — `scene -> time window -> the
  caption words spoken in that window`. A contact sheet shows plausible
  frames in a plausible order and hides visual/VO drift completely. This is
  a separate check from the sheet, and it is not optional. [EYE]
- If `loudnorm` undershoots the -14 target, the true-peak ceiling is binding:
  put a light `acompressor` + `alimiter` before it. [EYE]
