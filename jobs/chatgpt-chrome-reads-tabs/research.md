# Research — chatgpt-chrome-reads-tabs

Claims ledger + search log. Sources reused from the same-day sibling job jobs/chatgpt-chrome-tabs/research/.

## CLAIMS

- CLAIM: On 15 Oct 2026 OpenAI announced it is "bringing the power of computer use to anyone who uses Chrome".
  TIER: official
  SPOKEN: "On October 15th, OpenAI said it's bringing the power of computer use to anyone who uses Chrome"
  SURPRISE: 60
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI's own announcement thread, post 1 (fetched via api.fxtwitter.com 2026-10-19)
  SRC: https://www.ibtimes.com.au/openai-chatgpt-chrome-extension-computer-use-1876917
  VIA: OpenAI thread

- CLAIM: ChatGPT can now use your Chrome tabs: in Chat it looks across your open tabs and gathers info.
  TIER: official
  SPOKEN: "In Chat, it looks across every one, like the sofas you're shopping for"
  SURPRISE: 55
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI thread post 1 ("If you're in Chat, it can look across your open tabs and gather info"); demo video 1 shows eight sofa tabs
  SRC: https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/
  VIA: OpenAI X thread

- CLAIM: In Work, ChatGPT can control Chrome tabs: send messages, fill out forms, download files, and organize/group tabs.
  TIER: official
  SPOKEN: "it can send messages, fill out forms, download files, and even group the pile you have open"
  SURPRISE: 70
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI thread post 1 ("sending messages, filling out forms, or downloading files"; "organize and group that pile of tabs you have open")
  SRC: https://ppc.land/chatgpt-gains-control-of-chrome-tabs-to-fill-forms-and-send-messages/
  VIA: OpenAI X thread

- CLAIM: ChatGPT inside a Chrome tab (side panel) got the full ChatGPT: your entire ChatGPT history, Chat or Work side by side while you're on a site.
  TIER: official
  SPOKEN: "the ChatGPT side panel in Chrome got the full app: your entire chat history, with Chat or Work right beside the site you're on"
  SURPRISE: 55
  SRC: https://x.com/ChatGPT/status/2110823740309401654
  VIA: OpenAI thread post 2 ("the full power of ChatGPT is now in your browser. Your entire ChatGPT history is right there ... side by side while you're on a site")
  SRC: https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/
  VIA: OpenAI X thread + demo video 2

- CLAIM: Since 30 Jul 2026 the side panel (side chat) could already reference your open tabs; acting in tabs and the full app in the panel are new on 15 Oct.
  TIER: official
  SPOKEN: "Since July, that side panel could read your tabs"
  SURPRISE: 65
  SRC: https://x.com/ChatGPT/status/2082970812584432115
  VIA: OpenAI's own 30 Jul 2026 post (side chat can "reference your open tabs")
  SRC: https://digitaltrends.com/computing/chatgpts-chrome-extension-can-now-read-your-tabs-youtube-videos-and-highlighted-text
  VIA: OpenAI July update (search snippet; page fetch returned empty — corroborated by TechRadar's July hands-on)

- CLAIM: By default ChatGPT asks before it interacts with each new website.
  TIER: official
  SPOKEN: "By default, it checks with you before it acts on a new website"
  SURPRISE: 65
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation ("By default, ChatGPT asks before it interacts with each new website.")
  SRC: https://www.beri.net/article/chatgpt-chrome-extension-work-mode-computer-use-logged-in-tabs-enterprise-admin-controls-allowlist-no-action-log
  VIA: OpenAI docs; independent analysis that approval is per site

- CLAIM: Setup: add the ChatGPT extension to Chrome and @-mention Chrome.
  TIER: official
  SPOKEN: "add the ChatGPT extension to Chrome and mention @Chrome"
  SURPRISE: 45
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation
  SRC: https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg
  VIA: Chrome Web Store listing

- CLAIM: OpenAI says it is available on all ChatGPT plans.
  TIER: official
  SPOKEN: "OpenAI says it's available on every ChatGPT plan"
  SURPRISE: 50
  SRC: https://x.com/ChatGPT/status/2110825327811580209
  VIA: OpenAI's own post ("Available for all ChatGPT plans")
  SRC: https://the-decoder.com/chatgpt-becomes-a-full-chrome-browser-assistant-that-reads-and-acts-on-your-open-tabs/
  VIA: OpenAI X thread

## FEATURES + HOW TO USE

- Chat: look across open tabs and gather info — USED (the whole reel)
- Work: control tabs (messages, forms, downloads, grouping) — USED (the second half of the switch)
- Side panel gets the full ChatGPT (history, Chat/Work side by side) — USED (thread post 2)
- Side chat reading tabs, highlighted text, YouTube transcripts — USED only as 'since July' context; transcripts CUT
- Per-website permission prompts — USED for acting ("before it acts on a new website"); not claimed for reading
- Works in Edge, Brave, Opera, Vivaldi — CUT: title is Chrome
How to use: add the extension from the Chrome Web Store — USED; @-mention Chrome — USED; desktop app Settings > Computer Use — CUT (the demo itself runs at chatgpt.com in Chrome)

## NOT CLAIMED

- That reading tabs in the side panel is new (spoken as 'Since July'): side chat could reference open tabs from 30 Jul 2026. The script says "can now ... reading across your open Chrome tabs" from Chat, which is what OpenAI announced on 15 Oct.
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
