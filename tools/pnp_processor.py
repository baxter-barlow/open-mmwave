#!/usr/bin/env python3
"""Process pick-and-place data into machine format and placement map."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List

import xlrd


def parse_pnp(path: Path) -> List[Dict]:
    wb = xlrd.open_workbook(path.as_posix())
    sh = wb.sheet_by_index(0)
    header_row = None
    for row_idx in range(min(40, sh.nrows)):
        row = [str(sh.cell_value(row_idx, c)).strip().lower() for c in range(sh.ncols)]
        if "designator" in row and "rotation" in row and "center-x(mil)" in row:
            header_row = row_idx
            break
    if header_row is None:
        for row_idx in range(min(40, sh.nrows)):
            row = [str(sh.cell_value(row_idx, c)).strip().lower() for c in range(sh.ncols)]
            if "designator" in row and "rotation" in row and "mid x" in row:
                header_row = row_idx
                break
    if header_row is None:
        raise ValueError("PnP header not found")
    def norm(s: str) -> str:
        return "".join(ch for ch in s.lower() if ch.isalnum())

    headers = {norm(str(sh.cell_value(header_row, c)).strip()): c for c in range(sh.ncols)}
    rows = []
    for r in range(header_row + 1, sh.nrows):
        ref = str(sh.cell_value(r, headers.get("designator", -1))).strip()
        if not ref or ref == "!PCB":
            continue
        try:
            rotation = float(sh.cell_value(r, headers.get("rotation", -1)) or 0.0)
            x_mil = float(sh.cell_value(r, headers.get("centerxmil", -1)) or 0.0)
            y_mil = float(sh.cell_value(r, headers.get("centerymil", -1)) or 0.0)
        except ValueError:
            continue
        rows.append(
            {
                "refdes": ref,
                "package": str(sh.cell_value(r, headers.get("packagereference", -1))).strip(),
                "side": str(sh.cell_value(r, headers.get("layer", -1))).strip(),
                "rotation_deg": rotation,
                "x_mil": x_mil,
                "y_mil": y_mil,
            }
        )
    return rows


def write_svg(points: List[Dict], out_path: Path) -> None:
    if not points:
        return
    xs = [p["x_mil"] for p in points]
    ys = [p["y_mil"] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x + 100
    height = max_y - min_y + 100
    scale = 0.05
    w = width * scale
    h = height * scale
    lines = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'>"]
    for p in points:
        x = (p["x_mil"] - min_x + 50) * scale
        y = (max_y - p["y_mil"] + 50) * scale
        lines.append(f"<circle cx='{x:.2f}' cy='{y:.2f}' r='1' fill='black' />")
    lines.append("</svg>")
    out_path.write_text("\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pnp", type=Path, required=True, help="Pick and place .xls")
    ap.add_argument("-o", "--out-json", type=Path, required=True, help="Output JSON")
    ap.add_argument("--out-csv", type=Path, required=True, help="Output CSV")
    ap.add_argument("--out-svg", type=Path, required=True, help="Output SVG map")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        parse_pnp(args.pnp)
        return 0

    rows = parse_pnp(args.pnp)
    args.out_json.write_text(json.dumps(rows, indent=2, sort_keys=True))
    with args.out_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["RefDes", "Package", "Side", "Rotation", "X_mil", "Y_mil"])
        for r in rows:
            writer.writerow([r["refdes"], r["package"], r["side"], r["rotation_deg"], r["x_mil"], r["y_mil"]])
    write_svg(rows, args.out_svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
