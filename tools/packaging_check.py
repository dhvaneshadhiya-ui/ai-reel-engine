#!/usr/bin/env python3
"""Check a reel's packaging copy before it goes out.

WHY THIS EXISTS
---------------
2026-08-14. The `caption-and-hashtags` skill prescribes "12-15 hashtags".
Instagram's official maximum is 5 (since Aug 2025) — past that they are
ignored. That exact error was made once already in this project and corrected
by hand, which is precisely the kind of thing that comes back.

The user's call: keep the skill, cap the hashtags. So the cap is code.

    python3 tools/packaging_check.py <slug>

Reads jobs/<slug>/packaging.md, which is a simple labelled block per platform:

    ## instagram
    CAPTION: Apple Pay may finally launch in India this October...
    HASHTAGS: #ApplePay #India #iPhone
    FIRST COMMENT: Which bank do you want supported first?
    ALT TEXT: Presenter explains Apple Pay's India launch beside a card graphic.

    ## youtube
    TITLE: Apple Pay in India: what we actually know
    ...
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# From social/references/platform-limits.md — the CORRECTED figures.
LIMITS = {
    "instagram": dict(max_tags=5, rec_tags=(3, 5), title=None, caption=2200),
    "youtube":   dict(max_tags=15, rec_tags=(3, 5), title=100, caption=5000),
    "tiktok":    dict(max_tags=None, rec_tags=(3, 5), title=None, caption=2200),
    "x":         dict(max_tags=None, rec_tags=(1, 2), title=None, caption=280),
    "linkedin":  dict(max_tags=None, rec_tags=(3, 5), title=None, caption=3000),
}


def parse(text: str) -> dict[str, dict[str, str]]:
    blocks: dict[str, dict[str, str]] = {}
    cur = None
    for line in text.splitlines():
        h = re.match(r"^\s*#{1,3}\s*([A-Za-z/ ]+)\s*$", line)
        if h:
            cur = h.group(1).strip().lower().replace("/", "")
            blocks[cur] = {}
            continue
        f = re.match(r"^\s*([A-Z][A-Z ]+):\s*(.*)$", line)
        if f and cur:
            blocks[cur][f.group(1).strip().upper()] = f.group(2).strip()
    return blocks



# THE CAPTION IS PROSE A HUMAN READS, AND IT NEVER GOT A HUMAN EAR (2026-09-08).
#
# script_approval refuses to propose without a recorded humanizer pass, because
# "a script with nothing measurably wrong can still read like a machine wrote
# it". Every word of that applies to the CAPTION, which is the writing an actual
# reader meets first on Instagram — and packaging.md had no such requirement.
#
# It shows. The shipped whatsapp-agents caption is 174 words in ONE unbroken
# paragraph carrying an em-dash, on a platform that truncates at ~125
# characters. The em-dash is the exact tell CLAUDE.md records as the reason the
# humanizer became mandatory for scripts in the first place.
#
# Hash-bound like the script record: edit the caption afterwards and this
# refuses again, because the pass no longer covers the words being published.
def _caption_hash(slug: str) -> str:
    import hashlib
    body = (ROOT / "jobs" / slug / "packaging.md").read_text()
    caps = re.findall(r"^CAPTION:\s*(.+)$", body, re.M)
    return hashlib.sha256("\n".join(caps).encode()).hexdigest()[:16]


def record_humanized(slug: str) -> int:
    import json
    rec = ROOT / "jobs" / slug / "packaging-humanized.json"
    rec.write_text(json.dumps({"caption_sha256": _caption_hash(slug)}, indent=2) + "\n")
    print(f"  humanizer pass recorded for {slug}'s caption "
          f"(sha {_caption_hash(slug)})")
    print("  packaging_check will accept it until the caption changes.")
    return 0


def humanized_ok(slug: str) -> str | None:
    """None if fine, else the reason it is not."""
    import json
    rec = ROOT / "jobs" / slug / "packaging-humanized.json"
    if not rec.exists():
        return ("NO HUMANIZER PASS ON THE CAPTION. The script gets one and "
                "refuses without it; the caption is the prose a reader "
                "actually meets and got none.\n"
                "  Run the `humanizer` skill over the CAPTION text, then:\n"
                "    python3 tools/packaging_check.py " + slug + " --humanized\n"
                "  SKILL CUE: run the `humanizer` skill on this caption.")
    try:
        got = json.loads(rec.read_text()).get("caption_sha256")
    except Exception:                                          # noqa: BLE001
        got = None
    if got != _caption_hash(slug):
        return ("THE CAPTION CHANGED SINCE ITS HUMANIZER PASS. The record no "
                "longer covers the words being published — re-run the pass.\n"
                "  SKILL CUE: run the `humanizer` skill on this caption.")
    return None


def main() -> None:
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(argv) != 1:
        sys.exit("usage: python3 tools/packaging_check.py <slug> [--humanized]")
    slug = argv[0]
    if "--humanized" in sys.argv:
        sys.exit(record_humanized(slug))
    p = ROOT / "jobs" / slug / "packaging.md"
    if not p.exists():
        sys.exit(f"no packaging at {p}\n"
                 "  Write it with the `social` skill: caption, hashtags, "
                 "first comment, alt text — per platform.")

    blocks = parse(p.read_text())
    if not blocks:
        sys.exit(f"{p} has no '## <platform>' sections.")

    errors: list[str] = []
    _h = humanized_ok(slug)
    if _h:
        errors.append(_h)
    for plat, fields in blocks.items():
        lim = LIMITS.get(plat)
        if lim is None:
            errors.append(f"{plat}: unknown platform (known: {sorted(LIMITS)})")
            continue

        tags = re.findall(r"#\w+", fields.get("HASHTAGS", ""))
        n = len(tags)
        if lim["max_tags"] is not None and n > lim["max_tags"]:
            errors.append(
                f"{plat}: {n} hashtags, max {lim['max_tags']}. "
                + ("Instagram ignores ALL of them past 5 (official, Aug 2025)."
                   if plat == "instagram" else
                   "YouTube ignores ALL of them past 15."))
        lo, hi = lim["rec_tags"]
        if n and not (lo <= n <= hi) and (
                lim["max_tags"] is None or n <= lim["max_tags"]):
            errors.append(f"{plat}: {n} hashtags, recommended {lo}-{hi}.")

        cap = fields.get("CAPTION", "")
        if not cap:
            errors.append(f"{plat}: no CAPTION.")
        elif lim["caption"] and len(cap) > lim["caption"]:
            errors.append(
                f"{plat}: caption {len(cap)} chars, max {lim['caption']}.")

        if lim["title"] and len(fields.get("TITLE", "")) > lim["title"]:
            errors.append(
                f"{plat}: title {len(fields['TITLE'])} chars, "
                f"max {lim['title']}.")

        # accessibility — the one genuinely good idea taken from the skill we
        # did not install
        if not fields.get("ALT TEXT"):
            errors.append(
                f"{plat}: no ALT TEXT. Every post gets one line describing "
                "the video for people who cannot see it.")

        if "#" in cap:
            errors.append(
                f"{plat}: hashtags are in the CAPTION. Put them in the FIRST "
                "COMMENT and keep the caption's first line doing the work — "
                "it is the only line shown before 'more'.")

    if errors:
        print(f"PACKAGING FAILED — {slug}\n" +
              "\n".join(f"  - {e}" for e in errors))
        sys.exit(1)
    print(f"packaging ok — {slug} ({', '.join(sorted(blocks))})")


if __name__ == "__main__":
    main()
