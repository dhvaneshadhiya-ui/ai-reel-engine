#!/usr/bin/env python3
"""Measure a reference video so a FORMATS profile can be DERIVED, not guessed.

G23: "every number in a profile must come from a real teardown of reference
reels". This is that teardown, as a command — cut rhythm from scene detection,
speech rate from the caption track, beat lengths from the publisher's own
chapters. It prints one row per video plus a pooled summary, so a new genre's
band is a number with a provenance instead of an impression.

    python3 tools/measure_video.py <file.mp4> [more.mp4 ...] [--threshold 0.15] [--faces]

Expects, beside each video (as yt-dlp writes them):
    <name>.en.vtt          auto-captions  -> words/sec, speech density
    <name>.info.json       metadata       -> chapters, title, duration

`--faces` measures PRESENTER SHARE with Apple's Vision framework (needs Xcode,
which is on this machine since 2026-09-24): one frame every 10s, a face counted
only when it is at least FACE_MIN of the frame height, so a face inside a
screenshot or a video thumbnail does not read as a presenter. Added because the
first longform teardown eyeballed this number off a contact sheet and three of
four style calls made that way were wrong.

Self-check: python3 tools/measure_video.py --demo
"""
from __future__ import annotations

import json
import math
import re
import statistics as st
import shutil
import subprocess
import sys
from pathlib import Path


def cuts(path: Path, threshold: float) -> list[float]:
    """Seconds at which ffmpeg's scene detector sees a cut."""
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf",
         f"select='gt(scene,{threshold})',metadata=print:file=-", "-an", "-f", "null", "-"],
        capture_output=True, text=True).stdout
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", out)]


def vtt_words(path: Path) -> list[tuple[float, str]]:
    """(start_seconds, text) from a WebVTT caption file, de-duplicated —
    YouTube's auto-captions repeat each line as a rolling two-line window."""
    if not path.exists():
        return []
    rows, seen = [], set()
    t = None
    for line in path.read_text(errors="ignore").splitlines():
        m = re.match(r"(\d\d):(\d\d):(\d\d)\.(\d+)\s+-->", line)
        if m:
            h, mnt, s, ms = (int(x) for x in m.groups())
            t = h * 3600 + mnt * 60 + s + ms / 1000
            continue
        s = re.sub(r"<[^>]+>", "", line).strip()
        if t is not None and s and not s.startswith(("WEBVTT", "Kind:", "Language:")):
            if s not in seen:
                seen.add(s)
                rows.append((t, s))
    return rows


def chapters(info: Path) -> list[tuple[str, float]]:
    if not info.exists():
        return []
    d = json.loads(info.read_text())
    ch = d.get("chapters") or []
    return [(c.get("title", "?"), float(c["end_time"]) - float(c["start_time"])) for c in ch]


FACE_MIN = 0.10      # a presenter fills >=10% of frame height; a face in a
                     # screenshot does not (measured: Hayls presenter 0.21)


def face_share(path: Path, dur: float, every: float = 10.0) -> float | None:
    """Share of sampled frames with a presenter-sized face, via Vision.
    None when the helper cannot run (no swift / not macOS)."""
    helper = Path(__file__).resolve().parent / "face_frames.swift"
    if not helper.exists() or not shutil.which("swift"):
        return None
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf",
                        f"fps=1/{every}", f"{td}/f%04d.png"], check=True)
        shots = sorted(Path(td).glob("*.png"))
        if not shots:
            return None
        out = subprocess.run(["swift", str(helper), *map(str, shots)],
                             capture_output=True, text=True).stdout
        hits = 0
        for line in out.strip().splitlines():
            parts = line.split("\t")
            if len(parts) == 3 and float(parts[2]) >= FACE_MIN:
                hits += 1
        return hits / len(shots)


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def shot_lengths(cut_times: list[float], dur: float) -> list[float]:
    marks = [0.0] + cut_times + [dur]
    return [b - a for a, b in zip(marks, marks[1:]) if b > a]


def measure(path: Path, threshold: float, want_faces: bool = False) -> dict:
    stem = path.with_suffix("")
    dur = duration(path)
    sh = shot_lengths(cuts(path, threshold), dur)
    rows = vtt_words(Path(f"{stem}.en.vtt"))
    words = sum(len(s.split()) for _, s in rows)
    chs = chapters(Path(f"{stem}.info.json"))
    # speech density: share of 10s buckets that carry any words at all
    buckets = {int(t // 10) for t, _ in rows}
    return {
        "name": stem.name, "dur": dur, "shots": len(sh),
        "shot_p50": st.median(sh) if sh else 0,
        "shot_p75": st.quantiles(sh, n=4)[2] if len(sh) > 3 else (max(sh) if sh else 0),
        "shot_max": max(sh) if sh else 0,
        "words": words, "wps": words / dur if dur else 0,
        "talk_share": len(buckets) / max(1, math.ceil(dur / 10)),
        "chapters": len(chs),
        "chap_p50": st.median([d for _, d in chs]) if chs else 0,
        "chap_min": min([d for _, d in chs], default=0),
        "chap_max": max([d for _, d in chs], default=0),
        "face": face_share(path, dur) if want_faces else None,
    }


def report(rows: list[dict]) -> None:
    print(f"\n{'video':<18}{'dur':>7}{'shots':>7}{'s/cut p50':>11}{'p75':>7}{'longest':>9}"
          f"{'w/s':>7}{'talk%':>7}{'chaps':>7}{'chap p50':>10}{'face%':>8}")
    for r in rows:
        print(f"{r['name']:<18}{r['dur']:>6.0f}s{r['shots']:>7}{r['shot_p50']:>11.1f}"
              f"{r['shot_p75']:>7.1f}{r['shot_max']:>9.1f}{r['wps']:>7.2f}"
              f"{r['talk_share']*100:>6.0f}%{r['chapters']:>7}{r['chap_p50']:>9.0f}s"
              + (f"{r['face']*100:>7.0f}%" if r["face"] is not None else f"{'—':>8}"))
    if len(rows) > 1:
        pool = lambda k: st.median([r[k] for r in rows])
        print(f"\n  POOLED MEDIAN  runtime {pool('dur'):.0f}s · shot p50 {pool('shot_p50'):.1f}s · "
              f"shot p75 {pool('shot_p75'):.1f}s · {pool('wps'):.2f} w/s · "
              f"talk {pool('talk_share')*100:.0f}% · chapter {pool('chap_p50'):.0f}s")
    if any(r["face"] is not None for r in rows):
        print("\n  face% = frames (1 per 10s) carrying a face >= 10% of frame height — a "
              "presenter,\n  not a face inside a screenshot. Layout is still yours to read.\n")
    else:
        print("\n  Cut rhythm is MEASURED; face share is not — pass --faces, or read frames.\n")


def demo() -> int:
    assert shot_lengths([2.0, 5.0], 10.0) == [2.0, 3.0, 5.0]
    assert shot_lengths([], 8.0) == [8.0], "no cuts means one shot"
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        v = Path(td) / "x.en.vtt"
        v.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nhello there\n\n"
                     "00:00:03.000 --> 00:00:05.000\nhello there\n\n"   # rolling repeat
                     "00:00:05.000 --> 00:00:07.000\nsecond line\n")
        rows = vtt_words(v)
        assert [s for _, s in rows] == ["hello there", "second line"], rows
        assert rows[0][0] == 1.0 and rows[1][0] == 5.0, rows
    print("measure_video self-check passed — shot split, and rolling captions de-duplicated")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    if "--demo" in args:
        raise SystemExit(demo())
    th = 0.15
    if "--threshold" in args:
        i = args.index("--threshold"); th = float(args[i + 1]); del args[i:i + 2]
    if not args:
        raise SystemExit(__doc__)
    faces = "--faces" in args
    args = [a for a in args if a != "--faces"]
    report([measure(Path(a), th, faces) for a in args])
