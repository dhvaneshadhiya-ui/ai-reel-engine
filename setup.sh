#!/usr/bin/env bash
# Bootstrap the engine on a fresh machine or cloud sandbox.
#   bash setup.sh
set -euo pipefail

echo "== node deps =="
npm install

echo "== python deps =="
python3 -m pip install --quiet --upgrade pillow openai-whisper yt-dlp

echo "== playwright chromium (page capture) =="
npx playwright install chromium

echo "== whisper base model =="
# This machine's TLS breaks whisper's own downloader; curl is reliable and the
# URL path segment IS the expected sha256, so it is verifiable.
CACHE="$HOME/.cache/whisper"; mkdir -p "$CACHE"
if [ ! -f "$CACHE/base.pt" ]; then
  URL="https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt"
  curl -fsSL -o "$CACHE/base.pt" "$URL"
  EXPECT=$(echo "$URL" | awk -F/ '{print $(NF-1)}')
  ACTUAL=$(shasum -a 256 "$CACHE/base.pt" | cut -d' ' -f1)
  [ "$EXPECT" = "$ACTUAL" ] || { echo "checksum mismatch"; exit 1; }
  echo "  base.pt verified"
fi

echo "== ffmpeg =="
# Bundled static builds are an x86_64 CONVENIENCE, not a guarantee. They are
# unsigned, so on Apple Silicon under current macOS, XProtect DELETES them the
# first time they run -- silently, including the copy inside ./bin. Verified
# 2026-08-16: bin/ffmpeg vanished mid-setup on an arm64 Mac (Darwin 25.3.0).
# So: copy them, then PROVE they run. If they do not, fall through to brew.
if [ -x "./bin/ffmpeg" ] && ! command -v ffmpeg >/dev/null; then
  mkdir -p "$HOME/.local/bin"
  cp -f ./bin/ffmpeg ./bin/ffprobe "$HOME/.local/bin/"
  chmod +x "$HOME/.local/bin/ffmpeg" "$HOME/.local/bin/ffprobe"
  export PATH="$HOME/.local/bin:$PATH"
  # PATH must go in .zshenv, NOT .zshrc: zsh reads .zshrc only for INTERACTIVE
  # shells, and the agent runs every pipeline command non-interactively. With
  # the line only in .zshrc, doctor.py reports "ffmpeg not on PATH" forever.
  if ! grep -q '.local/bin' "$HOME/.zshenv" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshenv"
    echo "  added ~/.local/bin to PATH in ~/.zshenv"
  fi
  if "$HOME/.local/bin/ffmpeg" -version >/dev/null 2>&1 \
  && "$HOME/.local/bin/ffprobe" -version >/dev/null 2>&1; then
    echo "  installed bundled ffmpeg + ffprobe (no Homebrew needed)"
  else
    echo "!! the bundled x86_64 ffmpeg will not run on this Mac"
    echo "   (unsigned binary removed or blocked by macOS -- expected on Apple Silicon)"
    rm -f "$HOME/.local/bin/ffmpeg" "$HOME/.local/bin/ffprobe"
    hash -r 2>/dev/null || true
  fi
fi
# The source machine ran a standalone static build from evermeet.cx dropped on
# PATH (not brew, not npm). On Apple Silicon that route is a dead end -- those
# builds are unsigned x86_64 and macOS deletes them -- so brew is the answer.
if ! command -v ffmpeg >/dev/null; then
  if command -v brew >/dev/null; then
    echo "  installing via Homebrew..."
    brew install ffmpeg
  else
    echo "!! ffmpeg not found and Homebrew is not installed."
    echo "   Install Homebrew (asks for your Mac password once), then re-run this:"
    # NOTE: the \$ is escaped on purpose. Unescaped, \$(curl ...) runs at echo
    # time and prints the entire Homebrew installer instead of the command.
    echo "     /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "     brew install ffmpeg"
    echo "   Homebrew gives a native, signed build. Unsigned static builds"
    echo "   (evermeet.cx and friends) are removed by macOS on Apple Silicon."
    exit 1
  fi
fi
command -v ffprobe >/dev/null || { echo "!! ffprobe missing — it ships with ffmpeg; if you installed a standalone ffmpeg, download ffprobe too"; exit 1; }

echo
echo "== verifying =="
python3 scripts/doctor.py
python3 tools/test_gates.py | tail -1
echo
echo "Ready. Start a reel:  see CLAUDE.md"
