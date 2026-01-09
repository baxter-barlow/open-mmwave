# Validation Checklist - open_mmwave Rev G

This checklist provides measurable pass/fail criteria for hardware validation.
Sources: `data/power_validation_procedure.json`, `data/stackup_revG.json`, `data/signal_integrity_checklist.json`.

---

## 1. Visual Inspection

| Item | Criteria | Pass/Fail |
|------|----------|-----------|
| U1 (PMIC) orientation | Pin 1 dot aligned with silkscreen | [ ] |
| U2 (radar SoC) orientation | BGA alignment marks match footprint | [ ] |
| U3 (CP2105) orientation | Pin 1 aligned with silkscreen | [ ] |
| U19 (power mux) orientation | Pin 1 aligned with silkscreen | [ ] |
| D1, D2 Schottky polarity | Cathode band matches silkscreen | [ ] |
| L2-L5 (PMIC inductors) | 470 nH inductors populated | [ ] |
| L11-L14 (ferrite beads) | BLM18KG121TH1D populated | [ ] |
| Solder bridges | None visible on QFN/BGA | [ ] |
| Component presence | All BOM items populated | [ ] |

---

## 2. Power Rail Validation

Equipment required: DMM, bench supply with current limiting.

### 2.1 Pre-Power Checks

| Check | Method | Criteria | Pass/Fail |
|-------|--------|----------|-----------|
| 5V_IN to GND short | Ohmmeter | > 100 ohm | [ ] |
| 3.3V to GND short | Ohmmeter | > 50 ohm | [ ] |
| 1.8V to GND short | Ohmmeter | > 50 ohm | [ ] |
| 1.2V to GND short | Ohmmeter | > 50 ohm | [ ] |
| 1.0V to GND short | Ohmmeter | > 50 ohm | [ ] |

### 2.2 Stage 1: Input Power (Single Source Only)

Set bench supply: 5.0 V, 500 mA limit. Apply through ONE connector only.

| Source | Test Point | Expected | Tolerance | Measured | Pass/Fail |
|--------|------------|----------|-----------|----------|-----------|
| J1 (USB) | 5V_IN via D1 | 4.7 V | -0.3 V drop | _______ V | [ ] |
| J5 (USB breakaway) | TP4 (5V_IN_B) | 5.0 V | ±5% | _______ V | [ ] |
| J2 (HD connector) | 5V_HD_IN | 5.0 V | ±5% | _______ V | [ ] |

### 2.3 Stage 2: PMIC Output Rails

Apply 5V via J1. Current limit: 500 mA.

| Rail | Test Point | Nominal | Min | Max | Measured | Pass/Fail |
|------|------------|---------|-----|-----|----------|-----------|
| PMIC_3V3 | TP5 | 3.30 V | 3.20 V | 3.40 V | _______ V | [ ] |
| PMIC_1V8 | C47/C121 | 1.80 V | 1.75 V | 1.85 V | _______ V | [ ] |
| PMIC_1V2 | C45/C112 | 1.20 V | 1.16 V | 1.24 V | _______ V | [ ] |
| PMIC_1V0 | C46/C111 | 1.00 V | 0.97 V | 1.03 V | _______ V | [ ] |
| VCC_BA_3V3 | TP13 | 3.30 V | 3.20 V | 3.40 V | _______ V | [ ] |

### 2.4 Stage 3: SoC Rails (Post-Ferrite)

| Rail | After Component | Nominal | Min | Max | Measured | Pass/Fail |
|------|-----------------|---------|-----|-----|----------|-----------|
| AR_1V8 | L11 | 1.80 V | 1.75 V | 1.85 V | _______ V | [ ] |
| AR_1P2 | L13 | 1.20 V | 1.16 V | 1.24 V | _______ V | [ ] |
| AR_1P0_RF1 | L12 | 1.00 V | 0.97 V | 1.03 V | _______ V | [ ] |
| AR_1P0_RF2 | L14 | 1.00 V | 0.97 V | 1.03 V | _______ V | [ ] |

### 2.5 PMIC Status Signals

| Signal | Test Point | Expected State | Measured | Pass/Fail |
|--------|------------|----------------|----------|-----------|
| PMIC_PGOOD | U1 pin 16 / R25 | HIGH (>2.5 V) | _______ V | [ ] |
| PMIC_NRST | U1 pin 20 | HIGH (pulled up) | _______ V | [ ] |
| PMIC_EN1 | U1 pin 7 | HIGH (via R34) | _______ V | [ ] |
| PMIC_EN2 | U1 pin 15 | HIGH (via R35) | _______ V | [ ] |
| PMIC_EN3 | U1 pin 2 | HIGH (via R36) | _______ V | [ ] |

### 2.6 Current Consumption

| Stage | Current Limit | Expected | Measured | Pass/Fail |
|-------|---------------|----------|----------|-----------|
| Quiescent (no SoC activity) | 500 mA | < 200 mA | _______ mA | [ ] |
| SoC active (idle) | 1.0 A | TBD | _______ mA | [ ] |
| SoC active (radar TX) | 2.0 A | TBD | _______ mA | [ ] |

---

## 3. Reset and Clock Validation

| Signal | Test Point | Condition | Expected | Measured | Pass/Fail |
|--------|------------|-----------|----------|----------|-----------|
| AR_NRST | TP14 | After PMIC_PGOOD | HIGH (>2.5 V) | _______ V | [ ] |
| AR_OSC_CLKOUT | TP17 | SoC powered | 40 MHz clock | _______ | [ ] |
| PMIC_CLK | U1 pin 3 | U2 powered | Clock present | _______ | [ ] |

---

## 4. Communication Interface Validation

### 4.1 USB Enumeration (CP2105)

| Check | Method | Expected | Pass/Fail |
|-------|--------|----------|-----------|
| CP2105 enumeration | `lsusb` or Device Manager | VID:PID visible | [ ] |
| Dual UART ports | OS device list | Two COM/tty ports | [ ] |

### 4.2 UART Validation

| Signal | Test Point | Method | Expected | Pass/Fail |
|--------|------------|--------|----------|-----------|
| BREAK_RS232TX | TP18 | Scope | Idle HIGH | [ ] |
| BREAK_RS232RX | TP19 | Scope | Responds to input | [ ] |
| AR_MSS_LOGGER | TP26 | Scope | Boot messages at TBD baud | [ ] |

---

## 5. Mechanical Validation

### 5.1 PCB Dimensions

| Parameter | Specification | Tolerance | Measured | Pass/Fail |
|-----------|---------------|-----------|----------|-----------|
| Board thickness | 0.059 in (1.50 mm) | ±10% | _______ mm | [ ] |
| Layer count | 8 layers | exact | _______ | [ ] |

### 5.2 Layer Stackup (from ODB)

| Layer | Type | Nominal Dielectric | Copper Weight |
|-------|------|-------------------|---------------|
| TOP_LAYER | Signal | 0.0037 in | 1.3 oz |
| GND1 | Ground | 0.004 in | 1.9 oz |
| SIG1 | Signal | 0.0095 in | 0.9 oz |
| PWR1 | Power | 0.008 in | 1.9 oz |
| PWR2 | Power | 0.0095 in | 1.9 oz |
| SIG2 | Signal | 0.004 in | 0.9 oz |
| GND2 | Ground | 0.0037 in | 1.9 oz |
| BOTTOM_LAYER | Signal | 0.002 in | 1.3 oz |

---

## 6. Signal Integrity Spot Checks

### 6.1 Impedance-Controlled Nets

| Category | Target Impedance | Example Nets | Method |
|----------|-----------------|--------------|--------|
| USB | 90 ohm diff | USB_DP, USB_DM | TDR or calculated |
| LVDS | 100 ohm diff | AR_LVDS_0_P/N, AR_LVDS_CLK_P/N | TDR or calculated |
| SPI | 50 ohm single | SPI_CLK1, SPI_MOSI1, SPI_MISO1 | TDR or calculated |
| UART | 50 ohm single | AR_MSS_LOGGER | TDR or calculated |
| JTAG | 50 ohm single | AR_TCK, AR_TDI, AR_TMS, AR_TDO | TDR or calculated |

### 6.2 High-Speed Signal Quality (Scope)

| Signal | Rise Time | Overshoot | Ringing | Pass/Fail |
|--------|-----------|-----------|---------|-----------|
| USB_DP | < 4 ns | < 10% | < 3 cycles | [ ] |
| SPI_CLK1 | < 2 ns | < 15% | < 3 cycles | [ ] |
| AR_LVDS_CLK_P | < 1 ns | < 10% | < 2 cycles | [ ] |

---

## 7. RF Validation (If Applicable)

| Check | Equipment | Criteria | Pass/Fail |
|-------|-----------|----------|-----------|
| Antenna VSWR | VNA | < 2:1 at 60-64 GHz | [ ] |
| TX power | Spectrum analyzer | Within spec (TBD dBm) | [ ] |
| LO leakage | Spectrum analyzer | < -30 dBc | [ ] |
| Phase noise | Spectrum analyzer | Per datasheet | [ ] |

---

## 8. Validation Summary

| Section | Items Passed | Items Failed | Items TBD |
|---------|--------------|--------------|-----------|
| Visual Inspection | ___ / 9 | ___ | ___ |
| Power Rails | ___ / 17 | ___ | ___ |
| Reset/Clock | ___ / 3 | ___ | ___ |
| Communications | ___ / 5 | ___ | ___ |
| Mechanical | ___ / 2 | ___ | ___ |
| Signal Integrity | ___ / 3 | ___ | ___ |
| RF | ___ / 4 | ___ | ___ |

**Overall Status:** [ ] PASS / [ ] FAIL / [ ] INCOMPLETE

**Validated by:** _______________________
**Date:** _______________________
**Board Serial:** _______________________

---

## Notes and Observations

_Record any anomalies, workarounds, or observations here:_

```
[Space for handwritten or typed notes]
```
