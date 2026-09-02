# Research — apple-trade-in-value-in

Claims ledger + search log. Tiers: official / multi / single / disputed.
A single or disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: Apple India's published iPhone ceiling is Rs 57,000 (iPhone 16 Pro Max).
  TIER: official
  SPOKEN: "Apple says your old iPhone is worth fifty-seven thousand rupees."
  SRC: https://www.apple.com/in/shop/trade-in
  VIA: Apple India, own published page - table.dd-table read from the live DOM
       2026-09-02: 16 Pro Max "Up to Rs57000.00", 16 Pro "Rs51500.00",
       16 Plus "Rs36000.00", 16 "Rs36000.00".

- CLAIM: The visible table lists only four models, all iPhone 16 variants.
  TIER: official
  SPOKEN: "that table lists four phones, and all four are iPhone 16s"
  SRC: https://www.apple.com/in/shop/trade-in
  VIA: Apple India, own published page - the table has exactly four data rows.

- CLAIM: "See all iPhone values" opens the full list of 32 models, the lowest
    being an iPhone 8 at Rs 5,500.
  TIER: official
  SPOKEN: "tap See all iPhone values. That opens the full list, thirty-two models, down to an iPhone 8 at five and a half thousand"
  SRC: https://www.apple.com/in/shop/browse/overlay/tradein_landing/iphone_values
  VIA: Apple India, own overlay - 32 unique models read from the live DOM
       2026-09-02; iPhone 8 = "Up to Rs5500.00" is the lowest.

- CLAIM: India frames the credit as tied to buying a new iPhone.
  TIER: official
  SPOKEN: "Buy a new iPhone today and get four and a half thousand to fifty-seven thousand credit when you exchange."
  SRC: https://www.apple.com/in/shop/trade-in
  VIA: Apple India, own published page - h2 read verbatim from the live DOM
       2026-09-02: "Buy a new iPhone today and get Rs4500.00-Rs57000.00 credit
       when you exchange."

- CLAIM: The button under the India values card reads "Shop iPhone".
  TIER: official
  SPOKEN: "the button under that table says Shop iPhone"
  SRC: https://www.apple.com/in/shop/trade-in
  VIA: Apple India, own published page - read from a 1080x1920 screen
       recording of the page, 2026-09-02. The US card carries "Find your
       trade-in value" in the same position.

- CLAIM: Apple states value varies by condition, year and configuration, and
    that not all devices are eligible.
  TIER: official
  SPOKEN: "values vary by condition, year and configuration, and not every device is eligible"
  SRC: https://www.apple.com/in/shop/trade-in
  VIA: Apple India, own published page - footnote read verbatim 2026-09-02.
       Wording is identical to the US page.

ONE-SOURCE-OK: every figure is a fact about what Apple India publishes on its
own page, so Apple is the primary record, not merely the best source. A second
outlet reporting this table would be quoting this page. Verified against the
LIVE DOM: the table is JavaScript-rendered and a static fetch returns nothing.

## NOT CLAIMED

- We do NOT attribute the Rs 4,500 floor to any model. The lowest iPhone on
  the full list is Rs 5,500, so Rs 4,500 belongs to something not on it, and
  what that is could not be verified.
- We do NOT say what any individual will be offered.
- We do NOT cover the Android exchange line (Rs 3,000-Rs 37,000), which is a
  different device class and a different reel.
- We do NOT claim values change at the September 9 launch.

## SEARCHED

- 2026-09-02  live DOM read of https://www.apple.com/in/shop/trade-in
  (settled: every figure, both headlines, the button labels and the footnote.)
- 2026-09-02  live DOM read of the India iPhone values overlay
  (settled: the full 32-model list and the Rs 5,500 floor.)
- 2026-09-02  same two reads against the US pages
  (settled: the differences - "Exchange" branding, purchase-tied credit,
   "Shop iPhone" vs "Find your trade-in value", and 16 Plus/16 sharing one
   price in India but not in the US.)
