#!/usr/bin/env python3
"""Safely hand a completed HeyGen master into the local reel engine."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ENGINE = Path(__file__).resolve().parent.parent  # repo root


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def probe(path: Path) -> dict[str, object]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)
    duration = float(data.get("format", {}).get("duration", 0))
    video = next(
        (
            stream
            for stream in data.get("streams", [])
            if stream.get("codec_type") == "video"
        ),
        None,
    )
    audio = next(
        (
            stream
            for stream in data.get("streams", [])
            if stream.get("codec_type") == "audio"
        ),
        None,
    )
    if duration <= 0 or video is None or audio is None:
        raise SystemExit(f"avatar master is missing valid video/audio streams: {path}")
    return {"duration": duration, "video": video, "audio": audio}


def state_path(engine: Path, slug: str) -> Path:
    return engine / "_state" / f"{slug}.json"


def update_state(engine: Path, slug: str, **updates: object) -> None:
    path = state_path(engine, slug)
    data: dict[str, object] = {}
    if path.exists():
        data = json.loads(path.read_text())
    data.update(updates)
    data["slug"] = slug
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", dir=path.parent, prefix=f".{slug}.", delete=False
    ) as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("record", "download", "prepare"))
    parser.add_argument("slug")
    parser.add_argument("--video-id")
    parser.add_argument("--status")
    parser.add_argument("--source", type=Path)
    parser.add_argument(
        "--engine",
        type=Path,
        default=Path(os.environ.get("REEL_ENGINE", DEFAULT_ENGINE)),
    )
    args = parser.parse_args()
    engine = args.engine.expanduser().resolve()
    slug = args.slug
    asset_dir = engine / "public" / "assets" / slug
    master = asset_dir / "avatar-master.mp4"

    if args.action == "record":
        if not args.video_id or not args.status:
            raise SystemExit("record requires --video-id and --status")
        update_state(
            engine,
            slug,
            heygen_video_id=args.video_id,
            heygen_status=args.status,
        )
        print(f"recorded HeyGen state for {slug}")
        return

    if args.action == "download":
        url = os.environ.get("HEYGEN_DOWNLOAD_URL")
        if not url:
            raise SystemExit("set HEYGEN_DOWNLOAD_URL for the completed video")
        asset_dir.mkdir(parents=True, exist_ok=True)
        partial = asset_dir / ".avatar-master.partial"
        request = urllib.request.Request(url, headers={"User-Agent": "nick-reel/1"})
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                with partial.open("wb") as handle:
                    shutil.copyfileobj(response, handle, length=1024 * 1024)
            probe(partial)
            partial.replace(master)
        finally:
            partial.unlink(missing_ok=True)
        update_state(engine, slug, local_master=str(master), heygen_status="downloaded")
        print(f"downloaded and verified avatar master: {master}")
        return

    if args.source:
        source = args.source.expanduser().resolve()
        if not source.exists():
            raise SystemExit(f"source does not exist: {source}")
        asset_dir.mkdir(parents=True, exist_ok=True)
        if source != master:
            shutil.copy2(source, master)
    if not master.exists():
        raise SystemExit(f"avatar master is missing: {master}")

    metadata = probe(master)
    vo_wav = asset_dir / "vo.wav"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(master),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(vo_wav),
        ]
    )
    run(
        [
            "whisper",
            str(vo_wav),
            "--model",
            "base",
            "--language",
            "en",
            "--word_timestamps",
            "True",
            "--output_format",
            "json",
            "--output_dir",
            str(asset_dir),
        ]
    )
    vo_json = asset_dir / "vo.json"
    generated_json = asset_dir / f"{vo_wav.stem}.json"
    if generated_json.exists() and generated_json != vo_json:
        generated_json.replace(vo_json)

    calibration = engine / "_state" / f"{slug}-avatar-calibration.jpg"
    calibration.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(float(metadata["duration"]) / 2),
            "-i",
            str(master),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(calibration),
        ]
    )
    face_x = asset_dir / "face-x.txt"
    if not face_x.exists():
        config_path = engine / "config" / "creator.json"
        default_face_x = 0.5
        if config_path.exists():
            default_face_x = float(
                json.loads(config_path.read_text())
                .get("reel", {})
                .get("default_face_x", 0.5)
            )
        face_x.write_text(f"{default_face_x:.4f}\n")

    update_state(
        engine,
        slug,
        local_master=str(master),
        transcript=str(vo_json),
        calibration_frame=str(calibration),
        media=metadata,
        heygen_status="prepared",
    )
    print(f"prepared avatar, transcript, and calibration frame for {slug}")


if __name__ == "__main__":
    main()
