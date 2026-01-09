# Modification Recipes - open_mmwave Rev G

## Change PMIC Output
Use `change_pmic_output(rail, new_voltage)` and update the feedback divider in the schematic.

## Add Test Point
Use `add_test_point(net_name, location_hint)` to log a new TP addition.

## Substitute Component
Use `substitute_component(ref_des, new_part)` and validate footprint/pinout.
