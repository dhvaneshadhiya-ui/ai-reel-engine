#!/usr/bin/env python3
"""Post-compile finalise for iphone-18-pro.

compile_shot_plan writes the scene spine; these four things it does not know
about and they must be reapplied after EVERY recompile:
  1. script + approval  (G27 hashes the approved narration onto the sheet)
  2. the split hook's captions must clear the face seam (validate_job)
  3. scenes must sum EXACTLY to the audio (G01) — trailing silence on the last beat
  4. a real music bed with automation shaped to the story (G09), not a flat line
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SHEET = ROOT / "src/beats/iphone-18-pro.json"
AUDIO = 72.49

d = json.loads(SHEET.read_text()); sc = d["scenes"]
d["script"] = (ROOT / "jobs/iphone-18-pro/script.md").read_text().strip()
d["approval"] = json.loads((ROOT / "jobs/iphone-18-pro/approval.json").read_text())
if sc[0]["type"] == "split":
    sc[0]["captionBottom"] = 1000
sc[-1]["durationSec"] = round(sc[-1]["durationSec"] + (AUDIO - sum(s["durationSec"] for s in sc)), 3)

t, starts = 0.0, []
for s in sc:
    starts.append(t); t += s["durationSec"]
payoff = next(starts[i] for i, s in enumerate(sc) if s.get("title") == "5G VIA SATELLITE")
turn = next(starts[i] for i, s in enumerate(sc)
            if any("impact-boom" in str(c.get("src", "")) for c in s.get("sfx", [])))
d["music"] = {"src": "music/bed-02.mp3", "from": 0, "points": [
    {"t": 0.0, "vol": 0.16},                      # full under the hook
    {"t": 4.0, "vol": 0.085},                     # duck for the explanation
    {"t": round(payoff - 1.5, 2), "vol": 0.085},
    {"t": round(payoff + 0.3, 2), "vol": 0.15},   # rise on the satellite payoff
    {"t": round(payoff + 3.5, 2), "vol": 0.10},
    {"t": round(turn, 2), "vol": 0.15},           # up on the turn
    {"t": round(starts[-1], 2), "vol": 0.13},     # hold under the CTA
    {"t": round(AUDIO - 0.6, 2), "vol": 0.0},     # fade
]}
SHEET.write_text(json.dumps(d, indent=1, ensure_ascii=False))
face = sum(s["durationSec"] for s in sc
           if s["type"] == "footage" and "avatar-master" in str(s.get("src", "")))
print(f"finalised: {len(sc)} scenes, {sum(s['durationSec'] for s in sc):.2f}s "
      f"(audio {AUDIO}), facecam {face/AUDIO*100:.1f}%")
