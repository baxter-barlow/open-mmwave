# Interface Map - open_mmwave Rev G

Sources: schematic source files, IPC netlist.

## USB Connector J1 (Micro-USB, Main)
- Part: Molex 105017-0001 (BOM).
- Sheet: schematic source sheet 6.

| Pin | Net | Notes |
|---|---|---|
| 1 | USB_5V | Feeds 5V_IN via FL2 and D1 (power input). |
| 2 | USB_DM | USB D- to CP2105 U3. |
| 3 | USB_DP | USB D+ to CP2105 U3. |
| 4 | (ID) | Not shown in text extraction; verify in schematic symbol. |
| 5 | GND | Ground. |

## USB Connector J5 (Micro-USB, Breakaway)
- Part: Molex 105017-0001 (BOM).
- Sheet: schematic source sheet 10.

| Pin | Net | Notes |
|---|---|---|
| 1 | USB_5V_B | Feeds 5V_IN_B via FL14. |
| 2 | NC | Not present in IPC netlist for J5; no D+/D- shown in sheet 10 text extraction. |
| 3 | NC | Not present in IPC netlist for J5; no D+/D- shown in sheet 10 text extraction. |
| 4 | NC | ID pin not present in IPC netlist for J5. |
| 5 | GND | Ground. |

## HD Connector J2 (60-pin)
- Part: Samtec QSH-030-01-L-D-A (BOM).
- Sheet: schematic source sheet 7.
- Pin mapping extracted from IPC netlist; pins without net labels on sheet 7 are treated as NC and recorded as such in `data/connector_pinouts.json`.

| Pin | Net | Notes |
|---|---|
| 1 | NC | No net name in IPC netlist for J2 pin 1. |
| 2 | 5V_HD_IN | Input to U19 TPS2115A. |
| 3 | NC | No net name in IPC netlist for J2 pin 3. |
| 4 | NC | No net name in IPC netlist for J2 pin 4. |
| 5 | NC | No net name in IPC netlist for J2 pin 5. |
| 6 | NC | No net name in IPC netlist for J2 pin 6. |
| 7 | NC | No net name in IPC netlist for J2 pin 7. |
| 8 | HD_AR_DMM_SYNC | Direct net. |
| 9 | NC | No net name in IPC netlist for J2 pin 9. |
| 10 | HD_AR_DMM_CLK | Direct net. |
| 11 | HD_AR_TDI | Direct net. |
| 12 | AR_NRST_1 | Via RA9 (EXB-18VR000X pin 1-8 pair). Evidence: connector schematic source pin pairing + IPC netlist RA9 pin1/8. |
| 13 | HD_AR_TMS | Direct net. |
| 14 | PGOOD | Via RA9 (pin 2-7 pair). Evidence: connector schematic source pin pairing + IPC netlist RA9 pin2/7. |
| 15 | HD_AR_TCK | Direct net. |
| 16 | HD_AR_HOSTINTR1 | NET9 maps to HD_AR_HOSTINTR1 (IPC netlist NNAMENET9). |
| 17 | HD_AR_TDO_SOP0 | Direct net. |
| 18 | AR_MSS_LOGGER | Via RA9 (pin 4-5 pair) -> NetR58_2 -> R58 -> AR_MSS_LOGGER. Evidence: connector schematic source pin pairing + IPC netlist RA9 pin4/5, R58. |
| 19 | HD_AR_CS1 | Direct net. |
| 20 | GND | Ground. |
| 21 | HD_SPI_CLK1 | Direct net. |
| 22 | AR_LVDS_FRCLK_N | Via RA8 (pin 1-8 pair) -> NET1 -> AR_LVDS_FRCLK_N. Evidence: connector schematic source pin pairing + IPC netlist RA8, NNAMENET1. |
| 23 | HD_SPI_MOSI1 | Direct net. |
| 24 | AR_LVDS_FRCLK_P | Via RA8 (pin 2-7 pair) -> NET2 -> AR_LVDS_FRCLK_P. Evidence: connector schematic source pin pairing + IPC netlist RA8, NNAMENET2. |
| 25 | HD_SPI_MISO1 | Direct net. |
| 26 | GND | Ground. |
| 27 | HD_AR_DP0 | Direct net. |
| 28 | AR_SYNC_IN | Via RA8 (pin 3-6 pair) -> AR_SYNC_IN. Evidence: connector schematic source pin pairing + IPC netlist RA8. |
| 29 | HD_AR_DP1 | Direct net. |
| 30 | AR_SYNC_OUT_SOP1 | Via RA8 (pin 4-5 pair) -> NET4 -> AR_SYNC_OUT_SOP1. Evidence: connector schematic source pin pairing + IPC netlist RA8, NNAMENET4. |
| 31 | HD_AR_DP2 | Direct net. |
| 32 | GND | Ground. |
| 33 | HD_AR_DP3 | Direct net. |
| 34 | AR_LVDS_1_N | Via RA7 (pin 1-8 pair) -> AR_LVDS_1_N. Evidence: connector schematic source pin pairing + IPC netlist RA7. |
| 35 | HD_AR_DP4 | Direct net. |
| 36 | AR_LVDS_1_P | Via RA7 (pin 2-7 pair) -> AR_LVDS_1_P. Evidence: connector schematic source pin pairing + IPC netlist RA7. |
| 37 | HD_AR_DP5 | Direct net. |
| 38 | GND | Ground. |
| 39 | HD_AR_DP6 | Direct net. |
| 40 | AR_LVDS_CLK_N | Via RA7 (pin 3-6 pair) -> AR_LVDS_CLK_N. Evidence: connector schematic source pin pairing + IPC netlist RA7. |
| 41 | HD_AR_DP7 | Direct net. |
| 42 | AR_LVDS_CLK_P | Via RA7 (pin 4-5 pair) -> AR_LVDS_CLK_P. Evidence: connector schematic source pin pairing + IPC netlist RA7. |
| 43 | HD_AR_BSS_LOGGER | NET8 maps to HD_AR_BSS_LOGGER. Evidence: IPC netlist NNAMENET8. |
| 44 | GND | Ground. |
| 45 | HD_AR_OSC_CLKOUT | NET11 maps to HD_AR_OSC_CLKOUT. Evidence: IPC netlist NNAMENET11. |
| 46 | AR_LVDS_0_N | Via RA6 (pin 1-8 pair) -> AR_LVDS_0_N. Evidence: connector schematic source pin pairing + IPC netlist RA6. |
| 47 | HD_AR_MCUCLKOUT | NET10 maps to HD_AR_MCUCLKOUT. Evidence: IPC netlist NNAMENET10. |
| 48 | AR_LVDS_0_P | Via RA6 (pin 2-7 pair) -> AR_LVDS_0_P. Evidence: connector schematic source pin pairing + IPC netlist RA6. |
| 49 | HD_AR_PMIC_CLKOUT_SOP2 | NET12 maps to HD_AR_PMIC_CLKOUT_SOP2. Evidence: IPC netlist NNAMENET12. |
| 50 | GND | Ground. |
| 51 | HD_AR_WARMRST | Direct net. |
| 52 | AR_NERR_OUT | Via RA6 (pin 3-6 pair) -> AR_NERR_OUT. Evidence: connector schematic source pin pairing + IPC netlist RA6. |
| 53 | HD_AR_SDA | Direct net. |
| 54 | AR_NERRIN | Via RA6 (pin 4-5 pair) -> AR_NERRIN. Evidence: connector schematic source pin pairing + IPC netlist RA6. |
| 55 | HD_AR_SCL | Direct net. |
| 56 | AR_GPIO_0 | Via RA5 (pin 1-8 pair) -> AR_GPIO_0. Evidence: connector schematic source pin pairing + IPC netlist RA5. |
| 57 | NC | No net name in IPC netlist for J2 pin 57. |
| 58 | AR_GPIO_1 | Via RA5 (pin 2-7 pair) -> AR_GPIO_1. Evidence: connector schematic source pin pairing + IPC netlist RA5. |
| 59 | NC | No net name in IPC netlist for J2 pin 59. |
| 60 | AR_GPIO_2 | Via RA5 (pin 3-6 pair) -> AR_GPIO_2. Evidence: connector schematic source pin pairing + IPC netlist RA5. |

## HD Connector J11 (Breakaway 60-pin)
- Part: Samtec QSH-030-01-L-D-A (BOM).
- Pin mapping extracted from IPC netlist; pins without net labels on sheet 7 are treated as NC and recorded as such in `data/connector_pinouts.json`.

| Pin | Net | Notes |
|---|---|
| 1 | NetFL4_1 | 5V_HD_IN through FL4. Evidence: IPC netlist. |
| 2 | NetFL4_1 | 5V_HD_IN through FL4. |
| 3 | NetFL4_1 | 5V_HD_IN through FL4. |
| 4 | NC | No net name in IPC netlist for J11 pin 4. |
| 5 | NC | No net name in IPC netlist for J11 pin 5. |
| 6 | NC | No net name in IPC netlist for J11 pin 6. |
| 7 | AR_CS1_60PIN | Via R150 (0 ohm). |
| 8 | NC | No net name in IPC netlist for J11 pin 8. |
| 9 | SPI_CLK1 | Via R151 (0 ohm). |
| 10 | AR_HOSTINTR1 | Via R152 (0 ohm). |
| 11 | SPI_MOSI1 | Via R153 (0 ohm). |
| 12 | SPI_MISO1 | Via R154 (0 ohm). |
| 13 | PGOOD | Via R155 (0 ohm). |
| 14 | NC | No net name in IPC netlist for J11 pin 14. |
| 15 | AR_DMM_CLK | Direct net. |
| 16 | AR_SYNC_IN | Via R157 (0 ohm). |
| 17 | AR_DMM_SYNC | Direct net. |
| 18 | GND | Ground. |
| 19 | AR_DP0 | Direct net. |
| 20 | NC | No net name in IPC netlist for J11 pin 20. |
| 21 | AR_DP1 | Direct net. |
| 22 | NC | No net name in IPC netlist for J11 pin 22. |
| 23 | AR_DP2 | Direct net. |
| 24 | GND | Ground. |
| 25 | AR_DP3 | Direct net. |
| 26 | AR_LVDS_FRCLK_P | Via R142 (0 ohm) from NET2. |
| 27 | AR_DP4 | Direct net. |
| 28 | AR_LVDS_FRCLK_N | Via R143 (0 ohm) from NET1. |
| 29 | AR_DP5 | Direct net. |
| 30 | GND | Ground. |
| 31 | AR_DP6 | Direct net. |
| 32 | NC | No net name in IPC netlist for J11 pin 32. |
| 33 | AR_DP7 | Direct net. |
| 34 | NC | No net name in IPC netlist for J11 pin 34. |
| 35 | NC | No net name in IPC netlist for J11 pin 35. |
| 36 | GND | Ground. |
| 37 | NC | No net name in IPC netlist for J11 pin 37. |
| 38 | NC | No net name in IPC netlist for J11 pin 38. |
| 39 | NC | No net name in IPC netlist for J11 pin 39. |
| 40 | NC | No net name in IPC netlist for J11 pin 40. |
| 41 | NC | No net name in IPC netlist for J11 pin 41. |
| 42 | GND | Ground. |
| 43 | NC | No net name in IPC netlist for J11 pin 43. |
| 44 | AR_LVDS_CLK_P | Via R144 (0 ohm). |
| 45 | NC | No net name in IPC netlist for J11 pin 45. |
| 46 | AR_LVDS_CLK_N | Via R145 (0 ohm). |
| 47 | NC | No net name in IPC netlist for J11 pin 47. |
| 48 | GND | Ground. |
| 49 | NC | No net name in IPC netlist for J11 pin 49. |
| 50 | AR_LVDS_1_P | Via R146 (0 ohm). |
| 51 | AR_SDA | Via R186 (0 ohm). |
| 52 | AR_LVDS_1_N | Via R147 (0 ohm). |
| 53 | AR_SCL | Via R187 (0 ohm). |
| 54 | GND | Ground. |
| 55 | CONN_AR_RS232RX | Via R188 (0 ohm) from NET6. |
| 56 | AR_LVDS_0_P | Via R148 (0 ohm). |
| 57 | CONN_AR_RS232TX | Via R189 (0 ohm) from NET7. |
| 58 | AR_LVDS_0_N | Via R149 (0 ohm). |
| 59 | AR_NRST_1 | Via R190 (0 ohm). |
| 60 | GND | Ground. |

## Breakaway Panelization (J11/J5 Boundary)
The breakaway section is connected to the main board through J11 (60-pin) and J5 (USB power). Nets on J11 that also connect to the main board will be electrically severed when the breakaway is depanelized.

Key cross-boundary nets and components (from IPC netlist):
- AR_DMM_CLK (U2 pin U3) and AR_DMM_SYNC (U2 pin U4) route to J11 pins 15/17.
- AR_DP0–AR_DP7 (U2 pins U7/U6/V5/U5/V3/M1/L2/L1) route to J11 pins 19/21/23/25/27/29/31/33, with series resistors R88/R130/R132/R133/R135/R137/R138/R140 on the J2 path and direct nets on J11.
- AR_LVDS_FRCLK_P/N, AR_LVDS_CLK_P/N, AR_LVDS_0_P/N, AR_LVDS_1_P/N route through R142–R149 to J11 pins 26/28/44/46/56/58/50/52.
- AR_SDA/AR_SCL route through R186/R187 to J11 pins 51/53.
- CONN_AR_RS232RX/CONN_AR_RS232TX route through R188/R189 to J11 pins 55/57.
- AR_NRST_1 routes through R190 to J11 pin 59; PGOOD routes through R155 to J11 pin 13.
- 5V_HD_IN is present on J11 pins 1-3 via FL4 (NetFL4_1).

Assumptions / To-Verify
- None.
