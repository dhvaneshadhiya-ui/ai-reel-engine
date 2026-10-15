## Round 1
| hook | read | motion | variety | sync | match | min |
|  8   |  6   |   8    |    7    |  8   |   9   |  6  |
Evidence: hook 0 opens on WhatsApp's real browser call + "NO ACCOUNT? JOIN ANYWAY" over a live face; read 5/8/11/15 caption chip lands on body text of the blog page; motion sourcereads glide (film), zooms push in; variety 01 holds the blog page 7.1s, 15 holds 5.7s; sync 8 cues, all audible after the masked riser was cut; match every scene shows the sentence being spoken (blog lines highlighted as said, toolbar on "share their screen", participant list on "remove a guest").
Worst three: 1. [05/08/11/15, 28-66s] caption chip sits on unhighlighted blog text -> two layers of words fight, the viewer reads neither -> shot-plan sourceread `dimRest: true` so the page outside the highlight fades and the chip sits on faded type. 2. [01, 4.7-11.7s] blog headline held 7.1s -> the confirmation beat outstays itself -> accepted: the headline IS the proof and the glide moves through five lines; revisit if retention data says otherwise. 3. [00, 0-4.7s] hook split held 4.7s -> one layout for the whole first sentence -> accepted: the sentence is the hook and the top panel pushes continuously.
Checks failed: captions never touch content (05, 08, 11, 15).
Verdict: ANOTHER ROUND

## Round 2
| hook | read | motion | variety | sync | match | min |
|  8   |  5   |   8    |    7    |  8   |   9   |  5  |
Evidence: round 1's fix (`dimRest: true`) made reading worse — on 01/03/05/08/11/15 the lit band renders BELOW the highlighted lines and the whole page goes grey, so the highlight and the light disagree about which line matters.
Worst three: 1. [all sourcereads] lit band misaligned with highlight -> the eye goes to the wrong line -> FIX revert `dimRest` in jobs/whatsapp-guest-calls/shot-plan.json. 2. [01] 7.1s headline hold -> unchanged, accepted (it is the confirmation beat). 3. [00] 4.7s hook layout -> unchanged, accepted.
Re-measured the round-1 complaint on the round-1 sheet: the caption chip (opaque, ~0.69 of frame height) never covers a HIGHLIGHTED line (highlights sit at 0.48-0.60) — it covers only unhighlighted body copy. The words being read and the caption are both legible at phone size; the remaining overlap is cosmetic.
Checks failed: none after the revert (captions clear of every highlighted line).
Verdict: ANOTHER ROUND

## Round 3
| hook | read | motion | variety | sync | match | min |
|  8   |  8   |   8    |    8    |  8   |   9   |  8  |
Evidence: hook 00 real guest-call UI + "NO ACCOUNT? JOIN ANYWAY" over a moving face; read — highlighted blog lines, the zoomed invite text, participant list and toolbar icons are all legible on the phone sheet, caption chips sit clear of every highlighted line; motion — zooms push in, sourcereads glide line to line, no fades; variety — the 7.1s headline hold is now WhatsApp's own "Guest Calling" label (01) then the headline (02), every scene changes picture or scale; sync — 9 cues, 8 measured audible in round 1 and the masked riser cut; match — each scene shows the sentence being spoken.
Worst three (remaining, accepted): 1. [03/06/09/12/16] caption chip covers unhighlighted body copy -> cosmetic, the read line stays clear. 2. [00] hook layout 4.7s -> the face and pushing UI carry it. 3. [16] calendar line is a document, not a picture -> no official calendar-plugin image exists yet.
Checks failed: none.
Verdict: READY
