## Round 1
| hook | read | motion | variety | sync | match | min |
|  8   |  6   |   8    |    7    |  8   |   9   |  6  |
Worst three: 1. [07, 36.2-40.5s] text "Each one a tap away in the top bar" sits on top of the caption ("Live" caption runs through it) -> two lines of type collide on a phone -> shot-plan scene 7: clip h 920 -> 760 so the text lands above the caption band. 2. [09, 44.9-47.2s] focus on the custom-feed still crops YouTube's own headline "homepage experience" mid-word at the top edge -> reads as a broken frame -> focus rect [0,480,1080,700] -> [180,470,720,420] (phone top bar only). 3. [05, 24.8-31.4s] bar strip at h 360 leaves ~45% of the page empty until the text lands at 28s -> dead page for 3s mid-reel -> add the old-feed card (h 440) above the bar strip so the old app is on screen while "skipped the algorithm" is said.
Checks failed: empty page (scene 05 until its text arrives). End card holds 5.4s with presenter: ok.
Verdict: ANOTHER ROUND

## Round 2
| hook | read | motion | variety | sync | match | min |
|  8   |  7   |   8    |    8    |  8   |   7   |  7  |
Worst three: 1. [07, 36.2-40.5s] at h 760 the 4:5 clip is cover-cropped in a wide box and the phone's top bar (Live, Music) falls off the top -> the words being said are not on screen (Rule 3) -> new asset yt-topbar-feeds-wide (600x454 around the phone's top bar, scaled to 1080x818) so Live/Music fill the box. 2. [09, 44.9-47.2s] focus still slices YouTube's own title "homepage experience" at the top edge -> broken-looking frame -> new asset yt-custom-feed-ui (the still without its title, 1080x910 @ y 440); rects shifted -440. 3. [05, 24.8-31.4s] fixed from round 1: old feed card + bar strip, no empty band; kept.
Checks failed: none new; scene 07 caption collision fixed in round 1 holds.
Verdict: ANOTHER ROUND

## Round 3
| hook | read | motion | variety | sync | match | min |
|  8   |  8   |   8    |    8    |  8   |   9   |  8  |
Worst three: 1. [02/08/11/12, receipts] TeamYouTube post crops are small type at rest on a phone -> each lands a focus ring + zoom on the exact sentence within ~1s and a headline/row carries the point; kept (they are the official proof). 2. [13, 64.6-70s] end card stops at ~60% height beside the presenter circle -> spotlight is the block's natural size, holds 5.4s with the presenter speaking, readable twice; kept. 3. [09, 44.9-47.2s] fixed: ring on the top bar where the + sits, no edge crop; the full-width ring that crossed the Describe box is gone.
Checks failed: none. 29 SFX cues, 29/29 heard (27 audible over voice, 2 in pauses, 0 masked), -14.5 LUFS, frame-lint no blocking flags, captions clear of content (scene 07 fixed round 1).
Verdict: READY
