#!/usr/bin/env python3
"""Generate KiCad 7 hierarchical schematic with shared symbols."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import csv
import re


SHEET_MAP = {
    "pmic_block": "pmic.kicad_sch",
    "usb_uart_block": "usb_uart.kicad_sch",
    "hd_connector_block": "hd_connector.kicad_sch",
    "soc_core_block": "soc_core.kicad_sch",
    "reset_gpio_block": "gpio_reset.kicad_sch",
    "bt_display_block": "display_bt.kicad_sch",
    "can_interface_block": "gpio_reset.kicad_sch",
    "analog_mux_block": "display_bt.kicad_sch",
}


POWER_INPUT_REFS = {
    "U19",
    "D1",
    "D2",
    "C1",
    "C4",
    "C42",
    "C93",
    "C99",
    "C122",
    "FL1",
    "FL2",
    "FL3",
}


POWER_NET_PREFIXES = ("GND", "VCC", "5V", "3V", "PMIC_", "AR_1", "VCC_BA_3V3")


def _pin_type_from_net(net: str, ref: str) -> str:
    if net.startswith(("GND", "VCC", "5V", "3V")):
        return "power_in"
    if net.startswith("PMIC_") and ref == "U1":
        return "power_out"
    if net.startswith(("PMIC_", "VCC_")):
        return "power_in"
    if net.startswith(("AR_1P", "AR_1V")):
        return "power_in"
    if "RST" in net or "RESET" in net or "NRST" in net:
        return "input"
    if "EN" in net:
        return "input"
    if "TX" in net or "MOSI" in net or net.endswith("CLK"):
        return "output"
    if "RX" in net or "MISO" in net:
        return "input"
    if "SCL" in net:
        return "output"
    if "SDA" in net or "GPIO" in net:
        return "bidirectional"
    if net.startswith(("USB_", "AR_", "HD_", "SPI", "I2C", "UART", "CAN")):
        return "bidirectional"
    if ref.startswith(("C", "R", "L", "Y", "D", "TP")):
        return "passive"
    return "unspecified"


def _extract_pkg_size(desc: str) -> str | None:
    if not desc:
        return None
    match = re.search(r"\b(0201|0402|0603|0805)\b", desc)
    return match.group(1) if match else None


def _normalize_pkg_token(token: str) -> str | None:
    if not token:
        return None
    token = token.strip()
    for size in ("0201", "0402", "0603", "0805"):
        if size in token:
            return size
    numeric = token.replace(".", "")
    if numeric in ("201", "402", "603", "805"):
        return {
            "201": "0201",
            "402": "0402",
            "603": "0603",
            "805": "0805",
        }[numeric]
    return None


def _load_pkg_map(bom_path: Path | None, placement_path: Path | None) -> Dict[str, str]:
    pkg_map: Dict[str, str] = {}
    if placement_path and placement_path.exists():
        try:
            placement = json.loads(placement_path.read_text())
            for item in placement:
                ref = item.get("refdes")
                pkg = _normalize_pkg_token(item.get("package", ""))
                if ref and pkg:
                    pkg_map[ref] = pkg
        except json.JSONDecodeError:
            pass
    if bom_path and bom_path.exists():
        with bom_path.open() as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                ref = row.get("RefDes", "")
                if not ref or ref in pkg_map:
                    continue
                pkg = _extract_pkg_size(row.get("Description", "") or "")
                if pkg:
                    pkg_map[ref] = pkg
    return pkg_map


def _power_nets(nets: Iterable[str]) -> List[str]:
    power = []
    for net in nets:
        if net.startswith(POWER_NET_PREFIXES):
            power.append(net)
    return sorted(set(power))


def _symbol_name(ref: str, pins: List[str]) -> str:
    if ref == "U1":
        return "LP87524"
    if ref == "U2":
        return "RADAR_SOC"
    if ref == "U3":
        return "CP2105"
    if ref == "U19":
        return "TPS2115A"
    if ref == "A1":
        return "ANTENNA"
    if ref.startswith("C"):
        return "CAP"
    if ref.startswith("R"):
        return "RES"
    if ref.startswith("L"):
        return "IND"
    if ref.startswith("D"):
        return "DIODE"
    if ref.startswith("TP"):
        return "TP"
    if ref.startswith("J"):
        return f"CONN_{len(pins)}"
    if ref.startswith("FL"):
        return "FERRITE"
    if ref.startswith("SW"):
        return "SWITCH"
    if ref.startswith("Y"):
        return "XTAL"
    if ref.startswith("U"):
        return f"IC_{len(pins)}"
    return "GENERIC"


def _build_symbol_lib(symbols: Dict[str, List[str]], comp_to_pins: Dict, sym_ref_map: Dict[str, str]) -> str:
    lines = ["(kicad_symbol_lib (version 20231120) (generator codex))"]
    for name, pin_list in symbols.items():
        lines.append(f"  (symbol \"{name}\" (in_bom yes) (on_board yes)")
        lines.append("    (property \"Reference\" \"REF\" (at 0 2 0))")
        lines.append("    (property \"Value\" \"VAL\" (at 0 -2 0))")
        lines.append("    (graphic (rectangle (start -6 -6) (end 6 6)))")
        y = 4
        ref = sym_ref_map.get(name)
        for pin in pin_list:
            pin_type = "passive"
            if ref and ref in comp_to_pins:
                net = comp_to_pins[ref].get(pin, "")
                if net:
                    pin_type = _pin_type_from_net(net, ref)
            lines.append(
                f"    (pin {pin_type} line (at -8 {y} 0) (length 2) (name \"{pin}\") (number \"{pin}\"))"
            )
            y -= 2
        lines.append("  )")
    lines.append("  (symbol \"PWR_FLAG\" (in_bom no) (on_board yes)")
    lines.append("    (property \"Reference\" \"#PWR\" (at 0 2 0))")
    lines.append("    (property \"Value\" \"PWR_FLAG\" (at 0 -2 0))")
    lines.append("    (graphic (rectangle (start -3 -3) (end 3 3)))")
    lines.append("    (pin power_out line (at -6 0 0) (length 2) (name \"PWR\") (number \"1\"))")
    lines.append("  )")
    lines.append(")")
    return "\n".join(lines)


def _write_sheet(
    path: Path,
    comps: List[str],
    comp_to_pins: Dict,
    values: Dict,
    footprints: Dict[str, str],
) -> None:
    lines = [
        "(kicad_sch (version 20231120) (generator codex))",
        "  (paper \"A4\")",
    ]
    x0, y0 = 20, 20
    dx, dy = 40, 20
    for idx, comp in enumerate(sorted(comps)):
        x = x0 + (idx % 5) * dx
        y = y0 + (idx // 5) * dy
        pins = sorted(comp_to_pins.get(comp, {}).keys(), key=lambda p: (len(p), p))
        sym_name = _symbol_name(comp, pins)
        val = values.get(comp, comp)
        footprint = footprints.get(comp, "")
        lines.append(
            f"  (symbol (lib_id \"open_mmwave:{sym_name}\") (at {x} {y})"
            f" (property \"Reference\" \"{comp}\" (at {x} {y} 0))"
            f" (property \"Value\" \"{val}\" (at {x} {y+2} 0))"
            f" (property \"Footprint\" \"{footprint}\" (at {x} {y+4} 0)))"
        )
        for pin in pins:
            net = comp_to_pins[comp][pin]
            x1 = x - 6
            y1 = y
            lines.append(f"  (wire (pts (xy {x1} {y1}) (xy {x1-4} {y1})))")
            lines.append(f"  (label (at {x1-4} {y1}) (text \"{net}\"))")
            y -= 2
    # Add PWR_FLAG symbols for power nets in this sheet.
    sheet_nets = []
    for comp in comps:
        sheet_nets.extend(comp_to_pins.get(comp, {}).values())
    for idx, net in enumerate(_power_nets(sheet_nets)):
        x = 20 + (idx % 6) * 15
        y = 260 + (idx // 6) * 10
        ref = f"#PWR_{path.stem}_{idx}"
        lines.append(
            f"  (symbol (lib_id \"open_mmwave:PWR_FLAG\") (at {x} {y})"
            f" (property \"Reference\" \"{ref}\" (at {x} {y} 0))"
            f" (property \"Value\" \"PWR_FLAG\" (at {x} {y+2} 0)))"
        )
        lines.append(f"  (label (at {x+4} {y}) (text \"{net}\"))")
    lines.append(")")
    path.write_text("\n".join(lines))


def _infer_sheet_from_nets(ref: str, nets: List[str]) -> str:
    if ref == "U1":
        return "pmic.kicad_sch"
    if ref == "U2":
        return "soc_core.kicad_sch"
    if ref == "U3":
        return "usb_uart.kicad_sch"
    if ref == "U19":
        return "power_input.kicad_sch"
    if ref == "A1":
        return "soc_core.kicad_sch"
    if any(n.startswith("PMIC_") for n in nets):
        return "pmic.kicad_sch"
    if any(n.startswith("USB_") for n in nets):
        return "usb_uart.kicad_sch"
    if any(n.startswith("HD_") for n in nets):
        return "hd_connector.kicad_sch"
    if any(n.startswith(("X48M_", "X32K_", "XIN32", "XOUT32")) for n in nets):
        return "display_bt.kicad_sch"
    if any(n.startswith("AR_") for n in nets):
        return "soc_core.kicad_sch"
    if any(n.startswith("BT_") or n.startswith("DISP") for n in nets):
        return "display_bt.kicad_sch"
    if any(n.endswith("NRST") or n.startswith("SOP") or n.startswith("RESET") for n in nets):
        return "gpio_reset.kicad_sch"
    if ref.startswith("TP") or ref.startswith("SW"):
        return "gpio_reset.kicad_sch"
    return "misc.kicad_sch"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--netlist", type=Path, required=True, help="Netlist JSON")
    ap.add_argument("--values", type=Path, required=True, help="Component values JSON")
    ap.add_argument("--blocks", type=Path, required=True, help="Blocks JSON")
    ap.add_argument("--out-dir", type=Path, required=True, help="Output KiCad dir")
    ap.add_argument("--bom", type=Path, default=Path("data/bom_production.csv"), help="BOM CSV for package sizes")
    ap.add_argument(
        "--placement",
        type=Path,
        default=Path("data/component_placement.json"),
        help="Placement JSON for package hints",
    )
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        json.loads(args.netlist.read_text())
        json.loads(args.values.read_text())
        json.loads(args.blocks.read_text())
        return 0

    netlist = json.loads(args.netlist.read_text())
    values = json.loads(args.values.read_text())
    blocks = json.loads(args.blocks.read_text()).get("blocks", {})
    pkg_map = _load_pkg_map(args.bom, args.placement)
    comp_to_pins = netlist.get("comp_to_pins", {})

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    comp_to_sheet = {}
    for block_name, block in blocks.items():
        sheet = SHEET_MAP.get(block_name)
        if not sheet:
            continue
        for comp in block.get("components", []):
            comp_to_sheet[comp] = sheet

    for comp in POWER_INPUT_REFS:
        if comp in comp_to_pins:
            comp_to_sheet[comp] = "power_input.kicad_sch"

    sheets = {
        "power_input.kicad_sch": [],
        "pmic.kicad_sch": [],
        "soc_core.kicad_sch": [],
        "usb_uart.kicad_sch": [],
        "hd_connector.kicad_sch": [],
        "gpio_reset.kicad_sch": [],
        "display_bt.kicad_sch": [],
        "misc.kicad_sch": [],
    }

    for comp, pins in comp_to_pins.items():
        nets = list(pins.values())
        sheet = _infer_sheet_from_nets(comp, nets)
        # allow explicit override for power input list
        if comp in POWER_INPUT_REFS:
            sheet = "power_input.kicad_sch"
        comp_to_sheet[comp] = sheet
        sheets[sheet].append(comp)

    # Build symbol library with shared types
    symbols: Dict[str, List[str]] = {}
    sym_ref_map: Dict[str, str] = {}
    for comp, pins_map in comp_to_pins.items():
        pins = sorted(pins_map.keys(), key=lambda p: (len(p), p))
        sym = _symbol_name(comp, pins)
        if sym not in symbols:
            symbols[sym] = pins if sym in ("LP87524", "RADAR_SOC", "CP2105", "TPS2115A") else (
                ["1", "2"] if sym in ("CAP", "RES", "IND", "DIODE", "TP", "FERRITE") else pins
            )
            if sym in ("LP87524", "RADAR_SOC", "CP2105", "TPS2115A"):
                sym_ref_map[sym] = comp

    sym_text = _build_symbol_lib(symbols, comp_to_pins, sym_ref_map)
    (out_dir / "open_mmwave.kicad_sym").write_text(sym_text)
    (out_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        "  (lib (name open_mmwave) (type KiCad) (uri \"${KIPRJMOD}/open_mmwave.kicad_sym\") (options \"\") (descr \"\"))\n"
        ")\n"
    )

    # Root schematic with sheets
    root_lines = [
        "(kicad_sch (version 20231120) (generator codex))",
        "  (paper \"A4\")",
    ]
    x, y = 20, 20
    for sheet_name in [k for k in sheets.keys() if k != "misc.kicad_sch"]:
        root_lines.append(
            f"  (sheet (at {x} {y}) (size 60 20)"
            f" (property \"Sheet name\" \"{Path(sheet_name).stem}\")"
            f" (property \"Sheet file\" \"{sheet_name}\"))"
        )
        y += 30
        if y > 200:
            y = 20
            x += 80
    root_lines.append(")")
    (out_dir / "open_mmwave.kicad_sch").write_text("\n".join(root_lines))

    # Footprint mapping
    footprints = {}
    for comp in comp_to_pins.keys():
        if comp == "U1":
            footprints[comp] = "open_mmwave:QFN-24_4x4mm"
        elif comp == "U2":
            footprints[comp] = "open_mmwave:BGA-141_10.4x10.4mm"
        elif comp == "U3":
            footprints[comp] = "open_mmwave:QFN-24_4x4mm"
        elif comp == "U19":
            footprints[comp] = "open_mmwave:SOIC-8"
        elif comp.startswith(("C", "R", "L")):
            size = pkg_map.get(comp)
            if size:
                footprints[comp] = f"open_mmwave:{size}"
            else:
                footprints[comp] = "open_mmwave:GENERIC"
        elif comp.startswith("D"):
            footprints[comp] = "open_mmwave:SOT-23"
        elif comp.startswith("J"):
            footprints[comp] = "open_mmwave:CONN"
        elif comp.startswith("Y"):
            footprints[comp] = "open_mmwave:XTAL_4P"
        else:
            footprints[comp] = "open_mmwave:GENERIC"

    for sheet_name, comps in sheets.items():
        _write_sheet(out_dir / sheet_name, comps, comp_to_pins, values, footprints)

    (out_dir / "README.md").write_text("# KiCad Export\n\nHierarchical schematic generated.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
