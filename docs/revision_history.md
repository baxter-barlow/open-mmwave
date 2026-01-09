# Revision History - open_mmwave

Sources: IPC netlists `data/netlist_revF.json` and `data/netlist_revG.json`, delta `data/revF_to_revG_delta.json`.

## Rev F → Rev G (Netlist-Based Deltas)

Major additions (Rev G):
- J11 breakaway connector added with dedicated series resistors R142–R155/R157/R186–R190 and new nets NetJ11_* (IPC delta components and nets).
- FL4 added on NetFL4_1 (5V_HD_IN to J11 pins 1–3).
- L15 added between PMIC_1V0 and AR_1P0_RF2 (IPC netlist: L15 pins).
- New decoupling caps C111/C112/C113/C121/C131–C141 on PMIC rails and GND (IPC delta components).
- Net aliasing added for NET1–NET14 mapping to AR_LVDS/HD_AR_* signals (Rev G net_aliases; Rev F lacks these aliases).

Major removals (Rev G):
- Ferrites removed: FL1/FL6/FL7/FL8/FL9/FL10/FL20 (Rev F-only). These previously filtered AR_1V8 to VCLK_1V8/VIOIN_1V8/BB_1V8 and PMICOUT_3V3 to PMIC_3V3 (Rev F netlist).
- Nets removed: AR_VOUT_PA, BB_1V8, PMICOUT_3V3 (Rev F-only).
- Capacitors removed: C48/C49/C54/C77 (Rev F-only).
- R63 removed (Rev F-only).

Notes:
- The delta is purely netlist-based; schematic intent (renames vs functional changes) should be confirmed against Rev F/Rev G schematics.
