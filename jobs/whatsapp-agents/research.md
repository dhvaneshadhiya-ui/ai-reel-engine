# Research — whatsapp-agents

Claims ledger + search log.

## CLAIMS

- CLAIM: WhatsApp does not consider chats with third-party agents end-to-end
  encrypted, because they are handled by a Meta service on the agent
  developer's behalf.
  TIER: single
  SPOKEN: "WhatsApp is building a chat that WhatsApp itself says is not end-to-end encrypted."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo's teardown, quoting WhatsApp's own in-app wording

- CLAIM: The feature is present in WhatsApp beta for Android 2.26.35.3 and has
  not been announced by Meta.
  TIER: single
  SPOKEN: "WABetaInfo found them in the Android beta."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo's own teardown of the beta build

- CLAIM: Agents are configured from a new Agents section in WhatsApp settings,
  and connected by generating an API key in WhatsApp and pasting it into the
  platform hosting the agent.
  TIER: single
  SPOKEN: "You generate an API key and paste it into whatever's running the AI."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo
  SRC: https://www.pcquest.com/os-apps/whatsapp-third-party-ai-agents-android-beta-12498558
  VIA: WABetaInfo

- CLAIM: The account limit is five agents.
  TIER: single
  SPOKEN: "Up to five."
  SRC: https://9to5mac.com/2026/09/07/whatsapp-will-soon-let-users-chat-with-up-to-five-third-party-ai-agents/
  VIA: WABetaInfo
  SRC: https://www.pcquest.com/os-apps/whatsapp-third-party-ai-agents-android-beta-12498558
  VIA: WABetaInfo

- CLAIM: Each agent is given a name and profile photo by the user, and appears
  in the chat list like any other chat.
  TIER: single
  SPOKEN: "You name each one and give it a photo."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo
  SRC: https://9to5mac.com/2026/09/07/whatsapp-will-soon-let-users-chat-with-up-to-five-third-party-ai-agents/
  VIA: WABetaInfo

- CLAIM: The agent developer can access the messages sent in that chat, as part
  of running the service.
  TIER: single
  SPOKEN: "so the developer can read what you send"
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo, quoting WhatsApp's own in-app wording

- CLAIM: An agent can only read what is shared in its own chat, and cannot
  access other conversations, contacts or media.
  TIER: single
  SPOKEN: "Not your contacts, not your media, not one other conversation."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo, quoting WhatsApp's own in-app wording

- CLAIM: Personal messages and calls between people on WhatsApp remain fully
  end-to-end encrypted and are not affected by this feature.
  TIER: single
  SPOKEN: "Your personal chats stay encrypted exactly as before."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo, quoting WhatsApp's own in-app wording

- CLAIM: In October 2025 WhatsApp changed its Business API terms to bar
  general-purpose chatbots; the rules took effect 15 January 2026 and OpenAI,
  Perplexity and Microsoft said their WhatsApp bots would stop working.
  TIER: official
  SPOKEN: "Last October it barred general-purpose chatbots."
  SRC: https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform
  VIA: TechCrunch's own reporting plus a Meta spokesperson statement; the
       15 January 2026 update is TechCrunch's own

- CLAIM: Regulators in the EU, Italy and Brazil opened antitrust probes against
  Meta in relation to those rules.
  TIER: official
  SPOKEN: "the EU, Italy and Brazil opened antitrust probes"
  SRC: https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform
  VIA: TechCrunch update dated 15 January 2026

- CLAIM: The feature is limited to a small number of Android beta users in
  select countries.
  TIER: single
  SPOKEN: "It's still a handful of testers in a few countries."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: WABetaInfo

- CLAIM: ABSENCE. Nobody has publicly stated a link between the 2025 chatbot
  ban and this agent feature. Meta has not announced the agent feature at all,
  so it has offered no rationale for it, and none of the coverage of the beta
  finding connects the two. This is why the script asserts no causation: it
  lays the two dated facts side by side and says out loud that the link is
  unestablished.
  TIER: single
  SPOKEN: "Nobody has said those two are connected."
  SRC: https://wabetainfo.com/whatsapp-is-rolling-out-chats-with-third-party-agents/
  VIA: LOOKED AND FOUND NOTHING. 2026-09-08, searched "WhatsApp agents
       feature Meta official announcement blog 'agents' statement confirm"
       for any Meta statement on the agent feature: no announcement, no
       statement, no stated reason exists. The same search surfaced Meta's
       separate Business Agent launch of 3 June 2026, which is a different
       product and makes no reference to the ban either. The five outlets
       covering the beta finding (9to5Mac, PCQuest, MediaNama, Business
       Standard, Cryptopolitan) all trace to WABetaInfo and none of them
       draws the connection. The absence is therefore an absence of public
       statement, which is exactly and only what the line claims.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-08  "WhatsApp third-party AI agents API key not end-to-end encrypted
  September 2026"  (settled the five-agent cap, the API-key pairing flow, the
  beta build number 2.26.35.3 and the E2EE position; five outlets, all tracing
  to WABetaInfo)
- 2026-09-08  "WhatsApp Business API general-purpose AI chatbots ban January 15
  2026 policy"  (settled the ban, its effective date and the named bots)
- 2026-09-08  fetched the TechCrunch ban article directly  (settled Meta's own
  stated reason, the four named bots, and the 15 Jan 2026 update carrying the
  EU / Italy / Brazil antitrust probes)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is
###    not the vendor
- 2026-09-08  "WhatsApp agents feature Meta official announcement blog"
  (found NO hands-on. The feature is an APK teardown of a beta build gated to a
  very limited set of testers, so no independent party has used it. It did
  settle a separate fact: Meta shipped its OWN Meta Business Agent globally on
  3 June 2026 — relevant context, deliberately cut from the script, see
  structure.md.)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-08  "WhatsApp third-party agents reaction privacy criticism 'not
  end-to-end encrypted' users backlash"  (no user reaction to THIS feature
  exists yet — nobody has it. What the search did surface is the live
  California class action alleging Meta staff and contractors could read
  WhatsApp messages, which Meta calls "categorically false and absurd". Left
  out of the script: it is a different, contested allegation, and stapling it
  to a sourced beta finding would be the framework's certainty-vs-evidence
  failure.)

### 4. WHAT WOULD CONTRADICT THIS
- 2026-09-08  "WhatsApp FAQ business messages 'not end-to-end encrypted' Meta
  hosted business chats label warning in chat"  (this is the search that
  changed the script. WhatsApp ALREADY says Meta-hosted business chats are not
  covered by end-to-end encryption, so agent chats extend an existing carve-out
  rather than breaching a universal promise. The script therefore does not say
  or imply that ordinary WhatsApp chats are affected — WABetaInfo's own
  paragraph says personal messages and calls "remain fully end-to-end
  encrypted", and the script says so out loud.)

INDEPENDENT-CHECK: 2026-09-08 searched for hands-on testing, user reaction and
  an official Meta statement on the agent feature — found none of the three.
  Meta has not announced it; no one outside the limited beta can use it. Every
  outlet covering it traces to a single origin, WABetaInfo's teardown, so the
  feature claims are SINGLE tier and are spoken hedged throughout ("in the
  beta", "WhatsApp is building", "if it ships"). The one part of the story that
  is NOT single-sourced is the 2025 ban and the antitrust probes, which are
  TechCrunch's own reporting — and that is the half the reel leans its
  conclusion on.
