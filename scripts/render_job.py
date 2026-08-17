#!/usr/bin/env python3
"""Validate, render, loudness-master, and frame-lint a Nick-style reel."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
DEFAULT_ENGINE = Path(__file__).resolve().parent.parent  # repo root

# The master spec (RULES.md / CLAUDE.md): -14 LUFS, true peak -1.2 dBFS.
LOUDNORM_TARGET = "I=-14:TP=-1.2:LRA=7"


def run(command: list[str], cwd: Path, dry_run: bool) -> None:
    print("+", " ".join(shlex.quote(part) for part in command))
    if not dry_run:
        subprocess.run(command, cwd=cwd, check=True)


def master(raw: Path, final: Path, cwd: Path, dry_run: bool) -> None:
    """Loudness-master `raw` to `final` with a TWO-PASS loudnorm.

    WHY TWO PASSES (measured 2026-08-17, out/apple-pay-india-raw.mp4, 100.8s):

        single pass  -15.2 LUFS   1.2 LU short
        two pass     -14.2 LUFS   0.2 LU short

    `loudnorm` in one pass is adaptive and streaming: it converges toward the
    target as it goes and ends holding a residual offset it never applies. It
    is not even quiet about it — pass 1 of that same chain REPORTS the miss as
    `target_offset=1.18`, the exact amount the single pass left on the table.
    This script ran the single-pass form from the day it was written, so every
    reel shipped ~1-2 LU under target and platform normalisation left it
    quieter than everything around it in the feed.

    Two traps, both hit while verifying this:

    1. `-v error` HIDES the loudnorm JSON — `print_format=json` prints at info
       level. Pass 1 must use `-hide_banner -nostats` or it measures nothing.
    2. In an interactive zsh, the pass-2 filter string must be written
       `"${VAR}:linear=true"`; a bare `$VAR:l` is eaten as zsh's lowercase
       modifier and the filter arrives corrupted. Not a risk here — we exec
       ffmpeg directly with an argv list, no shell — but it is the reason the
       recipe looks the way it does if you copy it to a terminal.

    G31 re-measures the RESULT with ebur128 afterwards. This function is the
    fix; the gate is what keeps it fixed.
    """
    pass1 = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(raw),
             "-af", f"loudnorm={LOUDNORM_TARGET}:print_format=json",
             "-f", "null", "-"]
    print("+", " ".join(shlex.quote(part) for part in pass1))
    if dry_run:
        print("  (dry-run) pass 2 would feed the measured values back")
        return

    proc = subprocess.run(pass1, cwd=cwd, capture_output=True, text=True,
                          check=True)
    stats = _loudnorm_json(proc.stderr)
    print("  measured: " + " ".join(
        f"{k}={stats[k]}" for k in
        ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")))

    # loudnorm reports -inf on a silent or near-silent input, and feeding that
    # back as measured_* makes pass 2 fail outright. Fall back rather than
    # crash, loudly — G31 still measures the result and will block the build.
    values = {k: float(stats[k]) for k in
              ("input_i", "input_tp", "input_lra", "input_thresh",
               "target_offset")}
    if any(v != v or v in (float("inf"), float("-inf")) for v in values.values()):
        print("  WARNING: pass 1 returned a non-finite measurement "
              f"({values}) — the input may be silent. Falling back to a "
              "single pass; G31 will measure the result and block if it "
              "misses.")
        af = f"loudnorm={LOUDNORM_TARGET}"
    else:
        af = (f"loudnorm={LOUDNORM_TARGET}"
              f":measured_I={values['input_i']}"
              f":measured_TP={values['input_tp']}"
              f":measured_LRA={values['input_lra']}"
              f":measured_thresh={values['input_thresh']}"
              f":offset={values['target_offset']}"
              ":linear=true")

    # `-ar 48000` is NOT cosmetic. loudnorm runs internally at 192kHz and hands
    # the encoder whatever it likes; with nothing pinned, the aac encoder chose
    # 96kHz. Verified 2026-08-17: the raw render is 48kHz, and EVERY finished
    # master in out/ — including the shipped apple-pay-india-final.mp4 — came
    # out 96kHz. Pre-existing, not introduced by the two-pass change, and
    # pointless: the source has nothing above 24kHz, so it is double the bytes
    # carrying no audio. Pin it to the render's native rate.
    run(["ffmpeg", "-y", "-i", str(raw), "-c:v", "copy", "-af", af,
         "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(final)],
        cwd, dry_run)


def _loudnorm_json(stderr: str) -> dict:
    """The JSON object loudnorm prints at the END of its stderr output."""
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start == -1 or end < start:
        raise SystemExit(
            "loudnorm printed no JSON. `-v error` hides it — pass 1 needs "
            f"`-hide_banner -nostats`. Got:\n{stderr[-800:]}")
    return json.loads(stderr[start:end + 1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument(
        "--engine",
        type=Path,
        default=Path(os.environ.get("REEL_ENGINE", DEFAULT_ENGINE)),
    )
    args = parser.parse_args()
    engine = args.engine.expanduser().resolve()
    raw = engine / f"out/{args.slug}-raw.mp4"
    final = engine / f"out/{args.slug}-final.mp4"

    run(
        [
            sys.executable,
            str(SKILL / "scripts/register_beats.py"),
            "--engine",
            str(engine),
        ],
        engine,
        args.dry_run,
    )
    run(
        [
            sys.executable,
            str(SKILL / "scripts/validate_job.py"),
            args.slug,
            "--engine",
            str(engine),
        ],
        engine,
        args.dry_run,
    )
    run(["npx", "tsc", "--noEmit", "-p", "."], engine, args.dry_run)

    # FINAL QUALITY GATE (user rule 2026-08-12: "do not render final output
    # until all checks pass"). Until today this script ran validate + tsc and
    # went straight to render, so a sheet could fail reel_gates and still
    # produce an mp4 — the exact "rule that never fires" failure this repo
    # exists to prevent. doctor proves the toolchain is whole (Pillow, whisper,
    # gate self-test); reel_gates proves the sheet is sound. Both block.
    run([sys.executable, str(SKILL / "scripts/doctor.py")], engine, args.dry_run)
    # The user must have approved THIS script (user rule 2026-08-12). Checked
    # here as well as before generation, so an unapproved edit cannot reach an
    # mp4 by any route.
    run([sys.executable, str(SKILL / "tools/script_approval.py"), "check",
         args.slug], engine, args.dry_run)
    run([sys.executable, str(SKILL / "tools/reel_gates.py"), args.slug],
        engine, args.dry_run)

    if not args.skip_render:
        raw.parent.mkdir(parents=True, exist_ok=True)
        run(
            [
                "npx",
                "remotion",
                "render",
                "src/index.ts",
                args.slug,
                str(raw),
                "--concurrency=2",
                "--timeout=120000",
            ],
            engine,
            args.dry_run,
        )
    elif not raw.exists() and not args.dry_run:
        raise SystemExit(f"--skip-render requested but raw render is missing: {raw}")

    master(raw, final, engine, args.dry_run)

    # G31 — measure the ARTIFACT, not the filter that produced it. The chain
    # above is the fix for the single-pass undershoot; this is what stops it
    # regressing, and what catches any other way the master can miss target.
    run([sys.executable, str(SKILL / "tools/reel_gates.py"), "--master",
         str(final)], engine, args.dry_run)
    run(
        [
            sys.executable,
            "tools/lint_frames.py",
            args.slug,
            "--video",
            str(final),
        ],
        engine,
        args.dry_run,
    )
    run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_name,width,height,avg_frame_rate",
            "-of",
            "default=noprint_wrappers=1",
            str(final),
        ],
        engine,
        args.dry_run,
    )
    print(f"final: {final}")


if __name__ == "__main__":
    main()
