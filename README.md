# open_mmwave

open_mmwave is an open-source mmWave radar hardware platform. This repository contains the KiCad design, documentation, and supporting analysis tools.

## Capabilities
- Multi-rail power tree with on-board regulation and sequencing
- USB-to-UART interface for bring-up and debug
- High-density connector breakout and test points for validation
- Structured documentation and generated analysis artifacts

## Repository Layout
- `kicad/`: Schematic, PCB, and symbol/footprint libraries
- `docs/`: Hardware documentation and checklists
- `tools/`: Scripts for generating and validating data artifacts
- `data/`: Generated JSON/HTML outputs (sanitized)
- `release/`: Release artifacts and reports

## Getting Started
1. Open the KiCad project at `kicad/open_mmwave.kicad_pro`.
2. Start with `docs/INDEX.md` for documentation entry points.
3. Review `docs/bringup_revG.md` for power-up and validation guidance.
4. Use `docs/pcb_design_rules.md` and `docs/power_tree_revG.md` for layout prep.

## Contributing
See `CONTRIBUTING.md` for workflow, checks, and expectations.

## Notes
Local vendor reference materials are gitignored and should not be committed.
