#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_academic_rigor.py
----------------------
Audits markdown documents, slide transcripts, and papers for compliance with
academic rigor standards defined in Academic Agent Guardrails:

1. Anti-hyperbole check: Flags marketing or sensationalist buzzwords.
2. Chemical formula check: Flags flat, non-subscripted chemical formulas.
3. Ion symbol check: Flags unformatted ion superscripts.
4. Scientific notation check: Flags raw powers (e.g. 10^-4 instead of $10^{-4}$).

Usage:
    python scan_academic_rigor.py path/to/document.md
    python scan_academic_rigor.py papers/my_paper/
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Banned marketing and sensationalist hyperbole
BANNED_HYPERBOLE = [
    "军工级",
    "神级表现",
    "神级",
    "革命性颠覆",
    "革命性突破",
    "降维打击",
    "天花板",
    "遥遥领先",
    "逆天",
    "碾压",
    "暴冲",
    "奇迹",
    "不可思议",
    "秒杀",
    "无敌",
]

# 2. Plain chemical formulas that lack LaTeX math or sub tags
PLAIN_CHEM_PATTERNS = [
    (r"(?<![\\$a-zA-Z0-9_{])CO2(?![\\$a-zA-Z0-9_}])", "Plain CO2 -> should be $\\mathrm{CO_2}$"),
    (r"(?<![\\$a-zA-Z0-9_{])H2CO3(?![\\$a-zA-Z0-9_}])", "Plain H2CO3 -> should be $\\mathrm{H_2CO_3}$"),
    (r"(?<![\\$a-zA-Z0-9_{])Li3N(?![\\$a-zA-Z0-9_}])", "Plain Li3N -> should be $\\mathrm{Li_3N}$"),
    (r"(?<![\\$a-zA-Z0-9_{])Li2CO3(?![\\$a-zA-Z0-9_}])", "Plain Li2CO3 -> should be $\\mathrm{Li_2CO_3}$"),
    (r"(?<![\\$a-zA-Z0-9_{])C2H2(?![\\$a-zA-Z0-9_}])", "Plain C2H2 -> should be $\\mathrm{C_2H_2}$"),
    (r"(?<![\\$a-zA-Z0-9_{])H2O(?![\\$a-zA-Z0-9_}])", "Plain H2O -> should be $\\mathrm{H_2O}$"),
    (r"(?<![\\$a-zA-Z0-9_{])O2(?![\\$a-zA-Z0-9_}])", "Plain O2 -> should be $\\mathrm{O_2}$"),
    (r"(?<![\\$a-zA-Z0-9_{])N2(?![\\$a-zA-Z0-9_}])", "Plain N2 -> should be $\\mathrm{N_2}$"),
]

# 3. Plain ions lacking superscript
PLAIN_ION_PATTERNS = [
    (r"(?<![\\$a-zA-Z0-9_{])Li\+(?![\\$a-zA-Z0-9_}])", "Plain Li+ -> should be $\\mathrm{Li^+}$"),
    (r"(?<![\\$a-zA-Z0-9_{])Na\+(?![\\$a-zA-Z0-9_}])", "Plain Na+ -> should be $\\mathrm{Na^+}$"),
    (r"(?<![\\$a-zA-Z0-9_{])K\+(?![\\$a-zA-Z0-9_}])", "Plain K+ -> should be $\\mathrm{K^+}$"),
    (r"(?<![\\$a-zA-Z0-9_{])Zn2\+(?![\\$a-zA-Z0-9_}])", "Plain Zn2+ -> should be $\\mathrm{Zn^{2+}}$"),
    (r"(?<![\\$a-zA-Z0-9_{])Mg2\+(?![\\$a-zA-Z0-9_}])", "Plain Mg2+ -> should be $\\mathrm{Mg^{2+}}$"),
]

# 4. Units & scientific notation
SCIENTIFIC_NOTATION_PATTERNS = [
    (r"\b10\^-(\d+)\b", "Plain 10^-N -> should be $10^{-N}$"),
    (r"\bcm\^-1\b", "Plain cm^-1 -> should be $\\mathrm{cm^{-1}}$"),
    (r"\bmAh/g\b", "Plain mAh/g -> should be $\\mathrm{mAh\\ g^{-1}}$ (or consistent with paper format)"),
]


def audit_file(file_path: Path) -> dict:
    results = {
        "hyperbole": [],
        "chem": [],
        "ions": [],
        "notation": [],
    }

    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[SKIP] Could not read {file_path}: {e}")
        return results

    lines = text.splitlines()

    # 1. Hyperbole scan
    for h in BANNED_HYPERBOLE:
        for idx, line in enumerate(lines, 1):
            if h in line:
                results["hyperbole"].append((idx, h, line.strip()))

    # 2. Chemical formulas
    for pattern, desc in PLAIN_CHEM_PATTERNS:
        for idx, line in enumerate(lines, 1):
            if re.search(pattern, line):
                results["chem"].append((idx, desc, line.strip()))

    # 3. Ions
    for pattern, desc in PLAIN_ION_PATTERNS:
        for idx, line in enumerate(lines, 1):
            if re.search(pattern, line):
                results["ions"].append((idx, desc, line.strip()))

    # 4. Scientific notation
    for pattern, desc in SCIENTIFIC_NOTATION_PATTERNS:
        for idx, line in enumerate(lines, 1):
            if re.search(pattern, line):
                results["notation"].append((idx, desc, line.strip()))

    return results


def main():
    parser = argparse.ArgumentParser(description="Audit academic documents for rigorous tone and formatting.")
    parser.add_argument("target", help="File or directory path to audit")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero code if any violation found")

    args = parser.parse_args()
    target_path = Path(args.target)

    if not target_path.exists():
        print(f"[ERROR] Target path does not exist: {target_path}")
        sys.exit(1)

    files_to_scan = []
    if target_path.is_file():
        files_to_scan.append(target_path)
    else:
        for ext in ["*.md", "*.txt", "*.html", "*.py"]:
            files_to_scan.extend(target_path.rglob(ext))

    total_issues = 0

    print(f"\n================ ACADEMIC RIGOR AUDIT REPORT ================")
    print(f"Target: {target_path} (Scanned {len(files_to_scan)} files)")

    for f in sorted(files_to_scan):
        res = audit_file(f)
        sub_total = len(res["hyperbole"]) + len(res["chem"]) + len(res["ions"]) + len(res["notation"])
        if sub_total > 0:
            total_issues += sub_total
            print(f"\n📄 {f.name} ({sub_total} issues):")
            for line_no, word, snippet in res["hyperbole"]:
                print(f"  [HYPERBOLE] Line {line_no}: Found '{word}' -> '{snippet[:80]}'")
            for line_no, desc, snippet in res["chem"]:
                print(f"  [CHEM FORMULA] Line {line_no}: {desc} -> '{snippet[:80]}'")
            for line_no, desc, snippet in res["ions"]:
                print(f"  [ION SYMBOL] Line {line_no}: {desc} -> '{snippet[:80]}'")
            for line_no, desc, snippet in res["notation"]:
                print(f"  [NOTATION] Line {line_no}: {desc} -> '{snippet[:80]}'")

    print(f"\n--------------------------------------------------------------")
    if total_issues == 0:
        print("✅ [CLEAN] All scanned files comply with Academic Agent Guardrails!")
    else:
        print(f"⚠️  [ATTENTION] Found {total_issues} compliance issue(s). Please review and correct.")

    if args.strict and total_issues > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
