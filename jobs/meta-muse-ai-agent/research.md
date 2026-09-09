# Research — meta-muse-ai-agent

Claims ledger + search log. `script_approval.py propose` refuses
while placeholder angle-bracket fields remain; format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: Meta launched Muse on Sept 8-9, 2026, and its own press release is
  headlined "Introducing Muse: The World's First Personal AI Agent Built
  for Everyone."
  TIER: official
  SPOKEN: "Meta just called its new AI agent the world's first personal AI
  agent."
  SRC: https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
  VIA: Meta's own newsroom — this is Meta's claim about itself, not a
       third-party report.

- CLAIM: Mark Zuckerberg framed Muse, on his own account, as working
  continuously on the user's behalf ("works 24/7 to get things done for
  you").
  TIER: official
  SPOKEN: "Zuckerberg says it'll work 24/7 so you don't have to."
  SRC: https://www.tribuneindia.com/news/ai-agent/works-24-7-to-get-things-done-for-you-says-mark-zuckerberg-as-meta-enters-autonomous-ai-race-with-launch-of-personal-ai-agent-muse
  VIA: Zuckerberg's own post on X, quoted directly by the outlet at launch.

- CLAIM: Muse can autonomously send emails, book travel, fill out and submit
  forms, negotiate/lower bills, sell items, turn saved Instagram recipes into
  grocery lists, and plan a dinner party (menu + invites with dietary notes).
  TIER: official
  SPOKEN: "It emails people, books your flights, and haggles your bill down.
  It'll even turn a recipe you saved off Instagram into a grocery list."
  SRC: https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
  VIA: Meta's own feature list, corroborated independently by:
  https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/
  and https://www.foxbusiness.com/technology/meta-introduces-muse-personal-ai-agent-can-send-emails-book-travel

- CLAIM: Muse runs inside a dedicated "Muse Secure VM" holding the
  credentials for connected services, with a separate "Sentinel" agent
  isolated at the system level that has to approve anything before it
  reaches the internet; Meta says Muse itself has no visibility into
  passwords or payment methods (purchases route through single-use Stripe
  card numbers).
  TIER: official
  SPOKEN: "Muse runs inside its own secure computer, walled off from the
  rest of the internet. And a separate watchdog called Sentinel has to
  approve anything before it leaves that computer. So Meta says Muse never
  even sees your password or your card."
  SRC: https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
  VIA: Meta's own architecture claim, corroborated by
  https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/
  and https://siliconangle.com/2026/09/08/meta-debuts-its-secure-by-design-personal-ai-agent-muse/
  (both outlets flag that the claim itself "will require deeper investigation
  by security experts" — independent verification does not yet exist)

- CLAIM: Personal/agentic AI agents that act across apps and the web already
  shipped before Muse: Google's Project Mariner, OpenAI's Operator/ChatGPT
  Agent (now ChatGPT Work), Amazon's Nova Act, and Anthropic's Computer Use
  — so "world's first" is a marketing framing, not a factual first.
  TIER: multi
  SPOKEN: "Muse isn't the first personal AI agent. Four other companies
  already shipped agents like this before Meta did: Google, OpenAI, Amazon
  and Anthropic."
  SRC: https://the-decoder.com/google-and-meta-race-to-build-personal-ai-agents-as-anthropic-and-openai-pull-further-ahead/
  VIA: The Decoder's own reporting on the competitive AI-agent landscape
  SRC: https://www.pymnts.com/news/artificial-intelligence/2026/big-tech-personal-ai-agents-are-coming-to-do-list/
  VIA: PYMNTS' own reporting, independently arriving at the same roster of
       shipped agents (Mariner, Operator/ChatGPT Work, Nova Act) — also
       corroborated by TechCrunch's own framing of Muse entering "the AI
       agent wars"
       (https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/)

- CLAIM: Meta was fined $5 billion by the FTC in 2019 over privacy
  violations, and the FTC separately charged Meta in 2023 with violating
  that same order — the track record critics cite when asking whether to
  trust Muse with financial and health data.
  TIER: multi
  SPOKEN: "the FTC once fined this same company five billion dollars over
  how it handled people's data."
  SRC: https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/
  VIA: TechCrunch's own Muse trust-skepticism reporting, citing the
       settlement as context
  SRC: https://www.ftc.gov/news-events/news/press-releases/2019/07/ftc-imposes-5-billion-penalty-sweeping-new-privacy-restrictions-facebook
  VIA: the FTC's own primary press release announcing the penalty — the
       regulator, not a news outlet describing it

- CLAIM: Muse launched in the US only (more countries not yet announced),
  on iOS, Android and the web at muse.ai, with a free tier plus two paid
  tiers ($20/month and $100/month); support for Meta's AI glasses is
  "coming soon" with no date given.
  TIER: official
  SPOKEN: "Muse launches in the US only, on the phone or the web, free to
  start. Want more? That's $20 or $100 a month."
  SRC: https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
  VIA: corroborated by https://www.axios.com/2026/09/08/meta-debuts-muse-personal-ai-agent
  and https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/

## NOT USED (deliberately)

- Forkast News reports internal testing found ways around Muse's guardrails
  ("struggled with guardrail bypasses," a photo-exposure incident). SINGLE
  source, could not corroborate elsewhere, and the outlet's own framing
  leans on unverified "internal posts." Too disputed to spend one of ~190
  words on inside a 70s script — see structure.md WHAT WAS CUT.
- "Muse Image" (Meta's separate AI image generator, opt-out consent
  backlash, July 2026) — a DIFFERENT product that happens to share the Muse
  name. Not this launch; excluded to avoid conflating two stories.
- Muse Spark (Meta's foundation-model family the agent runs on, launched
  April 2026) and its own unrelated controversies (a disclosed third-party
  testing misconfiguration, a contributor-tier consent story) — model
  backstory, not the consumer product being reported here. Out of scope.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-09  "Meta Muse AI agent official announcement"  (found Meta's own
  Sept 8 2026 press release at about.fb.com, headlined "the world's first
  personal AI agent"; pricing, architecture and availability confirmed)
- 2026-09-09  "Meta Muse Zuckerberg quote personal AI agent"  (confirmed
  Zuckerberg's own framing: "works 24/7 to get things done for you",
  posted on X, consistent with the "personal agent for everyone" pitch)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is
###    not the vendor
- 2026-09-09  "Meta Muse hands-on review tested app"  (found the consumer
  Muse agent was still gated behind a waitlist/invite at several outlets'
  time of writing — no independent hands-on test of the CONSUMER agent
  itself exists yet; unrelated hands-on tests exist for Muse Spark and
  Muse Code, which are different products under the same model family)
- INDEPENDENT-CHECK: 2026-09-09 — searched for a non-Meta hands-on test of
  the Muse personal agent specifically — found none. Every detailed
  capability description traces back to Meta's own press materials,
  echoed by launch-day press. This is disclosed above (all capability
  claims tiered "official") rather than presented as independently
  verified.

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-09  "Meta Muse reddit reaction users think"  (no substantive
  public user reaction yet — launch is less than 24h old at research time,
  US-only, and rollout is gradual; nothing found worth citing as "what
  users say" — script does not claim otherwise)
- 2026-09-09  "Meta Muse privacy criticism experts reaction"  (found EFF's
  Thorin Klosowski and Privacy International commentary — but that
  commentary is about the SEPARATE "Muse Image" opt-out feature from July
  2026, not this agent launch; excluded per NOT USED above to avoid
  misattributing a different controversy to this product)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were
###    trying to prove the story wrong
- 2026-09-09  "ChatGPT Agent Google Project Mariner Amazon personal AI
  agent before Muse"  (this is the search that undercuts the hook: found
  Google's Project Mariner, OpenAI's Operator/ChatGPT Work, Amazon's Nova
  Act and Anthropic's Computer Use all shipped agentic, cross-app AI
  agents before Muse — confirming "world's first" does not hold up
  literally, which is the spine of this script rather than a fact being
  hidden from it)
- 2026-09-09  "Meta Muse hands-on review tested app" / androidauthority
  trust piece  (searched for evidence the security design fails in
  practice — found only "will require deeper investigation" framing from
  TechCrunch/SiliconANGLE and one single-source, uncorroborated Forkast
  report; neither rises to a claim this script states as fact)
