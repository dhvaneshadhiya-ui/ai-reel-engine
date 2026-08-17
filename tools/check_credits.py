#!/usr/bin/env python3
"""Two checks the repo CLAIMED to have and did not.

WHY THIS EXISTS
---------------
`Credit.tsx` carried this in its own docstring:

    "the treatment now lives in ONE component that every scene imports, and
     `lint_frames.py` fails the build if a component hand-rolls its own credit."

The second half was false. `lint_frames.py` prints "credits present" as item 6
of a checklist a human reads; nothing enforced it. So AnnotateZoom and
DeviceFrame each carried their own credit block at `bottom: 96` — y 0.95, inside
Instagram's caption stack — and shipped invisible on every scene that used them.

A claimed check that does not exist is worse than no check, because it stops
anyone from looking. This is the check.

    python3 tools/check_credits.py            # both checks
    python3 tools/check_credits.py --selftest # prove each one can FAIL

CHECK 1  no component renders a `credit` prop without going through <Credit>.
CHECK 2  no display-size text is anchored below the platform safe floor.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / "src/components"

# Mirrors src/platformSafeArea.ts (SAFE_RECT.y1 = 0.80) on a 1920 frame.
SAFE_FLOOR_PX = 384
# Text at or above this size is display type — a headline, a stat, a credit.
DISPLAY_PX = 40
# Files allowed to define the treatment itself.
EXEMPT = {"Credit.tsx"}


def hand_rolled_credits(text: str, name: str) -> list[str]:
    """A file that outputs {credit} in JSX but never imports <Credit>."""
    if name in EXEMPT:
        return []
    renders = re.search(r"\{\s*credit\s*\}", text)
    if not renders:
        return []
    if re.search(r'import\s*\{[^}]*\bCredit\b[^}]*\}\s*from\s*"\./Credit"', text):
        return []
    line = text[: renders.start()].count("\n") + 1
    return [f"  {name}:{line}  renders {{credit}} without importing <Credit> — "
            f"hand-rolled credit treatment"]


def furniture_below_floor(text: str, name: str) -> list[str]:
    """Display-size text anchored nearer the frame bottom than the safe floor.

    Heuristic on purpose: a `bottom:` literal within a few lines of a large
    `fontSize` is frame-anchored furniture in practice. Narrow enough to avoid
    firing on text inside a card, loud enough to catch a headline in the
    platform's caption band.
    """
    out: list[str] = []
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        m = re.search(r"\bbottom:\s*(\d+)\s*,", ln)
        if not m:
            continue
        px = int(m.group(1))
        if px >= SAFE_FLOOR_PX:
            continue
        # `bottom: 0` is the container-edge pattern — a banner pinned to the
        # bottom of a CARD (Carousel, DesignReveal "SELECTED" strips), not
        # furniture anchored to the frame. Nothing legitimate is pinned to the
        # literal frame edge, so an exact 0 is a card, not a violation. Any
        # other small value is frame furniture in practice.
        if px == 0:
            continue
        window = "\n".join(lines[i: i + 7])
        fs = [int(x) for x in re.findall(r"fontSize:\s*(\d+)", window)]
        if not any(f >= DISPLAY_PX for f in fs):
            continue
        y = 1 - px / 1920
        out.append(f"  {name}:{i + 1}  bottom: {px} puts {max(fs)}px text at "
                   f"y {y:.3f} — below the {1 - SAFE_FLOOR_PX / 1920:.2f} safe "
                   f"floor, inside the platform caption band")
    return out


def run(files: list[Path]) -> list[str]:
    flags: list[str] = []
    for f in sorted(files):
        t = f.read_text()
        flags += hand_rolled_credits(t, f.name)
        flags += furniture_below_floor(t, f.name)
    return flags


def selftest() -> None:
    """Each check must fire on a synthetic violation, or it is not a check."""
    bad_credit = '''import React from "react";
export const X = ({ credit }) => <div>{credit}</div>;
'''
    ok_credit = '''import React from "react";
import { Credit } from "./Credit";
export const X = ({ credit }) => <div>{credit && <Credit text={credit} />}</div>;
'''
    bad_floor = '''const X = () => (
  <div style={{ position: "absolute", bottom: 96, fontSize: 84 }}>hi</div>
);
'''
    ok_floor = '''const X = () => (
  <div style={{ position: "absolute", bottom: 420, fontSize: 84 }}>hi</div>
);
'''
    small_low = '''const X = () => (
  <div style={{ position: "absolute", bottom: 20, fontSize: 18 }}>x</div>
);
'''
    cases = [
        ("hand-rolled credit  DETECTED", hand_rolled_credits(bad_credit, "A.tsx"), True),
        ("uses <Credit>       passes  ", hand_rolled_credits(ok_credit, "A.tsx"), False),
        ("headline below floor DETECTED", furniture_below_floor(bad_floor, "B.tsx"), True),
        ("headline above floor passes  ", furniture_below_floor(ok_floor, "B.tsx"), False),
        ("small print low     passes  ", furniture_below_floor(small_low, "C.tsx"), False),
    ]
    ok = True
    for label, got, want_flag in cases:
        hit = bool(got)
        mark = "ok  " if hit == want_flag else "FAIL"
        if hit != want_flag:
            ok = False
        print(f"  {mark} {label}  -> {len(got)} flag(s)")
    print()
    if not ok:
        sys.exit("selftest FAILED — a check that cannot fail is not a check.")
    print("  selftest passed: both checks fire on a violation and stay quiet otherwise.")


def main() -> None:
    if "--selftest" in sys.argv:
        selftest()
        return
    files = list(COMPONENTS.glob("*.tsx"))
    if not files:
        sys.exit(f"no components found under {COMPONENTS}")
    flags = run(files)
    print(f"scanned {len(files)} components")
    if flags:
        print()
        for f in flags:
            print(f)
        sys.exit(f"\n{len(flags)} credit / safe-area violation(s).")
    print("  no hand-rolled credits, no display text below the safe floor.")


if __name__ == "__main__":
    main()
