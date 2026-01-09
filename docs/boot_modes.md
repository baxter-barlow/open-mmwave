# Boot Modes - open_mmwave Rev G

Sources: `data/boot_modes.json`, schematic source files.

## SOP Strap Network (Hardware)
| SOP | Pull-down | Pull-up | Alt Source | Series to Switch |
|---|---|---|---|---|
| SOP0 | R158 | R174 -> R2 -> PMIC_3V3 | AR_TDO_SOP0 via R83 | R159 |
| SOP1 | R170 | R16 -> VCC_BA_3V3 | NET4 (AR_SYNC_OUT_SOP1) via R84 | R171 |
| SOP2 | R172 | R176 via SW3 to PMIC_3V3 | NET3 (AR_PMIC_CLKOUT_SOP2) via R85 | - |

## SOP Configuration Map
Switch positions are from `data/boot_modes.json` (OFF = pull-down active, ON = pull-up active).

| Mode | SOP0 | SOP1 | SOP2 |
|---|---|---|---|
| Functional (normal) | OFF | OFF | OFF |
| Flash programming | OFF | OFF | ON |
| mmWaveICBoost | OFF | ON | OFF |

## Quick Reference
- Functional mode: all SOP switches OFF (pull-downs dominate).
- Flash programming: SOP2 ON, SOP0/SOP1 OFF.
- mmWaveICBoost: SOP1 ON, SOP0/SOP2 OFF.
