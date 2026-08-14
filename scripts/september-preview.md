# september-preview — script + beat map

**Format:** top5 (first top5 reel through the engine) · **Style:** nick-saraev
**Look:** 0aa05d6e (warm) · **Target:** 123 words → ~46s at measured 2.7 wps (band 26-48s)
**Refs:** MacRumors 2026-08-13 (Juli Clover) · Apple Newsroom 2026-04-20 (official)

## Script (spoken narration)

Apple's about to drop at least 5 new products.
September's list, straight from MacRumors.
1 — iPhone 18 Pro and Pro Max: A20 Pro chip on 2 nanometers, variable-aperture camera, Dark Cherry color.
Rumors say up to $300 pricier.
2 — Apple's first foldable: the iPhone Ultra. 7.8 inches unfolded, Touch ID, around $2,000.
3 — Watch Series 12: faster chip, bigger battery, same look.
4 — Watch Ultra 4: thinner, upgraded sensors — single source, so squint.
5 — a new boss: John Ternus runs his first keynote. Tim Cook goes Executive Chairman September 1.
No standard iPhone 18 though — that one's March.
Expect it all September 8 or 9.
Comment SEPT and I'll send the full list when it's official.

## Beat map (every beat bound to a verified asset or MG spec)

| anchor | visual |
|---|---|
| hook (≤2s) | `split` — top **clip-p-rods** (iPhone amid flying rods, neon 9:41), bottom face |
| "straight from MacRumors" | annotatezoom **receipt-mrs-hero** (underline red headline box) |
| item 1: chip/camera/color | **clip-p-drop** + label "01 · iPHONE 18 PRO" → **clip-p-dust** |
| "up to $300 pricier" | nick **infocard** overlay on the p-dust beat — heading "+$300?", body "rumored Pro pricing · MacRumors" |
| item 2: foldable | `deviceframe` (iPhone frame) on **receipt-mrs-fold** + label "02 · iPHONE ULTRA" — the article IS the visual (no fake foldable footage) |
| item 3: Watch S12 | **clip-w-trio** + label "03 · WATCH SERIES 12" → **clip-w-sleep** |
| item 4: Ultra 4 | **clip-w-ultra** + label "04 · WATCH ULTRA 4" → annotatezoom **receipt-mrs-watch** (circle "DigiTimes", underline "no other rumors have backed up the claim") lands on "single source, so squint" |
| item 5: new CEO | face pop ("a new boss") → **still-ceo-photo** floatcard (Cook + Ternus at Apple Park) → **receipt-ceo-hero** (official headline; stated flat — Apple Newsroom) + label "05 · NEW CEO" |
| "no standard iPhone 18 — March" | `wordcascade` — "NO iPhone 18" / "→ MARCH 2027" accent |
| "September 8 or 9" | `uidialog` — **NEW treatment**: Calendar-invite mock "Apple Event (rumored) · Sep 8 or 9 · Apple Park · [Accept]" |
| CTA | face pop → `commentcta` word **SEPT** |

**Discipline:** clips A/B frame-verified (start AND end — three windows were re-cut
after failing this); Watch pops are 1.1-1.6s clips, beats capped under them (G13).
AirPods segments banned (not in the story). All product footage = current-gen Apple
film used as preview b-roll, credited Apple; never labeled as the unreleased product.
Ternus/Cook = official, stated flat. DigiTimes caveat on screen AND in VO.
Facecam: hook bottom + item-5 pop + CTA pop ≈ 11-12% (band 10-20%).
SFX: nick pack (tiny clicks/pops, vols .06-.10) 6-9 cues; music bed-726 near-flat.
No treatments repeated from iphone18-split (no categorygrid/endquestion/timeline) or
from the last nick reels (no logoassemble hook, no statcard, no terminal).
