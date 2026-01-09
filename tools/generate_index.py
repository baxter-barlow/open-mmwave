#!/usr/bin/env python3
"""Generate repository index for tools, docs, and data."""
from __future__ import annotations

import argparse
from pathlib import Path


def list_files(root: Path, exts: tuple[str, ...]) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.suffix in exts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    tools = list_files(Path("tools"), (".py",))
    docs = list_files(Path("docs"), (".md",))
    data = list_files(Path("data"), (".json", ".csv"))

    Path("docs/INDEX.md").write_text(
        "# Repository Index\n\n"
        + "## Tools\n" + "\n".join(f"- {p}" for p in tools) + "\n\n"
        + "## Docs\n" + "\n".join(f"- {p}" for p in docs) + "\n\n"
        + "## Data\n" + "\n".join(f"- {p}" for p in data) + "\n"
    )
    Path("docs/TOOLS.md").write_text(
        "# Tools\n\n" + "\n".join(f"- {p}" for p in tools) + "\n"
    )
    Path("docs/DATA_CATALOG.md").write_text(
        "# Data Catalog\n\n" + "\n".join(f"- {p}" for p in data) + "\n"
    )
    if not Path("README.md").exists():
        Path("README.md").write_text(
            "# mmwave_hardware\n\nGenerated index in `docs/INDEX.md`.\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
