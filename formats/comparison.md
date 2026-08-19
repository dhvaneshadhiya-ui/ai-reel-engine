# Format: comparison

"iPhone 18 vs iPhone 17". "Grok vs ChatGPT". Perishable, but spikes hard at
launch moments.

**Numbers:** `python3 tools/reel_gates.py --formats`

## Honest status of this profile

The **timings are inherited from `news` and were NOT measured for this genre.**
There is no comparison teardown in `styles/`. Rather than nudge the bands to
something that would *look* derived, every timing is held deliberately
identical to news and labelled as inherited in `FORMATS._derived`.

**Before trusting them, tear down 3-5 real comparison reels and split the
profile off properly.** What follows below is structural — it comes from what
the genre IS, not from measurement, so it is safe to rely on.

## Structural rules (gate G26 — these BLOCK)

1. **Declare both sides.** `"sides": ["iPhone 18", "iPhone 17"]`, named exactly
   as they appear on screen.
2. **At least 3 compare scenes** — `comparesplit`, `hcompare`, `specsheet`,
   `chart`, `strikeswap`. Fewer than that is a review of one product that
   mentions the other.
3. **Balance 40-60%.** Tag every beat `"side": "a" | "b" | "both"`.
   Single-sided screen time must sit inside that band. A reel that gives one
   product 80% of the screen is an ad, and the gate says so by name.
   *If nothing is tagged, balance is reported as a WARNING — the absence of
   tags must never read as evidence of fairness.*
4. **Label every split.** `comparesplit` needs `leftLabel` + `rightLabel`;
   `hcompare` needs `topLabel` + `bottomLabel`. An unlabelled split is two
   videos playing next to each other.

## Scene vocabulary

| Beat | Scene type |
|---|---|
| Both on screen, same task | `comparesplit` (left/right) |
| Before/after, stacked | `hcompare` (top/bottom) |
| Spec table | `specsheet` |
| Benchmark or price bars | `chart` |
| "This is dead, use this" | `strikeswap` |
| One side's detail | `footage` / `deviceframe` + `side` tag |

## Story standard

`styles/shortform-script-framework.md` applies here too — it is universal by its
own title, and the skeleton below is a SHAPE, not a story. A comparison reel can hit
every beat of that skeleton and still be a list: the hook / name the two / rounds / the catch / verdict
tells you what goes where, and the framework tells you whether the viewer has a
reason to hear the next one.

**One caveat, stated because it is true:** `tools/check_script.py`'s structural
thresholds were calibrated on a matched pair of NEWS scripts, and no reel in
this repo has ever used `comparison`. Its bridge-rate and spec-density numbers are
orientation here, not a verdict — an enumerated list legitimately enumerates.
The framework itself applies unchanged; only the arithmetic is unproven.

## Script skeleton

1. **HOOK (<=2s)** — the *result*, not the matchup. "The cheaper one won." Not
   "today we compare X and Y."
2. **NAME THE TWO** — one line, both sides, as declared in `sides`.
3. **3-5 ROUNDS** — one dimension each (price, speed, battery, camera). Each
   round is ONE compare scene and ONE sentence. Alternate which side wins;
   if one side wins everything, say that plainly rather than manufacturing
   suspense.
4. **THE CATCH** — the thing spec sheets do not show. This is the beat people
   stay for.
5. **VERDICT + CTA (required)** — say which one, for whom. Then
   `endquestion` ("which are you buying?") or `commentcta`.

## Rules that still apply

Everything in `RULES.md`: source credit on borrowed footage (G14), attribution
on data cards (G15), standard notation (G16), presenter on screen by 5s (G17),
one highlight per beat (G22). Pick the avatar register (G19) — a comparison
with a clear loser is usually `serious`, a "both are great" is `warm`.
