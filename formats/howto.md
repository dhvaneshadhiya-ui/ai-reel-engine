# Format: `howto`

Teaching the viewer to **do something on their phone**. Not "here is what
happened" (that is `news`), not "here are five tools" (that is `top5`) — one
task, start to finish, done well enough that the viewer can repeat it.

Derived from a 7-reel teardown, 2026-09-02. Numbers live in `FORMATS["howto"]`
in `tools/reel_gates.py`; print them with `python3 tools/reel_gates.py
--formats`. Read that entry before changing anything here — it records which
figures were measured and which were inherited.

## References torn down

| Creator | Reel | Runtime |
|---|---|---|
| Hayls World | WhatsApp usernames | 63.0s |
| Hayls World | Samsung quick settings | 63.9s |
| Hayls World | iOS 27 photo tools | 66.5s |
| Daniel About Tech | remove objects from photos | 52.7s |
| Daniel About Tech | eSIM transfer | 58.7s |
| Daniel About Tech | live wallpaper | 75.1s |
| Payette Forward | hidden iPhone feature | 24.5s |

## The three things this genre does that news does not

### 1. It holds the shot

Pooled shot length across all seven, p75 = 6.46s even at the most aggressive
change detection. News caps a moving scene at 2.9s. **The reason is not that
tutorials are slower — it is that the screen is the content.** In a news reel a
held image is dead air; in a tutorial, cutting away mid-action destroys the
only thing the viewer came for. If a finger is completing a tap, the shot ends
when the tap resolves, not when a stopwatch says so.

`dur_max.motion` is 6.5s here. That is a ceiling, not a target — a step that
resolves in 2s should take 2s.

### 2. The presenter is often absent

Face share across the seven: 0%, 0%, 0%, ~8%, ~8%, ~17%, ~40%. **Three carry no
presenter at all.** News floors facecam at 10%; that floor would forbid the most
common form of this genre, so `howto` floors at 0.

Use a face where it earns its place — an opening line of context, a warning, a
CTA — and not because a gate asked for one.

### 3. The device is real, held, and in a real room

Both Hayls and Daniel shoot a **physical handset in hand**, finger operating it,
against a real background. Neither composites a screen recording into a drawn
bezel. The hand doing the tap is what makes a step legible: the viewer sees
*where* to press, not just what changed.

Our `deviceframe` draws a synthetic phone around a screen recording. That is a
legitimate second-best and it is what `chatgpt-stickers` used — but if the
choice exists, **record the real phone being used**. Declare such an asset
`"surface": "world"` (it is real footage of a device, not a screen capture) so
the compiler leaves it full-bleed and does not draw a bezel around a phone that
already has one.

## Structure

The genre's shape is a **sequence**, not an escalation. There is no turn and no
reveal — the promise is stated, then kept, step by step.

1. **Title over the first step.** Both creators burn a title onto the opening
   shot rather than spending a scene on it: "E-SIM FROM AN IPHONE TO ANOTHER",
   "NEW PHOTO EDITING TOOL". The reel is already doing the thing while it
   announces it.
2. **Steps, in the order a hand performs them.** One action per beat. The
   narration is procedural and unglamorous: "tap on transfer number", "and then
   swipe up", "now you'll see connecting".
3. **The blocker, said out loud.** The strongest moment in a tutorial is the
   place people get stuck — a minimum, a permission, a setting that must be on
   first. `chatgpt-stickers` does this with WhatsApp's three-sticker minimum.
   Do not bury it; it is why someone finishes the reel.
4. **The finished state, held.** End on the result existing — "Cellular Setup
   Complete", the pack in WhatsApp. The payoff of a how-to is proof it worked.
5. **CTA.** Required (`requires_cta`). A how-to has a natural one: the viewer
   who wants the longer version or the link.

## Writing it

- **Second person, imperative.** "Tap Add to chat apps." Not "the user then
  taps".
- **Say the label that is on screen**, in the words the UI uses. Rule 3 is
  strictest here: if the narration says "settings" and the button says
  "Preferences", the viewer stalls.
- **No suspense about the outcome.** Curiosity in this genre is "can I do
  this?", not "what will happen?". Withholding the result is not a hook, it is
  an obstacle.
- **One task.** A second task is a second reel.

## What was NOT measured

`hook_max` (2.0s), `sfx` (6-9) and `sfx_vol` are inherited from `news`. The
teardown's "first cut" figures — median 9.4s — measure editorial cut rhythm,
not how long the opening claim is held, and separating those needs the frames
rather than the detector. Re-measure before treating any of the three as a
fact about this genre.
