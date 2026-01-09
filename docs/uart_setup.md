# UART Setup - open_mmwave Rev G

Sources: `data/netlist_revG.json`, schematic source files.

## CP2105 (U3) Channel Mapping
| Channel | Signals | Evidence |
|---|---|---|
| Channel A | AR_MSS_LOGGER (TP26) | Netlist: `AR_MSS_LOGGER` on U3 pin 20. |
| Channel B | USB_AR_RS232TX / USB_AR_RS232RX | Netlist: `USB_AR_RS232TX` on U3 pin 12, `USB_AR_RS232RX` on U3 pin 13. |

## UART Mux Control
UART selection is controlled by UART_MUX_CTRL1 and UART_MUX_CTRL2.

| Net | Connected components | Evidence |
|---|---|---|
| UART_MUX_CTRL1 | S1 pin1, U18 pins 1/5, R19 | IPC netlist |
| UART_MUX_CTRL2 | S1 pin2, U15 pins 1/5, R1 | IPC netlist |

## Breakaway UART
| Net | Destination | Evidence |
|---|---|---|
| BREAK_RS232TX | TP18, U15 pin 10 | IPC netlist |
| BREAK_RS232RX | TP19, U15 pin 6 | IPC netlist |

## Driver Notes
The repository does not include CP2105 driver installers. Use Silicon Labs CP210x VCP drivers for host PCs and verify enumeration in the OS device manager.

## Expected Baud Rates
Baud rates are firmware-dependent and not listed in this repository. Verify in vendor SDK or mmWave demo firmware documentation.
