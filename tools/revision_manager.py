#!/usr/bin/env python3
"""Track revision metadata and file checksums."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict


def file_checksum(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", type=str, default="Rev G", help="Revision identifier")
    ap.add_argument("--files", nargs="+", required=True, help="Files to track")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output JSON path")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        for f in args.files:
            Path(f).exists()
        return 0

    manifest = {
        "revision": args.rev,
        "files": {},
    }
    for f in args.files:
        p = Path(f)
        if not p.exists():
            continue
        manifest["files"][f] = {
            "checksum_sha256": file_checksum(p),
            "mtime": p.stat().st_mtime,
        }
    args.out.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
