#!/usr/bin/env python3
"""Frame-lint: automated pre-delivery QC pass over a rendered reel.

Usage:
    python3 tools/lint_frames.py <slug> [--video out/<slug>.mp4]

Reads src/beats/<slug>.json + the rendered mp4, then:
  1. Extracts a labeled still at each scene's start (+0.35s) and midpoint into
     out/<slug>-lint/ (NN-<type>-start.png / -mid.png).
  2. Builds a contact sheet (lint-sheet-*.jpg) for the vision CRITIC pass.
  3. Runs programmatic checks per still and prints a report:
       - DEAD SPACE: fraction of near-uniform dark or bright area > 30%
       - DUPLICATE: consecutive scenes whose mid-frames are near-identical
         (repetition — same treatment/clip reused back-to-back)
       - EDGE TEXT: high-contrast content hugging the left/right frame edge
         (likely cropped mid-word screenshot)
  4. Prints the manual CRITIC checklist (from SKILL.md STEP 6) with the beats
     metadata each item needs (kinetic/headline/caption overlap windows).

Flags are still hints for the critic — ALWAYS eyeball the sheet — but this now
EXITS NON-ZERO when a hard flag fires, so a bad reel cannot scroll past.

Hard (exit 1): PACING, CLIP REUSE, EDGE TEXT, DUPLICATE.
Soft (exit 0): DEAD SPACE, DOUBLE TEXT? — judgement calls, reported only.
Pass --soft to downgrade everything to advisory.

Pillow is REQUIRED. It used to be optional, which meant every pixel check
silently skipped for weeks behind a single "[SKIP] PIL not installed" line
that was never read (see STYLE-RULES 2026-08-11). A safety net you cannot
tell is switched off is worse than none.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    from PIL import Image
except ImportError:
    sys.exit(
        "FATAL: Pillow is required for frame linting but is not installed.\n"
        "       pip3 install pillow\n"
        "       (Refusing to run half-blind — the pixel checks are the point.)")


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def extract(video, t, out, label):
    # NB: this ffmpeg build has no drawtext filter — label via PIL below.
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video),
        "-frames:v", "1", "-vf", "scale=540:-1", str(out),
    ])
    if True:  # Pillow is a hard requirement — see the module docstring
        from PIL import ImageDraw, ImageFont
        img = Image.open(out).convert("RGB")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except OSError:
            font = ImageFont.load_default()
        x0, y0, x1, y1 = draw.textbbox((12, 10), label, font=font)
        draw.rectangle((x0 - 8, y0 - 6, x1 + 8, y1 + 6), fill=(0, 0, 0))
        draw.text((12, 10), label, fill=(255, 255, 255), font=font)
        img.save(out)


def grid_stats(img, cells=12):
    """Per-cell (mean, stddev) on grayscale for dead-space detection."""
    g = img.convert("L")
    w, h = g.size
    cw, ch = w // cells, h // cells
    out = []
    for r in range(cells):
        for c in range(cells):
            cell = g.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
            hist = cell.histogram()
            n = sum(hist)
            mean = sum(i * v for i, v in enumerate(hist)) / n
            var = sum(v * (i - mean) ** 2 for i, v in enumerate(hist)) / n
            out.append((mean, var ** 0.5))
    return out


def dead_space_frac(img):
    cells = grid_stats(img)
    flat_dark = sum(1 for m, s in cells if s < 6 and m < 38)
    flat_bright = sum(1 for m, s in cells if s < 6 and m > 218)
    return max(flat_dark, flat_bright) / len(cells)


def ahash(img, size=16):
    """Perceptual hash of the frame's CONTENT, not its surround.

    Framed treatments (floatcard, sourceread, any card on a gradient) share an
    identical background by design, which dominated the full-frame hash and
    made every consecutive pair of DIFFERENT clips read as a duplicate. Hashing
    the centre 72% compares what actually changes.
    """
    w, h = img.size
    m = 0.14
    img = img.crop((int(w * m), int(h * m), int(w * (1 - m)), int(h * (1 - m))))
    g = img.convert("L").resize((size, size))
    px = list(g.getdata())
    avg = sum(px) / len(px)
    return [p > avg for p in px]


def hash_dist(a, b):
    return sum(1 for x, y in zip(a, b) if x != y) / len(a)


def edge_text_score(img):
    """Detect high-frequency content hugging L/R edges (cropped text)."""
    g = img.convert("L")
    w, h = g.size
    band = 8
    score = 0.0
    for x0 in (0, w - band):
        strip = g.crop((x0, int(h * 0.2), x0 + band, int(h * 0.8)))
        px = list(strip.getdata())
        mean = sum(px) / len(px)
        var = sum((p - mean) ** 2 for p in px) / len(px)
        score = max(score, var ** 0.5)
    return score


def check_css_animation() -> list[str]:
    """Remotion does not render CSS `transition` / `animation` / keyframes.

    2026-08-14: installing the official remotion-markup skill surfaced this as
    a correctness rule, and an audit immediately found two live cases —
    SourceRead's follow-scroll was delegated to a CSS transition (so it hard
    jumped for weeks while a comment claimed it glided), and PromptCard carried
    a dead `transition: all .2s`. Animation must be driven by
    useCurrentFrame() + interpolate().
    """
    import re
    bad = []
    for f in sorted((ROOT / "src").rglob("*.tsx")):
        for n, line in enumerate(f.read_text().splitlines(), 1):
            if re.search(r"(transition|animation)\s*:\s*[\"']", line) and \
               "none" not in line:
                bad.append(f"{f.relative_to(ROOT)}:{n}  {line.strip()[:70]}")
            if "@keyframes" in line:
                bad.append(f"{f.relative_to(ROOT)}:{n}  @keyframes will not render")
    return bad


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    from_stills = "--from-stills" in sys.argv
    video = ROOT / (
        sys.argv[sys.argv.index("--video") + 1]
        if "--video" in sys.argv
        else f"out/{slug}.mp4"
    )
    beats_path = ROOT / f"src/beats/{slug}.json"
    if not video.exists() and not from_stills:
        sys.exit(f"missing video: {video}")
    if not beats_path.exists():
        sys.exit(f"missing beats: {beats_path}")

    beats = json.loads(beats_path.read_text())
    scenes = beats["scenes"]
    lint_dir = ROOT / f"out/{slug}-lint"
    lint_dir.mkdir(parents=True, exist_ok=True)
    # --from-stills: the frames were rendered straight from Remotion by
    # tools/preflight_stills.py, BEFORE any video exists. Extraction is the
    # only step that needs a finished mp4; every check below works on pixels.
    # Wiping the directory here would delete exactly what we were handed.
    if not from_stills:
        for old in lint_dir.glob("*.png"):
            old.unlink()

    # -- 1. extract labeled stills ------------------------------------------
    stills = []  # (idx, type, phase, path, t)
    cursor = 0.0
    for i, s in enumerate(scenes):
        dur = s["durationSec"]
        marks = [("start", cursor + min(0.35, dur * 0.3)),
                 ("mid", cursor + dur / 2)]
        for phase, t in marks:
            label = f"{i:02d} {s['type']} {phase} @{t:.1f}s"
            p = lint_dir / f"{i:02d}-{s['type']}-{phase}.png"
            if from_stills:
                if not p.exists():
                    continue          # preflight samples mids only
            else:
                extract(video, t, p, label)
            stills.append((i, s["type"], phase, p, t))
        cursor += dur

    # contact sheets (mids only, 4 per row)
    mids = [p for (_, _, ph, p, _) in stills if ph == "mid"]
    for si in range(0, len(mids), 12):
        chunk = mids[si:si + 12]
        sheet = lint_dir / f"lint-sheet-{si // 12}.jpg"
        inputs = []
        for p in chunk:
            inputs += ["-i", str(p)]
        n = len(chunk)
        cols = min(4, n)
        rows = -(-n // cols)
        run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
             f"concat=n={n}:v=1:a=0,tile={cols}x{rows}", "-frames:v", "1",
             str(sheet)])

    # -- 2. programmatic checks ---------------------------------------------
    flags = []
    imgs = {}
    for (i, typ, phase, p, t) in stills:
        if phase != "mid":
            continue
        img = Image.open(p)
        imgs[i] = img
        # Threshold is type-aware. A typographic card on cream is ~65-80%
        # "flat" BY DESIGN, so a flat 30% bar fires on every one of them and
        # the flag becomes noise nobody reads — the same way [SKIP] was
        # ignored for weeks. Footage and small-asset-on-field stay strict;
        # designed cards get room; the HOOK is strictest of all because
        # "blank space in the first 2s is a hard fail" (STYLE-RULES 2026-08-04).
        DESIGNED = {"wordcascade", "typecard", "statcard", "chart", "specsheet",
                    "logoassemble", "logobeat", "floatcard", "checklist", "sourceread",
                    "categorygrid", "timeline", "promptcard", "settingspane",
                    "priceladder"}
        frac = dead_space_frac(img)
        limit = 0.70 if typ in DESIGNED else 0.30
        if i == 0:
            limit = 0.55          # the hook may never read as an empty field
        if frac > limit:
            sev = "HOOK DEAD SPACE" if i == 0 else "DEAD SPACE"
            flags.append(
                f"[{sev}] scene {i:02d} ({typ}): {frac:.0%} of frame is "
                f"flat/empty (limit {limit:.0%}) — fill the empty band with "
                "large type or a moving asset")
        if typ in ("receipt", "floatcard") and edge_text_score(img) > 34:
            flags.append(
                f"[EDGE TEXT] scene {i:02d} ({typ}): busy pixels at frame "
                "edge — screenshot likely cropped mid-word")
    hashes = {i: ahash(img) for i, img in imgs.items()}
    for i in sorted(hashes)[1:]:
        if i - 1 in hashes and hash_dist(hashes[i - 1], hashes[i]) < 0.08:
            a, b = scenes[i - 1]["type"], scenes[i]["type"]
            flags.append(
                f"[DUPLICATE] scenes {i-1:02d}({a}) → {i:02d}({b}) look "
                "near-identical — repeated treatment/clip back-to-back")

    # HEAD DRIFT (2026-08-13, made-by-google-26): a cut clip's first second
    # can be a DIFFERENT SHOT than the one scouted (keynote clips open on the
    # stage presenters before cutting to the product film). Five clips leaked
    # this way in one reel and only the contact sheet caught it. If a motion
    # scene's start frame diverges sharply from its mid frame, the head is
    # suspect — check it, or set `from` on the scene. Soft hint: real camera
    # motion also diverges, so a human decides.
    starts = {i: Image.open(p) for (i, typ, phase, p, t) in stills
              if phase == "start" and typ in ("footage", "floatcard", "split")}
    for i, simg in starts.items():
        if i in imgs and hash_dist(ahash(simg), ahash(imgs[i])) > 0.42:
            flags.append(
                f"[HEAD DRIFT] scene {i:02d} ({scenes[i]['type']}): first "
                "frame differs sharply from mid frame — the clip head may be "
                "a leaked shot from before the cut; verify or trim with "
                "`from`")

    # PACING (universal rule 2026-07-31). Thresholds come from reel_gates so
    # there is exactly ONE definition — the linter and the build gates
    # disagreeing is how a rule quietly becomes optional.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from reel_gates import DUR_MAX, HOOK_MAX, _dur_class
    for i, sc in enumerate(scenes):
        d = sc["durationSec"]
        if i == 0 and d > HOOK_MAX:
            flags.append(
                f"[PACING] scene 00 ({sc['type']}): hook layout held {d:.1f}s"
                f" — HARD LIMIT {HOOK_MAX}s (user rule, blocking)")
            continue
        cls = _dur_class(sc)
        if d > DUR_MAX[cls]:
            flags.append(
                f"[PACING] scene {i:02d} ({sc['type']}, {cls}): held layout "
                f"{d:.1f}s > {DUR_MAX[cls]}s — split across visuals or cut to "
                "footage")

    # CLIP REUSE (universal rule 2026-08-01): no source clip may carry more
    # than one footage beat — reusing the same shot reads as "limited footage".
    from collections import Counter
    used = Counter()
    for sc in scenes:
        src = str(sc.get("src") or "")
        if sc.get("type") == "footage" and src and "avatar-master" not in src:
            used[src] += 1
    for src, n in used.items():
        if n > 1:
            flags.append(
                f"[CLIP REUSE] {src.split('/')[-1]} used in {n} beats — every "
                "footage beat needs its OWN shot (blocking)")

    # caption-overlap advisory: display-type scenes that force chips ON
    for i, s in enumerate(scenes):
        display = s["type"] in ("typecard", "wordcascade") or "kinetic" in s
        if display and s.get("hideCaptions") is False:
            flags.append(
                f"[DOUBLE TEXT?] scene {i:02d} ({s['type']}) has display type "
                "but hideCaptions:false — verify chips don't duplicate it")

    # -- 3. report -----------------------------------------------------------
    print(f"\n=== frame-lint: {slug} — {len(scenes)} scenes ===")
    print(f"stills + sheets: {lint_dir}/")
    if flags:
        print("\nAUTO FLAGS (hints, verify by eye):")
        for f in flags:
            print("  " + f)
    else:
        print("\nno auto flags.")
    print("""
CRITIC CHECKLIST (review the lint sheets against the beat map):
  1. script-visual match: does each frame show what the VO claims?
  2. ONE TEXT SYSTEM: no karaoke chip while display type speaks the words
  3. no text collisions (headline vs card vs chip), captions off the face
  4. receipts: highlight framed big, box AROUND the data (never covering it)
  5. no content cropped mid-word at frame edges; screenshots card-framed
  6. every number carries units/labels; credits present; no app chrome
  7. display type legible on its actual backdrop (frame AT landing moment)
  8. dead space <30% of frame; no flat-black surrounds around small assets
  9. hook frame passes the sound-off test (names the subject visually)""")

    # -- 4. verdict ----------------------------------------------------------
    HARD = ("[PACING]", "[CLIP REUSE]", "[EDGE TEXT]", "[DUPLICATE]",
            "[HOOK DEAD SPACE]")
    hard = [f for f in flags if f.startswith(HARD)]
    if hard and "--soft" not in sys.argv:
        print(f"\nFRAME-LINT FAILED — {len(hard)} blocking flag(s) above.")
        print("Fix the plan and rebuild, or re-run with --soft to override "
              "deliberately (and say so when you hand the reel over).")
        sys.exit(1)
    if hard:
        print(f"\n{len(hard)} blocking flag(s) DOWNGRADED by --soft.")
    print("\nframe-lint: no blocking flags.")


if __name__ == "__main__":
    main()
