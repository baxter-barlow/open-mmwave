#!/usr/bin/env python3
"""Parse BOM .xls and correlate with IPC netlist components."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import csv
import xlrd


HEADER_ALIASES = {
    "designator": "designator",
    "refdes": "designator",
    "quantity": "quantity",
    "qty": "quantity",
    "value": "value",
    "comment": "value",
    "description": "description",
    "partnumber": "part_number",
    "manufacturer": "manufacturer",
    "packagereference": "package",
    "alternate partnumber": "alt_part_number",
    "alternate manufacturer": "alt_manufacturer",
}


def _normalize_header(cell: Any) -> str:
    return str(cell).strip().lower().replace(" ", "")


def _find_header_row(sheet: xlrd.sheet.Sheet) -> Tuple[int, Dict[str, int]]:
    for row_idx in range(min(sheet.nrows, 30)):
        headers = {}
        for col_idx in range(sheet.ncols):
            key = _normalize_header(sheet.cell_value(row_idx, col_idx))
            if key in HEADER_ALIASES:
                headers[HEADER_ALIASES[key]] = col_idx
        if "designator" in headers:
            return row_idx, headers
    raise ValueError("Could not locate BOM header row with Designator column")


def _split_designators(cell: Any) -> List[str]:
    raw = str(cell).replace("\n", " ").strip()
    if not raw:
        return []
    parts = [p.strip() for p in raw.replace(";", ",").split(",")]
    return [p for p in parts if p]


def parse_bom(path: Path) -> Dict[str, Any]:
    wb = xlrd.open_workbook(path.as_posix())
    sheet = wb.sheet_by_index(0)
    header_row, headers = _find_header_row(sheet)

    items = []
    refdes_to_item = {}
    dnp_refdes = []

    for row_idx in range(header_row + 1, sheet.nrows):
        designators = _split_designators(sheet.cell_value(row_idx, headers["designator"]))
        if not designators:
            continue
        row = {
            "designators": designators,
            "quantity": sheet.cell_value(row_idx, headers.get("quantity", -1))
            if "quantity" in headers
            else None,
            "value": sheet.cell_value(row_idx, headers.get("value", -1))
            if "value" in headers
            else None,
            "description": sheet.cell_value(row_idx, headers.get("description", -1))
            if "description" in headers
            else None,
            "package": sheet.cell_value(row_idx, headers.get("package", -1))
            if "package" in headers
            else None,
            "part_number": sheet.cell_value(row_idx, headers.get("part_number", -1))
            if "part_number" in headers
            else None,
            "manufacturer": sheet.cell_value(row_idx, headers.get("manufacturer", -1))
            if "manufacturer" in headers
            else None,
        }
        items.append(row)
        desc = str(row.get("description", "")).lower()
        val = str(row.get("value", "")).lower()
        if "dnp" in desc or "dnp" in val or "not fitted" in desc:
            dnp_refdes.extend(designators)
        for ref in designators:
            refdes_to_item[ref] = row

    return {
        "headers": headers,
        "items": items,
        "refdes_to_item": refdes_to_item,
        "dnp_refdes": sorted(set(dnp_refdes)),
    }


def _extract_mpn(item: Dict[str, Any]) -> str:
    pn = str(item.get("part_number", "")).strip()
    return pn


def correlate(bom: Dict[str, Any], netlist: Dict[str, Any]) -> Dict[str, Any]:
    bom_components = set(bom["refdes_to_item"].keys())
    netlist_components = set(netlist["comp_to_pins"].keys())

    bom_only = sorted(bom_components - netlist_components)
    netlist_only = sorted(netlist_components - bom_components)

    mpn_missing = [ref for ref, item in bom["refdes_to_item"].items() if not _extract_mpn(item)]

    return {
        "bom_only": bom_only,
        "netlist_only": netlist_only,
        "mpn_missing": sorted(set(mpn_missing)),
        "dnp_components": bom.get("dnp_refdes", []),
        "counts": {
            "bom_components": len(bom_components),
            "netlist_components": len(netlist_components),
            "bom_only": len(bom_only),
            "netlist_only": len(netlist_only),
        },
        "notes": [
            "Value mismatches cannot be checked because the IPC netlist does not contain value fields.",
            "MPN validation checks for blank PartNumber fields in BOM.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bom", type=Path, help="BOM .xls file")
    ap.add_argument("netlist", type=Path, help="Netlist JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    ap.add_argument("--bom-production", type=Path, help="Output production BOM CSV")
    ap.add_argument("--bom-procurement", type=Path, help="Output procurement BOM CSV")
    ap.add_argument("--cost-out", type=Path, help="Output cost estimate JSON")
    args = ap.parse_args()

    if args.dry_run:
        parse_bom(args.bom)
        json.loads(args.netlist.read_text())
        return 0

    bom = parse_bom(args.bom)
    netlist = json.loads(args.netlist.read_text())
    report = {
        "bom_path": str(args.bom),
        "netlist_path": str(args.netlist),
        "bom_summary": {
            "item_count": len(bom["items"]),
            "refdes_count": len(bom["refdes_to_item"]),
        },
        "correlation": correlate(bom, netlist),
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))

    if args.bom_production:
        with args.bom_production.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["RefDes", "Value", "Description", "MPN"])
            for ref, item in sorted(bom["refdes_to_item"].items()):
                writer.writerow([ref, item.get("value", ""), item.get("description", ""), item.get("part_number", "")])

    if args.bom_procurement:
        with args.bom_procurement.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["MPN", "Description", "Qty"])
            counts = {}
            for item in bom["items"]:
                mpn = _extract_mpn(item) or "UNKNOWN"
                qty = int(item.get("quantity") or 0)
                counts.setdefault(mpn, {"description": item.get("description", ""), "qty": 0})
                counts[mpn]["qty"] += qty
            for mpn, info in counts.items():
                writer.writerow([mpn, info["description"], info["qty"]])

    if args.cost_out:
        cost_report = {
            "total_cost_usd": None,
            "notes": ["No pricing data in repo; integrate distributor APIs for pricing."],
        }
        args.cost_out.write_text(json.dumps(cost_report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
