
## Round 1
| hook | read | motion | variety | sync | match | min |
|  8   |  7   |   8    |    7    |  8   |   7   |  7  |
Worst three: 1. [scene 04, 22.4s] the chart demo spends ~2s on the creator's own zoom transitions and a dark loading screen; the chart itself flashes for 0.4s -> the viewer never sees the thing the line names -> FIX: rebuild arg-chart.mp4 as chart frame held 2.3s with a slow push, then the prompt (13.2-14.2s), then the answer (16.3-17.8s, 1.67x slow).  2. [scene 06, 31.5s] end card holds 2.48s -> the question can't be read twice -> FIX: pad 1.0s of silence on the end of vo.mp3 so the card holds 3.48s.  3. [scene 02, 8.5s] (fixed before this round) the Google page rendered as an unreadable strip -> now two crops, headline then the Pro/Ultra paragraph on "Pro".
Checks failed: end card hold (2.48s)
Verdict: ANOTHER ROUND

## Round 2
| hook | read | motion | variety | sync | match | min |
|  8   |  7   |   8    |    8    |  8   |   9   |  7  |
Worst three: 1. [scene 05, 29s] the shot-list clip (h 900) runs down to the caption — "scripts." sits on its bottom edge -> content touching captions reads as clutter and hides the table's last row -> FIX: shot-plan h 900 -> 790.  2. [scene 01, 6s] same on the phone clip (h 900) -> FIX h 790.  3. [scene 03, 18s] 3D clip (h 860) bottom meets "room." -> FIX h 790.
Checks failed: captions touch content (scenes 01, 03, 05)
Verdict: ANOTHER ROUND

## Round 3
| hook | read | motion | variety | sync | match | min |
|  8   |  8   |   8    |    8    |  8   |   9   |  8  |
Evidence: hook — frame 0 is the Gemini app on a phone in hand under "Google's most powerful Gemini yet", the pill landing on "powerful" (scene 00). read — every clip now ends clear of the caption chip (scenes 01, 03, 05 at h 790); Google's post is two tight crops, headline then the Pro/Ultra paragraph, both readable at phone size; lint clean. motion — every scene is moving screen recording; the chart hold has a slow push; headlines and pills spring in. variety — phone / page / 3D render / chart / prompt / table / end card, a new picture every 3-7s, no clip repeated except the 3D room returning on the end card. sync — sfx_audibility 11 of 11 audible, 0 masked; music ducked from the voice; -14.4 LUFS. match — every demo is on screen while it is described (3D prompt and spinning room on "3D floor plan… spin around", chart then answer on "chart of LA electricity prices… cheapest hours", script PDFs and shot table on "three video scripts").
Worst three (remaining, accepted): 1. [scene 00] the hook clip is 2.4s of footage slowed 2.25x; the handheld motion reads slightly floaty. 2. G04 advice on overlay holds of 2-4s: the footage under them moves the whole time. 3. Creator's "One prompt → an interactive 3D room" label stays on the 3D shot (approved by the user).
Checks failed: none
Verdict: READY
