# Voice clone recording spec — how to make a clone that isn't flat

**Why this exists.** Measured 2026-08-26: the current clone ("iGeeks Blog")
produces **1.86 semitones** of pitch movement on a test line. A HeyGen stock
voice, same text and speed, produces **3.27**. Real creator references run
**3.74–6.63**. Two rounds of settings probes (stability 0.42→0.28, style
0.35→0.62, and eleven_v3) moved it **not at all**.

A voice clone reproduces the expressiveness of the audio it was trained on.
If the source read is level, the clone is level, permanently. It cannot be
argued into energy it never heard.

## What to record

**Length:** 3–5 minutes of clean speech is plenty. More flat audio is worse
than less good audio.

**The one thing that matters:** read like you are TALKING TO SOMEONE, not
reading aloud. The clone learns your range, not your words.

Record all four of these, because a clone trained on one register can only
produce that register:

1. **A cold open, punchy** — the kind of first line that makes someone stop
   scrolling. Land hard on the key word. Two or three takes, varied.
2. **An explanation, calm and level** — how something works, unhurried. This
   is the register most of a reel actually uses.
3. **A turn** — "but here's what nobody checked". Genuine change in pitch and
   pace when the story pivots. This is the register the current clone is
   most obviously missing.
4. **A close** — the last line of a video, landing, slightly slower.

**Deliberately include:** questions that actually rise at the end, a couple of
sentences said with real surprise, one said quietly, and one emphatic. Range
is the entire point.

**Avoid:** reading a paragraph of text top to bottom in one tone — which is
what produces a clone like the current one.

## Technical

- Quiet room, no music, no processing, no noise gate.
- One consistent mic at a consistent distance. Phone voice memos in a soft
  room beats a good mic in an echoey one.
- 44.1kHz+ WAV or M4A. No MP3 re-encodes.
- No long silences, no coughs, no edits mid-word.

## After recording

Hand the files over and the clone is rebuilt against them. Then, before it is
used on anything:

    python3 tools/vo_qc.py --wav <sample.wav>

**Accept the clone only if pitch variation clears 3.5 semitones** — the floor
taken from the flattest real creator reference. Below that, re-record with
more range rather than shipping and hoping the mix rescues it. It cannot.
