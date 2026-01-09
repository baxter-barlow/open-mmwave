#!/usr/bin/env python3
"""Generate minimal KiCad PCB with placed components."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
 ap = argparse.ArgumentParser()
 ap.add_argument("--placement", type=Path, required=True, help="Component placement JSON")
 ap.add_argument("--stackup", type=Path, required=True, help="ODB stackup JSON")
 ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
 ap.add_argument("--out-dir", type=Path, required=True, help="Output KiCad dir")
 ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
 args = ap.parse_args()

 if args.dry_run:
 json.loads(args.placement.read_text())
 json.loads(args.stackup.read_text())
 json.loads(args.netlist.read_text())
 return 0

 placement = json.loads(args.placement.read_text())
 out_dir = args.out_dir
 out_dir.mkdir(parents=True, exist_ok=True)
 fp_dir = out_dir / "footprints.pretty"
 fp_dir.mkdir(parents=True, exist_ok=True)

 (fp_dir / "GENERIC_FOOTPRINT.kicad_mod").write_text(
 "(footprint \"GENERIC_FOOTPRINT\"\n"
 "  (version 20231120)\n"
 "  (generator \"open_mmwave\")\n"
 "  (layer \"F.Cu\")\n"
 "  (attr smd)\n"
 "  (fp_text reference \"REF**\" (at 0 0) (layer \"F.SilkS\")\n"
 "    (effects (font (size 1 1) (thickness 0.15)))\n"
 "  )\n"
 "  (fp_text value \"GENERIC\" (at 0 -1) (layer \"F.Fab\")\n"
 "    (effects (font (size 1 1) (thickness 0.15)))\n"
 "  )\n"
 "  (fp_line (start -0.5 -0.5) (end 0.5 -0.5) (layer \"F.SilkS\")\n"
 "    (stroke (width 0.12) (type solid))\n"
 "  )\n"
 "  (fp_line (start 0.5 -0.5) (end 0.5 0.5) (layer \"F.SilkS\")\n"
 "    (stroke (width 0.12) (type solid))\n"
 "  )\n"
 "  (fp_line (start 0.5 0.5) (end -0.5 0.5) (layer \"F.SilkS\")\n"
 "    (stroke (width 0.12) (type solid))\n"
 "  )\n"
 "  (fp_line (start -0.5 0.5) (end -0.5 -0.5) (layer \"F.SilkS\")\n"
 "    (stroke (width 0.12) (type solid))\n"
 "  )\n"
 ")\n"
 )

 pcb_lines = [
 "(kicad_pcb (version 20211014) (generator codex))",
 " (general)",
 " (layers",
 " (0 F.Cu signal)",
 " (31 B.Cu signal)",
 " )",
 ]
 for item in placement:
 x_mm = item["x_mil"] * 0.0254
 y_mm = item["y_mil"] * 0.0254
 pcb_lines.append(
 f" (footprint \"GENERIC_FOOTPRINT\" (layer F.Cu) (at {x_mm:.3f} {y_mm:.3f})"
 f" (property \"Reference\" \"{item['refdes']}\") )"
 )
 pcb_lines.append(")")
 (out_dir / "open_mmwave.kicad_pcb").write_text("\n".join(pcb_lines))
 (out_dir / "open_mmwave.kicad_pro").write_text("{}")
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
