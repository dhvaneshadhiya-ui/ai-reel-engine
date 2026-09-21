# Structure — iphone-18-battery-prepare-to-ship

Written BEFORE the first sentence. Framework:
`frameworks/shortform-script-framework.md` (S17 shapes; S25 standard).

## STORY ENGINE (framework §4A)

A viewer who assumes "bigger battery" is a pure, free upgrade discovers that
the iPhone 18 Pro Max's battery got so big it broke a real, global shipping
rule — and Apple had to write a software feature just to make the phone legal
to put in a box. Matters because it shows there is a hard ceiling on phone
batteries that has nothing to do with engineering skill, and it changes what
happens the day you trade this phone in, sell it, gift it, or send it for
repair.

## SHAPE (S17)

**Explainer.** Nothing "happened" in the news sense — Apple published a
support page, quietly, alongside a phone that already launched. The engine
here is a question (why does ONE iPhone need a step no other iPhone has ever
needed?) answered in order: the rule -> how Apple solves it -> what it means
for you the one time it matters. News shape (event -> reaction -> what's
next) has no event to hang on; Explainer's context -> mechanism -> implication
sequence is what this material actually is.

## PROMISE (S2)

By the end, the viewer knows the actual number that trips this rule, why the
16-inch MacBook Pro's even bigger battery never has to do this, and the exact
moment THEY would ever see this screen.

## OPEN LOOP (S10)

Planted: the hook withholds WHY the biggest iPhone battery ever needs to go on
a diet before it's allowed to leave a warehouse.
Paid off: the MacBook Pro contrast (~1/3 in) answers "why this phone and not
Apple's own bigger battery," and the close returns to the viewer's own
first-hand case (repair/trade-in/resale/gift) — the actual moment this stops
being trivia and starts being a real extra step for them.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: iPhone 18 Pro Max has a new Settings toggle, "Prepare to Ship," that
discharges and caps the battery before the phone can be shipped.
WHY: its single battery cell is over 20 watt-hours — Apple's own stated
threshold — and a lithium-ion cell over that line needs extra handling to fly,
almost everywhere. No other iPhone has ever crossed it.
SO WHAT: normal use and travel are untouched. But send this phone for repair,
trade-in, resale, or as a gift, and you run this step first — sometimes with
your charge capped at 80% for two weeks after.

## CONFIRMATION BEAT (2-5s)

Right after the hook: Apple's own "Prepare to Ship" screen from
support.apple.com/en-us/127848 — the real Settings > General > Transfer or
Reset iPhone > Prepare to Ship screenshot, reframed into a phone mockup. Proves
in one look this is Apple's own documented feature, not a rumor or a leak,
before a single number is spoken.

## VIEWER QUESTIONS

- Q: What actually is "Prepare to Ship"? A: "That's Prepare to Ship: a setting that exists on no other iPhone."
- Q: Does this only matter if I ship my phone back someday? A: "Your brand-new iPhone 18 Pro Max already had its battery drained once, before you ever touched it."
- Q: Why does only the Pro Max need this? A: "Here's why: this phone's battery crossed a number no iPhone has ever crossed before, twenty watt-hours, all in one cell."
- Q: Doesn't Apple's own 16-inch MacBook Pro have an even bigger battery? A: "Compare that to Apple's own 16-inch MacBook Pro, which holds even more power and never needs this."
- Q: Does this affect me if I just charge and use the phone normally? A: NOT ANSWERED — carried by omission (the script never implies a use-time restriction); Apple's own page states it directly ("isn't required while traveling"), logged in research.md NOT CLAIMED, cut from narration for pacing inside a 70s runtime.
- Q: What actually happens, and what's the catch if I ever do ship it? A: "Ship this phone again, for repair, trade-in, resale, or as a gift, and it happens all over."

## WHAT WAS CUT (S11, S21)

- Exact Wh figure (21.75Wh / 21.06Wh). Apple's own page never states an exact
  number, only "over 20 Wh" — the precise figures in circulation are press
  math on an EU-mandated energy-label mAh disclosure, not an Apple-published
  Wh spec. Naming a false-precise number Apple never said would overclaim a
  TIER; the script uses Apple's own "over 20 watt-hours" language only.
- The US-vs-international regulatory approval gap (PHMSA cleared the firmware
  method in June 2025; IATA/ICAO/ADR reportedly hadn't formally signed off as
  of this reporting window). Single-sourced (GSMArena only) and a genuine
  aside, not core to what a viewer needs — cut for pacing, not because it's
  wrong.
- Ground-vs-air shipping nuance (a >20Wh cell can still move by US ground
  transport under a separate, higher DOT threshold). True and interesting,
  but it complicates the "why this exists" beat inside a 70s runtime without
  changing what the viewer actually experiences (Apple's own flow doesn't
  distinguish ground from air for the end user) — cut.
- MacRumors Forums reaction (the "what if my screen is broken" thread, the
  fire-risk sub-thread). Real and well-sourced, but this is an explainer
  about the mechanism, not a reaction piece — no room in 70s without cutting
  a load-bearing beat.
- Whether the iPhone 18 Pro Max is the first PHONE ever (any brand) to cross
  20Wh in one cell, vs. the first iPhone. Sourcing only supports "first
  iPhone" with confidence; "first phone ever" is an inference from an absence
  of counter-examples, not a positive claim any source makes. The script says
  "no iPhone" — never "no phone" — to stay inside what's actually sourced.
- Precise discharge/repair-window mechanics beyond the two numbers that
  matter (below 20Wh to ship; 80% cap for 14 days on repair/trade-in/return).
  The "Ready to Ship" red badge and the manual undo path are real but are
  UI trivia next to the two numbers a viewer would actually retain.

## SOURCES

- https://support.apple.com/en-us/127848 — Apple's own support article
  (official, primary; publish date 2026-09-18)
- https://www.macrumors.com/2026/09/18/iphone-18-pro-max-shipping-restriction/
  (independent confirmation + MacBook Pro cell-count explanation)
- https://9to5mac.com/2026/09/19/iphone-18-pro-maxs-battery-is-so-big-apple-had-to-add-this-new-feature-to-ios-27/
  (independent confirmation)
- https://www.gsmarena.com/heres_apples_clever_way_of_circumventing_20wh_battery_shipping_restrictions-news-74689.php
  (regulatory framing, iFixit-sourced capacity figures, "first iPhone" framing)
- https://www.ifixit.com/News/119329/inside-the-tiny-unfixable-eye-iphone-18-pro-and-pro-max-teardown
  (battery capacity teardown, independent of GSMArena)
- https://www.androidauthority.com/phone-battery-transportation-rules-3574123/
  (UN Special Provision 188 / 20Wh-per-cell regulation explainer)
- https://www.fedex.com/content/dam/fedex/us-united-states/services/Shipping-Lithium-Batteries-via-FedEx-Ground.pdf
  (independent corroboration of the 20Wh/100Wh regulatory split, citing 49 CFR 173.185)

Two independent non-Apple domains (MacRumors, 9to5Mac) confirm the feature
itself, neither citing the other — INDEPENDENT-CHECK: pass. The regulatory
threshold is corroborated across GSMArena, Android Authority and FedEx's own
compliance guide, none citing a shared upstream leaker (this is public
regulation, not a leak).
