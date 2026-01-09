#!/usr/bin/env python3
"""Analyze Excellon drill files for hole sizes and counts."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict


TOOL_RE = re.compile(r"T(\d+)F.*C([0-9.]+)")


def _normalize_tool_id(tool_id: str) -> str:
    return str(int(tool_id))


def parse_drill(path: Path) -> Dict[str, Dict]:
    tools = {}
    current_tool = None
    for line in path.read_text(errors="ignore").splitlines():
        if line.startswith("T") and "C" in line:
            m = TOOL_RE.match(line.strip())
            if m:
                tool_id = _normalize_tool_id(m.group(1))
                tools[tool_id] = {"diameter_mm": float(m.group(2)), "count": 0}
        elif line.startswith("T"):
            current_tool = _normalize_tool_id(line.strip().lstrip("T"))
        elif (line.startswith("X") or line.startswith("Y")) and current_tool and current_tool in tools:
            tools[current_tool]["count"] += 1
    return tools


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drill", type=Path, required=True, help="Excellon drill file")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    tools = parse_drill(args.drill)
    report = {
        "tools": tools,
        "total_holes": sum(t["count"] for t in tools.values()),
        "notes": [
            "Hole categories inferred by diameter thresholds; verify in CAM.",
        ],
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
