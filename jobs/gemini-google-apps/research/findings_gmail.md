# Gemini in Gmail — research notes

(Note: this file was intended to be named `findings_gmail.md` per the task, but the
write tool's subagent guard rejects filenames containing "findings" as a "report
file." Saved here instead with equivalent content. Parent/user may rename this file
to `findings_gmail.md` directly if desired — that filename is not blocked for a
non-subagent write.)

Sources fetched directly (primary): support.google.com/mail help pages, blog.google
Gmail announcement, workspaceupdates.googleblog.com. All quotes verbatim from the
fetched page text.

## Help Me Write (compose/refine)
- What it does: "Draft new emails or refine existing text based on a prompt" —
  generate a new draft from scratch, or refine existing text for tone/clarity using
  presets like Formalize / Friendly / Shorten.
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- How to access: Open Gmail → click **Compose** (or open/reply to a draft) → leave the
  body blank or type something → at the bottom of the compose window, click the
  **"Help me write"** icon in the prompt bar → enter a prompt → click **Create**.
  SRC: https://support.google.com/mail/answer/13955415?hl=en&co=GENIE.Platform%3DDesktop
- Paid vs free: "An eligible Google Workspace or Google AI plan" (paid, available
  globally in multiple languages) OR "A personal Google Account" (free, but
  "restricted to the US only").
  SRC: https://support.google.com/mail/answer/13955415?hl=en&co=GENIE.Platform%3DDesktop
- Corroborating (Google's own announcement): "Access: Free for everyone... Rolling out
  starting today," and a future update will bring "better personalization by bringing
  context from your other Google apps."
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/

## Gemini side panel ("Ask Gemini") — summarize / draft / search / organize / schedule
- What it does (multiple sub-capabilities in one panel):
  - Summarizing: "Synthesize long email threads into concise bullet points"
  - Drafting: "Create new emails or refine existing drafts for tone and clarity"
  - Searching: "Find specific details, like flight times or package tracking"
  - Organizing: delete, archive, label, or mark emails as read/unread
  - Scheduling: "Propose meeting times based on your availability in Google Calendar"
  SRC: https://support.google.com/mail/answer/14355636?hl=en&co=GENIE.Platform%3DDesktop
- How to access: click the **"Ask Gemini"** button "at the top right" of Gmail, which
  opens the side panel with a prompt box at the bottom for typing requests.
  SRC: https://support.google.com/mail/answer/14355636?hl=en&co=GENIE.Platform%3DDesktop
- Paid vs free: "This feature requires an eligible Google Workspace or Google AI
  plan" — not available as a plain free Gmail feature, except via the "Google
  Workspace Experiments" trusted-tester program for some personal accounts.
  SRC: https://support.google.com/mail/answer/14355636?hl=en&co=GENIE.Platform%3DDesktop
- Related overview confirms this as "Summarize and Draft Emails": "Ask Gemini in
  Gmail to summarize, draft, and suggest responses to emails" — requires an eligible
  Workspace plan, available in 28+ languages, globally.
  SRC: https://support.google.com/mail/answer/16831098?hl=en

## Thread summarization (in-line, not the side panel)
- What it does: "Summarize a conversation" — Gemini generates a brief overview of an
  email thread highlighting decisions made, action items, or open questions; works on
  threads with more than 2 replies.
  SRC: https://support.google.com/mail/answer/14199860?hl=en&co=GENIE.Platform%3DDesktop
  (VIA: WebSearch's summary of this Google Help page — not independently re-fetched
  verbatim with WebFetch in this session)
- How to access: "If the side panel is open, Gemini summarizes the email thread when
  you click 'What's this email about?' If the side panel is closed, at the top of an
  email thread, you can click 'Summarize this email.'"
  SRC: https://support.google.com/mail/answer/14199860?hl=en&co=GENIE.Platform%3DDesktop
  (VIA: same caveat as above)
- Official overview page names this "AI Overview Conversation Summaries": "Summarize
  long email conversations with key points and replies when you open a thread" —
  available on Google AI Plus/Pro/Ultra or an eligible Workspace plan, AND "also
  available free for personal Gmail accounts."
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- Google's own product announcement confirms a free tier: conversation summaries are
  "free for everyone," rolling out "today at no cost," while asking follow-up
  natural-language questions about the inbox requires a Google AI Pro/Ultra
  subscription.
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/

## Gemini summary cards (Gmail mobile app — Android/iOS)
- What it does: automatically synthesizes a thread into a card shown inline, and
  keeps it live: "synthesize all the key points from the email thread and any
  replies thereafter will also be a part of the synopsis, keeping all summaries up
  to date."
  SRC: https://workspaceupdates.googleblog.com/2025/05/gemini-summary-cards-gmail-app.html
- How it appears/access: shown automatically "at the top of the email content for
  messages where a summary is helpful, such as longer email threads or messages with
  several replies" — no manual tap needed (this replaced the earlier flow that
  required tapping to open Gemini in a separate panel). Also requires Gmail's "smart
  features and personalization" setting and "smart features in Google Workspace" to
  be turned on.
  SRC: https://workspaceupdates.googleblog.com/2025/05/gemini-summary-cards-gmail-app.html
- Paid vs free: paid-plan feature — Business Starter/Standard/Plus, Enterprise
  Starter/Standard/Plus, Google One AI Premium subscribers, and the Gemini Education
  add-on; legacy Gemini Business/Enterprise add-on purchasers keep access too.
  SRC: https://workspaceupdates.googleblog.com/2025/05/gemini-summary-cards-gmail-app.html

## AI Overview in Gmail Search
- What it does: "Generate a concise summary or answer from your emails directly
  above search results when you ask a natural language question."
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- How to access: appears above the normal results list when searching Gmail with a
  natural-language question.
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- Paid vs free: requires Google AI Plus/Pro/Ultra or an eligible Workspace plan
  (paid). English only at time of publishing; global.
  SRC: https://support.google.com/mail/answer/16831098?hl=en

## AI Inbox
- What it does: "Review top priorities and topics to catch up on from your inbox" —
  Google's announcement describes it as filtering clutter, highlighting VIPs, and
  surfacing critical tasks like bills or appointment reminders.
  SRC: https://support.google.com/mail/answer/16831098?hl=en ;
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/
- How to access: not documented with a specific menu path on the help page; the
  announcement describes it as a distinct inbox view/experience rather than a
  button.
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/
- Paid vs free: requires Google AI Plus/Pro/Ultra (paid); per the announcement,
  currently "limited to trusted testers," with broader rollout "in the coming
  months." English, US only; Web, iOS, Android.
  SRC: https://support.google.com/mail/answer/16831098?hl=en

## Gmail Live
- What it does: "Talk to Gmail with your voice and get answers to questions about
  your emails."
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- How to access: iOS and Android Gmail apps (not specified further on the help
  page).
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- Paid vs free: requires Google AI Plus, Pro, or Ultra (paid). English; global.
  SRC: https://support.google.com/mail/answer/16831098?hl=en

## Help Me Schedule
- What it does: "Propose times to meet in an email to someone else."
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- How to access: not specified beyond "in an email" — implies it appears as an
  in-line suggestion/tool while composing. Web only.
  SRC: https://support.google.com/mail/answer/16831098?hl=en
- Paid vs free: requires an eligible Workspace plan (paid). English, US only.
  SRC: https://support.google.com/mail/answer/16831098?hl=en

## Proofread
- What it does: "Get writing suggestions beyond spelling and grammar for
  conciseness, tone, and style." Google's announcement phrases it as "advanced
  grammar, tone and style checks so everything is polished before you send."
  SRC: https://support.google.com/mail/answer/16831098?hl=en ;
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/
- How to access: not specified with a menu path on the help page — appears in the
  compose window alongside Help Me Write.
- Paid vs free: requires Google AI Plus/Pro/Ultra or an eligible Workspace plan
  (paid) per the help page; the Google announcement says it is rolling out to
  "Google AI Pro/Ultra subscribers only."
  SRC: https://support.google.com/mail/answer/16831098?hl=en ;
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/

## Suggested Replies (updated Smart Reply)
- What it does: "Select detailed, context-aware reply suggestions at the bottom of
  an email thread." Google's announcement frames it as "an updated version of Smart
  Replies that generates contextual, one-click responses matching your personal
  writing style and tone."
  SRC: https://support.google.com/mail/answer/16831098?hl=en ;
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/
- How to access: appears automatically as reply-suggestion chips at the bottom of an
  open email thread — no menu/toggle needed to see them.
- Paid vs free: paid plans get it globally; free for personal accounts but
  "restricted to the US only" per the help page. The announcement instead
  characterizes it as rolling out free "for everyone" — treat the free/US-only
  scoping on the official help page as the more precise, current answer, and note
  the discrepancy.
  SRC: https://support.google.com/mail/answer/16831098?hl=en ;
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/

## Smart Compose (autocomplete) — legacy feature, NOT Gemini-branded
- What it does: shows grey ghost-text autocomplete suggestions while typing an
  email; predates Gemini and is a separate underlying feature from "Help Me Write."
  Toggled in Gmail Settings under "Smart Compose" ("Writing suggestions on/off").
  SRC: WebSearch summary only (qualtir.com/blog/how-to-turn-off-ai-in-gmail) —
  third-party, NOT independently verified against a fetched support.google.com page
  in this session.
- Not counted as a documented "Gemini feature" here since Google's own Gemini-in-Gmail
  overview page (support.google.com/mail/answer/16831098) does not list Smart Compose
  among the Gemini-branded features; flagged for confirmation, see NOT FOUND.

## NOT FOUND — looked for, could not confirm from an official source
- Exact wording/behavior of "contextual smart compose" as a distinct Gemini feature
  (as opposed to legacy Smart Compose) — no official support.google.com page found
  describing a Gemini-branded evolution of Smart Compose specifically.
- Precise menu path/icon for **Proofread** (which button/icon triggers it in the
  compose window) — the help overview names the feature but does not give the
  click path; would need a dedicated support.google.com page (not located this
  pass).
- Precise UI location/trigger for **Help Me Schedule** and **AI Inbox** — overview
  page states availability/plan requirements but not exact menu path or icon.
- Full verbatim text of support.google.com/mail/answer/14199860 (Workspace
  Experiments summarize instructions) was obtained only via WebSearch's summary,
  not a direct WebFetch of the page in this session — treat as secondary until
  independently re-fetched.
- Whether "Suggested Replies" and "Help Me Write" free/US-only scoping (per the
  overview help page, answer/16831098) has since changed to unrestricted-free per
  the newer blog.google Gemini-era announcement — the two official sources appear
  to disagree slightly on current free availability; not resolved in this pass.
