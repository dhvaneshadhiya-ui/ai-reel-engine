# iGeeksBlog Carousel Playbook (v2)

One system for every carousel we make — Apple, tech, gadgets, AI, gaming, apps, news & rumors, opinion. Read §1–§3 before starting anything; the rest is reference.

Related: `apple-newsletter/`, `partnerships/sponsorship.md` (sponsored slots), AI Reel Engine (scouting).

---

## 1. Inputs we need (ask only for what's missing)

| Input | Default |
|---|---|
| Topic + source URL(s) | — required |
| Brand handle | `@igeeksblog` (override: `@igeeksblog.ai`, etc. — set once, applies to every slide, caption and alt text) |
| Content type | inferred from topic via §2 router; confirm if ambiguous |
| Design variant | chosen via §5 matrix; confirm only if two variants fit |
| Output | static PNG + PDF + zip (default) · video carousel (§10) on request |
| CTA | picked from §8 menu by type |
| Sponsor | none (if sponsored, follow `partnerships/sponsorship.md`) |
| Design reference | none — when given (image or link), save it to `carousels/references/<name>.md` with a 5-line extraction (surface, accent, type scale, image treatment, what to borrow) and cite it in the log row |

---

## 2. Content-type router

Pick one. It fixes the slide template, the research depth, the image ladder and the caption tone.

| Type | Examples | Slide unit | Research bar | Visual source |
|---|---|---|---|---|
| **Launch / recap** | Apple Event, Unpacked, Made by Google | One product per slide (stat grid) → prices & dates | Official specs + official India pricing | Newsroom press kit |
| **Deep-dive** | iPhone 18 Pro explained | One feature per slide | Official specs page + newsroom, verbatim | Product page + newsroom |
| **Comparison** | Duo vs Fold8, M5 vs M4 | Two-column spec rows, winner in blue | Both official sources; third-party only for missing India prices | Both press kits |
| **Listicle / how-to** | Best wallpaper apps, 7 hidden iOS settings | One item per slide + Best for / Watch out | Our article + App Store data + hands-on check | App Store API, our own screenshots |
| **News & rumors** | "iPhone 19 may drop the SIM tray" | Claim → who says so → reliability → timeline | Primary report + at least one corroboration; reliability tag mandatory | Own mock-ups, official older renders, generated art (last resort) |
| **Explainer / AI / opinion** | What Siri AI actually does, Is 8K worth it | One argument per slide, one stat each | Docs, model cards, our testing; every stat cited internally | Logos, UI screenshots, dataviz, typographic slides |
| **Gaming** | PS6 vs Xbox, Best iPhone games | Same as comparison / listicle | Platform press sites, store pages | PlayStation/Xbox/Nintendo press, Steam/App Store art |

---

## 3. Standing rules (never need to be repeated)

1. **Research is the product.** Never rely only on the URLs given. Read the official spec page, the newsroom post, and at least one independent source. Write every figure down with where it came from *before* designing.
2. **Fact-check everything that lands on a slide.** Two-source rule for anything not on an official page (prices from resellers, rumor claims, benchmark numbers). If it can't be confirmed, it doesn't ship — use "Not disclosed" / "Unconfirmed", never a guess. Half-baked information does not go out under our name.
3. **Rumors are labelled.** Every rumor slide names the source and carries a reliability tag (Proven track record / Mixed / Unproven). A rumor is never phrased as fact in a headline.
4. **Brand handle bottom-right of every slide**, bold. Default `@igeeksblog`; use the handle given for the account it's going to.
5. **No source credits, no watermarks.** One generic price note on the last slide only.
6. **Header contrast.** Headline pure `#fff` (or `#0a0a0a` on light variants), 84px / 70px long. Section label 28px weight 600 `#e5e5ea`. Never grey headlines.
7. **Relevant image on every slide, filling its frame.** Trim to the subject's bounding box (§7). A small phone floating in a tile is a defect. Text-only slides only for price/summary or the Editorial variant.
8. **Scout first, generate last.** Official press kits → product pages → our own screenshots/photos → licensed footage → *only then* generated art (OpenArt or ChatGPT Image 2.5), and only for abstract topics with nothing to photograph. Never generate a product, logo or person.
9. **India-first.** INR, IST, "18 Sept", official India store pricing first, 91mobiles/Beebom/Smartprix as fallback with a note in the reply.
10. **Verbatim specs.** Quote as the brand wrote it. Unit and decimal exactly as source.
11. **Verdict on every comparison slide.** One line, plain-spoken, takes a side.
12. **Overflow zero.** The renderer reports OVERFLOW; fix copy or image height, never shrink body text below 21px.

---

## 4. Pipeline

1. **Angle** — one-line thesis, cover hook (a number, a contrast, or a question), and the slide-2 scroll-stopper. Write these three lines before anything else.
2. **Research** — official page(s) + newsroom + specs page + one independent source. Keep a claims ledger (`research.md`, format in §4a). Nothing enters a slide without a row here.
3. **Fact-check** — re-read every number against its source; cross-check prices and dates; for rumors, check the leaker's record.
4. **Scout** — follow the image ladder (§6) and write an asset manifest (§6a). If AI Reel Engine has already scouted the topic, read its `public/assets/<slug>/manifest.json` and `jobs/<slug>/research.md` first and reuse what is verified. Build a contact sheet and look at it before choosing.
5. **Design decision** — §5 matrix → variant + template.
6. **Author** `slides-<topic>.html` from base CSS (§12).
7. **Render** with `render.js` → fix every OVERFLOW.
8. **QA** — 4-up sheet, then full-size pass on cover, one content slide and the last slide (§11 checklist).
9. **Voice pass** — read every headline, verdict and the caption against §9. Run `humanizer` on all packaging copy, then `marketing:brand-review` when the copy is long.
10. **Export & package** — PNGs, PDF, zip, caption + alt text (§8). Send PDF, zip and 2–3 preview slides.
11. **Log** — add a row to the carousel log (topic, type, variant, CTA, date, later: saves/shares/comments).

### 4a. Claims ledger (`research.md`)

Same shape AI Reel Engine uses, with SPOKEN renamed to SHOWN because a carousel prints its claims:

```
- CLAIM: <one load-bearing fact>
  TIER: official | multi | single | disputed
  SHOWN: "<the exact words on the slide>"
  SRC: <url actually fetched>
  VIA: <ultimate source, e.g. "Apple Newsroom", "WABetaInfo teardown">

## SEARCHED
- 2026-09-10 "galaxy z fold8 india price" → 91mobiles, beebom
```

Rules: two independent VIAs for anything not on an official page (two outlets quoting one leaker is one source); a claim that can only reach `single` is shown with "reportedly" or a reliability pill, never as a headline fact; the SEARCHED log proves the research was ours and not just the URLs handed over. The user's references are inputs, not sourcing.

---

## 5. Design decision matrix

Four variants share one grid, one type scale and one component set; only surface changes. Decide from the topic, not by habit.

| Variant | Use for | Surface | Accent |
|---|---|---|---|
| **Apple Dark** (default) | Apple launches, deep-dives, comparisons, apps | `#000`, cards `#1d1d1f` | `#4da3ff` |
| **Studio White** | Products whose press imagery is on white (iPhone Duo, AirPods, Pixel, many accessories); light-mood listicles | `#fff`, cards `#f5f5f7`, ink `#1d1d1f` | `#0066cc` |
| **Editorial** | Opinion, explainers, AI, "what it means" pieces — type is the visual | `#000` or `#fff`, oversized headline 96–120px, one pull-stat per slide, sparse imagery | `#4da3ff` |
| **Alert** | News & rumors, deals, breaking | Apple Dark base + amber `#ffb340` (rumor) or red `#ff453a` (breaking) eyebrow tag and reliability pill | amber / red |

Rules: a brand's own imagery decides light vs dark (Samsung/Google follow their photo backgrounds); a recurring series keeps one variant and one cover treatment; never mix variants inside one carousel; sponsored slides follow `sponsorship.md` and sit inside the same variant.

Slide templates per type are in §13.

---

## 6. Image sourcing ladder (stop at the first clean asset)

**Order for everything:** official press kit → official product page → our own screenshots/photos → licensed footage/stock → generated (OpenArt / ChatGPT Image 2.5), abstract only.

**Apple** — `apple.com/newsroom` press release images (`…/newsroom/images/…/*_inline.jpg.large_2x.jpg`, 1300px+) → `apple.com/in/<product>/` HTML, grep `/v/<product>/a/images/overview/…*_large_2x.jpg` (best folders: `product-viewer/`, `media-hero/`, `highlights/`, `design/`, `pro-camera/`, `welcome/`; skip `*_startframe`, `icon_*`, `environment/`) → sibling pages for shared assets (Siri orb on the Watch page, A20 Pro on the 18 Pro page).

**Samsung** — `news.samsung.com/global` launch post press kit (`img.global.news.samsung.com/…`) → `samsung.com/in/smartphones/<product>/` → `images.samsung.com/in/smartphones/<product>/images/<product>-features-*.jpg`. India page hides price/specs behind JS; use newsroom + 91mobiles for numbers. Galaxy AI wordmark: crop from `…/galaxy_ai/01_galaxy_ai_kv_pc_static.jpg`.

**Google** — `store.google.com/in/product/<product>` HTML → `lh3.googleusercontent.com/<id>=w1600`. Gemini sparkle: `gstatic.com/lamda/images/gemini_sparkle_4g_512_lt_….png`.

**Chips & logos** — 91-img `…?tr=w-1200` (default is 240px). Pad square logos to tile ratio with edge-extended background; never crop a logo.

**Apps** — iTunes Search API `itunes.apple.com/search?term=<name>&entity=software&country=in` → `artworkUrl512`, `screenshotUrls` (rewrite size suffix to `/1290x2796bb.jpg`), `averageUserRating`, `sellerName`. Google Play: scrape the store page `<img>` with `=w2000`.

**Gaming** — PlayStation/Xbox/Nintendo press sites, publisher press kits, Steam store API (`store.steampowered.com/api/appdetails?appids=`) for header/capsule art.

**AI products** — vendor newsrooms (OpenAI, Google, Anthropic, Meta), model cards, official UI screenshots; logos from vendor brand pages.

**News & rumors** — never lift images from the reporting outlet. Use the brand's previous-gen official renders, our own mock-ups, or a typographic Alert slide.

**Video** — official product films (Apple/Samsung/Google host MP4s on the same CDNs), our own screen recordings, licensed stock. Check the license before use.

Always: desktop User-Agent, verify with PIL (size, corner colour), contact sheet before choosing. Log the source URL of every asset used.

### 6a. Asset manifest and the AI Reel Engine handover

AI Reel Engine (`~/AI Reel Engine`) is a Remotion reel pipeline; most of it (beats, voiceover, avatar) does not apply to carousels. Four things do, and we adopt them rather than re-inventing:

1. **Manifest format.** Every scouted asset is written to `assets/<slug>/manifest.json` as `{id, kind: footage|receipt|brand|still, source, tier: official|reliable|fallback, shows, quality: clean|has-chrome|busy, credit, crop}`, plus `verified_facts` and `explicitly_NOT_claimed`. `shows` is written only after looking at the file. When the engine has a manifest for the same topic, we read it and reuse anything `official` or `reliable`; a `fallback` asset is re-scouted.
2. **Screenshot receipts.** `node tools/capture.mjs screenshot <url> --selector <css> --scale 3` gives chrome-free, cookie-banner-free, 3x captures of a page element. Use it for App Store listings, settings pages, pricing tables and news receipts on rumor slides.
3. **Official logo SVGs.** `node tools/get_logo.mjs <name>` pulls the brand's SVG from svgl.app. Use it for assistant/brand logo slides instead of cropping wordmarks out of key visuals.
4. **Contact sheets.** `python3 tools/scout_sheet.py <dir>` for video candidates; our PIL sheet for stills. Look before choosing.

What we do **not** take from it: the 9:16 frame, VO-anchored cuts, the giveaway mechanic, and its style packs. Its packaging shape (fields as destinations, 5-tag cap, tags in the first comment) is adopted in §8.

---

## 7. Image fitting recipe

- Trim to content bounding box: difference vs the corner pixel, threshold ~18 (30–45 for glow-on-black renders), pad 4 %. Save `<name>_c.jpg`.
- Place with `object-fit: contain` in a tile whose background matches the image's own (white / black / sampled). `cover` only for edge-to-edge lifestyle shots.
- Tile heights: 340 comparison · 376–400 single product · 540 cover · 410 app screenshots.
- If the subject touches the frame edge in the source, pick another asset rather than cropping into it.

---

## 8. CTA menu and packaging

| CTA | Use when |
|---|---|
| **Comment "KEYWORD" → we DM the links** | Anything with links: apps, wallpapers, deals, downloads. Auto-DM runs on superprofile.bio; add the keyword there before posting. |
| **Team A or Team B?** | Comparisons |
| **Save this for launch day / pre-order day** | Launches with a future date |
| **Tag someone who…** | Gift guides, upgrade guides |
| **Which one are you picking?** | Listicles without links |

Packaging is a required deliverable for every carousel, written after the slides are final so it mirrors them exactly.

Packaging workflow: (1) draft the caption with `marketing:draft-content` — ask for 3 hook variants and pick one; (2) pick **3–5 hashtags, never more** (Instagram ignores every tag past five since Aug 2025); they go at the end of the FIRST COMMENT, not in the caption. Use `searchfit-seo:keyword-cluster` to choose them: one broad, two or three mid, one brand or product tag. `#iGeeksBlog` counts as one of the five; (3) write alt text from the rendered PNGs, not from the HTML — describe what is actually visible; (4) run `humanizer` (embedded mode) on the caption and every alt text, then `marketing:brand-review` against §9 and fix flags; (5) mirror the last slide's CTA verbatim. Humanizer rules that bite hardest on captions: no em/en dashes, no "not X but Y", no one-line dramatic closers, no forced triads, no stock AI words (crucial, showcase, elevate, seamless, game-changer).

Packaging file `<Topic>-Caption-and-Alt-Text.md`. Every field is a destination and is pasted verbatim (borrowed from AI Reel Engine's `packaging_check.py`, which enforces the same shape):

```
## instagram
CAPTION: <hook line ending 👇, 2–3 short paragraphs, India price/date block, pick-if lines for comparisons, CTA mirrored from the last slide, "Full … on iGeeksBlog (link in bio)". No hashtags here.>
FIRST COMMENT: <engagement question or the keyword-DM line> #tag1 #tag2 #tag3 #tag4 #tag5
ALT TEXT: <one per slide, "Slide n — Section", ≤ ~200 chars, image first then key numbers>
```

Record the humanizer pass: after the final edit, note `humanized: <date>` at the top of the file (AI Reel Engine keeps a `humanized.json` with a text hash for the same reason).

---

## 9. Voice

Confident, plain-spoken, specific. India-aware. Takes a side on comparisons. Numbers over adjectives. Sentence case headlines that could be said out loud. One light joke per carousel at most.
Never: "game-changer", "revolutionary", "insane", "you won't believe", exclamation marks in headlines, rumor stated as fact, unexplained acronyms.
Rumor phrasing: "may", "is reported to", "according to <source>" — plus the reliability pill.

---

## 10. Video carousels (Remotion / HyperFrames)

Use when motion adds information (a hinge folding, a feature in action, a price counter) — not by default.

- **Remotion** (local, `npm i remotion @remotion/cli`): one composition per slide, 1080×1350, 30 fps, 4–6 s each; reuse the same HTML/CSS tokens as React components; render `npx remotion render`. Best for spec counters, animated comparison rows, screenshot swipes.
- **HyperFrames** (HeyGen MCP `compose` / `render_video`): hosted project with a shareable canvas; best when the team wants to tweak on a timeline, or for a single hero video slide with voiceover.
- Assets: official product films and our own screen recordings first; generated video only for abstract B-roll.
- Deliver: MP4 per slide + a stitched preview MP4 + the static PNG fallback set.

---

## 11. QA checklist

- [ ] Fact table complete; every slide number has a verified row
- [ ] Rumor slides carry source + reliability pill
- [ ] Headline white/black, correct handle bottom-right, "n / N" counter correct
- [ ] Every image trimmed and filling its tile; no subject cut at the edge
- [ ] INR/IST; single generic price note on last slide only; no credits or watermarks
- [ ] Voice pass done (§9); CTA matches type (§8)
- [ ] render.js reports no OVERFLOW; cover scored (vidIQ `score_thumbnail`) when time allows
- [ ] PDF + zip + previews sent; caption/alt pack written; log row added

---

## 12a. Tool map (what we use at which step)

| Step | Tool | Notes |
|---|---|---|
| Topic selection | Ahrefs keyword volume; vidIQ trending/outliers | Weekly, not per carousel |
| Angle | `superpowers:brainstorming` | Only for opinion/explainer pieces |
| Research | WebFetch / WebSearch; `searchfit-seo:content-brief` when derived from an iGB article | Two-source rule |
| Scouting | AI Reel Engine; §6 ladder | Generated art via OpenArt / ChatGPT Image 2.5 as last resort |
| Charts | `dataviz` | Benchmarks, market share, price history |
| Copy | `marketing:draft-content` (caption variants) → `humanizer` (embedded) → `marketing:brand-review` against §9 | Humanizer is installed account-wide; §9 is the voice standard |
| Hashtags | `searchfit-seo:keyword-cluster` | |
| Cover check | vidIQ `score_thumbnail` | |
| Video | Remotion (local), HyperFrames (MCP) | §10 |
| Editable handoff | Canva `import-design-from-url`, Claude Design canvas, `pptx` | On request |
| Sponsored | `igb-partnerships` + `partnerships/sponsorship.md` | |
| Own products | `icon-pack-themes`, CrestWall assets | App-of-the-week, wallpapers |
| Scheduling | Native Instagram scheduler or Notion calendar (Metricool free plan is not used for publishing) | |
| Auto-DM | superprofile.bio keyword automation | Set the keyword before the post goes live |
| Analytics | Metricool MCP (`getAnalyticsDataByMetrics`, `getBestTimeToPostByNetwork`), Windsor.ai (`get_data` for Instagram organic), Google Search Console via Ahrefs `gsc-*` tools | Pull saves/shares/comments per post fortnightly into §14; GSC for article-to-carousel topic picks |

---

## 12. Base CSS and render script (copy verbatim)

```css
@font-face{font-family:Inter;font-weight:400;src:url(node_modules/@fontsource/inter/files/inter-latin-400-normal.woff2)}
@font-face{font-family:Inter;font-weight:500;src:url(node_modules/@fontsource/inter/files/inter-latin-500-normal.woff2)}
@font-face{font-family:Inter;font-weight:600;src:url(node_modules/@fontsource/inter/files/inter-latin-600-normal.woff2)}
@font-face{font-family:Inter;font-weight:700;src:url(node_modules/@fontsource/inter/files/inter-latin-700-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,-apple-system,"SF Pro Display",Helvetica,Arial,sans-serif;background:#333;-webkit-font-smoothing:antialiased}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;padding:76px 72px 72px;display:flex;flex-direction:column;margin:20px auto}
.dark{background:#000;color:#f5f5f7;--sec:#86868b;--acc:#2997ff;--card:#1d1d1f;--line:#2a2a2d}
.white{background:#fff;color:#1d1d1f;--sec:#6e6e73;--acc:#0066cc;--card:#f5f5f7;--line:#d2d2d7}
.top{display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:600;color:#e5e5ea;letter-spacing:.01em}
.top .n{font-variant-numeric:tabular-nums;color:#a1a1a6}
.eyebrow{font-size:28px;font-weight:600;color:#4da3ff;letter-spacing:-.01em;margin-top:34px}
h1{color:#fff;font-size:84px;line-height:1.02;font-weight:700;letter-spacing:-.045em;margin-top:14px}
h1.sm{font-size:70px}
.sub{font-size:34px;line-height:1.3;color:#c7c7cc;font-weight:500;letter-spacing:-.015em;margin-top:28px;max-width:880px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:auto}
.stat{background:var(--card);border-radius:28px;padding:24px 30px 22px}
.stat .v{font-size:52px;font-weight:700;letter-spacing:-.04em;line-height:1;color:var(--acc)}
.stat .v.w{color:inherit}
.stat .l{font-size:21px;color:var(--sec);margin-top:10px;line-height:1.3;font-weight:500}
.foot{display:flex;justify-content:space-between;align-items:flex-end;margin-top:26px;padding-top:22px;border-top:1px solid var(--line)}
.price{font-size:40px;font-weight:700;letter-spacing:-.03em}
.price small{display:block;font-size:24px;font-weight:500;color:var(--sec);margin-top:8px;letter-spacing:0}
.brand{font-size:24px;font-weight:700;color:#e5e5ea}
.list{margin-top:auto;display:flex;flex-direction:column}
.row{display:flex;gap:28px;align-items:flex-start;padding:14px 0;border-top:1px solid var(--line)}
.row:first-child{border-top:0}
.row .k{font-size:23px;font-weight:600;width:250px;flex:none;color:var(--sec);padding-top:4px}
.row .t{font-size:27px;font-weight:600;letter-spacing:-.02em;line-height:1.28}
.row .t span{color:var(--sec);font-weight:500}
.sw{display:inline-flex;gap:14px;vertical-align:middle;margin-left:6px}
.sw i{width:38px;height:38px;border-radius:50%;display:inline-block;border:2px solid rgba(128,128,128,.35)}
.vis{position:relative;flex:none;height:376px;margin:12px -72px 0;overflow:hidden;display:flex;align-items:center;justify-content:center}
.vis img{width:100%;height:100%;object-fit:contain}
.vis img.cover{object-fit:cover}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 60%,rgba(41,151,255,.28),transparent 60%);z-index:0}
table{width:100%;border-collapse:collapse;margin-top:auto;font-size:27px}
th{font-size:22px;font-weight:600;color:var(--sec);text-align:left;padding:0 0 18px;text-transform:uppercase;letter-spacing:.06em}
td{padding:17px 0;border-top:1px solid var(--line);vertical-align:top;line-height:1.3}
td.p{font-weight:700;letter-spacing:-.02em;white-space:nowrap}
td.d{color:var(--sec);font-weight:500}
td:first-child{font-weight:600}
.swipe{display:inline-flex;align-items:center;gap:14px;font-size:28px;font-weight:600;color:var(--acc)}
.cta{margin-top:auto;background:var(--card);border-radius:32px;padding:34px 44px}
.cta h2{font-size:42px;font-weight:700;letter-spacing:-.035em;line-height:1.1}
.cta p{font-size:25px;color:var(--sec);margin-top:16px;font-weight:500;line-height:1.35}
.note{font-size:20px;color:var(--sec);line-height:1.4}
/* comparison layout */
.duel{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:28px}
.tile{height:340px;border-radius:28px;overflow:hidden;display:flex;align-items:center;justify-content:center}
.tile img{width:100%;height:100%;object-fit:cover}
.tile img.fit{object-fit:contain}
.name{font-size:26px;font-weight:700;margin-top:14px;display:flex;align-items:center;gap:12px}
.name i{width:14px;height:14px;border-radius:50%;display:inline-block}
.cmp{margin-top:auto}
.cmp .r{display:grid;grid-template-columns:1fr 200px 1fr;gap:16px;align-items:center;padding:16px 0;border-top:1px solid var(--line)}
.cmp .r:first-child{border-top:0}
.cmp .k{font-size:21px;font-weight:600;color:#a1a1a6;text-align:center;text-transform:uppercase;letter-spacing:.06em}
.cmp .a,.cmp .b{font-size:27px;font-weight:600;letter-spacing:-.02em;line-height:1.25}
.cmp .b{text-align:right}
.cmp .a span,.cmp .b span{display:block;font-size:21px;color:#a1a1a6;font-weight:500;margin-top:3px}
.win{color:#4da3ff}
.verdict{font-size:30px;font-weight:700;letter-spacing:-.02em;line-height:1.25}
.verdict small{display:block;font-size:22px;color:#a1a1a6;font-weight:500;margin-top:6px}
/* listicle layout */
.app{display:flex;align-items:center;gap:26px;margin-top:26px}
.app img{width:120px;height:120px;border-radius:27px;flex:none}
.app .n{font-size:34px;font-weight:700;letter-spacing:-.02em}
.app .m{font-size:23px;color:#a1a1a6;font-weight:500;margin-top:6px}
.app .m b{color:#ffd60a;font-weight:600}
.shots{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px}
.shots img{width:100%;height:410px;object-fit:cover;object-position:top;border-radius:26px;background:#1d1d1f}
.icons{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:auto}
.icons img{width:100%;aspect-ratio:1;border-radius:22%;box-shadow:0 20px 50px rgba(0,0,0,.5)}
.rank{display:flex;flex-direction:column;gap:14px;margin-top:30px}
.rank .r{display:flex;align-items:center;gap:22px;background:#1d1d1f;border-radius:22px;padding:16px 24px}
.rank .r img{width:72px;height:72px;border-radius:17px}
.rank .r .i{font-size:26px;font-weight:700;color:#4da3ff;width:44px}
.rank .r .t{font-size:27px;font-weight:700;letter-spacing:-.02em}
.rank .r .t span{display:block;font-size:21px;color:#a1a1a6;font-weight:500;margin-top:2px}
```

Render script (`render.js`):

```js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1400 } });
  await page.goto('file://' + path.resolve(process.argv[2])); await page.evaluate(() => document.fonts.ready);
  const n = await page.$$eval('.slide', e => e.length);
  for (let i = 1; i <= n; i++) {
    const el = await page.$('#s' + i);
    await el.screenshot({ path: `${process.argv[3]}/slide-${String(i).padStart(2,'0')}.png` });
    const ov = await el.evaluate(e => Math.max(0, e.scrollHeight - e.clientHeight));
    console.log('slide', i, ov ? 'OVERFLOW ' + ov : 'ok');
  }
  await browser.close();
})();
```

Setup once per session: `npm i playwright @fontsource/inter` (do not run `playwright install`; use the preinstalled Chromium path above). PDF: PIL `ims[0].save(pdf, save_all=True, append_images=ims[1:], resolution=150)` — import `PIL.JpegImagePlugin` first or the save raises `KeyError: 'JPEG'`.


## 13. Slide templates

**Launch / recap** — cover · hero slide per product (4-stat grid, 2 blue) · optional detail slide (spec rows) · prices & dates table + CTA.

**Deep-dive** — cover · design · display · chip · headline feature · full camera/feature set · video · battery · software/AI · price by storage + dates + CTA. 10 slides.

**Comparison** — cover with both devices in tiles · design & build · displays · performance · cameras · battery & charging · software & AI · price & verdict. Each content slide: two `.tile`s with `.name` labels → 4–5 `.cmp .r` rows with winner in `.win` → `.verdict` footer. AI slide uses assistant logos, not phones.

**Listicle / how-to** — cover with 3×2 icon grid · per item: eyebrow "#n · hook", h1 tagline, `.app` row (icon 120px, name, seller · ★ rating · price), 3 `.shots` at 410px, 4-stat grid, "Best for / Watch out" footer · shortlist slide with ranked rows + keyword-DM CTA.

**News & rumors (Alert)** — cover with amber tag "RUMOR" or red "BREAKING" · claim slide (what) · source slide (who, reliability pill, track record) · evidence/context slide · timeline slide (expected when) · "what it means for you" · CTA "Would you buy it? / Save for the event".

**Explainer / opinion (Editorial)** — cover thesis · 5–7 argument slides, each one oversized line + one pull-stat + optional small image · counter-argument slide · verdict slide + CTA.

**Gaming** — comparison or listicle template with Studio White or Apple Dark depending on key art.

---

## 14. Log

| Date | Topic | Type | Variant | CTA | Slides | Notes |
|---|---|---|---|---|---|---|
| 09 Sept 2026 | Apple Event recap | Launch | Apple Dark / Studio White mix | Comment question | 9 | |
| 09 Sept 2026 | iPhone 18 Pro & Pro Max | Deep-dive | Apple Dark | Pro or Pro Max? | 10 | |
| 09 Sept 2026 | iPhone Duo vs Pixel 11 Pro Fold | Comparison | Apple Dark | Team Duo / Team Fold | 8 | |
| 10 Sept 2026 | iPhone Duo vs Galaxy Z Fold8 | Comparison | Apple Dark | Team Duo / Team Fold8 | 8 | Samsung IN page hides prices; used 91mobiles |
| 10 Sept 2026 | Best Wallpaper Apps for iPhone | Listicle | Apple Dark | Comment "WALLPAPERS" → DM | 8 | CrestWall is ours |
