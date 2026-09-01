# AutoDM — chatgpt-stickers (SuperProfile)

Structure follows the user's own SuperProfile pattern (supplied 2026-09-01 as a
worked example from the Mac-control-panel reel). Adapted, not copied — the two
reels differ in one important way, noted under DIFFERENCES.

## Trigger

Primary keyword: **`STICKERS`** — it is exactly what the reel says.

Variations to add if SuperProfile accepts multiple:

- `STICKERS`
- `stickers`
- `STICKER`
- `sticker pack`

**Do NOT add `GUIDE` or `LINK`.** They are not what the reel asks for, and
broad words fire on comments that were never a request.

**Matching caveat, worth checking in-product.** If SuperProfile matches on
*contains* rather than *exact*, `STICKERS` will also fire on "love these
stickers" and "need these stickers". The blast radius is small — someone gets
a free guide they did not ask for — but if there is an exact-match toggle,
turn it on. The same trap applies to short keywords generally: `APP` fires on
"great app!".

## Auto-reply to the comment

Short, and **no link** — the whole point is to move it into DM.

Rotate 3-4 so every comment does not get a byte-identical reply, which is the
pattern that reads as spam:

- Sent it to your DMs! 👀
- Just DM'd you 📩
- Check your messages 👀
- On its way 📩

## DM 1 — plain text version

    Here you go! 👇

    The full setup for the ChatGPT sticker packs from the Reel — the exact
    style, photo and emoji I used, a prompt you can paste, and all nineteen
    style names.

    📱 Open on your phone: [GUIDE LINK]

    Two things that trip people up:
    • Stickers is mobile only — it won't appear in ChatGPT on desktop
    • WhatsApp needs at least 3 stickers before it will export. A pack of
      nine clears that easily.

    If you make a pack, reply and show me! 👀

## DM 1 — button version (use this if SuperProfile supports buttons)

    You asked for the sticker setup from the Reel 👇

    One photo into nine WhatsApp stickers, inside ChatGPT. No cutout app,
    no third-party tool.

    Heads up: Stickers is mobile only, and WhatsApp needs at least three
    before it will let you export.

    [ Get the Guide ]   -> guide link
    [ Watch the Reel ]  -> reel permalink (optional)

## THE DEAD-END RULE — carried over from the user's example

The Mac reel sent BOTH the iPhone and Mac links, because sending only one
leaves the viewer installing it and then wondering why nothing works.

The same principle here, and it is the single most important line in the DM:

- **Mobile only.** Someone who opens the guide on a laptop, goes to ChatGPT
  on the web and finds no Stickers tile will conclude the reel was wrong.
- **The three-sticker minimum.** Someone who generates and then tries to
  export a single sticker hits a dead stop with no explanation.

Both are already in the guide, but the DM must carry them too — people act on
the DM before they read the PDF.

## DIFFERENCES from the supplied example — do not copy these across

**There is no withheld reveal target in this reel.** The Mac reel deliberately
concealed the app name and used the DM to reveal it, which is a real
retention device. This reel names ChatGPT in the first ten seconds and shows
the UI throughout; `brief.json` records `reveal_target: none` and
`framework_check` passes on reveal handling. So the DM has nothing to unveil —
its job is delivery, not revelation. Writing it as a big reveal would promise
a surprise that never arrives.

**Only one link, not two.** The Mac reel needed a pair because the product
needs a pair. Here the whole thing happens inside one app the viewer already
has, so a second link would be padding.

## Before this can go live

1. The guide must be reachable. Either share the artifact from its own share
   menu, or (better) upload `ChatGPT-Sticker-Packs-Guide.pdf` to SuperProfile
   as a free digital product and use that link — it keeps the audience on the
   user's own funnel and enables email capture.
2. Connect Instagram as a **Professional** account (Business or Creator).
   The messaging API does not work on a personal account.
3. Test from a second account before the reel is promoted.
4. Watch the first hour by hand for false keyword matches.

## Cost

Comment-triggered DMs on posts and reels are unlimited on SuperProfile's free
tier. Story/Live triggers, "Ask for a Follow to Get DM", and email capture are
the $29/month plan.

**Skip "Ask for a Follow" on this campaign.** Gating a promised deliverable
behind a follow sours an exchange the viewer already completed by commenting.
