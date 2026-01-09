#!/usr/bin/env python3
"""Build component parameter database from datasheets and existing inputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
 ap = argparse.ArgumentParser()
 ap.add_argument("--thermal-inputs", type=Path, required=True, help="Thermal inputs JSON")
 ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON")
 ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
 args = ap.parse_args()

 if args.dry_run:
 json.loads(args.thermal_inputs.read_text())
 return 0

 thermal = json.loads(args.thermal_inputs.read_text())
 comps = thermal.get("components", {})

 database = {
 "LP87524": {
 "manufacturer": "",
 "package": "VQFN-HR-26",
 "thermal": {
 "theta_ja": comps.get("U1", {}).get("theta_ja_c_per_w"),
 },
 "electrical": {
 "vin_min": None,
 "vin_max": None,
 "vout_min": None,
 "vout_max": None,
 "iout_max": None,
 },
 "timing": {},
 },
 "radar SoC": {
 "manufacturer": "",
 "package": "FCBGA ALP0180A",
 "thermal": {
 "theta_ja": comps.get("U2", {}).get("theta_ja_c_per_w"),
 "theta_jc": comps.get("U2", {}).get("theta_jc_c_per_w"),
 "theta_jb": comps.get("U2", {}).get("theta_jb_c_per_w"),
 },
 "electrical": {
 "power_typical_w": comps.get("U2", {}).get("power_typical_w"),
 "power_max_w": comps.get("U2", {}).get("power_max_w"),
 },
 "timing": {},
 },
 "CP2105": {
 "manufacturer": "Silicon Labs",
 "package": "QFN-24 4x4mm",
 "thermal": {"theta_ja": comps.get("U3", {}).get("theta_ja_c_per_w")},
 "electrical": {
 "power_typical_w": comps.get("U3", {}).get("power_typical_w"),
 "power_max_w": comps.get("U3", {}).get("power_max_w"),
 "supply_voltage_v": comps.get("U3", {}).get("supply_voltage_v"),
 },
 "timing": {},
 },
 "TPS2115A": {
 "manufacturer": "",
 "package": "SON-8 (DRB)",
 "thermal": {"theta_ja": comps.get("U19", {}).get("theta_ja_c_per_w")},
 "electrical": {
 "ron_ohm": 0.084,
 "power_typical_w": comps.get("U19", {}).get("power_typical_w"),
 },
 "timing": {},
 },
 }

 args.out.write_text(json.dumps(database, indent=2, sort_keys=True))
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
