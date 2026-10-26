#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_agents_to_opensource.py
-----------------------------
Reads the project root's AGENTS.md, sanitizes private paths, paper IDs, and specific user tokens,
and outputs a clean, production-ready AGENTS.template.md in Open Source/.
Also performs security and privacy leak verification using an optional .private_terms.txt list.

Usage:
    python scripts/sync_agents_to_opensource.py
    uv run scripts/sync_agents_to_opensource.py
"""

import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SKILL_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SKILL_DIR.parent.parent
AGENTS_SRC = PROJECT_ROOT / "AGENTS.md"
OUTPUT_TEMPLATE = SKILL_DIR / "AGENTS.template.md"
PRIVATE_TERMS_FILE = PROJECT_ROOT / ".private_terms.txt"

# Standard regex sanitization rules
SANITIZATION_RULES = [
    # Paths & Environment: replace drive letters and absolute paths
    (r"Repository:\s*\w+", r"Repository: <your_repository_name>"),
    (r"Working Directory:\s*`[A-Za-z]:\\[^`]+`", r"Working Directory: `<project_root>`"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+[\\/]scripts/", r"<project_root>/scripts/"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+[\\/]papers/", r"<project_root>/papers/"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+[\\/]presentations/", r"<project_root>/presentations/"),
    (r"[A-Za-z]:\\\\[^\\/\s\n\r]+\\\\.venv", r"<project_root>/.venv"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+\\.venv", r"<project_root>/.venv"),
    (r"[A-Za-z]:\\[A-Za-z0-9_.-]+", r"<project_root>"),
    
    # Internal paper codes & specific experiments
    (r"深刻吸取\s*[a-z]+\.\d+\s*惨痛教训", r"深刻吸取真实学术汇报严重返工教训"),
    (r"\b[a-z]{3,5}\.\d{4,}\b", r"<paper_id>"),
    (r"PAL vs PL", r"Sample-A vs Sample-B（实验组 vs 对照组）"),
    (r"Figure S10 的 50 圈 TGA 溶剂零挥发、Figure S7 的 -1\.45 eV 吸附能等", 
     r"Supporting Information 中补充机理测试（如溶剂挥发热重、DFT 理论吸附能计算等）"),
     
    # User specific theme colors / styles generalized
    (r"仅保留经典 `THANKS!`（Arial 粗体酒红色 `#9C1D22`）与汇报人及时间居中，\*\*严禁添加“敬请各位老师、师兄师姐批评指正！”\*\*",
     r"遵循用户既定风格（如大写英文致谢、特定主题色）与汇报人/时间居中排版，**严禁私自添加非预设的冗余客套话**（如“敬请批评指正”等）"),
]


def load_banned_patterns() -> list[tuple[str, str]]:
    """Loads patterns from an optional private configuration file if present."""
    patterns = [
        (r"[A-Za-z]:\\", "Windows Drive Path"),
    ]
    if PRIVATE_TERMS_FILE.exists():
        for line in PRIVATE_TERMS_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append((re.escape(line), f"Private Term: {line}"))
    return patterns


def sanitize_content(content: str) -> str:
    sanitized = content
    for pattern, replacement in SANITIZATION_RULES:
        sanitized = re.sub(pattern, replacement, sanitized)
    return sanitized


def verify_cleanliness(content: str) -> list[str]:
    violations = []
    for pattern, label in load_banned_patterns():
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            violations.append(f"Found banned token [{label}]: {len(matches)} match(es)")
    return violations


def main():
    if not AGENTS_SRC.exists():
        print(f"Error: {AGENTS_SRC} not found!")
        sys.exit(1)
        
    print(f"Reading source: {AGENTS_SRC}")
    raw_text = AGENTS_SRC.read_text(encoding="utf-8")
    
    sanitized_text = sanitize_content(raw_text)
    
    # Check for leaks
    violations = verify_cleanliness(sanitized_text)
    if violations:
        print("\n[CRITICAL ERROR] Sanitization failed! Sensitive tokens detected:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
        
    SKILL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_TEMPLATE.write_text(sanitized_text, encoding="utf-8")
    print(f"\n[SUCCESS] Successfully generated sanitized template:")
    print(f"  Destination: {OUTPUT_TEMPLATE}")
    print(f"  Total lines: {len(sanitized_text.splitlines())}")
    print("  Zero sensitive tokens detected.")


if __name__ == "__main__":
    main()
