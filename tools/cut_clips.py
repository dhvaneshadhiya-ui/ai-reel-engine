#!/usr/bin/env python3
"""Cut ONE long screen recording into the per-beat clips a shot plan needs.

WHY THIS EXISTS
---------------
chatgpt-stickers shipped because the user hand-cut 18 clips — beat00 through
beat20 — one per beat, before the pipeline ever saw them. Nothing in this repo
does that. `compile_shot_plan` plays what it is given from `from` for
`durationSec`; `cut_sheet.py` only REPORTS a cut. So the one manual step left
in an otherwise automated pipeline was the scissors, and it is the step that
scales worst: every extra beat is another trim by hand.

WHAT CAN AND CANNOT BE AUTOMATED HERE
-------------------------------------
The shot plan already knows exactly how long each beat runs — it is anchored to
spoken phrases and the whisper timings, which exist before any footage does. So
the DURATIONS are free.

What is NOT free is knowing WHICH moment of the recording belongs to which
line. That is a judgement about content — "this is where the style picker
opens" — and no amount of scene detection produces it. Anyone claiming
otherwise ships clips that do not match the narration, which is Rule 3.

So this tool splits at that seam, honestly:

    --scan   finds every visual change in the recording and contact-sheets
             them WITH timestamps, so a human or the agent can read off which
             moment is which. This is the part a machine is good at.
    --cut    given that mapping, cuts each beat to the exact length its line
             needs. This is the part a machine should never have left to a
             human.

The mapping in between is `jobs/<slug>/clip-map.json`, written by whoever read
the sheet:

    {"shots": {"3": 12.4, "4": 15.8}}      shot index -> seconds into the source

A shot with no entry is skipped, not guessed.

    python3 tools/cut_clips.py --scan _sources/foo/screen.mp4
    python3 tools/cut_clips.py --cut foo _sources/foo/screen.mp4
    python3 tools/cut_clips.py --selftest
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# A UI change is a much smaller pixel delta than a camera cut: a sheet sliding
# up or a keyboard appearing moves a fraction of the frame, so ffmpeg's usual
# 0.3-0.4 b-roll threshold finds nothing on a screen recording.
#
# MEASURED, on _sources/chatgpt-stickers/ChatGPT Video 3.mov — 17.6s, from
# which 8 beats were cut by hand (beat11-16, 19, 20):
#
# MEASURED across all three of chatgpt-stickers' raw recordings, against the
# number of beats actually cut from each by hand. Candidates AFTER the MIN_GAP
# merge, which is the number that reaches the contact sheet:
#
#   recording          length   beats cut   @0.01/0.25   @0.02/0.25
#   ChatGPT Video 1    10.1s        3           23           23
#   ChatGPT Video 2    21.2s        6           27           23
#   ChatGPT Video 3    17.6s        9           10            8
#
# 0.01 with a 0.25s merge is chosen because it NEVER offers fewer candidates
# than there were real moments. 0.02 under-detects Video 3 (8 for 9), and an
# under-detected moment cannot be chosen at all, while a spare tile costs a
# glance. The over-detection is 1.1x-7.7x and that is the intended direction:
# this feeds a sheet a human reads, not an automatic cut.
#
# (The first draft used 0.08 with a comment claiming it had been measured
# here. It had not been. 0.08 finds 2 of Video 3's 9.)
SCENE_THRESHOLD = 0.01
MIN_GAP = 0.25          # a UI animation fires a burst; merge it into one change


def die(msg: str) -> None:
    sys.exit(f"\n  {msg}\n")


def probe_duration(f: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def detect_changes(video: Path) -> list[float]:
    """Timestamps where the screen visibly changed."""
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(video), "-filter_complex",
         f"select='gt(scene,{SCENE_THRESHOLD})',metadata=print",
         "-an", "-f", "null", "-"],
        capture_output=True, text=True)
    hits: list[float] = []
    for line in r.stderr.splitlines():
        if "pts_time:" in line:
            try:
                t = float(line.split("pts_time:")[1].split()[0])
            except (IndexError, ValueError):
                continue
            if not hits or t - hits[-1] >= MIN_GAP:
                hits.append(t)
    return hits


def shot_durations(slug: str) -> list[dict]:
    """Each shot's line and how long it runs, from the plan and the VO.

    Reuses compile_shot_plan's own phrase matcher rather than re-deriving it —
    two definitions of "where does this shot start" is exactly how a cut drifts
    out of sync with the render that will later use it.
    """
    from compile_shot_plan import load_words, find_phrase

    plan_p = ROOT / f"jobs/{slug}/shot-plan.json"
    if not plan_p.exists():
        die(f"no {plan_p.relative_to(ROOT)}")
    vo = next((p for p in (ROOT / f"public/assets/{slug}/vo.json",
                           ROOT / f"_sources/{slug}/vo.json") if p.exists()), None)
    if vo is None:
        die(f"no vo.json for {slug} — the durations come from the read")

    words = load_words(vo)
    shots = json.loads(plan_p.read_text())["shots"]
    out, cursor = [], 0
    for i, shot in enumerate(shots):
        start_i, _ = find_phrase(words, str(shot.get("start_phrase", "")),
                                 cursor, f"shot {i} start_phrase")
        start = float(words[start_i]["start"])
        if i + 1 < len(shots):
            nxt, _ = find_phrase(words, str(shots[i + 1].get("start_phrase", "")),
                                 start_i + 1, f"shot {i+1} start_phrase")
            end = float(words[nxt]["start"])
        else:
            end = float(words[-1]["end"])
        cursor = start_i
        out.append({"index": i, "line": shot.get("line", ""),
                    "asset_id": shot.get("asset_id"),
                    "dur": round(end - start, 3)})
    return out


def scan(video: Path) -> int:
    if not video.exists():
        die(f"no such file: {video}")
    total = probe_duration(video)
    hits = detect_changes(video)
    sheet_dir = ROOT / "out" / f"{video.stem}-scan"
    sheet_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== scan — {video.name} ({total:.1f}s) ===\n")
    print(f"  {len(hits)} visual changes at threshold {SCENE_THRESHOLD}\n")
    if not hits:
        print("  Nothing detected. Either the recording holds one static\n"
              "  screen, or the threshold is too high for this footage.\n")
        return 1

    tiles = []
    for n, t in enumerate(hits[:48]):
        p = sheet_dir / f"{n:02d}-{t:07.2f}.jpg"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", str(video),
             "-frames:v", "1", "-vf",
             f"scale=240:-1,drawtext=text='{n:02d}  t={t:.2f}s'"
             f":fontsize=15:fontcolor=white:box=1:boxcolor=black@0.75:x=4:y=4",
             str(p)], capture_output=True)
        if p.exists():
            tiles.append(p)
        print(f"  {n:02d}  t={t:7.2f}s")

    if tiles:
        cols = min(6, len(tiles))
        rows = -(-len(tiles) // cols)
        tiles += [tiles[-1]] * (cols * rows - len(tiles))   # tile needs a full grid
        inputs = [a for p in tiles for a in ("-i", str(p))]
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
             f"concat=n={len(tiles)}:v=1:a=0,tile={cols}x{rows}",
             "-frames:v", "1", str(sheet_dir / "scan-sheet.jpg")],
            capture_output=True)
        print(f"\n  contact sheet: {(sheet_dir / 'scan-sheet.jpg').relative_to(ROOT)}")

    print("\n  Read the sheet, then write the moments you want into\n"
          "  jobs/<slug>/clip-map.json as {\"shots\": {\"<shot index>\": <seconds>}}\n"
          "  and run --cut. A shot with no entry is skipped, never guessed.\n")
    return 0


def cut(slug: str, video: Path) -> int:
    if not video.exists():
        die(f"no such file: {video}")
    map_p = ROOT / f"jobs/{slug}/clip-map.json"
    if not map_p.exists():
        die(f"no {map_p.relative_to(ROOT)} — run --scan first and write the "
            f"moments into it")
    mapping = (json.loads(map_p.read_text()) or {}).get("shots") or {}
    if not mapping:
        die(f"{map_p.relative_to(ROOT)} has no `shots` entries")

    shots = shot_durations(slug)
    total = probe_duration(video)
    out_dir = ROOT / f"public/assets/{slug}/clips"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== cut — {slug} from {video.name} ({total:.1f}s) ===\n")
    made, problems = [], []
    for s in shots:
        key = str(s["index"])
        if key not in mapping:
            continue
        at = float(mapping[key])
        dur = s["dur"]
        # A clip SHORTER than its beat renders a freeze at the tail, and that
        # is a RENDER fault the gates block on — so refuse here rather than
        # emitting one and letting the build discover it.
        if at + dur > total + 0.05:
            problems.append(
                f"shot {key}: needs {dur:.2f}s from t={at:.2f}s but the "
                f"recording ends at {total:.2f}s — the clip would run short "
                f"and freeze on its last frame")
            continue
        name = f"beat{int(key):02d}-{video.stem}.mp4"
        dst = out_dir / name
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", f"{at}", "-i", str(video),
             "-t", f"{dur}", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "18", "-pix_fmt", "yuv420p", "-an", str(dst)],
            capture_output=True, text=True)
        if r.returncode != 0 or not dst.exists():
            problems.append(f"shot {key}: ffmpeg failed — {r.stderr[-160:]}")
            continue
        got = probe_duration(dst)
        made.append((key, name, at, dur, got))
        print(f"  shot {key:>2}  t={at:6.2f}s  {dur:5.2f}s -> {name}"
              f"  (got {got:.2f}s)  {s['line'][:34]!r}")

    if problems:
        print(f"\n  {len(problems)} problem(s):\n")
        for p in problems:
            print(f"    - {p}")
    print(f"\n  {len(made)} clip(s) written to "
          f"{out_dir.relative_to(ROOT)}\n")
    if made:
        print("  Point each shot's scene.src at its clip, declare the asset\n"
              "  `\"surface\": \"screen\"` in the manifest so it is framed as a\n"
              "  phone, then recompile.\n")
    return 1 if problems else 0


def selftest() -> int:
    import tempfile
    fails, checks = [], 0

    def ok(label: str, cond: bool, detail: str = "") -> None:
        nonlocal checks
        checks += 1
        if not cond:
            fails.append(f"{label}: {detail}")

    tmp = Path(tempfile.mkdtemp(prefix="cut-clips-selftest-"))
    src = tmp / "rec.mp4"
    # Three flat frames, one second each: two unmistakable changes.
    #
    # LUMA-distinct, and that is not cosmetic. The first version of this
    # fixture used red/green/blue and detected only ONE of its two changes:
    # ffmpeg's scene metric scores pure red -> pure green at ~0.0 because it
    # compares downscaled luma, and those two hues sit close there. So it is a
    # real limitation of the detector, worth knowing rather than papering
    # over: a UI change that alters COLOUR ONLY at constant brightness can be
    # missed. Light-mode -> dark-mode, a sheet sliding up, a keyboard
    # appearing and text arriving are all large luma events and are found.
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y",
         "-f", "lavfi", "-i", "color=c=black:s=320x568:d=1",
         "-f", "lavfi", "-i", "color=c=white:s=320x568:d=1",
         "-f", "lavfi", "-i", "color=c=gray:s=320x568:d=1",
         "-filter_complex", "concat=n=3:v=1:a=0", "-pix_fmt", "yuv420p",
         str(src)], capture_output=True)
    ok("fixture built", src.exists())
    ok("fixture is 3s", abs(probe_duration(src) - 3.0) < 0.2,
       f"{probe_duration(src):.2f}")

    hits = detect_changes(src)
    ok("detects the colour changes", len(hits) >= 2,
       f"found {len(hits)} — a screen recording's changes are subtler than "
       f"these, so failing here means the detector is broken outright")

    # THE ONE THAT MATTERS: a clip must never come out SHORTER than its beat.
    # That renders a freeze on the last frame, which is a blocking RENDER
    # fault, and the whole point of cutting from durations is to make it
    # impossible. Cut 1.25s from t=0.5 and measure what came back.
    dst = tmp / "clip.mp4"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", str(src),
         "-t", "1.25", "-c:v", "libx264", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", "-an", str(dst)], capture_output=True)
    ok("a cut clip is not short of its beat",
       probe_duration(dst) >= 1.25 - 0.04,
       f"asked 1.25s, got {probe_duration(dst):.2f}s — a short clip freezes "
       f"on its last frame and blocks the build")

    ok("scene threshold is tuned for screens, not b-roll",
       SCENE_THRESHOLD < 0.3,
       "a b-roll threshold finds almost nothing on a UI recording")
    ok("the tile grid is always filled",
       "cols * rows - len(tiles)" in Path(__file__).read_text(),
       "an unfilled tile grid makes ffmpeg exit non-zero (lint_frames, "
       "2026-09-01)")

    if fails:
        print(f"cut_clips self-test FAILED ({len(fails)} of {checks})")
        for f in fails:
            print(f"  - {f}")
        return 1
    print(f"cut_clips self-test PASSED — {checks} checks")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()
    if "--scan" in argv and len(argv) >= 2:
        return scan(Path(argv[argv.index("--scan") + 1]).expanduser())
    if "--cut" in argv and len(argv) >= 3:
        i = argv.index("--cut")
        return cut(argv[i + 1], Path(argv[i + 2]).expanduser())
    print(__doc__.split("    python3")[0].strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
