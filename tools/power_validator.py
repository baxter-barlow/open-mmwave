#!/usr/bin/env python3
"""Generate power validation procedure and checklist from netlist data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


EXPECTED_RAILS = {
 "5V_IN": {"nominal_v": 5.0, "tolerance_pct": 5},
 "PMIC_3V3": {"nominal_v": 3.3, "tolerance_pct": 3},
 "PMIC_1V8": {"nominal_v": 1.8, "tolerance_pct": 3},
 "PMIC_1V2": {"nominal_v": 1.2, "tolerance_pct": 3},
 "PMIC_1V0": {"nominal_v": 1.0, "tolerance_pct": 3},
}


def load_json(path: Path) -> dict:
 return json.loads(path.read_text())


def extract_test_points(netlist: Dict) -> Dict[str, str]:
 tp_map = {}
 for comp, pins in netlist.get("comp_to_pins", {}).items():
 if not comp.startswith("TP"):
 continue
 for _pin, net in pins.items():
 tp_map[comp] = net
 return dict(sorted(tp_map.items(), key=lambda x: x[0]))


def build_procedure(netlist: Dict, pmic: Dict) -> Dict:
 test_points = extract_test_points(netlist)
 rails = []
 for rail, limits in EXPECTED_RAILS.items():
 tps = [tp for tp, net in test_points.items() if net == rail]
 rails.append(
 {
 "rail": rail,
 "nominal_v": limits["nominal_v"],
 "tolerance_pct": limits["tolerance_pct"],
 "test_points": tps,
 }
 )

 return {
 "sources": {
 "netlist": "data/netlist_revG.json",
 "pmic_mapping": "data/pmic_mapping.json",
 },
 "pmic_mapping": pmic.get("mapping", {}),
 "test_points": test_points,
 "rails": rails,
 "procedure": [
 {
 "stage": "Input Power",
 "steps": [
 "Set bench supply to 5.0 V and current limit to 0.5 A for initial checks.",
 "Apply power at a single input (J1, J5, or J2) and verify 5V_IN.",
 ],
 },
 {
 "stage": "PMIC Outputs",
 "steps": [
 "Verify PMIC_3V3 at TP5.",
 "Verify PMIC_1V8/PMIC_1V2/PMIC_1V0 at output caps on PMIC sheet.",
 "Check PMIC_PGOOD goes high after rails settle.",
 ],
 },
 {
 "stage": "SoC Rails",
 "steps": [
 "Verify AR_1V8, AR_1P2, AR_1P0_RF1, AR_1P0_RF2 after beads.",
 "Verify AR_NRST at TP14 after PMIC_PGOOD.",
 ],
 },
 ],
 }


def write_checklist(out_path: Path, data: Dict) -> None:
 lines = [
 "# Power Validation Checklist - open_mmwave Rev G",
 "",
 "Sources: `data/netlist_revG.json`, `data/pmic_mapping.json`.",
 "",
 "## Expected Rails",
 "| Rail | Nominal (V) | Tolerance | Test Points |",
 "|---|---:|---:|---|",
 ]
 for rail in data["rails"]:
 tps = ", ".join(rail["test_points"]) if rail["test_points"] else "TBD"
 lines.append(
 f"| {rail['rail']} | {rail['nominal_v']:.2f} | ±{rail['tolerance_pct']}% | {tps} |"
 )
 lines.extend(
 [
 "",
 "## Procedure",
 ]
 )
 for stage in data["procedure"]:
 lines.append(f"### {stage['stage']}")
 for step in stage["steps"]:
 lines.append(f"- {step}")
 lines.append("")
 out_path.write_text("\n".join(lines).strip() + "\n")


def main() -> int:
 ap = argparse.ArgumentParser()
 ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
 ap.add_argument("--pmic", type=Path, required=True, help="PMIC mapping JSON")
 ap.add_argument("--out-json", type=Path, required=True, help="Output JSON path")
 ap.add_argument("--out-md", type=Path, required=True, help="Output Markdown path")
 ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
 args = ap.parse_args()

 if args.dry_run:
 load_json(args.netlist)
 load_json(args.pmic)
 return 0

 netlist = load_json(args.netlist)
 pmic = load_json(args.pmic)
 procedure = build_procedure(netlist, pmic)
 args.out_json.write_text(json.dumps(procedure, indent=2, sort_keys=True))
 write_checklist(args.out_md, procedure)
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
