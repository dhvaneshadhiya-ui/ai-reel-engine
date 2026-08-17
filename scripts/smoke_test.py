#!/usr/bin/env python3
"""Run a no-network, no-credit smoke test of the Nick reel job compiler."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

# reel_gates.py owns the style/caption alias map — import it rather than
# keeping a second copy (two copies drift).
sys.path.insert(0, str(SCRIPTS.parent / "tools"))
from reel_gates import canon_caption  # noqa: E402


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="nick-reel-smoke-") as temporary:
        engine = Path(temporary)
        (engine / "package.json").write_text('{"name":"nick-reel-smoke"}\n')
        asset_dir = engine / "public/assets/pipeline-smoke"
        music_dir = engine / "public/music"
        asset_dir.mkdir(parents=True)
        music_dir.mkdir(parents=True)

        run(
            [
                sys.executable,
                str(SCRIPTS / "new_job.py"),
                "pipeline-smoke",
                "--topic",
                "A synthetic pipeline test",
                "--details",
                "No network or paid services",
                "--cta-keyword",
                "TEST",
                "--engine",
                str(engine),
            ]
        )
        run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "color=c=0xefe9dc:s=1080x1920:r=30:d=6",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=440:sample_rate=48000:duration=6",
                "-shortest",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                str(asset_dir / "avatar-master.mp4"),
            ]
        )
        run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "color=c=0xff6b4a:s=1080x960",
                "-frames:v",
                "1",
                str(asset_dir / "proof.png"),
            ]
        )
        run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=110:sample_rate=48000:duration=6",
                "-c:a",
                "libmp3lame",
                str(music_dir / "bed-726.mp3"),
            ]
        )

        words = [
            {"start": 0.0, "end": 0.5, "word": "This"},
            {"start": 0.5, "end": 1.0, "word": "is"},
            {"start": 1.0, "end": 1.5, "word": "a"},
            {"start": 1.5, "end": 2.0, "word": "fast"},
            {"start": 2.1, "end": 2.7, "word": "second"},
            {"start": 2.7, "end": 3.3, "word": "proof"},
            {"start": 3.3, "end": 4.0, "word": "stays"},
            {"start": 4.0, "end": 6.0, "word": "clear"},
        ]
        (asset_dir / "vo.json").write_text(json.dumps({"words": words}, indent=2))
        (asset_dir / "face-x.txt").write_text("0.5000\n")
        (asset_dir / "manifest.json").write_text(
            json.dumps(
                {
                    "slug": "pipeline-smoke",
                    "items": [
                        {
                            "id": "coded-proof",
                            "kind": "coded-graphic",
                            "local_path": "assets/pipeline-smoke/proof.png",
                            "claim": "Synthetic proof",
                            "shows": "A coral proof panel",
                            "rights_note": "generated fixture",
                        }
                    ],
                },
                indent=2,
            )
        )
        (engine / "jobs/pipeline-smoke/shot-plan.json").write_text(
            json.dumps(
                {
                    "emphasis": ["fast", "clear"],
                    "caption_corrections": {},
                    "shots": [
                        {
                            "start_phrase": "this is",
                            "end_phrase": "a fast",
                            "asset_id": "coded-proof",
                            "scene": {
                                "type": "split",
                                "topSrc": "assets/pipeline-smoke/proof.png",
                                "bottomSrc": "$AVATAR",
                                "bottomFrom": "$START",
                                "bottomFocusX": "$FOCUS_SPLIT",
                                "captionBottom": 1000,
                            },
                        },
                        {
                            "start_phrase": "second proof",
                            "end_phrase": "stays clear",
                            "scene": {
                                "type": "typecard",
                                "kinetic": {
                                    "text": "SECOND PROOF",
                                    "style": "caps",
                                },
                            },
                        },
                    ],
                },
                indent=2,
            )
        )
        (engine / "jobs/pipeline-smoke/giveaway.md").write_text(
            "# Synthetic resource\n\nComment **TEST** to receive this complete "
            "offline smoke-test checklist and reproducible fixture.\n"
        )
        (engine / "scripts/pipeline-smoke.md").write_text(
            "# Synthetic script\n\nThis is a fast second proof that stays clear. "
            "Comment TEST for the checklist.\n"
        )

        run(
            [
                sys.executable,
                str(SCRIPTS / "compile_shot_plan.py"),
                "pipeline-smoke",
                "--engine",
                str(engine),
            ]
        )
        run(
            [
                sys.executable,
                str(SCRIPTS / "validate_job.py"),
                "pipeline-smoke",
                "--engine",
                str(engine),
            ]
        )
        beats = json.loads((engine / "src/beats/pipeline-smoke.json").read_text())
        # Assert against the LOCKED value, not a literal — this asserted the
        # stale "chip-lg" and so agreed with the bug in compile_shot_plan.py
        # instead of catching it (fixed 2026-08-16).
        # Same fallback as validate_job.py / compile_shot_plan.py: the temp
        # engine this test builds carries no config.json.
        cfg = engine / "config.json"
        locked_style = "word-reveal"
        if cfg.exists():
            locked_style = json.loads(cfg.read_text()).get("defaults", {}).get(
                "captionStyle", locked_style)
        # Compare canonically: a legacy id and its canonical name are the same
        # treatment, so the assertion must not fail on the spelling alone.
        assert canon_caption(beats["captionStyle"]) == canon_caption(locked_style), (
            f'captionStyle {beats["captionStyle"]!r} != locked {locked_style!r}'
        )
        assert len(beats["scenes"]) == 2
        assert abs(sum(scene["durationSec"] for scene in beats["scenes"]) - 6) < 0.01
        assert beats["scenes"][0]["assetId"] == "coded-proof"
        print("nick-reel smoke test passed")


if __name__ == "__main__":
    main()
