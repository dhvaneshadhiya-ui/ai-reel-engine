# Findings — Gemini Workspace pricing and plans

**Personal path (Google One AI Premium → "Google AI Pro"):**
- $19.99/mo, includes "Gemini Advanced, 2TB storage" — SRC:
  blog.google/products-and-platforms/products/google-one/google-one-gemini-ai-gmail-docs-sheets/
  (original 2024 announcement; plan since renamed).
- Current tiers per one.google.com/about/google-ai-plans/ (fetched today, price fields
  didn't render): **Google AI Plus** = "Gemini in Google apps to help you proofread in
  Gmail" only. **Google AI Pro/Ultra** = same plus "work smarter in Docs and Sheets."
  Drive not mentioned on this page. $19.99/mo for Pro corroborated by third parties
  citing gemini.google/subscriptions, not independently confirmed on an official page
  with a rendered price. VIA (unconfirmed): some 2026 blogs report Plus $7.99/Ultra
  $249.99 — conflicts with official naming, flagged unconfirmed.

**Workspace (business) path:** SRC
workspaceupdates.googleblog.com/2025/01/expanding-google-ai-to-more-of-google-workspace.html
(official) — standalone Gemini add-on discontinued Jan 31 2025; Gemini bundled into
Business Starter/Standard/Plus and Enterprise Starter/Standard/Plus at new pricing (new
customers from Jan 16 2025). Features named: Help me write (Gmail+Docs), email
summarization, Drive/Docs summarization, meeting notes, Sheets tables, chat summaries —
post explicitly does NOT break features down per tier. VIA third parties (unconfirmed
live): Business Standard ~$16.80/user/mo, Business Plus ~$26.40/user/mo, Enterprise
custom.

**Feature specifics (official support.google.com pages):**
- Help me write (Gmail): support.google.com/mail/answer/13955415 & /16831098 —
  "eligible Workspace or Google AI plan: available globally in 8 languages"; "personal
  Google Account: US only." Web/iOS/Android.
- Thread summarization (Gmail): support.google.com/mail/answer/16831098 — "Available
  globally for Google AI Plus/Pro/Ultra, eligible Workspace plans, AND personal Gmail
  accounts" (free, global — broader than Help me write). Web/iOS/Android.
- Sheets formula generation: support.google.com/docs/answer/14356410 — "requires an
  eligible Google Workspace or Google AI plan"; shortcut Ctrl+Alt+G / Cmd+Ctrl+G.
  Literal phrase "Help me organize" NOT found verbatim on official pages checked —
  closest is Gemini's "Structure & Organization" (tables, pivot tables, filters).
- Ask Drive: support.google.com/drive/answer/16686008 — "must have an eligible Google
  Workspace or Google AI plan," plus "end users must have Workspace smart features
  enabled." Reached GA per
  workspaceupdates.googleblog.com/2026/04/ask-gemini-in-drive-now-generally-available.html
  (title confirmed, not fully fetched).

## NOT FOUND
- Live rendered USD price on one.google.com.
- USD version of workspace.google.com/pricing (resolved to India ₹ page with different
  tier names: Base/Starter/Standard/Enterprise).
- Official per-tier (Starter vs Standard vs Plus) feature breakdown.
- Any numeric rate limits.
- Verbatim "Help me organize" label (used informally in this ledger for the Sheets
  organize/structure actions; the official term is closer to "Structure & Organization").
- Confirmed $7.99/$249.99 Google AI Plus/Ultra tier breakdown.

## Ledger note
Exact USD prices are NOT confirmed on a live official page — treat any dollar figure as
single-source/secondary. The script should say "a paid Google AI or Workspace plan"
rather than cite an unverified price.
