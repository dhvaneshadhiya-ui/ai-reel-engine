# Research — siri-ai-ios27

Claims ledger + search log. Findings files in `research/`. Primary source for
every step is Apple's own support page + Apple's own support video; outlets are
corroboration (most VIA Apple). Labels were read off Apple's video frames at
full resolution (_sources/siri-ai-ios27/scout/grid1.jpg, grid2.jpg).

## CLAIMS

- CLAIM: Siri AI is opt-in: after updating to iOS 27 you must start it yourself from Settings.
  TIER: official
  SPOKEN: "Siri AI stays off until you ask for it"
  SURPRISE: 60
  SRC: https://support.apple.com/en-us/127893
  VIA: Apple Support
  SRC: https://www.macrumors.com/2026/09/15/ios-27-siri-ai-has-waitlist-how-to-join/
  VIA: Apple Support, relayed

- CLAIM: The path is Settings > Siri (scroll down) > Try Siri AI (Beta), shown at the top of the Siri page.
  TIER: official
  SPOKEN: "Open Settings, scroll down and tap Siri. At the top, tap Try Siri AI, Beta."
  SURPRISE: 55
  SRC: https://support.apple.com/en-us/127893
  VIA: Apple Support ("tap or click Siri, then tap or click Try Siri AI (Beta)")
  SRC: https://www.youtube.com/watch?v=-kduVTOdI6s
  VIA: Apple Support video 0:20-0:31 ("In Settings, scroll down and tap Siri")

- CLAIM: Next is a Continue on the "Siri with Apple Intelligence" intro, then Continue on the privacy screen.
  TIER: official
  SPOKEN: "Then Continue, and Continue again on the privacy screen."
  SURPRISE: 20
  SRC: https://www.youtube.com/watch?v=-kduVTOdI6s
  VIA: Apple Support video 0:29-0:45 ("tap Continue when you're ready")

- CLAIM: Depending on the device, setup offers voice choice with pace and expressivity sliders ("Customize Your Siri Voice").
  TIER: official
  SPOKEN: "Depending on your iPhone, you'll then pick a voice and set its pace."
  SURPRISE: 45
  SRC: https://www.youtube.com/watch?v=-kduVTOdI6s
  VIA: Apple Support video 0:45-0:55 ("Depending on your device, you might have the option to select the voice")
  SRC: https://9to5mac.com/2026/09/18/apple-intelligence-now-requires-almost-double-the-iphone-storage-on-latest-models/
  VIA: Apple Support 121115 (voice customization on newest models)

- CLAIM: You might be put on a waitlist; when admitted, the Siri app downloads and installs automatically.
  TIER: official
  SPOKEN: "you might land on a waitlist. When your turn comes, the Siri app installs itself."
  SURPRISE: 65
  SRC: https://support.apple.com/en-us/127893
  VIA: Apple Support ("wait times can vary")
  SRC: https://www.theapplepost.com/2026/09/14/72199/siri-ai-stuck-on-waiting-list-in-ios-27-heres-what-you-can-do/
  VIA: Apple Support, relayed

- CLAIM: Siri AI needs iPhone 15 Pro / 15 Pro Max, any iPhone 16 or later, or iPhone Air, while iOS 27 itself runs on many older iPhones.
  TIER: official
  SPOKEN: "you need an iPhone 15 Pro or newer, not just any phone that runs iOS 27"
  SURPRISE: 70
  SRC: https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/
  VIA: Apple Newsroom ("iPhone 16 models or later, iPhone 15 Pro, iPhone 15 Pro Max")
  SRC: https://9to5mac.com/2026/09/14/here-are-the-requirements-to-get-siri-ai-in-ios-27/
  VIA: Apple, relayed

- CLAIM: Device language and Siri language must be set to the same supported language, and Siri AI is English-only at launch.
  TIER: official
  SPOKEN: "your iPhone language and Siri language have to match, and for now that means English"
  SURPRISE: 75
  SRC: https://support.apple.com/en-us/127893
  VIA: Apple Support ("device language and Siri language are set to the same supported language")
  SRC: https://www.bgr.com/2265148/how-to-enable-siri-ai-ios-27-guide/
  VIA: BGR's own walkthrough (English (United States) fix)

- CLAIM: Siri AI is not available on iPhone in the EU, or for mainland China, at launch.
  TIER: official
  SPOKEN: "Siri AI isn't available in the EU or mainland China yet"
  SURPRISE: 40
  SRC: https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/
  VIA: Apple Newsroom
  SRC: https://sixcolors.com/post/2026/09/ios-27-review-little-things-mean-a-lot/
  VIA: Six Colors review ("it won't be available there")

- CLAIM: You can reach Siri AI by swiping down from the Dynamic Island, then typing or tapping the mic to speak.
  TIER: official
  SPOKEN: "swipe down on the Dynamic Island and type, or just talk"
  SURPRISE: 55
  SRC: https://www.youtube.com/watch?v=-kduVTOdI6s
  VIA: Apple Support video 1:48-2:10
  SRC: https://www.macrumors.com/guide/ios-27-siri/
  VIA: MacRumors guide ("Search or Ask")

- CLAIM: After enabling, the device indexes content locally; Apple says it might take a few days to finish, and personal-context results may be incomplete meanwhile.
  TIER: official
  SPOKEN: "Apple also says it can take days to finish indexing your phone, so answers about your own stuff may be patchy at first"
  SURPRISE: 85
  SRC: https://www.youtube.com/watch?v=-kduVTOdI6s
  VIA: Apple Support video 1:10-1:34 ("It might take a few days to finish optimizing")
  ONE-SOURCE-OK: Apple's own support video is the authority on its own setup behaviour; no outlet repeated this line.

## FEATURES + HOW TO USE

- Try Siri AI (Beta) entry point — USED (the core step)
- Intro + privacy Continue screens — USED
- Voice / pace / expressivity — USED (pace named; expressivity CUT for length)
- Share audio/text with Apple prompt — CUT (a prompt, not a decision the viewer needs help with)
- Waitlist + auto-install of Siri app — USED
- Dynamic Island swipe, type or talk — USED
- Side button / "Siri" / "Hey Siri" — CUT (viewers already know these)
- Indexing "a few days" caveat — USED
- Siri app history grid, search, new conversation, attachments — CUT (a second reel: using Siri AI)
- Personal context / onscreen awareness / app actions / web knowledge — CUT (feature reel, not setup)
- Daily usage limits, iCloud+ higher limits — CUT (no price or numbers published)
- Storage up to 14 GB / 8 GB — CUT (Apple Support 121115; true but not a step)

## NOT CLAIMED

- Any iPhone RAM minimum — no source gives one.
- "Siri is Gemini" / Google handles requests — Apple says models were custom-built with Google's Gemini; runs on device + Private Cloud Compute.
- Waitlist durations — anecdotal only (minutes to days).
- iGeeksBlog's "Try New Siri" label — Apple's screens say "Try Siri AI (Beta)".
- Our 2026-08-17 ios27-tiers reel said full Siri AI is 17 Pro / 17 Pro Max / Air only — superseded: Apple's shipped list is 15 Pro and later; only voice customization / better dictation are newest-model only.
- Extensions (ChatGPT/Gemini/Claude inside Siri) — pre-release Bloomberg report only.
- Forum fixes from the 2024 iOS 18.1 waitlist — not iOS 27.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-25  "Siri AI iOS 27 Apple newsroom"  (N1 launch post, devices, EU/China, English first)
- 2026-09-25  "support.apple.com how to get Siri AI"  (127893: path, waitlist, language rule)
- 2026-09-25  "Apple Support video How to get Siri AI"  (every setup screen, indexing caveat)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by
###    someone who is not the vendor
- 2026-09-25  "iOS 27 Siri AI review"  (TechCrunch, Six Colors: capable, with mistakes)
- 2026-09-25  "how to enable Siri AI iOS 27"  (BGR, MacRumors, iPhone in Canada walkthroughs)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-25  "Siri AI not showing iOS 27" / "stuck waitlist"  (The Apple Post, iPhone in Canada commenters: missing button, English (Canada), waitlist)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if
###    you were trying to prove the story wrong
- 2026-09-25  "Siri AI only iPhone 17 Pro"  (the pre-launch three-phone claim: Apple's shipped list is wider; 17 Pro tier is voice customization only)
- 2026-09-25  "Siri AI Apple Intelligence & Siri settings"  (one OSXDaily commenter; Apple's own screens show the Siri row)

INDEPENDENT-CHECK: 2026-09-25 searched hands-on reviews and setup walkthroughs — found TechCrunch (Ivan Mehta) and Six Colors (Dan Moren) reviews, plus BGR / MacRumors / iPhone in Canada walkthroughs that match Apple's steps; the label order was then confirmed on Apple's own video frames.
