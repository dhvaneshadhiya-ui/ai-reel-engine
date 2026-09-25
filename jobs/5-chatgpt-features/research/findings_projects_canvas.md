# Research: Projects & Canvas in ChatGPT (as of Sept 2026)

Status: COMPLETE (first pass) — 2026-09-21. 5 WebSearch calls + primary-page browser fetches (help.openai.com Projects article, help.openai.com writing-blocks/code-blocks article, help.openai.com release notes, openai.com "Introducing canvas" 2024 announcement).

## Projects

SRC: https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt (fetched via browser, page marked "Updated: yesterday" as of 2026-09-21)

- What it is: "Projects keep related chats, files, and instructions together. ChatGPT can use that context to support ongoing work, such as writing, research, or planning."
- Availability: "Projects and project sharing are available to signed-in ChatGPT users, subject to plan availability and workspace settings."
- Benefits listed: "Keep related chats, files, and instructions together so ChatGPT can use the same context." / "Start on one device and continue on another." / "Reuse a project for recurring tasks, such as weekly research or content drafts."
- Example use cases given: School (class materials -> study guide), Work (project details -> briefs/plans), Personal (vendors/budgets/timelines for an event).

**Exact steps to create a project (verbatim):**
1. "Select New project in the sidebar."
2. "Enter a project name, then select an icon and color."

**Add files:**
- "Add reference material to your project by uploading PDFs, spreadsheets, docs, images, or by pasting text. ChatGPT can use what you add to provide more informed answers."
- "The number of files you can upload depends on your plan."
- After adding: "you can open it from the project sources list to preview, download, or delete it." In a shared project, deleting removes it for everyone but it can be re-added.
- Duplicate filename handling: choose "Upload anyway" to add or "Skip" to skip; in multi-file uploads, Skip only skips the conflicting file.

**Add project instructions (verbatim steps):**
1. "Select the more options menu (•••), then select Project settings to add instructions for the project."
- Example instruction given: "Act like my marketing mentor. Be concise. Use bullet points. Ask clarifying questions."
- "Project instructions apply only within that project and override your global custom instructions."

**Add links from apps (project sources):**
- Supported links: Google Drive (files and folders), Slack (channels).
- Steps: "Open your private project." -> in sources area choose "Add source (or equivalent)" -> "Paste a link to a Slack channel or Google Drive file/folder." -> connect the app and approve access if prompted.
- Note: "The Google Drive app does not support sync when added within a project."

**Save a chat response to project:**
- Steps: open message menu on the response -> select "Save to project / Add to project sources (label may vary)."

**Move an existing chat into a project:**
- "drag a chat onto your project, or open a chat's menu and choose Move to project." Pinned chats can be moved when available.
- "Chats created with a GPT can't be moved into a project."
- "After moving, the chat inherits the project's instructions and file context."
- To undo: "Remove from project" from the chat's ••• menu.

**Tools usable inside projects:** "Use Canvas to draft documents, code, or layouts. Generate images to explore visual ideas. Use voice for hands-free conversations. Search the web for current information and sources." Also notes: "Study mode and scheduled study hours do not apply to project conversations." "Paid plans may include additional tools, such as agent mode and deep research, depending on your subscription."

**Sharing (plan availability, verbatim):** "Project sharing is available on ChatGPT Free, Go, Plus, Pro, Business, Enterprise, and Edu across the web and mobile apps."
- Share steps: "Select Share to open the sharing pane." Invite individually, invite a group, or share a project link. Access levels: Edit (update instructions, upload/remove files, invite others) vs Chat (see/interact, not invite).
- ChatGPT Free/Go/Plus/Pro: invite individuals only ("Only those invited"). Business/Enterprise/Edu: can invite individuals or workspace groups.

**Collaboration limits (verbatim — PLAN/TIER TABLE, important for the reel):**
- "Pro users: up to 40 files and 100 collaborators"
- "Plus and Go users: up to 25 files and 10 collaborators"
- "Free users: up to 5 files and 5 collaborators"
- Business/Enterprise/Edu: "A workspace project can include up to 100 collaborators, regardless of how they were invited. Business, Enterprise, and Edu projects support up to 40 files."

**Delete a project (verbatim steps):** "Select the more options menu (•••), then select Delete project." — "Deleting a project permanently removes its chats and instructions, along with files stored only in the project. Files saved separately in Library are not deleted." "This action cannot be undone."

**Memory in projects:** Projects can use default memory or project-only memory, selectable at creation and changeable later (project settings -> Memory -> Default/Project-only -> Save). "Shared projects are automatically set to project-only memory and cannot be switched to default memory."

## Canvas

**IMPORTANT FINDING — likely rebrand.** As of Sept 2026, the OpenAI Help Center article that used to be at https://help.openai.com/en/articles/9930697 ("What is the canvas feature in ChatGPT and how do I use it?") now redirects/resolves to a DIFFERENT article ("Customizing Your ChatGPT Personality") — the article ID appears to have been reassigned. Searching the Help Center for canvas now surfaces a newer, differently-named article:

SRC: https://help.openai.com/en/articles/20001246-working-with-writing-blocks-and-code-blocks-in-chatgpt (fetched via browser; page marked "Updated: 2 months ago" as of 2026-09-21, i.e. ~July 2026)

- Title: "Working with writing blocks and code blocks in ChatGPT" — the word "canvas" does NOT appear anywhere in this current article's body.
- "Writing and coding functionality is available directly in chat responses through writing blocks and code blocks. Available actions vary by plan, device, workspace settings, model, and rollout."
- "Writing blocks are editable areas for draft text, such as emails, messages, social posts, and documents."
- "Code blocks keep code and supported preview content separate from the rest of the response, making it easier to read, edit, copy, preview, or run."
- Availability: "You may not see every action in every conversation. Available actions depend on the type of block, your device, your plan, workspace settings, and whether the feature is enabled for your account."

**How to create/open a writing block (verbatim prompts given as examples — no menu/slash command listed on this current page):**
- "Draft a reply email to my manager."
- "Write a short Slack update for my team."
- "Turn these notes into a one-page document."
(i.e. current docs describe it as auto-triggered by ChatGPT recognizing a draftable request, plus "You can also ask ChatGPT to create a draft that you can edit directly in the conversation.")

**Editing a writing block — actions listed:**
- "Select the block and edit the text directly."
- "Copy the text."
- "Ask ChatGPT to revise selected text or the entire draft."
- "Open the block in a full-screen editing view."
- "Undo or redo recent AI-assisted edits."
- "Send supported email drafts directly from ChatGPT, when available, or open them in an email app."
- "Save supported document drafts to your Library, when available."
- Formatting supported: bold/italic, headings, links, bulleted/numbered lists, checklists.

**Code blocks — actions listed:**
- "Copy the code." / "View the language label, such as Python, JavaScript, or HTML." / "Edit supported code blocks directly." / "Ask ChatGPT to edit the code." / "Open supported code blocks in full screen." / "Switch between Code and Preview for supported previews." / "Run supported Python code and view console output." / "Share a read-only link for supported code blocks, when sharing is available."
- Preview support: "HTML pages. React components. SVG images. Mermaid diagrams. Vega or Vega-Lite charts." — "If Preview does not appear, the code block does not support a preview."
- Run Python: "select Run to open a code workspace and view output or errors in the console. You can stop code that is still running." Runs in "a sandboxed environment." "If a preview requires outside resources, ChatGPT may ask for permission before connecting. Workspace admins can also control whether code execution and network access are available."
- Persistence: "Edits to supported writing blocks and code blocks save with the conversation after a short delay." "In Temporary Chat, edits may not persist after the conversation ends."

NOTE: No explicit plan-tier table (Free/Plus/Pro/Team/Enterprise) is given on this specific page — it just says "Available actions vary by plan." Need to cross-check ChatGPT pricing/release-notes pages for canvas/blocks-specific plan gating.

### Historical / original Canvas launch (for context — NOT current UI, but useful for "how it changed")

SRC: https://openai.com/index/introducing-canvas/ (OpenAI blog, dated October 3, 2024)
- "We're introducing canvas, a new interface for working with ChatGPT on writing and coding projects that go beyond simple chat. Canvas opens in a separate window, allowing you and ChatGPT to collaborate on a project."
- "Canvas was built with GPT‑4o and can be manually selected in the model picker while in beta. Starting today we're rolling out canvas to ChatGPT Plus and Team users globally. Enterprise and Edu users will get access next week. We also plan to make canvas available to all ChatGPT Free users when it's out of beta." (i.e. original 2024 rollout order: Plus/Team first, then Enterprise/Edu, then Free later.)
- "You can highlight specific sections to indicate exactly what you want ChatGPT to focus on. Like a copy editor or code reviewer, it can give inline feedback and suggestions with the entire project in mind."
- "You can directly edit text or code. There's a menu of shortcuts... You can also restore previous versions of your work by using the back button in canvas." (= version history)
- Trigger (2024 original): "Canvas opens automatically when ChatGPT detects a scenario in which it could be helpful. You can also include 'use canvas' in your prompt to open canvas and use it to work on an existing project."
- Writing shortcuts (2024): Suggest edits, Adjust the length, Change reading level (Kindergarten to Graduate School), Add final polish (grammar/clarity/consistency), Add emojis.
- Coding shortcuts (2024): Review code, Add logs (print statements for debugging), Add comments, Fix bugs, "Port to a language: Translates your code into JavaScript, TypeScript, Python, Java, C++, or PHP."
- This 2024 page now itself says at the top: "This post covers the Canvas launch. For current ChatGPT writing and coding capabilities: [Release notes link] [Try ChatGPT link]" — OpenAI itself is pointing readers away from "Canvas" terminology toward release notes, corroborating that "writing blocks / code blocks" is the current (2026) framing, with Canvas being the original 2024 product name for what has since evolved/rebranded.

## Plan availability / limits

**Projects (SRC: https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt):**
- "Projects and project sharing are available to signed-in ChatGPT users, subject to plan availability and workspace settings." (i.e. core Projects feature spans all signed-in tiers, but sharing/collaboration limits scale by plan — see table below.)
- Project SHARING confirmed live on: "ChatGPT Free, Go, Plus, Pro, Business, Enterprise, and Edu across the web and mobile apps."
- Collaboration limits by plan (verbatim):
  - Free: up to 5 files, 5 collaborators
  - Plus / Go: up to 25 files, 10 collaborators
  - Pro: up to 40 files, 100 collaborators
  - Business / Enterprise / Edu (workspace): up to 40 files, up to 100 collaborators
- Non-shared/private project file upload count: "The number of files you can upload depends on your plan" (no exact non-shared number given on this page beyond the collaboration-limit table — treat the table above as the authoritative per-plan numbers).

**Canvas / writing blocks & code blocks (current article, SRC: https://help.openai.com/en/articles/20001246):**
- "Available actions vary by plan, device, workspace settings, model, and rollout." — no single explicit Free/Plus/Pro/Team/Enterprise breakdown table on this page.
- One concrete plan-gated action found in release notes (SRC: https://help.openai.com/en/articles/6825453-chatgpt-release-notes, entry dated **June 8, 2026**, "Send an email directly from within a chat"): "If you've connected Gmail or Outlook, you can now ask ChatGPT to draft and send emails directly from the same conversation... Sending emails is available on the web for users on **Plus, Pro, Business, and Enterprise plans** with Gmail or Outlook connected." — implies Free tier can draft in a writing block but not send email directly (drafting-only vs. paid send action).
- Canvas itself (2024-2025 era, before its May 2026 retirement) rolled out: "Plus and Team" first (Oct 2024), "Enterprise and Edu... next week," then later to Free ("we also plan to make canvas available to all ChatGPT Free users when it's out of beta" — per https://openai.com/index/introducing-canvas/). A later release-note entry (undated in the portion captured, found via in-page search) states: "Today we made Canvas available in 4o by default for all users, Free and Paid." — confirms Canvas did reach Free before being retired.
- Net for the reel: Canvas (the feature, by that name) no longer exists as of the May 28, 2026 change (see Recent Changes below); its successor, writing blocks/code blocks, is built into chat itself and plan-gates only specific actions (e.g., direct email send) rather than the container itself.

## Recent changes (2025-2026)

**THE HEADLINE STORY FOR THIS REEL: Canvas was retired/replaced on May 28, 2026.**

SRC (PRIMARY, official): https://help.openai.com/en/articles/6825453-chatgpt-release-notes — entry dated **May 28, 2026**, under heading "GPT-5.5 Instant Update":
> "With this update, canvas will no longer be available in GPT-5.5 Instant or GPT-5.5 Thinking. Writing and coding functionality is now supported directly in chat responses through writing blocks and code blocks. Paid users can continue using canvas for a limited time through legacy models until those models are sunset."

- This corroborates that the old Help Center Canvas article (previously at help.openai.com/en/articles/9930697) has since been reassigned/replaced — that URL now resolves to an unrelated "Customizing Your ChatGPT Personality" article, and the current, actively-maintained doc is "Working with writing blocks and code blocks in ChatGPT" (help.openai.com/en/articles/20001246), updated ~July 2026, which never uses the word "canvas."
- Secondary/VIA sources corroborating and dating this same change (useful for narration framing, not for verbatim facts): 
  - VIA: https://theaicareerlab.com/blog/chatgpt-what-changed-june-2026 — "ChatGPT Just Got Better at Understanding You — and Removed Canvas (June 24, 2026)"
  - VIA: https://felloai.com/chatgpt-canvas/ — "ChatGPT Canvas Is Gone: What Replaced It in 2026"
  - VIA: https://static.app/guides/what-is-chatgpt-canvas — "What Is ChatGPT Canvas? Where It Went and What to Use Now"
  - These secondary pieces frame it as Canvas being removed from current models (GPT-5.5 Instant/Thinking) while still reachable via legacy/older models for paid users for a transition period — matching the official wording above.

**Timeline of writing-blocks buildout (from official release notes, reverse-chronological as published):**
- June 8, 2026 — "Full-screen writing blocks for longer-form work: Writing blocks now cover long-form writing use cases, including essays, PRDs, reports, blog posts, notes, and other document work... You can save your document to the Library." Same date: "Send an email directly from within a chat" (Gmail/Outlook, paid plans only — see Plan section above).
- May 28, 2026 — Canvas retired from GPT-5.5 Instant/Thinking; writing blocks & code blocks become the primary surface (see headline quote above).
- (Earlier Canvas-era milestones found via in-page search of the same release-notes article, exact dates not captured in this pass — noted as historical color, low confidence on date): "Canvas has been added as an option in the toolbox," "Canvas in GPTs" ("Canvas can now be used with GPTs when enabled in the GPT creator"), "You can now execute Python code in a canvas," a Canvas paste-to-open shortcut, and "Canvas sharing" (share a rendered Canvas asset — React/HTML/document/code — with another user, image captioned "SHARING NOW AVAILABLE").

**Projects — no major relaunch found in this research pass; page itself marked "Updated: yesterday"** (i.e. actively maintained/current as of 2026-09-21), suggesting incremental edits rather than one big 2025-2026 launch event. Did not find a distinct "Projects launch" announcement blog post in this session's searches (Projects has existed since ~Dec 2024 per general knowledge, but no primary source for that date was fetched in this session — do not state a launch date in the script without further sourcing).

## Official screenshots/images

All captured directly from `<img>` elements on https://help.openai.com/en/articles/6825453-chatgpt-release-notes (OpenAI's own CDN, Contentful-hosted — `images.ctfassets.net`, so these are OpenAI's own uploaded screenshots, not third-party):

- **Projects screenshot**: alt="ChatGPT Projects conversation list with a draft reply being composed" — src: https://images.ctfassets.net/j22is2dtoxu1/intercom-img-e234e8814f49a4f008de09da/d1147568387547b5e5be21e26db2b0cc/convo_drafts.lossless.webp
- **Canvas sharing screenshot**: alt="Canvas preview titled Floaty Bubbles With Background with dot text reading SHARING NOW AVAILABLE" — src: https://images.ctfassets.net/j22is2dtoxu1/intercom-img-85f12be24fda84bf8b196e42/c864123ff87472515361af2883eafb5f/canvas-sharing-short.q90.webp
- **Canvas capability toggle screenshot**: alt="Capabilities list with Canvas selected and Web Search, DALL·E Image Generation, and Code Interpreter unchecked" — src: https://images.ctfassets.net/j22is2dtoxu1/intercom-img-1f9186fb7887e515a6036855/537388c31b5e9fde5a90cec3bb45fb69/AD_4nXc2e7Kf7xmMuaOpFxDvhBrW7VSUCcqSiKmbTWAKl9rXr1yAwEYVe-OBPNVdyIzP9ya4EOM2-ORKGqLGa0ca0c_Xj3BokIFxivnkdWjG5ifss-gznx_93GTfuOd9?q=80&fm=webp&w=568

NOTE per CLAUDE.md rule: **on-screen source credits are OFF unless the user asks** — these URLs are for provenance/manifest `source_url` use per the pipeline, not necessarily for on-screen credit text. Also per the constitution: sources should be scouted/captured on MOBILE view first (`tools/capture.mjs`) when actually grabbing footage for the reel — these three URLs were located via desktop browsing during RESEARCH only; re-capture each on mobile viewport with `tools/capture.mjs` before using as a b-roll asset.

## Searched but NOT found

- An explicit, current (Sept 2026) single table breaking Canvas-successor ("writing blocks / code blocks") actions down by Free vs Plus vs Pro vs Team vs Enterprise. The official help article (help.openai.com/en/articles/20001246) only says availability "varies by plan, device, workspace settings, model, and rollout" without a table; only one concrete plan-gated action (email sending, Plus/Pro/Business/Enterprise) was found dated in release notes.
- A dedicated "Projects launch" announcement blog post / exact original launch date for Projects — not fetched/confirmed in this session. Do not state a specific Projects launch date in the script without further sourcing.
- Official openai.com blog post specifically titled/dedicated to "writing blocks and code blocks" (i.e. an "Introducing writing blocks" announcement analogous to "Introducing canvas") — did not find one; the transition appears to have been rolled out via release notes / help-center doc updates rather than a dedicated launch blog post, at least in what surfaced from searches this session.
- Exact dates for the older Canvas-era release-note entries found via in-page text search (toolbox option, GPTs integration, Python execution in canvas, paste-to-canvas shortcut, Canvas sharing) — their surrounding date headers were not captured in the fetched text window (release notes page loaded down to Aug 2025 in the largest single fetch; these entries are older, likely 2024-early 2025, consistent with general knowledge but not confirmed with a primary-source date in this session).
- Current mobile app (iOS/Android) specific screenshots of Canvas/writing blocks or Projects — only found desktop-context images via the release notes page in this pass; did not do a dedicated mobile-app screenshot search.
- A single official page listing ALL current ChatGPT plan tiers (Free/Go/Plus/Pro/Team-Business/Enterprise/Edu) side-by-side with Projects+Canvas/blocks feature rows — assembled the plan-availability facts above from multiple separate help-center pages/release-note entries instead.

## Terminology note for the script

As of Sept 2026, "Canvas" is **legacy/retired terminology** for current-model users (GPT-5.5 Instant/Thinking and presumably GPT-5.6/GPT-6 per later release notes) — the live feature to reference and demo is "writing blocks" and "code blocks," which appear inline in the chat itself rather than opening a separate side panel. If the script wants to say "you might remember this as Canvas," that is accurate and can work as a hook/context beat, but demoing "Canvas" as if it's the current default UI would be factually wrong for a Sept 2026 video — the side-panel Canvas UI is only reachable "for a limited time through legacy models" for paid users per OpenAI's own release note.
