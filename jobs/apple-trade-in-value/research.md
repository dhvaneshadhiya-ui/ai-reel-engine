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

### 1. WHAT HAPPENED — the official record
- 2026-09-02  live DOM read of https://www.apple.com/shop/trade-in
  (settled: the $40-$720 headline, the four-row table, the footnote, the
   button label.)
- 2026-09-02  live DOM read of the US iPhone values overlay
  (settled: all 32 models and the $40 floor at iPhone 8.)
- 2026-09-02  static WebFetch of the same URL
  (settled that it is USELESS here: the table is JavaScript-rendered and a
   static fetch returns nothing. The payoff of this reel is invisible to it.)

### 2. WHO ELSE TRIED IT — hands-on, by someone who is not the vendor
- 2026-09-02  "Apple trade-in offer lower than quoted value after inspection"
  (settled that the published table is NOT the last number that moves: users
   report a quote of $70 revised to $15 after inspection, and a MacBook quoted
   ~$1,100 revised to $850 for "incorrect product or serial number". Apple's
   policy is that a revised value may be accepted or the device returned.
   SOURCES: discussions.apple.com thread 255241765, forums.macrumors.com
   thread 2443727.)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-02  same search as above
  (settled the recurring complaint: no recourse on a revised value beyond
   accept-or-return. This is the material the first draft of this reel did not
   have, and it is a better story than the "up to" wording alone.)

### 4. WHAT WOULD CONTRADICT THIS — the search to prove the story wrong
- 2026-09-02  NOT YET RUN. The story to disprove is "the table overstates what
  you get". Evidence against it would be users reporting offers HONOURED at the
  quoted figure. The search above surfaced complaints, which is a biased
  sample by nature — people post when it goes wrong. Recorded as a known
  weakness rather than presented as balance.

INDEPENDENT-CHECK: 2026-09-02 searched for hands-on trade-in experiences and
  found substantial reporting of values revised DOWN after inspection. The
  first draft of this ledger said N/A on the reasoning that "what Apple's page
  says" needs no independent test. That was wrong: what the page PROMISES and
  what people RECEIVE are different claims, and only the second needed looking
  up.
