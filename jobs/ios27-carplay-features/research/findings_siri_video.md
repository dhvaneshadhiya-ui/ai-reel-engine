# Findings: Siri AI in CarPlay (C) + Video apps in CarPlay (D)
Researched 2026-09-28. iOS 27 released 2026-09-14.
Quote caveat: WebFetch returns a model-summarised page; "quotes" below are what it
reported as verbatim. Re-confirm exact wording on the mobile capture before any
quote goes on screen.

## C. Siri AI in CarPlay

- **Apple confirms Siri AI reaches CarPlay.** https://www.apple.com/newsroom/2026/06/apple-introduces-siri-ai-a-profoundly-more-capable-and-personal-assistant/
  "on the go with iPhone, Apple Watch, CarPlay, and AirPods." (PRIMARY, TIER 1)
- **Device requirement: iPhone 15 Pro / 15 Pro Max, all iPhone 16 models or later, iPhone Air, iPhone 17 Pro/Pro Max** (Apple press release device list, same URL). (PRIMARY)
  - MacRumors restates for CarPlay: "available on CarPlay when it is used with an iPhone 15 Pro or newer" https://www.macrumors.com/2026/06/08/new-apple-carplay-features-ios-27/ (VIA Apple WWDC 2026)
  - MacRumors 09-17: needs "iPhone that supports Apple Intelligence" plus waitlist access. https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
- **Language: English only at launch**, more languages "quickly" (Apple press release). (PRIMARY)
- **Region: not initially on iPhone in the EU; unavailable in China** "while Apple works through regulatory requirements" (Apple press release). (PRIMARY) -> a CarPlay user in the EU/China cannot use it.
- **Status: Beta + waitlist.** Join via "Settings ➝ Siri" (MacRumors 09-17, URL above). Waitlist also reported by https://www.macrumors.com/2026/09/15/ios-27-siri-ai-has-waitlist-how-to-join/ , https://9to5mac.com/2026/09/14/ios-27-has-a-waitlist-for-accessing-new-siri-ai/ , https://appleinsider.com/articles/26/09/14/you-need-to-join-the-siri-ai-waitlist-before-you-can-use-it (these three seen as search results only, NOT fetched). The June press release does not mention a waitlist (said "later this year" beta).
- **What it does in the car:** "handles back-and-forth conversation in the car" and chats sync to iPhone's Siri app (MacRumors 09-17). 9to5Mac: "Conversations you have in CarPlay are automatically synced to the Siri app on iPhone." https://9to5mac.com/2026/09/21/heres-everything-new-for-carplay-in-ios-27/
  - 9to5Mac: "much better at answering questions of any kind" (compares to ChatGPT/Gemini) — same URL.
- **Car example from Apple (via MacRumors, from WWDC video):** "ask Siri which trailhead your friend suggested and get the answer instantly" https://www.macrumors.com/2026/06/08/new-apple-carplay-features-ios-27/ (VIA Apple WWDC 2026 keynote/video)
- Other Apple examples (not car-specific, press release): restaurant a friend messaged about; hotel confirmation number from an old email; when a musician is coming to town; what to bring to a potluck. Good in-car candidates: the restaurant/trailhead-from-messages type.
- **CarPlay voice template for third-party apps:** Apple gave devs a "voice control template that any category of CarPlay app can adopt" — "Nothing will change until individual app makers make use of it" (MacRumors 09-17). Announced, dependent on developers.

## D. Video apps in CarPlay

- **Apple developer page (PRIMARY):** https://developer.apple.com/carplay/
  "browse and watch their favorite content in supported cars when parked."
  AirPlay video: watch videos from iPhone on the CarPlay display "when they aren't driving."
  Automakers: "Integrate support for CarPlay with AirPlay video to enable this feature in your car."
- **Two parts:** (1) native CarPlay video apps with browsing (new in iOS 27); (2) AirPlay video from an iPhone app to the car's screen via the AirPlay menu (MacRumors 06-08). 9to5Mac: in iOS 26 video in the car "was limited to AirPlay streaming."
- **Parked-only:** "Playback only works when the vehicle is parked (it switches to audio if you shift into drive)" (MacRumors 09-17). Car must "share its drive state with iOS".
- **Apple's use cases (via MacRumors 06-08, VIA WWDC):** "While waiting in your car at the airport, or charging your electric vehicle"
- **Needs automaker support:** "Available in new vehicles that support it" (MacRumors 06-08, VIA Apple). Automakers must "certify AirPlay video integration for the vehicle"; an "iOS update alone can't enable it" (MacRumors 09-17). 9to5Mac: "won't be available automatically in every car."
- **Automakers: NONE announced.** "As of writing, no manufacturer has announced plans to support the feature" (MacRumors 09-17). => ANNOUNCED BUT NOT USABLE in any car today.
- **Apps:** Apple TV app reported as first confirmed app (search-result summary citing MacRumors guide https://www.macrumors.com/guide/ios-27-carplay/ — NOT fetched, unverified). No third-party video app confirmed in fetched pages.

## Looked for, did NOT find
- apple.com/ios/ios-27/ returned 404 on 2026-09-28 (feature page not captured; try again / mobile capture).
- No Apple September 2026 Siri AI release-day newsroom post fetched; waitlist is sourced to outlets, not Apple.
- **No Apple mention of Gemini** in the June Siri AI press release: it says Apple Foundation Models on device and Private Cloud Compute. The "Gemini-powered" framing in the brief is UNVERIFIED here — do not say it in the script without a source.
- No support.apple.com page on Siri AI in CarPlay or CarPlay video found.
- No named developer entitlement for CarPlay video apps on developer.apple.com/carplay.
- No automaker announcement (kbb, thedrive, pocket-lint not fetched within budget).
- No specific Siri-in-CarPlay-only limits (e.g. whether it needs CarPlay Ultra or works on all CarPlay cars): outlets imply any CarPlay car with a supported iPhone.
