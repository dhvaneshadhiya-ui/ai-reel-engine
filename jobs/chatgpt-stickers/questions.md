# Open questions — chatgpt-stickers

## 1. The CTA deliverable — RESOLVED 2026-09-01

The script ends: *"Comment STICKERS and I'll send you the exact setup I used."*

That promise is now backed. `giveaway.md` holds the guide, and it is published
as a shareable page for DM delivery:
https://claude.ai/code/artifact/78ae7b9a-e87c-4512-82fa-1107419ea982

It contains the seven steps, the exact template settings read off the screen
(style 3D, one portrait, emoji love-you / puzzle / rose / collision), the
verifiable portion of the generated prompt, a reusable prompt clearly marked
as ours rather than a transcript, all nineteen styles with a note on which
three to start with, the WhatsApp rules, and four real failure modes.

Deliberately NOT promised: the "24 copy-paste prompts" from the first draft.
There is one template with three dropdowns. Inventing a number for a giveaway
is the same failure as inventing one for a spec.

## 2. Which recording carries the style scroll

`screencap-1` shows the full nineteen-style scroll but the pack it is
building is the cat-and-woman sample, not your face. `screencap-3` is your
face. Beat 6 therefore cuts from your pack to the sample grid and back.

That is honest (it is all one feature) but it is a visible subject change
mid-reel. Options: accept it, or re-record the style scroll inside the
session that made your pack so the face is continuous. **My call: accept
it** — the style picker is obviously a picker, and the cut back to your grid
at beat 7 reads as "and here's mine."

## 3. Length

155 words lands at roughly 57 seconds on our measured pace, inside the
`ai-tools` band of 40-60s but near the top. If you want it tighter, the two
lines I would cut first are "That checkerboard is a real transparent PNG"
(the checkerboard is visible anyway) and "This is where it stops people"
(the next sentence explains it regardless). That takes it to about 48s.

## 4. Noted, not acted on

- `check_script` reports NO OPEN LOOP. The loop is real: "built the whole
  pack from one photo" in sentence two, returned to as "One photo, nine
  stickers, in WhatsApp" at the end. The checker looks for a literal phrase
  echo and does not see this one. Not changing the script for it.
- `check_script` reports NUMBERS one every 21 sentences. It counts digits;
  ours are spelled out because that is what the TTS needs. Artifact.
- `framework_check` F5 fired on an earlier draft because its ask-detector
  matches the word "type", and the line was "You don't type a prompt." The
  rule is right and the line was reworded to "There's no prompt box." Worth
  knowing the detector has that edge, since a future script saying "type" in
  a non-CTA sense will trip it too.
