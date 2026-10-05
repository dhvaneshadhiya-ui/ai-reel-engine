# Findings: Safari "Notify Me" (iOS 27). Researched 2026-10-05 (subagent A; saved by main session).

## Name
- Apple "About iOS 27 Updates" https://support.apple.com/en-us/149076 — "Notify Me can periodically check a webpage for updates, like price changes and item availability". Under "Apple Intelligence across apps (All iPhone 16 models and later, iPhone 15 Pro, iPhone 15 Pro Max)" > Safari.
- https://www.apple.com/ios/feature-availability/ — "Apple Intelligence: Safari: Notify me"

## What it does (Apple)
- Newsroom 2026-06-08 https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/ — "users can ask Safari to monitor a web page for changes, like product restocks or price drops"; "when Safari detects a change on that web page, they'll get a notification so they can take action."
- Newsroom 2026-09-14 https://www.apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/ — "On a user's iPhone 18 Pro, the Notify Me feature surfaces a website change on the Lock Screen."

## Steps
- Apple iPhone User Guide https://support.apple.com/guide/iphone/browse-the-web-iph1fbef4daa/27/ios/27 ("Get notified when a website changes"): "Go to a webpage." / "Tap [Page Menu], then tap Notify Me." / "Enter details about what Safari should look for." / "If necessary, tap Edit to adjust how often Safari should check for updates" / "At the time interval you set, a notification appears on your iPhone if Safari detects that a website has been updated."
- Tom's Guide (Kaycee Hill, 2026-09-16) — "tap the three-lined menu icon, and select Notify Me" (matches Apple).
- iOSHacker 2026-09-17 https://ioshacker.com/how-to/monitor-web-pages-in-safari-with-notify-me-on-ios-27 — "Describe a change…" field; "Edit button next to Check Daily".
- iDownloadBlog 2026-07-20 (beta) https://www.idownloadblog.com/?p=1060067 — "Alert me when the item is back in stock."
- Managing: Settings > Apps > Safari > Notify Me (iDB, iOSHacker; no Apple page).

## Frequency
- Default daily: Apple Mac screenshot "Check daily at 10:00 AM  Edit"; Cult of Mac "By default, Safari will check the website daily".
- Options hourly/daily/weekly/monthly: Cult of Mac 2026-09-24 https://www.cultofmac.com/how-to/safari-notify-me-monitor-website-changes ; iDB. Apple only says "adjust how often".

## Requirements
- Apple Intelligence (User Guide): "With Apple Intelligence, Safari can let you know when a website updates..." Device: iPhone 15 Pro / 15 Pro Max / iPhone 16 or later. "not available in all languages or regions".
- Languages (Feature Availability "Notify me"): English (AU, CA, IN, IE, NZ, SG, ZA, UK, US) + many others; NO Hindi; not China mainland.
- Also iPad and Mac.

## Limitations
- iDB: "doesn't work on all websites"; "If Safari can't do what you typed, it will throw an error"; scheduled, not real time; sites' own alerts "more reliable".
- Cult of Mac hourly check on Apple release notes page → got the notification.
- MacRumors commenters skeptical (audience language only).

## Official stills (_sources/ios27-safari-settings/)
1. apple_ios27_notifyme_lockscreen_260914.jpg — iPhone 18 Pro Lock Screen, "Notify Me / The Brian Tran Band Tour / An update was detected on this page." Landscape.
2. apple_notifyme_setup_mac_260608.jpg — Mac setup dialog, "What should Safari look for?" "When registration opens", "Check daily at 10:00 AM".
3. apple_notifyme_notification_mac_260608.jpg — Mac notification "Update found for: "When registration opens"".

## Not found
- Apple video; Apple image of iPhone setup sheet; Apple frequency list; on-device vs cloud; 9to5Mac/Verge/iGB hands-on (budget).
