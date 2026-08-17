# ios27-tiers — v2, revised against your answers

## What changed

1. **12GB RAM — left out**, as you chose. The script names the three phones.
2. **Regional expanded** from 3 beats to 6 (beats 18–23, ~24s): the EU block,
   the DMA mechanism, Apple's rejected workaround, the Mac/Vision Pro
   inconsistency, "no timeline", and China.
3. **Gemini added** — beats 15–17, corrected (see below).
4. **Adoption added** — beats 29–31, with the day counts stated in-line.
5. **`allowLong: true`** with a written reason. 326 words → **120.7s** at the
   measured 2.7 wps, 127.8s at the conservative 2.55. Ceiling is 180s.

## One correction you should see before approving

Your brief said Siri is *"finally rebuilt on Google's Gemini models."* That
overstates what Apple announced, and I've written the accurate version instead.

MacRumors' architecture piece, from Apple's own WWDC material:

> "The new architecture centers on **Apple Foundation Models co-developed with
> Google**, which Apple says are adapted to run both on-device and on servers
> through its existing **Private Cloud Compute** infrastructure."

So: Apple's own models, developed *with* Google using the technologies behind
Gemini, running on Apple silicon and Apple's servers. Google is not involved in
handling the data. The reel says "co-developed with" and then makes the privacy
point, which is a stronger beat than the licensing framing anyway.

I also **excluded** the "$1 billion a year" and "1.2-trillion-parameter"
figures that circulate with this story. They appear only on low-quality
aggregator sites; MacRumors' piece states no dollar figure and no parameter
count. If you have a primary source for either, I'll add it.

## How the adoption beat handles the window problem

You asked for the 74% vs 76% comparison, and my earlier concern was that it
misleads without the measurement windows. Fixed by putting both numbers in the
same sentence:

> "74% of recent iPhones after 150 days, against 76% for iOS 18 — and iOS 18
> only had 127 days on the clock."

Then beat 31 lands the actual insight, which closes the loop the reel opens at
beat 5:

> "But iOS 26 dropped three phones. iOS 27 drops none. Apple just removed the
> variable."

That is 9to5Mac's own stated factor, and it ties the adoption data straight
back to "Apple dropped zero devices." I think this is now the strongest ending
available — better than the tier recap I had before.

## Still open

1. **Runtime.** 120.7–127.8s. That is the honest cost of the three strands you
   asked to keep. I can cut ~15s by trimming the DMA mechanism (beat 20) and
   the China line (beat 23) if you'd rather land nearer 105s.
2. **Chart values.** Beat 30 renders as a `chart` with three bars — iOS 26 74%
   (150d), iOS 18 76% (127d), iOS 17 76% (139d), column header "% OF iPHONES
   FROM THE LAST 4 YEARS", sourced to 9to5Mac/Apple. Want iOS 17 in, or just
   the two-way comparison?
3. Everything else from v1 stands: no release date, question CTA, and
   CarPlay/parental controls/Cycle Tracking still out.
