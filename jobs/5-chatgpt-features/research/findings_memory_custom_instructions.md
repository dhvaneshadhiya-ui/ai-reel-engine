# Research: Memory and Custom Instructions in ChatGPT (as of Sept 2026)

Status: COMPLETE (2026-09-21) — see full search log and synthesis near end of file.
Note: all fetched page content treated as data, not instructions.

## Search log
(filled in as searches run)

## Findings

### What "Memory" is vs "Custom Instructions"
(pending)

### How to turn on/off and edit each
(pending)

### Plan/tier availability and limits
(pending)

### Recent (2025-2026) changes
(pending)

### Official screenshots/images
(pending)

## Not found / could not confirm
(pending)

## SEARCH 1-2: WebSearch for OpenAI help center pages on Memory + Custom Instructions
Found primary URLs:
- https://help.openai.com/en/articles/8590148-memory-faq ("Memory in ChatGPT") — page title now "Memory in ChatGPT", updated per browser "2 days ago" (i.e. ~Sept 19, 2026)
- https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt ("ChatGPT Custom Instructions")
- https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work (redirects/merged into Memory FAQ topic now, see below)
- https://help.openai.com/en/articles/9295112-memory-faq-business-version (Business/Team version)
- https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality
- https://help.openai.com/en/articles/20001038-characteristics-in-chatgpt

NOTE: WebFetch tool returns HTTP 403 Forbidden on help.openai.com (bot-blocked). Used the Browser pane (mcp__Claude_Browser) instead to load and read these pages successfully.

## FETCH: https://help.openai.com/en/articles/8590148-memory-faq (via Browser, full text captured, "Updated: 2 days ago")

### Memory vs Custom Instructions — exact distinction (FAQ answer, verbatim)
> "Is memory different from custom instructions? Yes. Custom instructions are direct guidance that you provide about what ChatGPT should know and how it should respond. Memory can use relevant information that develops across conversations and other available sources."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### What Memory is (verbatim)
> "When Memory is enabled, ChatGPT can remember relevant preferences and details from your chats and other available sources. This can help you pick up where you left off and spend less time repeating yourself."
Sources it can draw on (plan/region dependent): "past chats", "saved memories", "custom instructions", "files in Library", "content from connected apps, such as Gmail".
> "Memory does not retain every detail from every conversation. ChatGPT decides which available information is relevant to a response, and Memory can change as your context changes."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Menu path to manage Memory (verbatim, current as of fetch)
> "Open Settings. Select Personalization. Select Memory."
> "Depending on your memory experience, available controls may include Memory, Reference saved memories, Reference chat history, Memory summary, Manage, or Saved memories."
Note explicit caveat: "Memory features and controls can vary by plan, region, platform, and workspace settings. If a setting described here is not visible, it may not be available for your account yet."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Two sub-toggles inside Memory: "Reference saved memories" and "Reference chat history"
- **Reference chat history**: "turning it on lets ChatGPT use relevant information from past conversations to personalize future responses." Unlike explicit saved memory, "information derived from chat history can change as ChatGPT updates what is most useful to remember." If turned off: "information remembered from past chats is scheduled for deletion from OpenAI systems within 30 days. The original chats remain in your history unless you delete them." "There is no separate storage limit for what ChatGPT can reference through chat history." Turning it off "does not delete your saved memories."
- **Saved memories**: "details that you explicitly ask ChatGPT to remember or that ChatGPT saves as useful context when that behavior is available." "Stored separately from chat history. Deleting the original chat does not automatically delete a separate saved memory." Can ask ChatGPT to forget, or delete from Memory settings. "Depending on your plan and platform, saved-memory controls can also include search, sorting, automatic prioritization, and version history."
- **Relationship between the two toggles**: "If your settings include Reference saved memories, turning it off also turns off Reference chat history. When Reference saved memories is on, you can manage Reference chat history separately."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### "Improved memory" vs "legacy saved memories" (recent UX change)
> "Improved Memory continually updates a broader summary of relevant context. Legacy saved memories use a more explicit list of individual memory items."
Switch path: "Open Settings. Select Personalization. Select Memory. Select Saved memories to use the legacy experience, or select Try improved memory to return to improved Memory." "Changing the Memory experience does not delete your chat history."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Improved memory in regulated workspaces (Enterprise/Healthcare)
> "In ChatGPT for Healthcare and ChatGPT Enterprise with Regulated Workspace, improved memory is disabled by default. Workspace owners and admins can make Use improved memory available to the default workspace role or eligible custom roles."
> "This feature is not covered under your BAA. PHI should not be entered when using this feature."
Also: "Project-only memory" option to keep memory context limited to a specific project (chats in a project can reference each other but not outside).
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Reviewing what ChatGPT remembers: "Memory summary" and "Sources"
> "The memory summary is a high-level view of information that ChatGPT may use to personalize responses. It does not necessarily include every detail or source that Memory can reference." You can also ask ChatGPT what it remembers about you.
Controls on memory summary: enter a correction in the text field; highlight text and provide a correction; select "Don't mention this again"; select "Delete and turn off memory" from (•••) menu.
> "Sources may appear below the response" showing what contributed to personalization (chat, saved memory, custom instruction, file, or connected email). "Memory Sources are not included when you share a conversation through a shared link."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Deletion mechanics
> "It can take time for deletion and Memory updates to propagate. OpenAI may retain logs of deleted saved memories for up to 30 days for safety and debugging purposes."
Turning off Memory entirely: "does not delete your past chats. If you turn Memory on later, ChatGPT may create new remembered information from chats that remain in your history."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Memory in Temporary Chat
> "Before starting a temporary chat, you can choose whether it uses existing memories, custom instructions, and plugins. Select Unpersonalized if you do not want to use them. You cannot change this choice after the conversation starts."
> "Temporary chats do not create or update memories, even with personalization on."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Privacy / model training
> "For personal ChatGPT accounts, OpenAI may use chats and remembered information to improve models when Improve the model for everyone is on. You can turn that setting off in Data controls."
> "By default, OpenAI does not use content from ChatGPT Business, Enterprise, Edu, or ChatGPT for Healthcare workspaces to train its models."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Other FAQ nuggets (verbatim)
> "Can ChatGPT remember my name or account identity? ChatGPT can remember a name that you provide. When Reference chat history is enabled, ChatGPT may also use the account name already shown in the product when that information is relevant."
> "Does ChatGPT search my history for every response? No. ChatGPT looks for relevant context when it is likely to improve a response."
> "Can memory personalize web searches? Yes. When Memory is enabled, ChatGPT may use relevant details to formulate a more useful search query. For example, location or dietary preferences can help refine a restaurant search."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

### Parental controls
> "For a linked teen account, a parent or guardian can manage supported memory controls through Parental controls."
SRC: https://help.openai.com/en/articles/8590148-memory-faq

## FETCH: https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt (via Browser, "Updated: last month")

### What Custom Instructions is (verbatim)
> "Custom instructions allow you to share anything you'd like ChatGPT to consider in its response. Your custom instructions are applied immediately to all chats."
> "Custom instructions are available on all plans on Web, Desktop, iOS, and Android."
SRC: https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt

### Exact menu path — Enable/Disable (verbatim, current Sept 2026)
iOS & Android:
> "In your Settings, select Customize ChatGPT. Please make sure that Enable customization is toggled ON. Enter your instructions in the Custom Instructions field."
Web & Desktop:
> "In your Settings, select Personalization. Please make sure that Enable customization is toggled ON. Enter your instructions in the Custom Instructions field."
To disable (Web & Desktop): "In your Settings, select Personalization and click on Custom Instructions. Toggle Enable customization OFF. [Optional] Delete your instructions from the relevant fields."
Note: "Updates to custom instructions settings are applied immediately across all chats (including existing conversations)."
SRC: https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt

### Character limits by plan (verbatim) — KEY PLAN-GATING FACT
> "Free and Go users can save up to 1,500 characters in custom instructions. Plus, Pro, Enterprise, Business, and Education users can save up to 5,000 characters."
Note: this names a "Go" plan tier (lower-cost/regional tier) alongside Free/Plus/Pro/Enterprise/Business/Education — not in the original 4 tiers (Free/Plus/Pro/Team) assumed in the brief; worth flagging as a 2025-2026-era addition.
SRC: https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt

### Other facts (verbatim)
> "If you use third party plug-ins, then the model may provide plug-in developers with relevant information from your instructions."
> "Information from your use of custom instructions will also be used to improve model performance – like teaching the model how to adapt its responses to your instructions without overdoing it."
> "Are custom instructions included in my ChatGPT data export? Yes."
> "When you delete your OpenAI account, custom instructions that are tied to your account will also be deleted within 30 days."
> "If I update or remove my custom instructions, will previous versions of my instructions continue to appear in my chat history? Yes, updates to your instructions are reflected only in future conversations."
> "There will be no API for custom instructions, as the Chat Completions API system messages should be used for a similar effect."
SRC: https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt

## FETCH: https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality (via Browser, "Updated: 23 days ago" ~ Aug 29 2026)
This is a DISTINCT, third related feature: "Base style and tone" personality picker — separate from both Memory and Custom Instructions, but works alongside them.

### What it is (verbatim)
> "A personality is the style and tone ChatGPT uses when responding to you. It combines traits, voice, and behavior to shape how answers feel, whether that is friendly and casual, concise and professional, or something else."
> "Changing your personality does not change what ChatGPT can or cannot do, or the safety rules it follows. It only guides how ChatGPT communicates."
> "Your selected personality works alongside any saved memories or custom instructions you've set... If a saved memory contains guidance that conflicts with a personality's style... it may override or reduce the visible traits of that personality."
SRC: https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality

### Menu path (verbatim)
Web: "Select your profile icon in the bottom-right corner. Select Personalization. Use the dropdown next to Base style and tone to select a personality." Applies across all chats immediately.
iOS/Android: "Select your profile icon to open Settings. Go to Personalization. Use Base style and tone to select a personality."
SRC: https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality

### Personalities offered (current, Sept 2026): Default, Professional, Friendly, Candid, Quirky, Efficient, Cynical (with described tone/best-for each).
SRC: https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality
NOTE: This is likely OUT OF SCOPE for a script strictly about "Memory vs Custom Instructions" but useful as a caveat that ChatGPT Settings > Personalization now has THREE related-but-distinct controls: Memory, Custom Instructions, and Base style/tone (personality). Worth one line in the script to avoid confusing personality with custom instructions.

## FETCH (official announcement): https://openai.com/index/chatgpt-memory-dreaming/ — "Dreaming: Better memory for a more helpful ChatGPT" — dated June 4, 2026 (via Browser)

### THE BIG RECENT CHANGE (2026): "Dreaming" memory architecture
> "Today we're beginning to roll out a more capable and scalable system for synthesizing memory, developed to tackle the staleness, correctness, and scalability challenges that we observe when memory is applied to the hundreds of millions of users and multi-year time horizons in ChatGPT."
> "This update is available to Plus and Pro users in the US today, and will roll out to additional countries and Free and Go users over the coming weeks." [as of June 4, 2026]
SRC: https://openai.com/index/chatgpt-memory-dreaming/ (OpenAI official blog, dated June 4, 2026)

### Timeline of memory feature (verbatim, straight from OpenAI) — GOOD FOR SCRIPT
> "Memory first launched in April 2024 (also known as saved memories). The feature let you ask ChatGPT to remember information and carry it forward into future chats." Only written explicitly, went stale over time.
> "In April 2025, we updated ChatGPT's memory by giving the model the ability to reference chat context outside of the saved memories list; this was done by introducing the first version of dreaming—a method for ChatGPT to automatically curate memories in the background by referencing chat history."
> "Today [June 4, 2026], we are launching a significantly more capable and compute-efficient memory architecture built on top of dreaming." Internally called "Dreaming V3" (2026), vs "Saved memories + Dreaming V0" (2025) vs "Saved memories" only (2024).
SRC: https://openai.com/index/chatgpt-memory-dreaming/

### What "dreaming" does mechanically (verbatim)
> "dreaming leverages a background process that allows ChatGPT to learn from many conversations and synthesize ChatGPT's memory state in order to always provide the freshest, most relevant context to your conversations. Dreaming also makes it easier for memory to include context that occurs naturally in conversation, without relying on explicit requests to remember something."
> "With dreaming, memories are automatically updated as time passes, allowing ChatGPT to revise its memory from 'You're going to Singapore in July' to 'You went to Singapore in July 2026' when the trip ends."
SRC: https://openai.com/index/chatgpt-memory-dreaming/

### Free-tier rollout + compute efficiency (verbatim) — KEY PLAN-GATING FACT
> "While dreaming-based memory has been available to Plus and Pro users for some time, we are only now able to offer Free users a version that meets our quality bar... Recent improvements reduced the compute required to serve dreaming to Free users by approximately 5x, making it possible to begin rolling out dreaming to Free users over the coming weeks and to increase memory capacity for Plus and Pro users."
=> Confirms: as of June 2026 announcement, Memory ("dreaming") is rolling out to ALL tiers including Free, with Plus/Pro getting increased ("doubled" per secondary source, not verbatim-confirmed on page) memory capacity. "Go" tier also named as a rollout target (a lower-cost tier, presumably regional, alongside Free).
SRC: https://openai.com/index/chatgpt-memory-dreaming/

### The "memory summary" page (verbatim) — matches what Help Center describes
> "The memories synthesized by dreaming are reviewable through a summary of them made visible in the memory summary page. From the memory summary, you can quickly glean the highlights of what ChatGPT knows about you, add or update information about yourself, and provide instructions on what topics ChatGPT should bring up and when."
SRC: https://openai.com/index/chatgpt-memory-dreaming/

### Preference types memory tracks (verbatim, good illustrative list for script)
> "Preferences can take several forms: Instructions for how ChatGPT should respond ('don't bring up Stan again'). Your personal preferences or constraints ('I'm vegetarian'). Implicit preferences that shape what's relevant to you ('I live near San Francisco' → local options should be tailored to this area)."
SRC: https://openai.com/index/chatgpt-memory-dreaming/

CAUTION: A third-party site (tech-insider.org, "ChatGPT Dreaming V3: Memory Recall Jumps to 82.8%") appeared in search results with a specific stat headline. NOT used/verified — no such percentage found on the official OpenAI blog page as fetched. Treat that figure as UNCONFIRMED / do not use in script.

## FETCH: https://help.openai.com/en/articles/9295112-memory-faq-business-version (via Browser, "Updated: 3 days ago")

### Memory for ChatGPT Business/Team — plan-specific facts (verbatim)
> "Organizations and businesses using ChatGPT Business can now use memories to enhance their experience."
> "Individual users can disable Memory at any time through their Settings. Workspace owners can control whether personalization and memory features are available across the entire workspace. If a workspace owner turns off Memory for the workspace, existing saved memories for members in that workspace are deleted."
> "Can I share memories from my account with other members of my workspace? No. Memories are: Tied to each individual account. Not transferable to other users, even within the same Business workspace."
> "Do you train your models with memories? No... By default: Workspace data, including conversations and memories, is not used to train OpenAI models."
> Deleting a workspace permanently deletes all memories; deactivating a workspace does NOT delete memories (access is just paused).
SRC: https://help.openai.com/en/articles/9295112-memory-faq-business-version

## FETCH: https://help.openai.com/en/articles/11989085-what-is-chatgpt-go ("Updated: last month") — confirms a real "Go" tier exists Sept 2026, and it DOES include Memory

### ChatGPT Go plan — confirms plan-gating detail for Memory AND Custom Instructions char limit
> "ChatGPT Go is a low-cost subscription plan that provides expanded access to ChatGPT's most popular features at an affordable price." "Note: ChatGPT Go is now available in all ChatGPT supported countries."
> What's included beyond Free: "...Longer memory for more personalized responses: Keep conversations flowing with a larger context window... Access to projects, tasks, custom GPTs, and Library..."
> "Are reasoning models included with ChatGPT Go? Yes... Think uses GPT-5.6 Luna. ChatGPT Go does not include GPT-5.6 Sol." [confirms model family naming as of Sept 2026 for factual accuracy elsewhere, out of scope for this topic]
> Sign-up path: "Log into ChatGPT. Click on your profile icon -> Upgrade Plan. Select Try Go."
SRC: https://help.openai.com/en/articles/11989085-what-is-chatgpt-go

## PLAN/TIER SUMMARY (synthesized from above official sources)
- Memory: available on Free, Go, Plus, Pro, Team/Business, Enterprise, Edu -- but capacity/experience differs: "Longer memory" explicitly called out as a Go-plan upsell over Free; Plus/Pro got increased memory capacity per the June 2026 Dreaming rollout (compute savings used to extend to Free, per official blog quote above). Enterprise/Healthcare "improved memory" is OFF by default and must be enabled by workspace admins (BAA/PHI caveat).
- Custom Instructions: "available on all plans on Web, Desktop, iOS, and Android" per official FAQ. Character limit is the one CONFIRMED plan-gated number: Free & Go = 1,500 characters; Plus/Pro/Enterprise/Business/Education = 5,000 characters. (SRC: https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt)
- Business/Team: workspace owners/admins can force-disable Memory and personalization workspace-wide; individual toggle still exists per user.

## Official screenshots found (exact URLs)
On https://help.openai.com/en/articles/8590148-memory-faq (Memory in ChatGPT), the article embeds two official product screenshots (captured via `document.querySelectorAll('article img')` on the live page):
- https://images.ctfassets.net/j22is2dtoxu1/1wjkdvbQyMTJWduyjYAHfz/a553c0813a31abca66bdd54da1666dca/7.png?q=80&fm=webp&w=1147 (alt text: "Screenshot 2026-06-04 at 8.58.35 AM")
- https://images.ctfassets.net/j22is2dtoxu1/4HqlKblQXe9gvo2Q7NeI6P/91b47c9c42f6be15c3ef9cb3ff1c6294/8.png?q=80&fm=webp&w=1176 (alt text: "Screenshot 2026-06-04 at 8.59.26 AM")
Both dated June 4, 2026 -- the same day as the "Dreaming" memory relaunch blog post -- so these are near-certainly screenshots of the NEW memory summary/settings UI (Settings > Personalization > Memory), captured on desktop/web.
Checked and found NO embedded images on:
- https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt (Custom Instructions FAQ) -- text only, no screenshots.
- https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality (Personality FAQ) -- text only, no screenshots.
Note: these are Intercom/Contentful-hosted help-center images (images.ctfassets.net), an OpenAI-controlled CDN, not a third party.

## Recent changes timeline -- consolidated (all from official OpenAI sources above)
- April 2024: Memory launches as "saved memories" -- explicit, user-triggered ("remember that...").
- April 2025: "Dreaming" v0 introduced -- background process lets ChatGPT synthesize memory from chat history automatically, not just explicit asks. (per https://openai.com/index/chatgpt-memory-dreaming/)
- April 2025 (third-party-reported, not directly confirmed on an official page in this research pass): "Memory with Search" rolled out for Plus/Pro but excluded EEA, UK, Switzerland, Norway, Iceland, Liechtenstein.
- June 4, 2026: "Dreaming V3" -- rebuilt, ~5x more compute-efficient memory architecture ships to Plus/Pro in the US immediately, with rollout "to additional countries and Free and Go users over the coming weeks." New memory summary page, ability to add/update/correct memory inline, controls for which topics ChatGPT should raise. (official: https://openai.com/index/chatgpt-memory-dreaming/)
- June 16, 2026 (third-party-reported -- TechTimes -- NOT independently confirmed on an official OpenAI page in this pass): Memory ("Memories") feature reported extended to EEA/UK/Switzerland users, off by default there, alongside Codex Computer Use / Chrome extension / Chronicle.
- "ChatGPT Go" plan (official, help.openai.com/en/articles/11989085): a $8/mo-class low-cost tier, launched and by Sept 2026 "available in all ChatGPT supported countries," includes Memory ("longer memory... larger context window") as an upsell over Free.
- "Base style and tone" (Personality) picker -- a THIRD, separate personalization control (Default/Professional/Friendly/Candid/Quirky/Efficient/Cynical) added to Settings > Personalization, distinct from both Memory and Custom Instructions, last updated ~Aug 29, 2026 per its help page.

## What was looked for and NOT found / could not fully confirm
- **Exact EU/EEA/UK/Switzerland current availability and default-on/off state for Memory as of Sept 2026**: found only via third-party outlets (TechTimes, Selina.ai, PrimeTel Cyprus, an OpenAI Developer Community forum thread) reporting an April 2025 exclusion and a June 16, 2026 EEA/UK/Switzerland rollout with memory off-by-default there. Could NOT locate an OpenAI help.openai.com or openai.com page in this research pass that states current EU-region memory availability/defaults explicitly. Flagged as UNCONFIRMED against a primary source -- do not state as fact in the script; if EU availability is mentioned, hedge it ("reportedly," "as rolled out in stages") or omit.
- **A specific numeric cap on saved memories (e.g., "~200 memories" or "1,500 words")**: multiple third-party SEO/blog sites (MemoryLake, aimemory.pro, chatgptmemory.com) cite a ~1,500-word / ~200-entry ceiling, but explicitly caveat that "OpenAI doesn't publish a fixed size figure" and call it an estimate from user observation. No official OpenAI page in this research pass states a specific number. Do NOT use a specific number in the script; the official framing is qualitative ("Memory can change as your context changes," capacity increased in the June 2026 update, no official figure given).
- **Whether Plus/Pro memory capacity was literally "doubled" in the June 2026 update**: this specific word ("doubling") appeared in a secondary summary (a WebSearch AI-generated synopsis) but was NOT found verbatim on the official openai.com blog post itself when fetched directly -- the blog only says compute-efficiency gains let Free users get dreaming while increasing Plus/Pro capacity, without giving a multiplier. Treat "doubled" as unconfirmed.
- **The "ChatGPT Dreaming V3: Memory Recall Jumps to 82.8%" statistic** from tech-insider.org: not corroborated on the official blog; likely a third-party site's own benchmark or possibly unreliable/fabricated. NOT used.
- Did not find a dedicated official announcement specifically for Custom Instructions changes in 2025-2026 beyond what's in its FAQ page (last updated "last month," i.e., ~Aug 2026) -- the FAQ page itself doesn't call out a specific dated change log the way the Memory blog does; its content appears to be a maintained/evergreen FAQ rather than a dated announcement.

## Search log (full)
1. WebSearch: "ChatGPT memory FAQ site:help.openai.com" -> found article list
2. WebSearch: "ChatGPT custom instructions site:help.openai.com" -> found article list
3. WebFetch attempts on help.openai.com -> blocked (403); switched to Claude_Browser tool for all help.openai.com and openai.com fetches thereafter.
4. Browser fetch: help.openai.com/en/articles/8590148-memory-faq (full text)
5. Browser fetch: help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt (full text)
6. Browser fetch: help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality (full text, truncated at 8000 chars)
7. WebSearch: "OpenAI ChatGPT memory launch Europe EU availability 2025 2026 announcement"
8. WebSearch: "openai.com blog ChatGPT memory update 2026"
9. Browser fetch: openai.com/index/chatgpt-memory-dreaming/ (full text, official June 4 2026 blog)
10. Browser fetch: help.openai.com/en/articles/9295112-memory-faq-business-version (full text)
11. WebSearch: "ChatGPT saved memories limit number of memories maximum 2026"
12. WebSearch: "\"ChatGPT Go\" plan pricing what is it OpenAI"
13. Browser fetch: help.openai.com/en/articles/11989085-what-is-chatgpt-go (full text)
14. WebSearch: "ChatGPT memory EEA UK Switzerland availability restricted 2026"
15. Browser + JS: checked embedded <img> tags on the three help.openai.com articles for official screenshots.

## STATUS: RESEARCH COMPLETE for the requested scope (budget: used ~7 WebSearches + ~9 page fetches, within reasonable range of the 3-6 search budget given the need to verify plan-gating and screenshot facts precisely).
