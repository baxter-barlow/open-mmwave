# KiCad Version Compatibility Audit

**Date:** 2026-01-09
**Target Version:** KiCad 9.0+

## Executive Summary

The KiCad files have mixed format versions. **Schematic and symbol files are KiCad 7.x format** (forward-compatible with 9.0), but **footprint files use legacy KiCad 5.x format** which may cause issues or require conversion.

## File Format Analysis

### Project File (.kicad_pro)
| File | Format | Version | Status |
|------|--------|---------|--------|
| `open_mmwave.kicad_pro` | JSON | meta.version: 3 | ✅ Modern (KiCad 7+) |

### Schematic Files (.kicad_sch)
| File | Format Version | Generator | Status |
|------|---------------|-----------|--------|
| `open_mmwave.kicad_sch` | 20231120 | codex | ✅ KiCad 7.x |
| `power_input.kicad_sch` | 20231120 | codex | ✅ KiCad 7.x |
| `pmic.kicad_sch` | 20231120 | codex | ✅ KiCad 7.x |
| `soc_core.kicad_sch` | 20231120 | codex | ✅ KiCad 7.x |
| All others | 20231120 | codex | ✅ KiCad 7.x |

### Symbol Library (.kicad_sym)
| File | Format Version | Generator | Status |
|------|---------------|-----------|--------|
| `open_mmwave.kicad_sym` | 20231120 | codex | ✅ KiCad 7.x |

### Footprint Files (.kicad_mod) — CRITICAL ISSUE
| File | Format | Status |
|------|--------|--------|
| `0402.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `0603.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `0805.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `0201.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `QFN-24_4x4mm.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `BGA-141_10.4x10.4mm.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `SOIC-8.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `SOT-23.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `XTAL_4P.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `CONN.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |
| `GENERIC.kicad_mod` | `(module ...)` | ❌ Legacy KiCad 5.x |

## Footprint Format Issue Details

### Current (Legacy) Format
```
(module 0402 (layer F.Cu) (tedit 0)
  (fp_text reference REF** (at 0 0) (layer F.SilkS))
  (fp_text value 0402 (at 0 -1) (layer F.Fab))
  (pad 1 smd rect (at -0.5 0) (size 0.6 0.3) (layers F.Cu F.Paste F.Mask))
  (pad 2 smd rect (at 0.5 0) (size 0.6 0.3) (layers F.Cu F.Paste F.Mask))
)
```

### Required (Modern) Format for KiCad 9.0
```
(footprint "0402"
  (version 20231120)
  (generator "open_mmwave")
  (layer "F.Cu")
  (descr "0402 (1005 Metric) SMD passive")
  (tags "0402 1005")
  (attr smd)
  (fp_text reference "REF**" (at 0 -1.5) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value "0402" (at 0 1.5) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "1" smd roundrect (at -0.5 0) (size 0.6 0.5) (layers "F.Cu" "F.Paste" "F.Mask")
    (roundrect_rratio 0.25)
  )
  (pad "2" smd roundrect (at 0.5 0) (size 0.6 0.5) (layers "F.Cu" "F.Paste" "F.Mask")
    (roundrect_rratio 0.25)
  )
  (model "${KICAD9_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0402_1005Metric.wrl"
    (offset (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )
)
```

### Key Format Changes (KiCad 5 → 9)

| Element | Legacy (v5) | Modern (v6+) |
|---------|-------------|--------------|
| Root token | `(module NAME ...)` | `(footprint "NAME" ...)` |
| Version | `(tedit timestamp)` | `(version YYYYMMDD)` |
| Generator | None | `(generator "name")` |
| Layer strings | Unquoted: `F.Cu` | Quoted: `"F.Cu"` |
| Pad names | Unquoted: `1` | Quoted: `"1"` |
| Text effects | Simple | Full font specs required |
| Attributes | None | `(attr smd)` or `(attr through_hole)` |

## KiCad 9.0 Specific Requirements

Per [KiCad 9.0 documentation](https://docs.kicad.org/9.0/en/kicad/kicad.html):

1. **Backward Compatible**: KiCad 9 can read older formats
2. **Forward Conversion Only**: Once saved in KiCad 9, files cannot be opened in older versions
3. **Legacy Conversion**: When opening legacy files, KiCad 9 will auto-convert on save
4. **File Extensions**:
   - `.kicad_mod` (footprints) - current
   - `.kicad_sym` (symbols) - current
   - `.kicad_sch` (schematics) - current
   - `.kicad_pro` (project) - current

## Recommendations

### Option 1: Manual Regeneration (Recommended)
Regenerate all footprints using the generator script (`tools/kicad_pcb_gen.py` or similar) with proper modern format output.

**Pros:**
- Clean, consistent output
- Proper version/generator metadata
- Full control over format

**Cons:**
- Requires script updates

### Option 2: KiCad Auto-Conversion
Open the project in KiCad 9.0 and save all footprints. KiCad will auto-convert.

**Pros:**
- Simple process
- Guaranteed compatibility

**Cons:**
- Requires KiCad 9 installed
- May add unexpected elements

### Option 3: sed/Script Conversion
Use text processing to update format in place.

**Pros:**
- Fast
- No GUI needed

**Cons:**
- Risk of format errors
- May miss edge cases

## Recommended Actions

1. **P0**: Update `tools/kicad_schematic_gen.py` and/or `tools/kicad_pcb_gen.py` to output modern format
2. **P1**: Regenerate all footprints in `open_mmwave.pretty/`
3. **P2**: Test by opening in KiCad 9.0
4. **P3**: Run DRC and ERC to verify

## Library Table Status

| File | Format | Status |
|------|--------|--------|
| `sym-lib-table` | S-expression | ✅ OK |
| `fp-lib-table` | S-expression | ✅ OK |

Both use `${KIPRJMOD}` relative paths which is correct.

## References

- [KiCad 9.0 Documentation](https://docs.kicad.org/9.0/en/kicad/kicad.html)
- [KiCad Footprint File Format (Dev Docs)](https://dev-docs.kicad.org/en/file-formats/sexpr-footprint/index.html)
- [KiCad Library Conventions](https://klc.kicad.org/)
- [KiCad Forum: footprint vs module](https://forum.kicad.info/t/footprint-footprint-vs-module/48338)
