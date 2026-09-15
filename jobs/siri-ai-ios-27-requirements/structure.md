# Structure — siri-ai-ios-27-requirements

Written BEFORE the first sentence. Framework:
`styles/shortform-script-framework.md` (S17 shapes; S25 standard).
`script_approval.py propose` refuses while placeholders remain.

## STORY ENGINE (framework §4A)

A viewer who just updated to iOS 27 and expects the new Siri opens it and
gets... the old Siri — which matters because eligibility here isn't one
line, it's four separate gates (phone model, region, language, age), and
Apple buried that behind one press release headline.

## SHAPE (S17)

**Explainer**, structured as an escalating checklist. The material is
inherently a gate-by-gate walkthrough — model tier, then the sharper
advanced-feature tier, then region, then language, then age — so the shape
that fits is "here's gate one... but wait, gate two..." rather than a flat
feature announcement. Each gate should knock out a chunk of the audience
that thought they qualified, which is the retention engine: the viewer
keeps checking themselves against the next rule.

## PROMISE (S2)

By the end you'll know exactly whether YOUR phone, region, language and
age get you the new Siri on day one — not just "does iOS 27 support my
phone" (almost everything does) but "does Siri AI."

## OPEN LOOP (S10)

Planted: the cold open draws the line viewers assume doesn't exist,
"Your iPhone will install iOS 27. That doesn't mean you get the new
Siri." This plants the gap between OS compatibility and feature
compatibility.
Paid off: the closing lines return to the same pair of ideas by name,
"installing iOS 27" versus "actually getting the new Siri", naming that
all four gates (phone, region, language, age) have to clear, so the
viewer now knows which one their own phone actually has.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: iPhone 15 Pro/16-and-up is the floor; iPhone 17 Pro/iPhone Air is the
ceiling for the most capable voice; EU, China, non-English, and under-13
are locked out entirely right now.
WHY: Apple split Siri AI's compute between a base on-device model (older
Neural Engines can run it) and a heavier one only two current phones can
run (Expressive Voices), while the region/language/age gates are policy,
not hardware — rollout sequencing and regulatory clearance, not a compute
limit.
SO WHAT: A viewer's actual answer to "do I have the new Siri" depends on
which of four unrelated gates they clear — phone, region, language, age —
and getting even one wrong (right phone, wrong region; right phone, but
under 13) means still not having it, no matter what the update screen
says.

## WHAT WAS CUT (S11, S21)

- The alleged 12GB RAM requirement for Expressive Voices/advanced
  dictation — a search-engine summary asserted this, but two full-article
  fetches that should have carried the figure did not contain it. Cannot
  independently confirm, so it is not spoken. See research.md §4.
- The full feature list of what Siri AI actually DOES (personal-context
  search, on-screen awareness, systemwide app actions) — that's a
  different, "what's new" story; this reel is scoped to eligibility, per
  the user's exact topic ("requirements to get Siri AI"), not capability.
  Naming it would dilute the checklist shape into two stories at once.
- The watch/iPad/Mac/Vision Pro compatibility matrix — true and sourced,
  but the topic as given is about getting Siri AI, and iPhone is where the
  overwhelming majority of the audience's stake is. One passing line
  acknowledges other devices exist without turning this into a full
  cross-device spec sheet.
- iOS 27.1's exact October 23 date for additional languages — that date
  appeared in only one outlet's phrasing ("expected... by October 23")
  versus Apple's own "next month," which is vaguer but is the tier this
  reel treats as authoritative. Spoken as "next month," not a specific
  date, to stay at the tier the strongest source actually supports.

## SOURCES

- https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/ (official)
- https://www.apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/ (official)
- https://9to5mac.com/2026/09/14/here-are-the-requirements-to-get-siri-ai-in-ios-27/ (independent, matches the user's own topic phrasing)
- https://www.macrumors.com/guide/ios-27-siri/ (independent)
- https://www.businesstoday.in/latest/trends/photo/apple-ios-27-release-date-supported-iphones-and-siri-ai-requirements-everything-officially-confirmed-so-far-554372-2026-09-09 (independent)
