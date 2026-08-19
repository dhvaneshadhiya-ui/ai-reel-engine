#!/usr/bin/env python3
"""Does what the beat sheet DECLARES actually reach the frame?

WHY THIS EXISTS
---------------
Four separate defects on 2026-08-18, all the same shape — a check that reads the
beat sheet while the thing it protects lives in the picture:

  * captions rendered white on white footage; the sheet was silent and correct
  * five typecards declared `"credit": "MacRumors"` and drew nothing. G14
    (RIGHTS, blocking) passed every render, because the sheet had the credit
  * the `typecard` scene type never declared `credit` at all, so the field sat
    in JSON that TypeScript never type-checked and no component ever read
  * G05 held a typed character budget calibrated for the old display face; the
    face changed, the budget silently went wrong, and six headlines overflow
    the frame with a completely clean build

Every one passed its gate. None of them was a bad rule — they were rules
looking in the wrong place.

    python3 tools/check_frame_contract.py <slug>          # both layers
    python3 tools/check_frame_contract.py <slug> --static # no stills needed
    python3 tools/check_frame_contract.py --all           # contract layer, whole library

ADVICE, ALL OF IT. Per RULES.md section 0 this cannot become blocking without
passing the four-part test, and it does not: layer A infers what a component
reads by parsing source, which is a heuristic; layer B measures ink in a band,
which has a threshold somebody chose. Both are good enough to point at a real
bug and not good enough to be law. What it replaces is nobody looking at all.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / "src/components"
REEL = ROOT / "src/Reel.tsx"

# Fields the RENDERER consumes before a component ever sees the scene, so a
# component not reading them is correct, not a bug.
RENDERER_OWNED = {
    "type", "durationSec", "sfx", "headline", "sprites", "burst",
    "captionBottom", "captionTheme", "hideCaptions", "covers", "assetId",
    "product", "note", "impacts",
}

# Fields consumed by TOOLING rather than by the renderer. A component not
# reading these is correct. Each one names its reader, so the allowlist cannot
# become a place to silence a real finding: if the named tool stops reading it,
# the field is dead and belongs in neither list.
TOOL_OWNED = {
    "claimId": "scripts/compile_shot_plan.py",
}


def scene_component_map() -> dict[str, tuple[str, str]]:
    """`case "typecard": return <TypeCard ...>` -> {"typecard": (comp, form)}.

    THE CALL FORM MATTERS, and missing it made the first version of this tool
    report seven findings and get seven of them wrong. Two shapes are in use:

        <FootageScene scene={scene} />   the component reads `scene.foo`
        <ChartScene {...scene} />        the scene is SPREAD INTO PROPS, and the
                                         component destructures `{ title, items }`
                                         in its own signature — it never writes
                                         `scene.` at all

    Looking only for `scene.foo` marks every prop of every spread component as
    unread. A checker that is wrong seven times out of seven is worse than no
    checker: it gets ignored, and then it is ignored on the day it is right.
    """
    src = REEL.read_text()
    out = {}
    for m in re.finditer(
            r'case\s+"([a-z0-9]+)":\s*\n\s*return\s*<([A-Za-z0-9_]+)([^/>]*)', src):
        form = "spread" if "...scene" in m.group(3) else "prop"
        out[m.group(1)] = (m.group(2), form)
    return out


def fields_read_by(component: str, form: str = "prop") -> set[str] | None:
    """Fields a component reads off its scene prop.

    Deliberately generous: `scene.x`, destructured `const { x } = scene`, and
    `scene["x"]`. A false "unread" is worse than a miss here, because the point
    is to be believed.
    """
    for cand in (COMPONENTS / f"{component}.tsx", ROOT / "src" / f"{component}.tsx"):
        if cand.exists():
            src = cand.read_text()
            break
    else:
        # components can also live inside a barrel file (e.g. OssAlt.tsx)
        hits = [p for p in COMPONENTS.glob("*.tsx")
                if re.search(rf"export const {component}\b", p.read_text())]
        if not hits:
            return None
        src = hits[0].read_text()

    if form == "spread":
        # the scene became the prop object; read the component's own
        # destructuring signature instead
        m = re.search(rf"export const {component}[^=]*=\s*\(\s*\{{([^}}]*)\}}", src)
        if not m:
            return {"*"}          # cannot parse it — say nothing rather than lie
        names = set()
        for part in m.group(1).split(","):
            n = part.split(":")[0].split("=")[0].strip()
            if n and not n.startswith("."):
                names.add(n)
        return names

    read = set(re.findall(r"scene\.([A-Za-z_][A-Za-z0-9_]*)", src))
    read |= set(re.findall(r'scene\[\s*"([^"]+)"', src))
    for m in re.finditer(r"const\s*\{([^}]*)\}\s*=\s*scene\b", src):
        for part in m.group(1).split(","):
            name = part.split(":")[0].split("=")[0].strip()
            if name:
                read.add(name)
    # a component that spreads the whole scene consumes everything
    if re.search(r"\{\s*\.\.\.scene\s*\}", src):
        read.add("*")
    return read


def static_layer(sheets: list[Path]) -> list[str]:
    """Fields set in beat sheets that the drawing component never reads."""
    mapping = scene_component_map()
    declared: dict[str, dict[str, set[str]]] = {}
    for p in sheets:
        try:
            doc = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        for sc in doc.get("scenes", []):
            typ = sc.get("type")
            if not typ:
                continue
            for k in sc:
                declared.setdefault(typ, {}).setdefault(k, set()).add(p.stem)

    findings = []
    for typ in sorted(declared):
        entry = mapping.get(typ)
        comp, form = entry if entry else (None, "prop")
        if not comp:
            findings.append(f"  scene type {typ!r} has no component in Reel.tsx")
            continue
        read = fields_read_by(comp, form)
        if read is None:
            findings.append(f"  {typ}: component {comp} not found on disk")
            continue
        if "*" in read:
            continue
        for field, slugs in sorted(declared[typ].items()):
            if field in RENDERER_OWNED or field in TOOL_OWNED or field in read:
                continue
            where = ", ".join(sorted(slugs)[:3])
            more = f" +{len(slugs) - 3}" if len(slugs) > 3 else ""
            findings.append(
                f"  {typ:14} declares {field!r} in {where}{more} — "
                f"{comp}.tsx never reads it, so it reaches no frame")
    return findings


# --- layer B: is the declared thing actually drawn? -------------------------

def ink_fraction(img, x0f, y0f, x1f, y1f) -> float:
    """Fraction of sampled pixels that differ sharply from their neighbour.

    Text is high-frequency: a band containing type has many pixels unlike the
    pixel beside them. A flat card, a blurred backdrop or an empty margin does
    not. This is the same idea lint_frames.py uses for edge ink, scoped to a band.
    """
    W, H = img.size
    px = img.load()
    # CLAMP. The credit search walks bands down to y 0.98 + 0.03, which runs off
    # the bottom of the image and threw IndexError on the first real slug.
    x0, x1 = max(0, int(W * x0f)), min(W, int(W * x1f))
    y0, y1 = max(0, int(H * y0f)), min(H, int(H * y1f))
    if x1 <= x0 or y1 <= y0:
        return 0.0
    hits = n = 0
    for y in range(y0, max(y1, y0 + 2), 2):
        prev = None
        for x in range(x0, max(x1, x0 + 2), 2):
            r, g, b = px[x, y][:3]
            v = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if prev is not None and abs(v - prev) > 42:
                hits += 1
            prev = v
            n += 1
    return hits / n if n else 0.0


def pixel_layer(slug: str) -> list[str]:
    try:
        from PIL import Image
    except ImportError:
        return ["  (Pillow not installed — pixel layer skipped)"]

    lint = ROOT / f"out/{slug}-lint"
    if not lint.exists():
        return [f"  no stills at out/{slug}-lint — render once, then re-run"]

    doc = json.loads((ROOT / f"src/beats/{slug}.json").read_text())
    scenes = doc.get("scenes", [])
    findings = []

    # A STILL IS A PHOTOGRAPH OF A PAST RENDER. If the components have changed
    # since, every pixel finding describes a video that no longer exists —
    # which is how made-by-google-26's Aug 13 stills reported credits that the
    # Aug 17 code already moved. Say so first, so nobody debugs a ghost.
    newest_src = max((p.stat().st_mtime for p in COMPONENTS.glob("*.tsx")),
                     default=0)
    oldest_still = min((p.stat().st_mtime for p in lint.glob("*-mid.png")),
                       default=0)
    if oldest_still and newest_src > oldest_still:
        import datetime as _dt
        findings.append(
            f"  STALE: these stills are from "
            f"{_dt.date.fromtimestamp(oldest_still)} and components changed "
            f"{_dt.date.fromtimestamp(newest_src)} — findings below describe "
            f"the OLD render. Re-render this slug before acting on them.")
    for i, sc in enumerate(scenes):
        stills = list(lint.glob(f"{i:02d}-*-mid.png"))
        if not stills:
            continue
        img = Image.open(stills[0]).convert("RGB")

        # 1. A DECLARED CREDIT MUST BE VISIBLE. This is the typecard bug: the
        #    sheet said MacRumors, the frame said nothing, G14 was satisfied.
        if sc.get("credit"):
            # SEARCH THE WHOLE LOWER FRAME, don't just ask "is it in the lane".
            # The first version sampled only y 0.755-0.815 and reported four
            # credits on made-by-google-26 as "nothing is drawn there". They ARE
            # drawn — at y 0.83, the pre-2026-08-17 position. The finding was
            # real and the sentence was false, which is the worse of the two
            # failures: a reader checks one frame, sees the credit, and stops
            # believing the tool.
            #
            # So it reports WHERE it found the credit, and judges that against
            # the measured platform furniture rather than against our lane.
            # FIND IT BY ITS SIGNATURE, not by where we expect it.
            #
            # A fixed band was wrong twice. Starting at y 0.755 missed the
            # pre-fix position (y 0.83) and called four drawn credits missing;
            # starting at y 0.70 missed FloatingCard, which anchors its credit
            # to the CARD rather than the frame and puts it at y 0.64 on a wide
            # card. Both times the tool was confidently wrong about a component
            # doing its job.
            #
            # A credit line is a LOCAL SPIKE of ink in a narrow horizontal strip
            # on the left: a few hundred pixels of type with clear ground above
            # and below. That signature holds wherever a component decides to
            # put it, and it survives busy footage, where every band has ink but
            # only one band has markedly more than its neighbours.
            bands = [(0.45 + k * 0.02, ink_fraction(img, 0.04, 0.45 + k * 0.02,
                                                    0.55, 0.45 + k * 0.02 + 0.028))
                     for k in range(27)]
            vals = sorted(v for _, v in bands)
            median = vals[len(vals) // 2]
            peak_y, peak = max(bands, key=lambda b: b[1])
            found_at = (peak_y if peak >= 0.012 and peak >= max(3 * median, 0.012)
                        else None)
            if found_at is None:
                findings.append(
                    f"  scene {i:02d} ({sc['type']}) declares credit "
                    f"{sc['credit']!r} and nothing is drawn anywhere in the "
                    f"lower frame — the component is not rendering it")
            elif found_at >= 0.82:
                findings.append(
                    f"  scene {i:02d} ({sc['type']}) draws its credit at "
                    f"y {found_at:.2f} — Instagram's account row is measured at "
                    f"y 0.835, so the attribution is painted over on the phone. "
                    f"(A still older than the credit fix will say this; "
                    f"re-render before acting on it.)")

        # 2. A DECLARED HEADLINE MUST BE VISIBLE where it says it is.
        hl = sc.get("headline")
        if isinstance(hl, dict) and hl.get("lines"):
            y = float(hl.get("y", 0.5))
            band = ink_fraction(img, 0.06, max(0.0, y - 0.07), 0.94, min(1.0, y + 0.07))
            if band < 0.010:
                findings.append(
                    f"  scene {i:02d} ({sc['type']}) declares a headline at "
                    f"y {y:.2f} but that band is empty (ink {band:.3f})")

        # 3. NOTHING MAY RUN OFF THE SIDE. The receipt sliced mid-word, the
        #    typecard overflowed both edges, six headlines still overflow —
        #    each found by eye, one render at a time.
        # ONLY WHERE CONTENT IS BOUNDED BY DESIGN.
        #
        # A `footage` scene is full-bleed: the picture is SUPPOSED to reach the
        # frame edge, and a teardown clip of an exploded phone has parts running
        # off both sides because that is the shot. Running this check on every
        # type flagged made-by-google-26 scenes 10 and 16 as "content cut off"
        # when nothing was wrong — the third false-positive class in this tool,
        # and the same mistake each time: asserting a rule about laid-out
        # content against a frame that is a photograph.
        #
        # lint_frames.py already scopes its own edge check to
        # ("receipt", "floatcard") for this reason. Same list, plus the card
        # types added since — anything where WE decide the layout and therefore
        # anything at the edge is our overflow, not the source's composition.
        BOUNDED = {"receipt", "floatcard", "typecard", "statcard", "specsheet",
                   "sourceread", "annotatezoom", "chart", "checklist",
                   "promptcard", "categorygrid", "timeline", "priceladder",
                   "wordcascade", "carousel"}
        if sc["type"] not in BOUNDED:
            continue
        for side, (a, b) in (("left", (0.0, 0.012)), ("right", (0.988, 1.0))):
            edge = ink_fraction(img, a, 0.12, b, 0.80)
            if edge > 0.055:
                findings.append(
                    f"  scene {i:02d} ({sc['type']}) has busy ink against the "
                    f"{side} frame edge (ink {edge:.3f}) — content is probably "
                    f"cut off there")
    return findings


def selftest() -> int:
    """Prove both layers can still SEE the bugs they were built for.

    A checker that reports nothing is indistinguishable from a checker that is
    broken, and this repo has shipped both — `[SKIP] PIL not installed` sat
    unread for weeks while the pixel checks did nothing. So the four defects of
    2026-08-18 are reconstructed here as positive controls. If any of these
    stops firing, this tool has stopped working, whatever it prints on a real
    reel.
    """
    from PIL import Image, ImageDraw
    ok = True

    def check(name: str, condition: bool):
        nonlocal ok
        print(f"  {'ok  ' if condition else 'FAIL'} {name}")
        ok = ok and condition

    # 1. THE TYPECARD CREDIT — declared in the sheet, drawn nowhere.
    blank = Image.new("RGB", (1080, 1920), (244, 240, 230))
    check("empty credit band is detected",
          ink_fraction(blank, 0.04, 0.755, 0.62, 0.815) < 0.012)

    def credit_at(y_px):
        """A blank frame with a credit-like strip of type at y_px."""
        im = blank.copy()
        dd = ImageDraw.Draw(im)
        for k in range(28):
            dd.rectangle([60 + k * 22, y_px, 72 + k * 22, y_px + 40],
                         fill=(20, 20, 20))
        return im

    def locate(im):
        bands = [(0.45 + k * 0.02, ink_fraction(im, 0.04, 0.45 + k * 0.02,
                                                0.55, 0.45 + k * 0.02 + 0.028))
                 for k in range(27)]
        vals = sorted(v for _, v in bands)
        med = vals[len(vals) // 2]
        py, pk = max(bands, key=lambda b: b[1])
        return py if pk >= 0.012 and pk >= max(3 * med, 0.012) else None

    # the credit lane (y 0.78) — the standard position
    check("a credit in the standard lane is located",
          locate(credit_at(1500)) is not None)
    # FloatingCard anchors to the CARD: y 0.64 on a wide card. Searching from
    # y 0.70 reported this drawn credit as missing.
    check("a credit at y 0.64 (FloatingCard) is located",
          locate(credit_at(1230)) is not None)
    # the pre-2026-08-17 position, which IS a real defect: under the account row
    low = locate(credit_at(1610))
    check("a credit under the account row is located and low",
          low is not None and low >= 0.82)
    check("a frame with no credit at all reports none",
          locate(blank) is None)

    # 2. TYPE RUNNING OFF THE FRAME — the receipt sliced mid-word, the typecard
    #    overflowing both edges, and the six headlines G05 still passes.
    bleed = blank.copy()
    d = ImageDraw.Draw(bleed)
    for k in range(30):
        d.rectangle([0, 300 + k * 40, 9, 320 + k * 40], fill=(10, 10, 10))
    check("ink against the frame edge is detected",
          ink_fraction(bleed, 0.0, 0.12, 0.012, 0.80) > 0.055)
    # and the scoping that stops it firing on full-bleed video, which is the
    # false positive it produced on made-by-google-26 scenes 10 and 16
    import inspect as _inspect
    _src = _inspect.getsource(pixel_layer)
    check("edge check is scoped to bounded scene types",
          '"footage"' not in _src.split("BOUNDED = ")[1].split("}")[0])
    check("a clean margin is not flagged",
          ink_fraction(blank, 0.0, 0.12, 0.012, 0.80) <= 0.055)

    # 3. A FIELD THE COMPONENT NEVER READS.
    import tempfile, os
    with tempfile.TemporaryDirectory() as td:
        comp = Path(td) / "FakeCard.tsx"
        comp.write_text("export const FakeCard = ({ scene }) => scene.title;")
        global COMPONENTS
        keep = COMPONENTS
        COMPONENTS = Path(td)
        try:
            read = fields_read_by("FakeCard", "prop")
            check("a read field is seen as read", "title" in (read or set()))
            check("an unread field is seen as unread", "credit" not in (read or set()))
        finally:
            COMPONENTS = keep

    # 4. THE SPREAD FORM — the false-positive that made the first version of
    #    this tool wrong seven times out of seven.
    mapping = scene_component_map()
    check("chart is recognised as a spread-prop component",
          mapping.get("chart", ("", ""))[1] == "spread")
    check("footage is recognised as a scene-prop component",
          mapping.get("footage", ("", ""))[1] == "prop")
    chart_fields = fields_read_by("ChartScene", "spread") or set()
    check("spread component's destructured props are found",
          {"title", "items", "source"} <= chart_fields)

    print("\n  self-test PASSED\n" if ok else "\n  self-test FAILED\n")
    return 0 if ok else 1


def main() -> None:
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    everything = "--all" in sys.argv
    sheets = (sorted((ROOT / "src/beats").glob("*.json")) if everything
              else [ROOT / f"src/beats/{args[0]}.json"] if args else [])
    if not sheets:
        sys.exit(__doc__.split("    python3")[0].strip())

    print("\n  DECLARED BUT NEVER READ  (beat sheet -> component)")
    a = static_layer(sheets)
    print("\n".join(a) if a else "    every declared field is read by its component")

    if not everything and "--static" not in sys.argv:
        print("\n  DECLARED BUT NEVER DRAWN  (component -> pixels)")
        b = pixel_layer(args[0])
        print("\n".join(b) if b else "    every declared credit and headline is on the frame")
    else:
        b = []

    print(f"\n  {len(a) + len(b)} finding(s) — ADVICE. Nothing here blocks a "
          f"render;\n  see RULES.md section 0 for why it should not.\n")


if __name__ == "__main__":
    main()
