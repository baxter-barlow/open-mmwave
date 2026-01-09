#!/usr/bin/env python3
"""Advanced netlist diff with HTML and Markdown reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def load(path: Path) -> Dict:
    return json.loads(path.read_text())


def pins_set(netlist: Dict, net: str) -> set[Tuple[str, str]]:
    return set(tuple(p) for p in netlist["net_to_pins"].get(net, []))


def detect_renames(net_a: Dict, net_b: Dict) -> List[Dict]:
    renames = []
    used_b = set()
    for net in net_a["net_to_pins"]:
        pins = pins_set(net_a, net)
        if not pins:
            continue
        for other in net_b["net_to_pins"]:
            if other in used_b:
                continue
            if pins == pins_set(net_b, other) and net != other:
                renames.append({"from": net, "to": other})
                used_b.add(other)
                break
    return renames


def impact_blocks(changed_nets: List[str], blocks: Dict) -> Dict[str, List[str]]:
    block_map = {name: set(info.get("nets", [])) for name, info in blocks.items()}
    impact = {name: [] for name in block_map}
    for net in changed_nets:
        for name, nets in block_map.items():
            if net in nets:
                impact[name].append(net)
    return {k: sorted(v) for k, v in impact.items() if v}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=Path, required=True, help="Netlist JSON A")
    ap.add_argument("--b", type=Path, required=True, help="Netlist JSON B")
    ap.add_argument("--blocks", type=Path, required=True, help="Schematic blocks JSON")
    ap.add_argument("--out-json", type=Path, required=True, help="Output JSON")
    ap.add_argument("--out-html", type=Path, required=True, help="Output HTML")
    ap.add_argument("--out-md", type=Path, required=True, help="Output Markdown")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        load(args.a)
        load(args.b)
        load(args.blocks)
        return 0

    net_a = load(args.a)
    net_b = load(args.b)
    blocks = load(args.blocks).get("blocks", {})

    nets_a = set(net_a["net_to_pins"].keys())
    nets_b = set(net_b["net_to_pins"].keys())
    added = sorted(nets_b - nets_a)
    removed = sorted(nets_a - nets_b)

    changed = {}
    for net in sorted(nets_a & nets_b):
        a_pins = pins_set(net_a, net)
        b_pins = pins_set(net_b, net)
        if a_pins != b_pins:
            changed[net] = {
                "added_pins": sorted(b_pins - a_pins),
                "removed_pins": sorted(a_pins - b_pins),
            }

    renames = detect_renames(net_a, net_b)
    impacted = impact_blocks(list(changed.keys()) + added + removed, blocks)

    report = {
        "nets_added": added,
        "nets_removed": removed,
        "nets_changed": changed,
        "renamed_nets": renames,
        "impact_by_block": impacted,
    }
    args.out_json.write_text(json.dumps(report, indent=2, sort_keys=True))

    args.out_md.write_text(
        "# Netlist Diff Report\n\n"
        f"Added nets: {len(added)}\n\nRemoved nets: {len(removed)}\n\n"
        "See JSON for full details.\n"
    )

    html = ["<html><body><h1>Netlist Diff Report</h1>"]
    html.append(f"<h2>Added nets ({len(added)})</h2><pre>{'\\n'.join(added)}</pre>")
    html.append(f"<h2>Removed nets ({len(removed)})</h2><pre>{'\\n'.join(removed)}</pre>")
    html.append("</body></html>")
    args.out_html.write_text("\n".join(html))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
