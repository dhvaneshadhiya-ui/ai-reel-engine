# apple-reference-image — packaging

Validated with `python3 tools/packaging_check.py apple-reference-image`.

**Every field below is pasted VERBATIM into the place it names.**
There is no assembly step. Instagram has no HASHTAGS field: its
tags go at the END OF THE FIRST COMMENT, because that is where
they are posted. YouTube keeps one, because YouTube reads them
out of the description.

Instagram's hashtag maximum is **5** (past that it ignores all of
them, official since Aug 2025); YouTube's cap is 15 and the
recommended band is **3-5** on both.

`TAGS:` (YouTube only) pastes into Studio's separate **Tags** box under
"Show more" — not the description, not the hashtags. It has no algorithmic
weight on its own since 2021 but still helps YouTube parse misspellings and
close variants of the title; comma-separated, kept under the 500-character
total limit.

## instagram

CAPTION: You can't tell a real photo from an AI fake anymore, so Apple moved the proof to the sensor itself. On the iPhone 18 Pro, Apple Reference Image signs your photo's pixels the instant light hits them, before any software touches them. That signed file goes to Apple's Private Cloud Compute, which checks it and signs the final photo with quantum-resistant encryption. No name, no location, just proof an Apple sensor captured those exact pixels, one Apple can revoke if that sensor is ever compromised. Leica, Sony, Nikon and Google's Pixel use the older standard, which signs a photo after it's processed. Apple signs before any software runs at all. It ships switched off, built for photojournalists and courtrooms, and it can't prove a photo wasn't staged, only that the pixels weren't. The presenter's face and voice in this video are AI-generated.
FIRST COMMENT: Would a signed photo change how much you trust what you see online? #iPhone18Pro #Apple #AI #PhotoVerification
ALT TEXT: Presenter explains Apple's iPhone 18 Pro Reference Image feature, which cryptographically signs a photo at the camera sensor to prove it's real, shown beside Apple's official announcement, Apple's own three-screen Reference Image UI (comparing a press photo to its reference image, which reveals a person cropped out of the final shot), a signing-pipeline diagram, C2PA adopter logos (Leica, Sony, Nikon, Google Pixel), and a critical article questioning the claim.
AI LABEL: on (Advanced settings → Add AI label)

## youtube

TITLE: iPhone 18 Pro Photos Now Sign Themselves to Prove They're Real
CAPTION: You can't tell a real photo from an AI fake anymore, so Apple moved the proof to the sensor itself. Apple's new Reference Image mode, live on the iPhone 18 Pro, signs a photo's pixels the instant light hits the sensor, before any software touches them. That signed file goes to Apple's Private Cloud Compute, which checks it and signs the final photo with encryption strong enough to survive a quantum computer. It carries no name and no location, only proof that a specific Apple sensor captured those exact pixels, proof Apple can revoke if that sensor is ever found compromised. Leica, Sony, Nikon and Google's Pixel already use the existing industry standard, C2PA, which signs a photo after it's already been processed. Apple signs it before any software touches it at all, closing the window where a fake could get swapped in first. It ships switched off by default, built for photojournalists and courtroom evidence rather than everyday shooting. And it's not a perfect fix: critics point out it can only prove the pixels weren't staged, not that the scene in front of the camera wasn't. The presenter's face and voice in this video are AI-generated.
HASHTAGS: #iPhone18Pro #Apple #AI #PhotoVerification #Shorts
TAGS: iPhone 18 Pro, Apple Reference Image, Apple photo verification, AI photo detection, C2PA, photo authenticity, Apple security research, deepfake detection, iPhone camera sensor, Apple Private Cloud Compute, real vs AI photo
ALT TEXT: Presenter explains Apple's iPhone 18 Pro Reference Image feature, which cryptographically signs a photo at the camera sensor to prove it's real, shown beside Apple's official announcement, Apple's own three-screen Reference Image UI (comparing a press photo to its reference image, which reveals a person cropped out of the final shot), a signing-pipeline diagram, C2PA adopter logos (Leica, Sony, Nikon, Google Pixel), and a critical article questioning the claim.
ALTERED CONTENT: yes (YouTube Studio → Altered content → Yes)
