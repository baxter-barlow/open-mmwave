# Session Objective

Integrate version control safeguards into the existing `~/mmwave_hardware` project, connecting it to the public `open-mmwave` repository with strict content filtering.

# Repository

**URL:** https://github.com/baxter-barlow/open-mmwave
**Working Directory:** ~/mmwave_hardware
**Owner:** baxter-barlow

# Git Identity (Verify First)

```bash
cd ~/mmwave_hardware
git config user.name "baxter-barlow"
git config user.email "YOUR_EMAIL"
git remote -v # Should show github.com/baxter-barlow/open-mmwave
```

If remote is not set:
```bash
git remote add origin https://github.com/baxter-barlow/open-mmwave.git
# or
git remote set-url origin https://github.com/baxter-barlow/open-mmwave.git
```

# Tasks

## 1. Install Git Hooks

Copy the provided hooks to `.githooks/`:

```bash
mkdir -p .githooks
# Copy pre-commit, commit-msg, install.sh from provided files
chmod +x .githooks/*
./.githooks/install.sh
```

The hooks will:
- **BLOCK:** Vendor references (, radar SoC, etc.)
- **BLOCK:** Copying language (copying, mirror)
- **BLOCK:** Private files (sprr*, swrr*, session logs)
- **BLOCK:** Secrets, files >1MB
- **WARN:** AI patterns, indentation, marketing language

## 2. Update .gitignore

Ensure `.gitignore` includes these critical patterns:

```gitignore
# PRIVATE - NEVER COMMIT
sprr*/
swrr*/
swru*.pdf
TI_*/
CODEX_SESSION_PHASE*.md
*_SESSION_*.md
*.private.md
```

**Verify private files are ignored:**
```bash
git status
# local_vendor_docs/, local_vendor_docs/, local_vendor_docs/, local_vendor_docs.pdf, CODEX_SESSION_PHASE*.md
# should NOT appear in output
```

If they appear as untracked, the .gitignore is working. If they appear as tracked, remove them:
```bash
git rm --cached -r local_vendor_docs/ local_vendor_docs/ local_vendor_docs/
git rm --cached local_vendor_docs.pdf
git rm --cached CODEX_SESSION_PHASE*.md
```

## 3. Create Supporting Directories

```bash
mkdir -p .claude .codex .prompts
```

- `.claude/` — Claude audit reports, session state
- `.codex/` — Codex audit outputs
- `.prompts/` — Archived prompts

## 4. Create .git-author

```bash
echo "baxter-barlow" > .git-author
echo "YOUR_EMAIL@example.com" >> .git-author
```

## 5. Update CLAUDE.md

Add this section to existing `CLAUDE.md`:

```markdown
## Repository

**URL:** https://github.com/baxter-barlow/open-mmwave
**All commits by:** baxter-barlow

## Content Rules

This is a PUBLIC repository. All committed content must be FREE of:
- , references
- Specific part numbers (radar SoC, etc.)
- "copying" or "mirror" language
- References to development platforms or commercial development platforms

**Local reference only (GITIGNORED):**
- `local_vendor_docs/`, `local_vendor_docs/`, `local_vendor_docs/`, `local_vendor_docs.pdf`
- `CODEX_SESSION_PHASE*.md`

## Before Committing

```bash
# Check for forbidden content
git diff --cached | rg -i "copying|mirror|copying language"
# Must return empty!

# Verify author
git config user.name # must be: baxter-barlow
```
```

## 6. Verify Setup

```bash
# Test hook installation
git config core.hooksPath # Should show .githooks

# Test author
git config user.name # Should show baxter-barlow

# Test gitignore
git status # Private files should not appear

# Test hooks (dry run)
echo "test reference" > /tmp/test.txt
git add /tmp/test.txt
git commit -m "Test" # Should be BLOCKED by hooks
git reset HEAD /tmp/test.txt
rm /tmp/test.txt
```

## 7. Create Commit Rules

Create `.claude/commit-rules.md` with project-specific rules (copy from provided template).

# File Structure After Setup

```
~/mmwave_hardware/
├── .git-author # baxter-barlow identity
├── .githooks/
│ ├── pre-commit # Vendor/RE content filter
│ ├── commit-msg # Message style enforcement
│ └── install.sh
├── .gitignore # Updated with private patterns
├── .claude/
│ ├── commit-rules.md
│ ├── SESSION_STATE.md
│ └── AUDIT_*.md
├── .codex/
├── .prompts/
├── CLAUDE.md # Updated with repo rules
├── CODEX_SESSION_PROMPT.md
├── README.md
│
├── [COMMITTED - PUBLIC]
│ ├── kicad/
│ ├── simulation/
│ ├── tools/
│ ├── docs/
│ ├── data/
│ ├── templates/
│ └── release/
│
└── [GITIGNORED - LOCAL ONLY]
 ├── local_vendor_docs/
 ├── local_vendor_docs/
 ├── local_vendor_docs/
 ├── local_vendor_docs.pdf
 ├── CODEX_SESSION_PHASE*.md
 └── data_sheets/ (review before commit)
```

# Acceptance Criteria

- [ ] Git hooks installed and functional
- [ ] `git config user.name` returns `baxter-barlow`
- [ ] `git remote -v` shows `github.com/baxter-barlow/open-mmwave`
- [ ] Private files (sprr*, swrr*, session logs) are gitignored
- [ ] `git status` does not show private files
- [ ] Test commit with "" is blocked by hooks
- [ ] `.claude/`, `.codex/`, `.prompts/` directories exist
- [ ] CLAUDE.md updated with repo rules

# Do NOT

- Commit any component documentation
- Commit session logs (CODEX_SESSION_PHASE*.md)
- Remove private files from disk (just gitignore them)
- Use `--no-verify` to bypass hooks
