# Research — chatgpt-chrome-tabs

Claims ledger + search log. Research plan and raw findings in research/.

## CLAIMS

- CLAIM: In Work, ChatGPT can act inside the user's Chrome tabs (click, type, submit forms), on sites where the user is signed in.
  TIER: official
  SPOKEN: "ChatGPT will now click, type and hit submit in your Chrome tabs, signed in as you"
  SURPRISE: 70
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation ("ChatGPT can read or act on sites where you're already signed in")
  SRC: https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/
  VIA: OpenAI @ChatGPT X thread, 15 Oct 2026

- CLAIM: OpenAI shipped the update on 15 October 2026 via the ChatGPT Chrome extension (store version 1.26.1005.11759, updated Oct 15).
  TIER: official
  SPOKEN: "OpenAI shipped this on October 15th, in a Chrome extension"
  SURPRISE: 60
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI's own announcement
  SRC: https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg
  VIA: Chrome Web Store listing (updated date, captured on mobile 2026-10-19)

- CLAIM: The ChatGPT extension has 7,000,000 users on the Chrome Web Store.
  TIER: official
  SPOKEN: "a Chrome extension with 7 million users"
  SURPRISE: 65
  SRC: https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg
  VIA: Chrome Web Store listing, captured 2026-10-19 (shows "7,000,000 users")

- CLAIM: In Chat, ChatGPT can look across your open tabs and gather info.
  TIER: official
  SPOKEN: "In a normal chat, ChatGPT reads across your open tabs"
  SURPRISE: 40
  SRC: https://x.com/ChatGPT/status/2110823738531037651
  VIA: OpenAI's own announcement
  SRC: https://the-decoder.com/chatgpt-becomes-a-full-chrome-browser-assistant-that-reads-and-acts-on-your-open-tabs/
  VIA: OpenAI X thread

- CLAIM: In Work, ChatGPT can control Chrome tabs to send messages, fill out forms, download files, and organize/group tabs.
  TIER: official
  SPOKEN: "But in Work, its agent mode, it takes them over: sending messages, filling out forms, downloading files, even grouping your pile of tabs"
  SURPRISE: 70
  SRC: https://ppc.land/chatgpt-gains-control-of-chrome-tabs-to-fill-forms-and-send-messages/
  VIA: OpenAI @ChatGPT X thread ("sending messages, filling out forms, or downloading files"; "organize and group that pile of tabs")
  SRC: https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/
  VIA: OpenAI @ChatGPT X thread

- CLAIM: OpenAI's own demo shows ChatGPT finding a yoga receipt in email, opening Navan Expense in its own tab group, asking whether it is a wellness-benefit expense, filling the form and submitting it ("Expense submitted").
  TIER: official
  SPOKEN: "It finds the receipt, opens the expense site in its own tab group, asks one question, then fills in the form and submits it"
  SURPRISE: 75
  SRC: https://x.com/ChatGPT/status/2110823740309401654
  VIA: OpenAI's own demo video, frames read 2026-10-19 (prompt "submit my hothouse yoga receipt from my email please"; 0:34 question; 0:42 "Expense submitted")

- CLAIM: It can read or act on sites the user is already signed into, such as LinkedIn, Salesforce, Gmail.
  TIER: official
  SPOKEN: "that works on sites you're already signed into, like Gmail, LinkedIn and Salesforce"
  SURPRISE: 60
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation
  SRC: https://www.ibtimes.com.au/openai-chatgpt-chrome-extension-computer-use-1876917
  VIA: OpenAI docs

- CLAIM: Setup: ChatGPT desktop app > Settings > Computer Use > select browser > Install extension; then @-mention the browser in a Work (or Codex) chat.
  TIER: official
  SPOKEN: "open Settings, then Computer Use, and install the Chrome extension. Then type @Chrome in a Work chat"
  SURPRISE: 55
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation
  SRC: https://www.chromegeek.com/chatgpt-chrome-extension-tabs-work-mode/
  VIA: OpenAI docs

- CLAIM: By default ChatGPT asks before interacting with each new website; options Allow once / Allow for this site / Allow for all sites / Decline. "Allow for all sites" carries an Elevated Risk badge and ChatGPT then "no longer asks for confirmation before using websites".
  TIER: official
  SPOKEN: "By default, ChatGPT asks before it touches each new website"
  SURPRISE: 80
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation (captured on mobile, sections "Control website access" and "Allow for all sites")
  SRC: https://www.beri.net/article/chatgpt-chrome-extension-work-mode-computer-use-logged-in-tabs-enterprise-admin-controls-allowlist-no-action-log
  VIA: OpenAI docs; independent analysis that approval is site-level, not action-level

- CLAIM: Allow for all sites is marked Elevated Risk and removes the confirmation prompt.
  TIER: official
  SPOKEN: "OpenAI marks that last one as a risk, because then it stops asking"
  SURPRISE: 85
  SRC: https://learn.chatgpt.com/docs/chrome-extension
  VIA: OpenAI's own documentation

- CLAIM: While ChatGPT controls the browser, Chrome shows a '"ChatGPT" started debugging this browser' bar with a Cancel button; the user can stop the task or take over at any time.
  TIER: official
  SPOKEN: "Chrome shows a bar with a cancel button, so you can stop it any time"
  SURPRISE: 50
  SRC: https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg
  VIA: OpenAI's store screenshot 2 ("Work with your websites in Chrome")
  SRC: https://learn.chatgpt.com/docs/computer-use
  VIA: OpenAI docs ("You can stop the task or take over your computer at any time.")

## FEATURES + HOW TO USE

Vendor-documented features (learn.chatgpt.com/docs/chrome-extension, @ChatGPT thread 2026-10-15):
- Work: control Chrome tabs — send messages, fill out forms, download files — USED (the news)
- Work: organize and group open tabs — USED ("grouping your pile of tabs")
- Chat: look across open tabs to gather info — USED (one line, the contrast with Work)
- Acts on signed-in sites (Gmail, LinkedIn, Salesforce, internal tools) — USED (the stakes)
- Per-website permission: Allow once / this site / all sites / Decline — USED (the payoff)
- Allow for all sites = Elevated Risk, stops asking — USED (the payoff)
- Chrome "started debugging" bar with Cancel; stop or take over any time — USED (the safety close)
- Side chat panel (Cmd+Shift+.) — CUT: shipped July 30, not this update's news
- Right-click "Ask ChatGPT", highlighted text, YouTube transcripts — CUT: July features
- @-mention a specific tab for context — CUT: covered by "type @Chrome"; momentum
- Allowlist / blocklist under Settings > Computer Use > Manage — CUT: detail past the payoff
- Browser history access, asked every time, no always-allow — CUT: second Elevated Risk item would split the payoff
- Works in Edge, Brave, Opera, Vivaldi too (Opera no side chat) — CUT: title is Chrome; caption line
- Codex chats can drive the browser too — CUT: developer audience, not ours
- Plans: "Available for all ChatGPT plans" (extension) — CUT from voice: Work access on Free is disputed; caption, hedged

How to use (vendor steps):
1. ChatGPT desktop app > Settings > Computer Use; pick the browser — USED
2. Install beside the browser opens the store page; add the extension; review permissions — USED ("install the Chrome extension")
3. Confirm the browser shows Manage — CUT (momentum)
4. Start a Work or Codex chat and @-mention the browser — USED ("type @Chrome in a Work chat")

## NOT CLAIMED

- That tab READING is new on Oct 15: side chat could already reference open tabs from 2026-07-30 (x.com/ChatGPT/status/2082970812584432115; Digital Trends; TechRadar). The script calls out reading only as the Chat behaviour, and the news as control.
- Which plans get Work tab control. OpenAI: "Available for all ChatGPT plans" (extension); PiunikaWeb: Work needs at least Plus; PPC Land: unclear. Disputed -> not spoken; caption line only, hedged.
- Store rating (fetches read 1.9/5 and 2.4/5; most ratings predate the update). Not spoken; visible on the mobile store capture as the page shows it, not highlighted.
- Any prompt-injection success rate (OpenAI published none; competitor figures are second-hand).
- That it always asks before sending/submitting. It does not; approval is per website. "Stop before submitting" in OpenAI's examples is a user instruction.
- Atlas shutdown dates (Unite.AI AI-written, unconfirmed at primary) — context only, not spoken.
- The demo's sites (Navan, Gmail) are OpenAI's demo setup, not a claim that ChatGPT integrates with Navan.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-19  "ChatGPT Chrome tabs extension bring your Chrome tabs OpenAI October 2026"  (Oct 15 update; Chat reads tabs, Work controls tabs)
- 2026-10-19  learn.chatgpt.com/docs/chrome-extension.md + computer-use.md fetched  (setup, permissions, Elevated Risk, stop/take over)
- 2026-10-19  api.fxtwitter conversation 2110823738531037651  (@ChatGPT thread wording, two demo videos, "all ChatGPT plans")
- 2026-10-19  "OpenAI release notes ChatGPT Chrome extension plans"  (help.openai.com 403; no plan list)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by
###    someone who is not the vendor
- 2026-10-19  "ChatGPT Chrome extension control tabs hands-on tested we tried"  (no independent hands-on test of tab CONTROL found)
- 2026-10-19  "ChatGPT Chrome extension side chat read open tabs YouTube July 2026"  (TechRadar hands-on of July tab-reading; confirms reading predates Oct 15)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-19  "reddit ChatGPT Chrome extension control tabs Work mode"  (no Reddit threads yet; beri.net, Chrome Geek analysis)
- 2026-10-19  Chrome Web Store listing captured  (7M users; low rating mostly predating update)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if
###    you were trying to prove the story wrong
- 2026-10-19  "ChatGPT Chrome extension prompt injection security risk logged-in sessions"  (site-level approval only, no full action log; OpenAI: treat page content as untrusted)
- 2026-10-19  "ChatGPT Chrome extension not available EU OR waitlist OR doesn't work"  (no regional block or waitlist found)
- 2026-10-19  plan conflict search  (all plans vs min Plus — disputed, not spoken)

INDEPENDENT-CHECK: 2026-10-19 searched hands-on tests, Reddit/X reaction and security criticism of the Oct 15 tab-control update — found no independent hands-on test of tab control (every outlet rebuilds from OpenAI's thread/docs/demos); found independent analysis (PPC Land, beri.net) agreeing approval is per-site and that free-plan Work access is unclear. Every spoken claim is therefore OpenAI's own documentation or demo, attributed as such ("OpenAI's own demo", "OpenAI marks").
