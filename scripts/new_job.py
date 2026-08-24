#!/usr/bin/env python3
"""Initialize a Nick-style reel job without overwriting existing work."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ENGINE = Path(__file__).resolve().parent.parent  # repo root


def locked_style(engine: Path = DEFAULT_ENGINE) -> str:
    """Locked style pack from config.json — never hardcode it here.

    This stamped "nick-saraev" on every new brief until 2026-08-16 while
    config.json defaulted to the editorial pack, so the generic path opened
    each job in the wrong style. Same failure as compile_shot_plan.py.
    """
    cfg = engine / "config.json"
    locked = "editorial"
    if cfg.exists():
        try:
            locked = json.loads(cfg.read_text()).get("defaults", {}).get(
                "style", locked)
        except Exception:
            pass
    return locked


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:64]


def write_new(path: Path, content: str) -> None:
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="?")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--details", default="")
    parser.add_argument("--cta-keyword", default="")
    parser.add_argument("--target-seconds", type=int, default=90)
    # Background music is OPTIONAL per reel (user directive 2026-08-22);
    # SFX remain the default sound layer either way. The flag flows to the
    # shot plan, compile carries it onto the sheet, and G09 stays silent.
    parser.add_argument("--no-music", action="store_true",
                        help="VO + SFX only — no background music bed")
    parser.add_argument(
        "--engine",
        type=Path,
        default=Path(os.environ.get("REEL_ENGINE", DEFAULT_ENGINE)),
    )
    args = parser.parse_args()

    slug = slugify(args.slug or args.topic)
    if not slug:
        raise SystemExit("could not derive a safe slug")
    # user rule 2026-08-11: reels run 1-2 minutes, length chosen by topic
    if not 60 <= args.target_seconds <= 120:
        raise SystemExit("--target-seconds must be between 60 and 120")

    engine = args.engine.expanduser().resolve()
    if not (engine / "package.json").exists():
        raise SystemExit(f"news-reels engine not found: {engine}")

    keyword = re.sub(r"[^A-Z0-9]", "", args.cta_keyword.upper())
    if not keyword:
        keyword = re.sub(r"[^A-Z0-9]", "", slug.split("-")[0].upper())[:14] or "GUIDE"

    brief = {
        "slug": slug,
        "topic": args.topic,
        "details": args.details,
        "style": locked_style(engine),
        "target_seconds": args.target_seconds,
        "cta_keyword": keyword,
        "music": not args.no_music,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "initialized",
    }
    # "assets", not the legacy "items": G11 — a BLOCKING gate — resolves
    # assetIds against manifest["assets"] only (reel_gates.py). A fresh job
    # scaffolded into the legacy key starts life invisible to the gate that
    # protects it. Found 2026-08-21 auditing the fresh-job path.
    manifest = {"slug": slug, "assets": []}
    shot_plan = {
        "emphasis": [],
        "caption_corrections": {},
        "shots": [],
    }
    if args.no_music:
        shot_plan["noMusic"] = True

    write_new(
        engine / f"jobs/{slug}/brief.json",
        json.dumps(brief, indent=2, ensure_ascii=False) + "\n",
    )
    write_new(
        engine / f"jobs/{slug}/giveaway.md",
        f"# {args.topic}\n\nResource promised for comment keyword **{keyword}**.\n",
    )
    write_new(
        engine / f"public/assets/{slug}/manifest.json",
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    )
    write_new(
        engine / f"jobs/{slug}/shot-plan.json",
        json.dumps(shot_plan, indent=2, ensure_ascii=False) + "\n",
    )
    # research.md — the words' answer to the manifest. Every load-bearing
    # claim gets a source, a tier and the exact words that speak it, plus a
    # log of what was actually searched. tools/research_check.py refuses a
    # ledger that is missing, unfilled, unsourced, or describing words the
    # script never says; script_approval.py propose runs it.
    write_new(
        engine / f"jobs/{slug}/research.md",
        (
            f"# Research — {slug}\n\n"
            "Claims ledger + search log. `script_approval.py propose` refuses\n"
            "while <placeholders> remain; format in tools/research_check.py.\n"
            "Tiers: official / multi / single / disputed. A single or\n"
            "disputed claim must be SPOKEN hedged (framework S20).\n\n"
            "## CLAIMS\n\n"
            "- CLAIM: <the load-bearing claim, in your words>\n"
            "  TIER: <official|multi|single|disputed>\n"
            "  SPOKEN: \"<the exact script words that carry it>\"\n"
            "  SRC: <https://...>\n"
            "  VIA: <the ULTIMATE source the SRC cites — leaker, agency, own\n"
            "       testing; one line per independent origin, or delete>\n\n"
            "## SEARCHED\n\n"
            "- <YYYY-MM-DD  \"query\"  (what it settled)>\n"
        ),
    )
    # structure.md — framework S17, the decision that comes BEFORE the first
    # sentence (formats/README-structure.md). Scaffolded here because a file
    # that exists gets filled and a file that must be remembered does not:
    # the 2026-08-21 weak draft was written with no structure decision at all,
    # and script_approval.py propose now refuses while the <placeholders>
    # below are still in place.
    write_new(
        engine / f"jobs/{slug}/structure.md",
        (
            f"# Structure — {slug}\n\n"
            "Written BEFORE the first sentence. Framework:\n"
            "`styles/shortform-script-framework.md` (S17 shapes; S25 standard).\n"
            "`script_approval.py propose` refuses while <placeholders> remain.\n\n"
            "## SHAPE (S17)\n\n"
            "Options: Discovery / News / Product announcement / Explainer /\n"
            "Tutorial / Comparison / Story / List / Myth-busting / "
            "Transformation.\n\n"
            "<the shape chosen, and WHY it fits the material>\n\n"
            "## PROMISE (S2)\n\n"
            "<what the viewer is told they will get by watching>\n\n"
            "## OPEN LOOP (S10)\n\n"
            "Planted: <which sentence, and its words>\n"
            "Paid off: <where, and how the ending returns to it per S18>\n\n"
            "## WHAT -> WHY -> SO WHAT (S7)\n\n"
            "<the translation that turns the headline fact into viewer meaning>\n\n"
            "## WHAT WAS CUT (S11, S21)\n\n"
            "<facts left out, each with why — momentum beats density>\n\n"
            "## SOURCES\n\n"
            "<every source consulted — two independent minimum, or why one>\n"
        ),
    )
    (engine / f"_sources/assets/{slug}").mkdir(parents=True, exist_ok=True)

    print(f"initialized {slug}")
    print(f"brief: {engine / f'jobs/{slug}/brief.json'}")
    print(f"assets: {engine / f'public/assets/{slug}/'}")


if __name__ == "__main__":
    main()
