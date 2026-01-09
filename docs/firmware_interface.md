# Firmware Interface - open_mmwave Rev G

Sources: `data/pin_mux_config.json`, `docs/boot_modes.md`, `docs/uart_setup.md`, `docs/interface_map_revG.md`.

## Memory Map
- Not available in this repository. Use radar SoC TRM for peripheral base addresses.

## Pin Mux Configuration
- Extracted U2 pin-to-net mapping is provided in `data/pin_mux_config.json`.
- This mapping is netlist-based and does not include functional mux settings.

## Boot Sequence
- SOP straps and switch positions documented in `docs/boot_modes.md`.

## UART Console
- CP2105 UART mapping documented in `docs/uart_setup.md`.
- Expected baud rate and boot logs are firmware-dependent and not included in the repo.

## JTAG Debug
- JTAG signals are routed through J2/J11 (see `docs/interface_map_revG.md`).
- Debug probe setup must follow component documentation.

## Flash Programming
- No UniFlash procedure in the repo. Follow vendor flashing tool documentation and SOP boot modes.
