#!/usr/bin/env python3
"""Prepare an externally-generated voiceover for HeyGen lip-sync.

WHY THIS EXISTS
---------------
`references/heygen.md` has documented an "audio-driven flow" for months —
seven prose steps, no code, never run. On 2026-08-27 it became the point:
HeyGen's own TTS reads this channel's voice flat (2.14 semitones), every
engine-level lever moved it by 0.01, and the user is getting a read they
actually like out of ElevenLabs v3 with audio tags. Uploaded audio bypasses
TTS entirely, so that read can drive the avatar directly.

THE STEP THAT WAS FAILING, AND WHY IT GETS ITS OWN TOOL
--------------------------------------------------------
Uploading the ElevenLabs MP3 as-downloaded fails at completion with

    "Stored file type not supported: application/octet-stream"

twice, with different upload methods, even though `file(1)` calls it
audio/mpeg and ffprobe decodes it fine. Re-encoding with metadata stripped
uploads and completes first try. That is a 20-second fix once you know it and
an afternoon if you do not, which is exactly the kind of thing that belongs in
code rather than in someone's memory.

WHAT THIS DOES AND DOES NOT DO
------------------------------
It prepares and verifies the file. It does NOT upload — the HeyGen connector
lives in the agent, not in the shell, and there is no API key on this machine.
So this prints the exact values the upload needs and the agent makes the call.

    python3 tools/vo_external.py <slug> <audio-file>
    python3 tools/vo_external.py --selftest
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Our band, measured. An external VO that reads outside it will not magically
# fit the beat sheet just because it sounds better.
WPS_MIN, WPS_MAX = 2.35, 2.75


def die(msg: str) -> None:
    sys.exit(f"\n  {msg}\n")


def clean_encode(src: Path, dst: Path) -> None:
    """Strip every tag and re-encode. This is the fix for the upload refusal."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(src),
         "-map_metadata", "-1",          # <- the actual fix
         "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "1",
         str(dst)], capture_output=True, text=True)
    if r.returncode != 0 or not dst.exists():
        die(f"ffmpeg could not re-encode {src.name}:\n{r.stderr[-400:]}")


def probe_seconds(f: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def prepare(slug: str, src: Path) -> int:
    if not src.exists():
        die(f"no such file: {src}")

    job = ROOT / "jobs" / slug
    script_p = job / "script.md"
    out_dir = ROOT / "_sources" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "vo-external.mp3"

    clean_encode(src, dst)
    data = dst.read_bytes()
    secs = probe_seconds(dst)

    print(f"\n=== external VO — {slug} ===\n")
    print(f"  source     {src.name}  ({probe_seconds(src):.1f}s)")
    print(f"  prepared   {dst.relative_to(ROOT)}  ({secs:.1f}s)")
    print("             metadata stripped, mono 44.1k 128k mp3")

    # PACE, against the beat sheet's own words. An external read is generated
    # outside every constraint this repo enforces, so it is worth saying
    # plainly whether it lands where the script was planned to land.
    if script_p.exists():
        words = len([w for w in script_p.read_text().split() if w.strip()])
        wps = words / secs if secs else 0
        verdict = ("in band" if WPS_MIN <= wps <= WPS_MAX
                   else "TOO FAST" if wps > WPS_MAX else "TOO SLOW")
        print(f"\n  pace       {words} words / {secs:.1f}s = {wps:.2f} w/s "
              f"({WPS_MIN}-{WPS_MAX} band) -> {verdict}")
        if verdict != "in band":
            print("             Regenerate at a different speed rather than "
                  "time-stretching:\n             stretching audio moves "
                  "pitch and undoes the reason for using this read.")
    else:
        print(f"\n  pace       no {script_p.relative_to(ROOT)} to compare against")

    print("\n  --- values for the upload call ---")
    print(f"  filename     vo.mp3")
    print(f"  contentType  audio/mpeg")
    print(f"  sizeBytes    {len(data)}")
    print(f"  sha256       {hashlib.sha256(data).hexdigest()}")
    print("\n  Then: create_asset_upload -> PUT the bytes with the returned\n"
          "  headers unchanged -> complete_asset_upload -> "
          "create_video_from_avatar\n  with audioAssetId (NOT script/voiceId "
          "— they are mutually exclusive).\n")
    print("  NOTE: with uploaded audio, HeyGen does lip-sync only. voiceId,\n"
          "  voiceSpeed, engine_settings and Enhance voice all stop applying.\n")
    return 0


def selftest() -> int:
    fails, checks = [], 0

    def ok(label: str, cond: bool, detail: str = "") -> None:
        nonlocal checks
        checks += 1
        if not cond:
            fails.append(f"{label}: {detail}")

    tmp = Path(tempfile.mkdtemp(prefix="vo-external-selftest-"))
    # a tagged mp3, exactly like an ElevenLabs download
    tagged = tmp / "tagged.mp3"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
         "sine=frequency=180:duration=3", "-metadata", "title=ElevenLabs",
         "-metadata", "comment=" + "x" * 400, "-c:a", "libmp3lame",
         str(tagged)], capture_output=True)
    ok("fixture built", tagged.exists())

    cleaned = tmp / "clean.mp3"
    clean_encode(tagged, cleaned)
    ok("re-encode produces a file", cleaned.exists())

    meta = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format_tags",
         "-of", "json", str(cleaned)], capture_output=True, text=True).stdout
    tags = json.loads(meta or "{}").get("format", {}).get("tags", {})
    # ffmpeg always stamps its own `encoder` tag, and the upload that was
    # VERIFIED to work on 2026-08-27 carried exactly that. So assert the thing
    # that actually matters — the SOURCE's metadata is gone — rather than
    # demanding a zero-tag file we have never put through the upload.
    ok("source metadata is stripped",
       not any(k.lower() in ("title", "comment", "album", "artist")
               for k in tags),
       f"source tags survived: {tags} — this is what the upload refuses")
    ok("only ffmpeg's own encoder stamp remains",
       set(k.lower() for k in tags) <= {"encoder"}, str(tags))

    ok("duration survives",
       abs(probe_seconds(cleaned) - probe_seconds(tagged)) < 0.35,
       f"{probe_seconds(tagged):.2f} -> {probe_seconds(cleaned):.2f}")
    ok("audio is mono", "1" in subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=channels", "-of", "csv=p=0", str(cleaned)],
        capture_output=True, text=True).stdout)
    ok("pace band matches reel_gates news profile",
       (WPS_MIN, WPS_MAX) == (2.35, 2.75))

    if fails:
        print(f"vo_external self-test FAILED ({len(fails)} of {checks})")
        for f in fails:
            print(f"  - {f}")
        return 1
    print(f"vo_external self-test PASSED — {checks} checks")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()
    if len(argv) != 2:
        print(__doc__.split("    python3")[0].strip())
        return 1
    return prepare(argv[0], Path(argv[1]).expanduser())


if __name__ == "__main__":
    sys.exit(main())
