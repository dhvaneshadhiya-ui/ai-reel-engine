# Capturing sources for a 9:16 reel

Mobile is the default. Desktop is a deliberate exception that comes with an
obligation: **it must be cropped and moved, never fitted whole.**

Derived 2026-08-13 from the user's reference short (YouTube `q4_-y67JGCU`,
96s, 1080x1920, 41 cuts ≈ 2.3s/shot) plus a measured A/B on igeeksblog.com.

## The decision

**Capture on MOBILE when the source is a readable document** — a news article,
a blog post, a docs page, a support page, a changelog. `tools/capture.mjs`
defaults to 360x780 @3 = 1080x2340: native frame width, type already sized for
a hand, vertical headroom to scroll.

**Capture on DESKTOP (`--desktop`) when mobile is not feasible or not
truthful:**

- software UIs and desktop apps (the thing only exists at desktop width)
- dashboards, admin panels, editors, terminals
- side-by-side comparisons and wide tables
- any page with no mobile layout, or whose mobile layout hides the point
- benchmark charts and leaderboards that reflow into uselessness

## The obligation that comes with `--desktop`

A 2560x1440 grab fitted into 1080x1920 becomes 1080x608 — a third of the
frame, text unreadable. So a desktop capture is never shown whole:

1. **Crop to the region that matters.** Use `annotatezoom` with an explicit
   `focus` rect in source pixels. The camera starts slightly wide and eases in
   until that region fills the frame.
2. **Keep it moving.** A slow push-in or drift across the crop. In the
   reference, the wide Claude desktop app is cropped to the composer box and
   the crop window pans slowly — you can see the "Evening" header drift across
   frames.
3. **If the point is an interaction, RECORD it.** The same shot shows text
   being typed ("Add" -> "Add punctuation," -> "Add punctuation, fix grammar").
   A still cannot carry that; use `capture.mjs record` and a `floatcard` or
   `deviceframe`.

**Gate G29 enforces this**: an `annotatezoom` whose source is landscape and
which declares neither `focus` nor annotations is blocked, because the camera
would settle on the whole wide page.

## Treatments by source type

| Source | Capture | Component | Motion |
|---|---|---|---|
| Article / docs / support page | mobile | `sourceread` | fit to width, follow-scroll, progressive highlight |
| One paragraph that IS the claim | mobile | `annotatezoom` | ease into the paragraph, draw annotations |
| Software UI, dashboard | **desktop** | `annotatezoom` + `focus` | crop to region, push in, drift |
| A live interaction | **desktop, recorded** | `floatcard` / `deviceframe` | the interaction is the motion |
| Whole site, identity matters | mobile | `deviceframe` phone | push-in |
| Whole site, browser chrome matters | **desktop** | `deviceframe` browser | push-in |

## What the reference does with articles

The mobile-captured article is shown **full-bleed** — no card, no frame, no
letterbox — and carries a **progressive highlight** that extends phrase by
phrase in time with the narration, starting wide and pushing in as the
highlight advances. That is our `sourceread`, which already fits to frame
width, follow-scrolls the active line to ~58% down the frame, and applies a
slow zoom. Match the highlight cues to the words being spoken, not to a timer.

## Never

- Letterbox a wide capture into the frame with bars.
- Show a desktop page whole "so the viewer sees the context" — they cannot
  read it, and the context is what the narration is for.
- Use a mobile capture for a UI that does not exist at mobile width. That is
  not honest to the product.
