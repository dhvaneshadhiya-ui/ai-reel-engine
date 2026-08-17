---
name: ffmpeg-ytdlp
description: Verified ffmpeg and yt-dlp recipes for audio/video work — loudness mastering to a broadcast target, frame extraction, concat, scaling to vertical, trimming without re-encode, and downloading/probing a video or its subtitles. Use whenever a task calls ffmpeg, ffprobe, or yt-dlp, or mentions LUFS, loudnorm, transcoding, muxing, "normalize audio", "extract a frame", "convert to 9:16", or grabbing a clip from YouTube. Read the ARCHITECTURE CHECK before the first ffmpeg call on macOS.
metadata:
  version: 1.0.0
---

# ffmpeg / ffprobe / yt-dlp

Recipes here are **measured, not remembered**. Where a number appears, it was
produced by running the command. Re-measure before trusting any of it on a new
machine or a new ffmpeg version.

---

## ARCHITECTURE CHECK — do this once per macOS machine

An **unsigned x86_64** ffmpeg on an **arm64** Mac is a live hazard: it runs under
Rosetta, and macOS may delete the binary the first time it executes — silently,
with no log entry. Verified on Darwin 25.3.0.

```bash
uname -m && file "$(which ffmpeg)" && ffmpeg -version | head -1
```

- `arm64` + `Mach-O ... arm64` → fine.
- `arm64` + `Mach-O ... x86_64` → replace it. Native is also **~40% faster**
  (measured: 6s of 1080x1920 libx264 `-preset medium`, 2.7s Rosetta vs 1.6s native).
- Native arm64 binaries **must** carry at least an adhoc signature to execute.
  Sign a downloaded one with `codesign --force -s - <binary>` (no certificate,
  no password needed).

**Never trust a path or package label for architecture — run `file`.** The npm
package `ffprobe-static` ships an **x86_64** binary inside a directory named
`arm64`. `@ffprobe-installer/ffprobe` and `ffmpeg-static` do ship real arm64.

The clean fix on Apple Silicon is Homebrew (`brew install ffmpeg`), which gives a
current, properly signed, native pair. Installing Homebrew asks for the user's
password, so it is **their** step to run, not yours.

---

## Loudness mastering — one pass undershoots, use two

`loudnorm` in a single pass does **not** reach its target. It is adaptive and
streaming, so it ends with a residual offset it never applies.

Measured on a 100.8s voice track, target `I=-14`:

| chain | integrated | gap |
|---|---|---|
| single pass | **-15.8 LUFS** | 1.8 LU short |
| two pass | **-14.7 LUFS** | 0.7 LU short |

Pass 1 even tells you the gap — it reports `target_offset` (1.79 in that run),
which is precisely the amount a single pass leaves on the table.

**Pass 1 — measure.** `print_format=json` prints at *info* level, so `-v error`
will hide it. This is the most common way this recipe silently fails:

```bash
ffmpeg -hide_banner -nostats -i in.wav -af loudnorm=I=-14:TP=-1.2:LRA=7:print_format=json -f null -
```

**Pass 2 — apply**, feeding back `input_i`/`input_tp`/`input_lra`/`input_thresh`
as `measured_*`, plus `offset`, with `linear=true`:

```bash
ffmpeg -v error -y -i in.wav -af "loudnorm=I=-14:TP=-1.2:LRA=7:measured_I=-24.66:measured_TP=-4.67:measured_LRA=4.40:measured_thresh=-35.06:offset=1.79:linear=true" -ar 48000 out.wav
```

In **zsh**, write `"${VAR}:linear=true"` — a bare `$VAR:l` is consumed as zsh's
lowercase modifier and the filter string arrives corrupted.

**Verify independently.** Do not report loudness from the filter that produced
it; measure the finished file with `ebur128`:

```bash
ffmpeg -nostats -i out.wav -filter_complex ebur128=peak=true -f null - 2>&1 | tail -14
```

Targets: -14 LUFS for YouTube/Spotify, roughly -14 for Instagram/TikTok, TP
-1.0 to -1.2 dBFS. Landing within ~1 LU is normal and acceptable.

---

## Common ffmpeg operations

**Trim without re-encoding** — put `-ss`/`-t` *before* `-i` for a fast seek;
cuts land on keyframes, so use the re-encoding form when the cut must be exact.

```bash
ffmpeg -v error -y -ss 12.5 -t 8 -i in.mp4 -c copy out.mp4
```

**Extract one frame** at a timestamp:

```bash
ffmpeg -v error -y -ss 3.2 -i in.mp4 -frames:v 1 -q:v 2 frame.jpg
```

**Scale and pad to vertical 1080x1920** without distorting:

```bash
ffmpeg -v error -y -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:a copy out.mp4
```

**Concat** files that share a codec (paths need escaping if they contain quotes):

```bash
printf "file '%s'\n" /abs/a.mp4 /abs/b.mp4 > /tmp/list.txt
ffmpeg -v error -y -f concat -safe 0 -i /tmp/list.txt -c copy out.mp4
```

**Replace the audio** of a video, keeping video untouched and ending at the
shorter stream:

```bash
ffmpeg -v error -y -i video.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4
```

**Probe** duration or dimensions as a bare value:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 in.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 in.mp4
```

**Check a filter or encoder exists before depending on it** — static builds vary
in what is compiled in, and a missing filter fails at render time, not now:

```bash
ffmpeg -hide_banner -filters | grep -E "loudnorm|drawtext|subtitles"
ffmpeg -hide_banner -encoders | grep libx264
```

`drawtext` and `subtitles` are the two most often absent from minimal builds.

---

## yt-dlp

**Probe before downloading.** `--simulate` costs nothing and confirms the URL,
title, and length:

```bash
yt-dlp --no-warnings --simulate --print "%(title)s | %(duration)ss | %(resolution)s" "<url>"
```

**List formats**, then pick deliberately rather than trusting a guess:

```bash
yt-dlp -F "<url>"
```

**Download** best video+audio muxed to mp4 (needs ffmpeg on PATH for the merge):

```bash
yt-dlp -f "bv*+ba/b" --merge-output-format mp4 -o "%(title).80s.%(ext)s" "<url>"
```

**Audio only**, for transcription:

```bash
yt-dlp -f ba -x --audio-format wav -o "%(id)s.%(ext)s" "<url>"
```

**Subtitles / transcript without the video** — often all a research task needs,
and far cheaper than downloading the media:

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --convert-subs srt -o "%(id)s" "<url>"
```

**A specific span only**, without pulling the whole file:

```bash
yt-dlp --download-sections "*00:01:12-00:01:40" -f "bv*+ba/b" --merge-output-format mp4 "<url>"
```

Keep yt-dlp current — extractors break when sites change, and a stale copy fails
in confusing ways:

```bash
python3 -m pip install --user --upgrade yt-dlp
```

### Before downloading anything

Downloading third-party media is a rights question, not just a technical one.
Prefer official press assets and first-party sources. When a project has a
source-capture or attribution policy, follow it: credit on screen, use only
short excerpts, and never re-publish someone's footage as your own. If a
download is not clearly covered by fair use or a licence, ask the user rather
than assuming.

---

## Debugging habits that repeatedly pay off

1. **A check that cannot fail is not a check.** If a grep-based verification
   prints nothing, the pattern is wrong — treat empty output as a failed test,
   never as a pass.
2. **Measure the artifact, not the intent.** Read loudness, duration, and
   dimensions off the finished file with `ffprobe`/`ebur128`.
3. **`-v error` hides filter statistics.** Any recipe that reads numbers out of
   ffmpeg's own output needs `-hide_banner -nostats` instead.
4. **Verify a swap before adopting it.** When replacing an ffmpeg build, run the
   real chain through both and compare measured output. A version difference that
   changes nothing is safe; one that shifts loudness is not.
