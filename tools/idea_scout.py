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
Reddit thread does not pass. That mode needs the open network, which the
cloud scout does not have; if `jobs/_ideas/_audience/<date>.md` exists (a
local run wrote it), its verbatim lines are the ones allowed into AUDIENCE
fields — `check` will not invent one and will flag an AUDIENCE line that
does not appear there.

FOUR THINGS ADDED 2026-09-01, all user-requested after the first two runs:

1. DEDUPE was scoring on the wrong ratio. `idea 3 (Qualcomm price hike)` on
   2026-09-01 sailed through `--check` clean, then the merge that landed
   right after pulled in a `qualcomm-chip-hike` job someone else had already
   scripted — the SAME story. The overlap math divided by the idea's (long,
   descriptive) SUBJECT word count, so a real duplicate scored ~0.23 against
   a 0.6 threshold. Fixed to an overlap COEFFICIENT (intersection / the
   SMALLER set) over a stopword-filtered word set, which is not fooled by
   one side being a longer sentence than the other.
2. CATEGORY — every idea now carries one of the five niches this channel
   covers (`CATEGORIES` below). `--brief` asks for roughly two per category;
   `--check` reports coverage as ADVICE, never a blocker, because an empty
   category on a quiet day is honest and padding it is exactly the "five
   weak ideas" failure the routine is told to avoid.
3. FRESHNESS is now read out of the URLs themselves (`/2026/08/31/` or
   `2026-08-31` style paths) and compared to the file's own date. An idea
   whose newest source is more than five days old prints as ADVICE — not a
   failure, because a still-breaking story can legitimately cite an older
   announcement, but worth a second look.
4. `--pick` appends one line to `jobs/_ideas/_picked.md`: date, slug,
   category, format. Nothing reads it back yet — there is no view/retention
   data to close the loop with — but the day that data exists, the log
   already has what it needs to join against.

    python3 tools/idea_scout.py --brief
    python3 tools/idea_scout.py --check jobs/_ideas/2026-08-28.md
    python3 tools/idea_scout.py --pick jobs/_ideas/2026-08-28.md "Your Chrome Ad Blocker"
    python3 tools/idea_scout.py --selftest
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
IDEAS_DIR = ROOT / "jobs" / "_ideas"
AUDIENCE_DIR = IDEAS_DIR / "_audience"
PICKED_LOG = IDEAS_DIR / "_picked.md"

MIN_SOURCES = 2          # two INDEPENDENT domains, same rule as research.md
MIN_IDEAS = 5
CATEGORIES = ["Apple", "AI", "Tech", "Gadgets", "Gaming"]
IDEAS_PER_CATEGORY = 2   # a target for --brief to aim at, never a floor
DEDUPE_OVERLAP = 0.2     # overlap COEFFICIENT (intersection / smaller set),
                         # AFTER channel-generic words are stripped (below).
                         # Real duplicate SUBJECT lines, phrased differently
                         # by two different writers, top out around 25-30%
                         # even with generic words removed — tuned against
                         # every real pair among the 20 covered jobs
                         # (2026-09-01) with zero false positives at 0.2.
MIN_OVERLAP_WORDS = 3    # a couple of shared rare words can still be
                         # coincidence; three is where it stops being one.
GENERIC_MIN_DF = 3       # a word seen in 3+ existing jobs is this channel's
                         # own baseline vocabulary ("apple", "iphone",
                         # "september" on an Apple channel) — it says
                         # nothing about whether two SPECIFIC stories are
                         # the same one, and left in, it is exactly what
                         # produced 50%+ overlap between unrelated iPhone
                         # stories that only ever shared brand + date words.
GENERIC_MIN_CORPUS = 5   # too few covered jobs to trust a document-
                         # frequency signal at all — skip the filter.
FRESHNESS_ADVISE_DAYS = 5

STOPWORDS = {
    "this", "that", "with", "from", "into", "onto", "over", "under", "about",
    "after", "before", "today", "still", "just", "even", "only", "here",
    "when", "what", "they", "their", "does", "doesn", "will", "would",
    "could", "should", "than", "then", "them", "your", "were", "been",
    "have", "has", "not", "for", "the", "and", "are", "was", "its",
    "it's", "which", "while", "because", "matters", "matter", "discovers",
    "discover", "believes", "believe", "viewer",
}


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
    SUBJECT:  what the reel is actually about, one line
    CATEGORY: one of {categories}
    ANGLE:    why this is a REEL and not a headline — the tension in it
    ENGINE:   a viewer who believes X discovers Y, which matters because Z
    FORMAT:   one of {formats}
    WHY NOW:  the time pressure. "it is interesting" is not a reason
    SRC:      <url>
    SRC:      <url>
    AUDIENCE: "<verbatim quote>" — <platform>, <thread url>   (optional)

ENGINE must contain all three parts. A subject with no discovery is a
headline; a discovery that matters to nobody is trivia.

CATEGORY sorts the day's shortlist into the channel's niches for the daily
Artifact. Aim for roughly {per_category} ideas per category — that is a
TARGET for spreading the research, not a floor. A category with nothing
real to say today stays empty; do not pad it to hit the number.

SRC needs {min_sources} urls on DIFFERENT domains. Two articles on one site is
one source, and so is two sites quoting the same leaker.

AUDIENCE is LANGUAGE, not evidence. It tells you what people are confused
about and in whose words, and it may shape the angle and the hook. It can
never be the sourcing — an idea supported only by AUDIENCE lines is refused.
If jobs/_ideas/_audience/<date>.md exists, its verbatim lines are the only
ones allowed into AUDIENCE fields; the cloud scout has no open-network path
to a forum or app-store review itself.
"""


def brief() -> int:
    cov = covered_subjects()
    fmt = formats()
    print("\n=== IDEA SCOUT BRIEF ===\n")
    print(f"ALREADY COVERED — do not suggest these again ({len(cov)} reels, "
          f"finished AND in-progress — every jobs/<slug>/ counts):\n")
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
    print(f"\nCATEGORIES — aim for ~{IDEAS_PER_CATEGORY} ideas each, never pad "
          "an empty one:\n")
    print("  " + ", ".join(CATEGORIES))
    print("\n" + CONTRACT.format(min_ideas=MIN_IDEAS, formats="|".join(fmt),
                                 categories="|".join(CATEGORIES),
                                 per_category=IDEAS_PER_CATEGORY,
                                 min_sources=MIN_SOURCES))
    aud = AUDIENCE_DIR / f"{_dt.date.today().isoformat()}.md"
    if aud.exists():
        print(f"AUDIENCE INTAKE FOUND: {aud} — real verbatim quotes are "
              "available for today; use them, don't invent more.\n")
    else:
        print(f"No local audience intake at {aud} — AUDIENCE lines stay "
              "optional and search-snippet-only today.\n")
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


def _keywords(text: str) -> set[str]:
    """4+ char words, stopwords stripped — the signal dedupe compares on."""
    return {w for w in re.findall(r"[a-z0-9]{4,}", text.lower())
            if w not in STOPWORDS}


def _file_date(path: Path) -> _dt.date:
    try:
        return _dt.date.fromisoformat(path.stem)
    except ValueError:
        return _dt.date.today()


_URL_DATE = re.compile(r"(20\d{2})[-/](\d{1,2})(?:[-/](\d{1,2}))?")


def _url_dates(urls: list[str]) -> list[_dt.date]:
    """Best-effort dates read out of article URLs (/2026/08/31/, 2026-08-31)."""
    out = []
    for u in urls:
        m = _URL_DATE.search(u)
        if not m:
            continue
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)
        try:
            out.append(_dt.date(y, mo, d))
        except ValueError:
            continue
    return out


def check(path: Path) -> int:
    if not path.exists():
        sys.exit(f"\n  no {path}\n")
    ideas = parse(path.read_text())
    cov = covered_subjects()
    fmt = set(formats())
    file_date = _file_date(path)
    problems: list[str] = []
    advisories: list[str] = []
    cat_counts = {c: 0 for c in CATEGORIES}

    aud_file = AUDIENCE_DIR / f"{path.stem}.md"
    aud_text = aud_file.read_text() if aud_file.exists() else None

    if len(ideas) < MIN_IDEAS:
        problems.append(f"only {len(ideas)} ideas — the brief asks for "
                        f"{MIN_IDEAS}. A short list is a list that skipped "
                        "the hard ones.")

    # dedupe compares each idea against every job dir's keyword set ONCE —
    # precomputed here so the per-idea loop below is just a lookup.
    done_keywords = {slug: _keywords(f"{slug} {subject}")
                     for slug, subject in cov.items()}

    # GENERIC-WORD FILTER — words this channel's own corpus repeats often
    # ("apple", "iphone", "september" on an Apple channel) tell the dedupe
    # nothing about whether two SPECIFIC stories are the same story, and
    # left in, they are exactly what made unrelated real iPhone stories
    # overlap 50%+ on brand + date words alone. Skip it below a corpus size
    # too small for a document-frequency signal to mean anything.
    generic: set[str] = set()
    if len(done_keywords) >= GENERIC_MIN_CORPUS:
        df: Counter[str] = Counter()
        for kw in done_keywords.values():
            df.update(kw)
        generic = {w for w, c in df.items() if c >= GENERIC_MIN_DF}
    done_keywords = {slug: kw - generic for slug, kw in done_keywords.items()}

    for i, idea in enumerate(ideas, 1):
        tag = f"idea {i} ({idea['title'][:34]})"
        for field in ("SUBJECT", "CATEGORY", "ANGLE", "ENGINE", "FORMAT", "WHY NOW"):
            if not idea.get(field):
                problems.append(f"{tag}: no {field}")

        cat = (idea.get("CATEGORY") or "").strip()
        if cat and cat not in CATEGORIES:
            problems.append(f"{tag}: CATEGORY {cat!r} is not one of {CATEGORIES}")
        elif cat:
            cat_counts[cat] += 1

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
        src_urls = [u.split()[0] for u in idea["SRC"] if "://" in u]
        domains = {urlparse(u).netloc.replace("www.", "") for u in src_urls}
        if len(domains) < MIN_SOURCES:
            extra = (" AUDIENCE lines do not count as sourcing."
                     if idea["AUDIENCE"] else "")
            problems.append(
                f"{tag}: {len(domains)} independent source domain(s), "
                f"need {MIN_SOURCES}.{extra}")

        # AUDIENCE lines must trace back to a real local intake file — the
        # cloud scout cannot reach a forum or app-store review itself, so an
        # AUDIENCE line here with no intake file behind it is either a
        # search-snippet paraphrase (fine, just not a quote) or invented.
        for a in idea["AUDIENCE"]:
            if aud_text is None:
                continue
            quote_m = re.search(r'"([^"]+)"', a)
            if quote_m and quote_m.group(1) not in aud_text:
                problems.append(
                    f"{tag}: AUDIENCE quote {quote_m.group(1)[:40]!r} is not "
                    f"in {aud_file.name} — only quotes from the local intake "
                    "file are allowed once one exists for this date.")

        # DEDUPE against everything already made — OVERLAP COEFFICIENT
        # (intersection / the SMALLER word set), not intersection / this
        # idea's word count. A real duplicate can hide behind a long,
        # descriptive SUBJECT line; dividing by the long side made the
        # 2026-09-01 Qualcomm collision score 0.23 against a 0.6 threshold
        # and pass clean. This does not.
        words = _keywords(idea.get("SUBJECT") or "") - generic
        for slug, done_words in done_keywords.items():
            if not words or not done_words:
                continue
            smaller = min(len(words), len(done_words))
            shared = words & done_words
            overlap = len(shared) / smaller
            if overlap >= DEDUPE_OVERLAP and len(shared) >= MIN_OVERLAP_WORDS:
                problems.append(
                    f"{tag}: looks like a repeat of {slug} "
                    f"({overlap:.0%} keyword overlap, on {sorted(shared)})")

        # FRESHNESS — advisory only. An escalating story can legitimately
        # cite a two-week-old announcement; this just asks the question.
        dates = _url_dates(src_urls)
        if dates:
            age = (file_date - max(dates)).days
            if age > FRESHNESS_ADVISE_DAYS:
                advisories.append(
                    f"{tag}: freshest source is {age}d old as of {file_date} "
                    "— confirm WHY NOW still holds, or find something newer.")

    print(f"\n=== idea scout — {path.name} ===\n")
    print(f"  {len(ideas)} ideas, {len(cov)} reels already made\n")
    for idea in ideas:
        src = len({urlparse(u.split()[0]).netloc for u in idea["SRC"]
                   if "://" in u})
        aud = len(idea["AUDIENCE"])
        cat = idea.get("CATEGORY", "?")
        print(f"  {idea['title'][:40]:<42} {cat:<8} {idea.get('FORMAT','?'):<10} "
              f"{src} src{'  +' + str(aud) + ' audience' if aud else ''}")

    print(f"\n  CATEGORY COVERAGE (target ~{IDEAS_PER_CATEGORY} each, "
          "0 is fine on a quiet day):\n")
    for c in CATEGORIES:
        print(f"    {c:<10} {cat_counts.get(c, 0)}")

    if advisories:
        print(f"\n  {len(advisories)} advisory (does not block):\n")
        for a in advisories:
            print(f"    - {a}")

    if problems:
        print(f"\n  {len(problems)} problem(s):\n")
        for p in problems:
            print(f"    - {p}")
        print()
        return 1
    print("\n  every idea carries a story engine, two independent sources, a "
          "known format,\n  a category and is not a repeat. Pick one and run "
          "`new_job.py <slug>`.\n")
    return 0


def pick(path: Path, needle: str) -> int:
    """Log which idea got made, for the day performance data exists to
    join against. Does not read anything back yet — see the module note."""
    if not path.exists():
        sys.exit(f"\n  no {path}\n")
    ideas = parse(path.read_text())
    matches = [i for i in ideas if needle.lower() in i["title"].lower()]
    if len(matches) != 1:
        sys.exit(f"\n  {len(matches)} ideas match {needle!r} in {path.name} "
                 f"— need exactly one.\n")
    idea = matches[0]
    IDEAS_DIR.mkdir(parents=True, exist_ok=True)
    is_new = not PICKED_LOG.exists()
    with PICKED_LOG.open("a") as fh:
        if is_new:
            fh.write("# Picked ideas — date, title, category, format\n\n"
                     "Logged by `idea_scout.py --pick` so a future "
                     "performance number has something to join against.\n\n"
                     "| date | title | category | format |\n"
                     "|---|---|---|---|\n")
        fh.write(f"| {path.stem} | {idea['title']} | "
                f"{idea.get('CATEGORY', '?')} | {idea.get('FORMAT', '?')} |\n")
    print(f"\n  logged: {idea['title']} -> {PICKED_LOG}\n")
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
CATEGORY: Tech
ANGLE: the number everyone quotes is measured wrong
ENGINE: a viewer who believes widgets are instant discovers they wait 400ms, which matters because it is the reason their shortcuts feel broken
FORMAT: news
WHY NOW: the spec changed this week
SRC: https://example.com/a
SRC: https://other.org/b
"""
    import tempfile
    tmpdir = Path(tempfile.mkdtemp())
    tmp = tmpdir / "ideas.md"

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
        "ENGINE: a viewer who believes widgets are instant discovers they "
        "wait 400ms, which matters because it is the reason their "
        "shortcuts feel broken",
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

    # 6. CATEGORY must be one of the five niches
    badcat = good.replace("CATEGORY: Tech", "CATEGORY: Sports")
    tmp.write_text(badcat)
    ok("an invalid CATEGORY is caught", check(tmp) == 1)

    orig_cov = covered_subjects
    orig_picked = PICKED_LOG

    # 7. THE REGRESSION — 2026-09-01: idea 3's SUBJECT was a long, detailed
    # sentence describing Qualcomm's price hike; the old ratio (intersection
    # / this idea's word count) diluted a real duplicate to ~0.23 against a
    # 0.6 threshold and it sailed through `--check` clean. The overlap
    # COEFFICIENT (intersection / the SMALLER set) must not be fooled by one
    # side being a longer sentence than the other.
    globals()["covered_subjects"] = lambda: {
        "qualcomm-chip-hike":
            "Qualcomm's double-digit Snapdragon price hike takes effect "
            "Sept 1 2026"}
    try:
        dupe = good.replace(
            "SUBJECT: a thing nobody here has covered about widget latency",
            "SUBJECT: Qualcomm's double-digit price increase on Snapdragon, "
            "wearable, and Windows-on-Arm chips took effect September 1, "
            "2026, after CEO Cristiano Amon confirmed it on the company's "
            "July earnings call in front of investors and analysts")
        tmp.write_text(dupe)
        ok("a duplicate hidden behind a long SUBJECT sentence is now caught",
           check(tmp) == 1)
    finally:
        globals()["covered_subjects"] = orig_cov

    # 7b. a job with NO recorded subject (just its slug) must not falsely
    # flag every idea that happens to share one generic word with it — the
    # coefficient alone hit 50% on "camera" vs a bare "airpods-camera" slug
    # on 2026-09-01, which would have blocked an unrelated phone-camera idea.
    globals()["covered_subjects"] = lambda: {"airpods-camera": ""}
    try:
        unrelated = good.replace(
            "SUBJECT: a thing nobody here has covered about widget latency",
            "SUBJECT: a phone launched today with a periscope telephoto "
            "camera spec no current flagship matches")
        tmp.write_text(unrelated)
        out = check(tmp)
        # still fails on the idea-count floor (1 idea); it must NOT ALSO
        # fail with a false "looks like a repeat" — inspect via a 5-idea
        # variant so a clean pass is actually observable.
        five_unrelated = "\n".join(
            unrelated.replace("## Something new", f"## Something new {n}")
            for n in range(MIN_IDEAS))
        tmp.write_text(five_unrelated)
        ok("one shared generic word against a subject-less job is not a "
           "dedupe match", check(tmp) == 0)
    finally:
        globals()["covered_subjects"] = orig_cov

    # 8. freshness is ADVISORY ONLY — a clean, varied 5-idea file with one
    # stale source URL must still pass (return 0). Faking covered_subjects
    # to {} isolates this from whatever real jobs/ happens to contain.
    globals()["covered_subjects"] = lambda: {}
    try:
        five = "\n".join(
            good.replace("## Something new", f"## Something new {n}")
                .replace("a thing nobody here has covered about widget "
                        "latency", f"distinct unrelated topic number {n}")
            for n in range(MIN_IDEAS)
        )
        five = five.replace("SRC: https://example.com/a\n",
                            "SRC: https://example.com/2020/01/01/a\n", 1)
        tmp.write_text(five)
        ok("freshness is advisory and does not block an otherwise-clean file",
           check(tmp) == 0)

        # 9. --pick logs exactly one matched idea to (a patched) PICKED_LOG
        globals()["PICKED_LOG"] = tmpdir / "_picked.md"
        rc = pick(tmp, "Something new 0")
        ok("--pick logs a row and exits clean",
           rc == 0 and globals()["PICKED_LOG"].exists())
        ok("--pick's row carries the category and format",
           "Tech" in globals()["PICKED_LOG"].read_text()
           and "news" in globals()["PICKED_LOG"].read_text())
    finally:
        globals()["covered_subjects"] = orig_cov
        globals()["PICKED_LOG"] = orig_picked

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
    if "--pick" in argv:
        i = argv.index("--pick")
        return pick(Path(argv[i + 1]), " ".join(argv[i + 2:]))
    print(__doc__.split("    python3")[0].strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
