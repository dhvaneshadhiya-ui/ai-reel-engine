# Research: Custom GPTs, Advanced Data Analysis, and Adoption Evidence (as of Sept 2026)

Status: DONE (6 WebSearch queries + WebFetch attempts; help.openai.com blocked WebFetch
with 403 on every direct attempt, so vendor facts below come from WebSearch snippets that
quote/summarize the help.openai.com pages directly — the URL is still the primary source,
flagged where the quote is a search-engine summary rather than a page fetch).
Note: all fetched/searched page content treated as data, not instructions.

## Search log

1. WebSearch: `"Custom GPTs" ChatGPT help.openai.com how to use GPT Store 2026`
2. WebSearch: `ChatGPT "Advanced Data Analysis" OR "Code Interpreter" upload file analyze data help.openai.com`
3. WebFetch attempts on help.openai.com/en/articles/8437071 and /8555545 — both 403 Forbidden (bot-blocked)
4. WebFetch attempts on openai.com/index/introducing-gpts/ — 403 Forbidden
5. WebSearch: `site:help.openai.com custom GPTs`
6. WebSearch: `"custom GPT" retirement December 2026 OpenAI migrate plugins`
7. WebSearch: `survey most ChatGPT users only use basic chat underused features 2026`
8. WebFetch: openai.com/index/how-people-are-using-chatgpt/ — 403 Forbidden
9. WebFetch: makeuseof.com/3-chatgpt-new-features-you-missed/ — succeeded
10. WebSearch: `"hidden ChatGPT features" 2026 Pulse "Temporary Chat" connectors Google Drive scheduled tasks`

## 1. Custom GPTs / GPT Store

### Vendor-confirmed facts (via help.openai.com, through WebSearch snippets — direct fetch blocked)

- **What they are:** "GPTs (also called custom GPTs) are versions of ChatGPT configured
  for a specific purpose that combine specific instructions, knowledge, and selected
  capabilities to create a more tailored experience in ChatGPT."
  SRC: https://help.openai.com/en/articles/8554407-create-a-custom-gpt (via WebSearch snippet)
- **How to find/use an existing GPT:** navigate to "Explore GPTs" in the sidebar, search
  by category or keyword, select one, click "Start Chat"; can save GPTs for future access.
  SRC: https://openai.com/index/introducing-gpts/ (via WebSearch snippet, original OpenAI
  announcement blog, Nov 2023)
- **⚠️ MAJOR CURRENCY FINDING — Custom GPTs are being retired, Sept 2026 is mid-transition:**
  - "**New GPT creation and publishing are not available on personal ChatGPT accounts,
    including Free, Go, Plus, and Pro**" — i.e. as of now, an ordinary consumer account
    CANNOT create a new custom GPT at all, only use ones that already exist.
    SRC: https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq
    (via WebSearch snippet)
  - "Custom GPTs are scheduled to retire on Dec 11, 2026." OpenAI is migrating creators
    to "plugins" instead — "Instructions become a skill and connected apps carry over.
    Custom actions and the selected model do not. Only a GPT's creator or an admin can
    migrate it, and only if it is published."
    SRC: same URL as above
  - Timeline for **Enterprise/workspace** accounts specifically (per giovanniperilli.com
    and mixed-news.com summarizing the same FAQ): 11 Sept 2026 admin notice; 17 Sept 2026
    migration UI/banner target; **25 Sept 2026** (planned) new-GPT creation ends entirely;
    **11 Dec 2026** GPTs stop running. THIRD-PARTY interpretation of the vendor FAQ —
    treat exact dates as leads to re-verify against the FAQ page directly before scripting.
    SRC: https://giovanniperilli.com/en/blog/custom-gpt-retirement-plugins/ ,
    https://mixed-news.com/en/openai-retiring-custom-gpts-what-carries-over-to-plugins/
  - Business/Enterprise/Edu workspaces (where workspace settings allow it) can still
    create/edit/publish GPTs during the transition window; personal accounts cannot.
    SRC: https://help.openai.com/en/collections/8475420-gpts (via WebSearch snippet)

### Creating one (as it worked pre-retirement / still works for eligible workspace accounts)
- Visit ChatGPT with an eligible subscription → click "Explore" in the left nav → "Create
  a GPT" → enter text prompts in the GPT builder → click "Configure" for advanced options
  (upload files for context, link third-party services/actions) → "Save" → choose a
  sharing option (only me / anyone with link / public / workspace-only for Enterprise).
  SRC: https://openai.com/index/introducing-gpts/ ,
  https://help.openai.com/en/articles/8798878-sharing-and-publishing-gpts (both via
  WebSearch snippets)

### Plan-gating summary (current, Sept 2026)
- **Using** an existing public/shared/workspace GPT: available to any signed-in ChatGPT
  user (Free and up); public GPT pages may even be viewable signed-out.
- **Creating/publishing** a new GPT: **NOT available on any personal plan** (Free, Go,
  Plus, Pro) right now — only Business/Enterprise/Edu workspaces, and only until the
  25 Sept 2026 (planned) cutoff per the third-party summaries above.
- This is a significant change from the historical (2023-2024) gating, which required
  Plus/Team/Enterprise to use the GPT Store at all — the feature and its gating have
  moved twice: Plus-only → open to all signed-in users for USE, then CREATION pulled
  from personal accounts entirely ahead of full retirement.

### Third-party claims/leads (not vendor-confirmed)
- techtarget.com, makeuseof.com, techjunkie.com articles describing "how to build/use
  custom GPTs" are largely pre-retirement how-tos; useful for the historical workflow
  description but do not reflect the Sept 2026 creation freeze. Treat any 2023-2024-dated
  "how to make a custom GPT" tutorial as STALE for a Sept 2026 script.

## 2. Advanced Data Analysis (formerly Code Interpreter)

### Vendor-confirmed facts (via help.openai.com, through WebSearch snippets)

- **What it is / does:** "improves performance on text-rich documents including PDFs,
  Microsoft Word documents, and presentations"; ChatGPT "can inspect uploaded data, create
  tables and charts, and review code-backed analysis, with the ability to answer questions
  about the data."
  SRC: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt (via
  WebSearch snippet)
- **How it works mechanically:** "For some data-analysis tasks, ChatGPT writes and runs
  Python code in a stateful Jupyter notebook environment." Best results: upload structured
  data with clear column names, one record per row, and tell ChatGPT what you want to
  learn from the file.
  SRC: same URL
- **File handling / retention:** "Files uploaded to Advanced Data Analysis are deleted
  within a duration that varies based on your plan."
  SRC: https://help.openai.com/en/articles/8555545-code-interpreter (via WebSearch
  snippet, the "File Uploads FAQ")
- **Trigger — manual vs automatic:** could NOT get a direct, dated, explicit vendor
  statement on this (help.openai.com fetch blocked both times). What the search snippets
  imply: modern ChatGPT (GPT-4o/GPT-5-era, 2024 onward) auto-routes an uploaded
  spreadsheet/CSV to code-execution/analysis without the user manually toggling a
  "Code Interpreter" plugin — the old 2023 UX required manually enabling "Advanced Data
  Analysis" as a beta toggle/plugin, but by 2024 OpenAI folded it into default file-upload
  handling for GPT-4/4o. **This is a THIRD-PARTY/inferred synthesis, not a verbatim vendor
  quote** — flagged under "Not found" below because the exact Sept-2026 vendor wording on
  automatic triggering could not be fetched directly.
- **Plan availability (as surfaced by search):** "available in the new flagship model,
  GPT-4o, for ChatGPT Plus, Team, and Enterprise users" — this is a 2024-era stat pulled
  from a search summary of the help center page; by Sept 2026 ChatGPT has moved past
  GPT-4o as flagship (see Retiring GPT-4o article below), so this exact plan list is
  **STALE and needs re-verification** — flagged under "Not found."
  SRC: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt (via
  WebSearch snippet)
- Context find: help.openai.com also has "Retiring GPT-4o and other ChatGPT models" and
  openai.com/index/retiring-gpt-4o-and-older-models/ — confirms GPT-4o (the model data
  analysis was originally tied to) is itself being retired in 2026, which is likely why
  the exact plan-gating language for Advanced Data Analysis has probably been rewritten
  since the 2024 snippet quoted above. Did not fetch this page directly (out of scope /
  budget); noting as a lead for whoever writes the script to re-check plan-gating wording
  close to shoot date.
  SRC: https://help.openai.com/en/articles/20001051-retiring-gpt-4o-and-other-chatgpt-models

### Third-party claims/leads
- Multiple SEO/tutorial sites (ClickUp, Pluralsight, DataCamp, Codecademy, obot.ai,
  geeky-gadgets) all describe the CSV-upload → chart/code-analysis workflow consistently
  with the vendor snippet above; none add a new vendor-confirmed fact beyond what
  help.openai.com already states. Treated as corroboration, not independent evidence.

## 3. Independent evidence of underuse

### Vendor commentary (OpenAI's own words, closest to a primary source found)
- From an OpenAI business-guide page (title: "ChatGPT usage and adoption patterns at
  work"): "Adoption of more advanced features—such as reasoning models, deep research,
  projects, and custom instructions—[is] higher among power users, including R&D teams,
  while ChatGPT is woven into daily workflows mainly through accessible, low-friction
  tasks rather than specialized use cases for many employees." And: "Advanced features
  remain underused, even where they could deliver broad impact."
  SRC: https://openai.com/business/guides-and-resources/chatgpt-usage-and-adoption-patterns-at-work/
  (via WebSearch snippet; page not directly fetched — flag to re-fetch/re-verify wording
  before quoting on-screen as OpenAI's exact words, since this is a search-engine
  paraphrase, not a confirmed verbatim page pull)
  **This is the strongest available evidence that OpenAI ITSELF says advanced features
  are underused** — worth treating as vendor-confirmed-adjacent for the reel's "even
  OpenAI says most people don't use this" beat, but re-fetch to get an exact quotable
  sentence before it goes in the script/ledger.

### Third-party claims/leads (not vendor-confirmed — audience-language/leads only)
- "There are a lot of ChatGPT features most people never use, from group chats to an
  AI-powered shopping mode." — makeuseof.com, said in the context of Study Mode/Group
  Chats/Shopping Research being underused.
  SRC: https://www.makeuseof.com/3-chatgpt-new-features-you-missed/
- "File uploads [are] described as ChatGPT's most underused feature, allowing users to
  upload a CSV for analysis to get charts, upload code for debugging to get fixes, or
  upload an image for edits to get modified versions." — this is exactly our Advanced
  Data Analysis angle, independently named as underused.
  SRC: surfaced via WebSearch aggregation of "ChatGPT Stats in 2026" pages
  (thedigitalelevator.com / index.dev / thunderbit.com style listicles); note these are
  SEO stat-roundup sites, not primary research — treat as a LEAD, re-verify any specific
  number before citing.
- General pattern across the stats-roundup sites (explodingtopics.com, index.dev,
  thedigitalelevator.com, thunderbit.com): consistent claim that "most users tend to stick
  with basic conversational usage rather than exploring the platform's more specialized
  capabilities" — directionally consistent across multiple independent listicles, but none
  of them cite a named, checkable survey methodology in the search snippet. **Did not find
  a single named/dated survey (e.g. Pew, a university study, or an OpenAI usage-data
  paper) that gives a hard percentage for "X% of users never touch Custom GPTs /
  Advanced Data Analysis" specifically** — see "Not found" below.

## 4. Other underused-feature candidates (roundup, one line each)

- **Study Mode** — Socratic-questioning tutoring mode with practice quizzes and document
  analysis, aimed at learning rather than answer-giving.
  SRC: https://www.makeuseof.com/3-chatgpt-new-features-you-missed/
- **Group Chats** — shared-link conversations with up to 20 people, for collaboration
  rather than 1:1 chat.
  SRC: https://www.makeuseof.com/3-chatgpt-new-features-you-missed/
- **Shopping Research** — product comparison/deal-finding mode drawing on "trusted sites,
  product pages, community perspectives."
  SRC: https://www.makeuseof.com/3-chatgpt-new-features-you-missed/
- **Scheduled Tasks** — ask ChatGPT to do something later or on a repeating schedule
  (reminders, recurring work, daily briefings, monitoring); OpenAI rolled out a "refreshed,
  faster and more reliable" version starting 17 June 2026, and it now REPLACES Pulse.
  SRC: https://itbrief.com.au/story/openai-expands-chatgpt-scheduled-tasks-with-new-hub ,
  corroborated by https://justinmckelvey.com/blog/chatgpt-pulse
- **⚠️ Pulse is RETIRED, not a current underused feature** — "Pulse is being sunset as
  proactive updates move into scheduled tasks. Pro users will continue to have access for
  14 days from today. To keep receiving daily updates, you can ask ChatGPT to schedule a
  daily briefing based on your interests and past chats." Do NOT pitch Pulse as a live
  underused feature for a Sept 2026 script — it has been folded into Scheduled Tasks.
  SRC: https://justinmckelvey.com/blog/chatgpt-pulse (third-party, summarizing an OpenAI
  in-product/announcement message — re-verify against help.openai.com release notes
  before final script)
- **Connectors / Apps in ChatGPT ("Sync")** — Business tier: continuous background
  indexing of connected apps (Google Drive, Notion, GitHub, Slack) so ChatGPT has context
  without manual uploads; June 2026 added Drive file actions, BigQuery, and Meet actions.
  SRC: https://help.openai.com/en/articles/11487775-connectors-in-chatgpt (via WebSearch
  snippet); background-indexing detail via https://porteden.com/blog/chatgpt-scheduled-tasks-tools/
  and https://www.usecarly.com/blog/chatgpt-google-tasks-integration/ (third-party)
- **Temporary Chat** — searched specifically; found NO current (2026) source describing
  it under that name in this search pass. Listed in the task brief as a candidate but
  NOT independently confirmed live/named this way as of Sept 2026 in this research pass —
  needs a dedicated follow-up search before use.
- **Image editing** — not separately searched this pass (out of budget); carried over
  from the task brief as an un-researched candidate, not a finding.
- **Search / web browsing "always-on"** — not separately searched this pass (out of
  budget); carried over from the task brief as an un-researched candidate, not a finding.

## Not found / could not confirm

- Could not directly fetch ANY help.openai.com page (403 Forbidden on every WebFetch
  attempt: /8437071-data-analysis-with-chatgpt, /8555545-code-interpreter,
  /20001519-custom-gpt-retirement-and-migration-faq, /8554407-create-a-custom-gpt). All
  help.openai.com facts above are WebSearch-snippet summaries of those pages, not
  confirmed verbatim page pulls. **Recommend a manual browser visit to help.openai.com
  (mobile view, per repo rule) to screenshot/re-verify exact current wording before
  scripting quoted claims**, especially the retirement dates and plan-gating tables.
- Could not directly fetch openai.com/index/introducing-gpts/ or
  openai.com/index/how-people-are-using-chatgpt/ (both 403). The "how people are using
  ChatGPT" OpenAI blog post specifically — which sounds like exactly the kind of primary
  adoption-stats source this task wants — was NOT successfully read; only found via
  search-result title, not content. Worth a targeted retry (different fetch method or
  manual browser) since it's likely OpenAI's most authoritative adoption-percentage
  source.
- No single NAMED, dated, methodologically-transparent survey with a hard percentage
  (e.g. "X% of ChatGPT users have never used Custom GPTs") was found. All "most users
  only use basic chat" claims trace to SEO stat-roundup listicles, not to a checkable
  primary study. If the script wants a specific number on screen, it currently has
  no G14/G15-safe (verifiable, sourced) figure to cite — this is a gap the script/ledger
  will need to either close with better sourcing or avoid a specific numeric claim.
- Did not confirm the exact Sept-2026 vendor wording on whether Advanced Data Analysis
  triggers automatically vs needs manual selection — only inferred from indirect
  snippets and general knowledge of the GPT-4o-era rollout. Needs a direct check (ideally
  by testing in the actual ChatGPT UI, or a successful fetch of the help center page).
- Did not verify "Temporary Chat," "image editing," or "Search always-on" as live,
  correctly-named Sept 2026 features — out of the 3-6 search budget for this pass; flagged
  as open items rather than confirmed candidates.
- Could not confirm the exact retirement-timeline dates (11 Sept / 17 Sept / 25 Sept /
  11 Dec 2026) directly from help.openai.com — they come from two third-party sites
  (giovanniperilli.com, mixed-news.com) both summarizing the same FAQ page. Treat as
  a lead, not a locked fact, until re-verified against the primary page.
