# Research — ai-website-builder

Claims ledger + search log. Findings in `research/` (plan.md, findings_features_howto.md,
findings_price_reviews.md, findings_visuals.md, findings_alternatives.md).
Lead: the user's reference reel (Editminds Tech, YouTube Short lDQTPOEFnEU, 2025-09-04) —
"DeepSite v2, powered by DeepSeek, redesign by link, click to edit". 13 months stale:
DeepSite is now v4, defaults to Kimi K2.5, and is being migrated into HuggingChat. Every
spoken claim traces to Hugging Face's own pages or its open-source chat-ui code.

## CLAIMS

- CLAIM: HuggingChat's "Make my website" starter asks your name, what you do, your links and the style you want.
  TIER: official
  SPOKEN: "Tell it your name, what you do, your links and a style."
  SURPRISE: 75
  SRC: https://github.com/huggingface/chat-ui/blob/main/src/lib/constants/mcpExamples.ts
  VIA: Hugging Face chat-ui source, example "Make my website": "First ask me, in a few short lines: my name, what I do, links that represent me ... and the style I want."
  SRC: https://huggingface.co/chat/
  VIA: live HuggingChat home (fetched 2026-10-05) lists the starter "Make my website"

- CLAIM: The starter then researches you: it fetches your links, or searches the web for your name if you shared none, and builds the site without more questions.
  TIER: official
  SPOKEN: "it reads those links, or searches your name if you skip them, and writes the whole page"
  SURPRISE: 80
  SRC: https://github.com/huggingface/chat-ui/blob/main/src/lib/constants/mcpExamples.ts
  VIA: same prompt: "research me with your tools: fetch my links, or search the web for my name if I shared none. Once done, build the site right away"
  SRC: https://github.com/huggingface/chat-ui/pull/2303
  VIA: PR #2303 (merged 2026-06-10): web pages are "rendered in a dedicated side panel ... with live preview"

- CLAIM: The hook's "looks you up" is the same researched-you behaviour, as instructed by the official starter prompt.
  TIER: official
  SPOKEN: "Hugging Face's free AI asks who you are, looks you up, then builds your website."
  SURPRISE: 80
  SRC: https://github.com/huggingface/chat-ui/blob/main/src/lib/constants/mcpExamples.ts
  VIA: "Then research me with your tools ... search the web for my name"

- CLAIM: HuggingChat is Hugging Face's own chat app.
  TIER: official
  SPOKEN: "It's called HuggingChat"
  SURPRISE: 40
  SRC: https://huggingface.co/chat/
  VIA: "Welcome to HuggingChat, the chat app powered by open source AI models."
  SRC: https://github.com/huggingface/chat-ui
  VIA: "The open source codebase powering HuggingChat"

- CLAIM: DeepSite, Hugging Face's AI website builder, is being migrated into HuggingChat.
  TIER: official
  SPOKEN: "Hugging Face is moving its website builder, DeepSite, in here"
  SURPRISE: 85
  SRC: https://deepsite.hf.co/
  VIA: DeepSite's own modal (captured on mobile 2026-10-05): "DeepSite is moving to Hugging Face Chat" / "We are migrating DeepSite into Hugging Face Chat"; only link "Open Hugging Face Chat"
  SRC: https://huggingface.co/api/spaces/enzostvs/deepsite
  VIA: Space "DeepSite v4" by enzostvs (HF staff), 16,610 likes; old Space URL 302-redirects to deepsite.hf.co

- CLAIM: You watch the page being written live, in a side panel.
  TIER: official
  SPOKEN: "writes the whole page while you watch"
  SURPRISE: 40
  SRC: https://github.com/huggingface/chat-ui/pull/2303
  VIA: "unclosed artifacts grow as tokens arrive"; "live preview, code view, and version history"
  SRC: https://deepsite.hf.co/promo.mp4
  VIA: official promo "02 Watch it build."

- CLAIM: Follow-up requests change only the targeted part instead of rewriting the page.
  TIER: official
  SPOKEN: "Ask for a change and it edits only that part."
  SURPRISE: 45
  SRC: https://github.com/huggingface/chat-ui/pull/2303
  VIA: "targeted edits ... Small changes don't re-emit the whole artifact."

- CLAIM: One click deploys the page as a static Hugging Face Space owned by you, with its own URL.
  TIER: official
  SPOKEN: "one tap puts it online as a free Hugging Face Space, with its own link"
  SURPRISE: 65
  SRC: https://github.com/huggingface/chat-ui/pull/2370
  VIA: PR #2370 (merged 2026-06-22): "a one-click Deploy to Space action ... publishes an artifact as a static Hugging Face Space owned by the logged-in user"; dialog shows "success URL"
  SRC: https://huggingface.co/docs/hub/spaces-sdks-static
  VIA: "Static Spaces are free for everyone ... creating them never requires a paid plan."

- CLAIM: HuggingChat itself is free to use with a Hugging Face account; model usage draws on monthly Inference Providers credits.
  TIER: official
  SPOKEN: "It's free to start, which is where the catch comes in."
  SURPRISE: 30
  SRC: https://huggingface.co/docs/inference-providers/pricing
  VIA: "Every Hugging Face user receives monthly credits"; Free Users "$0.10, subject to change"
  SRC: https://github.com/huggingface/chat-ui
  VIA: chat-ui speaks to "the Hugging Face Inference Providers router"; login wall observed on huggingface.co/chat 2026-10-05

- CLAIM: A free Hugging Face account gets $0.10 of Inference Providers credit a month.
  TIER: official
  SPOKEN: "a free account gets ten cents of AI credit a month"
  SURPRISE: 85
  SRC: https://huggingface.co/docs/inference-providers/pricing
  VIA: table row Free Users: "$0.10, subject to change"
  SRC: https://discuss.huggingface.co/t/the-free-hugging-chat-limits/176499
  VIA: forum thread (2026-06-03/05) quoting the same table for HuggingChat

- CLAIM: One HuggingChat user reported spending the monthly free allowance in two queries.
  TIER: single
  SPOKEN: "One user says theirs was gone in two questions."
  SURPRISE: 80
  SRC: https://discuss.huggingface.co/t/the-free-hugging-chat-limits/176499
  VIA: meepmeow02, 2026-06-03: "I manged to use 10p in 2 quries"

- CLAIM: Hugging Face PRO costs $9 a month.
  TIER: official
  SPOKEN: "Pro costs nine dollars monthly and gives you twenty times that."
  SURPRISE: 40
  SRC: https://huggingface.co/pricing
  VIA: PRO "$9/month", "20× included inference credits"
  SRC: https://huggingface.co/docs/inference-providers/pricing
  VIA: PRO Users "$2.00" monthly credits

## FEATURES + HOW TO USE

Two products in play. The reel follows the NEW home (HuggingChat), because DeepSite says it is moving there.

HuggingChat website building (chat-ui, primary source = code + live site):
- "Make my website" starter (asks name/role/links/style, researches you, builds one HTML file with Tailwind) — USED (the spine)
- Artifacts side panel: live preview while generating — USED ("while you watch")
- Targeted edits — USED ("edits only that part")
- Version history / line diff — CUT (one feature too many; caption)
- One-click Deploy to Space, public/private toggle, re-deploy updates in place — USED (deploy + "its own link"); public/private CUT for length
- "Made with HuggingChat" badge added to deployed Spaces (PR #2456) — CUT (caption / viewer question)
- Model choice / Omni router — CUT (no viewer value in 50s)
- React, SVG, Mermaid artifacts — CUT

DeepSite v4 (still live at deepsite.hf.co):
- Redesign from a URL (redesign.tsx) — CUT: the reel follows HuggingChat; redesign has not been confirmed there
- "Click and edit any element" (the reference reel's claim) — CUT: not found in v4 code (old v2 feature)
- Multi pages, media upload, download, model picker (Kimi K2.5 default) — CUT
- "Powered by DeepSeek" (reference reel) — NOT CLAIMED: stale, default is Kimi K2.5

HOW TO USE (vendor steps, HuggingChat): open huggingface.co/chat, sign in with a Hugging Face account, tap "Make my website", answer its questions, watch it build in the side panel, ask for edits, tap Deploy to publish as a Space.

## NOT CLAIMED

- "Builds a website in minutes" as a timed fact — no vendor time figure; we never time a build. Script says "while you watch", not a duration.
- "No account needed" (listicles) — false: HuggingChat and DeepSite both redirect to HF login.
- "Unlimited free" / "completely free" (reference reel) — false: $0.10 monthly credit.
- "Powered by DeepSeek" / "DeepSite v2" (reference reel) — stale.
- "Click and edit any part" — not in DeepSite v4 code; not claimed for HuggingChat.
- "Redesign any site by pasting a link" — true for DeepSite v4, unverified in HuggingChat; not said.
- "How many websites ten cents buys" — depends on model and length; no source; not said. The forum "two questions" is one user's report, spoken hedged ("says").
- Backend / database / login for generated sites — static Spaces only ("no backend" per PR #2370); not claimed either way.
- "Better than Bolt / Lovable / Cursor" (reference reel) — no comparison made.
- "16,000+ likes / most liked Space" — 16,610 per HF API, but cut; not needed.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-05  yt-dlp metadata of reference lDQTPOEFnEU  (tool = DeepSite v2, Sept 2025 framing)
- 2026-10-05  deepsite.hf.co mobile capture  (DeepSite v4; modal "moving to Hugging Face Chat"; promo.mp4)
- 2026-10-05  HF API spaces/enzostvs/deepsite + repo files  (v4, MIT, Kimi K2.5 default, last commit 2026-02-06)
- 2026-10-05  "DeepSite moving to Hugging Face Chat"  (no press coverage; the modal is the record)
- 2026-10-05  gh api huggingface/chat-ui commits + PRs #2303 #2370 #2456  (artifacts 2026-06-10, Make my website 2026-06-12, deploy to Space 2026-06-22, badge 2026-07-29)
- 2026-10-05  huggingface.co/docs/inference-providers/pricing, /pricing, /docs/hub/spaces-sdks-static  ($0.10 / $2.00, PRO $9, static Spaces free)

### 2. WHO ELSE TRIED IT — hands-on by someone who is not the vendor
- 2026-10-05  "DeepSite review hands-on"  (Ashik Nesin, aiengineerguide.com 2025-11-29: "a good start", AI-look output)
- 2026-10-05  "HuggingChat build website deploy to Spaces"  (no independent hands-on of the HuggingChat builder found)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-05  DeepSite Space discussions #503 #562 #563 #466  (login loops, credit wall at ~5 prompts, edits deleting sections in v4, download unclear)
- 2026-10-05  "HuggingChat free limits 2026"  (forum: free allowance gone in two queries; asks for daily limits)
- 2026-10-05  discuss.huggingface.co "What happened to DeepSite 2.0"  (2026-04: v2 outdated, v4 current)

### 4. WHAT WOULD CONTRADICT THIS — trying to prove the story wrong
- 2026-10-05  "deepsite no account needed free unlimited"  (listicles claim it; current code returns 401 without login — contradicted, listed under NOT CLAIMED)
- 2026-10-05  HuggingChat login test on mobile  (welcome card -> huggingface.co/login: account required)
- 2026-10-05  chat-ui code search "deepsite"  (no mention: the migration is stated by DeepSite, not yet by chat-ui; script says "is moving in", present progressive, matching the modal)

INDEPENDENT-CHECK: 2026-10-05 searched DeepSite/HuggingChat hands-on reviews, HF forum and Space discussions — found one independent DeepSite review (aiengineerguide.com, "a good start"), many user complaints about credits and edits, and one forum report of the free HuggingChat allowance gone in two queries. No independent hands-on of the HuggingChat website builder itself exists yet; the feature claims are Hugging Face's own code, so they are spoken as what it does, and the one user report is hedged.
