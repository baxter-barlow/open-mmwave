# Getting Started - open_mmwave Rev G

## Repo Overview
- `tools/`: analysis and validation scripts
- `data/`: generated JSON/CSV artifacts
- `docs/`: documentation and guides

## Quick Start
1. Run `python tools/ipc_parser.py -o data/netlist_revG.json <ipc_netlist_path>`
2. Run `python tools/power_validator.py --netlist data/netlist_revG.json --pmic data/pmic_mapping.json --out-json data/power_validation_procedure.json --out-md docs/power_validation_checklist.md`
3. Review `docs/hardware_reference.md`
