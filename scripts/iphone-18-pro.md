# iphone-18-pro — script + beat map (v2, iGeeksBlog narrative framework)

format: news · style: editorial · avatar: digital twin f55b0b7c (neutral) · 181 words
predicted 65.8s (2.75 wps) – 77.0s (2.35 wps) — inside the 60–80s news band at every measured pace

STRUCTURE: hook+context → promise (gap planted) → camera → display → silicon →
gap payoff (satellite) → THE TURN → conclusion carrying the design → CTA. One story, not six headlines.

RULE-3 CONSTRAINT FROM THE MANIFEST: the MacRumors mockup is a BACK view. It may
illustrate ONLY the colors and the unified rear panel. Never on screen under the
display, Dynamic Island, aperture or chip lines.

| # | narration | visual | note |
|---|---|---|---|
| 01 | "Apple's iPhone 18 Pro is expected on September 9." | `split` — top `hook-pair` (auto-zoom), bottom avatar. HeadlineBuild: label `EXPECTED SEPT 9` (15), headline `iPHONE 18 PRO` (13) | ≤2.0s. Product + timing legible on mute in frame 0. Context BEFORE any fact. |
| 02 | "And if the reports hold, it changes more than any Pro in years," | MG `categorygrid` — headline `WHAT'S REPORTEDLY CHANGING`, cards `CAMERA` · `DISPLAY` · `CHIP` · `SIGNAL` | the promise, made visible. The viewer sees the map of the next 60s. |
| 03 | "including one that only matters when you have no signal." | same grid, `selectIndex` 3 (`SIGNAL`) lighting up, then held | **curiosity gap planted on screen**, not just in the VO. Paid off at beat 10. |
| 04 | "Start with the camera:" | facecam pop | orientation beat, spoken to camera. |
| 05 | "a mechanical iris on the main lens that physically opens and closes." | **MG:aperture-iris.mp4** — an iris animating open→closed→open, generated as a scene asset (see BUILD NOTE) | rule 11: show the aperture actually moving. |
| 06 | "Wide open in the dark. Stopped down when you want everything sharp." | MG `categorygrid` — `WIDE OPEN`/low light · `STOPPED DOWN`/all sharp | consequence, not spec. No f-numbers — the range is contested (manifest ban). |
| 07 | "Analyst Ming-Chi Kuo says that lens alone costs about 50% more." | MG `statcard` — title `LENS UNIT COST`, rows iPhone 17 Pro/`100%`, iPhone 18 Pro/`150%`. footnote `Ming-Chi Kuo estimate` | number carries its baseline and its source (G15). |
| 08 | "But you'd notice this one more: the Dynamic Island could shrink about 35%," | **MG:island-shrink.mp4** — the pill animating 20.76mm → 13.49mm against a held frame | rule 11: show it shrinking. |
| 09 | "as Face ID's illuminator moves under the display." | MG `specsheet` — title `DYNAMIC ISLAND`, rows Now/`20.76mm`, Reported/`13.49mm` accent, Change/`−35%`. footnote `Leaker Ice Universe, Jan 2026` | the mechanism behind the shrink. |
| 10 | "Inside, the A20 Pro would be Apple's first 2nm chip: reportedly 15% faster, on 30% less power." | MG `statcard` — title `A20 PRO vs A19 PRO`, rows Speed/`+15%`, Power draw/`−30%`. footnote `Projection — analyst Jeff Pu` | footnote marks projection, not measurement. |
| 11 | "Pair that with a Pro Max battery about 10% bigger." | MG `statcard` — title `BATTERY`, row iPhone 18 Pro Max/`≈ +10%`. footnote `Pro Max only — the smaller Pro is reported near flat` | footnote mandatory: manifest bans implying it covers both models. |
| 12 | "Back to that signal." | facecam pop | the gap hinge — triggers "wait, what was that thing about no signal?" |
| 13 | "Apple's own C2 modem reportedly adds 5G over satellite. Coverage with no tower in sight." | MG `checklist` — headline `5G VIA SATELLITE`, items `Apple C2 modem` done, `No Wi-Fi` done, `No cell tower` done | **the payoff.** The promise from beat 03 is honoured. |
| 14 | "So this isn't just a camera upgrade." | facecam pop | **the turn.** The negation the whole reel has been building to — delivered to camera, nothing competing with it. |
| 15 | "The screen, the chip, the signal, even the frosted back it's wrapped in, reportedly in a new Dark Cherry." | `floatcard` src `hero-lineup`, aspect 1.778, credit `Mockup: MacRumors`, kinetic `MacRumors mockup` | **the hero image lands ON the conclusion** — it is the visual proof of "broader redesign", and the words are about the back and the colors, which is exactly what it shows. |
| 16 | "None of it is official until Apple says so." | facecam pop | rule 9 honesty beat. |
| 17 | "But which one would actually make you upgrade?" | `endquestion` src `crop-cherry`, question over two headline lines, payoff half accented | specific to the story, not generic. |

## BUILD NOTE — two motion assets this script now requires
Beats 05 and 08 promise motion the still mockup cannot show (rule 11). Neither
exists in the component library, and RULES §10 forbids extending the engine for one
reel. The sanctioned route is CLAUDE.md's HyperFrames-as-scene-source clause: render
each as a standalone MP4 into `public/assets/iphone-18-pro/`, then reference it from
the beat sheet like any other footage, so every gate still applies to the finished reel.
FALLBACK if that is declined: beat 05 becomes the `categorygrid` two-state card and
beat 08 folds into the `specsheet` — the script does not change, only the visuals weaken.

## Sound plan (roles, G28)
transition on 03→04 and 12→13 · popup as grid/specsheet rows land (02, 09) ·
suspense under 12 resolving on 13 (the gap payoff) · impact on 07 and 10 ·
reveal on the mockup card (14). 6–9 cues, vols 0.10–0.19.

## Treatments used (log to STYLE-RULES after delivery)
split hook on a STILL pair · categorygrid x2 (one with selectIndex as a gap device) ·
statcard x3 · specsheet · checklist · generated iris + island MG clips · floatcard at
true 16:9 · wordcascade conclusion · endquestion over a product still.
NOT repeated from airpods-camera: bgSrc darkened-plate bed, sourceread, 3-receipts-
from-one-page, timeline, cascade-with-facecam-bottom.
