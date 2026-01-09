#!/usr/bin/env python3
"""Analyze power distribution network from netlist and BOM."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import xlrd


CAP_VALUE_RE = re.compile(r"([0-9.]+)\s*([pnumk]f)", re.IGNORECASE)


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text())


def parse_bom_caps(path: Path) -> Dict[str, float]:
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
    cap_map = {}
    for row_idx in range(header_row + 1, sheet.nrows):
        designators = str(sheet.cell_value(row_idx, headers["designator"])).strip()
        if not designators:
            continue
        value = str(sheet.cell_value(row_idx, headers.get("value", -1))).strip()
        m = CAP_VALUE_RE.search(value)
        if not m:
            continue
        val = float(m.group(1))
        unit = m.group(2).lower()
        if unit == "pf":
            cap_f = val * 1e-12
        elif unit == "nf":
            cap_f = val * 1e-9
        elif unit == "uf":
            cap_f = val * 1e-6
        elif unit == "mf":
            cap_f = val * 1e-3
        else:
            cap_f = 0.0
        parts = [p.strip() for p in designators.replace(";", ",").split(",") if p.strip()]
        for ref in parts:
            cap_map[ref] = cap_f
    return cap_map


def analyze_pdn(netlist: Dict, cap_map: Dict[str, float]) -> Dict:
    net_to_pins = netlist.get("net_to_pins", {})
    rail_caps: Dict[str, Dict] = {}
    ferrites: Dict[str, List[str]] = {}

    for net, pins in net_to_pins.items():
        caps = [comp for comp, _pin in pins if comp.startswith("C")]
        if caps:
            total = 0.0
            for c in caps:
                total += cap_map.get(c, 0.0)
            rail_caps[net] = {
                "caps": sorted(set(caps)),
                "total_cap_f": total,
            }

        beads = [comp for comp, _pin in pins if comp.startswith("FL") or comp.startswith("L")]
        if beads:
            ferrites[net] = sorted(set(beads))

    return {
        "rail_caps": rail_caps,
        "ferrites": ferrites,
        "notes": [
            "Capacitor totals are based on BOM value parsing; missing values default to 0.",
            "Inductor/ferrite DCR not available in BOM; resistance estimation omitted.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
    ap.add_argument("--bom", type=Path, required=True, help="BOM .xls")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        load_json(args.netlist)
        parse_bom_caps(args.bom)
        return 0

    netlist = load_json(args.netlist)
    cap_map = parse_bom_caps(args.bom)
    data = analyze_pdn(netlist, cap_map)
    args.out.write_text(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
