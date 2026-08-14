# capture.mjs — premium B-roll capture (screenshots + screen recordings)

Playwright-based CLI that produces high-DPI screenshot "receipts" and smooth
scripted screen-recording clips of real websites for the reel engine.
Requires: `playwright` (installed as devDependency, chromium downloaded) and
`ffmpeg` on PATH (needed by `record` only).

```
node tools/capture.mjs <screenshot|record|probe> <url> [flags]
```

## screenshot — high-DPI PNG, no app chrome

```
node tools/capture.mjs screenshot https://github.com/anthropics/claude-code \
  --out out/dev-capture/readme-3x.png --scale 3 --selector "article.markdown-body"
```

Flags:
- `--out file.png` (required)
- `--scale 2|3` — deviceScaleFactor, default 3 (3x device pixels, razor-sharp for 1080x1920 zooms)
- `--width px` — viewport width in CSS px, default 1200
- `--height px` — viewport height, default 900 (only matters without `--selector/--full`)
- `--selector css` — capture just that element (auto-scrolls, captures the FULL element even if taller than the viewport). This is how you get zero browser/app chrome.
- `--full` — full-page capture
- `--wait ms` — extra settle time after load, default 2500
- `--hide "css,css"` — extra elements to hide (sticky navs, promo bars, ...)

Useful selectors: GitHub readme `article.markdown-body`; GitHub file table
`table.Table-module__Box__HZKiQ` (verify with `probe`); docs sites usually `main` or `article`.

Cookie/consent banners (OneTrust, Cookiebot, cookielaw, `[class*="cookie-banner"]`,
`[id*="consent-banner"]`, usercentrics, quantcast, ...) are auto-clicked/hidden
best-effort before shooting. If one survives, pass its selector via `--hide`.

Prints the saved path + pixel dimensions.

## record — smooth 30fps screen-recording clip (webm)

```
# Default: slow smooth scroll through the page for the duration
node tools/capture.mjs record https://github.com/anthropics/claude-code \
  --out out/dev-capture/readme-scroll.webm --duration 6

# Scripted choreography
node tools/capture.mjs record https://github.com/anthropics/claude-code \
  --out out/dev-capture/readme-scripted.webm --duration 5 --script actions.json
```

Flags:
- `--out file.webm` (required) — VP9 webm, constant 30fps, exactly `--duration` long
- `--duration s` — default 8
- `--width/--height` — viewport in CSS px, default 1280x800
- `--scale 2|3` — default 2; output video is `width*scale x height*scale` real pixels (2560x1600 by default)
- `--script file.json` — action script (below); without it, a gentle eased scroll (~220 content px/sec, short hold at both ends)
- `--wait`, `--hide` — same as screenshot

How it works (why it looks good): the recorder is deterministic — the
choreography advances exactly 1/30s per output frame (scroll eased in small
per-frame increments, mouse moves eased) and every frame is captured
individually. No dropped frames, no jank, recording starts on the settled page
(zero load-flash pre-roll). Capture runs slower than real time (~10x; a 6s clip
takes about a minute) — that's expected.

### Action script format

JSON array of actions. `t` = start time in seconds on the clip timeline.
`duration` = milliseconds. `px`/`x`/`y` are in UNSCALED CSS px of the page
(the same numbers `probe --scale 1` would report); selector targets are
resolved automatically at action time.

```json
[
  { "t": 0.3, "action": "move",   "selector": "article.markdown-body h1", "duration": 800 },
  { "t": 1.2, "action": "scroll", "px": 900, "duration": 2000 },
  { "t": 3.5, "action": "hover",  "selector": "article.markdown-body h2", "duration": 600 },
  { "t": 4.0, "action": "click",  "selector": ".btn-primary" },
  { "t": 4.5, "action": "type",   "selector": "input[name=q]", "text": "claude", "delay": 60 }
]
```

- `scroll` — smooth eased scroll by `px` (default 600) over `duration` (default 1500ms)
- `move` / `hover` — eased mouse travel to `selector` center or `x`/`y` (default 700ms)
- `click` — eased travel to target then click (default 150ms travel)
- `type` — types `text` one char per `delay` ms (default 55); clicks `selector` first to focus

## probe — pick focus regions without opening a browser

```
node tools/capture.mjs probe https://github.com/anthropics/claude-code --scale 3
```

Prints the page title plus bounding boxes (x/y/w/h in device px at the given
`--scale`) and suggested selectors for headings, images, tables, `article`,
`main`, `pre`, video — so a director can choose screenshot selectors and
annotation focus coordinates. Use `--scale 1` when authoring record scripts
(script coordinates are unscaled CSS px).

## Caveats

- **x.com / twitter.com block headless browsers — do not capture there.** Tweet
  receipts come from the existing YT-screen-recording flow.
- Page-intrinsic motion (autoplaying videos, GIFs, CSS loops) runs in real time
  while the recorder steps slower than real time, so it appears sped up in
  `record` clips. Fine for scroll B-roll; avoid recording pages whose hero IS a
  video.
- `record` needs `ffmpeg` (`brew install ffmpeg`) and always emits webm; convert
  with `ffmpeg -i in.webm -c:v libx264 -crf 16 out.mp4` if a comp needs H.264.
- Sites behind logins/paywalls render logged-out; some (rarely) bot-block —
  check output dimensions/first frames.
- Element screenshots of very tall nodes at 3x can exceed 7000px tall — that is
  expected and good for pan/zoom receipts.

## Verified sample assets

- `out/dev-capture/readme-3x.png` — 2274x6969, 3x, GitHub readme, chrome-free
- `out/dev-capture/readme-scroll.webm` — 2560x1600, 6s, 30fps smooth scroll
- `out/dev-capture/readme-scripted.webm` — 2560x1600, 5s, scripted move+scroll+hover
