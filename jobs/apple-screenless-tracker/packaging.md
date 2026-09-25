# apple-screenless-tracker — packaging

Validated with `python3 tools/packaging_check.py apple-screenless-tracker`.

**Every field below is pasted VERBATIM into the place it names.**
There is no assembly step. Instagram has no HASHTAGS field: its
tags go at the END OF THE FIRST COMMENT, because that is where
they are posted. YouTube keeps one, because YouTube reads them
out of the description.

Instagram's hashtag maximum is **5** (past that it ignores all of
them, official since Aug 2025); YouTube's cap is 15 and the
recommended band is **3-5** on both.

Single-source story (Bloomberg/Mark Gurman exclusive, verified 2026-09-23
across 6 outlets — see research.md INDEPENDENT-CHECK): every caption below
hedges the project itself ("Bloomberg says", "reportedly") the same way the
script does, and never states the tracker as a confirmed Apple product.

## instagram

CAPTION: Apple just gave the Watch all-day heart tracking. 13 days later, Bloomberg says it's already testing a screenless fitness band: no display, just heart rate, recovery and sleep, the same way Whoop and Oura already do it. Tim Cook and Eddy Cue are reportedly behind it, but Apple hasn't approved anything, and it's not landing before 2028 if it lands at all. The presenter's face and voice in this video are AI-generated.
FIRST COMMENT: Would you actually wear a second wristband with no screen, or is the Watch already enough? #Apple #Whoop #Wearables #TechNews
ALT TEXT: Vertical video explaining Bloomberg's report that Apple is testing a screenless, Whoop-style fitness tracker, with screenshots of the MacRumors and 9to5Mac coverage and product photos of Whoop and Oura.
AI LABEL: on  (Advanced settings → Add AI label; the CAPTION also
 carries: The presenter's face and voice in this video are AI-generated.)

## youtube

TITLE: Apple Is Reportedly Building a Screenless Fitness Tracker
CAPTION: Bloomberg's Mark Gurman reports Apple is testing a screenless, Whoop-style fitness tracker: a thin fabric band with a sensor module and no display, backed by Tim Cook and Eddy Cue. It comes 13 days after Apple gave the Watch all-day heart tracking, which means the sensor was never the real gap. The question is whether people want a screen on their wrist at all, and Whoop ($10B) and Oura ($15.62B IPO) are both betting the answer is no. Apple hasn't approved this, and if it ships, it's not landing before 2028. The presenter's face and voice in this video are AI-generated.
HASHTAGS: #Apple #AppleWatch #Whoop #Wearables #TechNews
ALT TEXT: Vertical video explaining Bloomberg's report that Apple is testing a screenless, Whoop-style fitness tracker, with screenshots of the MacRumors and 9to5Mac coverage and product photos of Whoop and Oura.
ALTERED CONTENT: yes  (YouTube Studio → Altered content → Yes)

---

Paste-ready YouTube description, line-broken. Identical copy to CAPTION above;
the checker only reads the single-line version, humans should paste this one.

  Bloomberg's Mark Gurman reports Apple is testing a screenless,
  Whoop-style fitness tracker: a thin fabric band with a sensor module
  and no display, backed by Tim Cook and Eddy Cue.

  It comes 13 days after Apple gave the Watch all-day heart tracking,
  which means the sensor was never the real gap. The question is
  whether people want a screen on their wrist at all, and Whoop ($10B)
  and Oura ($15.62B IPO) are both betting the answer is no.

  Apple hasn't approved this, and if it ships, it's not landing before
  2028.

  Sources
  Bloomberg (Mark Gurman) · MacRumors · 9to5Mac · TechCrunch · The Globe
  and Mail

  The presenter's face and voice in this video are AI-generated.

  Would you actually wear a second wristband with no screen, or is the
  Watch already enough?

Notes for posting

  Single-source story, spoken hedged throughout ("Bloomberg says",
  "reportedly") — the caption carries that same hedge rather than
  presenting the tracker as a confirmed Apple product. No mockup or
  render of Apple's actual device is shown or implied anywhere in the
  copy or the video; every "screenless band" visual is Whoop's real
  shipping product or a generic stock photo, credited via source_url
  in the manifest, never captioned as Apple's.
