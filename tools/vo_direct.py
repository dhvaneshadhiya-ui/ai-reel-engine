#!/usr/bin/env python3
"""Direct the READ beat by beat, then assemble one voiceover.

WHY: the whole reel was being synthesised with ONE delivery setting, so a
hook, an explanation, a turn and a CTA were all read identically. That is the
"doesn't adapt to the topic" the user named (2026-08-26). The framework
already demands this of music — hook, stable pulse, build, accent, release,
CTA — and says nothing about voice because nobody had wired it.

So: each beat is synthesised with its OWN emotion, tempo and pause, using the
same voice reference throughout, and the pieces are joined with the gaps the
story wants. One voice, many registers.

    python3 tools/vo_direct.py <slug> --ref <reference.wav> [--engine cosyvoice]

The script is read from jobs/<slug>/script.md. A line may carry a delivery
tag; untagged lines are directed by POSITION, using the arc below.

    [hook] Your Claude bill is mostly the reading.
    [turn] But its README admits something.

Delivery vocabulary — the registers, not the knob values, because the knobs
differ per engine and the register is what the story asks for.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Register -> (emotion, speaking rate, gap AFTER this beat in seconds).
# Rates stay inside 0.9-1.35: past that the read stops sounding like one
# person. The gaps are the framework's "selective silence" — a beat before a
# turn and after a payoff is what makes them land.
REGISTERS: dict[str, tuple[str, float, float]] = {
    "hook":    ("eager",     1.12, 0.16),
    "context": ("calm",      1.02, 0.12),
    "build":   ("eager",     1.08, 0.10),
    "turn":    ("surprised", 1.00, 0.34),   # silence BEFORE lands the turn
    "proof":   ("calm",      1.05, 0.12),
    "payoff":  ("calm",      0.96, 0.30),
    "cta":     ("excited",   1.06, 0.10),
}

# Position-based arc when a line carries no tag: a reel opens hot, settles to
# explain, builds, turns, proves, pays off, asks.
ARC = ["hook", "context", "build", "build", "turn", "proof", "proof",
       "payoff", "cta"]


def direct(lines: list[str]) -> list[tuple[str, str]]:
    """Assign a register to every line."""
    out = []
    untagged = [i for i, l in enumerate(lines)
                if not re.match(r"^\s*\[(\w+)\]", l)]
    for i, line in enumerate(lines):
        m = re.match(r"^\s*\[(\w+)\]\s*(.*)$", line)
        if m and m.group(1).lower() in REGISTERS:
            out.append((m.group(1).lower(), m.group(2).strip()))
            continue
        # position in the untagged sequence -> position in the arc
        pos = untagged.index(i) / max(1, len(untagged) - 1)
        out.append((ARC[min(int(pos * len(ARC)), len(ARC) - 1)], line.strip()))
    return out


# TYPOGRAPHIC PUNCTUATION BREAKS THE TOKENIZER (2026-08-26). IndexTTS2
# rejects an em-dash outright — `unencodableText` — and this repo's house
# style uses them in almost every line, so 8 of 13 beats failed on the first
# real run. They are punctuation for the EYE; the voice wants a pause, which
# is what a comma already means.
_SPOKEN_PUNCT = {
    "\u2014": ",", "\u2013": ",", "\u2012": ",",      # em/en/figure dash
    "\u2018": "'", "\u2019": "'",                      # curly single quotes
    "\u201c": '"', "\u201d": '"',                      # curly double quotes
    "\u2026": "...", "\u00a0": " ", "\u200b": "",     # ellipsis, nbsp, zwsp
    # PROVED BY PROBE, not inferred: synthesising "One: see it works" is
    # rejected while "One, see it works" is accepted, and "A test; another
    # clause" is rejected too. The tokenizer takes , . ! ? and little else.
    # Both marks mean "pause, then continue" — which is a comma out loud.
    ":": ",", ";": ",",
}


def speakable(text: str) -> str:
    """Punctuation a TTS tokenizer accepts, meaning unchanged."""
    for bad, good in _SPOKEN_PUNCT.items():
        text = text.replace(bad, good)
    text = re.sub(r",\s*,", ",", text)          # ", ," from a dash after a comma
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)  # no space before punctuation
    return re.sub(r"\s+", " ", text).strip()


def synth(text: str, register: str, ref: Path, engine: str,
          out: Path, transcript: str | None) -> bool:
    emotion, rate, _ = REGISTERS[register]
    cmd = ["speech", "speak", "--engine", engine,
           "--voice-sample", str(ref), "--output", str(out)]
    if engine == "indextts2":
        cmd += ["--indextts2-emotion", emotion,
                "--indextts2-speaking-rate", f"{rate}",
                "--indextts2-max-pause", "0.30"]
    elif engine == "cosyvoice":
        # CosyVoice takes a natural-language style instruction, and its docs
        # are explicit that the reference transcript must always be passed.
        cmd += ["--cosy-instruct", f"Speak {emotion}ly and clearly."]
        if transcript:
            cmd += ["--cosy-reference-transcript", transcript]
    cmd.append(speakable(text))
    # A PRE-EXISTING FILE IS NOT SUCCESS. The first version returned
    # `out.exists()`, so a failed synthesis silently kept the previous run's
    # audio and reported ok — which is how a "directed" voiceover shipped as
    # 5 new beats and 8 stale ones from a different engine. Delete first,
    # then judge.
    if out.exists():
        out.unlink()
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not (out.exists() and out.stat().st_size > 1000):
        tail = (r.stderr or r.stdout or "").strip().splitlines()
        if tail:
            print(f"       {tail[-1][:100]}")
        return False
    return True


def concat(parts: list[tuple[Path, float]], dest: Path) -> None:
    """Join with the directed gap after each beat, at a common rate."""
    import numpy as np
    sr_target = 24000
    chunks = []
    for path, gap in parts:
        w = wave.open(str(path))
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 2:
            a = a.reshape(-1, 2).mean(axis=1).astype(np.int16)
        if sr != sr_target:                     # cheap linear resample
            idx = np.linspace(0, len(a) - 1, int(len(a) * sr_target / sr))
            a = np.interp(idx, np.arange(len(a)), a).astype(np.int16)
        chunks.append(a)
        if gap > 0:
            chunks.append(np.zeros(int(sr_target * gap), dtype=np.int16))
    joined = np.concatenate(chunks)
    with wave.open(str(dest), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr_target)
        w.writeframes(joined.tobytes())


def main() -> int:
    argv = sys.argv[1:]
    if not argv or "--ref" not in argv:
        print(__doc__.split("    python3")[0].strip())
        return 1
    slug = argv[0]
    ref = Path(argv[argv.index("--ref") + 1])
    # DEFAULT indextts2, measured 2026-08-26: its numeric emotion presets
    # actually move the read (hook 204Hz / turn 241Hz / payoff 202Hz — 3.0
    # semitones of DIRECTED spread on one line), while CosyVoice's
    # natural-language --cosy-instruct did not steer emotion at all: across
    # 13 directed beats its pitch wandered 3.2 semitones with no relation to
    # the register asked for ("payoff" came out highest). CosyVoice stays
    # available via --engine for its cleaner Apache-2.0 licence, but it
    # cannot take direction.
    engine = argv[argv.index("--engine") + 1] if "--engine" in argv else "indextts2"
    transcript = argv[argv.index("--transcript") + 1] if "--transcript" in argv else None

    src = ROOT / f"jobs/{slug}/script.md"
    lines = [l.strip() for l in src.read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    plan = direct(lines)

    work = ROOT / "_sources" / slug / "vo-parts"
    work.mkdir(parents=True, exist_ok=True)
    print(f"\n=== directing {len(plan)} beats — {engine} ===\n")
    parts = []
    for i, (reg, text) in enumerate(plan):
        emo, rate, gap = REGISTERS[reg]
        out = work / f"{i:02d}_{reg}.wav"
        ok = synth(text, reg, ref, engine, out, transcript)
        print(f"  {i:02d} {reg:8} {emo:9} rate {rate:<5} gap {gap:<5} "
              f"{'ok' if ok else 'FAILED'}  {text[:44]!r}")
        if ok:
            parts.append((out, gap))
    if not parts:
        print("\n  nothing synthesised\n")
        return 1
    dest = ROOT / "_sources" / slug / "vo-directed.wav"
    concat(parts, dest)
    print(f"\n  assembled -> {dest.relative_to(ROOT)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
