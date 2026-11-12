#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
env_guard_snippet.py
--------------------
Defensive runtime assertion snippet.
Add this snippet to the entry point of your project scripts to ensure
that AI agents or users execute within the designated virtual environment (.venv)
and never pollute the host system's global Python environment.
"""

import sys
from pathlib import Path


def assert_isolated_env():
    """Asserts that the current execution is within a virtual environment."""
    if sys.prefix == sys.base_prefix:
        project_root = Path(__file__).resolve().parent.parent
        venv_path = project_root / ".venv"
        error_msg = (
            f"\n[CRITICAL ENV ERROR] Global Python environment detected!\n"
            f"Execution must be performed inside the project virtual environment:\n"
            f"  Expected venv: {venv_path}\n"
            f"  Current prefix: {sys.prefix}\n"
            f"Please run using: uv run <script> or .venv\\Scripts\\python.exe <script>\n"
        )
        raise RuntimeError(error_msg)


if __name__ == "__main__":
    assert_isolated_env()
    print("✅ Environment check passed: executing within isolated virtual environment.")
