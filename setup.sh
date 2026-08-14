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
# whisper's own downloader fails on the source machine with
# "CERTIFICATE_VERIFY_FAILED: self-signed certificate" — i.e. something is
# intercepting TLS (a proxy or security agent) and Python's bundled certifi
# store does not carry that root, while curl uses the system keychain and
# succeeds. This is MACHINE-SPECIFIC: a clean Mac may not need the workaround.
# curl is used unconditionally because it is correct either way, and the URL's
# path segment IS the expected sha256, so the download is verifiable.
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
# Bundled static builds ship in the migration archive so a new Mac needs no
# Homebrew, no password and no terminal work. Link them into ~/.local/bin,
# which needs no sudo, and put that on PATH for future shells.
if [ -x "./bin/ffmpeg" ] && ! command -v ffmpeg >/dev/null; then
  mkdir -p "$HOME/.local/bin"
  cp -f ./bin/ffmpeg ./bin/ffprobe "$HOME/.local/bin/"
  chmod +x "$HOME/.local/bin/ffmpeg" "$HOME/.local/bin/ffprobe"
  export PATH="$HOME/.local/bin:$PATH"
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; esac
  if ! grep -q '.local/bin' "$HOME/.zshrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    echo "  added ~/.local/bin to PATH in ~/.zshrc"
  fi
  echo "  installed bundled ffmpeg + ffprobe (no Homebrew needed)"
fi
# The source machine ran a standalone static build from evermeet.cx dropped on
# PATH (not brew, not npm). On a new Mac, brew is the least fiddly route.
if ! command -v ffmpeg >/dev/null; then
  if command -v brew >/dev/null; then
    echo "  installing via Homebrew..."
    brew install ffmpeg
  else
    echo "!! ffmpeg not found and Homebrew is not installed."
    echo "   Either:  /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\" && brew install ffmpeg"
    echo "   Or:      download static builds of ffmpeg AND ffprobe from"
    echo "            https://evermeet.cx/ffmpeg/  and put both on your PATH"
    echo "            (this machine keeps them in ~/.npm-global/bin)."
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
