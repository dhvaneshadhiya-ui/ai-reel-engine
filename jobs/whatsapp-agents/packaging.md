# whatsapp-agents — packaging

Validated with `python3 tools/packaging_check.py whatsapp-agents`.

Instagram's hashtag maximum is **5** (past that Instagram ignores all of them,
official since Aug 2025); YouTube's hard cap is 15 but the recommended band is
also **3-5**. Every field below is pasted VERBATIM into the place it names.
Instagram has no HASHTAGS field: its tags sit at the END OF THE
FIRST COMMENT, because that is where they are posted. YouTube
keeps one, because YouTube reads them out of the description.

**Accuracy note for whoever posts this, and it is the whole story:** the reel
does NOT say ordinary WhatsApp chats lose encryption, and neither may the
caption. WABetaInfo's own paragraph says personal messages and calls "remain
fully end-to-end encrypted". The claim is narrow and it must stay narrow: a
NEW kind of chat, with a third-party agent, is not end-to-end encrypted. A
caption that blurs that is a bigger problem than a caption that underperforms.

## youtube

TITLE: WhatsApp Is Testing AI Agent Chats. Not Encrypted.
CAPTION: WhatsApp is rolling out chats with third-party AI agents. Up to five per account, each in its own chat with a name and profile photo you choose, set up from a new Agents section in settings: you generate an API key and paste it into whatever is running the agent. WABetaInfo found it in the WhatsApp beta for Android. Those chats run through a Meta service on the developer's behalf, which is why WhatsApp does not call them end-to-end encrypted — the developer can read what you send. Your personal chats are untouched and stay fully encrypted, and an agent only ever sees its own conversation, not your contacts or media. The timing is the interesting part: in October 2025 WhatsApp changed its terms to bar general-purpose chatbots, by 15 January 2026 ChatGPT and Perplexity had stopped working there, and the EU, Italy and Brazil opened antitrust probes over it. Eight months later there is a door back in, built by Meta. Nobody has said those two things are connected. Sources: WABetaInfo, 9to5Mac, TechCrunch.
HASHTAGS: #WhatsApp #AIAgents #Meta #Privacy #Encryption
FIRST COMMENT: Would you actually put an outside AI in your WhatsApp, knowing that one chat is not end-to-end encrypted?
ALT TEXT: A presenter explains that WhatsApp is testing chats with third-party AI agents, alongside WABetaInfo's article stating those chats are not end-to-end encrypted, WhatsApp's own "Secure by design" page, rendered mockups of the new Agents settings pane and a chat list, and a TechCrunch report on the 2025 chatbot ban and the antitrust probes that followed.

## instagram

CAPTION: WhatsApp is adding chats with third-party AI agents, and it says those agent chats are not end-to-end encrypted. Those are their words, found by WABetaInfo in the Android beta. There is a new Agents section in settings: generate an API key, paste it into whatever is running an outside AI, and it gets its own chat with a name and photo you pick. Up to five. So it sits in your list looking like everybody else — except that one runs through a Meta service on the developer's behalf, so the developer can read what you send. The fence is real, though: an agent sees its own chat and nothing else, and your personal chats stay encrypted exactly as before. Last October WhatsApp barred general-purpose chatbots. By January, ChatGPT and Perplexity had stopped working there, and the EU, Italy and Brazil opened antitrust probes. Eight months later, there is a door back in, built by Meta. Nobody has said those two are connected.
FIRST COMMENT: Would you put an outside AI in your WhatsApp knowing that chat is not end-to-end encrypted? #WhatsApp #AIAgents #Meta #Privacy #Encryption
ALT TEXT: A presenter explains WhatsApp's beta feature for chatting with third-party AI agents, with WABetaInfo's article stating those chats are not end-to-end encrypted, WhatsApp's own "Secure by design" page, rendered mockups of the Agents settings pane and a chat list, and TechCrunch's report on the 2025 chatbot ban and the antitrust probes.

---

Paste-ready YouTube description, line-broken. Same copy as CAPTION above; the
checker only reads the single-line version, humans should paste this one.

  WABetaInfo found a new Agents section in the WhatsApp beta for Android.

  How it works: you generate an API key, paste it into whatever is running
  your agent, and it gets its own chat — with a name and a profile photo
  you choose. Up to five agents per account.

  The catch, in WhatsApp's own words: chats with agents are NOT considered
  end-to-end encrypted. They are handled by a Meta service on the agent
  developer's behalf, and that developer can access the messages.

  What is NOT affected:
  • Your personal messages and calls stay fully end-to-end encrypted
  • An agent can only read its own chat — not your other conversations,
    not your contacts, not your media

  Why the timing is interesting:
  • Oct 2025 — WhatsApp changes its terms to bar general-purpose chatbots
  • 15 Jan 2026 — the rules take effect; OpenAI, Perplexity and Microsoft
    say their WhatsApp bots will stop working, and regulators in the EU,
    Italy and Brazil open antitrust probes
  • Sep 2026 — third-party agents appear in the beta

  Nobody has said those two things are connected. Meta has not announced
  the feature at all, and it is currently limited to a small number of
  Android beta testers in select countries.

  Sources: WABetaInfo, 9to5Mac, TechCrunch.

Notes for posting

  No in-video CTA and no comment-keyword — this is a straight news reel.
  The engagement question lives in the FIRST COMMENT.

  Cover: out/thumbnails/whatsapp-agents-vertical.png, made 2026-09-11 when
  covers became a standard step for every reel (the choice is recorded in
  jobs/whatsapp-agents/cover.json). Instagram: open the reel, then More,
  Edit, Edit cover, Add from camera roll, and compare it with the -grid.png.

  Do not let a shorter edit of this caption drop the words "with agents".
  "WhatsApp chats are not encrypted" is false and is the single most
  likely way this gets miswritten.

  THE FIRST DRAFT OF THIS FILE BROKE ITS OWN RULE (fixed 2026-09-08, on the
  user's challenge). The YouTube title read "WhatsApp's New Chat Is Not
  End-to-End Encrypted" and the Instagram caption opened "WhatsApp is
  building a chat that WhatsApp itself says is not end-to-end encrypted" —
  neither contained the words "AI agents". Those two strings are the only
  text most people ever read: the title in search and suggested, and the
  first caption line before "more". Both therefore delivered exactly the
  false generalisation the paragraph above forbids, and neither told anyone
  what the video is about. The subject now comes first in both, and the
  encryption angle second, where it is a consequence instead of a headline.
