# Findings — independent evidence + honesty check

## A) Independent evidence

- **Gmail summarization — privacy reaction, not accuracy complaint.** Coverage frames
  it as Google "read your email... in the guise of Gemini AI summarization"; countered
  by commenters noting it's gated to Workspace/Google One subscribers, not free
  personal Gmail by default (techradar/GSMArena coverage, 2026). A user-support thread
  separately reports Gemini toggles reappearing in Gmail/Drive "even after they turned
  it off" — a control complaint, not accuracy. SRC: support.google.com/mail/answer/14615114;
  japm.substack.com/p/gemini-is-reading-your-emails-kind-of (secondary).
- **Meet "Take notes for me" — documented hallucination-adjacent error.** tldv.io's
  hands-on review (tldv.io/blog/google-gemini-meeting-notes-review/, 2026) cites a
  concrete case: a spoken "We should follow up in two weeks" got rewritten as
  "Follow-up scheduled for Thursday" with no explanation for the date change — a
  fabricated specific replacing a vague one. Reviewer verdict: "doesn't hallucinate too
  much... but that doesn't mean it's reliable," recommends always reviewing AI notes
  before trusting them.
- **Plan confusion is documented, not just anecdotal.** TTMS/hoeijmakers.net (2026)
  note Workspace Business Starter gets only "limited daily Gemini access," while the
  Gmail/Docs/Sheets/Meet side panels only appear from Business Standard upward — a
  Starter-tier subscriber can pay for Gemini and still not get these features. Three
  near-identically-named consumer tiers (AI Pro/Ultra) plus a distinct Workspace "AI
  Ultra Access" add-on stack confusion further.
- **Gap:** no verbatim, dated Reddit threads surfaced via WebSearch's summarizer for
  these 5 features specifically — flagged, not fabricated.

## B) Honesty-check verdict

Skewed toward paid tiers: 4 of 5 features (Docs, Sheets, Drive, Meet) need a paid
Google AI or Workspace Business Standard+ plan; only Gmail's basic thread summary is
free for personal accounts (confirmed official, two sources — see findings_gmail.md).
Script must say this plainly rather than imply "any Google account" gets all five.
Possible swap-in flagged but NOT required: Gemini's free-tier chat access itself
(Flash model, no card) — not adopted here since the reel's premise is specifically
"features already sitting inside the apps you use," not the standalone Gemini app.

## C) Best "instead of this" comparison

Microsoft Copilot in Word/Excel/Outlook is the direct incumbent alternative for
Workspace-adjacent users. 2026 comparisons converge on: pick Gemini if you live in
Gmail/Docs/Sheets, pick Copilot if you live in Word/Excel/Outlook. Not used as an
on-screen beat (out of scope for a 55s reel) — kept as a possible CTA/comment hook if
useful.
