# Findings — generated subtitles · FaceTime interpreter API · game controller accessibility
Researched 2026-10-02 (subagent; saved by main session — subagents cannot write files here).
Primary for all three: Apple Newsroom 2026-05-19
https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/ (NEWSROOM)

## 1. Generated subtitles
- NEWSROOM: "videos can display transcriptions of spoken audio automatically" (… "when captions or subtitles are not already provided")
- NEWSROOM: "clips recorded on iPhone, received from friends and family, or streamed online"
- NEWSROOM: "With on-device speech recognition, subtitles are generated privately"
- NEWSROOM devices: "iPhone, iPad, Mac, Apple TV, and Apple Vision Pro"
- NEWSROOM: "customized in the video playback menu or in Settings"
- NEWSROOM gap: "subtitles for spoken dialogue are rarely available for personal videos"
- NEWSROOM fn4: "Generated subtitles will be available in English in the U.S. and Canada."
- WWDC26 session 256 https://developer.apple.com/videos/play/wwdc2026/256/ — "Multiple subtitle languages can be generated from English subtitles"; made "live, locally on the device as the media plays"; "you don't need to implement anything to turn on generated subtitles" (AVPlayerViewController); covers "customer-created content, like camera capture from the iPhone and social media videos"
- https://www.apple.com/os/ios/ — "it can even translate existing captions into other languages"
- Settings path (VIA idownloadblog, 2026-09-08 upd. 2026-10-01) https://www.idownloadblog.com/2026/09/08/turn-off-automatic-subtitles-ios-mac/ — Settings > Accessibility > Subtitles & Captioning > Automatic Subtitles; toggles When Languages Don't Match, Show When Muted, Show on Skip Back, Apply across apps. "Turn off the first three options under the Automatic Subtitles section"
- Tom's Guide (VIA Yahoo mirror, 2026-08-05, beta) https://www.tomsguide.com/phones/iphones/how-to-turn-off-ios-27s-automatic-subtitles-that-no-one-asked-for — seen in Photos and Safari; "pushing it on everyone by default feels like an overreach"; per-video More Controls > Subtitles > Off
- Shipped 27.0: yes (post-release idownloadblog + WWDC 256). No Apple Intelligence / device requirement stated — UNVERIFIED, do not say.
- Live Captions vs this: subagent synthesis only (Live Captions = system overlay; generated subtitles = a real subtitle track in the player, can translate).
- Visual: https://www.apple.com/newsroom/images/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/article/Apple-accessibility-features-generated-subtitles_inline.jpg.large.jpg

## 2. FaceTime sign-language interpreter API
- NEWSROOM: "a new API supports users in adding a human interpreter to an ongoing FaceTime video call" — for "sign language interpretation app developers"
- MacRumors (ORIGINAL) https://www.macrumors.com/guide/ios-27-2-beta-features/ (2026-09-16): "That feature appears to be live in iOS 27.2." → NOT in 27.0
- Same beta, TV app: "turn on sign language interpretation when available"
- Mac Observer VIA MacRumors https://www.macobserver.com/news/ios-27-2-facetime-sign-language-interpreters/ — no adopting apps named
- Curb Cuts 2026-09-22 — repeats Apple, no apps
- No adopting app, no user setting, no API name, no image.

## 3. Game controller accessibility (Sony Access Controller)
- NEWSROOM: "connect the Sony Access controller as a game controller with iOS, iPadOS, and macOS"
- NEWSROOM: "configure the thumbstick, nine built-in buttons, and up to four additional external buttons or specialty switches"
- NEWSROOM: "They can also combine two controllers"
- https://support.apple.com/en-us/111100 (2026-09-14) lists "PlayStation Access controller"
- Settings > General > Game Controller: SNIPPET only, unverified. No hands-on; no Newsroom image.

## Looked for and NOT found
AI/device requirement for subtitles; Apple support article for subtitles; Live Captions support body; FaceTime API adopter/name/docs; where "combine two controllers" lives; Access Controller hands-on; Newsroom images for API/controller; subtitles beyond EN US/CA.
Searches: 6 WebSearch, 11 WebFetch (2× 403, 3 truncated).
