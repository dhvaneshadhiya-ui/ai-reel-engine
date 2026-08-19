#!/usr/bin/env python3
"""Post-compile fixes for airpods-camera. Run after every compile_shot_plan run.

Three things compile_shot_plan.py does not do for this reel:

1. CAPTIONS FROM UNSPLIT WORDS. The compiler splits "Apple's" into two word
   entries so phrase anchors can match, then reuses those split tokens for
   captions — which renders "apple s own." (G34) and emits tokens that are not
   in the narration (G21). Captions are rebuilt here from the original whisper
   words, with whisper's split decimals ("26" + ".7") merged (G30/G16).
2. THE APPROVED SCRIPT + APPROVAL RECORD on the sheet (G27).
3. NO MUSIC BED. User call 2026-08-18: "Background music is too low. Let's
   remove background music from this video. However, use the sound effects."
   compile_shot_plan.py substitutes a default bed when the plan carries no
   `music`, so the key is removed here. The 9 SFX cues are untouched. G09 (a
   music bed on every reel) and G37 (a derived curve) both print as ADVICE —
   neither is in BLOCKING_RULES — so this is a judgement call, not an override.
4. TAIL PAD. The compiler ends the sheet at the last spoken WORD, but the
   avatar master runs slightly longer; validate_job.py requires the scenes to
   sum to within 0.2s of the audio. The pad goes on the final scene.
"""
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "airpods-camera"
beats_p = ROOT / f"src/beats/{SLUG}.json"
vo_p = ROOT / f"public/assets/{SLUG}/vo.json"
master = ROOT / f"public/assets/{SLUG}/avatar-master.mp4"

words = [w for s in json.loads(vo_p.read_text())["segments"] for w in s.get("words", [])]
merged = []
for w in words:
    t = w["word"].strip()
    if merged and re.fullmatch(r"[.,]\d+", t):
        merged[-1]["word"] = merged[-1]["word"].rstrip() + t
        merged[-1]["end"] = w["end"]
        continue
    merged.append(dict(w))
caps = [{"start": round(g[0]["start"], 3), "end": round(g[-1]["end"], 3),
         "text": " ".join(x["word"].strip() for x in g)}
        for g in (merged[i:i + 3] for i in range(0, len(merged), 3))]

b = json.loads(beats_p.read_text())
b["captions"] = caps
b["script"] = (ROOT / f"jobs/{SLUG}/script.md").read_text().strip()
b["approval"] = json.loads((ROOT / f"jobs/{SLUG}/approval.json").read_text())
b.pop("music", None)
b["noMusic"] = True
b["noMusicReason"] = (
    "User call 2026-08-18: the bed read as too quiet to earn its place, so this "
    "cut runs voice + SFX only. The 9 SFX cues are kept and carry the punctuation "
    "the bed was doing. Re-derive a curve with tools/duck_music.py if a bed "
    "is ever wanted back.")

audio = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(master)],
    capture_output=True, text=True).stdout.strip())
total = sum(s["durationSec"] for s in b["scenes"])
pad = round(audio - total, 3)
if pad > 0:
    b["scenes"][-1]["durationSec"] = round(b["scenes"][-1]["durationSec"] + pad, 3)

beats_p.write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n")
print(f"{len(caps)} captions | script+approval stored | tail pad {pad:+.3f}s "
      f"-> scenes {sum(s['durationSec'] for s in b['scenes']):.3f}s vs audio {audio:.3f}s")
