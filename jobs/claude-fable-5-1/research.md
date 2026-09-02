# Research — claude-fable-5-1

Claims ledger + search log. Tiers: official / multi / single / disputed.

## CLAIMS

- CLAIM: Claude Fable 5.1, Anthropic's most capable model, shipped 1 Sept 2026.
  TIER: multi
  SPOKEN: "Anthropic shipped its most capable model yesterday."
  SRC: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
  VIA: Anthropic platform docs (primary)
  SRC: https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads
  VIA: VentureBeat own reporting, 1 Sept 2026
  NOTE: "yesterday" is true on a 2 Sept publish. If this slips a day, the word
  changes to "this week" before the avatar is generated, not after — G27
  hashes the approved narration.

- CLAIM: Anthropic's own docs for Fable 5.1 tell developers to start with
  Opus 5 for most workloads, and reserve Fable 5.1 for demanding reasoning and
  long-horizon agentic work.
  TIER: official
  SPOKEN: "Its own documentation tells you not to make it your default."
  SPOKEN: "Those are their words, on the new model's page: for most workloads, start with Claude Opus 5."
  SPOKEN: "Because Fable 5.1 isn't an upgrade, it's a specialist."
  SRC: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
  VIA: Anthropic, verbatim: "For most workloads, start with Claude Opus 5...
       Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic
       work, or when your evals on Claude Opus 5 at higher effort still fall
       short." Captured to docs-start-with-opus-crop.png.

- CLAIM: Anthropic markets Fable 5.1 as ~25% cheaper on typical workloads
  (up to ~45% on highly agentic work) via a 75% cache-read cut.
  TIER: official
  SPOKEN: "Still, everyone's repeating twenty-five percent cheaper."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic, "Cost and availability", with a chart whose own footnote
       says the figures are measured AT DEFAULT EFFORT over four weeks of
       August 2026 usage. That scope is what makes the next claim compatible
       rather than contradictory, and the reel turns on exactly that.

- CLAIM: Artificial Analysis measured Fable 5.1 at max effort costing $3.76
  per Intelligence Index task against Fable 5's $3.14 — about 20% more —
  driven by roughly 1.7x the output tokens.
  TIER: single
  SPOKEN: "Artificial Analysis, which ran Anthropic's own pre-release evals, says it goes the other way: three dollars seventy-six a task, against three fourteen. Twenty percent more, on roughly one point seven times the output tokens."
  SRC: https://artificialanalysis.ai/articles/claude-fable-5-1
  VIA: Artificial Analysis' own measurement — ONE origin, so tiered single.
       It is hedged not by a weasel word but by naming the measurer out loud,
       which is the stronger form here: AA discloses "We supported Anthropic
       with pre-release evaluation of Claude Fable 5.1", so the number comes
       from a friendly witness, not a rival. The reel says so.
  NOTE: the preceding line "That discount is real. Verbosity just eats it."
       is an editorial bridge, deliberately NOT listed as a SPOKEN carrier:
       it names no figure, and the sentence that follows it attributes every
       number to Artificial Analysis by name.
  NOTE: this does NOT contradict the claim above. Anthropic measured default
  effort on real workloads; AA measured max effort on its index. Both are
  true, and the gap between them IS the reel. Nothing in the script asserts
  Anthropic is wrong.

- CLAIM: Fable 5.1 rewrites whole files instead of making targeted edits, at a
  cost in output tokens and time.
  TIER: official
  SPOKEN: "And Anthropic's docs say why. Editing a file, it rewrites the whole thing instead of the lines that moved."
  SRC: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
  VIA: Anthropic, verbatim: "When editing text files, the model is more likely
       to rewrite the entire file than make a targeted edit. The result is
       usually the same, but the rewrite costs more output tokens and time."
       Captured to docs-whole-file-rewrites.png.

- CLAIM: Claude Code defaults Fable 5.1 to high effort, and Anthropic's
  migration guide tells you to re-tune off that default.
  TIER: official
  SPOKEN: "Now, here's the setting that decides it."
  SPOKEN: "Claude Code runs it on high by default. Step three of the migration guide: re-tune effort from that default."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic, verbatim: "Fable 5.1 defaults to High effort in Claude Code,
       and to Medium in Claude Cowork and on Claude.ai."
  SRC: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
  VIA: Anthropic migration step 3, verbatim: "Re-tune effort from the default
       (`high`), and consider changing it mid-conversation instead of holding
       one level for the whole session." Captured to docs-retune-effort.png.

- CLAIM: At low or medium effort Anthropic claims results similar to or better
  than Fable 5 at much lower cost.
  TIER: official
  SPOKEN: "Go lower still, and Anthropic reckons you match Fable 5 for much less."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic, verbatim: "when set to Low or Medium effort, Fable 5.1
       achieves results similar to or better than Fable 5's at a much lower
       cost." Spoken as Anthropic's CLAIM, attributed in the sentence, because
       no independent test of the low/medium settings exists yet.

- CLAIM: At xhigh effort (one level below max) Fable 5.1 scores 65 on the
  Artificial Analysis Intelligence Index at $2.72 per task, against 66 at
  $3.76 at max — $1.04 less per task for one index point.
  TIER: single
  SPOKEN: "So drop it: Artificial Analysis says one notch down scores sixty-five instead of sixty-six, at a dollar four less a task."
  SRC: https://artificialanalysis.ai/articles/claude-fable-5-1
  VIA: Artificial Analysis' own measurement, verbatim: "At xhigh effort Fable
       5.1 scores 65 at $2.72 per task, $1.04 less than max, but still above
       Claude Opus 5 (max, 63) at $2.34." One origin, so tiered single and
       spoken with them named in the sentence. Captured to aa-cost-per-task.png,
       which carries this line and the $3.76 figure in one frame.

- CLAIM: At low effort Fable 5.1 calls search or retrieval tools less often and
  answers from memory more.
  TIER: official
  SPOKEN: "But the trade: at low effort it searches less, answering from memory more."
  SRC: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
  VIA: Anthropic, verbatim: "Answers from memory more often at `low` effort.
       At the lowest effort level the model calls a search or retrieval tool
       less often." Captured to docs-low-effort-memory.png. This is the
       counterweight to the advice above and is in the reel for that reason.

- CLAIM: A Millennium portfolio manager reports a one-in-a-million-runs crash
  that went four to five years unexplained; every model tried missed it
  including Fable 5, and Fable 5.1 traced it by disassembling a vendor library.
  TIER: official
  SPOKEN: "Then Millennium. A crash in one run per million, five years unexplained, and every model missed it, including Fable 5."
  SPOKEN: "This one took apart a vendor library and found it."
  SPOKEN: "That's what you buy max effort for."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic's launch page, attributed testimonial (Damien, Senior
       Portfolio Manager, Millennium). VENDOR-PUBLISHED customer testimony.
       It is in the reel as an ILLUSTRATION of the job worth paying max effort
       for, never as evidence of a benchmark, and the on-screen card shows it
       sitting on Anthropic's page so the viewer sees whose claim it is.

## SEARCHED

- 2026-09-02  fetched https://www.anthropic.com/claude-fable-and-mythos-5-1
  (four passes) — benchmarks, pricing, effort defaults per surface, the
  low/medium claim, Venus, the Millennium testimonial verbatim.
- 2026-09-02  "Claude Fable 5.1 independent benchmark testing results
  developers" — THE turning point. Surfaced Artificial Analysis and Vals, and
  showed that the first draft's closing line ("nobody outside has checked one
  yet") was false: independent measurement was published the same day. That
  line was written from assumption, not evidence, and the user caught it.
- 2026-09-02  fetched https://artificialanalysis.ai/articles/claude-fable-5-1
  — $3.76 vs $3.14 per task, ~1.7x output tokens, index 66, 11x token span
  across the five effort levels, and their pre-release disclosure.
- 2026-09-02  fetched https://www.vals.ai/models/anthropic_claude-fable-5-1 —
  #1 at 67.87%, LiveCodeBench 90.52%, Harvey legal agent 6.67% (18th of 55).
  Corroborates but is NOT spoken: the page discloses no relationship with
  Anthropic in either direction, so it cannot be presented as independent with
  the same confidence as AA, which discloses.
- 2026-09-02  "Anthropic Fable 5.1 effort parameter mid-conversation" then
  fetched the platform docs — settled that per-message effort is real (beta
  header `mid-conversation-output-config-2026-07-01`, does not invalidate the
  prompt cache), and produced the two strongest receipts in the reel: "For
  most workloads, start with Claude Opus 5" and migration step 3.
- 2026-09-02  fetched https://news.ycombinator.com/item?id=49525378 — day-one
  developer sentiment. NOT used: the thread is mostly about Opus 5's prose
  being unreadable, and Anthropic's own docs say Fable 5.1's prose is DENSER
  in places, so the "it writes better now" read would have been a claim built
  on a forum impression against a primary source that says the opposite.
- 2026-09-02  "Claude Fable 5 enterprise spending 11%" — FT/Ramp adoption
  figure. Researched and dropped with the previous angle; not in this script.
- 2026-09-02  the five x.com/claudeai posts in the brief: WebFetch returns HTTP
  402, and the in-app browser hits X's error wall. Could not be read. Nothing
  in the reel rests on them; the platform docs and the launch page carry the
  same content and are stronger sources.
