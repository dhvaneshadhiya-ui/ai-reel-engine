# HeyGen production flow

Use HeyGen tools through the connected account. Never place API keys,
presigned upload URLs, or access tokens in project files or logs.

## Selection

1. Resolve the authorized private Digital Twin look.
2. Confirm the look's `supported_api_engines`.
3. Prefer Avatar V when supported; otherwise use Avatar IV.
4. Resolve the approved cloned voice from the account.

The engine currently documents the creator defaults in `PIPELINE.md`. Treat
those IDs as configuration, not secrets, and verify they still exist before a
credit-spending render.

## Native TTS flow

Create one continuous 1080p avatar master from the final script. Follow the
active HeyGen connector's required aspect-ratio field. For the current video
connector, a vertical reel request must explicitly use `9:16`; do not omit the
field or substitute an unsupported ratio.

- aspect ratio: connector-compliant and explicit (`9:16` for portrait reels);
- engine: Avatar V when supported;
- voice speed: `1.2`;
- captions: off;
- background: the approved Digital Twin look;
- motion prompt: natural direct-to-camera creator delivery, measured hand
  gestures, energetic but not theatrical.

Poll until complete, download immediately, and store as
`public/assets/<slug>/avatar-master.mp4`.

Before using a new avatar/aspect-ratio combination for a full production,
inspect a calibration frame. Measure the face center and safe headroom. If the
connector's portrait crop is poorly framed, keep the result in a fitted
portrait card/split treatment or use a connector-supported landscape request;
never silently stretch or crop out the face.

## Audio-driven flow — THIS IS THE DEFAULT (2026-08-27)

It was documented here for months as the exception, in prose, and never once
run. It is now the standard path: the voice is generated in ElevenLabs v3 and
HeyGen does lip-sync only. Reason, measured on one voice and one avatar:
**2.14 semitones through HeyGen TTS, 3.60 through ElevenLabs** at 0.998
speaker similarity. `tools/vo_external.py` automates step 2 and prints the
values for step 3.

**Step 2 is not optional.** The ElevenLabs download is refused by step 5 as
`application/octet-stream` unless it is re-encoded with metadata stripped —
twice, with two upload methods, on a file `file(1)` reports as audio/mpeg.

1. Generate or obtain the final voice WAV.
2. Convert it to a compatible MP3.
3. Create a HeyGen asset upload.
4. PUT the raw file bytes to the presigned URL with every returned header
   unchanged.
5. Complete the asset upload and poll until ready.
6. Create the avatar video from the audio asset.
7. Poll and download the clean result.

Audio-driven output can lip-sync less tightly. Keep facecam exposure short and
regenerate a visibly failed section. (Checked 2026-08-27 on a 58s master: the
avatar animates and gestures normally, audio duration is preserved to 16ms,
and pitch variation survives at 3.40 -> 3.31. Watch it anyway — a still frame
cannot show sync.)

**With uploaded audio, `voiceId`, `voiceSpeed`, `engine_settings` and HeyGen's
"Enhance voice" all stop applying.** Uploaded audio bypasses TTS entirely.
Pace is set in ElevenLabs, not by `speed`.

**The TTS flow below is now the FALLBACK** — set `voice.mode` to `heygen-tts`
in config.json. Its settings are left intact and correct for that path.

## Verification

- Extract a midpoint frame and measure face-center fraction.
- Save the fraction to `face-x.txt`; crop in Remotion.
- Extract 16 kHz mono audio and transcribe with word timestamps.
- Cross-check every number, date, product name, acronym, and CTA keyword.
- Never trust a new automatic crop without inspecting the calibration frame.
