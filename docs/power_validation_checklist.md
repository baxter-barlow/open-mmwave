# Power Validation Checklist - open_mmwave Rev G

Sources: `data/netlist_revG.json`, `data/pmic_mapping.json`.

## Expected Rails
| Rail | Nominal (V) | Tolerance | Test Points |
|---|---:|---:|---|
| 5V_IN | 5.00 | ±5% | TBD |
| PMIC_3V3 | 3.30 | ±3% | TP5 |
| PMIC_1V8 | 1.80 | ±3% | TBD |
| PMIC_1V2 | 1.20 | ±3% | TBD |
| PMIC_1V0 | 1.00 | ±3% | TBD |

## Procedure
### Input Power
- Set bench supply to 5.0 V and current limit to 0.5 A for initial checks.
- Apply power at a single input (J1, J5, or J2) and verify 5V_IN.

### PMIC Outputs
- Verify PMIC_3V3 at TP5.
- Verify PMIC_1V8/PMIC_1V2/PMIC_1V0 at output caps on PMIC sheet.
- Check PMIC_PGOOD goes high after rails settle.

### SoC Rails
- Verify AR_1V8, AR_1P2, AR_1P0_RF1, AR_1P0_RF2 after beads.
- Verify AR_NRST at TP14 after PMIC_PGOOD.
