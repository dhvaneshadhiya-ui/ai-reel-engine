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
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Viewer's-language glossary. The fallback names the type in quotes, so an
# exotic scene degrades to jargon-with-a-flag rather than silence.
PLAIN = {
    "split": "screen split: {top} above the presenter on camera",
    "footage": "{clip}",
    # sourceread / annotatezoom / receipt used to be FIXED strings — "a
    # screenshot, zooming slowly into the highlighted region" — which names the
    # CAMERA MOVE and not one thing on the page. Exactly the fault the floatcard
    # note below records, and worse in practice: found 2026-08-26 on a reel
    # where 18 of 26 beats were one of these three, so 70% of the plan the user
    # was asked to approve said nothing about what they were approving. They now
    # resolve their asset from the manifest like {clip} does, and name the claim
    # the highlight is there to prove ({covers}, the spoken words the beat is
    # anchored to).
    "sourceread": "{shot}, the line proving it lights up as it is read",
    "annotatezoom": "{shot}, zoomed in on the part that proves it",
    "receipt": "{shot}, held while the highlight lands on the proof",
    "wordcascade": "big words land one by one: {words}",
    "checklist": "a checklist ticks through: {rows}",
    "comparesplit": "a side-by-side comparison",
    "typecard": "a full-screen text card: {texts}",
    "specsheet": "a spec sheet builds line by line",
    "statcard": "one big number on a card",
    "counter": "one big number rolls up to its final value, with what it counts underneath",
    # floatcard said "a floating info card over the scene" — which describes the
    # CONTAINER and not one thing inside it. An approver reading that learns
    # nothing about what they are approving, the exact failure this file exists
    # to prevent. It carries real footage, so it resolves its clip like
    # `footage` does (found 2026-08-22, on a reel whose three feature beats were
    # ALL floatcards).
    "floatcard": "{shot}, shown whole on a card so nothing is cropped out",
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


def _asset_for(scene: dict, shows: dict) -> dict | None:
    """The manifest entry behind this scene's `src`, longest id first.

    Longest-first because ids overlap: 'ui-topics-list' and 'ui-topic-open'
    both substring-match a src containing the former, and dict order would
    decide which one described the frame.
    """
    src = str(scene.get("src", ""))
    for aid in sorted((a for a in shows if a), key=len, reverse=True):
        if aid in src:
            return shows[aid]
    return None


def _gist(text: str, cap: int = 130) -> str:
    """The first idea in a manifest `shows` field.

    `shows` is written for the BUILDER and is deliberately exhaustive — the
    topics-list entry here runs 60 words. Printed in full it is accurate and
    unreadable, and printed four times (one asset, four beats) it buries the
    plan. The approver needs the gist plus the claim; the full text stays one
    file away in the manifest.
    """
    text = " ".join(text.split())
    if len(text) <= cap:
        return text
    head = text[:cap]
    for sep in (". ", "; ", ": ", ", "):
        i = head.rfind(sep)
        if i > cap * 0.5:
            return head[:i]
    return head[:head.rfind(" ")] + "…"


def _clip(scene: dict, shows: dict, noun: str = "a clip") -> str:
    src = str(scene.get("src", ""))
    if "avatar-master" in src:
        return "the presenter, on camera"
    meta = _asset_for(scene, shows)
    base = f"{noun}"
    if meta and meta.get("shows"):
        base = f"{noun} showing {_gist(meta['shows'])}"
    elif src:
        base = f"{noun} ({Path(src).stem})"
    if scene.get("credit"):
        base += f" — credited {scene['credit']}"
    return base


def _shot(scene: dict, shows: dict, seen: set | None = None) -> str:
    """Like _clip, but names the artefact by what it IS — a still says
    "a screenshot", not "a clip" — and appends the claim the beat proves.

    An asset used across several beats is described once. Repeats say "the
    same screenshot again", because a plan that re-prints the same 60 words
    four times is as hard to approve as one that prints nothing.
    """
    meta = _asset_for(scene, shows)
    kind = (meta or {}).get("kind", "")
    noun = "a clip" if kind == "footage" else "a screenshot"
    aid = (meta or {}).get("id")
    if seen is not None and aid and aid in seen:
        # Name WHICH one. "the same screenshot again" is unambiguous only while
        # a plan has one repeated asset; this reel has two interleaved, and the
        # phrase silently stopped identifying anything (2026-08-26).
        tag = _gist((meta or {}).get("shows", ""), 44)
        base = f"the same {noun.split()[-1]} again"
        if tag:
            base += f" ({tag}…)"
        if scene.get("credit"):
            base += f" — credited {scene['credit']}"
    else:
        base = _clip(scene, shows, noun=noun)
        if seen is not None and aid:
            seen.add(aid)
    covers = (scene.get("covers") or "").strip()
    if covers:
        base += f" — proving “{covers}”"
    return base


# A stage has no fixed picture, so it cannot be one PLAIN line: it is read out
# as its own things and what happens to them, in order (2026-09-15). This is
# the visual plan the user approves alongside the script.
_VERB_WORDS = {
    "arrive": "{a} comes in", "exit": "{a} leaves", "dim": "{a} fades back",
    "focus": "the camera pushes in on {a}", "highlight": "{a} gets highlighted",
    "stamp": "{a} is stamped “{text}”", "strike": "{a} is struck out",
    "count": "{a} counts up", "connect": "a line runs from {f} to {to}, pulses travelling along it",
}


def _slide_words(scene: dict) -> str:
    """A slide in the viewer's terms (2026-09-19). The animated format puts
    every reel through `slide`, and this printed "a slide scene" for all of
    them — an approval nobody could read, which is the exact failure the beat
    plan exists to prevent (2026-08-21)."""
    head = re.sub(r"\[\[(.*?)\]\]", r"\1", str(scene.get("headline") or "")).strip()
    bits = []
    for b in scene.get("blocks") or []:
        k = b.get("kind")
        if k == "gauge":
            to = b.get("to")
            bits.append(f"a battery draining from {b.get('from')}% to {to}%" if to is not None and to != b.get("from")
                        else f"a battery sitting at {b.get('from')}%")
        elif k == "clip":
            bits.append(f"a screen recording playing ({str(b.get('src') or '').split('/')[-1]})")
        elif k == "screen":
            bits.append(f"the page itself ({str(b.get('src') or '').split('/')[-1]}), zooming to the line")
        elif k == "steps":
            bits.append("a strip lighting up: " + ", ".join(f"“{s}”" for s in (b.get("steps") or [])))
        elif k == "rows":
            bits.append("rows: " + ", ".join(f"“{r.get('k')} — {r.get('v')}”" for r in (b.get("rows") or [])))
        elif k == "tips":
            bits.append("two cards: " + ", ".join(f"“{x}”" for x in (b.get("best"), b.get("watch")) if x))
        elif k in ("hero", "swap"):
            names = [s.get("name") for s in (b.get("side"), b.get("left"), b.get("right")) if isinstance(s, dict)]
            bits.append(("a swap: " if k == "swap" else "a card: ") + ", ".join(f"“{n}”" for n in names if n))
        elif k == "spotlight":
            bits.append(f"“{b.get('name')}” landing big")
        elif k == "logos":
            bits.append("logos: " + ", ".join(str(i.get("name")) for i in (b.get("items") or [])))
        elif k == "devices":
            bits.append(f"{b.get('hub')} linked to " + ", ".join(str(i) for i in (b.get("items") or [])))
        elif k == "waves":
            bits.append("two waveforms")
        elif k == "text":
            bits.append(f"a line: “{b.get('text')}”")
    who = " with the presenter in the corner" if scene.get("presenter") else ""
    strikes = [m.get("target") for m in scene.get("moves") or [] if m.get("do") == "strike"]
    struck = f", and {len(strikes)} of them get crossed out" if strikes else ""
    return f"a page headed “{head}”{who}: " + "; ".join(bits) + struck


def _stage_words(scene: dict) -> str:
    def name(e):
        if not e:
            return "something"
        if e.get("kind") == "number":
            return f"“{e.get('prefix', '')}{e.get('value', '?')}{e.get('suffix', '')}”"
        label = e.get("title") or e.get("text") or e.get("label")
        if label:
            return f"“{label}”"
        return "a picture of " + str(e.get("src", "")).rsplit("/", 1)[-1].rsplit(".", 1)[0].replace("-", " ")
    els = {e.get("id"): e for e in scene.get("elements") or []}
    steps, run = [], []   # a run of the same one-target verb reads as one step

    def flush():
        if not run:
            return
        verb, names = run[0][0], [n for _, n in run]
        joined = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
        phrase = _VERB_WORDS[verb].format(a=joined, f="", to="", text="✓")
        if len(names) > 1:   # plural verb
            phrase = (phrase.replace(" comes in", " come in").replace(" leaves", " leave")
                      .replace(" fades back", " fade back").replace(" gets ", " get ")
                      .replace(" counts up", " count up").replace(" is struck", " are struck"))
        steps.append(phrase)
        run.clear()

    for m in sorted(scene.get("moves") or [], key=lambda m: float(m.get("at") or 0)):
        verb = m.get("do")
        if verb not in _VERB_WORDS:
            continue
        if verb in ("arrive", "exit", "dim", "count", "strike", "highlight"):
            if run and run[0][0] != verb:
                flush()
            run.append((verb, name(els.get(m.get("target")))))
            continue
        flush()
        steps.append(_VERB_WORDS[verb].format(a=name(els.get(m.get("target"))), f=name(els.get(m.get("from"))),
                                              to=name(els.get(m.get("to"))), text=m.get("text", "✓")))
    flush()
    where = {"dark": "dark", "brand": "brand-colour"}.get(scene.get("set") or "", "light")
    line = f"an animated graphic on a {where} set"
    if scene.get("layout") == "split":
        line += ", the presenter below"
    if steps:
        line += ": " + "; ".join(steps)
    if scene.get("credit"):
        line += f" — credited {scene['credit']}"
    return line


def describe(scene: dict, shows: dict, seen: set | None = None) -> str:
    t = scene.get("type", "?")
    if t == "stage":
        return _stage_words(scene)
    if t == "slide":
        return _slide_words(scene)
    tpl = PLAIN.get(t)
    if tpl is None:
        extras = _texts(scene, 3)
        tail = f": {', '.join(repr(x) for x in extras)}" if extras else ""
        return f"a \"{t}\" scene{tail}"
    fills = {}
    if "{clip}" in tpl:
        fills["clip"] = _clip(scene, shows)
    if "{shot}" in tpl:
        fills["shot"] = _shot(scene, shows, seen)
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
    seen: set[str] = set()
    for i, s in enumerate(shots, 1):
        line = (s.get("line") or s.get("start_phrase") or "?").strip()
        scene = s.get("scene") or {}
        out.append(f"  {i:2}. HEAR  “{line}”")
        out.append(f"      SEE   {describe(scene, shows, seen)}"
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
