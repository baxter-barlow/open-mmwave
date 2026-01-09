# Design Intent - open_mmwave Rev G

## Power Architecture Decisions
- LP87524 selected for 4-output buck capability matched to SoC rails.
- PMIC enables are passive pullups; sequencing driven by SoC power-up.
- Ferrite beads used to isolate RF rails from digital noise.

## Component Selection Rationale
- Schottky diodes (NSR20F30NXT5G) provide low Vf ORing for 5V inputs.
- Ferrite beads selected for impedance vs. frequency to suppress switching noise.
- Decoupling values chosen for low impedance across PMIC switching frequencies.

## Layout Considerations
- RF keepout around AOP antennas; maintain ground continuity under device.
- Stitching vias around high-speed and RF regions.

## Signal Integrity Choices
- LVDS and USB impedance targets documented in `data/impedance_targets.json`.
- Length matching required for LVDS pairs; USB routed as differential pair.
