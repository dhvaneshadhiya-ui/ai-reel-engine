#!/usr/bin/env python3
"""Lengthen the SILENCES in a voiceover, never the words.

Three reels in a row came back from ElevenLabs too fast (five-free 3.34 w/s
within words, PairPods 3.09, ios27-battery-drain 3.27 overall) and each time
the fix was the same hand-rolled ffmpeg session: find the gaps between
sentences, make them longer, leave every syllable untouched. Time-stretching
would move the pitch and undo the reason for buying that read in the first
place (STYLE-RULES 2026-09-17), so this pads with digital silence instead.

    python3 tools/vo_pad.py <slug> [--target 79] [--in file.mp3]

Reads the prepared VO (public/assets/<slug>/vo.mp3 unless --in), finds every
silent run, and grows the ones that separate speech until the take lands near
--target seconds. Sentence gaps and paragraph gaps grow in proportion, so the
rhythm of the read survives; a pause inside a phrase (< MIN_GAP) is left alone.

Self-check: python3 tools/vo_pad.py --demo
"""
from __future__ import annotations

import array
import math
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WIN = 0.020          # 20ms analysis window
SILENCE_DB = -38.0   # below this, relative to full scale, counts as silence
MIN_GAP = 0.16       # shorter than this is breath inside a phrase — leave it
FLOOR = 1e-9


def _db(rms: float) -> float:
    return 20 * math.log10(max(rms, FLOOR) / 32768.0)


def _decode(src: Path, wav: Path) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
                    "-ac", "1", "-ar", "44100", "-f", "wav", str(wav)], check=True)


def silences(samples: array.array, rate: int) -> list[tuple[int, int]]:
    """[start, end) sample ranges quieter than SILENCE_DB for >= MIN_GAP."""
    win = int(rate * WIN)
    quiet: list[bool] = []
    for i in range(0, len(samples) - win, win):
        chunk = samples[i:i + win]
        rms = math.sqrt(sum(float(s) * s for s in chunk) / len(chunk))
        quiet.append(_db(rms) < SILENCE_DB)
    runs, start = [], None
    for i, q in enumerate(quiet):
        if q and start is None:
            start = i
        elif not q and start is not None:
            runs.append((start * win, i * win))
            start = None
    if start is not None:
        runs.append((start * win, len(quiet) * win))
    return [(a, b) for a, b in runs if (b - a) / rate >= MIN_GAP]


def pad(samples: array.array, rate: int, gaps: list[tuple[int, int]],
        extra_total: float) -> array.array:
    """Distribute `extra_total` seconds across the gaps, longest gaps first —
    a paragraph break earns more of the new air than a comma does."""
    inner = [g for g in gaps if g[0] > 0 and g[1] < len(samples)]
    if not inner or extra_total <= 0:
        return samples
    weights = [(b - a) for a, b in inner]
    total_w = sum(weights)
    out = array.array("h")
    prev = 0
    for (a, b), w in zip(inner, weights):
        out.extend(samples[prev:b])
        add = int(rate * extra_total * (w / total_w))
        out.extend(array.array("h", [0]) * add)
        prev = b
    out.extend(samples[prev:])
    return out


def run(slug: str, target: float, src: Path | None) -> int:
    src = src or (ROOT / "public" / "assets" / slug / "vo.mp3")
    if not src.exists():
        print(f"  no VO at {src}")
        return 1
    words = len((ROOT / "jobs" / slug / "script.md").read_text().split()) if slug else 0
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "in.wav"
        _decode(src, wav)
        with wave.open(str(wav)) as w:
            rate = w.getframerate()
            samples = array.array("h", w.readframes(w.getnframes()))
        before = len(samples) / rate
        gaps = silences(samples, rate)
        out = pad(samples, rate, gaps, target - before)
        after = len(out) / rate
        padded = Path(td) / "out.wav"
        with wave.open(str(padded), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
            w.writeframes(out.tobytes())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(padded),
                        "-map_metadata", "-1", "-c:a", "libmp3lame", "-b:a", "128k",
                        str(src)], check=True)
    print(f"\n=== VO pause-pad — {slug} ===\n")
    print(f"  before   {before:.1f}s   {words / before:.2f} w/s" if words else f"  before   {before:.1f}s")
    print(f"  gaps     {len(gaps)} silent runs >= {MIN_GAP}s, grown in proportion")
    print(f"  after    {after:.1f}s   {words / after:.2f} w/s" if words else f"  after    {after:.1f}s")
    print("\n  Words untouched — only the silence between them is longer.")
    print(f"  wrote {src.relative_to(ROOT)}\n")
    return 0


def demo() -> int:
    rate = 44100
    tone = array.array("h", [int(12000 * math.sin(i / 8)) for i in range(rate // 2)])
    quiet = array.array("h", [0]) * int(rate * 0.4)
    sig = tone + quiet + tone
    gaps = silences(sig, rate)
    assert len(gaps) == 1, f"expected one gap, got {gaps}"
    out = pad(sig, rate, gaps, 1.0)
    grew = (len(out) - len(sig)) / rate
    assert 0.9 < grew < 1.1, grew
    assert len(pad(sig, rate, [], 1.0)) == len(sig), "no gaps means no padding"
    # the speech itself must survive byte for byte
    assert sum(1 for s in out if s != 0) == sum(1 for s in sig if s != 0), "speech changed"
    print("vo_pad self-check passed — one gap found, padded by 1.0s, speech untouched")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--demo" in args:
        raise SystemExit(demo())
    if not args:
        raise SystemExit(__doc__)
    slug = args[0]
    target = float(args[args.index("--target") + 1]) if "--target" in args else 0.0
    src = Path(args[args.index("--in") + 1]) if "--in" in args else None
    if not target:
        raise SystemExit("  --target <seconds> is required: say how long the read should run.")
    raise SystemExit(run(slug, target, src))
