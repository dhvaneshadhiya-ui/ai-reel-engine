# Findings: VoiceOver Image Explorer / Live Recognition / Magnifier + Name Recognition (iOS 27)

Researched 2026-10-02. Primary pages fetched in full (Apple Support pages via curl + text extraction, the
Newsroom via WebFetch). Quotes are verbatim and under 15 words. Tiers: PRIMARY = Apple, SECONDARY = press.

## Search log
1. "Apple newsroom May 2026 accessibility features VoiceOver Image Explorer Magnifier Apple Intelligence Name Recognition"
2. "iOS 27 accessibility Image Explorer Name Recognition hands-on September 2026"
3. "support.apple.com iOS 27 Name Recognition Sound Recognition Settings Accessibility"
4. "support.apple.com iPhone user guide iOS 27 VoiceOver Live Recognition Action button Image Explorer Magnifier"
5. "support.apple.com iPhone Magnifier iOS 27 Apple Intelligence ask questions high contrast"
6. "iOS 27 Magnifier high-contrast / zoom in spoken Ask Magnifier hands-on review"

---

## (1a) VoiceOver Image Explorer

- PRIMARY. Announcement (2026-05-19): Image Explorer uses Apple Intelligence for richer image descriptions systemwide.
  SRC https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/
  QUOTE: "including what's in photographs, scanned bills, personal records, and other visual content"
- PRIMARY. Shipped in iOS 27 as three VoiceOver Recognition toggles (the support guide's iOS 27 version).
  SRC https://support.apple.com/guide/iphone/get-live-descriptions-of-your-surroundings-iph37e6b3844/ios
  QUOTE: "Explore content in an image, get descriptions, and ask questions: Turn on Explore Image."
  QUOTE: "Get detailed descriptions of images: Turn on Intelligent Image Description."
  QUOTE: "Ask questions and get information about images: Turn on Ask About Image."
- SETTINGS PATH (same page): Settings > Accessibility > VoiceOver > VoiceOver Recognition > Explore Image /
  Ask About Image / Intelligent Image Description (also Text Recognition).
  QUOTE: "Tap Accessibility, tap VoiceOver, tap VoiceOver Recognition"
- HOW TO USE (same page): select an image in Photos or Safari, swipe down for options, double-tap the option;
  QUOTE: "Move your finger around the image to find out the position of each object."
- Works where apps give no accessibility info. QUOTE: "even if they don't provide accessibility information"
- REQUIREMENT (same page, verbatim note): QUOTE: "Apple Intelligence-enabled iPhone 15 Pro, iPhone 15 Pro Max, or iPhone 16 model or later"
  plus "Apple Intelligence is not available in all languages or regions. Usage limits may apply."
  Image descriptions: QUOTE: "Image descriptions aren't available in all languages."
- RELATED NEW (same page): with VoiceOver focused on the Dynamic Island, Explore Screen / Ask About Screen
  (Settings > Accessibility > VoiceOver > VoiceOver Recognition > Image Descriptions). Dynamic Island models only.
  QUOTE: "explore what's on your screen in detail and ask follow-up questions"
- OFFICIAL VISUAL: Apple Support screenshot, alt "An Image Explorer screen giving a description of a cat adoption flyer."
  https://ipcdn-web.apple.com/assets/v2/web/681c7e46-a53e-4902-ac6e-94e2106e4096 (on the page above)
- SECONDARY (VIA Apple release notes): MacRumors 2026-09-14 iOS 27 release article lists
  QUOTE: "more detailed and contextual image understanding for photos, charts, and screenshots"
  SRC https://www.macrumors.com/2026/09/14/apple-releases-ios-27/  (VIA Apple's iOS 27 release notes, by its wording)

## (1b) Live Recognition + Action button + follow-up questions

- PRIMARY. Announcement: QUOTE: "press the Action button on iPhone to quickly ask a question"
  and QUOTE: "ask follow-up questions in their own words to get more visual information."
  SRC Newsroom URL above.
- PRIMARY. Shipped in iOS 27 support guide: start with VoiceOver on via four-finger triple-tap; "Ask" mode
  asks a default question. QUOTE: "The default question "What is this?" is asked automatically"
  Action button: QUOTE: "You can also customize the Action Button to ask a question in Live Recognition."
  SRC https://support.apple.com/guide/iphone/get-live-descriptions-of-your-surroundings-iph37e6b3844/ios
- SETTINGS (same page): Settings > Accessibility > Live Recognition. Options: Default Question (editable),
  Speak or Type, "Use Volume Buttons to Recapture", Live Recognition Rotor (People, Doors, Scenes, Ask),
  Activities (custom presets with Speech/Braille/Sounds/Haptics per mode). Also Document Capture and Point and Speak.
- SHORTCUTS: Action button, Accessibility Shortcut (triple-click), Back Tap, VoiceOver gesture.
  SRC https://support.apple.com/guide/iphone/set-up-shortcuts-for-live-recognition-ipheea9e5190/ios
  QUOTE: "Press the Action button: Customize the Action button to start Live Recognition."
  QUOTE: "If VoiceOver is off, the shortcut opens the Magnifier app in Detection Mode."
  QUOTE: "The Action button is available on supported iPhone models."
- LIMIT: People/doors/furniture detection only on supported models (LiDAR, per Apple's linked note; not verified here).
  QUOTE: "Detection of people, doors, and furniture is available only on supported iPhone models"
- SAFETY (Newsroom footnote 2): QUOTE: "should not be relied upon ... for navigation"
- WHAT CHANGED vs iOS 26: Live Recognition pre-existed as a VoiceOver/Magnifier detection feature; iOS 27 adds the
  conversational Ask (Apple Intelligence) + Action button entry + follow-ups. The newsroom phrases it as
  QUOTE: "With updates to Live Recognition" (implies it existed). I did NOT fetch the iOS 26 version of the page to
  confirm exactly what Live Recognition did in iOS 26.

## (1c) Magnifier with Apple Intelligence ("Ask Magnifier")

- PRIMARY. Announcement: QUOTE: "a high-contrast interface designed for users who have low vision"
  and spoken control QUOTE: "such as "zoom in" or "turn on flashlight.""; also works with the Action button.
  SRC Newsroom URL above.
- PRIMARY. iOS 27 support guide names the feature "Ask Magnifier":
  QUOTE: "ask questions about what your camera sees, like the total on a bill"
  (full example: "or the color of a shirt"). Tap Ask, then pick "What is this?", or Type/Speak a question.
  SRC https://support.apple.com/guide/iphone/magnify-information-iphe867dc99c/ios
- SETTINGS: in the Magnifier app, Settings (gear) > Ask Magnifier > Input (speak/type) and Default Question;
  show/hide Ask Magnifier in Control Panel.
  SRC https://support.apple.com/guide/iphone/customize-controls-ipheed8d2fca/ios
  QUOTE: "Ask Magnifier is available only on devices with Apple Intelligence."
- REQUIREMENT: same iPhone 15 Pro / 15 Pro Max / iPhone 16+ note on both Magnifier pages.
- AI languages (footnote on both Magnifier pages): Chinese (Simplified/Traditional), Danish, Dutch, English, French,
  German, Italian, Japanese, Korean, Norwegian, Portuguese, Spanish, Swedish, Turkish, Vietnamese.
- SHIPPED? MacRumors' 9/14 release article (reads as Apple's release notes) lists it as in iOS 27:
  QUOTE: "with a high-contrast interface and natural language app controls for zooming"
  SRC https://www.macrumors.com/2026/09/14/apple-releases-ios-27/ (VIA Apple release notes)
  CAVEAT: the two iOS 27 Magnifier support pages document Ask Magnifier but say NOTHING about a high-contrast
  interface or spoken "zoom in" controls. Treat those two as "in release notes, not yet documented"; verify in the
  simulator/device before saying them on camera.
- Existing pre-27 Magnifier pieces still there: Detection Mode (scenes, text, Point and Speak; doors/people/furniture
  on supported models), Accessibility Reader for captured text, activities.
- OFFICIAL VISUALS:
  - Newsroom hero: https://www.apple.com/newsroom/images/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/article/Apple-accessibility-features-Magnifier_big.jpg.large.jpg
    (caption per page: Magnifier high-contrast interface; WebFetch summary described it as a bill inquiry)
  - Support screenshot, alt "The Magnifier app showing a close-up of an unripe apple.":
    https://ipcdn-web.apple.com/assets/v2/web/cd442573-6489-42ac-b013-0711109016f2

## (2) Name Recognition, 50+ languages

- PRIMARY. Announcement: QUOTE: "works across more than 50 languages globally."
  QUOTE: "can notify users who are deaf or hard of hearing if someone says their name"
  SRC Newsroom URL above.
- PRIMARY. Language list on Apple's feature-availability page ("Accessibility: Name Recognition"): I counted
  54 language-region locales, from Arabic (Saudi Arabia) to Vietnamese (Vietnam), incl. Hindi (India),
  English (India), Hebrew, Thai, Ukrainian, Polish, Indonesian, Malay, Cantonese, Mandarin.
  SRC https://www.apple.com/ios/feature-availability/  (page does not state the OS version on that block)
- PRIMARY. It EXISTED in iOS 26 (this is an expansion, not new):
  QUOTE: "Name Recognition is available on iOS 26 and later."
  SRC https://support.apple.com/guide/iphone/use-name-recognition-iphb865d79be/ios
- HOW IT WORKS (same page): QUOTE: "continuously listen for your name and notify you when it's detected"
  You can record how you or someone else says your name; can add multiple names (Add Name).
- SETTINGS PATH: Settings > Accessibility > Sound & Name Recognition > Name Recognition > Set Up Name Recognition.
  Control Center toggle available. QUOTE: "Tap Accessibility, tap Sound & Name Recognition, tap Name Recognition"
- ALERT TYPE: Apple documents a NOTIFICATION. Screenshot alt text: "Name Recognition recognized a sound that may be a name."
  https://ipcdn-web.apple.com/assets/v2/web/372e687e-19bf-40c2-8afd-89c93ccbea89 (official screenshot)
  SECONDARY (iOS 26 era, 2025-11-14): alert also appears on a worn Apple Watch.
  SRC https://www.idownloadblog.com/2025/11/14/how-to-use-name-recognition-ios-macos/
  QUOTE: "the alert will appear on your wrist as well."
- SAFETY: QUOTE: "Don't rely on your iPhone to recognize your name in circumstances where you may be harmed"
- Not Apple Intelligence-gated (no AI note on the page); runs on any iOS 26+/27 iPhone (iOS 27 supports iPhone 11 and later per the guide's model list).
- Sibling feature, same menu: Sound Recognition (doorbell, siren, crying baby, custom alarm/appliance/doorbell).
  SRC https://support.apple.com/guide/iphone/use-sound-recognition-iphf2dc33312/ios

---

## Looked for and did NOT find
- A "flash" (LED or screen flash) alert for Name Recognition: no Apple page says it flashes. Only "notify". Do not say "flash".
- Which iOS 26 languages Name Recognition supported before (so the exact "before -> 50+" jump is unverified).
- Any Apple statement that a feature in this set is deferred to iOS 27.x; nothing says "later". Newsroom said "later this year".
- Apple Support documentation of the Magnifier high-contrast interface and spoken "zoom in"/"flashlight" commands (only in Newsroom + release notes).
- apple.com/ios/ios-27/ returns 404; apple.com/os/ios/ has only one-line summaries ("richer image descriptions and Action button integration").
- A genuine hands-on article published after 2026-09-14: MacObserver's VoiceOver and Magnifier round-ups both return 403 to fetch;
  MyVision Oxfordshire (https://www.myvision.org.uk/ios-27-accessibility-features/) is dated 2026-08-05 (beta era), restating Apple.
- Whether the Action button works for Live Recognition on iPhone 15 (non-Pro) etc.: Apple says only "supported iPhone models".

## Simulator note (for the visual plan)
Settings paths above (Accessibility > VoiceOver > VoiceOver Recognition; Accessibility > Live Recognition;
Accessibility > Sound & Name Recognition) are Settings panes, so likely capturable in the iOS 27 simulator.
Live camera Ask Magnifier/Live Recognition and Apple Intelligence results are NOT (no camera, no AI in sim).
