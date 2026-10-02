# Research — ios27-accessibility-features

Claims ledger + search log. Findings in `research/` (plan.md,
findings_vision_namerecog.md, findings_voicecontrol_reader.md,
findings_subtitles_facetime_games.md, findings_shipped_visuals.md, visuals.md).
Lead: BGR 2026-05-20 (José Adorno), a preview written off Apple's 2026-05-19
Newsroom release — used as a lead only, never a SRC. Every spoken claim traces
to Apple (Newsroom, iOS 27 release notes 149076, the iOS 27 iPhone User Guide,
apple.com/accessibility). apple.com/ios/ios-27/ returned 404 on 2026-10-02.

## CLAIMS

- CLAIM: Magnifier in iOS 27 can answer a spoken/typed question about what the camera sees, e.g. the total on a bill ("Ask Magnifier").
  TIER: official
  SPOKEN: "point your iPhone at a bill, ask how much it is, and it reads you the total"
  SURPRISE: 75
  SRC: https://support.apple.com/guide/iphone/magnify-information-iphe867dc99c/ios
  VIA: Apple iPhone User Guide (iOS 27): "ask questions about what your camera sees, like the total on a bill"
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom image: "How much is the bill for?" → "$83.89"
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple iOS 27 release notes: Magnifier "conversational visual assistance for users with low vision"

- CLAIM: These are iOS 27 features (shipped 2026-09-14), five of the accessibility additions Apple announced 2026-05-19.
  TIER: official
  SPOKEN: "In iOS 27"
  SPOKEN: "one of five accessibility upgrades worth turning on"
  SURPRISE: 40
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple "About iOS 27 Updates", Accessibility section under the iOS 27 heading
  SRC: https://www.macrumors.com/2026/09/14/apple-releases-ios-27/
  VIA: MacRumors release article (reprints Apple's notes)

- CLAIM: In Magnifier you tap Ask and can ask follow-up questions; Apple's own example follows the bill total with "When is this due?" → April 28, 2026.
  TIER: official
  SPOKEN: "Tap Ask, and you can ask a second question, like when the bill is due."
  SURPRISE: 55
  SRC: https://support.apple.com/guide/iphone/magnify-information-iphe867dc99c/ios
  VIA: Apple guide (tap Ask, then pick "What is this?" or type/speak a question)
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom: "ask follow-up questions in their own words"; Magnifier image shows "When is this due?"

- CLAIM: Voice Control in iOS 27 lets you describe on-screen items in natural language ("Flexible Item Names", on by default) instead of exact labels or numbers; Apple's demo says "Tap the orange folder" in Files and the folder opens.
  TIER: official
  SPOKEN: "Voice Control stops making you memorize button names. Say "tap the orange folder," and it opens."
  SURPRISE: 65
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom: "instead of memorizing exact labels or numbers"; Voice-Control-demo.mp4 (Apple media kit)
  SRC: https://support.apple.com/guide/iphone/use-voice-control-iph2c21a3c88/ios
  VIA: Apple guide: "refer to an item by its name, what it does, its color, or where"
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes: "describing elements on screen in your own words, like 'tap the gear'"

- CLAIM: VoiceOver (Image Explorer) gives detailed descriptions of images and lets you ask questions about them (Explore Image / Ask About Image / Intelligent Image Description).
  TIER: official
  SPOKEN: "VoiceOver describes a photo in detail and answers questions about what's in it."
  SURPRISE: 60
  SRC: https://support.apple.com/guide/iphone/get-live-descriptions-of-your-surroundings-iph37e6b3844/ios
  VIA: Apple guide: "Ask questions and get information about images: Turn on Ask About Image."
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom: Image Explorer "more detailed descriptions of images systemwide"

- CLAIM: Name Recognition notifies you when your name is detected; in iOS 27 it works in more than 50 languages (54 language-regions on Apple's list, including Hindi (India)). It existed in iOS 26 — this is an expansion, spoken as "now works in", never as new.
  TIER: official
  SPOKEN: "Name Recognition alerts you when someone says your name, and it now works in more than 50 languages, including Hindi."
  SURPRISE: 70
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom: "can notify users who are deaf or hard of hearing if someone says their name"; "works across more than 50 languages globally"
  SRC: https://www.apple.com/ios/feature-availability/
  VIA: Apple feature-availability, "Accessibility: Name Recognition": 54 entries incl. Hindi (India)
  SRC: https://support.apple.com/guide/iphone/use-name-recognition-iphb865d79be/ios
  VIA: Apple guide: "continuously listen for your name and notify you"; "available on iOS 26 and later"

- CLAIM: Name Recognition needs no Apple Intelligence: it works on any iPhone running iOS 26 or later, so any iPhone with iOS 27.
  TIER: official
  SPOKEN: "Name Recognition works on any iPhone with iOS 27."
  SURPRISE: 50
  SRC: https://support.apple.com/guide/iphone/use-name-recognition-iphb865d79be/ios
  VIA: Apple guide: "Name Recognition is available on iOS 26 and later." (no Apple Intelligence note, unlike the other four)
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom lists it under Additional Updates, outside the Apple Intelligence features

- CLAIM: Videos without captions get generated subtitles automatically (shown when muted), including clips recorded on iPhone; generated privately with on-device speech recognition.
  TIER: official
  SPOKEN: "videos with no captions now get subtitles on their own, even clips you shot, made right on the phone"
  SURPRISE: 70
  SRC: https://support.apple.com/guide/iphone/display-subtitles-and-captions-iph3e2e23d1/ios
  VIA: Apple guide: subtitles appear automatically "if your iPhone is muted"; Photos and Messages
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom: "clips recorded on iPhone"; "With on-device speech recognition, subtitles are generated privately"
  SRC: https://www.idownloadblog.com/2026/09/08/turn-off-automatic-subtitles-ios-mac/
  VIA: iDownloadBlog's own use after release (Automatic Subtitles toggles)

- CLAIM: Magnifier, Voice Control, VoiceOver and generated subtitles need an Apple Intelligence iPhone: iPhone 15 Pro / 15 Pro Max or any iPhone 16 or later.
  TIER: official
  SPOKEN: "The rest run on Apple Intelligence, so you need an iPhone 15 Pro or later."
  SPOKEN: "four of them come with a catch"
  SURPRISE: 60
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes: Accessibility under "Apple Intelligence across apps (All iPhone 16 models and later, iPhone 15 Pro, iPhone 15 Pro Max)"
  SRC: https://support.apple.com/guide/iphone/display-subtitles-and-captions-iph3e2e23d1/ios
  VIA: Apple guide: generated subtitles "available on iPhone 15 Pro, iPhone 15 Pro Max, and iPhone 16 models or later"

- CLAIM: Voice Control natural language is English-only in the US, Canada, UK and Australia; generated subtitles English-only in the US and Canada.
  TIER: official
  SPOKEN: "Voice Control and the subtitles are English-only, in places like the US and Canada."
  SURPRISE: 65
  SRC: https://www.apple.com/accessibility/
  VIA: Apple: "Generated subtitles are available in English in Canada and the U.S."; Voice Control "available in English in Australia, Canada, the UK, and the U.S."
  SRC: https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  VIA: Apple Newsroom footnotes 3 and 4

## FEATURES + HOW TO USE

Every accessibility addition in Apple's 2026-05-19 release and the iOS 27
release notes, marked USED or CUT. How-to steps are Apple's own (iPhone User
Guide, iOS 27), detail in research/findings_*.md.

- Ask Magnifier (Apple Intelligence) — USED (#1 + hook). Open Magnifier, tap Ask, pick "What is this?" or type/speak a question; follow up in the Ask sheet. Settings: Magnifier gear > Ask Magnifier.
- Voice Control Flexible Item Names — USED (#2). Settings > Accessibility > Voice Control > Set Up Voice Control (Wi-Fi for a one-time download); Flexible Item Names is on by default. English, US/CA/UK/AU.
- VoiceOver Image Explorer / Ask About Image / Intelligent Image Description — USED (#3). Settings > Accessibility > VoiceOver > VoiceOver Recognition; select an image, swipe down for options, double-tap.
- Accessibility Reader cleanup, summaries, translation — CUT (user, 2026-10-02: swapped for Name Recognition). Was Settings > Accessibility > Read & Speak > Accessibility Reader; open via Accessibility Shortcut (triple-click side button), Control Center or the share menu; tap Summarize; translate from the menu.
- Generated subtitles — USED (#5). On automatically when muted; Settings > Accessibility > Subtitles & Captioning > Automatic Subtitles (iDownloadBlog path); per video in the playback menu. English, US/CA.
- Live Recognition Ask + follow-ups — CUT as its own item: folded into VoiceOver (#3); a second VoiceOver item splits one idea.
- Action button ask (VoiceOver/Magnifier) — CUT: disputed (GeeksModo: options never appeared).
- Magnifier high-contrast interface + spoken "zoom in" — CUT: not in Apple's iOS 27 Magnifier guide.
- Name Recognition 50+ languages — USED (#4, user's pick 2026-10-02). Spoken as an expansion ("now works in"), since it shipped in iOS 26. Settings > Accessibility > Sound & Name Recognition > Name Recognition > Set Up Name Recognition; Control Center toggle; record how your name is said.
- FaceTime interpreter API — CUT: iOS 27.2 developer beta, developer-only.
- Sony Access controller — CUT: no post-release confirmation.
- Larger Text on Apple TV, Vision Pro wheelchair control, Hikawa grips — CUT: not iPhone features.

## NOT CLAIMED

- Action button shortcut for VoiceOver/Magnifier: Apple notes claim it; GeeksModo (2026-09-13) says the options "haven't appeared". Disputed → not said, not shown.
- Magnifier high-contrast interface and spoken "zoom in"/"turn on flashlight": Newsroom + release notes only, absent from both iOS 27 Magnifier guide pages → not said.
- Name Recognition as NEW in iOS 27 (it shipped in iOS 26; only the 50+ languages are iOS 27), and BGR's "flash" alert (Apple documents a notification only).
- FaceTime sign-language interpreter API: not in 27.0 (iOS 27.2 developer beta 1, Mac Observer VIA MacRumors), developer API, no app has adopted it.
- Sony Access controller support: press release only, no post-release confirmation.
- Accessibility Reader handling "scientific articles" / "multi-column" and translation that keeps "formatting, fonts, and colors": preview (Newsroom) wording only, not in shipping docs → not said.
- "Say what you see", "find files", "jump to app sections" (BGR's Voice Control wording): not Apple's words.
- Any claim that these work on iPhones without Apple Intelligence.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-02  "Apple newsroom May 2026 accessibility features … iOS 27"  (Newsroom 2026-05-19 release, footnotes 1-4)
- 2026-10-02  "iOS 27 release notes Voice Control 27.1 delayed"  (support 149076: Accessibility under Apple Intelligence iPhones)
- 2026-10-02  "support.apple.com iOS 27 Voice Control describe elements Accessibility Reader iPhone user guide"  (guide pages for each feature)
- 2026-10-02  "iOS 27 generated subtitles how to turn on"  (iPhone guide: 15 Pro+, English US/CA)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-10-02  "iOS 27 accessibility released hands-on generated subtitles"  (iDownloadBlog post-release toggles; Tom's Guide beta-era)
- 2026-10-02  "iOS 27 Voice Control natural language hands-on"  (9to5Mac list, no testing; AppleVis 403)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-02  "turn off iOS 27 automatic subtitles"  (Tom's Guide: "pushing it on everyone by default feels like an overreach")
- 2026-10-02  "iOS 27 VoiceOver Live Recognition Action button not working AppleVis"  (GeeksModo: Action button options missing)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-10-02  "iOS 27 Sony Access controller / Name Recognition / FaceTime interpreter API"  (FaceTime API in 27.2 beta; Name Recognition from iOS 26)
- 2026-10-02  "Name Recognition iOS 26 support.apple.com"  (Apple: "available on iOS 26 and later" — not new)

INDEPENDENT-CHECK: 2026-10-02 searched hands-on coverage after the 2026-09-14 release — found iDownloadBlog (subtitle toggles, post-release), Tom's Guide (subtitles on by default, beta), GeeksModo (Action button missing, pre-release); AppleVis and Mac Observer hands-ons returned 403. The five spoken features rest on Apple's own shipping documentation (release notes + iOS 27 User Guide), which is the vendor documenting a shipped OS rather than a promise.
