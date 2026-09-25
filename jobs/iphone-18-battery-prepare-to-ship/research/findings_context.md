# Research: CONTEXT — the real regulatory numbers behind "Prepare to Ship"

Subtopic: battery capacity figures + the actual air-transport lithium rules
(not tech-press paraphrase) + single-cell-vs-multi-cell reasoning + precedent.
Compiled 2026-09-21.

## 1. Battery capacities — iPhone 18 Pro Max vs. prior Pro Max models

- iPhone 18 Pro Max, US eSIM-only model: **5,567 mAh / 21.75 Wh** (iFixit
  teardown figure). SRC:
  https://www.gsmarena.com/heres_apples_clever_way_of_circumventing_20wh_battery_shipping_restrictions-news-74689.php
  — Quote: "5,567mAh (21.75Wh)". VIA: iFixit teardown. Corroborated
  independently: https://www.ifixit.com/News/119329/inside-the-tiny-unfixable-eye-iphone-18-pro-and-pro-max-teardown
  — Quote: "iPhone 18 Pro Max (eSIM model): 21.751 Wh (5567 mAh)"

- iPhone 18 Pro Max, physical-SIM (e.g. European) model: **5,391 mAh / 21.06 Wh**.
  SRC: https://www.gsmarena.com/heres_apples_clever_way_of_circumventing_20wh_battery_shipping_restrictions-news-74689.php
  — Quote: "European physical SIM model: 5,391 mAh or 21.06Wh". Also (mAh
  only): https://www.macrumors.com/2026/09/09/iphone-18-pro-max-battery-capacities/
  — figures sourced from "energy labels on its iPhone product pages in the
  EU," which Apple must publish (Apple's own disclosed number, not just a
  teardown estimate).

- iPhone 18 Pro (NOT the Pro Max — does not need Prepare to Ship), eSIM:
  **4,288 mAh / 16.76 Wh** — well under 20 Wh, consistent with only the Max
  needing this feature. SRC:
  https://www.ifixit.com/News/119329/inside-the-tiny-unfixable-eye-iphone-18-pro-and-pro-max-teardown
  — Quote: "iPhone 18 Pro (eSIM model): 16.76 Wh (4288 mAh)"

- iPhone 17 Pro Max — physical SIM: **4,823 mAh / 18.748 Wh**; eSIM-only:
  **5,088 mAh / 19.772 Wh** (already close to 20 Wh, but under it). SRC:
  WebSearch-aggregated table attributed to
  https://en.wikipedia.org/wiki/IPhone_17_Pro — **not independently
  WebFetched in this pass; tier as SRC-needs-confirm**, not verified, before
  using as a locked on-screen number.

- iPhone 16 Pro Max: **4,685 mAh / 18.17 Wh**. iPhone 15 Pro Max: **4,422 mAh
  / 17.32 Wh**. SRC: same WebSearch aggregation, attributed to
  https://en.wikipedia.org/wiki/IPhone_16_Pro and
  https://en.wikipedia.org/wiki/IPhone_15_Pro — same SRC-needs-confirm caveat.

**Script-relevant trend:** every Pro Max generation has crept closer to 20 Wh
(17.32 -> 18.17 -> 19.772 -> 21.75/21.06), and the 18 Pro Max is the first to
cross it — a clean rising-bar-chart-hits-a-red-line visual beat.

## 2. The actual regulation (not just tech-press paraphrase)

**Primary source attempted: IATA DGR Table 2.3.A.** Fetched the PDF directly
(https://www.iata.org/contentassets/6fea26dd84d24b26a7a1fd5788561d6e/dgr-62-en-2.3a.pdf)
but it is flate-encoded and the fetch tool could not extract readable text —
see SEARCHED below. Figures below are corroborated across multiple
independent secondary sources.

- **Single lithium-ion CELL limit: 20 Wh.** Above this, treated as fully
  regulated Class 9 dangerous goods (Section I) for air transport. SRC:
  https://www.hazmatuniversity.com/news/lithium-battery-air-transport-2026-iata-and-icao-compliance-guide/
  (via WebSearch synthesis) — "Lithium ion cells with a Watt-hour rating of
  20 Wh or less or batteries that are 100 Wh or less are not subject to all
  of the provisions of the DGR." / "Section I applies if the equipment
  contains lithium ion cells of >20 Wh or lithium ion batteries of >100 Wh."

- **Complete BATTERY (multi-cell pack) limit: 100 Wh** — the separate, larger
  threshold for an assembled pack (vs. one cell); governs laptop packs and
  carry-on spares. SRC (US equivalent primary rule):
  https://www.ecfr.gov/current/title-49/subtitle-B/chapter-I/subchapter-C/part-173/subpart-E/section-173.185
  (49 CFR 173.185) — **fetch was blocked by an unblock/bot-check redirect
  wall, not independently confirmed verbatim.** Secondary corroboration:
  https://www.fedex.com/content/dam/fedex/us-united-states/services/Shipping-Lithium-Batteries-via-FedEx-Ground.pdf
  (FedEx's own DG guide, citing 49 CFR 173.185 by name) — "lithium ion cells
  above 20 Wh and lithium ion batteries above 100 Wh considered
  high-energy"; "Packages containing lithium ion cells with a Watt-hour
  rating of not more than 20 Wh or batteries with not more than 100 Wh can
  be transported by air under certain conditions."

- **Underlying rule for both numbers: UN Special Provision 188 (SP188)**,
  mirrored by IATA DGR, the UN Model Regulations, ADR (road) and IMDG (sea).
  SRC: https://www.androidauthority.com/phone-battery-transportation-rules-3574123/
  (via WebSearch synthesis) — "UN Special Provision 188... That limit is
  20Wh (watt-hours) per cell" / "is mirrored in the ADR, IMDG, IATA, and
  other international rules." This is Android Authority's own explainer;
  treat as the operative citation until the primary UN Model Regulations
  text is fetched directly (attempted for IATA's PDF, blocked).

- **Reported claim: US regulator (PHMSA/DOT) approved Apple's exact firmware
  workaround in June 2025**, ahead of IATA/ICAO/ADR weighing in officially.
  SRC: https://www.gsmarena.com/heres_apples_clever_way_of_circumventing_20wh_battery_shipping_restrictions-news-74689.php
  — "the US transport regulator" approved it "back in June 2025," while
  "ADR, IATA and ICAO... still haven't officially chimed in." **Single-source
  claim — tier SUPPORTED, not VERIFIED, until a primary PHMSA record is
  found.**

- Same article: regulators reportedly discussing raising the 20 Wh ceiling as
  "increasingly obsolete," targeting a 2029 policy update. Tier
  SUPPORTED-WITH-LIMITS (no docket/version cited beyond this one article).

## 3. Apple's own explanation (strongest, most citable source)

SRC: https://support.apple.com/en-us/127848 (fetched directly)
- "Devices with a single-cell battery over 20 Wh have additional shipping
  requirements in most countries and regions."
- "iPhone 18 Pro Max uses an innovative battery-firmware solution that
  limits battery capacity to below 20 Wh from the time it's manufactured
  through its transport from the factory. When you activate your iPhone, the
  limit is removed and the battery's full charging capacity is available."
- "This feature discharges your battery to below 20 Wh and sets a charge
  limit so your iPhone stays below this limit while shipping."
- Discharge time: "might take only a few minutes, but if you start with a
  full charge, it can take up to a couple of hours." Battery "might become
  warmer than usual" during discharge.
- Path: Settings > General > Transfer or Reset iPhone > Prepare to Ship.
  Completion state: "Ready to Ship" with a red badge.
- Post-repair/trade-in/return: "the battery charge limit will be capped at
  80 percent for 14 days."
- Explicitly shipping-only: the limitation "isn't required while traveling
  or for any other iPhone model."

This is Apple's own primary-source statement of the core regulatory fact
(single-cell, 20 Wh, most countries/regions) — the strongest citation for the
whole video.

## 4. Single cell over 20 Wh vs. multiple cells under 20 Wh each (MacBook Pro)

Confirmed accurate, not an oversimplification — per a forum explanation
quoted inside a MacRumors piece: SRC:
https://www.macrumors.com/2026/09/18/iphone-18-pro-max-shipping-restriction/
— "Airlines have a limit of 100Wh in a device (where the 16" MacBook Pro is
at 99.9Wh) while each single battery cell can only have a maximum of 20Wh."
MacBook Pro reaches its total using "5 or 6 different cells that each are
under 20Wh but much larger as a combination." Also: "Since no other iPhones
have a single-cell battery over 20Wh, this procedure isn't needed for other
models."

This matches the two-tier structure (20 Wh/cell, 100 Wh/pack) independently
found in the IATA/49 CFR sourcing above — same rule, not a press invention.
The MacBook Pro's 99.9 Wh sits deliberately just under the pack ceiling,
built from cells individually under the cell ceiling. A phone is built
around one large pouch cell for space reasons, so there's no "split into
more cells" option without a redesign — which is exactly why Apple needed a
firmware workaround instead of a battery redesign.

General background (not iPhone-specific, not an on-screen citable claim,
context only): https://www.batterypowertips.com/battery-configurations-series-and-parallel-and-their-protections/

## 5. Precedent — has any other device crossed the single-cell 20 Wh line?

- **No other iPhone has crossed it** — MacRumors (quoted above): "Since no
  other iPhones have a single-cell battery over 20Wh, this procedure isn't
  needed for other models."
- **iPhone 18 Pro Max reported as a first for a phone** — first mainstream
  smartphone shipped with a single cell itself exceeding 20 Wh, needing a
  firmware/shipping workaround rather than a redesign. SRC:
  https://www.gsmarena.com/heres_apples_clever_way_of_circumventing_20wh_battery_shipping_restrictions-news-74689.php
  and https://www.analyticsinsight.net/news/iphone-18-pro-max-battery-crosses-20wh-apple-adds-new-shipping-rule
  (via WebSearch synthesis) — "The iPhone 18 Pro Max is the first iPhone to
  have a single-cell battery over 20Wh." Treat "first phone ever" (vs.
  "first iPhone") as SUPPORTED-WITH-LIMITS — sources are confident on "first
  iPhone," less explicit on ruling out every non-Apple phone globally.
- **Existing precedent for phones engineering AROUND the line: dual-cell
  packs.** OnePlus and OPPO already ship phones with two smaller cells (each
  under ~20 Wh / ~5,300 mAh at ~3.8V nominal) combining to more effective
  capacity than one 20 Wh cell, specifically to stay compliant while going
  bigger. SRC: https://www.androidauthority.com/phone-battery-transportation-rules-3574123/
  — "like OnePlus and OPPO circumvent limits through dual-cell designs";
  "Apple, Google, Samsung, and many others haven't pushed ahead with quite
  as large capacities" for this reason.
- **Regional battery-capacity splits as evidence the rule has shaped phone
  design for years:**
  - Nothing Phone 3: 5,150 mAh (regulated markets) vs. 5,500 mAh (India)
  - HONOR Magic 7 Pro: 5,270 mAh (Europe) vs. 5,850 mAh (China)
  - Xiaomi 15 Ultra: 5,410 mAh (global) vs. 6,000 mAh (China)
  SRC: https://www.androidauthority.com/phone-battery-transportation-rules-3574123/
  — China isn't bound by the same air-transport-driven ceiling for domestic
  units, hence larger China-market variants.
- **Related but DISTINCT precedent: drones/spare lithium batteries shipped
  at <=30% state of charge.** This is a different regulation (IATA/UN3480,
  for standalone spare lithium-ion batteries not installed in equipment),
  not the 20 Wh cell-rating threshold. Apple's Prepare to Ship is about a
  battery installed in the device crossing the Wh-capacity line, not a
  state-of-charge rule for loose spares. Worth distinguishing on screen so
  the reel doesn't conflate "why drone batteries ship at 30%" with "why the
  iPhone must discharge before shipping" — related fire-safety logic,
  different specific provision. SRC: WebSearch synthesis citing IATA
  DGR/UN3480; no single primary page fetched directly —
  SUPPORTED-WITH-LIMITS background only.

## SEARCHED — looked for, did not fully confirm

- **Primary IATA DGR Table 2.3.A PDF**: downloaded but flate-encoded; text
  could not be extracted in this pass. The 20 Wh/100 Wh figures are
  corroborated by multiple independent secondary sources (hazmatuniversity,
  FedEx, Android Authority) describing the same table consistently, but the
  primary IATA clause text itself was not directly quoted.
- **49 CFR 173.185 exact text**: eCFR redirected to a bot-check wall, not
  fetched. Corroborated only via FedEx's DG guide and WebSearch synthesis of
  PHMSA guidance.
- **Exact iPhone 17/16/15 Pro Max Wh figures**: found via WebSearch synthesis
  attributed to Wikipedia pages, but those pages were not independently
  WebFetched to confirm verbatim — flagged as SRC-needs-confirm.
- **Primary PHMSA docket confirming the reported "June 2025" approval**: not
  found; only the single GSMArena mention surfaced. No official ICAO or ADR
  statement found either, consistent with GSMArena's claim that those bodies
  "haven't officially chimed in."
- **A non-Apple phone that shipped with a single cell actually over 20 Wh**
  (i.e., beating Apple to it): not found. All sources describe other
  high-capacity phones (China-market Xiaomi/HONOR/Nothing) as staying under
  20 Wh per cell via dual-cell designs or regional variants; none documented
  as crossing the line the way the iPhone 18 Pro Max does.
- **Camera precedent**: none surfaced. Only phone (dual-cell workaround) and
  laptop (multi-cell pack) precedents were found. Did not exhaustively
  search cinema-camera brick batteries (RED/ARRI) — flagging as a gap, not
  asserting no camera has ever crossed the line.

## Source hygiene notes

- Two fetches failed with HTTP 403 and were not used for any claim:
  https://www.phonearena.com/news/the-iphone-18-pro-max-ships-to-you-with-a-smaller-battery-than-advertised_id183471
  and https://www.imaging-resource.com/news/apple-iphone-18-pro-and-pro-max-battery-capacities-revealed/
- No fetched page in this pass contained text addressed to an AI
  assistant/agent — no injected instructions observed. All fetched content
  was treated as data, not instructions.
