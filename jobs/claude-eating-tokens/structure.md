# Structure — claude-eating-tokens

## SHAPE (S17)

**Myth-busting, in service of a tutorial.** The viewer arrives believing the
fix for a big Claude bill is a terse-output skill, because that is what the
popular decks sell. The correction is mechanical and checkable: the model is
stateless, so every turn re-sends the whole conversation, which makes INPUT the
dominant cost — and terse-output skills cut OUTPUT. The reel overturns that,
then spends its second half handing over four things the viewer can do tonight.

Straight Tutorial was the alternative and was rejected: a bare list of four
tools is what both references already are, and it gives the viewer no way to
judge which one matters. The myth is what makes the list ordered.

## PROMISE (S2)

You will leave knowing which half of your token bill you are actually paying
for, and the three moves that touch it.

## OPEN LOOP (S10)

Planted: sentence 2 — "almost every token-saving skill you've seen cuts your
cheapest tokens." Distinctive word held back: *cheapest*.

Paid off: at "It is cutting the cheapest half", and returned to per S18 in the
final line — "And start with the expensive half, not the cheapest."

## WHAT -> WHY -> SO WHAT (S7)

WHAT: caveman claims 65% fewer output tokens and has ~100k stars.
WHY: output is not where a long session's money goes. Anthropic's docs say the
model remembers nothing between messages, so the entire conversation is re-sent
every turn — and caveman's own README concedes the skill only shrinks output,
that whole-session savings run smaller, and that it can go net negative.
SO WHAT: the honest ordering is see it (ccusage / claude-hud), stop generating
work you don't need (ponytail), and stop carrying history you don't need
(/clear, which costs nothing, over /compact, which re-reads to summarise).

## WHY THIS DRAFT EXISTS

The previous draft was a well-sourced news story about Uber's AI budget with no
takeaway for a viewer, and it reached that state because the reference posts
were dismissed on a misreading. Both were read in full before this draft; see
research.md -> CORRECTION TO THE RECORD.

## WHAT WAS CUT (S11, S21)

- Every mock number from the reference graphics (88,100 tokens, 87% fewer,
  "up to 85%") — promotional illustrations with no methodology.
- OmniRoute and claude-mem — real, but not verified in this pass, so not
  recommended on air.
- The whole Uber story — no viewer takeaway. Its own reel.
- /pin, /rewind, /handoff and /doctor — good levers, cut purely for runtime.
  /rewind is the strongest of the four and the first thing to add if this runs
  long enough for a fourth item.

## THE SAFETY LINE IS NOT OPTIONAL

The reel tells people to install three third-party things. Anthropic's plugin
docs are explicit that a plugin can ship hooks that execute commands, MCP
servers, and a bin/ directory on the Bash PATH. Recommending installs without
saying that would be careless, so the line stays even though it costs runtime.

## SOURCES

- https://code.claude.com/docs/en/prompt-caching
- https://code.claude.com/docs/en/costs
- https://code.claude.com/docs/en/plugins
- https://github.com/JuliusBrussee/caveman
- https://github.com/DietrichGebert/ponytail
- https://github.com/ccusage/ccusage
- https://github.com/jarrodwatts/claude-hud
