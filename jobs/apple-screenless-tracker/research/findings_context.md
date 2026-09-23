# Research: CONTEXT subtopic
## Apple screenless fitness tracker (Bloomberg, Sept 22 2026)
"How does this differ from what Apple already ships, and what do Whoop/Oura actually do?"

---

## 1. Apple Watch's current heart-rate limitation, and the Aug 30 2026 leak

- Current behavior: Apple Watch "records heart rate 'only during workouts and at random'" outside of exercise -- i.e. periodic/intermittent sampling, not continuous.
  SRC: https://9to5mac.com/2026/08/30/apple-watch-series-12-last-minute-leaks-new-fitness-app-heart-rate/ (VIA Bloomberg's Mark Gurman)

- The fix being tested: Apple is "testing the ability for the heart-rate sensor to record all day, rather than only during workouts and at random." Framed as making Apple Watch "a more data-rich experience" for Series 12 and Ultra 4.
  SRC: https://9to5mac.com/2026/08/30/apple-watch-series-12-last-minute-leaks-new-fitness-app-heart-rate/ (VIA Bloomberg's Mark Gurman)

- MacRumors' Aug 30 2026 version, same leak: "One new feature in testing allows the heart-rate sensor on the Apple Watch to continuously collect data throughout the day" -- contrasted against the status quo where "the sensor works continuously during workouts, while readings outside exercise are taken periodically."
  SRC: https://www.macrumors.com/2026/08/30/apple-watch-series-12-ultra-4-features/ (VIA Bloomberg's Mark Gurman) -- note: at the time it was unclear whether Apple would ship the change.

- FOLLOW-UP (found while searching; not one of the 4 assigned facts but directly relevant to "what Apple already ships"): at Apple's official Sept 9, 2026 announcement, the always-on heart sensor was confirmed and branded the "Health Sensing System" -- "a redesigned optical heart sensor that provides continuous heart rate monitoring for the first time ever," now measuring "every five seconds, a 60x frequency increase over previous models," which Apple calls "the most accurate heart rate sensor in a wearable."
  SRC: https://www.macrumors.com/2026/09/09/apple-watch-series-12-announced-all-day-hr-sensor/ and https://9to5mac.com/2026/09/09/apple-watch-series-12-and-ultra-4-unveiled-with-upgraded-health-tracking-system/
  STORY-LOGIC NOTE: Apple Watch had already closed the "only samples every few minutes" sensor gap by the time the Sept 22 screenless-tracker report landed -- so the screenless tracker isn't about matching Whoop/Oura's sensor frequency, it's about the SCREEN-FREE, notification-free, single-purpose interface, which even a continuously-sensing Apple Watch still doesn't offer.

---

## 2. What Whoop actually is

- No screen, worn 24/7: "WHOOP features a screen-free design with no pings, distractions, or unnecessary bells & whistles. The device is engineered to capture continuous, uncompromised biometric data 24/7."
  SRC: https://www.whoop.com/us/en/ (direct fetch blocked, HTTP 403; quote pulled via WebSearch snippet of whoop.com/us/en/ and whoop.com/us/en/one/ -- treat as close paraphrase of Whoop's own site copy, not a verified verbatim scrape)

- Three core metrics: "distill it into three fundamental physiological pillars: Strain (cardiovascular and muscular load), Recovery (autonomic readiness), and Sleep (circadian and sleep debt coaching)."
  SRC: https://www.whoop.com/us/en/ (same caveat -- WebSearch snippet, not a direct fetch)

- Subscription model, device bundled with membership, no separate hardware purchase: "All plans include the Whoop 5.0 device at no extra cost... You don't own the tracker; you rent access to it as part of your membership plan." Current (2026) tiered pricing: WHOOP One $199/yr, Peak $239/yr, Life $359/yr (medical-grade ECG/blood-pressure insights); monthly billing also available (~$25-$40/mo depending on tier).
  SRC: https://support.whoop.com/s/article/Membership-Pricing?language=en_US ; corroborated by https://trackervs.com/pricing/whoop-pricing/ (secondary, for the $199-$359/yr tier breakdown -- whoop.com itself was blocked, pricing pulled via WebSearch aggregation of these pages)

---

## 3. What Oura Ring is, and its IPO numbers

- Form factor / no screen: "a small and lightweight wearable device designed to fit snugly around your index or middle finger," available in titanium or ceramic -- no display; all data lives in the companion app.
  SRC: https://www.sleepfoundation.org/best-sleep-trackers/oura-ring-review (via WebSearch aggregation)

- Sleep Score: "reflects the quality and quantity of your sleep by analyzing key factors like sleep stages, restfulness, and timing," derived from resting heart rate, body temperature, movement, and sleep-stage data.
  SRC: https://ouraring.com/blog/readiness-score/ and https://support.ouraring.com/hc/en-us/articles/360025445574-Sleep-Score

- Readiness Score: "predicts how prepared your body is for the day ahead," built from sleep quality, activity levels, resting heart rate, HRV, and body temperature; scored 0-100, "85 or higher considered optimal."
  SRC: https://ouraring.com/blog/readiness-score/

- Subscription: first month of membership included with ring purchase; without an active membership only the three daily scores are visible -- deeper insights sit behind Oura Membership.
  SRC: https://support.ouraring.com/hc/en-us/articles/4409086524819-Oura-Membership

- IPO / unit numbers -- VERIFIED against the IPO filing as reported:
  - "The health-tech company sold 3.6 million Oura Rings in the 12 months ended June 30" -- matches the number in the task brief exactly.
    SRC: https://www.theglobeandmail.com/investing/article-smart-ring-maker-oura-targets-1562-billion-valuation-in-us-ipo/ (reporting on Oura's IPO filing)
  - IPO targeting "a fully-diluted valuation of US$15.62-billion" (up to $2.2B raise; Nasdaq ticker "OURA"; expected to price Sept 29, 2026).
    SRC: https://www.theglobeandmail.com/investing/article-smart-ring-maker-oura-targets-1562-billion-valuation-in-us-ipo/ ; corroborated https://www.techrepublic.com/article/news-oura-ipo-15-6-billion-valuation/ (via WebSearch snippet -- direct fetch of techrepublic blocked, HTTP 403)
  - Revenue: "revenue for the nine months ended June 30 surged roughly 74 per cent year-over-year to US$1.21-billion."
    SRC: https://www.theglobeandmail.com/investing/article-smart-ring-maker-oura-targets-1562-billion-valuation-in-us-ipo/
  - Paid members: "expects to end fiscal 2026 with roughly 5.7 million paid members, representing 96-per-cent growth over the prior year."
    SRC: https://www.theglobeandmail.com/investing/article-smart-ring-maker-oura-targets-1562-billion-valuation-in-us-ipo/

---

## 4. Why now / internal Apple context: Eddy Cue and the health team handoff

- Eddy Cue took over Apple's health/fitness teams in October 2025, timed to Jeff Williams' retirement: "Services chief Eddy Cue will reportedly gain oversight of Apple's health and fitness teams," with "the groups being consolidated under health lead Sumbul Desai" and "Fitness+ head Jay Blahnik" reporting to Desai; "longtime chief operating officer Jeff Williams prepares to depart at the end of this year" (Williams had announced retirement in July 2025).
  SRC: https://www.macrumors.com/2025/10/10/apple-health-fitness-teams-eddy-cue-reshuffle/
  Corroborating VIA: Bloomberg's original report -- titles only, not separately fetched: https://www.bloomberg.com/news/articles/2025-10-10/apple-to-move-health-fitness-divisions-to-services-in-reorganization and https://9to5mac.com/2025/10/09/apple-folds-health-and-fitness-into-services-splits-apple-watch-oversight/ (the MacRumors fetch above is the verbatim source actually used).
  Strategic read from the same MacRumors piece: "placing health and fitness under his Services umbrella suggests Apple wants to transform its wellness initiatives into a more significant revenue stream" -- ties to the also-reported "Health+ subscription service" featuring "an AI assistant providing personalized recommendations on nutrition, exercise, and sleep."

- What Cue has pushed for since taking over -- the direct "why now" for the screenless tracker, drawn from the Sept 22 2026 Bloomberg-sourced coverage of the screenless-tracker report itself:
  - "Cue took charge of Apple's health team last October, following the departure of Jeff Williams... Cue has pushed Apple's health team to adopt features from the newer rivals, whose products offer simpler interfaces focused squarely on fitness and health tracking."
    SRC: https://9to5mac.com/2026/09/22/apple-working-on-whoop-style-screenless-fitness-tracker-per-report/ (VIA Bloomberg's Mark Gurman)
  - Eddy Cue "now leads Apple's health teams" and is "pushing for wearables with simpler interfaces, like the screen-free Whoop and Oura Ring." Also: "Apple chair Tim Cook and services chief Eddy Cue are interested in the product, notable because Cue now leads Apple's health teams."
    SRC: https://www.macrumors.com/2026/09/22/apple-screenless-fitness-band/ (VIA Bloomberg's Mark Gurman)
  - Product shape reported: "a fabric band attached to a computing module that rests on the wrist. Sensors track heart rate and other metrics, similar to the Apple Watch." Status: "technology investigation" phase, prototypes exist, no decision to ship; "likely would not launch until at least 2028."
    SRC: https://www.macrumors.com/2026/09/22/apple-screenless-fitness-band/ and https://9to5mac.com/2026/09/22/apple-working-on-whoop-style-screenless-fitness-tracker-per-report/

---

## What I looked for and did NOT find

- A direct, individually-sourced statement that "Eddy Cue personally wears both Oura and Whoop." One aggregated WebSearch summary produced the line "Notably, Eddy Cue wears both Oura and Whoop, demonstrating that the Health app hasn't caught up to the devices Apple's own leadership prefers" -- but direct fetches of the two lead articles carrying this story (9to5mac and MacRumors, both Sept 22 2026) explicitly do NOT contain that claim ("the article contains no information about Eddy Cue wearing Oura or Whoop devices" / "the article does not contain specific information about Cue personally wearing Oura or Whoop devices, only that he advocates for their interface design philosophy"). TREAT "CUE PERSONALLY WEARS BOTH" AS UNVERIFIED -- do not use it as a spoken claim without locating its original source (may trace to Bloomberg's Gurman "Power On" newsletter, which is paywalled and was not directly fetched here).
- Direct fetch of whoop.com -- blocked with HTTP 403 on every attempt (homepage and /one/ membership page). All Whoop facts above are corroborated via WebSearch snippets/secondary sites rather than a direct scrape of Whoop's own marketing copy -- flag if verbatim on-brand Whoop phrasing is required for the script.
- Direct fetch of techrepublic.com -- blocked with HTTP 403; used theglobeandmail.com (reporting the same IPO-filing figures) as the primary verbatim source, cross-checked against the techrepublic WebSearch snippet (same numbers, no contradiction).
- The original Bloomberg article breaking the Sept 22 2026 screenless-tracker story -- not fetched directly (paywalled); relied on 9to5mac's and MacRumors' same-day write-throughs, both of which explicitly attribute to "Bloomberg's Mark Gurman."
- No Apple-internal quote in Cue's own words (memo, interview, etc.) was found -- all "Cue has pushed for X" framing above is reported/paraphrased by Bloomberg/9to5mac/MacRumors, not a direct Cue quote.
