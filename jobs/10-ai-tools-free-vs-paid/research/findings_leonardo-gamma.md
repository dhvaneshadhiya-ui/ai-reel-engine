# Findings: Leonardo.Ai and Gamma — free vs paid (as of 2026-09-18)

## Leonardo.Ai

- **Official pricing page fetched directly** (browser render, not a search snippet):
  SRC: https://leonardo.ai/pricing/ (page title "Leonardo.Ai Pricing: Individual, Team & API Plans | Leonardo.Ai")
- **FREE tier — exact limits (verbatim from page):**
  "FREE / \$0 /month / ex. tax. / Perfect for casual creators who want to explore AI art /
  Fast Tokens 150 / day / Token Bank 150 / Creations access Public / Presets ✓ /
  Quality settings Basic / Personal collections 1"
  — i.e. 150 "Fast Tokens" per day (bank caps at 150, no rollover accumulation beyond that),
  generations are PUBLIC (not private), only "Basic" quality settings, and only 1 personal
  collection.
  SRC: https://leonardo.ai/pricing/
- **PAID tiers — exact prices and what each unlocks over Free (verbatim from page):**
  - ESSENTIAL: "\$12 /month ex. tax. — Best for daily hobbyists and enthusiasts — Fast Tokens
    8,500 / month — Token Bank 25,500 — Creations access Private️ — Quality settings Enhanced —
    Personal collections Unlimited️ — Personal AI models 10 — Max Simultaneous Generations 2 —
    Top-up Tokens ✓"
  - PREMIUM: "\$30 /month ex. tax. — Fast Tokens 25,000 / month — Token Bank 75,000 — Personal AI
    models 20 — Max Simultaneous Generations 3 — Max generations queue 10 — Image Generation for
    select models at a relaxed pace* Unlimited"
  - ULTIMATE: "\$60 /month ex. tax. — Fast Tokens 60,000 / month — Token Bank 180,000 — Personal
    AI models 50 — Max Simultaneous Generations 6 — Max generations queue 20 — Image Generation
    ... Unlimited️ — Video Generation for select models at a relaxed pace* Unlimited️"
  - Over Free, every paid tier unlocks: **private generations** (free is public-only), **Enhanced
    quality settings** (vs Basic), **unlimited personal collections** (vs 1), **personal AI model
    training slots** (10/20/50 — free tier gets none listed), and **top-up token purchases**.
  - Premium+ add "unlimited relaxed-pace" generation on select models (Lucid Origin, Lucid
    Realism, Phoenix 1.0/0.9, Motion 1.0/2.0/2.0 Fast, Hailuo 2.3/2.3 Fast, Wan 2.6 — per the
    page's own footnote asterisk).
  SRC: https://leonardo.ai/pricing/
- **Team plans exist too** (STARTER \$72/mo or \$24/seat, GROWTH \$144/mo or \$48/seat) but are out
  of scope for an individual free-vs-paid comparison — noting only that they exist in case the
  script needs "team" framing.
  SRC: https://leonardo.ai/pricing/
- **Recency flag — HEDGE THIS:** Third-party trackers (not official) describe Leonardo's current
  Solo/Team/API structure as a 2026 consolidation of what used to be separate image/video plans
  into one token currency covering "image, video, design, and motion." I could not find an
  official Leonardo changelog page confirming an exact date for this change within the last 1-2
  months, so treat the CURRENT structure (confirmed live on the pricing page today) as accurate,
  but do not claim on-screen that it "just changed" without further digging — I found only
  secondary claims of an update, not a dated official announcement.
  VIA (secondary, not verified against an official changelog): eesel.ai
  (https://www.eesel.ai/blog/leonardo-ai-pricing) and flowith.io
  (https://flowith.io/blog/leonardo-ai-pricing-2026-free-vs-apprentice-vs-artisan/), both
  describing a "Solo (Free/Essential/Premium/Ultimate)" naming/consolidation.
- **Logo/wordmark source for a visual asset (not downloaded, URL only):** No official brand/press
  kit page was found directly on leonardo.ai in this search budget. Best available source noted:
  Brandfetch's Leonardo.Ai brand page, https://brandfetch.com/leonardo.ai (third-party asset
  aggregator, not Leonardo's own press kit — verify licensing before use). The live pricing page
  itself (https://leonardo.ai/pricing/) also renders the wordmark in its header/nav if a
  screenshot capture is preferred over a downloaded asset — consistent with the CLAUDE.md rule to
  capture sources on MOBILE via tools/capture.mjs rather than pull third-party logo files.
- **NOT FOUND:** an official Leonardo.Ai brand/press-kit page (e.g. leonardo.ai/press or
  leonardo.ai/brand) — did not surface in search results within budget.

## Gamma

- **Official pricing page fetched directly** (browser render): SRC: https://gamma.app/pricing
  (redirects/renders as https://gamma.app, page title "Plans and pricing | Gamma")
- **IMPORTANT CAVEAT — currency:** The page auto-localized to **INR (₹)** for this fetch (likely
  geo-detected), not USD. Verbatim from the official page:
  - Free: "₹0" — "400 credits at signup" — "Create up to 10 slides per prompt" — "Import from PDF
    & PPTX" — "Export to PDF, PPTX, PNG & Google Slides"
  - Plus: "₹400 / seat / month" ("₹4,800 per seat, billed annually") — "1,000 monthly credits" —
    "Create up to 100 slides per prompt" — "Remove Gamma branding" — "Advanced AI image models"
  - Pro: "₹950 / seat / month" ("₹11,400 per seat, billed annually") — "4,000 monthly credits" —
    "Premium AI image models" — "Custom branding" — "Detailed analytics & advanced sharing" —
    "Publish up to 10 custom domains" — "API access"
  - Ultra: "₹7,833.25 / seat / month" ("₹93,999 per seat, billed annually") — "20,000 monthly
    credits" — "Access to the most advanced AI models (text, image, video)" — "Publish up to 100
    custom domains" — "Early access to new features"
  SRC: https://gamma.app/pricing
  - I could not force the official page to show USD in this session (no currency/country
    selector found on the page; tried a `?currency=USD&country=US` query override, page ignored
    it). **HEDGE the USD numbers** — do not state a single confident USD figure on screen.
- **USD figures — VIA third-party aggregators only, and they DISAGREE with each other, which is
  itself a signal to hedge:**
  - VIA eesel.ai (https://www.eesel.ai/blog/gamma-pricing) [from search snippet, not directly
    fetched]: "Plus \$8/mo annually... Pro is \$20 per month annually, or \$25 monthly... Ultra at
    \$60 per month annually, or \$75 monthly."
  - VIA a separate search rollup citing SaaSworthy/other 2026 trackers: "Plus (\$9)... Pro (\$18)...
    Ultra (\$90)" when billed annually — these numbers do NOT match the eesel figures above.
  - Given the official page would not render USD for me and third-party USD figures conflict
    (\$8 vs \$9 Plus, \$20 vs \$18 Pro, \$60 vs \$90 Ultra), **the exact USD monthly price should be
    re-verified with a US-located fetch (VPN/proxy or a US-based teammate) before it is spoken as
    a hard number in the script** — safe to say "roughly \$8-10/mo for Plus, \$18-20/mo for Pro,
    \$60-90/mo for Ultra" as a hedged range, or avoid a specific dollar figure and lead with the
    feature contrast instead (branding removal, custom domains, API access), which is confirmed
    directly from the official page regardless of currency.
- **What paid unlocks over Free (confirmed directly from the official page, currency-independent):**
  higher/refreshing monthly credit allowance (1,000/4,000/20,000 vs 400 one-time at signup),
  higher slides-per-prompt ceiling (100 vs 10), **removes Gamma branding** (Plus+), advanced/
  premium AI image models (Plus/Pro), custom branding + advanced analytics/sharing (Pro), custom
  domain publishing (10 on Pro, 100 on Ultra), API access (Pro), and access to "the most advanced
  AI models (text, image, video)" (Ultra only).
- **Free-tier credits are a ONE-TIME signup grant, not a recurring monthly allowance** — verbatim:
  "400 credits at signup." This is a meaningfully different shape than the paid tiers' "monthly
  credits" language and is worth stating precisely on screen rather than implying free resets
  monthly.
  SRC: https://gamma.app/pricing
- **Recency flag — HEDGE THIS:** Search results surfaced a claim that "Gamma 3.0 replaced
  previously unlimited editing with per-edit credit charges" and a billing-cycle complaint, both
  from an August 2026 Trustpilot review — i.e. within the last 1-2 months. VIA (secondary,
  unverified against an official Gamma changelog): a search-engine rollup citing Trustpilot
  reviews, not independently opened in this session. Treat "Gamma recently tightened how credits
  are charged for edits" as a hedge-worthy claim to double check, not a confirmed fact, before it
  goes in a script.
- **Logo/wordmark source for a visual asset (not downloaded, URL only):** No dedicated
  press/brand-kit page was found on gamma.app itself within budget (gamma.app/docs/Brand-Kit
  surfaced but is Gamma's in-product "brand kit" FEATURE documentation, not Gamma's own company
  logo assets). Best available source noted: Brandfetch's Gamma page,
  https://brandfetch.com/gamma.app (third-party aggregator — verify licensing before use). The
  live pricing page (https://gamma.app/pricing) also renders Gamma's own wordmark in its header if
  a direct capture/screenshot is preferred.
- **NOT FOUND:** an official Gamma company press-kit/brand-assets page (e.g. gamma.app/press or
  gamma.app/brand); a way to force the official pricing page to render USD in this session.

## Summary of what to hedge in the script

1. Gamma's exact USD monthly prices — official page only rendered INR for this fetch; third-party
   USD figures conflict (\$8-9 / \$18-20 / \$60-90 across sources for Plus/Pro/Ultra). Re-verify with
   a US-geo fetch before stating a hard dollar figure, or use the confirmed feature unlocks
   (branding removal, custom domains, API access) instead of a number.
2. Gamma's "per-edit credit charges" / billing-cycle complaints — August 2026, VIA a Trustpilot
   rollup only, not confirmed against an official changelog.
3. Leonardo's "Solo/Team/API" consolidation into one cross-modal token currency — VIA secondary
   trackers only; the live pricing page confirms the CURRENT structure, but not a specific change
   date within the last 1-2 months.
