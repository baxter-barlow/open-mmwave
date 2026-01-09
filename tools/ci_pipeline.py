#!/usr/bin/env python3
"""Generate CI pipeline checks and baselines."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def checksum(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", type=Path, required=True, help="Baseline JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    files = [
        "data/netlist_revG.json",
        "data/thermal_analysis.json",
        "data/impedance_targets.json",
        "data/bom_netlist_correlation.json",
    ]
    baseline = {f: checksum(Path(f)) for f in files if Path(f).exists()}
    args.baseline.write_text(json.dumps(baseline, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
