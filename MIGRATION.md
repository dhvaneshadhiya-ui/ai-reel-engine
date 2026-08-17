# Setup guide — before, during, and after

Moving the engine to another Mac, or standing it up for the first time.
**You do not need the terminal.** Finder and the Claude desktop app are enough;
the agent runs the commands.

Every number and expected output below was captured from a working machine on
2026-08-14, not written from memory.

---

## PART 1 — Before you start, on the CURRENT Mac

Four things. In the Claude app, pointed at `~/Movies/ai-reel-engine`, say
*"run the pre-migration checks"* and it will do all of them.

### 1.1 Confirm the source machine is actually healthy

Never copy a broken install — whatever is wrong here travels.

```bash
python3 scripts/doctor.py
python3 tools/test_gates.py
```

Expected: `doctor ok — toolchain complete.` and
`all 64 checks passed — every gate fires on its violation.`

If either fails, fix it **before** building the archive.

### 1.2 Write down the state you will compare against

| Thing | This machine, 2026-08-14 |
|---|---|
| Gates | **33**, with **64** self-tests |
| Skills | **29** (20 + 9 hyperframes, added 2026-08-16) |
| Sound cues | **16** |
| Scene types | **42** |
| Formats | `news`, `top5`, `comparison` |
| Default avatar | `f55b0b7c` · digital twin · motion 4.41 · `avatar_v` |
| Voice speed | 1.05 |
| Runtime band | 60–80s (news) |
| Archive | ~57 MB |

### 1.3 Decide what to do about past reels

The archive excludes `public/assets/` (per-reel footage) and `out/` (renders).
Scripts, approvals and beat sheets DO travel.

- Want a finished reel on the new Mac? Copy that single `.mp4` from `out/`.
- Want to **re-render** an old reel? You also need its whole
  `public/assets/<slug>/` folder. Otherwise treat past reels as archived.

### 1.4 Build the archive

```bash
cd ~/Movies
tar --exclude=node_modules --exclude=out --exclude=_sources \
    --exclude='public/assets' --exclude='.claude/settings.local.json' \
    --exclude=.DS_Store --exclude=__pycache__ \
    -czf ~/Desktop/ai-reel-engine-migrate.tar.gz ai-reel-engine
```

3.5 GB of working directory becomes **~57 MB**, because everything excluded is
either regenerable or per-reel.

| Excluded | Size | Why |
|---|---|---|
| `node_modules/` | 603 MB | `npm install` rebuilds it |
| `out/` | 1.1 GB | finished renders |
| `_sources/` | 1.2 GB | raw scouted footage, re-fetchable |
| `public/assets/` | 716 MB | per-reel b-roll, mostly third-party |
| `.claude/settings.local.json` | — | this machine's permission list |

**`bin/` no longer exists in this copy, and an archive built here will not
contain it.** It once held static x86_64 `ffmpeg` and `ffprobe`, bundled so an
Intel Mac needed no Homebrew and no password.

> **That never worked on Apple Silicon.** Rosetta runs those builds, but they
> are *unsigned*, and current macOS deletes an unsigned binary the first time it
> executes — including the copy inside `bin/` itself. Verified 2026-08-16 on an
> arm64 Mac (Darwin 25.3.0): `bin/ffmpeg` disappeared mid-setup, no error and no
> log naming it. `bin/ffprobe` survived only because it was never run, and was
> then deleted deliberately as a useless orphan.
>
> **ffmpeg now comes from Homebrew** — native arm64, adhoc-signed, and it stays
> put. That costs **one password prompt** at Homebrew install (§2.1) and nothing
> after. `setup.sh` still handles a bundled `bin/` if you reintroduce one for an
> Intel target, but it now test-runs those binaries before trusting them and
> falls through to Homebrew when they fail.

---

## PART 2 — Before you start, on the NEW Mac

### 2.1 What must already exist

| Requirement | If missing |
|---|---|
| **macOS** | any recent version |
| **Node** | [nodejs.org](https://nodejs.org) — normal double-click installer |
| **Python 3** | python.org installer, or it arrives with developer tools |
| **Developer tools** | macOS prompts on first use — click **Install** |
| **Disk space** | ~3 GB free (node_modules, models, renders) |
| **Claude desktop app** | signed in to the same account |

**You do NOT need:** whisper, yt-dlp, Playwright, or any paid tool — installed
automatically.

**Homebrew: needed on Apple Silicon, not on Intel.** The bundled ffmpeg is
x86_64 and unsigned, so macOS removes it on an arm64 Mac (see §1.4). Check with
`uname -m`; if it says `arm64`, install Homebrew first — it is the one step
that asks for your Mac password:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

`setup.sh` then runs `brew install ffmpeg` for you.

### 2.2 What will not travel, and must be redone

1. **The HeyGen connector** — it lives in the Claude app, not the repo. No
   credentials are in `config.json`; it holds only avatar and voice IDs.
2. **Your HeyGen credit balance** — one shared pool on the account, not
   per-machine. Check it before generating anything.
3. **Per-reel footage and renders** — see 1.3.

---

## PART 3 — Setup

### 3.1 The five steps

1. **Copy** `ai-reel-engine-migrate.tar.gz` across — AirDrop, USB, cloud.
2. **Double-click it.** Finder unpacks `ai-reel-engine`.
3. **Drag the folder to `Movies`** — or anywhere. No path is hardcoded.
4. **Open the Claude desktop app**, start a conversation with its folder set to
   that folder, and say:

   > Set this machine up — read MIGRATION.md and do it.

   Approve the permission prompts.
5. **Reconnect HeyGen** in the app's connector settings.

### 3.2 What the agent does, in order

`bash setup.sh`:

1. `npm install` — Remotion and dependencies
2. `pip install pillow openai-whisper yt-dlp`
3. `npx playwright install chromium` — for page capture
4. **whisper `base` model**, fetched with `curl` and **checksum-verified** —
   the sha256 is the URL's own path segment, so a wrong or corrupt download
   fails loudly instead of silently degrading transcription
5. **ffmpeg + ffprobe** — the bundled pair is copied into `~/.local/bin` and
   then *test-run*. On Intel that is the end of it: no sudo, no Homebrew. On
   Apple Silicon the test fails (macOS has removed them), the dead copies are
   cleaned up, and `brew install ffmpeg` takes over. That path is added to
   **`~/.zshenv`, not `~/.zshrc`** — see §3.4
6. `doctor.py`, then the full gate self-test

### 3.3 Why whisper is fetched with curl

On the source machine, whisper's own model downloader fails with an SSL
certificate-chain error; `curl` works. Recorded because it looks like a network
problem and is not.

### 3.4 Why PATH goes in `.zshenv` and not `.zshrc`

zsh reads `~/.zshrc` **only for interactive shells**. The agent runs every
pipeline command non-interactively, so a PATH line living in `.zshrc` is
invisible to it: `doctor.py` reports `ffmpeg not on PATH` even though ffmpeg is
installed and a human typing `ffmpeg -version` in Terminal sees it work.
`~/.zshenv` is read by *every* zsh. Same class of failure as the missing
Pillow — the tool is there, the check just never sees it.

---

## PART 4 — After setup: verify it works

Six checks. Say *"verify the setup"* and the agent runs them.

### 4.1 The toolchain

```bash
python3 scripts/doctor.py
```

```
=== ai-reel-engine doctor ===
-- binaries --
[  ok  ] ffmpeg · ffprobe · node · yt-dlp · whisper
-- python modules --
[  ok  ] python:PIL          ← without this, pixel checks SILENTLY skip
[  ok  ] python:whisper
-- whisper models (cached) --
[  ok  ] whisper:base
-- node --
[  ok  ] node_modules  — remotion present
[  ok  ] playwright chromium
-- config --
[  ok  ] avatar  — Dhvanesh -- 59 (digital twin #2) · motion 4.41 · avatar_v
[  ok  ] defaults.lengthRangeSeconds  — 60-80s
-- sfx library --
[  ok  ] sfx catalogue  — 16 cues, all present.
-- gates --
[  ok  ] reel_gates self-test  — all 64 checks passed

doctor ok — toolchain complete.
```

**Proves:** binaries on PATH, Pillow present (its absence once disabled the
frame checks silently for weeks), models cached, config intact, avatar registry
survived the copy.

### 4.2 The rules

```bash
python3 tools/test_gates.py
```

Expect `33 gate ids, all unique`, then
`all 64 checks passed — every gate fires on its violation.`

**Proves:** every gate still fires on its own violation. A gate that never
triggers is worse than no gate.

### 4.3 The content libraries

```bash
python3 tools/sfx_library.py --check     # 16 cues, all present
python3 tools/reel_gates.py --formats    # news / top5 / comparison
ls .claude/skills                        # 29 entries
```

**Proves:** the sound files, format profiles and all 29 skills arrived. A
missing skill means the agent silently does not know the rules it carries.

### 4.4 The renderer

```bash
npx tsc --noEmit -p .
```

**Proves:** the Remotion components compile. The one check that needs
`npm install` to have finished.

### 4.5 HeyGen

Ask the agent for the current user. You should see the plan (`pro`) and the
remaining credits. An error means the connector is not attached to this
machine's Claude app yet.

### 4.6 A dry run that spends nothing

```bash
python3 tools/showrunner.py status <any-slug>
```

Reports pipeline state and stops at the first missing step. Nothing generated,
no credits spent — it confirms the orchestrator can read the repo.

---

## PART 5 — Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `DOCTOR FAILED — node_modules` | `npm install` did not run | Re-run `npm install` |
| `python:PIL` FAIL | Pillow missing | `pip3 install pillow`. **Do not ignore** — frame checks skip silently without it |
| `whisper:base missing` | model not fetched | Re-run `setup.sh`; it uses curl deliberately |
| `ffmpeg not on PATH` | `~/.local/bin` not on PATH yet | New terminal session, or re-run `setup.sh`. If a *human* sees ffmpeg work but doctor does not, the export is in `.zshrc` — move it to `.zshenv` (§3.4) |
| `bin/ffmpeg` has vanished from the repo | Apple Silicon. macOS deleted the unsigned x86_64 binary when it ran — no error, no log naming it | Expected, not a copy failure. `brew install ffmpeg` (§2.1). Re-copying it from the source Mac just gets it deleted again |
| ffmpeg "installed" but every command silently does nothing | same as above, caught mid-flight | `uname -m`; if `arm64`, use Homebrew |
| Skills missing in Claude | folder not set, or `.claude/` lost when unpacking | Confirm `.claude/skills` has 29 entries. Finder hides dot-folders — press ⌘⇧. |
| `news-reel` skill missing | unpacked from an archive older than 2026-08-14 | Skills are real directories now, not symlinks. Rebuild the archive |
| HeyGen calls fail | connector not attached here | Reconnect in the Claude app settings |
| `GATES FAILED` on an old reel | expected | Reels made before a gate existed can fail it. Do not retro-fix; the rule applies forward |
| A render looks wrong after the copy | `public/assets/<slug>/` was excluded | Copy that reel's assets, or treat it as archived |

---

## PART 6 — Keeping two machines honest

**Two copies drift.** `STYLE-RULES.md`, `config.json` and the gates diverge
silently — this project found **four stale-prose drifts in a single day on one
machine**. If both Macs will make reels:

- Put the repo on a **private git remote** and pull, rather than copying twice.
- `.gitignore` already excludes `node_modules/`, `out/`, `_sources/`,
  `public/assets/` and `bin/`, so a clone is small.
- `bin/` is excluded from git because 150 MB of binaries does not belong there;
  it ships only in the migration archive.

If you keep two independent copies anyway, treat **one as canonical** and
re-export the archive from it whenever the rules change.

---

## Answers to the obvious questions

**Is everything installable on a new machine?** Yes, and most is automatic.
Node and Python are installed by hand, both normal double-click installers. On
**Intel**, ffmpeg is bundled and nothing else is needed. On **Apple Silicon**,
add Homebrew — one command, one password prompt (§2.1). Nothing is licensed to
a machine, and no credentials are stored in the repo.

**Windows?** The Python and Node parts are cross-platform, but the shell
scripts and paths assume macOS or Linux. Use WSL, or port them.

**Can I keep working on the old Mac too?** Yes — but see Part 6.

**Do I need the terminal at all?** No. Every command here can be run for you by
the agent in the Claude app.
