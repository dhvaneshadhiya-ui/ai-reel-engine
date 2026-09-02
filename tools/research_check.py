#!/usr/bin/env python3
"""Check a reel's research ledger — the words' answer to the manifest.

WHY THIS EXISTS
---------------
The scouting side got hardened first, and the measurement that justified it
(capture_plan.py's docstring) applies verbatim here: per-item metadata that
costs attention is the metadata that gets dropped. Assets carried `shows` 229
times and a tier 18 times until a tool refused to run without the tier. The
research side had LESS than that: `verified_facts` in the manifest is a
convention no code reads, and the fact-check skill is advisory — which in this
repo's history means skipped. The iphone18-colors reel was scripted off ONE
source.

So research now leaves the same kind of record scouting does.
`jobs/<slug>/research.md` (scaffolded by new_job.py) carries a claims ledger:

    ## CLAIMS

    - CLAIM: the Pantone code leaked in April
      TIER: single
      SPOKEN: "leaked back in April"
      SRC: https://www.macworld.com/article/...
      VIA: Macworld exclusive           # optional: the ULTIMATE source the
                                        # SRC cites — one VIA line per
                                        # independent origin. A multi-tier
                                        # claim whose SRCs share one VIA is
                                        # one source dressed as many.

    ## SEARCHED

    - 2026-08-21  "iphone 18 pro dark cherry pantone"  (freshness re-check)

WHAT BLOCKS AND WHAT ADVISES — the G41/G42 split, reused
--------------------------------------------------------
REFUSED (propose exits 1): a ledger that is structurally dishonest —
  missing, still a template, a claim with no source URL or no valid TIER,
  a SPOKEN phrase that does not appear in the script (a ledger describing a
  script that does not exist is fiction wearing a record's badge), or an
  empty SEARCHED log.

ADVISED (printed, recorded in review.json, never blocks):
  - a single/disputed-tier claim whose spoken sentence carries no hedge —
    framework S20's own list; presenting a rumor as confirmed is the failure
    the user keeps catching by hand
  - fewer than two independent source domains with no ONE-SOURCE-OK line
  - FALSE CORROBORATION, both shapes: a multi-tier claim whose SRCs sit on
    one domain (two articles from the same outlet), and a multi-tier claim
    whose SRCs all trace VIA one ultimate source (MacRumors and PhoneArena
    both quoting the same Weibo leaker is ONE source dressed as two)

WHAT THIS CANNOT DO, said plainly: verify that a search happened, that a URL
says what the ledger claims, or that a fact is true. It verifies the record
exists, is internally consistent, and matches the script it claims to
describe. The last inch of research quality is judgement, same as writing.

    python3 tools/research_check.py <slug>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# The framework's six classes (frameworks/short-form-master.md §3.4), mapped
# onto the vocabulary this repo already had. Ours covered corroboration but
# had no word for a claim that is somebody's FORECAST rather than a report,
# and no word for one that must not ship at all (2026-08-26 audit).
#
#   official   <- Confirmed                (primary/authoritative source)
#   multi      <- Credibly Reported, corroborated
#   single     <- Credibly Reported / Rumor or Leak, one origin
#   prediction <- Prediction or Analysis   (must name WHOSE, and its basis)
#   disputed   <- Disputed                 (sources materially disagree)
#   unsupported<- Unsupported              (REFUSED — §3.5: the only class the
#                                           framework says must be excluded)
TIERS = {"official", "multi", "single", "prediction", "disputed"}
REFUSED_TIERS = {"unsupported"}

# framework S20's own hedging vocabulary, plus the attribution verbs that do
# the same job ("Kuo says" hedges as hard as "reportedly") and the leak family
# this beat runs on. Derived from the framework, not invented here.
HEDGES = {
    "reportedly", "reported", "reports", "rumored", "rumor", "rumors",
    "leak", "leaked", "leaker", "leakers", "expected", "expects", "could",
    "may", "might", "believed", "claims", "claimed", "says", "said",
    "according", "allegedly", "unconfirmed", "official",
}


# ABSENCE AND SUPERLATIVE CLAIMS — the ones a two-source ledger cannot support.
#
# WHY (2026-09-02, claude-fable-5-1). The script asserted "Nobody outside has
# checked one yet" about a model launched hours earlier that people were already
# testing publicly. The user caught it; the ledger never could have. Two
# separate holes met:
#
#   1. The ledger validates the claims you CHOSE to record. A confident
#      assertion you never thought to write down is invisible to every check
#      here, because they all start from the ledger and look outward.
#   2. An ABSENCE claim is not the same shape as a presence claim. "X said Y"
#      needs one source. "NOBODY has done Y" needs someone to have looked
#      everywhere and come back empty, and no number of SRC urls establishes it.
#
# So this scans the SCRIPT, not the ledger, and demands that any claim of this
# shape be recorded with real sourcing — or cut. Superlatives are here for the
# same reason: "the first", "the only", "never before" are absence claims
# wearing a positive grammar.
# TWO TIERS, because one regex over both fires on every honest hedge.
#
# UNVERIFIABLE — a claim about what OTHER PEOPLE have or have not done. No
# number of SRC urls establishes it; it needs someone to have looked
# everywhere and come back empty. This is the shape that shipped:
# "Nobody outside has checked one yet."
UNVERIFIABLE = re.compile(
    r"\b(nobody (?:else |outside )?(?:has|have|had|is|are)\b"
    r"|no one (?:else |outside )?(?:has|have|had|is|are)\b"
    r"|no-one (?:has|have|is)\b"
    r"|(?:has|have) yet to be\b|yet to be (?:tested|verified|checked|"
    r"confirmed|reviewed|benchmarked|independently)\b"
    r"|nobody (?:has )?(?:tested|checked|verified|tried|seen)\b)", re.I)

# SUPERLATIVE — "the first", "the only", "never been". Often perfectly
# sourceable, and common in real reporting, so this ADVISES rather than
# refusing. It is still worth a second look: each one is an absence claim
# wearing positive grammar.
SUPERLATIVE = re.compile(
    r"\b(first ever|the first (?:time|one|model|phone|company|device)"
    r"|for the first time|the only (?:one|way|phone|model|risk)"
    r"|never been|has never|unprecedented)\b", re.I)

# A sentence that is already flagging its own uncertainty is a HEDGE, not a
# claim: "Apple has confirmed none of this", "None of it is official until
# Apple says so". Those are the script being honest about sourcing, and an
# earlier draft of this check refused all sixteen reels that contained one.
HEDGE_CONTEXT = re.compile(
    r"\b(confirm(?:ed|s)?|official|reportedly|rumou?r|leak|allegedly|"
    r"claims?|says?|according to|until)\b", re.I)


def _sentences(script_text: str) -> list[str]:
    return [" ".join(x.split())
            for x in re.split(r"(?<=[.!?])\s+", script_text) if x.strip()]


def absence_claims(script_text: str) -> list[str]:
    """Sentences asserting what nobody else has done — the unverifiable shape."""
    return [t for t in _sentences(script_text)
            if UNVERIFIABLE.search(t) and not HEDGE_CONTEXT.search(t)]


def superlative_claims(script_text: str) -> list[str]:
    """Sentences claiming a first/only/never — sourceable, but worth checking."""
    return [t for t in _sentences(script_text)
            if SUPERLATIVE.search(t) and not HEDGE_CONTEXT.search(t)]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def parse_ledger(body: str) -> list[dict]:
    """CLAIM blocks: a `- CLAIM:` line, then TIER:/SPOKEN:/SRC: lines."""
    claims: list[dict] = []
    cur: dict | None = None
    in_claims = False
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            in_claims = line.upper().startswith("## CLAIMS")
            continue
        if not in_claims:
            continue
        if line.startswith("- CLAIM:"):
            cur = {"claim": line[8:].strip(), "tier": None,
                   "spoken": None, "srcs": []}
            claims.append(cur)
        elif cur is not None and line.startswith("TIER:"):
            cur["tier"] = line[5:].strip().lower()
        elif cur is not None and line.startswith("SPOKEN:"):
            cur["spoken"] = line[7:].strip().strip('"“”')
        elif cur is not None and line.startswith("SRC:"):
            cur["srcs"].append(line[4:].strip())
        elif cur is not None and line.startswith("VIA:"):
            cur.setdefault("vias", []).append(line[4:].strip())
    return claims


def check_research(slug: str, script_text: str | None,
                   root: Path | None = None) -> tuple[list[str], list[str]]:
    """Returns (errors, advice). Errors mean the ledger is not a record.

    `script_text=None` runs the STRUCTURAL half only — ledger exists, filled,
    claims tiered and sourced, search log present — and skips the SPOKEN and
    hedge checks, which need a script to check against. That is the honest
    mid-pipeline state: the ledger is started at research time, SPOKEN is
    filled at script time, and propose verifies the join.
    """
    root = root or ROOT
    p = root / "jobs" / slug / "research.md"
    errors: list[str] = []
    advice: list[str] = []

    if not p.exists():
        return ([f"NO RESEARCH LEDGER — missing {p}\n"
                 "  Record every load-bearing claim (CLAIM/TIER/SPOKEN/SRC)\n"
                 "  and the searches that produced them. new_job.py scaffolds\n"
                 "  it; tools/research_check.py has the format."], advice)
    body = p.read_text()
    if re.search(r"<[a-z][^>\n]{3,}>", body):
        return ([f"RESEARCH STILL A TEMPLATE — {p} has unfilled "
                 "<placeholders>."], advice)

    claims = parse_ledger(body)
    if not claims:
        errors.append(f"NO CLAIMS RECORDED in {p} — a reel scripted off "
                      "research that left no ledger is a one-source reel "
                      "until proven otherwise.")

    # SEARCHED log: at least one dated line. Presence is all that is
    # checkable; the log exists so the NEXT session can see what was and
    # was not looked for (the 08-21 freshness re-check changed the script).
    m = re.search(r"## SEARCHED(.*?)(?=\n## |\Z)", body, re.S | re.I)
    if not m or not re.search(r"^\s*-\s+\S", m.group(1), re.M):
        errors.append(f"NO SEARCH LOG in {p} — add '## SEARCHED' with one "
                      "dated line per query. What was not searched is the "
                      "part the next session needs to know.")

    script_norm = _norm(script_text) if script_text is not None else None
    script_words = script_norm.split() if script_norm is not None else []
    domains: set[str] = set()
    for i, c in enumerate(claims):
        tag = f"claim {i + 1} ({c['claim'][:40]!r})"
        if c["tier"] in REFUSED_TIERS:
            errors.append(
                f"claim {i}: tier 'unsupported' — the framework's one hard "
                "exclusion (§3.5). Narrow it, attribute it precisely, reframe "
                "the story around what IS supported, or cut the claim. "
                "Adding 'reportedly' to an unsupported claim does not make it "
                "publishable (§3.14).")
            continue
        if c["tier"] not in TIERS:
            errors.append(f"{tag}: TIER is {c['tier']!r} — must be one of "
                          f"{sorted(TIERS)}. An untiered claim is the 18/229 "
                          "problem again.")
        if not c["srcs"] or not any(s.startswith("http") for s in c["srcs"]):
            errors.append(f"{tag}: no SRC url. A claim with no source is an "
                          "assertion, and the ledger exists to kill those.")
        claim_domains = set()
        for s in c["srcs"]:
            if s.startswith("http"):
                d = urlparse(s).netloc.removeprefix("www.")
                domains.add(d)
                claim_domains.add(d)
        # FALSE CORROBORATION — the tier says "multi", the sourcing says one.
        # Two shapes, both advisory (2026-08-21, found in a LIVE ledger the
        # day the tier field shipped):
        #   * domain-level: two articles from the same outlet counted as two
        #     sources ("multi" off two MacRumors pieces)
        #   * source-level: different outlets all citing the same ultimate
        #     origin — MacRumors and PhoneArena both quoting Fixed Focus
        #     Digital is ONE leaker dressed as two domains. Recorded with
        #     VIA: lines (one per ultimate source); optional, but the tier
        #     is only as verifiable as the VIAs behind it.
        if c["tier"] == "multi":
            if len(claim_domains) < 2:
                advice.append(
                    f"{tag}: TIER multi but every SRC is on "
                    f"{next(iter(claim_domains), 'one domain')} — two "
                    "articles from one outlet corroborate less than they "
                    "look. Add a second outlet or downgrade to single.")
            vias = {v.strip().lower() for v in c.get("vias", []) if v.strip()}
            if len(claim_domains) >= 2 and len(vias) == 1:
                advice.append(
                    f"{tag}: TIER multi across {len(claim_domains)} domains, "
                    f"but every SRC traces VIA {c['vias'][0]!r} — one "
                    "ultimate source dressed as many outlets. The source "
                    "count is the VIA count, not the domain count. Downgrade "
                    "to single, or find a SRC with a different origin.")
        if script_norm is None:
            continue                      # structural pass — no script yet
        spoken = c["spoken"] or ""
        if not spoken:
            errors.append(f"{tag}: no SPOKEN phrase. The ledger must name the "
                          "words in the script that carry this claim — the "
                          "`covers` discipline, applied to research.")
            continue
        pos = script_norm.find(_norm(spoken))
        if pos < 0:
            errors.append(f"{tag}: SPOKEN {spoken!r} is not in the script. "
                          "A ledger describing words nobody says is fiction "
                          "wearing a record's badge — update it with the "
                          "script.")
            continue
        if c["tier"] in ("single", "disputed"):
            # Hedge scan on a +/-12-word window around the phrase — a hedge
            # one clause away still covers ("None of it's official...").
            at = len(script_norm[:pos].split())
            window = script_words[max(0, at - 12):
                                  at + len(_norm(spoken).split()) + 12]
            if not (set(window) & HEDGES):
                advice.append(
                    f"{tag}: tier {c['tier']} but spoken UNHEDGED near "
                    f"{spoken!r}. framework S20: a rumor spoken as fact is "
                    "the script lying about its own sourcing. Add "
                    "'reportedly'/'leaked'/attribution, or upgrade the tier "
                    "with a second source.")

    # EVERY ABSENCE CLAIM MUST BE LEDGERED. See the ABSENCE note above.
    if script_norm is not None:
        covered = [_norm(c["spoken"] or "") for c in claims if c["spoken"]]
        for sent in absence_claims(script_text or ""):
            n = _norm(sent)
            if any(sp and sp in n for sp in covered):
                continue
            errors.append(
                f"UNLEDGERED ABSENCE CLAIM: {sent!r}\n"
                "  This asserts that something does NOT exist, or is a first "
                "or an only. No number of sources proves an absence — it "
                "needs someone to have LOOKED and come back empty, and this "
                "one is not in the ledger at all.\n"
                "  claude-fable-5-1 shipped \"Nobody outside has checked one "
                "yet\" about a model launched hours earlier that people were "
                "already testing in public. Record it as a CLAIM with the "
                "search that establishes it, or cut the line."
            )

        for sent in superlative_claims(script_text or ""):
            n = _norm(sent)
            if any(sp and sp in n for sp in covered):
                continue
            advice.append(
                f"UNLEDGERED SUPERLATIVE: {sent!r} — a first/only/never is an "
                "absence claim in positive grammar, and it is the kind a "
                "reader checks. Often perfectly sourceable, which is why this "
                "advises rather than refusing; record it as a CLAIM if it is "
                "load-bearing.")

    if claims and len(domains) < 2 and "ONE-SOURCE-OK:" not in body:
        advice.append(
            f"only {len(domains)} source domain(s) across the whole ledger "
            f"({', '.join(sorted(domains)) or 'none'}). Two independent "
            "minimum, or add a line 'ONE-SOURCE-OK: <why>' — the "
            "iphone18-colors first draft came off one guide, and it read "
            "like it.")
    return errors, advice


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python3 tools/research_check.py <slug>")
    slug = sys.argv[1]
    sp = ROOT / "jobs" / slug / "script.md"
    script = sp.read_text() if sp.exists() else ""
    errors, advice = check_research(slug, script)
    for e in errors:
        print(f"  REFUSE  {e}")
    for a in advice:
        print(f"  advice  {a}")
    if not errors and not advice:
        print("  research ledger ok")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
