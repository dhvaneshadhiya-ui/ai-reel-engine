# Findings: CarPlay audio scrubbing + Home Screen widgets (iOS 27)

Researched 2026-09-28. iOS 27 released 2026-09-14. All pages fetched in full (WebFetch), not snippets.
Quotes are verbatim, under 15 words.

## A. Audio scrubbing on the Now Playing progress bar

**What it does**
- Now Playing gets a draggable progress bar: drag to any point instead of repeated skip taps.
  - https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/ (Tim Hardwick, 2026-09-17):
    "allowing you to drag to any point in a song or podcast"
- Covers music, audiobooks and podcasts; bar is larger and iPhone-like, "easy to grab and drag".
  - https://9to5mac.com/2026/09/21/heres-everything-new-for-carplay-in-ios-27/ (Ryan Christoffel, 2026-09-21):
    "a larger progress indicator that's similar to the iPhone design"
- Pre-release corroboration: https://www.macrumors.com/guide/ios-27-carplay/ (Juli Clover, dated 2026-08-18):
    "jump to a specific spot in a song, podcast, or audiobook"
- The "before" state (for a hook): previously you could not seek at all.
  - https://www.kbb.com/car-news/apples-new-ios-27-brings-a-host-of-updates-to-carplay/ (Chris Teague, 2026-09-17):
    "Previously, users could not move forward or backward in a song"
  - NOTE: KBB's sentence continues "...letting them skip ads" — garbled as written; read as "the new bar lets them skip ads". Do not quote the tail on screen.
- Ships alongside a persistent MiniPlayer (artwork + controls while browsing) — MacRumors 2026-09-17: "a persistent mini-player that keeps artwork and controls on screen". KBB and 9to5Mac also mention it.

**How to use:** no setup. Open Now Playing on CarPlay, press and drag the progress bar. (Inferred from all three descriptions; no source gives step-by-step.)

**Requirements/limits**
- MacRumors 2026-09-17 lists it as working in any CarPlay vehicle (no CarPlay Ultra / specific-car dependency). Needs iPhone on iOS 27.
- No source mentions wired vs wireless differences.
- No source says whether third-party audio apps (Spotify, Overcast, Audible) get it automatically or need an app update. OPEN QUESTION — verify on a real car/simulator before scripting "every app".

## B. Any compatible iPhone Home Screen widget on the CarPlay widgets screen

**What it does**
- CarPlay was previously limited to Apple's own stock widgets (widgets arrived in CarPlay with iOS 26 — Apple-only set); iOS 27 opens it to any compatible Home Screen widget, including third-party.
  - https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/ :
    "CarPlay is no longer limited to Apple's handful of stock widgets"
    "Any compatible widget from your iPhone's Home Screen can now be added"

**How to add (set on the iPhone, not on the car screen)**
- Settings > General > CarPlay > tap your car > Widgets > Add Widgets.
  - MacRumors 2026-09-17: "Settings ➝ General ➝ CarPlay, tap your car, then tap Widgets"
- Manage: drag to rearrange, tap to remove, toggles for Smart Rotate and Widget Suggestions.
  - MacRumors 2026-09-17: "toggle Smart Rotate and Widget Suggestions"

**Requirements/limits**
- MacRumors 2026-09-17: works in any CarPlay vehicle; iPhone on iOS 27.
- "Compatible" is undefined in every source read — which widgets/sizes qualify, whether interactive widgets stay interactive while driving, whether developers must opt in. OPEN QUESTION.
- No wired/wireless distinction stated.

## Corroboration count
- A (scrubbing): MacRumors (x2), 9to5Mac, KBB — 3 independent outlets. SOLID.
- B (third-party widgets): MacRumors 2026-09-17 only (fetched). Search snippets echo it from manofmany.com, supercarblondie.com, asumetech.com, newsbeep.com (the newsbeep pages are syndicated copies of MacRumors — VIA MacRumors). 9to5Mac (2026-09-21) and KBB do NOT mention it; MacRumors' August iOS 27 CarPlay guide does not mention it either. SINGLE-SOURCE until a second outlet or Apple page is fetched.

## Looked for and NOT found
- Apple primary source: https://www.apple.com/ios/ios-27/ returned 404. No Apple Newsroom WWDC 2026 release, support.apple.com CarPlay page, or "all new features" PDF surfaced in search. No Apple wording for either feature yet.
- Exact definition of "compatible widget"; developer opt-in (WidgetKit/CarPlay entitlement) details.
- Third-party audio app support for scrubbing.
- Wired vs wireless differences for either feature.
- User complaints: none in the articles read. A MacRumors Forums thread exists (https://forums.macrumors.com/threads/which-ios-27-carplay-features-actually-work-in-your-car.2489634/) but was not fetched — best place to look next.
- thedrive.com coverage — not searched (budget).
