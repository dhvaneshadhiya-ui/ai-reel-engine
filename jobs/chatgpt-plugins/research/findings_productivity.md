# Findings: productivity plugins (Gmail, Google Drive, Google Calendar, Notion, Dropbox)
Researched 2026-09-29 by a research subagent; saved by the main session.

## ACCESS NOTE
403 to WebFetch 2026-09-29: help.openai.com (11487775, 10929079, 6825453),
openai.com/business/plugins/gmail/, chatgpt.com/plugins, chatgpt.com/features/plugins/.
[SNIPPET] = WebSearch summary of the page, not a fetch. learn.chatgpt.com loaded.
WebFetch returns a model summary; verify quotes in a browser before on screen.

## Plugin Directory
- "bundle capabilities into reusable workflows in ChatGPT and Codex", skills + MCP servers, "one universal plugin directory". SRC https://learn.chatgpt.com/docs/plugins
- Invocation: describe the task, or "Use the `@` symbol". SRC same. No "+ menu" mention.
- Sensitive actions need approval ("Allow once" or persistent per conversation). SRC same
- "When ChatGPT sends data through an MCP server, that service's terms and privacy policy apply." SRC same
- Featured: "Gmail: Draft and manage email replies"; "Google Drive: Work across Drive, Docs, Sheets, and Slides"; "Google Calendar: Manage events and schedules"; "Notion: Workflows for specs, research, and knowledge capture". SRC same
- "On July 9, 2026, OpenAI moved the old app directory into the Plugin Directory" [SNIPPET] chatgpt.com/plugins (403)
- Dropbox 2026-07-12 post links "Dropbox plugin" at chatgpt.com/apps/dropbox/... SRC https://blog.dropbox.com/topics/news/trusted-dropbox-content-into-openai-workflows

## Gmail
- "Draft and manage email replies". SRC https://learn.chatgpt.com/docs/plugins
- "Review your Gmail conversations to prepare replies, recap recent exchanges, gather talking points for meetings, or highlight action items." [SNIPPET] https://openai.com/business/plugins/gmail/
- SEND since 2026-06-08: "you ask, it drafts, you approve, it sends". VIA https://www.usecarly.com/blog/chatgpt-work-google-workspace-integration/ (cites OpenAI release notes)
- "Sending emails is available on the web for users on Plus, Pro, Business, and Enterprise plans with Gmail or Outlook connected." [SNIPPET] release notes. WEB ONLY.
- "ChatGPT reads automatically but asks before anything with an effect outside the chat". VIA usecarly
- igeeksblog: "find the latest message about a project, pull out a deadline, or gather recent correspondence before a call." SRC https://www.igeeksblog.com/best-chatgpt-plugins/

## Google Drive
- "Work across Drive, Docs, Sheets, and Slides". SRC learn.chatgpt.com/docs/plugins
- "search Docs, Sheets, Slides, PDFs ... compare two budget sheets, find a decision in meeting notes". SRC igeeksblog
- Write actions since ~2026-06-15 (create, update, share, move, delete). VIA usecarly, knightli

## Google Calendar
- "Manage events and schedules". SRC learn.chatgpt.com/docs/plugins
- create a Calendar invite is OpenAI's worked write-action example. VIA usecarly
- "find a free afternoon or prepare for an upcoming meeting". SRC igeeksblog

## Google plugins: setup, plans, privacy
- Setup: find plugin, Connect, Google OAuth; then @Gmail etc. [SNIPPET] help 10929079
- Plans: "generally requires a paid ChatGPT plan" [SNIPPET, third party strategenceai]. Free/Go unconfirmed.
- Not used for training even with "Improve the model for everyone" on (except feedback, pasted/uploaded data). [SNIPPET] https://help.openai.com/en/articles/10408842-google-app-for-chatgpt-data-controls-faq ; VIA knightli
- Indexed copy deleted within 30 days of disconnecting. [SNIPPET] same FAQ

## Notion
- "Workflows for specs, research, and knowledge capture". SRC learn.chatgpt.com/docs/plugins
- "read from and write to your Notion pages in real-time"; "act with your full Notion permissions". SRC https://www.notion.com/help/notion-mcp

## Dropbox
- Launched in ChatGPT 2026-04-16: preview files, save AI output to Dropbox, share links; "available globally ... on any plan" (Dropbox plans). SRC https://blog.dropbox.com/topics/news/move-your-work-forward-with-new-dropbox-apps-in-chatgpt
- 2026-07-12: organize, file requests, multi-step workflows. SRC https://blog.dropbox.com/topics/news/trusted-dropbox-content-into-openai-workflows

## Official visuals
- Dropbox April post: blog-dbx-single-file-preview-1440x960.webp (file preview inside ChatGPT, landscape). July post: OpenAI_Dropbox_960x960.png logo lockup + 2 embedded videos.
- No official Gmail/Drive/Calendar screenshots found (OpenAI page 403).

## NOT found / NOT verified
- Primary OpenAI source for Gmail send + date; Free/Go eligibility for Google plugins;
  whether write actions work on iOS (only statement: "on the web"); EEA/UK limits;
  "+ menu"; primary source for 2026-07-09; plan reqs for Notion/Dropbox;
  official Gmail/Drive/Calendar visuals; Notion's own ChatGPT launch post.

## Subagent's view
Gmail first ("what's waiting for me / draft a reply"), then Google Calendar. Do not
promise one-tap send from the iPhone app — sending appears web-only.
