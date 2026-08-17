#!/usr/bin/env python3
"""Rehearse a script's VO locally, for free, BEFORE spending HeyGen credits.

WHY THIS EXISTS
---------------
A whole class of failure is invisible until the VO exists, because it depends
on WORD-LEVEL TIMINGS: compile_shot_plan.py anchors every shot to a
start_phrase/end_phrase in the transcript, word-reveal captions are driven by
whisper word timings, and scene durations derive from those timings — so G01
(tail freeze / audio truncation), G04 (scene dwell) and G20/G25 (cues landing
inside their scene) cannot be evaluated at all until then.

Until now the only way to get a VO was to generate the avatar, which costs
credits AND freezes the audio (CLAUDE.md). So the loop was:

    write -> SPEND CREDITS -> discover a phrase anchor doesn't resolve -> SPEND AGAIN

This synthesises a throwaway VO with chatterbox (local, free, no API key), runs
whisper on it, and checks everything that depends on word timings. Fix it all
for free, then generate the HeyGen master ONCE.

WHAT THIS IS NOT
----------------
**Not a runtime predictor.** The reel's length is predicted from the MEASURED
HeyGen rate (~2.5-2.7 wps / 148-162 wpm, three masters, ledger 2026-08-13), not
from how fast chatterbox happens to speak. Substituting an unmeasured rate for a
measured one is the exact failure G23 exists to prevent. The synthetic duration
is printed for information and explicitly labelled as not the number to trust.

**Not publishable.** The published voice is the digital twin. This audio is a
scratch artifact and is written under a rehearsal/ directory that no build step
reads.

TTS IS OPT-IN, AND WHY
----------------------
The default mode runs NO model and takes no measurable time, because the check
that actually kills a build — an unresolvable phrase anchor — can be made
against the script itself. compile_shot_plan.py matches normalised tokens
against whisper words, and whisper's words are supposed to BE the script's
words; an anchor that cannot be found in the script will never be found in the
transcript either.

Only the pronunciation check genuinely needs audio, so it sits behind --tts.
Measured 2026-08-16 on this machine (8 GB, arm64): loading chatterbox pushed
swap to 93% and the process sat at RSS 0.00 GB / 0.0% CPU for 16 minutes —
fully swapped out, making no progress. --tts therefore refuses to start unless
there is real memory free, rather than hanging and looking busy.

    python3 tools/rehearse_vo.py <slug>            # instant, no model
    python3 tools/rehearse_vo.py <slug> --tts      # + pronunciation (needs RAM)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from reel_gates import DEFAULT_FORMAT, FORMATS  # noqa: E402

VENV_PY = Path.home() / ".venvs/chatterbox/bin/python"

# MEASURED across three real masters (styles/editorial.md, ledger 2026-08-13).
# This — not the synthetic audio — is what predicts runtime.
WPS_LO, WPS_HI = 2.5, 2.7


def die(msg: str) -> None:
    sys.exit(f"rehearse_vo: {msg}")


def read_narration(slug: str) -> str:
    """Same extraction script_approval.py hashes — headings/comments stripped."""
    p = ROOT / "jobs" / slug / "script.md"
    if not p.exists():
        die(f"no script at {p} — write the narration there first.")
    spoken = "\n".join(
        l for l in p.read_text().splitlines()
        if l.strip() and not l.lstrip().startswith(("#", ">", "<!--"))
    )
    if not spoken.strip():
        die(f"{p} has no narration lines.")
    return " ".join(spoken.split())


def free_gb() -> float:
    """Free + inactive pages, in GB. Inactive is reclaimable, so it counts."""
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        pages = {}
        for line in out.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                pages[k.strip()] = int(v.strip().rstrip("."))
        return (pages.get("Pages free", 0) + pages.get("Pages inactive", 0)) * 4096 / 1073741824
    except Exception:
        return 99.0


MIN_FREE_GB = 3.0


def synthesise(text: str, out_wav: Path) -> None:
    have = free_gb()
    if have < MIN_FREE_GB:
        die(f"only {have:.1f} GB free — chatterbox needs ~{MIN_FREE_GB:.0f} GB.\n"
            f"  On 2026-08-16 it swapped this machine to 93% and sat at 0% CPU\n"
            f"  for 16 minutes without producing anything. Close some apps and\n"
            f"  retry, or drop --tts: anchors and runtime are checked without it.")
    if not VENV_PY.exists():
        die("chatterbox venv missing. Create it with:\n"
            "  python3 -m venv ~/.venvs/chatterbox && "
            "~/.venvs/chatterbox/bin/pip install chatterbox-tts\n"
            "Do NOT pip-install it into system python — it downgrades torch "
            "under whisper.")
    # Long text is chunked: TTS quality degrades and memory spikes on very long
    # single generations, and this machine has 8 GB.
    chunks, cur = [], ""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if len(cur) + len(sent) > 300 and cur:
            chunks.append(cur.strip())
            cur = sent
        else:
            cur += " " + sent
    if cur.strip():
        chunks.append(cur.strip())

    script = r'''
import sys, json, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
chunks = json.loads(sys.argv[1]); out = sys.argv[2]
dev = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"  device={dev}  chunks={len(chunks)}", flush=True)
m = ChatterboxTTS.from_pretrained(device=dev)
waves = []
for i, c in enumerate(chunks, 1):
    print(f"  synthesising {i}/{len(chunks)}", flush=True)
    waves.append(m.generate(c).squeeze(0).cpu())
torchaudio.save(out, torch.cat(waves).unsqueeze(0), m.sr)
print("  wrote", out, flush=True)
'''
    r = subprocess.run([str(VENV_PY), "-c", script, json.dumps(chunks), str(out_wav)])
    if r.returncode != 0 or not out_wav.exists():
        die("chatterbox synthesis failed (see output above)")


def transcribe(wav: Path, outdir: Path) -> list[dict]:
    if not shutil.which("whisper"):
        die("whisper not on PATH")
    subprocess.run(
        ["whisper", str(wav), "--model", "base", "--language", "en",
         "--word_timestamps", "True", "--output_format", "json",
         "--output_dir", str(outdir)],
        check=True, capture_output=True,
    )
    data = json.loads((outdir / f"{wav.stem}.json").read_text())
    return [w for seg in data.get("segments", []) for w in seg.get("words", [])]


def norm(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", s.lower().replace("’", "'"))


def check_anchors(slug: str, tokens: list[str], source: str) -> tuple[int, int]:
    """Every start_phrase/end_phrase must resolve, or compile_shot_plan dies.

    `tokens` is the normalised word stream to search — the script itself by
    default, or the whisper transcript under --tts. The script is the stricter
    and cheaper check: if a phrase is not in the script, no transcript of that
    script will contain it either.
    """
    plan_p = ROOT / "jobs" / slug / "shot-plan.json"
    if not plan_p.exists():
        print("\n-- phrase anchors --\n  (no shot-plan.json yet — skipped)")
        return 0, 0
    shots = json.loads(plan_p.read_text()).get("shots", [])
    if not shots:
        print("\n-- phrase anchors --\n  (shot-plan.json has no shots — skipped)")
        return 0, 0
    hay = tokens
    print(f"\n-- phrase anchors vs {source} (compile_shot_plan.py dies on any miss) --")
    ok = bad = 0
    cursor = 0
    for i, shot in enumerate(shots):
        for key in ("start_phrase", "end_phrase"):
            phrase = shot.get(key)
            if not phrase:
                continue
            needle = norm(phrase)
            found = -1
            for s in range(cursor, len(hay) - len(needle) + 1):
                if hay[s:s + len(needle)] == needle:
                    found = s
                    break
            if found >= 0:
                cursor = found
                ok += 1
            else:
                bad += 1
                print(f"  MISS shot {i} {key}={phrase!r} — not found after word {cursor}")
    print(f"  {ok} resolved, {bad} missing")
    return ok, bad


def check_pronunciation(script: str, words: list[dict]) -> None:
    """Words whisper heard differently are mispronunciation candidates.

    Feeds jobs/<slug>/shot-plan.json `caption_corrections`.
    """
    said = set(norm(script))
    heard = [t for w in words for t in norm(w["word"])]
    odd = [t for t in heard if t not in said]
    print("\n-- pronunciation (words whisper heard that aren't in the script) --")
    if not odd:
        print("  none — the read matches the script")
        return
    seen, out = set(), []
    for t in odd:
        if t not in seen:
            seen.add(t)
            out.append(t)
    print(f"  {len(out)} candidate(s): {', '.join(out[:14])}")
    print("  -> if a NAME or TERM is here, add it to `caption_corrections`")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--format", default=None, help="override format band")
    ap.add_argument("--tts", action="store_true",
                    help="also synthesise audio to check pronunciation "
                         "(loads a ~2 GB model; needs ~3 GB free)")
    ap.add_argument("--keep-audio", action="store_true")
    args = ap.parse_args()

    script = read_narration(args.slug)
    nwords = len(script.split())
    fmt = args.format or DEFAULT_FORMAT
    prof = FORMATS.get(fmt) or die(f"unknown format {fmt!r}")
    lo, hi = prof["runtime"]

    # _sources/, not public/ — doctor's hygiene rule exists because Remotion
    # copies ALL of public/ on every render, so a stray rehearsal wav would be
    # re-copied for the life of the job. _sources/ is the repo's scratch home
    # and is gitignored.
    outdir = ROOT / "_sources" / args.slug / "rehearsal"
    outdir.mkdir(parents=True, exist_ok=True)
    wav = outdir / "rehearsal-vo.wav"

    print(f"=== rehearsing {args.slug} ({fmt}) ===")
    print(f"  {nwords} words")

    # PREDICTED from the measured HeyGen rate. This is the number that matters.
    p_lo, p_hi = nwords / WPS_HI, nwords / WPS_LO
    verdict = ("IN BAND" if p_hi >= lo and p_lo <= hi else
               "OUT OF BAND — rewrite before generating")
    print(f"  predicted runtime {p_lo:.0f}-{p_hi:.0f}s "
          f"(measured {WPS_LO}-{WPS_HI} wps) vs {fmt} band {lo:.0f}-{hi:.0f}s  -> {verdict}")

    if not args.tts:
        bad = check_anchors(args.slug, norm(script), "the script")[1]
        print("\n-- pronunciation --")
        print("  skipped (needs audio) — re-run with --tts when RAM allows")
        print(f"\nNEXT: fix anything above, THEN generate the avatar once.")
        sys.exit(1 if bad else 0)

    print("\n-- synthesising (local, free) --")
    synthesise(script, wav)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(wav)],
        capture_output=True, text=True).stdout.strip() or 0)
    print(f"  synthetic audio {dur:.1f}s  <- NOT the runtime predictor; "
          f"chatterbox's rate is not the twin's")

    print("\n-- transcribing --")
    words = transcribe(wav, outdir)
    print(f"  {len(words)} timed words")

    hay = [norm(w["word"])[0] if norm(w["word"]) else "" for w in words]
    _, bad = check_anchors(args.slug, hay, "the synthetic transcript")
    check_pronunciation(script, words)

    if not args.keep_audio:
        wav.unlink(missing_ok=True)
    print(f"\nartifacts: {outdir.relative_to(ROOT)}/  "
          f"(scratch, outside public/ — no build step reads or copies this)")
    print("\nNEXT: fix anything above, THEN generate the avatar once.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
