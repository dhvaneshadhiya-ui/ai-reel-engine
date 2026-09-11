#!/usr/bin/env python3
"""Set each SFX gain from the file's MEASURED peak, so every cue lands equally loud.

THE PROBLEM, MEASURED 2026-08-18
--------------------------------
The user said sound effects were "hardly being used and if used, hardly
noticeable". Both halves are true, and there is a third fault underneath:

  USED     6-9 cues per reel, about one per 10 seconds
  QUIET    effective peaks average -22.4 dBFS against a voice peaking near -1.2
  UNEVEN   a 9 dB spread BETWEEN cues, because a flat ~0.14 gain is applied to
           files whose native peaks run from -2.1 to -12.4 dBFS

The third is the one nobody would have guessed. "vol: 0.14" reads like a level,
but it is a MULTIPLIER — so the same number on a hot file and a quiet file
produces two very different sounds. Magic Reveal lands 9 dB below Camera Shutter
while both are nominally set to the same volume.

Gain is therefore derived, not typed: measure the file's peak, then solve for the
gain that puts it at the target. Same arithmetic every cue, so a designer picks
WHICH sound and WHERE, never how loud.

    python3 tools/calibrate_sfx.py                 # report, every sheet
    python3 tools/calibrate_sfx.py grok-bot        # one sheet
    python3 tools/calibrate_sfx.py --write         # rewrite every sheet's vols
    python3 tools/calibrate_sfx.py --target -14    # a quieter mix

TARGET IS A DEFAULT, NOT A RULE. Under the constitution only the three standing
rules are law; how loud a whoosh should be is craft. -12 dBFS puts a transient
about 11 dB under the voice's peak: present, not fighting. Move it if the mix
wants otherwise.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel_gates import FORMATS, DEFAULT_FORMAT, SFX_PEAKS_FILE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = -12.0     # dBFS, effective peak of a punctuation cue
GAIN_MAX = 1.0             # never amplify past the file itself
GAIN_MIN = 0.02


def peak_dbfs(f: Path) -> float | None:
    """True peak in dBFS. Used instead of integrated LUFS ON PURPOSE.

    Most cues are 0.18-0.37s. EBU R128 integrated loudness is gated in 400ms
    blocks, so a short click has too few blocks and reports -70.0 — the floor.
    Measuring these with LUFS says 'silent' about a file that peaks at -2.1 dBFS,
    which is how the first pass at this analysis nearly reported three healthy
    cues as dead.
    """
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f),
                        "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"max_volume:\s*(-?[\d.]+)", r.stderr)
    return float(m.group(1)) if m else None


def main() -> None:
    write = "--write" in sys.argv
    # The target is PER FORMAT, read from the same profile G08 checks
    # against — `utility` mixes its cues quieter than `editorial` does, and
    # calibrating every sheet to one number would put the top5 sheets
    # permanently outside their own gate. An explicit --target overrides.
    target = None
    if "--target" in sys.argv:
        i = sys.argv.index("--target")
        if i + 1 < len(sys.argv):
            target = float(sys.argv[i + 1])
    forced = target

    # Optional slug filter. Added because another session was editing a sheet
    # in the same working tree: rewriting it would have collided with work in
    # progress, and reverting afterwards would have destroyed it.
    only = {a for a in sys.argv[1:] if not a.startswith("--")
            and not a.lstrip("-").replace(".", "").isdigit()}
    sheets = [p for p in sorted((ROOT / "src/beats").glob("*.json"))
              if not only or p.stem in only or p.stem.replace("-nomusic", "") in only]
    peaks: dict[str, float] = {}
    changed_files = 0
    rows: list[tuple] = []

    for p in sheets:
        doc = json.loads(p.read_text())
        fmt = FORMATS.get(doc.get("format") or DEFAULT_FORMAT,
                          FORMATS[DEFAULT_FORMAT])
        target = forced if forced is not None else fmt["sfx_peak"]
        touched = False
        for sc in doc.get("scenes", []):
            for cue in (sc.get("sfx") or []):
                src = str(cue.get("src") or "")
                if not src:
                    continue
                if src not in peaks:
                    f = ROOT / "public" / src
                    peaks[src] = peak_dbfs(f) if f.exists() else None
                pk = peaks[src]
                if pk is None:
                    continue
                old = float(cue.get("vol", 0))
                want = round(min(GAIN_MAX, max(GAIN_MIN,
                                               10 ** ((target - pk) / 20))), 3)
                rows.append((p.stem, src, pk, old, want, target))
                if abs(want - old) > 0.005:
                    touched = True
                    if write:
                        cue["vol"] = want
        if write and touched:
            p.write_text(json.dumps(doc, indent=2) + "\n")
            changed_files += 1

    if not rows:
        sys.exit("no sfx cues found")

    seen: dict[str, tuple] = {}
    for _slug, src, pk, old, want, _t in rows:
        seen.setdefault(src, (pk, old, want))
    tg = ", ".join(f"{t:.1f}" for t in sorted({r[5] for r in rows}))
    print(f"\n  target {tg} dBFS effective peak (per format)\n")
    print(f"  {'cue':34}{'peak':>8}{'was':>7}{'now':>7}{'change':>9}")
    for src, (pk, old, want) in sorted(seen.items()):
        db = 20 * math.log10(want / old) if old > 0 else 0
        print(f"  {src[-32:]:34}{pk:>8.1f}{old:>7.2f}{want:>7.2f}{db:>8.1f}dB")

    befores = [pk + 20 * math.log10(o) for _, (pk, o, _w) in seen.items() if o > 0]
    afters = [pk + 20 * math.log10(w) for _, (pk, _o, w) in seen.items() if w > 0]
    print(f"\n  effective peak BEFORE: {min(befores):.1f} to {max(befores):.1f} "
          f"dBFS  (spread {max(befores)-min(befores):.0f} dB)")
    print(f"  effective peak AFTER:  {min(afters):.1f} to {max(afters):.1f} "
          f"dBFS  (spread {max(afters)-min(afters):.0f} dB)")
    print("\n  A cue quieter than its target after calibration is a file whose own"
          "\n  peak is already below it — the gain is capped at 1.0 and it cannot"
          "\n  be made louder without distorting. Replace the sound, do not push it.")

    # Every catalogue file gets a cached peak, not only the ones a sheet uses
    # today — otherwise a new cue has no number until its first reel.
    from sfx_library import CATALOGUE  # noqa: E402
    for src in CATALOGUE:
        if src not in peaks and (ROOT / "public" / src).exists():
            peaks[src] = peak_dbfs(ROOT / "public" / src)

    # G08 cannot shell out to ffmpeg on every run, so the peaks live in a
    # committed sidecar. `bytes` is the staleness check: swap the file and the
    # cached peak stops applying, which the gate says out loud instead of
    # silently grading the new sound against the old one's number.
    #
    # Written on a plain report run too, not only under --write: measuring is
    # read-only, and rewriting 27 shipped beat sheets just to refresh a cache
    # would be the tail wagging the dog. MERGED rather than replaced, because
    # the cache is keyed by FILE and a single-slug run only sees that reel's
    # cues — replacing would delete every peak it did not happen to touch.
    cached = {}
    if SFX_PEAKS_FILE.exists():
        try:
            cached = json.loads(SFX_PEAKS_FILE.read_text()).get("peaks", {})
        except Exception:                                       # noqa: BLE001
            cached = {}
    cached.update({
        src: {"peak": pk,
              "bytes": (ROOT / "public" / src).stat().st_size}
        for src, pk in peaks.items()
        if pk is not None and (ROOT / "public" / src).exists()})
    SFX_PEAKS_FILE.write_text(json.dumps({
            "_": "measured peaks, dBFS — written by tools/calibrate_sfx.py, "
             "read by G08. Do not hand-edit.",
        "peaks": dict(sorted(cached.items())),
    }, indent=2) + "\n")
    print(f"\n  wrote {SFX_PEAKS_FILE.name} ({len(cached)} cues)")
    if write:
        print(f"  rewrote {changed_files} beat sheet(s)")
    else:
        print("\n  (--write to apply)")


if __name__ == "__main__":
    main()
