# Research — claude-memory-everywhere

Claims ledger + search log. Tiers: official / multi / single / disputed.
Every claim here is `official` — the primary source is Anthropic's own product
announcement, and two independent outlets corroborate. Nothing in this reel
rests on a leak, a forecast or an anonymous account, so nothing is spoken
hedged.

## CLAIMS

- CLAIM: Claude's memory is now visible to the user as a readable, editable, deletable list
  TIER: official
  SPOKEN: "Claude keeps a file on you, and now it shows you what's in it."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  SRC: https://techcrunch.com/2026/08/25/claude-cowork-finally-remembers-what-you-told-the-app-in-chat/
  VIA: Anthropic product announcement, 2026-08-25
  VIA: TechCrunch reporting on the same announcement

- CLAIM: the announcement is dated August 25, 2026, and users can edit or delete any saved memory
  TIER: official
  SPOKEN: "And as of August 25, you can change it, or throw it out."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  VIA: dateline on Anthropic's own post ("Date — August 25, 2026")

- CLAIM: some categories are refused outright, even with sensitive topics enabled
  TIER: official
  SPOKEN: "But here's the part that matters most: some of it Claude refuses to write down."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  VIA: Anthropic: "there are some topics that Claude does not store even when you have sensitive topics in memory turned on"

- CLAIM: everything Claude remembers is stored as short files filed under Topics
  TIER: official
  SPOKEN: "Because everything it knows about you is now a text file under a topic"
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  SRC: https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
  VIA: Anthropic: "Everything Claude remembers is in a list of files under Topics in Memory settings"

- CLAIM: the topic names Half Marathon Training, Client Pitch and Childcare Schedule are Anthropic's own examples
  TIER: official
  SPOKEN: "Half Marathon Training, Client Pitch, Childcare Schedule."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  VIA: read directly off the product screenshots embedded in that post (saved to _sources/)

- CLAIM: correcting one file propagates to every later conversation
  TIER: official
  SPOKEN: "Correct your company's old name there, and every chat after gets it right."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  VIA: Anthropic: "correct your company's old name in one file and every conversation from then on gets it right"

- CLAIM: chat and Cowork now share one memory, in both directions
  TIER: official
  SPOKEN: "And that memory stopped staying put — what Claude learns in chat, its cloud agent Cowork already has, and back again."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  SRC: https://www.engadget.com/2243753/claude-memory-now-works-across-both-chats-and-cowork-sessions/
  VIA: Anthropic: "When Cowork runs a task in the cloud, what Claude remembers from your chats is there, and vice versa"
  VIA: Engadget reporting on the same announcement


- CLAIM: health, race, ethnicity, religious beliefs, politics and gender identity are excluded from memory by default
  TIER: official
  SPOKEN: "Now, the subjects it leaves alone — health, race, religion, politics, gender identity — off by default."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  VIA: Anthropic: "By default, Claude does not store topics related to personal or sensitive subject matter, like your health, race, ethnicity, religious beliefs, politics, gender identity"

- CLAIM: an opt-in toggle exists, and each sensitive save shows the user a notice
  TIER: official
  SPOKEN: "But there's a switch if you want them in, and a notice each time it saves one."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  VIA: Anthropic: "With the setting turned on, each time Claude saves something on one of these topics to memory, you'll see a notice"

- CLAIM: SSNs, government ID numbers, criminal history and immigration status are never stored, and Claude says when it refused
  TIER: official
  SPOKEN: "Social Security numbers, government IDs, criminal history, immigration status."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  SRC: https://www.engadget.com/2243753/claude-memory-now-works-across-both-chats-and-cowork-sessions/
  VIA: Anthropic: "sensitive identification numbers (SSN, government ID numbers, etc), criminal history, immigration status... Claude will inform you when it's unable to update memory"
  VIA: Engadget reporting on the same announcement

- CLAIM: Claude tells the user when it has refused to save something
  TIER: official
  SPOKEN: "Those never get saved either way, and Claude tells you when it refused."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  VIA: Anthropic: "Claude will inform you when it's unable to update memory to include any of this information"

- CLAIM: memory is on by default on Free, Pro and Max; Team and Enterprise admins control it
  TIER: official
  SPOKEN: "It's all on by default on Free, Pro and Max. On Team and Enterprise, your admin decides."
  SRC: https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
  SRC: https://techcrunch.com/2026/08/25/claude-cowork-finally-remembers-what-you-told-the-app-in-chat/
  VIA: Anthropic: "Memory is on by default on Free, Pro and Max plans across web, desktop, and mobile... For Team and Enterprise, admins control availability"
  VIA: TechCrunch reporting on the same announcement

## SEARCHED

- 2026-08-26  fetched https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it  (primary text + the three embedded product screenshots; established date, plan availability, refused-category list)
- 2026-08-26  "Claude memory works everywhere you decide what's in it Anthropic announcement August 2026"  (found the independent coverage set: TechCrunch, Engadget, 9to5Mac, SiliconANGLE)
- 2026-08-26  fetched TechCrunch 2026-08-25  (independent confirmation of live-write behaviour and plan availability)
- 2026-08-26  fetched Engadget 2026-08-25  (independent confirmation of non-retroactive toggle and never-stored list)
- 2026-08-26  "Claude import memory from other AI providers"  (SETTLED A CUT: the Start-import control visible in Anthropic's screenshot is a MARCH 2026 feature — MacRumors 2026-03-02, Fast Company — NOT part of this announcement. Excluded from the script so it cannot read as new.)
- 2026-08-26  searched support.claude.com for the memory help article  (official corroboration of the Topics read/edit/delete mechanics)
