# ChatGPT Sticker Packs — the complete setup

Deliverable for comment keyword **STICKERS** (reel: `chatgpt-stickers`).

Everything here is taken from the actual session in the screen recordings
(2026-09-01). Where something could not be read off the screen, it says so
rather than guessing.

---

## What you need

- The **ChatGPT app on your phone**. Not the website — this is mobile only.
- **Free account works.** No Plus required.
- **One photo.** A clear, well-lit face shot works best. It can be you, a
  friend, or a pet.

---

## The seven steps

1. Open ChatGPT and tap the **`+`** next to the message box.
2. Tap **Plugins**, then **Create image**.
3. On the *Create an image* panel, tap the **Stickers** tile.
4. You get a fill-in-the-blanks sentence, not a prompt box:

   > Create a **`[style]`** sticker pack based on **`[photo]`**, remixing with **`[emoji]`**.

   Tap each underlined part in turn.
5. Tap the style slot to open **Choose a style**, and scroll. There are
   nineteen (full list below).
6. Tap the photo slot, pick your image. Tap the emoji slot, pick a few that
   match the moods you want.
7. Tap **Generate**. You get **nine stickers** in a 3×3 grid on a transparent
   background.

Then: **Add to chat apps** → **WhatsApp** → **name your pack** → **Add to
WhatsApp**. It lands in your sticker keyboard.

---

## The exact settings used in the video

Read directly off the screen:

| Slot | Value |
|---|---|
| Style | **3D** |
| Photo | one portrait, upper body, plain indoor background |
| Emoji | **🤟 🧩 🌹 💥** |

The emoji are doing more work than they look like they are. They are not
decoration — each one steers a different reaction in the finished pack. 🤟
produced the confident/thumbs-style poses, 💥 produced the WOW and HA HA
comic bursts, 🌹 produced the offering-a-rose sticker.

**Pick emoji for the range of moods you want, not for how they look.**

### The generated prompt

When you tap Generate, ChatGPT expands that sentence into a full prompt and
sends it. The part visible in the recording reads:

> "…expression, pose, or reaction. Separate the stickers with wide, fully
> transparent gaps. No background, shadows, or overlapping elements."

The opening of that prompt scrolled off screen before it was captured, so it
is not reproduced here.

### A reusable version

If you would rather type it yourself instead of using the template — this one
is written to match what the template produces, it is not a transcript of it:

```
Create a 3D sticker pack based on this photo. Nine stickers in a 3x3 grid,
each showing a different expression, pose, or reaction. Separate the stickers
with wide, fully transparent gaps. No background, shadows, or overlapping
elements.
```

Swap `3D` for any style below.

---

## All nineteen styles

Counted in the app. Most articles say eighteen; the picker's last row holds a
single tile on its own, which is what an odd number looks like in a
two-column grid.

3D · Hand-drawn · Chibi · Meme · Holographic · Chrome · Comic Book · Anime ·
Clay · Pixel Art · Kawaii · Retro · Watercolor · Minimal · Riso Print ·
Paper Cut · Embroidered · Graffiti · Traditional Tattoo

**Which to pick:** 3D and Clay hold a face best. Chibi and Kawaii push toward
cartoon and lose likeness. Meme is the one that actually produces reaction
stickers. Holographic and Chrome look great standing alone and read poorly at
sticker size in a chat.

---

## The rules that trip people up

- **You need at least three stickers to export to WhatsApp.** This is Meta's
  rule for every app that exports to WhatsApp, not a ChatGPT limit. A pack of
  nine clears it easily; a single sticker will not export.
- **A WhatsApp pack maxes out at 30.** One generation gives you nine, so this
  never binds unless you are combining packs.
- **Export targets are iMessage, WhatsApp and Save to photos.** Those three.
- **Name the pack when asked.** That name is what shows in WhatsApp when you
  use or share it, so it is worth a moment.

---

## If it goes wrong

- **Background isn't transparent.** Say "make the background fully
  transparent" and regenerate. The checkerboard pattern behind the stickers
  is how you confirm it worked.
- **Stickers are touching or overlapping.** That is what "wide, fully
  transparent gaps" in the prompt is there to prevent. Add it and regenerate.
- **It doesn't look like the person.** Use a sharper, better-lit, front-facing
  photo, and move toward 3D or Clay. Heavily stylised options are supposed to
  drift.
- **No Stickers tile.** Update the app. It rolled out 24 August 2026.

---

## Sources

- OpenAI's announcement, 24 August 2026 — https://x.com/ChatGPT/status/2091996384954069032
- 9to5Mac hands-on — https://9to5mac.com/2026/08/24/chatgpt-now-lets-users-create-custom-imessage-and-whatsapp-stickers/
- WhatsApp's own developer documentation, for the 3-minimum / 30-maximum —
  https://github.com/WhatsApp/stickers/blob/main/Android/README.md
- The nineteen-style list and the exact settings: counted and read off our own
  screen recordings, 2026-09-01.
