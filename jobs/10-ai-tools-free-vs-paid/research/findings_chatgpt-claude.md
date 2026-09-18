# Findings — ChatGPT (OpenAI) + Claude (Anthropic)

Subtopic 1 of `research/plan.md`. All figures fetched live 2026-09-18 (US
locale). ChatGPT's public pricing page and OpenAI help-center were unreachable
via WebFetch (403 Forbidden — Cloudflare bot block); the numbers below come
either from the browser tool driving the real page (primary, same content a
viewer sees) or from OpenAI's own backend pricing-config JSON that the page
itself loads (also primary — not a third-party repeat).

## ChatGPT (OpenAI)

- **Source (pricing/plans):** https://chatgpt.com/pricing/ (redirects from
  `openai.com/chatgpt/pricing/`; same operator, primary). Fetched via browser
  render, US locale confirmed via backend config (see below).
- **Source (raw USD pricing, primary API the page itself calls):**
  `https://chatgpt.com/backend-anon/checkout_pricing_config/configs/US`
  — returned JSON, quoted verbatim:
  `"free":{"month":{"amount":0.0}}`, `"go":{"month":{"amount":8.0}}`,
  `"plus":{"month":{"amount":20.0},"year":{"amount":16.67}}`,
  `"pro":{"month":{"amount":200.0}}`, `"prolite":{"month":{"amount":100.0}}`
  (a second, lower Pro-branded tier — see hedge below).

**FREE tier — what it includes (from the pricing page's own feature grid,
`Plan: Free, Feature: X, value` rows read from the live DOM):**
- Model: "Unlimited text chats with GPT-5.6 Luna" (the free-tier default
  model — page copy, "Get Free" card).
- "Everyday text chats" = `Unlimited*` (footnote: "*Usage must be reasonable
  and comply with our policies").
- GPT Instant total context window: **27K** (row: "Plan: Free, Feature: GPT
  Instant total context window, 27K"). Input maximum for that window is
  described on-page as "~12 pages of text" (shared footnote across plans).
- GPT Reasoning context window: listed as "Varies" (no fixed number given for
  any plan).
- File uploads: **Limited** ("Plan: Free, Feature: File uploads, Limited").
- Voice: **Yes** but capped — page copy "Limited voice chats"; feature-grid
  row says `Plan: Free, Feature: Voice, Yes` (so voice exists free, just
  rate-limited — no exact cap number published).
- Voice **with video**: **No** (`Plan: Free, Feature: Voice with video, No`).
- Image generation: **Limited** ("Limited and slower image generation";
  grid row `Plan: Free, Feature: Image generation, Limited"); "Image
  generation with Thinking": **No**.
- Memory / memory with past chats: **Limited** on both rows.
- Deep research: page copy "Limited deep research" (no number given).
- Advanced/reasoning models (GPT-6 Astra): **No** on Free
  (`Plan: Free, Feature: GPT-6 Astra, No`).
- Projects: grid shows **Yes** for Free too (`Plan: Free, Feature: Projects,
  Yes`) — note this contradicts the older "Plus unlocks Projects" framing;
  the current page's summary card copy for Plus still lists "Projects,
  scheduled tasks, and custom GPTs" as a Plus-tier line, so Free's Projects
  access is likely capped/limited even though the comparison-grid cell just
  says "Yes" with no asterisk breakdown — flag this as ambiguous, don't
  state a hard free/paid line on Projects without hedging.
- Codex access: "Limited Codex access" (Free card copy).
- "ChatGPT Work" on desktop: "Limited ... access" (Free card copy).

**PAID tier (Plus) — price and what it adds over Free:**
- **$20.00/month billed monthly, $16.67/month billed annually** (from the
  backend pricing config: `"plus":{"month":{"amount":20.0},"year":{"amount":
  16.67}}` — annual works out to $200/yr).
- Unlocks per the page: "Advanced reasoning models with GPT-6 Astra and
  GPT-5.6" (grid confirms `Plan: Plus, Feature: GPT-6 Astra, Yes`), expanded
  messages/uploads, "more complex and accurate image creation" + Image
  generation with Thinking (`Yes` vs `No` on Free), expanded deep research,
  expanded memory/context (GPT Instant context window row: Plus = **54K**
  vs Free's **27K**), "Projects, scheduled tasks, and custom GPTs", expanded
  Codex usage, expanded ChatGPT Work access, early access to new features.
- Voice with video: unlocked on Plus (`Yes`, vs `No` on Free).

**Also on the pricing page (not the free/Plus binary, but relevant context
for the reel and for the honesty pass in subtopic 6):**
- **Go** tier exists between Free and Plus: **$8.00/month**
  (`"go":{"month":{"amount":8.0}}`), "10x more messages, file uploads and
  image creation than the free tier" per third-party coverage of OpenAI's
  own announcement (see hedge below — not quoted from the pricing page
  itself, flagging as VIA).
- **Pro** tier: **$200.00/month** (`"pro":{"month":{"amount":200.0}}`),
  "5x more usage" than Plus, GPT-6 Astra "Pro reasoning", unlimited/faster
  image generation, maximum deep research/memory/Codex. GPT Instant context
  window row: Pro = **128K**.
- A second, separate **$100/month "prolite" tier** also exists in the same
  backend config (`"prolite":{"month":{"amount":100.0}}`) — third-party
  coverage (aipricing.guru, glbgpt.com) describes this as a second "Pro"
  tier alongside the $200 one. Not fully documented on the public pricing
  page's four visible cards; treat this as unconfirmed extra detail, not a
  script-ready fact.

**RECENT CHANGE — HEDGE THIS IN THE SCRIPT:**
- As of **2026-09-10** (8 days before this research), OpenAI **paused new
  sign-ups and upgrades to the $200 ChatGPT Pro plan** worldwide, citing
  capacity strain from GPT-6 Astra demand. Existing Pro subscribers keep
  access; Free/Go/Plus/Business/Enterprise sign-ups are unaffected. No
  reopen date announced as of 2026-09-18.
  - SRC: https://www.cio.com/article/4221092/openai-pauses-200-pro-tier-as-astra-demand-strains-capacity.html
  - SRC: https://fortune.com/2026/09/11/openai-astra-chatgpt-pro-pause/
  - Both are secondary reporting (VIA), not an OpenAI first-party post found
    in this search pass — treat the pause itself as reported-not-confirmed-
    on-openai.com, but corroborated by two independent outlets dated 9/11.
  - Because Pro is $200 (not the Free-vs-Plus comparison the script likely
    leads with), this mainly matters if the script mentions Pro at all —
    if it does, say "as of publishing" rather than stating availability as
    a flat fact.
- GPT-6 Astra itself (the flagship model gating Plus/Pro) also reads as a
  very recent release (the capacity-pause story is framing it as new,
  high-demand). Don't hard-code "GPT-6 Astra is the current top model" as a
  timeless fact — say "as of Sept 2026."

**Logo/wordmark source (for a visual asset later — not downloaded):**
- https://openai.com/brand/ — OpenAI's own "Design Guidelines" page with
  downloadable wordmark/logo assets ("Logo & Wordmark... crafted with OpenAI
  Sans, the 'O' formed as a perfect circle").

**Looked for and did NOT find:**
- An exact free-tier message-per-day or per-5-hour-window number stated on
  OpenAI's own pricing/help pages in this pass (help.openai.com articles
  returned 403 via WebFetch and were not reachable via the browser tool in
  this session — only third-party aggregators quoted a "10 messages per 5
  hours" figure, which is VIA and NOT verified against an OpenAI primary
  page here; do not put that number in the script without a fresh check).
- A stated numeric cap for "Limited voice chats" or "Limited deep research"
  on Free — the page uses the word "Limited" with no number in the grid.
- Confirmation of whether Free-tier "Projects" access (grid says "Yes") is
  capped in count the way Claude's Free "Up to 5" is — the page doesn't
  give a number for ChatGPT Free's Projects limit.

---

## Claude (Anthropic)

- **Source:** https://claude.com/pricing — fetched directly via browser
  render (loaded fine, no block). Primary source, US pricing (no region
  switch found necessary; page did not show localized currency the way
  ChatGPT's did).

**FREE tier — what it includes (quoted from the page's feature comparison
table, `Free` column):**
- Price: **$0** ("Free for everyone").
- Card copy: "Chat on web, desktop, and mobile", "Search the web, create
  files, and run code", "Memory across conversations", "Connect your apps
  and tools", "Create Artifacts".
- Models: **Sonnet — Yes, Haiku — Yes, Opus — No, Fable — No** (comparison
  table rows: "Opus / No / Yes / Yes / Yes" and "Fable / No / Yes (50% of
  weekly limits*) / ..." across Free/Pro/Max5x/Max20x).
- Context window: **"Up to 1M varies by model"** (same row text appears for
  every plan tier — the ceiling is not Free-exclusive-limited on paper, but
  it's gated by which model you can reach, since Opus/Fable — the models
  likelier to carry the largest windows — are Pro+ only).
- Projects: **"Up to 5"** on Free (table row: "Projects / Up to 5 / Yes /
  Yes / Yes" — Pro+ = unlimited/uncapped, shown just as "Yes").
- Usage credits (pay-as-you-go top-up beyond plan limits): **No** on Free
  (table: "Usage credits / No / Yes / Yes / Yes").
- Voice mode: **Yes** on Free (table row all "Yes").
- Incognito chats: **Yes** on Free.
- Research (Anthropic's deep-research feature): **No** on Free (table:
  "Research / No / Yes / Yes / Yes").
- Claude Code, Claude Design/Slides/Docs, Claude Science, Claude in Chrome,
  Claude for Microsoft 365/Outlook: all **No** on Free, all **Yes** starting
  at Pro.
- Usage limits: no fixed message count published. FAQ text, quoted
  verbatim: "Every plan has usage limits that reset on a rolling five-hour
  session window... Free covers everyday questions."

**PAID tier (Pro) — price and what it adds over Free:**
- **$17/month billed annually ($200 billed up front), $20/month billed
  monthly** — quoted verbatim from the page: "$17 / Per month with annual
  subscription discount ($200 billed up front). $20 if billed monthly."
- Unlocks per the card: "More usage*", "Hand off and schedule tasks",
  "Claude Design, Slides, Docs", "Claude Code", "Claude Science",
  "Projects" (uncapped), "More Claude models" (Opus + Fable), "Claude in
  Chrome and Microsoft 365".
- FAQ, quoted verbatim: "Pro gives you at least 5x more usage per 5-hour
  session than Free."
- Fable specifically: Pro gets "Usage credits" gating it at **"50% of
  weekly limits*"** per the table cell — i.e., even on Pro, Fable access is
  itself rationed to half the weekly allowance, not full/unlimited. Worth a
  precise phrasing in the script rather than "Pro = full access to every
  model."

**Also on the page (context, not part of the free/Pro binary):**
- **Max** plan: **"From $100/month"**, 5x or 20x Pro's usage, billed
  monthly only. Not the free-vs-paid pair this reel is comparing, but
  useful if the script needs a "how much further can you go" beat.
- Enterprise: "$20 per seat per month plus usage billed at API rates"
  (FAQ, quoted verbatim) — separate business plan, not relevant to an
  individual free-vs-paid comparison.

**RECENT CHANGE check:**
- No evidence found of a Claude Free/Pro price or limit change in the last
  1-2 months. Multiple third-party trackers (eesel.ai, intuitionlabs.ai,
  ssdnodes.com, usagebox.com — all VIA, not primary) independently describe
  the same $17/$20 split as stable "throughout 2026," and the page itself
  carries no "new" or "updated" badge near pricing. Treat $17/$20 as the
  current, not-recently-changed figure — no hedge needed on the price
  itself. (The Fable model being gated behind Pro-with-credits is plausibly
  newer than the rest of the plan structure, since Fable doesn't appear in
  this repo's own model list until now, but no explicit "Fable launched on
  X date" primary source was checked in this pass — flag as unconfirmed
  timing, not a firm recency claim.)

**Logo/wordmark source (for a visual asset later — not downloaded):**
- Anthropic's own newsroom/press kit is the right primary source but was
  not directly opened in this pass (search-only). Best link found via
  search, third-party aggregator only: https://brandfolder.com/anthropic/
  is described as hosting Anthropic's official brand assets, but this was
  NOT verified by opening it — before using a logo asset, open
  https://www.anthropic.com/newsroom (or claude.com's own footer/press
  link) directly and confirm it's Anthropic's own hosted kit, not a
  third-party mirror.

**Looked for and did NOT find:**
- Any exact numeric daily/hourly message cap for Claude Free (Anthropic
  states only that limits are usage-based and reset every 5 hours — no
  published message count, same pattern as ChatGPT).
- A verified, first-party Anthropic brand/press asset URL (only got there
  via a third-party aggregator in search results — needs a direct visit
  before use).
