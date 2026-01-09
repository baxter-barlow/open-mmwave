# Architecture Overview - open_mmwave Rev G

## System Block Diagram
- SoC (U2) with PMIC (U1) and power mux (U19)
- USB-UART bridge (U3)
- HD connectors (J2/J11) for external interfaces

## Power Architecture
See `docs/power_tree_revG.md` and `docs/hardware_reference.md`.

## Signal Flow
UART and LVDS routed through J2/J11, optional breakaway via J11.
