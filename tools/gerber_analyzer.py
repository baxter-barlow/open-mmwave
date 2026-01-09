#!/usr/bin/env python3
"""Analyze Gerber layers for basic completeness and geometry."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


APERTURE_RE = re.compile(r"%ADD(\d+)([A-Z]),?([0-9.X]+)\*%")
COORD_RE = re.compile(r"X(-?\d+)Y(-?\d+)")
FORMAT_RE = re.compile(r"%FS[LA]X(\d)(\d)Y(\d)(\d)\*%")
UNIT_RE = re.compile(r"%MO(IN|MM)\*%")


def parse_gerber(path: Path) -> Dict:
    apertures = {}
    draw_count = 0
    flash_count = 0
    min_x = min_y = None
    max_x = max_y = None
    unit = None
    fmt = None
    for line in path.read_text(errors="ignore").splitlines():
        m_unit = UNIT_RE.search(line)
        if m_unit:
            unit = m_unit.group(1)
        m_fmt = FORMAT_RE.search(line)
        if m_fmt:
            fmt = {
                "x_int": int(m_fmt.group(1)),
                "x_dec": int(m_fmt.group(2)),
                "y_int": int(m_fmt.group(3)),
                "y_dec": int(m_fmt.group(4)),
            }
        m = APERTURE_RE.search(line)
        if m:
            apertures[m.group(1)] = {"shape": m.group(2), "params": m.group(3)}
        if "D01" in line:
            draw_count += 1
        if "D03" in line:
            flash_count += 1
        m = COORD_RE.search(line)
        if m:
            x = int(m.group(1))
            y = int(m.group(2))
            min_x = x if min_x is None else min(min_x, x)
            max_x = x if max_x is None else max(max_x, x)
            min_y = y if min_y is None else min(min_y, y)
            max_y = y if max_y is None else max(max_y, y)
    bounds_mm = None
    if fmt and min_x is not None and min_y is not None:
        scale_x = 10 ** fmt["x_dec"]
        scale_y = 10 ** fmt["y_dec"]
        min_x_u = min_x / scale_x
        max_x_u = max_x / scale_x
        min_y_u = min_y / scale_y
        max_y_u = max_y / scale_y
        if unit == "IN":
            min_x_u *= 25.4
            max_x_u *= 25.4
            min_y_u *= 25.4
            max_y_u *= 25.4
        bounds_mm = {
            "min_x_mm": min_x_u,
            "max_x_mm": max_x_u,
            "min_y_mm": min_y_u,
            "max_y_mm": max_y_u,
        }
    return {
        "aperture_count": len(apertures),
        "draw_count": draw_count,
        "flash_count": flash_count,
        "unit": unit,
        "format": fmt,
        "bounds_raw": {
            "min_x": min_x,
            "max_x": max_x,
            "min_y": min_y,
            "max_y": max_y,
        },
        "bounds_mm": bounds_mm,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fab-dir", type=Path, required=True, help="Fabrication package directory")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    gerber_dir = args.fab_dir / "GerberNCdrills"
    layers = {
        "top_copper": "PROC091G.GTL",
        "inner1": "PROC091G.G1",
        "inner2": "PROC091G.G2",
        "inner3": "PROC091G.G3",
        "inner4": "PROC091G.G4",
        "inner5": "PROC091G.G5",
        "inner6": "PROC091G.G6",
        "bottom_copper": "PROC091G.GBL",
        "top_solder": "PROC091G.GTS",
        "bottom_solder": "PROC091G.GBS",
        "top_silk": "PROC091G.GTO",
        "bottom_silk": "PROC091G.GBO",
        "top_paste": "PROC091G.GTP",
        "bottom_paste": "PROC091G.GBP",
        "outline": "PROC091G.GM1",
    }
    report = {"layers": {}, "missing_layers": []}
    for name, fname in layers.items():
        path = gerber_dir / fname
        if not path.exists():
            report["missing_layers"].append(fname)
            continue
        report["layers"][name] = parse_gerber(path)

    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
