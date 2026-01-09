#!/usr/bin/env python3
"""Extract ODB++ structure data for stackup, nets, and components."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List


NET_RE = re.compile(r"^\$(\d+)\s+(\S+)")


def parse_matrix(path: Path) -> List[Dict]:
    layers = []
    block = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("LAYER {"):
            block = {}
        elif line == "}":
            if block:
                layers.append(block)
            block = None
        elif block is not None and "=" in line:
            k, v = line.split("=", 1)
            block[k.strip().lower()] = v.strip()
    return layers


def parse_netlist(path: Path) -> Dict[str, str]:
    nets = {}
    for line in path.read_text().splitlines():
        m = NET_RE.match(line.strip())
        if m:
            nets[m.group(1)] = m.group(2)
    return nets


def parse_eda_components(path: Path) -> Dict[str, int]:
    counts = {"top": 0, "bottom": 0, "via": 0}
    for line in path.read_text().splitlines():
        if line.startswith("SNT TOP"):
            counts["top"] += 1
        elif line.startswith("SNT BOT"):
            counts["bottom"] += 1
        elif line.startswith("SNT VIA"):
            counts["via"] += 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--odb", type=Path, required=True, help="ODB root (odb/)")
    ap.add_argument("--out-stackup", type=Path, required=True, help="Stackup JSON")
    ap.add_argument("--out-nets", type=Path, required=True, help="Netlist JSON")
    ap.add_argument("--out-components", type=Path, required=True, help="Component JSON")
    ap.add_argument("--out-rules", type=Path, required=True, help="Design rules JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    matrix = parse_matrix(args.odb / "matrix" / "matrix")
    args.out_stackup.write_text(json.dumps({"layers": matrix}, indent=2, sort_keys=True))

    nets = parse_netlist(args.odb / "steps" / "pcb" / "netlists" / "cadnet" / "netlist")
    args.out_nets.write_text(json.dumps({"nets": nets}, indent=2, sort_keys=True))

    eda_path = args.odb / "steps" / "pcb" / "eda" / "data"
    comps = parse_eda_components(eda_path) if eda_path.exists() else {}
    args.out_components.write_text(json.dumps({"counts": comps}, indent=2, sort_keys=True))

    rules_path = args.odb / "misc" / "attrlist"
    rules = rules_path.read_text().splitlines() if rules_path.exists() else []
    args.out_rules.write_text(json.dumps({"raw": rules}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
