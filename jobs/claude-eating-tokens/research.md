# Research — claude-eating-tokens

Claims ledger. Two domains: code.claude.com (Anthropic product docs) and
github.com (each tool's own repository). Every tool claim is sourced to the
tool's OWN README, including the caveat that contradicts its headline number.

## CLAIMS

- CLAIM: The model is stateless between requests, so Claude Code re-sends the
  full context — system prompt, project context, every prior message and tool
  result — on every turn. That resent history is input, and input dominates a
  long session's cost.
  TIER: official
  SPOKEN: "remembers nothing between messages"
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: caveman is a real Claude Code skill at github.com/JuliusBrussee/caveman
  with ~100.8k stars, whose README claims 65% average output-token savings.
  TIER: official
  SPOKEN: "A hundred thousand stars, and it does cut output"
  SRC: https://github.com/JuliusBrussee/caveman
  VIA: the project's own README

- CLAIM: caveman's README carries a section headed "Important - Honest number
  warning" stating verbatim that the skill only shrinks OUTPUT tokens, that
  input and reasoning tokens are untouched, and that THE SKILL ITSELF ADDS
  ~1-1.5k INPUT TOKENS PER TURN; whole-session savings run smaller than the
  output number and can go net-negative on already-terse workloads.
  TIER: official
  SPOKEN: "input is untouched, and it adds over a thousand input tokens a turn"
  SRC: https://github.com/JuliusBrussee/caveman
  VIA: the project's own README

- CLAIM: ccusage reads local agent-CLI logs and reports token usage and cost;
  claude-hud is a Claude Code plugin that surfaces context usage and running
  tools in the status line.
  TIER: official
  SPOKEN: "ccusage charts each session's cost"
  SRC: https://github.com/ccusage/ccusage
  VIA: the project's own README
  SRC: https://github.com/jarrodwatts/claude-hud
  VIA: the project's own README

- CLAIM: ponytail (github.com/DietrichGebert/ponytail, ~110.1k stars) enforces a
  decision ladder before code generation — does it exist already, can the
  standard library do it — so less new code is written.
  TIER: official
  SPOKEN: "Ponytail stops Claude rebuilding code that already exists"
  SRC: https://github.com/DietrichGebert/ponytail
  VIA: the project's own README

- CLAIM: /compact sends a request carrying the history it summarises, so it
  costs; /clear costs nothing.
  TIER: official
  SPOKEN: "type slash-clear — free"
  SRC: https://code.claude.com/docs/en/costs
  VIA: Anthropic product documentation
  SRC: https://code.claude.com/docs/en/prompt-caching
  VIA: Anthropic product documentation

- CLAIM: Claude Code plugins can ship hooks that execute commands, MCP servers,
  and a bin/ directory added to the Bash tool's PATH, so installing one runs
  third-party code with the agent's permissions; Anthropic's docs direct users
  to trust considerations before installing.
  TIER: official
  SPOKEN: "They run with your agent's permissions"
  SRC: https://code.claude.com/docs/en/plugins
  VIA: Anthropic product documentation

## CORRECTION TO THE RECORD (2026-08-25)

An earlier draft of this job asserted that six slash commands in the user's
first reference post "do not exist", based on a single fetch of Anthropic's
built-in command reference. **That was wrong, and the error was mine.** The post
never claimed they were built-ins — its cover slide reads "STOP IT WITH 6
SKILLS", and in Claude Code a skill or plugin defines its own slash command. On
reading the actual slides:

- /ponytail is github.com/DietrichGebert/ponytail, ~110.1k stars, verified live.
- /caveman-equivalent terse-output skills are real and widely installed.
- /pin, /handoff, /doctor, /rewind, /compact are the pack's other five skills,
  presented as skills throughout.

The mistake was checking the built-in command list and never opening the
carousel. Both reference posts were read slide by slide before this draft.

## WHAT THE REFERENCES ACTUALLY SAID (read in full, 2026-08-25)

Ref 1 — @zero.canon_ / @piyush.glitch, 6 skills:
  01 /doctor   — estimate what your context costs before prompting; names the
                 biggest hogs (their mock: docs 42.3k, examples 28.6k, history
                 17.2k = 88,100 tokens, 72% of the window)
  02 /pin      — pin context that must survive; immune to compaction
  03 /ponytail — terse answers (their mock: 12,840 -> 1,340 tokens, 87% fewer)
  04 /rewind   — jump back before a wrong turn instead of correcting for ten messages
  05 /compact  — condense to a checkpoint, "up to 85%" smaller
  06 /handoff  — carry progress to a new session without the transcript

Ref 2 — @charliehills, 5 repos chained, each sealing the last one's gap:
  1-1 OmniRoute          — one endpoint over many providers (GIVES YOU ACCESS)
  1-2 claude-mem         — compress a session, inject into the next (GIVES IT MEMORY)
  1-3 claude-hud+ccusage — status line + cost report (SHOWS YOU THE BURN)
  1-4 caveman            — terse output (CUTS THE TALK)
  1-5 ponytail           — reuse/stdlib before writing (CUTS THE WORK)

Both decks independently land on the same levers: SEE the spend, CUT the talk,
CUT the work, CARRY state instead of history. That convergence is why those
levers are the spine of this script.

## EXCLUDED — deliberately NOT claimed

- The per-skill mock numbers in ref 1 (88,100 tokens / 87% fewer / "up to 85%")
  are illustrations inside a promotional graphic with no published methodology.
  NOT spoken, NOT shown. The one savings figure we do speak (65%) is spoken as
  the project's own CLAIM and is immediately followed by its own caveat.
- OmniRoute and claude-mem: real slides, but not verified repo-by-repo in this
  pass, so they are not recommended on air.
- Uber's 2026 AI-budget story (Forbes/Fortune/Moneywise) — fully researched and
  sourced in the previous draft, but it is a news story with no viewer takeaway,
  which is exactly the failure this draft exists to correct. Kept for a
  separate reel.

## SEARCHED

- 2026-08-25  read BOTH reference carousels slide by slide in-browser (ref 1:
  cover + 6 skill slides + CTA; ref 2: all 7 slides). This is the step the
  earlier draft skipped.
- 2026-08-25  fetched https://github.com/DietrichGebert/ponytail  (exists,
  110.1k stars, decision-ladder behaviour, install command)
- 2026-08-25  fetched https://github.com/JuliusBrussee/caveman  (exists, 100.8k
  stars, 65% output claim AND the net-negative caveat)
- 2026-08-25  fetched https://github.com/ccusage/ccusage  (exists, 18.2k stars,
  npx ccusage@latest)
- 2026-08-25  fetched https://github.com/jarrodwatts/claude-hud  (exists, 27.6k
  stars, statusline context usage)
- 2026-08-25  fetched https://code.claude.com/docs/en/prompt-caching  (stateless
  re-send, cached reads ~10%, /compact cost, /clear)
- 2026-08-25  fetched https://code.claude.com/docs/en/costs  ("/clear costs
  nothing", reduce-token-usage strategies)
- 2026-08-25  fetched https://code.claude.com/docs/en/plugins  (plugins ship
  hooks, MCP servers, bin/ on PATH; trust considerations)

## SCOUT NOTE (2026-08-25, re-capture)

The caveman README gained a "Caveman 2" hero ~11h before capture, claiming
"33.2% fewer provider-reported input tokens in a pinned benchmark". The
"Honest number warning" our beat quotes is STILL in the same README
(verified live, line 227, verbatim: output-only, ~1-1.5k input added per
turn, can go net-negative). The script quotes the admission, which remains
true as written; the hero's competing v2 claim is the repo arguing with
itself, not with us.
