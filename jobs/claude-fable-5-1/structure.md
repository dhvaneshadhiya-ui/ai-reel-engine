# Structure — claude-fable-5-1

Written BEFORE the first sentence. Framework:
`styles/shortform-script-framework.md` (S17 shapes; S25 standard).

## STORY ENGINE (framework §4A)

A viewer who assumes a point-one model update is a rounding error discovers
that Fable 5.1 explained a crash a hedge fund had chased for five years — and
that the number Anthropic actually moved in this release is not on the
benchmark chart at all, it is the price of a cache read, because its smartest
model was the one almost nobody could afford to run.

## SHAPE (S17)

**News**, cold-opened as a Discovery. A straight product-announcement shape
would put the model name first and the price last, which is the order of the
press release, not the order of the story. The material has a genuine turn in
it — capability is the setup, price is the payoff — so the shape has to hold
one fact back. Discovery-into-news is the only shape that does.

## PROMISE (S2)

You will find out what actually changed in this release, and it is not the
thing the headline benchmarks are advertising.

## OPEN LOOP (S10)

Planted: "the number that changed this release isn't on any benchmark chart."
Paid off: the cache-read price — down 75% to $0.25 per million — with base
input/output pricing untouched. The ending returns to it (S18) by naming why
that matters: Fable 5's problem was never intelligence, it was the bill.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: Fable 5.1 and Mythos 5.1 shipped Sept 1; agentic-science benchmark more
than doubled (24.7% -> 52.6%).
WHY: those gains are useless if the model is too expensive to leave running,
and long agentic runs are dominated by cache reads.
SO WHAT: cutting cache reads 75% makes the same work 25-45% cheaper without
touching headline pricing — an admission about who was and wasn't using
Fable 5, and the reason you might now actually reach for it.

## WHAT WAS CUT (S11, S21)

- Every benchmark except Terminal-Bench-Science. Eight tables is density, not
  momentum; one doubled number carries the point and the rest are variations
  on it.
- Protein binder results (10x affinity, ~50% hit rate across 12 targets).
  Genuinely the most impressive item in the announcement, but it needs 15
  seconds of setup about what a binder is, and Venus does the same job with a
  picture that needs none.
- The 60% drop in cybersecurity false positives and the 85% drop on benign
  biology. Real, and interesting to a narrow audience; it is a third subject
  after capability and price, and the reel already has a twist to land.
- EU AI Act watermarking, EFS/zero-retention, the 1M context window, batch
  pricing, effort levels. Spec-sheet material with no story attached.
- The Mythos coding score (60.9% vs Fable 5.1's 55.8%). Interesting, but the
  Mythos beat is about ACCESS, and a second number there splits it.

## SOURCES

- Anthropic, "Introducing Claude Fable 5.1 and Claude Mythos 5.1" (primary,
  official) — benchmarks, pricing, Venus, Millennium testimonial, Mythos.
- VentureBeat, 1 Sept 2026 — independent write-up; cache read $1.00 -> $0.25;
  explicitly flags the figures as vendor-reported.
- Financial Times reporting on Ramp corporate-card data (via AI Weekly /
  aggregators) — Fable 5 at ~11% of Anthropic spend, overtaken by Opus 5.
  This is the only claim NOT from Anthropic, and it is the one the reel
  hedges by naming the outlet out loud.
