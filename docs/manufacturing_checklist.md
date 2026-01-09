# Manufacturing Checklist - open_mmwave Rev G

Sources: `data/manufacturing_validation.json`, fabrication package.

## Gerber Completeness
- Verify all required Gerber layers present (see `data/manufacturing_validation.json` for missing list).

## Drill Files
- Review drill tool sizes from the fabrication package.
- Confirm plated vs non-plated hole counts in CAM.
- Drill summary is captured in `data/drill_analysis.json`.

## Pick-and-Place vs BOM
- Compare PnP refdes list against BOM and IPC netlist.
- Investigate any missing-from-netlist or missing-from-PnP entries in `data/manufacturing_validation.json`.

## Layer Count
- Confirm 8 signal layers in ODB matrix from the fabrication package.

## Netlist Consistency
- Confirm both IPC netlist and ODB netlist are present in the fabrication package.
