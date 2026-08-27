#!/usr/bin/env python3
"""SessionStart: actually run the two commands CLAUDE.md says to run first.

"First two commands, every session" was prose, and prose gets skipped — a
missing dependency once silently disabled the frame checks for weeks. This
runs doctor at session start and reports the result into context, so a broken
toolchain is known before the first edit rather than after the first render.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# RE-ENTRANCY GUARD. doctor runs tools/test_hooks.py, which exercises this
# hook, which would run doctor again — an infinite loop that only ends on
# nested timeouts. It shipped, and the very next session start reported
# "doctor timed out (>110s)" for a check that takes 15 seconds alone.
# The variable is set on the doctor we launch and inherited by everything
# underneath it, so any nested copy of this hook reports instead of recursing.
GUARD = "AIRE_PREFLIGHT_RUNNING"


def main() -> int:
    if os.environ.get(GUARD):
        json.dump({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "Session preflight: already inside a doctor "
                                 "run (re-entrancy guard) — not re-running.",
        }}, sys.stdout)
        return 0

    env = {**os.environ, GUARD: "1"}
    try:
        proc = subprocess.run(
            [sys.executable, "scripts/doctor.py"], env=env,
            cwd=REPO, capture_output=True, text=True, timeout=110)
        out = (proc.stdout or "") + (proc.stderr or "")
        summary = [ln.strip() for ln in out.splitlines()
                   if ln.strip().startswith("doctor ")]
        verdict = summary[-1] if summary else f"doctor exited {proc.returncode}"
        if proc.returncode != 0:
            fails = [ln.strip() for ln in out.splitlines()
                     if "[fail]" in ln.lower() or "FAIL" in ln][:6]
            body = ("DOCTOR FAILED at session start. Fix this before anything "
                    "else — a broken toolchain silently disables gates.\n  "
                    + "\n  ".join(fails or [verdict]))
        else:
            body = f"Session preflight: {verdict}"
    except subprocess.TimeoutExpired:
        body = "Session preflight: doctor timed out (>110s). Run it manually."
    except Exception as exc:                                  # noqa: BLE001
        body = f"Session preflight: could not run doctor ({exc})."

    json.dump({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": body,
    }}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
