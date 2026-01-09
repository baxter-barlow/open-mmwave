# ERC Preparation Status (Rev G)

## Updates
- U3 (CP2105) confirmed in usb_uart schematic from IPC netlist mapping (`data/netlist_revG.json`).
- A1 (antenna) moved to soc_core and now uses dedicated ANTENNA symbol; Y1–Y4 verified by net association from IPC netlist.
- Pin electrical type inference tightened in `tools/kicad_schematic_gen.py` using net naming rules.
- Footprint assignments now use package hints from `data/component_placement.json` and size strings in `data/bom_production.csv` when available.
- PWR_FLAG symbols inserted per sheet for detected power nets (GND/VCC/5V/3V/PMIC_/AR_1*).

## Footprint Coverage
- Passives: 0201/0402/0603/0805 footprint selection uses placement package hints (fallback to BOM description).
- ICs: U1/U2/U3/U19 mapped to QFN/BGA/SOIC packages; remaining ICs use GENERIC until package confirmation.

## Known Gaps
- PWR_FLAG is placed on local sheet labels (no global label resolution). ERC still benefits, but true inter-sheet connectivity remains schematic-level placeholder.
- GENERIC footprints remain for passives lacking package hints or BOM sizing text.

## Next Verification
- Open in KiCad 7+ and run ERC to confirm PWR_FLAG coverage and pin-type warnings.
- Cross-check package assumptions for GENERIC footprints against datasheets or the Altium PCB footprint list.
