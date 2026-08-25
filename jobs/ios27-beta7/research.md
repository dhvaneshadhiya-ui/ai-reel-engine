# Research — ios27-beta7

Claims ledger + search log. Format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: Apple released the seventh developer beta of iOS 27 (and iPadOS 27)
  on August 24, 2026, one week after beta 6.
  TIER: multi
  SPOKEN: "one week after beta six"
  SRC: https://www.macrumors.com/2026/08/24/apple-seeds-ios-27-beta-7/
  VIA: MacRumors' own report of the seed, dated the same day.
  SRC: https://9to5mac.com/2026/08/24/ios-27-beta-7/
  VIA: 9to5Mac's own report of the seed, dated the same day, independent
       writeup naming the same beta number and date.

- CLAIM: This late in the cycle, beta 7 brings no new consumer features —
  every outlet covering the seed frames it as bug fixes and stability work
  instead.
  TIER: multi
  SPOKEN: "no new features this week"
  SRC: https://9to5mac.com/2026/08/24/ios-27-beta-7/
  VIA: 9to5Mac's own reporting on the beta-7 seed.
  SRC: https://www.macrumors.com/2026/08/24/apple-seeds-ios-27-beta-7/
  VIA: MacRumors' own reporting: "Apple is now focused primarily on bug
       fixes and stability improvements ahead of the official release
       expected in a few weeks."
  SRC: https://www.macworld.com/article/3172166/ios-27-beta-updates-features-release-date.html
  VIA: Macworld's own beta tracker, updated August 24, 2026, describing
       beta 6 as fine-tuning animations/interface behaviour and performance,
       and beta 7 as expected to bring "similar small refinements."

- CLAIM: The public release is expected within a few weeks of beta 7 (widely
  reported as September 2026); no source names an exact date.
  TIER: multi
  SPOKEN: "weeks from release"
  SRC: https://9to5mac.com/2026/08/24/ios-27-beta-7/
  VIA: 9to5Mac's own reporting: beta 7 "will likely become public beta 5"
       with "final release expected in September 2026."
  SRC: https://www.macworld.com/article/3172166/ios-27-beta-updates-features-release-date.html
  VIA: Macworld's own beta tracker: "only a month or less before the
       general release," as of August 24, 2026.

- CLAIM: Apple's own beta-7 release notes list a fix so a ringing alarm can
  now be stopped from the Lock Screen without unlocking the device.
  TIER: official
  SPOKEN: "you couldn't stop a ringing alarm without unlocking your phone"
  SRC: https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes
  VIA: Apple's own release notes, Clock section, Resolved Issues: "Fixed:
       You might be unable to stop a ringing alarm from the lock screen
       without unlocking your device." (177728602)

- CLAIM: Apple's own beta-7 release notes list a fix for Camera app Portrait
  mode, where the blur effect could render incorrectly on photos.
  TIER: official
  SPOKEN: "the blur was rendering wrong on photos"
  SRC: https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes
  VIA: Apple's own release notes, Camera section, Resolved Issues: "Fixed:
       In the Camera app, Portrait mode blur effect might render
       incorrectly for photos." (177335723)

- CLAIM: Apple's own beta-7 release notes list a fix so the newer American
  English Siri voices no longer silently fall back to the legacy voice when
  the phone overheats or is in Low Power Mode.
  TIER: official
  SPOKEN: "was reverting to the old one whenever your phone overheated"
  SRC: https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes
  VIA: Apple's own release notes, Siri section, Resolved Issues: "Fixed:
       New American English Siri voices 6 and 7 might default to legacy
       US voices when your device is overheated or in Low Power Mode."
       (177742977)

- CLAIM: As of beta 7, Apple's release notes document an on-device dictation
  model users can enable for better accuracy via a Keyboard-settings toggle.
  TIER: official
  SPOKEN: "a toggle waiting in Keyboard settings"
  SRC: https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes
  VIA: Apple's own release notes, Dictation section, New Features:
       "Dictation can now be powered by a new on-device model that boosts
       accuracy. To enable this, go to Keyboard settings > Dictation and
       Toggle on 'Advanced Dictation Preview'." (178444388) — presented as a
       standing capability of the 27 SDK as documented at beta 7, not
       claimed here as new IN this specific beta increment.

## EXPLICITLY NOT CLAIMED

- No claim about the Siri AI feature itself, its device-tier availability,
  or the EU rollout — that story was already told in full in the
  `ios27-tiers` reel (published). Repeating it here would violate the
  "never repeat the last reel's treatment for the same kind of information"
  rule; this reel is deliberately scoped to the BETA 7 release itself.
- No exact Release Candidate date or iPhone-event date is stated — no
  source consulted names one for iOS 27; only "a month or less" / "a few
  weeks" language, which is why the script says "weeks away," never a date.
- No claim that beta 7 introduces brand-new consumer features — every
  outlet consulted agrees it does not; the script states this as the
  contrast that makes the reel honest ("no new features this week").
- The hundreds of developer-only API fixes on Apple's release-notes page
  (CarPlay APIs, SwiftUI, StoreKit, Metal, MetricKit, RealityKit, etc.) are
  real but not spoken — meaningless to a viewer holding a phone, not a
  developer machine.
- The exact build number (24A5424a, replacing 24A5418b) is not spoken —
  a string of characters carries no meaning read aloud. Real and
  official-tier if it's wanted later as an on-screen-only label on a
  receipt card, but it is not a claim this script makes.

## SEARCHED

- 2026-08-25  "iOS 27 beta 7 changes new features August 24 2026"  (found
  AppleInsider, Macworld, MacObserver, Appleosophy writeups; confirmed build
  24A5424a and the "stability pass" framing across three independent outlets)
- 2026-08-25  "\"iOS 27 beta 7\" 9to5mac what's new"  (confirmed 9to5Mac's
  own beta-7 piece plus its "September 2026" release framing)
- 2026-08-25  fetched developer.apple.com official release notes directly
  in-browser (WebFetch could not render the JS page; the Browser pane's
  get_page_text pulled the full text) — this is the primary source for every
  specific bug-fix claim used in the script.
