# KiCad Schematic Loading Issue - Root Cause Analysis

## Symptom
`kicad/open_mmwave.kicad_sch` opens in KiCad with only a title block visible. Hierarchical sheets are not displayed.

## Root Cause
The `tools/kicad_schematic_gen.py` generator produces **structurally incomplete** KiCad S-expression files that are missing required elements for KiCad 6+ format.

### Evidence

1. **Missing UUIDs** (Critical)
   ```bash
   $ grep -c "uuid" kicad/open_mmwave.kicad_sch
   0
   ```
   KiCad 6+ requires `uuid` on every sheet, symbol, wire, and label element.

2. **Incorrect property key names** in sheet elements:
   - Generator outputs: `(property "Sheet name" "...")` and `(property "Sheet file" "...")`
   - KiCad expects: `(property "Sheetname" "...")` and `(property "Sheetfile" "...")`
   - Note: No space in property names.

3. **Missing `sheet_instances` section**:
   ```bash
   $ grep "sheet_instances" kicad/open_mmwave.kicad_sch
   (no output)
   ```
   The hierarchy paths are not defined, so KiCad cannot resolve sheet references.

4. **Incomplete property format**:
   - Generator outputs: `(property "Sheetname" "value")`
   - KiCad expects: `(property "Sheetname" "value" (at x y angle) (effects (font ...) (justify ...)))`

5. **Missing symbol UUIDs and instances** in child sheets.

### Current (Invalid) Format
```lisp
(sheet (at 20 20) (size 60 20)
  (property "Sheet name" "power_input")
  (property "Sheet file" "power_input.kicad_sch"))
```

### Required (Valid) Format
```lisp
(sheet (at 20 20) (size 60 20)
  (uuid "00000000-0000-0000-0000-000000000001")
  (property "Sheetname" "power_input"
    (at 50 25 0)
    (effects (font (size 1.27 1.27)) (justify left bottom)))
  (property "Sheetfile" "power_input.kicad_sch"
    (at 50 37.5 0)
    (effects (font (size 1.27 1.27)) (justify left top))))
```

Plus at end of file:
```lisp
(sheet_instances
  (path "/" (page "1"))
  (path "/00000000-0000-0000-0000-000000000001" (page "2"))
  ...)
```

## Affected Files

| File | Issue |
|------|-------|
| `tools/kicad_schematic_gen.py` | Lines 361-376: generates invalid sheet elements |
| `tools/kicad_schematic_gen.py` | Lines 215-219: symbols missing uuid |
| `kicad/open_mmwave.kicad_sch` | Root schematic with invalid sheets |
| `kicad/*.kicad_sch` | All child sheets missing uuid on symbols |

## Generator Code Issues

### `_write_sheet()` function (line 195-243)
- Outputs symbols without `uuid`
- Missing `lib_symbols` cache section
- Missing `symbol_instances` section

### Root schematic generation (lines 361-376)
```python
root_lines.append(
    f"  (sheet (at {x} {y}) (size 60 20)"
    f" (property \"Sheet name\" \"{Path(sheet_name).stem}\")"  # Wrong: "Sheet name"
    f" (property \"Sheet file\" \"{sheet_name}\"))"            # Wrong: "Sheet file"
)
```

Should generate:
- UUID for each sheet
- Correct property names (`Sheetname`, `Sheetfile`)
- Full property syntax with position and effects
- `sheet_instances` section at file end

## Confidence Level
**High** - Verified by:
1. Direct file inspection showing zero UUIDs
2. KiCad format documentation comparison
3. Property name mismatch confirmed in source code

## Fix Options

### Option 1: Update Generator (Recommended)
Modify `tools/kicad_schematic_gen.py` to output valid KiCad 7+ format:
- Add UUID generation (use Python `uuid.uuid4()`)
- Fix property names and format
- Add `sheet_instances` and `symbol_instances` sections

### Option 2: Post-Process with KiCad CLI
```bash
kicad-cli sch export netlist --format kicadxml kicad/open_mmwave.kicad_sch
```
Will fail, confirming the issue. No automatic fix available.

### Option 3: Manual KiCad Repair
Open in KiCad, manually add sheets, save. KiCad will write correct format.

## Self-Test

A CI script should verify:
1. Root schematic contains `uuid` elements
2. Sheet property names are `Sheetname` and `Sheetfile` (no spaces)
3. `sheet_instances` section exists
4. All referenced sheet files exist on disk

See `tools/kicad_sch_validate.py` for implementation.

## References

- [KiCad 8 File Formats](https://dev-docs.kicad.org/en/file-formats/)
- [KiCad Schematic S-Expression](https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/)
