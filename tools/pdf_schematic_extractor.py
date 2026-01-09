#!/usr/bin/env python3
"""Extract schematic text and net labels from PDF using pdftotext -bbox."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List


WORD_RE = re.compile(r"<word xMin=\"([0-9.]+)\" yMin=\"([0-9.]+)\" xMax=\"([0-9.]+)\" yMax=\"([0-9.]+)\">(.*?)</word>")
REF_RE = re.compile(r"^(R|C|L|U|J|TP|D|Q)\\d+$")
NET_RE = re.compile(r"^(AR_|PMIC_|USB_|HD_|VCC_|5V_|3V|1V|SOP|UART|SPI|I2C|CAN)")


def extract_words(pdf: Path) -> List[Dict]:
    out = subprocess.check_output(["pdftotext", "-bbox", str(pdf), "-"]).decode("utf-8", errors="ignore")
    words = []
    page = 0
    for line in out.splitlines():
        if line.startswith("<page"):
            page += 1
        m = WORD_RE.search(line)
        if m:
            words.append(
                {
                    "page": page,
                    "x_min": float(m.group(1)),
                    "y_min": float(m.group(2)),
                    "x_max": float(m.group(3)),
                    "y_max": float(m.group(4)),
                    "text": m.group(5),
                }
            )
    return words


def group_lines(words: List[Dict], y_tol: float = 2.0) -> Dict[int, List[List[Dict]]]:
    pages: Dict[int, List[List[Dict]]] = {}
    for w in words:
        pages.setdefault(w["page"], []).append(w)
    lines_by_page = {}
    for page, items in pages.items():
        items = sorted(items, key=lambda x: (x["y_min"], x["x_min"]))
        lines: List[List[Dict]] = []
        for w in items:
            placed = False
            for line in lines:
                if abs(line[0]["y_min"] - w["y_min"]) <= y_tol:
                    line.append(w)
                    placed = True
                    break
            if not placed:
                lines.append([w])
        for line in lines:
            line.sort(key=lambda x: x["x_min"])
        lines_by_page[page] = lines
    return lines_by_page


def extract_values(lines_by_page: Dict[int, List[List[Dict]]]) -> Dict[str, str]:
    mapping = {}
    for lines in lines_by_page.values():
        for line in lines:
            for idx, w in enumerate(line):
                if REF_RE.match(w["text"]):
                    if idx + 1 < len(line):
                        mapping[w["text"]] = line[idx + 1]["text"]
    return mapping


def extract_nets(words: List[Dict]) -> List[Dict]:
    nets = []
    for w in words:
        if NET_RE.match(w["text"]):
            nets.append({"text": w["text"], "page": w["page"], "x": w["x_min"], "y": w["y_min"]})
    return nets


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=Path, required=True, help="Schematic PDF")
    ap.add_argument("--out-text", type=Path, required=True, help="All text JSON")
    ap.add_argument("--out-values", type=Path, required=True, help="Component values JSON")
    ap.add_argument("--out-nets", type=Path, required=True, help="Net labels JSON")
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs only")
    args = ap.parse_args()

    if args.dry_run:
        return 0

    words = extract_words(args.pdf)
    lines = group_lines(words)
    values = extract_values(lines)
    nets = extract_nets(words)
    args.out_text.write_text(json.dumps(words, indent=2, sort_keys=True))
    args.out_values.write_text(json.dumps(values, indent=2, sort_keys=True))
    args.out_nets.write_text(json.dumps(nets, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
