#!/usr/bin/env python3
"""Tighten a VibeVoice VO: cap inter-word pauses + apply tempo, WITHOUT whisper.
Reconstructs audio from word spans and emits matching word timings."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "public/assets/pod-reel"
NAME = sys.argv[1]                      # vo-A / vo-B
TEMPO = float(sys.argv[2]) if len(sys.argv) > 2 else 1.17
CAP = 0.11                              # max kept pause between words
LEAD = 0.06

d = json.loads((P / f"{NAME}.json").read_text())
w = [(x["start"], x["end"], x["word"].strip()) for s in d["segments"] for x in s.get("words", [])]

# build "remove" intervals for gaps larger than CAP (+ leading trim)
removes = []
if w[0][0] > LEAD:
    removes.append((0.0, w[0][0] - LEAD))
for i in range(len(w) - 1):
    gap = w[i + 1][0] - w[i][1]
    if gap > CAP:
        mid_pad = CAP / 2
        removes.append((w[i][1] + mid_pad, w[i + 1][0] - mid_pad))

# keep segments = complement of removes across [0, last_end+0.15]
end = w[-1][1] + 0.15
keeps, cur = [], 0.0
for rs, re_ in removes:
    if rs > cur:
        keeps.append((cur, rs))
    cur = re_
keeps.append((cur, end))


def removed_before(t):
    return sum(min(r[1], t) - r[0] for r in removes if r[0] < t)


def newt(t):
    return round((t - removed_before(t)) / TEMPO, 3)


# emit new timings
nw = [{"start": newt(s), "end": newt(e), "word": word} for (s, e, word) in w]
(P / f"{NAME}-fast.json").write_text(json.dumps({"words": nw}))

# build ffmpeg aselect keep expression
expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keeps)
af = f"aselect='{expr}',asetpts=N/SR/TB,atempo={TEMPO}"
subprocess.run(["ffmpeg", "-y", "-i", str(P / f"{NAME}.wav"), "-af", af,
                "-ar", "24000", "-ac", "1", str(P / f"{NAME}-fast.wav")],
               check=True, capture_output=True)
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", str(P / f"{NAME}-fast.wav")], capture_output=True, text=True).stdout.strip()
print(f"{NAME}: {len(w)} words -> {NAME}-fast.wav {dur}s (VO ends {nw[-1]['end']}s)")
