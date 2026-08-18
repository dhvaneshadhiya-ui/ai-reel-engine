#!/usr/bin/env python3
"""Move components onto the type scale — the safe ones automatically, the rest by hand.

TWO KINDS OF TYPE, and only one of them is ours
-----------------------------------------------
Some components RECREATE another system's interface: SettingsPane is an iOS
Settings pane, XPost is a tweet, TerminalScene says of itself "a rendered macOS
terminal window (not a screenshot)", UIDialog is "an app-dialog recreation",
DeviceFrame and DesktopMockup draw browser chrome. Their type has to look like
the thing they imitate. Forcing our editorial scale onto a recreated iOS row
would break the recreation, which is the only reason those components exist.

So the scale governs OUR layer. The artifacts are exempt, by name, with reasons.

WHAT IT WILL NOT DO
-------------------
Snap a size when the jump is big enough to break a layout. 17px -> 28px is +65%:
that text was sized to fit a card, and a tool that "migrates" it has silently
rewritten a design. Anything over MAX_JUMP is listed for a human instead.

    python3 tools/migrate_type.py            # what would change
    python3 tools/migrate_type.py --write    # apply the safe ones
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / "src/components"

SCALE = [28, 36, 46, 60, 78, 100, 130]
MAX_JUMP = 0.25          # beyond this, a snap is a redesign, not a migration

# Recreations of somebody else's UI. Their type belongs to that UI, not to us.
ARTIFACTS = {
    "SettingsPane.tsx": "an iOS Settings pane",
    "XPost.tsx": "a tweet",
    "TerminalScene.tsx": "a macOS terminal window",
    "UIDialog.tsx": "an app dialog recreation",
    "DeviceFrame.tsx": "device / browser chrome",
    "DesktopMockup.tsx": "browser chrome",
}
# Already on the system.
DONE = {"HeadlineBuild.tsx", "Credit.tsx", "CaptionChips.tsx"}


def nearest(px: int) -> tuple[int, float]:
    best = min(SCALE, key=lambda s: abs(s - px))
    return best, (best - px) / px


def main() -> None:
    write = "--write" in sys.argv
    applied = held = 0
    touched_files = 0

    for f in sorted(COMPONENTS.glob("*.tsx")):
        if f.name in DONE:
            continue
        if f.name in ARTIFACTS:
            print(f"  {f.name:22} EXEMPT — {ARTIFACTS[f.name]}")
            continue
        src = f.read_text()
        sizes = sorted({int(m) for m in re.findall(r"fontSize: (\d+)", src)})
        off = [s for s in sizes if s not in SCALE]
        if not off:
            continue

        safe, risky = [], []
        for s in off:
            to, jump = nearest(s)
            (safe if abs(jump) <= MAX_JUMP else risky).append((s, to, jump))

        print(f"\n  {f.name}")
        for s, to, j in safe:
            print(f"     {s:>4} -> {to:<4} {j:+6.0%}")
        for s, to, j in risky:
            print(f"     {s:>4} -> {to:<4} {j:+6.0%}   HELD — a jump this size "
                  "is a redesign; size it by hand")
        applied += len(safe)
        held += len(risky)

        if write and safe:
            out = src
            for s, to, _j in safe:
                # word-boundary so 22 never matches inside 220
                out = re.sub(rf"fontSize: {s}\b", f"fontSize: {to}", out)
            if out != src:
                f.write_text(out)
                touched_files += 1

    print(f"\n  {applied} size(s) snap to the scale, {held} held for a human")
    if write:
        print(f"  rewrote {touched_files} component(s)")
    else:
        print("  (--write to apply the safe ones)")


if __name__ == "__main__":
    main()
