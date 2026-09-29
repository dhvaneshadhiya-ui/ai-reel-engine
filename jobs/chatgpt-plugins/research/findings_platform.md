# Findings: ChatGPT "plugins" platform facts (researched 2026-09-29)
Research subagent; saved by the main session.

Access: help.openai.com, chatgpt.com/pricing, chatgpt.com/features/plugins return 403
(WebFetch and curl). Loaded: learn.chatgpt.com/docs/plugins, developers.openai.com/plugins.
Tiers: PRIMARY (OpenAI page fetched) / MIRROR (releasebot verbatim) / SECONDARY / SNIPPET.

## 1. What a plugin is
- PRIMARY https://learn.chatgpt.com/docs/plugins: "Plugins bundle capabilities into reusable workflows in ChatGPT and Codex. They can include skills and MCP servers." One "universal plugin directory".
- PRIMARY https://developers.openai.com/plugins: "Build and publish plugins with skills, MCP servers, and optional UI."

## 2. Leads
A. 2026-07-09 Plugin Directory replaced App Directory — SECONDARY https://www.taskade.com/blog/chatgpt-plugins: "replacing the App Directory with the Plugin Directory. Existing app connections are unaffected." (release note itself not seen verbatim; mirror starts 2026-08-31)
B. 2026-09-11 custom GPT retirement — MIRROR https://releasebot.io/updates/openai/chatgpt (VIA help.openai.com release notes): "We're planning to retire custom GPTs across ChatGPT plans and provide a migration path to plugins". SNIPPET: retire Dec 11 2026, creation ends Oct 26 2026.
C. 2026-09-23 voice — MIRROR releasebot: "Live now supports plugins on web, iOS, and Android." / "You can use the plugins and connected apps available to your account during a Voice conversation"
D. Plans — CONFLICTING. taskade: "included on the Free, Go, Plus, and Pro plans". SNIPPET: "Some plugins require a paid plan." gradually.ai: directory "visible on every plan"; install depends on plan/region. composio: "Connectors are not available on the free ChatGPT tier" (likely stale). SAFE LINE: every plan, some plugins need paid.

## 3. Release-note entries (MIRROR)
- 2026-09-10 "install Data from the plugin directory, then start a conversation with @Data"
- 2026-09-01 Healthcare Public Data plugin

## 4. Install / use
- PRIMARY learn.chatgpt.com: Plugins tab; "Search or browse for a plugin, then open its details. Select the plus button to install the plugin." Use by describing the task, or "Using `@` to invoke specific plugins". Surfaces: "ChatGPT on web, desktop, and mobile"; some "Desktop only".
- SECONDARY composio: "@ mention ... You can also select + → More and choose the app."
- NOT FOUND: exact iPhone tap path.

## 5. Region
- SECONDARY composio: "Several of these plugins do not work in the EEA, Switzerland, or the UK."

## 6. Count: NOT FOUND officially.
## 7. 2023 plugins: launched 2023-03-23, closed 2024-04-09, ~1,000 plugins (SECONDARY taskade).
## 8. Official visuals: NONE found for the directory (no launch post/video). Receipt: learn.chatgpt.com/docs/plugins (mobile capture).

## 9. Is the list honest
- igeeksblog (updated 2026-09-28) 17 picks: Gmail, Google Drive, Google Calendar, Outlook Email, Outlook Calendar, Teams, SharePoint, Slack, Notion, Canva, GitHub, Adobe Acrobat, Fireflies, Dropbox, Atlassian Rovo, Shopify, Aha!.
- composio ranks itself #1. gradually.ai top 5 by prominence: Gmail, Drive, Calendar, Outlook, Teams.
- Directory rows (SNIPPET, unverified): Popular (Gmail, Google Drive, GitHub, Outlook Email); Small Business (Dropbox, QuickBooks, HubSpot, Stripe, Canva, Figma).
- Verdict: frame as "our picks"; OpenAI publishes no ranking.

## 10. NOT found
help.openai.com first-hand; pricing page first-hand; July 9 note verbatim; announcement/video; plugin count; iPhone path; Free-plan plugin limits; official EEA statement.
