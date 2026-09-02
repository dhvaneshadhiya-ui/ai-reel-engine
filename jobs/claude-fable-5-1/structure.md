# Structure — claude-fable-5-1

Written BEFORE the first sentence. Framework:
`styles/shortform-script-framework.md` (S17 shapes; S25 standard).

## STORY ENGINE (framework §4A)

A developer who is about to switch their default model to the new flagship
discovers that Anthropic's own documentation tells them not to, and that the
"25% cheaper" headline inverts to 20% MORE per task if they leave the effort
dial where Claude Code puts it — which matters because the fix is one setting,
not a different model.

## SHAPE (S17)

**News, told as Myth-busting.** The launch-day shape for this story is
"here is what shipped", and it is the wrong one: within a day of release the
material had already split into a marketing claim and a measured
contradiction, and the useful reel is the reconciliation, not the
announcement. Myth-busting is the only shape that can hold both numbers as
true at once, which they are.

Register is PRACTITIONER, not reporter. This is written for someone who runs
Claude Code every day and is deciding what to do on Tuesday morning, so every
beat answers "what do I change", and the reel ends on a rule rather than a
summary.

## PROMISE (S2)

The headline number everyone is repeating will cost you money if you act on
it, and by the end you will know the one setting that decides whether it is
true.

## OPEN LOOP (S10)

Planted: sentence 2, that Anthropic's own docs tell you not to default to it.
Paid off: the effort dial — Claude Code ships it on `high`, the migration
guide's step 3 says re-tune off that default, and at low/medium Anthropic
itself claims Fable 5 results or better for much less. The ending (S18)
returns to the "don't default" line by naming what you SHOULD spend max effort
on: the bug that has been open for years.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: Fable 5.1 tops every independent index (Artificial Analysis 66, Vals
#1) and Anthropic cut cache reads 75%.
WHY: it buys those scores with ~1.7x the output tokens — its own docs admit it
rewrites whole files instead of making targeted edits, and batches tool calls
less — so at max effort it costs $3.76/task against Fable 5's $3.14.
SO WHAT: it is not a default, it is a tool you reach for; the discount lives
at low/medium effort and evaporates at the top of the dial, and effort is now
changeable mid-conversation without invalidating the prompt cache.

## WHAT WAS CUT (S11, S21)

- Venus, the protein binders, Terminal-Bench-Science 52.6%. All real, all
  capability theatre for this angle: the reel's question is "what do I run on
  Tuesday", and no benchmark answers it. The Millennium crash survives ONLY
  because it defines the job worth paying max effort for.
- Mythos 5.1 entirely. It is Project Glasswing participants only, so for this
  audience it is an announcement about a door they cannot open.
- The three breaking API changes (forced tool use 400s, thinking-block
  binding, history edits). Genuinely important to anyone migrating, and a
  second reel — they do not fit under this promise.
- The 30-day data retention / no-ZDR restriction. Real objection, wrong reel;
  it is a procurement story, not a workflow one.
- Vals AI's numbers as a spoken claim. They corroborate, but their page
  discloses no relationship with Anthropic either way, and Artificial Analysis
  DOES disclose pre-release involvement — which makes AA the stronger witness
  precisely because it is the friendlier one.

## SOURCES

- Anthropic platform docs, "What's new in Claude Fable 5.1" (primary,
  official) — "For most workloads, start with Claude Opus 5"; "Re-tune effort
  from the default (high)"; whole-file rewrites; low-effort search behaviour;
  pricing table; per-message effort beta.
- Anthropic, "Introducing Claude Fable 5.1 and Claude Mythos 5.1" (primary,
  official) — the 25-45% cost claim, effort defaults per surface, the
  Millennium testimonial.
- Artificial Analysis, "Claude Fable 5.1 tops the Artificial Analysis
  Intelligence Index" — $3.76 vs $3.14 per task, ~1.7x output tokens, index 66,
  and their disclosure that they ran Anthropic's pre-release evaluation.
- Vals AI — corroboration only, not spoken.
