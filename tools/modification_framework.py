#!/usr/bin/env python3
"""Design modification framework for common hardware edits."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from pathlib import Path
from typing import Dict, List


@dataclass
class PowerRailModification:
    rail: str
    target_voltage: float
    feedback_top_ohm: float
    feedback_bottom_ohm: float

    def compute_new_divider(self) -> Dict[str, float]:
        return {
            "rail": self.rail,
            "target_voltage": self.target_voltage,
            "r_top_ohm": self.feedback_top_ohm,
            "r_bottom_ohm": self.feedback_bottom_ohm,
            "note": "Replace with PMIC datasheet equation when available.",
        }


@dataclass
class ComponentSubstitution:
    refdes: str
    new_part_number: str

    def validate(self) -> Dict[str, str]:
        return {
            "refdes": self.refdes,
            "new_part_number": self.new_part_number,
            "status": "unverified",
            "note": "Verify pinout and package compatibility against datasheets.",
        }


@dataclass
class ConnectorPinRemapping:
    connector: str
    pin: str
    new_net: str

    def validate(self) -> Dict[str, str]:
        return {
            "connector": self.connector,
            "pin": self.pin,
            "new_net": self.new_net,
            "status": "unverified",
            "note": "Update schematic symbol and connector pin table.",
        }


@dataclass
class FeatureRemoval:
    block: str
    refdes_list: List[str]

    def report(self) -> Dict[str, List[str]]:
        return {
            "block": self.block,
            "refdes_list": self.refdes_list,
            "action": "mark DNP",
        }


@dataclass
class FeatureAddition:
    name: str
    notes: str

    def report(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "notes": self.notes,
            "action": "create schematic + PCB update",
        }


def change_pmic_output(rail: str, new_voltage: float) -> Dict[str, str]:
    report = {
        "action": "change_pmic_output",
        "rail": rail,
        "new_voltage": new_voltage,
        "note": "Compute feedback divider per PMIC datasheet.",
    }
    _log_modification(report)
    return report


def add_test_point(net_name: str, location_hint: str) -> Dict[str, str]:
    report = {
        "action": "add_test_point",
        "net": net_name,
        "location_hint": location_hint,
        "note": "Select accessible location near connector or via.",
    }
    _log_modification(report)
    return report


def substitute_component(ref_des: str, new_part: str) -> Dict[str, str]:
    report = {
        "action": "substitute_component",
        "refdes": ref_des,
        "new_part": new_part,
        "note": "Validate pinout and footprint compatibility.",
    }
    _log_modification(report)
    return report


def _log_modification(entry: Dict[str, str]) -> None:
    path = Path("data/modification_history.json")
    history = []
    if path.exists():
        history = json.loads(path.read_text())
    entry["timestamp"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    history.append(entry)
    path.write_text(json.dumps(history, indent=2, sort_keys=True))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Validate only")
    args = ap.parse_args()

    if args.dry_run:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
