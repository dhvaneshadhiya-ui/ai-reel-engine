# Findings: Descript & Cursor — free vs paid (checked 2026-09-18)

## DESCRIPT

SRC: https://www.descript.com/pricing (fetched 2026-09-18)

- **Free tier — media minutes:** 60 minutes of media per month.
- **Free tier — AI credits:** 100 AI credits, **one-time only** (does not renew monthly). This is a meaningful gate — most other tools' free AI-credit pools refresh monthly; Descript's does not.
- **Free tier — export:** 720p export, watermarked.
- **Free tier — other:** transcription in 25 languages; limited access to Underlord (Descript's AI agent), Studio Sound, Green Screen, Eye Contact, Remove Filler Words; 5GB cloud storage; 1 seat.
- **Paid — Hobbyist: $16/month billed annually ($24/month billed monthly).** Unlocks: 10 media hours/month, 400 AI credits/month, watermark-free 1080p export, access to Underlord + AI tools, 100GB storage, 1 seat.
- **Paid — Creator: $24/month billed annually ($35/month billed monthly)** — marked "Most Popular" on the page. Unlocks: 30 media hours/month, 800 AI credits/month, watermark-free 4K export, full Underlord + "20+ AI tools", AI video generation with latest models, unlimited royalty-free stock media, 1TB storage, scales to 3 seats.
- **Paid — Business: $50/month billed annually ($65/month billed monthly).** Unlocks: 40 media hours/month, 1500 AI credits/month, team-wide Brand Studio access, translate/dub in 30+ languages with proofread, custom avatar generation, priority support with SLA, 2TB storage, scales to 5 seats.
- **Enterprise:** custom pricing, contact sales.

NOTE: the numbers above came back from a WebFetch summarization pass (page content run through a small model), not a raw HTML grab — treat as accurate to the source but re-verify exact wording (not necessarily verbatim string-for-string) if a script line needs to quote the page directly.

### Recent-change flag — HEDGE THIS
SRC (VIA, third-party aggregators, not primary — sonix.ai, castmagic.io, shade.inc, layer3labs.io, costbench.com, all dated 2026): they describe "a September 2025 overhaul [that] replaced 'transcription hours' with 'media minutes' and introduced metered AI credit top-ups," moving Underlord, Studio Sound, and Overdub into AI-credit pools.
- That structural change is ~1 year old as of Sept 2026, not within the last 1-2 months — do NOT flag it as "just changed." But DO hedge on exact credit/minute numbers in the script (e.g. "as of publishing") since Descript has a track record of restructuring free-tier mechanics.
- No evidence found of a Descript pricing change specifically in Jul-Sep 2026 — searched directly and nothing more recent than the Sept 2025 overhaul turned up.

### Logo / wordmark source
- No dedicated official brand/press/media-kit page found on descript.com — homepage footer has no Brand/Press/Media Kit link, and https://www.descript.com/press 404'd.
- Only first-party source located: descript.com's own site header/favicon.
- Third-party mirrors exist (licensing unverified): Brandfetch (https://brandfetch.com/descript.com), SeekLogo (https://seeklogo.com/vector-logo/448113/descript). Flag to editor: confirm licensing before using a third-party-hosted file; prefer pulling the mark from a first-party Descript page (screenshot/favicon) if no press kit turns up.

---

## CURSOR

SRC: https://cursor.com/pricing (fetched 2026-09-18)

- **Free tier — "Hobby":** verbatim bullets: "No credit card required" / "Limited Agent requests" / "Access to Composer". No quantified numeric limit is published on the pricing page itself — "Limited Agent requests" is the only free-tier usage description; no monthly request count, minute count, or token count is stated there.
- **Paid — Pro: $20/month.** Verbatim: "Extended limits on Agent" / "Generous limits for Grok" / "Access to frontier models" / "Grok Bot access" / "MCPs, skills, and hooks" / "Cloud agents" / "Bugbot on usage-based billing".
- **Paid — Pro+: $60/month.** Verbatim: "3x Pro limits on Agent" / "Generous limits for Grok" / "Access to frontier models" / "Higher Grok Bot usage limits" / "MCPs, skills, and hooks" / "Cloud agents" / "Bugbot on usage-based billing".
- **Paid — Ultra: $200/month.** Verbatim: "20x Pro limits on Agent" / "Generous limits for Grok" / "Access to frontier models" / "Highest Grok Bot usage limits" / "MCPs, skills, and hooks" / "Cloud agents" / "Bugbot on usage-based billing" / "Priority access to new features".
- Yearly billing: 20% savings across paid plans (per cursor.com/docs/account/pricing).
- Also exists, out of scope for an individual free-vs-paid piece: Teams and Enterprise.

### Recent-change flag — HEDGE THIS HARD; qualify with a date in the script
Cursor's pricing model has changed multiple times in 2026 — do not state it as a flat, permanent fact.

SRC (VIA, third-party aggregators relaying Cursor's own changelog — cloudzero.com, lowcode.agency, finout.io, cellcog.ai, all dated 2026):
- "Cursor changed how it charges three times in 2026 alone."
- Reported shift from request-based billing to dollar-denominated monthly usage credit pools, e.g. "Your $20 Pro plan now includes $20 in credits" — some aggregators additionally claim ~$70 of usage for Pro+ and ~$400 for Ultra. **This specific dollar-credit-pool claim was NOT confirmed on the primary cursor.com/pricing or /docs/account/pricing pages fetched directly this session — treat as VIA/unconfirmed; re-verify or omit the exact multiplier from the script.**
- VIA cellcog.ai: "Cursor retired the flat Auto rate ($1.25 input / $6 output per million tokens) on August 24, 2026. Every Auto request now bills at the list price of the routed model."
- VIA cellcog.ai: "Enterprise was the only plan allowed to keep the legacy flat Auto rate, and its window closed on September 7, 2026."
- VIA multiple aggregators: Teams split into two seat tiers effective June 1, 2026 — Standard $40/user/month, Premium $120/user/month with "5x the usage at 3x the price."
- VIA aggregators, not confirmed on a primary page this session: an added "$0.25-per-million-token Cursor Token Rate" on third-party model requests for Teams/Enterprise.

**Bottom line for the script:** state the plan names and the four headline prices ($0 / $20 / $60 / $200) as current and primary-sourced (cursor.com/pricing, fetched today). Do NOT state specific request counts, credit-dollar-equivalents, or Auto-billing mechanics as settled, timeless facts — attribute them explicitly ("Cursor changed its billing again in August 2026") or drop them, since even third-party trackers disagree on specifics and none of the mechanics were confirmed word-for-word on a primary Cursor page this session.

### Logo / wordmark source
- Official: https://cursor.com/brand — confirmed via search to be Cursor's own brand guidelines/asset page (logos in "2D default and 2.5D," horizontal lockup preferred, vertical lockup, cube-only, or wordmark-only). This is the right first-party URL for the visual asset. Did NOT fetch the page's own contents this session (only confirmed existence/description via search) — re-check for the exact SVG/PNG download link before building the asset.
- Cursor brand colors per a search-result summary of cursor.com/brand (VIA, re-verify before use): #F7F7F4, #14120B, #26251E. Typography: "Cursor Gothic" and "Berkeley Mono."

---

## NOT FOUND / NOT VERIFIED THIS SESSION
- Descript: no official press/brand-kit page exists at the guessed URL (descript.com/press → 404); no footer link to one on the descript.com homepage either.
- Descript: could not confirm whether AI-credit *pricing* (not just structure) changed in the last 1-2 months (Jul-Sep 2026) — only found the Sept 2025 structural overhaul.
- Cursor: exact numeric value behind "Limited Agent requests" on the free Hobby tier is not published on cursor.com/pricing — described only qualitatively.
- Cursor: did not independently fetch cursor.com/brand page contents (only confirmed via search snippet) — get the actual asset URL before production use.
- Cursor: the "$20/$70/$400 credit pool by tier" figure and the "$0.25/M token Cursor Token Rate" are VIA third-party aggregators only, not confirmed against a primary Cursor page this session.
