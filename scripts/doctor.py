#!/usr/bin/env python3
"""Preflight the toolchain. Run this before starting a reel.

WHY: on 2026-08-11 the frame linter's pixel checks were disabled for weeks
because Pillow was missing, behind a single "[SKIP] PIL not installed" line
nobody read. A dependency that silently downgrades a safety check is worse
than one that crashes. This fails loudly instead.

    python3 scripts/doctor.py          # exits 1 if anything is broken
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from reel_gates import RUNTIME_MIN, RUNTIME_MAX  # noqa: E402  single source of truth
OK, BAD, WARN = "  ok  ", " FAIL ", " warn "
problems: list[str] = []
warnings: list[str] = []


def report(state: str, name: str, detail: str = "") -> None:
    print(f"[{state}] {name}{'  — ' + detail if detail else ''}")


def need_bin(name: str, fix: str) -> None:
    path = shutil.which(name)
    if path:
        report(OK, name, path)
    else:
        report(BAD, name, f"not on PATH — {fix}")
        problems.append(name)


def need_module(mod: str, fix: str, why: str) -> None:
    try:
        __import__(mod)
        report(OK, f"python:{mod}")
    except ImportError:
        report(BAD, f"python:{mod}", f"{why} — {fix}")
        problems.append(mod)


def want_module(mod: str, fix: str, why: str) -> None:
    """Optional capability: WARN, never FAIL.

    For tooling the repo ships an integration for but does not require on the
    critical path. Manim sat in exactly this state until 2026-08-16 —
    tools/manim_scene.py + manim_theme.py + MANIM.md were all present and the
    library was not installed, so a whole themed capability was dark while
    doctor still printed "toolchain complete". A missing optional tool must be
    visible; it must not stop a build that never needed it.
    """
    try:
        __import__(mod)
        report(OK, f"python:{mod}")
    except ImportError:
        report(WARN, f"python:{mod}", f"missing — {why} — {fix}")
        warnings.append(mod)


def want_venv(mod: str, venv: Path, fix: str, why: str) -> None:
    """Optional capability that MUST stay in its own venv. WARN, never FAIL."""
    py = venv / "bin/python"
    if not py.exists():
        report(WARN, f"venv:{mod}", f"missing — {why} — {fix}")
        warnings.append(mod)
        return
    r = subprocess.run([str(py), "-c", f"import {mod}"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        report(OK, f"venv:{mod}", str(venv).replace(str(Path.home()), "~"))
    else:
        report(WARN, f"venv:{mod}", f"venv exists but import fails — {fix}")
        warnings.append(mod)
    # The whole point of the venv: system python must NOT carry it.
    leak = subprocess.run([sys.executable, "-c", f"import {mod}"],
                          capture_output=True, text=True)
    if leak.returncode == 0:
        report(WARN, f"venv:{mod} leak",
               "also installed in SYSTEM python — it downgrades torch under "
               f"whisper. Remove with: pip3 uninstall {mod}")
        warnings.append(f"{mod}-leak")


def want_filter(name: str, why: str) -> None:
    """An ffmpeg filter the repo may reach for. WARN, never FAIL.

    Homebrew's default `ffmpeg` formula omits libfreetype/libass, so drawtext,
    subtitles and ass are absent from it. `brew install ffmpeg-full` supplies
    them. Recorded because the absence is silent: ffmpeg runs fine and the
    filter simply does not exist.
    """
    ff = shutil.which("ffmpeg")
    if not ff:
        return
    try:
        out = subprocess.run([ff, "-hide_banner", "-filters"],
                             capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return
    if any(line.split()[1:2] == [name] for line in out.splitlines() if line.strip()):
        report(OK, f"ffmpeg:{name}")
    else:
        report(WARN, f"ffmpeg:{name}",
               f"filter absent — {why} — brew install ffmpeg-full")
        warnings.append(f"ffmpeg:{name}")


print("=== ai-reel-engine doctor ===\n-- binaries --")
# PATH is the only thing that counts: every call in this repo is a bare
# "ffmpeg". A copy sitting in bin/ is bytes, not an install — say so here, since
# the setup guide tells people to carry bin/ across and they will land on this
# line when it does not work.
_FF_FIX = ("`brew install ffmpeg`, or if you copied bin/ across, link it onto "
           "PATH: ln -s <repo>/bin/ffmpeg /usr/local/bin/ffmpeg")
need_bin("ffmpeg", _FF_FIX)
need_bin("ffprobe", _FF_FIX)
need_bin("node", "install Node >= 18")
need_bin("yt-dlp", "pip3 install yt-dlp && symlink it onto PATH "
                   "(the console script lands in ~/Library/Python/*/bin)")
need_bin("whisper", "pip3 install openai-whisper")

print("\n-- python modules --")
need_module("PIL", "pip3 install pillow",
            "frame-lint pixel checks SILENTLY SKIP without it")
need_module("whisper", "pip3 install openai-whisper", "word timings")

print("\n-- optional capabilities (warn only) --")
want_module("manim", "pip3 install manim (needs: brew install cairo pango pkg-config)",
            "tools/manim_scene.py + manim_theme.py render mechanism diagram clips")
# chatterbox lives in its OWN venv on purpose: installing it into system
# python downgraded torch 2.13 -> 2.6 under whisper, which is on the critical
# path (captions, tighten_vo, gates). Never pip-install it system-wide again.
want_venv("chatterbox", Path.home() / ".venvs/chatterbox",
          "python3 -m venv ~/.venvs/chatterbox && "
          "~/.venvs/chatterbox/bin/pip install chatterbox-tts",
          "local TTS for rehearsing script timing without spending HeyGen credits")

# 2026-08-17: the venv EXISTING is not the same as chatterbox WORKING. On this
# machine the directory was present and every import succeeded, yet generation
# died with `'NoneType' object is not callable` — because perth's package init
# does `from pkg_resources import resource_filename`, setuptools 81+ removed
# pkg_resources, so the submodule import failed SILENTLY and left
# `perth.PerthImplicitWatermarker = None`. Same class as the missing Pillow and
# the .zshrc PATH: the thing is installed, the check just never looked at it.
_cb = Path.home() / ".venvs/chatterbox/bin/python"
if _cb.exists():
    probe = ("import perth; "
             "assert perth.PerthImplicitWatermarker is not None, "
             "'perth watermarker is None — pip install \"setuptools<81\" in the venv'")
    r = subprocess.run([str(_cb), "-c", probe], capture_output=True, text=True,
                       timeout=90)
    if r.returncode == 0:
        report(OK, "chatterbox:usable", "perth watermarker loads")
    else:
        detail = (r.stderr.strip().splitlines() or ["unknown"])[-1]
        report(WARN, "chatterbox:usable",
               f"venv exists but generation would FAIL — {detail[:120]}")
        warnings.append("chatterbox-broken")
want_filter("drawtext", "burn-in text via ffmpeg; lint_frames.py falls back to PIL")
want_filter("subtitles", "burn-in .srt via ffmpeg (captions normally come from Remotion)")

print("\n-- whisper models (cached) --")
cache = Path.home() / ".cache/whisper"
for m in ("base", "small"):
    f = cache / f"{m}.pt"
    if f.exists():
        report(OK, f"whisper:{m}", f"{f.stat().st_size // 1_000_000} MB")
    elif m == "base":
        report(BAD, f"whisper:{m}", "missing — required for word timings")
        problems.append(f"whisper:{m}")
    else:
        report(WARN, f"whisper:{m}",
               "missing — needed to double-check suspected mispronunciations")
        warnings.append(f"whisper:{m}")
if problems and any(p.startswith("whisper:") for p in problems):
    print("      NOTE: this machine's TLS breaks whisper's own downloader.")
    print("      Fetch with curl into ~/.cache/whisper/ — the URL path segment")
    print("      is the expected SHA-256, so verify with `shasum -a 256`.")

print("\n-- node --")
if (ROOT / "node_modules/remotion").exists():
    report(OK, "node_modules", "remotion present")
else:
    report(BAD, "node_modules", "run `npm install`")
    problems.append("node_modules")
pw = Path.home() / "Library/Caches/ms-playwright"
if pw.exists() and any(pw.glob("chromium*")):
    report(OK, "playwright chromium")
else:
    report(WARN, "playwright chromium",
           "run `npx playwright install chromium` (needed by tools/capture.mjs)")
    warnings.append("playwright")

print("\n-- config --")
cfg_path = ROOT / "config.json"
if not cfg_path.exists():
    report(BAD, "config.json", "missing — copy config.example.json")
    problems.append("config.json")
else:
    cfg = json.loads(cfg_path.read_text())
    av, de = cfg.get("avatar", {}), cfg.get("defaults", {})
    checks = [
        # 1.12 locked 2026-08-25 (user: 1.05 read "slow and flat"; probed
        # fd83905a before the regen). Supersedes the 2026-08-11 1.05 lock.
        ("avatar.voiceSpeed", av.get("voiceSpeed"), 1.12),
        ("defaults.captionStyle", de.get("captionStyle"), "word-reveal"),
    ]
    for name, got, want in checks:
        if got == want:
            report(OK, name, str(got))
        else:
            report(BAD, name, f"is {got!r}, locked value is {want!r} (RULES.md §1)")
            problems.append(name)
    # engine is per-look now: it must MATCH the registry entry for the
    # selected avatar, not a hardcoded value (RULES.md, 2026-08-12)
    reg = cfg.get("avatarRegistry", {})
    aid = av.get("avatarId")
    entry = reg.get(aid)
    if not entry:
        report(BAD, "avatar.avatarId", f"{aid} is not in avatarRegistry — "
               "measure it first: tools/measure_avatar.py score <clip> --register <id>")
        problems.append("avatar unmeasured")
    elif entry.get("motion", 0) < 1.0:
        report(BAD, "avatar motion", f"{entry['name']} scores {entry['motion']} "
               "— frozen presenter, do not ship")
        problems.append("frozen avatar")
    elif av.get("engine") != entry.get("engine"):
        report(BAD, "avatar.engine", f"config says {av.get('engine')!r} but "
               f"{entry['name']} was measured on {entry.get('engine')!r}")
        problems.append("engine mismatch")
    else:
        report(OK, "avatar", f"{entry['name']} · motion {entry['motion']} · "
               f"{entry['engine']}")

    lo, hi = (de.get("lengthRangeSeconds") or [None, None])[:2]
    if [lo, hi] == [RUNTIME_MIN, RUNTIME_MAX]:
        report(OK, "defaults.lengthRangeSeconds", f"{RUNTIME_MIN:.0f}-{RUNTIME_MAX:.0f}s")
    else:
        report(BAD, "defaults.lengthRangeSeconds",
               f"is {[lo, hi]}, want {[RUNTIME_MIN, RUNTIME_MAX]} — config and reel_gates must agree")
        problems.append("lengthRange")
    if not av.get("avatarId") or not av.get("voiceId"):
        report(BAD, "avatar ids", "avatarId/voiceId not set")
        problems.append("avatar ids")
    else:
        report(OK, "avatar ids", "set")

print("\n-- sfx library --")
try:
    r = subprocess.run([sys.executable, str(ROOT / "tools/sfx_library.py"),
                        "--check"], capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        report(OK, "sfx catalogue", r.stdout.strip())
    else:
        report(BAD, "sfx catalogue", r.stdout.strip() or r.stderr.strip())
        problems.append("sfx")
except Exception as e:  # noqa: BLE001
    report(BAD, "sfx catalogue", str(e))
    problems.append("sfx")

print("\n-- platform safe area --")
# Credit.tsx used to CLAIM lint_frames.py enforced this. It did not, and two
# components carried their own credit at y 0.95 for weeks as a result. Now the
# check is real, and it runs here so nobody has to remember it.
for args, label in (
    (["--selftest"], "credit check can fail"),
    ([], "credits + safe floor"),
):
    try:
        r = subprocess.run([sys.executable, str(ROOT / "tools/check_credits.py"),
                            *args], capture_output=True, text=True, timeout=60)
        last = (r.stdout.strip().splitlines() or [""])[-1].strip()
        if r.returncode == 0:
            report(OK, label, last)
        else:
            report(BAD, label, last or r.stderr.strip()[:160])
            problems.append("safe-area")
    except Exception as e:  # noqa: BLE001
        report(BAD, label, str(e))
        problems.append("safe-area")

print("\n-- gates --")
try:
    r = subprocess.run([sys.executable, str(ROOT / "tools/test_gates.py")],
                       capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        report(OK, "reel_gates self-test", r.stdout.strip().splitlines()[-1])
    else:
        report(BAD, "reel_gates self-test", "a gate does not fire — see output")
        print(r.stdout[-800:])
        problems.append("gates")
except Exception as e:  # noqa: BLE001
    report(BAD, "reel_gates self-test", str(e))
    problems.append("gates")

# The script pipeline's own mechanical rules — structure-before-draft, the
# propose/approve review chain, and check_script's calibrated thresholds.
# Added 2026-08-21: these rules exist because prose guidance was skipped three
# times; a self-test that doctor never runs would be the same failure again.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/test_script_pipeline.py")],
        capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        report(OK, "script pipeline self-test",
               r.stdout.strip().splitlines()[-1])
    else:
        report(BAD, "script pipeline self-test",
               "a rule does not refuse — see output")
        print(r.stdout[-800:])
        problems.append("script-pipeline")
except Exception as e:  # noqa: BLE001
    report(BAD, "script pipeline self-test", str(e))
    problems.append("script-pipeline")

# Calibration staleness (2026-08-21) — AI_TELLS and the prose thresholds are
# frozen snapshots of the approved-script corpus. WARN, never FAIL: a grown
# corpus is progress, not breakage — but a checker flagging the user's own
# approved voice must not stay silent about it.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/check_script.py"),
         "--calibration"], capture_output=True, text=True, timeout=60)
    detail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    if r.returncode == 0:
        report(OK, "script calibration", detail)
    elif r.returncode == 2:
        report(WARN, "script calibration", detail
               + " — python3 tools/check_script.py --recalibrate")
    else:
        report(BAD, "script calibration", detail or "calibration check broke")
        problems.append("calibration")
except Exception as e:  # noqa: BLE001
    report(BAD, "script calibration", str(e))
    problems.append("calibration")

# WIRING (2026-08-26). A tool nobody calls and nobody is told to call is
# indistinguishable from one that was never written — except that it lets
# everyone believe the work is being done. That is how the humanizer pass
# stayed invisible for weeks. Every tool must be executed by the pipeline,
# named in a document, or explicitly legacy.
try:
    r = subprocess.run([sys.executable, str(ROOT / "tools/wiring_audit.py")],
                       capture_output=True, text=True, timeout=90)
    line = [l for l in r.stdout.splitlines() if "AUTO" in l]
    if r.returncode == 0:
        report(OK, "tool wiring", line[0].strip() if line else "no orphans")
    else:
        report(BAD, "tool wiring", "a tool is wired to nothing")
        print(r.stdout[-500:])
        problems.append("wiring")
except Exception as e:  # noqa: BLE001
    report(BAD, "tool wiring", str(e))
    problems.append("wiring")

# THE MASTER RULE AUDIT (2026-08-26). Every clause of the framework's §12
# mapped to the thing that makes it true, each probe run. Here because the
# question "is it really implemented?" was asked four times and answered from
# memory — once wrongly. A memory is not a check.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/framework_audit.py"), "--brief"],
        capture_output=True, text=True, timeout=90)
    tail = [l for l in r.stdout.splitlines() if "clauses:" in l]
    if r.returncode == 0:
        report(OK, "master rule audit", tail[-1].strip() if tail else "all clauses hold")
    else:
        report(BAD, "master rule audit", "a clause stopped being enforced")
        print(r.stdout[-600:])
        problems.append("framework-audit")
except Exception as e:  # noqa: BLE001
    report(BAD, "master rule audit", str(e))
    problems.append("framework-audit")

# The FRAMEWORK CHECK (2026-08-25) — the three rules of the short-form master
# framework that have a right answer: reveal-target concealment, certainty
# matching evidence, and source policy. Each one is a promise to the viewer.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/framework_check.py"), "--selftest"],
        capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        report(OK, "framework self-test", "reveal / certainty / source policy")
    else:
        report(BAD, "framework self-test", "a framework rule stopped firing")
        print(r.stdout[-700:])
        problems.append("framework")
except Exception as e:  # noqa: BLE001
    report(BAD, "framework self-test", str(e))
    problems.append("framework")

# The CAPTURE CONTRACT (2026-08-25). capture.mjs's defaults ARE rules —
# mobile-first (R2), live cursor (the ai-tools evidence grammar), real
# viewport, device-scale frames. Two of them had silently broken and shipped
# a whole scout session before anyone looked at a file's real dimensions.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/test_capture_defaults.py")],
        capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        report(OK, "capture defaults", r.stdout.strip().splitlines()[-1])
    else:
        report(BAD, "capture defaults", "a capture default changed")
        print(r.stdout[-700:])
        problems.append("capture")
except Exception as e:  # noqa: BLE001
    report(BAD, "capture defaults", str(e))
    problems.append("capture")

# Two self-tests that existed and were never run by anything (found
# 2026-08-26 by listing every --selftest in the repo and diffing against what
# doctor calls). check_frame_contract guards the safe-area/legibility contract;
# notation guards how numbers and units are written on screen. A self-test
# nobody runs is the same as no self-test, which is this repo's oldest bug.
for _tool, _label in (("check_frame_contract", "frame contract"),
                      ("notation", "on-screen notation"),
                      # 2026-08-27: added the same hour vo_external was
                      # written, because wiring_audit failed doctor for an
                      # unrun --selftest — the rule catching its own author.
                      ("vo_external", "external VO prep"),
                      ("vo_tagged", "tagged VO script"),
                      ("idea_scout", "idea scout")):
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / f"tools/{_tool}.py"), "--selftest"],
            capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            report(OK, _label, r.stdout.strip().splitlines()[-1].strip())
        else:
            report(BAD, _label, f"{_tool} self-test failed")
            print(r.stdout[-600:])
            problems.append(_label)
    except Exception as e:  # noqa: BLE001
        report(BAD, _label, str(e))
        problems.append(_label)

# The VO ALARM (2026-08-27). Its floor was lowered from the creator band to a
# corpus-derived one after the user deliberately chose a voice that reads flat
# by that band. Legitimate — and identical in shape to the illegitimate move of
# lowering a bar until the light goes green. So the suite asserts BOTH that a
# typical read stays quiet AND that a genuinely flat one still alarms.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/test_vo_qc.py")],
        capture_output=True, text=True, timeout=180)
    if r.returncode == 0:
        report(OK, "vo alarm", r.stdout.strip().splitlines()[-1])
    else:
        report(BAD, "vo alarm", "the calibrated VO alarm stopped working")
        print(r.stdout[-700:])
        problems.append("vo alarm")
except Exception as e:  # noqa: BLE001
    report(BAD, "vo alarm", str(e))
    problems.append("vo alarm")

# Has the VO corpus moved since we calibrated? Same reasoning as the script
# calibration: a threshold derived from three reads should be re-derived once
# more reads exist, or it silently stops describing what we ship.
try:
    import json as _json
    _cal = ROOT / "voice_calibration.json"
    if _cal.exists():
        _c = _json.loads(_cal.read_text())
        sys.path.insert(0, str(ROOT / "tools"))
        import vo_qc as _vq
        _now = len(_vq.corpus_wavs())
        if _now != _c.get("n"):
            report(WARN, "vo calibration",
                   f"corpus moved since calibration ({_c.get('n')} -> {_now} "
                   "reads). Run: vo_qc.py --recalibrate")
            warnings.append("vo calibration")
        elif _c.get("n", 0) < 5:
            report(WARN, "vo calibration",
                   f"PROVISIONAL — derived from only {_c['n']} read(s). "
                   "Recalibrate as more reels ship.")
            warnings.append("vo calibration")
        else:
            report(OK, "vo calibration", f"n={_c['n']}, alarm {_c['floor']}")
except Exception as e:  # noqa: BLE001
    report(WARN, "vo calibration", str(e))

# The HOOKS (2026-08-26). Hooks are the ONLY mechanism that can make a skill
# run without a human remembering to — everything else in this repo can print
# a reminder at best. A hook that quietly stops firing therefore removes a
# trigger while looking exactly like nothing being wrong, which is the same
# failure shape as the humanizer that was documented for weeks and never ran.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/test_hooks.py")],
        capture_output=True, text=True, timeout=180)
    if r.returncode == 0:
        report(OK, "claude hooks", r.stdout.strip().splitlines()[-1])
    else:
        report(BAD, "claude hooks", "a hook stopped firing")
        print(r.stdout[-900:])
        problems.append("hooks")
except Exception as e:  # noqa: BLE001
    report(BAD, "claude hooks", str(e))
    problems.append("hooks")

# The retention join (2026-08-21) — the tool that turns a published reel's
# curve into per-scene-type numbers. Its math is exactly the kind of thing
# that rots silently: a broken join would keep printing plausible tables.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/retention_ingest.py"),
         "--selftest"], capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        report(OK, "retention join self-test",
               r.stdout.strip().splitlines()[-1])
    else:
        report(BAD, "retention join self-test", "join math broke — see output")
        print(r.stdout[-600:])
        problems.append("retention")
except Exception as e:  # noqa: BLE001
    report(BAD, "retention join self-test", str(e))
    problems.append("retention")

# Scout contact sheets (2026-08-21) — also the live probe of the drawtext
# capability ffmpeg-full was installed for: a plain ffmpeg build would pass
# every PATH check above and still produce unlabeled sheets.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/scout_sheet.py"), "--selftest"],
        capture_output=True, text=True, timeout=90)
    if r.returncode == 0:
        report(OK, "scout sheet self-test", r.stdout.strip().splitlines()[-1])
    elif r.returncode == 2:
        report(WARN, "scout sheet self-test",
               "sheets work but UNLABELED — brew install ffmpeg-full")
    else:
        report(BAD, "scout sheet self-test", "sheeting broke — see output")
        print(r.stdout[-600:])
        problems.append("scout-sheet")
except Exception as e:  # noqa: BLE001
    report(BAD, "scout sheet self-test", str(e))
    problems.append("scout-sheet")

# Avatar ingest (2026-08-26) — the 25fps trap. Twin renders come back 25fps
# while the project is 30fps, and Remotion resolves the mismatch by REPEATING
# FRAMES rather than erroring, so a skipped conform ships a micro-stuttering
# facecam and nothing in any log says so. The self-test proves the conform
# still fires, and that an already-correct master is left alone.
try:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools/ingest_avatar.py"), "--selftest"],
        capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        report(OK, "avatar ingest self-test", r.stdout.strip().splitlines()[-1])
    else:
        report(BAD, "avatar ingest self-test", "fps conform broke — see output")
        print(r.stdout[-600:])
        problems.append("avatar-ingest")
except Exception as e:  # noqa: BLE001
    report(BAD, "avatar ingest self-test", str(e))
    problems.append("avatar-ingest")

# ------------------------------------------------------------- fresh clone
#
# `git clone` does NOT give a working engine, and the gap is invisible until a
# render fails. .gitignore deliberately excludes node_modules/, bin/,
# public/assets/ and _sources/ — the first two are needed to render at all, the
# last two are per-reel material that should never sit in a shared repo.
#
# This checks exactly what a clone is missing, and nothing else. Run it as the
# first thing on a new machine:
#
#     python3 scripts/doctor.py --fresh-clone
#
# Without the flag these same checks still run, because a half-set-up machine
# is a half-set-up machine whether or not you remembered the flag.
FRESH = "--fresh-clone" in sys.argv
print("\n-- what git does not carry --")

# node_modules is already checked under "-- node --", and checked HARDER there:
# it looks for node_modules/remotion, so a half-finished npm install fails it.
# Report it again here because this section is what a new machine reads top to
# bottom, but do not append a second time — a problem counted twice makes the
# summary line say "7 problems" about four, which is how the ffmpeg
# contradiction below stayed hidden in the noise.
if (ROOT / "node_modules/remotion").is_dir():
    report(OK, "node_modules", "present")
else:
    report(BAD, "node_modules", "run: npm install")
    if "node_modules" not in problems:
        problems.append("node_modules")

# ffmpeg/ffprobe are checked once, by need_bin, against PATH — see "-- binaries
# --" above. This section used to check them a SECOND time and accept a copy in
# bin/ as equally good ("either is fine"). That was false, and the two checks
# contradicted each other in exactly the case the setup guide recommends.
#
# Every invocation in this repo is a bare "ffmpeg" / "ffprobe" through
# subprocess.run — about twenty of them, across reel_gates, pace_reel,
# lint_frames, capture.mjs and the rest — so the binary is resolved through
# PATH, always. Nothing reads bin/, and nothing puts bin/ on PATH. A machine
# with bin/ffmpeg and no ffmpeg on PATH therefore fails at the first ffmpeg call
# while this check called it OK, and the remediation text told you to copy bin/
# across, which produces exactly that machine.
#
# So: bin/ is a transport for the bytes, not an install. Copying it is fine —
# but the copy has to be linked onto PATH before anything can use it, the same
# way yt-dlp is handled above.
bundled = [t for t in ("ffmpeg", "ffprobe") if (ROOT / "bin" / t).exists()]
if bundled and not all(shutil.which(t) for t in ("ffmpeg", "ffprobe")):
    report(WARN, "bin/ not on PATH",
           f"bin/ holds {', '.join(bundled)} but nothing resolves through bin/ — "
           f"every call in this repo is a bare `ffmpeg`. Link it: "
           f"ln -s \"{ROOT}/bin/ffmpeg\" /usr/local/bin/ffmpeg (same for ffprobe), "
           f"or `brew install ffmpeg`.")
    warnings.append("bin/ not on PATH")

# The display face. Space Grotesk became the display voice on 2026-08-19; a
# clone missing it silently falls back to Helvetica and every headline in every
# reel renders in the wrong typeface — the exact failure theme/fonts.tsx
# documents for Fraunces, which took weeks to notice.
missing_fonts = [f for f in ("space-grotesk-700.woff2", "PressStart2P.ttf")
                 if not (ROOT / "public/fonts" / f).exists()]
if missing_fonts:
    report(BAD, "display fonts", f"missing {', '.join(missing_fonts)} — these ARE "
           f"tracked in git, so a clone should have them; check the clone completed")
    problems.append("fonts")
else:
    report(OK, "display fonts", "Space Grotesk + Press Start 2P present")

# Per-reel material. Its ABSENCE is normal and must not fail — a clone can
# typecheck, gate and self-test without a single frame of footage. Say so
# plainly so nobody goes looking for a bug that is a design decision.
reels = sorted(p.stem for p in (ROOT / "src/beats").glob("*.json")
               if not p.stem.endswith("-nomusic"))
have = [r for r in reels if (ROOT / "public/assets" / r).is_dir()]
if len(have) < len(reels):
    report(WARN, "per-reel footage",
           f"{len(have)}/{len(reels)} reels have assets on this machine. "
           f"public/assets/ is excluded from git by design — the repo is the "
           f"SYSTEM, not the material. You can build and check any reel; you "
           f"can only RENDER the ones whose footage is here.")
    warnings.append("footage")
else:
    report(OK, "per-reel footage", f"all {len(reels)} reels have assets")

# GLOBAL skills. The 29 in-repo skills travel in the clone — .claude/skills/
# holds 8 real dirs plus 21 symlinks into .agents/skills/, and BOTH are tracked,
# so a clone gets all 661 files with no install step. The global ones do not:
# they live in ~/.agents/skills, outside any repo, and git cannot carry an
# installed copy. That is the same premise as this whole section, and it was the
# one item in the category nothing checked — so a new machine passed every check
# here while showrunner's humanizer / youtube-seo / thumbnail-design stages
# quietly had no skill to call.
#
# Read the expected set from the installer instead of retyping it. A list typed
# here is a second source of truth that goes stale the first time the installer
# gains a skill, which is the failure this check exists to catch.
installer = ROOT / "tools/install_global_skills.sh"
expected: list[str] = []
if installer.exists():
    body = installer.read_text()
    block = re.search(r"^SKILLS=\((.*?)^\)", body, re.S | re.M)
    if block:
        expected += re.findall(r'"[^"]*@([^"@]+)"', block.group(1))
expected += sorted(p.name for p in (ROOT / "skills-global").glob("*")
                   if (p / "SKILL.md").exists())

# ~/.claude/skills is the path the agent reads; ~/.agents/skills is where the
# files sit. .exists() follows symlinks, so a dangling link counts as missing —
# which is exactly right, and is how ffmpeg-ytdlp was found missing on the
# machine that wrote it.
read_path = Path.home() / ".claude/skills"
absent = [s for s in expected if not (read_path / s / "SKILL.md").exists()]
if not expected:
    report(WARN, "global skills", "could not read tools/install_global_skills.sh")
    warnings.append("global skills")
elif absent:
    report(WARN, "global skills",
           f"{len(expected) - len(absent)}/{len(expected)} installed; missing "
           f"{', '.join(absent)}. These are ADVISORY — every gate, self-test and "
           f"render works without them, but the scripting and packaging stages "
           f"lose the helpers they reach for. Fix: bash tools/install_global_skills.sh")
    warnings.append("global skills")
else:
    report(OK, "global skills", f"all {len(expected)} present in ~/.claude/skills")

if FRESH:
    print("\n  A fresh clone is ready when nothing above says FAIL — here, and "
          "in\n  `-- binaries --` up top, where ffmpeg and ffprobe are checked "
          "against PATH.\n  The footage warning is expected: scout a new reel, "
          "or copy\n  public/assets/<slug>/ for an old one. The skills warning, "
          "if any, is one\n  command: bash tools/install_global_skills.sh")

print("\n-- hygiene --")
stray = [p for p in (ROOT / "public/assets").glob("*/_sources") if p.is_dir()]
if stray:
    report(BAD, "public/ is heavy",
           f"{len(stray)} _sources dir(s) under public/ — Remotion copies all "
           "of public/ every render. Move to <repo>/_sources/<slug>/")
    problems.append("public/_sources")
else:
    report(OK, "public/ lean", "no raw sources under public/")

print()
if problems:
    print(f"DOCTOR FAILED — {len(problems)} problem(s): {', '.join(problems)}")
    sys.exit(1)
if warnings:
    print(f"doctor ok, {len(warnings)} warning(s): {', '.join(warnings)}")
else:
    print("doctor ok — toolchain complete.")


# ---------------------------------------------------------------- assumptions
#
# doctor proves the toolchain is whole. This asks a different question: is the
# toolchain still shaped around problems that still exist? Four constraints cost
# real time on 2026-08-19 after their reasons had been removed, and nothing
# noticed because nothing re-reads a reason. ADVICE — it never fails doctor.
try:
    import subprocess as _sp
    from pathlib import Path as _P
    _sp.run([__import__("sys").executable,
             str(_P(__file__).resolve().parent.parent / "tools/check_assumptions.py")],
            check=False)
except Exception as _e:  # noqa: BLE001
    print(f"  (assumption register unavailable: {_e})")

