# Research — five-free-ai-tools

Claims ledger + search log.

## CLAIMS

- CLAIM: Google AI Studio itself costs nothing, in every region it is offered.
  TIER: official
  SPOKEN: "Google AI Studio is free in every region it's offered: Gemini's models, in a browser."
  SRC: https://ai.google.dev/gemini-api/docs/pricing
  VIA: Google's own pricing page ("Google AI Studio usage is free of charge in all available regions")

- CLAIM: Gemini Notebook's free Standard tier is 50 chats a day and 3 audio overviews a day (the same page also lists 100 notebooks, 50 sources per notebook and 3 video overviews a day — recorded here, not spoken).
  TIER: official
  SPOKEN: "Gemini Notebook, the one you knew as NotebookLM, gives you fifty chats a day and three audio overviews."
  SRC: https://support.google.com/gemininotebook/answer/16213268
  VIA: Google's own Gemini Notebook help page

- CLAIM: Since 2 September 2026 those limits are compute-based and refresh every five hours rather than daily.
  TIER: multi
  SPOKEN: "Since September second, those limits refresh every five hours, not once a day, so a heavy morning doesn't cost the evening."
  SRC: https://blog.google/innovation-and-ai/products/gemini-notebook/new-flexible-usage-limits/
  VIA: Google's own announcement
  SRC: https://www.androidpolice.com/gemini-notebook-ditching-daily-limits-more-complicated/
  VIA: Android Police, reporting the change independently

- CLAIM: ElevenLabs' free plan is 10,000 credits a month covering text to speech, sound effects and music; voice cloning belongs to the paid Starter plan at $6 a month. ("enough for a few voiceovers, not a series" are our judgement of what that buys, deliberately vague: no credits-to-minutes conversion is claimed, because the pricing page states none.)
  TIER: official
  SPOKEN: "ElevenLabs gives you ten thousand credits a month for speech, sound effects and music, enough for a few voiceovers, not a series. Cloning starts at six dollars."
  SRC: https://elevenlabs.io/pricing
  VIA: ElevenLabs' own pricing page

- CLAIM: Suno's free plan is 50 credits a day with no commercial rights; Pro is $8 a month.
  TIER: official
  SPOKEN: "Suno gives fifty credits a day for music, but the free plan carries no commercial rights. Pro is eight."
  SRC: https://suno.com/pricing
  VIA: Suno's own pricing page

- CLAIM: GitHub Copilot Free is 2,000 code completions a month and needs no credit card; Copilot Pro is $10 a month.
  TIER: official
  SPOKEN: "And GitHub Copilot's free plan is two thousand completions a month, no card. Pro is ten."
  SRC: https://docs.github.com/en/copilot/get-started/plans
  VIA: GitHub's own documentation

- CLAIM: Copilot's free terms changed more than once during 2026 — sign-ups paused and limits tightened in April, billing moved to usage-based credits on 1 June, and model choice was cut to auto-only on 24 June.
  TIER: multi
  SPOKEN: "Copilot's changed more than once this year, so look it up first."
  SRC: https://www.heise.de/en/news/GitHub-removes-free-models-from-Copilot-plans-11275252.html
  VIA: heise online, reporting GitHub's announcement
  SRC: https://roboin.io/article/en/2026/06/25/github-copilot-free-and-student-plans-limited-to-auto-model-selection/
  VIA: Roboin, reporting the same announcement independently

## NOT CLAIMED

- That any of these is "the best" tool in its category — the reel ranks nothing, it states what each free tier gives you.
- That the Gemini API free tier is unchanged. It was tightened in 2026 (2.5 Pro removed from the free API tier, Flash request counts cut). The reel's claim is about AI Studio and Gemini Notebook, not the API.
- Any figure for Copilot Free's monthly chat requests. GitHub's own plan pages state the 2,000 completions but not a chat number, so no chat figure is spoken or shown.
- That the free plans are permanent. The close says the opposite.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-16  "best free AI tools September 2026 genuinely free tier no credit card"  (candidate list; all sources were listicle farms, so every pick was then verified on its vendor's own page)
- 2026-09-16  fetched ai.google.dev/gemini-api/docs/pricing  (AI Studio free in all regions; which models are free)
- 2026-09-16  fetched support.google.com/gemininotebook/answer/16213268  (the free Standard numbers)
- 2026-09-16  fetched elevenlabs.io/pricing, suno.com/pricing, docs.github.com/en/copilot/get-started/plans  (free ceilings + first paid price for each)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-16  "Gemini Notebook five hour usage limits users reaction September 2026 hands-on"  (Android Police, heise-class outlets and dev write-ups describing the five-hour reset in use: a morning session that exhausts the limit no longer blocks the evening)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-16  same search as 2  (the repeated user-side point is that compute-based limits are harder to predict than a daily count; the reel does not claim they are better, only what they are)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-16  "free tier removed or reduced 2026 Suno ElevenLabs GitHub Copilot free plan changes limits cut"  (found the strongest counter-evidence: Copilot's free terms moved three times in 2026. The free plan still exists, so the claim stands — and the finding became the reel's closing line rather than being left out.)

INDEPENDENT-CHECK: 2026-09-16 searched for hands-on reporting and free-tier rollbacks. Found independent coverage of the Gemini Notebook change (Android Police and others) and of GitHub's 2026 Copilot changes (heise, Roboin). The per-tool ceilings themselves are what each vendor's own page states; there is no independent test of a price list, which is why those claims are official-tier and single-domain by nature.
