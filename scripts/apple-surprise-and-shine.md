# apple-surprise-and-shine — script + beat map

**Canonical script:** `jobs/apple-surprise-and-shine/script.md` (read by
`script_approval.py` / `research_check.py`). This file mirrors it plus
carries the beat map and build notes.

**Format:** news · **Style:** editorial
**Look:** f55b0b7c (digital twin, neutral) · **Measured:** 204 words → ~76s at 2.7 wps (band 60-80s)
**Refs:** MacRumors 2026-08-26 (Juli Clover) · 9to5Mac 2026-08-26 (Zac Hall) · AppleInsider 2026-08-26 (Malcolm Owen) · Apple Newsroom 2026-04-20 (official)

## Script (spoken narration)

On September 9th, the person walking out to reveal the new iPhone won't be Tim Cook — that hasn't happened in fifteen years.
That's the event Apple just confirmed: "Surprise and shine," and it's incoming CEO John Ternus's very first keynote.
Here's why: Cook moves up to executive chairman on September 1st.
Four days later, Ternus steps up instead — not an outsider, but the guy who's run Apple's hardware engineering for the past five years.
Here's what's real right now: 10 AM Pacific, Steve Jobs Theater, one tagline.
Not one product named yet — you get a date, not a lineup.
Reportedly on deck: the iPhone 18 Pro and Pro Max, and Apple's first-ever folding iPhone, one that opens like a book into a tablet-sized screen, according to MacRumors and 9to5Mac.
Meaning, Apple's finally moving off a slab shape it's kept since the very first iPhone.
Samsung's had a folding phone since 2019. Google since 2023. Apple never has — until, maybe, now.
Still, nothing beyond the date is confirmed.
Underneath all that, here's what you're actually watching for: what an Apple without Tim Cook onstage even looks like.
Two firsts, one morning. That's what's real — everything else, September 9th tells us.

## Beat map (every beat bound to a verified asset or MG spec)

| anchor | visual |
|---|---|
| hook (≤2.2s) — "the person walking out ... won't be Tim Cook" | face pop, full frame, no card — line carries itself; caption hits "won't be Tim Cook" as the highlight |
| "That's the event Apple just confirmed ... Ternus's very first keynote" | `receipt` asset **invite-hero** (Apple's own glowing-logo invite art, captured via 9to5mac) full-bleed with slow drift-zoom |
| "Here's why: Cook moves up to executive chairman on September 1st" | annotatezoom on asset **ceo-receipt** (Apple Newsroom's own paragraph, "...effective on September 1, 2026") — underline the date |
| "Four days later, Ternus steps up instead ... past five years" | asset **ceo-photo** (official Apple Newsroom photo, Cook + Ternus walking at Apple Park) — slow push-in/parallax, NOT a floatcard (avoid repeating september-preview's treatment for this exact photo) |
| "Here's what's real right now: 10 AM Pacific, Steve Jobs Theater, one tagline" | `statcard`-style MG: three rows building in sequence — "10:00 AM PT" / "Steve Jobs Theater, Apple Park" / "'Surprise and shine'" — footnoted MacRumors, backed by asset **macrumors-body-receipt** as the receipt crop behind it |
| "Not one product named yet — you get a date, not a lineup" | wordcascade-style single line, stark, on black — "ZERO PRODUCTS NAMED" |
| "Reportedly on deck: iPhone 18 Pro and Pro Max, and Apple's first-ever folding iPhone ... according to MacRumors and 9to5Mac" | MG `specsheet`/statcard: "iPhone 18 Pro / Pro Max" + "Foldable iPhone" rows, each tagged "EXPECTED — not confirmed", footnote "MacRumors · 9to5Mac"; behind it, asset **macrumors-headline** as the credited receipt |
| "Meaning, Apple's finally moving off a slab shape it's kept since the very first iPhone" | MG timeline/strip motif implying years, no invented iPhone renders — abstract shape-silhouette graphic, not a real product photo (nothing has shipped) |
| "Samsung's had a folding phone since 2019. Google since 2023. Apple never has — until, maybe, now" | MG `HCompare`-style build: "Samsung — 2019" / "Google — 2023" / "Apple — —" landing on the blank |
| "Still, nothing beyond the date is confirmed" | face, stark cut back to facecam — honesty beat, no card, no distraction |
| "Underneath all that ... what an Apple without Tim Cook onstage even looks like" | asset **ceo-photo** reused, different crop/hold than its first appearance (G07: one clip = one footage beat — distinct region/zoom this time) |
| "Two firsts, one morning. That's what's real — everything else, September 9th tells us." | face pop close, then MG count-up card "SEPTEMBER 9" as final hold |

**Discipline:**
- No product renders used anywhere — nothing has shipped, so every "expected"
  row is a labeled stat card, never a photo implying a real device.
- Credits: Apple (invite art, CEO photo/receipt) once each on first use;
  MacRumors once (headline + body receipt). G14/G07 apply.
- Facecam: hook + honesty beat + so-what pivot + CTA close ≈ within band.
- No CTA keyword (`cta_keyword: none`) — closer is a follow-up-promise/date-
  anchor, not a comment-gate; G24 does not require a CTA scene for `news`.
- Treatment note: september-preview already used a `floatcard` on this same
  Cook/Ternus photo and a `receipt`+`annotatezoom` combo for the foldable
  story. This reel deliberately uses push-in/parallax on the photo instead
  of floatcard, and stat-card/HCompare treatments for the rumor cluster
  instead of repeating the receipt-on-deviceframe motif.
- Samsung/Google comparison (2019/2023) is spoken unhedged (research.md
  advises this) because it is settled public history, not a claim about the
  September 9 event — deliberate, documented in the ledger.
