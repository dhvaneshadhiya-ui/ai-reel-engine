# Research — ios27-battery-drain

Claims ledger + search log. Built 2026-09-19 from four parallel research agents
(`research/plan.md`, `research/findings_*.md`, `research/visuals.md`).
Tiers: official / multi / single / disputed.

## CLAIMS

- CLAIM: Apple documents that after an update, background tasks keep running and
  affect battery life and thermal performance.
  TIER: official
  SPOKEN: "After an update, tasks keep running in the background, and they hit battery life and heat."
  SURPRISE: 55
  SRC: https://support.apple.com/en-us/120745
  SRC: https://support.apple.com/en-us/125039
  VIA: Apple's own support documentation (120745 last updated 2026-09-17)

- CLAIM: Apple names the work: indexing data and files for search, downloading new
  assets, and updating apps.
  TIER: official
  SPOKEN: "Your phone is indexing your stuff for search, downloading new assets, and updating apps."
  SURPRISE: 62
  SRC: https://support.apple.com/en-us/120745
  SRC: https://support.apple.com/en-us/125039
  VIA: Apple support text, quoted independently by macobserver.com and 9to5mac.com

- CLAIM: Apple publishes NO duration. Its wording is "wait a few days and then check
  again"; no hour or day count appears anywhere.
  TIER: official
  SPOKEN: "Not four days, not seventy-two hours. Apple's actual words are, wait a few days, then check again."
  SURPRISE: 84
  SRC: https://support.apple.com/en-us/120745
  SRC: https://www.macobserver.com/news/apple-few-days-to-settle-after-update-no-number/
  VIA: Apple support page; Mac Observer checked the page for a figure independently

- CLAIM: Every confident number circulating about iOS 27 battery drain comes from
  somewhere other than Apple.
  TIER: multi
  SPOKEN: "So every confident number you've read came from somewhere other than Apple."
  SURPRISE: 88
  TIER-NOTE: rests on a verified ABSENCE, not on one outlet's opinion.
  SRC: https://support.apple.com/en-us/120745
  SRC: https://www.macobserver.com/tips/round-ups/ios-27-battery-drain-what-apple-has-published/
  VIA: Apple's own page, fetched 2026-09-19, carries no hour or day figure anywhere
  VIA: Mac Observer reached the same conclusion independently on 2026-09-11, auditing
       Apple's published iOS 27 material before the release

- CLAIM: The same post-update battery complaint wave arrived in September 2025 (iOS 26)
  and in 2024 (iOS 18), quoting the same Apple sentence.
  TIER: multi
  SPOKEN: "Same week last September, iOS 26 drained batteries and got the same sentence from Apple. The year before, iOS 18."
  SURPRISE: 72
  SRC: https://osxdaily.com/2025/09/18/ios-26-battery-life-suffering-heres-why/
  SRC: https://www.techradar.com/phones/iphone/youre-not-alone-many-users-are-reporting-iphone-16-battery-life-issues-on-ios-18
  VIA: OS X Daily's own 2025 reporting of the iOS 26 wave
  VIA: TechRadar's own 2024 reporting of the iOS 18 wave — a different year, a different
       newsroom, neither citing the other

- CLAIM: Settings > Battery can show an Insight naming the cause: "Ongoing iOS Update:
  A recent software update is finishing in the background."
  TIER: official
  SPOKEN: "If a note says a recent update is still finishing in the background, that's your answer."
  SURPRISE: 78
  SRC: https://support.apple.com/en-us/120745
  VIA: Apple support page, which also says where to look ("if you open Settings and tap
       Battery, you might see the Insight")

- CLAIM: Apple's software chief Craig Federighi, asked whether he force quits apps and
  whether it preserves battery, answered "No and no."
  TIER: single
  SPOKEN: "Apple's software chief was once asked if he force quits apps to save battery, and he said, no and no."
  SURPRISE: 86
  TIER-NOTE: one ultimate source — Federighi's email — so the line attributes it out
  loud ("Apple's software chief was once asked") rather than stating it as a finding.
  SRC: https://daringfireball.net/2017/07/you_should_not_force_quit_apps
  SRC: https://www.cnbc.com/2017/07/20/stop-quitting-apps-on-your-iphone-and-ipad-its-making-things-worse.html
  VIA: Federighi's own email reply, first published by Daring Fireball (2017-07-20)

- CLAIM: Maximum Capacity is a chemical-age measure defined across charge cycles —
  Apple rates iPhone 14 and earlier to 80% at 500 cycles, iPhone 15 and later to 1000.
  TIER: official
  SPOKEN: "maximum capacity is measured across hundreds of charge cycles, and one rough week can't move it."
  SURPRISE: 68
  SRC: https://support.apple.com/en-us/101575
  VIA: Apple's iPhone battery and performance page

- CLAIM: iOS 27 shipped 2026-09-14 and 27.0 is still the only build as of 2026-09-19.
  TIER: official
  SPOKEN: "since iOS 27"
  SURPRISE: 35
  SRC: https://support.apple.com/en-us/149076
  SRC: https://support.apple.com/en-us/100100
  VIA: Apple's "About iOS 27 Updates" page and the security releases index — one iOS 27
       row on each. (Not spoken as a date; it is why the script offers no "wait for the
       fix" advice.)

## NOT CLAIMED

Found in the coverage, deliberately NOT said in this reel:

- **"iOS 27 is worse than usual because it re-indexes your device for Siri AI."**
  9to5Mac's own inference (2026-09-15), carrying no source; Mac Observer's audit
  contradicts it in spirit ("Apple does not name one. No specific process is
  identified"). Apple documents the Spotlight/Photos/Mail search rebuild but never ties
  it to battery.
- **Any figure for how many people are affected**, including "millions" (UNILAD Tech's
  headline, extrapolated from install base).
- **"83% to 37% in ninety minutes."** One Reddit post, quoted through one outlet. The
  only concrete number in the entire coverage, and it is one person.
- **"3 to 5 days" / "about 4 days" / "24 to 48 hours."** Untraceable, or beta-tester
  reports on pre-release builds.
- **"Apple has acknowledged the problem."** It has not. No newsroom item, no statement,
  no iOS 27 battery document. The quoted text is a generic page updated 2026-09-17.
- **"A fix is coming in iOS 27.0.1."** No such build exists as of 2026-09-19; outlets
  only predict one.
- **"Turn off 5G to fix it."** 5G genuinely costs power (~6-11% vs LTE in cited tests),
  so calling it a myth would be wrong — but it is steady-state cost, not this story's
  cause. Cut rather than mis-say.
- **Photos face/scene re-analysis, app re-optimisation, iCloud re-sync as causes.**
  Outlet-asserted, no primary source.
- **Any iOS 27 Battery screen screenshot.** Apple's only public Battery screenshot is an
  iOS 26 iPhone 16 Pro image; Rule 3 forbids it standing in for an iOS 27 screen. A
  reported "Optimizing Search and Siri" progress banner in iOS 27 is unconfirmed in
  Apple's words, and we have no iOS 27 device to capture — so no iPhone UI is shown as
  a receipt. The receipts are Apple's own support pages.

## FIELD NOTE (user, 2026-09-19)

Apple's 120745 describes Settings > Battery > **Power Mode** > Low Power Mode as the
path. The user's own iPhone has no Power Mode row — Adaptive Power needs an Apple
Intelligence-capable iPhone, so on other models Low Power Mode remains its own toggle.
The script never speaks that path; do not repeat Apple's wording as if it is universal.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-19  "apple support battery drains quickly after update"  (Apple's wording:
  "wait a few days and then check again"; background tasks affect battery AND heat;
  the Ongoing iOS Update Insight exists)
- 2026-09-19  "About iOS 27 Updates" + Apple security releases index  (iOS 27 shipped
  2026-09-14; 27.0 is the only build; no 27.0.1)
- 2026-09-19  Apple Newsroom September 2026  (no iOS 27 battery item; /newsroom/2026/09/
  returns 404 — Apple has said nothing)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-19  "iOS 27 battery drain benchmark / screen-on time test"  (NOTHING. No
  outlet has measured this. No percentage, no delta, no benchmark)
- 2026-09-19  MacRumors / Verge / Tom's Guide / iMore / ZDNet post-release coverage
  (none found — the major outlets have not picked the story up)
- 2026-09-19  MacRumors iOS 27 battery thread  (HTTP 403, unread; treated as unverified,
  and it is mostly beta testers in any case)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-19  Reddit / Apple Support Communities "iOS 27 battery"  (audience language
  only: "Battery drain is soo bad", 83% to 37% in 90 minutes, iPhone 16 Pro Max. Apple
  Communities' big threads are iOS 26 / 2025, not iOS 27 — last year's wave)
- 2026-09-19  "iOS 27 battery life thread" forums  (beta-era posts; one tester reported
  the final release build was fine, which cuts against the panic)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run to prove the story wrong
- 2026-09-19  "iOS 27 battery bug confirmed / affected model / 27.0.1 fix"  (no
  confirmed bug, no named model, no fix shipped — so "don't panic" survives)
- 2026-09-19  "iOS 27 battery drain still bad after two weeks"  (no credible
  multi-week case found; the absence is unverified, not proof of none)
- 2026-09-19  "is post-update drain actually normal / does it ever not recover"
  (Mac Observer: "Nothing on the page says drained battery life will fully recover" —
  which is why the script ends on a re-check, not a promise)

INDEPENDENT-CHECK: 2026-09-19 searched for independent measurement of iOS 27 battery
drain — benchmarks, screen-on-time tests, outlet hands-on. Found NOTHING measured by
anyone. What exists independently is Mac Observer's audit of what Apple did and did not
publish (2026-09-11/12, predating both the release and 9to5Mac), UNILAD Tech's separately
sourced user reports (2026-09-16), and two prior-year waves (OS X Daily 2025, TechRadar
2024). The script therefore claims no magnitude at all — only what Apple documents, what
nobody has measured, and what recurs every year.
