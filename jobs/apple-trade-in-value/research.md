# Research — apple-trade-in-value

Claims ledger + search log. Tiers: official / multi / single /
disputed. A single or disputed claim must be SPOKEN hedged
(framework S20).

## CLAIMS

- CLAIM: Apple's US trade-in page headlines the iPhone range as $40 to $720.
  TIER: official
  SPOKEN: "Apple says your old iPhone is worth seven hundred and twenty dollars."
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page - read from the live DOM 2026-09-02,
       h2 reads "Get $40-$720 when you trade in an iPhone."

- CLAIM: The table on the trade-in page itself lists only four models, and all
    four are iPhone 16s.
  TIER: official
  SPOKEN: "that table lists four phones, and all four are iPhone 16s"
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page - table.dd-table read from the live DOM
       2026-09-02 contained exactly four rows: 16 Pro Max, 16 Pro, 16 Plus, 16.

- CLAIM: "See all iPhone values" opens a list of 32 models, the lowest being
    the iPhone 8 at up to $40.
  TIER: official
  SPOKEN: "That opens the full list, thirty-two models, all the way down to an iPhone 8 at forty dollars."
  SRC: https://www.apple.com/shop/browse/overlay/tradein_landing/iphone_values
  VIA: Apple, own value overlay - all 32 rows read from the live DOM
       2026-09-02. iPhone 8 and 8 Plus are both "Up to $40", and $40 is
       exactly the floor of the headline range, so the range is not
       rhetorical.

- CLAIM: Every row of Apple's list is prefixed "Up to".
  TIER: official
  SPOKEN: "Then look at what every single row starts with. Up to."
  SRC: https://www.apple.com/shop/browse/overlay/tradein_landing/iphone_values
  VIA: Apple, own page and overlay - every row of both reads "Up to".

- CLAIM: Apple states the value depends on condition, year and configuration,
    and that not every device gets credit at all.
  TIER: official
  SPOKEN: "values vary by condition, year and configuration, and not every device is eligible"
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page - footnote read verbatim from the live DOM
       2026-09-02: "Trade-in values will vary based on the condition, year,
       and configuration of your eligible trade-in device. Not all devices
       are eligible for credit."

- CLAIM: The actual quote comes from Apple's "Find your trade-in value" flow,
    not from the published list.
  TIER: official
  SPOKEN: "tap Find your trade-in value and answer the condition questions honestly"
  SRC: https://www.apple.com/shop/trade-in
  VIA: Apple, own published page - button label read from the live DOM
       2026-09-02; neither the table nor the overlay carries a
       per-condition figure.

ONE-SOURCE-OK: every figure spoken is a fact about what Apple publishes on
its own page, so Apple is not merely the best source here, it is the only one
that can be authoritative. A second outlet reporting this table would be
quoting this page. Verified against the LIVE DOM, not a static fetch - a
static fetch of the same URL returns no table at all.

## NOT CLAIMED

- We do NOT say what any individual will be offered. Every figure spoken is
  Apple's published US ceiling, and the script says "ceiling" out loud.
- We do NOT compare Apple's offer to carrier or third-party trade-in values.
  No sourcing was gathered and it would be a different reel.
- We do NOT claim the range changes at the September 9 launch. Plausible and
  widely assumed; nothing published supports it, so it is absent rather than
  hedged.
- We do NOT state any launch price, which would make the depreciation angle
  land harder and is exactly what this ledger cannot support.

## SEARCHED

- 2026-09-02  live DOM read of https://www.apple.com/shop/trade-in
  (settled: the headline range, the four-row table, the footnote, the button
   label.)
- 2026-09-02  live DOM read of the US iPhone values overlay
  (settled: all 32 models and the $40 floor at iPhone 8.)
- 2026-09-02  static WebFetch of the same trade-in URL
  (settled that it is USELESS here: it returned "the webpage content does not
   include a trade-in values table" because the table is JavaScript-rendered.
   Anything read only through a static fetch would have missed the payoff.)

INDEPENDENT-CHECK: N/A — every figure in this reel is a fact about
what Apple publishes on Apple's own page. There is no independent test
of "what does this page say"; the page is the primary record, and it
was read from the live DOM rather than a static fetch.
