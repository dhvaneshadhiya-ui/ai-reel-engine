# Research — gemini-4-argon

Claims ledger + search log. Tiers: official / multi / single / disputed.
A single or disputed claim must be SPOKEN hedged (framework S20).
Primary: Google launch post Sep 30 2026 (Koray Kavukcuoglu), Gemini app and
developer posts Oct 13 2026, Gemini API model + pricing pages, Google Cloud
post Oct 14, Fairwind Program page. Findings: research/findings_*.md.

## CLAIMS

- CLAIM: Argon was announced Sep 30 and first went only to trusted cyber defenders (Fairwind Program); broad paid access came Oct 13 — about two weeks later
  TIER: multi
  SPOKEN: "Gemini 4 Argon, spent its first two weeks with cyber defenders only"
  SURPRISE: 75
  SRC: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
  SRC: https://techcrunch.com/2026/09/30/google-releases-gemini-4-argon-called-its-most-powerful-model-yet/
  VIA: Google launch post Sep 30 (phased rollout "starting with" Fairwind defenders)
  VIA: TechCrunch Sep 30 ("only being rolled out to a select group of the company's cyber partners")

- CLAIM: Gemini 4 Argon is Google's flagship model, now in the Gemini app and AI Mode in Search for Google AI Pro and Ultra subscribers
  TIER: official
  SPOKEN: "it's live in the Gemini app and AI Mode in Search for Google AI Pro and Ultra subscribers"
  SURPRISE: 45
  SRC: https://blog.google/innovation-and-ai/products/gemini-app/gemini-4-argon-availability/
  SRC: https://www.engadget.com/2285023/google-gemini-4-argon-is-now-available-in-the-gemini-app-and-ai-mode-in-search/
  SRC: https://9to5google.com/2026/10/13/gemini-app-4-argon/
  VIA: Google Gemini app post Oct 13 ("Google AI Pro and Ultra subscribers can now access Gemini 4 Argon")
  VIA: 9to5Google Oct 13, own observation of the model picker showing "4 Argon"

- CLAIM: Google says Argon can autonomously find, validate and patch software vulnerabilities
  TIER: official
  SPOKEN: "Google says Argon can find security holes, test them and patch them by itself"
  SURPRISE: 65
  SRC: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
  SRC: https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud
  VIA: Google launch post (autonomously find, validate, and patch critical vulnerabilities)
  ONE-SOURCE-OK: a capability claim attributed to Google in the spoken words; no independent test exists yet.

- CLAIM: The public version ships with cyber mitigations that block offensive tasks; an unguarded version goes only to vetted defenders
  TIER: official
  SPOKEN: "So defenders got the first look, and your version refuses to help with attacks"
  SURPRISE: 60
  SRC: https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud
  SRC: https://deepmind.google/fairwind-program/
  VIA: Google Cloud post ("cyber mitigations that block offensive tasks such as pentesting and exploitation"; "without cyber guardrails to a select set of trusted defenders")
  ONE-SOURCE-OK: Google is the authority on its own model's safeguards.

- CLAIM: 1,048,576-token context window (input and output combined); input text, image, video, audio, PDF; output text only
  TIER: official
  SPOKEN: "It can read about a million tokens in one go, and it takes in text, images, video, audio and PDFs. But it only answers in text"
  SURPRISE: 40
  SRC: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon
  SRC: https://www.engadget.com/2285023/google-gemini-4-argon-is-now-available-in-the-gemini-app-and-ai-mode-in-search/
  VIA: Gemini API model page (1,048,576 tokens, "unified input and output"; output: Text)
  ONE-SOURCE-OK: the API spec page is the authoritative record of the model's limits.

- CLAIM: On the Artificial Analysis Intelligence Index, Argon (53) ties OpenAI's GPT-6 Astra
  TIER: multi
  SPOKEN: "the independent Artificial Analysis index has it tied with OpenAI's GPT-6 Astra"
  SURPRISE: 55
  SRC: https://artificialanalysis.ai/models/gemini-4-argon
  SRC: https://www.engadget.com/2285023/google-gemini-4-argon-is-now-available-in-the-gemini-app-and-ai-mode-in-search/
  VIA: Artificial Analysis model page (score 53, #8 of 216)
  VIA: Engadget, citing Artificial Analysis (matches GPT-6 Astra's score)

- CLAIM: Bloomberg reported Google employees say Argon struggles with real-world coding despite benchmark scores; Google denies it
  TIER: single
  SPOKEN: "But Bloomberg reports some Google staff say it struggles with real coding work, which Google disputes"
  SURPRISE: 80
  SRC: https://www.androidheadlines.com/2026/10/google-gemini-4-argon-launch-benchmark-performance-debate.html
  VIA: Bloomberg (paywalled), via Android Headlines Oct 1
  ONE-SOURCE-OK: spoken attributed to Bloomberg and paired with Google's denial; Bloomberg original is paywalled.

- CLAIM: API intro pricing $2 per 1M input tokens ($10 output) through Nov 30 2026, then $4 / $20
  TIER: official
  SPOKEN: "it's two dollars per million input tokens until November thirtieth. After that, the price doubles"
  SURPRISE: 50
  SRC: https://ai.google.dev/gemini-api/docs/pricing
  SRC: https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud
  VIA: Gemini API pricing page and Google Cloud post ("standard pricing of $4 per million input tokens and $20")
  ONE-SOURCE-OK: Google sets its own prices.

## FEATURES + HOW TO USE

- Gemini app + AI Mode for Pro/Ultra — USED
- API paid tier (AI Studio, Android Studio), Antigravity for Ultra — CUT (developer detail; price kept)
- Vulnerability find/validate/patch; Fairwind unguarded version — USED
- Default cyber mitigations block offensive tasks — USED
- 1M context; multimodal in; text out — USED
- Long decode up to ~1M output (default 65K) — CUT (needs caveat)
- Computer use (Preview) — CUT (preview)
- Benchmarks: DeepSWE 77.9%, LVBench 91.7%, AutomationBench 51.3% — CUT (Google's own numbers; independent AA tie used instead)
- Quantum optimization 40%, C/C++ to Rust 800K+ lines, Chromium refactor — CUT (internal demos, need explaining)
- Partner results (ServiceNow, HubX, Wiz) — CUT (vendor-reported)
- App changes: faster, less hedging, chat/tasks toggle — CUT (pace)

HOW TO USE (vendor): open the Gemini app or AI Mode on a Pro/Ultra plan and pick 4 Argon in the model picker; developers call model ID gemini-4-argon on the paid API tier.

## NOT CLAIMED

- Subscription prices ($19.99 / $99.99) — no Google page showed them.
- Google AI Plus access — plans page and app post conflict.
- "Beats" GPT-6 Astra — it is a tie; AA ranks it #8 overall.
- aiweekly hallucination figures (15% vs 51%) — snippet only.
- Vals ProgramBench 5/200 — snippet only.
- $400M cost of scrapped 3.5 Pro — Bloomberg Intelligence estimate via a secondary.
- Worldwide consumer availability — "globally" applies to the API only.
- "Too dangerous to release" — no source says that; defenders-first is Google's stated phasing.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-14  "Gemini 4 Argon Google"  (Google launch post Sep 30, app + developer posts Oct 13, API model page, Cloud post)
- 2026-10-14  "Gemini 4 Argon pricing API"  (intro $2/$10 to Nov 30, then $4/$20)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by
###    someone who is not the vendor
- 2026-10-14  "Gemini 4 Argon Artificial Analysis Intelligence Index"  (AA score 53, #8 of 216; Engadget: matches GPT-6 Astra)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-14  "Gemini 4 Argon reaction developers coding"  (Bloomberg via Android Headlines: staff say weak at real coding; Google denies; 9to5Google picker observation)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if
###    you were trying to prove the story wrong
- 2026-10-14  "Gemini 4 Argon struggles coding benchmark criticism"  (coding-gap reports; prices double Dec 1; rollout gradual; no free tier)

INDEPENDENT-CHECK: 2026-10-14 searched independent testing of Gemini 4 Argon — found Artificial Analysis index result (independent benchmark) and Bloomberg's employee reporting; no independent hands-on review of the app yet.
