# Structure — claude-eating-tokens

Written BEFORE the first sentence. Framework:
`styles/shortform-script-framework.md` (S17 shapes; S25 standard).

## SHAPE (S17)

**Myth-busting.** The premise handed to us — "Claude is eating your tokens" — is
a real meme and it is wrong in its causation. The reporting says the tokens at
Uber were eaten by an incentive: teams were ranked on internal leaderboards by
how much AI they used. Myth-busting is the only shape that puts that inversion
at the centre, and it earns the ending, which reverses the title outright.

News was the obvious alternative and was rejected. Told as News, this is "big
company overspends", which the viewer files under Not Me. The Myth-busting
frame makes the viewer's own incentives the subject, which is why the second
sentence hands them the word they get back at the end: rewarding.

## PROMISE (S2)

You will find out why an AI coding bill explodes, and it will not be the thing
you were about to blame.

## OPEN LOOP (S10)

Planted: sentence 2 — "And the real reason has nothing to do with Claude — it's
something you're probably rewarding." Forward reference plus a distinctive word
(*rewarding*) held back for the ending.

Paid off twice: the mechanism lands at "Uber was ranking its own teams on
internal leaderboards by how much AI they used", and the word itself returns per
S18 at "So before you blame the model, look at what you're rewarding" — then the
title inverts on "Claude isn't eating your tokens. Your scoreboard is."

## WHAT -> WHY -> SO WHAT (S7)

WHAT: Uber exhausted a full-year AI budget in four months, and its CTO says a
single two-hour session cost $1,200.
WHY: not model pricing — adoption was being gamified. Leaderboards ranked teams
by usage volume, so consuming more tokens was the visibly rewarded behaviour and
consuming fewer read as under-performing.
SO WHAT: the counter-turn is the point. It WORKED — around 70% of committed code
came out of those tools — so this is not an argument against the spend. It is an
argument that measuring input while never measuring output is how a budget
disappears without anyone able to say what it bought. Uber's own COO says the
link to shipped features is not there yet. The viewer's takeaway is to check
what their own team rewards, not to use Claude less.

## WHAT WAS CUT (S11, S21)

- The Kahn v. Anthropic Max class action — a genuinely newsworthy second story,
  but every line of it needs allegation framing and it pulls the reel away from
  the incentive thesis. See research.md -> EXCLUDED.
- Uber's reported $1,500/month per-tool cap — the primary (Bloomberg) is
  paywalled and returned 403; only aggregators carry it. Cut on sourcing, not
  on interest. It would have made a cleaner ending, and its absence is why the
  reel ends on the COO instead.
- Per-engineer spend bands ($150-250 average, $500-2,000 power users) — cut
  because stating either number invites the viewer to take it as typical, and
  the reel's argument does not need it.
- ~11% of live backend updates shipped by agents without human oversight — cut;
  it opens a safety question the runtime cannot answer responsibly.
- The whole prompt-caching mechanism (statelessness, exact prefix match, what
  invalidates a cache). This was the entire previous draft of this reel. It is
  accurate and useful, but it is an explainer about a tool, and this is a story
  about a company. Kept as a candidate for its own reel.

## KNOWN CHECKER DISAGREEMENT (recorded, not chased)

`check_script.py` reports NUMBERS one every 17.0 sentences and flags 1/1 spec
sentences as WHAT-WITHOUT-SO-WHAT. Both are artifacts: the detector counts
DIGITS (`\$?\d[\d.,]*`) and this script spells its numbers out for TTS. The
script actually carries eight numeric facts across seventeen sentences — one
every ~2.1, which MEETS the playbook's one-every-2-3. Numerals are not written
back in, because "$1,200" and "32%" are exactly what made whisper emit orphan
caption fragments (G30). Worth fixing in the checker: count spelled-out numerals
too.

A third artifact, same root: OPENING-has-no-anchor fires on sentence 1 even
though it opens "…says that this year he spent…". The detector accepts a digit
or one of (today|tomorrow|this week|just|now|yesterday) — "this year", "this
month" and every bare month name are missing from that list. The hook IS
anchored, in the viewer's language; the word list is short. All three of these
are advice and none blocks.

## SOURCES

Reporting, not disclosure — see `research.md` for the per-claim ledger, the VIA
chain, and what was excluded and why.

- https://www.forbes.com/sites/janakirammsv/2026/05/17/uber-burns-its-2026-ai-budget-in-four-months-on-claude-code/
- https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/
- https://finance.yahoo.com/technology/ai/articles/uber-blew-entire-2026-ai-145000897.html
