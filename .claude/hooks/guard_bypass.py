#!/usr/bin/env python3
"""PreToolUse(Bash): refuse the three bypasses CLAUDE.md only asked for politely.

Each of these is a rule the repo already states in prose, and prose is exactly
what gets skipped at 2am. render_job.py's own internal call to remotion is a
subprocess, not a Bash tool call, so it is untouched by this hook — only a
direct hand-typed bypass is.

Matching is POSITIONAL, not substring. The first version matched anywhere in
the command and promptly blocked the commit that was writing this file's own
test, because the test quotes the commands it expects to be blocked. Talking
about a command is not running one, so a segment only counts when the binary
sits where a shell would actually execute it.
"""
import json
import re
import sys

# Only these can start a blocked invocation, so a quoted mention inside a
# heredoc or a Python list never reaches the patterns below.
LAUNCHERS = re.compile(r"^(?:sudo\s+|command\s+|time\s+)*"
                       r"(npx|npm|pnpm|yarn|bunx|node|git|hyperframes)\b")

# Split on anything that starts a fresh command in a shell.
SEGMENT = re.compile(r"(?:\n|;|&&|\|\||\||\$\(|`)")

# A heredoc body is DATA — the file being written, not commands being run.
# This is the third false positive of the same shape: the body has been a
# Python test quoting blocked commands, and a CLAUDE.md table describing them
# in a markdown row (whose pipes and backticks split into perfect fake
# commands). Text about a command is never a command.
HEREDOC = re.compile(r"<<-?\s*[\"']?(\w+)[\"']?")


def strip_heredocs(command: str) -> str:
    """Remove every heredoc body, keeping the lines that actually execute."""
    out, lines, i = [], command.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        marks = HEREDOC.findall(line)
        i += 1
        for delim in marks:
            while i < len(lines) and lines[i].strip() != delim:
                i += 1
            i += 1  # drop the closing delimiter too
    return "\n".join(out)

BLOCKS = (
    (re.compile(r"\bremotion\s+render\b", re.I),
     "Direct remotion render bypasses scripts/render_job.py, which runs doctor "
     "and reel_gates first. A render that skips the gates is exactly what the "
     "gates exist to prevent. Run: python3 scripts/render_job.py <slug>"),
    (re.compile(r"\bhyperframes\s+(render|init|check|doctor|lint)\b", re.I),
     "The HyperFrames pipeline knows nothing about G01-G52, the beat-sheet "
     "contract, script approval or the -14 LUFS master. HyperFrames is allowed "
     "to make ONE scene asset into public/assets/<slug>/; the reel is assembled "
     "and rendered by render_job.py. (CLAUDE.md, HyperFrames section.)"),
    (re.compile(r"^git\s+reset\s+--hard\b", re.I),
     "A parallel session may have pushed. The recorded rule is MERGE, never "
     "reset — a hard reset here has already cost another session's work once. "
     "Use: git pull --no-rebase, resolve, then push."),
    (re.compile(r"^git\s+push\b.*?\s(-f|--force)(?!-with-lease)\b", re.I),
     "Force-pushing discards whatever a parallel session pushed. The recorded "
     "rule is MERGE, never force. Use git pull --no-rebase, resolve, then push "
     "— or --force-with-lease if you have genuinely checked the remote."),
)


def segments(command: str):
    """Yield the parts of a command line where a binary would actually run."""
    for raw in SEGMENT.split(strip_heredocs(command)):
        seg = raw.strip().lstrip("({ \t")
        if seg and LAUNCHERS.match(seg):
            yield seg


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0
    if payload.get("tool_name") != "Bash":
        return 0

    for seg in segments(payload.get("tool_input", {}).get("command", "")):
        for pattern, reason in BLOCKS:
            if pattern.search(seg):
                json.dump({"hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }}, sys.stdout)
                return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
