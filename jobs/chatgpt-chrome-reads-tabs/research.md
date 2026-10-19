# Research — chatgpt-chrome-reads-tabs

Claims ledger + search log. Sources reused from the same-day sibling job jobs/chatgpt-chrome-tabs/research/.

## CLAIMS

- CLAIM: OpenAI's 15 Oct 2026 update to the ChatGPT Chrome extension lets ChatGPT use your open Chrome tabs.
  TIER: official
  SPOKEN: "OpenAI's October 15th update to the ChatGPT Chrome extension hands ChatGPT every tab you have open"
  SURPRISE: 55
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI's own announcement ("ChatGPT can now use your tabs in Chrome")
  SRC: https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg
  VIA: Chrome Web Store listing, version updated 15 Oct 2026

- CLAIM: ChatGPT has a Chat / Work toggle; in Chat it looks across your open tabs, in Work it can control them.
  TIER: official
  SPOKEN: "Leave it on Chat, and ChatGPT just reads them"
  SURPRISE: 60
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI's own announcement (Chat "can look across your open tabs and gather info"; Work "can control your Chrome tabs"); the Chat | Work toggle is visible in OpenAI's demo video 1 at 0:03
  SRC: https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/
  VIA: OpenAI X thread

- CLAIM: OpenAI's demo: eight sofa tabs open, the user asks which fits their apartment, ChatGPT compares the tabs and answers with a clear favorite.
  TIER: official
  SPOKEN: "Ask which one fits, and it compares every tab and picks a favorite"
  SURPRISE: 50
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI's own demo video 1 (4K), frames read 2026-10-19: 8 sofa tabs; "compare dimensions, materials, and prices"; "I found seven sofa options across your open tabs, and I already have a clear favorite."

- CLAIM: In Work, ChatGPT can control Chrome tabs to send messages, fill out forms, download files, and organize/group tabs.
  TIER: official
  SPOKEN: "it can send messages, fill out forms, download files, and even group your tabs"
  SURPRISE: 70
  SRC: https://ppc.land/chatgpt-gains-control-of-chrome-tabs-to-fill-forms-and-send-messages/
  VIA: OpenAI @ChatGPT X thread ("sending messages, filling out forms, or downloading files"; "organize and group that pile of tabs")
  SRC: https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/
  VIA: OpenAI @ChatGPT X thread

- CLAIM: By default ChatGPT asks before it interacts with each new website.
  TIER: official
  SPOKEN: "Before it acts on a new website, it asks you first, by default"
  SURPRISE: 65
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation ("By default, ChatGPT asks before it interacts with each new website.")
  SRC: https://www.beri.net/article/chatgpt-chrome-extension-work-mode-computer-use-logged-in-tabs-enterprise-admin-controls-allowlist-no-action-log
  VIA: OpenAI docs; independent analysis that approval is per site

- CLAIM: Setup: add the ChatGPT extension to Chrome and @-mention Chrome.
  TIER: official
  SPOKEN: "add the ChatGPT extension to Chrome, then mention @Chrome when you ask"
  SURPRISE: 45
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation (install the extension; select your browser with an @-mention)
  SRC: https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg
  VIA: Chrome Web Store listing

- CLAIM: OpenAI says the extension is available on all ChatGPT plans.
  TIER: official
  SPOKEN: "According to OpenAI, the extension is available on every ChatGPT plan"
  SURPRISE: 50
  SRC: https://x.com/ChatGPT/status/2110825327811580209
  VIA: OpenAI's own post ("Available for all ChatGPT plans")
  SRC: https://the-decoder.com/chatgpt-becomes-a-full-chrome-browser-assistant-that-reads-and-acts-on-your-open-tabs/
  VIA: OpenAI X thread

## FEATURES + HOW TO USE

- Chat: look across open tabs and gather info — USED (the whole reel)
- Work: control tabs (messages, forms, downloads, grouping) — USED (the second half of the switch)
- Side chat panel, highlighted text, YouTube transcripts — CUT: shipped 30 Jul
- Per-website permission prompts — USED for acting ("before it acts on a new website"); not claimed for reading
- Works in Edge, Brave, Opera, Vivaldi — CUT: title is Chrome
How to use: add the extension from the Chrome Web Store — USED; @-mention Chrome — USED; desktop app Settings > Computer Use — CUT (the demo itself runs at chatgpt.com in Chrome)

## NOT CLAIMED

- That reading tabs is brand new: side chat could reference open tabs from 30 Jul 2026. The script says "can now ... reading across your open Chrome tabs" from Chat, which is what OpenAI announced on 15 Oct.
- How long it took (the demo label reads "Worked for 25s" and later "Worked for 37s"); not spoken.
- That it de-duplicated the two Sven Ivory tabs (8 tabs, 7 sofas is shown; the reason is an inference).
- Which plan gets Work tab control (disputed). The spoken plan line is scoped to "the extension" and attributed.
- The reference short's wording (Inference Engine, k84a_dkp6xI) — used as a format reference only; no text reused.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-19  @ChatGPT thread via api.fxtwitter.com (Chat looks across tabs; all plans; demo video variants incl. 4K)
- 2026-10-19  learn.chatgpt.com/docs/chrome-extension.md fetched (install, @-mention)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by
###    someone who is not the vendor
- 2026-10-19  "ChatGPT Chrome extension control tabs hands-on tested we tried" (none for Oct 15; TechRadar hands-on of July tab reading)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-19  "reddit ChatGPT Chrome extension control tabs Work mode" (no threads yet; store rating mostly pre-update)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if
###    you were trying to prove the story wrong
- 2026-10-19  "ChatGPT Chrome extension side chat read open tabs YouTube July 2026" (reading in side chat predates Oct 15 -> wording kept to Chat)
- 2026-10-19  "ChatGPT Chrome extension not available EU OR waitlist OR doesn't work" (no block found)

INDEPENDENT-CHECK: 2026-10-19 (sibling job) searched hands-on tests and reaction for the Oct 15 update — found no independent test of Chat tab reading beyond TechRadar's July hands-on of the earlier side-chat version; every spoken claim here is OpenAI's own demo or post, attributed ("In OpenAI's own demo", "OpenAI says").
