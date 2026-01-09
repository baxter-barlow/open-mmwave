# Contributing to open_mmwave

Thanks for your interest in improving open_mmwave. This repository is public and sanitization rules are strict.

## Quick Start
- Open the KiCad project at `kicad/open_mmwave.kicad_pro`.
- Read `docs/INDEX.md` for documentation entry points.
- Use `docs/bringup_revG.md` for validation guidance.

## Contribution Workflow
1. Create a branch from `main`.
2. Make focused changes and keep commits small and descriptive.
3. Run checks before committing:
   - ERC: `kicad-cli sch erc kicad/open_mmwave.kicad_sch --output erc_report.txt`
   - CI baseline: `python tools/ci_pipeline.py --baseline data/ci_baseline.json`
4. Open a pull request with a clear summary and any verification results.

## Sanitization Rules
Do not add vendor names, part numbers, or references to development platforms or SDKs. Use generic descriptions based on function.

## Repository Hygiene
- Do not commit local reference materials or session logs.
- Keep generated data in `data/` and `release/` sanitized.
