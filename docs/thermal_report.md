# Thermal Report - open_mmwave Rev G

Sources: `data/thermal_analysis.json`, `data/thermal_inputs.json`.

## Summary
- LP87524 theta_ja sourced from datasheet (RθJA 34.6 °C/W, RNF VQFN 26 pins).
- radar SoC uses θJA 20.3 °C/W and 2.5 W typical power; 5.5 W worst-case noted.
- CP2105 uses θJA 34 °C/W and 56 mW typical power.
- TPS2115A uses θJA 45.2 °C/W and 25 mW typical power.

## Component Estimates
See `data/thermal_analysis.json` for per-component junction temperature estimates using typical power.
