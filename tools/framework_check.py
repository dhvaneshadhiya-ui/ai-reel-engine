#!/usr/bin/env python3
"""The parts of the short-form master framework a machine can hold.

`frameworks/short-form-master.md` (user-supplied 2026-08-25) is the binding
production framework. Most of it is judgement and belongs in the manual —
story engine, escalation, pattern interrupts, the editor's eye. Three of its
rules are NOT judgement: they have a right answer, they fail silently, and
each one breaks trust rather than taste. Those live here.

    F1  REVEAL TARGET       a campaign that withholds an identity for a DM
                            must not disclose it in narration, on-screen
                            text, or the CTA. Leak it and the promised
                            delivery is already spent — the framework calls
                            this out as its own audit, and it is the one
                            failure the viewer experiences as a lie.
    F2  CERTAINTY           "Never convert uncertain information into
                            certainty." A claim recorded as single-source or
                            disputed must not be SPOKEN as fact. The ledger
                            already knows each claim's strength; nothing
                            checked that the words matched it.
    F3  SOURCE POLICY       research sources and footage sources are separate
                            categories, and a restriction on one does not
                            imply the other. Stated per job, checked here.

    F4  CLARITY             "Create curiosity without creating confusion."
                            If a reveal target is withheld, the SUBJECT must
                            still be spoken — the viewer has to know what
                            category of thing they are being offered.

Run by `script_approval.py propose` (so a leak is caught before the user is
asked to approve) and self-tested by doctor.

    python3 tools/framework_check.py <slug>
    python3 tools/framework_check.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Words that assert a thing IS so. Framework §3.7 lists the conversions it
# forbids; these are the landing side of each one.
CERTAIN = [
    "will ", "is releasing", "is launching", "is coming", "confirmed",
    "guaranteed", "definitely", "certainly", "is going to", "ships with",
    "comes with", "has been confirmed", "proves", "always",
]
# Words that keep a claim at its real strength.
HEDGE = [
    "may", "might", "could", "reportedly", "expected", "appears",
    "suggests", "according to", "claims", "rumou", "rumor", "leak",
    "unconfirmed", "not clear", "disagree", "one source", "so far",
    "in our", "we measured", "on this machine", "our own",
]
POLICIES = {
    "official-facts-only", "official-footage-only", "official-preferred",
    "approved-only", "no-third-party-media", "none",
}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


def _tokens(s: str) -> set[str]:
    return {w for w in _norm(s).split() if len(w) > 2}


def check(brief: dict, script: str, claims: list[dict],
          assets: list[dict], onscreen: str = "",
          packaging: str = "") -> tuple[list[str], list[str]]:
    """Returns (failures, advice)."""
    fail: list[str] = []
    note: list[str] = []

    target = str(brief.get("reveal_target") or "none").strip()
    subject = str(brief.get("subject") or brief.get("topic") or "").strip()
    policy = str(brief.get("source_policy") or "none").strip()

    # ---- F1  reveal target ------------------------------------------------
    if target and target.lower() != "none":
        t_norm = _norm(target).strip()
        t_words = [w for w in t_norm.split() if len(w) > 2]
        surfaces = {
            "narration": script,
            "on-screen text": onscreen,
            "packaging/CTA": packaging,
        }
        for where, text in surfaces.items():
            if not text:
                continue
            hay = _norm(text)
            if t_norm and t_norm in hay:
                fail.append(
                    f"F1 REVEAL TARGET said out loud in {where}: {target!r}. "
                    "The campaign promises to deliver it after the action; "
                    "saying it first spends the delivery and makes the CTA a "
                    "lie (framework §5).")
            elif t_words and all(w in hay.split() for w in t_words):
                fail.append(
                    f"F1 REVEAL TARGET assembled in {where}: every word of "
                    f"{target!r} appears. Clues that combine ARE a "
                    "disclosure (framework §5, reveal-target audit).")
        # F4 — the subject must survive the concealment
        if subject and not (_tokens(subject) & _tokens(script)):
            fail.append(
                f"F4 CLARITY: the reveal target is withheld and the SUBJECT "
                f"({subject!r}) is never spoken. The viewer cannot tell what "
                "category of thing they are being offered — that is "
                "confusion, not curiosity (framework §5 clarity audit).")

    # ---- F2  certainty vs evidence ---------------------------------------
    for c in claims:
        tier = str(c.get("tier", "")).lower()
        spoken = str(c.get("spoken", ""))
        if tier in ("official", "multi") or not spoken:
            continue
        low = spoken.lower()
        hit = [w for w in CERTAIN if w in low]
        if hit and not any(h in low for h in HEDGE):
            fail.append(
                f"F2 CERTAINTY: a {tier!r}-tier claim is spoken as fact — "
                f"{spoken[:70]!r} carries {hit[0]!r} with no qualifier. "
                "Framework §3.7: never convert 'may' into 'will'. Say who "
                "reported it, or hedge it to its real strength.")

    # ---- F2b  a prediction must name WHOSE it is --------------------------
    # Framework §3.6: "[Analyst/source] expects..., based on...". A forecast
    # with no owner is an assertion wearing a hedge.
    for c in claims:
        if str(c.get("tier", "")).lower() != "prediction":
            continue
        spoken = str(c.get("spoken", ""))
        if spoken and not re.search(
                r"\b(according to|expects?|predicts?|estimates?|analyst|"
                r"reports?|says?|per |'s forecast|believes?)\b", spoken, re.I):
            fail.append(
                f"F2b PREDICTION with no owner: {spoken[:60]!r} is recorded as "
                "a forecast but the words do not say whose it is. Framework "
                "\u00a73.6: attribute the prediction and its basis.")

    # ---- F3  source policy ------------------------------------------------
    if policy not in POLICIES:
        note.append(
            f"F3 source_policy {policy!r} is not one of {sorted(POLICIES)} — "
            "state the restriction so footage and facts can be judged "
            "separately (framework §3).")
    if policy == "official-facts-only":
        bad = [c for c in claims
               if str(c.get("tier", "")).lower() not in ("official",)]
        if bad:
            fail.append(
                f"F3 SOURCE POLICY 'official-facts-only' but {len(bad)} "
                f"claim(s) rest on non-official sourcing (first: "
                f"{str(bad[0].get('claim',''))[:60]!r}).")
    if policy in ("official-footage-only", "no-third-party-media"):
        bad = [a for a in assets
               if str(a.get("tier", "")).lower() not in ("official", "")]
        if bad:
            fail.append(
                f"F3 SOURCE POLICY {policy!r} but {len(bad)} asset(s) are "
                f"third-party (first: {bad[0].get('id','?')!r}). Third-party "
                "reporting may still INFORM the script; its media may not "
                "appear.")

    # ---- advisory: proof vs illustrative ---------------------------------
    unmarked = [a.get("id") for a in assets if not a.get("evidence")]
    if assets and unmarked:
        note.append(
            f"{len(unmarked)} asset(s) do not say whether they are PROOF or "
            "ILLUSTRATIVE (framework §3). Illustrative context presented as "
            "evidence is the quiet way a sourced reel becomes untrue.")
    return fail, note


def _load(slug: str) -> tuple[dict, str, list, list, str, str]:
    job = ROOT / "jobs" / slug
    brief = {}
    bp = job / "brief.json"
    if bp.exists():
        brief = json.loads(bp.read_text())
    script = (job / "script.md").read_text() if (job / "script.md").exists() else ""
    claims = []
    rp = job / "research.md"
    if rp.exists():
        cur: dict = {}
        for line in rp.read_text().splitlines():
            s = line.strip()
            if s.startswith("- CLAIM:"):
                if cur:
                    claims.append(cur)
                cur = {"claim": s.split(":", 1)[1].strip()}
            elif s.startswith("TIER:") and cur:
                cur["tier"] = s.split(":", 1)[1].strip()
            elif s.startswith("SPOKEN:") and cur:
                cur["spoken"] = s.split(":", 1)[1].strip().strip('"')
        if cur:
            claims.append(cur)
    assets = []
    mp = ROOT / "public/assets" / slug / "manifest.json"
    if mp.exists():
        assets = json.loads(mp.read_text()).get("assets", [])
    onscreen = ""
    bs = ROOT / "src/beats" / f"{slug}.json"
    if bs.exists():
        beats = json.loads(bs.read_text())
        bits = []
        for sc in beats.get("scenes", []):
            hl = sc.get("headline")
            if isinstance(hl, dict):
                bits += [l.get("text", "") for l in hl.get("lines", [])]
            kin = sc.get("kinetic")
            if isinstance(kin, dict):
                bits += [l.get("text", "") for l in kin.get("lines", [])]
            for k in ("keyword", "question", "title", "footnote"):
                if isinstance(sc.get(k), str):
                    bits.append(sc[k])
        onscreen = " ".join(bits)
    pk = job / "packaging.md"
    packaging = pk.read_text() if pk.exists() else ""
    return brief, script, claims, assets, onscreen, packaging


def selftest() -> int:
    ok = True

    def t(label: str, cond: bool) -> None:
        nonlocal ok
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        ok = ok and cond

    B = {"subject": "an AI cost tool", "reveal_target": "Ponytail",
         "source_policy": "official-preferred"}
    f, _ = check(B, "This tool cuts your bill. Comment TOOL.", [], [])
    t("F1 silent when the target is never said", not any("F1" in x for x in f))
    f, _ = check(B, "Ponytail cuts your bill. Comment TOOL.", [], [])
    t("F1 fires when narration says the target", any("F1" in x for x in f))
    f, _ = check(B, "This cuts your bill.", [], [], onscreen="PONYTAIL")
    t("F1 fires on on-screen text too", any("F1" in x for x in f))
    f, _ = check(B, "This cuts your bill.", [], [], packaging="get Ponytail here")
    t("F1 fires on the packaging/CTA copy", any("F1" in x for x in f))
    f, _ = check({**B, "subject": "an AI cost tool"}, "It saves money.", [], [])
    t("F4 fires when the subject is never spoken",
      any("F4" in x for x in f))
    f, _ = check({**B, "reveal_target": "none"}, "Ponytail is great.", [], [])
    t("F1 silent when no reveal target is declared",
      not any("F1" in x for x in f))

    claims_bad = [{"claim": "x", "tier": "single", "spoken": "Apple will ship it in March"}]
    f, _ = check({}, "s", claims_bad, [])
    t("F2 fires on a single-source claim spoken as certainty",
      any("F2" in x for x in f))
    claims_ok = [{"claim": "x", "tier": "single",
                  "spoken": "one source claims Apple will ship it in March"}]
    f, _ = check({}, "s", claims_ok, [])
    t("F2 silent when the same claim is attributed",
      not any("F2" in x for x in f))
    claims_off = [{"claim": "x", "tier": "official", "spoken": "Apple will ship it"}]
    f, _ = check({}, "s", claims_off, [])
    t("F2 silent on an official-tier claim", not any("F2" in x for x in f))

    f, _ = check({}, "s", [{"claim": "x", "tier": "prediction",
                            "spoken": "the price drops in March"}], [])
    t("F2b fires on an unattributed prediction", any("F2b" in x for x in f))
    f, _ = check({}, "s", [{"claim": "x", "tier": "prediction",
                            "spoken": "Kuo expects the price to drop"}], [])
    t("F2b silent when the forecast names its owner",
      not any("F2b" in x for x in f))

    f, _ = check({"source_policy": "official-facts-only"}, "s",
                 [{"claim": "c", "tier": "single", "spoken": "reportedly"}], [])
    t("F3 fires when facts-only meets a non-official claim",
      any("F3" in x for x in f))
    f, _ = check({"source_policy": "official-footage-only"}, "s", [],
                 [{"id": "a", "tier": "fallback"}])
    t("F3 fires when footage-only meets third-party media",
      any("F3" in x for x in f))
    f, _ = check({"source_policy": "official-footage-only"}, "s",
                 [{"claim": "c", "tier": "single", "spoken": "reportedly"}],
                 [{"id": "a", "tier": "official"}])
    t("F3 lets third-party RESEARCH through a footage-only policy",
      not any("F3" in x for x in f))
    _, n = check({}, "s", [], [{"id": "a", "tier": "official"}])
    t("proof/illustrative advises when unmarked",
      any("PROOF" in x.upper() for x in n))

    print("\n  self-test PASSED\n" if ok else "\n  self-test FAILED\n")
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    if len(sys.argv) < 2:
        print("usage: framework_check.py <slug> | --selftest")
        return 1
    slug = sys.argv[1]
    fail, note = check(*_load(slug))
    print(f"\n=== framework check — {slug} ===")
    for f in fail:
        print(f"  FAIL {f}")
    for n in note:
        print(f"  note {n}")
    if not fail and not note:
        print("  clean — reveal handling, certainty and source policy all hold.")
    print()
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
