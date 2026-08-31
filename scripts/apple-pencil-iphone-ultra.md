# apple-pencil-iphone-ultra — script + beat map

**Canonical script:** `jobs/apple-pencil-iphone-ultra/script.md` (read by
`script_approval.py` / `research_check.py`). This file mirrors it plus
carries the beat map and build notes.

**Format:** news · **Style:** editorial
**Look:** f55b0b7c (digital twin, neutral) · **Measured:** 206 words → ~76s at 2.7 wps (band 60-80s)
**Refs:** 9to5Mac 2026-08-30 (Michael Burkhardt) · MacRumors 2026-08-30 (Joe Rossignol) · both citing Bloomberg's Mark Gurman ("Power On"); Sept 9 event + invite art reused from apple-surprise-and-shine (MacRumors 2026-08-26, official)

## Script (spoken narration)

Apple's foldable iPhone debuts September 9th, about a week from now. It almost shipped with an accessory you will never get to buy.
That accessory is a Pencil, and the real reason it got buried says more about the phone than the pencil.
Bloomberg's Mark Gurman has the receipt: he says Apple didn't just sketch this, it prototyped it and tested it.
This one's shorter than your iPad Pencil, magnets in the side, sized to match the phone once it folds shut. Close enough to have shipped.
So that killed it.
Stuck to the side, it made the phone awkward to even hold.
And what's worse, Gurman says the tip would rest against Apple's most fragile screen yet and leave what he calls "unsightly marks."
This is Gurman's reporting, not Apple's word. One report, repeated everywhere, verified nowhere else.
But here's why Gurman says that matters more than the specs: Apple doesn't want to contradict Steve Jobs, who said back in 2007 that nobody wants a stylus.
Simply put, this was never really about the pencil. It's Apple admitting its first folding screen might not survive a sharp tip touching it. That's the real reason you'll never hold one.
We'll know everything else in a week.

## Beat map (every beat bound to a verified asset or MG spec)

| anchor | visual |
|---|---|
| hook (≤2.2s) — "Apple's foldable iPhone debuts September 9th, about a week from now. It almost shipped with an accessory you will never get to buy." | asset **hook-hero** (9to5Mac's own headline + its "iPhone ULTRA" editorial render, folded+unfolded, dual camera bump), full-bleed, slow push-in — sound-off test passes: a folding phone reads as the subject even muted |
| "That accessory is a Pencil, and the real reason it got buried says more about the phone than the pencil." | face, full frame, no card — plants the open loop, paid off at the close |
| "Bloomberg's Mark Gurman has the receipt: he says Apple didn't just sketch this, it prototyped it and tested it." | `receipt` asset **mr-headline** (MacRumors' own headline card, "Apple Pencil for iPhone Ultra Was Tested" + byline) — "tested it" in narration lands on "Tested" on screen |
| "This one's shorter than your iPad Pencil, magnets in the side, sized to match the phone once it folds shut. Close enough to have shipped." | `annotatezoom` on asset **pencil-pro-photo** (the REAL Apple Pencil Pro, Apple's own product photo via MacRumors), slow zoom along the shaft; on-screen label "REAL Apple Pencil Pro — shown for scale, not the prototype" so nobody mistakes it for a leak photo |
| "So that killed it." | face, stark cut — short act-break, no card |
| "Stuck to the side, it made the phone awkward to even hold." | `receipt` asset **two-reasons-receipt**, top half in frame (9to5Mac's own paragraph: "awkward to hold... since it'd stick on the side") |
| "And what's worse, Gurman says the tip would rest against Apple's most fragile screen yet and leave what he calls 'unsightly marks.'" | same asset **two-reasons-receipt**, slow drift down to the second paragraph ("unsightly marks... more delicate inside screen") — G07-safe: one clip, one continuous drift, not a re-cut |
| "This is Gurman's reporting, not Apple's word. One report, repeated everywhere, verified nowhere else." | face, stark cut back to facecam — the honesty beat, no card, no distraction |
| "But here's why Gurman says that matters more than the specs: Apple doesn't want to contradict Steve Jobs, who said back in 2007 that nobody wants a stylus." | `receipt` asset **jobs-quote-receipt** (9to5Mac's own paragraph naming Gurman's Steve-Jobs framing + the "Who wants a stylus?" quote) — Gurman's own connection as reported, not this reel's invention |
| "Simply put, this was never really about the pencil. It's Apple admitting its first folding screen might not survive a sharp tip touching it. That's the real reason you'll never hold one." | face, full frame — interpretive payoff, no receipt to point at; pays off the open loop planted in beat 2 |
| "We'll know everything else in a week." | asset **invite-hero** (Apple's own official Sept 9 "Surprise and shine" invite art, reused verbatim from apple-surprise-and-shine — same event, already verified official) — bookends the hook's "about a week" anchor |

**Discipline:**
- No photo of the actual tested prototype exists anywhere and none is implied
  — the one product photo used (**pencil-pro-photo**) is on-screen labeled as
  the real, shipping Apple Pencil Pro, shown for scale only.
- Every claim beyond the two official facts (Sept 9 event; the 2007 Jobs
  quote) is single-source Gurman reporting and is spoken hedged ("Gurman
  says", "his own reporting, not Apple's word", "one report, repeated
  everywhere, verified nowhere else") per research.md.
- Credits: 9to5Mac (hook-hero, two-reasons-receipt, jobs-quote-receipt),
  MacRumors (mr-headline, pencil-pro-photo's underlying product shot
  credited to Apple), Apple (invite-hero). On-screen per credit_instructions.
- Facecam: "that accessory is a Pencil" (open-loop plant) / "so that killed
  it" / the honesty beat / the "simply put" so-what payoff — four facecam
  beats, well inside the usual band for a receipt-heavy news reel.
- No CTA keyword (`cta_keyword: ""`) — closer is a date-anchor / follow-up
  promise, not a comment-gate; G24 does not require a CTA scene for `news`.
- Open loop: planted in beat 2 ("the real reason it got buried says more
  about the phone than the pencil"), paid off verbatim near the close
  ("That's the real reason you'll never hold one") — shared 3-word phrase
  is deliberate, per framework S10/S18.
- Humanizer pass (2026-08-31, whole script, this pipeline's own shipped
  scripts as voice sample): cut a throat-clearing "Worth saying plainly:"
  opener, cut the overused word "quietly", broke up a third repeated
  "That's..." sentence-opener ("So that killed it."), swapped a house tic
  ("that's why it", already used in claude-eating-tokens) for a fresh
  phrase. Kept the "not X but Y" honesty-beat construction ("Gurman's
  reporting, not Apple's word") deliberately — it is the mandated
  attribution language, not filler.
- Treatment note: does NOT reuse apple-surprise-and-shine's `annotatezoom`-
  on-deviceframe motif the same way — here the annotatezoom sits on a REAL
  product photo (Pencil Pro) with its own "shown for scale, not the
  prototype" disclaimer, which that reel didn't need. `invite-hero` is
  reused as an ASSET (identical official art, identical event) rather than
  re-captured — new for this pipeline; prior reels always re-scouted per
  slug.

## Known checker false positive (documented, not fixed)

`check_script.py`'s SECOND PERSON check strips "quoted" spans between any
two apostrophes (`[\"'][^\"']{8,}[\"']`) before searching for "you" — on a
script this contraction-heavy ("Apple's", "Gurman's", "didn't", "it's"), that
regex treats the stretch between two unrelated contractions as one long fake
quotation and deletes it, which ate the hook's own "you will never get to
buy" in testing. Verified directly against the regex in a standalone
interpreter (2026-08-31) — the script does address the viewer with "you" in
the hook (word ~20 of 206) and again in the payoff; forcing it earlier or
stripping contractions to dodge the tool would fight the style pack's own
"contractions always" rule for no real gain. Left as-is; this is the kind of
finding `check_script.py`'s own header calls advice, not a rule.
