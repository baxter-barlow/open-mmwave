# Power Tree - open_mmwave Rev G

Sources: schematic source files, BOM, IPC netlist.

## Input Power Sources and ORing

- J1 USB_5V feeds 5V_IN through FL2 and Schottky D1.
 - Evidence: schematic sheet 6 (USB connector path), D1/FL2 on schematic source; D1/FL2 in BOM.
- J5 USB_5V_B feeds 5V_IN_B through FL14.
 - Evidence: schematic sheet 10; BOM FL14; IPC netlist net `USB_5V_B` and `5V_IN_B`.
- J2 5V_HD_IN (60-pin HD connector) feeds TPS2115A U19 IN1.
 - Evidence: schematic sheet 7; BOM U19 (TPS2115ADRBR).
- U19 TPS2115A selects between 5V_HD_IN (IN1) and 5V_IN_B (IN2); output 5V_IN_SW goes through FL11 and Schottky D2 to 5V_IN.
 - Evidence: schematic sheet 7; IPC netlist for nets `5V_HD_IN`, `5V_IN_B`, `5V_IN_SW`, `5V_IN`.

## Power Tree (Rev G)

| Rail / Net | Nominal | Source / Path | Key Components | Evidence |
|---|---|---|---|---|
| USB_5V | 5 V | J1 -> FL2 -> D1 -> 5V_IN | J1 (Molex 105017-0001), FL2 (BLM15PD300SZ1D), D1 (NSR20F30NXT5G) | schematic sheet 6; BOM |
| USB_5V_B | 5 V | J5 -> FL14 -> 5V_IN_B | J5 (Molex 105017-0001), FL14 (BLM15PD300SZ1D) | schematic sheet 10; BOM |
| 5V_HD_IN | 5 V | J2 -> FL4 -> U19 IN1 | J2 (Samtec QSH-030-01-L-D-A), FL4 (BLM15PD300SZ1D), U19 (TPS2115ADRBR) | schematic sheet 7; BOM |
| 5V_IN_B | 5 V | USB_5V_B path -> U19 IN2 | C42/C122 (10uF), TP4 on 5V_IN_B | schematic sheet 10; IPC netlist TP4 |
| 5V_IN_SW | 5 V | U19 OUT -> FL11 -> D2 -> 5V_IN | U19 TPS2115A, FL11 (BLM15PD300SZ1D), D2 (NSR20F30NXT5G) | schematic sheet 7; IPC netlist |
| 5V_IN | 5 V | ORed from D1 (USB_5V) and D2 (5V_IN_SW) | D1, D2 Schottkys | schematic sheet 6 and 7; IPC netlist |
| PMIC_3V3 | 3.3 V | U1 LP87524 buck (SW0) -> L2 | U1 LP87524JRNFRQ1; L2 (470 nH); C44/C45/C46/C47/C111/C112/C113/C121 (22uF) | schematic sheet 5; BOM |
| PMIC_1V2 | 1.2 V | U1 LP87524 buck (SW1) -> L3 | L3 (470 nH); output caps on schematic sheet 5 | schematic sheet 5; BOM |
| PMIC_1V0 | 1.0 V | U1 LP87524 buck (SW2) -> L4 | L4 (470 nH); output caps on schematic sheet 5 | schematic sheet 5; BOM |
| PMIC_1V8 | 1.8 V | U1 LP87524 buck (SW3) -> L5 | L5 (470 nH); output caps on schematic sheet 5 | schematic sheet 5; BOM |
| VCC_BA_3V3 | 3.3 V | PMIC_3V3 -> FL22 | FL22 (BLM15PD300SZ1D), TP13 | IPC netlist (FL22, TP13) |
| AR_1V8 | 1.8 V | PMIC_1V8 -> L11 | L11 (BLM18KG121TH1D) | schematic sheet 5 and 4; BOM |
| AR_1P2 | 1.2 V | PMIC_1V2 -> L13 | L13 (BLM18KG121TH1D) | schematic sheet 5 and 4; BOM |
| AR_1P0_RF1 | 1.0 V | PMIC_1V0 -> L12 | L12 (BLM18KG121TH1D) | schematic sheet 5 and 4; BOM |
| AR_1P0_RF2 | 1.0 V | PMIC_1V0 -> L14 | L14 (BLM18KG121TH1D) | schematic sheet 5 and 4; BOM |

## PMIC Pin-to-Rail Mapping (Connectivity-Verified)

Sources: schematic source (U1 pin names) and IPC netlist (U1 pin-to-net).

| U1 pin name | Pin | Net | Evidence |
|---|---|---|---|
| SW_B0 | 10 | SW0 | schematic pin record + IPC netlist U1 pin 10 |
| SW_B1 | 12 | SW1 | schematic pin record + IPC netlist U1 pin 12 |
| SW_B2 | 25 | SW2 | schematic pin record + IPC netlist U1 pin 25 |
| SW_B3 | 23 | SW3 | schematic pin record + IPC netlist U1 pin 23 |
| FB_B0 | 8 | PMIC_3V3 | schematic pin record + IPC netlist U1 pin 8 |
| FB_B1 | 14 | PMIC_1V2 | schematic pin record + IPC netlist U1 pin 14 |
| FB_B2 | 1 | PMIC_1V0 | schematic pin record + IPC netlist U1 pin 1 |
| FB_B3 | 21 | PMIC_1V8 | schematic pin record + IPC netlist U1 pin 21 |
| EN1 | 7 | PMIC_EN1 | schematic pin record + IPC netlist U1 pin 7 |
| EN2 | 15 | PMIC_EN2 | schematic pin record + IPC netlist U1 pin 15 |
| EN3 | 2 | PMIC_EN3 | schematic pin record + IPC netlist U1 pin 2 |
| \\RST | 20 | PMIC_NRST | schematic pin record + IPC netlist U1 pin 20 |
| \\INT | 19 | PMIC_NINT | schematic pin record + IPC netlist U1 pin 19 |
| PGOOD | 16 | PMIC_PGOOD | schematic pin record + IPC netlist U1 pin 16 |
| SCL | 5 | PMIC_SCL | schematic pin record + IPC netlist U1 pin 5 |
| SDA | 6 | PMIC_SDA | schematic pin record + IPC netlist U1 pin 6 |
| CLKIN | 3 | PMIC_CLK | schematic pin record + IPC netlist U1 pin 3 |

## Inductor-to-Rail Mapping (Connectivity-Verified)

| Switch net | Inductor | Output rail | Evidence |
|---|---|---|---|
| SW0 | L2 | PMIC_3V3 | IPC netlist L2 pins (SW0 / PMIC_3V3) |
| SW1 | L3 | PMIC_1V2 | IPC netlist L3 pins (SW1 / PMIC_1V2) |
| SW2 | L4 | PMIC_1V0 | IPC netlist L4 pins (SW2 / PMIC_1V0) |
| SW3 | L5 | PMIC_1V8 | IPC netlist L5 pins (SW3 / PMIC_1V8) |

## PMIC Output Capacitors (Connectivity-Verified)

| Rail | Capacitors on net | Evidence |
|---|---|---|
| PMIC_3V3 | C44, C2, C3, C100, C101, C102, C126, C87, C88 | IPC netlist PMIC_3V3 net |
| PMIC_1V2 | C45, C112 | IPC netlist PMIC_1V2 net |
| PMIC_1V0 | C46, C111, C113 | IPC netlist PMIC_1V0 net |
| PMIC_1V8 | C47, C121 | IPC netlist PMIC_1V8 net |

## PMIC Enable/Reset Control Logic (Connectivity-Verified)

No active control logic is connected to PMIC_EN1/EN2/EN3/PMIC_NRST/PMIC_PGOOD beyond passive pullups to PMICVIO_3V3. The IPC netlist shows each net only connects to U1 and its pullup resistor. The reset/GPIO sheet (schematic sheet 8) does not label any PMIC_EN* or PMIC_NRST routing beyond AR reset logic, so no additional drivers are present in that sheet.

| Net | Connected components | Evidence |
|---|---|---|
| PMIC_EN1 | U1 pin 7, R34 | `data/netlist_revG.json` derived from IPC netlist |
| PMIC_EN2 | U1 pin 15, R35 | `data/netlist_revG.json` derived from IPC netlist |
| PMIC_EN3 | U1 pin 2, R36 | `data/netlist_revG.json` derived from IPC netlist |
| PMIC_NRST | U1 pin 20, R33 | `data/netlist_revG.json` derived from IPC netlist |
| PMIC_PGOOD | U1 pin 16, R25 | `data/netlist_revG.json` derived from IPC netlist |
## Source-Selection Truth Table (Electrical Behavior)

This board uses two diode-OR inputs into 5V_IN (D1 from USB_5V and D2 from 5V_IN_SW). U19 selects between 5V_HD_IN and 5V_IN_B to create 5V_IN_SW. The effective source is the one with the highest voltage after its diode drop.

| USB J1 present | USB J5 present | 5V_HD_IN present | Expected 5V_IN source | Notes |
|---|---|---|---|---|
| No | No | Yes | 5V_HD_IN via U19 -> D2 | Verify U19 priority and D2 polarity in schematic/PCB. |
| No | Yes | No | USB_5V_B via U19 -> D2 | Verify U19 input selection logic; ILIM set by R27 (510 ohm). |
| Yes | No | No | USB_5V via D1 | Straight USB path. |
| Yes | Yes | No | Higher of (USB_5V via D1) or (USB_5V_B via U19->D2) | Diode drops decide. |
| Yes | No | Yes | Higher of (USB_5V via D1) or (5V_HD_IN via U19->D2) | Diode drops decide. |
| No | Yes | Yes | Higher of (USB_5V_B via U19->D2) or (5V_HD_IN via U19->D2) | U19 chooses between inputs. |
| Yes | Yes | Yes | Higher of (USB_5V via D1) and U19 output | Avoid dual-source unless validated. |

Assumptions / To-Verify
- SW0-SW3 mapping to PMIC_3V3/1V2/1V0/1V8 is inferred from schematic sheet 5 layout; confirm in schematic source pin wiring.
- U19 input priority (IN1 vs IN2) and current-limit behavior: verify in TPS2115A datasheet and schematic wiring (schematic sheet 7).
- D1/D2 polarity confirmed by schematic symbols and PCB orientation; verify against Altium sources.
