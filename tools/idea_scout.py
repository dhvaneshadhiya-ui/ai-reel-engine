#!/usr/bin/env python3
"""The daily idea pipeline's deterministic half: the brief, and the check.

WHY THIS EXISTS
---------------
Topic selection was the one stage of this pipeline with no system at all.
Reels got picked off whatever news happened to be in front of someone, and
nothing ever read what the audience was actually asking about. Every other
stage — research, structure, script, voice, render — has a tool, a gate and a
self-test. This one had a habit.

WHAT THIS TOOL DOES AND DOES NOT DO
-----------------------------------
It cannot research. Research needs the web, and that belongs to the agent.
What a tool CAN do is the two halves either side of the thinking:

    --brief          everything the researcher must know before starting:
                     every subject already covered (so it cannot suggest a
                     repeat), the formats and their measured bands, and the
                     output contract.
    --check <file>   whether what came back is usable: a real story engine,
                     two independent sources, a known format, not a repeat.

THE GUARDRAIL THAT MATTERS
--------------------------
`marketing-skills:customer-research` was adopted 2026-08-27 for its
watering-hole mode — App Store 1-3 star reviews, YouTube and Instagram
comments, topic subreddits. Its output is AUDIENCE LANGUAGE, never evidence.
A forum comment tells you what people are confused about and in whose words;
it does not establish a fact. So `AUDIENCE:` lines are parsed separately from
`SRC:` lines and are REFUSED as sourcing — an idea whose only support is a
Reddit thread does not pass.

    python3 tools/idea_scout.py --brief
    python3 tools/idea_scout.py --check jobs/_ideas/2026-08-28.md
    python3 tools/idea_scout.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
IDEAS_DIR = ROOT / "jobs" / "_ideas"

MIN_SOURCES = 2          # two INDEPENDENT domains, same rule as research.md
MIN_IDEAS = 5


def covered_subjects() -> dict[str, str]:
    """Every subject already made, so the scout cannot re-suggest one."""
    out = {}
    for job in sorted((ROOT / "jobs").iterdir()):
        if not job.is_dir() or job.name.startswith("_"):
            continue
        subject = ""
        brief = job / "brief.json"
        if brief.exists():
            try:
                subject = str(json.loads(brief.read_text()).get("subject", ""))
            except Exception:                                  # noqa: BLE001
                pass
        if not subject:
            script = job / "script.md"
            if script.exists():
                subject = " ".join(script.read_text().split()[:18])
        out[job.name] = subject
    return out


def formats() -> list[str]:
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import reel_gates
        return sorted(reel_gates.FORMATS)
    except Exception:                                          # noqa: BLE001
        return ["news", "top5", "ai-tools", "comparison"]


CONTRACT = """\
## Output contract — jobs/_ideas/<YYYY-MM-DD>.md

Write ONE block per idea, at least {min_ideas}. Fields exactly as named:

    ## <short title>
    SUBJECT: what the reel is actually about, one line
    ANGLE:   why this is a REEL and not a headline — the tension in it
    ENGINE:  a viewer who believes X discovers Y, which matters because Z
    FORMAT:  one of {formats}
    WHY NOW: the time pressure. "it is interesting" is not a reason
    SRC:     <url>
    SRC:     <url>
    AUDIENCE: "<verbatim quote>" — <platform>, <thread url>   (optional)

ENGINE must contain all three parts. A subject with no discovery is a
headline; a discovery that matters to nobody is trivia.

SRC needs {min_sources} urls on DIFFERENT domains. Two articles on one site is
one source, and so is two sites quoting the same leaker.

AUDIENCE is LANGUAGE, not evidence. It tells you what people are confused
about and in whose words, and it may shape the angle and the hook. It can
never be the sourcing — an idea supported only by AUDIENCE lines is refused.
"""


def brief() -> int:
    cov = covered_subjects()
    fmt = formats()
    print("\n=== IDEA SCOUT BRIEF ===\n")
    print(f"ALREADY COVERED — do not suggest these again ({len(cov)} reels):\n")
    for slug, subject in cov.items():
        print(f"  {slug:<28} {subject[:70]}")
    print(f"\nFORMATS AND THEIR MEASURED BANDS:\n")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import reel_gates
        for name in fmt:
            p = reel_gates.FORMATS[name]
            lo, hi = p["runtime"]
            # the key is `requires_cta`; `cta` never existed, so every
            # format printed "optional" and top5/ai-tools/comparison — which
            # all REQUIRE one — were being briefed wrong.
            cta = "CTA required" if p.get("requires_cta") else "cta optional"
            print(f"  {name:<12} {lo:.0f}-{hi:.0f}s   hook <={p['hook_max']}s"
                  f"   {cta}")
    except Exception:                                          # noqa: BLE001
        print("  " + ", ".join(fmt))
    print("\n" + CONTRACT.format(min_ideas=MIN_IDEAS, formats="|".join(fmt),
                                 min_sources=MIN_SOURCES))
    return 0


# ---------------------------------------------------------------- checking
def parse(text: str) -> list[dict]:
    ideas, cur = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            if cur:
                ideas.append(cur)
            cur = {"title": line[3:].strip(), "SRC": [], "AUDIENCE": []}
            continue
        if cur is None:
            continue
        m = re.match(r"\s*([A-Z][A-Z ]+):\s*(.+)", line)
        if m:
            key, val = m.group(1).strip(), m.group(2).strip()
            if key in ("SRC", "AUDIENCE"):
                cur[key].append(val)
            else:
                cur[key] = val
    if cur:
        ideas.append(cur)
    return ideas


def check(path: Path) -> int:
    if not path.exists():
        sys.exit(f"\n  no {path}\n")
    ideas = parse(path.read_text())
    cov = covered_subjects()
    fmt = set(formats())
    problems: list[str] = []

    if len(ideas) < MIN_IDEAS:
        problems.append(f"only {len(ideas)} ideas — the brief asks for "
                        f"{MIN_IDEAS}. A short list is a list that skipped "
                        "the hard ones.")

    for i, idea in enumerate(ideas, 1):
        tag = f"idea {i} ({idea['title'][:34]})"
        for field in ("SUBJECT", "ANGLE", "ENGINE", "FORMAT", "WHY NOW"):
            if not idea.get(field):
                problems.append(f"{tag}: no {field}")

        eng = (idea.get("ENGINE") or "").lower()
        if eng and not ("discover" in eng and ("matter" in eng or "because" in eng)):
            problems.append(
                f"{tag}: ENGINE is not a story engine — it needs what the "
                "viewer believed, what they discover, and why it matters. "
                f"Got: {idea['ENGINE'][:60]!r}")

        f = (idea.get("FORMAT") or "").strip()
        if f and f not in fmt:
            problems.append(f"{tag}: FORMAT {f!r} is not one of {sorted(fmt)}")

        # SOURCING — audience language is deliberately not counted here.
        domains = {urlparse(u.split()[0]).netloc.replace("www.", "")
                   for u in idea["SRC"] if "://" in u}
        if len(domains) < MIN_SOURCES:
            extra = (" AUDIENCE lines do not count as sourcing."
                     if idea["AUDIENCE"] else "")
            problems.append(
                f"{tag}: {len(domains)} independent source domain(s), "
                f"need {MIN_SOURCES}.{extra}")

        # DEDUPE against everything already made.
        subj = (idea.get("SUBJECT") or "").lower()
        words = {w for w in re.findall(r"[a-z0-9]{4,}", subj)}
        for slug, done in cov.items():
            done_words = {w for w in re.findall(r"[a-z0-9]{4,}",
                                                (slug + " " + done).lower())}
            if words and done_words:
                overlap = len(words & done_words) / len(words)
                if overlap > 0.6:
                    problems.append(
                        f"{tag}: looks like a repeat of {slug} "
                        f"({overlap:.0%} subject overlap)")

    print(f"\n=== idea scout — {path.name} ===\n")
    print(f"  {len(ideas)} ideas, {len(cov)} reels already made\n")
    for idea in ideas:
        src = len({urlparse(u.split()[0]).netloc for u in idea["SRC"]
                   if "://" in u})
        aud = len(idea["AUDIENCE"])
        print(f"  {idea['title'][:44]:<46} {idea.get('FORMAT','?'):<10} "
              f"{src} src{'  +' + str(aud) + ' audience' if aud else ''}")
    if problems:
        print(f"\n  {len(problems)} problem(s):\n")
        for p in problems:
            print(f"    - {p}")
        print()
        return 1
    print("\n  every idea carries a story engine, two independent sources, a "
          "known format,\n  and is not a repeat. Pick one and run "
          "`new_job.py <slug>`.\n")
    return 0


def selftest() -> int:
    fails, checks = [], 0

    def ok(label: str, cond: bool, detail: str = "") -> None:
        nonlocal checks
        checks += 1
        if not cond:
            fails.append(f"{label}: {detail}")

    good = """## Something new
SUBJECT: a thing nobody here has covered about widget latency
ANGLE: the number everyone quotes is measured wrong
ENGINE: a viewer who believes widgets are instant discovers they wait 400ms,
 which matters because it is the reason their shortcuts feel broken
FORMAT: news
WHY NOW: the spec changed this week
SRC: https://example.com/a
SRC: https://other.org/b
"""
    import tempfile
    tmp = Path(tempfile.mkdtemp()) / "ideas.md"

    # 1. a single good idea still fails the COUNT — a short list skipped work
    tmp.write_text(good)
    ok("refuses a list shorter than the brief asks for", check(tmp) == 1)

    # 2. audience-only sourcing must be refused — the whole guardrail
    aud_only = good.replace("SRC: https://example.com/a\nSRC: https://other.org/b\n",
                            'AUDIENCE: "it feels slow" — Reddit, https://reddit.com/x\n')
    tmp.write_text(aud_only * 1)
    out = check(tmp)
    ok("audience quotes are refused as sourcing", out == 1)

    # 3. a non-engine ENGINE is caught
    noeng = good.replace(
        "ENGINE: a viewer who believes widgets are instant discovers they wait 400ms,\n"
        " which matters because it is the reason their shortcuts feel broken",
        "ENGINE: widgets are slow")
    tmp.write_text(noeng)
    ok("a headline masquerading as an engine is caught", check(tmp) == 1)

    # 4. parsing keeps SRC and AUDIENCE apart
    parsed = parse(good + '\nAUDIENCE: "x" — Reddit, https://r.com/1\n')
    ok("SRC and AUDIENCE parse separately",
       len(parsed[0]["SRC"]) == 2 and len(parsed[0]["AUDIENCE"]) == 1)

    # 5. the brief actually lists what we have made
    cov = covered_subjects()
    ok("brief knows what we have already made", len(cov) >= 10, str(len(cov)))
    ok("dedupe list carries real slugs",
       any("iphone" in s for s in cov), "no iphone reel found in jobs/")

    if fails:
        print(f"idea_scout self-test FAILED ({len(fails)} of {checks})")
        for f in fails:
            print(f"  - {f}")
        return 1
    print(f"idea_scout self-test PASSED — {checks} checks")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--selftest" in argv:
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = selftest()
        print(buf.getvalue().strip().splitlines()[-1])
        return rc
    if "--brief" in argv:
        return brief()
    if "--check" in argv:
        return check(Path(argv[argv.index("--check") + 1]))
    print(__doc__.split("    python3")[0].strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
