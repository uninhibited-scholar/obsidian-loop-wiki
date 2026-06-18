#!/usr/bin/env bash
# Demo recording aid for obsidian-loop-wiki.
#
# It stages the demo-vault so the Obsidian graph starts SPARSE, waits for you to
# begin screen-recording, then reveals the compiled nodes in waves so the graph
# visibly "grows" into a network — then runs the verifier as a closing shot.
#
# It only MOVES files in and out of demo-vault/.demo_stash/ and always restores
# them, even on Ctrl-C. It does not delete or alter any note content.
#
# Usage:  bash demo/stage-reveal.sh
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VAULT="$REPO/demo-vault"
STASH="$VAULT/.demo_stash"
# Reveal order: entities first, then concepts, then the comparison + MOC hub last
# so the map node visibly ties everything together at the end.
WAVE1=("entities")
WAVE2=("concepts")
WAVE3=("comparisons" "moc")
ALL=("${WAVE1[@]}" "${WAVE2[@]}" "${WAVE3[@]}")

restore() {
  # Move everything back from the stash, no matter how we exit.
  if [ -d "$STASH" ]; then
    for d in "${ALL[@]}"; do
      if [ -d "$STASH/$d" ]; then
        mkdir -p "$VAULT/$d"
        mv "$STASH/$d"/*.md "$VAULT/$d"/ 2>/dev/null || true
      fi
    done
    rm -rf "$STASH"
  fi
}
trap restore EXIT

echo "==> Staging demo-vault into a sparse starting state..."
mkdir -p "$STASH"
for d in "${ALL[@]}"; do
  mkdir -p "$STASH/$d"
  mv "$VAULT/$d"/*.md "$STASH/$d"/ 2>/dev/null || true
done

cat <<EOF

The graph is now sparse (only the raw source + control files remain).

Now, in this order:
  1. Switch to Obsidian (demo-vault open, Graph View showing, dark theme).
  2. Confirm the graph looks nearly empty.
  3. START your screen recorder (capture the Obsidian window only).
  4. Come back here and press ENTER to begin the reveal.

EOF
read -r -p "Press ENTER when recording is rolling... " _

reveal_wave() {
  for d in "$@"; do
    if [ -d "$STASH/$d" ]; then
      mkdir -p "$VAULT/$d"
      mv "$STASH/$d"/*.md "$VAULT/$d"/ 2>/dev/null || true
    fi
  done
}

echo "==> Wave 1: entities"
reveal_wave "${WAVE1[@]}"; sleep 1.6
echo "==> Wave 2: concepts"
reveal_wave "${WAVE2[@]}"; sleep 1.6
echo "==> Wave 3: comparison + MOC hub"
reveal_wave "${WAVE3[@]}"; sleep 2.0

echo
echo "==> Verifying the grown vault (closing shot):"
python3 "$REPO/scripts/verify_wiki.py" "$VAULT" || true

echo
echo "Done. Let the graph settle for ~2s, then STOP recording."
echo "(Files are already restored to their normal place.)"
