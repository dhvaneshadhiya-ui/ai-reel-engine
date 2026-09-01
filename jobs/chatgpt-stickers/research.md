# Research — chatgpt-stickers

Claims ledger + search log. Two independent origins behind the load-bearing
claims: OpenAI's own announcement (24 Aug 2026) and hands-on testing — both
9to5Mac's and, for the details the press got wrong or never counted, our own
screen recordings of the shipped feature (2026-09-01, three iPhone captures,
originals in `_sources/chatgpt-stickers/`).

Where own testing and press coverage disagree, own testing wins and the
disagreement is recorded. That happened once: every outlet that names a
style count says 18. The app shows 19.

## CLAIMS

- CLAIM: ChatGPT makes sticker packs natively, with no third-party sticker
  app and no manual cutting out; free, on mobile, rolled out 24 Aug 2026.
  TIER: official
  SPOKEN: "No cutting anything out, no third-party app. It's already inside ChatGPT."
  SRC: https://x.com/ChatGPT/status/2091996384954069032
  VIA: OpenAI's own announcement post
  SRC: https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
  VIA: 9to5Mac hands-on testing

- CLAIM: The entry path on the shipped iOS build is the composer's plus menu
  -> Plugins -> Create image -> the Stickers tile. (Press describes a sidebar
  -> Images -> Stickers route; the build we recorded routes through the plus
  menu. We say what we show.)
  TIER: official
  SPOKEN: "It starts on the chat screen. Plus menu, Create image, then Stickers."
  SRC: https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
  VIA: own testing — ChatGPT Video 2.mov, 2026-09-01, frames at 1.5s (plus
       menu), 2.5s (Plugins list), 4.5s (Create an image panel, Stickers tile)

- CLAIM: Sticker creation is driven by a fill-in-the-blanks template
  ("Create a [style] sticker pack based on [photo], remixing with [emoji]."),
  three dropdowns, not a free-text prompt box.
  TIER: official
  SPOKEN: "There's no prompt box. You fill in a sentence: style, photo, reactions."
  SRC: https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
  VIA: own testing — ChatGPT Video 1.mov and Video 2.mov, template visible
       throughout both

- CLAIM: The style picker offers NINETEEN styles: 3D, Hand-drawn, Chibi,
  Meme, Holographic, Chrome, Comic Book, Anime, Clay, Pixel Art, Kawaii,
  Retro, Watercolor, Minimal, Riso Print, Paper Cut, Embroidered, Graffiti,
  Traditional Tattoo. Press coverage that names a number says 18 and is
  wrong; the final row holds a single orphan tile, which is what an odd
  count looks like in a two-column grid.
  TIER: official
  SPOKEN: "Nineteen: 3D, Anime, Chrome, Pixel Art, Traditional Tattoo."
  SRC: https://x.com/ChatGPT/status/2091996384954069032
  VIA: own testing — ChatGPT Video 1.mov, all 19 tiles counted across the
       full scroll (frames at 3.0s, 4.0s, 4.5s, 5.0s, 6.0s)

- CLAIM: Output carries a genuinely transparent background, cut automatically,
  with no manual masking step.
  TIER: official
  SPOKEN: "Pick one and it cuts the background out for you, the step that used to need a separate app."
  SRC: https://x.com/ChatGPT/status/2091996384954069032
  VIA: OpenAI's own announcement post ("now with transparent backgrounds")
  SRC: https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
  VIA: 9to5Mac hands-on testing

- CLAIM: One generation returns nine stickers, laid out as a 3x3 grid.
  TIER: multi
  SPOKEN: "Nine, same face, nine reactions."
  SRC: https://www.storyboard18.com/digital/chatgpt-gets-custom-stickers-feature-powered-by-images-2-0-108697.htm
  VIA: OpenAI's own announcement post
  SRC: https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
  VIA: own testing — ChatGPT Video 3.mov, 3x3 grid rendered at 11.5-13.5s

- CLAIM: Export runs through an "Add to chat apps" button offering iMessage,
  WhatsApp and Save to photos, then a "Name your sticker pack" dialog.
  TIER: official
  SPOKEN: "Then Add to chat apps, choose WhatsApp."
  SRC: https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
  VIA: own testing — ChatGPT Video 3.mov, export menu at 14.0-15.5s, naming
       dialog at 16.5-17.6s

- CLAIM: A WhatsApp sticker pack must contain at least 3 and at most 30
  stickers. This is Meta's requirement on every app that exports to WhatsApp,
  not a ChatGPT limitation.
  TIER: official
  SPOKEN: "You need at least three for that button to work. That's WhatsApp's rule, not ChatGPT's."
  SRC: https://github.com/WhatsApp/stickers/blob/main/Android/README.md
  VIA: WhatsApp's own developer documentation (primary)
  SRC: https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
  VIA: 9to5Mac hands-on testing

## SEARCHED

- 2026-09-01  "ChatGPT stickers feature create sticker packs images sidebar"  (established the feature is real, shipped 2026-08-24, and the Images -> Stickers entry point)
- 2026-09-01  "OpenAI ChatGPT sticker maker \"Add to Chat Apps\" WhatsApp export"  (settled the export button label and its three targets; first sighting of the 3-sticker rule as Meta's)
- 2026-09-01  "WhatsApp sticker pack minimum 3 stickers requirement third party apps"  (traced the 3-minimum to WhatsApp's own developer repo — min 3, max 30 — rather than to coverage)
- 2026-09-01  "ChatGPT stickers \"18 styles\" OR \"18 aesthetics\" holographic anime 3D style list"  (found the 18 figure carried only by outlets that did not test it; no outlet lists the styles by name — flagged for in-app verification, which then showed 19)
- 2026-09-01  "openai.com release notes ChatGPT stickers August 2026 images transparent backgrounds announcement"  (confirmed free / mobile / global and the transparent-background claim at OpenAI's own post; help.openai.com returned 403)
- 2026-09-01  own testing: three iPhone screen recordings supplied by the user, frame-read at 1fps plus full-res crops. Settled the entry path, the template shape, the 19-style count and every export step.

## ONE-SOURCE-OK

Not needed — every claim carries two independent origins except the entry
path and the template shape, which are corroborated by 9to5Mac's hands-on
plus our own recording of the same screens.
