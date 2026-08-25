# Research — claude-eating-tokens

Claims ledger + search log. Angle researched independently, 2026-08-25.

Three source domains, three distinct VIAs: forbes.com (VIA The Information),
fortune.com (VIA Andrew Macdonald's own remarks on the Rapid Response podcast),
finance.yahoo.com (VIA Moneywise's own reporting). This is REPORTING, not an
Uber disclosure — none of these outlets cites an Uber press release or a
financial filing for the operational figures. Policy applies: attribute once,
early, then state directly, and credit every outlet on screen.

## CLAIMS

- CLAIM: Uber's CTO Praveen Neppalli Naga said he spent $1,200 in a two-hour
  session with Claude Code.
  TIER: multi
  SPOKEN: "twelve hundred dollars in a two-hour coding session"
  SRC: https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-its-2026-ai-budget-in-four-months-on-claude-code/
  VIA: The Information (CTO confirmation), cited by Forbes
  SRC: https://finance.yahoo.com/technology/ai/articles/uber-blew-entire-2026-ai-145000897.html
  VIA: Moneywise (Clay Halton, 2026-07-15), syndicated by Yahoo Finance

- CLAIM: Uber rolled Claude Code out to an engineering org of roughly 5,000.
  TIER: multi
  SPOKEN: "about five thousand engineers"
  SRC: https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-its-2026-ai-budget-in-four-months-on-claude-code/
  VIA: The Information, cited by Forbes
  SRC: https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/
  VIA: Fortune (Jake Angelo, 2026-05-26)

- CLAIM: Claude Code adoption at Uber went from 32% of engineers in February
  2026 to 84% classified as agentic coding users in March 2026.
  TIER: single
  SPOKEN: "thirty-two percent in February to eighty-four in March"
  SRC: https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-its-2026-ai-budget-in-four-months-on-claude-code/
  VIA: The Information, cited by Forbes

- CLAIM: Uber exhausted its full-year 2026 AI budget by April, four months in.
  TIER: multi
  SPOKEN: "The entire 2026 AI budget was gone by April."
  SRC: https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/
  VIA: Fortune's own reporting
  SRC: https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-its-2026-ai-budget-in-four-months-on-claude-code/
  VIA: The Information, cited by Forbes
  SRC: https://finance.yahoo.com/technology/ai/articles/uber-blew-entire-2026-ai-145000897.html
  VIA: Moneywise

- CLAIM: Uber ranked teams/engineers on internal leaderboards by AI tool usage
  volume, which incentivised consumption.
  TIER: multi
  SPOKEN: "ranking its own teams on internal leaderboards by how much AI they used"
  SRC: https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/
  VIA: Fortune's own reporting
  SRC: https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-its-2026-ai-budget-in-four-months-on-claude-code/
  VIA: The Information, cited by Forbes

- CLAIM: Roughly 70% of code committed at Uber originated from AI tools.
  TIER: single
  SPOKEN: "seventy percent of committed code came out of those tools"
  SRC: https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-its-2026-ai-budget-in-four-months-on-claude-code/
  VIA: The Information, cited by Forbes

- CLAIM: Uber president and COO Andrew Macdonald questioned the AI spend,
  saying that without a direct line to shipped features the trade is hard to
  justify.
  TIER: single
  SPOKEN: "if you can't link it to what you're shipping, that trade gets hard to justify"
  SRC: https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/
  VIA: Andrew Macdonald, Rapid Response podcast, quoted by Fortune

## EXCLUDED — checked and deliberately NOT claimed

- The $1,500/month per-tool cap Uber reportedly imposed: the primary report is
  Bloomberg (2026-06-02), which returned HTTP 403 and could not be read. Every
  other page carrying it is an aggregator. Per the sourcing rule, an aggregator
  is never cited — go to the original — so the cap is NOT spoken and NOT shown.
- Kahn v. Anthropic, PBC (N.D. Cal., filed 2026-06-14/15), the Claude Max
  usage-limits class action: real and reported (Qz, PYMNTS via WSJ; Anthropic
  declined to comment). CUT, not disbelieved — it is a second story with its
  own legal-framing burden, and every sentence of it would have to be marked as
  an untested allegation. The reel is about Uber's own incentives.
  The widely repeated "15% of a weekly allowance in one 5-hour session" detail
  traces only to low-tier aggregators; PYMNTS does not carry it. Would have
  needed the docket before it could ever be spoken.
- "$500-$2,000 per engineer per month" as a HEADLINE average: this is wrong and
  is exactly the distortion the search summaries repeat. Forbes gives $150-$250
  as the average engineer and $500-$2,000 for POWER USERS. The reel states no
  per-engineer average at all rather than imply the high band is typical.
- ~11% of live backend updates written by agents with no human oversight
  (Forbes, single) — true but cut for runtime; it opens a safety argument the
  reel does not have time to handle responsibly.
- Uber R&D $951M in Q1 2026, up ~17% YoY (Fortune) — cut; it is total R&D, not
  AI spend, and putting it beside AI figures invites the viewer to conflate them.
- The "roughly $500M single-month Claude invoice" story that surfaced in search:
  traced only to Yahoo/Dallas Express aggregation of an unnamed company. No
  primary source, no named company. NOT claimed.

## SEARCHED

- 2026-08-25  "Claude Code token usage complaints limits August 2026"  (surfaced
  the Uber story, the Kahn suit, and conflicting claims about a temporary
  weekly-limit boost)
- 2026-08-25  "Anthropic Claude weekly usage limits change developers reaction"
  (limit-change timeline; sources disagreed on the boost expiry date - Aug 19 vs
  Aug 31 - so no limit-change claim entered the script)
- 2026-08-25  fetched https://www.theregister.com/2026/01/05/claude_devs_usage_limits/
  (Jan 2026 complaints traced to expiring holiday bonus; not used)
- 2026-08-25  fetched https://explainx.ai/blog/claude-usage-limits-2026-timeline-explained
  (low-tier SEO blog, contradicted the search summary on the boost date; treated
  as unreliable and not used)
- 2026-08-25  "Uber 5000 engineers Claude Code budget per engineer month AI spend"
  (found Forbes, Fortune, Bloomberg, Moneywise)
- 2026-08-25  fetched Forbes 2026-05-17 (adoption timeline, per-engineer bands,
  CTO's $1,200 session, ~70% committed code, leaderboards, source attribution)
- 2026-08-25  fetched https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/
  (COO Macdonald's remarks verbatim, leaderboard confirmation, Q1 R&D figure)
- 2026-08-25  fetched Bloomberg 2026-06-02 -> HTTP 403, unreadable; the $1,500
  cap therefore stays out of the script
- 2026-08-25  fetched https://www.pymnts.com/news/artificial-intelligence/2026/claude-max-customer-sues-anthropic-over-usage-limits/
  (lawsuit basics via WSJ; no case number, no 15% detail, Anthropic declined to
  comment)
- 2026-08-25  fetched Qz lawsuit article -> HTTP 403, unreadable
