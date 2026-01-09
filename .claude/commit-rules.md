# Commit Rules & Code Style Guidelines — open-mmwave

Source of truth for all commits to https://github.com/baxter-barlow/open-mmwave

## CRITICAL: Public Repository Rules

This is a **PUBLIC** repository. All committed content must comply with these rules.

### Forbidden Content (BLOCKING)

**Vendor References — NEVER COMMIT:**
- Vendor company names or trademarks
- Vendor-specific part numbers or device families
- Vendor SDK or tool names
- Vendor document identifiers
- Evaluation or development platform references
- Vendor reference design identifiers

**Copying Language — NEVER COMMIT:**
- "copying," "copyingd," "cloning"
- "mirror original," "copying language"
- "matched baseline board"
- "identified as [vendor part]"
- "from the development platform"

**Private Files — NEVER COMMIT:**
- `local_vendor_docs*/`, `local_vendor_docs.pdf` (component datasheet)
- `CODEX_SESSION_PHASE*.md` (session logs)
- `*.private.md`, `*.private.txt`

### Approved Replacements

| Forbidden | Use Instead |
|-----------|-------------|
| vendor company name | [omit entirely] |
| vendor part numbers | "mmWave frontend IC" / "radar SoC" |
| evaluation kit terms | "development platform" / "reference board" |
| copying language | "build" / "develop" / "implement" |
| copying | "implement" / "create" |
| matched baseline | "verified against specifications" |

### Pre-Commit Check

Before every commit:
```bash
# Check staged content for forbidden terms
git diff --cached | rg -i "copying|mirror|copying language|development platform"
# ^^^ MUST return empty

# Verify private files not staged
git status
# local_vendor_docs*, CODEX_SESSION_PHASE* should NOT appear
```

---

## Code Style

### Indentation
- **Tabs only** for indentation (all languages)
- Remove trailing whitespace
- LF line endings
- Max 2 consecutive blank lines

### Comment Style

**Remove AI patterns:**
- "This function...", "This method...", "This class..."
- "Note that...", "Please note...", "It's worth noting..."
- Hedging: "might", "could potentially", "appears to"
- Decorative headers: `# --- Section ---` or `// =====`
- Verbatim narration of the next line

**Good comment style:**
- Terse, assumes reader competence
- Explain *why*, not *what*
- TODO/FIXME markers where appropriate
- No period at end of single-line comments

### Variable Naming
- Concise but meaningful
- Avoid verbose AI-style: `userInputStringFromCommandLine` → `user_input`
- Trust reader to follow standard patterns

---

## Commit Messages

**Natural language style:**
```
Add power supply schematic
Fix UART buffer overflow in radar_comm
Update BOM with alternative capacitors
Clean up DSP filtering code
```

**NOT acceptable:**
```
feat(power): add supply schematic # No conventional commits
🎉 Add new feature # No emoji
Added the schematic for power # Use imperative mood
Implement blazingly fast processing # No marketing language
Fix development platform issue # No vendor refs!
```

**Format:**
- First line: imperative mood, <50 chars ideal, <72 max
- Blank line before body (if needed)
- Body: wrap at 72 chars

---

## Documentation

### README Style
- Factual, technical tone
- No marketing fluff: "powerful," "seamless," "cutting-edge"
- No emoji bullet lists
- No "Made with ❤️" footers
- Max 3 badges (functional only)

### Hardware Documentation
- State confidence levels: [High/Med/Low]
- Reference datasheet pages
- Document assumptions explicitly
- Note what's verified vs inferred

---

## Pre-Commit Checklist

Before every commit:

1. [ ] `git config user.name` shows `baxter-barlow`
2. [ ] No vendor references in staged content
3. [ ] No RE language in staged content
4. [ ] Private files (local_vendor_docs*, sessions) not staged
5. [ ] Tabs for indentation
6. [ ] No AI comment patterns
7. [ ] Natural commit message (no feat:, no emoji)
8. [ ] No files >1MB

---

## Bypassing Hooks

```bash
git commit --no-verify -m "Message"
```

**Use ONLY when:**
- Emergency fix needed immediately
- False positive from hook
- Approved by project owner

**NEVER use to bypass:**
- Vendor reference checks
- Private file checks
- Author identity checks
