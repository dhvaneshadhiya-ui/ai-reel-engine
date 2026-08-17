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


# Above this, a single multiplier is a lie and the tool reports a RANGE.
SPREAD_LIMIT = 0.25


def cal_factor() -> tuple[float, float, str]:
    """(lo, hi, basis). lo == hi only when the calibration was tight.

    Tolerates a calibration.json written by an OLDER build of this tool, which
    stored a single `factor` and no lo/hi. Reading one used to raise
    KeyError('lo') and take `speak` down — a stale artifact must degrade, never
    crash, so the pre-range format is reconstructed and LABELLED as such.
    """
    if not CAL_FILE.exists():
        return 1.0, 1.0, "UNCALIBRATED — run `calibrate`; duration is raw chatterbox"
    d = json.loads(CAL_FILE.read_text())
    basis = d.get("basis", "calibration.json")
    if "lo" in d and "hi" in d:
        return float(d["lo"]), float(d["hi"]), basis
    if "factor" in d:
        f = float(d["factor"])
        spread = float(d.get("spread") or 0.0)
        if spread > SPREAD_LIMIT:
            # Only the mean and the spread survived; the true endpoints did not.
            # Reconstruct symmetrically and say so, rather than quoting the mean
            # as if it were tight.
            return (f - spread / 2, f + spread / 2,
                    basis + "  [pre-range file — endpoints RECONSTRUCTED from "
                            "mean±spread/2; re-run `calibrate` for the real range]")
        return f, f, basis + "  [pre-range file]"
    return (1.0, 1.0,
            f"UNREADABLE calibration.json (keys: {sorted(d)}) — re-run `calibrate`")


def cmd_speak(slug: str, text: str | None) -> None:
    ref = OUT / f"ref-{slug}.wav"
    if not ref.exists():
        ref = build_ref(slug)
    body = text if text else spoken_text(slug)
    words = len(body.split())
    dest = OUT / f"{slug}-rehearsal.wav"
    dur = generate(body, ref, dest)
    lo, hi, basis = cal_factor()
    print(f"\n  words           {words}")
    print(f"  chatterbox      {dur:.1f}s  ({words/dur:.2f} wps)")
    if abs(hi - lo) < 1e-6:
        print(f"  HeyGen estimate {dur*lo:.1f}s   x{lo:.3f}")
    else:
        print(f"  HeyGen RANGE    {dur*lo:.0f}-{dur*hi:.0f}s   "
              f"x{lo:.3f}-{hi:.3f}")
    print(f"  basis           {basis}")
    print(f"  audio           {dest.relative_to(ROOT)}")
    print("\n  LISTEN to it. The duration is weak evidence — measured 2026-08-17,")
    print("  chatterbox runs anywhere from 15% slower to 16% faster than HeyGen")
    print("  on the same words, so use this to judge PHRASING, and keep the")
    print("  approval gate's word budget for length.")


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
    fs = [r[3] for r in rows]
    lo, hi = min(fs), max(fs)
    spread = hi - lo
    OUT.mkdir(parents=True, exist_ok=True)
    tight = spread <= SPREAD_LIMIT
    mean = sum(fs) / len(fs)
    CAL_FILE.write_text(json.dumps(
        {"lo": round(lo if not tight else mean, 4),
         "hi": round(hi if not tight else mean, 4),
         "mean": round(mean, 4), "spread": round(spread, 4), "n": len(rows),
         "tight": tight,
         "basis": (f"{len(rows)} masters, first 40 words each, spread "
                   f"{spread:.3f}" + ("" if tight else
                   " — TOO WIDE for a single multiplier, reported as a range"))},
        indent=2))
    print(f"\n  n={len(rows)}  mean {mean:.3f}  range {lo:.3f}-{hi:.3f}  "
          f"spread {spread:.3f}")
    if not tight:
        print(f"  SPREAD > {SPREAD_LIMIT} — a single factor would be a lie. The mean "
              f"({mean:.3f}) hides\n  that chatterbox is SLOWER on some masters and "
              "FASTER on others, so `speak`\n  will report a range and tell you to "
              "trust the word budget for length.")


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
