# Structure is not format

Found 2026-08-19, tracing why the framework "for all niches and topics" did not
seem to reach past tech news.

## They are two different things, and this repo had one word for both

`python3 tools/reel_gates.py --formats` prints what `format` actually controls:

    format      runtime    hook   facecam  sfx   sfx-vol      cta
    news        60-80s     2.0s   10%-20%  6-9   0.1-0.19     optional
    top5        26-48s     2.0s   10%-20%  6-9   0.06-0.1     required
    comparison  60-80s     2.0s   10%-20%  6-9   0.1-0.19     required

Every column is a **production envelope** — how long, how loud, how much face.
None of it is a story shape. `format` is the box the reel has to fit in.

`styles/shortform-script-framework.md` S17 is the **narrative structure** — the
shape of the telling. It lists ten:

    Discovery · News · Product announcement · Explainer · Tutorial
    Comparison · Story · List · Myth-busting · Transformation

## The gap

Only 3 of those 10 have a format file, and choosing a structure meant choosing a
format. So seven narrative shapes were unreachable — not because they were
rejected, but because the only vocabulary for "what kind of video is this" was a
list of runtime budgets.

A myth-busting explainer and a news round-up can share the `news` envelope
exactly — 60-80s, 2s hook, 6-9 SFX — and be completely different scripts. The
envelope has nothing to say about which one you are writing.

## What changed

**Structure is now a recorded decision, not a side effect of picking a format.**
`jobs/<slug>/structure.md` names the S17 shape, the promise, and the open loop,
and it is written BEFORE the first sentence — because none of the three can be
retrofitted by editing lines afterwards.

Format keeps doing its job: runtime, hook, SFX, CTA, and the gates that enforce
them. It just stopped pretending to describe the story.

## A caveat that is worth more than it looks

`tools/reel_gates.py --formats` says of two of the three formats, in its own
words, that their numbers are **inherited and unmeasured** — comparison is
"INHERITED from news ... Do not present these timings as derived", and top5's
face share is inherited too. All ten reels in this repo are `news`.

So the envelope layer is itself calibrated on one genre, and
`tools/check_script.py`'s prose thresholds are calibrated on one matched pair
within that genre. Both are honest about it. Neither should be quoted as a
verdict outside tech news until a reel in another genre exists to measure.
