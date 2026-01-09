#!/usr/bin/env python3
"""Analyze DFM risks from BOM and alternative components list."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import xlrd


def parse_bom(path: Path) -> Dict[str, Dict]:
    wb = xlrd.open_workbook(path.as_posix())
    sheet = wb.sheet_by_index(0)
    header_row = None
    headers = {}
    for row_idx in range(min(30, sheet.nrows)):
        row = [str(sheet.cell_value(row_idx, c)).strip().lower() for c in range(sheet.ncols)]
        if "designator" in row:
            header_row = row_idx
            for c, name in enumerate(row):
                headers[name] = c
            break
    if header_row is None:
        raise ValueError("Designator header not found")
    parts = {}
    for row_idx in range(header_row + 1, sheet.nrows):
        designators = str(sheet.cell_value(row_idx, headers["designator"])).strip()
        if not designators:
            continue
        desc = str(sheet.cell_value(row_idx, headers.get("description", -1))).strip()
        pkg = str(sheet.cell_value(row_idx, headers.get("packagereference", -1))).strip()
        pn = str(sheet.cell_value(row_idx, headers.get("partnumber", -1))).strip()
        for ref in [p.strip() for p in designators.replace(";", ",").split(",") if p.strip()]:
            parts[ref] = {"description": desc, "package": pkg, "part_number": pn}
    return parts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bom", type=Path, required=True, help="BOM .xls")
    ap.add_argument("--alts", type=Path, required=True, help="Alternative components JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        parse_bom(args.bom)
        json.loads(args.alts.read_text())
        return 0

    bom = parse_bom(args.bom)
    alts = json.loads(args.alts.read_text())

    package_counts = {}
    for ref, info in bom.items():
        pkg = info.get("package", "")
        package_counts[pkg] = package_counts.get(pkg, 0) + 1

    report = {
        "unique_part_count": len(set(info.get("part_number", "") for info in bom.values())),
        "component_count": len(bom),
        "package_counts": package_counts,
        "single_source_components": list(alts.get("alternatives", {}).keys()),
        "assembly_complexity_score": min(10, max(1, len(package_counts) // 5)),
        "notes": [
            "Lead time risk analysis requires supplier data.",
            "Single-source list derived from alternative_components.json entries.",
        ],
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
