# Research — apple-screenless-tracker

Claims ledger + search log. `script_approval.py propose` refuses
while placeholder text remains; format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: Apple is developing a screenless fitness/health tracker to rival Whoop, and is testing prototypes
  TIER: single
  SPOKEN: "Bloomberg's Mark Gurman reports Apple is testing a completely different device, one with no screen at all"
  SURPRISE: 82
  SRC: https://www.macrumors.com/2026/09/22/apple-screenless-fitness-band/
  SRC: https://9to5mac.com/2026/09/22/apple-working-on-whoop-style-screenless-fitness-tracker-per-report/
  VIA: Mark Gurman / Bloomberg (original: https://www.bloomberg.com/news/articles/2026-09-22/apple-is-developing-new-fitness-tracker-aimed-at-rivaling-whoop, paywalled — not directly fetched)

- CLAIM: The device is a thin fabric band with a sensor-equipped computing module and no display
  TIER: single
  SPOKEN: "It's reportedly a thin fabric band with a sensor module on your wrist. No display. No notifications."
  SURPRISE: 55
  SRC: https://www.macrumors.com/2026/09/22/apple-screenless-fitness-band/
  SRC: https://techcrunch.com/2026/09/22/apple-could-take-on-whoop-with-a-new-fitness-tracker-report-says/
  VIA: Mark Gurman / Bloomberg

- CLAIM: Tim Cook and Eddy Cue are both interested in / backing the project
  TIER: single
  SPOKEN: "Gurman says Tim Cook and Eddy Cue are both behind it."
  SURPRISE: 60
  SRC: https://www.macrumors.com/2026/09/22/apple-screenless-fitness-band/
  VIA: Mark Gurman / Bloomberg

- CLAIM: Eddy Cue has led Apple's health team since October 2025 (after Jeff Williams's departure) and has pushed for interfaces simpler than the Watch's, like Whoop/Oura
  TIER: single
  SPOKEN: "Cue's run Apple's health team since last October, reportedly pushing for something simpler than the Watch."
  SURPRISE: 48
  SRC: https://9to5mac.com/2026/09/22/apple-working-on-whoop-style-screenless-fitness-tracker-per-report/
  SRC: https://www.macrumors.com/2025/10/10/apple-health-fitness-teams-eddy-cue-reshuffle/
  VIA: Mark Gurman / Bloomberg (health reorg first reported 2025-10-10: https://www.bloomberg.com/news/articles/2025-10-10/apple-to-move-health-fitness-divisions-to-services-in-reorganization)

- CLAIM: Apple's watch did not track heart rate continuously outside workouts until the Sept 9 2026 launch of the "Health Sensing System," which now samples every 5 seconds (a 60x frequency increase)
  TIER: official
  SPOKEN: "But that sensor gap was already closed in September."
  SURPRISE: 68
  SRC: https://www.macrumors.com/2026/09/09/apple-watch-series-12-announced-all-day-hr-sensor/
  SRC: https://9to5mac.com/2026/09/09/apple-watch-series-12-and-ultra-4-unveiled-with-upgraded-health-tracking-system/

- CLAIM: Oura filed for an IPO targeting a fully-diluted valuation of roughly $15.62 billion, after selling 3.6 million rings in the 12 months ended June 30, 2026
  TIER: official
  SPOKEN: "Oura just filed to go public at a sixteen billion dollar valuation."
  SURPRISE: 71
  SRC: https://www.theglobeandmail.com/investing/article-smart-ring-maker-oura-targets-1562-billion-valuation-in-us-ipo/

- CLAIM: Whoop is valued at roughly $10 billion
  TIER: single
  SPOKEN: "Whoop's reportedly worth ten billion too."
  SURPRISE: 54
  SRC: https://techcrunch.com/2026/09/22/apple-could-take-on-whoop-with-a-new-fitness-tracker-report-says/

- CLAIM: Apple has not decided whether to release the product; it is in a "technology investigation" phase, and if it ships, it likely would not launch before 2028
  TIER: single
  SPOKEN: "Gurman says it's a technology investigation: prototypes, not a product. It's not landing before 2028, if it lands at all."
  SURPRISE: 40
  SRC: https://techcrunch.com/2026/09/22/apple-could-take-on-whoop-with-a-new-fitness-tracker-report-says/
  SRC: https://www.macrumors.com/2026/09/22/apple-screenless-fitness-band/
  VIA: Mark Gurman / Bloomberg

## NOT CLAIMED

- "Eddy Cue personally wears both Oura and Whoop" — surfaced only in an AI search-summary,
  explicitly absent from direct fetches of both the 9to5Mac and MacRumors Sept 22 pieces. NOT USED.
- Vision Pro/Vision hardware team involvement in engineering the device — single-sourced to
  one WebFetch pass, absent from MacRumors/9to5Mac. NOT USED.
- A quote from Promus Ventures' Mike Collett about Oura's IPO — could not be verified in its
  cited source (article predates the Sept 22 report by ~4 weeks and doesn't contain the quote).
  NOT USED.
- Apple previously explored and killed a smart-ring project — sourced only to thetechportal.com,
  a lower-confidence outlet, and not corroborated elsewhere. NOT USED (too thin to be load-bearing
  for an honesty beat; the "technology investigation" / "hasn't decided" / "2028" hedges already
  carry that job on solid sourcing).
- Any codename for the device — none found in any source.
- Any Apple denial or "no comment" — none found; TechCrunch reached out to Apple and got no
  quoted reply, which is standard silence on unannounced hardware, not a denial.
- Any public statement from Whoop or Oura reacting to the report — none found.

INDEPENDENT-CHECK: this is a single-origin story. Every outlet checked (9to5Mac, MacRumors,
TechCrunch, Athletech News, PYMNTS, The Verge via Techmeme aggregation) traces to one Bloomberg
exclusive by Mark Gurman (2026-09-22); none cites a second, separate source chain. That is why
every claim specific to the device/project above is tiered `single` and spoken hedged, even
though four+ source domains appear in the ledger — the domain count is not the source count here.
The two `official` claims (Apple Watch's own Sept 9 announcement; Oura's IPO filing numbers) are
independently verifiable facts, not part of the Bloomberg exclusive.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-23  "Apple Whoop-style screenless fitness tracker report September 2026"  (found the Bloomberg/Gurman exclusive, syndicated by 9to5Mac, MacRumors, TechCrunch, PYMNTS, Athletech News)
- 2026-09-23  "Apple screenless fitness band Whoop Oura rival report"  (confirmed same story, found MacDailyNews/gadgetsandwearables pickups, confirmed device description: fabric band + sensor module, Cook/Cue backing, 2028 timeline)
- 2026-09-23  Apple Watch Series 12 Sept 9 2026 official announcement — "Health Sensing System" continuous HR every 5 seconds  (settled: Apple already shipped always-on HR before this report)
- 2026-09-23  Oura IPO filing coverage (Globe and Mail) — 3.6M rings sold, $15.62B valuation target, $1.21B revenue  (verified against brief's numbers)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- N/A — the device is an unannounced internal prototype; no unit exists for anyone outside Apple to test. Whoop and Oura themselves are established, reviewed products (sleepfoundation.org review fetched for Oura's form factor/scoring), used here only as comparison context, not as claims about the unreleased Apple device.

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-23  MacRumors forum thread comments (recovered via the MacRumors article's embedded top comments after the thread itself 403'd) — split reaction: top comment (27 votes) enthusiastic ("Instant buy from me... I do want this"); second comment (6 votes) skeptical of the report itself ("typical Gurman, throw things at the wall").

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-23  "Apple denial screenless fitness tracker" / TechCrunch Apple-comment check  — no denial found; TechCrunch reached out to Apple, no quoted reply.
- 2026-09-23  Mark Gurman accuracy track record — found a general 86.5% accuracy figure (AppleTrack) and a dissenting MacRumors forum thread ("Is Mark Gurman a con artist?"); NOT used as a spoken claim (too soft/unverifiable as a precise figure), but informs how hard the hedge needs to be — kept hedged throughout rather than stated as fact.
- 2026-09-23  Independent-sourcing check across 6 outlets — confirmed ZERO true independent sources; every outlet traces to the same Bloomberg/Gurman story (see INDEPENDENT-CHECK above).

INDEPENDENT-CHECK: 2026-09-23 — searched 9to5Mac, MacRumors, TechCrunch, Athletech News, PYMNTS,
and The Verge (via Techmeme aggregation, direct fetch blocked) for independent sourcing on the
Apple screenless-tracker claim — found none; every outlet is syndication of one Bloomberg
exclusive. Recorded as single-tier throughout rather than falsely upgraded to multi.
