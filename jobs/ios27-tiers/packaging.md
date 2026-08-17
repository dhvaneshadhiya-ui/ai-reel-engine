# ios27-tiers — packaging

Validated with `python3 tools/packaging_check.py ios27-tiers`.

Two things the checker enforces that the `caption-and-hashtags` skill gets
wrong, so they are worth restating: Instagram's hashtag maximum is **5** (past
that Instagram ignores all of them), and YouTube's *recommended* band is also
**3-5** even though its hard cap is 15. Hashtags live in the FIRST COMMENT, not
the caption — the caption's first line is the only line shown before "more".

`CAPTION:` is one line per platform because that is what the checker parses.
The paste-ready line-broken YouTube description is at the bottom of this file.

## youtube

TITLE: iOS 27 Compatibility: Every iPhone Since 2019 Gets It, Almost None Get Siri AI
CAPTION: Apple dropped zero devices with iOS 27 — iPhone 11 and up, the same list as iOS 26. But "supported" now means three completely different phones, and the split runs straight through a single model year. Only the iPhone 17 Pro, 17 Pro Max and iPhone Air get the full Siri AI. The iPhone 16 line and the 15 Pro get standard Apple Intelligence — the new Siri look, not the whole assistant. From the iPhone 15 down: iOS 27 with no Apple Intelligence at all. Same year, same name, different OS. What everyone does get is the Liquid Glass transparency slider in Settings › Appearance, replacing iOS 26's two options with a continuous dial. And Apple says app launches are up to 30% faster — read the footnote and that figure was measured on an iPhone 11 Pro Max, the oldest phone iOS 27 supports. One catch: Siri AI will not ship in the EU at launch, blocked by the Digital Markets Act. Sources on screen throughout: Apple's own iOS 27 preview and footnotes, Apple Newsroom, MacRumors and 9to5Mac.
HASHTAGS: #iOS27 #iPhone #AppleIntelligence #Shorts
FIRST COMMENT: So which tier does your iPhone land in — full Siri AI, standard Apple Intelligence, or no AI at all?
ALT TEXT: A presenter explains iOS 27's three support tiers beside Apple's own device list and footnotes, with the phrase "iPhone 11 Pro Max" circled in Apple's performance footnote.

## instagram

CAPTION: Every iPhone going back to 2019 gets iOS 27. Almost none of them get the part you've been reading about. Apple dropped zero devices this year — iPhone 11 and up, the same list as iOS 26. But "supported" now means three completely different phones. Only three get the full Siri AI: iPhone 17 Pro, 17 Pro Max and iPhone Air. The 16 line and the 15 Pro get standard Apple Intelligence, which is the new Siri look and not the whole assistant. From the iPhone 15 down, there is no Apple Intelligence at all — so the line cuts straight through one model year. iPhone 15 Pro is in. iPhone 15 is out. Same year, same name, different OS. The part that got buried: everyone gets the Liquid Glass transparency slider, a continuous dial in Settings › Appearance instead of iOS 26's two options. And Apple's own "up to 30% faster app launches" claim? Check the footnote — Apple measured it on an iPhone 11 Pro Max, the oldest phone on the list. One catch: Siri AI will not ship in the EU at launch because of the Digital Markets Act. Every figure in this reel is on screen with its source: Apple's iOS 27 preview and footnotes, Apple Newsroom, MacRumors and 9to5Mac.
HASHTAGS: #iOS27 #iPhone #AppleIntelligence #Apple #iGeeksBlog
FIRST COMMENT: So which tier does your iPhone land in — full Siri AI, standard Apple Intelligence, or no AI at all? #iOS27 #iPhone #AppleIntelligence #Apple #iGeeksBlog
ALT TEXT: A presenter explains iOS 27's three support tiers beside Apple's own device list and footnotes, with the phrase "iPhone 11 Pro Max" circled in Apple's performance footnote.

---

Paste-ready YouTube description, line-broken. Identical copy to CAPTION above;
the checker only reads the single-line version, humans should paste this one.

  Apple dropped zero devices with iOS 27 — iPhone 11 and up, the same list as
  iOS 26. But "supported" now means three completely different phones.

  The three tiers
  • Full Siri AI — iPhone 17 Pro, 17 Pro Max, iPhone Air
  • Standard Apple Intelligence — iPhone 16 line (incl. 16e), 15 Pro, 15 Pro Max
  • iOS 27, no Apple Intelligence — iPhone 15 and older, iPhone SE (2nd gen+)

  The sharpest cut in the lineup is the iPhone 15 and the 15 Pro. Same model
  year, same name, entirely different OS.

  What every supported iPhone gets
  • Liquid Glass transparency slider — Settings › Appearance, a continuous dial
    from ultraclear to fully tinted, replacing iOS 26's two options
  • An optimized CPU scheduler and rebuilt system search
  • Apple says app launches are up to 30% faster — and the footnote shows that
    figure was measured on an iPhone 11 Pro Max, the oldest phone iOS 27 supports

  One regional catch
  Siri AI will not ship in the EU at launch, blocked by the Digital Markets Act.

  Sources, all shown on screen
  Apple's iOS 27 preview and footnotes (apple.com/os/ios) · Apple Newsroom ·
  MacRumors · 9to5Mac

  So which tier does your iPhone land in?

Notes for posting

  Shorts uses a frame from the video rather than a custom thumbnail in most
  surfaces. The strongest still is the Liquid Glass "27" hook at 00:00-00:01
  (it names the subject with sound off) or the three-tier card at ~00:20.

  No comment-keyword CTA: that is a `top5` device per CLAUDE.md, and this is a
  news reel. The CTA is the question, which is also the exact question every
  "iOS 27 is here" piece attracts — so the comments answer it.
