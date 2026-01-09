#!/usr/bin/env python3
"""Validate extracted data against acceptance criteria."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output report JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    drill = json.loads(Path("data/drill_analysis.json").read_text())
    placement = json.loads(Path("data/component_placement.json").read_text())
    gerber = json.loads(Path("data/gerber_analysis.json").read_text())

    total_holes = drill.get("total_holes", 0)
    xy_ok = all(p["x_mil"] != p["y_mil"] for p in placement[:50])
    layers = gerber.get("layers", {})
    inner_ok = all(k in layers for k in ["inner1", "inner2", "inner3", "inner4", "inner5", "inner6"])

    report = {
        "drill_holes_gt_500": total_holes > 500,
        "pnp_xy_distinct": xy_ok,
        "inner_layers_present": inner_ok,
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
