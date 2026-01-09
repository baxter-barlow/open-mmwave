# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **hardware design repository** for open_mmwave, an open-source mmWave radar platform. This is NOT a software project - it contains PCB schematics, fabrication files, and hardware documentation.

**Primary IC:** radar SoC (mmWave front-end)
**Design Tool:** Altium Designer
**PCB:** 8-layer board
**Active Revision:** Rev G (latest), with Rev F as stable reference

## Repository Structure

```
mmwave_hardware/
├── docs/ # Hardware documentation (markdown)
│ ├── bringup_revG.md # Power-up sequencing and validation checklist
│ ├── power_tree_revG.md # Power distribution and PMIC mapping
│ ├── interface_map_revG.md # Connector pinouts (J1, J2, J5, J11)
│ └── open_questions_revG.md # 10 unresolved design verification items
├── release/ # Release artifacts and reports
└── tools/ # Scripts and utilities
```

Local vendor reference material is gitignored and should never be committed.

## Key Hardware Components

| Component | Part Number | Function |
|-----------|-------------|----------|
| U1 | LP87524JRNFRQ1 | Quad-output PMIC (3.3V, 1.8V, 1.2V, 1.0V) |
| U2 | XI6843ARQGALP | radar SoC (BGA) |
| U3 | CP2105 | Dual USB-to-UART bridge |
| U19 | TPS2115ADRBR | Power mux for 5V input selection |
| D1, D2 | NSR20F30NXT5G | Schottky diodes for power ORing |
| L2-L5 | 470 nH | PMIC buck inductors |
| L11-L14 | BLM18KG121TH1D | RF rail ferrite beads |

## Power Architecture

Three input sources OR'd to 5V_IN:
- **J1 (USB):** USB_5V → FL2 → D1 → 5V_IN
- **J5 (Breakaway USB):** USB_5V_B → FL14 → U19 → D2 → 5V_IN
- **J2 (HD connector):** 5V_HD_IN → U19 → D2 → 5V_IN

PMIC outputs (U1 LP87524):
- SW0 → L2 → **PMIC_3V3** (→ VCC_BA_3V3 via FL22)
- SW1 → L3 → **PMIC_1V2** (→ AR_1P2 via L13)
- SW2 → L4 → **PMIC_1V0** (→ AR_1P0_RF1/RF2 via L12/L14)
- SW3 → L5 → **PMIC_1V8** (→ AR_1V8 via L11)

## Hardware Bring-up Test Points

| Test Point | Signal | Purpose |
|------------|--------|---------|
| TP4 | 5V_IN_B | Secondary USB input verification |
| TP5 | PMIC_3V3 | Main 3.3V rail |
| TP13 | VCC_BA_3V3 | Filtered 3.3V |
| TP14 | AR_NRST | AOP reset state |
| TP17 | AR_OSC_CLKOUT | Clock verification |
| TP18/TP19 | BREAK_RS232TX/RX | Breakaway UART |
| TP26 | AR_MSS_LOGGER | Main UART output |

## Working with This Repository

### Design Verification
Open questions requiring Altium schematic tracing are tracked in `docs/open_questions_revG.md`. Key items:
1. PMIC buck output mapping (SW0-SW3) - verify in schematic source files
2. PMIC feedback divider resistors (R33/R34/R35/R36/R50/R52)
3. Reset gating logic (U16 SN74LVC1G11) - trace in schematic source files
4. SOP boot mode strap configuration
5. J2/J11 connector nets (many NetJ2_x/NetJ11_x are unnamed)

### Key Source Files for Schematic Analysis
See the local schematic source files (gitignored) for power management, reset/enable logic, SoC I/O, and connector mappings.

### IPC Netlist Reference
The IPC netlist from the fabrication package provides net connectivity but many nets are unnamed (e.g., NetJ2_12, NET9). Cross-reference with schematic source files for actual signal names.

## Current State

**Complete:**
- PCB design (Rev G) with full fabrication package
- Power tree documentation
- Basic bring-up procedure
- Reference designs from local sources (gitignored)

**Pending (documented in open_questions_revG.md):**
- 10 design verification items requiring Altium schematic tracing
- Expected current draw measurements (TBD)
- Complete J2/J11 pinout resolution
- RF stackup/impedance review

## Repository

**URL:** https://github.com/baxter-barlow/open-mmwave
**All commits by:** baxter-barlow

## Content Rules

This is a PUBLIC repository. All committed content must be FREE of:
- Vendor name references
- Vendor-specific part numbers
- "copying" or "mirror" language
- References to development platforms or commercial development platforms

**Local reference only (GITIGNORED):**
- `local_vendor_docs/`, `local_vendor_docs/`, `local_vendor_docs/`, `local_vendor_docs.pdf`
- `CODEX_SESSION_PHASE*.md`

## Before Committing

```bash
# Check for forbidden content
git diff --cached | rg -i "copying|mirror|copying language|development platform"
# Must return empty!

# Verify author
git config user.name # must be: baxter-barlow
```
