#!/usr/bin/env python3
"""Find colours that came from nowhere.

WHY
---
On 2026-08-18 the user said, of a published reel: "I don't like this sort of
orange color." The orange was not in either style pack. It was line 18 of
HeadlineBuild.tsx:

    const ACCENT = "#d97757"; // Anthropic clay

in a file whose own theme contract reads "Components must use this — never
hardcode colors". It got there for a defensible reason (the editorial accent is
amber, and amber text on a bright frame is unreadable), was applied to BOTH
grounds, and then shipped as the loudest colour in the reel's final frame.

theme/tokens.ts now derives the two text-safe accent variants from the ONE
declared accent, so the reason for reaching past the theme is gone. This makes
the reaching visible when it happens again.

    python3 tools/check_palette.py            # every off-palette colour
    python3 tools/check_palette.py --worst    # the components to fix first

ADVICE, never blocking. A colour genuinely outside the palette is legitimate —
a scrim, a shadow, a recreated iOS control that has to match iOS. This does not
decide which is which; it makes each one a thing somebody chose on purpose
rather than a thing nobody can find.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / "src/components"

# Everything the style packs declare, plus the neutrals every scene needs.
# Kept in step with src/theme/tokens.ts by hand — if that file grows a colour,
# this list grows with it in the same commit.
PALETTE = {
    "#f4f0e6", "#0a0a0a", "#ffffff", "#ffd84d", "#141414", "#f5f2ea",
    "#efe9dc", "#0d0d0d", "#e0785a", "#181512", "#f2ede3",
    "#000000", "#fff", "#000",
}

# Files that RECREATE another system's interface. Their colours belong to that
# interface — an iOS toggle is #34c759 or it is not an iOS toggle. Kept in step
# with tools/check_type.py, which exempts the same set for the same reason.
EXEMPT = {
    "SettingsPane.tsx",     # an iOS Settings pane
    "XPost.tsx",            # a tweet
    "TerminalScene.tsx",    # a macOS terminal window
    "UIDialog.tsx",         # an app dialog recreation
    "DeviceFrame.tsx",      # device / browser chrome
    "DesktopMockup.tsx",    # browser chrome
}

HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def main() -> None:
    worst = "--worst" in sys.argv
    rows = []
    for f in sorted(COMPONENTS.glob("*.tsx")):
        if f.name in EXEMPT:
            continue
        off = []
        for i, line in enumerate(f.read_text().splitlines(), 1):
            # a hex inside a comment is documentation, usually of this exact
            # problem — flagging it would make the write-up the violation
            stripped = line.strip()
            if stripped.startswith(("*", "//", "/*")):
                continue
            for m in HEX.findall(line):
                if m.lower() not in PALETTE:
                    off.append((i, m))
        if off:
            rows.append((f.name, off))

    if not rows:
        print("\n  every component colour comes from the palette.\n")
        return

    rows.sort(key=lambda r: -len(r[1]))
    total = sum(len(r[1]) for r in rows)
    print(f"\n  {len(rows)} component(s) carry {total} off-palette colour(s)\n")
    for name, off in (rows[:8] if worst else rows):
        seen: list[str] = []
        for _, h in off:
            if h.lower() not in [s.lower() for s in seen]:
                seen.append(h)
        first = off[0][0]
        print(f"  {name:24} {len(off):>3} use(s)  {', '.join(seen[:6])}"
              f"{'...' if len(seen) > 6 else ''}   first at :{first}")
    if worst and len(rows) > 8:
        print(f"  ... and {len(rows) - 8} more")
    print("\n  ADVICE — a scrim, a shadow or a recreated control is allowed an "
          "off-palette\n  colour. This only makes the choice visible. Brand "
          "colour belongs in\n  theme/tokens.ts, where accentInk / accentOnDark "
          "are derived from it.\n")


if __name__ == "__main__":
    main()
