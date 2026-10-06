# Critique — openai-image-ads

## Round 1
| hook | read | motion | variety | sync | match | min |
|  6   |  6   |   7    |    7    |  7   |   8   |  6  |
Worst three: 1. [scenes 00-01, 0-17s] focus rects on the mockup were narrow (230-420px wide) so the zoom sliced the ad card mid-word ("eas", "dinner") -> the hook proof reads as broken -> widened every mockup rect to the full 840px width (shot-plan scenes 00/01/03).  2. [scenes 00-01] mockup at h 860/900 pushed captions to 80-81% -> lint [PLATFORM ZONE] blocked -> h 700/760 and scene 01 captionBottom 440.  3. [scene 05, ~33s] the focus ring's edge ran THROUGH a line of the OpenAI paragraph -> looked like a strike-through on the very promise being quoted -> rects re-derived from measured line gaps (labeled 205-287, separate 290-375, answers 375-625).
Checks failed: no empty page (scene 02 opened on bare background for ~1.5s, row now shows on "reaches"); captions touched content (scene 00 caption at 81%).
Verdict: ANOTHER ROUND

## Round 2
| hook | read | motion | variety | sync | match | min |
|  7   |  7   |   8    |    7    |  8   |   9   |  7  |
Worst three: 1. [scene 02, 13-19s] the OpenAI mark rendered black on a black tile -> the only brand anchor in the reel was invisible -> built openai-tile-light.svg (official paths, white tile, black mark).  2. [scenes 04 + 07] step strips at h 620/640 filled a third of the frame, 52-63% dead space -> h 800.  3. [scene 09, 55-58s] the payoff card was two rows on an empty page -> added OpenAI's own ad mockup under the rows, landing on "ads come with them".
Checks failed: scene 07 strip at h 900 touched the caption -> settled at 800.
Verdict: ANOTHER ROUND

## Round 3
| hook | read | motion | variety | sync | match | min |
|  8   |  8   |   8    |    8    |  8   |   9   |  8  |
Evidence: hook — frame 0 is the presenter circle over OpenAI's own example screen, "An ad while your image loads", pill lands on "ads" at 1.8s, ring moves 62% -> ad card. read — phone sheet: every headline, row, step and swap legible; captions in their own band (lint: no blocking flags). motion — no fades; rows, steps, swap sides and rings arrive on spoken words; spotlight lands with a burst. variety — 11 scenes: mockup / mockup walk / logo spotlight + rows / carousel mockup / steps / announcement receipt / help receipt + swap / steps / help receipt / rows + mockup / end card. sync — 28 cues, 28/28 AUDIBLE (sfx_audibility), -14.6 LUFS, TP -3.7. match — each scene shows its line: the 62% loading image on "still loading", the ad card on "grocery ad", OpenAI's paragraph on "labeled", the plans line on "Plus, Pro, Business", the Ads-Free paragraph on "messages, and image generation".
Worst three (remaining, accepted): 1. [scenes 02, 06, 09] lint advises DEAD SPACE 46-60% under rows/swap cards -> the lower band is the caption + platform zone; next reel: give card scenes a second visual.  2. [scenes 00, 01, 03, 09, 10] the one OpenAI mockup carries five scenes -> it is the only image of the format that exists; nobody has seen a live ad yet (test starts later this month).  3. [whole reel] 28 sound cues, one every 2.3s, over G08's 6-9 advice -> all audible and none masked, but busier than the house norm; slideSfx left on per the ios-27-2-beta-3 note.
Checks failed: none (no empty page; longest gap scene 06 ~2.9s while the help-page ring holds on the plans line; one accent; end card holds ~3.8s with "Pay to skip them?" at XL).
Verdict: READY
