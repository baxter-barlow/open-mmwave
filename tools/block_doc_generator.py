#!/usr/bin/env python3
"""Generate block documentation from schematic block data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import xlrd


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text())


def parse_bom(path: Path) -> Dict[str, Dict[str, Any]]:
    wb = xlrd.open_workbook(path.as_posix())
    sheet = wb.sheet_by_index(0)
    headers = {}
    header_row = None
    for row_idx in range(min(30, sheet.nrows)):
        row = [str(sheet.cell_value(row_idx, c)).strip().lower() for c in range(sheet.ncols)]
        if "designator" in row:
            header_row = row_idx
            for c, name in enumerate(row):
                headers[name] = c
            break
    if header_row is None:
        raise ValueError("Designator header not found in BOM")
    ref_map: Dict[str, Dict[str, Any]] = {}
    for row_idx in range(header_row + 1, sheet.nrows):
        designators = str(sheet.cell_value(row_idx, headers["designator"])).strip()
        if not designators:
            continue
        parts = [p.strip() for p in designators.replace(";", ",").split(",") if p.strip()]
        value = sheet.cell_value(row_idx, headers.get("value", -1)) if "value" in headers else ""
        desc = sheet.cell_value(row_idx, headers.get("description", -1)) if "description" in headers else ""
        part = sheet.cell_value(row_idx, headers.get("partnumber", -1)) if "partnumber" in headers else ""
        for ref in parts:
            ref_map[ref] = {"value": value, "description": desc, "part_number": part}
    return ref_map


def render_block(block_name: str, block: Dict, bom_map: Dict[str, Dict[str, Any]]) -> str:
    comps = block.get("components", [])
    nets = block.get("nets", [])
    lines = [
        f"# {block_name.replace('_', ' ').title()}",
        "",
        "Source: `data/schematic_blocks.json`, BOM, IPC netlist.",
        "",
        "## Component List",
        "| Refdes | Value | Description | Part Number |",
        "|---|---|---|---|",
    ]
    for comp in comps:
        info = bom_map.get(comp, {})
        lines.append(
            f"| {comp} | {info.get('value', '')} | {info.get('description', '')} | {info.get('part_number', '')} |"
        )
    lines.extend(
        [
            "",
            "## Nets",
            ", ".join(sorted(nets)) if nets else "None",
            "",
            "## Power Rails",
            ", ".join(sorted([n for n in nets if n.startswith('PMIC_') or n.endswith('3V3')])) if nets else "None",
            "",
            "## Notes",
            "- Block extraction is netlist-based; schematic annotations were not parsed.",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blocks", type=Path, required=True, help="Schematic blocks JSON")
    ap.add_argument("--bom", type=Path, required=True, help="BOM .xls")
    ap.add_argument("--out-dir", type=Path, required=True, help="Output directory")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        load_json(args.blocks)
        parse_bom(args.bom)
        return 0

    blocks = load_json(args.blocks)
    bom_map = parse_bom(args.bom)
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# Block Documentation Index",
        "",
        "Generated from `data/schematic_blocks.json` and BOM.",
        "",
    ]
    for block_name, block in blocks.get("blocks", {}).items():
        filename = f"{block_name}.md"
        (out_dir / filename).write_text(render_block(block_name, block, bom_map))
        index_lines.append(f"- {filename}")
    (out_dir / "README.md").write_text("\n".join(index_lines).strip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
