#!/usr/bin/env bash
set -euo pipefail

# Force-push helper for this repository.
# Safer than plain --force: uses --force-with-lease.
#
# Usage:
#   03_script/99_git_force_push.sh [branch]
#
# Default branch: autosync (recommended to avoid rewriting main/master history)

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRANCH="${1:-autosync}"

cd "$REPO_ROOT"

git add -A

if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

TS_UTC="$(date -u +%Y-%m-%dT%H%M%SZ)"
git commit -m "sync: ${TS_UTC}"

echo "Force pushing to origin/${BRANCH} (with lease)."
git push --force-with-lease -u origin "HEAD:${BRANCH}"

