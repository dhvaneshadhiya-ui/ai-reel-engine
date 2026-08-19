#!/usr/bin/env python3
"""The parts every build script rewrites from scratch.

WHY (measured 2026-08-19, answering "why does a video take two hours")
----------------------------------------------------------------------
Eight build scripts, 3,825 lines, and only 18 lines longer than 25 characters
are shared by all of them — 5 to 8% of any one file. Yet they do the same work:

    6 distinct helpers, 29 separate definitions across 8 files
    chunk() redefined in 8 of 8

Of a 486-line build script, about 42 lines are the actual creative decisions —
the beat table mapping a spoken phrase to its shots. The other ~440 are helpers
and machinery, retyped per reel.

THE COST IS NOT ONLY TIME. Copy-pasted helpers mean a bug is written once and
shipped eight times:

  * `cb=300` — the value that printed captions under Instagram's account row —
    lived in six separate copies of face(). Fixing it meant six edits.
  * build_applepay.py's face() contains `if cb: s["captionBottom"] = cb` where
    the dict is named `sc`. `s` is a float from an unrelated function, so that
    line raises NameError whenever cb is truthy. It survived because it is one
    of eight copies and nobody reads eight copies.

So: one definition, one place for a bug to be, and a build script that is a beat
table instead of a program.

    from reelkit import Reel
    kit = Reel(slug="iphone-fold-ultra",
               avatar="assets/iphone-fold-ultra/avatar-master-169.mp4",
               clips="assets/iphone-fold-ultra/clips",
               credit="Unbox Therapy", focus_x=0.485)

    BEATS = [
        ("taller iphone",     [kit.shot("footprint-flat", zoom="out")]),
        ("decision explains", [kit.face()]),
    ]
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent

# A shot builder: given (start_time, duration) it returns a scene dict.
Builder = Callable[[float, float], dict]


@dataclass
class Reel:
    """Per-reel constants, so the helpers below never hardcode them."""

    slug: str
    avatar: str
    clips: str
    credit: str = ""
    focus_x: float = 0.5

    # ---- shot helpers -----------------------------------------------------

    def shot(self, name: str, zoom: str = "in", headline: Any = None,
             cb: int | None = None, sfx: list | None = None,
             credit: str | None = None, infocard: Any = None,
             ext: str = "mp4", **extra: Any) -> Builder:
        """B-roll from the reel's clip directory."""
        def build(t0: float, d: float) -> dict:
            s: dict[str, Any] = {
                "type": "footage", "src": f"{self.clips}/{name}.{ext}",
                "durationSec": d, "zoomDir": zoom,
                "credit": credit if credit is not None else self.credit,
                "assetId": f"clip-{name}",
            }
            _put(s, headline=headline, captionBottom=cb, sfx=sfx,
                 infocard=infocard, **extra)
            return s
        return build

    def face(self, headline: Any = None, cb: int | None = None,
             infocard: Any = None, **extra: Any) -> Builder:
        """The presenter, cut from the avatar master at the beat's own time.

        `from` is the position on the master timeline and must equal the
        scene's start, or the lips stop matching the words. That is why it is
        computed here from t0 rather than passed in.
        """
        def build(t0: float, d: float) -> dict:
            s: dict[str, Any] = {
                "type": "footage", "src": self.avatar, "durationSec": d,
                "from": round(t0, 2), "focusX": self.focus_x,
            }
            # NB the dict is `s` in every branch. The applepay copy wrote to a
            # different name here and raised NameError whenever cb was set.
            _put(s, headline=headline, captionBottom=cb, infocard=infocard,
                 **extra)
            return s
        return build

    def card(self, src: str, aspect: float | None = None, bg: str = "cream",
             credit: str | None = None, cb: int | None = None,
             **extra: Any) -> Builder:
        """A floating card — a clip or still framed on a field."""
        def build(t0: float, d: float) -> dict:
            s: dict[str, Any] = {
                "type": "floatcard", "src": f"{self.clips}/{src}",
                "durationSec": d, "bg": bg,
                "credit": credit if credit is not None else self.credit,
            }
            _put(s, aspect=aspect, captionBottom=cb, **extra)
            return s
        return build

    def mg(self, spec: dict, sfx: list | None = None, **extra: Any) -> Builder:
        """A motion-graphics scene: the spec IS the scene, minus its duration."""
        def build(t0: float, d: float) -> dict:
            s = dict(spec)
            s["durationSec"] = d
            _put(s, sfx=sfx, **extra)
            return s
        return build

    def az(self, png: str, aid: str, sw: int, sh: int, focus: dict,
           annotations: list | None = None, credit: str | None = None,
           bg: str = "cream", sfx: list | None = None,
           cb: int | None = None, **extra: Any) -> Builder:
        """An annotated zoom onto a screenshot."""
        def build(t0: float, d: float) -> dict:
            s: dict[str, Any] = {
                "type": "annotatezoom", "src": png, "durationSec": d,
                "srcWidth": sw, "srcHeight": sh, "assetId": aid,
                "focus": focus, "backdrop": bg,
                "credit": credit if credit is not None else self.credit,
            }
            _put(s, annotations=annotations, sfx=sfx, captionBottom=cb, **extra)
            return s
        return build


    def doc(self, name: str, aid: str, credit: str | None = None,
            backdrop: str = "cream", headline: Any = None,
            highlights: list | None = None, sfx: list | None = None,
            covers: str | None = None, **extra: Any) -> Builder:
        """A STILL — a screenshot, an article, a spec capture.

        Renders `receipt`, which is an <Img>. Never `floatcard` or `footage`:
        both render an <OffthreadVideo>, and ffmpeg decodes a PNG as a ONE-FRAME
        video, so any position past 0 dies with "Compositor error: No frame
        found at position N". G35.

        Six build scripts wired stills into floatcard anyway, and every one of
        them has been unable to run since G35 was written. They did it for a
        real reason, recorded in build_iphonefoldultra's flo(): ReceiptScene's
        1.35 zoom floor overflowed wide captures and cut their text mid-word.
        That floor was capped on 2026-08-18 — a document may now be cropped
        vertically, never horizontally — so the workaround outlived its cause.

        DIMENSIONS ARE MEASURED, not passed. A receipt places its highlights in
        source pixels, so a wrong srcWidth misplaces every mark on the page.
        """
        from PIL import Image
        path = ROOT / "public" / f"{self.clips}/{name}"
        with Image.open(path) as im:
            w, h = im.size

        def build(t0: float, d: float) -> dict:
            s: dict[str, Any] = {
                "type": "receipt", "src": f"{self.clips}/{name}",
                "durationSec": d, "srcWidth": w, "srcHeight": h,
                "backdrop": backdrop, "assetId": aid,
                "credit": credit if credit is not None else self.credit,
            }
            _put(s, headline=headline, highlights=highlights, sfx=sfx,
                 covers=covers, **extra)
            return s
        return build


def _put(scene: dict, **kv: Any) -> None:
    """Set only the keys that carry a value.

    Every build script writes this as a run of `if x: s["x"] = x` lines, which
    is where the applepay typo hid. One helper, and a typo becomes impossible
    rather than invisible.
    """
    for k, v in kv.items():
        if v is not None and v is not False and v != []:
            scene[k] = v


def chunk(words: list, max_words: int = 4, max_gap: float = 0.55) -> list:
    """Group word timings into caption spans.

    Redefined in 8 of 8 build scripts. The defaults are the shipped values;
    pass explicit ones where a reel disagrees rather than editing a copy.
    """
    out: list[list] = []
    cur: list = []
    for w in words:
        if not cur:
            cur = [w]
            continue
        gap = w[0] - cur[-1][1]
        if len(cur) >= max_words or gap > max_gap:
            out.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        out.append(cur)
    return out


def assemble(beats: list, spans: dict) -> list:
    """Turn a beat table into scenes, splitting each phrase's time across shots.

    `beats` is [(phrase, [builder, ...]), ...] and `spans` maps a phrase to its
    (start, end) from the VO. A phrase with three shots gives each a third of
    its span — the same arithmetic every build script writes inline.
    """
    scenes: list[dict] = []
    for phrase, builders in beats:
        if phrase not in spans:
            raise KeyError(
                f"beat {phrase!r} has no span in the VO. Every beat must be "
                f"anchored to words that were actually spoken (Rule 3).")
        t0, t1 = spans[phrase]
        n = max(1, len(builders))
        each = (t1 - t0) / n
        for j, b in enumerate(builders):
            start = t0 + j * each
            scenes.append(b(start, round(each, 3)))
    return scenes
