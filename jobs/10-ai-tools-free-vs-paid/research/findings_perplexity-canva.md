# Findings: Perplexity & Canva (free vs paid) — captured 2026-09-18

Note on capture: WebFetch returned HTTP 403 on both perplexity.ai and canva.com
directly (bot-blocked). All quotes below were pulled via the in-session
Browser tool loading the live, rendered official pages — content is genuine
DOM text from the primary URLs, not search snippets. Canva's pricing page
geolocated to India (INR) on first load; the USD figures below are from the
same page after confirming region/toggling billing period, same DOM,
confirmed twice.

## Perplexity

- **FREE tier — search limits.** Official Help Center: "Search history access,
  Practically unlimited basic searches, Very limited amount of Pro Searches
  ... No access to advanced AI models, image generation, or premium support."
  The plan-comparison table on the same page gives the exact number: **"Pro
  Searches — 3/day"** for Free, and **"Research Queries — 1/month"** for Free.
  SRC: https://www.perplexity.ai/help-center/en/articles/11187416-which-perplexity-subscription-plan-is-right-for-you

- **FREE tier — file uploads.** Same page: Free = "Basic file uploads
  (limited)"; the comparison table lists File Uploads (sessions) as
  "Limited" for Free vs. weekly-limit tiers for paid plans.
  SRC: https://www.perplexity.ai/help-center/en/articles/11187416-which-perplexity-subscription-plan-is-right-for-you

- **PRO tier — price.** Official pricing page (perplexity.ai, rendered):
  "$20 /month ... Popular. Better answers. More answers. Built for serious
  work." Bullet list under it: "Expanded Computer access, 4,000 bonus
  credits, Deep research, Access to top AI models, Select between AI models,
  Create polished documents & apps, More usage limits and memory."
  SRC: https://www.perplexity.ai/hub/pricing (renders at perplexity.ai)

- **PRO tier — what it unlocks over Free, in Perplexity's own words.** FAQ on
  the pricing page: "Free includes access to the top AI models with limited
  weekly usage. Pro raises every limit and adds Perplexity Computer, premium
  data sources like PitchBook and Statista, search across the web, files, and
  apps, model council, and the ability to select a preferred model per
  query." Comparison table confirms Pro gets "Access to advanced models,"
  "10x" on web/file/asset-generation limits vs Free, and unlocks Image
  Generation (Free = "No").
  SRC: https://www.perplexity.ai/hub/pricing ; https://www.perplexity.ai/help-center/en/articles/11187416-which-perplexity-subscription-plan-is-right-for-you

- **PRO tier — models named.** FAQ: "Perplexity orchestrates multiple top
  models and selects the best one per query, including ChatGPT, Google
  Gemini, Anthropic Claude, and NVIDIA Nemotron. Pro and Max both allow
  selecting a preferred model."
  SRC: https://www.perplexity.ai/hub/pricing

- **PRO tier — file upload cap, named number.** Help Center: "Up to 50 file
  uploads per project."
  SRC: https://www.perplexity.ai/help-center/en/articles/11187416-which-perplexity-subscription-plan-is-right-for-you

- **MAX tier (context, not free/paid pair but useful contrast).** Pricing
  page: "$200 /month ... Maximum Computer usage, 35,000 bonus credits, 10,000
  monthly credits, Expert level research, Frontier AI models, Highest usage
  limits and memory, Priority access to new features."
  SRC: https://www.perplexity.ai/hub/pricing

- **HEDGE — free-tier Pro Search limit reportedly cut recently, and a Pro
  perk reportedly quietly removed.** Third-party coverage (VIA, NOT
  confirmed on an official Perplexity page in this session): a piece titled
  "Perplexity Pro Slashed Limits: What Paying Users Lost" (dated ~May 2026)
  reports Perplexity tightened limits during 2026, and other aggregator
  write-ups claim "the $5/month API credit for Perplexity Pro subscribers
  was quietly removed in early 2026 without notifying subscribers." The
  official Help Center page fetched above states the CURRENT numbers (3 Pro
  Searches/day free, 4,000 bonus credits/mo Pro) as of 2026-09-18 — treat
  any script line about limits as a current-snapshot claim, not a stable
  one, and do not repeat the "quietly removed $5 credit" claim as fact since
  it wasn't verified on an official page. VIA: freeainews.com aggregator
  search summary, 2026-09-18 search (no direct official perplexity.ai
  confirmation found).

- **Logo / wordmark source (not downloaded, URL only).** Official Perplexity
  Help Center logo assets, both light and dark variants:
  https://mintcdn.com/perplexity-help-center/7GnFipLPzNZrXrL_/help-center/logo/perplexity-logo-dark.png
  https://mintcdn.com/perplexity-help-center/7GnFipLPzNZrXrL_/help-center/logo/perplexity-logo-light.png
  (Served off Perplexity's help-center CDN, referenced directly from
  perplexity.ai's own help pages — no separate brand/press-kit page was
  found; see NOT FOUND below.)

## Canva

- **FREE tier — price and scope.** Official pricing page (canva.com/pricing,
  rendered, USD after region confirmed): "Free — Design anything and bring
  your ideas to life. No cost, just creativity. US$0 /month for one person."
  Feature table: Free gets "4.7+ million" stock photos/graphics/fonts/videos/
  audio and "1.6+ million" templates, vs Pro's "141+ million" assets and
  "3.6+ million" templates. "Customize templates" = "Unavailable" on Free;
  "Design in bulk" = "Unavailable" on Free.
  SRC: https://www.canva.com/pricing/ (renders at canva.com/pricing)

- **FREE tier — AI usage allowance, exact number.** Official Help Center
  article "Understanding your AI usage": "Canva Free and Pro Lite: Up to 20
  uses of Standard AI tools, OR Premium AI tools. No access to Ultra AI
  tools or Affinity's Premium AI tools." Also: "For Canva Free and Pro Lite,
  Standard AI tools still draw from the monthly AI allowance" (unlike paid
  plans, where Standard AI tools such as Magic Write don't count against the
  allowance at all). Reset timing: "If you're on Canva Free, your AI
  allowance resets at 12:00 a.m. UTC on the first of each month."
  SRC: https://www.canva.com/help/ai-access/

- **PRO tier — price, confirmed both billing modes.** Official pricing page,
  toggled live in-session: Yearly billing shows "US$144 /year for one
  person" for Pro; switching the same page to Monthly billing shows "US$18
  /month for one person" for Pro (so annual works out to $12/mo
  equivalent — the page's own "Save from 16%" banner applies to a different
  comparison, not a flat number worth restating without the raw figures).
  Free stays "US$0" in both views. Business plan on the same page: "US$25
  /month per person" (monthly) / "US$250 /year per person" (yearly).
  SRC: https://www.canva.com/pricing/

- **PRO tier — what it unlocks, in Canva's own words.** Pricing page: "Pro —
  Unlock premium content, more powerful design tools, and AI features."
  FAQ: "Canva Pro is perfect for solo creators who want to design like a
  pro, with premium templates, and AI-powered features that make it easy to
  create standout content."
  SRC: https://www.canva.com/pricing/

- **PRO tier — AI usage allowance, exact number, and what changes.** Help
  Center: "Canva Pro/Teams/Nonprofits: Standard AI tools — does not draw
  from AI allowance* for all paid plans. Allowance: up to 200 uses for
  Premium AI tools, OR up to 20 uses for Ultra AI tools." I.e. Pro doesn't
  just raise a number — it moves an entire tool category (Standard AI:
  Magic Write, Translate, Photo/Video Animations, AI Voice) OFF the shared
  allowance entirely, on top of a 10x jump in the Premium-tool allowance
  (20 -> 200) over Free.
  SRC: https://www.canva.com/help/ai-access/

- **Named Magic Studio / AI tools, by tier.** Help Center defines three tool
  tiers with named examples: "AI design tools" (unlimited on paid plans):
  "Canva AI (text), Magic Write, Photo and Video Animations, AI Voice,
  On-device ML tools in Affinity." "Standard AI tools": "Image Upscaler,
  Image generation with Canva AI, Magic Formulas." "Premium AI tools":
  "Magic Layers, Generate a design with Canva AI, Create an image with
  Canva AI, Build interactive experiences with Canva Code, Generate
  elements with Canva AI (shapes, 3D, charts, forms, and more), Music and
  Sound Effect Generator, Form generator, Premium AI tools in Affinity,
  including Generative Fill, Expand, Edit, Generate Images and Vectors."
  "Ultra AI tools": "Conversational design with Canva AI 2.0, Create a video
  clip with Canva AI, Create an image with Canva AI." Also explicit: "Premium
  and Ultra AI tools are available with: Canva Pro, Canva Teams, Canva
  Business, Canva Enterprise, Canva Nonprofit" — i.e. gated behind a paid
  plan, full stop, regardless of allowance.
  SRC: https://www.canva.com/help/ai-access/

- **HEDGE — rebranding away from "Magic Studio" name, and a new regional
  tier, both recent/in-flux.** Third-party coverage (VIA, spot-checked
  against what the live pricing page actually showed): as of a 2026-09-09
  observation, "the term 'Magic Studio' is no longer the primary branding,
  with canva.com/magic serving a page titled Canva AI 2.0, though the
  individual Magic tools remain available" — worth hedging the "Magic
  Studio" name itself in narration (the individual tool names like Magic
  Write / Magic Eraser / Magic Media are still live and named in Canva's own
  Help Center, confirmed above, so those are safe to use verbatim). Separately,
  Canva's OWN pricing page (confirmed live, this session) now shows a
  region-limited "Pro Lite" tier between Free and Pro (seen at INR pricing
  before the page resolved to USD) — third-party coverage says it is
  "currently available in India and Indonesia" and a few other Asian
  markets, not the US, so it should NOT be presented as a global option in
  the free-vs-paid comparison. VIA: search aggregation, 2026-09-18 (Canva
  Help Center article "About Canva Pro Lite" was found by title but not
  fetched directly this session — treat the market list as unconfirmed
  detail; confirmed only that the tier exists and is region-gated).

- **HEDGE — price history, so don't state $18/mo as if it's been stable.**
  Multiple third-party trackers (VIA, not from an official Canva page)
  report Canva Pro rose from $12.99/mo -> $15/mo -> $18/mo across 2025-2026,
  i.e. it has moved within the last ~12 months. The $18/mo figure captured
  above IS the current live price (confirmed directly on canva.com/pricing
  this session), but script language should avoid implying it's a
  long-stable number.

- **Logo / wordmark source (not downloaded, URL only).** Canva's own header
  logo asset, pulled live from canva.com/pricing's rendered DOM:
  https://static.canva.com/web/images/8439b51bb7a19f6e65ce1064bc37c197.svg
  (No separate brand/press-kit page was found; see NOT FOUND below.)

## Looked for and did NOT find

- A dedicated official Perplexity brand/press-kit page with logo download
  assets (searched `site:perplexity.ai` for "press kit" / "brand assets" —
  nothing came back beyond general product pages; used the Help Center's own
  logo image URLs instead, which are genuinely Perplexity-hosted).
- A dedicated official Canva brand/press-kit page (searched `site:canva.com`
  for "logo" / "brand assets" / "press kit" — results were all about
  Canva's in-app Brand Kit FEATURE for end users, not Canva's own corporate
  logo assets; used the live header SVG instead).
- Direct confirmation, on an official Perplexity page, of the "$5/month API
  credit quietly removed" claim — this stayed at VIA/third-party level, not
  independently verified against a Perplexity source in this session.
- Direct fetch of the Canva Help Center "About Canva Pro Lite" article
  (canva.com/help/pro-lite/) — only saw it referenced by title in search
  results; did not open it to confirm the exact country list or price.
- An exact word-for-word "Free = daily search count" figure for Perplexity
  beyond "3/day Pro Searches" and "1/month Research Queries" — Perplexity's
  own copy calls basic (non-Pro) search "practically unlimited" rather than
  giving it a hard number.
