#!/usr/bin/env python3
"""Does it still sound like the same person? A number, not an impression.

Built 2026-08-26 to settle a specific question: a voice clone trained on a
20-second reference may carry the words and lose the identity, and "it sounds
close enough to me" is not a basis for replacing a brand voice.

Compares an MFCC fingerprint — the standard cheap proxy for vocal timbre —
between a REFERENCE recording and one or more candidates. Cosine similarity
of the mean cepstrum over voiced frames.

    python3 tools/voice_similarity.py ref.wav candidate.wav [more.wav ...]

READ IT AS A RANKING, NOT A VERDICT. The number is only meaningful against a
CONTROL: pass a recording of a genuinely different speaker as one of the
candidates, and judge every other candidate by how far it sits from that
control. An absolute score has no units anyone should trust.
"""
from __future__ import annotations

import sys
import wave
from pathlib import Path

import numpy as np


def _mel_filters(sr: int, n_fft: int, n_mels: int = 26) -> np.ndarray:
    def hz2mel(f):
        return 2595 * np.log10(1 + f / 700)

    def mel2hz(m):
        return 700 * (10 ** (m / 2595) - 1)

    lo, hi = hz2mel(80), hz2mel(min(7600, sr / 2))
    pts = mel2hz(np.linspace(lo, hi, n_mels + 2))
    bins = np.floor((n_fft + 1) * pts / sr).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(1, n_mels + 1):
        l, c, r = bins[i - 1], bins[i], bins[i + 1]
        if c == l:
            c = l + 1
        if r == c:
            r = c + 1
        if r >= fb.shape[1]:
            r = fb.shape[1] - 1
        if c >= r or l >= c:
            continue
        fb[i - 1, l:c] = (np.arange(l, c) - l) / (c - l)
        fb[i - 1, c:r] = (r - np.arange(c, r)) / (r - c)
    return fb


def fingerprint(path: Path) -> np.ndarray:
    w = wave.open(str(path))
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    a = a.astype(float) / 32768.0
    if w.getnchannels() == 2:
        a = a.reshape(-1, 2).mean(axis=1)
    n_fft, hop = 512, 256
    fb = _mel_filters(sr, n_fft)
    win = np.hanning(n_fft)
    feats = []
    for i in range(0, len(a) - n_fft, hop):
        x = a[i:i + n_fft]
        if np.sqrt((x ** 2).mean()) < 0.01:      # skip silence
            continue
        spec = np.abs(np.fft.rfft(x * win)) ** 2
        mel = np.log(fb @ spec + 1e-10)
        # DCT-II -> cepstrum; drop c0 (energy), keep 1..13 (timbre)
        c = np.array([
            (mel * np.cos(np.pi * k * (np.arange(len(mel)) + 0.5) / len(mel))).sum()
            for k in range(14)])
        feats.append(c[1:])
    if not feats:
        raise SystemExit(f"no voiced audio in {path}")
    f = np.array(feats)
    v = f.mean(axis=0)
    return v / (np.linalg.norm(v) + 1e-9)


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__.split("    python3")[0].strip())
        return 1
    ref = Path(sys.argv[1])
    ref_fp = fingerprint(ref)
    print(f"\n=== voice similarity vs {ref.name} ===\n")
    rows = []
    for p in sys.argv[2:]:
        path = Path(p)
        sim = float(ref_fp @ fingerprint(path))
        rows.append((path.name, sim))
    for name, sim in sorted(rows, key=lambda r: -r[1]):
        bar = "#" * int(max(0, sim) * 40)
        print(f"  {sim:6.3f}  {bar:<40} {name}")
    print("\n  Judge against the CONTROL — a known different speaker. A "
          "candidate\n  near the control is a different voice, whatever the "
          "absolute number.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
