#!/usr/bin/env python3
"""Parse IPC-D-356A netlist and emit connectivity JSON.

Outputs:
- net_to_pins: {net_name: [(component, pin), ...]}
- comp_to_pins: {component: {pin: net_name}}
- net_aliases: {NETx: actual_net_name}
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

P_ALIAS_RE = re.compile(r"^P\s+NNAMENET(\d+)\s+(\S+)")
REC_327_RE = re.compile(r"^(\d{3})([^\s]+)\s+([A-Za-z][A-Za-z0-9]*)\s+-([A-Za-z0-9]+)\s+")


def parse_ipc(path: Path) -> dict:
    net_aliases = {}
    net_to_pins = {}
    comp_to_pins = {}

    for line in path.read_text().splitlines():
        line = line.rstrip()
        if not line:
            continue
        m_alias = P_ALIAS_RE.match(line)
        if m_alias:
            net_idx = m_alias.group(1)
            net_name = m_alias.group(2)
            net_aliases[f"NET{net_idx}"] = net_name
            continue
        m_327 = REC_327_RE.match(line)
        if m_327:
            net_name = m_327.group(2)
            comp = m_327.group(3)
            pin = m_327.group(4)
            net_to_pins.setdefault(net_name, []).append((comp, pin))
            comp_to_pins.setdefault(comp, {})[pin] = net_name

    return {
        "net_aliases": net_aliases,
        "net_to_pins": net_to_pins,
        "comp_to_pins": comp_to_pins,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ipc", type=Path, help="IPC-D-356A netlist")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    args = ap.parse_args()

    data = parse_ipc(args.ipc)
    args.out.write_text(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
