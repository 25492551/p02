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

# Prefer repo-local SSH key if present (no global SSH config needed).
if [[ -f "git/id_ed25519" ]]; then
  chmod 600 "git/id_ed25519" 2>/dev/null || true
  chmod 644 "git/id_ed25519.pub" 2>/dev/null || true
  mkdir -p "git" 2>/dev/null || true
  # Ensure GitHub host key is present (avoid interactive prompt).
  ssh-keyscan -H github.com >> "git/known_hosts" 2>/dev/null || true
  export GIT_SSH_COMMAND="ssh -i git/id_ed25519 -o IdentitiesOnly=yes -o UserKnownHostsFile=git/known_hosts -o StrictHostKeyChecking=accept-new"
fi

git add -A

if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

TS_UTC="$(date -u +%Y-%m-%dT%H%M%SZ)"
git commit -m "sync: ${TS_UTC}"

echo "Force pushing to origin/${BRANCH} (with lease)."
git push --force-with-lease -u origin "HEAD:${BRANCH}"

