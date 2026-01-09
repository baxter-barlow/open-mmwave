#!/usr/bin/env python3
"""Export data artifacts into Altium-friendly CSV formats."""
from __future__ import annotations

import csv
from pathlib import Path


def main() -> int:
    data = Path("data/component_placement.json")
    out = Path("data/component_placement_altium.csv")
    if not data.exists():
        return 0
    import json

    items = json.loads(data.read_text())
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Designator", "X(mil)", "Y(mil)", "Rotation", "Layer"])
        for it in items:
            writer.writerow([it["refdes"], it["x_mil"], it["y_mil"], it["rotation_deg"], it["side"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
