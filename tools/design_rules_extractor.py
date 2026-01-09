#!/usr/bin/env python3
"""Extract PCB design rules from fabrication files."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict


def parse_tool_sizes(path: Path) -> Dict[str, float]:
    tools = {}
    if not path.exists():
        return tools
    for line in path.read_text().splitlines():
        m = re.match(r"T(\d+).+C([0-9.]+)", line)
        if m:
            tools[m.group(1)] = float(m.group(2))
    return tools


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fab-dir", type=Path, required=True, help="Fabrication package directory")
    ap.add_argument("--stackup", type=Path, required=True, help="Stackup JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        json.loads(args.stackup.read_text())
        return 0

    stackup = json.loads(args.stackup.read_text())
    gerber_dir = args.fab_dir / "GerberNCdrills"
    round_tools = parse_tool_sizes(gerber_dir / "PROC091G-RoundHoles.TXT")
    slot_tools = parse_tool_sizes(gerber_dir / "PROC091G-SlotHoles.TXT")

    report = {
        "board_thickness_in": stackup.get("board_thickness_in"),
        "signal_layers": 8,
        "min_drill_mm": min(round_tools.values()) if round_tools else None,
        "min_slot_mm": min(slot_tools.values()) if slot_tools else None,
        "drill_tools": {
            "round_holes_mm": round_tools,
            "slot_holes_mm": slot_tools,
        },
        "min_trace_width": None,
        "min_spacing": None,
        "notes": [
            "Trace width/spacing not specified in fabrication files; verify with CAM/fab notes.",
        ],
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
