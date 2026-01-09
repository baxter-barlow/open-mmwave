#!/usr/bin/env python3
"""Generate alternative component sourcing guidance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict


DEFAULT_ALTS = {
 "U1": {
 "part": "LP87524",
 "alternatives": [],
 "risk": "single-source PMIC; no in-repo alternatives.",
 },
 "U3": {
 "part": "CP2105",
 "alternatives": [],
 "risk": "No alternatives listed in repo; verify USB-UART compatibility externally.",
 },
 "U19": {
 "part": "TPS2115A",
 "alternatives": [],
 "risk": "No alternatives listed in repo; verify power mux requirements externally.",
 },
 "connectors": {
 "part": "Samtec QSH-030-01-L-D-A / Molex 105017-0001",
 "alternatives": [],
 "risk": "Connector footprint compatibility must be verified.",
 },
 "passives": {
 "part": "R/C/L/FL parts",
 "alternatives": ["Generic equivalents with same package and rating"],
 "risk": "Match voltage/current/temp and ESR/ESL as required.",
 },
}


def main() -> int:
 ap = argparse.ArgumentParser()
 ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
 ap.add_argument("--dry-run", action="store_true", help="Validate only")
 args = ap.parse_args()

 if args.dry_run:
 return 0

 data = {
 "source": "Repository BOM only; no validated alternates included.",
 "alternatives": DEFAULT_ALTS,
 }
 args.out.write_text(json.dumps(data, indent=2, sort_keys=True))

 lifecycle = {
 "source": "No lifecycle data in repo; placeholder statuses.",
 "components": {
 "U1": {"part": "LP87524", "lifecycle": "unknown", "risk": "single-source"},
 "U2": {"part": "radar SoC", "lifecycle": "unknown", "risk": "single-source"},
 "U3": {"part": "CP2105", "lifecycle": "unknown", "risk": "single-source"},
 "U19": {"part": "TPS2115A", "lifecycle": "unknown", "risk": "single-source"},
 },
 }
 Path("data/component_lifecycle.json").write_text(json.dumps(lifecycle, indent=2, sort_keys=True))

 risk = {
 "scores": {
 "U1": 8,
 "U2": 8,
 "U3": 6,
 "U19": 6,
 },
 "notes": ["Scores are heuristic; replace with supplier data."],
 }
 Path("data/supply_chain_risk.json").write_text(json.dumps(risk, indent=2, sort_keys=True))
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
