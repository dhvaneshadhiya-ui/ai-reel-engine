#!/usr/bin/env python3
"""The critique pass: score the cut as a motion director who owes it nothing.

Adopted 2026-10-02 from the motion-reel plugin (MIT, Aries Spring) and adapted
to this engine. Our own STEP 5 asked "read every frame as a hostile viewer" and
left the verdict to whoever had just made the thing; v2 of
ios27-settings-longform passed it with a dark dip at every cut, 148 sounds and
a 5-second empty page. A score per axis, the worst three with a concrete fix,
and a verdict that needs every score at 8+ makes that review hard to wave
through.

    python3 tools/critique.py <slug>           # build the sheet + facts, print the brief
    python3 tools/critique.py --check <slug>   # exit 1 unless the last round is READY
    python3 tools/critique.py --demo

The round goes in jobs/<slug>/critique.md, newest last, in exactly this shape:

    ## Round 1
    | hook | read | motion | variety | sync | match | min |
    |  6   |  8   |   5    |    7    |  7   |   9   |  5  |
    Worst three: ...
    Verdict: ANOTHER ROUND

READY needs every score >= 8 and round 3 or later. Rounds 1-2 may be scored on
preflight stills (tools/preflight_stills.py) so a round does not cost a render.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
AXES = ("hook", "read", "motion", "variety", "sync", "match")

BRIEF = """
CRITIQUE PASS — round {n} of {slug}. You did not make this cut and owe it nothing.
Find the three things that most hurt it and say exactly how to fix them.

LOOK AT (open every one; do not score from memory of the plan):
  {sheet}   one frame per scene at PHONE size
  the facts printed above, the shot plan, and the script.

SCORE 1-10, each with one line of evidence (scene number + what you see):
  hook     frame 0 already interesting; the first 2s stop a thumb
  read     every word readable on the phone-size sheet, clear of captions and UI
  motion   arrivals have direction and weight; nothing fades in from nothing;
           nothing scales type (it shakes); nothing linear unless mechanical
  variety  something new every 2-4s; shot types and scale change; no trick repeats
  sync     every accent has a sound, the mix breathes, voice always on top
  match    every scene shows what is being SAID while it is up (Rule 3);
           real product only — a redraw carries its illustration label

CHECK, pass/fail each:
  [ ] no empty page: no scene opens on bare background
  [ ] longest gap without a new event (above) — say which scene and why
  [ ] one accent colour; captions never touch content
  [ ] the end card holds long enough to read twice

APPEND to jobs/{slug}/critique.md, exactly:
  ## Round {n}
  | hook | read | motion | variety | sync | match | min |
  |  x   |  x   |   x    |    x    |  x   |   x   |  x  |
  Worst three: 1. [scene, time] WHAT -> WHY it hurts the viewer -> FIX (which
  file, which value, what changes on screen)  2. ...  3. ...
  Checks failed: ...
  Verdict: ANOTHER ROUND | READY   (READY only if every score >= 8, no failed
  checks, and this is round 3 or later)
"""


def rounds(text: str) -> list[dict]:
    """Every '## Round N' with its six scores and its verdict."""
    out = []
    for m in re.finditer(r"^## Round (\d+)(.*?)(?=^## Round |\Z)", text, re.S | re.M):
        rows = [r for r in m.group(2).splitlines() if r.strip().startswith("|")]
        nums = [int(x) for x in re.findall(r"\d+", rows[1])] if len(rows) > 1 else []
        verdict = re.search(r"Verdict:\s*(READY|ANOTHER ROUND)", m.group(2))
        out.append({"n": int(m.group(1)), "scores": nums[:len(AXES)],
                    "verdict": verdict.group(1) if verdict else None})
    return out


def problem(text: str) -> str | None:
    """Why the last round does not clear the bar, or None."""
    rs = rounds(text)
    if not rs:
        return "no '## Round N' in critique.md — run the critique pass"
    last = rs[-1]
    if len(last["scores"]) < len(AXES):
        return f"round {last['n']} scores {len(last['scores'])} of {len(AXES)} axes"
    if last["verdict"] != "READY":
        return f"round {last['n']} verdict is {last['verdict'] or 'missing'}, not READY"
    low = [f"{a} {s}" for a, s in zip(AXES, last["scores"]) if s < 8]
    if low:
        return f"round {last['n']} says READY with {', '.join(low)} — READY needs every score >= 8"
    if last["n"] < 3:
        return f"READY at round {last['n']} — the bar is round 3 or later"
    return None


def facts(slug: str) -> list[str]:
    """What a reviewer should not have to estimate: gaps and sound density."""
    from reel_gates import slide_reveals
    beats = json.loads((ROOT / f"src/beats/{slug}.json").read_text())
    scenes, t, gaps, cues = beats.get("scenes") or [], 0.0, [], 0
    for i, sc in enumerate(scenes):
        d = float(sc.get("durationSec") or 0)
        if sc.get("type") == "slide" and not any(b.get("kind") == "clip" for b in sc.get("blocks") or []):
            rv = slide_reveals(sc)
            g, a = max((b - a, a) for a, b in zip(rv, rv[1:]))
            gaps.append((g, i, t + a))
        cues += len(sc.get("sfx") or [])
        t += d
    gaps.sort(reverse=True)
    out = [f"runtime {t:.1f}s, {len(scenes)} scenes, {cues} sound cues "
           f"(one every {t / max(cues, 1):.1f}s)"]
    out += [f"gap {g:.1f}s with nothing new: scene {i:02d} from {a:.1f}s" for g, i, a in gaps[:5] if g > 4.0]
    return out


def sheet(slug: str) -> Path:
    """One frame per scene from the final render, at a third of its size."""
    video = ROOT / "out" / f"{slug}-final.mp4"
    beats = json.loads((ROOT / f"src/beats/{slug}.json").read_text())
    dest = ROOT / "out" / f"{slug}-lint" / "phone-sheet.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    t, mids = 0.0, []
    for sc in beats.get("scenes") or []:
        d = float(sc.get("durationSec") or 0)
        mids.append(t + d / 2)
        t += d
    with tempfile.TemporaryDirectory() as td:
        for k, m in enumerate(mids):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{m:.2f}", "-i", str(video),
                            "-frames:v", "1", "-vf", "scale=iw/3:-2", f"{td}/{k:03d}.png"], check=True)
        cols = 6 if beats.get("format") == "longform" else 8
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{td}/%03d.png", "-vf",
                        f"tile={cols}x{-(-len(mids) // cols)}:padding=6", "-frames:v", "1", str(dest)], check=True)
    return dest


def demo() -> int:
    row = "| hook | read | motion | variety | sync | match | min |\n"
    ok = f"## Round 3\n{row}| 8 | 9 | 8 | 8 | 9 | 9 | 8 |\nVerdict: READY\n"
    assert problem(ok) is None
    assert "round 3 or later" in problem(ok.replace("Round 3", "Round 2"))
    assert "every score" in problem(ok.replace("| 8 | 9 | 8 |", "| 8 | 9 | 6 |"))
    assert "not READY" in problem(ok.replace("READY", "ANOTHER ROUND"))
    assert "no '## Round" in problem("")
    two = f"## Round 3\n{row}| 9 | 9 | 9 | 9 | 9 | 9 | 9 |\nVerdict: READY\n" + ok.replace("Round 3", "Round 4").replace("| 8 | 9 | 8 |", "| 5 | 9 | 8 |")
    assert "hook 5" in problem(two), "the LAST round decides"
    print("critique self-check passed — READY needs 8+ on every axis at round 3 or later")
    return 0


def main() -> int:
    a = sys.argv[1:]
    if "--demo" in a:
        return demo()
    slugs = [x for x in a if not x.startswith("-")]
    if not slugs:
        print(__doc__)
        return 1
    slug = slugs[0]
    record = ROOT / "jobs" / slug / "critique.md"
    text = record.read_text() if record.exists() else ""
    if "--check" in a:
        why = problem(text)
        print(f"  critique: {why}" if why else f"  critique: READY ({record.relative_to(ROOT)})")
        return 1 if why else 0
    for line in facts(slug):
        print(f"  {line}")
    path = sheet(slug)
    print(BRIEF.format(n=len(rounds(text)) + 1, slug=slug, sheet=path.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
