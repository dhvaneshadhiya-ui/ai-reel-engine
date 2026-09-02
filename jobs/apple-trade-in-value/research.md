# Research — apple-trade-in-value

Claims ledger + search log. Tiers: official / multi / single /
disputed. A single or disputed claim must be SPOKEN hedged
(framework S20).

## CLAIMS

- CLAIM: Apple's US trade-in page headlines the iPhone range as $40 to $720.
  TIER: official
  SPOKEN: "Apple says your old iPhone is worth seven hundred and twenty dollars."
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page — read from the live DOM 2026-09-02,
       h2 reads "Get $40–$720 when you trade in an iPhone."

- CLAIM: Every row of Apple's published iPhone values table is prefixed "Up to".
  TIER: official
  SPOKEN: "Now look at what every one of those rows starts with. Up to."
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page — table.dd-table read from the live DOM
       2026-09-02: iPhone 16 Pro Max "Up to $720", 16 Pro "Up to $630",
       16 Plus "Up to $485", 16 "Up to $480".

- CLAIM: The published table's top figure is the iPhone 16 Pro Max at up to $720.
  TIER: official
  SPOKEN: "sixteen Pro Max at seven twenty, sixteen Pro at six thirty, the plain sixteen at four eighty"
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page — same table read 2026-09-02.

- CLAIM: Apple states the value depends on condition, year and configuration,
    and that not every device gets credit at all.
  TIER: official
  SPOKEN: "values vary by condition, year and configuration, and not every device is eligible"
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page — disclaimer read verbatim from the live
       DOM 2026-09-02.

- CLAIM: The actual quote comes from Apple's "Find your trade-in value" flow,
    not from the published table.
  TIER: official
  SPOKEN: "Tap Find your trade-in value and answer the condition questions honestly."
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page — button label read from the live DOM
       2026-09-02; the table carries no per-condition figure.

ONE-SOURCE-OK: every figure spoken is a fact about what Apple publishes on
its own page, so Apple is not merely the best source here, it is the only one
that can be authoritative. A second outlet reporting this table would be
quoting this page. The claim is "Apple's page says X", and the page is the
primary record. (Verified against the LIVE DOM, not a static fetch — a static
fetch of the same URL returns no table at all.)

## NOT CLAIMED

- We do NOT say what any individual will be offered. Every figure spoken is
  Apple's published ceiling for a model in the US, and the script says
  "ceiling" and "US" out loud rather than implying a quote.
- We do NOT compare Apple's offer to carrier or third-party trade-in values.
  No sourcing was gathered for that and it would be a different reel.
- We do NOT claim the range changes at the September 9 launch. Plausible,
  and widely assumed, but nothing published supports it — so it is absent
  from the script rather than hedged into it.

## SEARCHED

- 2026-09-02  "iOS 27 new feature how to enable September 2026 iPhone settings"
  (settled: iOS 27 ships ~Sept 2026; surfaced Extend Wallpaper and Safari
   topics as candidate how-to subjects. Abandoned — see below.)
- 2026-09-02  "iOS 27 lock screen wallpaper extend photo Apple Intelligence how to"
  (settled: Extend is real, multi-sourced across macrumors/9to5mac/
   idownloadblog. ABANDONED as this reel's subject: it exists only on the
   iOS 27 beta and the user cannot record it, so the footage rule decided
   the topic, not the research.)
- 2026-09-02  "Apple Intelligence supported iPhone models list iPhone 15 Pro requirement"
  (settled: Apple Intelligence needs iPhone 15 Pro/Pro Max or 16 and newer.
   Retained here because it was verified; unused in this script.)
- 2026-09-02  live DOM read of https://www.apple.com/shop/trade-in via
  tools/capture.mjs probe + browser JS
  (settled: EVERY figure in this script. The values table is rendered by
   JavaScript, so a static fetch of the same URL returns no table at all —
   WebFetch reported "the webpage content does not include a trade-in values
   table" while the live page showed it plainly. Anything read only through
   a static fetch would have missed the entire payoff.)
