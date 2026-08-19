# iPhone 18 Pro — script v3, as an Explainer

Shape, promise and loop declared in `structure.md` before writing. Goal in
`goal.md`. Facts from `public/assets/iphone-18-pro/manifest.json`.

**Why Explainer and not News:** News runs on *what happened*, and nothing has.
Apple has announced nothing; every fact is reported or projected. News has no
engine here, which is why the first draft defaulted to nine features in source
order. Explainer runs on *question → context → how it works → example →
implication*, and the question is answerable with what we have.

---

## Narration

Why does your phone shoot beautifully outdoors and turn to mush indoors? It isn't the software. It's a piece of glass that can't move.
Apple's iPhone 18 Pro is expected on September 9, and reportedly that changes, though it still isn't the one I'd care about most.
The main 48MP lens gets a mechanical iris: an aperture that physically opens and closes.
Open it wide, more light gets in, less of the frame stays sharp.
Close it down, everything's sharp, if you have light.
That trade is one every real camera lives with, and your phone has never had the choice.
So: a dark restaurant, wide open. A group shot, stopped down. One lens, both.
And it isn't cheap: analyst Ming-Chi Kuo says the lens alone costs about 50% more.
Then moving parts cost battery, which is why the A20 Pro matters: Apple's first 2nm chip, projected 15% faster on 30% less power.
But here's the one I'd actually want. Apple's own C2 modem reportedly adds 5G over satellite: signal where there's no tower.
None of it is official until Apple says so.
Which is the pattern: a phone built to keep working where phones normally stop, with no light, no battery, or no bars.
Which of those would you notice first?

---

## How the shape changed the script

The News draft and this one use the same facts and are not the same video.

| | News draft | Explainer |
|---|---|---|
| opens on | the date | the viewer's own problem |
| the iris is | a feature, stated | a **mechanism**, explained |
| the trade-off | absent | the middle third |
| chip / modem | two more features | consequence and payoff |
| ending | summary | returns to the opening question |

The middle third is the real difference. News states *"a mechanical iris that
opens and closes"* and moves on; Explainer spends four sentences on **why an
aperture is a trade** — light against depth of field — because that is the thing
the viewer does not know and cannot infer. Framework S17: the structure decides
what the script is *for*.

## Beats

| # | Line | Visual | Note |
|---|---|---|---|
| 1 | outdoors vs indoors | MG: HCompare | S15 visual contrast — the question, shown |
| 2 | a piece of glass that can't move | **NEEDS SCOUT** | a fixed aperture, any lens |
| 3 | expected September 9 | `hook-pair` | |
| 4 | not the one I'd care about most | facecam | the loop, on the face |
| 5 | the mechanism | **NEEDS SCOUT** | an iris opening/closing — see gaps |
| 6-8 | wide / narrow / the trade | MG: HCompare | one diagram, two states |
| 9 | restaurant / group shot | **NEEDS SCOUT** | two real photos would do it |
| 10 | Kuo: ~50% more | `rc-macrumors-head` | the receipt |
| 11 | A20 Pro, 2nm, 15% / 30% | MG: SpecSheet | projections, attributed |
| 12 | the one I'd actually want | facecam | loop pays off |
| 13 | C2 modem, satellite | `rc-9to5mac-head` | the receipt |
| 14 | none of it official | MG: TypeCard | honesty beat |
| 15 | the pattern | MG: TypeCard, 3 claims | no light / no battery / no bars |
| 16 | which would you notice? | facecam | CTA answers the opening |

## Asset gaps

Worse than the News draft's, and that is the honest cost of this shape: an
Explainer has to SHOW the mechanism it explains (S13, S14), and our six assets
are back-view mockups plus two headline screenshots. The manifest's own
exclusions say the mockup shows no display, no camera, no aperture.

Three beats need footage that does not exist yet — a fixed aperture, an iris
moving, and one dark/one group photo. None needs to be Apple's; the mechanism is
generic. Until they exist this script is not shootable, and cutting to a static
back while the narration explains a moving part is exactly the Rule 3 break the
frame gates are for.

## Measured

    18 sentences · 212 words · 79s at 2.7 wps   (band 60-80s)
    bridges 44% · spec density 22% · longest spec run 1 · loop present
    em dashes 0

## humanizer pass (2026-08-19)

Applied per SKILL.md 2a — scoped, three patterns rejected on sight.

**Taken:**

- **S14, five em dashes.** Decisive on evidence: the approved script for this
  slug has ZERO, and the playbook bans "em-dash-speak" by name, so S14's
  writer's-sample exemption does not apply. They were my tic, not the voice.
  `tools/check_script.py` does not measure this at all.
- **S28, "Here's the mechanism:".** Announcing the next point instead of
  stating it. The mechanism sentence says the same thing without the throat-clear.
- **S13, "has never been allowed to make it".** Passive with a hidden actor ->
  "has never had the choice".

**Rejected, per 2a:** S5 vague sources (S20 and the manifest REQUIRE the hedges),
S9 not-X-but-Y (it answers the question just asked), S10 groups of three (the
payoff triad three beats were built to reach).

**What the pass exposed.** Removing the dashes by splitting sentences dropped
bridges 44% -> 23%: an em dash IS a bridge, and a period is not. The fix was to
delete the dash and keep the connective — colons and "and"/"then"/"though" —
which held the bridge rate and took the script from 81s to 79s, inside the band.

Two borrowed tools disagreed, and the disagreement was real: the humanizer is
calibrated on written prose where a dash is decoration, the framework on
narrative flow where it is connective tissue.
