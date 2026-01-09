# Reproduction Guide - open_mmwave Rev G

Sources: fabrication package, `docs/hardware_reference.md`, `docs/modification_guide.md`.

## Prerequisites
- CAD: Altium Designer or viewer for SchDoc/PCB.
- Fabrication: CAM tool supporting Gerber/ODB.
- Assembly: pick-and-place capability for BGA/QFN parts.

## Bill of Materials
- Use the exported BOM from the component database or ERP.
- Cross-check with `data/bom_netlist_correlation.json`.

## Fabrication Package
- Send Gerber/NC drill outputs from the fabrication package.
- Optionally provide an ODB archive from the fabrication package.

## Assembly Package
- Pick and place file from the fabrication package.
- Stencil thickness and paste aperture are not documented in repo; verify with CM.

## Programming
- Boot modes: `docs/boot_modes.md`.
- UART setup: `docs/uart_setup.md`.
- Flashing: follow vendor flashing tool (not included in repo).

## Validation
- Use `tools/hw_test_framework.py` and `docs/power_validation_checklist.md`.
- Signal integrity checklist: `docs/signal_integrity.md`.

## Modifications
- See `docs/modification_guide.md` and `data/modification_templates.json`.

## Troubleshooting
- See `docs/troubleshooting.md`.
