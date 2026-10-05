# Research — ios27-safari-settings

Claims ledger + search log. Findings in `research/` (plan.md, findings_notify_me.md,
findings_describe_extension.md, findings_tabs_and_honesty.md). Lead: Tom's Guide
(Kaycee Hill, 2026-09-16) — used as a lead only. Every spoken claim traces to
Apple (iOS 27 release notes 149076, iOS 27 iPhone User Guide, Feature
Availability, Newsroom).

## CLAIMS

- CLAIM: In iOS 27, Safari's Notify Me monitors a webpage and notifies you when it changes, e.g. a price drop or restock.
  TIER: official
  SPOKEN: "Safari in iOS 27 will watch it for you and tell you when the price drops"
  SURPRISE: 70
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple iOS 27 release notes: "Notify Me can periodically check a webpage for updates, like price changes and item availability"
  SRC: https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/
  VIA: Apple Newsroom: "monitor a web page for changes, like product restocks or price drops"
  SRC: https://www.cultofmac.com/how-to/safari-notify-me-monitor-website-changes
  VIA: Cult of Mac own testing (got the notification when the watched page changed)

- CLAIM: Notify Me, Describe an Extension and tab topics are three new Safari features in iOS 27.
  TIER: official
  SPOKEN: "setting one of three worth switching on"
  SURPRISE: 50
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes list Notify Me, Describe an Extension and Organize by Topic under Safari, iOS 27
  SRC: https://www.macrumors.com/guide/ios-27-safari/
  VIA: MacRumors iOS 27 Safari guide

- CLAIM: To set it up you tap the Page Menu button (left of the search field), tap Notify Me, and describe what Safari should look for.
  TIER: official
  SPOKEN: "Tap the menu beside the address bar, tap Notify Me, and describe what you're waiting for"
  SURPRISE: 60
  SRC: https://support.apple.com/guide/iphone/browse-the-web-iph1fbef4daa/27/ios/27
  VIA: Apple User Guide: "Tap [Page Menu], then tap Notify Me. Enter details about what Safari should look for."
  SRC: https://ioshacker.com/how-to/monitor-web-pages-in-safari-with-notify-me-on-ios-27
  VIA: iOSHacker hands-on: "menu button (three lines) on the left side of the URL"

- CLAIM: "Back in stock" is a valid kind of thing to watch for (item availability / restock).
  TIER: official
  SPOKEN: "like "back in stock.""
  SURPRISE: 30
  SRC: https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/
  VIA: Apple: "like product restocks or price drops"
  SRC: https://www.idownloadblog.com/?p=1060067
  VIA: iDownloadBlog example: "Alert me when the item is back in stock."

- CLAIM: Safari checks daily by default; you can edit how often it checks.
  TIER: official
  SPOKEN: "Safari checks daily unless you change the schedule."
  SURPRISE: 45
  SRC: https://support.apple.com/guide/iphone/browse-the-web-iph1fbef4daa/27/ios/27
  VIA: Apple User Guide: "tap Edit to adjust how often Safari should check for updates"
  SRC: https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/
  VIA: Apple Newsroom setup screenshot: "Check daily at 10:00 AM  Edit"
  SRC: https://www.cultofmac.com/how-to/safari-notify-me-monitor-website-changes
  VIA: Cult of Mac: "By default, Safari will check the website daily"

- CLAIM: Describe Extension is in the same Page Menu; you describe what you want and Safari generates a custom extension.
  TIER: official
  SPOKEN: "That same menu holds setting two, Describe Extension."
  SPOKEN: "Describe what you want a site to do, and Safari builds the extension."
  SURPRISE: 80
  SRC: https://support.apple.com/guide/iphone/get-extensions-iphab0432bf6/27/ios/27
  VIA: Apple User Guide: "Tap [Page Menu], then tap Describe Extension. Enter a description of what you want to create"
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes: "create a custom extension using natural language"
  SRC: https://iphonelife.com/content/create-custom-extensions-safari
  VIA: iPhone Life hands-on on an iPhone 15 Pro (built a "Cookie Rejector")

- CLAIM: Apple's own example is a toolbar button to save (and rate) recipes.
  TIER: official
  SPOKEN: "Apple's example adds a button that saves recipes."
  SURPRISE: 40
  SRC: https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/
  VIA: Apple: "like adding a button to save and rate recipes a user has tried"

- CLAIM: In the tab view, tap Organize, then Automatically Create Topics, and Safari groups similar tabs into topics.
  TIER: official
  SPOKEN: "In your tabs, tap Organize, then Automatically Create Topics, and Safari sorts them into groups."
  SPOKEN: "Setting three fixes tab clutter."
  SURPRISE: 65
  SRC: https://support.apple.com/guide/iphone/organize-your-tabs-iph3028ebf68/ios
  VIA: Apple User Guide: "tap [Tabs], tap [Organize], then tap Automatically Create Topics"
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes: "automatically grouping similar tabs together"
  SRC: https://www.macrumors.com/guide/ios-27-safari/
  VIA: MacRumors: "icon with three lines in the upper right of the display while in tab view"

- CLAIM: All three require Apple Intelligence: iPhone 15 Pro, iPhone 15 Pro Max, or iPhone 16 and later.
  TIER: official
  SPOKEN: "All three run on Apple Intelligence, which means an iPhone 15 Pro, 15 Pro Max, or any iPhone 16 and up."
  SURPRISE: 55
  SRC: https://support.apple.com/en-us/149076
  VIA: Apple release notes heading: "Apple Intelligence across apps (All iPhone 16 models and later, iPhone 15 Pro, iPhone 15 Pro Max)"
  SRC: https://www.apple.com/ios/feature-availability/
  VIA: Apple: "Apple Intelligence: Safari: Notify me / Describe an extension / Group tabs into topics"
  SRC: https://www.macrumors.com/guide/ios-27-safari/
  VIA: MacRumors: "Safari features like automatic tab grouping, custom extensions, and custom notifications require Apple Intelligence."

## FEATURES + HOW TO USE

Vendor = Apple (iOS 27 iPhone User Guide, release notes 149076). Every iOS 27 Safari feature Apple documents:

- Notify Me — USED (item one; hook). Steps: open page > Page Menu (left of search field) > Notify Me > describe what to look for > Edit to change frequency > checkmark. Manage alerts: Settings > Apps > Safari > Notify Me (outlets).
- Describe an Extension — USED (item two). Steps: Page Menu > Describe Extension > describe or pick a category (Boost Productivity, Improve Focus, Get Creative, Design & Develop) > Safari checks App Store > Create > Try > Edit or checkmark to save. Delete: Page Menu > Manage Extensions > select > Delete Extension.
- Organize by Topic (tab topics) — USED (item three). Steps: Tabs button > Organize > Automatically Create Topics. Off: Organize > Never. Topic actions: Copy Links, Move Tabs, Close Tabs.
- Passwords upgrade to strong passwords via Safari — CUT: a Passwords feature, not a Safari setting you switch on; different list.
- Ask to Browse (parents approve each new site) — CUT: family/Screen Time feature, different audience.
- Hide Distracting Items — CUT: shipped before iOS 27 (iOS 18), not new.
- Speed/battery improvements — CUT: not a setting; benchmark claims only.

## NOT CLAIMED

- "Local machine intelligence" / on-device: Tom's Guide only; Apple never says device vs Private Cloud Compute.
- Tom's Guide's extension examples (reading-time badge, grayscale, block elements): not Apple's.
- "Organize Tabs" as a label: not Apple's wording.
- Notify Me "the moment" a page changes: it checks on a schedule (iDB), not live.
- Notify Me frequency options hourly/weekly/monthly: two outlets (Cult of Mac, iDB) + MacRumors, not Apple; not spoken.
- Notify Me works on every site: iDB says it does not.
- Generated extensions reviewed by Apple / code viewable: not reviewed, no code view (stefanvd.net, beta 1).
- Apple's 2026-09-14 caption "Describe a Shortcut": Apple's own typo, never quoted.
- Any claim these work without Apple Intelligence, in Hindi, or in mainland China.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-05  "iOS 27 Safari Notify Me support.apple.com"  (User Guide steps; release notes 149076)
- 2026-10-05  "Describe an Extension Safari iOS 27 Apple newsroom"  (Newsroom 2026-06-08; User Guide "Create your own extension")
- 2026-10-05  "Safari iOS 27 Automatically Create Topics organize tabs"  (User Guide organize tabs; release notes "Organize by Topic")
- 2026-10-05  "apple.com ios feature-availability Safari Notify me"  (Apple Intelligence devices + languages, no Hindi)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-10-05  "Safari Notify Me iOS 27 how to hands-on"  (Cult of Mac test worked; iOSHacker steps; iDB beta)
- 2026-10-05  "create custom extension Safari iOS 27 hands-on"  (iPhone Life on a 15 Pro; stefanvd.net developer test)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-05  "Safari Notify Me not working iOS 27"  (iDB: not every site; error if Safari can't do it)
- 2026-10-05  "macrumors Safari notify me comments"  (forum skepticism about daily checks; audience language only)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-10-05  "Safari tab topics on-device private cloud compute"  (nothing from Apple; on-device claim dropped)
- 2026-10-05  "Describe an Extension EU not available"  (iThinkDiff beta-era only; unresolved, not spoken)

INDEPENDENT-CHECK: 2026-10-05 searched post-release hands-on for all three — found Cult of Mac (Notify Me worked on an hourly check of Apple's release-notes page), iPhone Life (built an extension on an iPhone 15 Pro), iDownloadBlog (Notify Me unreliable on some sites), MacRumors guide (all three need Apple Intelligence). The spoken steps rest on Apple's iOS 27 User Guide.
