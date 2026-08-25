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
