# Visual inventory — ios27-battery-drain

Scouted 2026-09-19. Mobile-first (Constitution rule 2). Nothing downloaded;
`_sources/ios27-battery-drain/` is empty. Rights tag on every item.

Beat names used below (working, from research/plan.md — rename to match
structure.md once the shape is fixed):
HOOK · CONFIRMATION · CAUSE · APPLE-SAYS · HOW-LONG · WHAT-TO-CHECK ·
WHAT-TO-DO · NOT-NORMAL · END

---

## 1. APPLE OFFICIAL — pages and images

- **ASSET:** Apple Support — "About Apple software updates", the battery &
  thermal paragraph
  **URL:** https://support.apple.com/en-us/125039
  **WHAT IT SHOWS:** Text only, no images on the page. The load-bearing
  sentence, verbatim: "Immediately after completing an update, particularly a
  major release, you might notice a temporary impact on battery life and
  thermal performance. This is normal, because your device needs time to
  complete the setup process in the background, including indexing data and
  files for search, downloading new assets, and updating apps." It also says
  new features "require additional resources from the device" and that "some
  users may notice a small impact on performance or battery life."
  **WHICH BEAT:** APPLE-SAYS — the whole "don't panic" claim rests on this one
  paragraph. This is the receipt. Capture mobile, `film` mode fits (page is
  taller than the frame, multi-line, and we hold on the key sentence).
  **RIGHTS:** Apple official. Screenshot of a public support page, used as a
  cited document. Credits stay in the manifest (showCredits off).

- **ASSET:** Apple Support — "If the battery in your iPhone or iPad drains too
  quickly"
  **URL:** https://support.apple.com/en-us/120745
  **WHAT IT SHOWS:** Apple's own remedy list, with exact menu paths:
  Settings > Battery (suggestions + Daily Usage), Settings > Battery >
  Battery Health (iPhone 15 and later), Settings > Battery > Battery Health &
  Charging (iPhone 14 and earlier), Settings > Battery > Power Mode (to turn
  on Low Power Mode), Settings > Wi-Fi, Settings > Cellular > Cellular Data
  Options > Voice & Data. It names Background App Refresh as something Low
  Power Mode reduces, but gives no separate path to it.
  **The page carries one Apple screenshot**, captioned "The Battery Settings
  screen, showing Daily Usage" — an iOS 26 iPhone 16 Pro Battery screen with
  the Daily Usage chart. There is also a video thumbnail about iPhone battery.
  **WHICH BEAT:** WHAT-TO-DO — Apple's own list is what keeps our advice from
  being a listicle's opinion. The embedded screenshot is Apple's only public
  image of the Battery screen we found, but it is **iOS 26**, so it cannot
  stand in for an iOS 27 screen (Rule 3: what's on screen must match what's
  said).
  **RIGHTS:** Apple official.

- **ASSET:** Apple Support — "About iOS 27 Updates" (release notes index)
  **URL:** https://support.apple.com/en-us/149076
  **WHAT IT SHOWS:** The running list of iOS 27.x releases and what each fixed.
  Not yet read line by line — **check before script lock** whether any 27.x
  note mentions a battery or indexing fix. If one exists it either strengthens
  HOW-LONG or breaks the "don't panic" framing (this is the contradiction
  search in research.md §4).
  **WHICH BEAT:** NOT-NORMAL, or HOW-LONG.
  **RIGHTS:** Apple official.

- **ASSET:** Apple iPhone User Guide — "What's new in iOS 27"
  **URL:** https://support.apple.com/guide/iphone/whats-new-in-ios-27-iphfed2c4091/ios
  **WHAT IT SHOWS:** Apple's own feature list for iOS 27: Siri AI / next-gen
  Apple Intelligence, new parental controls and Screen Time, iCloud Shared
  Albums, Custom EQ for AirPods, perimenopause/menopause in Cycle Tracking,
  independent Alarm and Timer volumes, extra-large Home Screen widgets. No
  images on the page itself. **Nothing in Apple's iOS 27 feature list is a new
  battery feature** — worth saying out loud, because it means the drain is the
  cost of the Siri AI re-index, not a new battery setting.
  **WHICH BEAT:** CAUSE — Siri AI is the thing being indexed for.
  **RIGHTS:** Apple official.

- **ASSET:** Apple User Guide — "Save battery life with Power Modes on iPhone"
  **URL:** https://support.apple.com/guide/iphone/save-battery-life-with-power-modes-on-iphone-iphcab9aecd1/ios
  **WHAT IT SHOWS:** The Power Modes page (Low Power Mode lives here in the
  modern layout — it is Settings > Battery > Power Mode, not a standalone
  toggle). The fetch returned only the guide's nav shell, so the mode names and
  screenshots on this page are **unconfirmed** — open it on the device while
  capturing and read it there.
  **WHICH BEAT:** WHAT-TO-DO.
  **RIGHTS:** Apple official.

- **ASSET:** Apple Support — "iPhone battery and performance"
  **URL:** https://support.apple.com/en-us/101575
  **WHAT IT SHOWS:** Not fetched this pass. Apple's long-standing explainer on
  battery chemistry, peak performance capability and Battery Health. Useful
  only if the script goes near "is my battery dying?"
  **WHICH BEAT:** NOT-NORMAL (distinguishing a worn battery from a settling
  update). Fetch before use.
  **RIGHTS:** Apple official.

- **ASSET:** Apple — "Batteries: Maximizing Performance"
  **URL:** https://www.apple.com/batteries/maximizing-performance/
  **WHAT IT SHOWS:** Not fetched. Apple's consumer battery page; historically
  carries clean Apple-made battery graphics that photograph well in 9:16.
  **WHICH BEAT:** Decorative only — no claim rests on it. Check it on mobile
  before committing; the desktop layout is wide.
  **RIGHTS:** Apple official.

- **ASSET:** Apple Newsroom — "Major updates for Apple's software platforms are
  now available" (Sept 2026)
  **URL:** https://www.apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/
  **WHAT IT SHOWS:** The release-day announcement for iOS 27 / iPadOS 27 /
  macOS 27 / watchOS 27 / visionOS 27 / tvOS 27, led by Siri AI and parental
  controls. Newsroom posts carry Apple-produced hero images and a press
  gallery — **the cleanest legitimately-Apple imagery available for this
  topic.** Not opened this pass; open on mobile and list the actual images
  before relying on one.
  **WHICH BEAT:** HOOK or CAUSE — "the update everyone just installed".
  **RIGHTS:** Apple official, Newsroom images are offered for editorial use.
  Editorial reporting is exactly our use; keep the source_url in the manifest.

- **ASSET:** Apple Newsroom — "Siri AI, a profoundly more capable and personal
  assistant, is here"
  **URL:** https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/
  **WHAT IT SHOWS:** Apple's own framing and imagery for Siri AI — the feature
  whose on-device index is the reason the phone is working overnight.
  **WHICH BEAT:** CAUSE — pairs with the "Optimizing Search and Siri" capture
  below: here is the feature, here is your phone building it.
  **RIGHTS:** Apple official / editorial.

- **NOT FOUND:** a consumer-facing `apple.com/ios/ios-27/` marketing page did
  not surface in search, and no Apple page we read shows an **iOS 27** Battery
  settings screenshot. Every Apple Battery screenshot we located is iOS 26.
  Treat "Apple has an image of the iOS 27 Battery screen" as unproven — we
  capture it ourselves (§4).

---

## 2. THE REFERENCE ARTICLE — 9to5Mac

- **ASSET:** 9to5Mac article page
  **URL:** https://9to5mac.com/2026/09/15/battery-draining-faster-after-updating-to-ios-27-dont-panic/
  **HEADLINE, EXACT:** "Battery draining faster after updating to iOS 27?
  Don't panic …" — by Ben Lovejoy, Sep 15 2026, 6:35 am PT.
  **WHAT IT SHOWS:** Yes, it has its own graphic — a hero image of **three
  iPhone 18 models running iOS 27**, alt text "Battery draining faster after
  updating to iOS 27? Don't panic … | Image shows three iPhone 18 models
  running the new OS". No screenshots inside the article body. The piece
  argues the drain is temporary and normal, attributes it to background work
  "particularly re-index[ing] your device for use with Siri AI", says it can
  run "several days", quotes the Apple 125039 paragraph above, and closes that
  battery life should return to normal or better.
  **WHICH BEAT:** CONFIRMATION — a named tech outlet with the same read,
  captured as a headline hold. The headline itself is the story in six words.
  **RIGHTS:** Third-party press. Screenshot the headline + byline as a cited
  document (fair reporting use); **do not** lift their hero image — it is
  9to5Mac's composite, not Apple's. Capture on mobile, `film` mode fits.

---

## 3. THE INSTAGRAM REEL

- **ASSET:** https://www.instagram.com/p/DdZL8B4CHqc/
  **WHAT IT SHOWS: nothing — Instagram blocked it.** WebFetch returned a page
  containing only the word "Instagram": a login wall. No account name, no
  caption, no description, no thumbnail is publicly visible. No workaround was
  attempted and none should be: no login, no cookies, no scraper.
  **WHICH BEAT:** none. It is a lead for the *angle*, not an asset.
  **RIGHTS:** n/a — unusable. If the user wants what that reel said, they can
  open it on their phone and paste the caption; treat anything they paste as
  audience language, never as a sourced claim.

---

## 4. SCREENS WE CAPTURE OURSELVES (iOS 27, on device)

These are the reel's real visuals. Everything above is paper; this is the
phone doing the thing. Capture at 1080x2340-class device resolution, in the
same session, same wallpaper, same time of day, Do Not Disturb on.

- **ASSET:** **"Optimizing Search and Siri" in Settings** — THE money shot
  **PATH:** open Settings; the banner appears on the top-level Settings screen
  while indexing runs.
  **WHAT IT SHOWS:** New in iOS 27: after updating, Settings shows an
  "Optimizing Search and Siri" status **with a live progress percentage and a
  last-refreshed timestamp**. This is the visible, measurable proof that the
  phone is doing extra work — and it did not exist in iOS 26.
  **WHICH BEAT:** CONFIRMATION (2-5s, right after the hook, per G70) and
  CAUSE. It proves the promise on screen in one frame.
  **RIGHTS:** Our own capture.
  **VERIFY FIRST:** corroborated by Tom's Guide
  (https://www.tomsguide.com/phones/why-your-iphone-says-optimizing-search-and-siri-in-ios-27-and-how-to-speed-it-up)
  and several smaller sites; **not yet confirmed in Apple's own words.** The
  exact label and the presence of a percentage must be confirmed on the device
  before any script line claims it. If the phone has finished indexing, the
  banner is gone and it cannot be re-staged — grab it from a device that is
  still working, or from a fresh update.

- **ASSET:** **Settings > Battery** — the usage graph
  **PATH:** Settings > Battery. Sections to frame: the battery-level chart,
  Daily Usage / trend, and the period switch (the "Last 10 Days" style view).
  **WHAT IT SHOWS:** The drain the viewer is complaining about, as a shape —
  tall bars on update day, shorter bars as it settles. If the capture device
  updated a few days ago, this single screen tells the entire story without a
  word of narration.
  **WHICH BEAT:** HOOK and HOW-LONG. The 10-day view is the payoff visual:
  the spike, then the return to normal.
  **RIGHTS:** Our own capture.
  **CHANGED SINCE iOS 26?** iOS 26 is where the Battery screen was overhauled
  (Daily Usage + trend "are you using more than usual", plus Adaptive Power).
  **No source we found reports a further redesign of the Battery screen in
  iOS 27** — so assume it looks like iOS 26 until the device says otherwise,
  and never illustrate an iOS 27 line with Apple's iOS 26 screenshot. Note on
  capture whether "Last 10 Days" is still the label.

- **ASSET:** **Settings > Battery > Battery Health** (iPhone 15 and later) /
  **Battery Health & Charging** (iPhone 14 and earlier)
  **PATH:** exactly as Apple names it in 120745 — the label differs by model,
  so say which phone is on screen or the viewer thinks we got it wrong.
  **WHAT IT SHOWS:** Maximum Capacity percentage and Peak Performance
  Capability.
  **WHICH BEAT:** NOT-NORMAL — the "is my battery actually dying?" fork. An
  unchanged Maximum Capacity before and after the update is the cleanest
  possible proof that the update is not eating the battery.
  **RIGHTS:** Our own capture.

- **ASSET:** **Settings > General > Background App Refresh**
  **PATH:** Settings > General > Background App Refresh (unchanged in iOS 27
  per third-party reporting; Apple's 120745 names the feature but not the
  path — confirm on device).
  **WHAT IT SHOWS:** The master toggle (Off / Wi-Fi / Wi-Fi & Cellular) and
  the per-app list.
  **WHICH BEAT:** WHAT-TO-DO — and a caution beat: this is the setting every
  listicle tells people to kill, while Apple's own advice is Low Power Mode.
  **RIGHTS:** Our own capture.

- **ASSET:** **Low Power Mode toggle** — Settings > Battery > Power Mode
  **PATH:** Settings > Battery > Power Mode (per Apple 120745). Also reachable
  from Control Center; the Control Center version is the better 9:16 visual
  because the toggle animates.
  **WHAT IT SHOWS:** The mode turning on, and the battery indicator going
  yellow — a state change the eye catches on mute.
  **WHICH BEAT:** WHAT-TO-DO. Apple's own recommendation, so it is the one
  "fix" in the reel that carries a source.
  **RIGHTS:** Our own capture.
  **CONFIRM ON DEVICE:** whether iOS 27 still lists Adaptive Power alongside
  Low Power Mode under Power Mode, and whether Adaptive Power is on by default
  on the capture device — it changes what the viewer will see when they look.

- **ASSET:** **The update screen itself** — Settings > General > Software
  Update showing iOS 27 installed
  **WHAT IT SHOWS:** Version number on screen. One second, establishes that
  everything after it is genuinely iOS 27.
  **WHICH BEAT:** HOOK / CONFIRMATION. Cheap, and it inoculates the comments
  section against "that's not even iOS 27".
  **RIGHTS:** Our own capture.

---

## 5. APPLE-OFFICIAL VIDEO / B-ROLL (YouTube, Apple's own channel only)

Checked the 120 most recent uploads on https://www.youtube.com/@Apple/videos
and the recent @AppleSupport uploads.

- **NO iOS 27 VIDEO EXISTS ON APPLE'S CHANNEL.** The recent uploads are all
  hardware — iPhone 18 Pro, iPhone Duo, Apple Watch Series 12, AirPods 5, the
  September '26 event recap. There is no "Introducing iOS 27". Several
  third-party videos carry that exact title in search results; one of them
  (`u0G7Py-DxHA`) is titled "Introducing iOS 27" and is **not** on Apple's
  channel (it is now unavailable and could not be verified at all). Do not
  mistake it for Apple footage.

- **ASSET:** Apple — "Apple's next big step for Siri and iPhone"
  **URL:** https://www.youtube.com/watch?v=2PW5y3zAvPE
  **VERIFIED:** channel = Apple, uploaded 2026-06-08 (WWDC week), 96 seconds.
  **WHAT IT SHOWS:** Apple's own Siri AI announcement piece. **Content not yet
  inspected frame by frame** — nothing was downloaded — so no timestamp can be
  given honestly yet. Pull it and scrub before using: we want a few seconds of
  Siri AI on an iPhone, which is the feature the indexing serves.
  **WHICH BEAT:** CAUSE.
  **RIGHTS:** Apple official, but it is **Apple's copyrighted video**, not a
  press image. Brief excerpt in commentary only, seconds not tens of seconds,
  and only if the narration is talking about Siri AI while it is on screen
  (Rule 3). Keep source_url in the manifest.

- **ASSET:** Apple — "iOS 26: Introducing Liquid Glass"
  **URL:** https://www.youtube.com/watch?v=jGztGfRujSE
  **VERIFIED:** channel = Apple, uploaded 2025-06-09, 274 seconds.
  **WHAT IT SHOWS:** The iOS **26** launch film. Listed only to rule it out:
  it is the wrong OS, and using it under an iOS 27 line breaks Rule 3.
  **WHICH BEAT:** none. Do not use.
  **RIGHTS:** Apple official, wrong subject.

---

## Gaps to close before the shot plan

- **No iOS 27 device capture exists yet.** Every asset in §4 is a plan, not a
  file. The reel cannot be built without them, and the "Optimizing Search and
  Siri" banner is perishable — it disappears when indexing finishes.
- **"Optimizing Search and Siri" is single-tier-ish**: strong secondary
  reporting (Tom's Guide), no Apple page confirming the label or the
  percentage. Either confirm on device (our own capture becomes the evidence)
  or hedge the line per framework S20.
- **support.apple.com/en-us/149076 not read yet** — a 27.x note about a battery
  or indexing fix would change the story's framing.
- **Apple Newsroom images not enumerated** — open the two Newsroom posts on
  mobile and list the actual images before planning a beat around one.
