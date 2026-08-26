#!/usr/bin/env python3
"""Prove every .claude hook fires when it should and stays quiet when it should not.

A hook is the only thing in this repo that can make a SKILL run without a human
remembering to run it, so a silently broken hook removes the trigger and looks
exactly like nothing being wrong. Run by doctor.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOOKS = REPO / ".claude" / "hooks"
fails, checks = [], 0


def run(hook: str, payload: dict, env: dict | None = None) -> dict:
    proc = subprocess.run([sys.executable, str(HOOKS / hook)],
                          input=json.dumps(payload), capture_output=True,
                          text=True, timeout=130,
                          env={**os.environ, **(env or {})})
    if proc.returncode != 0:
        return {"__exit__": proc.returncode, "__err__": proc.stderr[-300:]}
    if not proc.stdout.strip():
        return {}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"__bad_json__": proc.stdout[:200]}


def ctx(out: dict) -> str:
    return out.get("hookSpecificOutput", {}).get("additionalContext", "")


def check(label: str, cond: bool, detail: str = "") -> None:
    global checks
    checks += 1
    if not cond:
        fails.append(f"{label}: {detail}")


def bash(cmd: str = "", stdout: str = "") -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": cmd},
            "tool_response": {"stdout": stdout, "stderr": ""}}


# ---- settings wiring -------------------------------------------------------
settings = json.loads((REPO / ".claude" / "settings.json").read_text())
wired = json.dumps(settings)
for event in ("SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse"):
    check(f"settings has {event}", event in settings["hooks"])
for hook in ("session_start.py", "reel_precedence.py", "guard_bypass.py",
             "skill_cue.py"):
    check(f"{hook} wired", hook in wired)
    check(f"{hook} exists", (HOOKS / hook).exists())

# ---- skill_cue -------------------------------------------------------------
real_cue = ("  SKILL CUE: packaging is written with the `social` and "
            "`caption-and-hashtags`\n  skills (and `youtube-seo` for the "
            "Shorts title/description).")
out = ctx(run("skill_cue.py", bash("python3 tools/prepublish.py x", real_cue)))
for name in ("social", "caption-and-hashtags", "youtube-seo"):
    check(f"cue names {name}", name in out, f"got: {out[:120]}")
check("cue is an instruction", "Skill tool" in out, out[:120])
check("cue forbids silent skip", "silently" in out)

check("wrapped cue lines are read",
      "humanizer" in ctx(run("skill_cue.py", bash(
          "python3 tools/script_doctor.py x",
          "  SKILL CUE: rewrite it with\n  the `humanizer` skill."))))

check("no cue -> silent", ctx(run("skill_cue.py", bash("ls", "file.txt"))) == "")

# Reading source that QUOTES a cue is not a cue. This fired for real while the
# hook was being written, on a sed that was only displaying the cue's own text.
for reader in ("sed -n '92,98p' tools/prepublish.py",
               "grep -rn 'SKILL CUE' tools/",
               "cat tools/script_doctor.py | head -40"):
    check(f"inspection ignored: {reader[:22]!r}",
          ctx(run("skill_cue.py", bash(reader, real_cue))) == "")
# ...but a real run that happens to pipe through a reader still counts.
check("run piped to grep still cues",
      "social" in ctx(run("skill_cue.py", bash(
          "python3 tools/prepublish.py x | grep -A3 CUE", real_cue))))
check("unknown skill name ignored",
      ctx(run("skill_cue.py", bash("x", "SKILL CUE: use `not-a-real-skill`"))) == "")
check("non-Bash ignored",
      ctx(run("skill_cue.py", {"tool_name": "Read",
                               "tool_response": "SKILL CUE: `humanizer`"})) == "")

# A FAILING media command triggers ffmpeg-ytdlp. Nothing of ours prints a cue
# for it, because the failure happens inside ffmpeg — including the macOS
# arch trap that skill exists to document.
check("failing ffmpeg cues ffmpeg-ytdlp",
      "ffmpeg-ytdlp" in ctx(run("skill_cue.py", bash(
          "ffmpeg -i a.mov -c:v libx264 out.mp4",
          "dyld: incompatible architecture (have 'x86_64', need 'arm64e')"))))
check("failing yt-dlp cues ffmpeg-ytdlp",
      "ffmpeg-ytdlp" in ctx(run("skill_cue.py", bash(
          "yt-dlp -f best https://x", "ERROR: Unable to extract video data"))))
check("succeeding ffmpeg stays quiet",
      ctx(run("skill_cue.py", bash("ffmpeg -i a.mov out.mp4",
                                   "video:1024kB audio:96kB muxing overhead"))) == "")
check("unrelated failure stays quiet",
      ctx(run("skill_cue.py", bash("python3 x.py", "Error opening file"))) == "")

# ---- reel_precedence -------------------------------------------------------
def prompt(text: str) -> str:
    return ctx(run("reel_precedence.py", {"prompt": text}))


fired = prompt("make me a reel about the new iPhone")
check("reel request fires", "news-reel" in fired, fired[:100])
check("names the hijack", "hyperframes" in fired and "FALSE" in fired)
check("carries approval rule", "G27" in fired)
check("carries no-terminal rule", "does not run terminal" in fired)
# PRODUCTION prompts — every one of these is a real request from this repo's
# history. Missing one of these is the expensive failure: the job goes to
# `social` or the hyperframes router and skips every gate.
PRODUCTION = [
    "write the script for the shorts video",
    "fix the voiceover",
    "make me a reel about the Gemini 3 launch",
    "Go ahead with the avatar generation",
    "Rewrite the hook as short sentences and re-render",
    "our system still generates very poor scripts",
    "Show me the final video when it's done",
    "captions must have transparent background",
    "Comment CTA should be like this video",
]
# MAINTENANCE prompts — also all real. The repo is NAMED "AI Reel Engine", so
# the word reel is in the housekeeping too. This exact prompt fired the hook
# before the filter was tightened.
MAINTENANCE = [
    "audit the repo wiring",
    "why did the gate fail",
    "explain how doctor works",
    "commit and push to github",
    "go through our entire AI Reel Engine thoroughly and make sure everything "
    "works fine, and everything (including skills) gets auto triggered at the "
    "right time",
    "Everything pushed to github repo so far?",
    "make sure the hooks fire at the right time",
    "Run the framework audit",
]
for text in PRODUCTION:
    check(f"fires on {text[:26]!r}", "news-reel" in prompt(text),
          "MISSED a production request")
for text in MAINTENANCE:
    check(f"quiet on {text[:26]!r}", prompt(text) == "", prompt(text)[:50])

# ---- guard_bypass ----------------------------------------------------------
BLOCKED = [
    "npx remotion render src/index.ts reel out/a.mp4",
    "cd /tmp && npx remotion render x y z",
    "npx hyperframes render",
    "hyperframes doctor",
    "git reset --hard origin/main",
    "git push -f origin main",
    "git push --force origin main",
]
ALLOWED = [
    "python3 scripts/render_job.py my-slug",
    "git push origin main",
    "git push --force-with-lease origin main",
    "python3 tools/reel_gates.py --formats",
    "ls out/",
    "git log --oneline -5",
    # A command that merely QUOTES a blocked one must still run — this is the
    # false positive that blocked this file's own first commit.
    "cat > t.py <<'PY'\nCMDS = [\"npx remotion render a b\"]\nPY",
    "grep -rn 'hyperframes render' docs/",
    # A markdown table INSIDE a heredoc: its pipes and backticks split into
    # perfect fake commands. This blocked the CLAUDE.md commit that documents
    # the guard. A heredoc body is data, never a command.
    ("python3 - <<'PY'\ns = '''| `guard_bypass.py` | denies `git reset --hard`"
     " and `npx remotion render` |'''\nPY\necho done"),
    "cat >> NOTES.md <<'MD'\nrun `git push --force` never\nMD",
    # ...and a real command AFTER a heredoc must still be seen.
]
BLOCKED_AFTER_HEREDOC = "cat > a.txt <<'EOF'\nharmless\nEOF\ngit reset --hard HEAD"


def decision(cmd: str) -> str:
    return run("guard_bypass.py", bash(cmd)).get(
        "hookSpecificOutput", {}).get("permissionDecision", "allow")


for cmd in BLOCKED:
    check(f"blocks {cmd[:30]!r}", decision(cmd) == "deny")
for cmd in ALLOWED:
    check(f"allows {cmd[:30]!r}", decision(cmd) == "allow")
check("real command after a heredoc still blocked",
      decision(BLOCKED_AFTER_HEREDOC) == "deny")

reason = run("guard_bypass.py", bash("npx remotion render a b c")).get(
    "hookSpecificOutput", {}).get("permissionDecisionReason", "")
check("block explains the fix", "render_job.py" in reason, reason[:80])

# ---- session_start ---------------------------------------------------------
# RE-ENTRANCY. doctor runs this file, which runs this hook, which runs doctor.
# That loop shipped and broke the next session's preflight, so the guard is
# tested rather than trusted — and this test runs UNDER the guard so it stays
# fast and cannot re-enter doctor itself.
GUARD = "AIRE_PREFLIGHT_RUNNING"
t0 = time.time()
guarded = ctx(run("session_start.py", {"hook_event_name": "SessionStart"},
                  env={GUARD: "1"}))
elapsed = time.time() - t0
check("guarded preflight does not re-run doctor", "re-entrancy" in guarded,
      guarded[:120])
check("guarded preflight returns immediately", elapsed < 10,
      f"took {elapsed:.1f}s")
src = (HOOKS / "session_start.py").read_text()
check("hook passes the guard to doctor",
      'GUARD: "1"' in src and "env=env" in src,
      "doctor would be launched unguarded")
check("hook checks the guard before running", "os.environ.get(GUARD)" in src)

# ---- report ----------------------------------------------------------------
if fails:
    print(f"hook self-test FAILED ({len(fails)} of {checks})")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print(f"hook self-test PASSED — {checks} checks, 4 hooks")
