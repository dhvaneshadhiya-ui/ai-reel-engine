#!/usr/bin/env python3
"""Take dead air out of a reel without touching how fast the creator talks.

WHY THIS IS NOT A SPEED CONTROL (2026-08-18)
--------------------------------------------
Asked for: "creator's talking speed sometimes feels too slow... if video is
going to be more than 1 minute, creator's speed is little increased (however,
he sounds clear)".

Measured on iphone-fold-ultra before building anything:

    overall rate         2.30 words/sec   (this is what "slow" feels like)
    ARTICULATION rate    2.77 words/sec   (how fast he talks when talking)
    inter-word silence   13.4s of 79.1s   — 17% of the reel, across 29 gaps

tools/voice_clone.py records the natural range of this voice, measured off five
real HeyGen masters: 2.35-2.75 words/sec. He is already articulating at 2.77 —
at the TOP of the range, faster than any of the five. There is no slack in his
delivery to take. Speeding the audio would push him past the fastest he has ever
naturally spoken, which is precisely the thing the request rules out.

The reel feels slow because a sixth of it is silence. So this cuts the silence
and leaves the voice alone.

WHAT IT WILL NOT CUT
--------------------
A pause that happens while the PRESENTER IS ON SCREEN. Cutting there is a jump
cut on a talking head — his hands teleport. On this reel that protects 7 of 23
gaps and costs 1.6s, which is the right trade: 3.5s of invisible tightening
beats 5.1s with seven visible glitches.

Video and audio are cut TOGETHER, from the one master, so lipsync is preserved
exactly. Every time in the beat sheet — scene durations, avatar `from` offsets,
SFX cues, music envelope points, caption word timings — is remapped through the
same monotone function, so nothing drifts out of sync.

    python3 tools/pace_reel.py <slug>            # what it would reclaim
    python3 tools/pace_reel.py <slug> --write    # cut and remap

RUNTIME IS THE INPUT, not a fixed cap. Under 60s a reel has room to breathe and
the cap stays loose; over 60s attention is the scarce thing and it tightens.
That is the "based on the topic length" judgement, expressed as the one number
it actually depends on.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def cap_for(runtime: float) -> float:
    """Longest pause to keep, in seconds, from the reel's runtime.

    Not a cliff at 60s — a cliff would make a 59s and a 61s reel feel like
    different shows. It ramps: 0.42s of air at 45s down to 0.24s at 100s.
    """
    if runtime <= 45:
        return 0.42
    if runtime >= 100:
        return 0.24
    return round(0.42 - (runtime - 45) * (0.42 - 0.24) / 55, 3)


def load_words(slug: str) -> list[dict]:
    p = ROOT / f"public/assets/{slug}/vo.json"
    if not p.exists():
        sys.exit(f"no word timings at {p}")
    d = json.loads(p.read_text())
    return d.get("words") or [w for s in d.get("segments", []) for w in s.get("words", [])]


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    slug, write = args[0], "--write" in sys.argv

    bp = ROOT / f"src/beats/{slug}.json"
    doc = json.loads(bp.read_text())
    scenes = doc["scenes"]
    words = load_words(slug)

    runtime = sum(s["durationSec"] for s in scenes)
    CAP = cap_for(runtime)

    # --- where the presenter is on screen -----------------------------------
    avatar: list[tuple[float, float]] = []
    c = 0.0
    for s in scenes:
        src = str(s.get("src") or s.get("bottomSrc") or s.get("topSrc") or "")
        if "avatar" in src.lower():
            avatar.append((c, c + s["durationSec"]))
        c += s["durationSec"]

    def on_face(a: float, b: float) -> bool:
        return any(a < e and b > st for st, e in avatar)

    # --- choose the removals -------------------------------------------------
    removes: list[tuple[float, float]] = []
    protected = 0.0
    for i in range(len(words) - 1):
        a, b = float(words[i]["end"]), float(words[i + 1]["start"])
        if b - a <= CAP:
            continue
        if on_face(a, b):
            protected += (b - a) - CAP
            continue
        # keep CAP of air, split either side so neither word is clipped
        pad = CAP / 2
        removes.append((a + pad, b - pad))
    removes.sort()
    reclaimed = sum(b - a for a, b in removes)

    articulation = len(words) / (
        (float(words[-1]["end"]) - float(words[0]["start"]))
        - sum(max(0.0, float(words[i + 1]["start"]) - float(words[i]["end"]))
              for i in range(len(words) - 1)))

    print(f"\n  {slug}   runtime {runtime:.1f}s   pause cap {CAP:.2f}s "
          f"(from runtime, not typed)")
    print(f"  articulation {articulation:.2f} words/sec — the voice's own "
          f"measured range is 2.35-2.75,")
    print(f"  so his DELIVERY is not the problem and is left untouched.")
    print(f"\n  {len(removes)} cut(s) reclaim {reclaimed:.1f}s "
          f"-> {runtime - reclaimed:.1f}s")
    print(f"  {protected:.1f}s left in place to avoid jump-cutting the presenter")
    if not removes:
        print("\n  nothing to reclaim.\n")
        return
    if not write:
        print("\n  (--write to cut the master and remap the sheet)\n")
        return

    # --- the monotone time map ----------------------------------------------
    def remap(t: float) -> float:
        return round(t - sum(min(b, t) - a for a, b in removes if a < t), 3)

    keeps: list[tuple[float, float]] = []
    cur = 0.0
    for a, b in removes:
        if a > cur:
            keeps.append((cur, a))
        cur = b
    keeps.append((cur, runtime + 2.0))

    # --- cut the master, video and audio together ---------------------------
    master = ROOT / "public" / str(doc["audio"])
    if not master.exists():
        sys.exit(f"avatar master missing: {master}")
    # Every time in the sheet is about to change, so keep a copy — but NOT in
    # src/beats/. scripts/register_beats.py registers every *.json in that
    # directory as a composition, so a backup there is a SECOND composition
    # claiming the same id, and the render dies at step one with "duplicate
    # composition id". Which is exactly what happened on the first run of this
    # tool: the pacing was correct, the sheet was correct, and nothing rendered.
    backups = ROOT / "out/pace-backup"
    backups.mkdir(parents=True, exist_ok=True)
    sheet_backup = backups / f"{slug}.orig.json"
    if not sheet_backup.exists():
        sheet_backup.write_text(bp.read_text())
        print(f"  kept the original sheet as out/pace-backup/{sheet_backup.name}")
    backup = master.with_suffix(".orig.mp4")
    if not backup.exists():
        shutil.copy2(master, backup)
        print(f"  kept the original as {backup.name}")

    sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keeps)
    tmp = master.with_suffix(".paced.mp4")
    cmd = ["ffmpeg", "-y", "-i", str(backup),
           "-vf", f"select='{sel}',setpts=N/FRAME_RATE/TB",
           "-af", f"aselect='{sel}',asetpts=N/SR/TB",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17",
           "-c:a", "aac", "-b:a", "192k", str(tmp)]
    print("  + " + " ".join(cmd[:6]) + " ...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])
    tmp.replace(master)

    # --- remap every time in the sheet --------------------------------------
    c = 0.0
    for s in scenes:
        start, end = c, c + s["durationSec"]
        c = end
        ns, ne = remap(start), remap(end)
        # SCENE-RELATIVE TIMES: convert to absolute, map, convert back.
        #
        # `sfx.at` was handled from the start and `headline.lines[].at` was NOT
        # — found 2026-08-18 when sync_impacts.py, re-run after a pace pass,
        # moved two cues that were already locked to their headline. The cues
        # had moved with the cut; the headline had not, so a sound and the
        # picture it accents drifted apart, and on a scene that shortened by
        # more than the line's `at` the headline would land after its own scene
        # had ended. Anything measured from the start of a scene has to travel
        # with that scene.
        for cue in s.get("sfx") or []:
            abs_at = start + float(cue.get("at", 0))
            cue["at"] = round(max(0.0, remap(abs_at) - ns), 3)
        hl = s.get("headline")
        if isinstance(hl, dict):
            for ln in hl.get("lines") or []:
                if "at" in ln:
                    ln["at"] = round(max(0.0, remap(start + float(ln["at"])) - ns), 3)
            if hl.get("impacts"):
                hl["impacts"] = [round(max(0.0, remap(start + float(v)) - ns), 3)
                                 for v in hl["impacts"]]
        if isinstance(s.get("kinetic"), dict) and "at" in s["kinetic"]:
            k = s["kinetic"]
            k["at"] = round(max(0.0, remap(start + float(k["at"])) - ns), 3)
        # `from` MEANS TWO DIFFERENT THINGS and only one of them may be
        # remapped. On an avatar scene it is a position on the master timeline
        # — the same timeline being cut — so it must move. On a b-roll clip it
        # is an offset into THAT file, which this tool never touches; remapping
        # it would silently seek to the wrong moment of someone else's footage.
        # Checked per scene rather than assumed: on this sheet all eight happen
        # to be avatar scenes, which is exactly how a bug like that survives.
        src = str(s.get("src") or "")
        if "from" in s:
            if "avatar" in src.lower():
                s["from"] = remap(float(s["from"]))
            else:
                print(f"     left `from` alone on a b-roll scene "
                      f"({Path(src).name}) — it indexes that clip, not the reel")
        if "bottomFrom" in s and "avatar" in str(s.get("bottomSrc", "")).lower():
            s["bottomFrom"] = remap(float(s["bottomFrom"]))
        if "topFrom" in s and "avatar" in str(s.get("topSrc", "")).lower():
            s["topFrom"] = remap(float(s["topFrom"]))
        s["durationSec"] = round(max(0.2, ne - ns), 3)

    for w in doc.get("captions") or []:
        w["start"], w["end"] = remap(float(w["start"])), remap(float(w["end"]))
        for ww in w.get("words") or []:
            ww["t"] = remap(float(ww["t"]))
    for pt in (doc.get("music") or {}).get("points") or []:
        pt["t"] = remap(float(pt["t"]))

    # RECONCILE AGAINST THE FILE, don't trust the arithmetic.
    #
    # ffmpeg's `select` snaps every cut to a frame boundary, so the media loses
    # a slightly different amount than the sheet's float maths says it should —
    # 16 cuts here removed 3.33s of video while the sheet removed 3.41s. That
    # 0.08s, on top of the 0.19s of trailing silence the sheet already carried,
    # pushed the total past validate_job.py's 0.20s tolerance and killed the
    # render. The first version of this tool computed the timings and never
    # asked the file what it had actually become.
    #
    # The slack the sheet carried BEFORE is preserved rather than zeroed: it is
    # trailing room after the last word, and removing it would clip the outro.
    def probe(p: Path) -> float:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(p)], capture_output=True, text=True)
        return float(out.stdout.strip())

    old_slack = probe(backup) - runtime
    target = probe(master) - old_slack
    total = sum(s["durationSec"] for s in scenes)
    drift = round(target - total, 3)
    if abs(drift) > 0.005:
        scenes[-1]["durationSec"] = round(scenes[-1]["durationSec"] + drift, 3)
        print(f"  reconciled {drift:+.3f}s of frame-rounding into the last scene "
              f"(sheet {total:.2f}s -> {target:.2f}s, master {probe(master):.2f}s)")

    bp.write_text(json.dumps(doc, indent=2) + "\n")

    vp = ROOT / f"public/assets/{slug}/vo.json"
    vd = json.loads(vp.read_text())
    for w in (vd.get("words") or []):
        w["start"], w["end"] = remap(float(w["start"])), remap(float(w["end"]))
    for seg in (vd.get("segments") or []):
        seg["start"], seg["end"] = remap(float(seg["start"])), remap(float(seg["end"]))
        for w in seg.get("words") or []:
            w["start"], w["end"] = remap(float(w["start"])), remap(float(w["end"]))
    vp.write_text(json.dumps(vd))

    print(f"\n  cut the master, remapped {len(scenes)} scenes, "
          f"{len(doc.get('captions') or [])} caption spans and the music curve")
    print(f"  {runtime:.1f}s -> {sum(s['durationSec'] for s in scenes):.1f}s\n")


if __name__ == "__main__":
    main()
