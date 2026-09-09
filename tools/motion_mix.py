#!/usr/bin/env python3
"""How much of a reel is actually MOVING — measured, not scene-detected.

WHY THIS IS NOT `ffmpeg select='gt(scene,N)'`
---------------------------------------------
Scene score is a CUT detector. It answers "did the picture change abruptly",
which is a different question from "is anything moving", and it has now misled
this repo twice. On 2026-09-08 it reported the Wisdom Loom reference reel
cutting every 0.85s against our 2.9s ceiling, which read as "they cut three
times faster than us". They do not: their beats run ~2.7s, essentially
identical to ours. The detector was firing on animation INSIDE a held beat.

So this measures displacement instead: mean per-pixel change between frames
sampled at 6fps on a 96x170 grayscale grid. That number is small when a card
sits still and large when a person or a street moves, which is the actual
quantity the eye is judging.

    python3 tools/motion_mix.py out/<slug>-final.mp4      # one render
    python3 tools/motion_mix.py --all                     # every render in out/
    python3 tools/motion_mix.py --selftest

THREE BANDS, and the middle one is the interesting one:
    near-static  <3    a card holding, a document with nothing sweeping
    animating    3-10  a highlight sweeping, a push-in, type landing
    live         >10   real footage, a person, a street

REFERENCE, measured 2026-09-08 on 4 Wisdom Loom shorts (2 hits, 2 flops):
near-static 8%-34%. Ours ran 15%-69% on the ten renders then on disk, with
seven of the ten above their worst. That gap is EDITORIAL, not a setting —
it is what happens when 41% of a reel is one document at a time. There is
deliberately NO THRESHOLD here and no gate: a check that fired at their 34%
ceiling would fire on eight of our ten reels, which per this repo's own
2026-09-08 lesson is a check describing a house style rather than a fault.
Read the number, then decide whether the story has anything live to show.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H, FPS = 96, 170, 6
REFERENCE = (0.08, 0.34)   # Wisdom Loom near-static share, n=4, 2026-09-08


def motion_series(path: Path) -> list[float]:
    """Mean per-pixel change between consecutive sampled frames."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path),
         "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
        capture_output=True)
    buf = r.stdout
    px = W * H
    n = len(buf) // px
    if n < 2:
        return []
    frames = [buf[i * px:(i + 1) * px] for i in range(n)]
    out = []
    for a, b in zip(frames, frames[1:]):
        out.append(sum(abs(x - y) for x, y in zip(a, b)) / px)
    return out


def mix(series: list[float]) -> tuple[float, float, float]:
    """(near-static, animating, live) as fractions of runtime."""
    if not series:
        return (0.0, 0.0, 0.0)
    n = len(series)
    lo = sum(1 for d in series if d < 3) / n
    hi = sum(1 for d in series if d > 10) / n
    return (lo, 1 - lo - hi, hi)


def report(path: Path) -> tuple[float, float, float]:
    lo, mid, hi = mix(motion_series(path))
    flag = "" if lo <= REFERENCE[1] else f"  (reference tops out at {REFERENCE[1]:.0%})"
    print(f"  {path.name[:38]:40} near-static {lo:5.0%}   animating {mid:5.0%}   "
          f"live {hi:5.0%}{flag}")
    return lo, mid, hi


def selftest() -> int:
    """The bands must actually separate a still from a moving picture."""
    ok = True
    still = [0.0] * 50
    moving = [22.0] * 50
    swept = [5.0] * 50
    for series, want, label in ((still, 0, "a frozen picture"),
                                (moving, 2, "real footage"),
                                (swept, 1, "a sweeping highlight")):
        got = mix(series).index(max(mix(series)))
        good = got == want
        ok &= good
        print(f"  {'ok  ' if good else 'FAIL'} {label} lands in band {want}")
    # and the middle band must not swallow the ends
    lo, mid, hi = mix([0.0] * 25 + [22.0] * 25)
    good = abs(lo - 0.5) < 0.02 and abs(hi - 0.5) < 0.02 and mid < 0.02
    ok &= good
    print(f"  {'ok  ' if good else 'FAIL'} a half-still half-live reel splits 50/50, "
          f"not into the middle")
    print("motion_mix selftest", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main() -> None:
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    if "--all" in args:
        files = sorted((ROOT / "out").glob("*-final.mp4"))
        if not files:
            sys.exit("no *-final.mp4 renders in out/")
        print(f"\n  {len(files)} render(s). Wisdom Loom reference near-static "
              f"{REFERENCE[0]:.0%}-{REFERENCE[1]:.0%} (n=4, 2026-09-08)\n")
        for f in files:
            report(f)
        print()
        return
    if not args:
        sys.exit(__doc__.strip().splitlines()[0] +
                 "\n  usage: motion_mix.py <render.mp4> | --all | --selftest")
    p = Path(args[0])
    if not p.is_absolute():
        p = ROOT / p
    if not p.exists():
        sys.exit(f"no such render: {p}")
    print()
    report(p)
    print()


if __name__ == "__main__":
    main()
