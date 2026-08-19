#!/usr/bin/env python3
"""Which constraints are still earning their keep?

WHY THIS EXISTS (2026-08-19)
----------------------------
Four times in one day, something that cost real time turned out to be a
workaround whose reason had already been removed:

    --concurrency=2      guarded against a Fraunces loadFont() delayRender
                         timeout, fixed 2026-08-16 by moving to @font-face.
                         Cost: every render ran at a quarter speed, 390s
                         instead of 165s.
    flo() / floatcard    avoided ReceiptScene's zoom floor overflowing wide
                         captures. The floor was capped the previous day.
                         Cost: SEVEN of eight build scripts could not run.
    receipt for stills   same cause, same day.
    LINE_MAX_CHARS       a character budget calibrated for Fraunces, still
                         enforced after the display face changed to a wider
                         one. Cost: six headlines overflow with a clean build.

Every one was correct when written. Every one was DOCUMENTED, honestly, with
its reason. None was re-checked when the reason went away, because nothing
re-checks reasons — 15 conditional claims live in this codebase and exactly two
have an executable check, both written by accident while fixing something else.

This is the inverse of every other checker here. It does not look for defects.
It looks for CONSTRAINTS THAT ARE NO LONGER NEEDED — places where the system is
still paying a cost for a problem it already solved.

    python3 tools/check_assumptions.py

ADVICE, and it cannot be otherwise: a condition holding does not prove the
constraint is right, only that its stated reason is still true. What it kills
is the silent case — a cost nobody re-examined because nobody was told to.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(rel: str) -> str:
    p = ROOT / rel
    return p.read_text() if p.exists() else ""


# Each entry: what we pay, why, and the CONDITION that justifies still paying.
# `check` returns (condition_holds, evidence).
def _loadfont_at_module_scope():
    hits = []
    for p in (ROOT / "src").rglob("*.tsx"):
        src = p.read_text()
        for m in re.finditer(r"^\s*(?:const\s+\w+\s*=\s*)?loadFont\(", src, re.M):
            line = src[: m.start()].count("\n") + 1
            # inside a component body is fine; at module scope it is not
            before = src[: m.start()]
            if before.count("{") - before.count("}") == 0:
                hits.append(f"{p.name}:{line}")
    return (not hits), ("no module-scope loadFont()" if not hits
                        else "FOUND: " + ", ".join(hits))


def _receipt_caps_zoom():
    src = read("src/components/ReceiptScene.tsx")
    ok = "cardFits" in src and "Math.min(fitsZoom(width, uw), cardFits)" in src
    return ok, ("ReceiptScene still caps Z to the card width"
                if ok else "the cardFits cap is GONE — stills can overflow again")


def _caption_floor_derived():
    src = read("src/platformSafeArea.ts")
    ok = ("captionFloorPx" in src and "creditBottomPx(frameH) + CREDIT_H" in src)
    return ok, ("the floor is still derived from the credit geometry"
                if ok else "captionFloorPx no longer derives from CREDIT_Y/CREDIT_H")


def _g05_budget_matches_advance():
    fit = read("src/theme/fit.ts")
    m = re.search(r"export const ADVANCE = ([\d.]+);", fit)
    gates = read("tools/reel_gates.py")
    g = re.search(r"_ADVANCE = ([\d.]+)", gates)
    if not m or not g:
        return False, "could not read one of the two ADVANCE values"
    ok = m.group(1) == g.group(1)
    return ok, (f"both read {m.group(1)}" if ok
                else f"fit.ts={m.group(1)} but reel_gates={g.group(1)} — G05 is "
                     f"budgeting for a different typeface than the renderer uses")


def _all_reels_are_news():
    fmts = set()
    for p in (ROOT / "src/beats").glob("*.json"):
        if p.stem.endswith("-nomusic"):
            continue
        try:
            fmts.add(json.loads(p.read_text()).get("format") or "news")
        except Exception:  # noqa: BLE001
            pass
    ok = fmts <= {"news"}
    return ok, (f"every reel is still `news` ({len(fmts)} format in use)" if ok
                else f"formats now in use: {sorted(fmts)} — the news-calibrated "
                     f"thresholds in check_script.py and the INHERITED numbers in "
                     f"formats/*.md are being applied outside what they measured")


def _all_credits_go_through_credit():
    """No component may draw attribution itself."""
    import os
    bad = []
    comp = ROOT / "src/components"
    for f in sorted(comp.glob("*.tsx")):
        if f.name == "Credit.tsx":
            continue
        src = f.read_text()
        draws = re.search(r"\{\s*(?:scene\.)?(credit|source|footnote)\s*\}", src)
        if draws and 'from "./Credit"' not in src:
            bad.append(f"{f.name} draws {{{draws.group(1)}}} itself")
    return (not bad), ("every component routes attribution through <Credit>"
                       if not bad else "; ".join(bad))


ASSUMPTIONS = [
    dict(
        pay="one credit per source, short label",
        because="every component draws attribution through <Credit>, which is "
                "the only place the policy lives",
        where="src/components/Credit.tsx, RULES.md 2c",
        check=_all_credits_go_through_credit,
        if_broken="the component listed draws its own label and silently opts "
                  "out of BOTH rules — route it through <Credit>",
    ),
    dict(
        pay="render at --concurrency=6 (2.4x faster than the old 2)",
        because="the delayRender timeout it guarded against came from a "
                "module-scope loadFont(), removed 2026-08-16",
        where="scripts/render_job.py, PIPELINE.md",
        check=_loadfont_at_module_scope,
        if_broken="drop back toward 2 and re-measure — a module-scope "
                  "loadFont() reintroduces the timeout this speed depends on",
    ),
    dict(
        pay="stills render as `receipt` via reelkit.doc()",
        because="ReceiptScene caps zoom so a document is cropped vertically, "
                "never horizontally — the reason flo() used floatcard",
        where="tools/reelkit.py doc(), src/components/ReceiptScene.tsx",
        check=_receipt_caps_zoom,
        if_broken="wide captures will be sliced mid-word again; restore the cap "
                  "before trusting doc()",
    ),
    dict(
        pay="G45 blocks below 317 and G46 advises below 500",
        because="the floor is derived from the credit plate, not typed",
        where="src/platformSafeArea.ts, tools/reel_gates.py",
        check=_caption_floor_derived,
        if_broken="the two numbers become unexplained constants — re-derive or "
                  "demote the gate",
    ),
    dict(
        pay="G05 advises on line length using a character budget",
        because="the budget is computed from the SAME advance the renderer fits "
                "with; a typed budget went silently wrong when the face changed",
        where="src/theme/fit.ts, tools/reel_gates.py",
        check=_g05_budget_matches_advance,
        if_broken="G05 is budgeting for a different typeface than the one on "
                  "screen — exactly the 2026-08-18 failure",
    ),
    dict(
        pay="check_script.py thresholds and two of three format envelopes",
        because="they were calibrated on news, and every reel has been news",
        where="tools/check_script.py, formats/comparison.md, formats/top5.md",
        check=_all_reels_are_news,
        if_broken="treat those numbers as orientation, not verdicts, and "
                  "re-calibrate on the first reel in the new format",
    ),
]


def selftest() -> int:
    """Break each condition synthetically and prove the register notices.

    Every checker written today that reported nothing turned out to need this:
    the frame-contract tool was wrong seven times out of seven before its
    controls existed, and check_script passed a script the user called weak.
    A register that says "all clear" without ever having said anything else is
    not evidence.
    """
    import tempfile, shutil
    ok = True

    def check_(label: str, cond: bool):
        nonlocal ok
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        ok = ok and cond

    # 1. a module-scope loadFont() must be found
    tmp = ROOT / "src/components/__probe_loadfont.tsx"
    tmp.write_text('import {loadFont} from "x";\nconst f = loadFont({family:"y"});\n')
    try:
        holds, why = _loadfont_at_module_scope()
        check_("module-scope loadFont() is detected", not holds and "__probe" in why)
    finally:
        tmp.unlink()
    holds, _ = _loadfont_at_module_scope()
    check_("and the clean tree reads as holding", holds)

    # 2. the receipt zoom cap
    rp = ROOT / "src/components/ReceiptScene.tsx"
    orig = rp.read_text()
    try:
        rp.write_text(orig.replace("Math.min(fitsZoom(width, uw), cardFits)",
                                   "fitsZoom(width, uw)"))
        holds, _ = _receipt_caps_zoom()
        check_("a removed zoom cap is detected", not holds)
    finally:
        rp.write_text(orig)
    check_("and it reads as holding once restored", _receipt_caps_zoom()[0])

    # 3. the two ADVANCE values drifting apart
    fp = ROOT / "src/theme/fit.ts"
    orig = fp.read_text()
    try:
        fp.write_text(orig.replace("export const ADVANCE = 0.655;",
                                   "export const ADVANCE = 0.700;"))
        holds, why = _g05_budget_matches_advance()
        check_("drifting ADVANCE values are detected", not holds)
    finally:
        fp.write_text(orig)
    check_("and they read as matching once restored",
           _g05_budget_matches_advance()[0])

    print("\n  self-test PASSED\n" if ok else "\n  self-test FAILED\n")
    return 0 if ok else 1


def main() -> None:
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("\n  ARE THESE CONSTRAINTS STILL EARNING THEIR KEEP?\n")
    stale = 0
    for a in ASSUMPTIONS:
        holds, why = a["check"]()
        if not holds:
            stale += 1
        print(f"  [{'holds' if holds else 'GONE '}] {a['pay']}")
        print(f"          because: {a['because']}")
        print(f"          evidence: {why}")
        if not holds:
            print(f"          -> {a['if_broken']}")
        print()
    if stale:
        print(f"  {stale} constraint(s) whose stated reason no longer holds.\n"
              f"  That is not a bug report — it is a cost you may have stopped "
              f"needing to pay.\n")
    else:
        print("  Every constraint's stated reason still holds. Nothing here is "
              "being paid for\n  a problem that was already solved.\n")


if __name__ == "__main__":
    main()
