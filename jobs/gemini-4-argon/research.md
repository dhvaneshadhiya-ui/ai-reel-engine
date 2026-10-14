# Research — gemini-4-argon

Claims ledger + search log. Tiers: official / multi / single / disputed.
A single or disputed claim must be SPOKEN hedged (framework S20).
Primary: Google launch post Sep 30 2026 (Koray Kavukcuoglu), Gemini app and
developer posts Oct 13 2026, Gemini API model + pricing pages, Google Cloud
post Oct 14, Fairwind Program page. Findings: research/findings_*.md.

## CLAIMS

- CLAIM: Gemini 4 Argon is Google's most powerful model yet, now in the Gemini app
  TIER: multi
  SPOKEN: "Google just put its most powerful Gemini yet in the Gemini app"
  SURPRISE: 40
  SRC: https://techcrunch.com/2026/09/30/google-releases-gemini-4-argon-called-its-most-powerful-model-yet/
  SRC: https://blog.google/innovation-and-ai/products/gemini-app/gemini-4-argon-availability/
  VIA: Google (launch post calls it its flagship / "next era of frontier intelligence"), reported by TechCrunch as "its most powerful model yet"
  VIA: Google Gemini app post Oct 13

- CLAIM: Google AI Pro and Ultra subscribers can use Argon in the Gemini app now (from Oct 13)
  TIER: official
  SPOKEN: "It's Gemini 4 Argon, and if you're on Pro or Ultra, it's yours today"
  SURPRISE: 45
  SRC: https://blog.google/innovation-and-ai/products/gemini-app/gemini-4-argon-availability/
  SRC: https://www.engadget.com/2285023/google-gemini-4-argon-is-now-available-in-the-gemini-app-and-ai-mode-in-search/
  SRC: https://9to5google.com/2026/10/13/gemini-app-4-argon/
  VIA: Google ("Google AI Pro and Ultra subscribers can now access Gemini 4 Argon")
  VIA: 9to5Google own observation of "4 Argon" in the model picker

- CLAIM: In the Gemini app with Argon (High), one prompt produced an interactive 3D floor plan of a 12x15 ft living room with lighting controls
  TIER: single
  SPOKEN: "he asked for a 3D floor plan of a twelve by fifteen foot living room. Argon built a room he could spin around, lighting included"
  SURPRISE: 70
  SRC: https://www.instagram.com/reel/DecUb-FKNqA/
  SRC: https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud
  VIA: Renz Sadiwa screen recording, Gemini app header "Argon High", prompt "Build an interactive 3D floor plan ... 12x15 foot space, plus simulating lighting" (ref 2.5-10.9s)
  VIA: Google Cloud post ("spatial reasoning, mathematical precision and visual coding")
  ONE-SOURCE-OK: the claim is the demo itself, shown on screen while it is spoken; Google states the capability class.

- CLAIM: Given an LA electricity-price-by-hour chart, Argon recommended the cheapest hours to run laundry, dishwasher and charging
  TIER: single
  SPOKEN: "a chart of LA electricity prices. It found the cheapest hours to run his laundry"
  SURPRISE: 60
  SRC: https://www.instagram.com/reel/DecUb-FKNqA/
  SRC: https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud
  VIA: Renz Sadiwa screen recording (prompt with electricity-price-by-hour chart; answer "Run your high-energy appliances and charging between 8:00 PM and 10:00 AM") (ref 12.5-18.4s)
  VIA: Google Cloud post ("reads long documents that mix text, tables, charts and images")
  ONE-SOURCE-OK: the demo is shown on screen while it is spoken.

- CLAIM: Given three script PDFs, Argon built a shot list for each
  TIER: single
  SPOKEN: "Then three video scripts. It planned the shots for every one"
  SURPRISE: 55
  SRC: https://www.instagram.com/reel/DecUb-FKNqA/
  SRC: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon
  VIA: Renz Sadiwa screen recording ("These are my next three scripts. Build a shot list for each one", 3 PDFs, table output) (ref 18.5-24.4s)
  VIA: Gemini API model page (PDF input supported)
  ONE-SOURCE-OK: the demo is shown on screen while it is spoken.

## FEATURES + HOW TO USE

- Gemini app + AI Mode for Pro/Ultra — USED
- API paid tier (AI Studio, Android Studio), Antigravity for Ultra — CUT (developer detail; price kept)
- Vulnerability find/validate/patch; Fairwind unguarded version — CUT (v2: demo-led reel per user reference)
- Default cyber mitigations block offensive tasks — CUT (v2)
- 1M context; multimodal in; text out — CUT (v2; PDF + chart input shown in demos)
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
