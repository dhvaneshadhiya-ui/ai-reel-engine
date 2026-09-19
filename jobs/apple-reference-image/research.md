# Research — apple-reference-image

Claims ledger + search log. `script_approval.py propose` refuses
while placeholder text remains; format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: On iPhone 18 Pro and Pro Max, the camera sensor itself cryptographically signs the pixel data the instant it is captured, before the sensor's own firmware can alter it — this is the core mechanism of "Apple Reference Image" (ARI).
  TIER: official
  SPOKEN: "the sensor signs the pixels the instant light hits it, before anything else can touch them"
  SRC: https://security.apple.com/blog/apple-reference-image/
  VIA: Apple Security Research (Apple's own engineering blog)

- CLAIM: That signed "digital negative" is uploaded to Apple's Private Cloud Compute, which verifies the signatures, checks the raw image against expected physical characteristics, then does the normal processing (demosaicing, tone mapping, compression) and issues a final reference image with a quantum-resistant composite signature (hybrid RSA-3072 + ML-DSA-87).
  TIER: official
  SPOKEN: "that signed file goes to Apple's Private Cloud Compute, which checks it and signs the final photo with encryption strong enough to survive quantum computers"
  SRC: https://security.apple.com/blog/apple-reference-image/
  VIA: Apple Security Research

- CLAIM: Apple's stated reason for not using the existing C2PA standard (used by Leica, Sony, Nikon, Google Pixel 10, and adopted by OpenAI) is that C2PA attaches provenance metadata AFTER capture, leaving a window where a photo could be altered before it's certified — Apple signs at the sensor before any software runs.
  TIER: multi
  SPOKEN: "It signs a photo after it's already been processed. Apple signs it before any software touches it at all"
  SRC: https://security.apple.com/blog/apple-reference-image/
  SRC: https://www.androidauthority.com/apple-reference-image-vs-android-c2pa-3711734/
  VIA: Apple's own engineering blog (primary technical claim)
  VIA: Android Authority's own independently-built comparison table

- CLAIM: The reference image carries no photographer identity, no device IP address (timestamping uses Oblivious HTTP), and no location data — only cryptographic proof that a specific model of Apple sensor captured those exact pixels, with a revocation list Apple can use to invalidate images from a sensor later found compromised.
  TIER: official
  SPOKEN: "it doesn't carry your name or your location — only proof that an Apple sensor captured those exact pixels, one Apple can revoke if that sensor is ever compromised"
  SRC: https://security.apple.com/blog/apple-reference-image/
  VIA: Apple Security Research

- CLAIM: Reference mode is opt-in and off by default, aimed at photographers, journalists, and people who need to prove a photo in a legal proceeding — not everyday shooting.
  TIER: multi
  SPOKEN: "it comes switched off, built for photojournalists and courtrooms, not your everyday shot"
  SRC: https://www.macrumors.com/2026/08/10/ios-27-apple-reference-image/
  SRC: https://www.idropnews.com/iphone-18-pro/apple-reference-image-iphone-18-pro-photo-verification/268576/
  VIA: MacRumors' own iOS 27 beta teardown
  VIA: idropnews' own independent reporting

- CLAIM: Proving a photo came from an unaltered Apple sensor is not the same as proving the scene in it wasn't staged or misleading — the guarantee is scoped to pixel/sensor authenticity, not scene truthfulness.
  TIER: official
  SPOKEN: "it can't tell you the photo wasn't staged, only that the pixels weren't"
  SRC: https://security.apple.com/blog/apple-reference-image/
  SRC: https://www.squaredtech.co/apples-iphone-18-pro-camera-security-claim-needs-proof
  VIA: Apple's own scope statement — Apple Security Research's post defines the guarantee narrowly as "a real photograph, captured by a real sensor in an iPhone camera, at a specific time," explicitly not a claim about the scene itself; a perfectly staged or misleading scene photographed with Reference mode would still produce a valid, verified reference image. Verified directly via fact-check-workflow on 2026-09-18 by re-reading Apple's own post for its scope language.
  VIA: SquaredTech's independent framing of the same limitation ("provenance can help, but it cannot settle truth")

- CLAIM: The C2PA standard Apple is bypassing is already used by Leica, Sony, Nikon, and Google's Pixel phones.
  TIER: multi
  SPOKEN: "Leica, Sony, Nikon, and Google's Pixel use the existing standard"
  SRC: https://www.macrumors.com/2026/08/10/ios-27-apple-reference-image/
  SRC: https://www.androidauthority.com/apple-reference-image-vs-android-c2pa-3711734/
  VIA: MacRumors' own reporting
  VIA: Android Authority's own independently-built comparison table
  NOTE: an earlier draft of this claim cited "500 companies" from squaredtech.co; that figure could not be
  independently corroborated (a search turned up a "6,000+ members" figure from Jan 2026 instead, itself
  not traceable to a primary C2PA count page), so it was dropped in favor of the named-adopters claim above,
  which IS independently corroborated.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-18  "iPhone 18 photo verification Apple Content Credentials"  (found Apple's own Sept 16 2026 Security Research post, "Apple Reference Image: A New Approach for Verified Photography," the primary source for the whole reel)
- 2026-09-18  fetched security.apple.com/blog/apple-reference-image/ directly  (full technical mechanism: sensor signing, PCC pipeline, hybrid RSA-3072/ML-DSA-87 signature, revocation list, opt-in status, what data is/isn't included)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-18  "Apple Reference Image criticism security researchers reaction"  (ETH Zurich researcher Fernando Cardes assessed the sensor-signing approach as making mass forgery "practically impossible" without a costly physical chip attack — independent technical read, not Apple's own framing)
- 2026-09-18  fetched androidauthority.com's Apple-vs-Android comparison  (independent side-by-side table of ARI vs C2PA; confirms timing-of-signature and privacy differences Apple claims; the piece's own "researcher forged C2PA last month" claim is unnamed/undated and was NOT used as a spoken claim in this reel for that reason)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-18  "Apple Reference Image criticism security researchers reaction"  (this is a Sept-16-2026 feature with no consumer install base yet — it targets photojournalists/legal use, not a general shipped-and-used-by-crowds feature. No first-person "I used it" reaction exists yet; noted as a limitation of the story's freshness, not skipped)
- N/A beyond the above — feature is two days old at research time (announced 2026-09-15/16, researched 2026-09-18); there is no consumer usage corpus yet to sample. This is itself worth a line in the script (framed honestly as "just landed," not as "everyone's using it").

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-18  fetched squaredtech.co's skeptical op-ed  (argues Apple hasn't "shown its work" comparing itself to a non-monolithic "Android," that C2PA/provenance was never designed to prove a scene's truth only its chain of custody, and that Apple's closed system risks becoming a "blue-bubble" for photos with no interoperability — used as the script's honest hedge line)

INDEPENDENT-CHECK: 2026-09-18 searched for security-researcher reaction, hands-on testing, and critical commentary beyond Apple's own post — found ETH Zurich's Fernando Cardes assessing the sensor-signing design (independent technical validation) and SquaredTech's critical op-ed (independent skepticism about the marketing framing and the "provenance isn't truth" limitation). Both are used in the script/structure as the honesty counterweight to Apple's own claims. The one unnamed/undated claim found (a researcher allegedly forging C2PA "last month") was deliberately NOT used as a spoken fact because it can't be sourced to a name, date, or writeup — noted here so it isn't silently reintroduced later.
