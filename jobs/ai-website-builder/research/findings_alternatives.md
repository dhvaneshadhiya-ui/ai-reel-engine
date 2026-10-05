# Findings: alternatives to DeepSite and how it differs
All fetches 2026-10-05 (research subagent). Verbatim quotes <15 words. Gaps stated; non-vendor figures marked VIA.

## Bolt.new
- Free: SRC https://bolt.new/pricing "300,000 token daily limit" / "1 million token monthly limit"
- Pro: "$25 per month billed monthly" / "Start at 10M tokens per month"
## Lovable
- Free: SRC https://lovable.dev/pricing "5 build credits (up to 30 a month)"; docs.lovable.dev "5 per day, up to 30 per month"
- Pro $25/100 credits: VIA superblocks.com, uibakery.io (vendor table did not render — NOT first-party)
## v0 by Vercel
- Free: SRC https://v0.app/pricing "7 message/day limit"; Plus "$30/user/month"
## Google Stitch — no first-party limits; listicle figures conflict. Do not speak.
## Google AI Studio Build mode — SRC https://ai.google.dev/gemini-api/docs/aistudio-build-mode "Firebase Firestore and Authentication"; no free quota number.
## Replit — Starter "daily credits for Agent usage, up to a monthly cap" (no number); Core "$20 / month"
## Cursor — Hobby "Limited Agent requests"; Pro "$20 / mo."; a code editor, not a site builder.
## DeepSite
- SRC https://huggingface.co/spaces/enzostvs/deepsite/blob/main/README.md: license MIT, sdk docker; models DeepSeek-V3-0324, DeepSeek-V3.2, Qwen3-Coder-30B-A3B-Instruct, Kimi-K2-Instruct-0905, GLM-4.7, MiniMax-M2.1
- SRC https://deepsite.hf.co/ "Powered by cutting-edge open source AI models"; "Free Hosting"; "Multi Pages"
- SRC https://huggingface.co/docs/inference-providers/pricing Free Users "$0.10, subject to change"; PRO $2.00/month
- VIA duplicate Space eddyencode/deepsitev3 snippet: login + PRO upgrade prompt at limit (unverified)
- github.com/huggingface/deepsite 404; no self-host instructions in README.
## Differentiator: only MIT open-source tool in the set, open-weight models, duplicable Space. Free = small allowance, never "unlimited".
## Lacks: no evidence of backend/DB/auth generation — say "front-end sites", not "can't do backend".
## Not found: Lovable Pro first-party; Replit/Cursor free numbers; Stitch official limits; AI Studio quota; DeepSite per-user generation count; official GitHub repo.
