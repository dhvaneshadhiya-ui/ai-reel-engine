# Structure — claude-eating-tokens

Written BEFORE the first sentence. Framework:
`styles/shortform-script-framework.md` (S17 shapes; S25 standard).

## SHAPE (S17)

**Myth-busting**, not Explainer. The premise the audience already carries — the
one both reference posts sell — is "Claude is greedy, and the fix is a list of
commands." The material says something different and more useful: the cost is a
mechanism (a stateless model plus an exact-prefix cache), and the commonest
"optimization" habits are what trigger it. Myth-busting fits because there is a
specific wrong belief to overturn and a verifiable replacement for it.

Explainer was the obvious alternative and was rejected: an explainer would walk
the caching mechanism start to finish and land as a lecture. The reversal — the
thing you do to save tokens is the thing that costs you — is the story, and only
Myth-busting puts that reversal at the centre.

## PROMISE (S2)

By the end you will know the one mechanism that decides your token bill, and the
three ordinary habits that quietly break it — including the command most people
run specifically to save tokens.

## OPEN LOOP (S10)

Planted: sentence 5 — "Right up until you break it — and the habits people use
to save tokens are exactly what breaks it." The viewer now knows a named,
counter-intuitive reveal is coming and does not yet know which habit.

Paid off: the compact beat — "So does compact... that's the most expensive
compact you'll ever run" — then closed on its inverse, "Clear costs nothing."
Per S18 the ending returns to the loop's own terms: the final line is the
instruction the loop implied ("clear — don't compact").

## WHAT -> WHY -> SO WHAT (S7)

WHAT: cached input bills at roughly 10% of the normal input rate.
WHY: because the model is stateless, the entire conversation is re-sent every
turn — caching is the only thing standing between you and paying full price for
your whole history on every message.
SO WHAT: anything that changes the top of the request throws that discount away
for one full turn. That is why a mid-task model switch, an effort change, an MCP
toggle, or a cold /compact each cost far more than the action looks like it
should — and why /clear, which looks destructive, is the free one.

## WHAT WAS CUT (S11, S21)

- Agent teams at ~7x tokens — official, but a separate mechanism; it would open
  a second spine and the reel has one.
- Enterprise cost averages ($13/active day, $150-250/month) — official, but they
  are averages across enterprise deployments and read as a scare number when
  said to an individual developer.
- Cache TTL detail (one hour on a subscription, five minutes on usage credits or
  an API key) — true and interesting, but it needs a billing-model caveat to say
  honestly, and the caveat costs more runtime than the fact earns.
- CLAUDE.md-under-200-lines, hooks that pre-filter logs, subagent isolation —
  all real fixes, all cut. They are a list, and a list is what the reference
  posts already are. The reel keeps one mechanism and three symptoms.
- /rewind hitting an already-cached prefix — the single best cut line I dropped;
  it is a fourth fix and the ending was already full.

## SOURCES

Anthropic product documentation only — see `research.md` for the per-claim
ledger and the ONE-SOURCE-OK justification.

- https://code.claude.com/docs/en/prompt-caching
- https://code.claude.com/docs/en/costs
- https://code.claude.com/docs/en/commands

The two Instagram reference posts supplied by the user were read for FRAMING and
STRUCTURE only. Neither is used as a factual source; six of the slash commands
one of them lists do not exist. See `research.md` -> EXCLUDED.
