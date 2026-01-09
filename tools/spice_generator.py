#!/usr/bin/env python3
"""Generate simplified SPICE models and test benches."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, required=True, help="Simulation output dir")
    ap.add_argument("-o", "--out-json", type=Path, required=True, help="Model parameter JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "power_input.cir").write_text(
        "* Power input ORing model\n"
        "VUSB 1 0 DC 5\n"
        "VHD 2 0 DC 5\n"
        "D1 1 3 DGEN\n"
        "D2 2 3 DGEN\n"
        "RLOAD 3 0 10\n"
        ".model DGEN D\n"
        ".op\n"
        ".end\n"
    )

    (out_dir / "pmic_behavioral.cir").write_text(
        "* PMIC behavioral model\n"
        "VIN 1 0 DC 5\n"
        "E3V3 2 0 1 0 0.66\n"
        "E1V8 3 0 1 0 0.36\n"
        "E1V2 4 0 1 0 0.24\n"
        "E1V0 5 0 1 0 0.20\n"
        "RLOAD3V3 2 0 33\n"
        "RLOAD1V8 3 0 18\n"
        "RLOAD1V2 4 0 12\n"
        "RLOAD1V0 5 0 10\n"
        ".op\n"
        ".end\n"
    )

    (out_dir / "reset_circuit.cir").write_text(
        "* Reset AND gate model\n"
        "V1 1 0 PULSE(0 3.3 0 1n 1n 5m 10m)\n"
        "V2 2 0 DC 3.3\n"
        "V3 3 0 PULSE(0 3.3 1m 1n 1n 5m 10m)\n"
        "BAND 4 0 V = (V(1)>1.5 && V(2)>1.5 && V(3)>1.5)?3.3:0\n"
        ".tran 0.1m 20m\n"
        ".end\n"
    )

    (out_dir / "README.md").write_text(
        "# SPICE Models\n\n"
        "These are simplified behavioral models intended for quick sanity checks.\n"
    )

    params = {
        "power_input": {"diode_model": "DGEN"},
        "pmic": {"rails": ["3V3", "1V8", "1V2", "1V0"]},
        "reset": {"logic": "3-input AND"},
    }
    args.out_json.write_text(json.dumps(params, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
