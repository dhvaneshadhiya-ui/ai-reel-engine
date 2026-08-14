#!/usr/bin/env python3
"""Compile a phrase-anchored Nick reel shot plan into a Remotion beat sheet."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_ENGINE = Path(__file__).resolve().parent.parent  # repo root


def normalize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower().replace("’", "'"))


def load_words(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text())
    if isinstance(raw, dict) and isinstance(raw.get("words"), list):
        words = raw["words"]
    elif isinstance(raw, dict) and isinstance(raw.get("segments"), list):
        words = [
            word
            for segment in raw["segments"]
            for word in segment.get("words", [])
        ]
    else:
        raise SystemExit(f"unsupported Whisper JSON shape: {path}")

    out: list[dict[str, Any]] = []
    for index, word in enumerate(words):
        text = str(word.get("word", word.get("text", ""))).strip()
        if not text:
            continue
        try:
            start = float(word["start"])
            end = float(word["end"])
        except (KeyError, TypeError, ValueError):
            raise SystemExit(f"invalid word timing at index {index}: {word!r}")
        tokens = normalize(text)
        if not tokens:
            continue
        # Whisper occasionally returns ".8" or punctuation as a separate word.
        if text.startswith(".") and out and tokens[0].isdigit():
            out[-1]["text"] = f'{out[-1]["text"]}.{tokens[0]}'
            out[-1]["norm"] = normalize(out[-1]["text"])[-1]
            out[-1]["end"] = end
            continue
        for token_index, token in enumerate(tokens):
            out.append(
                {
                    "text": text if len(tokens) == 1 else token,
                    "norm": token,
                    "start": start,
                    "end": end,
                    "source_index": index,
                    "sub_index": token_index,
                }
            )
    if not out:
        raise SystemExit(f"no timed words found in {path}")
    return out


def find_phrase(
    words: list[dict[str, Any]], phrase: str, cursor: int, label: str
) -> tuple[int, int]:
    needle = normalize(phrase)
    if not needle:
        raise SystemExit(f"{label} cannot be empty")
    haystack = [word["norm"] for word in words]
    for start in range(cursor, len(haystack) - len(needle) + 1):
        if haystack[start : start + len(needle)] == needle:
            return start, start + len(needle) - 1
    preview = " ".join(haystack[cursor : cursor + 24])
    raise SystemExit(
        f"could not resolve {label} {phrase!r} after word {cursor}; "
        f"next transcript words: {preview!r}"
    )


def media_info(path: Path) -> dict[str, float] | None:
    if not path.exists() or not shutil.which("ffprobe"):
        return None
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,width,height",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        data = json.loads(result.stdout)
        video = next(
            stream
            for stream in data.get("streams", [])
            if stream.get("codec_type") == "video"
        )
        return {
            "duration": float(data["format"]["duration"]),
            "width": float(video["width"]),
            "height": float(video["height"]),
        }
    except (StopIteration, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def css_focus_x(
    face_x: float, image_width: float, image_height: float, box_width: float, box_height: float
) -> float:
    """Return CSS object-position x that centers a face in a cover-fitted box."""
    image_aspect = image_width / image_height
    box_aspect = box_width / box_height
    if image_aspect <= box_aspect:
        return 0.5
    scaled_width = image_width * (box_height / image_height)
    crop = scaled_width - box_width
    if crop <= 0:
        return 0.5
    position = (face_x * scaled_width - box_width / 2) / crop
    return round(max(0.0, min(1.0, position)), 4)


def substitute(value: Any, tokens: dict[str, Any]) -> Any:
    if isinstance(value, dict):
        return {key: substitute(child, tokens) for key, child in value.items()}
    if isinstance(value, list):
        return [substitute(child, tokens) for child in value]
    if isinstance(value, str) and value in tokens:
        return tokens[value]
    return value


def caption_words(
    words: list[dict[str, Any]], corrections: dict[str, str]
) -> list[dict[str, Any]]:
    corrected: list[dict[str, Any]] = []
    for word in words:
        text = word["text"].strip()
        key = re.sub(r"[^a-z0-9]", "", text.lower())
        if key in corrections:
            punctuation = re.sub(r"[A-Za-z0-9.]+", "", text)
            text = corrections[key] + punctuation
        corrected.append({"start": word["start"], "end": word["end"], "text": text})

    chunks: list[dict[str, Any]] = []
    for index in range(0, len(corrected), 3):
        group = corrected[index : index + 3]
        chunks.append(
            {
                "start": round(group[0]["start"], 3),
                "end": round(group[-1]["end"], 3),
                "text": " ".join(item["text"] for item in group),
            }
        )
    return chunks


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

    engine = args.engine.expanduser().resolve()
    public = engine / "public"
    job_dir = engine / "jobs" / slug
    plan_path = job_dir / "shot-plan.json"
    vo_path = public / f"assets/{slug}/vo.json"
    manifest_path = public / f"assets/{slug}/manifest.json"
    avatar_rel = f"assets/{slug}/avatar-master.mp4"
    face_path = public / f"assets/{slug}/face-x.txt"
    for path in (plan_path, vo_path, manifest_path):
        if not path.exists():
            raise SystemExit(f"missing required input: {path}")

    plan = json.loads(plan_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    words = load_words(vo_path)
    audio_end = float(words[-1]["end"])
    avatar_info = media_info(public / avatar_rel)
    if avatar_info is not None:
        audio_end = min(audio_end, avatar_info["duration"])
    face_x = 0.5
    if face_path.exists():
        try:
            face_x = float(face_path.read_text().strip())
        except ValueError:
            raise SystemExit(f"invalid face-center value: {face_path}")
    if not 0 <= face_x <= 1:
        raise SystemExit("face-x.txt must contain a fraction from 0 to 1")
    if avatar_info is not None:
        focus_full = css_focus_x(
            face_x,
            avatar_info["width"],
            avatar_info["height"],
            1080,
            1920,
        )
        focus_split = css_focus_x(
            face_x,
            avatar_info["width"],
            avatar_info["height"],
            1080,
            960,
        )
    else:
        focus_full = focus_split = round(face_x, 4)

    manifest_items = {
        str(item.get("id")): item for item in manifest.get("items", []) if item.get("id")
    }
    shots = plan.get("shots")
    if not isinstance(shots, list) or not shots:
        raise SystemExit(f"shot plan contains no shots: {plan_path}")

    resolved: list[dict[str, Any]] = []
    cursor = 0
    for index, shot in enumerate(shots):
        start_i, _ = find_phrase(
            words, str(shot.get("start_phrase", "")), cursor, f"shot {index} start_phrase"
        )
        end_i = start_i
        if shot.get("end_phrase"):
            _, end_i = find_phrase(
                words,
                str(shot["end_phrase"]),
                start_i,
                f"shot {index} end_phrase",
            )
        start = float(words[start_i]["start"]) + float(shot.get("start_offset", 0))
        end = float(words[end_i]["end"]) + float(shot.get("end_offset", 0))
        if index == 0:
            start = 0.0
        resolved.append({"start": max(0.0, start), "end": min(audio_end, end), **shot})
        cursor = max(start_i + 1, end_i)

    # Phrase endpoints are editorial anchors. Make the final timeline seamless
    # by cutting each scene at the next scene's resolved start.
    scenes: list[dict[str, Any]] = []
    for index, shot in enumerate(resolved):
        start = float(shot["start"])
        end = (
            float(resolved[index + 1]["start"])
            if index + 1 < len(resolved)
            else audio_end
        )
        if end <= start:
            raise SystemExit(f"shot {index} has non-positive resolved duration")
        asset_id = shot.get("asset_id")
        asset = manifest_items.get(str(asset_id)) if asset_id else None
        if asset_id and asset is None:
            raise SystemExit(f"shot {index} references unknown manifest asset {asset_id!r}")
        scene = substitute(
            shot.get("scene", {}),
            {
                "$AVATAR": avatar_rel,
                "$START": round(start, 3),
                "$FACE_X": round(face_x, 4),
                "$FOCUS_FULL": focus_full,
                "$FOCUS_SPLIT": focus_split,
            },
        )
        if not isinstance(scene, dict) or not scene.get("type"):
            raise SystemExit(f"shot {index} lacks a valid scene")
        scene["durationSec"] = round(end - start, 3)
        if asset:
            scene.setdefault("assetId", str(asset_id))
            scene.setdefault("claimId", str(shot.get("claim_id", asset_id)))
            if asset.get("source_url"):
                scene.setdefault("sourceUrl", asset["source_url"])
            if asset.get("credit") and scene["type"] in {
                "footage",
                "receipt",
                "floatcard",
                "split",
            }:
                scene.setdefault("credit", asset["credit"])
        for media_key, trim_key in (
            ("src", "from"),
            ("bottomSrc", "bottomFrom"),
            ("topSrc", "topFrom"),
            ("bgSrc", "bgFrom"),
        ):
            if scene.get(media_key) == avatar_rel and trim_key not in scene:
                scene[trim_key] = round(start, 3)
        if scene.get("src") == avatar_rel and scene.get("type") == "footage":
            scene.setdefault("focusX", focus_full)
        if scene.get("bottomSrc") == avatar_rel:
            scene.setdefault("bottomFocusX", focus_split)
        scenes.append(scene)

    corrections = {
        re.sub(r"[^a-z0-9]", "", str(key).lower()): str(value)
        for key, value in plan.get("caption_corrections", {}).items()
    }
    music = plan.get("music") or {
        "src": "music/bed-726.mp3",
        "from": 0,
        "points": [
            {"t": 0, "vol": 0.11},
            {"t": max(0, audio_end - 0.8), "vol": 0.11},
            {"t": round(audio_end, 3), "vol": 0.0},
        ],
    }
    beats = {
        "id": slug,
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "style": "nick",
        "audio": avatar_rel,
        "music": music,
        "captionStyle": "chip-lg",
        "emphasis": plan.get("emphasis", []),
        "scenes": scenes,
        "captions": caption_words(words, corrections),
    }
    output = engine / f"src/beats/{slug}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(beats, indent=2, ensure_ascii=False) + "\n")
    print(f"compiled {len(scenes)} shots, {audio_end:.3f}s: {output}")


if __name__ == "__main__":
    main()
