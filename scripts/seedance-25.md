# seedance-25 — script + shot plan (varun-mayya)

Target ~45s @ HeyGen speed 1.2. 163 words.
Every beat below binds to a manifest asset id or `MG:` spec. No beat is unbound.

---

## Script (as spoken — this exact text goes to HeyGen)

The company that owns TikTok just shipped an AI that generates thirty seconds
of video and its own soundtrack in a single pass.

It's called Seedance 2.5. The developer API opened last Friday.

The old version capped out at fifteen seconds. Google's newest video model
tops out around ten. This one runs thirty, then extends.

But here's the part almost nobody noticed.

You can feed it fifty reference assets in one job. Thirty images, ten video
clips, and ten audio tracks. The old model took nine images and three clips.

And that audio slot is the real unlock. Hand it a song and it cuts to the
beat. Hand it a voice and it syncs the lips — in a dozen languages, from the
same shot.

Now, ByteDance hasn't published a single benchmark number. So every clip
you've seen is a demo they chose.

Still — thirty seconds, one pass, with sound. That's a whole ad. Would you
trust it with a client's brief?

---

## Beat map

| # | anchor phrase (VO) | ~dur | visual | treatment |
|---|---|---|---|---|
| 1 | "owns TikTok" | 2.0 | `logo-tiktok` + `clip-train-window` + face | **brandhook** — TikTok mark draws on in brand pink, giant "SEEDANCE 2.5", moving window, facecam card. Face on screen by s1. |
| 2 | "thirty seconds of video" | 2.1 | `clip-jellyfish` | footage, zoom in |
| 3 | "in a single pass" | 2.1 | `clip-porthole-girl` | footage, zoom out — payoff frame, plays clean |
| 4 | "opened last Friday" | 2.8 | `card-keynote` | **floatcard** (framed 16:9) + display headline "API LIVE / AUG 7" |
| 5 | "tops out around ten" | 3.2 | MG:specsheet | columns ["MAX CLIP", "IN ONE PASS"], rows Seedance 2.0 / Gemini Omni Flash / Seedance 2.5 (accent). bgSrc `clip-debris-bw` |
| 6 | "runs thirty" | 1.5 | `clip-forest-stream` | footage |
| 7 | "then extends" | 1.4 | `clip-clouds-plane` | footage |
| 8 | "nobody noticed" | 1.8 | avatar | facecam — the bridge, spoken to camera |
| 9 | "fifty reference assets" | 2.2 | `clip-refs-fan` | footage — literally the reference fan in the UI |
| 10 | "ten audio tracks" | 3.0 | MG:specsheet | columns ["2.0", "2.5"], rows Images 9/30, Video clips 3/10, Audio tracks 0/10 (accent) |
| 11 | "nine images and three clips" | 2.3 | `clip-ballroom-group` | footage — the result those references produced |
| 12 | "cuts to the beat" | 2.4 | `clip-red-dress` | footage — dance cut on music |
| 13 | "syncs the lips" | 2.2 | `clip-lipsync-en` | footage |
| 14 | "a dozen languages" | 2.6 | `clip-lipsync-en` + `clip-lipsync-jp` | **comparesplit** — EN / 日本語 labels, same shot both sides |
| 15 | "from the same shot" | 2.2 | `clip-lipsync-jp` | footage |
| 16 | "single benchmark number" | 2.2 | avatar | facecam — the honesty beat is an on-camera opinion |
| 17 | "a demo they chose" | 2.6 | MG:wordcascade (cream) | "no published benchmark." / "no third-party eval." / "not yet." |
| 18 | "That's a whole ad" | 1.8 | `clip-space` | footage — spectacle |
| 19 | "one pass, with sound" | 1.8 | avatar | facecam |
| 20 | "a client's brief?" | 1.9 | avatar + headline | facecam + CTA question |

**Validation gate — PASSED.** All 20 beats resolve: 13 to manifest asset ids,
4 to the avatar master, 3 to MG components that need no sourcing.

Treatment check vs STYLE-RULES history: no plain black typecard (banned).
New treatments this reel: **comparesplit used for a language pair**, and a
**specsheet whose accent row is a competitor comparison with units**. Neither
appears in the logged history (indiaai-gpu / kimi-india / ibm-rehiring /
model-wave).

## Honesty note

The 4K demos in the source are Seedance **2.0** marketing and are excluded —
see `banned_frames` in the manifest. Beat 16-17 states plainly that no
benchmark exists rather than implying a ranking the sources do not support.
