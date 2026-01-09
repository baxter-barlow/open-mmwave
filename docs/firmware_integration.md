# Firmware Integration Package - open_mmwave Rev G

Sources: `data/pin_mux_config.json`, `docs/boot_modes.md`, `docs/interface_map_revG.md`.

## Memory Map Summary
- Not present in repo; use radar SoC TRM for base addresses and memory regions.

## Pin Configuration Table
Pin-to-net mapping is available in `data/pin_mux_config.json`.

## Boot Mode Configuration
See `docs/boot_modes.md` for SOP switch positions and expected behavior.

## Debug Interface
JTAG pins are on J2/J11 per `docs/interface_map_revG.md`.
Recommended probes: JTAG probe or equivalent (verify with component datasheet).
