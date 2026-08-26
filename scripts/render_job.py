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
LOUDNORM_TARGET = "I=-14:TP=-2.0:LRA=7"
# TRUE-PEAK BACKSTOP. loudnorm in `linear=true` applies ONE fixed gain, so it
# can overshoot its own TP target on a peaky master: iphone-18-pro asked for
# TP=-1.2 and landed -0.9, over G31's -1.0 ceiling. RULES section 11 prescribes a
# limiter for exactly this. The target moved to -1.5 for headroom and the
# limiter is a hard ceiling after it, so a peak can no longer clip on a lossy
# re-encode. General fix: any reel can overshoot, not just this one.
# MEASURED AGAIN 2026-08-21 (iphone18-colors), and the previous fix was only
# half right: `alimiter`'s `limit` is a SAMPLE-peak ceiling, not a true-peak
# one, and this ffmpeg build has no oversampling option. limit=0.83 (-1.62 dBFS
# sample) still measured -0.9 dBFS TRUE peak — +0.72 dB of inter-sample
# overshoot, straight back over G31's -1.0 ceiling, which is exactly the
# symptom the note above says was fixed.
# So the ceiling now carries headroom for the overshoot rather than pretending
# it does not exist: 0.75 = -2.5 dBFS sample, landing about -1.8 dBFS true.
# ...and lowering `limit` made it WORSE, not better: 0.83 -> -0.9 dBFS true,
# 0.75 -> -0.7 dBFS true. Harder limiting sharpens transients, which RAISES
# inter-sample peaks. The ceiling was never the problem — the limiter simply
# cannot see between samples at 48k.
# So limit at 4x OVERSAMPLE, where the inter-sample peaks are real samples the
# limiter can act on, then let the output `-ar 48000` bring it back down. This
# is the standard true-peak technique and it is what G31 has been asking for
# through three attempts at moving a number.
# THE OVERSHOOT IS THE AAC ENCODER, NOT THE LIMITER. Measured 2026-08-21 by
# splitting the chain: the PCM master out of loudnorm+limiter was a clean
# -1.9 dBFS true peak; the SAME audio encoded to AAC 192k measured -0.3. The
# codec adds up to ~1.6 dB, so no amount of pre-encode limiting can hold the
# delivered file under G31's ceiling — the master has to carry headroom THROUGH
# the encode. Three prior attempts moved the loudnorm TP target instead and all
# three shipped over the ceiling.
#
# Measured post-AAC true peak vs limiter ceiling on this reel:
#   limit 0.85 -> -0.6 dBFS   (fails)      limit 0.63 -> -2.9 dBFS  (passes)
#   limit 0.72 -> -0.6 dBFS   (fails)      limit 0.56 -> -4.1 dBFS  (too quiet)
# 0.63 is the first ceiling that survives the encode. It only engages on the
# loudest transients, so quieter material is unaffected and loudnorm alone
# still lands the integrated target.
TRUE_PEAK_LIMITER = ("aresample=192000,alimiter=limit=0.63:level=disabled,"
                     "aresample=48000")


def run(command: list[str], cwd: Path, dry_run: bool) -> None:
    print("+", " ".join(shlex.quote(part) for part in command))
    if not dry_run:
        try:
            subprocess.run(command, cwd=cwd, check=True)
        except subprocess.CalledProcessError as e:
            # The step already printed its own diagnosis — validate_job says
            # exactly which manifest is missing, and that is the whole answer.
            # Re-raising buried that one useful line under fourteen lines of
            # Python internals ending in CalledProcessError, which is the first
            # thing a fresh clone sees after doctor passes: footage is excluded
            # from git by design, so the first render attempt is EXPECTED to
            # stop here. It should read as a missing file, not a crash.
            print(f"\nrender stopped — {Path(command[1]).name} exited "
                  f"{e.returncode}. Its message is above.", file=sys.stderr)
            sys.exit(e.returncode)


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
        af = f"loudnorm={LOUDNORM_TARGET},{TRUE_PEAK_LIMITER}"
    else:
        af = (f"loudnorm={LOUDNORM_TARGET}"
              f":measured_I={values['input_i']}"
              f":measured_TP={values['input_tp']}"
              f":measured_LRA={values['input_lra']}"
              f":measured_thresh={values['input_thresh']}"
              f":offset={values['target_offset']}"
              ":linear=true"
              f",{TRUE_PEAK_LIMITER}")

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
    # ITERATION LEVERS, added 2026-08-21. A draft is for the eye during
    # iteration — half scale, fast encode, no master/lint — and is NEVER a
    # deliverable: it renders to -draft.mp4 and the -final path only exists
    # through the full pipeline. The editorial law still applies to drafts
    # (approval + gates run either way); what a draft skips is delivery QC,
    # which the final re-runs from scratch anyway.
    parser.add_argument("--draft", action="store_true",
                        help="half-scale fast render for iteration; skips "
                             "master/lint/measurements, keeps gates")
    parser.add_argument("--frames", default=None, metavar="A-B",
                        help="draft only: render just this frame range — "
                             "re-checking one fixed scene costs seconds, "
                             "not a full render")
    parser.add_argument("--concurrency", type=int, default=6,
                        help="Remotion workers. 6 was MEASURED on the 8-core "
                             "machine (390s -> 165s vs 2); on a different "
                             "machine, re-measure before trusting a higher "
                             "number and record it in STYLE-RULES")
    parser.add_argument(
        "--engine",
        type=Path,
        default=Path(os.environ.get("REEL_ENGINE", DEFAULT_ENGINE)),
    )
    args = parser.parse_args()
    engine = args.engine.expanduser().resolve()
    if args.frames and not args.draft:
        raise SystemExit("--frames without --draft would produce a partial "
                         "deliverable. Partial renders are a draft tool.")
    raw = engine / f"out/{args.slug}{'-draft' if args.draft else '-raw'}.mp4"
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
    if not args.draft:      # draft keeps the LAW below; doctor + delivery
        run([sys.executable, str(SKILL / "scripts/doctor.py")],
            engine, args.dry_run)   # QC re-run in full on the final anyway
    # The user must have approved THIS script (user rule 2026-08-12). Checked
    # here as well as before generation, so an unapproved edit cannot reach an
    # mp4 by any route.
    run([sys.executable, str(SKILL / "tools/script_approval.py"), "check",
         args.slug], engine, args.dry_run)
    # FRAMEWORK CHECK, AGAIN, AT BUILD TIME (2026-08-25). It already runs at
    # propose — but propose only ever sees the SCRIPT. Every on-screen
    # surface (headlines, kinetic type, the CTA keyword card) is authored
    # LATER, at compile, so the place a reveal target most plausibly leaks is
    # the one place approval could not have audited. Same shape as G27
    # re-checking the script hash at build time, and for the same reason: the
    # artifact is what ships, not the plan.
    run([sys.executable, str(SKILL / "tools/framework_check.py"), args.slug],
        cwd=engine)
    run([sys.executable, str(SKILL / "tools/reel_gates.py"), args.slug],
        engine, args.dry_run)

    # THE CRAFT PASSES — the ones that MAKE the reel better, not just report.
    #
    # Audited 2026-08-18: calibrate_sfx.py, sync_impacts.py and pace_reel.py
    # existed and NOTHING called them. calibrate_sfx is the fix for the user's
    # "sound effects are hardly noticeable" and it ran only when somebody
    # remembered to type it; sync_impacts and pace_reel were written the same
    # day and left equally unreachable. Building the capability and not the
    # habit is the same failure as writing a check nobody runs, one layer up.
    #
    # These two WRITE to the beat sheet, and both are idempotent — a second run
    # on a calibrated sheet changes nothing. They run before the render so the
    # frame gets the benefit, and after the gates so a broken sheet is rejected
    # before anything rewrites it.
    #
    # pace_reel.py is deliberately NOT here. It re-encodes the avatar master and
    # rewrites every timing in the sheet; that is a decision with a listen-back,
    # not a step that should fire unattended in a render. It is reported in the
    # measurement block below and run by hand.
    if not args.dry_run and not args.draft:
        for tool in ("tools/calibrate_sfx.py", "tools/sync_impacts.py"):
            print(f"\n+ {tool} {args.slug} --write")
            subprocess.run([sys.executable, str(SKILL / tool), args.slug,
                            "--write"], cwd=engine, check=False)

    # THE MEASUREMENTS, run where somebody will actually see them.
    #
    # tools/auto_contrast.py, check_type.py, check_palette.py and
    # check_safe_area.py were each written to answer a defect and then left as
    # things a person runs by hand. Nobody ran them. iphone-fold-ultra shipped
    # on 2026-08-18 with the word "iPhone," in white over a white phone at 0:03
    # — a defect auto_contrast detects in two seconds and had never been asked
    # about. A check nobody runs is worse than no check, because it lets people
    # believe the question was asked.
    #
    # ADVISORY BY CONSTRUCTION: check=False, so none of them can stop a render.
    # They report; the blocking authority stays with reel_gates and BLOCKING_RULES.
    # auto_contrast runs in REPORT mode on purpose — it could write `theme` from
    # the pixels, but silently rewriting a sheet the user approved (G27) during
    # a render is not a measurement, it is an edit.
    if not args.dry_run and not args.draft:
        print("\n── measurements (advice — none of these block) " + "─" * 26)
        for tool, tool_args in [
            ("tools/check_frame_contract.py", [args.slug]),
            ("tools/pace_reel.py", [args.slug]),      # report only — see above
            ("tools/auto_contrast.py", [args.slug]),
            ("tools/check_safe_area.py", [args.slug]),
            ("tools/check_palette.py", ["--worst"]),
            ("tools/check_type.py", ["--worst"]),
        ]:
            print(f"\n+ {tool} {' '.join(tool_args)}")
            subprocess.run([sys.executable, str(SKILL / tool), *tool_args],
                           cwd=engine, check=False)
        print("─" * 70 + "\n")

    # PREFLIGHT ON STILLS — catch on 5 frames what used to cost 2283.
    #
    # Measured 2026-08-19: one still is 3.3s, one full render + master + lint is
    # ~8 minutes. iphone-fold-ultra was rendered SEVEN times in one session and
    # every re-render was triggered by something visible in a single frame — a
    # caption printed through the credit, white captions on white footage, a
    # receipt sliced mid-word, two identical scenes, empty typecards.
    #
    # They were found late for one structural reason: lint_frames.py extracted
    # its frames FROM THE FINISHED VIDEO, so nothing could be checked until
    # everything had been rendered. Rendering the same frames straight from
    # Remotion removes that dependency.
    #
    # ADVISORY, deliberately. It samples one frame per scene type, so it cannot
    # see a defect that only exists in one scene of a type, and a hard failure
    # here would block a render over an incomplete sample. It prints; the
    # post-render lint still decides.
    if not args.dry_run and not args.skip_render and not args.draft:
        print("\n── preflight stills (advice — the post-render lint still decides) ──")
        subprocess.run([sys.executable, str(SKILL / "tools/preflight_stills.py"),
                        args.slug, "--types"], cwd=engine, check=False)
        subprocess.run([sys.executable, str(SKILL / "tools/lint_frames.py"),
                        args.slug, "--from-stills", "--soft"],
                       cwd=engine, check=False)
        print("── end preflight ──\n")

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
                # CONCURRENCY 6, NOT 2 — measured 2026-08-19 on this machine
                # (8 cores / 16 GB):
                #
                #     300 frames @ 2 -> 51.0s      full reel @ 2 -> ~390s
                #     300 frames @ 6 -> 29.9s      full reel @ 6 ->  165s
                #
                # 2283 frames, 1080x1920, zero errors, byte-comparable output.
                #
                # The 2 was not arbitrary: AGENT.md records "the default hits
                # delayRender timed out". That was the Fraunces loadFont() at
                # module scope in a Root-imported file — fixed on 2026-08-16 by
                # moving to @font-face, which carries no delayRender at all. The
                # workaround outlived its cause, exactly like flo() and the
                # receipt zoom floor. Re-measure if a component ever calls
                # loadFont() again; that is the condition this depends on.
                f"--concurrency={args.concurrency}",
                "--timeout=120000",
            ]
            + (["--scale=0.5", "--crf=28"] if args.draft else [])
            + ([f"--frames={args.frames}"] if args.frames else []),
            engine,
            args.dry_run,
        )
    elif not raw.exists() and not args.dry_run:
        raise SystemExit(f"--skip-render requested but raw render is missing: {raw}")

    if args.draft:
        print(f"draft: {raw}")
        print("A draft is for the eye — half scale, fast encode, no master, "
              "no lint.\nIt is NEVER a deliverable. Full pipeline: "
              f"python3 scripts/render_job.py {args.slug}")
        return

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
