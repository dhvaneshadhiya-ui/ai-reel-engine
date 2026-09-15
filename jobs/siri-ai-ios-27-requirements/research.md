# Research — siri-ai-ios-27-requirements

Claims ledger + search log. `script_approval.py propose` refuses
while placeholders remain; format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: iOS 27 launched September 14, 2026 (the date the "two separate gates" framing below is hung on).
  TIER: official
  SPOKEN: "iOS 27 landed on September 14th, and Apple split it into two separate gates."
  SRC: https://www.apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/
  VIA: Apple newsroom (own announcement)

- CLAIM: Basic Siri AI requires iPhone 15 Pro, iPhone 15 Pro Max, or iPhone 16 and later — not every phone that can run iOS 27.
  TIER: official
  SPOKEN: "Siri AI itself needs an iPhone 15 Pro or newer, so 15 Pro, 15 Pro Max, or any 16 and up."
  SRC: https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/
  VIA: Apple newsroom (own spec)

- CLAIM: iPhone 11 through iPhone 15 and 15 Plus can install iOS 27 but cannot use Siri AI / Apple Intelligence features at all.
  TIER: multi
  SPOKEN: "That includes every iPhone back to the 11, so the software installs almost everywhere."
  SRC: https://9to5mac.com/2026/09/14/here-are-the-requirements-to-get-siri-ai-in-ios-27/
  VIA: 9to5Mac reporting on Apple's published compatibility list
  SRC: https://www.businesstoday.in/latest/trends/photo/apple-ios-27-release-date-supported-iphones-and-siri-ai-requirements-everything-officially-confirmed-so-far-554372-2026-09-09
  VIA: Business Today reporting on the same Apple compatibility list

- CLAIM: The most expressive Siri feature — customizable voice expressivity and pace ("Expressive Voices") — is limited to iPhone 17 Pro and iPhone Air, because it needs a heavier on-device model those phones alone run.
  TIER: multi
  SPOKEN: "The version that actually sounds like it's paying attention, with adjustable pace and expressiveness, needs extra processing only the iPhone 17 Pro or iPhone Air can run."
  SRC: https://www.macrumors.com/guide/ios-27-siri/
  VIA: MacRumors, citing Apple's on-device model split for iPhone 17 Pro / iPhone Air
  SRC: https://www.businesstoday.in/latest/trends/photo/apple-ios-27-release-date-supported-iphones-and-siri-ai-requirements-everything-officially-confirmed-so-far-554372-2026-09-09
  VIA: Business Today, same distinction

- CLAIM: Siri AI is not available in the EU on iPhone or iPad at launch (it IS available on Mac), and is not available in China, for regulatory reasons.
  TIER: official
  SPOKEN: "two regions, the EU and China, don't get it at launch at all, both stuck behind regulatory hurdles Apple hasn't cleared."
  SRC: https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/
  VIA: Apple newsroom (own disclosure)
  SRC: https://www.macrumors.com/guide/ios-27-siri/
  VIA: MacRumors, corroborating the EU-Mac-but-not-iPhone/iPad split

- CLAIM: At launch Siri AI works only with the device language set to English; French, Japanese, Korean, Portuguese, and Spanish are coming "next month" (framed elsewhere as the iOS 27.1 update).
  TIER: multi
  SPOKEN: "It's English-only for now too. French, Japanese, Korean, Portuguese and Spanish arrive next month."
  SRC: https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/
  VIA: Apple newsroom (own timeline, "next month")
  SRC: https://9to5mac.com/2026/09/14/here-are-the-requirements-to-get-siri-ai-in-ios-27/
  VIA: 9to5Mac, same five-language list

- CLAIM: Siri AI is not available to users under 13, with no parental-permission exception.
  TIER: official
  SPOKEN: "Thirteen and up only, no parental workaround."
  SRC: https://9to5mac.com/2026/09/14/here-are-the-requirements-to-get-siri-ai-in-ios-27/
  VIA: 9to5Mac, quoting Apple's own age-gate footnote
  SRC: https://www.macobserver.com/news/siri-ai-age-limit-not-available-users-under-13-2/
  VIA: MacObserver, independently quoting the same Apple line ("Siri AI is not available to users under 13") from footnote 2 of Apple's own September 9 press release

- ADDITIONAL FINDING, NOT SPOKEN: Siri AI (and some other server-side Apple Intelligence features) reportedly carry daily usage caps unless/until a future paid tier launches (AppleInsider, 2026-09-09, "Siri AI will launch in beta, complicated by daily usage caps & future paid access": Apple's own release language says limits "may vary by feature, request complexity, system demand, system policies, and other factors" with no exact numbers, and "expanded access will be available for a fee in the future" with no pricing or date). Not used here because (a) it's a post-access USAGE limit, not an ELIGIBILITY gate, which is what this script is scoped to per structure.md, and (b) Apple has not published a concrete number worth spoken emphasis. Flagged to the user as a possible separate reel.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-15  "iOS 27 Siri AI requirements which iPhone models"  (surfaced Apple's own newsroom post plus 8 outlets covering the same requirements list)
- 2026-09-15  "Apple Intelligence Siri iOS 27 features requirements September 2026"  (confirmed Sept 14, 2026 ship date and the EU/China carve-out)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-15  fetched MacRumors' own guide (`macrumors.com/guide/ios-27-siri`) — independent write-up, not Apple's page, corroborating the device tiers and adding the iPhone 17 Pro / iPhone Air on-device-model detail Apple's own post did not spell out.
- N/A for genuine hands-on usage testing — the reel airs the day of/right after launch (iOS 27 shipped 2026-09-14, this research ran 2026-09-15), before independent reviewers have had time to publish usage impressions of Siri AI itself. The claims here are compatibility/eligibility facts, not quality/performance claims, so this gap does not weaken what's spoken.

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- N/A — same timing gap as above; no meaningful user-reaction corpus exists yet less than 24 hours after launch. Nothing in the script claims a reaction, so nothing here needed hedging.

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-15  "iOS 27 Siri AI 12GB RAM requirement"  — a search-engine summary asserted a 12GB RAM floor for Expressive Voices/advanced dictation, but neither of two full-article fetches (9to5Mac, Tom's Guide) that should have carried that detail actually contained it. Could not confirm from a real article body. Treated as unconfirmed and NOT spoken — see structure.md WHAT WAS CUT.
- 2026-09-15  checked TechRadar's compatibility explainer for a contradicting device list — page returned only a paywall/signup shell, no contradicting figures found, dropped as a source.

INDEPENDENT-CHECK: 2026-09-15 searched for hands-on/independent testing or user reaction to Siri AI in iOS 27 — found none published yet (device shipped less than 24 hours before this research). All claims here are eligibility/compatibility facts sourced to Apple's own newsroom post plus independent outlets (9to5Mac, MacRumors, Business Today) reporting the same published compatibility list, not performance claims that would need a hands-on check.
