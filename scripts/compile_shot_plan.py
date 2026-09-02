#!/usr/bin/env python3
"""Compile a phrase-anchored Nick reel shot plan into a Remotion beat sheet."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_ENGINE = Path(__file__).resolve().parent.parent  # repo root


_CONTRACTION_TAILS = {"s", "t", "d", "ll", "re", "ve", "m"}


def normalize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower().replace("’", "'"))


def normalize_phrase(value: str) -> list[str]:
    """Normalise a start_phrase the way the TRANSCRIPT is normalised.

    The transcript merges a possessive/contraction back onto its stem, so
    "Apple's" is stored as ONE entry with norm "apples" (see the merge at the
    top of `timed_words`). `normalize()` alone splits it into ["apple", "s"],
    which can never equal ["apples"] — so every start_phrase containing a
    possessive failed to resolve with "could not resolve shot N".

    Found 2026-08-21 on iphone18-colors, whose first shot starts "Apple's
    iPhone 18 Pro". The transcript half of this was fixed when gate G34 was
    added; the needle half was not, and nothing had exercised it because the
    earlier reels' start_phrases happened to begin on a plain word.

    Merging is done PER WHITESPACE-WORD, exactly like the transcript: a tail
    is only absorbed when it came from the same source word, so "it s" written
    as two separate words is left alone.
    """
    out: list[str] = []
    for word in value.split():
        tokens = normalize(word)
        for token_index, token in enumerate(tokens):
            if token_index > 0 and token in _CONTRACTION_TAILS and out:
                out[-1] = out[-1] + token
            else:
                out.append(token)
    return out


def locked_style(engine: Path) -> str:
    """Read the locked STYLE pack from config.json.

    Hardcoded "nick" until 2026-08-16 while config.json defaulted to the
    editorial pack, so the generic new-reel path produced a utility-styled
    beat sheet for every reel. Same failure as the caption style below:
    validate_job.py was fixed on 2026-08-12, the producer was not.
    """
    cfg = engine / "config.json"
    locked = "editorial"
    if cfg.exists():
        try:
            locked = json.loads(cfg.read_text()).get("defaults", {}).get(
                "style", locked)
        except Exception:
            pass
    return locked


def locked_caption_style(engine: Path) -> str:
    """Read the locked caption treatment from config.json.

    Never hardcode it here. This emitted the pre-2026-07-30 "chip-lg" value
    long after the treatment was locked (now "word-reveal"), so every beat sheet
    this script produced was rejected by validate_job.py and gate G10 — the
    generic new-reel path was dead while the bespoke tools/build_*.py scripts
    (which set it themselves) kept working and hid it.
    validate_job.py already reads config.json; this mirrors it. Fixed
    2026-08-16.
    """
    cfg = engine / "config.json"
    locked = "word-reveal"
    if cfg.exists():
        try:
            locked = json.loads(cfg.read_text()).get("defaults", {}).get(
                "captionStyle", locked)
        except Exception:
            pass
    return locked


def load_words(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text())
    if isinstance(raw, dict) and isinstance(raw.get("words"), list):
        words = raw["words"]
    elif isinstance(raw, dict) and isinstance(raw.get("segments"), list):
        words = [
            word
            for segment in raw["segments"]
            for word in segment.get("words", [])
        ]
    else:
        raise SystemExit(f"unsupported Whisper JSON shape: {path}")

    out: list[dict[str, Any]] = []
    for index, word in enumerate(words):
        text = str(word.get("word", word.get("text", ""))).strip()
        if not text:
            continue
        try:
            start = float(word["start"])
            end = float(word["end"])
        except (KeyError, TypeError, ValueError):
            raise SystemExit(f"invalid word timing at index {index}: {word!r}")
        tokens = normalize(text)
        if not tokens:
            # A PUNCTUATION-ONLY token. whisper emits "%" as its own word, and
            # normalize() returns [] for it, so this loop used to `continue` and
            # DROP IT — shipping "shrink about 35" and "reportedly 15" with no
            # unit at all, against the standard-notation rule. Glue it onto the
            # word it belongs to instead. Caught on the iphone-18-pro contact
            # sheet; the gates do not see a missing symbol.
            if out and text and out[-1].get("source_index") == index - 1:
                out[-1]["text"] = f'{out[-1]["text"]}{text}'
                out[-1]["end"] = end
            continue
        # A token whisper starts with a hyphen belongs to the word before it:
        # "Ming" + "-Chi" shipped as "Ming -Chi". Documented in STYLE-RULES for
        # build_template.py; this generic path never inherited it.
        if text.startswith("-") and out:
            out[-1]["text"] = f'{out[-1]["text"]}{text}'
            # The WHOLE compound, joined — the SAME defect the comma branch
            # below records, one block up and never fixed with it. `[-1]` kept
            # only the last token, so whisper's "co" + "-work," carried norm
            # "work" and an anchor on "Cowork" could never resolve; "Ming" +
            # "-Chi" was searchable only as "chi". Found 2026-08-26 on
            # claude-memory-everywhere, whose glossary makes the voice say
            # "co-work" for Cowork, so every reel naming that product hits it.
            out[-1]["norm"] = "".join(normalize(out[-1]["text"]))
            out[-1]["end"] = end
            continue
        # Whisper occasionally returns ".8" or ",000" as a separate word. Both
        # must be merged back or the caption reads "$2 ,000" — gate G30, which
        # calls it "an orphan numeric fragment": a split number makes the
        # caption say something the creator did not.
        # The comma case was missing until 2026-08-21 (iphone18-colors, "two
        # thousand dollars" -> "$2" + ",000"); only "." was handled.
        if text[:1] in (".", ",") and out and tokens and tokens[0].isdigit():
            out[-1]["text"] = f'{out[-1]["text"]}{text[:1]}{tokens[0]}'
            # The WHOLE number, joined: [-1] kept only the last token, so
            # "100,000" carried norm "000" and no anchor containing the
            # number could ever resolve (found 2026-08-25 on claude-eating-
            # tokens shot 4 — the display half of this merge was right, the
            # matching half silently wasn't).
            out[-1]["norm"] = "".join(normalize(out[-1]["text"]))
            out[-1]["end"] = end
            continue
        # Whisper writes a spoken time-of-day "AM"/"PM" as TWO tokens: "a"
        # (or "p") then ".m." — the written abbreviation "a.m." with the
        # space the TTS left between the letters treated as a word break.
        # The second token alone is an orphan single-letter caption (gate
        # G34: "'.m. Pacific, Steve' carries an orphan single-letter
        # token"). CONFIRMED not a TTS artifact — isolated whisper (base
        # AND medium) on apple-surprise-and-shine 2026-08-27 both transcribe
        # the audio as "10 a.m. Pacific" cleanly; this is whisper's own
        # house style for the sound, not a mispronunciation, so the fix is a
        # merge like the ones above, not cutting the master. General fix:
        # any reel that states a time this way hits it, not just this one.
        if (out and out[-1].get("norm") in ("a", "p")
                and re.fullmatch(r"\.?m\.?", text.lower())):
            letter = out[-1]["norm"]
            out[-1]["text"] = f"{letter.upper()}M"
            out[-1]["norm"] = f"{letter}m"
            out[-1]["end"] = end
            continue
        # A possessive/contraction ("Apple's") normalises to ["apple","s"], and
        # emitting each token separately ships a caption chip reading just "s".
        # Gate G34 catches it; this merges the tail back onto the word it came
        # from, restoring the ORIGINAL spelling for display. General fix, not a
        # per-reel patch: every reel with a possessive hit this.
        for token_index, token in enumerate(tokens):
            if (
                token_index > 0
                and token in _CONTRACTION_TAILS
                and out
                and out[-1].get("source_index") == index
            ):
                out[-1]["text"] = text
                out[-1]["norm"] = out[-1]["norm"] + token
                out[-1]["end"] = end
                continue
            out.append(
                {
                    "text": text if len(tokens) == 1 else token,
                    "norm": token,
                    "start": start,
                    "end": end,
                    "source_index": index,
                    "sub_index": token_index,
                }
            )
    if not out:
        raise SystemExit(f"no timed words found in {path}")
    return out


def _match_at(haystack: list[str], needle: list[str], start: int) -> int | None:
    """Match `needle` at `start`, tolerating whisper's compound splits.

    Whisper splits written compounds into their spoken words — "README" comes
    back as "read me", "ccusage" as "cc usage" — so an exact window compare
    can never resolve a start_phrase containing one (found 2026-08-25 on
    claude-eating-tokens shot 5, "But its README admits"). Same class as the
    possessive fix in normalize_phrase, mirrored: there the NEEDLE was split
    too finely; here the TRANSCRIPT is. So allow one needle token to consume
    up to 3 consecutive transcript tokens whose concatenation equals it, and
    the reverse for the rare join. Returns the index of the last transcript
    word consumed, or None.
    """
    i, j = start, 0
    while j < len(needle):
        if i >= len(haystack):
            return None
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            continue
        joined = haystack[i]
        for k in range(i + 1, min(i + 3, len(haystack))):
            joined += haystack[k]
            if joined == needle[j]:
                break
            if len(joined) >= len(needle[j]):
                joined = None
                break
        else:
            joined = None
        if joined is not None:
            i = k + 1
            j += 1
            continue
        merged = needle[j]
        for m in range(j + 1, min(j + 3, len(needle))):
            merged += needle[m]
            if merged == haystack[i]:
                break
            if len(merged) >= len(haystack[i]):
                merged = None
                break
        else:
            merged = None
        if merged is None:
            return None
        i += 1
        j = m + 1
    return i - 1


def find_phrase(
    words: list[dict[str, Any]], phrase: str, cursor: int, label: str
) -> tuple[int, int]:
    needle = normalize_phrase(phrase)
    if not needle:
        raise SystemExit(f"{label} cannot be empty")
    haystack = [word["norm"] for word in words]
    for start in range(cursor, len(haystack)):
        end = _match_at(haystack, needle, start)
        if end is not None:
            return start, end
    preview = " ".join(haystack[cursor : cursor + 24])
    raise SystemExit(
        f"could not resolve {label} {phrase!r} after word {cursor}; "
        f"next transcript words: {preview!r}"
    )


def media_info(path: Path) -> dict[str, float] | None:
    if not path.exists() or not shutil.which("ffprobe"):
        return None
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,width,height",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        data = json.loads(result.stdout)
        video = next(
            stream
            for stream in data.get("streams", [])
            if stream.get("codec_type") == "video"
        )
        return {
            "duration": float(data["format"]["duration"]),
            "width": float(video["width"]),
            "height": float(video["height"]),
        }
    except (StopIteration, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def duration_of(path: Path) -> float | None:
    """Duration of ANY media file, video stream or not.

    media_info() insists on a video stream because it also returns width and
    height for the avatar's face framing. An audio-only VO track has no video
    stream, so media_info() returned None for it and the trailing-silence
    extension below silently never ran — leaving the scene total 0.23s short of
    the audio and tripping validate_job (found 2026-08-22 on the first VO-only
    reel).
    """
    if not path.exists() or not shutil.which("ffprobe"):
        return None
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=False,
    )
    try:
        return float(json.loads(result.stdout)["format"]["duration"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def css_focus_x(
    face_x: float, image_width: float, image_height: float, box_width: float, box_height: float
) -> float:
    """Return CSS object-position x that centers a face in a cover-fitted box."""
    image_aspect = image_width / image_height
    box_aspect = box_width / box_height
    if image_aspect <= box_aspect:
        return 0.5
    scaled_width = image_width * (box_height / image_height)
    crop = scaled_width - box_width
    if crop <= 0:
        return 0.5
    position = (face_x * scaled_width - box_width / 2) / crop
    return round(max(0.0, min(1.0, position)), 4)


def substitute(value: Any, tokens: dict[str, Any]) -> Any:
    if isinstance(value, dict):
        return {key: substitute(child, tokens) for key, child in value.items()}
    if isinstance(value, list):
        return [substitute(child, tokens) for child in value]
    if isinstance(value, str) and value in tokens:
        return tokens[value]
    return value


def _apply_phrases(text: str, phrase_fixes: dict[str, str]) -> str:
    """Case-insensitive replacement of multi-word correction keys.

    Punctuation-tolerant between words: whisper punctuates mishears
    unpredictably, and a literal match of "see use it" can never find
    "see, use it" — which is exactly how the ccusage correction silently
    did nothing on claude-eating-tokens (found 2026-08-25 in a rendered
    frame, after compile, validate and every gate passed). Spaces in the
    key match any non-alphanumeric run in the text.
    """
    for key, value in phrase_fixes.items():
        pattern = r"[^A-Za-z0-9]+".join(
            re.escape(part) for part in key.split())
        text = re.sub(pattern, value, text, flags=re.IGNORECASE)
    return text


def caption_words(
    words: list[dict[str, Any]], corrections: dict[str, str]
) -> list[dict[str, Any]]:
    corrected: list[dict[str, Any]] = []
    for word in words:
        text = word["text"].strip()
        key = re.sub(r"[^a-z0-9]", "", text.lower())
        if key in corrections:
            # TRAILING punctuation only. `re.sub(r"[A-Za-z0-9.]+", "", text)`
            # collected punctuation from ANYWHERE in the token, so a token
            # whisper had merged across a hyphen — "purple-tongued." — yielded
            # "-" and the correction came out as "purple-tinged-".
            # Found 2026-08-21 on iphone18-colors. Dots stay excluded from the
            # class so the existing "drop the full stop" behaviour is unchanged;
            # only interior punctuation stops leaking onto the end.
            match = re.search(r"[^A-Za-z0-9.]+$", text)
            text = corrections[key] + (match.group(0) if match else "")
        corrected.append({"start": word["start"], "end": word["end"], "text": text})

    # MULTI-WORD corrections are applied to the WORD STREAM, before chunking.
    #
    # They used to run on the CHUNK text afterwards, which works only while a
    # phrase happens to sit inside one three-word chunk. Regenerate the voice
    # and the boundaries move: on 2026-08-26 the v4 read chunked as
    # "see it, CC" / "usage charts, it", so "cc usage" -> "ccusage" matched
    # nothing and THREE tool names silently vanished from the captions of a
    # reel whose entire job is naming those tools. Same failure shape as the
    # anchor matcher's compound splits: the fix is to stop letting an
    # arbitrary grouping decide what is adjacent.
    #
    # A matched run collapses to ONE word entry spanning the run's timing, so
    # the name can never be split by a later chunk boundary either.
    phrase_fixes = {k: v for k, v in corrections.items() if " " in k}
    for key, value in sorted(phrase_fixes.items(), key=lambda kv: -len(kv[0])):
        parts = key.split()
        i = 0
        while i <= len(corrected) - len(parts):
            window = [re.sub(r"[^a-z0-9]", "", corrected[i + j]["text"].lower())
                      for j in range(len(parts))]
            if window == [re.sub(r"[^a-z0-9]", "", p) for p in parts]:
                merged = {
                    "start": corrected[i]["start"],
                    "end": corrected[i + len(parts) - 1]["end"],
                    "text": value,
                }
                corrected[i:i + len(parts)] = [merged]
            i += 1

    chunks: list[dict[str, Any]] = []
    for index in range(0, len(corrected), 3):
        group = corrected[index : index + 3]
        text = _apply_phrases(
            " ".join(item["text"] for item in group), phrase_fixes
        )
        # PER-WORD TIMINGS — the caption component's word-reveal, karaoke
        # envelope and EMPHASIS matching all key off `words`; without it the
        # whole chunk falls back to one "word" whose concatenation matches no
        # emphasis entry, so the accent highlight silently never fired on any
        # generic-path reel (found 2026-08-25 — the bespoke build_*.py sheets
        # all carry `words`, this compiler never did; same family as the
        # style/captionBottom/G27 gaps). A phrase fix can merge or reword the
        # chunk, so re-split its TEXT and map word starts positionally,
        # padding with the group's last start if the fix grew the word count.
        split = text.split()
        starts = [item["start"] for item in group]
        chunks.append(
            {
                "start": round(group[0]["start"], 3),
                "end": round(group[-1]["end"], 3),
                "text": text,
                "words": [
                    {"t": round(starts[min(w, len(starts) - 1)], 3),
                     "text": word}
                    for w, word in enumerate(split)
                ],
            }
        )
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    # The overwrite guard below tests `"--force" in sys.argv`, and argparse
    # rejected the flag before that test could ever run — so the tool printed
    # "Re-run with --force if replacing it is what you meant" and then refused
    # that exact command. Declared here so the instruction is followable
    # (found 2026-08-22).
    parser.add_argument(
        "--force", action="store_true",
        help="replace an existing beat sheet instead of refusing")
    parser.add_argument(
        "--engine",
        type=Path,
        default=Path(os.environ.get("REEL_ENGINE", DEFAULT_ENGINE)),
    )
    args = parser.parse_args()
    slug = args.slug
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        raise SystemExit("slug must use lowercase letters, numbers, and hyphens")


    engine = args.engine.expanduser().resolve()
    public = engine / "public"
    job_dir = engine / "jobs" / slug
    plan_path = job_dir / "shot-plan.json"
    vo_path = public / f"assets/{slug}/vo.json"
    manifest_path = public / f"assets/{slug}/manifest.json"
    avatar_rel = f"assets/{slug}/avatar-master.mp4"
    face_path = public / f"assets/{slug}/face-x.txt"
    for path in (plan_path, vo_path, manifest_path):
        if not path.exists():
            raise SystemExit(f"missing required input: {path}")

    plan = json.loads(plan_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    words = load_words(vo_path)
    audio_end = float(words[-1]["end"])
    # THE AUDIO TRACK IS NOT ALWAYS AN AVATAR (added 2026-08-22).
    # `audio` was hardcoded to assets/<slug>/avatar-master.mp4, which silently
    # assumed every reel is avatar-led. A VO-only reel — no presenter, narration
    # over footage — is a legitimate build (Scene.audio already documents "the
    # video's audio OR a wav"), and it had no way through this compiler. The
    # shot plan may now name its own `audio`; the avatar path is still the
    # default, so every existing plan compiles identically.
    audio_rel = str(plan.get("audio") or avatar_rel)
    audio_dur = duration_of(public / audio_rel)
    avatar_info = media_info(public / avatar_rel)
    if audio_dur is not None:
        audio_end = min(audio_end, audio_dur)
    face_x = 0.5
    if face_path.exists():
        try:
            face_x = float(face_path.read_text().strip())
        except ValueError:
            raise SystemExit(f"invalid face-center value: {face_path}")
    if not 0 <= face_x <= 1:
        raise SystemExit("face-x.txt must contain a fraction from 0 to 1")
    if avatar_info is not None:
        focus_full = css_focus_x(
            face_x,
            avatar_info["width"],
            avatar_info["height"],
            1080,
            1920,
        )
        focus_split = css_focus_x(
            face_x,
            avatar_info["width"],
            avatar_info["height"],
            1080,
            960,
        )
    else:
        focus_full = focus_split = round(face_x, 4)

    # Read `assets`, which is what every manifest in this repo actually writes.
    #
    # This said `manifest.get("items", [])` and nothing has ever used that key —
    # all seven manifests carry `assets` and zero carry `items`. So the lookup was
    # ALWAYS empty and any shot naming an asset_id died with "unknown manifest
    # asset". That is why every jobs/*/shot-plan.json holds 0 shots and why the
    # reels were hand-assembled by bespoke build_<slug>.py scripts instead: the
    # phrase-anchored path was not rejected on merit, it was broken on first
    # contact and quietly abandoned. `items` stays accepted in case an older
    # manifest turns up.
    manifest_items = {
        str(item.get("id")): item
        for item in (manifest.get("assets") or manifest.get("items") or [])
        if item.get("id")
    }
    shots = plan.get("shots")
    if not isinstance(shots, list) or not shots:
        raise SystemExit(f"shot plan contains no shots: {plan_path}")

    resolved: list[dict[str, Any]] = []
    cursor = 0
    for index, shot in enumerate(shots):
        start_i, _ = find_phrase(
            words, str(shot.get("start_phrase", "")), cursor, f"shot {index} start_phrase"
        )
        end_i = start_i
        if shot.get("end_phrase"):
            _, end_i = find_phrase(
                words,
                str(shot["end_phrase"]),
                start_i,
                f"shot {index} end_phrase",
            )
        start = float(words[start_i]["start"]) + float(shot.get("start_offset", 0))
        end = float(words[end_i]["end"]) + float(shot.get("end_offset", 0))
        if index == 0:
            start = 0.0
        resolved.append({"start": max(0.0, start), "end": min(audio_end, end), **shot})
        cursor = max(start_i + 1, end_i)

    # Phrase endpoints are editorial anchors. Make the final timeline seamless
    # by cutting each scene at the next scene's resolved start.
    scenes: list[dict[str, Any]] = []
    for index, shot in enumerate(resolved):
        start = float(shot["start"])
        end = (
            float(resolved[index + 1]["start"])
            if index + 1 < len(resolved)
            else audio_end
        )
        if end <= start:
            raise SystemExit(f"shot {index} has non-positive resolved duration")
        asset_id = shot.get("asset_id")
        asset = manifest_items.get(str(asset_id)) if asset_id else None
        if asset_id and asset is None:
            raise SystemExit(f"shot {index} references unknown manifest asset {asset_id!r}")
        scene = substitute(
            shot.get("scene", {}),
            {
                "$AVATAR": avatar_rel,
                "$START": round(start, 3),
                "$FACE_X": round(face_x, 4),
                "$FOCUS_FULL": focus_full,
                "$FOCUS_SPLIT": focus_split,
            },
        )
        if not isinstance(scene, dict) or not scene.get("type"):
            raise SystemExit(f"shot {index} lacks a valid scene")
        scene["durationSec"] = round(end - start, 3)
        # Split captions must clear the face seam (validate_job rejects
        # captionBottom < 900). Every shipped split scene carries 1000, but
        # only via the bespoke build_*.py scripts — the generic path emitted
        # nothing and died in validation (found 2026-08-25, same
        # generic-path-vs-bespoke-path family as the style/captionStyle
        # hardcodes above). Default it; a shot may still override.
        if scene.get("type") == "split":
            scene.setdefault("captionBottom", 1000)
        # A keyword CTA draws a 207px word centred at 67% of the frame, so the
        # caption has to sit ABOVE it — at the default the two overlapped and
        # the last beat rendered the caption THROUGH the keyword (2026-08-25).
        # The reference keeps its caption near mid-frame with the keyword
        # below; 880 puts the caption's bottom edge at y=1040 (54%), clear of
        # the keyword's top edge at y=1182.
        if (scene.get("type") == "commentcta"
                and scene.get("variant") == "keyword"):
            scene.setdefault("captionBottom", 880)
        # SEVERAL THINGS TO READ IS A READ, NOT A FRAME (2026-09-02).
        #
        # Two document components exist and nothing ever chose between them.
        # ReceiptScene frames ONE region and pushes 5%. SourceRead fits the
        # page to frame width and SCROLLS between the lines as they land.
        # Measured on the rendered pixels, displacement over one second
        # mid-scene:
        #
        #     sourceread   15.0 - 16.5      (footage reference: 12.9 - 17.3)
        #     receipt       0.97 - 4.7
        #
        # claude-fable-5-1 used `receipt` sixteen times and `sourceread` never,
        # which is why it reads as a slideshow of stills — the user's "no
        # zooming or scrolling effects", measured.
        #
        # The principled line: a document carrying TWO OR MORE highlights has
        # two or more things to read, and a component that frames one region
        # can only shrink to fit both. Reading them in sequence is what
        # SourceRead is for. 17 of 90 receipt scenes in this repo are that
        # shape. `keepReceipt` opts out for a page where the two marks really
        # are one glance.
        hls = scene.get("highlights") or []
        if scene.get("type") == "receipt" and len(hls) >= 2 \
                and not scene.get("keepReceipt"):
            dur = float(scene.get("durationSec") or 0) or 2.5
            # spread the landings across the beat, leaving the tail to settle
            span = max(0.6, dur - 0.9)
            scene["type"] = "sourceread"
            scene["lines"] = [
                {"at": round(0.5 + (span * n / max(1, len(hls) - 1)), 2),
                 "x": h.get("x", 0), "y": h.get("y", 0),
                 "w": h.get("w", 0), "h": h.get("h", 0)}
                for n, h in enumerate(hls)
            ]
            scene.pop("highlights", None)
            scene.setdefault("follow", True)
            print(f"  shot {index}: receipt with {len(hls)} highlights -> "
                  f"sourceread, read in sequence. It scrolls; a receipt does "
                  f"not. Set \"keepReceipt\": true to frame it as one glance.")

        # A CAPTION MUST NOT SIT ON THE WORDS THE RECEIPT IS HIGHLIGHTING
        # (2026-09-02). Only `split` and `commentcta` ever got a caption lane,
        # so a receipt used the global fallback and landed wherever that put
        # it — on claude-fable-5-1 that meant "banned" printed across the
        # yellow highlight it was describing, and the credit chip printed
        # across the line under it. Two text systems fighting over the same
        # band, which is the failure G58's "one text system at a time" note
        # already describes for typecards.
        #
        # ReceiptScene centres the highlight union at frame centre, so the
        # clear lane is below it; reel_gates.receipt_caption_bottom mirrors
        # that geometry and test_gates pins the two together.
        if scene.get("type") in ("receipt", "sourceread") \
                and "captionBottom" not in scene:
            from reel_gates import receipt_caption_bottom
            scene["captionBottom"] = receipt_caption_bottom(scene)
        # WHAT IS THE VIEWER LOOKING AT? (2026-09-02)
        #
        # `surface` answers the one question that decides whether an asset
        # belongs inside a device frame, and it is DECLARED because it cannot
        # be measured. The obvious guess — "1080x1920 means a phone screen
        # recording" — is wrong: 8 of the 32 exactly-1080x1920 clips in this
        # repo are iphone18-colors' Pantone chip graphics, and a bezel around
        # a colour swatch lies about what is on screen. The manifest's existing
        # `kind` could not carry this: it is already a mix of media type and
        # provenance (clip / receipt / still / coded-graphic / brand /
        # first-party-product-video), so a new asset's `kind` says nothing
        # about how it should be framed.
        #
        #   screen   a device UI recording -> deviceframe. "go do this."
        #   graphic  full-frame designed art -> full bleed. "look at this."
        #   world    real-world footage -> full bleed. "look at this."
        #
        # FORCED, with an explicit escape hatch, exactly like the zoomDir hold
        # above: the whole reason to record a screen is to show the phone, and
        # a full-bleed UI recording was the user's own complaint on
        # chatgpt-stickers ("didn't use real iPhone mockup"). An author who
        # genuinely wants a screen recording full-bleed writes
        # `"fullBleed": true` on the scene and this leaves it alone. Advice was
        # tried for exactly one reel and ignored, which is this repo's whole
        # recurring lesson.
        surface = str((asset or {}).get("surface") or "")
        if surface and surface not in ("screen", "graphic", "world"):
            raise SystemExit(
                f"shot {index}: asset {asset_id!r} declares surface "
                f"{surface!r} — must be 'screen', 'graphic' or 'world'")
        if surface == "screen" and scene.get("type") == "footage" \
                and not scene.get("fullBleed"):
            src_keep = scene.get("src")
            scene["type"] = "deviceframe"
            scene["kind"] = "phone"
            scene.pop("zoomDir", None)      # a device card keeps its push
            if src_keep:
                scene["src"] = src_keep
            print(f"  shot {index}: asset {asset_id!r} is a screen recording "
                  f"-> deviceframe(phone). Set \"fullBleed\": true on the "
                  f"scene to keep it full-frame.")
        if scene.pop("fullBleed", None) and surface == "screen":
            print(f"  shot {index}: screen recording held FULL BLEED by "
                  f"explicit fullBleed — the UI will not sit in a phone.")

        if asset:
            scene.setdefault("assetId", str(asset_id))
            scene.setdefault("claimId", str(shot.get("claim_id", asset_id)))
            # RULE 3 / G39 — the line this visual illustrates.
            #
            # It is the shot's own anchor, and that is the whole point: a
            # phrase-anchored shot was DEFINED by the words it sits under before
            # anyone went looking for footage, so `covers` here is evidence, not
            # a restatement of whatever happened to be said over a finished
            # scene. That inversion is why deriving it is legitimate here and
            # circular in tools/link_shots.py, which has to work backwards from
            # reels that were hand-assembled without a plan.
            anchor = str(shot.get("start_phrase", "")).strip()
            if anchor:
                scene.setdefault("covers", anchor)
            if asset.get("source_url"):
                scene.setdefault("sourceUrl", asset["source_url"])
            if (
                asset.get("credit")
                and scene.get("creditOnScreen") is not True
                and scene["type"] in {
                    "footage",
                    "receipt",
                    "floatcard",
                    "split",
                }
            ):
                # creditOnScreen (2026-08-25): the scene declares its frame
                # names the source itself, so the manifest credit must not be
                # re-injected here — popping `credit` from the plan did
                # nothing while this setdefault put it straight back.
                scene.setdefault("credit", asset["credit"])
        for media_key, trim_key in (
            ("src", "from"),
            ("bottomSrc", "bottomFrom"),
            ("topSrc", "topFrom"),
            ("bgSrc", "bgFrom"),
        ):
            if scene.get(media_key) == avatar_rel and trim_key not in scene:
                scene[trim_key] = round(start, 3)
        # A SCALE ON A FRAME-WIDTH CAPTURE CUTS ITS TEXT (2026-08-25). A mobile
        # capture is 1080 wide — exactly the frame — so any zoom above ~1.15
        # pushes words off both edges. On the editor's pass a `zoom: 1.5` meant
        # to make a README claim readable did the opposite: it chopped the
        # claim in half. Frame a full-width capture with `from` and `focusY`
        # (which slice, at 1:1) instead of scale. Advice at compile time, where
        # the asset's real width is already known.
        if (scene.get("type") == "footage" and float(scene.get("zoom", 1)) > 1.15
                and scene.get("src") and scene["src"] != avatar_rel):
            info = media_info(public / scene["src"])
            if info and info.get("width", 0) and info["width"] <= 1080:
                print(f"  ADVICE shot {index}: zoom {scene['zoom']} on a "
                      f"{int(info['width'])}px-wide capture — at frame width, "
                      f"scale crops text off both edges. Use `from`/`focusY` "
                      f"to choose the slice instead.")
        # A RECEIPT WITHOUT `highlights` GETS A GENERIC PUSH, NOT A POINT
        # (2026-09-01). ReceiptScene does a real focus pull — zooming onto the
        # highlight cluster as it fires — but ONLY when highlights exist. With
        # none it ken-burns the whole page, which frames nothing in particular.
        # 57% of receipts across the reels have none, because nothing ever
        # asked for them. The rect cannot be inferred here: knowing WHERE on
        # the page the claim sits needs someone to look at the image, which is
        # what the scout step is for.
        # A PUSH ON AN EXACT-FIT SCREEN RECORDING CROPS THE UI (2026-09-01).
        # FootageScene defaults to `zoomDir ?? "in"`, a 1.1x push. That is right
        # for b-roll, where a slow move keeps a static shot alive. It is WRONG
        # for a screen recording already delivered at exactly 1080x1920: the
        # push cuts ~10% off every edge, and the first casualty is the header
        # or status bar at the top of the screen. Found on chatgpt-stickers,
        # where "Create an image" was sliced in half on a recording that had
        # fit the frame perfectly.
        #
        # Forced rather than advised: the whole point of a UI recording is to
        # see the UI, and the crop is invisible in a beat sheet. Set an explicit
        # `zoom` if a tighter frame is genuinely wanted.
        if scene.get("type") == "footage" and scene.get("src") \
                and scene["src"] != avatar_rel and scene.get("zoomDir") != "none":
            info = media_info(public / scene["src"])
            if info and (info.get("width"), info.get("height")) == (1080, 1920):
                scene["zoomDir"] = "none"
                print(f"  ADVICE shot {index}: {scene['src'].split('/')[-1]} is "
                      f"exactly 1080x1920 — a push would crop the UI, so "
                      f"zoomDir is held at 'none'. Use `zoom` to reframe "
                      f"deliberately.")
                # Once `surface` is declared the author has ANSWERED this
                # question, and repeating it is noise — which is how a repo
                # full of advisories teaches people to skip advisories.
                if not surface:
                    print(f"  ADVICE shot {index}: IF this is a phone SCREEN "
                        f"RECORDING, `deviceframe` (kind 'phone') reads as "
                        f"a real handset and keeps its push, because the push "
                        f"scales the device CARD and cannot crop the UI. "
                        f"Full-bleed footage has to choose between motion and "
                        f"a whole screen; a device frame does not. IF it is a "
                        f"full-frame motion graphic or vertical b-roll, leave "
                        f"it full-bleed — 1080x1920 does NOT mean 'screen': "
                        f"iphone18-colors has 8 Pantone chip graphics at "
                        f"exactly this size, and a bezel around a colour "
                        f"swatch would be a lie about what is on screen.")

        if scene.get("type") == "deviceframe" and scene.get("zoomDir") == "none":
            # THE EXACT-FIT RULE ABOVE DOES NOT TRANSFER HERE (2026-09-01).
            # A device push scales the phone CARD inside the frame, so it has
            # no edge to crop — unlike full-bleed footage, where the same push
            # eats 10% of the screen. chatgpt-stickers pinned all 17 device
            # shots to 'none' by carrying the footage rule across, and the
            # frame linter caught it as two identical consecutive scenes.
            scene.pop("zoomDir")
            print(f"  ADVICE shot {index}: deviceframe was pinned to "
                  f"zoomDir 'none' — released. A device push moves the card, "
                  f"not a crop window, so it cannot cut the UI. A frozen "
                  f"device makes consecutive shots of one screen identical.")

        if scene.get("type") == "receipt" and not scene.get("highlights"):
            print(f"  ADVICE shot {index}: receipt with no `highlights` — the "
                  f"scene will push the whole page instead of pulling to the "
                  f"claim. Add a highlight rect around the words this beat "
                  f"covers ({str(scene.get('covers',''))[:40]!r}).")
        if scene.get("src") == avatar_rel and scene.get("type") == "footage":
            scene.setdefault("focusX", focus_full)
        if scene.get("bottomSrc") == avatar_rel:
            scene.setdefault("bottomFocusX", focus_split)
        scenes.append(scene)

    # THE VIDEO MUST COVER THE WHOLE AUDIO TRACK. `audio_end` is the last WORD
    # onset, so any trailing silence in the master was left uncovered and the
    # reel cut to black before the audio stopped — validate_job rejects a scene
    # total that differs from the track by more than 0.20s.
    # Found 2026-08-21 on iphone18-colors: last word 70.04s, master 70.44s.
    # Only the FINAL beat is extended, so nothing else in the plan moves.
    if audio_dur and scenes:
        spare = float(audio_dur) - audio_end
        if spare > 0.01:
            scenes[-1]["durationSec"] = round(
                scenes[-1]["durationSec"] + spare, 3)
            audio_end = float(audio_dur)

    # Keep INTERIOR SPACES when normalising the key. Stripping every non
    # alphanumeric collapsed "dark cherry" to "darkcherry", which matches no
    # single token and no chunk — so multi-word corrections silently did
    # nothing. Single-word keys are unaffected (they contain no space).
    corrections = {
        re.sub(r"[^a-z0-9 ]", "", str(key).lower()).strip(): str(value)
        for key, value in plan.get("caption_corrections", {}).items()
    }
    # The bed comes from config.json, not from a filename typed in here.
    # This defaulted to "music/bed-726.mp3", which is not in public/music — so
    # the generic path produced a sheet that validate_job rejected for a
    # missing asset every time (found 2026-08-22).
    default_bed = "music/bed-02.mp3"
    try:
        default_bed = json.loads((engine / "config.json").read_text()) \
            .get("defaults", {}).get("musicBed", default_bed)
    except Exception:  # noqa: BLE001
        pass
    # STANDING RULE (2026-08-24, user directive): reels ship voice + SFX only,
    # no music bed, by default — this flips what used to sit here (a bed was
    # always auto-built when the plan said nothing). Precedent: airpods-camera
    # (2026-08-18, "logged as a per-video call, not a standing rule") and
    # iphone18-colors-nomusic (2026-08-21) both shipped noMusic by request
    # before this made it the default. See RULES.md §8 / STYLE-RULES.md.
    # A plan opts a reel back into a bed with `"music": true` (locked default
    # bed) or its own full music object; `plan["noMusic"]`/`noMusicReason` are
    # still honoured verbatim if a plan sets them itself.
    plan_music = plan.get("music")
    music = None
    if plan_music is True:
        music = {
            "src": default_bed,
            "from": 0,
            "points": [
                {"t": 0, "vol": 0.11},
                {"t": max(0, audio_end - 0.8), "vol": 0.11},
                {"t": round(audio_end, 3), "vol": 0.0},
            ],
        }
    elif isinstance(plan_music, dict):
        music = plan_music

    no_music = plan.get("noMusic")
    no_music_reason = plan.get("noMusicReason")
    if music is None and not no_music:
        no_music = True
        no_music_reason = no_music_reason or (
            "Standing rule (2026-08-24 user directive): reels ship voice + "
            "SFX only, no music bed by default. Set plan[\"music\"] = true "
            "(or a full music object) to opt this reel back into a bed."
        )

    beats = {
        "id": slug,
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "style": locked_style(engine),
        "audio": audio_rel,
        "captionStyle": locked_caption_style(engine),
        "emphasis": plan.get("emphasis", []),
        "scenes": scenes,
        "captions": caption_words(words, corrections),
    }
    if music:
        beats["music"] = music
    elif no_music:
        beats["noMusic"] = True
        beats["noMusicReason"] = no_music_reason
    # FORMAT changes the gate physics (news / top5 / comparison), and this
    # compiler never emitted it — so every reel built here was judged as `news`
    # whatever it actually was. noCredits is the user's per-reel call on
    # on-screen attribution (RULES.md 2c) and likewise had no way through.
    # Both are pass-throughs: absent from the plan, the sheet is unchanged.
    for passthrough in ("format", "noCredits", "sides", "allowLong",
                        "allowLongReason", "captionStyle",
                        "captionStyleReason"):
        if plan.get(passthrough) is not None:
            beats[passthrough] = plan[passthrough]
    # STYLE FOLLOWS FORMAT (CLAUDE.md locked table: editorial = news,
    # comparison · utility = top5, ai-tools). locked_style() reads the
    # config default (editorial), which silently mis-dressed every utility-
    # format reel built on the generic path — claude-eating-tokens rendered
    # a full ai-tools reel in the editorial pack before anyone noticed
    # (2026-08-25). A plan may still pin "style" explicitly.
    # CREDIT INSTRUCTIONS (framework §2/§3) — the brief decides whether a
    # credit is DRAWN; the manifest always records provenance either way.
    # Scaffolded 2026-08-26 and read by nothing until now, which is the same
    # defect as the style mapping: a field nobody reads is a decision nobody
    # made. "internal"/"none" sets noCredits with the brief as its reason, so
    # G47 still refuses a silent switch-off.
    try:
        _brief = json.loads((engine / f"jobs/{slug}/brief.json").read_text())
        _ci = str(_brief.get("credit_instructions", "on-screen")).lower()
        if _ci in ("internal", "none", "internal only") and "noCredits" not in beats:
            beats["noCredits"] = {
                "reason": f"brief.credit_instructions = {_ci!r} "
                          "(framework §3: provenance stays in the manifest)"}
    except (OSError, ValueError):
        pass
    if plan.get("style"):
        beats["style"] = plan["style"]
    elif beats.get("format") in ("top5", "ai-tools"):
        beats["style"] = "utility"
    # G27 — the sheet carries the narration it was built from plus the approval
    # hash. Without these the gate blocks, and it is right to: a sheet that
    # cannot name the script it came from cannot prove the user approved it.
    # The bespoke tools/build_<slug>.py scripts set this themselves; this
    # generic path never did, so every reel compiled here failed G27.
    # Found 2026-08-21 on iphone18-colors.
    script_path = engine / f"jobs/{slug}/script.md"
    approval_path = engine / f"jobs/{slug}/approval.json"
    if script_path.exists():
        beats["script"] = script_path.read_text().strip()
    if approval_path.exists():
        beats["approval"] = json.loads(approval_path.read_text())
    output = engine / f"src/beats/{slug}.json"
    output.parent.mkdir(parents=True, exist_ok=True)

    # Refuse to shrink an existing beat sheet without being told to.
    #
    # Found the hard way 2026-08-17: compiling a 2-shot test plan silently
    # replaced a finished 47-scene sheet, taking its `covers` links and its
    # derived music curve with it. Recovering from git was luck — the sheet
    # happened to be committed. A compile that can quietly delete an evening's
    # work needs to say so first.
    if output.exists() and "--force" not in sys.argv:
        try:
            prev = json.loads(output.read_text()).get("scenes", [])
        except (OSError, json.JSONDecodeError):
            prev = []
        if len(prev) > len(scenes):
            raise SystemExit(
                f"{output.relative_to(engine)} already has {len(prev)} scenes and "
                f"this plan compiles only {len(scenes)}.\n"
                "Refusing to overwrite: the existing sheet may carry `covers` "
                "links, a derived music curve, or hand-tuned beats.\n"
                "Re-run with --force if replacing it is what you meant."
            )

    output.write_text(json.dumps(beats, indent=2, ensure_ascii=False) + "\n")
    print(f"compiled {len(scenes)} shots, {audio_end:.3f}s: {output}")


if __name__ == "__main__":
    main()
