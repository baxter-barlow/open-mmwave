#!/usr/bin/env python3
"""Generate signal integrity checklist from netlist and impedance targets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text())


def collect_nets(netlist: Dict, prefix_list: List[str]) -> List[str]:
    nets = []
    for net in netlist.get("net_to_pins", {}).keys():
        for prefix in prefix_list:
            if net.startswith(prefix):
                nets.append(net)
                break
    return sorted(set(nets))


def build_checklist(netlist: Dict, impedance: Dict) -> Dict:
    usb = ["USB_DP", "USB_DM"]
    lvds = collect_nets(netlist, ["AR_LVDS"])
    spi = collect_nets(netlist, ["SPI_", "HD_SPI"])
    jtag = collect_nets(netlist, ["HD_AR_T", "AR_T"])
    uart = collect_nets(netlist, ["UART", "RS232", "AR_MSS_LOGGER"])

    return {
        "categories": {
            "usb": {
                "nets": usb,
                "impedance_target": "90ohm_diff",
            },
            "lvds": {
                "nets": lvds,
                "impedance_target": "100ohm_diff",
            },
            "spi": {
                "nets": spi,
                "impedance_target": "50ohm_single",
            },
            "jtag": {
                "nets": jtag,
                "impedance_target": "50ohm_single",
            },
            "uart": {
                "nets": uart,
                "impedance_target": "50ohm_single",
            },
        },
        "impedance_targets": impedance.get("targets", []),
        "notes": [
            "Impedance targets are approximate; see data/impedance_targets.json for assumptions.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
    ap.add_argument("--impedance", type=Path, required=True, help="Impedance targets JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        load_json(args.netlist)
        load_json(args.impedance)
        return 0

    netlist = load_json(args.netlist)
    impedance = load_json(args.impedance)
    data = build_checklist(netlist, impedance)
    args.out.write_text(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
