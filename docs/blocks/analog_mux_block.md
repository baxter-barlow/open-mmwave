# Analog Mux Block

Source: `data/schematic_blocks.json`, BOM, IPC netlist.

## Component List
| Refdes | Value | Description | Part Number |
|---|---|---|---|
| R1 |  | 10 kOhms ±0.5% 0.05W, 1/20W Chip Resistor 0201 (0603 Metric)  Thin Film | RR0306P-103-D |
| R19 |  | 10 kOhms ±0.5% 0.05W, 1/20W Chip Resistor 0201 (0603 Metric)  Thin Film | RR0306P-103-D |
| S1 |  | Switch, Slide, SPST 4 poles, SMT | 218-4LPST |
| U15 |  | Dual 10-ohm SPDT Analog Switch, RSE0010A (UQFN-10) | TS5A23157RSER |
| U18 |  | Dual 10-ohm SPDT Analog Switch, RSE0010A (UQFN-10) | TS5A23157RSER |

## Nets
AR_RS232RX, AR_RS232RX_BT, AR_RS232TX, AR_RS232TX_BT, BREAK_RS232RX, BREAK_RS232TX, GND, NET6, NET7, NetR16_2, PMIC_3V3, SOP0, SOP1, UART_MUX_CTRL1, UART_MUX_CTRL2, USB_AR_RS232RX, USB_AR_RS232TX, VCC_BA_3V3

## Power Rails
PMIC_3V3, VCC_BA_3V3

## Notes
- Block extraction is netlist-based; schematic annotations were not parsed.
