# Digital twin — recording spec

Written 2026-08-13 after the first twin (`8e49c9d1`, "Dhvanesh -- 55") came
back unusable for reels. It cost ~337 credits. Read this before recording the
next one.

## What the first twin proved — the good news

**A digital twin BREAKS the fixed-smile problem.** Measured on the identical
three-register probe used against the photo avatar: the twin's face stays
neutral and level through the caveat instead of grinning. Photo avatars cannot
do this at any `expressiveness` setting (proven 2026-08-12). So the twin route
is worth pursuing — this spec is about doing it right, not abandoning it.

## Why the first one failed

| Defect | Measured | Why it matters |
|---|---|---|
| **Branding burned in** | "iGeeksBlog" lower-third + social icons in **19 of 19** sampled frames; a SUBSCRIBE button too | Permanent, un-removable, and it collides with our own captions and credits |
| **Resolution / aspect** | render 1280x640, source 1440x720 — both **2:1** | Reels are 1080x1920. A 9:16 crop from 640px height is 360x640 and needs a ~3x upscale |
| **Frame rate** | 25 fps | The project is 30 fps |
| **No hands** | head-and-shoulders framing; motion **1.71 = stiff** | Hands are outside the frame, so gestures are impossible no matter what `motionPrompt` says |

Root cause of the first three: **it was trained on a PUBLISHED, EDITED video**
rather than raw camera footage.

## Recording spec for the retrain

### Absolutely required

1. **RAW footage only.** No watermark, no logo bug, no lower-third, no
   subscribe button, no end-card, no burned-in captions, no B-roll cutaways,
   no jump cuts, no zoom-in edits. Straight out of the camera.
2. **16:9, 1080p minimum** (4K preferred — it survives the 9:16 crop).
   **NOT 2:1 / cinematic / letterboxed.**
3. **30 fps** to match the project.
4. **Waist-up framing, hands visible and gesturing.** This is the single
   biggest fix: the current twin physically cannot gesture. Leave headroom and
   space either side of the torso so the 9:16 crop keeps the hands.
5. **Hands empty the whole time** — no pen, no phone, no papers, no props.
   Same permanent rule as `config.json` -> `avatar.motionPrompt`.

### Strongly recommended

6. **2-5 minutes of continuous delivery**, static camera, even lighting, plain
   or simple background.
7. **Cover all three registers in the take**, because the source footage sets
   the expressive range:
   - ~1 min explaining something neutrally (level brows, no smile)
   - ~1 min on a caveat or a warning (serious, concerned)
   - ~1 min warm and positive (genuine smile, enthusiasm)
   - include natural gestures: open palms, counting on fingers, a small
     forward lean on a key number
8. Look straight down the lens. No reading visibly off a side monitor.
9. Same wardrobe/room as you would want on screen — this becomes the look.

## After the twin is created — measure, do not assume

```bash
# 1. framing + resolution, before spending anything else
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate \
  -of csv=p=0 <clip>

# 2. motion  (<1.0 frozen · 1.0-2.5 stiff · 3+ gestures)
python3 tools/measure_avatar.py score <clip> --register <lookId>
```

3. Spend ~3 credits on the standard three-register probe and read a face-crop
   strip at <=0.5s spacing, plus a hand-region strip at <=0.5s spacing for
   props. The probe script, used for every avatar so results are comparable:

   > SuperGrok Heavy is three hundred dollars a month. Now, here is the honest
   > problem. The launch material does not explain credential handling, or
   > permission scope. So, would you hand it your passwords?

4. Only then set `register` and `engine` in `config.json` -> `avatarRegistry`.

**`avatar_v` + `motionPrompt` is available now** — the API accepts it once the
group contains a digital twin, which was the blocker that forced `avatar_iv`
on 2026-08-11. Test both engines on the retrained twin and register whichever
measures higher.

## Budget note

Twin training is expensive: credits went 436 -> 92 (~337) on 2026-08-13, with
a reset on 2026-08-22. **Check `get_current_user` before training another
one**, and do not retrain until the footage meets every "absolutely required"
item above — a second bad twin costs the same as a good one.
