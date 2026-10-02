# Findings — is the list honest + official visuals
Researched 2026-10-02 (subagent; saved by main session — subagents cannot write files here).

## 1. Primary: Apple Newsroom, 2026-05-19
https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
- Headline "Apple unveils new accessibility features, and updates powered by Apple Intelligence"; "coming later this year"; never names iOS 27. BGR (2026-05-20) VIA Apple.
- Image Explorer "uses Apple Intelligence to give more detailed descriptions of images systemwide"
- Live Recognition "press the Action button on iPhone to quickly ask"; "ask follow-up questions in their own words"
- Magnifier "also works with the Action button"; spoken "zoom in", "turn on flashlight"
- Voice Control "describe onscreen buttons and controls with natural language"; "tap the purple folder"
- Reader "handling text with multiple columns, images, and tables"; "On-demand summaries"; "new built-in translation"
- Subtitles "appear automatically for uncaptioned videos on iPhone, iPad, Mac, Apple TV, and Apple Vision Pro"
- Name Recognition "works across more than 50 languages globally"
- FaceTime "a new API supports users in adding a human interpreter"
- Footnotes: 1 AI languages list; 2 "should not be relied upon … for navigation"; 3 "Voice Control powered by Apple Intelligence will be available in English in the U.S., Canada, the UK, and Australia."; 4 "Generated subtitles will be available in English in the U.S. and Canada."

## 2. Shipped in iOS 27.0
- Release notes https://support.apple.com/en-us/149076 (About iOS 27 Updates): Accessibility under "Apple Intelligence across apps (All iPhone 16 models and later, iPhone 15 Pro, iPhone 15 Pro Max)". VoiceOver "more detailed and contextual image understanding for photos, charts, and screenshots" + "Action button integration"; Magnifier "conversational visual assistance for users with low vision"; Reader "better text cleanup and formatting, images and tables, on-demand summaries, and translation"; Voice Control "describing elements on screen in your own words, like 'tap the gear'". Not listed: subtitles, Name Recognition, FaceTime API, Sony controller.
- https://www.apple.com/accessibility/ — "Generated subtitles are available in English in Canada and the U.S."; Voice Control NL "available in English in Australia, Canada, the UK, and the U.S."
- iPhone User Guide https://support.apple.com/guide/iphone/display-subtitles-and-captions-iph3e2e23d1/ios — generated subtitles "available on iPhone 15 Pro, iPhone 15 Pro Max, and iPhone 16 models or later"; "available in English (U.S. and Canada)"; appear automatically "if your iPhone is muted"; Photos, Messages; labelled "Transcribed".
- https://www.apple.com/ios/feature-availability/ — rows for VoiceOver/Magnifier ask, Voice Control flexible item names, Reader cleanup+summaries, Name Recognition (54 entries). No subtitles row.
- WWDC26 256 https://developer.apple.com/videos/play/wwdc2026/256/

## 3. Contradictions
- Action button ask: GeeksModo 2026-09-13 (pre-release) "These options for the Action button haven't appeared." vs Apple notes. UNRESOLVED → do not script.
- FaceTime API: Mac Observer 2026-09-17 "iOS 27.2 developer beta 1" → not in 27.0.
- Sony controller: no post-release confirmation.

## 4. Table
| Feature | 27.0? | Requirement |
|---|---|---|
| VoiceOver Image Explorer | Yes | AI iPhone |
| Live Recognition Ask | Yes | AI iPhone; LiDAR for detectors |
| Action-button ask | DISPUTED | — |
| Magnifier AI (Ask Magnifier) | Yes | AI iPhone |
| Voice Control NL | Yes | AI; English US/CA/UK/AU |
| Accessibility Reader | Yes | AI |
| Generated subtitles | Yes (guide) | 15 Pro+/16+; English US/CA |
| Name Recognition 50+ | Likely | not stated |
| FaceTime API | No (27.2 beta) | dev API |
| Sony Access controller | Unconfirmed | controller |

## 5. Visuals — media kit in _sources/ios27-accessibility-features/media-kit/ (web copies nr-*.jpg, sheets in frames/)
LEGAL_NOTICE: "personal or editorial and non-commercial"; "cannot be altered or modified in any way".
1. Magnifier 3240x2160 — two portrait iPhones: bill, "How much is the bill for?", "$83.89", "When is this due?" → April 28, 2026. BEST STILL.
2/3. Accessibility Reader on Mac before/after 3840x2160 (two-column PDF → navy/yellow single column, Summarize bar, table).
4. generated-subtitles_inline 3070x3840 portrait, an iPad; caption "Seagulls are very territorial apparently".
5/6. Hikawa grips (accessory). 7-9. Larger Text on Apple TV.
10. Voice-Control-demo.mp4 1080x1080 17.1s — iPhone in Files: "Tap the orange folder" → Final Designs → "Tap the beach pilot" → "Zoom in on solar". BEST MOTION.
11. VoiceOver-with-Apple-Intelligence.mp4 1920x1080 76.4s lifestyle film (Messages image description, "Which is the plain one?" shirts, keys); phone screens small.
12. Wheelchair-Control.mp4 (Vision Pro).
No Image Explorer-only image; none for Name Recognition/FaceTime/Sony.

## Not found
iOS 27 marketing page (404); subtitles/Name Recognition/FaceTime/Sony in 27.0 notes; post-release Action-button or Sony confirmation; AppleVis/MacObserver/Gadget Hacks (403).

## Search log (2026-10-02)
1 Apple Newsroom May 2026 accessibility iOS 27 VoiceOver Image Explorer · 2 iOS 27 accessibility released hands-on generated subtitles · 3 iOS 27 release notes Voice Control 27.1 delayed · 4 iOS 27 "generated subtitles" how to turn on · 5 iOS 27 Voice Control natural language hands-on · 6 iOS 27 Sony Access controller / Name Recognition / FaceTime interpreter API · 7 iOS 27 VoiceOver Live Recognition Action button not working AppleVis
