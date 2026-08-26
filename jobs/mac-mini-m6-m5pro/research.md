# Research — mac-mini-m6-m5pro

Claims ledger + search log. Format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: Apple's new Mac mini starts at $899 — a $300 jump, ~50%, from the
  $599 the M4 mini launched at less than two years ago, and it is the
  second hike this year (raised to $699 in June before this second rise)
  TIER: multi
  SPOKEN: "So in June, the base price jumped from $599 to $699. Wednesday, it jumped again, to $899."
  SRC: https://www.macworld.com/article/3220063/apple-launches-new-m6-mac-mini-with-another-price-hike.html
  VIA: Macworld's own price-history reporting
  SRC: https://www.bgr.com/2243709/mac-mini-2026-release-date-price-features/
  VIA: BGR's own price-history reporting, cites the RAM shortage
  SRC: https://www.tomshardware.com/desktops/mini-pcs/apple-price-hikes-continue-as-mac-mini-with-16gb-ram-and-256gb-is-now-usd899-1tb-storage-option-adds-usd500-to-entry-level-headless-system
  VIA: Tom's Hardware's own price-history reporting

- CLAIM: The M5 Pro Mac mini also rose $300 from the previous generation
  ($1,399 to $1,699), the same pattern as the base M6 model
  TIER: multi
  SPOKEN: "That's another $300 jump from last generation, same story."
  SRC: https://www.bgr.com/2243709/mac-mini-2026-release-date-price-features/
  VIA: BGR's own price-history reporting
  SRC: https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/
  VIA: Apple Newsroom (current $1,699 figure; prior-gen $1,399 is BGR's
       own reporting, not restated by Apple)

- CLAIM: Apple and outlets attribute the price rise to the ongoing memory
  (DRAM/RAM) shortage, not a spec change
  TIER: multi
  SPOKEN: "That's because of the memory shortage hitting every chipmaker"
  SRC: https://www.bgr.com/2243709/mac-mini-2026-release-date-price-features/
  VIA: BGR, quoting the RAM-shortage rationale used across coverage
  SRC: https://www.macworld.com/article/3220063/apple-launches-new-m6-mac-mini-with-another-price-hike.html
  VIA: Macworld's own analysis of the June and August hikes

- CLAIM: Apple's official Mac mini M6 pricing is $899 (standard) / $799
  (education); M5 Pro is $1,699 (standard) / $1,599 (education). Only the
  $899 base figure is spoken in the script; $799/$1,699/$1,599 appear only
  on screen via the pricing-availability-receipt (Rule 3: receipt may show
  more than is spoken, as long as it doesn't contradict the words).
  TIER: official
  SPOKEN: "to $899"
  SRC: https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/
  VIA: Apple Newsroom (primary announcement)

- CLAIM: M6 is a 12-core CPU / 12-core GPU chip (two more cores of each than
  M4), with Neural Accelerators in every GPU core for the first time on Mac
  mini, and delivers up to 4x faster AI performance, 2x faster graphics and
  40% faster CPU performance than M4
  TIER: official
  SPOKEN: "12 CPU cores, 12 GPU cores, and up to 4 times the AI performance of the M4. Graphics: twice as fast. CPU: 40 percent faster."
  SRC: https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/
  VIA: Apple Newsroom (primary announcement)
  SRC: https://9to5mac.com/2026/08/25/apple-announces-new-mac-mini-heres-everything-new/
  VIA: 9to5mac's own report on the same Apple announcement

- CLAIM: M6 is Apple's first chip built on a 2nm process
  TIER: multi
  SPOKEN: "the new M6 is Apple's first chip built on 2 nanometers"
  SRC: https://9to5mac.com/2026/08/25/apple-announces-new-mac-mini-heres-everything-new/
  VIA: 9to5mac's own report
  SRC: https://camerajabber.com/photography-news/apples-m6-mac-mini-brings-2nm-silicon-and-a-300-price-rise/
  VIA: Camera Jabber's own report

- CLAIM: The M5 Pro configuration offers up to an 18-core CPU, up to a
  20-core GPU, up to 64GB unified memory at 307GB/s bandwidth, and three
  rear Thunderbolt 5 ports (vs Thunderbolt 4 on the base M6 mini)
  TIER: official
  SPOKEN: "18 CPU cores, 20 GPU cores, up to 64 gigs of memory, and Thunderbolt 5"
  SRC: https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/
  VIA: Apple Newsroom (primary announcement)
  SRC: https://9to5mac.com/2026/08/25/apple-announces-new-mac-mini-heres-everything-new/
  VIA: 9to5mac's own report on the same Apple announcement

- CLAIM: Pre-orders for the new Mac mini opened August 25, 2026; it ships
  September 22, 2026
  TIER: official
  SPOKEN: "It ships to you September 22nd."
  SRC: https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/
  VIA: Apple Newsroom (primary announcement)

## EXPLICITLY NOT CLAIMED

- Genlock/USB-C camera-sync support, Wi-Fi 7 / Bluetooth 6 / N1 chip,
  100% recycled-material enclosure claims, and the per-app benchmark
  figures (Excel, Blender, Affinity, Cyberpunk 2077) are all real per
  Apple's own release but CUT from the script for word budget — see
  structure.md "WHAT WAS CUT". None of these are contradicted, just unused.
- Do NOT claim the price hike is "because of AI demand" — that is
  Macworld's speculation ("may benefit from reduced budget-market demand"),
  not a stated Apple reason. The script attributes the hike only to the
  memory/DRAM shortage, which multiple outlets state as fact.

## SEARCHED

- 2026-08-26  "Mac mini M6 2nm N1 chip price increase $899"  (found the
  price-history angle: $599 -> $699 June 2026 -> $899 Aug 2026)
- 2026-08-26  fetched apple.com/newsroom Mac mini M6/M5 Pro press release
  (official specs, pricing, ship date)
- 2026-08-26  fetched 9to5mac's "everything new" writeup (corroborating
  specs + the 2nm/N1 details)
- 2026-08-26  fetched macworld.com, bgr.com, tomshardware.com for the price
  history and the memory-shortage rationale (three independent domains)
