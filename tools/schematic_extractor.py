#!/usr/bin/env python3
"""Extract schematic blocks from Altium sources with netlist fallback."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Set


BLOCK_DEFS = {
    "pmic_block": {
        "nets": [
            r"^PMIC_",
            r"^PMICVIO",
            r"^SW[0-3]$",
            r"^PMIC_EN",
            r"^PMIC_NRST$",
            r"^PMIC_PGOOD$",
            r"^PMIC_SCL$",
            r"^PMIC_SDA$",
            r"^PMIC_CLK$",
            r"^5V_IN$",
        ],
    },
    "reset_gpio_block": {
        "nets": [
            r"NRST",
            r"WARMRST",
            r"SENS_NRST",
            r"BT_RST",
        ],
    },
    "usb_uart_block": {
        "nets": [
            r"^USB_",
            r"USB_DP",
            r"USB_DM",
            r"UART",
            r"RS232",
        ],
    },
    "hd_connector_block": {
        "nets": [
            r"^HD_",
            r"AR_LVDS",
            r"AR_DP",
            r"AR_DMM",
        ],
    },
    "can_interface_block": {
        "nets": [
            r"CAN",
            r"MCAN",
        ],
    },
    "analog_mux_block": {
        "nets": [
            r"MUX",
        ],
    },
    "bt_display_block": {
        "nets": [
            r"BT_",
            r"DISPLAY",
        ],
    },
    "soc_core_block": {
        "components": ["U2"],
    },
}


def load_netlist(path: Path) -> Dict:
    return json.loads(path.read_text())


def compile_patterns(patterns: List[str]) -> List[re.Pattern]:
    return [re.compile(p) for p in patterns]


def component_in_block(comp: str, nets: List[str], block_def: Dict) -> bool:
    if "components" in block_def and comp in block_def["components"]:
        return True
    patterns = compile_patterns(block_def.get("nets", []))
    for net in nets:
        for pat in patterns:
            if pat.search(net):
                return True
    return False


def extract_blocks(netlist: Dict) -> Dict[str, Dict]:
    comp_to_nets: Dict[str, List[str]] = {}
    for comp, pins in netlist.get("comp_to_pins", {}).items():
        comp_to_nets[comp] = list(set(pins.values()))

    blocks: Dict[str, Dict] = {}
    assigned: Set[str] = set()
    for block_name, block_def in BLOCK_DEFS.items():
        comps = []
        nets: Set[str] = set()
        for comp, comp_nets in comp_to_nets.items():
            if component_in_block(comp, comp_nets, block_def):
                comps.append(comp)
                nets.update(comp_nets)
                assigned.add(comp)
        blocks[block_name] = {
            "components": sorted(comps),
            "nets": sorted(nets),
            "method": "netlist_fallback",
        }
    unassigned = sorted(set(comp_to_nets.keys()) - assigned)
    return {"blocks": blocks, "unassigned_components": unassigned}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        load_netlist(args.netlist)
        return 0

    netlist = load_netlist(args.netlist)
    blocks = extract_blocks(netlist)
    blocks["source"] = {
        "netlist": str(args.netlist),
        "note": "SchDoc parsing not available; blocks inferred from netlist patterns.",
    }
    args.out.write_text(json.dumps(blocks, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
