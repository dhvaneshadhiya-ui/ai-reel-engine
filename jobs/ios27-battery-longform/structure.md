# Structure — ios27-battery-longform (longform PILOT)

## STORY ENGINE (framework §4A)

Someone a few days into iOS 27 watches the battery fall and has to decide between
two explanations: the update is still working, or the phone is failing. Apple
documents the first and refuses to time it; the internet fills the silence with
numbers nobody can trace. Which matters because the two things people do in
response — panic about battery health, and swipe away every app — are the two
things that cannot help.

## SHAPE (S17)

Myth-busting, in chapters. The reel version had 80 seconds and had to choose one
beat; the long version can do the thing the short one could not: show the phone
admitting it, in Apple's own interface, and then take the popular fix apart with
Apple's own software chief on the record.

## PROMISE (S2)

The one screen that separates "still working" from "something is wrong", what the
phone is doing meanwhile, and which popular fix is worthless.

## OPEN LOOP (S2, S10)

The cold open promises a specific screen and withholds it for two chapters
("I'll show you that screen"). It pays off at the top of chapter 3, and the close
returns to it as the thing to check again in three days.

## CONFIRMATION BEAT (4-20s)

Apple's support page, captured on mobile, decelerating onto "certain tasks related
to the update continue in the background and might affect battery life and thermal
performance" — the claim is Apple's, in Apple's words, before any of our graphics.

## CHAPTERS — titled as the viewer would search, not as parts

Segment boundaries decided here ARE the chapters (technical-video-script). Timecodes
fill in after the render; the titles do not change.

- 00:00  Why your battery drops after an iOS 27 update
- ~0:35  What the update is doing in the background
- ~1:15  The iOS 27 row that shows it is still working
- ~1:55  How long it lasts, and the numbers nobody can trace
- ~2:45  The Battery screen that tells you which it is
- ~3:15  Why closing your apps does not help
- ~3:50  Whether your battery health is affected

## OLD CHAPTER NOTES

1. **What's happening** (~0:12-1:05) — Apple's page, then the phone admitting it:
   the iOS 27 "Optimising Search and Siri" row, captured live from the simulator.
2. **How long** (~1:05-1:55) — Apple's missing number against the internet's very
   specific ones, then the three-Septembers pattern.
3. **What helps, what doesn't** (~1:55-2:55) — the Battery screen note, the
   force-quit myth with Federighi on the record, and the charge-cycle arithmetic.

## WHAT -> WHY -> SO WHAT

WHAT: the battery falls faster after the update.
WHY: documented background work — indexing, asset downloads, app updates — that
Apple will not put a clock on.
SO WHAT: check one screen, leave the app switcher alone, look again in three days,
and escalate only if the update note is gone and the drain is not.

## VIEWER QUESTIONS

- Q: Is my battery dying? A: "Maximum capacity is measured across hundreds of charge cycles."
- Q: What is the phone actually doing? A: "It's indexing your files for search, downloading new assets, and updating your apps."
- Q: How can I SEE that it's doing it? A: "Open Settings, and above General there's a row that isn't normally there at all: Optimising Search and Siri."
- Q: How long does this last? A: "Not four days, not seventy-two hours, no hour count anywhere on that page."
- Q: Should I close my apps? A: "His answer was, no and no."
- Q: When should I actually worry? A: "If the update note is gone and the battery is still draining, that's when something is genuinely wrong and worth taking further."

## WHAT WAS CUT (S11, S21)

- The reference article's Siri-AI-reindexing explanation: its own inference, no source.
- Every circulating duration, except as examples of numbers with no origin.
- The Settings > Battery screenshot: the simulator has no battery hardware, so that
  screen is described in Apple's words, never faked.
- Low Power Mode and Adaptive Power paths: they differ by model (the user's own iPhone
  has no Power Mode row), and this cut does not need them.

## THE CUT LIST, DECIDED BEFORE RECORDING

Three of twelve pages are marked cuttable in shot-plan.json, in this order if the
runtime overruns: the simulator aside (the row disappearing), the three-Septembers
context beat, and the battery-health reassurance. Cutting all three still delivers
the promise. Decided now so nobody has to decide it at edit time
(technical-video-script, criterion 6 — "the one people skip").

## THE PASSES THIS SCRIPT HAS BEEN THROUGH

- **Audio-only pass.** Read with the screen off: no sentence depends on the picture.
  Two soft deictics were rewritten ("that isn't a setting" -> "Optimising Search and
  Siri isn't a setting"; "I recorded that" -> "I recorded that row").
- **The 30-second window.** The promise lands at ~27s of an 80-word opening.
- **Register, measured.** 19.0 words/sentence, 24% over 25 words, "you" 4.4/100 —
  inside the band measured across five in-format references (16-18, 14-20%, 4-6).
- **Humanizer**, whole script, recorded.

## PILOT NOTE

Deliberately ~3 minutes against the format's measured 500-700s band, so G02 will
advise and should. The point is to measure render time per minute and hear the voice
at length before committing nine minutes of VO credits to it.

## SOURCES

Apple support 120745 / 125039 / 101575 / 149076 / 100100; Mac Observer 2026-09-11 and
09-12; Daring Fireball 2017-07-20 (Federighi) + CNBC; OS X Daily 2025-09-18; TechRadar
2024. Apple's own iOS 27.0 simulator runtime for the Settings row. Ledger: research.md.
