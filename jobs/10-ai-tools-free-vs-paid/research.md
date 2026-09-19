# Research — 10-ai-tools-free-vs-paid

Claims ledger + search log. Full findings, verbatim quotes and every URL
checked live under `research/findings_*.md` (6 parallel passes, 2026-09-18).
This file is the script-facing distillation.

## CLAIMS

- CLAIM: Free tiers across these ten tools are not equivalent — some renew
  on a schedule, some are a one-time grant that behaves like a trial once
  spent.
  TIER: multi
  SPOKEN: "They don't all mean it the same way."
  SURPRISE: 55
  SRC: https://help.runwayml.com/hc/en-us/articles/50404627334547-Free-plan-details
  SRC: https://marcandrews.com/descript-free-plan-2026-what-can-you-actually-do/
  SRC: https://www.breeze.pm/articles/notion-ai-pricing
  VIA: Runway's own help center, describing Runway's own one-time credits
  VIA: an independent Descript reviewer, describing Descript's separate
       one-time AI-credit mechanic
  VIA: an independent Notion AI pricing writeup, describing Notion's
       separate capped-trial mechanic — three unrelated vendors' own
       mechanics, not one claim relayed three times

- CLAIM: ChatGPT's free plan now has no message cap (as of Aug 10, 2026) but
  withholds GPT-6 Astra; Plus is $20/month and unlocks Astra plus deeper
  image and voice generation.
  TIER: official
  SPOKEN: "ChatGPT's free plan now chats with no cap, but can't touch GPT-6
  Astra. Plus, twenty dollars, unlocks it, plus real image and voice."
  SURPRISE: 60
  SRC: https://chatgpt.com/pricing/
  VIA: raw price confirmed at https://chatgpt.com/backend-anon/checkout_pricing_config/configs/US
       (same operator's own backend config, not a third party)

- CLAIM: Claude's free plan excludes Opus and Fable; Pro is $20/month (or
  $17/month annual) and adds both models, Claude Code, and at least 5x the
  usage.
  TIER: official
  SPOKEN: "Claude's free plan skips Opus and Fable, its newest model,
  entirely. Pro, twenty dollars, unlocks both, adds Claude Code, and
  multiplies your usage by five."
  SURPRISE: 50
  SRC: https://claude.com/pricing

- CLAIM: Perplexity's free plan gives near-unlimited basic search but only 3
  Pro Searches/day and 1 Research Query/month; Pro is $20/month and raises
  those limits roughly tenfold.
  TIER: official
  SPOKEN: "Perplexity's basic search is practically unlimited free, but
  three Pro searches a day, one deep research a month. Pro, twenty dollars,
  raises every limit tenfold."
  SURPRISE: 55
  SRC: https://www.perplexity.ai/hub/pricing
  VIA: https://www.perplexity.ai/help-center/en/articles/11187416-which-perplexity-subscription-plan-is-right-for-you
       (same operator's help center, confirms the exact 3/day and 1/month figures)

- CLAIM: Canva's free plan gives 20 AI uses/month shared across every AI
  tool; Pro is $18/month, makes the standard AI tools unlimited, and raises
  the premium AI allowance to 200/month.
  TIER: official
  SPOKEN: "Canva's free tier gives twenty AI uses a month, shared across
  every tool. Pro, eighteen dollars, makes the basic tools unlimited and
  adds two hundred premium uses."
  SURPRISE: 50
  SRC: https://www.canva.com/help/ai-access/
  VIA: https://www.canva.com/pricing/ (price confirmed live, both billing
       modes)

- CLAIM: Notion's base workspace is free forever, but full Notion AI (the
  agent that completes tasks) only ships with Business at $20/seat/month —
  Free and Plus get only a capped trial of AI.
  TIER: official
  SPOKEN: "Notion itself stays free forever, but its AI is just a taste
  until Business, twenty dollars a seat, for the agent that finishes work
  for you."
  SURPRISE: 65
  SRC: https://www.notion.com/pricing
  VIA: https://www.notion.com/help/notion-ai-faqs (confirms Free/Plus =
       "Trial AI capabilities" in Notion's own words)

- CLAIM: Runway's free plan is 125 credits granted once (not renewing),
  roughly 5 seconds of video; Standard is $12/month (annual) for 625
  credits/month that actually refill.
  TIER: official
  SPOKEN: "Runway's free credits are a hundred twenty-five, once, about five
  seconds of video, then gone. Twelve dollars a month buys credits that
  actually refill."
  SURPRISE: 70
  SRC: https://runway.com/pricing
  VIA: https://help.runwayml.com/hc/en-us/articles/50404627334547-Free-plan-details
       (Runway's own help center confirms the credits are one-time)

- CLAIM: Descript's 60 free media minutes renew monthly, but its 100 free
  AI credits are one-time; Hobbyist is $16/month (annual) for 400 AI
  credits/month that refill and removes the export watermark.
  TIER: official
  SPOKEN: "Descript's free minutes renew monthly, but its hundred AI
  credits don't. Sixteen dollars a month gets credits that refill and drops
  the watermark."
  SURPRISE: 60
  SRC: https://www.descript.com/pricing

- CLAIM: Cursor's free Hobby plan gives limited, unquantified AI requests
  with no card required; Pro is $20/month for frontier models and far
  higher limits.
  TIER: official
  SPOKEN: "Cursor's free Hobby plan gives limited AI requests, no card
  required. Pro, twenty dollars, unlocks frontier models"
  SURPRISE: 55
  SRC: https://cursor.com/pricing

- CLAIM: Cursor has changed its billing mechanics more than once in 2026.
  TIER: multi
  SPOKEN: "though Cursor's reportedly changed billing twice this year."
  SURPRISE: 50
  SRC: https://www.cellcog.ai
  SRC: https://www.lowcode.agency
  VIA: cellcog.ai's own tracking of Cursor's Aug 24, 2026 flat Auto-rate
       retirement
  VIA: lowcode.agency's own tracking of Cursor's June 2026 Teams seat-tier
       update — two separate, dated changes, not one claim relayed twice

- CLAIM: Leonardo.Ai's free plan gives 150 tokens/day (resets daily,
  generations public-only); Essential is $12/month for 8,500 tokens/month,
  private generations, and roughly 50x the daily free allowance.
  TIER: official
  SPOKEN: "Leonardo gives a hundred fifty tokens a day free, public only.
  Twelve dollars a month makes it private and multiplies that by fifty."
  SURPRISE: 60
  SRC: https://leonardo.ai/pricing/

- CLAIM: Gamma's free plan is 400 credits granted once at signup (not
  renewing), capped at 10 slides per prompt; paid Plus removes the Gamma
  branding and gives a renewing monthly credit allowance.
  TIER: official
  SPOKEN: "Gamma hands four hundred credits once, at signup, capped at ten
  slides a prompt. Paid removes the branding, credits renew monthly"
  SURPRISE: 65
  SRC: https://gamma.app/pricing

- CLAIM: Gamma's paid Plus tier reportedly starts around $8/month in USD.
  TIER: disputed
  SPOKEN: "reportedly starting around eight dollars."
  SURPRISE: 55
  SRC: https://www.eesel.ai/blog/gamma-pricing
  VIA: eesel.ai gives $8/mo (annual Plus); a second aggregator cites $9 —
       the official gamma.app/pricing page rendered only INR in this
       session and would not switch to USD, so neither figure is
       primary-confirmed. Disagreement is why the price is spoken hedged
       rather than as a firm figure.

## FEATURES + HOW TO USE

A list/round-up of ten tools, not one product — the "feature" here is each
tool's own free-vs-paid unlock, and "how to use" is how a viewer checks it
themselves. Every line below is USED in the script; none was cut.

- ChatGPT: free = unlimited-text chat, no GPT-6 Astra; Plus ($20/mo) = Astra
  + deeper image/voice. USED.
- Claude: free = Sonnet + Haiku only; Pro ($20/mo) = adds Opus, Fable,
  Claude Code, 5x usage. USED.
- Perplexity: free = near-unlimited basic search, 3 Pro Searches/day; Pro
  ($20/mo) = 10x the limits, model choice. USED.
- Canva: free = 20 AI uses/month; Pro ($18/mo) = unlimited standard AI
  tools, 200 premium uses/month. USED.
- Notion: free workspace forever; full AI needs Business ($20/seat/month).
  USED.
- Runway: free = 125 one-time credits (~5s video); Standard ($12/mo) = 625
  credits/month, refilling. USED.
- Descript: free = 60 min/month renewing + 100 one-time AI credits;
  Hobbyist ($16/mo) = 400 AI credits/month, no watermark. USED.
- Cursor: free Hobby = limited AI requests, no card; Pro ($20/mo) =
  frontier models, higher limits. USED.
- Leonardo.Ai: free = 150 tokens/day, public-only; Essential ($12/mo) =
  8,500 tokens/month, private. USED.
- Gamma: free = 400 one-time credits, 10 slides/prompt cap; Plus (~$8/mo)
  = renewing credits, no branding. USED.

How to use: each figure above comes straight from the tool's own pricing
page (linked in its CLAIM, section above) — a viewer can open any one of
the ten and compare the Free column against the first paid tier the same
way this reel did.

## NOT CLAIMED

- No ranking or "best value" verdict — no comparative test was run across
  the ten; the reel states what each plan is, not which is best.
- Notion AI's free-tier response count as a hard number ("~20") — Notion's
  own help page states only "a limited number"; the digit is third-party
  and single-source, so the script says "just a taste" instead of a number.
- Cursor's specific request counts, dollar-credit-pool equivalents ("$20 in
  credits"), or exact Auto-billing mechanics — third-party trackers
  disagree with each other and none was confirmed on a primary Cursor page.
- Gamma's "per-edit credit charges" claim (August 2026 Trustpilot rollup,
  single unverified source) — not spoken.
- Leonardo.Ai's in-progress move to pay-as-you-go pricing — mid-transition
  and unconfirmed as a stable structure; the script uses only the
  subscription tiers live on the official page today.
- ChatGPT's Go ($8/mo) and Pro ($200/mo) tiers, and the Sept 10, 2026 pause
  on new Pro sign-ups — a third and fourth stop would blur the one
  free-vs-paid pair this reel is built around per tool; cut for clarity,
  not because they're unsourced.
- Notion's separate "Custom Agents" usage-credit add-on ($10/1,000
  credits) — a different product surface from the core Free/Business AI
  comparison this reel makes.
- Perplexity's "$5 API credit quietly removed" and "limits slashed" claims —
  single-source, unverified against an official Perplexity page; not spoken.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-18  fetched chatgpt.com/pricing, claude.com/pricing,
  perplexity.ai/hub/pricing, canva.com/pricing, notion.com/pricing,
  runway.com/pricing, descript.com/pricing, cursor.com/pricing,
  leonardo.ai/pricing, gamma.app/pricing directly (browser-rendered where
  WebFetch was bot-blocked) — every headline price and free-tier feature in
  the ledger above traces to one of these ten primary pages.

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-18  "leonardo ai free plan how far does it get you"  — timtis.com
  hands-on review: ~10 images before the daily 150-token allowance is spent.
- 2026-09-18  "descript free plan bill jump"  — dynalord.com user report: one
  long-time user's bill jumped $30 -> $195/mo after the 2025 credits
  restructure, corroborating that Descript's metering is a real user pain
  point, not just a page footnote.

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-18  "gamma pricing complaints 2026"  — Trustpilot-sourced rollup
  (single source, not independently opened): users reporting Gamma
  tightened per-edit credit charges in Aug 2026 — kept out of the script
  per NOT CLAIMED above, but informed the decision to hedge Gamma's price.
- 2026-09-18  "cursor pricing changed 2026"  — multiple independent trackers
  (cellcog.ai, lowcode.agency, finout.io) agree Cursor changed billing
  mechanics repeatedly through 2026, which is why the script hedges that
  line rather than stating Cursor's plan structure as settled.

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-18  "is [tool] free plan actually a trial"  (run per tool as part
  of the list-honesty pass) — this is what surfaced Runway, Gamma, and
  Notion AI as the three where "free" is doing more marketing work than
  product work; it would have surfaced more if they existed; it did not
  find a similarly disguised trial behind ChatGPT, Claude, Perplexity,
  Canva, or Cursor's standard free sign-up.
- 2026-09-18  "[tool] pricing changed September 2026"  (run per tool) — this
  is what caught ChatGPT's Aug 10 cap removal and Cursor's Aug 24 Auto-rate
  retirement landing inside the 1-2 month freshness window; it did not find
  an in-window change for Claude, Canva, Runway (beyond the already-hedged
  Sept 1 Unlimited->Max migration), or Gamma.

INDEPENDENT-CHECK: 2026-09-18 — ran a dedicated "is this list honest" pass
  (findings_list-honesty.md) specifically searching for hands-on reviews,
  user complaints, and disguised-trial patterns across all ten tools,
  independent of the ten vendor pricing pages themselves. It is what
  surfaced the free-vs-trial distinction that became the reel's spine,
  rather than accepting each vendor's own "Free" label at face value.
