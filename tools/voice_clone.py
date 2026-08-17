#!/usr/bin/env python3
"""Local voice clone — rehearse a script's timing without spending credits.

WHY THIS EXISTS
---------------
The approval gate blocks a script whose SLOWEST plausible delivery overshoots
the format band, using a measured 2.35-2.75 words/sec range taken from five
real HeyGen masters. That range is wide because the voice genuinely varies, so
a borderline script gets rejected on the pessimistic end even when it would
have been fine.

Chatterbox (Resemble AI, MIT) clones the voice locally from a reference sample,
so a script can be SPOKEN and MEASURED before a single credit is spent.

    python3 tools/voice_clone.py speak  <slug>            # rehearse a job's script
    python3 tools/voice_clone.py speak  <slug> --text "…" # rehearse arbitrary text
    python3 tools/voice_clone.py ref    <slug>            # build the reference sample
    python3 tools/voice_clone.py calibrate                # chatterbox vs HeyGen pace

HONEST LIMITS — read before trusting a number
---------------------------------------------
1. **This is NOT the HeyGen voice.** It is a local clone of a reference sample.
   Its absolute pace differs, so a raw duration is not a HeyGen prediction.
   `calibrate` measures the ratio against real masters; `speak` applies it and
   says so. Treat the output as an ESTIMATE WITH A STATED SOURCE, never as the
   render.
2. **Every output is watermarked.** Chatterbox embeds Resemble's imperceptible
   Perth watermark in all generated audio. Fine for rehearsal; it means this
   audio is detectably synthetic and is NOT a substitute for the real VO.
3. **It runs in its own venv on purpose.** chatterbox-tts pins torch 2.6.0;
   the system has 2.13.0 under whisper. Installing it system-wide downgrades
   torch and breaks transcription — verified 2026-08-17, which is why
   MIGRATION.md §6.3 says NEVER system-wide.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = Path.home() / ".venvs/chatterbox/bin/python"
OUT = ROOT / "out/voice-clone"

# Set by `calibrate`. 1.0 means "unknown — treat the duration as raw".
CAL_FILE = OUT / "calibration.json"


def need_venv() -> None:
    if not VENV.exists():
        sys.exit("chatterbox venv missing. Install it (NEVER system-wide — it "
                 "downgrades torch under whisper):\n"
                 "  python3 -m venv ~/.venvs/chatterbox\n"
                 "  ~/.venvs/chatterbox/bin/pip install chatterbox-tts")


def spoken_text(slug: str) -> str:
    p = ROOT / "jobs" / slug / "script.md"
    if not p.exists():
        sys.exit(f"no script at {p}")
    return " ".join(
        l.strip() for l in p.read_text().splitlines()
        if l.strip() and not l.lstrip().startswith(("#", ">", "<!--")))


def build_ref(slug: str) -> Path:
    """A clean ~11s mono reference from that reel's VO master."""
    vo = ROOT / "public/assets" / slug / "vo.wav"
    if not vo.exists():
        sys.exit(f"no VO master at {vo} — pick a slug that has been generated")
    OUT.mkdir(parents=True, exist_ok=True)
    ref = OUT / f"ref-{slug}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-t", "11",
                    "-i", str(vo), "-ac", "1", "-ar", "24000", str(ref)],
                   check=True)
    print(f"reference: {ref.relative_to(ROOT)}")
    return ref


def generate(text: str, ref: Path, dest: Path) -> float:
    """Speak `text` in the cloned voice; returns duration in seconds."""
    need_venv()
    OUT.mkdir(parents=True, exist_ok=True)
    script = f'''
import torch, torchaudio
from chatterbox.tts import ChatterboxTTS
dev = "mps" if torch.backends.mps.is_available() else "cpu"
m = ChatterboxTTS.from_pretrained(device=dev)
w = m.generate({text!r}, audio_prompt_path={str(ref)!r})
torchaudio.save({str(dest)!r}, w, m.sr)
'''
    r = subprocess.run([str(VENV), "-c", script], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("chatterbox failed:\n" + r.stderr[-1500:])
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(dest)],
        capture_output=True, text=True, check=True).stdout.strip())
    return dur


def cal_factor() -> tuple[float, str]:
    if CAL_FILE.exists():
        d = json.loads(CAL_FILE.read_text())
        return float(d["factor"]), d.get("basis", "calibration.json")
    return 1.0, "UNCALIBRATED — run `calibrate` first; duration is raw chatterbox"


def cmd_speak(slug: str, text: str | None) -> None:
    ref = OUT / f"ref-{slug}.wav"
    if not ref.exists():
        ref = build_ref(slug)
    body = text if text else spoken_text(slug)
    words = len(body.split())
    dest = OUT / f"{slug}-rehearsal.wav"
    dur = generate(body, ref, dest)
    factor, basis = cal_factor()
    print(f"\n  words           {words}")
    print(f"  chatterbox      {dur:.1f}s  ({words/dur:.2f} wps)")
    print(f"  HeyGen estimate {dur*factor:.1f}s   x{factor:.3f}")
    print(f"  basis           {basis}")
    print(f"  audio           {dest.relative_to(ROOT)}")
    print("\n  This is an ESTIMATE from a local clone, not the HeyGen voice.")


def cmd_calibrate() -> None:
    """Speak the exact words of real masters and compare to their true length."""
    need_venv()
    rows = []
    for vo in sorted((ROOT / "public/assets").glob("*/vo.json")):
        slug = vo.parent.name
        wav = vo.parent / "vo.wav"
        if not wav.exists():
            continue
        d = json.loads(vo.read_text())
        words = [w["word"] for s in d.get("segments", []) for w in s.get("words", [])]
        if len(words) < 40:
            continue
        real = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(wav)],
            capture_output=True, text=True, check=True).stdout.strip())
        # rehearse the FIRST ~40 words only — enough to measure pace, cheap
        text = " ".join(words[:40]).strip()
        ref = OUT / f"ref-{slug}.wav"
        if not ref.exists():
            ref = build_ref(slug)
        got = generate(text, ref, OUT / f"cal-{slug}.wav")
        # HeyGen pace over the same 40 words, from its own word timings
        flat = [w for s in d.get("segments", []) for w in s.get("words", [])]
        heygen_span = float(flat[39]["end"]) - float(flat[0]["start"])
        rows.append((slug, heygen_span, got, heygen_span / got))
        print(f"  {slug:22} heygen {heygen_span:5.1f}s  chatterbox {got:5.1f}s  "
              f"x{heygen_span/got:.3f}")
    if not rows:
        sys.exit("no masters with word timings found")
    factor = sum(r[3] for r in rows) / len(rows)
    spread = max(r[3] for r in rows) - min(r[3] for r in rows)
    OUT.mkdir(parents=True, exist_ok=True)
    CAL_FILE.write_text(json.dumps(
        {"factor": round(factor, 4), "spread": round(spread, 4),
         "n": len(rows),
         "basis": f"{len(rows)} masters, first 40 words each, spread {spread:.3f}"},
        indent=2))
    print(f"\n  factor {factor:.3f} across {len(rows)} masters, spread {spread:.3f}")
    if spread > 0.25:
        print("  WARNING: spread is wide — treat the estimate as a range, not a number.")


def main() -> None:
    a = sys.argv[1:]
    if not a or a[0] not in ("speak", "ref", "calibrate"):
        sys.exit(__doc__.split("HONEST LIMITS")[0].strip())
    if a[0] == "calibrate":
        cmd_calibrate()
    elif a[0] == "ref":
        build_ref(a[1])
    else:
        text = None
        if "--text" in a:
            text = a[a.index("--text") + 1]
        cmd_speak(a[1], text)


if __name__ == "__main__":
    main()
