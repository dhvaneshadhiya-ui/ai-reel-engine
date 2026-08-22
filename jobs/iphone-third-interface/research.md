# Research — iphone-third-interface

Claims ledger + search log. `script_approval.py propose` refuses
while template placeholders remain; format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

NOTE ON SOURCING (user directive, 2026-08-22): this reel is restricted to
FIRST-PARTY visual and factual sources — the developer's own site and the
developer's own App Store listing. Third-party coverage (Product Hunt,
YouTube, blogs) was read for orientation only and supplies nothing here.
Both SRC domains therefore trace to one ultimate origin: the developer.
That is a deliberate, stated constraint, not a research gap. Every claim
below is a description of what the product does, sourced from the party
that makes it — the appropriate tier for product capability claims. No
performance, popularity, or comparative claim is made anywhere in the
script, so nothing here needs an independent origin to be honest.

## CLAIMS

- CLAIM: The iPhone acts as a third control interface for the Mac, after
  the keyboard and the trackpad.
  TIER: official
  SPOKEN: "a third input device"
  SRC: https://choclift.com/
  VIA: developer's own site — its positioning line is "After the keyboard
       and trackpad redefined how we interact with computers, it's time for
       the next step: ... the third interface in your Mac setup".

- CLAIM: The iPhone acts as a customizable touch control surface for the Mac.
  TIER: official
  SPOKEN: "into a custom control panel for your Mac"
  SRC: https://choclift.com/
  VIA: developer's own site — "Use your iPhone to access apps, Shortcuts,
       websites and emojis on your Mac", with up to 8 customizable pages.
       Demonstrated in official-websites (tap a tile, the Mac responds).

- CLAIM: Tapping an icon on the iPhone launches or switches to a Mac app.
  TIER: official
  SPOKEN: "Tap once to open the apps you use every day"
  SRC: https://choclift.com/
  VIA: developer's own site — "Launch and switch between Mac apps instantly
       from your iPhone". Demonstrated end to end in official-apps.

- CLAIM: An Apple Shortcut can be added and triggered from the iPhone, so a
  multi-step workflow runs from one tap.
  TIER: official
  SPOKEN: "Add a shortcut, and a whole workflow becomes one button"
  SRC: https://choclift.com/
  VIA: developer's own site — "Add shortcuts, customize them with emojis
       and trigger them directly". Demonstrated in official-shortcuts,
       where TILE LAST 4 WINDOWS is tapped and the Mac re-tiles.

- CLAIM: Finger gestures on the iPhone move and minimize Mac windows.
  TIER: official
  SPOKEN: "control windows with gestures"
  SRC: https://choclift.com/
  VIA: developer's own site — "Minimize and maximize apps with a swipe".
       Demonstrated in official-gestures.

- CLAIM: It needs a companion Mac app, and both devices on the same Wi-Fi;
  the actions run locally on the Mac.
  TIER: official
  SPOKEN: "It needs a companion app on your Mac and the same"
  SRC: https://apps.apple.com/us/app/choclift-workflow-sweetener/id6759246284
  VIA: developer's own App Store listing — "All actions are executed
       locally on your Mac through the companion app"; requires iOS 18.0+,
       macOS 14+, both devices on the same Wi-Fi network.

- CLAIM: Websites can be saved with custom names and launched on the Mac with
  a single tap from the same grid.
  TIER: official
  SPOKEN: "Save the sites you always open"
  SRC: https://choclift.com/
  VIA: developer's own site — "Save websites with custom names and launch them
       with a single tap." Demonstrated end to end in official-websites.

- CLAIM: A timeline of recently opened Mac apps can be scrolled from the iPhone
  and tapped to switch straight to one.
  TIER: official
  SPOKEN: "Scroll back through everything you had open"
  SRC: https://choclift.com/
  VIA: developer's own site — "Jump back through a timeline of your recent apps
       and pin favorites to the front. No more Cmd+Tab cycling."
       Demonstrated in official-recents.

## CUT FROM THE SPOKEN SCRIPT (2026-08-22, user direction)

Only the **Emoji Bar** is left out. It is real and sourced, and it was in the
first cut; the reel now demonstrates five features end to end and a sixth
would cost every other one its room. Nothing about it is claimed here, and no
emoji footage appears in the cut.

## NOT CLAIMED — and why (mirrored into the manifest)

- NOT CLAIMED: any speed, productivity, time-saved or popularity figure.
  No such figure is published by the developer and none is invented.
- NOT CLAIMED: that it replaces the keyboard, trackpad, Stream Deck, or
  any competing product. No comparison is made.
- NOT CLAIMED: price. The listing shows free with in-app purchases
  ($2.99/month, $29.99 lifetime, 7-day trial) — accurate as of
  2026-08-22, deliberately left out of a 40-second reel because prices
  change and the reel carries no price on screen.
- NOT CLAIMED: that it controls iPhone apps. It is the reverse — the
  iPhone is the input surface, the Mac does the work.
- BANNED FROM THE CUT: official-hero.mp4 in its entirety, and
  official-gestures.mp4 after t=9.0s. Both carry the product wordmark
  baked into the frame (see manifest `nameSafe`), which the user's brand
  restriction forbids on screen.

## SEARCHED

- 2026-08-22  fetched https://choclift.com/ (mobile viewport, 375x812)
  — settled the six features, the exact vendor wording for each, the
  "third interface" positioning line, the no-AI/shot-on-iPhone-15-Pro
  statement, and the 7 first-party product video URLs.
- 2026-08-22  fetched https://apps.apple.com/us/app/choclift-workflow-sweetener/id6759246284
  — settled system requirements (iOS 18 / macOS 14 / visionOS 26), the
  companion-Mac-app requirement, same-Wi-Fi requirement, local execution,
  pricing, version 2.3, developer identity.
- 2026-08-22  OCR name audit (tesseract, 4fps, 467 frames) across all 7
  official clips — located every on-frame occurrence of the wordmark.
  Result: hits in official-gestures (t>=10.0s) and official-hero (t>=51s).
  A manual frame review then found a wordmark OCR MISSED in official-hero
  at t=41-46s, under the "App Time Travel" card. Conclusion recorded:
  OCR is a screen, not a proof — the final rendered reel is audited
  frame-by-frame before delivery, and hero is dropped entirely.
