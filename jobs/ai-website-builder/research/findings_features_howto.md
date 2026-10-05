# DeepSite: current features and vendor how-to (research subagent, 2026-10-05)
Primary sources only (live page, Space repo files, HF Hub API). UI strings from source, not watched rendering.

## Version
- https://huggingface.co/api/spaces/enzostvs/deepsite "title": "DeepSite v4"; landing "DeepSite: v4 is here"; 16,610 likes; created 2025-03-26; last modified 2026-02-06
- v4 commits Jan 26-28 2026; last commits Feb 5-6 2026 ("add download project"). Quiet ~8 months.
- README license: mit; "Generate any application by Vibe Coding it"

## Models
- https://huggingface.co/spaces/enzostvs/deepsite/raw/main/lib/providers.ts default `moonshotai/Kimi-K2.5`; picker: Kimi K2.5, DeepSeek V3-0324, DeepSeek V3.2, Qwen3 Coder Next, GLM-4.7, MiniMax M2.1
- Safe line: "open models like Kimi, DeepSeek, Qwen". Do NOT say "powered by DeepSeek".

## Features (v4)
- Prompt -> website: HTML + Tailwind CDN; "Always responsive and mobile-friendly" (lib/prompts.ts)
- Multi Pages (landing); multi-file
- Chat follow-ups patch code: "DO NOT rewrite entire files when updating" (prompts.ts)
- Redesign from URL CURRENT: components/ask-ai/redesign.tsx "Redesign your Site!", "Enter your website URL to get started:"; tour "Redesign with a Click"
- Media upload: "Upload files to include them in the AI context." (uploader.tsx)
- Model picker: tour "The Brains Behind It"
- Publish: app/api/projects/route.ts sdk "static", user's account, DeepSite badge; public default (inferred); <name>.static.hf.space
- Desktop/Mobile + Code/Chat toggles (header.tsx); version history; download route; rename
- Limits: components/pro-modal/index.tsx "reached the monthly free limit of DeepSite." "Subscribe to PRO ($9/month)"

## Sept-2025 reel claims
- "v2": STALE (v4). "powered by DeepSeek": STALE (default Kimi K2.5). "redesign by link": CURRENT. "click and edit any part": NOT FOUND in v4 code.

## HOW TO USE (vendor steps, onboarding.tsx + UI strings)
1. Open deepsite.hf.co
2. Type what you want in the prompt box
3. Optional: pick a model
4. Optional: Redesign -> paste URL -> Redesign
5. Optional: paperclip to add media
6. Send; preview Desktop/Mobile; Code to see files
7. Ask for changes in chat
8. Sign in with Hugging Face; publish as static Space; "See Live preview"
9. History / download

## Not found
Dated v4 launch post; v3 changelog; click-to-edit in v4; custom domains; exact free quota; mobile behaviour test.
