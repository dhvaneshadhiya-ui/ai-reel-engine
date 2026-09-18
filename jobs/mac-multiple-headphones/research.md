# Research — mac-multiple-headphones

Claims ledger + search log; format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: PairPods, a free app, plays a Mac's audio to two or more Bluetooth devices at the same time.
  TIER: multi
  SPOKEN: "Your Mac can play one movie to two pairs of headphones at the same time. It takes a free app called PairPods"
  SRC: https://pairpods.app/
  VIA: developer site ("Share audio across two or more devices at once"; "For free."; "no hidden fees, time limits, or premium features")
  SRC: https://github.com/wozniakpawel/PairPods
  VIA: public source repository README ("Share audio between two or more Bluetooth devices"; "Completely free and open source", MIT)

- CLAIM: How to use: pair/connect the devices in macOS Bluetooth settings; open the PairPods menu-bar icon; tick the devices to include; press the Share Audio toggle (again to stop).
  TIER: multi
  SPOKEN: "First, connect every pair in Bluetooth settings. Then open PairPods from the menu bar, tick the devices you want, and flip Share Audio on."
  SRC: https://pairpods.app/
  VIA: developer site steps ("Connect your devices" / "Customize … deselect any devices you don't want to include" / "Press the Share Audio toggle"); official step screenshots step-1..3.png show the per-device checkboxes and the toggle
  SRC: https://www.oldergeeks.com/downloads/file.php?id=4667
  VIA: OlderGeeks download listing (v0.1.0, 28 Feb 2025): "Click on the PairPods menubar icon and press the Share Audio toggle"

- CLAIM: Works with any Bluetooth audio device macOS supports, named as AirPods, Samsung Buds, Sony headphones and Bluetooth speakers.
  TIER: official
  SPOKEN: "AirPods, Sony headphones, Samsung Buds, even a Bluetooth speaker."
  SRC: https://pairpods.app/
  VIA: developer site ("AirPods, Samsung Buds, Sony headphones, or any Bluetooth speaker"; "All Bluetooth devices supported by macOS")

- CLAIM: Each device has its own volume slider.
  TIER: official
  SPOKEN: "each device gets its own volume slider, so your friend can listen louder than you."
  SRC: https://pairpods.app/
  VIA: developer site ("adjust volume levels independently"); official screenshots show per-device sliders (Your AirPods Pro 75%, Friend's AirPods 40%)

- CLAIM: The menu shows each device's battery level and sample rate, and a crown selects the master device that the others sync to.
  TIER: official
  SPOKEN: "You also see every pair's battery and sample rate, and the crown sets the master device the others sync to."
  SRC: https://pairpods.app/
  VIA: developer site ("See each device's sample rate and battery level"; "one device acts as the master clock that all others sync to"); release v0.6.0 "Master device selection — tap the crown icon next to any device"

- CLAIM: Auto-reconnect waits a configurable time (Off, 5, 10 or 30 seconds) for a device that drops out.
  TIER: official
  SPOKEN: "if a pair drops out, PairPods waits five, ten or thirty seconds for it to reconnect."
  SRC: https://pairpods.app/
  VIA: developer site ("Choose how long it waits for a disconnected device to come back — Off, 5 seconds, 10 seconds, or 30 seconds"); release v0.6.0

- CLAIM: macOS has a built-in route, a Multi-Output Device in Audio MIDI Setup, but with it the keyboard and menu-bar volume controls do not work.
  TIER: multi
  SPOKEN: "Apple's route, a Multi-Output Device in Audio MIDI Setup. It works, but it takes away your volume keys."
  SRC: https://support.apple.com/guide/audio-midi-setup/play-audio-through-multiple-devices-at-once-ams7c093f372/mac
  VIA: Apple's own Audio MIDI Setup User Guide (the route exists)
  SRC: https://github.com/ExistentialAudio/BlackHole/wiki/Multi-Output-Device
  VIA: Existential Audio: "macOS does not support changing the volume of a Multi-Output device"
  SRC: https://www.amionmute.com/blog/multiple-audio-outputs-mac.html
  VIA: Am I on Mute? (12 Mar 2026): "you can't control volume from the keyboard or menu bar"

- CLAIM: Sync is not guaranteed; devices with different native sample rates can sound pitch-shifted, so same-model devices are recommended.
  TIER: multi
  SPOKEN: "sync isn't guaranteed, and different models can sound slightly off-pitch, so matching pairs work best."
  SRC: https://pairpods.app/
  VIA: developer site ("cannot guarantee perfectly synchronized playback"; mismatched sample rates "may experience slight pitch shifting")
  SRC: https://github.com/wozniakpawel/PairPods/issues
  VIA: user bug report #35 (27 Feb 2026) "Music Tuning Out of Control When Sharing Audio"

- CLAIM: PairPods is free, open source and requires macOS 13.5 or later.
  TIER: multi
  SPOKEN: "PairPods is free, open source and needs macOS 13.5 or later."
  SRC: https://pairpods.app/
  VIA: developer site ("Requires macOS 13.5 or later"; free)
  SRC: https://github.com/wozniakpawel/PairPods
  VIA: README ("macOS 13.5 (Ventura) or later"; MIT licence)

## FEATURES + HOW TO USE (the product itself, in full — 2026-09-17 rule)

Every feature the vendor documents, and whether the reel uses it:
- Share audio to two or more Bluetooth devices at once — USED (hook)
- Per-device checkboxes to choose which devices take part — USED (how-to)
- Independent volume per device — USED
- Battery level per device — USED
- Sample rate per device — USED (briefly)
- Master device / master clock via crown — USED
- Auto-reconnect with Off / 5s / 10s / 30s timeout — USED
- Launch at Login, Automatic Updates (visible in official screenshots) — CUT: settings, not reasons to download
- Homebrew cask install — CUT: link is in the pinned comment
How to use (vendor): 1 connect devices in Bluetooth settings → 2 choose master, volumes, deselect devices → 3 Share Audio toggle. USED in full.
Visual proof: official step screenshots step-1/2/3.png are the same menu in three states (crown moves, sliders move, HomePod unticked, Share Audio flips on) — used as real UI, not a mock-up.

## NOT CLAIMED

- That macOS has no way at all to use two headphones — it does (Multi-Output Device), and the reel says so.
- That PairPods adds no latency or syncs perfectly — the developer says the opposite.
- Any limit on how many devices PairPods can share to — the site says "two or more", no maximum.
- That PairPods is on the Mac App Store — it is a direct download or Homebrew cask.
- Any sponsorship or affiliation with the developer — user confirmed not sponsored.
- HomePod support: the developer's screenshots show a "Living Room HomePod" in the list, but no written claim covers it (the site says Bluetooth devices; HomePod reaches a Mac over AirPlay). Not spoken, not shown as supported.
- That PairPods remembers preferred device combinations — no source says so (a Google AI summary did); the documented feature is the reconnect timeout.

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-17  fetched pairpods.app  (features, price, requirements, stated limitations)
- 2026-09-17  fetched support.apple.com Audio MIDI Setup "Play audio through multiple devices at once"  (built-in route exists; steps)
- 2026-09-17  fetched support.apple.com "Change the sound output settings on Mac"  (single output selection)
- 2026-09-17  fetched github.com/wozniakpawel/PairPods + releases  (MIT, v0.7.0 22 Mar 2026, volume/battery features)

- 2026-09-17 (v2)  re-fetched pairpods.app for EVERY feature + how-to; fetched raw README; downloaded official step-1/2/3 and showcase screenshots  (per-device checkboxes, crown master, battery, kHz, reconnect Off/5/10/30s, Launch at Login, Automatic Updates)
- 2026-09-17 (v2)  fetched oldergeeks.com listing  (v0.1.0 how-to; no HomePod / device-memory claims)
- 2026-09-17 (v2)  checked a Google AI summary against the sources  (HomePod and "remembers device combinations" unsupported in text; HomePod appears only in the developer's screenshots)

### 2. WHO ELSE TRIED IT — hands-on, testing, benchmarks by someone who is not the vendor
- 2026-09-17  "PairPods Mac app connect two AirPods at once"  (Mac Observer round-up — 403 on fetch; Android Authority / Pocket-lint / MakeUseOf how-tos describe the Audio MIDI Setup route)
- 2026-09-17  "Mac Audio MIDI Setup multi-output device two Bluetooth headphones limitations volume"  (BlackHole wiki and Am I on Mute? both state the volume-key limitation; MacRumors and OWC how-tos do not mention it)

### 3. WHAT ARE PEOPLE SAYING — the ones actually using it
- 2026-09-17  "PairPods reddit mac share audio two headphones experience"  (MPU Talk forum thread on the utility; AlternativeTo listing)
- 2026-09-17  fetched PairPods GitHub issues  (2 open: #47 app not opening, #35 pitch "tuning out of control" while sharing — corroborates the pitch caveat)

### 4. WHAT WOULD CONTRADICT THIS — the search you would run if you were trying to prove the story wrong
- 2026-09-17  checked whether Apple's own route already solves it  (it does, with manual setup and no keyboard volume — the reel presents it rather than hiding it)
- 2026-09-17  checked PairPods' own limitations and open bugs  (sync not guaranteed, pitch shift on mismatched sample rates, a launch-failure report — the caveat is spoken)

INDEPENDENT-CHECK: 2026-09-17 searched for independent use of PairPods and of the built-in Multi-Output Device — found independent write-ups of the volume limitation (BlackHole wiki, Am I on Mute?) and a user bug report confirming the pitch issue; no independent latency measurement exists, which is why sync is described only as "not guaranteed".
