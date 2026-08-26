#!/usr/bin/env python3
"""Turn a downloaded HeyGen master into the three things the build needs.

WHY THIS EXISTS
---------------
Every reel needs the same four steps after the avatar renders — conform the
frame rate, extract a 16k mono wav, whisper it with word timestamps, measure
the face — and until now all four were prose in PIPELINE.md §4 and AGENT.md
STEP 2, run by hand each time. Prose steps get skipped or done slightly
differently, which is the failure mode this whole repo is built around.

Two of them have a trap that is invisible if you skip them:

1. **25fps.** The twin renders come back 25fps while the project is 30fps
   (config.json avatarRegistry.renderFps, measured 2026-08-13). Remotion
   plays a 25fps source in a 30fps composition by repeating frames, so the
   facecam micro-stutters and nothing in the logs says so. Conform on ingest.

2. **Whisper is the master clock, not the script.** Scene cuts anchor to
   whisper's word onsets, so vo.json must come from the ACTUAL audio. A word
   whisper heard differently is a caption problem (fix it in
   caption_corrections, display text only) — never a reason to edit timings.

    python3 tools/ingest_avatar.py <slug> [--src downloaded.mp4] [--model base]

Writes, under public/assets/<slug>/:
    avatar-master.mp4   conformed to the project fps
    vo.json             [{start,end,word}, ...] from whisper
    face-x.txt          face-centre fraction, measured on a mid frame
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT_FPS = 30


def die(msg: str) -> None:
    sys.exit(f"  ERROR  {msg}")


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        die(f"{cmd[0]} failed: {(p.stderr or p.stdout)[-400:]}")
    return p.stdout


def probe(path: Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=r_frame_rate,width,height",
               "-show_entries", "format=duration",
               "-of", "json", str(path)])
    j = json.loads(out)
    st = j["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    return {"fps": float(num) / float(den), "w": st["width"],
            "h": st["height"], "dur": float(j["format"]["duration"])}


def conform(src: Path, dst: Path, fps: float) -> None:
    """Re-time to the project fps. Only touched when it actually differs —
    a needless re-encode costs quality for nothing."""
    if abs(fps - PROJECT_FPS) < 0.01:
        if src.resolve() != dst.resolve():
            shutil.copy(src, dst)
        print(f"  fps {fps:g} already matches the project — copied, not re-encoded")
        return
    print(f"  conforming {fps:g}fps -> {PROJECT_FPS}fps")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
         "-r", str(PROJECT_FPS), "-c:v", "libx264", "-preset", "medium",
         "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         str(dst)])


def word_timings(master: Path, out: Path, model: str) -> int:
    wav = master.with_name("vo16.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(master),
         "-ac", "1", "-ar", "16000", "-vn", str(wav)])
    if not shutil.which("whisper"):
        die("whisper not on PATH — run setup.sh")
    tmp = master.parent / "_whisper"
    tmp.mkdir(exist_ok=True)
    run(["whisper", str(wav), "--model", model, "--language", "en",
         "--word_timestamps", "True", "--output_format", "json",
         "--output_dir", str(tmp), "--verbose", "False"])
    j = json.loads((tmp / (wav.stem + ".json")).read_text())
    words = [{"start": w["start"], "end": w["end"], "word": w["word"].strip()}
             for seg in j["segments"] for w in seg.get("words", [])]
    if not words:
        die("whisper returned no word timings")
    out.write_text(json.dumps({"words": words}, indent=1))
    shutil.rmtree(tmp, ignore_errors=True)
    wav.unlink(missing_ok=True)
    return len(words)


def face_x(master: Path, dur: float) -> float:
    """Face-centre as a fraction of frame width, from a mid-reel frame.

    Deliberately crude and deliberately MEASURED: the fraction only has to be
    good enough to drive objectPosition. A native 9:16 render is already
    centre-framed, so this mostly confirms that rather than correcting it —
    but confirming is the point, because the one time it is wrong is the time
    nobody checked.
    """
    frame = master.with_name("_facecheck.png")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur / 2:.2f}",
         "-i", str(master), "-frames:v", "1", str(frame)])
    try:
        import numpy as np
        from PIL import Image
        a = np.asarray(Image.open(frame).convert("RGB")).astype(int)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        # coarse skin mask; upper 60% of frame only, so hands/desk do not vote
        skin = ((r > 95) & (g > 40) & (b > 20) & (r > g) & (r > b)
                & ((r - np.minimum(g, b)) > 15))
        skin[int(skin.shape[0] * 0.6):, :] = False
        cols = skin.sum(axis=0)
        if cols.sum() < 500:
            return 0.5
        xs = np.arange(cols.size)
        return float((xs * cols).sum() / cols.sum() / cols.size)
    finally:
        frame.unlink(missing_ok=True)


def selftest() -> None:
    """Pin the one behaviour this tool exists for: a non-project fps IS
    conformed. Everything else here is a documented ffmpeg/whisper call whose
    result is printed; this is the step that fails SILENTLY (Remotion repeats
    frames rather than erroring), so it is the step that gets a test."""
    import tempfile
    fails = 0

    def ok(name: str, cond: bool) -> None:
        nonlocal fails
        print(f"  {'ok  ' if cond else 'FAIL'}   {name}")
        if not cond:
            fails += 1

    with tempfile.TemporaryDirectory(prefix="ingest-selftest-") as d:
        tmp = Path(d)
        src = tmp / "src25.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
             "-i", "testsrc=size=180x320:rate=25:duration=2",
             "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono", "-shortest",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25", str(src)])
        ok("fixture really is 25fps", abs(probe(src)["fps"] - 25) < 0.01)

        dst = tmp / "out.mp4"
        conform(src, dst, probe(src)["fps"])
        ok("a 25fps master is conformed to the project fps",
           abs(probe(dst)["fps"] - PROJECT_FPS) < 0.01)
        ok("conforming preserves duration",
           abs(probe(dst)["dur"] - probe(src)["dur"]) < 0.25)

        # and the negative: an already-correct master must NOT be re-encoded
        same = tmp / "same.mp4"
        conform(dst, same, PROJECT_FPS)
        ok("a master already at the project fps is copied, not re-encoded",
           same.read_bytes() == dst.read_bytes())

    print(f"\n  {'ingest selftest PASSED' if not fails else f'{fails} FAILED'}")
    sys.exit(1 if fails else 0)


def main() -> None:
    if "--selftest" in sys.argv:
        selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--src", help="downloaded master; default <assets>/avatar-raw.mp4")
    ap.add_argument("--model", default="base", help="whisper model (base|small)")
    a = ap.parse_args()

    assets = ROOT / "public" / "assets" / a.slug
    if not assets.is_dir():
        die(f"no asset dir at {assets}")
    src = Path(a.src) if a.src else assets / "avatar-raw.mp4"
    if not src.exists():
        die(f"no master at {src}")

    info = probe(src)
    print(f"=== ingest {a.slug} ===")
    print(f"  source {info['w']}x{info['h']} @ {info['fps']:g}fps, {info['dur']:.2f}s")
    if (info["w"], info["h"]) != (1080, 1920):
        print(f"  NOTE non-native size {info['w']}x{info['h']} — expected 1080x1920 "
              f"for a 9:16 twin render; check the generation call before building")

    master = assets / "avatar-master.mp4"
    conform(src, master, info["fps"])
    out = probe(master)
    print(f"  master {out['w']}x{out['h']} @ {out['fps']:g}fps, {out['dur']:.2f}s")

    n = word_timings(master, assets / "vo.json", a.model)
    print(f"  vo.json {n} words (whisper {a.model})")

    fx = face_x(master, out["dur"])
    (assets / "face-x.txt").write_text(f"{fx:.3f}\n")
    print(f"  face-x {fx:.3f}"
          + ("" if 0.4 <= fx <= 0.6 else "   <-- OFF CENTRE, look at a frame"))
    print("\nNEXT: python3 scripts/compile_shot_plan.py " + a.slug)


if __name__ == "__main__":
    main()
