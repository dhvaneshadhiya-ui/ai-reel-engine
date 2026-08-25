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
            out[-1]["norm"] = normalize(out[-1]["text"])[-1]
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
            out[-1]["norm"] = normalize(out[-1]["text"])[-1]
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

    # MULTI-WORD corrections. The per-word pass above keys on a single token
    # with punctuation stripped, so a two-word product name ("dark cherry")
    # silently did nothing — and mapping the words separately is wrong, because
    # "dark" is also an ordinary word earlier in this script ("in the dark").
    # Phrase keys are therefore applied to the CHUNK text, after chunking.
    phrase_fixes = {k: v for k, v in corrections.items() if " " in k}

    chunks: list[dict[str, Any]] = []
    for index in range(0, len(corrected), 3):
        group = corrected[index : index + 3]
        chunks.append(
            {
                "start": round(group[0]["start"], 3),
                "end": round(group[-1]["end"], 3),
                "text": _apply_phrases(
                    " ".join(item["text"] for item in group), phrase_fixes
                ),
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
            if asset.get("credit") and scene["type"] in {
                "footage",
                "receipt",
                "floatcard",
                "split",
            }:
                scene.setdefault("credit", asset["credit"])
        for media_key, trim_key in (
            ("src", "from"),
            ("bottomSrc", "bottomFrom"),
            ("topSrc", "topFrom"),
            ("bgSrc", "bgFrom"),
        ):
            if scene.get(media_key) == avatar_rel and trim_key not in scene:
                scene[trim_key] = round(start, 3)
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
