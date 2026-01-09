#!/usr/bin/env python3
"""Extract component values from BOM production CSV."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


PASSIVE_RE = re.compile(r"^[CRL]\d+", re.IGNORECASE)
CAP_RE = re.compile(r"(\d+\.?\d*)\s*(pF|nF|uF|µF)", re.IGNORECASE)
RES_RE = re.compile(r"(\d+\.?\d*)\s*(k?ohm|k?ohms|mohm|mohms|k|m|r)", re.IGNORECASE)
IND_RE = re.compile(r"(\d+\.?\d*)\s*(pH|nH|uH|µH|mH)", re.IGNORECASE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bom", type=Path, required=True, help="Production BOM CSV")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    values = {}
    with args.bom.open() as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        value_idx = 1
        desc_idx = 2
        if headers:
            for idx, name in enumerate(headers):
                lname = name.strip().lower()
                if lname == "value":
                    value_idx = idx
                if lname == "description":
                    desc_idx = idx
        for row in reader:
            if len(row) < 2:
                continue
            refdes = row[0].strip()
            val = row[value_idx].strip() if len(row) > value_idx else ""
            desc = row[desc_idx].strip() if len(row) > desc_idx else ""
            if PASSIVE_RE.match(refdes):
                if not val and desc:
                    m = CAP_RE.search(desc)
                    if m:
                        val = f"{m.group(1)}{m.group(2)}"
                    m = RES_RE.search(desc)
                    if m and not val:
                        suffix = m.group(2).lower()
                        if suffix in ("k", "kohm", "kohms"):
                            val = f"{m.group(1)}k"
                        elif suffix in ("m", "mohm", "mohms"):
                            val = f"{m.group(1)}M"
                        elif suffix in ("r", "ohm", "ohms"):
                            val = f"{m.group(1)}R"
                    m = IND_RE.search(desc)
                    if m and not val:
                        val = f"{m.group(1)}{m.group(2)}"
                values[refdes] = val

    args.out.write_text(json.dumps(values, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
