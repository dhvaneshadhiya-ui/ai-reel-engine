---
name: nick-reel
description: Create a complete Nick Saraev-style vertical reel from only a topic, link, post, or short set of details. Use for “make a reel about X”, “turn this into a reel”, or any request for a zero-manual-edit AI reel with research, script, HeyGen presenter and voice, real product visuals, coded motion graphics, captions, music, sound design, rendering, and QA.
---

# Nick Reel

Produce the finished 1080×1920 MP4. Do not stop at a script, shot list, or
storyboard. The user delegates creative and production decisions; do not ask
them to choose templates, visual tools, captions, or transitions.

Engine: `<ENGINE_ROOT>`

## Required context

Before starting a reel:

1. Read the engine's `FEEDBACK.md` completely.
2. Read `styles/nick-saraev.md`.
3. Read [references/style.md](references/style.md).
4. Read [references/job-contract.md](references/job-contract.md).
5. Read [references/qa.md](references/qa.md).
6. Read [references/tool-policy.md](references/tool-policy.md) only when
   selecting an animation or generative-media tool.
7. Read [references/heygen.md](references/heygen.md) before generating the
   presenter.

Rules in `FEEDBACK.md` override this skill.

## Workflow

### 1. Initialize without questions

Infer a short slug, CTA keyword, and 30–45 second target from the topic. Ask the
user only when a missing factual choice would materially change the story or
authorize a new external action. Run:

```bash
python3 ~/.codex/skills/nick-reel/scripts/new_job.py <slug> \
  --topic "<topic>" --details "<details>" --cta-keyword "<keyword>"
```

Tell the user the intended length, that the presenter uses HeyGen credits, and
separately whether any paid generative-video clips are planned. Continue
without waiting for approval because the user requested finished production.

### 2. Research and scout assets before scripting

Browse current primary sources. Every factual claim needs a source. Build
`public/assets/<slug>/manifest.json` with:

- claim or beat it proves;
- primary source URL and publication date;
- local asset path;
- asset kind: receipt, screenshot, screen recording, official footage, logo,
  coded graphic, generated illustration, or generated video;
- what the asset visibly shows;
- required on-screen credit;
- crop or highlight notes.

Use this order:

1. Official product footage, screenshots, launch pages, documentation, or
   repositories.
2. Automated real browser screenshots or screen recordings.
3. A faithful coded recreation of a small UI/dialog/chart.
4. Generated illustration.
5. Generated video only for non-factual conceptual beats.

Do not script an important claim until a visual or coded treatment can show it.
Do not generate fake product UI, logos, terminal output, benchmark tables, or
receipts.

### 3. Write the script and companion resource

Write `scripts/<slug>.md` with the final spoken script and a phrase-to-visual
beat map. Aim for 202–252 WPM, normally about 230 WPM.

Use the Nick grammar:

- hook in the first sentence, normally using free, new, top five, or a concrete
  result;
- one-line explanation;
- proof, numbered steps, examples, or mechanism;
- comment-gated CTA with one memorable keyword.

Keep claims concrete and pronunciation-friendly. Create
`jobs/<slug>/giveaway.md` containing the links, prompts, commands, or checklist
the user can actually send when someone comments the CTA keyword. Never promise
a link or guide that does not exist.

### 4. Generate voice and presenter

Use the authorized private HeyGen Digital Twin. Prefer native HeyGen voice for
reliable lip sync unless the user explicitly requests another voice. Follow
the active connector's required portrait/aspect-ratio schema. Use the
configured Avatar V look when supported, speed 1.2, and a natural motion
prompt. Preserve a calibration frame and use Remotion's measured focus point;
do not trust an unverified automatic face crop.

Download the clean presenter master to
`public/assets/<slug>/avatar-master.mp4`. Extract 16 kHz mono audio and run
Whisper with word timestamps. Verify every number, date, product name, and CTA
keyword against the script before editing.

Record the connector's non-secret video ID, ingest the result, and prepare
timings with:

```bash
python3 ~/.codex/skills/nick-reel/scripts/avatar_handoff.py record <slug> \
  --video-id "<video-id>" --status completed
HEYGEN_DOWNLOAD_URL="<temporary-url>" \
  python3 ~/.codex/skills/nick-reel/scripts/avatar_handoff.py download <slug>
python3 ~/.codex/skills/nick-reel/scripts/avatar_handoff.py prepare <slug>
```

Never print or persist the temporary download URL.

### 5. Direct and build visuals

Keep the face visible in the opening two seconds, then change the visual.
Target a major visual change every 1.6–2.4 seconds. Facecam should occupy about
35–50% of runtime in short returns, not one long block.

Prefer the existing Remotion components. Add a custom component only when an
existing treatment would misrepresent the beat. Follow
[references/tool-policy.md](references/tool-policy.md) for Lottie, Manim,
Motion Canvas, p5.js, or other optional tools.

Create `jobs/<slug>/shot-plan.json`. Every beat must map to its exact VO phrase
and a verified manifest asset or coded graphic. Compile it into the renderable
beat sheet:

```bash
python3 ~/.codex/skills/nick-reel/scripts/compile_shot_plan.py <slug>
```

The compiler resolves phrase anchors against Whisper timestamps, calculates
media trims, generates captions, and writes `src/beats/<slug>.json`. Enforce:

- exactly one text system at a time;
- real screenshots card-framed and focused on the spoken region;
- no raw screenshot full-bleed;
- Nick cream/black/orange palette only;
- chip-lg captions, editorial serif display type, restrained pixel accents;
- internal motion on every designed scene;
- a music bed plus small Nick-style clicks/pops; ordinary cuts remain silent;
- generative video no more than about 15% of runtime unless the topic itself is
  a visual demonstration.

### 6. Register, validate, render, and master

Run:

```bash
python3 ~/.codex/skills/nick-reel/scripts/register_beats.py
python3 ~/.codex/skills/nick-reel/scripts/validate_job.py <slug>
python3 ~/.codex/skills/nick-reel/scripts/render_job.py <slug>
```

Fix every validation error. Treat warnings as critic prompts, not automatic
failures.

### 7. Review before delivery

Open every lint contact sheet and inspect representative full-resolution
frames. Check script/visual match, subject crops, text hierarchy, screenshot
focus, captions, credits, visual variety, and CTA. Listen for pronunciation,
lip-sync failures, clipping, weak transitions, and music masking the voice.
Repair and re-render until the reel passes [references/qa.md](references/qa.md).

Deliver:

- `out/<slug>-final.mp4`;
- `jobs/<slug>/giveaway.md`;
- a one-sentence summary of the treatment;
- any unavoidable limitation that remains.

Do not make the user operate the pipeline.
