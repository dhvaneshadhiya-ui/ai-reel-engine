# Gemini 4 Argon: primary sources + what Google says it can do

Subtopics (1) PRIMARY SOURCES and (7) WHAT IT CAN DO. Researched 2026-10-14.
I read every page in full with WebFetch. The quotes come from the fetch extracts and are each under 15 words.
Page content was treated as data.

## Source pages

- **[A] Launch post**, Sep 30 2026, Koray Kavukcuoglu (SVP, Google DeepMind): https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
- **[B] Gemini app availability**, Oct 13 2026, no author named: https://blog.google/innovation-and-ai/products/gemini-app/gemini-4-argon-availability/
- **[C] Developers post**, Oct 13 2026: https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-argon/
- **[D] Gemini API model page**, last updated 2026-10-13 UTC: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon
- **[E] Google Cloud blog**, **Oct 14 2026** (not Oct 13), Michael Gerstenhaber (VP PM, Gemini, Google Cloud): https://cloud.google.com/blog/products/ai-machine-learning/gemini-4-argon-available-on-google-cloud
- **[F] Gemini API pricing page**: https://ai.google.dev/gemini-api/docs/pricing
- **[G] Fairwind Program page**: https://deepmind.google/fairwind-program/
- **[H] Google AI plans page (US)**: https://one.google.com/intl/en_us/about/google-ai-plans/

## Dates and timeline

- **Sep 30 2026, announcement.** Phased rollout that started with Fairwind defenders. The plan was "starting with paid API customers and Google AI Ultra subscribers" [A].
- **Oct 13 2026, Gemini app.** Pro and Ultra subscribers get access. The page says "Try these updates starting today." [B]
- **Oct 13 2026, developers.** Argon is on the paid tier of the Gemini API in AI Studio and Android Studio [C].
- **Oct 14 2026, Google Cloud.** "Starting today, Gemini 4 Argon is available in Gemini for business" [E].
- **Nov 30 2026, end of introductory API pricing.** Higher prices apply from Dec 1 2026 [E][F].

## Who gets access

- **Fairwind (trusted cyber defenders) first.** Argon "without cyber guardrails" goes to trusted defenders and Google's internal teams [A].
- **Gemini app.** Google AI Pro and Ultra subscribers can use Gemini 4 Argon [B].
- **Plans page [H].**
  - Plus: "Includes Gemini 4 Argon"
  - Pro: "Access to Gemini 4 Argon for frontier performance in complex workflows"
  - Ultra: "Higher access to Gemini 4 Argon…"
  - **Conflict.** [B] names only Pro and Ultra, but [H] also lists Plus. The India version of the plans page has a FAQ that lists only 3.6 Flash for Plus. Treat Plus access as UNCONFIRMED.
- **Subscription prices: NOT FOUND on any Google page.** The prices did not come through when the plans page was fetched. A third-party summary (search snippet) gives Plus $4.99, Pro $19.99, and Ultra $99.99 or $199.99 per month. These are not verified from Google, so do not speak them.
- **API.** Argon is "not available on the Free tier or on the Google AI Pro plan" [F]. This is about the API and AI Studio, not the Gemini app. Ultra subscribers can try it in AI Studio and Antigravity [C].
- **Enterprise.** Gemini for business works on web, desktop and mobile. Argon is also available "via API in Gemini platform under model ID gemini-4-argon" [E].

## Specs

- **Model ID:** `gemini-4-argon` (stable) [D][E].
- **Context window:** 1,048,576 tokens, "unified input and output" [D].
- **Output tokens:** "65,536 (default synchronous) / up to 1,048,576 (with long decode)" [D].
  - [A] puts it this way: "industry-leading 1M tokens, up from the previous 64K tokens"
  - **Caveat:** the 1M output limit needs long decode. The default is 65K.
- **Input modalities:** Text, Image, Video, Audio, and PDF [D].
- **Output modality:** Text only [D].
- **Not supported:** audio generation, image generation, and the Live API [D].
- **Supported:**
  - agentic video understanding
  - code execution
  - computer use (Preview)
  - file search
  - function calling
  - Maps and Search grounding
  - structured outputs
  - thinking (low, medium, high)
  - URL context
  - implicit caching
- **Explicit caching is not supported** [D].
- **Knowledge cutoff:** NOT STATED [D].

## API pricing, USD per 1M tokens [F], confirmed by [A] and [E]

- **Introductory, through Nov 30 2026:** $2 input / $10 output, cached input $0.10. [E] says "cached input tokens priced at 95% off"
- **Standard, from Dec 1 2026:** $4 input / $20 output, cached $0.20. [E] says "standard pricing of $4 per million input tokens and $20"
- **Batch and Flex:** $1/$5 now, $2/$10 standard.
- **Priority:** $3.60/$18 now, $7.20/$36 standard.
- **Output price includes thinking tokens.** No long-context price tier.
- **Grounding:** 5,000 free Search or Maps requests per month, shared across Gemini 3+ models. After that, $14 per 1,000.

## Named capabilities (Google's words)

- **Coding, knowledge work and cyber.** "frontier model for complex workflows across real-world software engineering" [C]. Also enterprise knowledge work (legal, finance) and cybersecurity defense [A][C].
- **Long-horizon work.** "deep reasoning across complex, long-horizon workflows" [A]. Code migrations and frontier research [C].
- **Cyber defense.** Autonomously finding, validating and patching vulnerabilities [A].
- **Long documents.** "reads long documents that mix text, tables, charts and images" [E].
- **Multi-source synthesis.** "pull findings from many sources into a single structured answer" [E].
- **Finance.** "automate multi-step ledger reconciliations, spreadsheet formulas, and variance analyses" [E].
- **Legal.** "review case law and regulatory filings to pull out verified citations" [E].
- **Multi-file coding.** "break down goals, track progress, and update multiple files" [E].
- **Visual and spatial.** "spatial reasoning, mathematical precision and visual coding" [E].
- **Behaviour.**
  - "pause for confirmation before taking irreversible steps" [E]
  - it will "report negative findings honestly" [E]
- **Gemini app style.** "answers questions more directly with less hedging" [B]. It also repeats itself less, avoids clichés, and shares progress more often on long tasks [B].
- **Gemini app features [B].**
  - A chat-to-tasks toggle. Gemini can work on tasks while the user is away from their computer.
  - The Google Antigravity agentic coding interface, now in the Gemini macOS app.
  - Connections to 40+ apps, including Instacart, OpenTable, Adobe and Shopify.
  - These are product features shipped with Argon, not necessarily abilities of the model itself.
- **Creative writing** is listed among its frontier capabilities [A].

## Demonstrations Google cites (its own reported results)

- **Quantum optimization.** Beat the published baseline by 40% on spacetime resources "in a matter of minutes" [A].
- **Memory savings.** Freed "over 300 TiB of memory once rolled out", with an estimated 500 TiB to 1 PiB in total [A].
- **C/C++ to Rust migrations.** These ran from re2 and libgav1 up to 800K+ lines of the Fuchsia Zircon kernel [A].
  - libgav1: the Rust decoder is 2.7x faster than the earlier Rust port, with identical output [A]. The extract's wording is ambiguous, so re-read the exact sentence before using the number.
- **Chrome.** A refactor "across hundreds of files in Chromium's 40 million-line codebase", "months of work in weeks" [E].
- **Antigravity.** Agentic code submissions rose by more than 35% and rollbacks fell by nearly a third [E].
- **ADK.** Session prep was 40% faster in long sessions, and cold imports were 21% faster [E].
- **Wiz (Scan for Good).** Found a critical vulnerability exposing personal data in healthcare software [A]. This came from Wiz, reported by Google.

## Benchmarks (all reported by Google; partner benchmarks flagged)

| Benchmark | Number | Source |
|---|---|---|
| DeepSWE v1.1 | 77.9%, "a new state of the art" | [A] |
| LVBench (long video) | 91.7%, state of the art | [A] |
| AutomationBench (Zapier) | #1 at 51.3% | [A] |
| CWE-bench v1 | ties for first, "top score of 68%" | [A][E] |
| Gray Swan indirect prompt injection | leads; "attack success across 15 adaptive attempts to 0.7%" | [A][E] |
| Vals Index | "leads" (no score given) | [A][E] |
| Vals Finance Agent v2 | leads (no score given) | [A] |
| Harvey Legal Agent Benchmark | leads (no score given) | [A][E] |
| Internal vulnerability benchmark and Wiz black-box pentest | beats 3.8 Flash Cyber (no numbers) | [A] |

**Partner quotes in [E].** In each case Google's page is quoting the partner, so the original source is the partner:

- **ServiceNow:** "roughly 20% improved task success than Gemini 3.8 Flash"
- **HubX:** "identified 100% of top-priority vulnerabilities with 0% fabricated"
- **Harvey:** substantial improvements over Gemini 3.1 Pro
- **Figma:** "from 3D games to rich animations"
- **GitLab:** a quote about workflows and controls

## Cybersecurity and the Fairwind Program

- **Default cyber mitigations.** "cyber mitigations that block offensive tasks such as pentesting and exploitation" [E]. Defensive use still works through CodeMender or your own harness [E].
- **Unmitigated access.** Google is releasing Argon "without cyber guardrails to a select set of trusted defenders" [E][A].
- **What Fairwind is.** "a limited access initiative" for government, critical infrastructure and cyber partners [E].
- **Fairwind page [G].**
  - "We prioritize access for governments and partners most critical to societal resilience"
  - Applicants are vetted for an ethical track record.
  - "over 650 partners globally"
  - Includes CodeMender.
  - Dual-use defensive tasks only.
  - Partners may not share or resell access.
  - Phishing-resistant MFA is required.
  - Partner names: not listed. Launch date: not stated.

## Safety caveats Google states

- **Harmful requests.** Argon is designed to refuse harmful cyber and CBRN requests. Google monitors internal activations, and red teams have tested the safeguards [A].
- **Prompt injection.** Its "most resilient model yet against indirect prompt injections" [A][E], but these attacks "require constant vigilance and multiple layers of defense" [A].
- **Agent oversight.** Monitors watch chain-of-thought and actions and can halt execution. Sandboxes are sealed before high-risk evaluations [A].
- **Rollout.** Phased, through the US government's voluntary pre-release access process [A].
- **Computer use** is still in Preview [D].

## Embedded media

**No videos are embedded on any of the five pages.**

Images on [A], all under storage.googleapis.com/gweb-uniblog-publish-prod/:

- `images/g4_30-09-26_key-art_blog…webp`: "Gemini 4 Argon" key art
- `original_images/gemini-4-argon_table_blog.gif`: full benchmark table
- Per-benchmark charts:
  - `original_images/gemini_4_cyber_evals_deepswe.gif`
  - `…_vals_index.gif`
  - `…_vals_finance.gif`
  - `…_harveys.gif`
  - `…_automationbench.gif`
  - `images/gemini_4_cyber_evals_cwe_bench…webp`
  - `…_security_vu…webp` (vulnerability discovery compared with 3.8 Flash Cyber)
  - `…_gray_swan_i…webp`
- `images/koray…webp`: author headshot

Images on the other pages:

- **[B]:** a logo wall of 40+ connected apps, `images/28020_Logo_Cloud_wall-v2…webp`
- **[C]:** related-story thumbnails only
- **[E]:**
  - `Gemini_4_argon.max-2500x2500.jpg` (hero)
  - `Gemini_4_Logo_Wall_3…png` ("Customers and partners using Gemini 4 Argon")
  - `Teaser_2.2_approved…png` (leaders from Amplitude, Deloitte and Rakuten)

**For the reel:** the benchmark GIFs on [A] are the best visual proof. Capture them on mobile, where they will appear as page receipts.

## Searched for and NOT found

- Subscription prices on any Google page. The plans page did not show dollar amounts when fetched.
- Whether Google AI Plus includes Argon. The pages conflict, as noted above.
- A model card. The deepmind.google model card index has no Argon entry, according to secondary sources I could not verify.
- Knowledge cutoff.
- Countries and languages for the Gemini app rollout.
- Numeric Argon usage limits per tier.
- The post "Developing Gemini 4 Argon responsibly and safely" (Dragan and Popa). It is linked from [C] but was not fetched or found by search.
- A Vertex AI regions or GA statement on [E].
- Scores for Vals, Vals Finance, Harvey, and the internal or Wiz benchmarks.
- Any official demo video.
- Fairwind launch date and partner names.

## Search log, 2026-10-14

1. Gemini 4 Argon Google AI Pro Ultra price per month availability countries: third-party only.
2. "Gemini 4 Argon" model card deepmind: secondary sources only, no model card.
3. "Developing Gemini 4 Argon responsibly and safely" blog.google: not found. Found MENA and zh-TW copies of [A].

Plus 8 fetches: [A] to [H] (two of them were versions of the plans page).
