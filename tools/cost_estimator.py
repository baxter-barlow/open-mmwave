#!/usr/bin/env python3
"""Estimate BOM cost using placeholder pricing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import xlrd


def parse_bom(path: Path) -> Dict[str, float]:
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
        raise ValueError("Designator header not found in BOM")
    count = 0
    for row_idx in range(header_row + 1, sheet.nrows):
        designators = str(sheet.cell_value(row_idx, headers["designator"])).strip()
        if not designators:
            continue
        parts = [p.strip() for p in designators.replace(";", ",").split(",") if p.strip()]
        count += len(parts)
    return {"component_count": count}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bom", type=Path, required=True, help="BOM .xls")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        parse_bom(args.bom)
        return 0

    summary = parse_bom(args.bom)
    report = {
        "summary": summary,
        "total_cost_usd": None,
        "notes": [
            "No pricing data in repo; integrate with supplier pricing to compute totals.",
        ],
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
