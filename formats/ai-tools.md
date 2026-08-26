# Format: ai-tools

AI / Claude / automation tool reels — what a tool does, whether it's worth it,
how to use it. Added 2026-08-25 from an 8-reel measured teardown (5× Badar
Munir YT shorts, 3× Nick Saraev IG reels); full numbers and provenance in the
STYLE-RULES entry of that date and in `FORMATS["ai-tools"]["_derived"]`.

**Numbers:** `python3 tools/reel_gates.py --formats`

## The blend (user decision 2026-08-25)

**Saraev's skeleton, Badar's evidence.**

- **Skeleton — face bookends.** The presenter opens the reel (hook, with the
  problem stated) and closes it (CTA). The middle belongs to evidence. This
  fits a HeyGen twin; Badar's own ~60% on-camera style leans on a live human's
  gestures and was deliberately not adopted.
- **Evidence doctrine — the format's own reading of Rule 3:** *a named tool is
  ON SCREEN, running or being itself, while it is named.* Its real page, its
  real output, a real terminal, a real before/after. A README screenshot is
  evidence only for a claim ABOUT the README (e.g. "its README admits...").
  Full-screen text cards standing in for demos are this format's
  logo-build anti-pattern — the claude-eating-tokens v1 failure.
- **The unfair advantage:** for Claude-topic reels the artifacts are
  recordable in-house — real ccusage output, a real growing context, real
  /clear — tier `official`, zero rights friction. Record, don't screenshot.

## Script skeleton

1. **Problem hook, ≤2s** — the viewer's pain, artifact already on frame 0.
   Not "here's a tool": "your X looks/costs/does Y".
2. **The mechanism or myth** (optional but our differentiator) — one
   checkable reason WHY, sourced.
3. **Numbered tools, 2–4.** Each gets: one plain-words sentence of what it
   does → the NAME lands while its artifact is on screen → its result shown.
   Never a name before its plain-words intro (the "So take caveman" failure).
4. **Follow/comment CTA** — required (G24); all 8 corpus reels carry one.

## Pace notes

The corpus speaks at 217–237 wpm; our twin is locked at 2.35–2.75 wps. The
40–60s band is those word counts (~95–176) mapped through OUR pace — do not
copy corpus runtimes directly, and do not pad a single-tool reel to fill the
band. Cut rhythm on list reels measures 1.4–1.7s/cut, walkthroughs 4–5s;
that is playbook guidance, not a gate.

## Inherited, unmeasured — tighten later

`sfx` count/vol are inherited from news (stills can't measure sound). The
face band (0.10–0.25) is measured off Saraev's bookends only. Re-derive both
from the first shipped ai-tools reel's retention data (`retention_ingest`).

## Observation study 2026-08-25 (9 reels frame-read, 8 transcribed — user-picked set)

### Scouting & sources — how they actually use footage and screenshots

- **The default composition is the split-stack** (Badar ~90% of frames):
  evidence in the top half, presenter under it. Saraev interleaves instead:
  evidence full-frame on a BRAND CANVAS (terracotta when sponsored, white
  organic), face beats between runs. Our `split` and canvas backdrops map 1:1.
- **Evidence is captured as WINDOWED recordings with a live cursor** — the
  repo page scrolled at reading speed, a button actually clicked ("Use for
  free"), a dropdown opened, text filling in. Never a static full-page
  screenshot. Our equivalent: `capture.mjs record` + `floatcard` (a clip
  shown whole on a card).
- **READMEs and docs are quoted as clean text cards with one line
  highlighted** (Saraev black-highlight, our `sourceread`), used only when
  the claim IS about the text.
- **Tool OUTPUTS are shown as the proof** — Badar's HyperFrames reel is
  mostly videos the tool made (charts, maps, avatar clips, the editor
  timeline), labeled with small pill captions ("a Full Product launch
  Video"). Show what it made, not what it says about itself.
- **Meme/stock b-roll appears exactly once, at the hook** — Badar's pasted-
  logo dumpster meme, Saraev's dark dev-at-desk stock for the pain beat.
  Never mid-reel.

### Motion graphics — the shared vocabulary

- **Logo/wordmark cards at naming moments**: the instant a tool is named, a
  designed card lands — Badar's "CLAUDE CODE" in chunky PIXEL type beside
  the real logos, Saraev's glossy 3D icon grids for "platforms". Ours:
  `logobeat` / pixel display face (Press Start 2P is already the pack's
  pixel voice).
- **Money and metrics as big color pops**: green $ figures, orange bar
  charts ("API USAGE"), star-rating product cards. Ours: `statcard` with
  animated bars.
- **Keyword pops on the CTA verbs**: one word in huge neon green (INSTALL /
  COMMENT / FOLLOW / SETUP) over the face. Ours: `commentcta` keyword +
  `emphasis`.
- **Everything floats on a canvas** — windowed cards with soft shadows over
  a flat color, sliding and settling; nothing full-bleed except the hook
  and demos.

### Script style — the measured grammar (8 transcripts)

- **Hook = a claim about the VIEWER or a shock inversion**, never a product
  announcement: "Your Claude Code designs look average — and it's not
  Claude, it's your setup" / "HeyGen just made HeyGen useless" /
  "Everyone's talking about how expensive it is to build apps."
- **One plain sentence of function fused to each name**, artifact on screen
  at the name. Numbers stay concrete (200 templates, $3,000 a pop, 3.3GB).
- **Their hype markers — "yes you heard it right", "the crazy part",
  "completely free" ×3 — are NOT ours.** The house register is reporting;
  we keep their compression and their fused function-plus-name, not their
  sell. Saraev's sponsored reel burns a disclosure line — if we ever take a
  sponsor, so do we.
- **CTA is two-step and verb-first**: "Just comment X and I'll send you Y",
  sometimes "follow me, then comment". All 9 reels close this way.
