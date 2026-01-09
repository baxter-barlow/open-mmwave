#!/usr/bin/env python3
"""Analyze test coverage from netlist and test point data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text())


def extract_test_points(netlist: Dict) -> Dict[str, str]:
    tps = {}
    for comp, pins in netlist.get("comp_to_pins", {}).items():
        if comp.startswith("TP"):
            for _pin, net in pins.items():
                tps[comp] = net
    return tps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        load_json(args.netlist)
        return 0

    netlist = load_json(args.netlist)
    tps = extract_test_points(netlist)

    report = {
        "test_points": tps,
        "coverage": {
            "power_rails": [tp for tp, net in tps.items() if net.startswith("PMIC_") or net.endswith("3V3") or net == "5V_IN_B"],
            "digital_io": [tp for tp, net in tps.items() if net.startswith("AR_") or net.startswith("HD_")],
            "analog": [],
            "interfaces": {
                "uart": [tp for tp, net in tps.items() if "RS232" in net or "LOGGER" in net],
                "i2c": [tp for tp, net in tps.items() if "SCL" in net or "SDA" in net],
                "spi": [],
                "can": [],
            },
            "rf": [],
        },
        "notes": [
            "Coverage is derived from TP* nets only; connector access not included.",
        ],
    }
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
