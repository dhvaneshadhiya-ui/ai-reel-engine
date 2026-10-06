# Research — openai-image-ads

Claims ledger + search log. Tiers: official / multi / single / disputed.

## CLAIMS

- CLAIM: OpenAI is introducing a visual ad format in ChatGPT, tested first during image generation
  TIER: official
  SPOKEN: "during image generation only"
  SURPRISE: 80
  SRC: https://openai.com/index/new-chatgpt-ads-format-and-measurement/
  SRC: https://techcrunch.com/2026/10/05/openai-launches-visual-ads-that-appear-alongside-image-generation-results/
  SRC: https://www.bleepingcomputer.com/news/artificial-intelligence/openai-will-show-visual-ads-in-chatgpt-while-you-generate-images/
  VIA: OpenAI announcement, Oct 5 2026 ("Initially, we'll test this new ad format during image generation in ChatGPT.")

- CLAIM: OpenAI's own example shows the image at 62% loaded with a Heirloom Grocery ad (photos + Learn more button) directly under it
  TIER: official
  SPOKEN: "the image is sixty-two percent done, and right under it is a grocery ad, with photos and a Learn more button"
  SURPRISE: 85
  SRC: https://openai.com/index/new-chatgpt-ads-format-and-measurement/
  VIA: OpenAI hero image heirloom-grocery-visual-ads-hero.png (alt: "Two ChatGPT mobile screens show Heirloom Grocery visual ads with product images and Learn more buttons during image generation."), opened and read 2026-10-06

- CLAIM: Testing begins later this month (October 2026) in the US with an initial group of advertisers
  TIER: official
  SPOKEN: "Testing starts later this month in the US"
  SURPRISE: 60
  SRC: https://openai.com/index/new-chatgpt-ads-format-and-measurement/
  SRC: https://www.bleepingcomputer.com/news/artificial-intelligence/openai-will-show-visual-ads-in-chatgpt-while-you-generate-images/
  VIA: OpenAI ("Testing will begin later this month in the US with an initial group of advertisers.")

- CLAIM: Ad testing in ChatGPT began in the US on February 9, 2026, with ads appearing below the end of a response
  TIER: official
  SPOKEN: "ads have run under its answers since February"
  SURPRISE: 40
  SRC: https://help.openai.com/en/articles/20001047-ads-in-chatgpt
  SRC: https://www.searchenginejournal.com/openai-begins-testing-ads-in-chatgpt-for-free-and-go-users/
  VIA: OpenAI help center ("Ad testing started in the United States on February 9, 2026." / "Ads can appear below the end of a response.")

- CLAIM: OpenAI says the visual format shows product inspiration, product usage, or the experiences a product makes possible
  TIER: official
  SPOKEN: "Now they get pictures, showing a product or how you'd use it"
  SURPRISE: 30
  SRC: https://openai.com/index/new-chatgpt-ads-format-and-measurement/
  VIA: OpenAI ("images showing product inspiration, product usage, or the experiences they make possible")

- CLAIM: Ads are clearly labeled, separate from the generated image, and do not influence ChatGPT's answers (OpenAI's stated policy, attributed)
  TIER: official
  SPOKEN: "OpenAI says the ads are labeled, kept separate from your image, and don't change ChatGPT's answers"
  SURPRISE: 35
  SRC: https://openai.com/index/new-chatgpt-ads-format-and-measurement/
  SRC: https://techcrunch.com/2026/10/05/openai-launches-visual-ads-that-appear-alongside-image-generation-results/
  VIA: OpenAI ("Ads will be clearly labeled, and remain separate from the image being created. ... advertising does not influence the answers ChatGPT provides.")

- CLAIM: ChatGPT reaches 1.2 billion people each week
  TIER: official
  SPOKEN: "ChatGPT reaches one point two billion people a week"
  SURPRISE: 45
  SRC: https://openai.com/index/new-chatgpt-ads-format-and-measurement/
  SRC: https://www.bleepingcomputer.com/news/artificial-intelligence/openai-will-show-visual-ads-in-chatgpt-while-you-generate-images/
  VIA: OpenAI's own figure (self-reported)

- CLAIM: Ads may appear for Free and Go users; Plus, Pro, Business, Enterprise and Edu get no ads; no ads for accounts identified as under 18
  TIER: official
  SPOKEN: "Paying for Plus, Pro, Business, Enterprise or Edu? You get no ads. Free and Go users do, unless they're under eighteen"
  SURPRISE: 55
  SRC: https://help.openai.com/en/articles/20001047-ads-in-chatgpt
  SRC: https://www.searchenginejournal.com/openai-begins-testing-ads-in-chatgpt-for-free-and-go-users/
  VIA: OpenAI help center

- CLAIM: Free users can switch to Ads-Free via Settings > Ads controls; it brings lower message limits and no access to tools like image generation
  TIER: official
  SPOKEN: "OpenAI's help page says it costs you messages, and image generation"
  SURPRISE: 90
  SRC: https://help.openai.com/en/articles/20001047-ads-in-chatgpt
  VIA: OpenAI help center ("This removes ads, but comes with lower usage limits and reduced feature access (for example, fewer messages and no access to some tools like image generation or deep research)." / steps: Settings > Ads controls > Change plan > Reduce message limits)
  ONE-SOURCE-OK: this is OpenAI's own documented product behaviour; the help center is the authority on it. The inference "if you make images for free, the ads come with them" follows from it plus the official image-generation placement, and holds only where ads are being tested.

## NOT CLAIMED

- Ads paying for / funding image generation: OpenAI says ads "help us bring the benefits of AI to more people", not that they fund images specifically.
- Any Plus/Go price: not fetched from an OpenAI page this session — no price is spoken.
- That the ad appears ONLY while loading: OpenAI's wording is "during image generation"; the 62% bar is from its own example image, and the script attributes it ("In its own example").
- Heirloom Grocery as a real advertiser: it is OpenAI's sample brand in a mockup; the script says "a grocery ad".
- Measurement partners, WeightWatchers CPA -15.3%, Dose, Portland Leather stats: advertiser-facing, cut (see structure.md).
- Global rollout: TechCrunch says "will eventually" target all users "once they roll out globally" — speculative, not spoken.
- Dec 2025 "promotional messages" controversy (app suggestions, no financial component): different thing, not ads; not spoken.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-06  fetched techcrunch.com ref article (Sarah Perez, Oct 5)  (core claims, no OpenAI quotes in it)
- 2026-10-06  "openai.com ads ChatGPT visual ad format image generation measurement partners"  (found partner list, led to primary)
- 2026-10-06  openai.com/index/new-chatgpt-ads-format-and-measurement/ (403 to WebFetch; rendered in headless Chrome, text saved to _sources/openai-image-ads/openai-announcement.txt)  (primary wording, hero image)
- 2026-10-06  help.openai.com/en/articles/20001047-ads-in-chatgpt (rendered, saved help-ads.txt)  (plans, under-18, Ads-Free tradeoff, Feb 9 start)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-10-06  "OpenAI ChatGPT visual ads image generation results October 2026"  (BleepingComputer, Gadget Review, Quartz, PYMNTS — all report the announcement; nobody has seen a live visual ad yet, testing starts later in October)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-06  "OpenAI visual ads ChatGPT image generation criticism reaction users"  (no reaction to the visual format yet; past backlash in Dec 2025 over "promotional messages" for paying users, Mark Chen said OpenAI "fell short")
- 2026-10-06  "ChatGPT ads which plans see ads Free Go tier Plus ad-free help center 2026"  (Free opt-out with fewer messages, confirmed by SEJ Feb 9 coverage)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-10-06  checked help center for whether Ads-Free on Free keeps image generation — it explicitly does not ("no access to tools like images"); checked whether Plus sees ads — it does not.
- 2026-10-06  checked whether the format is live now — it is not; "later this month", test only, US only. Script says "about to" and "Testing starts".

INDEPENDENT-CHECK: 2026-10-06 searched for hands-on sightings of the visual ad format and user reaction — found none; the format is not live until later in October, so every outlet (TechCrunch, BleepingComputer, Quartz, PYMNTS) reports OpenAI's announcement. Plan/opt-out facts independently confirmed by Search Engine Journal (Feb 9 2026).
