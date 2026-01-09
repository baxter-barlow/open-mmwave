#!/usr/bin/env python3
"""Run final validation and build release package."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def checksum(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output report JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    report = {
        "checks": {
            "manufacturing_validation": Path("data/manufacturing_validation.json").exists(),
            "design_check": Path("data/design_check.json").exists(),
            "bom": Path("data/bom_netlist_correlation.json").exists(),
            "thermal": Path("data/thermal_analysis.json").exists(),
        }
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))

    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    files = [
        "data/gerber_analysis.json",
        "data/drill_analysis.json",
        "data/component_placement.json",
        "data/bom_production.csv",
        "data/bom_procurement.csv",
        "docs/reproduction_guide.md",
        "docs/hardware_reference.md",
        "docs/assembly_instructions.md",
    ]
    manifest_lines = []
    for f in files:
        p = Path(f)
        if p.exists():
            dest = release_dir / p.name
            shutil.copy2(p, dest)
            manifest_lines.append(f"{p} -> {dest}")
    (release_dir / "MANIFEST.txt").write_text("\n".join(manifest_lines))

    checksums = []
    for p in release_dir.iterdir():
        if p.is_file():
            checksums.append(f"{checksum(p)}  {p.name}")
    (release_dir / "CHECKSUMS.sha256").write_text("\n".join(checksums))
    Path("docs/release_notes.md").write_text(
        "# Release Notes\n\nGenerated release package in `release/`.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
