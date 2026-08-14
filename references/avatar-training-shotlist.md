# Training set for the personal model — 30 shots

For HeyGen "Train your personal model" (10 minimum, 30+ for best results,
60 credits, 10–15 min). Works whether you upload real photos or generate them
in the AI Generated looks tab.

## The one rule that decides whether this works

**THE TRAINING SET BECOMES THE EXPRESSION RANGE.**

Measured 2026-08-12: the current photo avatar (`0aa05d6e`, "Smiling podcaster
in blue hoodie") smiles through every line because it is a deformation of ONE
smiling still. `motionPrompt` could not change it. `expressiveness: low` could
not change it — it only dropped motion 6.90 → 1.02 and kept the smile.

The existing look library is almost entirely smiling. **Train on those and you
get a better-moving avatar that still grins on "here is the honest problem."**

So: **at least 12 of the 30 must be non-smiling.** That is the whole point of
doing this.

## Constraints that apply to EVERY shot

Paste these into every prompt, and check them on every uploaded photo:

- **Hands empty, holding nothing — no pen, no phone, no papers, no props.**
  (2026-08-12: the avatar invented pens mid-gesture at 1:36 of grok-bot. The
  prop ban is now permanent in `config.json` → `avatar.motionPrompt`.)
- Same person, same glasses, clean-shaven consistency, same general studio
  world — vary the *pose and face*, not the identity.
- **16:9 landscape**, subject centred-left, head and shoulders well inside the
  frame. Reels generate 16:9 and crop to 9:16 at a measured face-x, so a
  subject drifting to frame edges crops badly.
- Eyes sharp and unobstructed; no heavy glasses glare hiding the eyes.
- No hands crossing in front of the face; no hair/mic covering the mouth.

## The 30 shots

Each row is one complete image. The matrix is covered on purpose: every angle
and framing appears with more than one expression, so the model does not learn
"3/4 left = smiling".

### Block A — SERIOUS / NEUTRAL register (12 shots) — the missing half

| # | Angle | Framing | Expression | Hands |
|---|---|---|---|---|
| 1 | Straight on | Medium (waist up) | Fully neutral, resting face, mouth closed, brows level | Loosely clasped on desk |
| 2 | Straight on | Medium close (chest up) | Serious and concerned, brows slightly drawn | Open palms low, mid-explain |
| 3 | 3/4 left | Medium | Level and focused, mid-sentence, mouth slightly open | One hand raised, palm up |
| 4 | 3/4 right | Medium close | Skeptical — one brow raised, slight head tilt | Fingers steepled |
| 5 | Straight on | Close (shoulders up) | Flat, unimpressed, mouth a straight line | Out of frame |
| 6 | Slight low angle | Medium | Firm and authoritative, chin level, no smile | One palm pressed down (settling a point) |
| 7 | 3/4 left | Medium | Thinking — eyes just off camera, brow furrowed | Hand near chin, NOT touching face |
| 8 | Straight on | Medium | Warning — brows drawn, direct eye contact | Both palms forward (stop) |
| 9 | 3/4 right | Medium | Explaining a mechanism, engaged but not warm | Both hands framing a size |
| 10 | Straight on | Medium close | Reading bad news, mouth closed, eyes steady | Hands still, resting |
| 11 | Slight high angle | Medium | Measured, weighing two options | One palm up, then other (scales) |
| 12 | Straight on | Wide (desk visible) | Neutral listening face, attentive | Both forearms on desk |

### Block B — WARM / POSITIVE register (9 shots)

| # | Angle | Framing | Expression | Hands |
|---|---|---|---|---|
| 13 | Straight on | Medium | Genuine closed-mouth smile | Open palms, welcoming |
| 14 | 3/4 left | Medium close | Broad open smile, eyes crinkled | One hand gesturing outward |
| 15 | Straight on | Close | Warm, mid-laugh | Out of frame |
| 16 | 3/4 right | Medium | Pleased, knowing half-smile | Thumb-and-finger pinch (small detail) |
| 17 | Straight on | Medium | Enthusiastic, brows up, mouth open mid-word | Both hands lifted off desk |
| 18 | Slight low angle | Medium close | Confident and friendly, direct | One index finger raised (point one) |
| 19 | 3/4 left | Medium | Encouraging, soft smile, head slightly forward | Hand toward camera (to the viewer) |
| 20 | Straight on | Wide | Relaxed, comfortable, easy smile | Leaning back slightly, hands open |
| 21 | Straight on | Medium close | Delivering a punchline, amused | One hand flicked open |

### Block C — REACTION / EMPHASIS (5 shots)

| # | Angle | Framing | Expression | Hands |
|---|---|---|---|---|
| 22 | Straight on | Medium close | Surprised — brows high, eyes wide, mouth slightly open | Both hands paused mid-air |
| 23 | 3/4 right | Medium | Disbelief, head pulled back slightly | One palm up, questioning |
| 24 | Straight on | Medium | Counting — clearly showing two fingers | Two fingers up, clear silhouette |
| 25 | Straight on | Medium | Counting — clearly showing three fingers | Three fingers up |
| 26 | 3/4 left | Medium close | Emphatic, leaning in on a key number | One fist gently landing on the other palm |

### Block D — ANGLE + FRAMING coverage (4 shots)

| # | Angle | Framing | Expression | Hands |
|---|---|---|---|---|
| 27 | Profile-ish 45° left | Medium | Neutral, looking toward where a graphic would sit | Relaxed at desk |
| 28 | Profile-ish 45° right | Medium | Mild interest, looking toward a graphic | One hand gesturing to the side |
| 29 | Straight on | Very close (face fills frame) | Neutral, direct, mouth closed | Out of frame |
| 30 | Straight on | Wide desk / room | Mid-gesture, general presenting energy | Both hands active |

## Balance check before you press Train

- Non-smiling: **12** (Block A) — the minimum. More is better.
- Smiling/warm: 9
- Reaction: 5
- Coverage: 4
- Straight on 16 · 3/4 left 6 · 3/4 right 5 · low 2 · high 1
- Hands visible and EMPTY in 26 of 30

If your generated set drifts smiley (it will — the models default to it),
regenerate Block A with "not smiling, mouth closed, serious" stated twice in
the prompt.

## Prompt template for the AI Generated looks tab

> Indian man in his 30s with rectangular glasses, seated at a podcast desk with
> a studio microphone, [BACKGROUND]. [ANGLE], [FRAMING]. Expression:
> [EXPRESSION] — not smiling, mouth closed. [HANDS]. Hands are empty and hold
> nothing — no pen, no phone, no papers, no props. Sharp focus on the eyes,
> natural skin texture, 16:9 landscape, subject centred.

Drop "not smiling, mouth closed" for Blocks B and C only.

## After training

1. Measure it before trusting it:
   `python3 tools/measure_avatar.py score <clip> --register <lookId>`
   Thresholds: <1.0 frozen · 1.0–2.5 stiff · 3+ gestures.
2. **Probe the expression range with a ~7s, 3-credit clip** carrying all three
   registers in one script (figure → caveat → closing question), then inspect a
   face crop strip at ≤0.5s spacing. That is exactly how the current avatar's
   fixed smile was proven.
3. If it holds a range, set `register` accordingly in `avatarRegistry` — a
   trained model that genuinely varies could replace the warm/serious PAIR
   with one avatar, and G19's "one look per reel" constraint relaxes.
4. If it still smiles through caveats, the two-look system stands. Record the
   outcome either way in `STYLE-RULES.md`.

**Do not update `avatarRegistry` from the training preview alone.** Every
avatar claim in this repo has been wrong at least once until measured.
