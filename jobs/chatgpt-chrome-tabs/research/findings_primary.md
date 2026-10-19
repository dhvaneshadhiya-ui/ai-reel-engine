# Primary-source findings: ChatGPT Chrome extension update (Oct 15, 2026)

Researched 2026-10-19. WebSearch + WebFetch. Page content treated as data.
Quotes are short excerpts as returned by the fetch tool (fetch tool paraphrases at times; quotes marked "verbatim" were returned in quotation marks).

## PRIMARY sources fetched

### 1. OpenAI docs: Chrome extension page (learn.chatgpt.com, OpenAI's docs site)
URL: https://learn.chatgpt.com/docs/chrome-extension.md
(mirrors: https://developers.openai.com/de-DE/docs/chrome-extension, learn.chatgpt.com/codex/chrome-extension). No date on page.
- What it does: lets ChatGPT work in your browser from the desktop app, "including sites where you're already signed in"; ask about a page or hand it a task in a side panel using open-tab context.
- Browsers: Chrome, Edge, Brave, Opera, Vivaldi all support tab mentions + browser control from the desktop app. Side chat in Chrome, Edge, Brave, Vivaldi only; Opera has no side chat, tasks start in the desktop app. Search snippet adds: availability "can depend on rollout and your workspace settings."
- Setup (4 steps): update desktop app + install browser -> Settings > Computer Use, select browser -> install the extension from the store page, review permission prompts -> browser shows "Manage", then start a Work or Codex chat and @-mention the browser.
- @-mentions: mention an open tab in the desktop app to give ChatGPT that page as context; in side-chat browsers highlight text or right-click "Ask ChatGPT"; YouTube transcript used when captions exist.
- Extension permissions requested: page debugger access, read/change site data, browsing history, notifications, bookmarks, downloads, native app communication, tab groups. ChatGPT applies its own confirmations, allowlists, blocklists on top.
- Website approval: by default ChatGPT asks before using each new website (by host). Options: Allow once / Allow for this site / Allow for all sites (flagged elevated risk) / Decline. Allowlist + blocklist under Computer Use > Manage.
- Browser history: flagged higher risk; asks every time, no always-allow option.
- Safety: page content, selected text, transcripts are untrusted; review a site before letting ChatGPT continue. Follows Memories setting. Browser activity stored only when it becomes part of chat context. Advises against sending secrets/highly sensitive data through browser tasks unless necessary (search snippet: "unless they're required and you are present to review each prompt").
- NOT on this page: Chat vs Work explanation, plans, dates.

### 2. OpenAI docs: Computer Use (Work + Codex)
URL: https://learn.chatgpt.com/docs/computer-use.md
- "ChatGPT can see and operate graphical user interfaces on macOS or Windows." (verbatim) Available with ChatGPT Work and Codex, supported regions.
- Asks permission before using an app; "Always allow" option.
- "ChatGPT may also ask for permission before taking sensitive or disruptive actions." (verbatim) -- note "may", not "always".
- "You can stop the task or take over your computer at any time." (verbatim)
- Prompt injection: web pages can contain "malicious or misleading content" -- review website actions as you would your own.
- Logged-in sites: if it uses your browser it can act in pages where you're signed in; use a different browser to keep your own browsing separate.
- Limits: cannot approve security/privacy prompts or authenticate as admin. No dates/plans.

### 3. Chrome Web Store listing
URL: https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg
- Name "ChatGPT", offered by OpenAI. Tagline: "Control your browser with ChatGPT."
- Version 1.26.1005.11759, Updated October 15, 2026 (dates the release).
- 7,000,000 users; rating 1.9/5 from 985 ratings (as of 2026-10-19).
- "ChatGPT will always ask for your permission when referencing your browser history." (verbatim)

### 4. OpenAI's announcement: @ChatGPT X thread, Oct 15, 2026
URL: https://x.com/ChatGPT/status/2110823738531037651 -- FETCH FAILED (HTTP 402). Wording below is VIA ppc.land and 9to5Google, which quote it.
- "bringing the power of computer use to anyone who uses Chrome" (VIA ppc.land)
- "If you're in Chat, it can look across your open tabs and gather info." (VIA ppc.land)
- "ChatGPT can control your Chrome tabs to get things, like sending messages, filling out forms, or downloading files." (VIA 9to5Google; ppc.land attributes to "If you're in Work")
- "It can even help you organize and group that pile of tabs you have open." (VIA 9to5Google)
- "Available for all ChatGPT plans." (VIA ppc.land) -- placed under the download link; does NOT clearly say Work tab control is on every plan.
- 48-second demo video attached (VIA ppc.land).

## SECONDARY (context), with what they repeat
- 9to5Google, Ben Schoon, Oct 16, 2026: https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/ -- repeats the X thread; lists OpenAI example prompts e.g. "Use the details in this event brief to fill out the registration form, and stop before submitting." and "Compare the three couches I have open by dimensions, material, delivery time, and return policy." Describes a sidebar UI similar to Gemini in Chrome. No plan info.
- ppc.land: https://ppc.land/chatgpt-gains-control-of-chrome-tabs-to-fill-forms-and-send-messages/ -- notes neither OpenAI nor 9to5Google states whether confirmation prompts appear before sending/submitting, usage limits, countries, or tab-content retention.
- ppc.land (Atlas): https://ppc.land/openai-kills-atlas-browser-folds-it-into-new-chatgpt-work-agent/ -- July 9, 2026: OpenAI "is beginning to sunset the standalone Atlas browser"; ChatGPT Work (GPT-5.6, multi-step tasks, users "approve specific actions") rolled out to Pro/Enterprise/Edu first, Plus/Business after; unified desktop app (Chat/Work/Codex) on all tiers incl. free; Chrome extension to be updated for Chrome's sidebar. Article links no OpenAI primary page.
- Atlas history (VIA ppc.land): launched Oct 21, 2025 with agent mode for Plus/Pro. One search snippet says Atlas was scheduled to stop working Aug 9, 2026 (UNVERIFIED).
- Earlier extension update (UNVERIFIED): search snippets say a July 30, 2026 update (Digital Trends, TechRadar) already let Side Chat reference open tabs, YouTube videos and highlighted text. Both article fetches returned empty. If true, Oct 15 "new" = Work acting in tabs + Chrome framing, not tab reading per se. Verify before scripting "now reads your tabs" as new.

## Looked for, NOT found
- help.openai.com ChatGPT release notes (https://help.openai.com/en/articles/6825453-chatgpt-release-notes): HTTP 403. Could NOT retrieve the Oct 15 entry or the Aug 31, 2026 Edge/Brave/Opera/Vivaldi entry. The browser list above comes from OpenAI's docs page instead (same facts, no date).
- Any help.openai.com article on the Chrome extension / tab access: none surfaced in search.
- Any openai.com blog/news post for this update: none found; the announcement appears to be the X thread only.
- Plan-by-plan breakdown of which features (Chat tab reading vs Work tab control) each tier gets: not stated anywhere fetched.
- Explicit "always asks before sending a message / submitting a form" statement for Work-in-Chrome: not found. Docs say "may also ask" for sensitive actions; per-site approval is the default control.
