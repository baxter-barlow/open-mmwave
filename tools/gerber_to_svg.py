#!/usr/bin/env python3
"""Render a simple SVG outline from Gerber GM1 file."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


COORD_RE = re.compile(r"X(-?\d+)Y(-?\d+)")
FORMAT_RE = re.compile(r"%FS[LA]X(\d)(\d)Y(\d)(\d)\*%")
UNIT_RE = re.compile(r"%MO(IN|MM)\*%")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outline", type=Path, required=True, help="Gerber outline file")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output SVG")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    unit = "MM"
    fmt = {"x_dec": 4, "y_dec": 4}
    points = []
    for line in args.outline.read_text(errors="ignore").splitlines():
        m_unit = UNIT_RE.search(line)
        if m_unit:
            unit = m_unit.group(1)
        m_fmt = FORMAT_RE.search(line)
        if m_fmt:
            fmt = {"x_dec": int(m_fmt.group(2)), "y_dec": int(m_fmt.group(4))}
        m = COORD_RE.search(line)
        if m:
            x = int(m.group(1)) / (10 ** fmt["x_dec"])
            y = int(m.group(2)) / (10 ** fmt["y_dec"])
            if unit == "IN":
                x *= 25.4
                y *= 25.4
            points.append((x, y))

    if not points:
        return 0

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    w = max_x - min_x
    h = max_y - min_y
    svg = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{w:.2f}mm' height='{h:.2f}mm' viewBox='{min_x} {min_y} {w} {h}'>",
        f"<rect x='{min_x}' y='{min_y}' width='{w}' height='{h}' fill='none' stroke='black' />",
        "</svg>",
    ]
    args.out.write_text("\\n".join(svg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
