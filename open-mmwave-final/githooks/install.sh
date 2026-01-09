#!/usr/bin/env bash
set -e

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel)"

echo "Installing git hooks for open-mmwave..."
echo ""

# Set hooks path
git config core.hooksPath "$HOOK_DIR"

# Make executable
chmod +x "$HOOK_DIR/pre-commit" "$HOOK_DIR/commit-msg"

# Set author identity
git config user.name "baxter-barlow"
echo "Set git user.name: baxter-barlow"

# Check if .git-author exists for email
if [ -f "$REPO_ROOT/.git-author" ]; then
	AUTHOR_EMAIL=$(sed -n '2p' "$REPO_ROOT/.git-author" | tr -d '\r\n')
	if [ -n "$AUTHOR_EMAIL" ] && [ "$AUTHOR_EMAIL" != "your-email@example.com" ]; then
		git config user.email "$AUTHOR_EMAIL"
		echo "Set git user.email: $AUTHOR_EMAIL"
	fi
fi

# Verify .gitignore has required patterns
echo ""
echo "Checking .gitignore..."

REQUIRED_IGNORES=(
	"sprr*/"
	"swrr*/"
	"swru*.pdf"
	"CODEX_SESSION_PHASE*.md"
)

MISSING_IGNORES=""
for pattern in "${REQUIRED_IGNORES[@]}"; do
	if [ -f "$REPO_ROOT/.gitignore" ]; then
		if ! grep -qF "$pattern" "$REPO_ROOT/.gitignore"; then
			MISSING_IGNORES="$MISSING_IGNORES $pattern\n"
		fi
	else
		MISSING_IGNORES="$MISSING_IGNORES $pattern\n"
	fi
done

if [ -n "$MISSING_IGNORES" ]; then
	echo "⚠️ Missing from .gitignore:"
	echo -e "$MISSING_IGNORES"
	echo "Add these patterns to prevent committing private files."
fi

echo ""
echo "✓ Hooks installed"
echo ""
echo "Current git identity:"
echo " user.name: $(git config user.name)"
echo " user.email: $(git config user.email 2>/dev/null || echo '[not set]')"
echo ""
echo "Remote:"
echo " $(git remote -v | head -1)"
echo ""
echo "Hooks enforce:"
echo " ✗ BLOCK: Vendor refs (names, part numbers, SDKs)"
echo " ✗ BLOCK: Copying language (copying, mirror)"
echo " ✗ BLOCK: Private files (sprr*, swrr*, session logs)"
echo " ✗ BLOCK: Secrets, large files"
echo " ⚠ WARN: AI patterns, indentation, marketing fluff"
echo ""
echo "To bypass (use sparingly): git commit --no-verify"
