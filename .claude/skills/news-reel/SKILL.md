---
name: news-reel
description: Produce a finished vertical news/explainer reel end to end — script, HeyGen avatar, sourced b-roll, motion graphics, captions, audio master — with no manual editing. Use whenever the user wants a reel, short, or vertical video about a tech news item, product launch, or announcement; asks to "make a reel about X"; names a topic and a style profile; or asks to re-cut, fix, or iterate an existing reel. Also use when adding a new creator style profile to the engine.
---

# News reel

**The engine lives at `/Users/dhvaneshadhiya/Movies/ai-reel-engine`. Work from
that directory.** (Set 2026-08-11 by the user. A second, older engine exists at
`~/AI Videos/reel-engine` with a completely different `pipeline/make.mjs`
workflow — do NOT use it, and do not mix its commands in here. If the user
explicitly names the old one, follow that repo's own README instead.)

## Read these first, in this order

1. **`RULES.md`** — the short, current, binding rule set. Each rule is marked
   **[GATE]** (code raises and stops the build), **[LINT]** (linter exits
   non-zero), or **[EYE]** (no automation — you are the only check). Start here.
2. **`AGENT.md`** — the operating manual: order of operations, the beat-sheet
   contract, the failure-mode table.
3. **`styles/<style>.md`** — default `varun-mayya`. Also load
   `styles/varun-script-playbook.md` when writing the script.
4. **`STYLE-RULES.md`** — the dated ledger behind RULES.md. Read it for *why* a
   rule exists and for the **treatment history** (never repeat the last reel's
   treatment for the same kind of information). It is append-only and contains
   superseded entries; where it disagrees with RULES.md, RULES.md wins.
5. **`PIPELINE.md`** — technical spec when you need scene-type detail.

First command of any session: **`python3 scripts/doctor.py`**. It verifies the
toolchain, the locked config values, and that every gate still fires. A missing
dependency used to silently disable the frame checks — this fails loudly.

Confirm topic and style with the user only if genuinely ambiguous. Everything
else is your job.

## Locked user settings (do not silently change)

| Setting | Value | Why |
|---|---|---|
| Length | **60-80s** | User rule 2026-08-12 (was 60-120). Gate G02. Longer is allowed only with `allowLong` + a written `allowLongReason`. Cut every sentence that does not change the viewer's understanding. |
| Hook | **<=2.0s** | User rule 2026-08-12. Gate G03. Open on the actual tension, surprise or consequence — never a generic product announcement. |
| HeyGen engine | **per-look, by MEASUREMENT** | Do NOT hardcode an engine. Run `tools/measure_avatar.py` and match `config.json -> avatarRegistry[<lookId>].engine`. The 2026-08-11 'always avatar_v' rule was WRONG for the current look: on `0aa05d6e` Avatar V scores 0.48 (frozen) while `avatar_iv` + `expressiveness:high` + `motionPrompt` scores 6.90 (gestures). `doctor.py` refuses a mismatch. |
| Avatar register | **pick the LOOK** | A photo avatar's expression is fixed by its source still — no prompt or `expressiveness` value changes it (measured 2026-08-12). `0aa05d6e` = warm, `7123b3d0` = serious. One look per reel; gate G19 blocks a serious script on the warm face. |
| Script approval | **required** | Show the narration + beat plan and get a yes BEFORE generating the avatar. Generation costs credits and freezes the audio. |
| Voice speed | **1.05** | User note 2026-08-11 "slow down a little". Supersedes the old 1.2. |
| Caption style | `nick-display` | Per-word reveal; `emphasis` list drives the accent keyword. |
| Avatar / voice | from `config.json` | Never hardcode ids in a build script. |

`motionPrompt` is **rejected** by the API alongside `avatar_v` when the
avatar's group has no digital twin — which is why the current look runs on
`avatar_iv`. The prompt MUST keep the prop ban verbatim ("hands hold nothing
at any point - no pen, no phone, no papers, no props of any kind"); without
it avatar_iv invents pens. Do NOT put per-section expression instructions in
the prompt: measured 2026-08-12, they do nothing. Expression is chosen by the
LOOK.

Before a full generation, probe prompt-side changes with a ~7s clip (~3 of
the 436 monthly credits) and inspect a hand-region frame strip at <=0.5s
spacing. A contact sheet is too coarse to catch a prop.

## Sound design

Run `python3 tools/sfx_library.py` to see the catalogue grouped by role. Place
cues by ROLE, not by taste: transition on a cut, popup on an element entering,
suspense before a reveal (and it MUST resolve), reveal on the payoff, impact on
a data card or the single biggest claim. Gate G28 blocks a cue that is not in
the catalogue, sits on the wrong beat type, outruns its scene, or breaks the
per-role caps. Full reasoning and the lead-time table:
`references/sfx-placement.md`.

## Order of operations

**STEP 0, BEFORE ANYTHING IS GENERATED: get the script approved.**
`python3 tools/script_approval.py propose <slug>`, show the user the script and
the beat plan, ask the open questions, wait for an explicit yes, then
`approve <slug>`. `check <slug>` exits 1 until that happens and gate G27
re-checks the hash at build time. Never generate an avatar on an unapproved
script.


Do not reorder. The expensive failure is writing a script about footage you
do not have.

### 1 — Scout BEFORE scripting

**Capture source pages on MOBILE.** `tools/capture.mjs` defaults to a real
mobile viewport (360x780 @3 = 1080x2340, iPhone UA, `isMobile` so the site
serves its mobile layout). Every reel is 9:16: a desktop grab at 1200x900 fits
to 1080x810 inside the frame — 42% of the height, body text unreadable.
Measured on igeeksblog.com 2026-08-13. Pass `--desktop` when mobile is not feasible or not truthful — software UIs,
dashboards, editors, wide comparisons, pages with no mobile layout. **A desktop
capture must then be CROPPED AND MOVED, never fitted whole**: `annotatezoom`
with an explicit `focus` rect, easing in until that region fills the frame,
plus a slow drift. If the point is an interaction, RECORD it instead of
screenshotting. Gate G29 blocks a landscape capture in a `sourceread`, and a
landscape `annotatezoom` with no `focus`. Full policy:
`references/source-capture-policy.md`.

Verify the story with WebSearch/WebFetch (topics are newer than your training
data). Get every figure from a primary announcement plus 2-3 pieces of
coverage. Then hunt visuals and write
`public/assets/<slug>/manifest.json` with:

- `verified_facts` — every figure with its unit AND source url
- `explicitly_NOT_claimed` — claims the sources do NOT support, plus the
  **source timestamps banned** from the reel so a plausible-but-unsupported
  claim cannot leak in as b-roll
- `assets[]` — each with `shows` written **only after looking at extracted
  frames**, plus `quality` and the exact `crop`

Scout order: official channels/keynotes → creator demo compilations (credit
them) → screenshot receipts (`tools/capture.mjs`) → brand marks
(`tools/get_logo.mjs`).

Keep raw downloads in `<repo>/_sources/<slug>/`, **never** under `public/` —
Remotion copies all of `public/` on every render.

yt-dlp section downloads: always pass **`-N 8`** (concurrent fragments) — the
sequential default crawls at ~10 MB/min on this network vs under a minute
with -N 8. Do NOT pass `--force-keyframes-at-cuts` (ffmpeg exits 8 on merge,
and the file is discarded after fully downloading); sub-clips are re-cut
frame-accurately later anyway. After cutting clips, **check the FIRST second
of every cut** — broadcast sources open on the previous shot (stage
presenters) and the leak is invisible except on frames; the linter's
[HEAD DRIFT] hint flags candidates.

### 2 — Script + beat map

Write `scripts/<slug>.md`: the spoken script **and** a beat table where every
beat carries `visual: <manifest asset id>` or `visual: MG:<component + spec>`.
A beat that resolves to neither is illegal — re-scout or rewrite the line.
At the MEASURED ~2.7 words/sec (2026-08-13, three masters), 60s ≈ 162 words, 80s ≈ 216, 90s ≈ 243, 120s ≈ 324. script_approval.py refuses an out-of-band propose.

### 3 — Voice + face

One continuous avatar master via the HeyGen MCP
(`create_video_from_avatar`, `engine:{type:"avatar_v"}`, 16:9 1080p,
`voiceSettings:{speed:1.05}`). Save as
`public/assets/<slug>/avatar-master-169.mp4`. Extract 16k mono wav → whisper
`--word_timestamps True` → `vo.json`. Measure face-x once on a mid frame with
a decile grid and write `face-x.txt`.

If the master runs long, pause-tightening is free: jump-cut video+audio
together at mid-silence gaps >0.5s, record every cut point, and never let a
facecam beat span one (see RULES.md). ~4-5% runtime back for zero credits.

**Verify every number and date** in the whisper transcript against the script.
A misspelling from whisper `base` is NOT proof of a mispronunciation —
re-run whisper `small` on the 2s slice before spending credits on a re-record.

### 4 — Build, register, render, master

```bash
python3 tools/plan_shots.py <slug> --write   # script -> one shot per clause
# scout to satisfy each line, then fill asset_id + scene per shot
python3 scripts/compile_shot_plan.py <slug>  # writes src/beats/<slug>.json, sets `covers`
python3 scripts/register_beats.py
python3 scripts/render_job.py <slug>         # render + TWO-PASS master + G31
```

Fallback for a reel the shot plan cannot express — you then owe `covers` by
hand (`python3 tools/link_shots.py <slug>` justifies what it can and refuses to
guess the rest):

```bash
cp tools/build_template.py tools/build_<slug>.py   # then fill it in
python3 tools/build_<slug>.py        # writes src/beats/<slug>.json
```

**Never master with a bare ffmpeg line.** This block used to end with
`ffmpeg -af "loudnorm=I=-14:TP=-1.2:LRA=7"`, a SINGLE pass — loudnorm is
adaptive and converges toward the target without reaching it, landing ~1 LU
short, which G31 now rejects. `render_job.py` measures first, then applies the
measured values.


`tools/build_template.py` already wires in `reel_gates.check_beats()`, which
**raises** only on `BLOCKING_RULES` — the three standing rules (Reels/Shorts
format, mobile-first scouting, picture matches words) plus render correctness
and rights. Runtime band, pacing ceilings, headline lengths, facecam share,
clip reuse, SFX count and music automation are **advice** since 2026-08-17:
they print with their evidence and stop nothing. A failing sheet is never written, so it
cannot reach the renderer. Do not work around a gate — fix the plan. If a gate
is genuinely wrong, change it in `reel_gates.py` AND add a case to
`tools/test_gates.py`. The concurrency/timeout flags are required.

### 5 — Critic pass (mandatory, never skip)

```bash
cp out/<slug>-final.mp4 out/<slug>.mp4 && python3 tools/lint_frames.py <slug>
ffmpeg -v error -y -i out/<slug>-final.mp4 -vf "fps=1,scale=150:-1,tile=12x5" -frames:v 1 out/<slug>-lint/sheet.jpg
```

The linter **exits non-zero** on a hard flag. `--soft` overrides it — if you
use that, say so explicitly when handing the reel over.

**Read every frame as a hostile viewer.** The linter catches geometry; only you
catch meaning. Asset errors are invisible in logs —
in the last reel the contact sheet is what caught a clipped hook title, a
missing brand mark, and a creator's PiP webcam baked into a still. Check:
does each frame show what the VO claims at that second; no text cropped
mid-word at frame edges; no app chrome or PiP anywhere; every number carries
its unit; captions clear of the face; integrated loudness ≈ −14 to −15 LUFS.

Fix, re-render, re-verify. Only then deliver.

### 6 — Log it

Append to `STYLE-RULES.md` as *raw note → root cause → distilled rule*, and add
this reel's treatments to the treatment-history list so the next reel does not
repeat them. The ledger is what makes the system improve instead of repeating
mistakes. This step is not optional.

## Report honestly

If beats failed, assets were dropped, or a rule was consciously relaxed, say
so and name them. Never describe a reel as finished when it is not.
