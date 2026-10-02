# Structure — ios27-accessibility-features

Written BEFORE the first sentence. Framework:
`frameworks/shortform-script-framework.md` (S17 shapes; S25 standard).

## STORY ENGINE (framework §4A)

An iPhone owner who skips Accessibility settings because they assume it is
"not for them" discovers that iOS 27 put some of its most useful Apple
Intelligence tricks there (a phone that reads a bill's total, voice commands
in plain words, auto subtitles), plus one that works on any iPhone in 50+
languages, which matters because they can try them tonight, and know which
ones need a 15 Pro or newer.

## SHAPE (S17)

List with a withheld catch. Open on the most concrete demo (Magnifier reading
a bill total) so frame 0 is the payoff, then number it as #1 and run the other
four in order of how many people meet them: voice, photos, your name, video. The
catch (four need an iPhone 15 Pro, two are English-only; Name Recognition is the
exception that runs anywhere) is promised up front and paid at the end, so a list of five equals has a reason to keep going.

## PROMISE (S2)

Five iOS 27 accessibility upgrades worth turning on, and the catch that
covers four of them.

## OPEN LOOP (S10)

Planted: sentence 2, "and four of them come with a catch."
Paid off: "The catch? Name Recognition works on any iPhone with iOS 27. The rest run on Apple Intelligence, so you need an iPhone 15 Pro or later." Then the
narrower catch for two of them (English only, a few countries), then the CTA.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: iOS 27 adds Ask Magnifier, natural-language Voice Control, VoiceOver
image Q&A and generated subtitles, and widens Name Recognition to 50+ languages.
WHY: four run on Apple Intelligence, which is why they need a 15 Pro or later;
Name Recognition does not.
SO WHAT: on an eligible iPhone they are ready to try now; on an older one,
none of them will appear, so don't go looking.

## CONFIRMATION BEAT (2-5s)

Frame 0 to ~4s: Apple's own Magnifier image, the phone on the bill with
"How much is the bill for?", then the answer screen with "$83.89". The viewer
sees the hook happen before item two is named.

## VIEWER QUESTIONS

- Q: Will this work on my iPhone?  A: "Name Recognition works on any iPhone with iOS 27. The rest run on Apple Intelligence, so you need an iPhone 15 Pro or later."
- Q: Does it work in Hindi?  A: "it now works in more than 50 languages, including Hindi"
- Q: Where is the bill feature?  A: "That first one is Magnifier. Tap Ask"
- Q: Do I have to learn Voice Control commands?  A: "Voice Control stops making you memorize button names."
- Q: Why are subtitles showing up on my videos?  A: "videos with no captions now get subtitles on their own"
- Q: Does it work in my language?  A: "Voice Control and the subtitles are English-only, in places like the US and Canada."

## WHAT WAS CUT (S11, S21)

- Accessibility Reader (cleanup, summaries, translation): cut at the user's call 2026-10-02 for Name Recognition. Name Recognition is spoken as an expansion ("now works in"), since it shipped in iOS 26.
- FaceTime sign-language interpreter API: not in iOS 27.0 (first seen in the 27.2 developer beta), developer-only, no app uses it.
- Sony Access controller: press-release claim only, no post-release confirmation.
- Action button shortcut for Live Recognition/Magnifier: disputed (one hands-on says the option never appeared).
- Magnifier's high-contrast mode and spoken zoom: not in Apple's iOS 27 Magnifier guide.
- Settings paths for each feature: true (Apple guides), cut for length; they go in the caption.
- Live Recognition camera Q&A ("which is the plain one?"): folded into VoiceOver; a second VoiceOver item would split one idea in two.

## SOURCES

Apple Newsroom 2026-05-19 (release + media kit), Apple support 149076 (iOS 27
release notes), Apple iPhone User Guide iOS 27 (Magnifier, Voice Control,
VoiceOver recognition, Accessibility Reader, subtitles), apple.com/accessibility,
apple.com/ios/feature-availability, WWDC26 session 256, iDownloadBlog, Tom's
Guide, GeeksModo, Mac Observer, MacRumors, 9to5Mac. BGR = lead only.
Full ledger in research.md.
