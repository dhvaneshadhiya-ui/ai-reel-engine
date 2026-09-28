# Visual inventory — ios27-carplay-features

Scouted 2026-09-28. Every "what it shows" line was written after looking at the
image or at a frame pulled from the video. Local files are under
`_sources/ios27-carplay-features/` (never public/). Subtitles are in `subs/`
(`<id>.txt` = timestamped plain text), verification frames in `frames/`,
downloaded stills in `stills/`.

Tiers: **official** = Apple produced it; **reliable** = established outlet
(MacRumors, 9to5Mac, AppleInsider) or its own capture; **fallback** = an
independent creator.

## Headline findings (read these first)

1. **The keynote has almost nothing on CarPlay.** In the 76-minute WWDC26 keynote
   CarPlay is spoken once, at **39:02-39:06**: "All these updates to Siri extend to
   CarPlay as well as AirPods." The picture under that line is about 3-4 seconds of
   CarPlay Siri AI on a car screen (checked frame by frame: iPad at 39:02, CarPlay at
   39:03-39:05, AirPods runner at 39:07). MacRumors reports a slide listing the four
   smaller features (audio scrubbing, GPS/heading, MiniPlayer, wireless reliability)
   that was "shown very briefly". **I did not find its timestamp.** The keynote
   subtitles never mention it, and finding it would mean scrubbing the video frame by
   frame.
2. **Apple's detailed CarPlay material is the developer session, not the keynote:**
   "Rev up your CarPlay app" (WWDC26 session 212). It has official motion of the
   video app, the MiniPlayer and the voice-control overlay, all shown in the CarPlay
   Simulator.
3. **apple.com has no iOS 27 CarPlay section.** `apple.com/ios/ios-27/` returns 404.
   The live page is `apple.com/os/ios/` (same for `/in/os/ios/`), and it never
   mentions CarPlay: no section and no images. `apple.com/ios/carplay/` is the
   general CarPlay page with nothing specific to iOS 27. None of the three WWDC26 or
   September newsroom releases has a CarPlay image. The Siri AI release mentions
   CarPlay in one sentence, and the three hero images I downloaded and checked do
   not show CarPlay. I deleted them.
4. **RIGHTS/ACCURACY FLAG: "third-party widgets" may not be new in iOS 27.** In
   session 212 (01:07) Apple describes "Live Activities and widgets from any app" as
   something CarPlay already supports. iOS 26 (WWDC25) brought widgets and Live
   Activities to CarPlay. Some outlets (Man of Many, Pocket-lint) call it an iOS 27
   feature. Check this in research.md before it becomes one of the five. I found no
   visual of a third-party widget on a CarPlay dashboard.

---

## 1. OFFICIAL MOTION

### A1. WWDC26 keynote (Apple)
- URL: https://www.youtube.com/watch?v=hF8swzNR1-o (uploaded 2026-06-08, 76:14, "Apple WWDC 2026 June 8: Introducing Siri AI and more")
- Local: subtitles only, `subs/hF8swzNR1-o.txt`; frames `frames/keynote_39m05.jpg` (plus 38m30/38m36/39m02 for context)
- CarPlay segment: **39:03 → ~39:06** (one shot). Spoken over it: 39:02 "All these updates to Siri extend to" / 39:04 "CarPlay as well as AirPods."
- What it shows (looked): a car centre display seen from the driver's side, trees through the windscreen. Apple Maps (green, dark) near the Japanese Tea Garden and De Young. A glass Siri card for "Aaron Morris" with Reply / Repeat / Done buttons and a Siri glow at the bottom edge. Climate strip below (OFF, AUTO, MAX, REAR, A/C).
- Proves: **Siri AI in the car** (official, but it is a message read-out card, not a back-and-forth conversation)
- Tier: official. Credit: Apple

### A2. "Rev up your CarPlay app" — WWDC26 session 212 (Apple Developer)
- URL: https://www.youtube.com/watch?v=ykwG0I8UGjg (15:56) · https://developer.apple.com/videos/play/wwdc2026/212/
- Local: `subs/ykwG0I8UGjg.txt`
- Sub-timestamps (from subtitles):
  - 01:07 "CarPlay supports Live Activities and widgets from any app" (described as existing support; see flag 4)
  - 01:19-02:00 video apps: "browse and play videos in new cars that support the video in car feature… waiting for a friend at the airport, parked at a charging station"
  - 02:19-02:24 video playback not available (while driving)
  - 03:13 / **06:22-06:48** MiniPlayer for Now Playing ("All apps that show now playing will automatically show the MiniPlayer")
  - 06:52-08:23 voice-based conversational apps, Voice Control template and overlay
  - **09:11-11:42 demo in CarPlay Simulator**: the Landmarks app with a Videos tab (09:32), the MiniPlayer top right (09:37), a video playing (11:06-11:17), notifications over the video (11:28)
  - 11:49+ navigation app features
- What it shows: not looked at frame by frame (no frames pulled). The 9to5Mac still B3 below appears to be a grab from this demo: same Alps / Epic Moments UI.
- Proves: **video apps while parked** (best official motion), **MiniPlayer / Now Playing**. It does NOT show audio scrubbing, Maps, wireless or the look.
- Tier: official. Credit: Apple
- Note: the screen is the CarPlay Simulator (a flat UI render), not a real car.

## 2. OFFICIAL STILLS

### S1. Session 212 thumbnail
- URL: https://devimages-cdn.apple.com/wwdc-services/images/9B2E82C5-4DDF-4B9A-9459-328D8E297696/10722/10722_wide_900x506_2x.jpg
- Local: `stills/apple_dev_wwdc26-212-thumb.jpg` — **1800x1012**
- What it shows (looked): CarPlay on a wide car display (dark dashboard). Left dock: 9:41 5G, Maps, Music, Messages, Calendar "Wed 1". Big map: I-280 N, Skyline Blvd, Skyline Park, speed limit 65, "10:23 arrival 42 min 32 mi". Right column of three glass cards: "8.2 mi Stay on 280 North", a media card with album art and ⏮ ⏸ ⏭, and a calendar card "FaceTime with Mom 10:00-11:00 AM". "WWDC26" wordmark bottom left.
- Proves: **Liquid Glass look** (glass dashboard cards, official) and a dashboard with widgets (Calendar/Now Playing cards; these are Apple's own, not third-party). No scrub bar.
- Tier: official. Credit: Apple
- Crop note: the WWDC26 logo sits bottom left; crop above it.

(No apple.com/os/ios or newsroom CarPlay stills exist; see headline finding 3.)

## Reliable-tier stills (outlet images; some are Apple renders)

### B1. MacRumors "CarPlay-Siri-AI"
- URL: https://images.macrumors.com/article-new/2026/06/CarPlay-Siri-AI.jpg (in https://www.macrumors.com/2026/06/08/new-apple-carplay-features-ios-27/)
- Local: `stills/mr_CarPlay-Siri-AI.jpg` — **1392x904**
- What it shows (looked): the same shot as keynote A1 (Aaron Morris card, Reply/Repeat/Done, Japanese Tea Garden map, climate strip), cropped tighter with a sharper render. Almost certainly Apple's keynote or press render, re-hosted.
- Proves: **Siri AI in the car**
- Tier: reliable (Apple-origin image). Credit: Apple (via MacRumors)
- Best still for Siri in the car.

### B2. 9to5Mac "siri-ai-ui-ios-27-carplay"
- URL: https://9to5mac.com/wp-content/uploads/sites/6/2026/06/siri-ai-ui-ios-27-carplay.jpg
- Local: `stills/9to5_siri-ai-ui-ios-27-carplay.jpg` — **2000x1000**
- What it shows (looked): a close crop of the CarPlay home grid (Phone, Music, Maps, Messages, Now Playing / Podcasts, Audiobooks, a ChatGPT-logo app, News, Calendar "Mon 8") on a dark purple wave wallpaper. A dark Siri orb with a light glow sits at the bottom centre over the ChatGPT icon.
- Proves: **Siri AI** (the new orb UI); also the **new wallpaper look**
- Tier: reliable (9to5Mac screenshot). Credit: 9to5Mac

### B3. 9to5Mac "carplay-video-car-ios-27"
- URL: https://9to5mac.com/wp-content/uploads/sites/6/2026/06/carplay-video-car-ios-27.jpg
- Local: `stills/9to5_carplay-video-car-ios-27.jpg` — **2000x1000**
- What it shows (looked): a wide car display with CarPlay. Tabs "Videos | Audio Stories". A MiniPlayer pill top right: "Alps ▶ ⏭". Row "Epic Moments": Rocky Mountains (NEW), Alps (progress bar, 1m), Yellow Aster Butte, Kirkjufell Mountain. Row "Now Streaming" with LIVE tiles. Left dock: Maps, Landmarks app, Messages, Calendar.
- Proves: **video apps while parked** (browse UI) and the **MiniPlayer**
- Tier: reliable. It is Apple's session 212 demo, so for full official provenance use A2 at ~09:32-09:47. Credit: Apple (via 9to5Mac)

### B4. 9to5Mac "ios-27-carplay-miniplayer-audio"
- URL: https://9to5mac.com/wp-content/uploads/sites/6/2026/08/ios-27-carplay-miniplayer-audio.jpg
- Local: `stills/9to5_ios-27-carplay-miniplayer-audio.jpg` — **2000x1000**
- What it shows (looked): a Podcasts-style CarPlay library (Library tab, Saved, Latest Episodes, "Recently Updated" podcast art row). Top right MiniPlayer: "The Town" art, "Can the Param…", ▶, 30-second skip. **No scrub bar is visible.**
- Proves: **MiniPlayer** only. It does NOT prove scrubbing.
- Tier: reliable. Credit: 9to5Mac

### B5. 9to5Mac "siri-app-ios-27-carplay"
- URL: https://9to5mac.com/wp-content/uploads/sites/6/2026/06/siri-app-ios-27-carplay.jpg
- Local: `stills/9to5_siri-app-ios-27-carplay.jpg` — **2000x1000**
- What it shows (looked): an iPhone (not the car) showing the Siri app "Conversations" list. "Celebrity Game Attendance" and "Knicks Game Result" carry a **car icon**, and "Music Navigation Bar Minimizing" carries a Podcasts icon. Pink/orange gradient background.
- Proves: **Siri AI conversations sync from CarPlay to the Siri app** (the car icon)
- Tier: reliable. Credit: 9to5Mac

### B6. MacRumors guide feature graphic (low value)
- URL: https://images.macrumors.com/article-new/2026/07/8-CarPlay-Features-in-iOS-27-Feature.jpg
- Local: `stills/mr_8-CarPlay-Features-iOS-27.jpg` — **2500x1406**
- What it shows (looked): two app icons on a slate background: a dark glass "27" iOS icon and the green CarPlay icon. No UI.
- Proves: nothing specific. At most a title card, and it is MacRumors' artwork, so **do not use** unless credited; better to build our own.
- Tier: reliable (editorial art). Credit: MacRumors

## 3. HANDS-ON CREATOR VIDEOS (real cars)

Frames checked: `frames/*.jpg`. Subtitles for KOxybEDk5Aw, 2y502Uo1TxM and
LRcAIXgS1Fw did NOT download (YouTube HTTP 429 rate limit), so those three are
listed with metadata only.

### H1. AppleInsider — "CarPlay Just Got Way More Powerful with iOS 27!"
- URL: https://www.youtube.com/watch?v=HMZkIIn3zIo (2026-06-16, 9:28) · subs `subs/HMZkIIn3zIo.txt`
- Car: a large portrait touchscreen (Ram/Jeep-style, with a finger visibly tapping). Beta-era footage.
- Timestamps:
  - **Siri AI** 00:58-01:47. Frame at 01:10 (looked): CarPlay showing a Siri "Conversations" list (CarPlay References, New Conversation) with a finger tapping. Also a "glowing glass orb" (01:08-01:10).
  - **MiniPlayer** 02:19-03:23
  - **Audio scrubbing** 02:31-02:50: "tap on the little middle of the scrub bar and slide that indicator left and right". The frame at 02:46 (looked) shows the Music library (Home/New/Radio/Library) with a finger on the screen. The scrub bar itself is not clearly visible in that single frame, so pull frames from 02:46-02:50 before choosing a cut.
  - **Video apps** 03:58-04:44. Frame at 04:31 is a black display with a loading spinner (no usable video footage here).
  - **Wallpapers / look** 06:32-06:45: "12 new wallpapers". Frame at 06:40 (looked): the Wallpaper picker, a grid of pastel pink/purple/blue/green wave wallpapers, finger scrolling. **Good for the Liquid Glass / new-look beat.**
  - **Wireless** 07:18-07:42: a new wireless icon in settings plus a "more robust wireless connection". The frame at 07:22 is the presenter talking to camera, not the car.
  - 08:44-08:58: a parked-car widget on the Apple Watch Smart Stack (not CarPlay)
- Tier: reliable (AppleInsider). Credit: AppleInsider

### H2. zollotech — "iOS 27 - Every New Apple CarPlay Feature"
- URL: https://www.youtube.com/watch?v=SvOMPhNB7WM (2026-07-03, 8:11) · subs `subs/SvOMPhNB7WM.txt`
- Car: a wide landscape display with climate controls built into the bottom strip.
- Timestamps:
  - Liquid Glass icons 00:07-00:11. **Wallpapers 00:50-01:35**. Frame at 00:52 (looked): the Wallpaper picker, a 3x3 grid of dark purple/blue/red/gold wave wallpapers.
  - MiniPlayer 01:59
  - **Audio scrubbing 02:40-02:51**: "you can now scrub audio… drag back and forth". Frame at 02:45 (looked): a full Now Playing podcast screen ("Apple's Price Increase is Here, $25K Slate Truck EV…", Primary Technology, June 25 2026). **A finger is on the scrub bar mid-drag (32:53 / -58:26)**, with a 1x speed control. **Best scrubbing visual found.**
  - Siri AI 02:56-03:59
  - Video apps 05:12-05:40 (talked about, "near future")
  - Maps / Google Maps 06:04-06:38. **GPS accuracy/heading 06:48-06:57**. Wireless 00:24-00:30 and 07:00-07:19
- Tier: fallback (independent creator). Credit: zollotech

### H3. 9to5Mac — "iOS 27 Just Changed CarPlay Forever and I LOVE IT"
- URL: https://www.youtube.com/watch?v=96pCsMK28No (2026-07-01, 8:20) · subs `subs/96pCsMK28No.txt` (auto-subs are rough)
- Car: a wide display in a Jeep-style dash, filmed from the driver's seat with the wheel in frame.
- Timestamps:
  - Liquid Glass 02:41. Wallpapers 02:53-02:58
  - Siri requirements 03:15-03:25 ("iPhone 15 [Pro]", "wired or wireless")
  - **Natural-language directions via Siri 05:03-05:17**: "Can you give me directions to Till's office?" and Siri answers "Would you like directions to Tilly …'s appointment at Optum Pediatrics or Tilly Little's gym appointment?" The frame at 05:13 (looked) shows the CarPlay screen **blurred by the creator** (personal info), so the audio carries this moment, not the picture. It also contains a private person's name and appointment, so **do not use the audio as-is**.
  - Maps behaviour 05:26-05:40
  - **Wireless reliability 05:48-06:00**: "much more reliable". Frame at 05:52 (looked): creator picture-in-picture plus an Apple Maps CarPlay screen (San Francisco waterfront) on the car display.
  - Video while parked 06:16-06:36
- Tier: reliable (9to5Mac). Credit: 9to5Mac

### H4. 9to5Mac — "CarPlay Just Got WAY Better in iOS 27"
- URL: https://www.youtube.com/watch?v=Lvci5LfFE4w (2026-06-09, 5:57) · subs `subs/Lvci5LfFE4w.txt`
- Reaction/explainer the day after WWDC. Siri AI 00:25-02:31, video apps 02:37-03:33 ("You have to be parked"), wallpapers/Liquid Glass 03:48-03:56, MiniPlayer 04:24, scrubbing 04:35-05:00. **Frames not checked**: likely Apple b-roll and a talking head, not a real car.
- Tier: reliable. Credit: 9to5Mac

### H5-H7. Not transcribed (YouTube 429). Metadata only; frames not checked.
- https://www.youtube.com/watch?v=KOxybEDk5Aw — Nick O'Leary, "iOS 27 Apple CarPlay | 10 NEW FEATURES!" (2026-09-09, 16:02). Fallback.
- https://www.youtube.com/watch?v=2y502Uo1TxM — HotshotTek, "iOS 27 CarPlay is AMAZING! Try these 20 things first!" (2026-09-14, release day, 9:59). Fallback.
- https://www.youtube.com/watch?v=LRcAIXgS1Fw — HotshotTek, "iOS 27 FINALLY Brings YouTube Videos to CarPlay" (2026-09-16, 9:48). **Most likely source of real in-car video playback while parked.** Fallback.
  Retry the subtitle download later: `yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt -o _sources/ios27-carplay-features/subs/%(id)s <url>`.

---

## Best asset per feature

| Feature | Best asset | Tier | Backup |
|---|---|---|---|
| Audio scrubbing (Now Playing) | H2 zollotech 02:40-02:51 (finger dragging the scrub bar) | fallback | H1 AppleInsider 02:31-02:50 (check frames) |
| Third-party widgets on dashboard | **none found** (see flag 4) | — | S1 shows Apple's own dashboard cards only |
| Siri AI in the car | A1 keynote 39:03-39:06 / B1 still | official | H1 01:08-01:47 (real car, Conversations), B2, B5 (car icon in Siri app) |
| Video apps while parked | A2 session 212 09:11-11:42 (Simulator) / B3 still | official | H5-H7 LRcAIXgS1Fw (unchecked) |
| Natural-language Maps directions | H3 05:03-05:17 (screen blurred, private name in audio) | reliable, weak | **real gap** |
| More reliable wireless CarPlay | nothing visual; H1 07:18-07:42 (new wireless icon, talk) | reliable | treat as a text/graphic beat |
| Liquid Glass look / wallpapers | S1 session thumbnail (glass cards) | official | H1 06:40 or H2 00:52 wallpaper pickers in real cars |
| MiniPlayer (bonus) | A2 06:22 + 09:37 / B3 / B4 | official | H1 02:19 |

## Gaps

- **No Apple imagery on apple.com or in the newsroom for iOS 27 CarPlay.** Official material is limited to the 3-4 second keynote shot and developer session 212.
- **The keynote "four features" slide was not located.** Its timestamp is unknown; finding it would need a frame scan of the iOS section (~20-40 min).
- **Third-party widgets:** no visual, and the claim that this is new in iOS 27 is doubtful (Apple's own session describes it as existing support).
- **Natural-language Maps directions:** the only demo found has a blurred screen and a private person's name. No clean visual.
- **Wireless reliability:** invisible by nature. There is only talk and a settings icon.
- **Video while parked in a real car:** only the Simulator (official) so far. LRcAIXgS1Fw is the likely real-car source but is unchecked.
- Creator footage (H1-H7) is third-party. It needs credit and a rights decision before use.
