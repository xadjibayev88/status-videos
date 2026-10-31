#!/usr/bin/env bash
# Installs OpenMontage (github.com/calesthio/OpenMontage, AGPL-3.0) next to this office repo,
# with the office's free-only settings. Run once on your own computer:
#   bash tools/openmontage/install.sh
# Needs: git, Python 3.10+, Node.js 18+, FFmpeg.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="${OPENMONTAGE_DIR:-$HOME/OpenMontage}"
PIN="195eab2"   # version reviewed by the office on 2026-10-31

if [ ! -d "$DEST/.git" ]; then
  git clone https://github.com/calesthio/OpenMontage "$DEST"
fi
git -C "$DEST" checkout -q "$PIN" 2>/dev/null || echo "note: pinned version not found, staying on the latest"

# free-only settings: budget 0, hard cap, vertical output
cp "$HERE/config.free.yaml" "$DEST/config.yaml"

cd "$DEST"
make setup
echo
echo "OpenMontage is ready in $DEST (budget capped at \$0: free stock, local TTS and local rendering only)."
echo "Open that folder in Claude Code and describe the video you want."
