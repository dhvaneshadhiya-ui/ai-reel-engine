# Critique — chatgpt-try-on

## Round 1
| hook | read | motion | variety | sync | match | min |
|  6   |  8   |   8    |    6    |  8   |   9   |  6  |
Worst three: 1. [scene 00, 0-1.4s] frame 0 shows OpenAI's whole phone small inside a wide black box; the try-on photo (the subject) is a postage stamp until the first ring -> a thumb sees black, not a person wearing the skirt -> instant focus on the photo region [0,0,1208,1450] at frame 0 (shot-plan scene 00), so the result fills the box from the first frame.  2. [scene 05, 31.5-35.7s] Google's headline card is the only object and stops at 56% (lint LOWER HALF EMPTY) -> half the page is black while the "catching up" line plays -> screen h 560 -> 700.  3. [scene 08, 41-45s] the listing phone runs close to the caption band, and the two-line caption stagger ("the size / chart") brushes it -> phone h 860 -> 800.
Checks failed: no empty page — pass; longest gap scene 03 ~2.2s on the help paragraph (the ring holds on the screenshot line, the text block lands on "ask"); one accent — pass; end card ~5.2s, holds — pass. Variety: phone-listing carries scenes 01/06/08 and help-fit 03/07 — the only official images of the feature that exist (no demo video).
Verdict: ANOTHER ROUND

## Round 2
| hook | read | motion | variety | sync | match | min |
|  7   |  8   |   8    |    6    |  8   |   9   |  6  |
Worst three: 1. [scene 00, 0-1.4s] the round-1 instant focus barely zoomed — a tall rect (1208x1450) in a wide box is limited by width, so the phone stayed small -> rect re-cut to the box's aspect [0,330,1208,845]; frame 0 now opens on the woman wearing the skirt filling the box.  2. [scene 00, 8.7-9.7s; scene 08, 43-45s] the price/size ring's bottom edge ran through "Free delivery · 14-day return" -> reads as a strike-through on the very line the VO points to -> rects end in the gap above the buttons (scene 00 h 560 -> 620; scene 08 return rect 1980/240 -> 2040/250, size rect 300 -> 330).  3. [scenes 01/06/08 + 03/07] two OpenAI images carry five scenes -> accepted: OpenAI published only these stills; each repeat shows a different region (button, size row, return line; screenshot paragraph vs fit paragraph).
Checks failed: none new (Google scene now runs to ~68%; scene 08 clear of the caption band).
Verdict: ANOTHER ROUND

## Round 3
| hook | read | motion | variety | sync | match | min |
|  8   |  8   |   8    |    8    |  8   |   9   |  8  |
Evidence: hook — frame 0 is the presenter circle over OpenAI's try-on result (the woman wearing the skirt) filling the box, "See it on you" with the pill on "wearing" at 1.7s; the ring moves face -> full look -> price/size row on "paying". read — phone sheet: every headline, help-page paragraph, row and step legible; captions in their own band (lint: no blocking flags; hook caption raised to 445 so the word-entry stagger clears 80%). motion — no fades; rings, rows, steps and state crossfades (selfie -> result, Add to -> Library) land on spoken words. variety — 13 scenes: result / listing button / selfie->result / help paragraph / headline + rows / Google headline / result under "Does it fit" / fit paragraph / return line / saved-photos paragraph / settings steps / Favorites sheet->Library / end card. sync — 28 cues, 27 audible + 1 unmasked in a pause (sfx_audibility), -14.6 LUFS, TP -3.6. match — each scene shows its line: the Try on button on "Try on button", the selfie camera on "take or upload a selfie" crossfading to the result on "picture", OpenAI's screenshot paragraph on "Upload a screenshot", the fit paragraph on "doesn't guarantee fit or size", the return line on "return policy", the saved-photos paragraph on "saved", the path steps on "Settings, Personalization, Reference photos".
Worst three (remaining, accepted): 1. [scenes 07-12] lint advises DEAD SPACE 38-58%: the screen box letterboxes portrait phones with black sides -> the lower 20% is caption + platform zone; next reel: a portrait-shaped box for phone stills.  2. [whole reel] 28 cues, one every 2.2s, over G08's 6-9 advice (13 lens-zooms from focus moves) -> all heard, none masked, same density as openai-image-ads; a ring-less focus should not cue — compiler change owed.  3. [scenes 01/08] the listing image appears twice and help-fit twice -> the only official images of the feature; each use frames a different region.
Checks failed: none (no empty page; longest gap scene 03 ~2.2s while the ring holds on the screenshot paragraph; one accent; end card ~5.2s with "Selfie or size chart?" at XL).
Verdict: READY
