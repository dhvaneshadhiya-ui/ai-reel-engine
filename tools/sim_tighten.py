#!/usr/bin/env python3
"""Shorten the frozen stretches in a simulator screen recording.

Driving the iOS simulator through the MCP panel lags a second or more per tap,
so a 15-second tap path records as a minute of mostly still screen. mpdecimate
was tried first and silently dropped whole navigation steps (a push animation
reads as "near-duplicate" to it). This keeps every moving frame and only caps
each still stretch at --hold seconds, so every screen the viewer should see is
still in the clip, just without the wait.

    python3 tools/sim_tighten.py in.mp4 out.mp4 [--hold 0.6] [--min 0.8]

Self-check: python3 tools/sim_tighten.py --demo
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def freezes(src: Path, min_s: float) -> list[tuple[float, float]]:
    """(start, end) of every still stretch at least min_s long."""
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(src), "-vf",
         f"freezedetect=n=-60dB:d={min_s}", "-map", "0:v", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", err)]
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
    ends += [dur] * (len(starts) - len(ends))   # still at the very end
    return list(zip(starts, ends))


def keep_spans(dur: float, still: list[tuple[float, float]],
               hold: float) -> list[tuple[float, float]]:
    """Everything that moves, plus the first `hold` seconds of each still."""
    spans, t = [], 0.0
    for a, b in still:
        if a > t:
            spans.append((t, a))
        spans.append((a, min(b, a + hold)))
        t = b
    if t < dur:
        spans.append((t, dur))
    return [(a, b) for a, b in spans if b - a > 0.01]


def tighten(src: Path, dst: Path, hold: float, min_s: float) -> float:
    # simctl recordVideo is VARIABLE frame rate: a still screen writes no frames
    # at all, so a select on t then keeps the wrong ones. Make it CFR first.
    cfr = Path(tempfile.mkdtemp()) / "cfr.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-r", "30",
                    "-fps_mode", "cfr", "-an", "-c:v", "libx264", "-crf", "14",
                    "-pix_fmt", "yuv420p", str(cfr)], check=True)
    src = cfr
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
    spans = keep_spans(dur, freezes(src, min_s), hold)
    sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in spans)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf",
         f"select='{sel}',setpts=N/30/TB", "-r", "30", "-fps_mode", "cfr",
         "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
         str(dst)], check=True)
    return sum(b - a for a, b in spans)


def demo() -> int:
    # 3 still seconds, a 1s colour change, 3 still seconds -> about 0.6+1+0.6
    with tempfile.TemporaryDirectory() as td:
        src, out = Path(td) / "in.mp4", Path(td) / "out.mp4"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
             "color=c=white:s=120x240:d=3:r=30", "-f", "lavfi", "-i",
             "testsrc=s=120x240:d=1:r=30", "-f", "lavfi", "-i",
             "color=c=black:s=120x240:d=3:r=30", "-filter_complex",
             "[0][1][2]concat=n=3:v=1", "-pix_fmt", "yuv420p", str(src)],
            check=True)
        kept = tighten(src, out, 0.6, 0.8)
        assert 1.8 < kept < 2.6, kept
        assert keep_spans(10, [], 0.6) == [(0.0, 10)], "no stills -> untouched"
    print(f"sim_tighten self-check passed — 7s of mostly-still video kept {kept:.1f}s")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--demo" in a:
        raise SystemExit(demo())
    if len(a) < 2:
        raise SystemExit(__doc__)
    hold = float(a[a.index("--hold") + 1]) if "--hold" in a else 0.6
    mn = float(a[a.index("--min") + 1]) if "--min" in a else 0.8
    kept = tighten(Path(a[0]), Path(a[1]), hold, mn)
    print(f"  kept {kept:.1f}s -> {a[1]}")
