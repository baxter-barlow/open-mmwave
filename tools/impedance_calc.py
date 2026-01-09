#!/usr/bin/env python3
"""Calculate impedance targets from stackup data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional


OZ_TO_IN = 0.00137


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def microstrip_z0(width: float, height: float, er: float, t: float) -> float:
    # Hammerstad approximation for microstrip.
    if width <= 0 or height <= 0:
        return 0.0
    w_eff = width + t / 3.14159
    u = w_eff / height
    if u <= 1:
        z0 = (60 / (er**0.5)) * (1 / (u + 0.25 * u * u))
    else:
        z0 = (120 * 3.14159) / ((er**0.5) * (u + 1.393 + 0.667 * (u + 1.444) ** 0.5))
    return z0


def stripline_z0(width: float, height: float, er: float, t: float) -> float:
    # Symmetric stripline approximation.
    if width <= 0 or height <= 0:
        return 0.0
    return (60 / (er**0.5)) * (1 / (width / (height - t) + 0.441))


def solve_width(target_z0: float, height: float, er: float, t: float, mode: str) -> float:
    lo, hi = 0.001, 0.2
    for _ in range(60):
        mid = (lo + hi) / 2
        z0 = microstrip_z0(mid, height, er, t) if mode == "microstrip" else stripline_z0(mid, height, er, t)
        if z0 > target_z0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def diff_impedance(z0: float, spacing: float, height: float) -> float:
    # Simple edge-coupled microstrip diff approximation.
    if height <= 0:
        return 0.0
    return 2 * z0 * (1 - 0.48 * (2.71828 ** (-0.96 * spacing / height)))


def build_targets(stackup: Dict, er: float) -> Dict:
    layers = []
    for layer in stackup.get("layers", []):
        if layer.get("type") != "SIGNAL":
            continue
        name = layer.get("name")
        if name in ("TOP_LAYER", "BOTTOM_LAYER"):
            mode = "microstrip"
        else:
            mode = "stripline"
        height = layer.get("dielectric_in") or 0.0
        t = (layer.get("copper_weight_oz") or 0.0) * OZ_TO_IN
        if height == 0.0:
            continue
        width_50 = solve_width(50.0, height, er, t, mode)
        spacing = width_50
        z0 = microstrip_z0(width_50, height, er, t) if mode == "microstrip" else stripline_z0(width_50, height, er, t)
        z90 = diff_impedance(z0, spacing, height)
        width_90 = width_50
        width_100 = width_50
        layers.append(
            {
                "layer": name,
                "mode": mode,
                "height_in": height,
                "copper_thickness_in": t,
                "single_ended_50ohm_width_in": width_50,
                "diff_90ohm_width_in": width_90,
                "diff_90ohm_spacing_in": spacing,
                "diff_100ohm_width_in": width_100,
                "diff_100ohm_spacing_in": spacing,
                "estimated_diff_ohms_at_50_width": z90,
            }
        )
    return {
        "assumptions": {
            "er": er,
            "copper_thickness_from_oz": f"{OZ_TO_IN} in per oz/ft^2",
            "dielectric_in_source": "ODB layer attrlist .layer_dielectric",
            "diff_spacing_assumption": "spacing = width",
            "note": "Stackup lacks Dk and reference plane distances; results are approximate.",
        },
        "targets": layers,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stackup", type=Path, help="Stackup JSON")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--er", type=float, default=4.0, help="Relative dielectric constant")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        load_json(args.stackup)
        return 0

    stackup = load_json(args.stackup)
    data = build_targets(stackup, args.er)
    args.out.write_text(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
