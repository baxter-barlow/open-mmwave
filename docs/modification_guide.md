# Modification Guide - open_mmwave Rev G

Sources: `tools/modification_framework.py`, `data/modification_templates.json`.

## Overview
Use the modification framework to document and plan design changes in a structured way.

## Common Modifications
### Power Rail Change
- Update PMIC feedback divider values and verify stability.
- Track resistor changes and update BOM.

### Component Substitution
- Confirm pinout and footprint compatibility.
- Validate electrical characteristics (voltage, current, thermal).

### Connector Pin Remap
- Update schematic symbol and connector pin tables.
- Confirm no net conflicts.

### Feature Removal
- Mark block components DNP.
- Verify no shared nets needed elsewhere.

### Feature Addition
- Add new schematic block and routing.
- Update BOM and test procedures.

## Data Templates
Templates are available in `data/modification_templates.json`.
