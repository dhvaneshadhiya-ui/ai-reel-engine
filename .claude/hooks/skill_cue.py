#!/usr/bin/env python3
"""PostToolUse(Bash): turn a printed SKILL CUE into an actual instruction.

Our tools print `SKILL CUE: ... `social` ...` when a finding needs a skill.
A printed line is not a trigger — the agent has to notice it, and for weeks
it did not (the humanizer never ran once).  This hook reads the tool output
and injects an instruction the agent cannot scroll past.

Input : PostToolUse JSON on stdin.
Output: hookSpecificOutput.additionalContext, or nothing at all.
"""
import json
import re
import sys
from pathlib import Path

MAX_CONTEXT = 1200

# A cue must be EMITTED by a run, not quoted by one. Reading the source that
# contains a cue (grep, sed, cat) fired the hook while this file was being
# written — the same class of false positive that made guard_bypass block its
# own test. Inspection commands are excluded at the first segment.
READERS = re.compile(
    r"^(?:sudo\s+)?(grep|rg|ag|sed|cat|head|tail|less|more|awk|bat|"
    r"diff|wc|strings|open)\b")


# Commands that produce NO stdout of their own, so they cannot be the source of
# a cue and must not count against an otherwise-inspection command.
#
# `cd` is the one that mattered (2026-09-02). Every command in this repo is
# written as `cd "<repo>"` followed by the real work, so `cd` failed the
# all-readers test and EVERY inspection command defeated the guard — the very
# false positive this function was written for fired routinely for a week, most
# recently on a `sed` that printed G23's help text and cued `reel-analyzer`
# when no gate had fired. `echo` is deliberately NOT here: it emits arbitrary
# text and so could legitimately carry a cue.
NEUTRAL = re.compile(r"^(?:cd|pwd|true|:)\b|^cd$")


def is_inspection(command: str) -> bool:
    """True when the command only READS files that may quote a cue."""
    segments = [s.strip().lstrip("({ \t")
                for s in re.split(r"(?:\n|;|&&|\|\||\|)", command)]
    runnable = [s for s in segments if s and not NEUTRAL.match(s)]
    return bool(runnable) and all(READERS.match(s) for s in runnable)


def installed_skills() -> set:
    names = set()
    for root in (Path(__file__).resolve().parents[1] / "skills",
                 Path.home() / ".agents" / "skills",
                 Path.home() / ".claude" / "skills"):
        try:
            for d in root.iterdir():
                if (d / "SKILL.md").exists():
                    names.add(d.name)
        except OSError:
            pass
    return names


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0

    if is_inspection(payload.get("tool_input", {}).get("command", "")):
        return 0

    blob = json.dumps(payload.get("tool_response", ""))
    # Unescape so backticked names survive the json.dumps round trip.
    text = blob.encode().decode("unicode_escape", "ignore")

    cued, known = [], installed_skills()
    for line in text.splitlines():
        if "SKILL CUE" not in line:
            continue
        # A cue names its skills in backticks; keep only ones that exist.
        for name in re.findall(r"`([a-z0-9][a-z0-9-]{2,40})`", line):
            if name in known and name not in cued:
                cued.append(name)

    # Cues wrap, so also sweep the two lines after each cue marker.
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "SKILL CUE" in line:
            for follow in lines[i + 1:i + 4]:
                for name in re.findall(r"`([a-z0-9][a-z0-9-]{2,40})`", follow):
                    if name in known and name not in cued:
                        cued.append(name)

    # A FAILING media command is its own trigger. `ffmpeg-ytdlp` holds the
    # measured recipes and the macOS arch trap, and no tool of ours prints a
    # cue for it because the failure happens in ffmpeg, not in our code.
    media = re.search(r"\b(ffmpeg|ffprobe|yt-dlp|youtube-dl)\b",
                      payload.get("tool_input", {}).get("command", ""))
    broke = re.search(r"(incompatible architecture|command not found|"
                      r"Unknown encoder|Invalid argument|No such filter|"
                      r"Conversion failed|Error opening|error while|"
                      r"Unable to (find|extract))", text, re.I)
    if media and broke and "ffmpeg-ytdlp" in known and "ffmpeg-ytdlp" not in cued:
        cued.append("ffmpeg-ytdlp")

    if not cued:
        return 0

    listed = ", ".join(f"`{n}`" for n in cued[:5])
    msg = (
        f"SKILL TRIGGER (from the tool you just ran): {listed}.\n"
        "That tool found something these skills exist to fix. Invoke them now "
        "with the Skill tool, before writing or revising the thing they cover. "
        "If one genuinely does not apply here, say in one line why you skipped it "
        "— do not skip silently, which is the failure this hook was built to stop."
    )[:MAX_CONTEXT]

    json.dump({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": msg,
    }}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
