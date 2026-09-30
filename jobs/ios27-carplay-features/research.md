# Research — ios27-carplay-features

Claims ledger + search log. Findings files in `research/` (plan.md,
findings_scrub_widgets.md, findings_siri_video.md,
findings_maps_wireless_honesty.md, visuals.md). Apple has published no
CarPlay page for iOS 27 (apple.com/ios/ios-27/ returned 404 on 2026-09-28,
apple.com/carplay not updated), so the feature list rests on outlet testing
plus Apple's own Siri AI release and CarPlay developer page. Quotes came
through a summarising fetch; recheck wording on the mobile capture before any
quote goes on screen.

## CLAIMS

- CLAIM: iOS 27 is out (released 2026-09-14) and brings new CarPlay features; four of the five in this reel work in any CarPlay car, video needs the car.
  TIER: multi
  SPOKEN: "Four work in your car today. One, no car on the road can use yet."
  SURPRISE: 70
  SRC: https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
  VIA: MacRumors' own sorting ("Works in Any CarPlay Vehicle" / "Needs the Right Car")
  SRC: https://www.pocket-lint.com/ios-27-new-carplay-features-availability/
  VIA: Pocket-lint's own availability breakdown

- CLAIM: CarPlay gets 14 new wave-style wallpapers matching iOS 27's, and app icons refreshed with updated Liquid Glass designs; works in any CarPlay car.
  TIER: multi
  SPOKEN: "fourteen new wave wallpapers matching iOS 27, and app icons redrawn in Liquid Glass"
  SURPRISE: 40
  SRC: https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
  VIA: MacRumors ("New wave designs found in iOS 27 and macOS 27 ... in 14 color options")
  SRC: https://9to5mac.com/2026/09/21/heres-everything-new-for-carplay-in-ios-27/
  VIA: 9to5Mac's own use ("App icons have been refreshed with updated Liquid Glass designs")

- CLAIM: The wallpaper is chosen on the car's screen: CarPlay Settings app > Wallpaper.
  TIER: official
  SPOKEN: "Pick one in CarPlay's own Settings, under Wallpaper."
  SURPRISE: 35
  SRC: https://support.apple.com/guide/iphone/change-settings-in-carplay-iph6ade13329/ios
  VIA: Apple Support iPhone User Guide
  SRC: https://www.howtogeek.com/690321/how-to-change-your-carplay-wallpaper/
  VIA: How-To Geek walkthrough (Settings > Wallpaper on the head unit)

- CLAIM: Now Playing has a draggable progress bar (audio scrubbing) for music, podcasts and audiobooks; previously you could only skip.
  TIER: multi
  SPOKEN: "you can finally drag the progress bar to any point in a podcast or audiobook, instead of tapping skip"
  SURPRISE: 55
  SRC: https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
  VIA: MacRumors ("drag to any point in a song or podcast rather than tap skip")
  SRC: https://9to5mac.com/2026/09/21/heres-everything-new-for-carplay-in-ios-27/
  VIA: 9to5Mac's own use ("audio scrubbing on the Now Playing screen ... audiobooks, or podcasts")
  SRC: https://www.kbb.com/car-news/apples-new-ios-27-brings-a-host-of-updates-to-carplay/
  VIA: KBB

- CLAIM: Apple's new Siri AI works in CarPlay, conversationally; Apple's in-car example is asking which trailhead a friend suggested.
  TIER: official
  SPOKEN: "Siri AI rides along. Ask it which trailhead your friend suggested, then keep talking."
  SURPRISE: 45
  SRC: https://www.apple.com/newsroom/2026/06/apple-introduces-siri-ai-a-profoundly-more-capable-and-personal-assistant/
  VIA: Apple Newsroom ("on the go with iPhone, Apple Watch, CarPlay, and AirPods")
  SRC: https://www.macrumors.com/2026/06/08/new-apple-carplay-features-ios-27/
  VIA: Apple WWDC 2026 ("ask Siri which trailhead your friend suggested")
  SRC: https://9to5mac.com/2026/09/21/heres-everything-new-for-carplay-in-ios-27/
  VIA: 9to5Mac's own use (CarPlay conversations sync to the Siri app)

- CLAIM: Siri AI needs iPhone 15 Pro / 15 Pro Max, iPhone 16 or later, or iPhone Air; access may start on a waitlist.
  TIER: official
  SPOKEN: "It needs an iPhone 15 Pro or later, and there may be a waitlist."
  SURPRISE: 55
  SRC: https://www.apple.com/newsroom/2026/06/apple-introduces-siri-ai-a-profoundly-more-capable-and-personal-assistant/
  VIA: Apple Newsroom device list
  SRC: https://support.apple.com/en-us/127893
  VIA: Apple Support (waitlist; "wait times can vary")
  SRC: https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
  VIA: MacRumors ("there's a Siri AI waitlist to get access")

- CLAIM: Wireless CarPlay connections are more dependable in iOS 27, with improved GPS accuracy and navigation heading detection (Apple's claim; no figures published).
  TIER: multi
  SPOKEN: "Apple says wireless CarPlay is more dependable now, with sharper GPS heading, so the map knows which way you're facing"
  SURPRISE: 60
  SRC: https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
  VIA: Apple, relayed ("improved GPS accuracy and navigation heading detection")
  SRC: https://www.pocket-lint.com/ios-27-new-carplay-features-availability/
  VIA: Apple, relayed ("better GPS accuracy for navigational headings")

- CLAIM: CarPlay now supports video apps (browse and watch) and AirPlay video, only when the car is parked; playback falls back to audio in drive.
  TIER: official
  SPOKEN: "video apps, only while you're parked"
  SURPRISE: 50
  SRC: https://developer.apple.com/carplay/
  VIA: Apple developer page ("in supported cars when parked")
  SRC: https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
  VIA: MacRumors ("switches to audio if you shift into drive")

- CLAIM: Video needs the automaker to certify AirPlay video for the car (an iOS update alone cannot enable it), and as of mid-September no automaker has announced support.
  TIER: multi
  SPOKEN: "Your carmaker has to enable it, and so far none has said it will."
  SURPRISE: 85
  SRC: https://developer.apple.com/carplay/
  VIA: Apple ("Integrate support for CarPlay with AirPlay video to enable this feature in your car")
  SRC: https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/
  VIA: MacRumors ("no manufacturer has announced plans to support the feature")
  SRC: https://9to5mac.com/2026/09/21/heres-everything-new-for-carplay-in-ios-27/
  VIA: 9to5Mac ("won't be available automatically in every car")

## FEATURES + HOW TO USE

Every iOS 27 CarPlay change found (MacRumors guide + "which work", 9to5Mac, Pocket-lint):
- New wave wallpapers (14 colours) + Liquid Glass icon refresh — USED (item 1; any car; CarPlay Settings > Wallpaper)
- Audio scrubbing on Now Playing — USED (item 2; any car; just drag the bar)
- Siri AI in CarPlay — USED (item 3; iPhone 15 Pro or later, English, not EU/China, waitlist)
- Wireless reliability + GPS accuracy/heading — USED (item 4; any car, phone-side)
- Video apps + AirPlay video when parked — USED as the exception (item 5; needs automaker certification, none announced)
- MiniPlayer in media apps — CUT: a smaller cousin of scrubbing; time
- Apple Music library filters — CUT: minor
- Natural-language Maps directions (avoid tolls/highways) — CUT: one outlet, overlaps Siri
- Route data to the car's built-in nav / instrument cluster — CUT: needs car support, would blur the single exception
- Voice control template for any app category — CUT: depends on developers, nothing visible today
- Third-party widgets — CUT: not new (iOS 26)

HOW TO: nothing to enable for items 1, 2, 4 beyond updating to iOS 27; Siri AI is
turned on at Settings > Siri > Try Siri AI (Beta) on the iPhone (Apple Support 127893).

## NOT CLAIMED

- Third-party / any-app widgets as NEW in iOS 27: MacRumors' 09-17 piece says so, but iDownloadBlog (2025-11-24) documents third-party CarPlay widgets in iOS 26, MacRumors' own iOS 27 guide lists no widget change, and Apple's WWDC26 session 212 "Rev up your CarPlay app" (youtube ykwG0I8UGjg, 01:07) describes widgets and Live Activities from any app as something CarPlay ALREADY supports. Not new; cut from the list.

- Gemini powering Siri AI: Apple's release says Apple Foundation Models + Private Cloud Compute and names no Gemini. Not said.
- Apple TV as the first CarPlay video app: search-summary only. Not said.
- Any number for the wireless/GPS improvement: none published. Said as "Apple says".
- "Celosia" wallpaper name: search summary only.
- Natural-language Maps directions work without Apple Intelligence: unverified; the feature itself is cut.
- Pocket-lint's "Siri AI available now" (no waitlist): contradicted by Apple Support 127893; script hedges "you may".

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-28  "iOS 27 CarPlay new features"  (feature set: scrubbing, widgets, video, Siri AI, wireless, Maps, wallpapers)
- 2026-09-28  "Apple iOS 27 CarPlay newsroom September 2026"  (no Apple CarPlay newsroom text; release date 2026-09-14)
- 2026-09-28  "apple.com newsroom June 2026 iOS 27 CarPlay widgets"  (CarPlay features were a keynote slide only; Apple never detailed them)
- 2026-09-28  fetched apple.com/newsroom Siri AI release, developer.apple.com/carplay, apple.com/ios/ios-27 (404), apple.com/carplay (not updated)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-28  "iOS 27 CarPlay third-party widgets any widget dashboard"  (geeky-gadgets via HotShotTek hands-on; MacRumors testing)
- 2026-09-28  "CarPlay widgets Settings General CarPlay ..." + fetched idownloadblog 2025-11-24 (third-party CarPlay widgets already in iOS 26 — widget claim dropped)
- 2026-09-28  "Apple Support change wallpaper in CarPlay"  (Apple Support: CarPlay Settings > Wallpaper)
- 2026-09-28  fetched 9to5mac.com everything-new-in-CarPlay (own use: scrubbing, MiniPlayer, Siri AI sync, wallpapers)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-28  "If you can't access some of iOS 27's new CarPlay features" (pocket-lint: confusion over car-dependent features — the angle of this reel); MacRumors Forums thread "Which iOS 27 CarPlay features actually work in your car" surfaced (title only)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-28  "iOS 27 CarPlay video automaker support announced" / gotechtor "features that almost no car can actually use yet"  (no automaker announcement found; confirms the exception)

INDEPENDENT-CHECK: 2026-09-28 searched hands-on coverage of iOS 27 CarPlay — found 9to5Mac's own use, MacRumors' per-feature testing, Geeky Gadgets relaying HotShotTek's in-car video, and Pocket-lint's availability test.
