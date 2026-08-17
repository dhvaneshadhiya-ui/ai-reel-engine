#!/usr/bin/env python3
"""Measure how much a HeyGen look actually MOVES, and register the result.

WHY: a still photo tells you nothing about motion. Look `0aa05d6e` (blue
hoodie) and `48d4076` (black hoodie) are the same person, same engine, same
parameters — and differ by 6.4x in hand movement. The only way to know is to
render a few seconds and measure it (STYLE-RULES 2026-08-12).

    # measure a rendered test clip and print the score
    python3 tools/measure_avatar.py score out/gesture-ref/testA.mp4

    # same, and write it into config.json's avatar registry
    python3 tools/measure_avatar.py score clip.mp4 --register 48d4076... \
        --name "Man in black hoodie recording" --engine avatar_v

    # show the registry, best-moving first
    python3 tools/measure_avatar.py list

    # switch the default presenter (refuses anything measured as frozen)
    python3 tools/measure_avatar.py use 0aa05d6e90e74f9fa23b75d0d8c267c4

A single reel can override the default without touching config: put
`"avatar": "<look id>"` in that reel's public/assets/<slug>/manifest.json.

SCORE = mean frame-to-frame luminance delta across the hand region (the lower
~29% of frame). Guide, from measured reels:
    < 1.0   frozen presenter — do not ship
    1.0-2.5 stiff; usable only in short pops
    > 3.0   genuinely gestures
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.json"

FROZEN, STIFF = 1.0, 2.5


def score(clip: Path, sample_fps: float = 6.0) -> tuple[float, float]:
    """(mean, peak) frame-to-frame delta in the hand region."""
    try:
        from PIL import Image, ImageChops
    except ImportError:
        sys.exit("FATAL: pillow required — pip3 install pillow")
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(clip)],
        capture_output=True, text=True)
    w, h = (int(x) for x in probe.stdout.strip().split(",")[:2])
    crop_h = int(h * 0.29)
    crop_y = h - crop_h
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf",
             f"fps={sample_fps},crop={w}:{crop_h}:0:{crop_y},scale=200:-1",
             f"{td}/%04d.png"], check=True)
        frames = sorted(Path(td).glob("*.png"))
        if len(frames) < 3:
            sys.exit("clip too short to measure — use at least ~3 seconds")
        vals = []
        for a, b in zip(frames, frames[1:]):
            ia = Image.open(a).convert("L")
            ib = Image.open(b).convert("L")
            px = list(ImageChops.difference(ia, ib).getdata())
            vals.append(sum(px) / len(px))
    return sum(vals) / len(vals), max(vals)


def verdict(mean: float) -> str:
    if mean < FROZEN:
        return "FROZEN — do not ship"
    if mean < STIFF:
        return "stiff — short pops only"
    return "gestures"


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    cfg = json.loads(CONFIG.read_text())
    registry = cfg.setdefault("avatarRegistry", {})

    if cmd == "list":
        if not registry:
            sys.exit("registry empty — measure a look first")
        rows = sorted(registry.items(), key=lambda kv: -kv[1].get("motion", 0))
        print(f"{'MOTION':>7}  {'VERDICT':<24} {'ENGINE':<10} NAME")
        for aid, m in rows:
            mark = "*" if aid == cfg["avatar"]["avatarId"] else " "
            print(f"{m.get('motion', 0):7.2f}  {verdict(m.get('motion', 0)):<24} "
                  f"{m.get('engine', '?'):<10} {mark}{m.get('name', aid)}")
        print("\n* = current default in config.avatar.avatarId")
        return

    if cmd == "use":
        aid = sys.argv[2]
        if aid not in registry:
            sys.exit(f"{aid} is not measured yet — run `score` with --register first")
        m = registry[aid]
        if m["motion"] < FROZEN:
            sys.exit(f"refusing: {m['name']} scores {m['motion']} — {verdict(m['motion'])}")
        cfg["avatar"]["avatarId"] = aid
        cfg["avatar"]["engine"] = m.get("engine", "avatar_v")
        if m.get("needsMotionPrompt"):
            cfg["avatar"]["expressiveness"] = "high"
            cfg["avatar"]["useMotionPrompt"] = True
        else:
            cfg["avatar"].pop("expressiveness", None)
            cfg["avatar"]["useMotionPrompt"] = False
        CONFIG.write_text(json.dumps(cfg, indent=2))
        print(f"default avatar -> {m['name']} ({m['motion']}, {m.get('engine')})")
        return

    if cmd != "score":
        sys.exit(__doc__)

    clip = Path(sys.argv[2])
    if not clip.exists():
        sys.exit(f"no such clip: {clip}")
    mean, peak = score(clip)
    print(f"{clip.name}: motion {mean:.2f} (peak {peak:.2f}) -> {verdict(mean)}")

    if "--register" in sys.argv:
        aid = sys.argv[sys.argv.index("--register") + 1]
        name = (sys.argv[sys.argv.index("--name") + 1]
                if "--name" in sys.argv else aid)
        engine = (sys.argv[sys.argv.index("--engine") + 1]
                  if "--engine" in sys.argv else "avatar_v")
        entry = registry.setdefault(aid, {})
        entry.update({"name": name, "motion": round(mean, 2),
                      "peak": round(peak, 2), "engine": engine,
                      "verdict": verdict(mean)})
        if "--motion-prompt" in sys.argv:
            entry["needsMotionPrompt"] = True
        CONFIG.write_text(json.dumps(cfg, indent=2))
        print(f"registered {name} ({aid[:8]}…) at motion {mean:.2f}")


if __name__ == "__main__":
    main()
