#!/usr/bin/env python3
"""Suggest cost optimizations based on alternative components."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alts", type=Path, required=True, help="Alternative components JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        json.loads(args.alts.read_text())
        return 0

    alts = json.loads(args.alts.read_text())
    suggestions = []
    for comp, info in alts.get("alternatives", {}).items():
        if not info.get("alternatives"):
            suggestions.append({"component": comp, "suggestion": "find second source"})
    args.out.write_text(json.dumps({"suggestions": suggestions}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
