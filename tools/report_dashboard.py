#!/usr/bin/env python3
"""Generate HTML dashboard from key metrics."""
from __future__ import annotations

from pathlib import Path


def main() -> int:
    sections = [
        "docs/hardware_reference.md",
        "docs/thermal_report.md",
        "docs/signal_integrity.md",
        "docs/production_test_spec.md",
    ]
    html = ["<html><body><h1>Hardware Dashboard</h1>"]
    for path in sections:
        p = Path(path)
        html.append(f"<h2>{p.name}</h2>")
        html.append("<pre>")
        html.append(p.read_text() if p.exists() else "Missing file")
        html.append("</pre>")
    html.append("</body></html>")
    Path("data/dashboard.html").write_text("\n".join(html))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
