# Research — carplay-youtube-free

Claims ledger + search log. Tiers: official / multi / single / disputed.
A single or disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: YouTube has no CarPlay video app; officially only YouTube Music (audio) is on CarPlay
  TIER: multi
  SPOKEN: "YouTube has no CarPlay app"
  SURPRISE: 45
  SRC: https://cartechstudio.com/blogs/in-vehicle-apps/youtube-on-carplay
  SRC: https://carpuride.com/blogs/news/how-to-watch-youtube-on-carplay
  VIA: cartechstudio ("there is no official YouTube CarPlay app, and there never has been"), read 2026-10-09
  VIA: carpuride guide, independent outlet, same conclusion (YouTube needs a workaround on CarPlay)

- CLAIM: CarTV mirrors the whole iPhone screen to the car display, from any app, even apps without a Cast button
  TIER: official
  SPOKEN: "puts your whole iPhone screen on your car's display"
  SURPRISE: 85
  SRC: https://apps.apple.com/us/app/cartv-m3u-iptv-player-cast/id6800211040
  SRC: https://cartv.app/
  VIA: developer's App Store description ("Put your whole iPhone screen on the car display: works with any app, even ones without a Cast button"), read 2026-10-09
  ONE-SOURCE-OK: this is the developer's own documented feature, confirmed on screen by our own filmed test; independent hands-on is the Gadget Gig demo (reference) and App Store reviews ("cast my screen", Sep 24 2026).

- CLAIM: The mirroring works with any app, including ones that have no Cast button
  TIER: official
  SPOKEN: "It works with any app, even ones without a cast button"
  SURPRISE: 55
  SRC: https://apps.apple.com/us/app/cartv-m3u-iptv-player-cast/id6800211040
  VIA: App Store description, verbatim wording
  ONE-SOURCE-OK: developer's own feature statement; shown working with YouTube in our filmed test.

- CLAIM: No adapter box is needed: an iPhone and a CarPlay car are all it takes
  TIER: official
  SPOKEN: "with no adapter box"
  SURPRISE: 60
  SRC: https://cartv.app/
  SRC: https://cartechstudio.com/blogs/in-vehicle-apps/youtube-on-carplay
  VIA: cartv.app FAQ ("An iPhone and a car with CarPlay"); cartechstudio describes the usual route as a plug-in Android AI box

- CLAIM: The app is listed as "CarTV - M3U IPTV Player & Cast" by Lyntra Technology Ltd, free with in-app purchases, iOS 18 or later
  TIER: official
  SPOKEN: "Install the one called CarTV, M3U IPTV Player and Cast"
  SURPRISE: 10
  SRC: https://apps.apple.com/us/app/cartv-m3u-iptv-player-cast/id6800211040
  VIA: App Store listing + iTunes lookup API (v1.1.1, 2026-09-30, 4.5 stars / 3,673 ratings), read 2026-10-09
  ONE-SOURCE-OK: the App Store listing is the authority on its own name and price.

- CLAIM: Free to download; the free tier's casting/mirroring is time-limited; Pro ("Unlimited casting ... no time limit") removes the limit. US prices: Weekly $3.99, Yearly $45.99, Lifetime $21.49
  TIER: official
  SPOKEN: "The free version still works. It just has a time limit, which Pro removes"
  SURPRISE: 70
  SRC: https://cartv.app/
  SRC: https://apps.apple.com/us/app/cartv-m3u-iptv-player-cast/id6800211040
  VIA: cartv.app Pro section ("Unlimited casting: Receive casts and mirror your screen with no time limit"); App Store IAP list
  VIA: the app's own Pro screen, seen in the Gadget Gig demo: "Unlimited casting — Receive casts from other apps with no time limit" listed as a Pro feature
  VIA: App Store review, Sep 14 2026 ("40 free minutes") — a user report, NOT spoken; the exact minutes are not documented by the developer

- CLAIM: Setup order: connect CarPlay, open CarTV on the car display, then tap the Cast to Car tab on the phone
  TIER: official
  SPOKEN: "connect your iPhone to CarPlay, and open CarTV on the car's display"
  SURPRISE: 30
  SRC: https://cartv.app/
  SRC: https://apps.apple.com/us/app/cartv-m3u-iptv-player-cast/id6800211040
  VIA: cartv.app ("Connect your iPhone to CarPlay, open CarTV on the car display"); App Store ("One tap on the Cast to Car tab to start")

- CLAIM: The mirroring is started from the Cast to Car tab
  TIER: official
  SPOKEN: "tap the Cast to Car tab at the bottom"
  SURPRISE: 20
  SRC: https://apps.apple.com/us/app/cartv-m3u-iptv-player-cast/id6800211040
  VIA: App Store description; tab position (bottom bar) seen in the reference demo and to be confirmed on our footage
  ONE-SOURCE-OK: UI label documented by the developer and verified on our own screen recording.

- CLAIM: The app is for passenger use only; never watch while driving. No source shows an automatic lock while moving
  TIER: official
  SPOKEN: "This is for passengers, or for when you're parked. Never watch while driving"
  SURPRISE: 15
  SRC: https://apps.apple.com/us/app/cartv-m3u-iptv-player-cast/id6800211040
  SRC: https://cartv.app/
  VIA: App Store ("for passenger use only. Never watch while driving."); cartv.app ("When the car is parked and the big display lights up")

## NOT CLAIMED

- Mirroring needs no Wi-Fi, it goes over the CarPlay connection (cartv.app FAQ): true, cut for length, used in packaging.

- The exact free time limit (40 minutes is one reviewer's report; the developer publishes no number).
- That video stops automatically when the car moves (nothing found showing that CarTV does).
- Apple's own iOS 26 AirPlay-video-in-CarPlay feature: parked-only, needs automaker opt-in; a different mechanism, not this app.
- AI-box prices ($150-300, single source) — "no adapter box" is said without a price.
- How CarTV technically gets video onto CarPlay — not documented; not spoken.
- That audio plays through the car speakers — shown in the reference demo; spoken ONLY if our own footage confirms it.

## FEATURES + HOW TO USE

Vendor-documented features (App Store description + cartv.app), one task chosen:
- Screen mirroring of the whole iPhone, any app, via the Cast to Car tab — USED (the spine)
- Works with apps that have no Cast button — USED
- DLNA/UPnP cast target in 35+ video apps (needs Wi-Fi + Local Network) — CUT (a second method; mirroring is simpler and needs no Wi-Fi)
- Lock Screen Live Activity, keeps casting in background — CUT (detail, not a step)
- M3U/M3U8 IPTV playlists, Xtream, HLS/HTTP streams — CUT (the app's main pitch, a different task; a second task is a second reel)
- Jellyfin / Emby media server — CUT (same reason)
- Car Mode landscape layout for passengers — CUT
- Real-time subtitles to the big screen (Pro) — CUT
- Local file import, offline play, mini player, favourites, QR playlist add — CUT
- Pro: unlimited sources, Car mode, subtitles, unlimited casting with no time limit — USED only as "time limit, which Pro removes"

Vendor how-to steps (cartv.app + App Store), in order:
1. Install CarTV (iOS 18 or later) — USED
2. Connect the iPhone to CarPlay — USED
3. Open CarTV on the car display (if the icon is missing: Settings > General > CarPlay > your car > Customize) — USED (the fix is a packaging note)
4. Tap the Cast to Car tab on the phone to start mirroring — USED
5. Open any app (YouTube) — it appears on the car display — USED
The Pro screen at first launch and its close button: seen in the reference demo, to be confirmed on our footage — USED

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-09  App Store listing + iTunes lookup API id6800211040  (name, developer, price, IAPs, iOS 18+, description wording, v1.1.1 Sep 30)
- 2026-10-09  cartv.app home, Pro, Cast & Mirror, FAQ  (setup order, free tier time-limited, passenger-only, no Wi-Fi for mirroring)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by
###    someone who is not the vendor
- 2026-10-09  Gadget Gig Short JL8kOTJFS2w (reference), frames + whisper transcript  (install, close Pro screen, Cast to Car tab, CarTV on car display, YouTube playing, audio through car)
- 2026-10-09  "CarTV Lyntra CarPlay app review free trial mirroring"  (no professional review found; App Store reviews only)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-09  App Store reviews page  (praise for casting; "40 free minutes"; audio/video delay on some cars, Mercedes rotary controller; casting disconnect bug acknowledged by developer)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if
###    you were trying to prove the story wrong
- 2026-10-09  "CarTV app free version time limit minutes mirroring CarPlay reddit"  (free is NOT unlimited — Pro lists "no time limit"; script says so)
- 2026-10-09  "CarTV app CarPlay mirror iPhone screen video driving stops"  (no driving lock found; TikTok claims of iOS 26.4+ contradict App Store's iOS 18 — App Store wins)
- 2026-10-09  "iOS 26 AirPlay video CarPlay parked"  (Apple's own route is parked-only and automaker-gated, so "YouTube has no CarPlay app" still stands)

INDEPENDENT-CHECK: 2026-10-09 searched for hands-on reviews and Reddit
  threads on CarTV — found no professional review; independent evidence is
  the Gadget Gig demo, App Store user reviews, and our own filmed test.
