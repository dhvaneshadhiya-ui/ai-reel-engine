# Research — five-free-ai-presentation-tools

Claims ledger + search log. Findings files: research/findings_*.md (four parallel agents,
2026-09-23), plan in research/plan.md, visuals in research/visuals.md.

## CLAIMS

- CLAIM: Gamma generates a full presentation from a topic prompt ("Generate – AI drafts an initial version based on your topic").
  TIER: official
  SPOKEN: "Gamma builds a whole designed deck from one prompt."
  SURPRISE: 20
  SRC: https://help.gamma.app/en/articles/7838093-how-do-i-create-a-new-presentation-document-or-webpage-in-gamma
  VIA: Gamma's own help centre

- CLAIM: Gamma's free plan is 400 AI credits given once at sign-up that never refresh, up to 10 slides per prompt, and free-plan PDF/PPTX exports carry the "Made by Gamma" badge.
  TIER: official
  SPOKEN: "Free is four hundred credits at signup that never top up, ten slides per prompt, and a Gamma badge on exports."
  SURPRISE: 70
  SRC: https://help.gamma.app/en/articles/7834324-how-do-credits-work-in-gamma
  VIA: Gamma help centre ("Each new Free user receives 400 credits when initially signing up." / "credits do not refresh")
  SRC: https://help.gamma.app/en/articles/8077107-how-can-i-upgrade-my-gamma-subscription
  VIA: Gamma help centre ("Generate up to 10 slides in a single prompt" / "AI credits do not refresh in the Free Plan.")
  SRC: https://help.gamma.app/en/articles/8022861-what-s-the-easiest-way-to-export-my-gamma
  VIA: Gamma help centre ("The 'Made by Gamma' badge appears on PDF and PPTX exports when your workspace is on the Free plan")

- CLAIM: Claude's free plan can create downloadable PowerPoint (.pptx) files; it is enabled under Settings > Capabilities, and file creation draws from the plan's usage limit faster than normal chat.
  TIER: official
  SPOKEN: "Free Claude makes them into a real PowerPoint file. Turn on file creation in settings, and expect it to eat your limit faster."
  SURPRISE: 75
  SRC: https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude
  VIA: Anthropic help centre ("available to all Claude users (Free, Pro, Max, Team, and Enterprise)" / "PowerPoint presentations (.pptx)" / "Enable file creation from Settings > Capabilities" / "creating files will use more of your limit compared to normal chats")
  SRC: https://claude.com/blog/create-files
  VIA: Anthropic's own announcement

- CLAIM: Pitch's agent edits a deck through chat (its own suggested prompt: "This slide is too wordy, can you trim it?"); the free plan is 100 AI credits that do not renew, and PowerPoint export is a Plus feature (free PDF exports are branded).
  TIER: official
  SPOKEN: "Pitch fixes the deck by chat: tell it a slide is too wordy. Free is a hundred credits that never renew, and PowerPoint export costs extra."
  SURPRISE: 65
  SRC: https://pitch.com/pricing
  VIA: Pitch pricing ("100 AI credits — … This amount does not renew once used." / "PDF exports Branded" / PowerPoint exports on Plus)
  SRC: https://help.pitch.com/en/articles/12755590-guide-to-ai-credits
  VIA: Pitch help centre ("100 lifetime (non-recurring) credits for new Free accounts.")
  SRC: https://pitch.com/use-cases/ai-presentation-maker
  VIA: Pitch ("refines slides through chat"); the wordy-slide prompt is visible in Pitch's own help screenshot

- CLAIM: PowerPoint Designer turns text such as lists and timelines into graphics; on PowerPoint for the web it is available to everyone (desktop needs a subscription), and it needs the file stored in OneDrive or SharePoint.
  TIER: official
  SPOKEN: "On the web, Designer turns a bullet list into a timeline, free for everyone. Keep the file in OneDrive."
  SURPRISE: 70
  SRC: https://support.microsoft.com/en-us/office/create-professional-slide-layouts-with-designer-53c77d7b-dc40-45c2-b684-81415eac0617
  VIA: Microsoft support ("On PowerPoint for the web, design suggestions are available to everyone." / "can turn text such as lists, processes, or timelines into an easily readable graphic"); Microsoft's own before/after sample slides are a bullet list and a timeline of the same dates
  SRC: https://www.microsoft.com/en-us/microsoft-365/free-office-online-for-the-web
  VIA: Microsoft ("Get free access to Word, Excel, and PowerPoint using Microsoft 365 for the web")

- CLAIM: Napkin turns text into diagrams; its free plan is 500 AI credits per week, and Napkin branding on exports cannot be turned off on Free.
  TIER: official
  SPOKEN: "Napkin draws a paragraph as one: five hundred credits a week, with its logo on every export."
  SURPRISE: 60
  SRC: https://www.napkin.ai/pricing/
  VIA: Napkin pricing ("500 AI credits per week" / "Napkin branding on visuals")
  SRC: https://help.napkin.ai/en/articles/15924385-how-to-remove-the-napkin-watermark-from-exports
  VIA: Napkin help centre (the toggle "cannot be turned off" on Free)
  SRC: https://www.napkin.ai/
  VIA: Napkin ("Napkin Visuals turns your text into diagrams, flowcharts, mind maps, infographics, and data charts.")

- CLAIM: Gamma's free plan can import an existing PowerPoint (and PDF), so a Claude-made .pptx can be brought into Gamma.
  TIER: official
  SPOKEN: "draft in Claude, import the file into Gamma"
  SURPRISE: 55
  SRC: https://help.gamma.app/en/articles/7838093-how-do-i-create-a-new-presentation-document-or-webpage-in-gamma
  VIA: Gamma help centre ("Import – AI converts existing files, decks, or web pages" / "Upload a PowerPoint, document, or enter a URL")
  SRC: http://web.archive.org/web/20260921101008/https://gamma.app/pricing
  VIA: Gamma pricing, Free card ("Import from PDF & PPTX"; live page 403s to fetch, snapshot 2026-09-21)

## FEATURES + HOW TO USE

Gamma:
- Generate from a topic — USED. Paste text / Import file or URL — USED (the close: import the Claude file).
- Edit a slide with AI (sparkle icon), AI Agent, themes, images, export to PDF/PPTX/PNG/Google Slides — CUT: the free ceiling is the point; export badge USED.
- How to use (vendor): Create New AI > Generate > enter topic > edit outline > generate. Shown via Gamma's own demo (prompt box, "Generate outline", outline filling in).
Claude:
- Create .xlsx/.pptx/.docx/PDF — USED (.pptx only). Save to Google Drive — CUT. Claude for PowerPoint add-in — CUT: paid plans only.
- How to use (vendor): Settings > Capabilities > toggle Code execution and file creation on > describe the file > download. USED (the toggle).
Pitch:
- Agent generates decks from a prompt — CUT (Gamma already carries prompt-to-deck). Chat edits (rewrite, trim, add slides) — USED. Brand from domain, 20+ AI actions, image tools — CUT for time.
- How to use (vendor): Create with AI > prompt > template > Generate; edit in the Pitch Agent panel. Panel USED.
PowerPoint Designer:
- Layout suggestions; turns lists/timelines into graphics — USED. Theme ideas / photo layouts — CUT. Copilot in PowerPoint — CUT: paid (M365 Personal and up).
- How to use (vendor): Design tab > Design Suggestions > pick one. Requires file in OneDrive/SharePoint — USED.
Napkin:
- Text to diagrams/flowcharts/mind maps/charts — USED. Napkin Slides (beta decks) — CUT: its PPT export on Free contradicts the pricing page, unresolved. Import PPT/DOC/PDF — CUT.
- How to use (vendor): paste text > generate > pick a visual > customize > export. Shown via Napkin's own flow poster.

## NOT CLAIMED

- Any ranking or "best". The reel states what each free plan gives.
- Canva. Its pricing page lists Premium AI (Canva AI) as included on Free with 20 AI uses a month, but a June 2026 hands-on (nexodatech.com) found the presentation generator not available free, and Canva's own eligibility table lists only paid plans. Unresolved, so excluded rather than hedged.
- Google Slides + Gemini: needs Google AI Pro ($19.99) or a Workspace plan; free only through the Workspace Experiments tester programme (18+, some countries, desktop, English). Excluded.
- Copilot in PowerPoint: "free plans … don't come with Copilot access". Excluded. The "60 AI credits a month" figure is stale and not used.
- Plus AI and Beautiful.ai: trials requiring a card. SlidesGPT: export is paid. Genspark: undisclosed lifetime cap. Presentations.AI: "100 credits … Up to 20 Slides" on Starter, but whether credits renew and whether free export is watermarked are not stated. Kimi: free amount not published. All excluded.
- Any paid price for Gamma Plus (only third-party figures, $8-9; gamma.app/pricing blocks fetching). No price spoken for Gamma.
- Credits per deck for Gamma, Pitch or Napkin: no vendor publishes it. The reel never converts credits into decks.
- That Claude files carry no watermark: not stated by Anthropic, so not claimed.
- That Designer has no limit: Microsoft states no cap, but absence of a stated cap is not a claim of unlimited use.
- Napkin's "~100 credits per slide" and "Monday reset": third-party only.
- "Save this for the night before your next deck" is a CTA, not a claim.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-23  "Gamma free plan credits 400 help center pricing 2026"  (Gamma help centre: 400 one-time credits, 10 slides/prompt, badge on exports)
- 2026-09-23  "Pitch AI presentation generator how to use help center pitch.com"  (Pitch Agent, 100 lifetime credits, PPTX on Plus)
- 2026-09-23  "Canva free plan AI uses per month Magic Write Magic Design help center"  (20 AI uses/month; presentation generator eligibility contradictory)
- 2026-09-23  "Napkin AI pricing free plan credits per week"  (500 credits/week, branding on Free)
- 2026-09-23  "Copilot in PowerPoint free Microsoft account personal 2026"  (Copilot paid; Designer free on the web)
- 2026-09-23  "Gemini in Google Slides personal Google account free "Help me create" 2026"  (Slides AI needs AI Pro / Workspace)
- 2026-09-23  "Claude create and edit files PowerPoint free plan support.claude.com"  (file creation on Free, .pptx, Settings > Capabilities)
- 2026-09-23  fetched presentations.ai/pricing, plusdocs.com, slidesgpt.com, kimi.ai text-to-ppt  (trial/card/export limits -> excluded)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-23  "PowerPoint for the web Designer "free" Microsoft account review 2026"  (no contradiction; "Microsoft Designer 15 credits" reviews are a different product)
- 2026-09-23  "reddit Canva free "20" AI uses limit 2026 Canva AI presentation free plan"  (nexodatech 2026-06-14 hands-on: presentation generator not free -> Canva excluded)
- 2026-09-23  "Pitch.com free plan review 2026 AI credits 100 limit PDF branding"  (toolradar/anygen agree with Pitch's own page)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-23  "reddit gamma app free credits ran out watermark free plan"  (the complaint is that 400 credits are lifetime, not monthly, and the badge — the reel leads each tool's catch with exactly that)
- 2026-09-23  "reddit napkin ai free plan credits ran out watermark"  (techpoint.africa hands-on: credits "run dry quickly", "The only catch was the watermark")

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-23  ""PowerPoint for the web" Copilot free Microsoft account without subscription"  (confirmed Copilot is NOT free, so the reel names Designer, not Copilot)
- 2026-09-23  "reddit Google Workspace Experiments Gemini Slides free personal account generate presentation"  (Slides AI free only via a tester programme -> excluded)
- 2026-09-23  "help.napkin.ai Napkin Slides credits per slide free plan export watermark"  (Napkin Slides export on Free contradicts pricing -> Slides not claimed; diagrams only)

INDEPENDENT-CHECK: 2026-09-23 searched hands-on reviews and user complaints for every candidate. Found a June 2026 hands-on contradicting Canva's free presentation generator (Canva cut), techpoint.africa's hands-on of Napkin's credits and watermark (consistent with the pricing page), and user complaints about Gamma's credits being lifetime (consistent). The per-tool ceilings themselves are what each vendor's own page states; there is no independent test of a price list, which is why those claims are official-tier.
