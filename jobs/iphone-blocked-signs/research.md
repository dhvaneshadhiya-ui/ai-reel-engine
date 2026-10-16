# Research — iphone-blocked-signs

Claims ledger + search log.

## CLAIMS

- CLAIM: Apple does not notify a person when they are blocked; blocking is
  designed to give the blocked person no signal.
  TIER: official
  SPOKEN: "Apple's support page is blunt: you're never notified"
  SURPRISE: 45
  SRC: https://support.apple.com/en-us/111104
  VIA: Apple Support, "Block phone numbers, contacts, and emails on your iPhone or iPad" (29 May 2026): "the contact won't get a notification that the call or message was blocked"
  SRC: https://discussions.apple.com/thread/256225798
  VIA: Apple Community reply, Jan 2026: no indication is given, by design

- CLAIM: Messages from a blocked contact are not delivered to the person who
  blocked them.
  TIER: official
  SPOKEN: "your texts just stop reaching them"
  SURPRISE: 30
  SRC: https://support.apple.com/en-us/111104
  VIA: Apple Support: "Messages that are sent or received won't be delivered."
  SRC: https://www.igeeksblog.com/how-to-know-if-someone-has-blocked-you-on-imessage/
  VIA: own testing / Apple doc

- CLAIM: Since iOS 16.5 the "Delivered" label can appear under a text to
  someone who has blocked you, so it proves nothing either way. Older tests
  (Macworld 2020) saw no "Delivered"; the newer behaviour is reported by
  several outlets and Apple Community users, not documented by Apple.
  TIER: multi
  SPOKEN: "Since iOS 16.5, guides report it can show up even when you're blocked"
  SURPRISE: 85
  SRC: https://iphonelife.com/node/274079
  VIA: iPhone Life (Leanne Hays, updated 24 Sep 2026)
  SRC: https://www.laptopmag.com/phones/how-to-know-if-youre-blocked-on-imessage
  VIA: Laptop Mag (Sarah Chaney, updated 2 Jun 2025)
  SRC: https://discussions.apple.com/thread/256225798
  VIA: Apple Community users, Jan 2026 — "Delivered" shown while blocked, 153 "me too"

- CLAIM: A green bubble does not prove a block: it means the message went as
  SMS, which also happens when someone turns off iMessage or moves to
  Android. Macworld's own test saw a blocked iMessage stay blue.
  TIER: multi
  SPOKEN: "A green bubble doesn't settle it either. It can just mean they turned off iMessage, or moved to Android."
  SURPRISE: 60
  SRC: https://www.igeeksblog.com/how-to-know-if-someone-has-blocked-you-on-imessage/
  VIA: iGeeksBlog: other causes include turning off iMessage
  SRC: https://www.laptopmag.com/phones/how-to-know-if-youre-blocked-on-imessage
  VIA: Laptop Mag: "unless the other person changed from iPhone to Android"
  SRC: https://www.macworld.com/article/668658/how-to-tell-if-someone-has-blocked-your-number-on-iphone.html
  VIA: Macworld own test: blocked text "remained blue"

- CLAIM: A call to someone who blocked you rings once or not at all, then
  goes to voicemail; two or more rings suggests you were not blocked.
  TIER: multi
  SPOKEN: "If it rings once, or not at all, and goes to voicemail every time, that points to a block. Two rings or more, and you're likely in the clear."
  SURPRISE: 65
  SRC: https://www.macworld.com/article/668658/how-to-tell-if-someone-has-blocked-your-number-on-iphone.html
  VIA: Macworld own testing (David Price): "if your phone rings twice or more, you've not been blocked"
  SRC: https://iphonelife.com/node/274079
  VIA: iPhone Life: "with barely even one ring"
  SRC: https://www.laptopmag.com/phones/how-to-know-if-youre-blocked-on-imessage
  VIA: Laptop Mag: "straight to voicemail with barely one ring"

- CLAIM: The call test is not proof: a phone that is off, a Focus / Do Not
  Disturb, or Silence Unknown Callers produce the same voicemail result.
  TIER: multi
  SPOKEN: "a phone that's off, a Focus, or Silence Unknown Callers can sound exactly the same"
  SURPRISE: 55
  SRC: https://www.macworld.com/article/668658/how-to-tell-if-someone-has-blocked-your-number-on-iphone.html
  VIA: Macworld: switched-off phone can ring once; Silence Unknown Callers sends calls to voicemail
  SRC: https://www.laptopmag.com/phones/how-to-know-if-youre-blocked-on-imessage
  VIA: Laptop Mag: phone off, out of service, or Do Not Disturb

- CLAIM: A blocked caller can still leave a voicemail; the person who blocked
  them gets no notification of it.
  TIER: official
  SPOKEN: "Apple says you can still leave a voicemail. They just won't get a notification."
  SURPRISE: 75
  SRC: https://support.apple.com/en-us/111104
  VIA: Apple Support: "they can still leave a voicemail, but you won't get a notification"
  SRC: https://www.macworld.com/article/668658/how-to-tell-if-someone-has-blocked-your-number-on-iphone.html
  VIA: Macworld: blocked voicemails land in a separate "blocked messages" folder

## FEATURES + HOW TO USE

What blocking does, per Apple's 29 May 2026 page:
- Blocked contact not notified — USED (the premise)
- Messages not delivered — USED
- Blocked caller can still leave a voicemail, no notification — USED
- Blocked email goes to trash — CUT (the reel is about texts and calls)
- Block from Phone / FaceTime / Messages ("Block Caller") or Settings >
  Privacy & Security > Blocked Contacts — CUT as steps (this reel is the
  blocked person's side); the Settings screen may appear as a visual only
- Blocking applies across devices on the same Apple Account — CUT

Signs the guides list, and what this reel does with each:
- "Delivered" missing — USED, as a myth (meaningless since iOS 16.5)
- Green bubble — USED, as not conclusive
- One ring then voicemail — USED, the strongest clue
- Hidden caller ID (*67) test — CUT: US-only code, fails against Silence
  Unknown Callers, and Macworld and Laptop Mag both warn it can read as
  harassment
- FaceTime error — CUT: guides disagree on the exact error and network
  faults cause the same thing
- Focus status "notifications silenced" — CUT: only one outlet claims it rules
  out a block, and a forum answer contradicts it
- Check other apps — CUT: not an iPhone sign

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-10-16  fetched support.apple.com/en-us/111104  (settled: no notification,
  messages not delivered, voicemail still possible without a notification;
  page dated 29 May 2026)
- 2026-10-16  "site:support.apple.com block phone numbers contacts emails iPhone blocked caller voicemail"
  (regional copies of the same page; nothing Apple says about Delivered labels or rings)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is
###    not the vendor
- 2026-10-16  fetched macworld.com/article/668658  (own test: none-or-one ring =
  blocked, two+ = not; blocked text stayed blue; Silence Unknown Callers caveat)
- 2026-10-16  fetched iphonelife.com/node/274079, laptopmag.com  (one-ring
  voicemail; Delivered shown since iOS 16.5)
- 2026-10-16  fetched igeeksblog.com/how-to-know-if-someone-has-blocked-you-on-imessage
  and guidingtech.com  (green bubble has other causes; FaceTime errors vary)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-10-16  fetched discussions.apple.com/thread/256225798  (Jan 2026: users
  blocked yet seeing "Delivered", 153 "me too"; reply: no indication, by design;
  another reply warns repeated contact can be treated as harassment)
- 2026-10-16  "blocked on iMessage "Delivered" still shows iOS 16.5 or later blocked contact"
  (older 2023 Community tests conflict — they predate or straddle 16.5)

### 4. WHAT WOULD CONTRADICT THIS
- 2026-10-16  "iPhone blocked number call goes to voicemail one ring hide caller ID test Silence Unknown Callers"
  (Silence Unknown Callers, Focus, phone off all mimic a block — so the call
  clue is spoken as "points to", never "proves")
- 2026-10-16  "notifications silenced Focus status blocked contact"  (Focus-status
  sign is contradicted between sources — cut)
- Macworld's 2020 test saw no "Delivered" — older than iOS 16.5, so it dates the
  claim rather than contradicting it; spoken as "guides report", not as fact.

INDEPENDENT-CHECK: 2026-10-16 searched hands-on tests and user reports —
  found Macworld's own ring-count test, and an Apple Community thread of users
  seeing "Delivered" while blocked. No outlet claims any single sign is proof;
  the script says so.
