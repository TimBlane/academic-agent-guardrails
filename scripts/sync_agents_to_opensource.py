#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sync_agents_to_opensource.py
-----------------------------
Open-source reference synchronization & sanitization pipeline (v2.0.0).

Reads a project root's AGENTS.md, .agents/skills/*, and scripts/pub_style.py,
sanitizes local drive paths, WSL mount paths, paper IDs, and custom tokens listed
in an optional .private_terms.txt file, enforces the <= 22,000 byte cap on
AGENTS.template.md, and outputs clean open-source assets.

Usage:
    python scripts/sync_agents_to_opensource.py
    uv run scripts/sync_agents_to_opensource.py
"""

import re
import shutil
import sys
from pathlib import Path

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILL_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SKILL_DIR.parent.parent
AGENTS_SRC = PROJECT_ROOT / "AGENTS.md"
WORKSPACE_SKILLS_DIR = PROJECT_ROOT / ".agents" / "skills"
PUB_STYLE_SRC = PROJECT_ROOT / "scripts" / "pub_style.py"

OUTPUT_TEMPLATE = SKILL_DIR / "AGENTS.template.md"
OPEN_SOURCE_SKILLS_DIR = SKILL_DIR / "skills"
OUTPUT_PUB_STYLE = SKILL_DIR / "scripts" / "pub_style.py"
PRIVATE_TERMS_FILE = PROJECT_ROOT / ".private_terms.txt"

SYNC_SKILLS = [
    "group-meeting-pptx",
    "scientific-plotting-svg",
    "paper-bilingual-reader",
]

AGENTS_MAX_BYTES = 22_000

SANITIZATION_RULES: list[tuple[str, str]] = [
    (r"Repository:\*\*\s*`[A-Za-z0-9_.-]+`", r"Repository:** `<your_repository_name>`"),
    (r"Repository:\s*[A-Za-z0-9_.-]+", r"Repository: <your_repository_name>"),
    (r"Working Directory:\*\*\s*`[A-Za-z]:\\[^`]+`", r"Working Directory:** `<project_root>`"),
    (r"Working Directory:\s*`[A-Za-z]:\\[^`]+`", r"Working Directory: `<project_root>`"),
    (r"/mnt/[a-z]/[A-Za-z0-9_.-]+/\.venv-linux/bin/python", r"<wsl_project_root>/.venv-linux/bin/python"),
    (r"/mnt/[a-z]/[A-Za-z0-9_.-]+", r"<wsl_project_root>"),
    (r"[A-Za-z]:\\\\[^\\/\s\n\r]+\\\\\.venv\\\\Scripts\\\\python\.exe", r".venv\\\\Scripts\\\\python.exe"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+\\\.venv\\Scripts\\python\.exe", r".venv\\Scripts\\python.exe"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+\\\.agents\\skills\\", r"skills/"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+\\scripts\\", r"scripts/"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+[\\/]scripts/", r"<project_root>/scripts/"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+[\\/]papers/", r"<project_root>/papers/"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+[\\/]presentations/?", r"<project_root>/presentations"),
    (r"[A-Za-z]:\\\\[^\\/\s\n\r]+\\\\\.venv", r"<project_root>/.venv"),
    (r"[A-Za-z]:\\[^\\/\s\n\r]+\\\.venv", r"<project_root>/.venv"),
    (r"[A-Za-z]:\\[A-Za-z0-9_.-]+", r"<project_root>"),
    (r"\b[a-z]{3,6}\.\d{4,}\b", r"<paper_id>"),
]


def load_banned_patterns() -> list[tuple[str, str]]:
    """Loads generic drive-path checks and optional .private_terms.txt entries."""
    patterns = [
        (r"[A-Za-z]:\\", "Windows Drive Path"),
        (r"file:" + r"/{3}", "Local file URI"),
    ]
    if PRIVATE_TERMS_FILE.exists():
        for line in PRIVATE_TERMS_FILE.read_text(encoding="utf-8").splitlines():
            term = line.strip()
            if term and not term.startswith("#"):
                patterns.append((re.escape(term), f"Private Term: {term}"))
    return patterns


def sanitize_content(content: str, rel_role: str = "root") -> str:
    text = content
    uri_prefix = "file:" + "///"
    if rel_role == "root":
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/\.agents/skills/", "skills/", text)
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/scripts/", "scripts/", text)
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/", "", text)
    elif rel_role == "skill":
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/\.agents/skills/", "../", text)
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/scripts/", "../../scripts/", text)
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/", "../../", text)
    elif rel_role == "reference":
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/\.agents/skills/", "../../", text)
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/scripts/", "../../../scripts/", text)
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/", "../../../", text)
    else:
        text = re.sub(uri_prefix + r"[A-Za-z]:/[^/]+/", "<project_root>/", text)

    for pattern, replacement in SANITIZATION_RULES:
        text = re.sub(pattern, replacement, text)

    if rel_role in {"skill", "reference"}:
        text = text.replace(".agents\\skills\\", "skills/")
        text = text.replace(".agents/skills/", "skills/")
    return text


def verify_cleanliness(content: str, label_prefix: str) -> list[str]:
    violations = []
    for pattern, label in load_banned_patterns():
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            violations.append(f"{label_prefix} -> [{label}]: {len(matches)} match(es)")
    return violations


def main() -> None:
    if not AGENTS_SRC.exists():
        print(f"Error: {AGENTS_SRC} not found! Run from a workspace containing AGENTS.md.")
        sys.exit(1)

    SKILL_DIR.mkdir(parents=True, exist_ok=True)
    all_violations: list[str] = []

    sanitized_agents = sanitize_content(AGENTS_SRC.read_text(encoding="utf-8"), rel_role="root")
    all_violations.extend(verify_cleanliness(sanitized_agents, "AGENTS.template.md"))
    byte_len = len(sanitized_agents.encode("utf-8"))
    if byte_len > AGENTS_MAX_BYTES:
        all_violations.append(
            f"AGENTS.template.md exceeds {AGENTS_MAX_BYTES} bytes cap: {byte_len} bytes"
        )
    OUTPUT_TEMPLATE.write_text(sanitized_agents, encoding="utf-8")
    print(f"[SYNC] AGENTS.template.md ({byte_len} bytes)")

    if WORKSPACE_SKILLS_DIR.exists():
        OPEN_SOURCE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        for skill_name in SYNC_SKILLS:
            src_skill = WORKSPACE_SKILLS_DIR / skill_name
            dst_skill = OPEN_SOURCE_SKILLS_DIR / skill_name
            if not src_skill.exists():
                continue
            if dst_skill.exists():
                shutil.rmtree(dst_skill)
            dst_skill.mkdir(parents=True, exist_ok=True)
            for src_file in sorted(src_skill.rglob("*")):
                if src_file.is_dir() or "__pycache__" in src_file.parts or src_file.suffix == ".pyc":
                    continue
                rel_path = src_file.relative_to(src_skill)
                dst_file = dst_skill / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                if src_file.suffix.lower() in {".md", ".py", ".txt", ".json", ".yaml", ".yml"}:
                    role = (
                        "skill"
                        if rel_path.name == "SKILL.md"
                        else ("reference" if "references" in rel_path.parts else "script")
                    )
                    cleaned = sanitize_content(src_file.read_text(encoding="utf-8"), rel_role=role)
                    all_violations.extend(
                        verify_cleanliness(cleaned, f"skills/{skill_name}/{rel_path.as_posix()}")
                    )
                    dst_file.write_text(cleaned, encoding="utf-8")
                else:
                    shutil.copy2(src_file, dst_file)
            print(f"[SYNC] skills/{skill_name}/")

    if PUB_STYLE_SRC.exists():
        cleaned_pub = sanitize_content(PUB_STYLE_SRC.read_text(encoding="utf-8"), rel_role="script")
        all_violations.extend(verify_cleanliness(cleaned_pub, "scripts/pub_style.py"))
        OUTPUT_PUB_STYLE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PUB_STYLE.write_text(cleaned_pub, encoding="utf-8")
        print("[SYNC] scripts/pub_style.py")

    if all_violations:
        print("\n[CRITICAL ERROR] Sanitization failed! Sensitive tokens detected:")
        for v in all_violations:
            print(f"  - {v}")
        sys.exit(1)

    print("\n[SUCCESS] Sanitized v2.0.0 assets written with zero sensitive tokens detected.")


if __name__ == "__main__":
    main()
