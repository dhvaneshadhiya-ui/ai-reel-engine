#!/usr/bin/env python3
"""Validate a Nick-style reel job and its beat sheet."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_ENGINE = Path(__file__).resolve().parent.parent  # repo root

# reel_gates.py owns the style/caption alias map; import it rather than keeping
# a second copy here (two copies drift — see CLAUDE.md "Keeping two machines
# honest"). Falls back to identity if tools/ is unavailable.
sys.path.insert(0, str(DEFAULT_ENGINE / "tools"))
try:
    from reel_gates import canon_caption, canon_style  # noqa: E402
except Exception:                                       # pragma: no cover
    def canon_style(v):    # type: ignore[misc]
        return v

    def canon_caption(v):  # type: ignore[misc]
        return v
MEDIA_KEYS = {
    "src",
    "topSrc",
    "bottomSrc",
    "bgSrc",
    "media",
    "leftSrc",
    "rightSrc",
    "topSrc",
    "bottomSrc",
    "audio",
}
DISPLAY_TYPES = {"typecard", "wordcascade"}
FACE_TYPES = {"split", "footage", "wordcascade"}


def iter_media(value: Any, key: str | None = None):
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key in MEDIA_KEYS and isinstance(child, str):
                yield child_key, child
            yield from iter_media(child, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from iter_media(child, key)


def duration(path: Path) -> float | None:
    if not path.exists() or not shutil.which("ffprobe"):
        return None
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument(
        "--engine",
        type=Path,
        default=Path(os.environ.get("REEL_ENGINE", DEFAULT_ENGINE)),
    )
    args = parser.parse_args()
    slug = args.slug
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        raise SystemExit("slug must use lowercase letters, numbers, and hyphens")

    # A DERIVATIVE sheet (e.g. "<slug>-nomusic", the sanctioned music-free
    # export) shares the parent's brief, script, manifest and assets — only the
    # beat sheet differs. Resolving those against the derivative slug demanded a
    # duplicate job folder and a second copy of every asset under public/, which
    # the repo explicitly does not want. Same staleness the ledger records twice
    # for this file: reel_gates already accepted these sheets, validate_job did not.
    base = slug
    for suffix in ("-nomusic",):
        if slug.endswith(suffix):
            candidate = slug[: -len(suffix)]
            if (DEFAULT_ENGINE / f"jobs/{candidate}/brief.json").exists():
                base = candidate
            break

    engine = args.engine.expanduser().resolve()
    public = engine / "public"
    errors: list[str] = []
    warnings: list[str] = []

    required = {
        "brief": engine / f"jobs/{base}/brief.json",
        "giveaway": engine / f"jobs/{base}/giveaway.md",
        # THE APPROVED NARRATION, not a second copy of it. This pointed at
        # scripts/<slug>.md while script_approval.py hashes
        # jobs/<slug>/script.md — so the CTA-keyword check ran against a file
        # that G27 does not protect and that nothing keeps in step with the
        # words actually spoken. Two copies drift; check the one that is
        # binding (2026-08-22). Older reels that only have the scripts/ copy
        # still validate through the fallback below.
        "script": (engine / f"jobs/{base}/script.md"
                   if (engine / f"jobs/{base}/script.md").exists()
                   else engine / f"scripts/{base}.md"),
        "manifest": public / f"assets/{base}/manifest.json",
        "beats": engine / f"src/beats/{slug}.json",
    }
    for label, path in required.items():
        if not path.exists():
            errors.append(f"missing {label}: {path}")
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors))
        raise SystemExit(1)

    brief = json.loads(required["brief"].read_text())
    manifest = json.loads(required["manifest"].read_text())
    beats = json.loads(required["beats"].read_text())

    # 2026-08-12: was hardcoded to "nick-saraev", which meant the job path
    # rejected every reel actually shipped (all varun-mayya) while config.json
    # defaulted to varun-mayya. A style is valid if it has a pack in styles/.
    # 2026-08-16: packs renamed to editorial/utility; legacy creator ids are
    # canonicalised first so old briefs still validate.
    known = sorted(p.stem for p in (DEFAULT_ENGINE / "styles").glob("*.md")
                   if not p.stem.endswith("-playbook"))
    if canon_style(brief.get("style")) not in known:
        errors.append(f"brief style {brief.get('style')!r} has no pack in "
                      f"styles/ — known: {known}")
    if beats.get("id") != slug:
        errors.append(f"beat id must equal slug {slug!r}")
    for key, expected in (("fps", 30), ("width", 1080), ("height", 1920)):
        if beats.get(key) != expected:
            errors.append(f"{key} must be {expected}")
    # Locked caption style lives in config.json (user rule 2026-07-30;
    # renamed to word-reveal 2026-08-16). reel_gates G10 is the primary gate;
    # this mirrors it instead of hardcoding a literal.
    cfg = engine / "config.json"
    locked_style = "word-reveal"
    if cfg.exists():
        try:
            locked_style = json.loads(cfg.read_text()).get("defaults", {}).get(
                "captionStyle", locked_style)
        except Exception:
            pass
    if canon_caption(beats.get("captionStyle")) != canon_caption(locked_style):
        # PER-REEL OVERRIDE, WITH A REASON — same shape as allowLong,
        # noCredits and capture.mjs --desktop-reason (added 2026-08-22).
        #
        # This blocked outright while reel_gates only ADVISES the same thing
        # (G10), so the two tools disagreed about whether the locked caption
        # treatment is law. It is a DEFAULT: the user picks the treatment, and
        # on 2026-08-22 asked for a bolder one to match a reel's subject. What
        # the lock should stop is drifting off the production treatment by
        # accident, so the override is an argument, not a switch.
        reason = str(beats.get("captionStyleReason") or "").strip()
        if reason:
            warnings.append(
                f"captionStyle is {beats.get('captionStyle')!r}, not the locked "
                f"{locked_style!r}. Reason: {reason}")
        else:
            errors.append(
                f"captionStyle must be {locked_style}, or set "
                f"`captionStyleReason` on the beat sheet saying why this reel "
                f"differs")

    scenes = beats.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must be a non-empty list")
        scenes = []
    captions = beats.get("captions")
    if not isinstance(captions, list) or not captions:
        errors.append("captions must be a non-empty list")

    total = 0.0
    for index, scene in enumerate(scenes):
        scene_type = scene.get("type", "")
        scene_duration = scene.get("durationSec")
        if not isinstance(scene_duration, (int, float)) or scene_duration <= 0:
            errors.append(f"scene {index}: invalid durationSec")
            continue
        total += float(scene_duration)
        if scene_duration > 4.2:
            warnings.append(
                f"scene {index} ({scene_type}) is {scene_duration:.2f}s; "
                "verify it moves internally"
            )
        if scene_type == "split" and scene.get("captionBottom", 0) < 900:
            errors.append(f"scene {index}: split captions must clear the face seam")
        if scene_type in DISPLAY_TYPES and scene.get("hideCaptions") is False:
            errors.append(f"scene {index}: display type cannot force captions on")

    if scenes:
        first = scenes[0]
        face_ok = first.get("type") in FACE_TYPES and (
            first.get("type") == "split"
            or "avatar" in str(first.get("src", "")).lower()
            or "avatar" in str(first.get("bottomSrc", "")).lower()
        )
        # A reel with NO presenter anywhere is a deliberate build (VO over
        # footage), not an opening that forgot the face. reel_gates already
        # treats facecam share as ADVICE (G06/G17); this blocked on it, so the
        # two tools disagreed about whether a presenter is optional. Blocks
        # only when the reel HAS a presenter and the opening hides them.
        has_presenter = any(
            "avatar" in str(sc.get(k, "")).lower()
            for sc in scenes for k in ("src", "topSrc", "bottomSrc")
        )
        if not face_ok:
            if has_presenter:
                errors.append("opening scene must visibly include the presenter")
            else:
                warnings.append(
                    "no presenter anywhere — VO-only reel; opening face rule "
                    "skipped")
        if first.get("durationSec", 0) > 2.8:
            warnings.append("opening face scene exceeds 2.8s")
        average = total / len(scenes)
        if average > 2.5:
            warnings.append(f"average scene duration {average:.2f}s exceeds 2.5s")
        for index in range(1, len(scenes)):
            if scenes[index - 1].get("type") == scenes[index].get("type"):
                warnings.append(
                    f"scenes {index - 1} and {index} repeat "
                    f"{scenes[index].get('type')} treatment"
                )

    # A VO-only cut is legitimate, and reel_gates.py (the authority on what
    # blocks a render) has said so since 2026-08-17 via `noMusic` +
    # `noMusicReason` — the same shape as G02's `allowLong`. This validator was
    # never taught the escape hatch, so a sheet that passes the gates failed
    # here on a rule the gates already allow an argued exception to. Same
    # staleness as the opening-scene check above. The reason string is still
    # mandatory: the hatch has to be argued for in one line, not switched on.
    music = beats.get("music")
    if beats.get("noMusic"):
        if not str(beats.get("noMusicReason") or "").strip():
            errors.append("noMusic is set with no noMusicReason")
    elif not isinstance(music, dict) or not music.get("points"):
        errors.append("music bed with automation points is required")

    missing_media: set[str] = set()
    for _, media_path in iter_media(beats):
        if re.match(r"^https?://", media_path):
            continue
        local = public / media_path
        if not local.exists():
            missing_media.add(media_path)
    for media_path in sorted(missing_media):
        errors.append(f"missing public asset: {media_path}")

    audio_path = beats.get("audio")
    audio_duration = duration(public / audio_path) if isinstance(audio_path, str) else None
    if audio_duration is not None and abs(audio_duration - total) > 0.20:
        errors.append(
            f"scene duration {total:.2f}s differs from audio "
            f"{audio_duration:.2f}s by more than 0.20s"
        )

    # Current manifest schema (AGENT.md §2) keeps sourced assets in
    # "assets" (id/kind/source/credit); "items" is the legacy shape.
    items = manifest.get("items") or manifest.get("assets") or []
    if not isinstance(items, list) or not items:
        warnings.append("manifest contains no sourced assets")
    for index, item in enumerate(items if isinstance(items, list) else []):
        if item.get("kind") in {"coded-graphic", "generated-illustration", "generated-video"}:
            continue
        if not (item.get("source_url") or item.get("source")):
            errors.append(f"manifest item {index} lacks source_url")
        if not item.get("credit"):
            warnings.append(f"manifest item {index} lacks on-screen credit")

    script_text = required["script"].read_text()
    keyword = str(brief.get("cta_keyword", ""))
    if keyword and keyword.lower() not in script_text.lower():
        errors.append(f"CTA keyword {keyword!r} is missing from the final script")
    if required["giveaway"].stat().st_size < 80:
        errors.append("giveaway resource is still a placeholder")

    print(f"job: {slug}")
    print(f"scenes: {len(scenes)}, total: {total:.2f}s")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        raise SystemExit(1)
    print("validation passed")


if __name__ == "__main__":
    main()
