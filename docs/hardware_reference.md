# Hardware Reference - open_mmwave Rev G

Sources: `docs/power_tree_revG.md`, `docs/interface_map_revG.md`, `data/netlist_revG.json`, `docs/boot_modes.md`.

## Power Tree Summary
| Rail | Source | Evidence |
|---|---|---|
| 5V_IN | USB J1 via D1 or U19 (TPS2115A) output via D2 | `docs/power_tree_revG.md` |
| PMIC_3V3 | U1 SW0 -> L2 | `docs/power_tree_revG.md` |
| PMIC_1V8 | U1 SW3 -> L5 | `docs/power_tree_revG.md` |
| PMIC_1V2 | U1 SW1 -> L3 | `docs/power_tree_revG.md` |
| PMIC_1V0 | U1 SW2 -> L4 | `docs/power_tree_revG.md` |

## Connector Quick Reference
### J1 (USB, Main)
| Pin | Net |
|---|---|
| 1 | USB_5V |
| 2 | USB_DM |
| 3 | USB_DP |
| 5 | GND |

### J5 (USB, Breakaway Power-Only)
| Pin | Net |
|---|---|
| 1 | USB_5V_B |
| 2 | NC |
| 3 | NC |
| 4 | NC |
| 5 | GND |

### J2 (HD Connector)
Key pins only. Full map: `docs/interface_map_revG.md`.

| Pin | Net |
|---|---|
| 2 | 5V_HD_IN |
| 8 | HD_AR_DMM_SYNC |
| 10 | HD_AR_DMM_CLK |
| 16 | HD_AR_HOSTINTR1 |
| 43 | HD_AR_BSS_LOGGER |
| 45 | HD_AR_OSC_CLKOUT |
| 47 | HD_AR_MCUCLKOUT |
| 49 | HD_AR_PMIC_CLKOUT_SOP2 |

### J11 (Breakaway)
Key pins only. Full map: `docs/interface_map_revG.md`.

| Pin | Net |
|---|---|
| 1-3 | 5V_HD_IN (via FL4) |
| 15 | AR_DMM_CLK |
| 17 | AR_DMM_SYNC |
| 19-33 | AR_DP0–AR_DP7 |
| 26/28 | AR_LVDS_FRCLK_P/N |
| 44/46 | AR_LVDS_CLK_P/N |
| 50/52 | AR_LVDS_1_P/N |
| 56/58 | AR_LVDS_0_P/N |
| 51/53 | AR_SDA / AR_SCL |
| 55/57 | CONN_AR_RS232RX/TX |
| 59 | AR_NRST_1 |

## Test Points (IPC Netlist)
| TP | Net |
|---|---|
| TP4 | 5V_IN_B |
| TP5 | PMIC_3V3 |
| TP13 | VCC_BA_3V3 |
| TP14 | AR_NRST |
| TP17 | AR_OSC_CLKOUT |
| TP18 | BREAK_RS232TX |
| TP19 | BREAK_RS232RX |
| TP26 | NetTP26_1 |

## Boot Modes
See `docs/boot_modes.md` for SOP strap network and switch positions.

## Key Components
| Refdes | Function | Evidence |
|---|---|---|
| U1 | LP87524 PMIC | `docs/power_tree_revG.md` |
| U2 | radar SoC | `docs/power_tree_revG.md` |
| U3 | CP2105 USB-UART | `docs/uart_setup.md` |
| U16 | SN74LVC1G11 reset gate | `docs/power_tree_revG.md` |
| U19 | TPS2115A power mux | `docs/power_tree_revG.md` |
