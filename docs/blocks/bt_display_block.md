# Bt Display Block

Source: `data/schematic_blocks.json`, BOM, IPC netlist.

## Component List
| Refdes | Value | Description | Part Number |
|---|---|---|---|
| J7 |  | CONN HEADER R/A 10POS 1.27MM | GRPB052MWCN-RC |
| R102 |  | RES SMD 0 OHM JUMPER 1/20W 0201 | RC0201JR-070RL |
| R90 |  | RES SMD 0 OHM JUMPER 1/20W 0201 | RC0201JR-070RL |
| R91 |  | RES SMD 0 OHM JUMPER 1/20W 0201 | RC0201JR-070RL |
| U10 |  | Low-Voltage 8-Bit I2C and SMBus I/O Expander, 1.65 to 5.5 V, -40 to 85 degC, 16-pin UQFN (RSV), Green (RoHS & no Sb/Br) | TCA6408ARSVR |
| U8 |  | SimpleLink(TM) Bluetooth(R) 5 low energy Wireless MCU, RGZ0048A (VQFN-48) | CC2642R1FRGZR |

## Nets
ALERT, AR_CS1_BT, AR_RS232RX_BT, AR_RS232TX_BT, BT_RST, BT_UART_RX, BT_UART_TX, DCDC_SW, DIO6_GLED, DISP, GND, INTN, JTAG_TCK, JTAG_TDI, JTAG_TDO, JTAG_TMS, MRDY, NET5, NetC24_1, NetR100_2, NetR101_1, NetR112_2, NetR113_2, NetR131_2, NetR161_2, NetR30_2, NetR86_2, NetR87_2, NetR99_1, RESETN, RF_N, RF_P, SENS_NRST, SRDY, VCC_BA_3V3, VDDR, VDDS, X32K_Q1, X32K_Q2, X48M_N, X48M_P, nRESET

## Power Rails
VCC_BA_3V3

## Notes
- Block extraction is netlist-based; schematic annotations were not parsed.
