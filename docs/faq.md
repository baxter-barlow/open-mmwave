# FAQ - open_mmwave Rev G

## Where are the schematics?
See `kicad/open_mmwave.kicad_sch`.

## How do I power the board?
Use J1 (USB), J5 (breakaway USB power-only), or J2 (5V_HD_IN). See `docs/bringup_revG.md`.

## How do I program the device?
Use SOP boot modes and vendor flashing tool (not included in repo). See `docs/boot_modes.md`.

## Where is the full connector pinout?
See `docs/interface_map_revG.md`.

## What is the test procedure?
Use `docs/power_validation_checklist.md` and `tools/hw_test_framework.py`.
