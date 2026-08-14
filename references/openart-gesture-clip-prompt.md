# OpenArt i2v — merged gesture + expression prompt

One prompt covering every gesture and emotional register we need, for
generating a presenter clip from a still. Engines: Kling 3.0 (~30s, best
identity hold) or Seedance 2.5 (~30s, 4K). Veo 3.1 if a ~60s take is wanted.

## Precondition — this decides whether it works at all

**The source photo must be waist-up, 16:9, with both hands visible and
empty.** i2v cannot animate hands that were never in frame. That is exactly
what killed digital twin #1 (`8e49c9d1`): head-and-shoulders framing, motion
1.71 (stiff), no gestures possible at any prompt.

## The prompt

> Locked-off camera, no camera movement, no zoom, no cuts — one continuous
> take of the seated presenter talking directly to the lens. His expression
> and his hands change together as he speaks: he begins neutral and focused
> with level brows, hands open and palms turning upward as he explains; his
> eyebrows lift in surprise and both hands rise slightly off the desk on a
> striking number; he counts one, two, three clearly on his fingers, then
> raises a single index finger to make one point; he brings finger and thumb
> close together for a small detail, then moves both hands apart to show a
> size; his brows draw in and the smile drops as he turns serious and
> concerned, one palm facing forward in caution; he tilts his head slightly
> with one eyebrow raised in skepticism; he leans a little toward the camera
> to press an important point; and he finishes with a warm genuine smile, one
> open hand gesturing toward the viewer before both hands settle loosely on
> the desk. Hands stay empty the entire time — no pen, no phone, no papers, no
> props of any kind. Fingers stay clearly separated and anatomically correct
> at all times. Natural blinking, subtle head movement, relaxed shoulders,
> natural breathing. Lighting, wardrobe, background and facial identity remain
> identical from the first frame to the last.

## What it covers

**Gestures (10):** open palms up · hands lifting off the desk · counting
one-two-three on fingers · single index finger raised · finger-thumb pinch ·
hands apart for scale · palm forward in caution · forward lean on emphasis ·
open hand toward the viewer · hands settling to rest.

**Expressions (6):** neutral and focused · surprised, brows lifted · serious
and concerned, no smile · skeptical, one brow raised with head tilt · warm
genuine smile · relaxed close.

Gesture and expression are deliberately PAIRED rather than listed separately —
"brows draw in AND one palm forward in caution" — because the failure we are
solving is a face that does not track the script.

## If the engine drops beats

Ten beats in 30 seconds is dense; some engines rush or skip the tail. If that
happens, split into two takes off the same photo and keep both:

- **Take 1 (gesture-led):** everything up to "moves both hands apart to show a
  size", ending with hands settling.
- **Take 2 (register-led):** start neutral, then the serious/concerned beat,
  the skeptical beat, the forward lean, and the warm close.

## Timestamped variant

Some engines follow explicit timing better. Same content, structured:

> [0-3s] neutral and focused, level brows, open palms turning upward
> [3-6s] eyebrows lift in surprise, both hands rise slightly off the desk
> [6-10s] counting one, two, three clearly on his fingers
> [10-13s] single index finger raised to make one point
> [13-16s] finger and thumb pinched for a small detail, then hands apart to
> show a size
> [16-21s] brows draw in, smile drops, serious and concerned, one palm facing
> forward in caution
> [21-24s] head tilts slightly, one eyebrow raised in skepticism
> [24-27s] leans toward camera to press an important point
> [27-30s] warm genuine smile, one open hand toward the viewer, hands settle
> Throughout: locked-off camera, no cuts, hands empty — no pen, phone, papers
> or props. Fingers separated and anatomically correct. Natural blinking.
> Lighting, wardrobe, background and identity identical from first frame to
> last.

## What to check before using the output

The same checks that condemned twin #1 — run them on the generated clip:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate -of csv=p=0 <clip>
python3 tools/measure_avatar.py score <clip>
```

- resolution/aspect: needs to survive the 9:16 crop (16:9 1080p+, not 2:1)
- motion: <1.0 frozen · 1.0-2.5 stiff · **3+ gestures**
- **hand strip at <=0.5s spacing** — check every frame for melted or extra
  fingers. This is i2v's known weak point and the reason the clip might be
  unusable.
- face strip at <=0.5s spacing — confirm the registers actually changed.

## Intended use

NOT as HeyGen twin training footage (i2v hands and non-phoneme mouth motion
would be baked into the twin). Use it as a gesture plate and lip-sync it to
our voiceover with HeyGen `create_lipsync` — gestures from OpenArt, correct
mouth movement from the real audio.
