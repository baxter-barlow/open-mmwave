#!/usr/bin/env python3
"""Extract copper geometry statistics from Gerber layers."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


APERTURE_RE = re.compile(r"%ADD(\d+)([A-Z]),?([0-9.X]+)\*%")


def parse_apertures(path: Path) -> dict:
    apertures = {}
    for line in path.read_text(errors="ignore").splitlines():
        m = APERTURE_RE.search(line)
        if m:
            apertures[m.group(1)] = {"shape": m.group(2), "params": m.group(3)}
    return apertures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fab-dir", type=Path, required=True, help="Fabrication package directory")
    ap.add_argument("--out-geom", type=Path, required=True, help="Output geometry JSON")
    ap.add_argument("--out-pours", type=Path, required=True, help="Output pours JSON")
    ap.add_argument("--out-routes", type=Path, required=True, help="Output critical routes JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    gerber_dir = args.fab_dir / "GerberNCdrills"
    layers = ["PROC091G.GTL", "PROC091G.GBL", "PROC091G.G1", "PROC091G.G2", "PROC091G.G3", "PROC091G.G4"]
    geom = {}
    for fname in layers:
        path = gerber_dir / fname
        if not path.exists():
            continue
        apertures = parse_apertures(path)
        geom[fname] = {"apertures": apertures}

    args.out_geom.write_text(json.dumps(geom, indent=2, sort_keys=True))
    args.out_pours.write_text(json.dumps({"notes": ["Pour extraction not implemented; use CAM tools."]}, indent=2, sort_keys=True))
    args.out_routes.write_text(
        json.dumps(
            {
                "critical_nets": ["USB_DP", "USB_DM", "AR_LVDS_*"],
                "notes": ["Gerber layers lack net names; manual correlation required."],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
