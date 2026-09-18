# Structure — apple-reference-image

Written BEFORE the first sentence. Framework:
`frameworks/shortform-script-framework.md` (S17 shapes; S25 standard).
`script_approval.py propose` refuses while placeholder text remains.

## STORY ENGINE (framework §4A)

A viewer who assumes "a photo is a photo" discovers that on the iPhone 18
Pro, Apple moved the proof of authenticity all the way back to the sensor
itself — the camera signs the pixels before its own software ever sees them
— which matters because AI fakes are now good enough that "I saw the photo"
is stopping being proof of anything, and this is the first real attempt to
put that proof back at the hardware level instead of trusting an app.

## SHAPE (S17)

Explainer (with a News frame on top): open on the actual problem (fakes are
indistinguishable now), reveal the mechanism as the answer, then earn the
ending with the honest limitation. Not a straight news bulletin, because the
"what" (a signed photo) is meaningless to a viewer until they feel the "why"
(they can no longer trust their eyes) — Explainer shape puts the mechanism
in service of that feeling instead of just reporting it happened.

## PROMISE (S2)

By the end, the viewer knows exactly what makes an iPhone 18 Pro's "verified"
photo different from any photo before it — down to the moment in the camera
pipeline where the proof actually gets created — and knows the one thing it
still can't prove.

## OPEN LOOP (S10)

Planted: the hook states a photo now carries proof "before your phone even
finishes taking it" — raising the question of how that's physically possible
when a photo is normally just pixels with no memory of where they came from.
Paid off: the mechanism beat (sensor signs at capture, before firmware,
before Apple's own cloud ever sees a processed image) answers exactly that,
and the ending closes the loop by returning to the hook's claim — "proof,
not a promise" — while being honest about what proof still can't cover.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: the iPhone 18 Pro's camera sensor cryptographically signs pixel data
the moment it's captured, and that signed file is verified and re-signed by
Apple's Private Cloud Compute into a quantum-resistant "reference image."
WHY: because the existing standard (C2PA) only certifies a photo after it's
already been processed — leaving a window where a fake could be inserted
before the certificate is ever attached. Apple is closing that window by
starting the chain of trust at the sensor, before any software runs.
SO WHAT: this is the first mainstream attempt to make "this photo is real"
a hardware-backed claim instead of a software one — useful for journalists
and courtrooms today, and a preview of where phone cameras are headed as AI
image generation keeps getting harder to spot by eye. It is not, and cannot
be, proof that what's IN the photo wasn't staged.

## WHAT WAS CUT (S11, S21)

- The full cryptographic algorithm name (hybrid MLDSA87-RSA-3072-PSS-SHA512)
  — kept as "quantum-resistant encryption," the number of syllables buys
  nothing for a viewer who can't verify it by ear.
- The Secure Enclave Processor / factory key-provisioning detail (how the
  sensor's signing identity is first created in the factory) — real, but a
  second layer of mechanism the hook doesn't need to pay off.
- The 15-minute cryptographic timestamp heartbeat detail — precise but not
  meaning-bearing at this length; "before and after" timestamping is enough
  for the viewer to trust the *when* claim without the *how often*.
- The Oblivious HTTP / no-IP-address privacy detail — true and interesting,
  but a third privacy claim on top of "no name, no location" starts to read
  as a list; cut to keep the privacy line to one clean sentence.
- The vague, unnamed "researcher forged C2PA last month" claim from Android
  Authority — excluded entirely per research.md, since it can't be sourced
  to a name or date.
- iPad/Mac verification-app speculation from the pre-announcement MacRumors
  beta teardown — superseded by Apple's own Sept 16 post, which only confirms
  the iPhone 18 Pro sensor; not carried into the script to avoid stating
  something Apple's own final explainer didn't confirm.

## SOURCES

- https://security.apple.com/blog/apple-reference-image/ (official — primary technical source)
- https://gizmodo.com/apple-explains-how-its-new-iphone-18-photo-verification-actually-works-2000812623 (the exact story the user named)
- https://www.macrumors.com/2026/08/10/ios-27-apple-reference-image/ (pre-announcement beta discovery, context only)
- https://9to5mac.com/2026/08/12/apple-authenticating-iphone-photos-is-just-the-start/ (industry-context corroboration)
- https://www.androidauthority.com/apple-reference-image-vs-android-c2pa-3711734/ (independent comparison table)
- https://www.squaredtech.co/apples-iphone-18-pro-camera-security-claim-needs-proof (critical/skeptical counterweight)
