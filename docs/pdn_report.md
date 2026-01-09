# PDN Report - open_mmwave Rev G

Sources: `data/pdn_analysis.json`, `data/netlist_revG.json`, BOM.

## Rail Capacitance Summary
See `data/pdn_analysis.json` for per-net capacitor lists and totals.

## Ferrite/Inductor Filtering
Ferrite and inductor components are listed per net in `data/pdn_analysis.json`.

## Notes
- Capacitor totals depend on BOM value parsing; missing values default to 0.
- DCR and transient response calculations require component electrical specs not in the repo.
