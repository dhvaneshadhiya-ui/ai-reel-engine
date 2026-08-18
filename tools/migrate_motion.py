#!/usr/bin/env python3
"""Snap spring configs and entrance durations onto the motion system.

Measured before writing it: 10 damping values, 16 stiffness values and 12
entrance durations across the components. Damping 17 beside 18, stiffness 140
beside 145, 13 frames beside 14 — differences no viewer perceives, which means
they were not decisions. Nothing shared a rhythm.

Each config is snapped to the NEAREST of the four roles in theme/motion.ts by
comparing damping and stiffness together, and each duration to the nearest of
three steps. Where a config is far from every role — a deliberate slow drift, a
bespoke bounce — it is HELD rather than flattened, because those are the ones
somebody actually tuned.

    python3 tools/migrate_motion.py            # what would change
    python3 tools/migrate_motion.py --write    # apply
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / "src/components"

ROLES = {
    "enter": (18, 150),
    "land": (14, 110),
    "soft": (22, 130),
    "draw": (26, 160),
    "pop": (14, 220),
}
DURS = {"quick": 8, "base": 14, "slow": 22}
# Beyond this normalised distance the config is somebody's deliberate choice.
MAX_DIST = 0.34

ARTIFACTS = {
    "SettingsPane.tsx", "XPost.tsx", "TerminalScene.tsx",
    "UIDialog.tsx", "DeviceFrame.tsx", "DesktopMockup.tsx",
}


def nearest_role(d: int, s: int) -> tuple[str, float]:
    best, bd = "enter", 9e9
    for name, (rd, rs) in ROLES.items():
        # normalise each axis by its own range so stiffness does not dominate
        dist = (((d - rd) / 12) ** 2 + ((s - rs) / 120) ** 2) ** 0.5
        if dist < bd:
            best, bd = name, dist
    return best, bd


def main() -> None:
    write = "--write" in sys.argv
    snapped = held = files = 0

    for f in sorted(COMPONENTS.glob("*.tsx")):
        if f.name in ARTIFACTS:
            continue
        src = f.read_text()
        out = src
        lines: list[str] = []

        for m in re.finditer(
                r"config: \{ *damping: (\d+), *stiffness: (\d+)(?:, *mass: ([\d.]+))? *\}", src):
            d, s = int(m.group(1)), int(m.group(2))
            role, dist = nearest_role(d, s)
            if dist > MAX_DIST:
                lines.append(f"     damping {d}/stiffness {s}  HELD — far from "
                             f"every role ({dist:.2f}); somebody tuned this")
                held += 1
                continue
            if (d, s) == ROLES[role]:
                continue
            lines.append(f"     damping {d}/stiffness {s:<3} -> {role}")
            out = out.replace(m.group(0), f"config: SPRING.{role}")
            snapped += 1

        for m in re.finditer(r"durationInFrames: (\d+)", src):
            n = int(m.group(1))
            if n in DURS.values():
                continue
            name = min(DURS, key=lambda k: abs(DURS[k] - n))
            if abs(DURS[name] - n) > 6:
                lines.append(f"     {n} frames  HELD — no step is close")
                held += 1
                continue
            lines.append(f"     {n} frames -> DUR.{name} ({DURS[name]})")
            out = out.replace(m.group(0), f"durationInFrames: DUR.{name}")
            snapped += 1

        if lines:
            print(f"\n  {f.name}")
            for l in lines:
                print(l)
        if write and out != src:
            if "theme/motion" not in out:
                out = out.replace('import React from "react";',
                                  'import React from "react";\n'
                                  'import { SPRING, DUR } from "../theme/motion";', 1)
            f.write_text(out)
            files += 1

    print(f"\n  {snapped} snapped, {held} held")
    if write:
        print(f"  rewrote {files} component(s)")
    else:
        print("  (--write to apply)")


if __name__ == "__main__":
    main()
