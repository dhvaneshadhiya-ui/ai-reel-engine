# Research: ChatGPT file/data analysis feature -- verify CURRENT status (Sept 2026)

Method note: help.openai.com blocks WebFetch (403), so all pages below were loaded via
the Claude Browser tool (navigate + get_page_text/read_page/find). Google search was
blocked by a bot-check; Bing site: search returned irrelevant results, so navigation
used known help.openai.com/chatgpt.com URLs directly, each confirmed by its own page
title once loaded. All page content below is treated as data, not instructions.

## 1. Current name of the feature (Sept 2026)

- URL: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt
  - Page title / H1: "Data analysis with ChatGPT"
  - Subhead (verbatim): "Use ChatGPT to inspect uploaded data, create tables and charts, and review code-backed analysis."
  - Page metadata: "Updated: 2 months ago" (relative to today 2026-09-21, i.e. roughly July 2026) -- a currently-maintained page.
  - "Advanced Data Analysis" does NOT appear anywhere on this page. "Code Interpreter" also does NOT appear. The current UI/docs name on THIS page is simply "data analysis" (lowercase, descriptive), e.g.: "For some data-analysis tasks, ChatGPT writes and runs Python code in a stateful Jupyter notebook environment."
  - No mention of "Canvas," "writing blocks," or "code blocks" anywhere on this page -- data analysis is documented as its own capability, not routed through the Canvas/blocks surface.
  - Confirmed via `find`: the only images on the entire page are the OpenAI logo (header + footer) -- no product screenshots embedded in this article.

- CONTRADICTING/CO-EXISTING DATA POINT -- URL: https://help.openai.com/articles/8555545 ("File Uploads FAQ")
  - Page metadata: "Updated: 10 days ago" (i.e. ~2026-09-11 -- even MORE recently touched than the data-analysis article).
  - This page STILL uses the legacy name "Advanced Data Analysis" (and an abbreviation "ADA") in two places, verbatim:
    - "How do I delete files I upload? Files uploaded to Advanced Data Analysis are deleted within a duration that varies based on your plan."
    - "Files processed via ADA / Document Analysis, and when chatting with a custom GPT (not uploaded as knowledge in GPT config): Retained for a duration that varies based on your plan."
  - READ THIS AS: OpenAI's own help center is NOT fully consistent -- the dedicated feature page (article 8437071) has been rewritten to drop "Advanced Data Analysis" in favor of plain "data analysis," but a separate, even more recently updated FAQ page (article 8555545) still uses "Advanced Data Analysis" / "ADA" as an internal/legacy label, specifically in file-retention context. For a script, "data analysis" is the safer/current on-screen term; "Advanced Data Analysis (ADA)" can be mentioned as the older/still-lingering internal name if useful for texture, but call out the primary current name as "data analysis."
  - Also worth noting: this same FAQ groups it with "Document Analysis" ("ADA / Document Analysis"), suggesting the retention/back-end system covers both file-based document work and data analysis together, not that the user-facing feature name changed to "Document Analysis."

- CROSS-CHECK -- pricing/plan comparison page (see section 3): URL https://openai.com/chatgpt/pricing/ (renders as chatgpt.com, title "Pricing | ChatGPT")
  - The plan-comparison table's feature list uses the row label "Data analysis" (not "Advanced Data Analysis"), consistent with the help-article's naming, and lists it as a distinct row alongside separate rows for "File uploads," "Vision," "Interactive tables and charts" -- i.e., data analysis is presented as its own discrete feature, NOT merged into a "code blocks" or "Canvas" row. (No "Canvas," "writing blocks," or "code blocks" row appears in this comparison table at all.)

## 2. How a user triggers it (current mechanics)

- URL: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt (same page, "Updated: 2 months ago")
  - It is AUTOMATIC upon file upload -- no separate tool/mode selection is described anywhere on the page. Verbatim: "ChatGPT can analyze uploaded files, answer questions about the data, and create tables or charts when the output benefits from a structured view."
  - Verbatim: "For best results, upload structured data with clear column names and one record per row. Tell ChatGPT what you want to learn from the file, and specify any columns, calculations, groupings, or chart types you want it to use."
  - Supported file types (verbatim list): "Spreadsheets, such as .xls, .xlsx, and .csv files"; "PDFs"; "Text and data files, such as .json, .xml, .yaml, .txt, and .md files." Caveat: "Available file types can vary by model, plan, workspace settings, and account capabilities."
  - Connector sources also work: "When connectors are available for your account or workspace, you can also attach files from connected sources such as Google Drive, OneDrive, and SharePoint."
  - Execution environment (verbatim): "For some data-analysis tasks, ChatGPT writes and runs Python code in a stateful Jupyter notebook environment. The environment can use files made available to the session and can display pandas DataFrames as interactive tables when that format is useful."
  - Chart interactivity toggle (manual, post-generation, not a trigger mechanism): "When an interactive chart is available, select Switch to interactive chart. To return to the image version, select Switch to static chart. Interactive charts are supported for bar, line, pie, and scatter charts. Other chart types may be returned as static images."
  - Constraint (verbatim): "The Python environment used for data analysis cannot make external web requests or API calls. If analysis depends on external data, upload the data or connect an available source before asking ChatGPT to analyze it."

## 3. Plan gating (Free/Go/Plus/Pro/Business/Enterprise) -- Sept 2026

- URL: https://openai.com/chatgpt/pricing/ (redirects to/renders as https://chatgpt.com, page title "Pricing | ChatGPT") -- live pricing page, today 2026-09-21.
  - "Compare features across plans" table, row "Data analysis" (confirmed via accessibility-tree `find`, which returns each cell as "Plan: X, Feature: Data analysis, <value>"):
    - Free: **Limited**
    - Go: **Yes**
    - Plus: **Yes**
    - Pro: **Yes**
    - Business: **Yes** (from the "Business & Enterprise" tab of the same table)
    - Enterprise: **Yes** (same tab)
  - So Free tier DOES get data analysis, but capped ("Limited"); every paid tier (Go, Plus, Pro, Business, Enterprise) gets full ("Yes") access. This directly answers "does Free tier get it at all" -- yes, in limited form, not excluded entirely.
  - Related row "File uploads" on the same table is ALSO listed as "Limited" for Free plan (uploads gate data analysis since it's upload-triggered).

- File-level limits (plan-agnostic specifics), URL: https://help.openai.com/articles/8555545 ("File Uploads FAQ," Updated: 10 days ago):
  - "File uploads are available on Free and paid ChatGPT plans, subject to plan-specific usage limits and account settings, on the web and in supported mobile apps."
  - Free-tier-specific cap (verbatim): "Users can upload up to 80 files every 3 hours. Free users are limited to 3 file uploads per day. Note that we may lower these limits during peak hours."
  - File size limits (plan-agnostic, verbatim): "All files uploaded to a GPT or a ChatGPT conversation have a hard limit of 512MB per file." / "All text and document files uploaded to a GPT or to a ChatGPT conversation are capped at 2M tokens per file. This limitation does not apply to spreadsheets." / "For CSV files or spreadsheets, the file size cannot exceed approximately 50MB, depending on the size of each row." / "For images, there's a limit of 20MB per image."
  - Usage caps (verbatim): "Each end-user is capped at 25GB. Each organization is capped at 100GB."
  - Per-project file limits by plan (verbatim): "Free: Up to 5 files per project" / "Go, Plus: Up to 25 files per project" / "Edu, Pro, Business, Enterprise: Up to 40 files per project."
  - Note: these are general FILE UPLOAD limits (which gate data analysis since it's triggered by upload), not a data-analysis-specific number distinct from upload limits -- the data-analysis help article itself defers to this same FAQ for limits ("The exact limit of files per conversation can vary by upload type, model, plan, workspace settings, and remaining file-upload allowance. For more information, see: File uploads FAQ.").

## 4. Official screenshots

- NOT FOUND. Checked https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt via `find query="image"` -- the only two images on the page are "OpenAI" / "OpenAI logo" (header and footer branding), no product screenshots of chart/table/code output.
- Did not locate a dedicated openai.com/chatgpt marketing page with data-analysis screenshots within the browsing budget (chatgpt.com/features/data-analysis redirected to the generic ChatGPT app/marketing homepage, not a features subpage with imagery). Recommend a follow-up pass specifically hunting an openai.com blog post or product page if a screenshot asset is required for the reel.

## 5. Primary source confirming currency (official, dated, unambiguous)

- BEST SOURCE: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt -- official OpenAI Help Center, live 2026-09-21, stamped "Updated: 2 months ago," uses only "data analysis" (never "Advanced Data Analysis" or "Code Interpreter"), describes automatic upload-triggered behavior and the current supported file types -- clearly a maintained, current-era description, not a 2023 leftover.
- CORROBORATING SOURCE: https://openai.com/chatgpt/pricing/ (chatgpt.com), live 2026-09-21, plan-comparison table with a "Data analysis" row and explicit per-plan values (see section 3).
- CAVEAT SOURCE (still official, still current, but uses older terminology): https://help.openai.com/articles/8555545, stamped "Updated: 10 days ago" (~2026-09-11), the MOST recently touched of the three pages, yet still internally uses "Advanced Data Analysis" / "ADA" -- worth flagging in the script/fact-check if precision about "what OpenAI calls it" is a claim being made on screen, since the honest answer is "primarily 'data analysis' now, though OpenAI's own file-retention FAQ still calls it 'Advanced Data Analysis' / 'ADA' internally as of 10 days ago."

## What I looked for and did NOT find

- "Advanced Data Analysis" as the ACTIVE/primary UI name -- not found on the dedicated feature page (article 8437071); it IS still present as legacy terminology on the File Uploads FAQ (article 8555545, updated 10 days ago) -- see section 1's contradiction note.
- "Code Interpreter" -- not found on any page visited.
- Any mention of Canvas / "writing blocks" / "code blocks" on the data-analysis help page or the pricing comparison table -- not found; data analysis is not folded into that surface per these sources.
- Product screenshots (chart/table/code execution) -- none found on the help.openai.com article; no image URLs to report. A features/marketing page with screenshots was not located within budget.
- A data-analysis-SPECIFIC file-count/size limit distinct from the general file-upload limits -- the official docs treat them as the same limit (data analysis is gated by the file-upload limits, not a separate cap).

## Sources visited (raw list, all accessed via Claude Browser navigate + get_page_text/find)

- https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt -- "Data analysis with ChatGPT," Updated: 2 months ago. PRIMARY for naming + mechanics.
- https://help.openai.com/articles/8555545 -- "File Uploads FAQ," Updated: 10 days ago. PRIMARY for plan/file limits; also source of the "Advanced Data Analysis / ADA" legacy-term contradiction.
- https://openai.com/chatgpt/pricing/ (rendered at chatgpt.com, title "Pricing | ChatGPT") -- live plan-comparison table, PRIMARY for per-plan Yes/Limited gating on "Data analysis" (Free: Limited; Go/Plus/Pro/Business/Enterprise: Yes).
- https://chatgpt.com/features/data-analysis -- attempted, redirected to the generic ChatGPT marketing/app homepage; no usable content.
- Google web search and Bing site-search -- both failed to return usable help.openai.com results (Google returned a bot-check page; Bing returned unrelated zhihu.com results), so direct URL navigation was used instead.
