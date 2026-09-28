# Findings: Maps / wireless / visual refresh + "is this list honest"

Searched/fetched 2026-09-28. 9 calls (6 fetches OK, 2 fetches failed, 2 searches).
Quotes are verbatim as returned by the fetch tool (a summarizer). Recheck a quote on the live page before it goes on screen.

## E. Natural-language directions in Apple Maps via Siri (avoid tolls/highways)
- https://www.macrumors.com/guide/ios-27-carplay/ : "extended natural language search to navigation". Siri directions can avoid "toll roads, highways, and more".
- https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/ : "You can ask Siri for directions that avoid toll roads, highways" (listed under "Works in Any CarPlay Vehicle", no requirement).
- iPhone requirement is UNRESOLVED. A WebSearch summary said it "operates independently of Apple Intelligence and works on every iOS 27 iPhone", but no page I fetched says that, and I could not tell which page it came from (the likely source, Gadget Hacks, returned 403). MacRumors' "which work" page puts it in the no-requirement group, which points the same way. **Treat it as unverified until Apple or a fetched page confirms it.**

## F. Wireless reliability + GPS accuracy / heading
- https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/ : "Wireless CarPlay connections are more dependable in iOS 27, with improved GPS accuracy."
- https://www.macrumors.com/2026/09/17/seven-ios-27-carplay-features-actually-notice/ : Apple improved "location accuracy and navigation heading detection."
- https://www.pocket-lint.com/ios-27-new-carplay-features-availability/ : "more reliable, with better GPS accuracy for navigational headings" (any iPhone on iOS 27, any car).
- Note: a reliability claim can't be shown on screen, and no source gives a number. Script it as "Apple says", not "fixed".

## G. Visual refresh (Liquid Glass, wallpapers, animations)
- https://9to5mac.com/2026/09/21/heres-everything-new-for-carplay-in-ios-27/ : app icons get "updated Liquid Glass designs in iOS 27"; "new CarPlay wallpapers available now".
- https://www.macrumors.com/guide/ios-27-carplay/ : "wave-style designs in a range of colors, with 14 total options available".
- https://www.macrumors.com/2026/09/17/which-ios-27-carplay-features-actually-work/ : "available in CarPlay in 14 color options" (works in any car).
- Digital Trends VIA WebSearch summary (https://www.digitaltrends.com/cars/everything-new-coming-to-carplay-with-ios-27/, page not fetched): the wallpaper style is called "Celosia". UNVERIFIED.
- Pocket-lint: custom wallpapers are still not supported. The name "Liquid Glass" for CarPlay itself was not confirmed as NEW in iOS 27 (Liquid Glass came with iOS 26). 9to5Mac only says the icons were "updated".
- No source describes new CarPlay **animations**. NOT FOUND.

## Other iOS 27 CarPlay additions (to inform the list)
- **Siri AI** (conversational, synced to the Siri app): 9to5Mac says it "appears as a glowing orb at the bottom-center of the screen" and "conversations you have in CarPlay are automatically synced to the Siri app". The MacRumors "seven" page says it needs iPhone 15 Pro/Pro Max or iPhone 16+ and is "unavailable in EU at launch". The MacRumors "which work" page says "Waitlist access required". Pocket-lint says "Available now". **CONFLICT** on whether there is a waitlist.
- **Custom widgets** from the iPhone Home Screen: MacRumors "which work" says "Any compatible widget from your iPhone's Home Screen can now be added". Pocket-lint says "add almost any widget that you can add to your iPhone's home screen". Works in any car. (Widgets on CarPlay existed in iOS 26. What's new is the wider widget support. Check the wording.)
- **Audio scrubbing**: MacRumors "which work" says "The Now Playing screen now has a proper progress bar". Pocket-lint says "skim the progress bar of a song, podcast, video, audiobook". Works in any car.
- **MiniPlayer**: MacRumors guide says "persistent mini-player" with "artwork and playback controls in the top right corner". Works in any car.
- **Apple Music filters**: MacRumors "which work" says "Filter your library to sort playlists, albums, artists, and songs". Works in any car.
- **Video apps (parked only)**: MacRumors guide says "browse for and watch videos on your in-car display while parked" and "no automakers have announced plans". Needs the automaker to certify it. **Not usable yet.**
- **Route data to the car's built-in nav / cluster**: MacRumors "which work" says "Navigation apps can now pass route data to a vehicle's built-in infotainment" and lists it as not yet available. Pocket-lint says "Available now for compatible cars". **CONFLICT.** Either way it needs the automaker and the app developer to support it.
- **Voice control for all app categories**: MacRumors guide says "All app categories can now offer a voice control option". The developer has to opt in.
- **Apple primary**: https://www.apple.com/carplay/ has not been updated for iOS 27. It covers CarPlay Ultra ("select 2024 and later models") and custom wallpapers for the dashboard, and says nothing new for iOS 27. https://www.apple.com/ios/ios-27/ returned **404**. No Apple newsroom iOS 27 CarPlay page was found. The Digital Trends summary (via search) says the CarPlay updates were "buried in a developer-only video" at WWDC.

## Honesty table
| Feature | Works in any CarPlay car? | iPhone requirement | Usable today? |
|---|---|---|---|
| Siri natural-language directions (avoid tolls/highways) | Yes | iOS 27. Apple Intelligence NOT required per one unverified search summary | Yes |
| Wireless reliability + GPS/heading | Yes (wireless cars) | iOS 27 | Yes |
| New wallpapers (14 colors) | Yes | iOS 27 | Yes |
| Liquid Glass icon refresh | Yes | iOS 27 | Yes |
| Custom Home Screen widgets | Yes | iOS 27 | Yes |
| Audio scrubbing | Yes | iOS 27 | Yes |
| MiniPlayer | Yes | iOS 27 | Yes |
| Apple Music filters | Yes | iOS 27 | Yes |
| Siri AI (conversational) | Yes | iPhone 15 Pro / 16 or later. Not in the EU at launch | Conflicting: "waitlist" (MacRumors) vs "available now" (Pocket-lint) |
| Video apps (parked) | NO, needs automaker certification | iOS 27 | NO, no automaker has signed on |
| Route data to car's built-in nav | NO, needs car + app support | iOS 27 | Conflicting: MacRumors says not yet, Pocket-lint says yes for compatible cars |
| Voice control in all app categories | Yes, if the app developer adopts it | iOS 27 | Depends on the app |

## Looked for, NOT found
- Apple's own iOS 27 CarPlay feature page (apple.com/ios/ios-27 returned 404). Apple Newsroom iOS 27 release text covering CarPlay.
- The Drive, Autoblog and KBB hands-ons (not reached within budget).
- Any iOS 27 change to CarPlay Ultra.
- New CarPlay animations. Live Activities or dashboard layout changes new in iOS 27. Message or notification changes in CarPlay.
- Any number for the wireless or GPS improvement.
- A fetched page confirming whether natural-language directions need Apple Intelligence. Gadget Hacks returned 403.
