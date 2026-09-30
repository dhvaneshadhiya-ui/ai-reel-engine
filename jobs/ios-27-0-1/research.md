# Research — ios-27-0-1

Claims ledger + search log. Apple's own release notes (Apple Support 149076)
and security page (100100) are the spine; outlets add the trigger detail
(Passwords app) and the "software, not hardware" point.

## CLAIMS

- CLAIM: iOS 27.0.1 was released 2026-09-28, the first update to iOS 27 (released 2026-09-14), with three listed bug fixes.
  TIER: official
  SPOKEN: "Apple just shipped iOS twenty seven point oh point one, the first update to iOS 27. It fixes three bugs."
  SURPRISE: 30
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes ("This update provides bug fixes for your iPhone, including fixes for the following issues")
  SRC: https://support.apple.com/en-us/100100
  VIA: Apple security releases table (iOS 27.0.1, 28 Sep 2026; iOS 27, 14 Sep 2026)
  SRC: https://www.macrumors.com/2026/09/28/apple-releases-ios-27-0-1/
  VIA: MacRumors' own report

- CLAIM: Two of the three fixes apply only to iPhone 18 Pro / Pro Max; the Notification Center + Control Center fix applies to all iPhones.
  TIER: official
  SPOKEN: "Two only hit one iPhone. The third could hit yours."
  SURPRISE: 60
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes (device named per line)
  SRC: https://9to5mac.com/2026/09/28/apple-releases-ios-27-0-1-for-iphone-heres-whats-new/
  VIA: 9to5Mac ("the Notification Center/Control Center issue affecting all iPhone models")

- CLAIM: iPhone 18 Pro / Pro Max may unexpectedly restart when Face ID fails to authenticate; fixed in 27.0.1.
  TIER: official
  SPOKEN: "When Face ID failed inside an app like Passwords, some of them froze and restarted."
  SURPRISE: 55
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes
  SRC: https://www.theapplepost.com/2026/09/24/72642/apple-confirms-fix-is-coming-for-iphone-18-pro-face-id-reboot-bug/
  VIA: The Apple Post (occurs when Face ID fails inside apps; freeze, then reboot)
  SRC: https://www.idropnews.com/news/apple-releases-ios-27-0-1-iphone-18-pro-face-id-fix/268975
  VIA: iDrop News (Passwords app, Safari private tabs, "Try Face ID Again" -> freeze -> reboot)

- CLAIM: The Face ID restart was a software problem; a replaced phone did not help and no hardware replacement is needed.
  TIER: multi
  SPOKEN: "That was a software bug, so you don't need a new phone."
  SURPRISE: 65
  SRC: https://www.theapplepost.com/2026/09/24/72642/apple-confirms-fix-is-coming-for-iphone-18-pro-face-id-reboot-bug/
  VIA: The Apple Post ("this is a software issue, no hardware replacement is necessary")
  SRC: https://www.idropnews.com/news/apple-releases-ios-27-0-1-iphone-18-pro-face-id-fix/268975
  VIA: iDrop News (users who exchanged phones saw it recur)
  SRC: https://9to5mac.com/2026/09/28/apple-releases-ios-27-0-1-for-iphone-heres-whats-new/
  VIA: Apple confirmation to 9to5Mac that a software update fixes it

- CLAIM: A color artifact may appear on photos captured at 2x under certain lighting at f/1.48 on a small number of iPhone 18 Pro / Pro Max devices; fixed. (f/1.48 is the widest aperture of the 18 Pro's variable aperture.)
  TIER: official
  SPOKEN: "some 2x photos, shot at the widest aperture in certain light, came out with a color glitch. Apple says only a small number of phones had it."
  SURPRISE: 50
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes
  SRC: https://www.photographytalk.com/iphone-18-pro-green-flare/
  VIA: PhotographyTalk (f/1.48 is the widest setting of the new variable aperture)

- CLAIM: Opening Notification Center and Control Center simultaneously may cause the touchscreen to become unresponsive; fixed, all iPhones on iOS 27.
  TIER: official
  SPOKEN: "pull down Notification Center and Control Center together, and your screen could stop responding to touch"
  SURPRISE: 70
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes
  SRC: https://www.gizbot.com/mobile/news/your-iphone-freezing-on-ios-27-bug-fix-coming-128829.html
  VIA: Gizbot (swipe NC from top left, CC from top right; phone appears frozen)

- CLAIM: iOS 27.0.1 has no published CVE entries (no listed security fixes).
  TIER: official
  SPOKEN: "Apple lists no security fixes, so there's no rush."
  SURPRISE: 60
  SRC: https://support.apple.com/en-us/100100
  VIA: Apple security releases ("This update has no published CVE entries.")
  ONE-SOURCE-OK: Apple's own security table is the only authority on what Apple patched.

- CLAIM: Update path: Settings > General > Software Update.
  TIER: official
  SPOKEN: "It's in Settings, General, Software Update."
  SURPRISE: 10
  SRC: https://support.apple.com/en-us/118575
  VIA: Apple Support "Update your iPhone"
  SRC: https://www.macrumors.com/2026/09/28/apple-releases-ios-27-0-1/
  VIA: MacRumors

## FEATURES + HOW TO USE

Everything in Apple's iOS 27.0.1 notes (Apple Support 149076) — no new features:
- Face ID failure restart fix (iPhone 18 Pro / Pro Max) — USED (item 1)
- 2x color artifact at f/1.48 fix (iPhone 18 Pro / Pro Max, small number) — USED (item 2)
- Notification Center + Control Center unresponsive touch fix (all iPhones) — USED (item 3, the open loop's payoff)
- Security content: none published — USED (the "should you update" answer)
- iPadOS / visionOS / watchOS / macOS 27.0.1 same day — CUT: not an iPhone viewer's question
- iOS 26.7.1 for phones staying on iOS 26 — CUT: different audience, time
- Build 24A446 — CUT: nobody asks

HOW TO: Settings > General > Software Update > Update Now (Apple Support 118575).

## NOT CLAIMED

- "Green flare" as the name of Apple's color artifact: outlets link the two, Apple only says "color artifact". Not said; no user flare photos shown.
- The NC + CC freeze as a "prank": Gizbot framing only. Not said.
- Face ID hardware cause (under-display IR camera): speculation. Not said.
- Other iOS 27 bugs (indexing battery drain, keyboard lag, touch loss after restore): reported, not in 27.0.1's notes. Not claimed fixed.
- Any count of affected phones: none published.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-29  "iOS 27.0.1 released what's new"  (released 2026-09-28, three fixes)
- 2026-09-29  "support.apple.com About iOS 27 Updates 27.0.1"  (fetched 149076: release notes verbatim)
- 2026-09-29  fetched support.apple.com/en-us/100100  (no published CVE entries)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-29  "iPhone 18 Pro Face ID not available Apple confirms software update fix"  (The Apple Post, 9to5Mac confirmation, trigger inside apps)
- 2026-09-29  "iPhone 18 Pro f/1.48 2x photo color artifact"  (PhotographyTalk / Jiemian: flare at f/1.48 + 2x in dim warm light)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-29  "iOS 27.0.1 users report after update still Face ID reboot battery"  (users swapped phones and the bug recurred; indexing battery complaints persist, not fixed)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-29  fetched Gizbot "not one bug, it is three, and only one has a fix coming" (pre-release; Apple's final notes DO include the NC+CC fix, so it is superseded)
- 2026-09-29  "Apple iOS 27.0.1 update bug fixes security notes" (confirms no CVEs; no claim of security fixes anywhere)

INDEPENDENT-CHECK: 2026-09-29 searched user reports and hands-on coverage of the Face ID reboot and the 2x artifact — found The Apple Post / iDrop News on the in-app trigger and phone swaps, PhotographyTalk on the f/1.48 flare.
