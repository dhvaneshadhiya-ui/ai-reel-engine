# Research — claude-eating-tokens

Claims ledger + search log.

ONE-SOURCE-OK: every claim here is about how Anthropic's own product bills its
own requests. The vendor's product documentation IS the primary source for that
— there is no more-ultimate origin to trace back to, and no third party can
observe Claude Code's cache keys or TTL buckets from outside. Both domains used
(code.claude.com, platform.claude.com) are Anthropic, so they are recorded as
ONE origin rather than claimed as corroboration. Nothing in this script rests on
reporting, a leak, or an analyst estimate. The two Instagram reference posts
supplied by the user were NOT used as sources — see EXCLUDED below.

## CLAIMS

- CLAIM: The model is stateless between requests, so Claude Code re-sends the
  entire context — system prompt, project context, every prior message and tool
  result — on every single turn.
  TIER: official
  SPOKEN: "Claude remembers nothing between messages."
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: The full re-sent history is what a new turn carries; the new message is
  appended at the end.
  TIER: official
  SPOKEN: "Every turn, Claude Code re-sends all of it"
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: Cached input tokens are billed at roughly 10% of the standard input
  rate, which is what makes re-sending the whole history affordable.
  TIER: official
  SPOKEN: "roughly ten percent of the normal input rate"
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: Cache matching is an exact prefix match — a change anywhere in the
  prefix recomputes everything after it. There is no per-file or per-segment
  caching.
  TIER: official
  SPOKEN: "The match has to be exact."
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: Switching model with /model invalidates the cache — each model has its
  own cache, so the next request reads the whole history with no cache hits.
  TIER: official
  SPOKEN: "Switching models mid-task does it."
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: Changing effort level with /effort invalidates the cache — the cache is
  keyed by effort as well as model.
  TIER: official
  SPOKEN: "Changing effort does it."
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: Connecting or disconnecting an MCP server invalidates the cache when
  its tool definitions are loaded into the prefix rather than deferred.
  TIER: official
  SPOKEN: "Toggling an MCP server does it."
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: /compact itself sends a request carrying the same history it is
  summarizing; after a break longer than the cache lifetime there is no cache
  left to read, so it reprocesses the full history as uncached input — which is
  why /compact costs the most when you resume an old session.
  TIER: official
  SPOKEN: "the most expensive compact you'll run"
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: /clear costs nothing, in contrast to /compact, which reads the
  conversation it summarizes.
  TIER: official
  SPOKEN: "Clear costs nothing."
  SRC: https://code.claude.com/docs/en/costs
  VIA: Anthropic product documentation

- CLAIM: /context visualizes current context usage, and is the documented way to
  see what is consuming space before trying to reduce it.
  TIER: official
  SPOKEN: "So check context before you optimize."
  SRC: https://code.claude.com/docs/en/commands
  VIA: Anthropic product documentation

- CLAIM: Anthropic's own guidance is to pick model and effort at the top of a
  session and save /compact for natural breaks between tasks.
  TIER: official
  SPOKEN: "Pick your model at the start."
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: Clearing between unrelated tasks is the documented habit, because stale
  context is re-sent on every subsequent message.
  TIER: official
  SPOKEN: "And between two unrelated tasks, clear — don't compact."
  SRC: https://code.claude.com/docs/en/costs
  VIA: Anthropic product documentation

## EXCLUDED — checked and deliberately NOT claimed

- The user's reference post (@zero.canon_ / @piyush.glitch) lists a "15-skill
  Claude field pack" of slash commands. SIX of them are not documented anywhere
  in Anthropic's command reference: /pin, /ponytail, /handoff, /scope, /trace,
  /think. Verified 2026-08-25 against
  https://code.claude.com/docs/en/commands. NOT spoken, NOT shown on screen.
- That post's numeric claims ("85% smaller history", "ship 3x faster on half the
  spend") have no source. NOT spoken.
- The second reference post (@charliehills) names five third-party GitHub repos
  as the fix. Third-party tooling is not verifiable as a token-saving claim from
  the vendor docs, and the reel does not need it. NOT spoken, NOT shown.
- "Agent teams use approximately 7x more tokens" IS official
  (https://code.claude.com/docs/en/costs) but is cut for runtime — the reel's
  spine is the cache, and agent teams are a separate mechanism.
- Cost figures (~$13/developer/active day, $150-250/month) are official but cut:
  they are enterprise averages and would read as a scare number out of context.

## SEARCHED

- 2026-08-25  fetched https://code.claude.com/docs/en/costs  (settled: what
  drives token cost, /clear costs nothing, why usage climbs in a long session,
  CLAUDE.md loaded at session start, agent-team 7x, enterprise cost averages)
- 2026-08-25  fetched https://code.claude.com/docs/en/prompt-caching  (settled:
  statelessness, full re-send each turn, exact prefix match, ~10% cached read
  rate, the full list of cache-invalidating actions, cache TTL one hour on
  subscription vs five minutes on credits/API key, /compact cost mechanics,
  /rewind hits an already-cached prefix)
- 2026-08-25  fetched https://code.claude.com/docs/en/commands  (settled: which
  slash commands actually exist; confirmed /pin /ponytail /handoff /scope
  /trace /think are NOT documented, which is why the reference posts' command
  list is excluded above)
- 2026-08-25  read the two supplied Instagram reference posts in-browser
  (settled: their framing and structure; NOT used as factual sources)
