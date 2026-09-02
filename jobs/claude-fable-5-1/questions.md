# Open questions — claude-fable-5-1

Four judgement calls. I have taken a position on each; say so if you disagree.

## 1. Runtime: 245 words, about 90s. The news band is 60-80s.

I went over deliberately and want your call. The reel has three movements
(capability, the price turn, why the price turn happened) and cutting to 80s
means deleting one of these:

- **Venus (about 13s)** — the only proof of capability that is a picture rather
  than a number, and the before/after is the strongest visual in the reel.
- **The Financial Times adoption beat (about 11s)** — the WHY. Without it the
  price cut is a spec, not a story.

My position: keep both, ship at ~90s, set `allowLong`. Say the word and I cut
the FT beat instead.

## 2. The hook has no date anchor, on purpose.

It opens "One crash in every million runs. Five years, and nobody on the team
could explain it." The subject and date land at second four. `check_script`
flags this (framework S1/S16 want the WHEN up front) and I am overriding it:
the crash is the reason to keep watching, and "Anthropic released a model on
September first" is the announcement, not the story. Frame 0 still shows the
Anthropic quote card, so the brand is legible on mute.

## 3. The hook is a testimonial Anthropic published about itself.

The Millennium quote is real and attributed (Damien, Senior Portfolio Manager),
but it sits on Anthropic's own launch page. I keep it AND say so out loud in
the same breath, then close the reel on "every figure here is Anthropic's own."
The alternative is opening on the benchmark instead, which is duller and no
more independent. My position: keep it.

## 4. One claim is not Anthropic's.

The Financial Times / Ramp figure (Fable 5 at ~11% of Anthropic spend) is
single-origin: one dataset, one outlet, everything else aggregates it. It is
spoken with the outlet named and hedged with "reportedly". My position: keep,
because it is the only outside check in the reel and it is what makes the
price cut mean something.

## Also worth knowing

- The five x.com/claudeai links you sent could not be read. WebFetch gets HTTP
  402 and the in-app browser hits X's error page. Nothing in the reel depends
  on them; the announcement page carries the same launch content and is the
  stronger source. Flagging it rather than quietly skipping it.
- No CTA. News format makes it optional and nothing here earns one.
