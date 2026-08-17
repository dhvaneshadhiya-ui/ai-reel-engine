# AI Reel Engine

Turn a topic into a finished vertical reel — AI presenter, sourced footage,
motion graphics, captions, SFX and music — rendered entirely as code.
**1080×1920, 30fps, mastered to −14 LUFS. Zero manual video editing.**

Built on [Remotion](https://remotion.dev) (video as React) + Python build
scripts + Whisper word-timings, driven by a coding agent.

---

## Give this to an agent

Point any coding agent (Claude Code, Codex, Cursor…) at this folder and say:

> **Read `AGENT.md`, then make a reel about `<your topic>`.**

That file is the complete operating manual: the workflow, the beat-sheet
contract, the visual rules, and the failure modes to avoid.

---

## Quickstart

```bash
npm install
cp config.example.json config.json     # add YOUR avatar + voice IDs
npx remotion studio                    # opens the preview
```

Requirements: Node ≥ 18, Python 3, `ffmpeg`, `yt-dlp`,
`pip install openai-whisper`, headless Chrome, and an avatar/TTS account
(HeyGen by default — swap freely).

---

## What's in here

| Path | What it is |
|---|---|
| `AGENT.md` | **Start here.** Operating manual for the agent. |
| `PIPELINE.md` | Full technical spec — schema, scene types, render flags. |
| `STYLE-RULES.md` | Learned rules ledger. These override everything. |
| `src/types.ts` | The contract — every scene type is defined here. |
| `src/components/` | 34 scene renderers (receipts, spec sheets, comparisons…). |
| `src/Reel.tsx` | The player: scene switching, captions, music, SFX. |
| `scripts/` | Job pipeline: new job → compile → validate → register → render. |
| `tools/` | Voice tightening, frame linting, screen capture, examples. |
| `styles/` | Style packs — the LOOK and script voice per creator style. |
| `references/` | Job contract, avatar flow, QA checklist, tool policy. |
| `examples/` | A real beat sheet, script + shot map, and asset manifest. |
| `public/fonts, music, sfx*` | Shared fonts, music beds and sound effects. |

---

## How it works (60 seconds)

A reel is a **beat sheet** — one JSON file of timed scenes. Components render
them. A build script generates that JSON by anchoring every cut to the
**voiceover's word timings**, so visuals land exactly on the words.

The order matters more than anything else:

```
topic → scout assets FIRST → write script bound to those assets
      → voice + face → word timings → beat sheet → render → master → QC
```

> **The rule:** never script a claim you can't show. Source footage first,
> then write to it.

---

## Bring your own

This repo ships the **engine**, not anyone's identity. You supply:

- your avatar + voice IDs (in `config.json`)
- your own footage, receipts and per-reel assets (in `public/assets/<slug>/`)
- your own style pack, or edit the included ones

No credentials, avatars, voice samples or personal assets are included.

---

## Licence / attribution notes

Style packs describe editing *techniques* (pacing, typography, sound design) —
use them as craft references, not to impersonate anyone. When you use
third-party footage, keep the `@credit` on screen and respect the source's
terms.
