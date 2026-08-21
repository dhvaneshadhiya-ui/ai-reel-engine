#!/usr/bin/env python3
"""Join a published reel's retention curve to its beat sheet.

WHY THIS EXISTS
---------------
Every number in FORMATS came from teardowns of OTHER people's reels, because
that was the only data that existed. Our own published reels are the ground
truth nobody was using — and this pipeline has an advantage no teardown has:
the beat sheet knows what is on screen at every frame. Join the retention
curve to that timeline and "retention dipped at 40s" becomes "the specsheet
at 40s bleeds 1.9pp/s while footage bleeds 0.4pp/s" — a measured, per-scene-
type answer to questions the gates currently answer with borrowed numbers.

G23's discipline, finally pointed at our own output: derived, never invented.

GETTING THE DATA (v1 does NOT do OAuth — the join is the value, fetching is
commodity):
  * YouTube Studio -> Analytics -> Advanced mode -> Audience retention ->
    Export current view -> CSV. Zero setup. Columns: video position,
    absolute retention, (optionally) relative retention.
  * Or the Analytics API (needs OAuth once): dimension elapsedVideoTimeRatio,
    metrics audienceWatchRatio,relativeRetentionPerformance — 100 rows per
    video. Save the JSON and pass --api-json.
  * Instagram exposes NO per-second retention by API or export. Reels
    Insights give aggregates only; record those by hand in packaging notes.
    This tool is YouTube-curve-only, on purpose, until that changes.

    python3 tools/retention_ingest.py <slug> --csv chart.csv \\
        [--duration 76.1] [--views 12400] [--title "..."]
    python3 tools/retention_ingest.py <slug> --api-json rows.json ...
    python3 tools/retention_ingest.py --aggregate      # cross-reel table
    python3 tools/retention_ingest.py --selftest

Writes jobs/<slug>/performance.json (previous ingests kept under "history").

HONEST LIMITS, so nobody oversells a curve:
  * The beat sheet is the PRE-pace-cut timeline. If tools/pace_reel.py
    trimmed silences, the published video is shorter and cuts are
    non-uniform; this tool scales proportionally and WARNS when the
    published duration differs >2% from the sheet. Treat per-scene numbers
    as approximate on a pace-cut reel.
  * 100 points on a ~75s reel is ~0.75s resolution — a 1.7s hook spans two
    points. Scene types are trustworthy; single short scenes are noisy.
  * Under ~500 views a retention curve is mostly noise. The tool warns; it
    cannot fix sample size.
  * audienceWatchRatio can exceed 1.0 — a segment replayed more times than
    the video has views. Upticks are REPLAYS, and on a spec card they are a
    good sign (people pausing to read), not an error.

FORMATS RE-DERIVATION IS A HUMAN STEP. --aggregate prints the evidence; the
numbers land in reel_gates.FORMATS only via a dated STYLE-RULES entry, and
not before several reels agree. One curve is an anecdote.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MIN_VIEWS_FOR_SIGNAL = 500
SCALE_WARN = 0.02          # sheet vs published duration mismatch
REPLAY_EPS = 0.005         # uptick size that counts as a replay


# ---------------------------------------------------------------- curve input

def _to_ratio(v: str | float) -> float:
    if isinstance(v, str):
        v = v.strip().rstrip("%").replace(",", "")
    return float(v)


def load_curve_csv(text: str) -> list[tuple[float, float, float | None]]:
    """Studio export: liberal about header names and %-vs-ratio units."""
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        sys.exit("empty CSV")
    head = [h.lower() for h in rows[0]]

    def col(*words):
        for i, h in enumerate(head):
            if all(w in h for w in words):
                return i
        return None
    pos = col("position")
    ab = col("absolute") or col("watch")
    rel = col("relative")
    if pos is None or ab is None:
        sys.exit(f"CSV header not recognised: {rows[0]!r} — need a position "
                 "column and an absolute/watch column (Studio 'Audience "
                 "retention' export).")
    out = []
    for r in rows[1:]:
        if len(r) <= max(pos, ab) or not r[pos].strip():
            continue
        out.append((_to_ratio(r[pos]), _to_ratio(r[ab]),
                    _to_ratio(r[rel]) if rel is not None and len(r) > rel
                    and r[rel].strip() else None))
    return _normalise(out)


def load_curve_api(text: str) -> list[tuple[float, float, float | None]]:
    """API response: {"rows": [[ratio, watch, rel], ...]} or a bare list."""
    d = json.loads(text)
    rows = d.get("rows") if isinstance(d, dict) else d
    if not rows:
        sys.exit("no rows in API JSON")
    out = []
    for r in rows:
        out.append((float(r[0]), float(r[1]),
                    float(r[2]) if len(r) > 2 and r[2] is not None else None))
    return _normalise(out)


def _normalise(pts) -> list[tuple[float, float, float | None]]:
    """Positions to 0..1 ratios; sorted; sanity-checked."""
    if not pts:
        sys.exit("no data points parsed")
    mx = max(p[0] for p in pts)
    if mx > 1.5:                      # positions were percentages
        pts = [(p / 100.0, w if w <= 1.5 else w / 100.0, r)
               for p, w, r in pts]
    else:
        pts = [(p, w if w <= 1.5 else w / 100.0, r) for p, w, r in pts]
    pts.sort()
    if len(pts) < 20:
        sys.exit(f"only {len(pts)} points — that is not a retention curve.")
    return pts


def watch_at(curve, ratio: float) -> float:
    """Linear interpolation on the curve."""
    prev = curve[0]
    for pt in curve:
        if pt[0] >= ratio:
            if pt[0] == prev[0]:
                return pt[1]
            f = (ratio - prev[0]) / (pt[0] - prev[0])
            return prev[1] + f * (pt[1] - prev[1])
        prev = pt
    return curve[-1][1]


# ---------------------------------------------------------------- the join

def timeline(sheet: dict) -> list[dict]:
    t, out = 0.0, []
    for i, sc in enumerate(sheet["scenes"]):
        d = float(sc["durationSec"])
        out.append(dict(i=i, type=sc.get("type", "?"), start=t, end=t + d))
        t += d
    return out


def analyze(sheet: dict, curve, video_secs: float | None,
            views: int | None) -> dict:
    scenes = timeline(sheet)
    sheet_secs = scenes[-1]["end"]
    secs = video_secs or sheet_secs
    scaled = abs(secs - sheet_secs) / sheet_secs > SCALE_WARN
    warnings = []
    if scaled:
        warnings.append(
            f"published {secs:.1f}s vs sheet {sheet_secs:.1f}s "
            f"({(secs / sheet_secs - 1) * 100:+.1f}%) — pace_reel or an edit "
            "moved the timeline; the join is scaled proportionally and "
            "per-scene numbers are APPROXIMATE.")
    if views is not None and views < MIN_VIEWS_FOR_SIGNAL:
        warnings.append(f"{views} views — under {MIN_VIEWS_FOR_SIGNAL}, the "
                        "curve is mostly noise. Re-ingest when it has aged.")

    per = []
    for sc in scenes:
        r0, r1 = sc["start"] / sheet_secs, sc["end"] / sheet_secs
        w0, w1 = watch_at(curve, r0), watch_at(curve, r1)
        dur = sc["end"] - sc["start"]
        rels = [r for p, _, r in curve if r0 <= p <= r1 and r is not None]
        per.append(dict(
            i=sc["i"], type=sc["type"],
            start=round(sc["start"], 2), end=round(sc["end"], 2),
            watchStart=round(w0, 4), watchEnd=round(w1, 4),
            ppLost=round((w0 - w1) * 100, 2),
            ppLostPerSec=round((w0 - w1) * 100 / dur, 3) if dur else 0.0,
            relAvg=round(sum(rels) / len(rels), 3) if rels else None))

    by: dict[str, dict] = {}
    for p in per:
        b = by.setdefault(p["type"], dict(seconds=0.0, ppLost=0.0, scenes=0))
        b["seconds"] += p["end"] - p["start"]
        b["ppLost"] += p["ppLost"]
        b["scenes"] += 1
    for b in by.values():
        b["seconds"] = round(b["seconds"], 2)
        b["ppLost"] = round(b["ppLost"], 2)
        b["ppLostPerSec"] = round(b["ppLost"] / b["seconds"], 3) \
            if b["seconds"] else 0.0

    replays = []
    prev = None
    for p, w, _ in curve:
        if prev is not None and w > prev + REPLAY_EPS:
            t = p * sheet_secs
            sc = next((s for s in scenes if s["start"] <= t < s["end"]),
                      scenes[-1])
            replays.append(dict(at=round(t, 1), scene=sc["i"],
                                type=sc["type"], uptick=round(w - prev, 4)))
        prev = w
    replays.sort(key=lambda r: -r["uptick"])

    return dict(
        sheetSeconds=round(sheet_secs, 2),
        videoSeconds=round(secs, 2), timelineScaled=scaled,
        views=views, warnings=warnings,
        hookWatchAt2s=round(watch_at(curve, 2.0 / sheet_secs), 4),
        curve=[[round(p, 4), round(w, 4),
                round(r, 4) if r is not None else None]
               for p, w, r in curve],
        scenes=per, byType=by, replays=replays[:8])


# ---------------------------------------------------------------- reporting

def report(a: dict) -> None:
    print(f"\n  {a['videoSeconds']}s published · sheet {a['sheetSeconds']}s "
          f"· hook watch @2s: {a['hookWatchAt2s'] * 100:.0f}%")
    for w in a["warnings"]:
        print(f"  ! {w}")
    print("\n  scene types, worst bleed first (pp lost per second on screen):")
    for t, b in sorted(a["byType"].items(),
                       key=lambda kv: -kv[1]["ppLostPerSec"]):
        print(f"    {t:16} {b['ppLostPerSec']:6.3f} pp/s over "
              f"{b['seconds']:5.1f}s in {b['scenes']} scene(s)")
    worst = sorted(a["scenes"], key=lambda s: -s["ppLostPerSec"])[:3]
    print("\n  worst single scenes:")
    for s in worst:
        print(f"    scene {s['i']:02d} ({s['type']}) {s['start']}-{s['end']}s"
              f"  -{s['ppLost']}pp ({s['ppLostPerSec']}pp/s)")
    if a["replays"]:
        print("\n  replayed (watch ratio rose — people rewound to look):")
        for r in a["replays"][:4]:
            print(f"    {r['at']}s scene {r['scene']:02d} ({r['type']}) "
                  f"+{r['uptick']}")
    print("\n  One curve is an anecdote. FORMATS numbers move only via a "
          "dated\n  STYLE-RULES entry, after --aggregate shows several reels "
          "agreeing.")


def aggregate() -> None:
    rows: dict[str, dict] = {}
    n = 0
    for p in sorted(ROOT.glob("jobs/*/performance.json")):
        rec = json.loads(p.read_text())
        a = rec.get("latest") or rec
        n += 1
        for t, b in a.get("byType", {}).items():
            r = rows.setdefault(t, dict(seconds=0.0, ppLost=0.0, reels=0))
            r["seconds"] += b["seconds"]
            r["ppLost"] += b["ppLost"]
            r["reels"] += 1
    if not rows:
        sys.exit("no jobs/*/performance.json yet — publish, export the "
                 "retention CSV from Studio, ingest, then aggregate.")
    print(f"\n  {n} reel(s) ingested. pp lost per on-screen second, by type:")
    for t, r in sorted(rows.items(),
                       key=lambda kv: -(kv[1]["ppLost"] / kv[1]["seconds"]
                                        if kv[1]["seconds"] else 0)):
        pps = r["ppLost"] / r["seconds"] if r["seconds"] else 0
        print(f"    {t:16} {pps:6.3f} pp/s · {r['seconds']:6.1f}s across "
              f"{r['reels']} reel(s)")
    print(f"\n  Evidence, not law: with {n} reel(s), re-derive FORMATS only "
          "when several\n  agree, via a dated STYLE-RULES entry (G23).")


# ---------------------------------------------------------------- selftest

def selftest() -> int:
    ok = True

    def check(label, cond):
        nonlocal ok
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        ok = ok and cond

    # CSV variants: percent strings with %, plain ratios, missing relative
    c1 = load_curve_csv("Video position (%),Absolute audience retention (%),"
                        "Relative audience retention (%)\n" + "\n".join(
                            f"{i}%,{100 - i}%,{50 + i / 10}%"
                            for i in range(0, 101, 2)))
    check("CSV with %-strings parses", len(c1) == 51 and c1[0][1] == 1.0)
    c2 = load_curve_csv("position,watch ratio\n" + "\n".join(
        f"{i / 100},{1 - i / 200}" for i in range(0, 101, 2)))
    check("CSV with bare ratios and no relative parses",
          len(c2) == 51 and c2[-1][2] is None)
    c3 = load_curve_api(json.dumps(
        {"rows": [[i / 100, 1 - i / 200, 0.5] for i in range(0, 101, 2)]}))
    check("API JSON parses", len(c3) == 51 and c3[0][2] == 0.5)

    # The join: 10s sheet — 2s footage hook, 3s specsheet, 5s footage.
    # Curve loses 5pp/s inside the specsheet, 1pp/s elsewhere.
    sheet = {"scenes": [
        {"type": "footage", "durationSec": 2.0},
        {"type": "specsheet", "durationSec": 3.0},
        {"type": "footage", "durationSec": 5.0}]}

    def synth(t):                      # piecewise watch ratio at second t
        if t <= 2:
            return 1.0 - 0.01 * t
        if t <= 5:
            return 0.98 - 0.05 * (t - 2)
        return 0.83 - 0.01 * (t - 5)
    curve = [(t / 10, synth(t), None) for t in
             [i * 0.1 for i in range(101)]]
    a = analyze(sheet, curve, None, views=10000)
    by = a["byType"]
    check("specsheet bleeds worst",
          by["specsheet"]["ppLostPerSec"] > by["footage"]["ppLostPerSec"])
    check("specsheet rate ~5pp/s",
          abs(by["specsheet"]["ppLostPerSec"] - 5.0) < 0.3)
    check("no scale warning when durations match", not a["timelineScaled"])

    a2 = analyze(sheet, curve, video_secs=9.0, views=10000)
    check("scale warning fires on pace-cut duration", a2["timelineScaled"]
          and any("APPROXIMATE" in w for w in a2["warnings"]))
    a3 = analyze(sheet, curve, None, views=120)
    check("low-views warning fires",
          any("noise" in w for w in a3["warnings"]))

    bump = [(p, w + (0.05 if abs(p - 0.35) < 0.02 else 0), r)
            for p, w, r in curve]
    a4 = analyze(sheet, bump, None, views=10000)
    check("replay uptick detected in the right scene",
          a4["replays"] and a4["replays"][0]["type"] == "specsheet")

    print("\n  retention selftest "
          + ("PASSED" if ok else "FAILED") + "\n")
    return 0 if ok else 1


# ---------------------------------------------------------------- main

def main() -> None:
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    if "--aggregate" in argv:
        aggregate()
        return
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug = args[0]

    def opt(name, cast=str):
        if name in argv:
            i = argv.index(name)
            return cast(argv[i + 1]) if i + 1 < len(argv) else None
        return None

    sheet_p = ROOT / f"src/beats/{slug}.json"
    if not sheet_p.exists():
        sys.exit(f"no beat sheet at {sheet_p} — the join needs the timeline "
                 "of what was on screen.")
    sheet = json.loads(sheet_p.read_text())

    csv_p, api_p = opt("--csv"), opt("--api-json")
    if not csv_p and not api_p:
        sys.exit("need --csv <studio-export> or --api-json <rows.json> — "
                 "see the docstring for where each comes from.")
    text = Path(csv_p or api_p).read_text()
    curve = load_curve_csv(text) if csv_p else load_curve_api(text)

    a = analyze(sheet, curve, opt("--duration", float), opt("--views", int))
    a["platform"] = opt("--platform") or "youtube"
    a["title"] = opt("--title")
    a["ingestedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    out = ROOT / f"jobs/{slug}/performance.json"
    hist = []
    if out.exists():
        old = json.loads(out.read_text())
        hist = old.get("history", [])
        if "latest" in old:
            prev = dict(old["latest"])
            prev.pop("curve", None)      # history keeps stats, not 100 points
            hist.append(prev)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"slug": slug, "latest": a, "history": hist},
                              indent=2))
    print(f"  wrote {out}")
    report(a)


if __name__ == "__main__":
    main()
