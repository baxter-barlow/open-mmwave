#!/usr/bin/env python3
"""Map BOM to LCSC part numbers (placeholder)."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bom", type=Path, required=True, help="Production BOM CSV")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output CSV")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    with args.bom.open() as f:
        rows = list(csv.reader(f))
    with args.out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["RefDes", "MPN", "LCSC_PN"])
        for row in rows[1:]:
            ref, _val, _desc, mpn = row
            writer.writerow([ref, mpn, "TBD"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
