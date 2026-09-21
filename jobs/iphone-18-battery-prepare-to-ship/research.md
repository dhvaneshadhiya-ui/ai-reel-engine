# Research — iphone-18-battery-prepare-to-ship

Claims ledger + search log. Tiers: official / multi / single / disputed.

## CLAIMS

- CLAIM: iPhone 18 Pro Max has a Settings feature called "Prepare to Ship"
  that does not exist on any other iPhone.
  TIER: official
  SURPRISE: 70
  SPOKEN: "That's Prepare to Ship: a setting that exists on no other iPhone."
  SRC: https://support.apple.com/en-us/127848
  VIA: Apple's own support article, "Prepare your iPhone 18 Pro Max to ship"
  SRC: https://www.macrumors.com/2026/09/18/iphone-18-pro-max-shipping-restriction/
  VIA: MacRumors, independent confirmation, reports it as Apple's own
  published guidance, not a leak

- CLAIM: The feature exists because the iPhone 18 Pro Max has a single-cell
  battery over 20 watt-hours, and devices with a single-cell battery over
  20 Wh have additional shipping requirements in most countries and regions.
  No other iPhone has ever had a single-cell battery over 20 Wh; this
  procedure applies only to the iPhone 18 Pro Max, not during ordinary use
  or travel.
  TIER: official
  SURPRISE: 85
  SPOKEN: "Here's why: this phone's battery crossed a number no iPhone has
  ever crossed before, twenty watt-hours, all in one cell."
  SRC: https://support.apple.com/en-us/127848
  VIA: Apple's own words, verbatim: "Devices with a single-cell battery over
  20 Wh have additional shipping requirements in most countries and
  regions"; the limitation "isn't required while traveling or for any other
  iPhone model"
  SRC: https://www.macrumors.com/2026/09/18/iphone-18-pro-max-shipping-restriction/
  VIA: "Since no other iPhones have a single-cell battery over 20Wh, this
  procedure isn't needed for other models." NOTE: scoped to iPhones only —
  script says "no iPhone," never "no phone" or "first ever" (sourcing does
  not establish a claim about every non-Apple device; see structure.md CUT
  list and NOT CLAIMED below).

- CLAIM: Every iPhone 18 Pro Max unit — including new retail units — ships
  discharged/capped below 20 Wh from the time it is manufactured through
  factory transport; activating the phone removes the limit and restores
  full charging capacity.
  TIER: official
  SURPRISE: 90
  SPOKEN: "So every unit gets discharged at the factory, then capped, until
  it's activated."
  SRC: https://support.apple.com/en-us/127848
  VIA: Apple, verbatim: "iPhone 18 Pro Max uses an innovative
  battery-firmware solution that limits battery capacity to below 20 Wh
  from the time it's manufactured through its transport from the factory.
  When you activate your iPhone, the limit is removed and the battery's
  full charging capacity is available."

- CLAIM: Apple's own 16-inch MacBook Pro carries a bigger total battery
  (99.9 Wh, under the separate 100 Wh assembled-battery limit) than the
  iPhone 18 Pro Max and never needs this treatment. It reportedly reaches
  that total via roughly 5-6 individual cells each under 20 Wh, rather than
  one large cell.
  TIER: single
  SURPRISE: 60
  SPOKEN: "It reportedly spreads the same total across several smaller
  cells, each one under that line."
  SRC: https://www.macrumors.com/2026/09/18/iphone-18-pro-max-shipping-restriction/
  VIA: an unnamed forum commenter, quoted by MacRumors — "Airlines have a
  limit of 100Wh in a device (where the 16-inch MacBook Pro is at 99.9Wh)
  while each single battery cell can only have a maximum of 20Wh," reaching
  its total using "5 or 6 different cells that each are under 20Wh but much
  larger as a combination."
  SRC: https://www.androidauthority.com/phone-battery-transportation-rules-3574123/
  VIA: independent regulatory explainer corroborating the general 20 Wh
  per-cell / 100 Wh per-battery structure (UN Special Provision 188,
  mirrored by IATA/ADR/IMDG), but NOT the specific "5-6 cells" MacBook Pro
  figure, which stays single-sourced to the MacRumors-quoted forum comment —
  hence TIER single and the spoken hedge "reportedly", not "official".

- CLAIM: If the phone is shipped again after activation — for repair,
  trade-in, resale, or as a gift — the discharge-below-20Wh process happens
  again.
  TIER: official
  SURPRISE: 55
  SPOKEN: "Ship this phone again, for repair, trade-in, resale, or as a
  gift, and it happens all over."
  SRC: https://support.apple.com/en-us/127848
  VIA: Apple, verbatim: "if you need to ship your iPhone 18 Pro Max for a
  repair, trade-in, return, or as a gift, for example, use the Prepare to
  Ship feature"

- CLAIM: The discharge can take from a few minutes up to a couple of hours
  depending on starting charge, and the iPhone may become warmer than usual
  during the process.
  TIER: official
  SURPRISE: 50
  SPOKEN: "The battery discharges under that ceiling, running warm while it
  does."
  SRC: https://support.apple.com/en-us/127848
  VIA: Apple, verbatim: "might take only a few minutes, but if you start
  with a full charge, it can take up to a couple of hours" / battery "might
  become warmer than usual. This is expected."

- CLAIM: When shipping for repair, trade-in, or return specifically, the
  charge limit is capped at 80 percent for 14 days after activating
  Prepare to Ship, before it can be disabled.
  TIER: official
  SURPRISE: 75
  SPOKEN: "But send it in for repair, trade-in, or return, and your charge
  gets capped at 80 percent for two weeks after."
  SRC: https://support.apple.com/en-us/127848
  VIA: Apple, verbatim: "If you're enabling Prepare to Ship to send to Apple
  or an iPhone reseller or carrier to repair, trade in, or return, the
  battery charge limit will be capped at 80 percent for 14 days, so that it
  remains below the 20-Wh requirement." / "After the 14-day period, you can
  disable Prepare to Ship and enable full charging."

## FEATURES + HOW TO USE

N/A — this is a news/explainer reel about a single shipping-compliance
feature, not a product/app walkthrough with a feature list.

## NOT CLAIMED

- The exact Wh capacity of the iPhone 18 Pro Max battery (e.g. "21.75 Wh" or
  "21.06 Wh"). Apple's own page states only "over 20 Wh" — the precise
  figures circulating in tech press are calculated by outlets (GSMArena) from
  an EU-mandated energy-label mAh disclosure (5,567 mAh / 5,391 mAh), not an
  Apple-published Wh spec. Not spoken or shown as an Apple-attributed number.
- That the iPhone 18 Pro Max is the first phone from ANY manufacturer, ever,
  to have a single cell over 20 Wh. Sourcing supports only "first iPhone" —
  the script says "no iPhone," never "no phone" or "first ever".
- That international air-transport regulators (IATA, ICAO, ADR) have formally
  approved Apple's firmware-discharge method. Per GSMArena (single source),
  the US regulator (PHMSA) reportedly cleared it in June 2025, but IATA/ICAO/
  ADR reportedly had not yet formally weighed in as of this reporting window.
  Not claimed as globally, uniformly approved.
- That a battery too large to ship by air cannot be shipped at all. A
  >20 Wh single cell can still move via US ground/rail transport under a
  separate, higher DOT threshold — the "can't ship" framing in casual
  coverage applies to air transport specifically. Not claimed as an absolute
  shipping block.
- Any claim sourced only from an AI-synthesized WebSearch summary without an
  independent direct-fetch confirmation (e.g., the 14-day undo detail was
  re-verified against a direct fetch of Apple's own page before being
  included above — see SEARCHED).
- That the "5 or 6 cells" MacBook Pro figure is Apple-confirmed — it is a
  single-sourced, forum-derived figure quoted by MacRumors, spoken hedged
  ("reportedly") rather than stated as fact.
- The menu path (Settings > General > Transfer or Reset iPhone > Prepare to
  Ship) and the "Ready to Ship" red-badge completion state are shown
  ON SCREEN ONLY, via the real Apple screenshot (confirmation beat) and an
  on-screen caption reproducing Apple's own UI text — neither is narrated,
  so neither appears as a ledger CLAIM (the SPOKEN field only tracks
  narration). Sourced to https://support.apple.com/en-us/127848.
- That normal use or air travel with the phone (as opposed to shipping it)
  is restricted in any way. Apple's own page states this explicitly
  ("isn't required while traveling or for any other iPhone model"); the
  point is carried in the script by omission (nothing implies a use-time
  restriction) rather than a dedicated spoken sentence, so it is not a
  formal ledger CLAIM either.

## SEARCHED

### WHAT HAPPENED

- 2026-09-21  "iPhone 18 Pro Max 'Prepare to Ship' battery mode"  (found the
  Apple support page, MacRumors, 9to5Mac, and 6 other outlets — established
  the story is real, dated 2026-09-18/19/20, not a rumor)
- 2026-09-21  "iPhone 'Prepare to Ship' battery feature Apple"  (corroborated
  the same set of facts across a second search pass)
- 2026-09-21  fetched support.apple.com/en-us/127848 directly (three times —
  full feature description, then to pin verbatim quotes on the 20 Wh
  threshold / 14-day cap / undo path, then again to confirm the exact
  "14-day period... can disable Prepare to Ship" wording)
- 2026-09-21  fetched macrumors.com/2026/09/18/iphone-18-pro-max-shipping-restriction
  directly (independent confirmation + the MacBook Pro cell-count
  explanation, sourced to a forum comment quoted in the piece)
- 2026-09-21  fetched 9to5mac.com/2026/09/19/... directly (second independent
  confirmation domain)
- 2026-09-21  research subagent fetched the regulatory background directly:
  Apple's own page, MacRumors, GSMArena (iFixit-sourced battery capacity
  figures), Android Authority (UN Special Provision 188 / IATA/ADR/IMDG),
  FedEx's own dangerous-goods compliance guide (49 CFR 173.185) — see
  research/findings_context.md.

### WHO ELSE TRIED IT

- 2026-09-21  research subagent searched specifically for a real screen
  recording/screenshot of an actual device running the Prepare to Ship flow
  from any outlet, and for hands-on video (YouTube/TikTok) — see
  research/visuals.md. RESULT: none found anywhere, including on Apple's own
  page beyond the one menu screenshot. The feature requires an already-
  activated device later being shipped (repair/trade-in/etc.), a scenario
  that takes time to occur after a September launch, so a genuine hands-on
  of the full flow likely does not exist yet from anyone. This directly
  shaped the manifest's `explicitly_NOT_claimed` list and the decision to
  build two beats (the discharge screen, the "Ready to Ship" badge) as
  motion graphics rather than claimed captures.
- 2026-09-21  research subagent searched iFixit specifically for commentary
  on the firmware-battery-lock mechanism itself (vs. their teardown/capacity
  reporting) — not found; iFixit's coverage is capacity-only, no stated
  opinion on the shipping-compliance feature.

### WHAT ARE PEOPLE SAYING

- 2026-09-21  research subagent read the MacRumors Forums thread ("iPhone 18
  Pro Max Requires 'Prepare to Ship' Battery Drain Before Shipping",
  2026-09-18, page 1 of 3) in full — real, named, timestamped user reactions:
  curiosity, mild confusion (why not the 16" MacBook Pro), some joking, and a
  genuine safety sub-thread about swollen batteries at altitude. No outrage
  or right-to-repair framing on page 1. See research/findings_reaction.md.
  None of this made it into the 70s script (cut for pacing, not because it
  contradicts anything — see structure.md WHAT WAS CUT).
  RESULT: reaction volume is genuinely thin — the story is ~3 days old at
  research time. The one clearly critical/skeptical outlet found (Dissenter,
  "firmware-locks battery") was not fetched directly and is not used as a
  source.

### WHAT WOULD CONTRADICT THIS

- 2026-09-21  research subagent ran a dedicated contradiction pass:
  `"Prepare to Ship" battery clickbait OR wrong OR overhyped OR debunk` —
  found NO outlet disputing the core facts (menu path, threshold number,
  purpose). See research/findings_contradiction.md.
- 2026-09-21  same pass checked whether the feature is confirmed GA (not
  beta-only/unconfirmed): Apple's support page is published and dated
  2026-09-18, iOS 27 itself reached general availability 2026-09-14, and
  real users are already discussing it on the MacRumors Forums — CONFIRMED
  live, not a leak or beta-only claim.
  same pass checked whether "20 Wh" is Apple's own language or press
  rounding: CONFIRMED as Apple's own verbatim wording (quoted directly from
  the support page) — but the EXACT Wh figures used elsewhere in tech press
  (21.75/21.06 Wh) are press-calculated from an EU energy-label mAh
  disclosure, not an Apple-published Wh spec — hence excluded from the
  script and manifest (see NOT CLAIMED).
  same pass searched for any prior phone (any brand, any year) with a
  single-cell battery over 20 Wh: NONE found — only dual-cell workarounds
  (OnePlus, OPPO, rumored Samsung SDI) that stay under the line by splitting
  cells, which is circumstantial support for, not proof of, "first" framing
  — hence the script's careful "no iPhone," never "first phone ever."

### VISUALS SCOUTED

- 2026-09-21  scouted and captured Apple's own official "Prepare to Ship"
  menu screenshot (cdsassets.apple.com, direct asset fetch, already a
  portrait device-frame render) and Apple's official iPhone 18 Pro Burgundy
  product photography (apple.com/v/iphone-18-pro CDN, direct asset fetch)
  into _sources/iphone-18-battery-prepare-to-ship/ then
  public/assets/iphone-18-battery-prepare-to-ship/ — see that folder's
  manifest.json for full asset records and the `explicitly_NOT_claimed`
  entries covering the two beats built as motion graphics instead of
  captures.

INDEPENDENT-CHECK: MacRumors and 9to5Mac both confirm the feature
independently, neither citing the other or a shared leaker (this is a
published Apple support page, not a leak) — PASS, two-domain minimum met.
The regulatory-threshold claim (20 Wh / 100 Wh split) is corroborated by
GSMArena, Android Authority, and FedEx's own compliance documentation, none
tracing to a shared single origin — PASS. The one single-tier claim (the
MacBook Pro's "5-6 cells") is spoken hedged with "reportedly" per S20.
