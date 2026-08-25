#!/usr/bin/env node
/**
 * capture.mjs — premium B-roll capture tool for the news-reels engine.
 *
 * Subcommands:
 *   screenshot <url> --out file.png [--scale 3] [--width 1200] [--height 900]
 *                    [--selector css] [--full] [--wait 2500] [--hide css,css]
 *   record     <url> --out file.webm [--duration 8] [--width 1280] [--height 800]
 *                    [--scale 2] [--wait 2500] [--script actions.json] [--hide css,css]
 *   probe      <url> [--scale 3] [--width 1200] [--wait 2500]
 *
 * Produces high-DPI screenshots (deviceScaleFactor 2/3) and smooth scripted
 * screen recordings of real websites, with best-effort cookie-banner removal.
 */

import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawnSync } from "node:child_process";

// ---------------------------------------------------------------- arg parsing

const [, , cmd, url, ...rest] = process.argv;

function usage(exit = 1) {
  console.error(`Usage:
  node tools/capture.mjs screenshot <url> --out shot.png [--scale 3] [--width 1200] [--height 900] [--selector "article"] [--full] [--wait 2500] [--hide "css,css"]
  node tools/capture.mjs record     <url> --out clip.webm [--duration 8] [--width 1280] [--height 800] [--scale 2] [--script actions.json] [--wait 2500] [--hide "css,css"]
  node tools/capture.mjs probe      <url> [--scale 3] [--width 1200] [--wait 2500]
  node tools/capture.mjs batch      <plan.json> [--workers 4]

BATCH takes a plan — an array of {url, out, ...flags} — and captures them with
ONE browser instead of one per asset. Measured 2026-08-19: a single invocation
costs 1.2-1.5s of node+chromium startup before any network, and a reel scouts
22-51 assets, so the launches alone were a minute of pure overhead on top of
running them one at a time.

MOBILE IS THE DEFAULT (360x780 @3 = 1080x2340) because every reel is 9:16.
Record where the source came from:
  --tier official|reliable|fallback   which tier this source is (see TIERS below)
  --desktop-reason "<why>"            required with --desktop: mobile could not show it

Pass --desktop for pages with no mobile layout, wide dashboards, or
side-by-side comparisons.`);
  process.exit(exit);
}

if (!cmd || !["screenshot", "record", "probe", "batch"].includes(cmd)) usage();
if (cmd !== "batch" && !url) usage();

const flags = {};
for (let i = 0; i < rest.length; i++) {
  const a = rest[i];
  if (!a.startsWith("--")) usage();
  const key = a.slice(2);
  const boolFlags = new Set(["full", "mobile", "desktop", "no-cursor"]);
  // --tier and --desktop-reason take VALUES, so they must not be bool flags.
  if (boolFlags.has(key)) {
    flags[key] = true;
  } else {
    flags[key] = rest[++i];
    if (flags[key] === undefined) usage();
  }
}

const num = (v, d) => (v === undefined ? d : Number(v));

/*
 * MOBILE IS THE DEFAULT (2026-08-13, user request).
 *
 * This engine only ever ships 9:16. A desktop capture at 1200x900 cropped to
 * 9:16 keeps a 675px-wide sliver of a layout designed for 1200 — most of the
 * page is thrown away and the surviving text is tiny on a phone. A real mobile
 * viewport is already tall and narrow, its type is sized for a hand, and at
 * DPR 3 it lands at 1080x2340 — a native fit for a 1080x1920 frame with room
 * to pan.
 *
 * 360x780 @ scale 3 = 1080x2340 exactly. Pass --desktop to opt out (product
 * pages with no mobile layout, wide dashboards, side-by-side comparisons).
 */
const MOBILE = !flags.desktop;   // --desktop opts out; --mobile is redundant but accepted

const opts = {
  out: flags.out,
  mobile: MOBILE,
  scale: num(flags.scale, MOBILE ? 3 : cmd === "record" ? 2 : 3),
  width: num(flags.width, MOBILE ? 360 : cmd === "record" ? 1280 : 1200),
  height: num(flags.height, MOBILE ? 780 : cmd === "record" ? 800 : 900),
  wait: num(flags.wait, 2500),
  duration: num(flags.duration, 8),
  selector: flags.selector,
  full: !!flags.full,
  hide: flags.hide ? flags.hide.split(",").map((s) => s.trim()).filter(Boolean) : [],
  script: flags.script,
  tier: flags.tier,
  desktopReason: flags["desktop-reason"],
};

/**
 * SOURCE TIER, recorded at capture time.
 *
 * The rule (2026-08-14): look for the EXACT thing being said, official source
 * first; if it is not there — and for an unannounced product it usually is not —
 * an established outlet with a named reporter is expected, not a failure; only
 * then something merely relevant.
 *
 *   official   the maker's own newsroom, spec page, keynote
 *   reliable   established outlet, named reporter
 *   fallback   merely relevant. Recorded so it can be counted and argued with.
 *
 * Recorded HERE because the operator knows which it is at the moment they paste
 * the URL, and nobody can recover it from the pixels afterwards.
 */
const TIERS = new Set(["official", "reliable", "fallback"]);
if (opts.tier && !TIERS.has(opts.tier)) {
  console.error(`error: --tier must be one of ${[...TIERS].join(" | ")}`);
  process.exit(1);
}

if ((cmd === "screenshot" || cmd === "record") && !opts.out) {
  console.error(`error: --out is required for ${cmd}`);
  usage();
}

// ------------------------------------------------------------------- helpers

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Best-effort cookie/consent banner cleanup: click accept-ish buttons, then hide leftovers. */
async function dismissBanners(page, extraHide = []) {
  // 1) Try clicking well-known accept buttons (short timeouts; ignore failures).
  const clickTargets = [
    "#onetrust-accept-btn-handler",
    "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
    "button#accept-cookies",
    '[data-testid="cookie-banner-accept"]',
    ".cc-allow",
    ".cc-btn.cc-dismiss",
    '[aria-label="Accept cookies"]',
    '[aria-label="Accept all cookies"]',
  ];
  for (const sel of clickTargets) {
    try {
      const el = page.locator(sel).first();
      if (await el.isVisible({ timeout: 250 })) {
        await el.click({ timeout: 1000 });
        await sleep(300);
      }
    } catch {}
  }

  // 2) Nuke common banner containers + any user-supplied selectors with CSS.
  const hideSelectors = [
    "#onetrust-consent-sdk",
    "#onetrust-banner-sdk",
    ".onetrust-pc-dark-filter",
    "#CybotCookiebotDialog",
    "#CybotCookiebotDialogBodyUnderlay",
    "#cookie-banner",
    "#cookie-notice",
    "#cookieConsent",
    ".cookie-banner",
    ".cookie-notice",
    ".cookie-consent",
    '[class*="cookie-banner"]',
    '[id*="cookie-banner"]',
    '[class*="cookieBanner"]',
    '[class*="consent-banner"]',
    '[id*="consent-banner"]',
    '[class*="gdpr-banner"]',
    ".cc-window",
    ".qc-cmp2-container",
    "#usercentrics-root",
    "#sp_message_container",
    '[class*="js-consent-banner"]',
    ...extraHide,
  ];
  try {
    await page.addStyleTag({
      content: hideSelectors
        .map((s) => `${s}{display:none !important;visibility:hidden !important;}`)
        .join("\n"),
    });
  } catch {}
}

async function newBrowser() {
  return chromium.launch({
    headless: true,
    args: ["--hide-scrollbars", "--force-color-profile=srgb", "--disable-blink-features=AutomationControlled"],
  });
}

const DESKTOP_UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";
const MOBILE_UA =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1";

// isMobile makes Chromium honour the page's meta-viewport, which is what
// actually triggers the mobile LAYOUT — a narrow window alone does not.
const CONTEXT_BASE = {
  userAgent: opts.mobile ? MOBILE_UA : DESKTOP_UA,
  locale: "en-US",
  reducedMotion: "no-preference",
  colorScheme: "light",
  ...(opts.mobile ? { isMobile: true, hasTouch: true } : {}),
};

async function settle(page, pageUrl = url, o = opts) {
  await page.goto(pageUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForLoadState("load", { timeout: 20000 }).catch(() => {});
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await dismissBanners(page, o.hide);
  // Nudge lazy-loaded images near the top of the page into loading.
  await page.evaluate(() => {
    document.querySelectorAll('img[loading="lazy"]').forEach((img) => (img.loading = "eager"));
  }).catch(() => {});
  await sleep(o.wait);
}

function pngDimensions(file) {
  const buf = fs.readFileSync(file);
  // PNG IHDR: width @ byte 16, height @ byte 20 (big-endian).
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

/**
 * Write a provenance sidecar next to the captured file.
 *
 * G29 has been inferring "was this captured on mobile?" from the IMAGE ASPECT —
 * a portrait picture is assumed to be a phone capture. That proxy cannot tell a
 * real 360x780 mobile render from a tall crop of a desktop page, and it says
 * nothing at all about WHERE the source came from. Recording it at capture time
 * turns Rule 2 and the tier rule from inferences into facts.
 */
function writeProvenance(outPath, url, o, cmd) {
  const rec = {
    url,
    kind: cmd,
    capturedAt: new Date().toISOString(),
    viewport: { width: o.width, height: o.height, scale: o.scale },
    mobile: !!o.mobile,
    tier: o.tier || null,
    desktopReason: o.mobile ? null : (o.desktopReason || null),
  };
  const side = outPath.replace(/\.[^.]+$/, "") + ".capture.json";
  fs.writeFileSync(side, JSON.stringify(rec, null, 2) + "\n");
  const warn = [];
  if (!rec.tier) warn.push("no --tier recorded");
  if (!rec.mobile && !rec.desktopReason) warn.push("--desktop with no --desktop-reason");
  console.log(`provenance ${path.resolve(side)}${warn.length ? "  [" + warn.join("; ") + "]" : ""}`);
}


function ensureOutDir(file) {
  fs.mkdirSync(path.dirname(path.resolve(file)), { recursive: true });
}

// -------------------------------------------------------------- screenshot

async function screenshot() {
  ensureOutDir(opts.out);
  const browser = await newBrowser();
  const context = await browser.newContext({
    ...CONTEXT_BASE,
    viewport: { width: opts.width, height: opts.height },
    deviceScaleFactor: opts.scale,
  });
  const page = await context.newPage();
  await settle(page);

  if (opts.selector) {
    const el = page.locator(opts.selector).first();
    await el.waitFor({ state: "visible", timeout: 15000 });
    await el.scrollIntoViewIfNeeded();
    await sleep(400);
    await el.screenshot({ path: opts.out, type: "png" });
  } else {
    await page.screenshot({ path: opts.out, type: "png", fullPage: opts.full });
  }

  await browser.close();
  const { w, h } = pngDimensions(opts.out);
  console.log(`saved ${path.resolve(opts.out)}  ${w}x${h}px  (scale ${opts.scale}x)`);
  writeProvenance(opts.out, url, opts, "screenshot");
}

// ------------------------------------------------------------------- batch
//
// WHY (measured 2026-08-19, answering "why does a reel take two hours")
// Scouting was the largest hand stage and the only one still running strictly
// one asset at a time: `capture.mjs screenshot <url>` launches Chromium, takes
// one picture and closes it. Reels carry 22-51 assets.
//
//     fixed cost per invocation   1.2-1.5s   (node + chromium, no network)
//     assets per reel             22-51
//
// So the launches alone were ~60s, and every page's network wait was serialised
// behind the one before it. One browser, N pages in parallel, same per-asset
// provenance — the tier and desktop-reason rules are unchanged, because those
// are Rule 2 and a faster tool must not make them easier to skip.

async function batch() {
  const planPath = url;                       // second positional arg
  const plan = JSON.parse(fs.readFileSync(planPath, "utf8"));
  if (!Array.isArray(plan)) {
    console.error("batch: plan must be a JSON array of {url, out, ...} items");
    process.exit(1);
  }
  const workers = Math.max(1, Number(flags.workers || 4));
  const browser = await newBrowser();
  let done = 0, failed = 0;
  const started = Date.now();

  const queue = plan.slice();
  async function drain() {
    for (;;) {
      const item = queue.shift();
      if (!item) return;
      const o = { ...opts, ...item };          // item flags override defaults
      try {
        ensureOutDir(o.out);
        const context = await browser.newContext({
          ...CONTEXT_BASE,
          viewport: { width: o.width, height: o.height },
          deviceScaleFactor: o.scale,
        });
        const page = await context.newPage();
        // The SAME settle() the single-shot path uses — lazy-image nudge,
        // banner dismissal, network idle. A batch that reimplements it would
        // drift from it, and then a page would capture differently depending
        // on which command took it.
        await settle(page, item.url, o);
        if (o.selector) {
          const el = page.locator(o.selector).first();
          await el.waitFor({ state: "visible", timeout: 15000 });
          await el.scrollIntoViewIfNeeded();
          await sleep(400);
          await el.screenshot({ path: o.out, type: "png" });
        } else {
          await page.screenshot({ path: o.out, type: "png", fullPage: !!o.full });
        }
        await context.close();
        const { w, h } = pngDimensions(o.out);
        console.log(`  ok    ${o.out}  ${w}x${h}`);
        writeProvenance(o.out, item.url, o, "screenshot");
        done++;
      } catch (e) {
        // One bad URL must not take the other fifty with it.
        console.error(`  FAIL  ${item.out}  ${String(e).split("\n")[0].slice(0, 90)}`);
        failed++;
      }
    }
  }

  await Promise.all(Array.from({ length: workers }, drain));
  await browser.close();
  const secs = ((Date.now() - started) / 1000).toFixed(0);
  console.log(`\n  ${done} captured, ${failed} failed, ${secs}s with ${workers} workers ` +
              `(one browser, not ${plan.length}).`);
  if (failed) process.exitCode = 1;
}

// ------------------------------------------------------------------ record
//
// Deterministic frame-stepped recorder. Real-time screen capture at hi-DPI sizes
// tops out at ~4-5 fps (surface readback cost), which reads as janky B-roll.
// Instead we advance the choreography EXACTLY 1/30s per output frame — scroll
// positions and mouse moves are eased in small per-frame increments — and grab a
// CDP screenshot for every frame. Capture runs slower than real time, but the
// resulting clip is perfectly smooth 30fps with zero dropped frames.

const FPS = 30;
const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

async function centerOf(page, selector) {
  const box = await page.locator(selector).first().boundingBox();
  if (!box) throw new Error(`record: selector not found/visible: ${selector}`);
  return { x: box.x + box.width / 2, y: box.y + box.height / 2 };
}

/**
 * Normalize a raw script entry. Times are seconds; px/x/y are authored in
 * css px of the page (the numbers you would use at --scale 1) and are used
 * AS-IS: since 2026-08-25 the recording viewport is real CSS size with
 * deviceScaleFactor carrying the detail, so mouse, scroll and selector
 * coordinates all live in one space. Selector targets are resolved lazily at
 * the action's start frame (post-scroll layout).
 */
function normalizeAction(a, S) {
  const durDefault = { scroll: 1.5, move: 0.7, hover: 0.7, click: 0.15, type: 0 }[a.action] ?? 0.5;
  return {
    ...a,
    t: a.t ?? 0,
    dur: a.duration != null ? a.duration / 1000 : durDefault, // script durations are ms
    px: a.px,
    x: a.x,
    y: a.y,
    started: false,
    done: false,
  };
}

async function record() {
  ensureOutDir(opts.out);
  const S = opts.scale;
  // EVEN PHYSICAL DIMENSIONS. VP9 accepts odd sizes, so a recording looked
  // fine here and then h264 refused it at the mp4 conform ("height not
  // divisible by 2", 2026-08-25) — the failure landed a step away from its
  // cause. Nudge the CSS viewport instead, so it can never reach ffmpeg odd.
  for (const dim of ["width", "height"]) {
    if ((opts[dim] * S) % 2 !== 0) {
      opts[dim] += 1;
      console.warn(`record: ${dim} ${opts[dim] - 1}x${S} is odd — using ` +
                   `${opts[dim]} so h264 can encode the conform`);
    }
  }
  const videoW = opts.width * S;
  const videoH = opts.height * S;
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "capture-video-"));

  // Real DPR, never CSS zoom (2026-08-25). The old "Hi-DPI trick" set the
  // viewport to width*scale CSS px and zoomed the root — so every media query
  // saw a 1080px viewport and responsive sites (GitHub) applied their DESKTOP
  // breakpoint squeezed into 360 effective px: overlapping columns, mangled
  // layout, found on the claude-eating-tokens repo recordings. Screenshot
  // mode always did it right; this now matches it: 360x780 CSS viewport,
  // deviceScaleFactor 3 → CDP captures 1080x2340 physical px natively, and
  // every coordinate (mouse, scroll, cursor overlay) is uniformly CSS px.
  const browser = await newBrowser();
  const context = await browser.newContext({
    ...CONTEXT_BASE,
    viewport: { width: opts.width, height: opts.height },
    deviceScaleFactor: S,
  });
  const page = await context.newPage();
  await settle(page);

  // VISIBLE CURSOR (2026-08-25). page.mouse moves the real pointer but Chrome
  // paints nothing for it, so every recording to date had invisible clicks.
  // The ai-tools teardown (formats/ai-tools.md, observation study) found the
  // live cursor is load-bearing in the genre: the viewer follows it to the
  // button, the scroll, the field. Injected as a fixed SVG arrow with a soft
  // shadow + a pulse ring on click; --no-cursor restores the old behaviour.
  // Coordinates: mouse.x/y and the fixed cursor element share one CSS-px
  // space now that the viewport is real-size (no zoom, DPR carries detail).
  const showCursor = !flags["no-cursor"];
  if (showCursor) {
    await page.evaluate(() => {
      const c = document.createElement("div");
      c.id = "__cap_cursor";
      c.style.cssText = "position:fixed;left:0;top:0;z-index:2147483647;" +
        "pointer-events:none;width:44px;height:64px;transition:none;" +
        "filter:drop-shadow(0 2px 5px rgba(0,0,0,.45));display:none;";
      c.innerHTML = '<svg viewBox="0 0 26 38" width="44" height="64">' +
        '<path d="M2 1 L2 30 L9 24 L14 36 L19 34 L14 22 L23 22 Z" ' +
        'fill="#fff" stroke="#111" stroke-width="1.6"/></svg>';
      const ring = document.createElement("div");
      ring.id = "__cap_ring";
      ring.style.cssText = "position:fixed;z-index:2147483646;" +
        "pointer-events:none;width:14px;height:14px;border-radius:50%;" +
        "border:3px solid rgba(37,99,235,.9);opacity:0;transition:none;";
      document.documentElement.append(c, ring);
    });
  }
  const paintCursor = async (mx, my, ringP = null) => {
    if (!showCursor) return;
    await page.evaluate(([x, y, s, rp]) => {
      const c = document.getElementById("__cap_cursor");
      if (!c) return;
      c.style.display = "block";
      c.style.left = x + "px";
      c.style.top = y + "px";
      const r = document.getElementById("__cap_ring");
      if (r) {
        if (rp === null) { r.style.opacity = "0"; }
        else {
          const grow = 14 + rp * 30;
          r.style.width = r.style.height = grow + "px";
          r.style.left = (x - grow / 2 + 3) + "px";
          r.style.top = (y - grow / 2 + 2) + "px";
          r.style.opacity = String(0.9 * (1 - rp));
        }
      }
    }, [mx, my, S, ringP]);
  };
  let ringT = -1; // seconds since last click, -1 = no ring

  // Build the timeline.
  let actions;
  if (opts.script) {
    const raw = JSON.parse(fs.readFileSync(opts.script, "utf8"));
    actions = raw.map((a) => normalizeAction(a, S)).sort((x, y) => x.t - y.t);
  } else {
    // Default: hold, one continuous slow scroll through the page, hold.
    const scrollable = await page.evaluate(
      () => document.documentElement.scrollHeight - window.innerHeight
    );
    const hold = Math.min(0.8, opts.duration * 0.1);
    const scrollDur = opts.duration - 2 * hold;
    const px = Math.max(0, Math.min(scrollable, scrollDur * 220 * S)); // ~220 content px/sec
    actions = px > 0 ? [{ action: "scroll", t: hold, dur: scrollDur, px, started: false, done: false }] : [];
  }

  const cdp = await context.newCDPSession(page);
  const totalFrames = Math.round(opts.duration * FPS);
  let scrollBase = await page.evaluate(() => window.scrollY);
  let mouse = { x: 0, y: 0 };
  let mouseDirty = false;

  for (let k = 0; k < totalFrames; k++) {
    const t = k / FPS;
    let scrollY = scrollBase;

    for (const a of actions) {
      if (a.done || t < a.t) continue;
      if (!a.started) {
        a.started = true;
        // Resolve lazily so selector coordinates reflect the current scroll.
        if ((a.action === "move" || a.action === "hover" || a.action === "click") ) {
          if (a.selector) {
            const c = await centerOf(page, a.selector);
            a.tx = c.x; a.ty = c.y;
          } else { a.tx = a.x; a.ty = a.y; }
          a.fx = mouse.x; a.fy = mouse.y;
        }
        if (a.action === "scroll") a.from = scrollY;
        if (a.action === "type") {
          if (a.selector) await page.locator(a.selector).first().click();
          a.chars = [...(a.text ?? "")];
          a.typed = 0;
          a.delay = (a.delay ?? 55) / 1000;
        }
      }
      const p = a.dur > 0 ? Math.min(1, (t - a.t) / a.dur) : 1;
      switch (a.action) {
        case "scroll":
          scrollY = a.from + a.px * easeInOutCubic(p);
          scrollBase = scrollY;
          if (p >= 1) a.done = true;
          break;
        case "move":
        case "hover": {
          const e = easeInOutCubic(p);
          const nx = a.fx + (a.tx - a.fx) * e;
          const ny = a.fy + (a.ty - a.fy) * e;
          if (nx !== mouse.x || ny !== mouse.y) { mouse = { x: nx, y: ny }; mouseDirty = true; }
          if (p >= 1) a.done = true;
          break;
        }
        case "click": {
          const e = easeInOutCubic(p);
          mouse = { x: a.fx + (a.tx - a.fx) * e, y: a.fy + (a.ty - a.fy) * e };
          mouseDirty = true;
          if (p >= 1) { await page.mouse.click(a.tx, a.ty); ringT = 0; a.done = true; }
          break;
        }
        case "type": {
          const want = Math.min(a.chars.length, Math.floor((t - a.t) / Math.max(a.delay, 1 / FPS)) + 1);
          while (a.typed < want) await page.keyboard.type(a.chars[a.typed++]);
          if (a.typed >= a.chars.length) a.done = true;
          break;
        }
        default:
          console.warn(`record: unknown action "${a.action}" — skipped`);
          a.done = true;
      }
    }

    await page.evaluate((y) => window.scrollTo(0, y), scrollY);
    if (mouseDirty) { await page.mouse.move(mouse.x, mouse.y); mouseDirty = false; }
    if (ringT >= 0) { ringT += 1 / FPS; if (ringT > 0.45) ringT = -1; }
    await paintCursor(mouse.x, mouse.y, ringT >= 0 ? ringT / 0.45 : null);

    // Playwright screenshot with scale:"device", never raw CDP: CDP's
    // Page.captureScreenshot returns CSS-pixel frames and silently ignores
    // the context's deviceScaleFactor — the "1080x2340" recordings it saved
    // were actually 360x780 (found 2026-08-25 by ffprobe, after the log's
    // computed dimensions had claimed otherwise for a full scout session).
    const shot = await page.screenshot({
      type: "jpeg",
      quality: 92,
      scale: "device",
      animations: "allow",
    });
    fs.writeFileSync(path.join(tmpDir, `f-${String(k).padStart(5, "0")}.jpg`), shot);
  }

  await browser.close();

  const ff = spawnSync(
    "ffmpeg",
    [
      "-y", "-v", "error",
      "-framerate", String(FPS),
      "-i", path.join(tmpDir, "f-%05d.jpg"),
      "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "26", "-deadline", "good", "-cpu-used", "4",
      "-pix_fmt", "yuv420p",
      "-an",
      path.resolve(opts.out),
    ],
    { stdio: "inherit" }
  );
  if (ff.status !== 0) {
    throw new Error("record: ffmpeg is required to assemble the video (brew install ffmpeg)");
  }
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log(
    `saved ${path.resolve(opts.out)}  ${videoW}x${videoH}px  ${opts.duration}s @ ${FPS}fps  (scale ${S}x, ${totalFrames} frames)`
  );
}

// ------------------------------------------------------------------- probe

async function probe() {
  const browser = await newBrowser();
  const context = await browser.newContext({
    ...CONTEXT_BASE,
    viewport: { width: opts.width, height: opts.height },
    deviceScaleFactor: 1, // measure in CSS px, then report scaled
  });
  const page = await context.newPage();
  await settle(page);

  const title = await page.title();
  const items = await page.evaluate(() => {
    const out = [];
    const seen = new Set();
    const nodes = document.querySelectorAll(
      "h1, h2, h3, article, main, table, img, [role='article'], .markdown-body, video, pre"
    );
    const cssFor = (el) => {
      if (el.id) return `#${CSS.escape(el.id)}`;
      const tag = el.tagName.toLowerCase();
      const cls = [...el.classList].slice(0, 2).map((c) => `.${CSS.escape(c)}`).join("");
      let sel = tag + cls;
      // Disambiguate if the selector matches several elements.
      const matches = [...document.querySelectorAll(sel)];
      if (matches.length > 1) sel += `:nth-of-type(${matches.indexOf(el) + 1})`.replace(":nth-of-type(0)", "");
      return sel;
    };
    for (const el of nodes) {
      const r = el.getBoundingClientRect();
      if (r.width < 24 || r.height < 12) continue; // skip invisible/tiny
      const key = `${el.tagName}|${Math.round(r.x)}|${Math.round(r.y + window.scrollY)}|${Math.round(r.width)}`;
      if (seen.has(key)) continue;
      seen.add(key);
      const text = (el.tagName === "IMG" ? el.alt || el.src.split("/").pop() : el.textContent || "")
        .trim()
        .replace(/\s+/g, " ")
        .slice(0, 60);
      out.push({
        tag: el.tagName.toLowerCase(),
        selector: cssFor(el),
        text,
        x: r.x,
        y: r.y + window.scrollY,
        w: r.width,
        h: r.height,
      });
    }
    return out.slice(0, 80);
  });

  await browser.close();

  const s = opts.scale;
  console.log(`title: ${title}`);
  console.log(`viewport: ${opts.width}css px wide, boxes reported at scale ${s}x (device px)\n`);
  const pad = (v, n) => String(v).padEnd(n);
  for (const it of items) {
    console.log(
      `${pad(it.tag, 8)} ${pad(it.selector.slice(0, 44), 46)} x=${Math.round(it.x * s)} y=${Math.round(
        it.y * s
      )} w=${Math.round(it.w * s)} h=${Math.round(it.h * s)}  ${it.text ? JSON.stringify(it.text) : ""}`
    );
  }
}

// -------------------------------------------------------------------- main

const run = { screenshot, record, probe, batch }[cmd];
run().catch((err) => {
  console.error(`capture ${cmd} failed: ${err.message}`);
  process.exit(1);
});
