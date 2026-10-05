# DeepSite: price, limits, login, licence, complaints (research subagent, 2026-10-05)

## Where it lives
- huggingface.co/spaces/enzostvs/deepsite -> 302 huggingface.co/deepsite -> 302 https://deepsite.hf.co/ ("DeepSite | Build with AI", calls itself v4)
- deepsite.hf.co: "Push your changes and watch them go live instantly." "Free Hosting", "global CDN"; DeepSeek, MiniMax, Kimi. No price/licence/limits stated.
- 2026-10-05 own mobile capture: modal "DeepSite is moving to Hugging Face Chat" (see findings_visuals / _sources).

## Free? Account? PRO?
- Login required: https://huggingface.co/spaces/enzostvs/deepsite/raw/main/app/api/ask/route.ts `if (!session) ... "Unauthorized" ... 401`; inference billed to user's own token.
- Same route sets `showProMessage: true` on "exceeded your monthly included credits".
- https://huggingface.co/docs/inference-providers/pricing Free users "$0.10, subject to change"; PRO "$2.00"
- https://huggingface.co/pricing PRO "$9/month", "20× included inference credits"
- Discussion #503 (Oct 2025): "Log In to use DeepSite for free"; "It's happening again after running prompt 5 times." enzostvs: "check your inference providers billing"
- "No account needed" = listicles only, contradicted by code. Do not use.

## Rate limits
- No app limiter; the wallet is the limit. #563 (Feb 2026) 429s traced to billing $1.83/$2.00.

## Licence
- README front-matter license: MIT; tagline "Generate any application by Vibe Coding it". No LICENSE file. Next.js on Docker; self-host needs own HF OAuth app.
- Repo last commits 8-9 months old; live v4 may differ. Say "open-source code on Hugging Face".

## Publishing / download
- projects/route.ts: createRepo "sdk: static", injects DeepSite badge, public by default; *.static.hf.space
- #466 download: maintainer "download your space on your profile"; user "there is no option to download??" unresolved.
- #505 second HTML page broke project opening (later fixed).

## Independent evidence
- https://aiengineerguide.com/til/huggingface-deepsite/ (Ashik Nesin, 2025-11-29): weather app; "the AI vibe but it's a good start"
- #563 (Feb 2026): "More recent versions are utter garbage"; edits delete sections; "not usable for client work anymore"; enzostvs on old builds: "unfortunately not really at the moment"
- #562 (Feb-Mar 2026): 404s, upload/save failures. #503: login loops, save failures.
- Discussions incl. "can this run on mobile?" #568. Pinned "DeepSite v3 is out" #427.
- "16,000+ likes" = listicles only, unverified.
- Framing: first draft really does take minutes; iterating to a finished site is where it breaks.

## Not found
Official free generation count; DeepSite pricing page; Reddit hands-on; GitHub repo; v3 announcement text; proof live v4 = MIT repo; current like count; download test.
