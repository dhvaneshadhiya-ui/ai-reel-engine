# Findings — coverage, reaction, contradictions (agent B, 2026-10-19; saved by parent)
Quotes near-verbatim via WebFetch extractor.

## Primary: https://learn.chatgpt.com/docs/chrome-extension.md
- Per-site approval: "Allow once", "Allow for this site", "Allow for all sites", "Decline"; all-sites => "no longer asks for confirmation before using websites."
- History: asks every time, no always-allow.
- "Treat page content as untrusted context, and review the website before allowing ChatGPT to continue."
- Activity stored "only when it becomes part of the ChatGPT context" (no full action log).
- Install permission: "Read and change all your data on all websites."
- Chrome, Edge, Brave, Opera, Vivaldi: browser control. "Opera doesn't support side chat."
- "Browser availability can depend on rollout and your workspace settings." No plans named.

## Own analysis (no hands-on)
- PPC Land 2026-10-16 https://ppc.land/chatgpt-gains-control-of-chrome-tabs-to-fill-forms-and-send-messages/ VIA OpenAI X thread, 9to5Google, store. Unclear whether free users get tab control (Work launched Pro/Enterprise/Edu first). No built-in confirmation before sending stated; "stop before submitting" is a user instruction.
- beri.net 2026-10-18 https://www.beri.net/article/chatgpt-chrome-extension-work-mode-computer-use-logged-in-tabs-enterprise-admin-controls-allowlist-no-action-log VIA OpenAI docs. Site-level approval, not action-level; no full action log.
- Let's Data Science https://letsdatascience.com/news/chatgpt-extension-adds-tab-context-and-side-chat-9caaa1ff — store: 7M users, 2.4/5 (915), v1.26.1005.11759 updated Oct 15. (Agent A read 1.9/5 from 985 — conflicting; ratings NOT used.)

## Repeat coverage
- 9to5Google 2026-10-16 https://9to5google.com/2026/10/16/chatgpt-gets-deeper-google-chrome-integration-including-control-over-tabs/ VIA X thread + two demo videos. "similar to how you can use Chrome's built-in Gemini integration."
- The Decoder 2026-10-16 https://the-decoder.com/chatgpt-becomes-a-full-chrome-browser-assistant-that-reads-and-acts-on-your-open-tabs/ VIA X thread: "works with all ChatGPT plans."
- PiunikaWeb 2026-10-16 https://piunikaweb.com/2026/10/16/chatgpt-chrome-extension-tab-control-automation/ : Work "requires at minimum a Plus subscription"; quotes OpenAI "in the background, without ever taking over your active browsing session."
- tbreak https://tbreak.com/chatgpt-chrome-extension-open-tabs/ : advises closing banking/health/admin tabs.
- Chrome Geek https://www.chromegeek.com/chatgpt-chrome-extension-tabs-work-mode/ : Settings > Computer Use; @-mention in Work or Codex chat.
- IBTimes AU https://www.ibtimes.com.au/openai-chatgpt-chrome-extension-computer-use-1876917 : Atlas timeline; works in signed-in Gmail/LinkedIn/Salesforce.
- Unite.AI (AI-written byline, low weight): Atlas deprecation announced 2026-07-09, stopped 2026-08-09.

## Contradictions
1. Plans: "all plans" (OpenAI thread) vs "min Plus" (PiunikaWeb) vs unclear (PPC Land). Guide names none. => speak hedged / do not name plans for Work.
2. Approval per site; all-sites removes prompts.
3. Replaces Atlas.
4. No OpenAI prompt-injection numbers; competitor figures second-hand (not used).
5. No regional block / waitlist found.

## Searches 2026-10-19
1 "ChatGPT Chrome extension Work mode control tabs October 2026" — cluster, doc, plan conflict
2 "...hands-on tested we tried" — no independent test
3 "9to5google ChatGPT Chrome extension tabs sidebar" — 9to5G, LDS
4 "The Verge ... Atlas tabs computer use" — Atlas context
5 "reddit ... control tabs Work mode" — no Reddit threads; beri.net
6 "... prompt injection security risk logged-in sessions" — security critique
7 "OpenAI release notes ... plans" — help.openai.com 403
8 "... not available EU OR waitlist OR doesn't work" — none

## NOT found
Independent hands-on test; user reactions; OpenAI plan list for Work; regional exclusion; OpenAI injection rate.
