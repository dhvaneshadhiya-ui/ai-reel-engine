# Research — claude-fable-5-1

Claims ledger + search log. Tiers: official / multi / single / disputed.

## CLAIMS

- CLAIM: A Millennium portfolio manager says a one-in-a-million crash went
  unexplained for four to five years, every model tried missed it including
  Fable 5, and Fable 5.1 was the first to find it.
  TIER: official
  SPOKEN: "One crash in every million runs."
  SPOKEN: "Five years, and nobody on the team could explain it."
  SPOKEN: "Every model they tried missed it, including Anthropic's own Fable 5."
  SPOKEN: "That's a Millennium portfolio manager, quoted on Anthropic's own launch page."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic's own launch page, attributed testimonial (Damien, Senior
       Portfolio Manager, Millennium). This is VENDOR-PUBLISHED customer
       testimony, not independent verification, which is why the script names
       the page out loud in the same breath as the claim.

- CLAIM: Claude Fable 5.1 shipped 1 September 2026.
  TIER: multi
  SPOKEN: "Then Fable 5.1 shipped on September first, and found it."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic (primary announcement)
  SRC: https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads
  VIA: VentureBeat own reporting, 1 Sept 2026

- CLAIM: On Terminal-Bench-Science 0.1 (agentic scientific research) Fable 5.1
  scores 52.6% vs Fable 5's 24.7%.
  TIER: official
  SPOKEN: "Take the headline number."
  SPOKEN: "On agentic science work, Fable 5.1 more than doubled Fable 5: twenty-four point seven percent, to fifty-two point six."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic's own benchmark table. Vendor-run; the reel says so at the end.
  SRC: https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads
  VIA: VentureBeat, which repeats the figures and labels them vendor-reported.

- CLAIM: Fable 5.1 trained a neural network producing a new elevation map of a
  third of Venus; the prior altimetry footprint was 10-20 km, the new map
  resolves features down to 2-3 km. The paired source images are captioned
  "Altimetry 10-20km footprint" and "New DEM (300m) a volcano 15km across".
  TIER: official
  SPOKEN: "Then Venus, where it redrew a third of the planet."
  SPOKEN: "The old map's resolution was ten to twenty kilometres, so a volcano fifteen kilometres wide came out as a smudge."
  SPOKEN: "Here it is."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic, with the before/after images published on the same page.
  NOTE: the reel speaks ONLY the 10-20 km figure and the 15 km volcano, both of
  which are stated on the page. The 300 m DEM grid figure appears only in the
  image caption and is NOT spoken, because grid spacing and resolvable feature
  size are different quantities and conflating them would overclaim.

- CLAIM: Cache reads now cost $0.25 per million tokens, 75% less than Fable 5's
  $1.00; input stays $10/M and output stays $50/M.
  TIER: multi
  SPOKEN: "Back to the bottom of that page. It's the price of a cache read."
  SPOKEN: "Down seventy-five percent, to twenty-five cents a million tokens. Input and output didn't move."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic, "Cost and availability"
  SRC: https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads
  VIA: VentureBeat, which supplies the prior $1.00 rate Anthropic states only
       as a percentage.

- CLAIM: The cache-read cut lowers effective cost ~25% on typical workloads and
  up to ~45% on complex coding / highly agentic tasks.
  TIER: official
  SPOKEN: "So if you leave an agent running against the API, you now pay roughly twenty-five percent less than on Fable 5, and closer to forty-five on the heaviest jobs."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic, with a published chart indexing Fable 5 = 100 against 75
       (typical) and 55 (highly agentic), measured over four weeks of August
       2026 usage at default effort. Spoken hedged ("roughly", "closer to")
       because Anthropic itself writes "around" and "up to around".

- CLAIM: Fable 5 reached only about 11% of Anthropic model spend among ~70,000
  companies in Ramp's card data, and cheaper Opus 5 overtook it.
  TIER: single
  SPOKEN: "Which says what went wrong last time."
  SPOKEN: "The Financial Times put Fable 5 near eleven percent of Anthropic spend."
  SPOKEN: "Anthropic's best model, and reportedly almost nobody left it running."
  SRC: https://aiweekly.co/node/10679
  VIA: Financial Times reporting on Ramp corporate-card transaction data. ONE
       origin (Ramp), reported by one outlet (FT); every other hit is an
       aggregator of the same FT piece. Spoken hedged by naming the outlet out
       loud and by "near", per framework S20. This is the only claim in the
       reel that is not Anthropic's own, and it is deliberately the one with
       attribution in the sentence itself.
  SRC: https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads
  VIA: VentureBeat, citing the same FT/The Information reporting — NOT an
       independent origin, logged so the tier is not mistaken for multi.

- CLAIM: Mythos 5.1 is identical to Fable 5.1 with more permissive safeguards,
  available only to vetted US organisations via cyberdefence and life-sciences
  trusted-access programmes.
  TIER: official
  SPOKEN: "Meanwhile Mythos 5.1 is the same model on a looser leash: vetted US cyberdefence and life sciences only."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic, "Trusted access for Claude Mythos 5.1" and "Cost and
       availability" ("only available to a set of US organizations").

- CLAIM: The benchmark figures are Anthropic's own, run with its production
  safeguards enabled, and no independent evaluation exists yet.
  TIER: official
  SPOKEN: "But every figure here is Anthropic's own, measured with its safeguards switched on."
  SPOKEN: "Nobody outside has checked one yet."
  SRC: https://www.anthropic.com/claude-fable-and-mythos-5-1
  VIA: Anthropic states "Fable 5.1 was evaluated with its production safeguards
       enabled".
  SRC: https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads
  VIA: VentureBeat, which calls the results "vendor-reported results rather
       than independent proof" — the basis for the closing line.

## SEARCHED

- 2026-09-02  fetched https://www.anthropic.com/claude-fable-and-mythos-5-1
  (three passes: full announcement, science/real-world section verbatim,
  Millennium quote + cost + Mythos sections verbatim). Settled every benchmark,
  the pricing, the Venus figures and the Mythos access rules.
- 2026-09-02  "Anthropic Claude Fable 5.1 Mythos 5.1 release" — settled the
  1 Sept date, the 1M context / 128k output figures, and located independent
  coverage.
- 2026-09-02  fetched VentureBeat 1 Sept 2026 — settled the prior $1.00 cache
  rate, batch pricing, and supplied the vendor-reported caveat.
- 2026-09-02  fetched 9to5Mac 1 Sept 2026 — surfaced the Millennium crash story
  and confirmed the GA / trusted-access split.
- 2026-09-02  "Claude Fable 5 enterprise spending 11% The Information Financial
  Times adoption pricing" — settled the FT/Ramp figure (11.4% of dollar spend,
  6% of tokens, ~70,000 companies) and that Opus 5 overtook it. Established
  that every aggregator traces to the same single FT piece, hence TIER single.
- 2026-09-02  attempted the five x.com/claudeai posts supplied in the brief.
  WebFetch returns HTTP 402 and the in-app browser hits X's error wall, so the
  official thread could NOT be read. Nothing in the reel rests on it; the same
  launch content is on the announcement page, which is the stronger primary
  source anyway. Logged so the gap is visible rather than assumed covered.
