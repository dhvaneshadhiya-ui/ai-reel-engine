# Research — apple-trade-in-value-in

Claims ledger + search log. Tiers: official / multi / single / disputed.
A single or disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: Apple India's ceiling for an iPhone 11 Pro Max is Rs 15,500.
  TIER: official
  SPOKEN: "Apple will give you fifteen and a half thousand rupees for an iPhone 11 Pro Max."
  SRC: https://www.apple.com/in/shop/browse/overlay/tradein_landing/iphone_values
  VIA: Apple India, own value overlay - read from the live DOM 2026-09-02,
       "iPhone 11 Pro Max = Up to Rs15500.00".

- CLAIM: Across six Pro Max generations Apple India lists 57,000 / 48,000 /
    39,500 / 32,000 / 21,500 / 15,500.
  TIER: official
  SPOKEN: "Sixteen Pro Max, fifty-seven thousand. Fifteen, forty-eight. Fourteen, thirty-nine and a half. Thirteen, thirty-two. Twelve, twenty-one and a half. Eleven, fifteen and a half."
  SRC: https://www.apple.com/in/shop/browse/overlay/tradein_landing/iphone_values
  VIA: Apple India, own value overlay - all six read from the live DOM
       2026-09-02 in one pass.

- CLAIM: The span from 16 Pro Max to 11 Pro Max is Rs 41,500.
  TIER: official
  SPOKEN: "Five generations, forty-one and a half thousand rupees, gone."
  VIA: arithmetic on the row above - 57,000 minus 15,500. No outside source
       needed or claimed; it is subtraction on Apple's own published figures.
  SRC: https://www.apple.com/in/shop/browse/overlay/tradein_landing/iphone_values

- CLAIM: The largest single-generation drop in that ladder is 13 Pro Max to
    12 Pro Max, Rs 10,500 - larger than the newest step.
  TIER: official
  SPOKEN: "It's the step from thirteen to twelve. Ten and a half thousand, in a single generation."
  VIA: arithmetic on the same six figures. Steps are 9,000 / 8,500 / 7,500 /
       10,500 / 6,000, so 10,500 is the maximum and it is not the newest.
  SRC: https://www.apple.com/in/shop/browse/overlay/tradein_landing/iphone_values

- CLAIM: Every figure in Apple's list is prefixed "Up to".
  TIER: official
  SPOKEN: "every figure there begins with the same two words. Up to."
  SRC: https://www.apple.com/in/shop/trade-in
  VIA: Apple India, own page and overlay - every row of both reads "Up to".

- CLAIM: Averaged over those five generations the ceiling falls about
    Rs 8,300 a year.
  TIER: official
  SPOKEN: "that's roughly eight thousand rupees a year"
  VIA: arithmetic - 41,500 over 5 generations = 8,300. SPOKEN deliberately
       rounds DOWN to "roughly eight thousand" rather than up, and says
       "roughly", because one generation is not exactly one year.
  SRC: https://www.apple.com/in/shop/browse/overlay/tradein_landing/iphone_values

ONE-SOURCE-OK: every figure is a fact about what Apple India publishes on its
own page, so Apple is the primary record. A second outlet reporting this table
would be quoting it. Verified against the LIVE DOM - the values are
JavaScript-rendered and a static fetch returns nothing.

## NOT CLAIMED

- We do NOT state what any iPhone originally cost. A launch-price comparison
  would make the depreciation figure far more dramatic, and it is exactly the
  claim this ledger cannot support: no launch price was verified this session,
  so none is spoken.
- We do NOT say a generation equals a year. The script says "roughly" and
  "a single generation" for that reason.
- We do NOT claim these values drop at the September 9 launch.
- We do NOT cover the Android exchange line, or the purchase-tied framing -
  that is the other cut's material.

## SEARCHED

- 2026-09-02  live DOM read of the Apple India iPhone values overlay
  (settled: all 32 models, including the six Pro Max generations this reel is
   built on.)
- 2026-09-02  live DOM read of https://www.apple.com/in/shop/trade-in
  (settled: the "Up to" prefix and the footnote.)
- 2026-09-02  attempted screen capture of the values overlay at mobile width
  (settled that it is UNUSABLE as footage: the overlay renders a desktop
   layout even at 360px, putting 32 rows on one screen at unreadable size.
   The ladder is therefore a coded graphic built from the verified numbers,
   with the readable four-row table as its receipt.)

INDEPENDENT-CHECK: N/A — same as the USD cut: the claims are what
Apple India's own page and value overlay say, read from the live DOM
2026-09-02. No third party can be more authoritative about Apple's
published prices than Apple's published prices.
