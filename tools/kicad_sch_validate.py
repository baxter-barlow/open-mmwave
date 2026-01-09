#!/usr/bin/env python3
"""Validate KiCad schematic hierarchy structure.

This script checks that the root schematic file has valid sheet definitions
and that all referenced sheet files exist. It catches common generator bugs
that cause blank schematics in KiCad.

Usage:
    python tools/kicad_sch_validate.py kicad/open_mmwave.kicad_sch

Exit codes:
    0 - All checks passed
    1 - Validation errors found
    2 - File not found or parse error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


class ValidationError:
    def __init__(self, severity: str, message: str, line: int = 0):
        self.severity = severity  # "error" or "warning"
        self.message = message
        self.line = line

    def __str__(self) -> str:
        loc = f" (line {self.line})" if self.line else ""
        return f"[{self.severity.upper()}]{loc} {self.message}"


def parse_sheets(content: str) -> List[Tuple[int, str, str, bool]]:
    """Extract sheet definitions from schematic content.

    Returns list of (line_number, sheet_name, sheet_file, has_uuid).
    """
    sheets = []
    lines = content.split("\n")

    # Patterns for sheet element parsing
    uuid_pattern = re.compile(r'\(uuid\s+"?[0-9a-fA-F-]+"?\)')
    sheetname_pattern = re.compile(r'\(property\s+"(Sheet\s*name|Sheetname)"\s+"([^"]+)"')
    sheetfile_pattern = re.compile(r'\(property\s+"(Sheet\s*file|Sheetfile)"\s+"([^"]+)"')

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Check if this line starts a sheet element (handles both single-line and multi-line)
        if stripped == "(sheet" or stripped.startswith("(sheet "):
            # Collect the full sheet element (may span multiple lines)
            sheet_content = line
            paren_depth = line.count("(") - line.count(")")

            # If sheet is not complete on this line, read more
            j = i
            while paren_depth > 0 and j < len(lines):
                j += 1
                if j <= len(lines):
                    next_line = lines[j - 1]
                    sheet_content += " " + next_line
                    paren_depth += next_line.count("(") - next_line.count(")")

            # Parse the complete sheet element
            has_uuid = bool(uuid_pattern.search(sheet_content))
            name_match = sheetname_pattern.search(sheet_content)
            file_match = sheetfile_pattern.search(sheet_content)

            sheet_name = name_match.group(2) if name_match else ""
            sheet_file = file_match.group(2) if file_match else ""

            sheets.append((i, sheet_name, sheet_file, has_uuid))

    return sheets


def validate_schematic(sch_path: Path) -> List[ValidationError]:
    """Validate a KiCad schematic file structure."""
    errors: List[ValidationError] = []

    if not sch_path.exists():
        errors.append(ValidationError("error", f"File not found: {sch_path}"))
        return errors

    content = sch_path.read_text()
    lines = content.split("\n")
    sch_dir = sch_path.parent

    # Check 1: Version header present
    if not content.startswith("(kicad_sch"):
        errors.append(ValidationError("error", "Missing kicad_sch header"))

    # Check 2: Parse sheet elements
    sheets = parse_sheets(content)

    if not sheets:
        # Root schematic with no sheets might be intentional, but warn
        errors.append(ValidationError("warning",
            "No sheet elements found - schematic may appear empty"))

    # Check 3: Validate each sheet
    for line_num, sheet_name, sheet_file, has_uuid in sheets:
        # UUID check
        if not has_uuid:
            errors.append(ValidationError("error",
                f"Sheet '{sheet_name}' missing uuid attribute", line_num))

        # Sheet file exists check
        if sheet_file:
            sheet_path = sch_dir / sheet_file
            if not sheet_path.exists():
                errors.append(ValidationError("error",
                    f"Referenced sheet file not found: {sheet_file}", line_num))
        else:
            errors.append(ValidationError("error",
                f"Sheet at line {line_num} has no Sheetfile property"))

    # Check 4: Property name format (warn on legacy format)
    if re.search(r'\(property\s+"Sheet name"', content):
        errors.append(ValidationError("warning",
            'Legacy property format: "Sheet name" should be "Sheetname"'))
    if re.search(r'\(property\s+"Sheet file"', content):
        errors.append(ValidationError("warning",
            'Legacy property format: "Sheet file" should be "Sheetfile"'))

    # Check 5: sheet_instances section (required for hierarchy)
    if sheets and "(sheet_instances" not in content:
        errors.append(ValidationError("error",
            "Missing (sheet_instances ...) section - hierarchy will not load"))

    # Check 6: At least one uuid anywhere (basic format check)
    if "(uuid" not in content and sheets:
        errors.append(ValidationError("error",
            "No uuid elements found - file may be malformed"))

    return errors


def validate_hierarchy(root_sch: Path) -> List[ValidationError]:
    """Validate entire schematic hierarchy starting from root."""
    all_errors: List[ValidationError] = []
    visited = set()
    to_visit = [root_sch]

    while to_visit:
        sch_path = to_visit.pop(0)
        if sch_path in visited:
            continue
        visited.add(sch_path)

        errors = validate_schematic(sch_path)
        for err in errors:
            err.message = f"[{sch_path.name}] {err.message}"
            all_errors.append(err)

        # Parse child sheets and add to visit list
        if sch_path.exists():
            content = sch_path.read_text()
            sheets = parse_sheets(content)
            for _, _, sheet_file, _ in sheets:
                if sheet_file:
                    child_path = sch_path.parent / sheet_file
                    if child_path not in visited:
                        to_visit.append(child_path)

    return all_errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KiCad schematic hierarchy structure"
    )
    parser.add_argument("schematic", type=Path, help="Root schematic file (.kicad_sch)")
    parser.add_argument("--hierarchy", "-r", action="store_true",
                        help="Recursively validate all sheets")
    parser.add_argument("--min-sheets", type=int, default=0,
                        help="Minimum expected sheet count (0 to skip)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Only output errors")
    args = parser.parse_args()

    if not args.schematic.exists():
        print(f"Error: File not found: {args.schematic}", file=sys.stderr)
        return 2

    if args.hierarchy:
        errors = validate_hierarchy(args.schematic)
    else:
        errors = validate_schematic(args.schematic)

    # Check minimum sheets if specified
    if args.min_sheets > 0:
        content = args.schematic.read_text()
        sheets = parse_sheets(content)
        if len(sheets) < args.min_sheets:
            errors.append(ValidationError("error",
                f"Expected at least {args.min_sheets} sheets, found {len(sheets)}"))

    # Output results
    error_count = sum(1 for e in errors if e.severity == "error")
    warning_count = sum(1 for e in errors if e.severity == "warning")

    for err in errors:
        if args.quiet and err.severity == "warning":
            continue
        print(err)

    if not args.quiet:
        print(f"\nValidation complete: {error_count} error(s), {warning_count} warning(s)")
        if error_count == 0 and warning_count == 0:
            print("All checks passed.")

    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
