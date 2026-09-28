# Long-form video: what this engine can and cannot do today

Written 2026-09-25 after a read of the code, the gates and the two cost accounts.
This is a findings document, not a decision. Numbers are computed, not estimated,
except where marked.

## What carries over unchanged

The expensive half of the pipeline is format-agnostic:

- **Research.** `reel-research` (plan -> parallel agents -> findings), the claims
  ledger with TIER/SRC/VIA/SURPRISE, `research_check.py`, `source-verification`.
  A 10-minute script needs 5-6x the claims, not a different method.
- **The approval chain.** structure.md -> research.md -> humanizer -> propose ->
  approve, all hash-bound (G27). Works at any length; the UX of approving ~1,500
  words in one block is the open question, not the mechanism.
- **Sourcing and capture.** `capture.mjs` (mobile + desktop), `get_logo.mjs`,
  yt-dlp recipes, the manifest with `source_url` per asset.
- **Audio master.** Two-pass loudnorm to -14 LUFS, G31, `sfx_audibility.py`.
- **Packaging.** `packaging_check.py`, the AI-disclosure rule, `youtube-seo`.

## What breaks, concretely

1. **G02 hard ceiling is 180s.** A long-form cut needs its own format profile and
   a raised ceiling for that profile only.
2. **Every scene component is 1080x1920.** 44 component files, 46 scene types,
   authored against a vertical frame: fixed pixel heights, the caption band at
   75-78%, `platformSafeArea.ts` (measured Reels/Shorts overlays, which do not
   exist on YouTube desktop or TV). `Root.tsx` already declares a 1920x1080
   composition for the Instagram CTA card, so the plumbing takes landscape; the
   LAYOUTS are the work.
3. **Every pacing number is calibrated to 26-80s.** G03 hook <=2.0s, G04 static
   max 1.7s, facecam 10-20%, SFX 6-9 cues, clip-reuse limits. None of it
   transfers. G23 says a new genre's numbers come from a real teardown of 3-5
   reference videos — that discipline applies here more than anywhere.
4. **Burned word-reveal captions are a short-form convention.** Long form wants
   an SRT sidecar instead (whisper already produces the timings).
5. **The cover tool's wide layout is the retired path** (STYLE-RULES 2026-09-11:
   a 14-character line wraps in the wide layout). A 16:9 thumbnail needs a pass.

## Cost per video, computed

| Length | Words @2.7 w/s | ElevenLabs (19.7 cr/s) | HeyGen face-led (1 cr / 3s) | HeyGen bookends |
|---|---|---|---|---|
| 6 min  |   972 |  7,088 credits | 120 of 436/mo | ~12 |
| 8 min  | 1,296 |  9,451 credits | 160 of 436/mo | ~12 |
| 12 min | 1,944 | 14,177 credits | 240 of 436/mo | ~12 |

Reference: ios27-battery-drain (67s of speech) cost 1,317 ElevenLabs credits and
~12 HeyGen credits with bookends.

**The voice is the budget, not the avatar.** A face-led 8-minute video is 160 of
436 monthly HeyGen credits (2.7 videos/month); the same script is ~9,500
ElevenLabs credits whichever route is chosen. Check the ElevenLabs plan quota
before committing to a cadence.

**Render time scales linearly** and has not been measured past 80s. Assume an
8-minute cut is ~6x today's render per iteration, and that iteration count is what
actually costs the day.

## The honest blocker that is not technical

`config.json` records it already (2026-08-26, measured): the cloned voice carries
1.86 semitones of pitch movement where real creator references measure 3.74-6.63,
and no stability/style setting fixes it — the fix is a re-clone from expressive
source recordings (`references/voice-clone-recording-spec.md`). Eighty seconds of
flat read is survivable. Eight minutes is not. A re-clone is a prerequisite for
long form, not a nice-to-have.

## Three routes

**A. Roundup cut** — stitch existing vertical reels into a weekly landscape
roundup with a designed frame (chapter rail beside a 9:16 panel), new intro and
outro. Cheapest: no new VO for the body, no component port. Ceiling is low; it is
a compilation, and the body was written for a different attention curve.

**B. Voice-led landscape explainer (recommended)** — one topic, 6-8 minutes,
avatar bookends only, body carried by slides, real screen recordings, captured
receipts and sourced b-roll. Keeps the credit cost at ~12 HeyGen credits, reuses
the research and approval chain wholesale, and needs: a `longform` format profile
from a teardown, a 16:9 layout pass on ~6 scene types (not all 46), chapter
structure, an SRT deliverable, a 16:9 cover.

**C. Talking-head + b-roll** — classic YouTube explainer, face on screen most of
the runtime. Simplest layout work, highest credit cost (160/video), and it puts
the weakest asset (the flat clone) in front for eight minutes. Not until the
re-clone.

## What a pilot looks like

1. Teardown 3-5 reference long-form videos in our niche with `reel-analyzer` plus
   ffprobe/scene-detect — cut rhythm, chapter length, how often the face returns,
   where the retention devices sit. Write `formats/longform.md` + a `FORMATS`
   profile with MEASURED numbers.
2. Port the 6 scene types the profile actually needs to a width-aware layout, with
   a `safeArea` profile for YouTube instead of the Reels overlay.
3. Build one 6-8 minute pilot end to end on a topic with real depth, through the
   existing approval chain, chapter by chapter.
4. Measure before scaling: render time per iteration, VO credits, and whether the
   research method holds at 40-60 claims.
