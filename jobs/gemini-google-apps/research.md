# Research — gemini-google-apps

Claims ledger + search log. Product/list reel (5 Gemini-in-Google-apps features),
format `ai-tools`, animated treatment.

## CLAIMS

- CLAIM: Gemini's Gmail conversation summarization ("Summarize this email," accessed
  from the Gemini panel on an open email/thread) is available free on a personal Gmail
  account, not just on a paid plan — distinct from the broader multi-purpose "Ask
  Gemini" side panel (draft/search/organize/schedule), which does require a paid plan.
  TIER: official
  SPOKEN: "open Gemini on any email and tap Summarize this email to shrink the whole thread into a short summary. That one's free, even on a personal account."
  SURPRISE: 74
  SRC: https://support.google.com/mail/answer/16831098
  SRC: https://blog.google/products-and-platforms/products/gmail/gmail-is-entering-the-gemini-era/
  VIA: Google's own Help Center overview page ("AI Overview Conversation Summaries... also
       available free for personal Gmail accounts") corroborated by Google's own product
       announcement ("conversation summaries are free for everyone, rolling out today at
       no cost") — two independent Google-published pages, not one page repeated. NOTE:
       the screenshot used for this beat (from support.google.com/mail/answer/14199860,
       "Summarize a conversation") shows the Gemini panel's own menu of quick actions
       (Summarize / Suggest a reply / List action items); only the Summarize action is
       spoken as free here — the other two chips are visible on screen but not claimed
       as free, since Suggested Replies' free tier is documented as US-only and "List
       action items" has no separate free-tier confirmation.

- CLAIM: In Google Docs, the Ask Gemini side panel can summarize the document you have
  open and answer in bullet points, citing the source(s) it drew from (shown as a
  "Sources" list in the panel).
  TIER: official
  SPOKEN: "ask Gemini to summarize the page you're on, and it answers in bullets, with the sources it used."
  SURPRISE: 55
  SRC: https://support.google.com/docs/answer/14206696
  VIA: Google Docs Help Center, "Collaborate with Gemini in Google Docs" — "opening the
       Ask Gemini side panel on a text-heavy document surfaces an automatic summary; can
       also be requested" and the bottom bar's "Sources" icon pulls in Drive/Gmail/web
       content. The screenshot used (hero animation on this page) shows exactly this: a
       prompt asking Gemini to "Summarize features from the latest Bik project proposal,"
       a bulleted answer, and a "Sources" section listing the documents used.

- CLAIM: In Google Sheets, the Ask Gemini panel can generate a chart from data spread
  across multiple tabs/sources in the same spreadsheet (not just the sheet you're
  looking at), and returns a written explanation naming which sources it used.
  TIER: official
  SPOKEN: "ask Gemini to chart your data, and it pulls from every tab, not just the one you're on."
  SURPRISE: 63
  SRC: https://support.google.com/docs/answer/14356410
  VIA: Google Sheets Help Center, "Collaborate with Gemini in Google Sheets" — "Chart/
       graph generation: prompt Gemini to build a chart with specified axes/data" and
       "Summarize Drive files / Gmail context... Sources." The screenshot used shows the
       exact prompt "Generate one chart of trends over time which contain the data from
       all three teams," a rendered multi-team revenue chart, and a "Sources (3)" list
       naming the three team tabs it drew from.

- CLAIM: Google Drive's "Ask Gemini" lets a user pick sources across Drive, Gmail, and
  Chat (grouped as a Project) and ask questions that draw on all of them at once, and
  this reached General Availability in a rollout between April 22 and May 6, 2026.
  TIER: official
  SPOKEN: "Drive can now pick sources across Drive, Gmail, and Chat, then answer questions using all of them. Google only finished rolling that out this spring."
  SURPRISE: 79
  SRC: https://support.google.com/drive/answer/16963068
  SRC: https://workspaceupdates.googleblog.com/2026/04/ask-gemini-in-drive-now-generally-available.html
  VIA: Google Drive Help Center ("group related files, folders, or emails ... as sources.
       Then, ask questions to help connect the dots across your data") corroborated by
       Google's own Workspace Updates GA announcement blog post naming the April 22 – May
       6, 2026 rollout window — two independent Google-published pages. NOTE: the
       screenshot used shows the Ask Gemini panel's empty "Add sources" / "Let Gemini
       search for sources" toggle with Drive/Gmail/Chat/Docs/Google icons, which is why
       the spoken line stays at "pick sources... then answer questions" rather than
       claiming the screenshot itself shows a cited answer — the citations claim is
       real and sourced, but this particular frame shows the source-picker, not a
       completed answer, so the citations detail is not spoken over it.

- CLAIM: Google Meet's "Take notes for me" auto-generates meeting notes (a Google Doc,
  built as the call happens) after a single click, with no manual note-taking.
  TIER: official
  SPOKEN: "click one button, and Gemini takes the notes for the whole call"
  SURPRISE: 61
  SRC: https://support.google.com/meet/answer/14754931
  VIA: Google Meet Help Center, "Take notes for me with Gemini in Google Meet" — "click
       the icon after joining, then Start taking notes; auto-generates a Google Doc, live
       Summary so far, organizer recap email." The screenshot used shows the actual
       in-call "Let Gemini take notes for this meeting" panel with its "Start taking
       notes" button, exactly as narrated.

- CLAIM: An independent hands-on review found Gemini's Meet meeting notes can rewrite a
  vague spoken statement into a more specific (and incorrect) detail without flagging the
  change, so the notes should be checked rather than trusted outright.
  TIER: single
  SPOKEN: "worth a skim since it could get a detail wrong"
  SURPRISE: 52
  SRC: https://tldv.io/blog/google-gemini-meeting-notes-review/
  VIA: tldv.io's own hands-on test (a competitor meeting-notes vendor's review, so read as
       an interested party, but the specific example is a first-hand test case, not a
       second-hand repeat of someone else's finding) — "We should follow up in two weeks"
       became "Follow-up scheduled for Thursday" with no explanation for the added
       specificity; reviewer verdict: "doesn't hallucinate too much... but that doesn't
       mean it's reliable."

- CLAIM: Of these five features, only Gmail's conversation summarization is free on a
  personal Google account — Docs summarization, Sheets chart generation, Drive Ask
  Gemini, and Meet's auto notes each require a paid Google AI (Plus/Pro/Ultra) or
  Google Workspace plan.
  TIER: official
  SPOKEN: "Only Gmail's is free. Everything else here needs a paid Google AI or Workspace plan."
  SURPRISE: 46
  SRC: https://support.google.com/docs/answer/14206696
  SRC: https://support.google.com/docs/answer/14356410
  SRC: https://support.google.com/drive/answer/16686008
  SRC: https://support.google.com/meet/answer/14754931
  VIA: each app's own Google Help Center page independently states "requires an eligible
       Google Workspace or Google AI plan" (or equivalent) for that specific feature — four
       separate official pages, one per app, agreeing on the same gating.

## FEATURES + HOW TO USE

Every Gemini-in-Google-apps feature examined this pass, marked USED or CUT with why.
How-to steps for each are the vendor's own, captured in research/findings_*.md.

- Gmail — Summarize this email / conversation summary — USED. Free on personal Gmail,
  also on paid plans. How to use: open a thread with 2+ replies → if the side panel is
  closed, click "Summarize this email" at the top of the thread (or "What's this email
  about?" if the panel is open). The confirmation-beat screenshot shows the Gemini
  panel's own quick-action menu (Summarize / Suggest a reply / List action items); only
  Summarize is spoken as free, since the other two chips' free-tier scope is not
  separately confirmed.
- Gmail — Help Me Write, the broader multi-purpose Ask Gemini side panel (draft/search/
  organize/schedule as one paid feature), summary cards (mobile), AI Overview search, AI
  Inbox, Gmail Live, Help Me Schedule, Proofread, Suggested Replies — CUT. All real and
  documented, but each needs a paid plan (Help Me Write's free tier is US-only, Suggested
  Replies likewise) or is still trusted-tester-only (AI Inbox). Summarization was chosen
  as the one Gmail feature that is both free AND broadly available, making the strongest
  confirmation-beat opener.
- Google Docs — automatic summarization via the Ask Gemini side panel, with a "Sources"
  list citing what it drew from — USED, because it is the one Docs feature with an
  actual official screenshot (the page's hero animation shows exactly this flow); no
  screenshot exists anywhere on the Docs Help Center for the Refine floating-toolbar
  steps (confirmed by loading the live page — that section is text-only), so Refine was
  not used despite being real and sourced.
- Google Docs — Help me write (new text) / Refine (rewrite existing text), document
  creation from a prompt, inline/cover image generation — CUT for scope (Refine
  additionally cut for having no illustrative screenshot); all real, logged in
  research/findings_docs_sheets.md for a future reel.
- Google Sheets — chart generation pulling from multiple tabs/sources, with a cited
  "Sources" list — USED, for the same reason as Docs: it is the one Sheets sub-feature
  the page's single long demo GIF actually shows in a completed state (a rendered
  multi-team chart + a named 3-source list). The page's formula-generation and "Fix"
  steps are real and sourced but have no screenshot of their own on the live page
  (confirmed by inspecting every embedded image on the page — only small 24-36px UI
  icons exist alongside the one large table/chart demo GIF).
- Google Sheets — natural-language formula generation, "Fix" on formula errors, table/
  spreadsheet creation from a prompt, `=AI()`/`=Gemini()` in-cell function, pivot tables,
  conditional formatting, dropdowns, checkboxes, "Build or edit entire spreadsheets" —
  CUT for scope (formula generation and Fix additionally cut for having no illustrative
  screenshot); all real, logged in research/findings_docs_sheets.md.
- Google Drive — "Ask Gemini" cross-file Q&A across Drive/Gmail/Chat sources — USED.
  Reached GA April 22 – May 6, 2026. How to use: on drive.google.com or the Drive app,
  tap "Ask Gemini" (top right); group files/folders/emails as sources; ask a question;
  answers cite the sources and can be saved as a shareable Project. The screenshot used
  shows the source-picker (empty "Add sources" state with app icons), not a completed
  cited answer, so the spoken line describes picking sources and answering, not the
  citation UI specifically.
- Google Drive — AI-powered search ("AI Overview" in the search bar), file/folder
  summarization ("Summarise" toolbar button, one folder at a time) — CUT for scope;
  real, logged in research/findings_drive_other.md.
- Google Meet — "Take notes for me" (auto notes + live summary + organizer recap email)
  — USED. How to use: after joining a call, click the notes icon → "Start taking
  notes" (or pre-enable via the Calendar event's Meet video-call options).
- Google Meet — Translated captions — CUT; branding as a "Gemini" feature is unconfirmed
  on its own help page (flagged uncertain in research/findings_drive_other.md), so it was
  not used as a Gemini claim.
- Google Slides — "Help me visualize" (Insert > Help me visualize > Image/Infographic,
  Gemini-generated) — CUT for scope. Real and documented (support.google.com/docs/answer/16443280)
  but gated to paid plans or the Workspace Experiments trusted-tester program, narrower
  availability than the five picks used; adding a 6th app would also push the reel past
  the ai-tools runtime band. Logged for a future reel.

## NOT CLAIMED

- That any exact USD price applies to Google AI Plus/Pro/Ultra or a Workspace tier —
  no official page with a rendered price was found (one.google.com's price fields did
  not render, and workspace.google.com/pricing resolved to a non-US currency page with
  different tier names). Third-party figures (~$19.99/mo, Business Standard ~$16.80/user/mo)
  are secondary/unverified and are NOT spoken or shown. The script says only "a paid
  Google AI or Workspace plan."
- That Meet's Translated captions or "Ask Gemini in Meet" Q&A are confirmed, current
  Gemini-branded features — the first's Gemini branding is unconfirmed on its own help
  page, and the second's help page (support.google.com/meet/answer/16024610) was
  surfaced by search but never independently fetched/verified. Neither is spoken or
  shown.
- That these five features are a complete list of everything Gemini does inside Google
  apps — at least 15 additional documented features were found and cut for scope (see
  FEATURES + HOW TO USE); the script does not imply completeness.
- Any specific Workspace SKU (Business Starter vs. Standard vs. Plus vs. Enterprise)
  breakdown of which of these features each tier includes — only the generic "eligible
  Google Workspace or Google AI plan" language was found on the primary pages; SEO/
  aggregator sources (TTMS, hoeijmakers.net) claim Business Starter gets only "limited"
  access and side panels start at Standard, but this was not independently confirmed on
  an official Google page, so it is not spoken as a per-SKU claim.
- Any adoption/usage percentage for how many Google users have tried these features —
  no sourced figure was found; not claimed.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-22 Four parallel research passes fetched Google Help Center and Google
  Workspace blog primary pages for: Gemini in Gmail (9 features found); Gemini in Docs
  & Sheets (14+ features found); Gemini in Drive, Slides, and Meet (7 features found);
  pricing/plan gating across all four apps. Full source lists and verbatim quotes in
  jobs/gemini-google-apps/research/findings_*.md.

### 2. WHO ELSE TRIED IT — hands-on or testing by someone who is not the vendor
- 2026-09-22 "Google Meet Gemini notes review accuracy" — found tldv.io's hands-on
  review documenting a specific fabricated-detail case (see CLAIMS). No independent
  hands-on test that added a fact beyond the vendor pages for Gmail summarization, Docs
  Refine, Sheets formulas, or Drive Ask Gemini specifically — these are largely
  vendor-documented product-mechanics claims (see INDEPENDENT-CHECK below).

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-22 "Gemini Gmail Drive privacy reaction Reddit forum" — found tech-press
  coverage (TechRadar/GSMArena-style) framing Gmail/Drive Gemini summarization as a
  privacy concern ("reading your email"), and a Google support thread reporting Gemini
  toggles reappearing after being turned off (a control complaint, not an accuracy one).
  Verbatim, dated Reddit threads specifically about these five features were not
  surfaced by WebSearch's summarizer — flagged as a gap, not fabricated (see
  research/findings_evidence_honesty.md).
- 2026-09-22 "Google Workspace Gemini plan confusion Business Starter Standard" — found
  secondary coverage (TTMS, hoeijmakers.net) describing real plan-tier confusion (Business
  Starter gets limited access; side panels require Standard+) — used to inform the
  honesty framing (see NOT CLAIMED) but not spoken as a confirmed per-SKU fact.

### 4. WHAT WOULD CONTRADICT THIS — the search that would prove the story wrong
- 2026-09-22 "is Gemini in Drive still in preview / beta 2026" — this is what surfaced
  the GA announcement (April 22 – May 6, 2026 rollout), confirming Ask Gemini in Drive
  is not still a limited beta as an older search result might have implied.
- 2026-09-22 Checked whether any of the five USED features had since been renamed,
  retired, or had their plan-gating changed since the pages were published — Gmail
  summarization (confirmed current via two 2026 official pages agreeing on a free tier),
  Docs Refine (confirmed via the Docs Help Center's own dated overview page), Sheets
  formulas (confirmed via the Sheets Help Center's own dated overview page), Drive Ask
  Gemini (confirmed current AND recently promoted to GA, strengthening rather than
  undermining the claim), Meet notes (confirmed via the Meet Help Center's own page, and
  independently stress-tested for reliability by the tldv.io review).

INDEPENDENT-CHECK: 2026-09-22 searched for hands-on/independent testing of Gmail
summarization, Docs Refine, Sheets formula generation, and Drive Ask Gemini specifically
and found tech-press reaction to the privacy/rollout angle but no independent lab that
re-tests these as product-mechanics claims — these are "what does this menu item do, who
can access it" questions that only the vendor's own documentation can authoritatively
answer, same as 5-chatgpt-features' equivalent claims. The one feature where independent,
critical hands-on testing DOES exist (Meet auto notes) was found and used, adding a
hedge the vendor's own page would never volunteer.
