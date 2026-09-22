# Research: ChatGPT Voice Mode + Tasks (as of Sept 2026)

Sources fetched via browser (help.openai.com blocks plain WebFetch with 403 - used
Claude_Browser tool to render and extract text from the live page instead).

## VOICE MODE

SRC: https://help.openai.com/en/articles/8400625-voice-mode (renders as "ChatGPT Voice | OpenAI Help Center")
Page says "Updated: 9 days ago" (checked 2026-09-21, so page last updated ~2026-09-12).

### What it is (current naming, Sept 2026)
- Official current name in the help center is just "ChatGPT Voice", not "Advanced
  Voice Mode" -- "Advanced" is now one of THREE selectable sub-modes.
- Quote: "ChatGPT Voice lets you speak with ChatGPT and hear a spoken response. Voice
  works within a chat, so you can listen while following the response in text, type
  when you cannot speak, and review earlier messages without starting over."
- Three Voice options under Settings -> Voice:
  1. Live -- quote: "Live is powered by GPT-Live-1 or GPT-Live-1 mini, depending on
     your plan. Live is designed for natural back-and-forth conversation and can use
     web search and memory, show visual results through supported widgets, and work
     with text and images in the same chat. Live does not initially support video,
     screen sharing, connected apps, or plugins." Live can listen and speak
     simultaneously (real interruption support).
  2. Advanced -- quote: "The previous real-time Voice experience. Use Advanced when
     you need supported mobile capabilities such as video or screen sharing." (i.e.
     "Advanced Voice Mode" from 2024 is now the legacy/secondary option, kept alive
     specifically for video/screen-share.)
  3. Standard -- quote: "A turn-by-turn Voice experience that transcribes your
     speech before generating a response."
- "The options available to you may depend on your plan, workspace settings, region,
  app version, and parental controls."
- To switch: "open Settings -> Voice and select Live, Advanced, or Standard."

### Exact steps to start a Voice conversation (verbatim from help center)
On iOS and Android:
1. Select the Voice icon in the message bar.
2. If prompted, allow the ChatGPT app to access your microphone.
3. If this is your first Voice conversation, choose a preferred voice.
4. After Voice opens, begin speaking to start the conversation.
5. During the conversation, select the microphone control to mute/unmute; select the
   exit control to end.

On web:
1. Go to ChatGPT.com.
2. Select the Voice icon in the prompt window.
3. If prompted, allow your browser to access your microphone.
4. After Voice opens, begin speaking to start the conversation.
5. Same mute/exit controls as above.

Desktop app (macOS/Windows) -- business context: "Voice in Desktop: Use voice to
start tasks, check progress, ask questions about your agents, and coordinate multiple
agents through one conversation. Available in the ChatGPT desktop app on macOS and
Windows, with paired remote access." (This is a separate "Voice in Desktop" product for
Business/Enterprise/Edu/Healthcare workspaces, distinct from the consumer web/mobile
Voice icon.)

### Platforms confirmed live (Sept 2026)
- iOS app, Android app, web (ChatGPT.com), and ChatGPT desktop app (macOS/Windows,
  workspace context) via "Voice in Desktop."
- Apple CarPlay: "ChatGPT is available in Apple CarPlay on supported iPhones. You can
  start a Voice conversation, continue a recent or pinned chat, or start a conversation
  in a project from your CarPlay screen."
- Background conversation support: "turn on Background conversations under Settings ->
  Voice" -- lets Voice keep running while using other apps / phone locked.
- "Start with Voice" setting: "On supported mobile app versions, turn on Start with
  Voice under Settings -> Voice. When this setting is on, opening ChatGPT to a new or
  empty conversation starts Voice automatically."

### Plans/tiers and limits (Voice in Chat, usage measured over rolling 24h for Live)
| Plan | Usage |
|---|---|
| Free | "Limited access to GPT-Live-1 mini. Limits may change." |
| Go | 3 hours with GPT-Live-1 mini |
| Plus | 3 hours with GPT-Live-1 |
| Pro ($100/month) | 15 hours with GPT-Live-1 |
| Pro ($200/month) | Unlimited GPT-Live-1 |
| Business Standard | 3 hours GPT-Live-1; extra = 1.25 credits/min |
| Business Premium | 15 hours GPT-Live-1; extra = 1.25 credits/min |
| K-12 Teachers | 3 hours GPT-Live-1 |
| Enterprise/Edu/Clinicians (credit pricing) | 1.25 credits per minute |
| Enterprise (usage-based USD) | $0.05 per minute |
| Legacy Enterprise/Edu | 3 hours GPT-Live-1 |

NOTE: this help page shows a "Pro ($100/month)" and "Pro ($200/month)" split -- worth
double-checking against pricing page if used on screen (may be two different Pro-tier
offers by Sept 2026, not the single $200 Pro plan widely known from the Dec 2024
launch).

- "You can have one Voice conversation at a time."
- Video/screen sharing: ONLY available via "Advanced" mode, iOS/Android, for eligible
  subscribers -- NOT supported in Live. Quote: "Live does not support video or screen
  sharing." / "Video and screen sharing remain available to eligible subscribers in the
  ChatGPT iOS and Android apps when using Advanced."
- Captions: Live shows response text live in chat; Advanced has a dedicated "cc" button
  on iOS/Android during a Voice conversation.

### Voice options (named voices) -- Settings -> Voice -> Voice
Arbor, Breeze, Cove, Ember, Juniper, Maple, Sol, Spruce, Vale (+ in Brazil: Viola, Rio).

### Data / retention
- Audio (Live/Advanced) and video (Advanced) clips stored with transcript, retained 30
  days; deleted within 30 days of deleting the chat (barring legal holds).
- Standard mode: audio deleted immediately after transcription (unless user opted to
  share for training).
- Training opt-in: Free/Plus/Pro personal workspaces can toggle "Improve the model for
  everyone" + "Include your audio/video recordings" in Settings -> Data Controls. NOT
  available to share in Business/Enterprise/Edu workspaces.

## STILL TO DO
- [ ] Search for recent 2025-2026 changes/launches to Voice (Live mode rollout date)
- [ ] Fetch help.openai.com Tasks page directly (browser) for verbatim quotes + limits
- [ ] Search for recent 2025-2026 changes/launches to Tasks
- [ ] Find official screenshots (openai.com blog posts, help center images)
- [ ] Confirm plan tiers for Tasks specifically (Free included? limits per plan)

---

## TASKS (Scheduled Tasks in ChatGPT)

SRC: https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt
("Scheduled tasks in ChatGPT | OpenAI Help Center", page says "Updated: 24 days ago"
-- checked 2026-09-21, so last updated ~2026-08-28.)

### What it is
Quote: "ChatGPT can run one-time or recurring tasks, monitor for changes, and respond
to supported events when available. Use Scheduled to create, review, manage, and share
eligible tasks."

Three task types implied by the doc: (1) one-time tasks, (2) recurring tasks, (3)
event-triggered / webhook-based tasks (Gmail/Slack/GitHub, run in "Work").

### Exact steps to create a task (verbatim)
Standard task:
1. Go to "Scheduled" (a dedicated page/section) to create a task and set its schedule.
2. To create a task, ask ChatGPT to complete an action, such as "Let me know when my
   package is delivered." (i.e. created conversationally inside a normal chat -- ChatGPT
   recognizes the time/recurrence phrasing and turns it into a task.)
   - Caveat: "If you create a task in a project, it cannot access uploaded files or
     files stored in that project."
3. After a task is created, ChatGPT displays a confirmation card (exact wording not
   captured as text, shown as a UI card).
4. To manage notifications: "go to Settings > Notifications and select Push, Email, or
   both."

Event-triggered task (Gmail/Slack/GitHub), separate flow, lives in "Work":
1. Go to Settings > Apps and connect a supported Gmail, Slack, or GitHub account.
2. Open "Work" and describe the event and the action ChatGPT should take.
3. Review Trigger, Condition, and Prompt, and complete any required authorization.
4. Go to Scheduled to review, edit, pause, or delete the task.
- "Gmail tasks can respond to a new message or filter by sender or subject. Slack tasks
  can respond to new channel messages. Add @ChatGPT to each monitored Slack channel.
  GitHub tasks can respond to supported pull request activity in an authorized
  github.com repository."
- Enterprise/Edu/Healthcare admins must enable "Allow event-triggered scheduled tasks"
  org-wide first.
- Healthcare workspaces: event-triggered tasks OFF by default, NOT covered under BAA;
  do not use for PHI.

### Where it lives / how to view and manage (verbatim)
- "Go to Scheduled to view and manage tasks."
- From Settings: "Go to Settings > Notifications. Select Manage tasks to open
  Scheduled."
- From a conversation: "select the more options menu (...), then select See scheduled
  tasks."
- To edit: "Select the task title in its conversation. Use the task panel to edit,
  pause, manage, or delete the task." Also: "Open a task in Scheduled to review or edit
  its schedule."

### Platforms
- Web (ChatGPT.com) and "supported ChatGPT mobile app[s]" (push notifications require
  creating the task in a supported mobile app).
- Desktop app: quote -- "Availability depends on the app, app version, and account. If
  Scheduled does not appear in the ChatGPT desktop app, use ChatGPT on the web. You can
  create, share, and update event-triggered tasks on the web or in supported mobile
  apps. The desktop app can display existing event-triggered tasks, but it does not
  support creating or editing their trigger conditions." So: Scheduled/Tasks page may
  not always be present in the desktop app; web + mobile are the reliable places to
  create tasks.
- "Codex uses separate automations" -- Codex (coding agent) has its own distinct
  scheduling system, not the same as ChatGPT Tasks.

### Plans/tiers and limits (verbatim / near-verbatim)
- "Scheduled tasks and scheduled task sharing are available to eligible ChatGPT Free,
  Go, Plus, Pro, Business, Enterprise, and Edu users, and users in eligible ChatGPT for
  Healthcare workspaces, subject to account and workspace settings." -- i.e. Tasks
  (standard/recurring) ARE available on the FREE plan.
- Event-triggered (webhook) tasks: "available to eligible users on Plus, Pro, Business,
  Enterprise, and Edu plans, and in ChatGPT for Healthcare workspaces. Free and Go
  accounts cannot create event-triggered tasks, and event-triggered tasks are not
  available in FedRAMP workspaces."

**Active task limits (concurrent tasks), quote:**
"Active task limits depend on the plan: 3 for Free and Go, 5 for Plus, 10 for Business
and Edu, and 15 for Pro and Enterprise. Limits for other eligible plans depend on the
account or workspace."

**Scheduling frequency limits, quote:**
"Free users can schedule a one-time task or a recurring task no more than once per day.
Free tasks use flexible scheduling windows, such as morning, afternoon, or night.
Hourly schedules and exact delivery times require an eligible paid plan."
- FAQ restates: "Free users can schedule a one-time task or a recurring task no more
  than once per day. Eligible paid plans support recurring tasks up to once per hour and
  exact delivery times."
- Event-triggered tasks: "can run up to 30 times per hour and 720 times per day across
  all of your event-triggered tasks. Multiple events may be grouped together. Inactive
  tasks may pause automatically."

### What Tasks does NOT support
Quote: "Scheduled tasks do not support: Voice chats / GPTs" -- i.e. you cannot create a
scheduled task inside a Voice conversation, and Tasks cannot invoke a custom GPT.

### Sharing a task (feature detail)
- Any eligible active/paused task (including event-triggered) can be shared via a link:
  Scheduled -> task's ••• menu -> Share -> Copy link.
- Shared link snapshot includes: task title, instructions, schedule, original time
  zone, and optionally the selected ChatGPT mode/model. Does NOT include: creator's
  name, chat history, previous results, saved memories, custom instructions, attached
  files, connected app data/credentials.
- Business/Enterprise/Edu/Healthcare task links are workspace-scoped (only members of
  that workspace can open them); personal-account links are open to anyone with the
  link.
- Recipient schedules their own separate copy of the task using their own account/
  permissions -- it does not run on the sharer's account/credentials.

### Compliance
- "Scheduled tasks are included in the Compliance API. Shared task links and the saved
  snapshots they contain are not currently included."

### Integrations named
- Gmail, Slack, GitHub (event-triggered / connected apps).
- ChatGPT Health and ChatGPT Finances: "Scheduled tasks can use information from
  ChatGPT Health or ChatGPT Finances when those features are available for the
  account. For example, a task can provide a portfolio update after the market closes
  or summarize recent spending. ChatGPT Health and ChatGPT Finances are not supported
  sources for event-triggered tasks." Notably: connecting a financial account to
  ChatGPT Finances auto-creates a "Weekly finances update" task by default (can be
  paused/deleted from Scheduled).

### FAQ highlights (good sound-bite material for a reel)
- "How often can tasks run, and is there a limit?" -- answered above (once/day free,
  hourly+exact-time on paid, event triggers up to 30/hr & 720/day).
- "What is the difference between scheduled tasks and Codex automations?" -- "Scheduled
  tasks run in ChatGPT and can handle reminders, recurring work, daily updates, and
  monitoring. Codex automations run in Codex."
- "Why did my task pause?" -- "A task may pause if it is inactive, requires additional
  action, or its associated chat is deleted."
- "What are monitoring tasks?" -- "Monitoring tasks check for changes and send a
  notification when a relevant update occurs. They can use information from previous
  runs and stop when a defined end condition is met."

## RECENT CHANGES / LAUNCHES (2025-2026)

### Voice: "Live" replaced/absorbed "Advanced Voice Mode" -- July 8, 2026
SRC (secondary, via WebSearch synthesis of multiple outlets -- treat as VIA, not yet
independently verified against openai.com primary post text, which is in progress):
- WebSearch summary: "On July 8, 2026, OpenAI replaced ChatGPT's Advanced Voice Mode
  with GPT-Live -- a fully rebuilt voice system that can listen and speak at the same
  time." New models: GPT-Live-1 and GPT-Live-1 mini, described as "full-duplex" (process
  incoming speech and generate outgoing speech concurrently, rather than waiting for the
  user to finish talking).
- "Free users get GPT-Live-1 mini automatically; paid users (Go, Plus, Pro) get the
  full GPT-Live-1." (consistent with the Usage limits table pulled directly from the
  official help center above)
- Candidate primary source: https://openai.com/index/introducing-gpt-live/ (OpenAI
  blog post "Introducing GPT-Live") -- fetching directly now for verbatim quotes/date/
  images; WebFetch tool returns 403 on openai.com, using browser tool instead.
- Also reported: GPT-Live-1 released in the OpenAI API on/around September 10, 2026
  (secondary source, TechCrunch-adjacent coverage) -- NOT YET VERIFIED against an OpenAI
  primary source.
- Result: "Advanced" mode (the old 2024-era Advanced Voice Mode) still exists in the
  live product as of Sept 2026, but demoted to a secondary option kept specifically for
  video/screen-share on iOS/Android, per the help center text captured above.

### Memory ("Dreaming") -- tangential, not Voice/Tasks, but same OpenAI blog family
Found while trying to load the GPT-Live post (browser initially routed to this article
instead -- OpenAI's blog navigation is client-side/JS and the fetch landed on a
different in-progress/cached article). NOT part of this brief's scope (Voice/Tasks) --
noting only to explain the detour. SRC: https://openai.com/index/dreaming-better-memory-for-a-more-helpful-chatgpt/
dated June 4, 2026. Not used in findings below.

## STILL TO DO
- [ ] Verify "Introducing GPT-Live" post directly (openai.com) -- date, verbatim quotes,
      screenshot/image URLs, plan tiers as OpenAI itself states them
- [ ] Search for recent 2025-2026 Tasks-specific launch/change history (e.g. Tasks
      launched Jan 2025; find event-triggered tasks launch date, ChatGPT Finances/Health
      task integration launch date)
- [ ] Find + list official screenshot/image URLs for both features (help center article
      images use client-rendered <img> not always captured by get_page_text -- may need
      read_page or screenshot)
- [ ] Confirm Team plan explicitly (help center table doesn't list "Team" by name --
      only Free/Go/Plus/Pro/Business/Enterprise/Edu/Healthcare/K-12 -- note this
      discrepancy: "Team" plan may be branded as "Business" now, needs confirmation)

---

## VERIFIED PRIMARY SOURCE: "Introducing GPT-Live" (OpenAI blog)

SRC: https://openai.com/index/introducing-gpt-live/ -- dated **July 8, 2026**, category
"Product / Release". (Confirmed directly via browser render; WebFetch tool 403s on
openai.com so this was pulled with the Claude_Browser tool.) Contains an inline update
dated July 31, 2026 (see below).

### What changed, in OpenAI's own words
- Quote: "We're launching GPT-Live, a new generation of voice models that make talking
  with AI feel much more like having a real conversation."
- Quote: "GPT-Live is built on a full-duplex architecture, meaning it can listen and
  speak at the same time. During conversations, GPT-Live can show it's paying attention
  with phrases like 'mhmm' or 'yeah', engage in quick back-and-forth, or just stay quiet
  when you need a moment to think."
- Quote: "GPT-Live is also our smartest voice model yet. For questions that require web
  search, deeper reasoning, or more complex work, it delegates to our latest frontier
  model behind the scenes and brings the result back into the conversation when it's
  ready... At launch, GPT-Live will use GPT-5.5 in the background."
- Quote: "We're beginning to roll out two versions of GPT-Live -- GPT-Live-1 and
  GPT-Live-1 mini -- to ChatGPT users globally today [July 8, 2026]."

### History of ChatGPT Voice architecture, per OpenAI (good for a reel's "how we got
here" beat)
1. **Cascaded voice systems** (original ChatGPT Voice / "Standard"): "chained three
   models together: a speech-to-text model to transcribe your speech, a large language
   model to produce a response, and a text-to-speech model to convert it back into
   speech... information could be lost across models, and responses were slow and
   stilted."
2. **Turn-based voice models** (ChatGPT Advanced Voice Mode, launched 2024): "processed
   and generated audio within a single model, reducing latency... but they still
   operated through discrete turns. The model had to wait for the user to stop speaking
   before responding, resulting in rigid back-and-forth... even a brief pause or
   background noise could be mistaken for the end of turn -- causing the model to
   interrupt at unnatural times."
3. **GPT-Live (full-duplex, July 2026):** "continuously processes input while
   generating output. The model can therefore make interaction decisions many times per
   second: whether to speak, continue listening, pause, interrupt, or invoke a tool."
   Also supports "live translation."

### Scale claim
Quote: "Each week, more than 150 million people talk to ChatGPT using features like
Voice and Dictation."

### New Voice capabilities described (July 2026)
- "More natural conversations" -- acknowledges with "mhmm"/"got it" while listening;
  "We've also remastered the nine distinct voices in ChatGPT for GPT-Live." (matches
  the 9 named voices captured from the help center: Arbor, Breeze, Cove, Ember,
  Juniper, Maple, Sol, Spruce, Vale)
- "Smarter answers" -- "You can also choose the level of reasoning that fits your
  needs: Instant for fast responses, or Medium and High when you want ChatGPT to spend
  more time thinking." (reasoning-effort selector for Voice)
- "Better listening" -- waits during pauses instead of interrupting; can be told to
  "stay quiet and listen"; improved background-noise focus.
- "Visual answers at a glance" -- quote: "While you're talking, ChatGPT can now show
  rich visual cards for topics like weather, stocks, sports, and more. Voice also
  continues to support search, memory, images, and file uploads." (matches "supported
  widgets" language from the help center page)

### Availability & limitations (verbatim, OpenAI's own section header)
Quote: "GPT-Live is rolling out now to ChatGPT users globally across iOS, Android, and
ChatGPT.com. GPT-Live-1 will become the default model powering ChatGPT Voice for Go,
Plus, and Pro users, and GPT-Live-1 mini will become the default for Free users."
Quote: "At launch, GPT-Live will not support voice with video or screen sharing in
ChatGPT, but we're working to introduce these capabilities soon. You can still access
legacy versions of ChatGPT Voice, including Standard and Advanced Voice Mode, where
these features are available." -- this directly explains why the help center still
lists "Advanced" as a selectable option: it's the fallback specifically for video/
screen-share, exactly as captured earlier from help.openai.com.
- Language: "optimized GPT-Live for some of the most popular languages... For certain
  languages, the model may have a non-native accent or gaps in fluency."

### Safety / watermarking update -- July 31, 2026 (inline update on the same post)
Quote: "Update July 31, 2026: Supported audio generated with GPT-Live through ChatGPT
Voice and the OpenAI API now includes SynthID watermarking. Our public verification
tool can now detect OpenAI provenance signals in supported audio files, and we've
introduced API access for verification so developers and organizations can incorporate
provenance checks into their own workflows."
- Also: "GPT-Live is designed for conversation, not voice impersonation. It uses a set
  of predefined voices in ChatGPT, with safeguards to prevent it from imitating a real
  person's voice."
- Teen/parental: "Parents can choose whether their teen can use ChatGPT Voice through
  Parental Controls, and linked parents may be notified in higher-risk situations
  involving signs of potential self-harm or suicidal intent."

### Benchmarks cited (OpenAI's own claims, use with TIER/caveat language, not as bare
fact)
- GPQA (expert scientific reasoning): "GPT-Live-1 substantially outperforms Advanced
  Voice Mode."
- BrowseComp (agentic web search): "GPT-Live-1 shows strong gains over Advanced Voice
  Mode."
- "tau^3-Voice Telecom" (internal eval, multi-turn telecom support): "GPT-Live-1
  outperforms Advanced Voice Mode."
- Footnote: "GPT-Live-1 (instant) and GPT-Live-1 mini use the GPT-5.5 Instant model in
  the background, while GPT-Live-1 Medium and GPT-Live-1 High use the GPT-5.5 Thinking
  model with medium and high reasoning effort."

### Images/visuals on the page
The page is heavily video/audio-embedded (multiple "00:00" audio/video player widgets
for example conversations: Standard Voice Mode, Advanced Voice Mode, GPT-Live-1
"Continuous interaction" demo, GPT-Live-1 "Delegation for deeper work" demo) rather than
static screenshots. get_page_text does not return image/video src URLs -- if static
screenshots are needed for the reel, recommend either (a) screen-capturing the diagrams
directly from https://openai.com/index/introducing-gpt-live/ per tools/capture.mjs
(mobile-first per CLAUDE.md), or (b) using the in-app Voice icon UI itself (mobile
capture) rather than this blog post's abstract diagrams. NOT YET fetched as raw image
URLs -- would need read_page/DOM inspection or view-source if exact <img>/<video> src
attributes are required for sourcing.

## STILL TO DO
- [ ] Tasks-specific launch history (original Jan 2025 Tasks launch; event-triggered
      tasks launch date) -- not yet searched
- [ ] Official screenshot URLs (img src) for Voice icon UI and Scheduled/Tasks UI --
      not yet captured at the asset-URL level
- [ ] Confirm "Team" plan naming/mapping (still open -- see note above)

---

## TASKS -- LAUNCH HISTORY (secondary sources, cross-checked)

- Tasks launched in beta **January 15, 2025** (secondary sources, high agreement across
  outlets -- Shelly Palmer, TestingCatalog, arturmarkus.com; no single one is clearly
  "the" original OpenAI post, all appear to be press coverage of the same OpenAI
  announcement, so treat these as VIA: OpenAI's Jan 2025 announcement, not independently
  primary-sourced in this session):
  - "OpenAI rolled out ChatGPT Tasks in beta to all Plus, Team, and Pro subscribers
    globally on January 15, 2025." Powered by GPT-4o at launch, via a "4o with
    scheduled tasks" model-picker option.
  - Beta limit at launch: throttled to **10 tasks per user**; "no integrations and no
    actions" (i.e. the January 2025 beta predates today's Gmail/Slack/GitHub
    event-triggered tasks and today's per-plan limits of 3/5/10/15 documented above).
  - NOT verified against an OpenAI primary post directly in this session (help.openai.com
    "ChatGPT -- Release Notes" page was found in search results but not fetched — would
    need a follow-up fetch to pin exact OpenAI-authored launch wording/date if the reel
    needs it word-for-word).

## "Team" plan -- resolved
Secondary-source confirmation (cloudzero.com / general pricing roundups, not an OpenAI
primary page): "OpenAI renamed the old Team plan to ChatGPT Business in 2025 as a
naming change only... feature parity between the renamed plan and the old Team plan
staying the same at launch." This explains why the current (Sept 2026) OpenAI help
center pages for both Voice and Tasks list "Business Standard" / "Business Premium" /
"Business" rather than "Team" -- "Team" is the deprecated/legacy name for what is now
called Business. Current ChatGPT Team plan pricing cited by aggregators: ~$30/user/
month monthly, ~$25/user/month billed annually (secondary source, not confirmed on an
OpenAI pricing page in this session).

## SUMMARY TABLE -- what plan gets what (Sept 2026, per help.openai.com primary pages)

| Plan | Voice (Live) | Voice limit | Tasks | Active task limit | Task frequency | Event-triggered tasks |
|---|---|---|---|---|---|---|
| Free | GPT-Live-1 mini | "Limited access... Limits may change" | Yes | 3 | 1x/day, flexible windows only | No |
| Go | GPT-Live-1 mini | 3 hrs/24h | Yes | 3 | 1x/day (free-tier-like) per general FAQ wording -- NOTE: Go's task frequency isn't separately broken out from Free in the FAQ text captured; both are grouped under "Free users" language in one place, but Go get its own row in the active-task-limit table matching Free (3) | No |
| Plus | GPT-Live-1 | 3 hrs/24h | Yes | 5 | up to hourly + exact times | Yes |
| Pro ($100/mo) | GPT-Live-1 | 15 hrs/24h | Yes | 15 | up to hourly + exact times | Yes |
| Pro ($200/mo) | GPT-Live-1 | Unlimited | Yes | 15 | up to hourly + exact times | Yes |
| Business Standard | GPT-Live-1 | 3 hrs/24h + 1.25 credits/min extra | Yes | 10 | up to hourly + exact times | Yes (admin must enable) |
| Business Premium | GPT-Live-1 | 15 hrs/24h + 1.25 credits/min extra | Yes | 10 | up to hourly + exact times | Yes (admin must enable) |
| Enterprise | 1.25 credits/min or $0.05/min | -- | Yes | 15 | up to hourly + exact times | Yes (admin must enable) |
| Edu | 3 hrs/24h (legacy) or per-plan | -- | Yes | 10 | up to hourly + exact times | Yes (admin must enable) |
| Healthcare | per workspace | -- | Yes (Weekly finances/health-aware tasks) | per workspace | -- | Off by default, not under BAA |

CAVEAT: the Go-plan task-frequency detail above is an inference, not a directly quoted
line -- the Help Center FAQ literally says "Free users can schedule a one-time task or a
recurring task no more than once per day" without repeating "and Go" in that specific
sentence, even though the active-task-limit table explicitly groups "Free and Go" at 3.
Flag this as needing a second look/re-fetch if precision on Go's task frequency matters
for an on-screen claim.

## WHAT WAS LOOKED FOR AND NOT FOUND / NOT FULLY VERIFIED
- Exact <img>/<video> src URLs for official screenshots (both help center pages render
  mostly text + UI confirmation cards + a few "opens in a new window" outbound links;
  the GPT-Live blog post is built around embedded audio/video demo players, not static
  screenshots -- no clean static screenshot URL was captured for either feature in this
  session).
- An OpenAI-primary (not press-coverage) source for the exact Jan 15, 2025 Tasks launch
  date and wording -- only secondary/press sources were used for that date.
- OpenAI's own current pricing page for exact Team/Business dollar pricing (used a
  secondary aggregator instead).
- Any Sept-2026-dated Tasks-specific product update (the only recent Tasks-adjacent
  change found was the auto-created "Weekly finances update" task tied to ChatGPT
  Finances, which is undated in the help center text -- not confirmed as a 2026 change
  vs. older).
- Precise task-frequency limit for the Go plan specifically (see caveat above).

## RECOMMENDATION FOR THE REEL (not a claim, just a production note)
For on-screen "how to start it" steps, capture MOBILE screenshots directly from the
live iOS/Android ChatGPT app per CLAUDE.md's mobile-first capture rule (tools/
capture.mjs) rather than relying on the OpenAI blog's abstract audio/video demo
widgets, which are desktop-only and not phone-native UI. The help center steps above
(Voice icon in message bar; Scheduled page in sidebar / conversation ••• menu) are the
exact on-screen actions to demonstrate.
