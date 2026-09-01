# chatgpt-stickers — packaging

Validated with `python3 tools/packaging_check.py chatgpt-stickers`.

Instagram's hashtag maximum is **5** (past that Instagram ignores all of
them, official since Aug 2025); YouTube's hard cap is 15 but the recommended
band is also **3-5**. Hashtags live in the FIRST COMMENT, not the caption —
the caption's first line is the only line shown before "more".

`CAPTION:` is one line per platform because that is what the checker parses.
The paste-ready line-broken YouTube description is at the bottom of this file.

**The nineteen is the hook.** Every published article on this feature says
eighteen styles. We counted them in the app and put the scroll on screen, so
the correction is the single most shareable thing here and it leads the copy
on both platforms.

## youtube

TITLE: ChatGPT Sticker Packs: One Photo Into 9 WhatsApp Stickers
CAPTION: ChatGPT can now build WhatsApp and iMessage sticker packs natively, and the whole thing runs off one photo. No cutout app, no third-party tool, no manual masking. Open the plus menu, tap Create image, then Stickers. You don't type a prompt — you fill in a sentence: a style, a photo, and the emoji reactions you want. There are nineteen styles, not the eighteen every article reports; I counted every tile in the picker and the scroll is on screen in this video. Pick one and it removes the background for you, so what comes out is a genuine transparent PNG. One generation returns nine stickers, not one. Then Add to chat apps, and choose WhatsApp. The thing that stops most people on their first try: you need at least three stickers before that button will work, and that is WhatsApp's rule for every app that exports to it, not a ChatGPT limitation. Name the pack and it lands in your keyboard. Comment STICKERS and I'll send you the complete setup: the exact style, photo and emoji used here, a prompt you can paste, and all nineteen style names.
HASHTAGS: #ChatGPT #WhatsAppStickers #AITools #StickerPack #TechTips
FIRST COMMENT: Nineteen styles, not eighteen — I counted them in the app. Which one would you make your pack in?
ALT TEXT: A presenter explains ChatGPT's new sticker feature beside iPhone screen recordings showing the Stickers tile, the style picker scrolling all nineteen options, a 3x3 grid of nine stickers of his own face on a transparent checkerboard, and the Add to chat apps export into WhatsApp.

## instagram

CAPTION: Every one of those stickers is my own face, and ChatGPT built all nine from a single photo. No cutout app, no third-party tool — it is already inside the ChatGPT app on your phone. Open the plus menu, tap Create image, then Stickers. You don't type a prompt: you fill in a sentence, choosing a style, a photo and the emoji reactions you want. There are nineteen styles, not the eighteen every article says. I counted every tile in the picker and you can watch the scroll in this reel. Pick one and it cuts the background out for you, so what you get is a real transparent PNG. One generation gives you nine stickers, not one. Then Add to chat apps, choose WhatsApp, name the pack, and it is sitting in your keyboard. The one thing that trips people up on their first go: you need at least three stickers before that button will work, and that is WhatsApp's rule, not ChatGPT's. Comment STICKERS and I'll send you the full setup: the exact style, photo and emoji I used, a prompt you can paste, and the complete list of all nineteen styles.
HASHTAGS: #ChatGPT #WhatsAppStickers #AITools #StickerPack #TechTips
FIRST COMMENT: Nineteen styles, not eighteen — I counted them in the app. Which one would you make your pack in? #ChatGPT #WhatsAppStickers #AITools #StickerPack #TechTips
ALT TEXT: A presenter explains ChatGPT's new sticker feature beside iPhone screen recordings showing the Stickers tile, the style picker scrolling all nineteen options, a 3x3 grid of nine stickers of his own face on a transparent checkerboard, and the Add to chat apps export into WhatsApp.

---

Paste-ready YouTube description, line-broken. Identical copy to CAPTION above;
the checker only reads the single-line version, humans should paste this one.

  ChatGPT can now build WhatsApp and iMessage sticker packs natively, and
  the whole thing runs off one photo. No cutout app, no third-party tool,
  no manual masking.

  The steps

  • Open the plus menu, tap Create image, then Stickers
  • You don't type a prompt — you fill in a sentence: a style, a photo,
    and the emoji reactions you want
  • Pick a style and it removes the background for you, so what comes out
    is a genuine transparent PNG
  • One generation returns nine stickers, not one
  • Add to chat apps → WhatsApp → name the pack

  Nineteen styles, not eighteen

  Every published article on this feature reports eighteen. I counted
  every tile in the picker and there are nineteen — the scroll is on
  screen in this video. The last row holds a single tile on its own,
  which is what an odd number looks like in a two-column grid.

  The rule that stops most people

  You need at least three stickers before the WhatsApp button will work.
  That is Meta's requirement for every app that exports to WhatsApp, not
  a ChatGPT limitation. A pack of nine clears it easily; a single sticker
  will not export.

  Comment STICKERS and I'll send you the complete setup — the exact
  style, photo and emoji used here, a prompt you can paste, and all
  nineteen style names.

  Sources
  Screen recordings of the shipped feature, recorded 1 September 2026 ·
  WhatsApp's own developer documentation for the 3-sticker minimum ·
  OpenAI's announcement, 24 August 2026

Notes for posting

- **Hashtags go in the FIRST COMMENT on Instagram**, not the caption. The
  YouTube description can carry them inline at the end; the checker reads
  them from the HASHTAGS line either way.
- **The CTA is a real promise.** `giveaway.md` is written and published, so
  "Comment STICKERS" is deliverable the moment this goes live. Do not post
  before that page is shared from its own share menu.
- **Do not promise "24 copy-paste prompts"** anywhere. There is one template
  with three dropdowns; the number was dropped from the script for the same
  reason.
- **The nineteen is a correction, not a flex.** If a commenter says their app
  shows a different count, that is worth checking rather than defending —
  the count was read off one build on one day.
