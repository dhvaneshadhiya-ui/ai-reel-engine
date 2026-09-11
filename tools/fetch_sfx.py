#!/usr/bin/env python3
"""Fetch the ACTION sounds onto this machine. They are never committed.

WHY A FETCH, NOT A FOLDER IN GIT
--------------------------------
Our library is genre sounds (whoosh, impact, riser). These are the sound of
the ACTION on screen: a marker pen for an ink mark, paper for a card landing,
a lens for the magnifier, a lock for a counter settling. The idea is from
video-talkcraft's effect library (every one of its 108 effects has a cue);
the sounds themselves are Mixkit's, picked by us.

Mixkit's Sound Effects Free License allows commercial use in finished videos
but says: "You can't redistribute the Item on its own, as stock, in a tool or
template, or with source files." This repo is a tool, and public. So each
machine downloads them straight from Mixkit, `.gitignore` keeps them out of
git, and the committed thing is only this list: id, name, size.

    python3 tools/fetch_sfx.py            # fetch what is missing, verify all
    python3 tools/fetch_sfx.py --check    # exit 1 if any is missing (doctor)

setup.sh runs it, so a new machine gets them with everything else.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "public" / "sfx-action"
URL = "https://assets.mixkit.co/active_storage/sfx/{id}/{id}-preview.mp3"

# file -> (Mixkit id, Mixkit title, bytes at 2026-09-11). Titles matched to ids
# card by card on mixkit.co; the size is the check that the same file came down.
SOUNDS = {
    "marker.mp3":      (2998, "Pen marker line",        39045),
    "paper-slide.mp3": (1530, "Paper slide",            37161),
    "paper-quick.mp3": (2380, "Paper quick movement",   31682),
    "lens-zoom.mp3":   (2617, "UI zoom in",             20458),
    "lock.mp3":        (2854, "Quick lock sound",       37894),
    "tick.mp3":        (1061, "Clock ticker single",    20508),
    "typekey.mp3":     (1382, "Mechanical typewriter single hit", 21398),
}


def missing() -> list[str]:
    return [f for f in SOUNDS if not (DEST / f).exists()]


def fetch() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    bad = 0
    for name, (sid, title, size) in SOUNDS.items():
        out = DEST / name
        if not out.exists():
            req = urllib.request.Request(URL.format(id=sid), headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                out.write_bytes(r.read())
        got = out.stat().st_size
        ok = size is None or got == size
        bad += not ok
        print(f"  {'ok  ' if ok else 'SIZE'} {name:16} {got:>6} B  Mixkit {sid} \"{title}\"")
    return 1 if bad else 0


def main() -> None:
    if "--check" in sys.argv:
        m = missing()
        if m:
            sys.exit("action sounds missing on this machine: " + ", ".join(m) +
                     " — run `python3 tools/fetch_sfx.py` (downloads from Mixkit).")
        print(f"action sounds ok — {len(SOUNDS)} present.")
        return
    sys.exit(fetch())


if __name__ == "__main__":
    main()
