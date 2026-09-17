# Research — mac-multiple-headphones

Claims ledger + search log; format in tools/research_check.py.
Tiers: official / multi / single / disputed. A single or
disputed claim must be SPOKEN hedged (framework S20).

## CLAIMS

- CLAIM: In macOS Sound settings you pick one output device from a list, so headphones play one pair at a time by default.
  TIER: official
  SPOKEN: "pick headphones in your Mac's sound settings and only one pair plays."
  SRC: https://support.apple.com/guide/mac-help/change-the-sound-output-settings-mchlp2256/mac
  VIA: Apple's own Mac User Guide ("select the device you want to use in the list of sound output devices")

- CLAIM: macOS has a built-in way to play through several devices: Audio MIDI Setup can create a Multi-Output Device.
  TIER: official
  SPOKEN: "Audio MIDI Setup: a Multi-Output Device that plays to both."
  SRC: https://support.apple.com/guide/audio-midi-setup/play-audio-through-multiple-devices-at-once-ams7c093f372/mac
  VIA: Apple's own Audio MIDI Setup User Guide

- CLAIM: With a Multi-Output Device selected, the Mac's keyboard and menu-bar volume controls do not work; each device's volume is set in Audio MIDI Setup.
  TIER: multi
  SPOKEN: "your Mac's volume keys stop working, so you set each pair's volume by hand."
  SRC: https://github.com/ExistentialAudio/BlackHole/wiki/Multi-Output-Device
  VIA: Existential Audio (BlackHole audio driver developer): "macOS does not support changing the volume of a Multi-Output device"
  SRC: https://www.amionmute.com/blog/multiple-audio-outputs-mac.html
  VIA: Am I on Mute? (12 Mar 2026): "you can't control volume from the keyboard or menu bar"

- CLAIM: PairPods is a free, open-source (MIT) menu-bar app that shares audio to two or more Bluetooth devices with a single Share Audio toggle.
  TIER: multi
  SPOKEN: "It does the same job with one toggle in the menu bar, and it's free and open source."
  SRC: https://pairpods.app/
  VIA: the developer's own site ("Share audio on macOS with just a click. For free."; "no hidden fees, time limits, or premium features")
  SRC: https://github.com/wozniakpawel/PairPods
  VIA: the public source repository (MIT licence, 856 stars at research time)

- CLAIM: PairPods gives each device its own volume control and shows each device's battery level.
  TIER: official
  SPOKEN: "Each pair gets its own volume and battery level"
  SRC: https://pairpods.app/
  VIA: developer site ("adjust volume levels independently"; "sample rate and battery level at a glance"); release notes v0.2.0 individual volume controls, v0.6.0/v0.7.0 battery level

- CLAIM: It works with any Bluetooth audio device macOS supports — AirPods, Samsung Buds, Sony headphones, Bluetooth speakers — on macOS 13.5 or later, Intel or Apple silicon.
  TIER: official
  SPOKEN: "it works with AirPods, Sony headphones and Samsung Buds, even a Bluetooth speaker, on macOS 13.5 or later."
  SRC: https://pairpods.app/
  VIA: developer site ("AirPods, Samsung Buds, Sony headphones, or any Bluetooth speaker"; "Requires macOS 13.5 or later")

- CLAIM: Sync is not guaranteed, and devices with different native sample rates can sound pitch-shifted; the developer suggests using the same model or choosing the master device.
  TIER: multi
  SPOKEN: "sync isn't guaranteed. Mix two different models and one can sound slightly off-pitch, so matching pairs work best."
  SRC: https://pairpods.app/
  VIA: developer site ("cannot guarantee perfectly synchronized playback"; mismatched sample rates "may experience slight pitch shifting")
  SRC: https://github.com/wozniakpawel/PairPods/issues
  VIA: user bug report #35, 27 Feb 2026: "Music Tuning Out of Control When Sharing Audio"

## NOT CLAIMED

- That macOS has no way at all to use two headphones — it does (Multi-Output Device), and the reel says so.
- That PairPods adds no latency or syncs perfectly — the developer says the opposite.
- Any limit on how many devices PairPods can share to — the site says "two or more", no maximum.
- That PairPods is on the Mac App Store — it is a direct download or Homebrew cask.
- Any sponsorship or affiliation with the developer (see questions.md).

## SEARCHED

### 1. WHAT HAPPENED — the official record
- 2026-09-17  fetched pairpods.app  (features, price, requirements, stated limitations)
- 2026-09-17  fetched support.apple.com Audio MIDI Setup "Play audio through multiple devices at once"  (built-in route exists; steps)
- 2026-09-17  fetched support.apple.com "Change the sound output settings on Mac"  (single output selection)
- 2026-09-17  fetched github.com/wozniakpawel/PairPods + releases  (MIT, v0.7.0 22 Mar 2026, volume/battery features)

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
