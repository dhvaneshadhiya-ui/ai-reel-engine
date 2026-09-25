# Structure — gemini-google-apps

Written BEFORE the first sentence. Framework:
`frameworks/shortform-script-framework.md` (S17 shapes; S25 standard).

## STORY ENGINE (framework §4A)

A viewer who thinks "Gemini" means opening a separate chatbot app discovers it is
already sitting inside the five Google apps they have open every day, which matters
because most of these sit behind one button nobody has clicked, and only one of the
five is actually free.

## SHAPE (S17)

**List**, with a spine — same shape as five-free-ai-tools and 5-chatgpt-features. The
spine here is "you don't need to go anywhere" — every item names which app it lives in,
the exact button/menu path, and whether it's free or paid — so five separate menu items
accumulate into one idea (Gemini is already inside the tools you have, not a destination)
instead of five random tips.

## PROMISE (S2)

By the end you know exactly where five real, currently-live Gemini features live inside
Gmail, Docs, Sheets, Drive, and Meet, what each one does differently, and whether you
already have free access or need to pay for it.

## OPEN LOOP (S10)

Planted: the hook's claim — five Gemini features are sitting inside apps the viewer
already has open — and the immediate turn, "most people have never touched the button."
That plants the premise that the viewer has probably scrolled past this exact button
without knowing what it does.
Paid off: the close ("only Gmail's is free... find the button, then decide if it's worth
the plan") turns the premise into an action and answers the money question the whole list
has been building toward — the loop closes by telling the viewer which one costs nothing
and handing them the decision the other four require.

## WHAT -> WHY -> SO WHAT (S7)

WHAT: five Gemini features — Gmail conversation summarization, Docs summarization with
cited sources, Sheets multi-tab chart generation, Drive Ask Gemini (cross-file Q&A),
Meet auto notes — that already exist inside apps most viewers already have open daily.
WHY: Google built Gemini into the apps people already use rather than making them adopt
a separate assistant, so most of these sit behind an easy-to-miss button layered onto an
interface people already know, and four of the five are gated behind a paid plan most
casual users have never checked whether they have.
SO WHAT: a viewer who knows where to click gets a thread summary, a cited document
summary, a chart built from data they didn't have to gather by hand, cross-file answers,
or hands-off meeting notes, without ever leaving the app they were already in — free in
Gmail's case, for the cost of one plan check in the other four.

## CONFIRMATION BEAT (2-5s)

Right after the hook, the first stage scene is Gmail's "Summarize this email" itself: the
official demo animation from support.google.com/mail/answer/14199860, showing the Gemini
panel's own quick-action menu with "Summarize this email" highlighted. It proves the
hook's claim immediately — this exact button is sitting in the viewer's own inbox right
now, for free — before the reel moves to the four paid features most viewers have never
opened.

## VIEWER QUESTIONS

- Q: Do I need to install a separate Gemini app to get any of this? A: "five Gemini
  features are sitting inside apps you already have open" — the hook itself answers
  this.
- Q: Is any of this actually free? A: "That one's free, even on a personal account" (said
  of the Gmail feature specifically, not implied for all five).
- Q: Which of these needs a paid plan? A: "Only Gmail's is free. Everything else here
  needs a paid Google AI or Workspace plan."
- Q: Where exactly do I click for each one? A: NOT ANSWERED in narration by design — each
  stage card shows the exact menu path on screen (Summarize this email at the top of a
  Gmail thread; Ask Gemini side panel in Docs; Ask Gemini side panel in Sheets; Ask
  Gemini top-right in Drive; the notes icon after joining a Meet call) — readable and
  pausable on screen, not read aloud as a click-by-click menu path.
- Q: Can I trust what Gemini writes/summarizes without checking it? A: "worth a skim
  since it could get a detail wrong" (said specifically of Meet's auto notes, where an
  independent review documented a fabricated-detail case — not generalized to all five
  features, since only Meet had that independent evidence).

## WHAT WAS CUT (S11, S21)

- Gmail's Help Me Write, Ask Gemini side panel, summary cards, AI Overview search, AI
  Inbox, Gmail Live, Help Me Schedule, Proofread, Suggested Replies — all real and
  documented (research.md), but each needs a paid plan (Help Me Write's free tier is
  US-only) or is still trusted-tester-only (AI Inbox). Thread summarization was chosen
  as the one Gmail feature that is both free AND broadly available — the strongest
  possible confirmation-beat opener.
- Docs "Help me write" / Refine (rewrite existing text), document creation from a
  prompt, inline/cover image generation — real, cut. Refine specifically was cut not
  just for scope but because NO screenshot exists anywhere on its own Help Center page
  for the Refine floating-toolbar steps (confirmed by loading the live page — that
  section is text instructions only); summarization-with-sources was used instead
  because it is the one Docs sub-feature the page's own demo animation actually shows
  completed on screen.
- Sheets natural-language formula generation, "Fix" on formula errors, table/
  spreadsheet creation from a prompt, `=AI()`/`=Gemini()` in-cell function, pivot
  tables, conditional formatting, dropdowns, checkboxes, "Build or edit entire
  spreadsheets" — real, cut. Formula generation and Fix specifically were cut not just
  for scope but because the Sheets Help Center page has no screenshot of its own for
  either (confirmed by inspecting every embedded image on the live page — only small
  UI icons exist alongside one long demo GIF); multi-tab chart generation was used
  instead because it is the one sub-feature that same GIF actually completes on screen,
  with a named source list.
- Drive's AI-powered search and file/folder summarization — real, cut for scope; Ask
  Gemini was chosen because it is the newest (GA this spring) and most visually distinct
  (multi-file citations) of the three Drive features found.
- Meet's Translated captions — cut because its own help page never confirms "Gemini"
  branding (flagged uncertain in research.md); including it as a Gemini feature would be
  a claim the source does not actually support.
- Google Slides "Help me visualize" (Insert > Help me visualize > Image/Infographic) —
  real and researched, but gated to a narrower trusted-tester rollout than the five picks
  used, and a 6th app would push the reel past the ai-tools 40-60s runtime band. Logged
  in research.md for a future reel.
- The exact dollar price of any Google AI or Workspace plan — no official page with a
  rendered current USD price was found (see research.md NOT CLAIMED); the script says
  "a paid Google AI or Workspace plan" rather than cite an unverified figure.
- The Microsoft Copilot comparison surfaced by independent-evidence research — a real,
  useful "instead of this" angle, but out of scope for a 55s features list; kept in
  research/findings_evidence_honesty.md as a possible future CTA/comment hook.

## SOURCES

Google's own Help Center (support.google.com) pages for Gmail, Docs, Sheets, Drive, and
Meet — each fetched directly and current as of this research — plus two Google-published
announcement/blog posts (blog.google's Gmail Gemini-era post; workspaceupdates.googleblog.com's
Drive GA post) that independently corroborate the Gmail free-tier claim and the Drive GA
date. One independent, non-Google review (tldv.io) for the Meet reliability hedge. Full
list with verbatim quotes and VIA lines in research.md and research/findings_*.md.
