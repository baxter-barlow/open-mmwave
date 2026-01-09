# Signal Integrity Checklist - open_mmwave Rev G

Sources: `data/signal_integrity_checklist.json`, `data/impedance_targets.json`, IPC netlist.

## USB 2.0
- Nets: USB_DP, USB_DM
- Target: 90 ohm differential

## LVDS
- Nets: AR_LVDS_*_P/N
- Target: 100 ohm differential

## SPI
- Nets: SPI_* / HD_SPI_*
- Target: 50 ohm single-ended

## JTAG
- Nets: HD_AR_T* / AR_T*
- Target: 50 ohm single-ended

## UART
- Nets: UART_* / RS232* / AR_MSS_LOGGER
- Target: 50 ohm single-ended

## Routing Notes
- Refer to `data/impedance_targets.json` for layer-specific width recommendations and assumptions (Dk=4.3).
