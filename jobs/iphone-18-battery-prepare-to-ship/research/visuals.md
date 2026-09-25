# Visual assets — iPhone 18 Pro Max "Prepare to Ship" battery feature

Subtopic: OFFICIAL VISUALS — what can actually be shown on screen to prove this story,
captured MOBILE-first. Researched 2026-09-21 via WebFetch/WebSearch (budgeted 6 calls).

## Headline finding

**No outlet — not MacRumors, not 9to5Mac, not GSMArena, not anyone found in search —
has an actual screen recording or original screenshot of a real device running the
Prepare to Ship flow.** The only real UI screenshot in circulation anywhere is Apple's
own single static support-page illustration. Every tech-news writeup (MacRumors,
9to5Mac, GSMArena, Appleosophy, MacObserver, etc.) describes the flow in prose only,
or reuses/crops Apple's own device photography as a header image. This is a real
constraint for the reel: the "core visual proof" beat cannot be an original recording
of the live flow — it has to be built from Apple's one illustration, on-screen text
recreating the other states (Ready to Ship badge, progress screen) described only in
words, or our own simulated capture of the equivalent Settings > General > Transfer or
Reset iPhone path on a current iPhone (the real Prepare to Ship entry does not exist
on non-18-Pro-Max hardware, so a simulated capture can only get as far as the parent
menu, not the feature screen itself).

---

## ASSET 1 — Apple's own "Prepare to Ship" screenshot (the ONLY real UI image found)

- **SOURCE URL:** https://support.apple.com/en-us/127848 ("Prepare your iPhone 18 Pro
  Max to ship")
- **WHAT IT SHOWS:** The Settings > General > Transfer or Reset iPhone > Prepare to
  Ship screen. Alt text on the page: *"iPhone screen shows 'Prepare to Ship' with
  instructions to discharge battery to 80%."* This is the confirmation/instruction
  screen a user sees before starting the discharge — not the in-progress discharge
  screen and not the "Ready to Ship" red-badge end state (those exist only as prose
  on the same support page, no separate screenshot).
- **IMAGE URL:** `https://cdsassets.apple.com/live/7WUAS350/images/iphone/ios-27-iphone-new-settings-general-transfer-reset-iphone.png`
- **WHICH BEAT:** The core visual proof beat — "here's the actual toggle screen" —
  the single strongest piece of screen evidence in the whole story. Should anchor the
  moment the script says the words "Prepare to Ship" / "discharge your battery."
- **PROVENANCE:** Official Apple material (support-page asset, Apple's own render/
  screenshot, not press photography). This is a DESKTOP-captured static PNG served
  from Apple's CDN — it is not a mobile screen recording. Per the mobile-first
  scouting rule, if used verbatim it should be re-presented inside a phone-frame
  mockup (deviceframe-style) at 9:16 rather than shown as a bare rectangle, or
  re-captured with `tools/capture.mjs` at 1080x2340 against the live support page on
  a mobile viewport to get a phone-realistic crop instead of using Apple's raw asset
  edge-to-edge.

## ASSET 2 — MacRumors article header image

- **SOURCE URL:** https://www.macrumors.com/2026/09/18/iphone-18-pro-max-shipping-restriction/
- **WHAT IT SHOWS:** Could not be confirmed as a UI screenshot from the HTML alone —
  filename is `iphone-18-pro-max-prepare.jpg`, sized as a 400px-wide article thumbnail.
  WebFetch could not determine on-screen content beyond the filename; it is most
  likely an illustrative photo/graphic MacRumors built for the story rather than a
  captured device screen (MacRumors' own text in this story describes the feature
  without embedding Apple's support-page screenshot).
- **IMAGE URL:** `https://images.macrumors.com/t/Z29s4KLigVwpjHjtXEtv_6ulU2I=/400x0/article-new/2026/09/iphone-18-pro-max-prepare.jpg?lossy` (thumbnail; a larger crop likely exists at the same path without the `400x0` transform — not verified)
- **WHICH BEAT:** Weak candidate at best — low confidence on content, low resolution
  (400px wide is below usable width even cropped for 9:16). Not recommended as a
  primary asset; worth a manual look before use, not worth building the story around.
- **PROVENANCE:** Third-party (MacRumors), likely an editorial graphic, NOT a
  screenshot of a real device mid-flow.

## ASSET 3 — 9to5Mac article header image

- **SOURCE URL:** https://9to5mac.com/2026/09/19/iphone-18-pro-maxs-battery-is-so-big-apple-had-to-add-this-new-feature-to-ios-27/
- **WHAT IT SHOWS:** Product shot of the iPhone 18 Pro Max device (not a Settings
  screenshot). 9to5Mac's own text confirms: despite describing the Prepare to Ship
  Settings flow in detail, **the article includes no screenshot of the Settings UI at
  all** — text description only.
- **IMAGE URL:** `https://9to5mac.com/wp-content/uploads/sites/6/2026/09/iphone-18-pro-max-ship.jpg?quality=82&strip=all&w=1600` (1600px wide — usable resolution)
- **WHICH BEAT:** Could work as a hook/establishing shot of the device itself (not
  the feature), or as a cutaway while narration explains the battery spec, but it is
  a generic product photo, not proof of the shipping feature.
- **PROVENANCE:** Likely 9to5Mac's own product photo of the device, or Apple press
  imagery repurposed by 9to5Mac — cannot confirm origin from HTML alone.

## ASSET 4 — GSMArena inline images

- **SOURCE URL:** https://www.gsmarena.com/heres_apples_clever_way_of_circumventing_20wh_battery_shipping_restrictions-news-74689.php
- **WHAT IT SHOWS:** Unknown from HTML — no alt text or caption extracted. Two inline
  images referenced (`gsmarena_001.jpg`, `gsmarena_006.jpg`), full HTML did not carry
  descriptive text confirming whether either is a Settings screenshot or a product
  photo. GSMArena's headline framing ("Apple's clever way of circumventing 20Wh
  restrictions") suggests it may include its own explanatory graphic, but this is
  unconfirmed — would need a visual (not text) fetch/screenshot to verify.
- **IMAGE URLs:**
  - `https://fdn.gsmarena.com/imgroot/news/26/09/iphone-18-pro-max-ifr/inline/-1200w5/gsmarena_001.jpg`
  - `https://fdn.gsmarena.com/imgroot/news/26/09/iphone-18-pro-max-ifr/inline/-1200w5/gsmarena_006.jpg`
- **WHICH BEAT:** Unconfirmed — flag for manual visual check before use; do not build
  a beat around this until someone actually looks at the images (WebFetch only reads
  HTML/text, not image pixels).
- **PROVENANCE:** Unknown — third-party outlet, possibly editorial graphic.

## ASSET 5 — Apple.com iPhone 18 Pro Max hero/product photography (for hook/cover use)

- **SOURCE URL:** https://www.apple.com/iphone-18-pro/ (also mirrored at
  https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/
  for the launch press release)
- **WHAT IT SHOWS:** Official Apple product photography — hero shots and the color/
  finish gallery (Burgundy, Glacier, Silver, Black) plus an all-in-one hero angled to
  show the rear camera system. Clean device beauty shots, no UI/Settings content —
  suited only to a hook/cover shot or a "here's the phone we're talking about" cutaway,
  not to proving the feature itself.
- **IMAGE URLs** (relative to `https://www.apple.com`):
  - `/v/iphone-18-pro/b/images/overview/media-hero/hero_startframe__ck15fj8f67hy_large.jpg`
  - `/v/iphone-18-pro/b/images/overview/media-hero/hero_endframe__fbxsnz8txcia_large.jpg`
  - `/v/iphone-18-pro/b/images/overview/aio/hero__elo7tt0mnqy6_large.jpg` (Burgundy finish, partial back exterior angled to show pro camera system — best single "hero" candidate)
  - `/v/iphone-18-pro/b/images/overview/product-viewer/color_burgundy__f95it7a6dnyq_large.jpg`
  - `/v/iphone-18-pro/b/images/overview/product-viewer/color_glacier__fkxlpbz0ruy6_large.jpg`
  - `/v/iphone-18-pro/b/images/overview/product-viewer/color_silver__c0oudn0fzw4m_large.jpg`
  - `/v/iphone-18-pro/b/images/overview/product-viewer/color_black__dseo2tvypuc2_large.jpg`
- **WHICH BEAT:** iPhone 18 Pro Max hero shot for the hook / cover, or a cutaway during
  the "biggest battery Apple has ever shipped in a phone" line. NOT proof of the
  Prepare to Ship feature — it's the product, not the software.
- **PROVENANCE:** Official Apple press/product photography (apple.com CDN). These are
  landscape/product renders, not mobile-captured — will need reframing to 9:16 (crop
  or motion-graphic treatment), consistent with how the reel already treats hero
  product shots.

## Apple Newsroom launch release (separate, general iPhone 18 Pro launch, not battery-specific)

- **SOURCE URL:** https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/
- **WHAT IT SHOWS:** General iPhone 18 Pro/Pro Max launch imagery (camera system,
  Dynamic Island, Photographic Styles) — no Prepare to Ship or battery-shipping
  content. Useful only as a general b-roll/press-image source for device hero shots,
  same caveat as Asset 5 (reframe to 9:16, not mobile-native).

---

## SEARCHED, NOT FOUND

- **A real screen recording or screenshot of an actual device going through the live
  Prepare to Ship flow (any state: the toggle, the in-progress discharge/percentage
  countdown, or the "Ready to Ship" red badge end state) from ANY outlet.** Searched
  directly ("Prepare to Ship iPhone 18 Pro Max screenshot settings screen recording")
  and via TikTok/YouTube Shorts angle ("20 watt-hour iPhone 18 Pro Max battery
  shipping feature video"). Every hit was a text writeup of the same Apple support
  page; none embeds or links a hands-on capture. This is worth re-checking closer to
  production since Prepare to Ship requires an already-activated device being
  shipped — a scenario (repair/trade-in) that takes time to occur after a 2026-09
  launch, so a real hands-on recording may not exist yet from anyone.
- **A dedicated screenshot of the in-progress discharge/percentage screen.** Apple's
  support page describes it ("may take only a few minutes or up to a couple of hours,"
  "iPhone may get warmer than usual") but does not illustrate it with a second image —
  only the one Prepare to Ship confirmation screen (Asset 1) is illustrated.
  Text-graphic recreation will be needed for this beat.
- **A dedicated screenshot of the "Ready to Ship" red-badge end state.** Confirmed by
  search summary text (Apple: "the iPhone shows a 'Ready to Ship' status in Settings")
  but no image of this state was found anywhere, including on Apple's own support
  page. Will need to be built as an on-screen text/graphic recreation, clearly
  distinguished from a real capture, or simulated on our own test device if any
  current iPhone exposes an equivalent-looking Transfer/Reset menu state to shoot
  against (note: the actual red "Ready to Ship" badge itself is 18-Pro-Max-only and
  cannot be reproduced on other hardware).
- **Video content (Apple explainer video, YouTube/TikTok hands-on) of the feature.**
  None surfaced in search. The story currently rests entirely on text reporting plus
  one static Apple image.
- **A confirmed high-confidence description of the GSMArena inline images (Asset 4).**
  WebFetch reads HTML/text, not image pixels, so the actual content of
  `gsmarena_001.jpg` / `gsmarena_006.jpg` is unconfirmed — needs an actual visual
  check (e.g. `tools/capture.mjs` or opening the image URL directly) before ruling it
  in or out as a second real screenshot source.
- **MacRumors' full-resolution version of its header image** — only the 400px
  thumbnail transform was extractable from HTML; a larger crop may exist at the same
  base path but was not verified.
