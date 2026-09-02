# Open questions — apple-trade-in-value

1. **US figures, global audience.** Every number is from Apple's US page and
   the script says "On Apple's US page" out loud. Your audience is not all US.
   Options: leave it (honest, and the *lesson* travels — every market's page
   uses the same "Up to" framing), or reshoot the captures on Apple India and
   quote rupees instead. I went with the US page because that is where the
   $40-$720 headline exists; I could not verify the equivalent Indian range.

2. **The CTA promises a reply.** "Comment TRADE with your model and I'll tell
   you what it tops out at." That is deliverable — the values are on the page —
   but it is a commitment to actually answer comments. Say if you would rather
   it be a plain follow/save CTA.

3. **The hook has no time anchor.** The framework flags that the opening does
   not say WHEN. Trade-in values change, so "Apple says" could go stale.
   I left it because adding "right now" costs a beat and the reel is dense
   already. Happy to add it.

4. **Is this a how-to or a warning?** I wrote it as the tutorial shape — the
   correction arrives as the step people skip, not as an accusation, because
   Apple's disclaimer is right there on the page and there is no villain.
   If you want it sharper/more confrontational, that is a different cut and
   I would rewrite rather than tweak.

5. **Should you be on camera at all?** The 7-reel teardown found three of seven
   how-to reels carry NO presenter, and the `howto` profile floors facecam at
   0% for that reason. This reel is entirely screen evidence, so it works
   faceless — but every other iGeeksBlog reel is presenter-led, so going
   faceless is a channel decision, not a format one. My default: presenter on
   the CTA only (~15%), which keeps the face on the ask and gives the whole
   middle to the page. Say if you want a normal presenter open too.

6. **Platform: YouTube Shorts.** The CTA now points at the description, where
   Apple's full 32-model list is linked, because a YouTube description carries
   a real clickable link. The India cut cannot do this and asks for a comment
   instead. Nothing else about the render changes: `SAFE_RECT` in
   `src/platformSafeArea.ts` is deliberately the INTERSECTION of both
   platforms' overlays ("the rect below clears both"), so one geometry is
   already correct for either. I did not add a platform switch to the
   renderer, because there is nothing for it to switch.
