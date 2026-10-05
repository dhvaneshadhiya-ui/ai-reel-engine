# Critique — ios27-safari-settings

## Round 1
| hook | read | motion | variety | sync | match | min |
|  6   |  7   |   6    |    5    |  7   |   8   |  5  |
Worst three: 1. [scenes 04-05, 06-07, 16-17] the same image twice in a row (page menu, Notify Me dialog, CTA card) -> reads as a stalled edit, lint [DUPLICATE] blocks -> merge each pair into one slide in shot-plan.json (18 -> 15 shots) and move the second line's focus moves onto the first.  2. [cut 08->09, 28.8s] the Describe Extension sheet opens as a small portrait image on black, then pushes in -> a dip to luma 26 at the cut -> start that scene already zoomed (focus at 0).  3. [scene 09->10] two white sheets back to back (category sheet, Recipe Keeper) -> no change of shot -> put a rows card ("Apple typed / Safari built") above Recipe Keeper and shrink the screen to h 620.
Checks failed: no empty page (scene 03 "One catch" is 78% empty); one sound buried (paper-slide under speech).
Verdict: ANOTHER ROUND

## Round 2
| hook | read | motion | variety | sync | match | min |
|  6   |  7   |   7    |    7    |  7   |   9   |  6  |
Worst three: 1. [cut 05->06, 23.5s] focus at 0 still eases from the whole image over 0.7s, so the portrait page menu opens with black bars -> dip to luma 7 -> add an opt-in `instant` focus to SlideBlocks.tsx (lands at full zoom on frame 0) and use it on every at-0 focus.  2. [scene 00, 0.0s] the hook is a small Lock Screen on white, the Notify Me alert unreadable until 2.6s -> the thumb has no reason to stop -> open with an instant focus on the notification, box h 760.  3. [scenes 03 and 11] "One catch for all 3" / "The catch" are a headline over an empty page -> the promise and its payoff have nothing to look at -> three rows (Notify Me / Describe Extension / Tab topics) with "?" on both, answered with "Apple Intelligence" in scene 12.
Also fixed this round: caption `like ""back` (a correction re-added quotes the script already had); CTA "track ?" wrapping the "?" onto its own line -> pill "[[track?]]".
Checks failed: no empty page (scenes 03, 11); paper-slide still MASKED (-29 dB under -15 dB speech) -> Camera Shutter.
Verdict: ANOTHER ROUND

## Round 3
| hook | read | motion | variety | sync | match | min |
|  8   |  8   |   8    |    8    |  8   |   9   |  8  |
Evidence: hook — scene 00 opens on Apple's Lock Screen already framed on the Notify Me alert ("An update was detected on this page.") and holds that framing into scene 01, pill lands on "refreshing" at ~0.5s. read — phone sheet: every headline, row and the page-menu rows legible; captions sit in their own band below content. motion — no fades (instant focus on every at-0 focus), rows and pills arrive on spoken words. variety — 15 slides over 56s, image / rows / steps+clip / Apple video alternate; no back-to-back repeat (lint clean). sync — 8 cues, all AUDIBLE or UNMASKED (sfx_audibility), voice-first mix at -14.6 LUFS. match — each slide shows the line being spoken (menu row on "Notify Me", "Check daily" ring on "checks daily", Recipe Keeper on "saves recipes", Apple's tab-topics animation on "sorts them into groups").
Worst three (remaining, accepted): 1. [all slides] content ends near 60% of the frame, lint advises DEAD SPACE 32-61% -> the lower band reads a little bare on a large phone -> next reel: raise screen boxes to h 900+ or add a second block; not changed here because the caption band and platform UI sit below it.  2. [scene 05, ~17-22s] 2.5s without a new event while the Notify Me dialog is read -> acceptable for a how-to step, focus moves land on "waiting for", "checks daily", "change the".  3. [scenes 04, 06] Apple's User Guide page-menu art is 490x1008, upscaled -> slightly soft at full zoom -> a real-device or simulator recording would fix it (no Xcode on this machine).
Checks failed: none (no empty page — catch slides now carry the three "?" rows; longest gap scene 05 2.46s; one accent colour, captions clear; end card holds 3.2s, read twice).
Verdict: READY
