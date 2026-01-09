# Test Fixture Specification - open_mmwave Rev G

Sources: `docs/hardware_reference.md`, `docs/power_validation_checklist.md`, `data/test_coverage.json`.

## Test Points
- TP4: 5V_IN_B
- TP5: PMIC_3V3
- TP13: VCC_BA_3V3
- TP14: AR_NRST
- TP18: BREAK_RS232TX
- TP19: BREAK_RS232RX
- TP26: AR_MSS_LOGGER (NetTP26_1)

## Pogo Pin Requirements
- 1.0 mm pitch recommended for test point access.
- Spring probes rated for 1 A on power rails.

## Mechanical
- Fixture should support board edges and avoid antenna keepout areas.
- Provide alignment pins to match mounting holes.

## Equipment
- Programmable bench supply (0–5 V, 2 A).
- USB analyzer or host PC for CP2105 enumeration.
- DMM/oscilloscope for rail and reset timing.
