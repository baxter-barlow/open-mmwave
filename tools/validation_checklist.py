#!/usr/bin/env python3
"""Generate pre-production validation checklist."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_checklist() -> dict:
 return {
 "electrical": [
 "All power rails within ±5% of nominal",
 "PMIC PGOOD asserts within 100 ms",
 "Junction temperatures below 100°C at 40°C ambient",
 "USB enumeration successful",
 "UART communication at expected baud rate",
 ],
 "mechanical": [
 "Board dimensions match specification",
 "Mounting holes aligned",
 "Connector footprints verified",
 "Keepout zones respected",
 ],
 "rf": [
 "Antenna pattern verification points",
 "RF isolation measurements",
 "mmWave signal integrity checks",
 ],
 }


def main() -> int:
 ap = argparse.ArgumentParser()
 ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
 ap.add_argument("--out-md", type=Path, required=True, help="Output Markdown path")
 ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
 args = ap.parse_args()

 if args.dry_run:
 return 0

 data = build_checklist()
 args.out.write_text(json.dumps(data, indent=2, sort_keys=True))
 lines = ["# Validation Checklist - open_mmwave Rev G", ""]
 for section, items in data.items():
 lines.append(f"## {section.title()}")
 for item in items:
 lines.append(f"- [ ] {item}")
 lines.append("")
 args.out_md.write_text("\n".join(lines).strip() + "\n")
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
