# Research — chatgpt-creator-prompts

Claims ledger + search log. Findings: research/findings_*.md (four parallel agents,
2026-09-24), plan in research/plan.md, visuals in research/visuals.md.

## CLAIMS

- CLAIM: In Sprout Social's Q1 2026 Pulse survey (2,250 social users, US/UK/Australia, Feb 5-9 2026), 50% of Gen Z said they have unfollowed, muted or blocked a brand or creator because their content felt like AI slop.
  TIER: official
  SPOKEN: "You get slop, and half of Gen Z say they've unfollowed someone over it."
  SURPRISE: 60
  SRC: https://media.sproutsocial.com/uploads/2026/03/Sprout-Social-Q1-2026-Pulse-Survey-Analysis.pdf
  VIA: Sprout Social's own survey ("Gen Z was also the most likely to unfollow, mute or block accounts because their content felt like AI slop, with 50% saying they have done so.")

- CLAIM: OpenAI's own published marketing prompts ask the user to supply their own material in brackets, e.g. "Use this background for context: [paste details]".
  TIER: official
  SPOKEN: "Even OpenAI's own prompts leave a gap that says paste details."
  SURPRISE: 55
  SRC: https://academy.openai.com/public/clubs/work-users-ynjqu/resources/use-cases-marketing
  VIA: OpenAI Academy "ChatGPT for marketing" prompt pack, "Create a social post series" row

- CLAIM: ChatGPT Projects gather files and instructions in one place, project instructions override global custom instructions, and Free accounts get Projects with up to 5 files per project.
  TIER: official
  SPOKEN: "make a Project, drop in your three best scripts, and tell it to write like those. Free accounts get Projects too."
  SURPRISE: 55
  SRC: https://academy.openai.com/public/clubs/work-users-ynjqu/resources/projects
  VIA: OpenAI Academy ("Projects in ChatGPT let you organize work into dedicated spaces where you can gather context, files, and instructions.")
  SRC: https://help.openai.com/en/articles/8555545-file-uploads-faq
  VIA: OpenAI help centre ("Free: Up to 5 files per project")
  SRC: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
  VIA: OpenAI help centre ("Project instructions apply only within that project and override your global custom instructions.")

- CLAIM: Pasting your own past scripts/posts so the output matches your voice is a technique recommended by independent creator publishers.
  TIER: multi
  SPOKEN: "drop in your three best scripts, and tell it to write like those"
  SURPRISE: 40
  SRC: https://zapier.com/blog/write-video-scripts-with-chatgpt/
  VIA: Zapier (author pastes "a script from a recent video")
  SRC: https://vidiq.com/blog/post/chatgpt-youtube-vidiq-ai-coach/
  VIA: vidIQ ("A title suggestion without knowing your niche, audience age, posting cadence, and the videos that already worked is just brainstorming.")

- CLAIM: Descript's creator prompt for ideas is "What would [audience] like to know about [topic]?" and its guidance is to qualify the audience: "A hook on the wrong audience is attention bait."
  TIER: multi
  SPOKEN: "ask what your audience wants to know about your topic, and name them"
  SURPRISE: 35
  SRC: https://www.descript.com/blog/article/100-chatgpt-prompts-for-creators-speed-up-your-workflow-with-ai
  VIA: Descript blog, 2026-07-29 (both lines on the page, captured mobile; the audience prompt sits in its podcast-research list, used here as a general ideas prompt)
  SRC: https://sproutsocial.com/insights/ai-prompt/
  VIA: Sprout Social ("The more guidance you give upfront in a prompt, the stronger and more reliable the output will be.") — naming the audience recurs on 7 of 9 publisher pages

- CLAIM: Hook prompts built on your own transcript that ask for several variations each testing a different hook or tone: Descript ("Write [number] hooks for this video: [paste video transcript]") and OpenAI's own pack ("Each version should test a different hook or tone").
  TIER: multi
  SPOKEN: "paste your transcript and ask for five hooks, each in a different tone."
  SURPRISE: 45
  SRC: https://www.descript.com/blog/article/100-chatgpt-prompts-for-creators-speed-up-your-workflow-with-ai
  VIA: Descript blog
  SRC: https://academy.openai.com/public/clubs/work-users-ynjqu/resources/use-cases-marketing
  VIA: OpenAI Academy ("Create 5 ad copy variations ... Each version should test a different hook or tone.")

- CLAIM: A script prompt that sets length and asks for the output as a two-column table, narration left, visuals right (Descript); OpenAI's own 60-second script prompt also asks for "suggested visuals or animations".
  TIER: multi
  SPOKEN: "Ask for a thirty-second script with narration left and visuals right, so you get a shot list."
  SURPRISE: 60
  SRC: https://www.descript.com/blog/article/100-chatgpt-prompts-for-creators-speed-up-your-workflow-with-ai
  VIA: Descript ("Output the script in a 2-column table with the narration on the left and the associated visuals on the right." — template prompt, length as [number] [minutes/words])
  SRC: https://academy.openai.com/public/clubs/work-users-ynjqu/resources/use-cases-marketing
  VIA: OpenAI Academy ("Draft a script for a 60-second explainer video ... with suggested visuals or animations.")

- CLAIM: Sprout Social's repurposing prompt: "Identify three self-contained pull quotes from this webinar transcript that would work as standalone clips for a short social video." OpenAI documents no way for ChatGPT to watch a YouTube link, so the transcript is the input.
  TIER: multi
  SPOKEN: "paste a long video's transcript, not the link, and ask for three moments that stand alone as clips."
  SURPRISE: 50
  SRC: https://sproutsocial.com/insights/ai-prompt/
  VIA: Sprout Social (prompt 13, captured mobile)
  SRC: https://www.descript.com/blog/article/100-chatgpt-prompts-for-creators-speed-up-your-workflow-with-ai
  VIA: Descript ("[Paste transcript] Write a [Twitter thread/social carousel] based on key insights") — transcript-as-input recurs at S, D, Z, Ho
  SRC: https://help.openai.com/en/articles/8555545-file-uploads-faq
  VIA: OpenAI help centre — lists supported uploads (documents, CSV, images); no YouTube-link reading documented

- CLAIM: YouTube's monetization policy (clarified July 15, 2025, "inauthentic content") makes ineligible "AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective".
  TIER: official
  SPOKEN: "YouTube won't pay for mass-produced AI videos without your own insight."
  SURPRISE: 50
  SRC: https://support.google.com/youtube/answer/1311392?hl=en
  VIA: YouTube Help, YPP policies
  SRC: https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/
  VIA: Social Media Today coverage of the same update (repeats YouTube)

## FEATURES + HOW TO USE

ChatGPT (the product the prompts run in):
- Projects (files + instructions, Free: 5 files/project) — USED (prompt 1).
- Custom instructions (Free 1,500 chars) — CUT: Projects carry the same idea with files; one feature per beat.
- Saved context / chat history — CUT: "Limited" on Free, wording varies by plan; not needed.
- File uploads (Free 3/day) — CUT from speech; noted in NOT CLAIMED. Pasting a transcript as text avoids the cap.
- Canvas — CUT: retired May 28 2026 (release notes).
- Voice, Tasks, GPTs, apps/plugins — CUT: not part of the creator prompt workflow; GPTs being retired.
Prompt types (publisher recurrence): ideas 5, captions 5, repurpose 5, script-to-spec 4, hooks 3-4, titles 3 — ideas/hooks/script/repurpose USED; captions and titles CUT for time (listed as a cut in structure.md).

## NOT CLAIMED

- That ChatGPT CANNOT read a YouTube link. OpenAI documents no such feature; the script gives advice ("paste the transcript, not the link"), not a capability claim.
- That generic AI posts get less reach. No primary measured study; blog figures ("20-45% less reach", "12% penalty") untraced. The Sprout number is self-reported behaviour and is spoken as "say".
- That YouTube "bans AI". It is a monetization clarification about mass-produced templated content.
- "300+ official prompts": unverified on an OpenAI page.
- Adobe's 86% / 85% creator figures: primary but cut for time.
- That these prompts "go viral" or guarantee views. No publisher measures outcomes.
- The Free upload cap (3 files/day): true (help 8555545) but not needed; three scripts in a Project could hit it on one day, so the script doesn't promise "instantly".
- "Save this for your next script" is a CTA, not a claim.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-24  "OpenAI Academy prompt pack marketing ChatGPT prompts"  (public marketing + any-role packs; [paste details] slot; 60-second script prompt)
- 2026-09-24  "ChatGPT Projects free plan files per project help center"  (Free: 5 files/project; instructions override global)
- 2026-09-24  "ChatGPT release notes 2026 default model free Canvas"  (GPT-5.6 Luna default on Free; Canvas retired May 28)
- 2026-09-24  "YouTube inauthentic content policy July 2025 AI generic templates"  (YPP page wording)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-24  "ChatGPT prompts for content creators hooks scripts repurpose Descript Sprout HubSpot"  (9 publisher pages; recurrence table; no page measures outcomes)
- 2026-09-24  "write video scripts with ChatGPT paste past script voice"  (Zapier, vidIQ: feed it your own past work)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-24  "AI slop survey 2026 unfollow creators"  (Sprout Q1 2026 Pulse: 56% see slop often; Gen Z 50% unfollowed/muted/blocked)
- 2026-09-24  "Adobe creators toolkit report 2026 AI"  (85% say the final creative decision should remain theirs)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-24  "AI generated posts reach engagement penalty study"  (only untraced blog figures; nothing primary -> reach not claimed)
- 2026-09-24  "ChatGPT watch YouTube video link analyze"  (no OpenAI page documents it; third-party only -> advice phrased as advice)
- 2026-09-24  "YouTube demonetize AI videos July 2025 clarification not ban"  (it is a clarification of an existing rule -> spoken as "won't pay for mass-produced", not "bans AI")

INDEPENDENT-CHECK: 2026-09-24 searched independent creator publishers (Descript, Sprout, HubSpot, Zapier, vidIQ, Riverside, Hootsuite, Buffer) for which prompts recur and whether any measured results; found strong recurrence for ideas/hooks/script/repurpose and the audience + own-material advice, and NO measured outcome anywhere — so the reel never promises results. Searched for studies contradicting the AI-slop framing: only self-report surveys exist, spoken as "say".
