# Production Test Specification - open_mmwave Rev G

Sources: `docs/power_validation_checklist.md`, `docs/signal_integrity.md`, IPC netlist.

## Bare Board Test
1. Continuity tests: critical nets (5V_IN, PMIC rails, GND).
2. Isolation: verify no short between 5V and GND.
3. Impedance verification: USB_DP/DM (90Ω diff), LVDS (100Ω diff).

## Assembled Board Test
1. Power-on sequence and PMIC_PGOOD.
2. Current consumption limits per stage (see bring-up checklist).
3. Verify test points: TP4/TP5/TP13/TP14/TP18/TP19/TP26.
4. UART programming/console validation.

## Final Test
1. RF calibration procedure outline (refer to calibration documentation).
2. Performance criteria: pass/fail thresholds defined by application.
3. Record test logs and serial numbers.
