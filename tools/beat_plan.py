#!/usr/bin/env python3
"""The beat plan, in the VIEWER'S language — what you hear, what you see.

WHY THIS EXISTS
---------------
2026-08-21: the user was shown a beat table for approval that read
"chip with label withheld / generated MG" and "✓ ✓ ?" — the pipeline's
internal vocabulary, meaningful to the session that wrote it and opaque to
the person being asked to approve it. Approval is informed consent on the
script AND the plan (CLAUDE.md); a plan the approver cannot picture makes
the second half of that consent hollow.

The shot plan already contains everything a human needs — the spoken line,
the scene's actual content, the asset behind it. This renders it as a
walkthrough:

     3. HEAR  "Which is odd, because we know its exact Pantone code."
        SEE   the presenter, on camera

`script_approval.py propose` prints this automatically when a shot plan
exists. Scene-type names appear only as a small trailing tag — they are for
the builder, not the approver.

    python3 tools/beat_plan.py <slug>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Viewer's-language glossary. The fallback names the type in quotes, so an
# exotic scene degrades to jargon-with-a-flag rather than silence.
PLAIN = {
    "split": "screen split: {top} above the presenter on camera",
    "footage": "{clip}",
    "sourceread": "the source article on screen — the quoted line lights up "
                  "as it is read",
    "annotatezoom": "a screenshot, zooming slowly into the highlighted region",
    "wordcascade": "big words land one by one: {words}",
    "checklist": "a checklist ticks through: {rows}",
    "comparesplit": "a side-by-side comparison",
    "typecard": "a full-screen text card: {texts}",
    "specsheet": "a spec sheet builds line by line",
    "statcard": "one big number on a card",
    # floatcard said "a floating info card over the scene" — which describes the
    # CONTAINER and not one thing inside it. An approver reading that learns
    # nothing about what they are approving, the exact failure this file exists
    # to prevent. It carries real footage, so it resolves its clip like
    # `footage` does (found 2026-08-22, on a reel whose three feature beats were
    # ALL floatcards).
    "floatcard": "{clip}, shown whole on a card so nothing is cropped out",
    "receipt": "a screenshot 'receipt' slides through",
    "chart": "an animated chart",
    "headlinebuild": "a headline assembles on screen",
    "priceladder": "prices stack into a ladder",
    "endquestion": "the closing question on screen",
    "commentcta": "the comment-gate call to action: the keyword types itself "
                  "into a comment field, then a 'link sent' notification",
    "logobeat": "the brand mark, on the beat",
    "timeline": "a timeline sweeps through its entries",
}

MARKS = {"done": "✓", "no": "✗", "q": "?"}


def _texts(obj, cap=6) -> list[str]:
    """Every "text" value inside a scene fragment, in order — headline
    lines, kinetic lines, cascade words — without knowing each shape."""
    out: list[str] = []

    def walk(o):
        if len(out) >= cap:
            return
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "text" and isinstance(v, str):
                    out.append(" / ".join(v.split("\n")))
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return out


def _clip(scene: dict, shows: dict) -> str:
    src = str(scene.get("src", ""))
    if "avatar-master" in src:
        return "the presenter, on camera"
    aid = None
    for a, meta in shows.items():
        if a and a in src:
            aid = a
            break
    base = "a video clip"
    if aid and shows[aid].get("shows"):
        base = f"a clip showing {shows[aid]['shows']}"
    elif src:
        base = f"a clip ({Path(src).stem})"
    if scene.get("credit"):
        base += f" — credited {scene['credit']}"
    return base


def describe(scene: dict, shows: dict) -> str:
    t = scene.get("type", "?")
    tpl = PLAIN.get(t)
    if tpl is None:
        extras = _texts(scene, 3)
        tail = f": {', '.join(repr(x) for x in extras)}" if extras else ""
        return f"a \"{t}\" scene{tail}"
    fills = {}
    if "{clip}" in tpl:
        fills["clip"] = _clip(scene, shows)
    if "{top}" in tpl:
        top = str(scene.get("topSrc", ""))
        fills["top"] = ("the presenter, on camera" if "avatar-master" in top
                        else _clip({"src": top,
                                    "credit": scene.get("credit")}, shows))
    if "{words}" in tpl or "{texts}" in tpl:
        words = _texts(scene) or ["…"]
        key = "words" if "{words}" in tpl else "texts"
        fills[key] = ", ".join(f"“{w}”" for w in words)
    if "{rows}" in tpl:
        rows = scene.get("rows") or []
        fills["rows"] = ", ".join(
            f"{r.get('label', '?')} {MARKS.get(r.get('state'), '')}".strip()
            for r in rows) or "…"
    line = tpl.format(**fills)
    heads = _texts({"h": scene.get("headline")}, 3)
    if heads:
        line += " — headline: " + ", ".join(f"“{h}”" for h in heads)
    if scene.get("credit") and "credited" not in line:
        line += f" — credited {scene['credit']}"
    return line


def render(slug: str, root: Path | None = None) -> list[str]:
    root = root or ROOT
    sp = root / "jobs" / slug / "shot-plan.json"
    if not sp.exists():
        return []
    shots = json.loads(sp.read_text()).get("shots") or []
    if not shots:
        return []
    shows: dict[str, dict] = {}
    man = root / "public" / "assets" / slug / "manifest.json"
    if man.exists():
        try:
            m = json.loads(man.read_text())
            for a in (m.get("assets") or m.get("items") or []):
                if a.get("id"):
                    shows[a["id"]] = a
        except Exception:
            pass
    out = []
    for i, s in enumerate(shots, 1):
        line = (s.get("line") or s.get("start_phrase") or "?").strip()
        scene = s.get("scene") or {}
        out.append(f"  {i:2}. HEAR  “{line}”")
        out.append(f"      SEE   {describe(scene, shows)}"
                   f"   [{scene.get('type', '?')}]")
    return out


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__.split("    python3")[0].strip())
    lines = render(args[0])
    if not lines:
        sys.exit(f"no shot plan (or no shots) at jobs/{args[0]}/shot-plan.json")
    print("\n  THE BEAT PLAN — what is on screen while each line is spoken\n")
    print("\n".join(lines))
    print("\n  Type tags in [brackets] are for the builder; everything else "
          "is what the viewer\n  experiences. If a SEE line is not "
          "understandable, the plan is not ready to approve.")


if __name__ == "__main__":
    main()
