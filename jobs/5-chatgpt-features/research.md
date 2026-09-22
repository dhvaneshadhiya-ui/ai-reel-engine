# Research — 5-chatgpt-features

Claims ledger + search log. Product/list reel (5 ChatGPT features), format `ai-tools`.

## CLAIMS

- CLAIM: Each week, more than 150 million people talk to ChatGPT using Voice or Dictation.
  TIER: official
  SPOKEN: "In September 2026, over one hundred fifty million people talk to ChatGPT out loud every week."
  SRC: https://openai.com/index/introducing-gpt-live/
  VIA: OpenAI's own "Introducing GPT-Live" blog post, July 8, 2026 ("Each week, more than 150 million people talk to ChatGPT using features like Voice and Dictation.")
  SURPRISE: 78

- CLAIM: On July 8, 2026 OpenAI replaced the old turn-based Advanced Voice Mode with GPT-Live, a full-duplex model that can listen and speak at the same time instead of waiting for the user to finish talking.
  TIER: official
  SPOKEN: "Voice got rebuilt this July into full duplex: listening and talking at once."
  SRC: https://openai.com/index/introducing-gpt-live/
  VIA: OpenAI's own blog ("GPT-Live is built on a full-duplex architecture, meaning it can listen and speak at the same time" / prior models "had to wait for the user to stop speaking before responding, resulting in rigid back-and-forth")
  SURPRISE: 62

- CLAIM: ChatGPT Tasks lets a user schedule a one-time or recurring action; Free and Go accounts get 3 active tasks at once (5 on Plus, 10 on Business/Edu, 15 on Pro/Enterprise), and only Plus and above can create event-triggered tasks that watch a connected Gmail, Slack, or GitHub account.
  TIER: official
  SPOKEN: "Tasks are hands-off too: run one-time or recurring, up to three active on free accounts. Paid plans get hourly scheduling and can watch things like Gmail for you."
  SRC: https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt
  VIA: OpenAI Help Center, "Scheduled tasks in ChatGPT" (updated ~2026-08-28) — "Active task limits depend on the plan: 3 for Free and Go, 5 for Plus..."; "event-triggered tasks... available to eligible users on Plus, Pro, Business, Enterprise, and Edu plans... Free and Go accounts cannot create event-triggered tasks."; "Free users can schedule a one-time task or a recurring task no more than once per day... Eligible paid plans support recurring tasks up to once per hour and exact delivery times."
  SURPRISE: 81

- CLAIM: ChatGPT's Memory (rebuilt on a "dreaming" architecture in June 2026) automatically synthesizes and updates what it remembers about a user across conversations, not only when explicitly asked to remember something, and OpenAI extended this rebuilt version to Free-tier accounts for the first time in June 2026.
  TIER: official
  SPOKEN: "Memory doesn't wait to be asked. It remembers you across every chat, and this June OpenAI opened it to free accounts as well."
  SRC: https://openai.com/index/chatgpt-memory-dreaming/
  VIA: OpenAI's own blog, "Dreaming: Better memory for a more helpful ChatGPT," June 4, 2026 — "dreaming leverages a background process that allows ChatGPT to learn from many conversations and synthesize ChatGPT's memory state... without relying on explicit requests to remember something"; "we are only now able to offer Free users a version that meets our quality bar... making it possible to begin rolling out dreaming to Free users"
  SURPRISE: 70

- CLAIM: ChatGPT's data-analysis feature triggers automatically on file upload (no manual tool selection) — it writes and runs Python in a stateful notebook environment to answer questions, build tables, and chart uploaded spreadsheets/CSVs/PDFs — and Free-tier accounts get it in limited form, capped at 3 file uploads a day.
  TIER: official
  SPOKEN: "Data analysis works automatically: drop in a spreadsheet, get code, a chart, and answers. Free gets three uploads a day."
  SRC: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt
  SRC: https://help.openai.com/articles/8555545
  SRC: https://openai.com/chatgpt/pricing/
  VIA: OpenAI Help Center, "Data analysis with ChatGPT" (updated ~2026-07) — "ChatGPT can analyze uploaded files, answer questions about the data, and create tables or charts... For some data-analysis tasks, ChatGPT writes and runs Python code in a stateful Jupyter notebook environment"; File Uploads FAQ (updated ~2026-09-11) — "Free users are limited to 3 file uploads per day"; live chatgpt.com pricing comparison table, row "Data analysis": Free = Limited, all paid tiers = Yes.
  SURPRISE: 66

- CLAIM: ChatGPT Projects groups related chats, files, and project-specific instructions into one space; collaboration limits scale by plan — Free gets up to 5 files and 5 collaborators, Plus/Go up to 25 files and 10 collaborators.
  TIER: official
  SPOKEN: "And Projects pulls it together, chats, files, and instructions in one space, so ChatGPT stops starting from zero. Free gets five files, Plus twenty-five."
  SRC: https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt
  VIA: OpenAI Help Center, "Using projects in ChatGPT" (updated ~2026-09-20) — "Projects keep related chats, files, and instructions together so ChatGPT can use the same context"; "Free users: up to 5 files and 5 collaborators" / "Plus and Go users: up to 25 files and 10 collaborators."
  SURPRISE: 55

## FEATURES + HOW TO USE

Every ChatGPT feature examined this pass, marked USED or CUT with why. How-to steps for
each is the vendor's own, captured in research/findings_*.md.

- Voice (Live) — USED. Full-duplex real-time conversation. How to use: tap the Voice icon
  in the message bar (iOS/Android/web) → allow microphone → begin speaking. Switch mode at
  Settings > Voice > Live/Advanced/Standard.
- Tasks (Scheduled tasks) — USED. One-time/recurring/event-triggered automated actions.
  How to use: ask ChatGPT conversationally ("remind me when...") or open the Scheduled
  page from the sidebar / Settings > Notifications > Manage tasks.
- Memory — USED. Persistent, auto-synthesized personalization across chats. How to use:
  Settings > Personalization > Memory; toggle Reference saved memories / Reference chat
  history; review at the memory summary page.
- Data analysis (formerly Advanced Data Analysis / Code Interpreter) — USED. Automatic
  file-upload analysis, charts, and code execution. How to use: upload a spreadsheet/CSV/
  PDF directly in a chat and ask a question; no separate mode to enable.
- Projects — USED. Grouped chats/files/instructions with project-specific rules. How to
  use: "New project" in the sidebar → name it → add files/instructions via Project
  settings (•••) → move or start chats inside it.
- Custom Instructions — CUT. Real, live, all-plan feature (Settings > Personalization >
  Custom Instructions, 1,500 chars free / 5,000 paid) and a strong candidate, but cut for
  visual variety: it is a settings-box feature like Memory, and the reel already opens
  with two personalization-adjacent items (Voice, Memory). Keeping it would make 2 of 5
  items read as "another settings toggle" back to back with Memory. Noted here so a
  future reel (or a 6th slide) can use it — the research is complete and sourced.
- Personality ("Base style and tone") — CUT. Real, live (Settings > Personalization,
  updated ~Aug 29 2026), but it changes tone only, not capability — thinner payoff than
  the other five, and risks being confused with Custom Instructions in a fast list.
- Canvas — CUT, and NOT because it is unused: it no longer exists under that name.
  OpenAI's own release notes (help.openai.com/en/articles/6825453, entry dated May 28,
  2026): "canvas will no longer be available in GPT-5.5 Instant or GPT-5.5 Thinking.
  Writing and coding functionality is now supported directly in chat responses through
  writing blocks and code blocks." Demonstrating "Canvas" as current UI in a Sept 2026
  reel would be factually wrong. Its successor (writing blocks/code blocks, auto-
  triggered inline) was considered as a 6th/replacement item but cut for scope — the
  reel already has a code-adjacent item (data analysis) and adding a second would
  crowd the runtime.
- Custom GPTs / GPT Store — CUT. Mid-retirement as of Sept 2026: OpenAI's own FAQ
  (help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq) states
  new GPT creation and publishing are "not available on personal ChatGPT accounts,
  including Free, Go, Plus, and Pro" — only pre-existing GPTs can still be used, and the
  whole feature is "scheduled to retire on Dec 11, 2026" in favor of "plugins." Pitching
  viewers to go build a custom GPT would be stale advice within months of publishing.
- Pulse — CUT (does not exist as a separate feature anymore). It was sunset and folded
  into Scheduled Tasks; the current, correctly-named feature is Tasks, which is USED.

## NOT CLAIMED

- That Custom Instructions, Canvas, Custom GPTs, or Pulse are current picks — see CUT
  reasons above. Canvas and Custom GPTs are explicitly retired/retiring; naming them as
  live, usable features would be inaccurate for a September 2026 reel.
- Any exact EU/EEA-specific Memory availability or defaults — found only in third-party
  reporting (TechTimes), no primary OpenAI page located confirming current EU state. Not
  spoken or shown.
- A specific numeric cap on saved memories (e.g. "~200 memories") — no official figure
  exists; third-party estimates only. Not spoken or shown.
- That Plus/Pro memory capacity was literally "doubled" in the June 2026 update — that
  word appeared only in a secondary AI-generated search summary, not in OpenAI's own
  blog text. Not spoken.
- That Advanced Data Analysis / data analysis triggers manually — OpenAI's own page
  confirms it is automatic on upload; no manual toggle is described or claimed.
- Any comparison of the 150-million-a-week Voice/Dictation figure against ChatGPT's total
  user base, or any claim that Voice usage is a "small percentage" of users — no sourced
  total-weekly-user figure was researched this pass, so no fraction/percentage is stated.
  The hook states the raw number and invites the viewer to recognize whether they are
  part of it — a rhetorical address, not a statistical claim.
- Go plan's exact task-scheduling frequency (whether it matches Free's once-a-day cap
  precisely) — the Help Center groups Free+Go at the same active-task-limit (3) but the
  frequency-limit sentence names only "Free users." Not spoken as a Go-specific claim.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-21 Four parallel research passes fetched OpenAI Help Center and openai.com
  primary pages (via Claude Browser, since WebFetch returns 403 on both domains) for:
  Memory + Custom Instructions + Personality; Projects + Canvas; Voice + Tasks; Custom
  GPTs + Data Analysis + adoption evidence. Full source lists and verbatim quotes in
  jobs/5-chatgpt-features/research/findings_*.md.
- 2026-09-21 Follow-up pass specifically verifying Data Analysis's current name, trigger
  mechanics, and plan gating (findings_data_analysis_verify.md) — resolved a stale
  2024-era "GPT-4o only" gating claim found in the first pass.

### 2. WHO ELSE TRIED IT — hands-on or testing by someone who is not the vendor
- 2026-09-21 "hidden ChatGPT features 2026" / "underrated ChatGPT features" —
  makeuseof.com coverage of Study Mode, Group Chats, Shopping Research (not used in this
  script; noted as candidates for a future reel). No independent hands-on test of Voice/
  Tasks/Memory/Data-analysis/Projects specifically that added a fact beyond the vendor
  pages — these five are all "what the vendor's own settings do," which is inherently a
  vendor-documented, not third-party-tested, kind of claim (see INDEPENDENT-CHECK below).

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-21 "survey most ChatGPT users only use basic chat underused features 2026" —
  found consistent directional claims across SEO stat-roundup sites (explodingtopics.com,
  index.dev, thedigitalelevator.com) that most users stick to basic chat, but no named,
  dated, methodologically-transparent survey with a checkable percentage. NOT used as a
  claim — see NOT CLAIMED. The one vendor-adjacent statement worth noting (not used as a
  spoken claim, found via search snippet only, not independently re-fetched this pass):
  an OpenAI business-guide page states "Advanced features remain underused, even where
  they could deliver broad impact" — directionally consistent with this reel's premise
  but not used as an on-screen quote since the page itself was not directly re-verified.

### 4. WHAT WOULD CONTRADICT THIS — the search that would prove the story wrong
- 2026-09-21 "custom GPT retirement December 2026 OpenAI migrate plugins" — this search,
  aimed at Custom GPTs, is what surfaced the retirement finding and is why Custom GPTs
  was cut rather than used: the search that would have made the reel wrong (pitching a
  dying feature) is exactly what removed it.
- 2026-09-21 Checked whether any of the five USED features had a similar rug-pull in
  progress (renamed, retired, or plan-gating changed out from under the claim) — Voice
  (confirmed current via July 8 2026 primary announcement + Sept 12 2026-updated help
  page), Tasks (confirmed current via Aug 28 2026-updated help page), Memory (confirmed
  current via June 4 2026 primary announcement), Data analysis (confirmed current via a
  dedicated follow-up pass after an initial stale GPT-4o-era gating claim was flagged),
  Projects (confirmed current via a help page updated the day before this research).

INDEPENDENT-CHECK: 2026-09-21 searched for hands-on/independent testing of these five
specific ChatGPT settings and could not find any — these are product-mechanics claims
("what does this menu item do, who can access it") that only the vendor's own
documentation can authoritatively answer; there is no independent lab that re-tests a
settings menu. What WAS checked independently is the "is this still current / not
retired" question (see WHAT WOULD CONTRADICT THIS above), which is the failure mode that
actually matters for a features list. The one genuinely third-party angle — evidence that
these features are underused — surfaced only SEO-listicle-grade sourcing with no
checkable methodology, so it was not used as a spoken claim.
