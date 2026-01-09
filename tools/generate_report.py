#!/usr/bin/env python3
"""Generate a simple HTML report from existing docs."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
 ap = argparse.ArgumentParser()
 ap.add_argument("--out", type=Path, required=True, help="Output HTML path")
 ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
 args = ap.parse_args()

 if args.dry_run:
 return 0

 sections = [
 ("Hardware Reference", "docs/hardware_reference.md"),
 ("Bring-up Checklist", "docs/bringup_revG.md"),
 ("Power Validation", "docs/power_validation_checklist.md"),
 ("Signal Integrity", "docs/signal_integrity.md"),
 ]
 body = ["<html><body><h1>open_mmwave Rev G Report</h1>"]
 for title, path in sections:
 body.append(f"<h2>{title}</h2>")
 if Path(path).exists():
 content = Path(path).read_text()
 body.append("<pre>")
 body.append(content)
 body.append("</pre>")
 else:
 body.append("<p>Missing file.</p>")
 body.append("</body></html>")
 args.out.write_text("\n".join(body))
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
