#!/usr/bin/env python3
"""Turn the APPROVED script into a tagged script for ElevenLabs v3.

WHY THIS IS A SEPARATE ARTEFACT FROM script.md
----------------------------------------------
Tags must NOT live in `jobs/<slug>/script.md`. G27 hashes that text as the
approved narration and G21 verifies captions against it, so markup in there
would mean the user approves `[curious]` as if it were a word, and the caption
check compares against words nobody speaks. Tags are DELIVERY — the same
category as voiceSpeed — so they are generated FROM the approved script and
never folded back into it.

WHY THE TAGS ARE POSITIONAL
---------------------------
`vo_direct.py` already holds this repo's per-beat registers (hook / context /
build / turn / proof / payoff / cta) and the positional arc used when a line
carries no explicit register. This reuses both, so the emotional shape of a
read is the same idea whether it is rendered by HeyGen's TTS or by ElevenLabs.

ONLY DOCUMENTED ELEVENLABS TAGS ARE EMITTED. `[serious]`, `[emphatic]` and
`[slowly]` were invented in an earlier draft and are not in ElevenLabs' list;
an unrecognised tag is either spoken aloud or silently dropped, and both are
worse than no tag.

    python3 tools/vo_tagged.py <slug>
    python3 tools/vo_tagged.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

# PRONUNCIATION RESPELLINGS (2026-09-01). The same job HeyGen's brand glossary
# used to do — and which the move to external voice (config.json voice.mode
# 'external-mcp') silently took away, because a glossary only applies to audio
# HeyGen synthesises, never to an uploaded file. So an initialism that reads
# wrong now has nowhere to be recorded, and gets rediscovered per reel.
#
# EVERY ENTRY IS EARNED BY A PROBE, never by guessing how a word "should" sound.
#   DRAM: the qualcomm-chip-hike take read it as "drum" on two load-bearing
#   lines. whisper base AND small both transcribed "drum", so it was the audio,
#   not the transcriber (RULES.md section 11). A 16.8s probe (~243 credits)
#   compared D-RAM / DEE-ram / D.R.A.M.: all three transcribe as DRAM and all
#   three run 0.60-0.66s, so none is spelled out letter by letter. D-RAM is the
#   plainest and is what ships.
#
# The respelling lands ONLY in script-tagged.txt. script.md keeps the real
# word, so G27's approved hash, G21's caption check and G53's transcript match
# are all unaffected — whisper writes "DRAM" either way.
PRONOUNCE = {
    "DRAM": "D-RAM",
}


def respell(text: str) -> str:
    """Apply PRONOUNCE to whole words only, preserving surrounding punctuation."""
    for term, said in PRONOUNCE.items():
        text = re.sub(rf"\b{re.escape(term)}\b", said, text)
    return text


# Documented in ElevenLabs' v3 prompting guide. Mapped from OUR register names
# so the two engines describe the same performance.
TAG_FOR_REGISTER = {
    "hook":    "[curious]",
    "context": "[calm]",
    "build":   "[curious]",
    "turn":    "[surprised]",
    "proof":   "[calm]",
    "payoff":  "[excited]",
    "cta":     "[excited]",
}


def sentences(text: str) -> list[str]:
    """Split on sentence ends, keeping the punctuation."""
    body = " ".join(l for l in text.splitlines()
                    if l.strip() and not l.lstrip().startswith("#"))
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]


def tag_script(text: str) -> tuple[str, dict[str, int]]:
    import vo_direct
    arc, used = vo_direct.ARC, {}
    out, sents = [], sentences(text)
    for i, sent in enumerate(sents):
        # Same positional arc vo_direct uses, stretched over the sentence count.
        reg = arc[min(int(i / max(len(sents), 1) * len(arc)), len(arc) - 1)]
        tag = TAG_FOR_REGISTER.get(reg, "[calm]")
        # One tag per register RUN, not per sentence: a tag repeated on every
        # line reads as noise and ElevenLabs holds a tag until the next one.
        if out and out[-1][0] == tag:
            out.append((tag, sent, False))
        else:
            out.append((tag, sent, True))
            used[tag] = used.get(tag, 0) + 1
    lines = []
    for tag, sent, show in out:
        sent = respell(sent)
        lines.append(f"{tag} {sent}" if show else sent)
    return "\n\n".join(lines), used


def main() -> int:
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()
    if len(argv) != 1:
        print(__doc__.split("    python3")[0].strip())
        return 1
    slug = argv[0]
    src = ROOT / "jobs" / slug / "script.md"
    if not src.exists():
        sys.exit(f"\n  no {src.relative_to(ROOT)}\n")
    tagged, used = tag_script(src.read_text())
    out = ROOT / "jobs" / slug / "script-tagged.txt"
    out.write_text(tagged + "\n")

    print(f"\n=== tagged script — {slug} ===\n")
    print(tagged)
    print(f"\n  wrote {out.relative_to(ROOT)}")
    print(f"  tags used: {', '.join(f'{t}x{n}' for t, n in used.items())}")
    print("\n  SKILL CUE: generate this with the `news-reel` flow — "
          "creative_generate_speech,\n  model eleven_v3, voice id from "
          "config.json voice.elevenLabsVoiceId.\n  Then: python3 "
          "tools/vo_external.py " + slug + " <downloaded.mp3>\n")
    print("  The WORDS are identical to the approved script — only tags were\n"
          "  added — so G53 will still match the read against the approval.\n")
    return 0


def selftest() -> int:
    fails, checks = [], 0

    def ok(label: str, cond: bool, detail: str = "") -> None:
        nonlocal checks
        checks += 1
        if not cond:
            fails.append(f"{label}: {detail}")

    script = ("Claude keeps a file on you. It is the same file everywhere. "
              "You stop re-explaining yourself. But some subjects it leaves "
              "alone. Health and politics are off by default. That is the "
              "switch. The file did not go away. You just got the key.")
    tagged, used = tag_script(script)

    # THE ONE THAT MATTERS: stripping the tags must give back the exact words.
    # If tagging can alter a word, it breaks G53 and the approval chain.
    stripped = re.sub(r"\[[a-z ]+\]\s*", "", tagged)
    ok("words survive tagging unchanged",
       " ".join(stripped.split()) == " ".join(script.split()),
       "tagging altered the narration — this would break G53 and approval")

    # PRONUNCIATION RESPELLINGS ARE THE ONE ALLOWED EXCEPTION, AND THEY ARE
    # ONLY SAFE UNDER ONE CONDITION: the respelling must be the SAME LETTERS
    # with punctuation inserted. "DRAM" -> "D-RAM" is safe because whisper
    # transcribes it back to one token, DRAM, so G53's transcript match and
    # G21's caption check never see it. "DRAM" -> "dee ram" would NOT be: it
    # becomes two words in the transcript and drifts the approval match.
    # Without this check, the next entry added here could quietly break the
    # guarantee that the check above exists to protect.
    for term, said in PRONOUNCE.items():
        ok(f"respelling of {term!r} only inserts punctuation",
           re.sub(r"[^A-Za-z0-9]", "", said).lower() == term.replace(" ", "").lower(),
           f"{said!r} changes the letters of {term!r} — whisper would "
           "transcribe something the approved script does not say")
    ok("respell applies to a whole word only",
       respell("DRAM and DRAMATIC") == "D-RAM and DRAMATIC",
       "respell matched inside another word")
    ok("respell leaves an untouched script alone",
       respell("The phone ships Tuesday.") == "The phone ships Tuesday.")

    ok("something was tagged", bool(used), "no tags emitted at all")
    ok("only documented tags are used",
       set(used) <= set(TAG_FOR_REGISTER.values()),
       f"undocumented tag emitted: {set(used) - set(TAG_FOR_REGISTER.values())}")
    ok("tags are not repeated line after line",
       max(used.values()) <= len(sentences(script)),
       "a tag on every line is noise")
    ok("output has more than one distinct tag", len(used) > 1,
       f"only {used} — the read would have no arc")
    ok("registers come from vo_direct, not a private copy",
       set(TAG_FOR_REGISTER) == set(__import__("vo_direct").REGISTERS),
       "register names drifted from vo_direct")

    if fails:
        print(f"vo_tagged self-test FAILED ({len(fails)} of {checks})")
        for f in fails:
            print(f"  - {f}")
        return 1
    print(f"vo_tagged self-test PASSED — {checks} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
