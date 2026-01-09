# Troubleshooting - open_mmwave Rev G

Sources: `docs/bringup_revG.md`, `docs/power_validation_checklist.md`.

## No Power
- Check 5V input source and diode orientation (D1/D2).
- Verify U19 (TPS2115A) output 5V_IN_SW.
- Measure PMIC_3V3 at TP5.

## PMIC_PGOOD Low
- Verify PMIC_CLK at U1 pin 3.
- Check PMIC_EN1/2/3 and PMIC_NRST pullups.
- Inspect PMIC input 5V_IN and feedback resistors.

## No UART Output
- Verify CP2105 enumerates on host.
- Confirm UART mux control settings (UART_MUX_CTRL1/2).
- Check AR_NRST and PMIC_PGOOD.

## LVDS Issues
- Confirm LVDS nets on J2/J11 and series resistors present.
- Check impedance control and pairing on PCB.
