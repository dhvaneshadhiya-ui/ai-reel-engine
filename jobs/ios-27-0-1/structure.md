# Structure — ios-27-0-1

Written BEFORE the first sentence. Framework:
`frameworks/shortform-script-framework.md` (S17 shapes; S25 standard).

## STORY ENGINE (framework §4A)

An iPhone owner who sees "iOS 27.0.1" in Software Update and assumes it is
a nothing patch for someone else discovers that two of its three fixes are
for iPhone 18 Pro owners only, but the third fixes a touchscreen freeze any
iPhone on iOS 27 can hit, which matters because they now know whether to
update tonight or whenever.

## SHAPE (S17)

List, with a withheld exception. Three fixes in Apple's order, but framed
by WHO they hit: the two 18 Pro fixes first, then the one for everyone
saved for last. A three-line release note is three equal bullets; the
"which one hits me?" question is what carries a viewer to the end, and the
answer is the question every viewer actually has: should I update?

## PROMISE (S2)

What iOS 27.0.1 fixes, which fix affects your iPhone, and whether to update.

## OPEN LOOP (S10)

Planted: hook, "Two only hit one iPhone. The third could hit yours."
Paid off: "Which leaves the one for everyone: pull down Notification Center
and Control Center together..." then the ending answers the question the
hook raised: should YOU update.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: iOS 27.0.1 fixes a Face ID restart and a 2x photo color glitch on the
iPhone 18 Pro, and a Notification Center + Control Center touch freeze on
every iPhone.
WHY: they are the first bugs reported after iOS 27 and the 18 Pro launched;
the Face ID one looked like hardware (people swapped phones) but was software.
SO WHAT: an 18 Pro owner should update today and keep their phone; everyone
else can update whenever, because there are no security fixes in it.

## CONFIRMATION BEAT (2-5s)

Right after the hook: Apple's own iOS 27.0.1 release notes, captured on
mobile from support.apple.com, with the three fix lines on screen, so the
viewer sees the actual document before the first fix is named.

## VIEWER QUESTIONS

- Q: Does this affect my iPhone?  A: "Two only hit one iPhone. The third could hit yours."
- Q: Is my Face ID broken / do I need a replacement?  A: "That was a software bug, so you don't need a new phone."
- Q: Is it a security update, do I need it now?  A: "Apple lists no security fixes, so there's no rush. On an 18 Pro, though, do it today."
- Q: Where do I get it?  A: "It's in Settings, General, Software Update."

## WHAT WAS CUT (S11, S21)

- "Green flare" naming of the photo artifact: Apple says only "color artifact"; outlets connect them. Not said, and no user flare photos.
- NC+CC freeze as a "prank": one outlet's framing.
- The under-display Face ID camera as a cause: speculation.
- Other iOS 27 complaints (indexing battery drain, keyboard lag): not in 27.0.1, would muddy "what's fixed".
- iPadOS/macOS/watchOS/visionOS 27.0.1 and iOS 26.7.1: different viewer.
- Build number 24A446: nobody asks.

## SOURCES

Apple Support 149076 (release notes), Apple Support 100100 (security
releases: no CVEs), Apple Support 118575 (how to update), MacRumors,
9to5Mac, The Apple Post, iDrop News, PhotographyTalk, Gizbot (contradiction
check). Full ledger in research.md.
