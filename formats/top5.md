# Format: top5

Tips, roundups, "top 5", free-tool reels. The evergreen counterpart to `news`:
these keep earning long after a news reel is dead.

**Numbers:** `python3 tools/reel_gates.py --formats`
**Derived from:** `styles/nick-saraev.md` v2 — 12-reel teardown, 2026-07-24
(full-res detail crops + 8fps motion bursts). Approved as-is by the user
2026-08-12; do not re-derive it without being asked.

Three of its numbers differ from `news` and are the reason this profile
exists: a much shorter runtime, noticeably **quieter** SFX, and a **mandatory**
CTA.

## Structural rule (gate G24 — BLOCKS)

**A CTA scene is required** — `commentcta`, `endquestion` or `instacta`. The
comment-gate CTA is a defining property of the genre, not a garnish: the reel
exists to convert. "Comment WORD and I'll DM the link."

## Script skeleton

1. **HOOK** — "You can now X for free" / "You don't need to pay for X anymore"
   / "here are the top 5 Y you need". **"Free" is the magnet word.**
2. **WHAT IT IS** — one line.
3. **THE LIST** — numbered, First / Then / Next. One item, one card, one
   sentence. Every item earns its slot.
4. **CTA** — the comment gate. Last line, short.

## Scene vocabulary

`categorygrid`, `toolstack`, `carousel`, `checklist`, `logoassemble` for the
items; `deviceframe` or `floatcard` for the tool actually running; `statcard`
when an item has a number worth showing.

## Known gap

**Facecam share is inherited from `news`, not measured for this format.** It
was derived as a general retention rule rather than a genre rule. Measure it
on the first top5 reel and tighten `FORMATS["top5"]["face"]` if it disagrees.
