#!/usr/bin/env python3
"""Validate fabrication package completeness and consistency."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

import xlrd


REQUIRED_GERBERS = [
    "PROC091G.GTL",
    "PROC091G.GBL",
    "PROC091G.GTS",
    "PROC091G.GBS",
    "PROC091G.GTO",
    "PROC091G.GBO",
    "PROC091G.GTP",
    "PROC091G.GBP",
]


def parse_round_holes(path: Path) -> Dict[str, float]:
    tool_sizes = {}
    if not path.exists():
        return tool_sizes
    for line in path.read_text().splitlines():
        if line.startswith("T") and "C" in line:
            m = re.match(r"T(\d+).+C([0-9.]+)", line)
            if m:
                tool_sizes[m.group(1)] = float(m.group(2))
    return tool_sizes


def parse_pnp(path: Path) -> List[str]:
    wb = xlrd.open_workbook(path.as_posix())
    sheet = wb.sheet_by_index(0)
    header_row = None
    for row_idx in range(min(30, sheet.nrows)):
        row = [str(sheet.cell_value(row_idx, c)).strip().lower() for c in range(sheet.ncols)]
        if "designator" in row:
            header_row = row_idx
            break
    if header_row is None:
        return []
    designator_idx = None
    for c in range(sheet.ncols):
        if str(sheet.cell_value(header_row, c)).strip().lower() == "designator":
            designator_idx = c
            break
    if designator_idx is None:
        return []
    refs = []
    for row_idx in range(header_row + 1, sheet.nrows):
        ref = str(sheet.cell_value(row_idx, designator_idx)).strip()
        if ref and ref != "!PCB":
            refs.append(ref)
    return refs


def count_signal_layers(matrix_path: Path) -> int:
    count = 0
    for line in matrix_path.read_text().splitlines():
        if line.strip().startswith("TYPE=SIGNAL"):
            count += 1
    return count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fab-dir", type=Path, required=True, help="Fabrication package directory")
    ap.add_argument("--pnp", type=Path, required=True, help="Pick and place .xls")
    ap.add_argument("--bom", type=Path, required=True, help="BOM .xls")
    ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        json.loads(args.netlist.read_text())
        parse_pnp(args.pnp)
        return 0

    gerber_dir = args.fab_dir / "GerberNCdrills"
    existing = {p.name for p in gerber_dir.iterdir()} if gerber_dir.exists() else set()
    missing = [f for f in REQUIRED_GERBERS if f not in existing]

    round_holes = parse_round_holes(gerber_dir / "PROC091G-RoundHoles.TXT")
    slot_holes = parse_round_holes(gerber_dir / "PROC091G-SlotHoles.TXT")

    pnp_refs = set(parse_pnp(args.pnp))
    netlist = json.loads(args.netlist.read_text())
    netlist_refs = set(netlist.get("comp_to_pins", {}).keys())

    matrix_path = args.fab_dir / "ODB" / "odb" / "matrix" / "matrix"
    signal_layers = count_signal_layers(matrix_path) if matrix_path.exists() else 0

    report = {
        "gerbers": {
            "required": REQUIRED_GERBERS,
            "missing": missing,
            "present_count": len(existing),
        },
        "drill_tools": {
            "round_hole_tools": round_holes,
            "slot_hole_tools": slot_holes,
        },
        "pnp": {
            "refdes_count": len(pnp_refs),
            "missing_from_netlist": sorted(pnp_refs - netlist_refs),
            "missing_from_pnp": sorted(netlist_refs - pnp_refs),
        },
        "layer_count": {
            "signal_layers": signal_layers,
            "expected": 8,
            "matches_expected": signal_layers == 8,
        },
        "netlist_consistency": {
            "odb_netlist_present": (args.fab_dir / "ODB" / "proc091g_netlist.rep").exists(),
            "ipc_netlist_present": (args.fab_dir / "IPC-D-356A Netlist" / "PROC091G.ipc").exists(),
        },
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
