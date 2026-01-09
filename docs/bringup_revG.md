# Bring-up Checklist - open_mmwave Rev G

Sources: component datasheet, BOM, IPC netlist.

## Visual and Continuity
- Verify U1 (LP87524JRNFRQ1), U19 (TPS2115ADRBR), U3 (CP2105) are populated and oriented.
- Verify inductors L2-L5 (470 nH) and ferrites L11-L15 (RF rails) are populated per BOM.
- Verify D1 and D2 Schottky diodes (NSR20F30NXT5G) orientation.
- Check for solder shorts on U2 BGA (XI6843ARQGALP) and around L2-L5.

## Power-Up (Current-Limited)

Set bench supply to 5.0 V with a conservative current limit (TBD). Apply power through a single source only (J1, J5, or J2) to avoid ORing ambiguity.

### Stage 1: Input Power
- J1: check USB_5V and 5V_IN via D1.
- J5: check USB_5V_B and 5V_IN_B at TP4.
- J2: check 5V_HD_IN at J2 pin 2.

### Stage 2: Power Mux and ORing
- With J2 or J5 input, check 5V_IN_SW at U19 output and 5V_IN after D2.
- With J1 input, check 5V_IN after D1.

### Stage 3: PMIC Outputs
- Measure PMIC_3V3 at TP5.
- Measure PMIC_1V8 / PMIC_1V2 / PMIC_1V0 at output caps (C131/C133/C135 etc on PMIC sheet 5).
- Check PMIC_PGOOD net state (logic high expected after stable rails).

### PMIC Enable/Reset Sequencing (Connectivity-Verified)
- PMIC_EN1 pulled up to PMICVIO_3V3 via R34 (4.99 k); only connected to U1 pin 7 and R34. Evidence: IPC netlist (`PMIC_EN1`, `R34`, `U1`).
- PMIC_EN2 pulled up to PMICVIO_3V3 via R35 (10 k); only connected to U1 pin 15 and R35. Evidence: IPC netlist.
- PMIC_EN3 pulled up to PMICVIO_3V3 via R36 (10 k); only connected to U1 pin 2 and R36. Evidence: IPC netlist.
- PMIC_NRST pulled up to PMICVIO_3V3 via R33 (4.99 k); only connected to U1 pin 20 and R33. Evidence: IPC netlist.
- PMIC_PGOOD is pulled up to PMICVIO_3V3 via R25 (4.99 k); only connected to U1 pin 16 and R25. Evidence: IPC netlist.
- PMIC_CLK is sourced from NET3 through R103 (0 ohm) into U1 pin 3; NET3 connects to U2 pin V10 (PMIC_CLKOUT). Evidence: IPC netlist; U2 pin V10 function from schematic source.

If PMIC_PGOOD never asserts:
- Verify PMICVIO_3V3 at R33/R34/R35/R36/R25 (pullup node). Check R50 (1.0 k) to 5V_IN and R52 (1.96 k) to GND (PMICVIO_3V3 divider). Evidence: IPC netlist (`R50`, `R52`, `PMICVIO_3V3`).
- Verify PMIC_CLK present at U1 pin 3 (PMIC_CLK) and that U2 is powered.

### AR_NRST Gating (Connectivity-Verified)
- U16 (SN74LVC1G11) is a 3-input AND gate: A pin1 = AR_NRST_1, B pin3 = NetR178_2, C pin6 = AR_NRST_2, Y pin4 = AR_NRST, VCC pin5 = VCC_BA_3V3, GND pin2 = GND. Evidence: schematic source pin names for U16 + IPC netlist U16 pin nets.
- NetR178_2 is pulled up to VCC_BA_3V3 via R178 (10k). Evidence: IPC netlist (`R178`).

### Stage 4: AOP Rails
- Measure AR_1V8 after L11, AR_1P2 after L13, AR_1P0_RF1 after L12, AR_1P0_RF2 after L14.

## PCB Stackup (ODB Extract)
- Board thickness: 0.059155 in from fabrication package.
- Layer order (top to bottom): TOP_LAYER, GND1, SIG1, PWR1, PWR2, SIG2, GND2, BOTTOM_LAYER (from fabrication package).
- Dielectric thickness per layer recorded in `data/stackup_revG.json` (from ODB layer attrlists).
- Keep-out layer present: KEEP-OUT_LAYER in ODB matrix; no explicit impedance notes found in ODB or layer plot PDF.

## Test Points (from IPC Netlist)
- TP4: 5V_IN_B
- TP5: PMIC_3V3
- TP13: VCC_BA_3V3
- TP14: AR_NRST
- TP17: AR_OSC_CLKOUT
- TP18: BREAK_RS232TX
- TP19: BREAK_RS232RX
- TP26: AR_MSS_LOGGER (UART)

## Minimal Comms Validation (UART)
- Connect USB at J1; verify CP2105 enumerates (device present in host).
- Confirm UART path selection (UART_MUX_CTRL1/2 and S1 switch) on sheet 10.
- Use UART at AR_MSS_LOGGER pins; expected baud TBD (verify component datasheet and firmware).

## Common Faults and Quick Checks
- No 3.3 V: check 5V_IN, D1/D2 orientation, U1 enable signals.
- Low RF rail: inspect L11-L14 beads and nearby caps.
- USB not enumerating: verify U3 CP2105 power (PMIC_3V3) and USB_DP/DM routing.

Assumptions / To-Verify
- Expected current draw for each stage is TBD; measure on a known-good board and update. [Confidence: low]
- UART default baud and log strings depend on firmware; verify with firmware documentation. [Confidence: low]
