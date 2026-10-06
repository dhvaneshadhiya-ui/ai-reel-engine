## Round 1
| hook | read | motion | variety | sync | match | min |
|  7   |  8   |   7    |    7    |  8   |   9   |  7  |
Evidence: hook — sc0 opens on presenter circle + real Software Update card + "Beta 3" pill at frame 0, but the card is text-heavy and static until the 0.9s focus. read — every label legible at phone size; captions clear of content after the 2026-10-06 layout fixes (sc6 caption raised to 470). motion — spring arrivals, clips move on their own; no fades. variety — 12 scenes alternate real clips and cards, but 5 consecutive scenes (sc4-sc8) share one layout: eyebrow, headline, one clip. sync — 22 cues, one every 3.0s, all audible (sfx_audibility 21 AUDIBLE, 1 UNMASKED). match — every change is shown on a tester's own beta-3 iPhone while it is spoken; cards only for the timeline and the PCC explanation.
Worst three: 1. [sc0, 0-6s] the Software Update card is a wall of disclaimer text -> the eye has nowhere to land after the headline -> FIX: focus rect tighter on the title row ([0,0,1080,300]) and hold it, so the "iOS 27.2 Beta 3" line fills the card. 2. [sc5, 26.7-35.9s] longest hold, 9.2s on one clip -> attention dips mid-reel -> FIX: split at "That's on select models" into its own card (needs a plan split; not done this round). 3. [sc9-10, 49.9-60.9s] two timeline cards back to back with the same steps layout -> reads as one long card -> FIX: give sc9 the Siri-language list instead of steps.
Checks failed: none hard. Longest gap without a new event: sc5 (Type to Siri clip, 9.2s; the "Select models only" note lands at 34.1s).
Verdict: ANOTHER ROUND

## Round 2
| hook | read | motion | variety | sync | match | min |
|  8   |  7   |   8    |    8    |  8   |   9   |  7  |
Evidence: hook — title-row focus now lands on "just dropped". read — sc5 Type to Siri clip at h860 ran into the caption ("Type"). variety — sc6 select-models card splits the 9.2s hold; sc10 is now a Siri-languages card, not a second steps strip. sync — 21 cues, all audible.
Worst three: 1. [sc5, 31s] clip bottom under the caption -> words on top of UI -> FIX shot-plan sc5 clip h 860 -> 760. 2. [sc10, 49.9s] page opened bare (rows waited for "five") -> empty frame for 1.4s -> FIX: drop the show move on r.0. 3. [sc10, 50.2s] caption chunk "Messages So" across a sentence break -> FIX caption_corrections "Messages So" -> "Messages. So".
Checks failed: no empty page (sc10).
Verdict: ANOTHER ROUND

## Round 3
| hook | read | motion | variety | sync | match | min |
|  8   |  8   |   8    |    8    |  8   |   9   |  8  |
Evidence (1s sheet of the final render, out/ios-27-2-beta-3-lint/sheet1s.jpg): hook — frame 0 is the presenter + the real "iOS 27.2 Beta 3" Software Update card + yellow pill; the title row zooms by 2.6s. read — every caption clear of content (sc6 caption raised to 470 for its two-line wrap; lint no blocking flags). motion — spring arrivals, no fades, clips move on their own. variety — 13 scenes, clip/card alternation, longest hold 7.4s on a moving clip. sync — 21 cues, 20 AUDIBLE + 1 UNMASKED, 0 masked; voice on top, -14.5 LUFS. match — each beta-3 change is on a tester's own iPhone (beta 2 beside beta 3) while it is spoken; cards only for timeline and the servers explanation.
Remaining (not blocking): sc3 "4 small changes" pill waits for "four"; the hook card is text-dense even after the zoom.
Checks failed: none (sc3 empty-page fixed: first row now on from frame 0; end card holds 5.1s, reads twice).
Verdict: READY
