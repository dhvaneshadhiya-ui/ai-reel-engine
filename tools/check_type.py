#!/usr/bin/env python3
"""Find type that is off the scale.

WHY
---
Measured 2026-08-18, before src/theme/type.ts existed: 41 distinct font sizes and
7 weights across 38 components. Sizes one and two pixels apart — 17, 19, 20, 22,
24, 26, 27, 28, 30, 32, 33, 34, 36, 38, 40, 42, 44, 46, 48... Nobody chose those;
they accumulated, because every component assembled its own type in isolation.

A type scale only holds if going off it is visible. This lists every size and
weight that is not on the scale, so the remaining components can be migrated
deliberately instead of discovered later in a render.

    python3 tools/check_type.py            # what is still off-scale
    python3 tools/check_type.py --worst    # the components to migrate first

ADVICE, never blocking. A scene that genuinely needs an off-scale size can have
one — typeAt() exists for that. This just makes the exception visible instead of
letting it pass for a decision.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / "src/components"

# Mirrors src/theme/type.ts. If the scale moves, move it here in the same commit.
SIZES = {28, 36, 46, 60, 78, 100, 130}
WEIGHTS = {400, 600, 700, 800, 900}
# Files that legitimately define the system, or draw type as GRAPHICS rather
# than set it as text.
# Components that RECREATE another system's interface. Their type belongs to
# that interface, not to us: forcing our scale onto a rebuilt iOS row or a tweet
# would break the recreation, which is the only reason they exist. Kept in step
# with tools/migrate_type.py.
EXEMPT = {
    "Credit.tsx",
    "SettingsPane.tsx",     # an iOS Settings pane
    "XPost.tsx",            # a tweet
    "TerminalScene.tsx",    # a macOS terminal window
    "UIDialog.tsx",         # an app dialog recreation
    "DeviceFrame.tsx",      # device / browser chrome
    "DesktopMockup.tsx",    # browser chrome
}


def main() -> None:
    worst = "--worst" in sys.argv
    rows = []
    for f in sorted(COMPONENTS.glob("*.tsx")):
        if f.name in EXEMPT:
            continue
        src = f.read_text()
        sizes = [int(m) for m in re.findall(r"fontSize: (\d+)", src)]
        weights = [int(m) for m in re.findall(r"fontWeight: (\d+)", src)]
        off_s = sorted({s for s in sizes if s not in SIZES})
        off_w = sorted({w for w in weights if w not in WEIGHTS})
        uses_scale = "theme/type" in src
        if off_s or off_w:
            rows.append((f.name, off_s, off_w, uses_scale, len(sizes)))

    if not rows:
        print("\n  every component is on the scale.\n")
        return

    rows.sort(key=lambda r: -(len(r[1]) + len(r[2])))
    total_off = sum(len(r[1]) for r in rows)
    print(f"\n  {len(rows)} component(s) carry off-scale type "
          f"({total_off} distinct sizes)\n")
    show = rows[:8] if worst else rows
    for name, off_s, off_w, uses_scale, n in show:
        mark = "partly migrated" if uses_scale else ""
        print(f"  {name:24} {len(off_s):>2} sizes  {str(off_s[:9])[:46]:48}{mark}")
        if off_w:
            print(f"  {'':24} weights {off_w}")
    if worst and len(rows) > 8:
        print(f"  ... and {len(rows) - 8} more")
    print(f"\n  scale: {sorted(SIZES)}   weights: {sorted(WEIGHTS)}")
    print("  ADVICE — typeAt() exists for a scene that genuinely needs another "
          "size.\n  This only makes the exception visible.\n")


if __name__ == "__main__":
    main()
