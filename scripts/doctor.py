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
need_bin("ffmpeg", "install ffmpeg")
need_bin("ffprobe", "install ffmpeg")
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
        ("avatar.voiceSpeed", av.get("voiceSpeed"), 1.05),
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
