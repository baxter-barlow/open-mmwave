#!/usr/bin/env python3
"""Estimate thermal dissipation with datasheet-based inputs when available."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Optional


DEFAULTS = {
 "U1": {"name": "LP87524", "power_w": None, "theta_ja_c_per_w": None},
 "U2": {"name": "radar SoC", "power_w": None, "theta_ja_c_per_w": None},
 "U3": {"name": "CP2105", "power_w": None, "theta_ja_c_per_w": None},
 "U19": {"name": "TPS2115A", "power_w": None, "theta_ja_c_per_w": None},
}


def _compute_power(entry: Dict) -> Optional[float]:
 if entry.get("power_typical_w") is not None:
 return float(entry["power_typical_w"])
 if entry.get("power_w") is not None:
 return float(entry["power_w"])
 if "supply_voltage_v" in entry and "supply_current_ma" in entry:
 return float(entry["supply_voltage_v"]) * float(entry["supply_current_ma"]) / 1000.0
 if "supply_voltage_v" in entry and "quiescent_current_ua" in entry:
 return float(entry["supply_voltage_v"]) * float(entry["quiescent_current_ua"]) / 1_000_000.0
 if "rail_currents_max_ma" in entry and "rail_volts" in entry:
 total = 0.0
 for rail, current_ma in entry["rail_currents_max_ma"].items():
 volts = entry["rail_volts"].get(rail, 0.0)
 total += volts * (current_ma / 1000.0)
 return total
 return None


def analyze(ambient_c: float, inputs: Dict) -> Dict:
 results = {}
 total_power = 0.0
 components = inputs.get("components", {})
 for ref, defaults in DEFAULTS.items():
 entry = components.get(ref, defaults)
 pd = _compute_power(entry)
 theta = entry.get("theta_ja_c_per_w")
 tj = ambient_c + pd * theta if pd is not None and theta is not None else None
 if pd is not None:
 total_power += pd
 results[ref] = {
 "name": entry.get("name", defaults.get("name")),
 "power_w": pd,
 "theta_ja_c_per_w": theta,
 "ambient_c": ambient_c,
 "junction_c": tj,
 "notes": entry.get("notes"),
 }
 return {
 "ambient_c": ambient_c,
 "total_power_w": total_power,
 "components": results,
 "notes": [
 "Computed power uses datasheet currents where provided; missing values yield nulls.",
 ],
 }


def main() -> int:
 ap = argparse.ArgumentParser()
 ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
 ap.add_argument("--inputs", type=Path, default=Path("data/thermal_inputs.json"), help="Thermal input JSON")
 ap.add_argument("--ambient-c", type=float, default=25.0, help="Ambient temperature in C")
 ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
 args = ap.parse_args()

 if args.dry_run:
 if args.inputs.exists():
 json.loads(args.inputs.read_text())
 return 0

 inputs = json.loads(args.inputs.read_text()) if args.inputs.exists() else {"components": {}}
 data = analyze(args.ambient_c, inputs)
 args.out.write_text(json.dumps(data, indent=2, sort_keys=True))
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
