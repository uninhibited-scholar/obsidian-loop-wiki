#!/usr/bin/env bash
# Install the obsidian-loop-wiki skill for Claude Code.
# Copies skill/ into ~/.claude/skills/loop-wiki/ so Claude Code can trigger it.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skill"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/loop-wiki"

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "error: $SRC/SKILL.md not found — run this from the repo root." >&2
  exit 1
fi

mkdir -p "$DEST"
cp -R "$SRC/." "$DEST/"
chmod +x "$DEST/scripts/verify_wiki.py" 2>/dev/null || true

echo "Installed loop-wiki skill to: $DEST"
echo
echo "Next steps:"
echo "  1. export WIKI_PATH=\"\$HOME/MyVault\"   # point at your Obsidian vault"
echo "  2. In Claude Code, say: \"整理 inbox\" or \"ingest this article\""
echo
echo "Not a Claude Code user? Copy AGENTS.md into your project root instead."
