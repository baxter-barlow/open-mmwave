# RF Design Notes - open_mmwave Rev G

## Antenna Integration
- AOP (Antenna-on-Package) eliminates external RF routing.
- Maintain keepout zones around antenna region and minimize metal nearby.
- Preserve continuous ground plane under the device as specified by .

## RF Signal Routing
- Controlled impedance guidance: see `data/impedance_targets.json`.
- Use via stitching and solid ground returns around RF region.

## Interference Mitigation
- Separate high-speed digital routes from RF-sensitive zones.
- Keep PMIC switching nodes away from RF region.

## Calibration Interface
- Use RF test points and calibration procedures (not in repo).
- Capture performance parameters per development platform guidance.
