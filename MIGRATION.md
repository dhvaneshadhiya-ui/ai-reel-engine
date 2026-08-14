# Setup guide — before, during, and after

Moving the engine to another Mac, or standing it up for the first time.

**Two equivalent routes, given side by side throughout.** Pick either, or mix
them — setting up in Terminal and then working in the app is normal, and is
what this project has mostly done.

| | |
|---|---|
| **APP** — the Claude desktop app | You describe what you want; the agent runs the commands and reads results back. No paths to think about. |
| **CLI** — Terminal | You run the same commands yourself. Useful for scripting the move or running it over SSH. Identical results — the agent runs exactly these commands. |

Either way, **making a reel happens in a conversation**, so the app is involved
eventually even if you set up entirely from Terminal.

Every number and expected output below was captured from a working machine on
2026-08-14, not written from memory.

---

## PART 1 — Before you start, on the CURRENT Mac

### 1.1 Confirm the source machine is actually healthy

Never copy a broken install — whatever is wrong here travels.

**APP** — with the conversation's folder set to the engine:
> Run the pre-migration checks.

**CLI**
```bash
cd ~/Movies/ai-reel-engine
python3 scripts/doctor.py
python3 tools/test_gates.py
```

Expected: `doctor ok — toolchain complete.` and
`all 57 checks passed — every gate fires on its violation.`

If either fails, fix it **before** building the archive.

### 1.2 Write down the state you will compare against

| Thing | This machine, 2026-08-14 |
|---|---|
| Gates | **33**, with **57** self-tests |
| Skills | **20** |
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

**APP**
> Build the migration archive to my Desktop.

**CLI**
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

**Included on purpose:** `bin/ffmpeg` and `bin/ffprobe`. Static x86_64 builds —
native on Intel, Rosetta on Apple Silicon — so the new Mac needs no Homebrew
and no password.

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

**You do NOT need:** Homebrew, ffmpeg, whisper, yt-dlp, Playwright, or any paid
tool. Bundled or installed automatically.

### 2.2 What will not travel, and must be redone

1. **The HeyGen connector** — it lives in the Claude app, not the repo. No
   credentials are in `config.json`; it holds only avatar and voice IDs.
2. **Your HeyGen credit balance** — one shared pool on the account, not
   per-machine. Check it before generating anything.
3. **Per-reel footage and renders** — see 1.3.

---

## PART 3 — Setup

### 3.1 Copy the archive across

`ai-reel-engine-migrate.tar.gz` — AirDrop, USB, cloud. Same on both routes.

### 3.2 Unpack it and place it

**APP / Finder** — double-click the file; Finder unpacks `ai-reel-engine`.
Drag it into `Movies`, or anywhere. No path is hardcoded.

**CLI**
```bash
mkdir -p ~/Movies && cd ~/Movies
tar -xzf ~/Desktop/ai-reel-engine-migrate.tar.gz
cd ai-reel-engine
```

### 3.3 Install everything

**APP** — open a conversation with its folder set to that folder, and say:
> Set this machine up — read MIGRATION.md and do it.

Approve the permission prompts.

**CLI**
```bash
bash setup.sh
```

Same script either way; it ends by running doctor and the full gate self-test.

### 3.4 Reconnect HeyGen

In the Claude app's connector settings. **Identical on both routes** — the
connector belongs to the app, not the repo.

### 3.5 Point Claude at the folder

Even if you set up from Terminal, the work happens in a conversation whose
folder is the engine. `CLAUDE.md` loads automatically. Then name a topic.

### 3.6 What `setup.sh` does, in order

1. `npm install` — Remotion and dependencies
2. `pip install pillow openai-whisper yt-dlp`
3. `npx playwright install chromium` — for page capture
4. **whisper `base` model**, fetched with `curl` and **checksum-verified** —
   the sha256 is the URL's own path segment, so a wrong or corrupt download
   fails loudly instead of silently degrading transcription
5. **bundled ffmpeg + ffprobe** copied into `~/.local/bin`, and that path added
   to `~/.zshrc` — no sudo, no Homebrew
6. `doctor.py`, then the full gate self-test

### 3.7 Why whisper is fetched with curl

On the source machine, whisper's own downloader fails with
`CERTIFICATE_VERIFY_FAILED: self-signed certificate`. Diagnosed 2026-08-14:
something on that Mac **intercepts TLS** (a proxy or security agent), and
Python's bundled `certifi` store does not carry that root — while `curl` uses
the system keychain and succeeds. Verified the same day: `python3 urllib` fails
on that URL, `curl -sI` returns `200`.

**This is machine-specific.** A clean Mac may have no such interception and
whisper's own downloader would work. `setup.sh` uses `curl` unconditionally
because it is correct either way, and the sha256 in the URL makes it
verifiable.

It matters because the error *looks* like a network outage and is not — without
this note it costs an afternoon.

---

## PART 4 — After setup: verify it works

Six checks.

**APP**
> Verify the setup.

**CLI**
```bash
python3 scripts/doctor.py
python3 tools/test_gates.py
python3 tools/sfx_library.py --check
python3 tools/reel_gates.py --formats
ls .claude/skills | wc -l
npx tsc --noEmit -p .
```

What each one is actually telling you:

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
[  ok  ] reel_gates self-test  — all 57 checks passed

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
`all 57 checks passed — every gate fires on its violation.`

**Proves:** every gate still fires on its own violation. A gate that never
triggers is worse than no gate.

### 4.3 The content libraries

```bash
python3 tools/sfx_library.py --check     # 16 cues, all present
python3 tools/reel_gates.py --formats    # news / top5 / comparison
ls .claude/skills                        # 20 entries
```

**Proves:** the sound files, format profiles and all 20 skills arrived. A
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
| `ffmpeg not on PATH` | `~/.local/bin` not on PATH yet | New terminal session, or re-run `setup.sh` |
| Skills missing in Claude | folder not set, or `.claude/` lost when unpacking | Confirm `.claude/skills` has 20 entries. Finder hides dot-folders — press ⌘⇧. |
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
ffmpeg and ffprobe are bundled; only Node and Python are installed by hand,
both normal double-click installers. Nothing is licensed to a machine, and no
credentials are stored in the repo.

**Windows?** The Python and Node parts are cross-platform, but the shell
scripts and paths assume macOS or Linux. Use WSL, or port them.

**Can I keep working on the old Mac too?** Yes — but see Part 6.

**Do I need the terminal at all?** No — every command here can be run for you by
the agent. But both routes are documented above because they are equally valid,
and Terminal is better when you want to script the move or watch raw output.
