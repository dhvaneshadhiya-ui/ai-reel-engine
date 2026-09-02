# Structure — apple-trade-in-value-in

Written BEFORE the first sentence. Framework:
`styles/shortform-script-framework.md` (S17 shapes; S25 standard).

## STORY ENGINE (framework §4A)

A viewer who believes the Rs 57,000 on Apple India's Exchange Offer page is what their old
iPhone is worth discovers that every figure on that page is a ceiling — the
same headline says Rs 4,500 — which matters because they are about to trade a phone
in against the September 9 launch and will budget against a number Apple never
promised them.

## SHAPE (S17)

**Tutorial.** The material is a task — find what your iPhone is actually worth —
and the whole payoff is on screen and reproducible in four taps. It is not
Myth-busting: nothing here is a myth, the page is honest, and the ceiling is
printed in Apple's own words. Treating it as debunking would manufacture a
villain out of a disclaimer that is right there. The tutorial shape lets the
correction arrive as the step people skip rather than as an accusation.

Format `howto`, per the 2026-09-02 teardown: sequence not escalation, long
holds on the screen, presenter optional.

## PROMISE (S2)

By the end you know where Apple publishes real trade-in numbers, what your
model's ceiling is, and the one word that separates that ceiling from the offer
you will actually be made.

## OPEN LOOP (S10)

Planted: the hook states the Rs 57,000 and immediately says "read it again" —
the viewer is told the number is wrong before being told why.
Paid off: at the values table, when "Up to" is named, and closed completely at
"the table was the advert" — which returns to the hook's number and reclassifies
it rather than merely repeating it (S18).

## WHAT -> WHY -> SO WHAT (S7)

WHAT: Apple's page lists iPhone 16 Pro Max at up to Rs 57,000, and headlines the
range as Rs 4,500–Rs 57,000.
WHY: every row is a ceiling for a perfect example of that model; the real figure
comes from the condition questions behind "Find your trade-in value".
SO WHAT: budget against the quote, not the table — the gap between Rs 57,000 and Rs 4,500
is the whole difference between a discounted upgrade and a surprise.

## WHAT MAKES THIS A DIFFERENT REEL, NOT A TRANSLATION

India brands it "iPhone Exchange Offer", ties the credit to buying a new
iPhone in the headline itself, puts a "Shop iPhone" button where the US
card puts "Find your trade-in value", and prices iPhone 16 Plus and
iPhone 16 identically at Rs 36,000 where the US separates them. The
lesson is the same; almost none of the specifics are.

## WHAT WAS CUT (S11, S21)

- Apple Watch, iPad and Mac trade-in tables (5 tables on the page). One task,
  one device class — a second class is a second reel, per the howto playbook.
- Carrier and third-party trade-in comparisons. No sourcing was gathered and
  it would change the subject from "what does this page mean" to "who pays
  most".
- Any claim that values drop after the September 9 launch. Plausible and
  widely assumed; nothing published supports it, so it is out rather than
  hedged in.
- Apple Intelligence device requirements, researched for the abandoned iOS 27
  subject and irrelevant here.

## SOURCES

Apple, https://www.apple.com/in/shop/trade-in — read from the LIVE DOM on
2026-09-02 (values table, headline range, disclaimer, button label).

One source, and deliberately: every figure spoken is a fact about what Apple
publishes on its own page, so Apple is not merely the best source, it is the
only one that can be authoritative. A second outlet reporting the same table
would be quoting this page. ONE-SOURCE-OK: the claim is "Apple's page says X",
and the page is the primary record.

Note for anyone re-deriving this: the table is JavaScript-rendered. A static
fetch of the same URL returns no table — the payoff of this reel is invisible
to WebFetch and had to be read from the live page.
