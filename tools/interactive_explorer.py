#!/usr/bin/env python3
"""Simple interactive explorer for data files."""
from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    data_dir = Path("data")
    files = sorted(p for p in data_dir.glob("*.json"))
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    if not files:
        return 0
    choice = input("Select file number: ").strip()
    if not choice.isdigit():
        return 0
    idx = int(choice) - 1
    if idx < 0 or idx >= len(files):
        return 0
    print(files[idx].read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
