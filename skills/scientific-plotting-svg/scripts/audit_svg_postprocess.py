#!/usr/bin/env python3
"""Normalize fonts and audit editable text integrity (<tspan> count) in exported SVGs."""

import argparse
import re
import sys
from pathlib import Path

DISALLOWED_FONT_SUBSTRS = ("STIXGeneral", "DejaVu")


def normalize_svg_fonts(content: str) -> tuple[str, int]:
    """Replace residual Matplotlib fallback fonts with Times New Roman."""
    replacements = [
        (r"font-family:\s*['\"][^'\"]*STIXGeneral[^'\"]*['\"]", "font-family: 'Times New Roman'"),
        (r"font-family:\s*['\"][^'\"]*DejaVu[^'\"]*['\"]", "font-family: 'Times New Roman'"),
        (r"font-family:\s*'Times New Roman',\s*'DejaVu Serif',\s*serif", "font-family: 'Times New Roman'"),
        (r'font-family="[^"]*STIXGeneral[^"]*"', 'font-family="Times New Roman"'),
        (r'font-family="[^"]*DejaVu[^"]*"', 'font-family="Times New Roman"'),
    ]
    total_subs = 0
    updated = content
    for pat, repl in replacements:
        updated, count = re.subn(pat, repl, updated)
        total_subs += count
    return updated, total_subs


def collect_svg_files(targets: list[str], recursive: bool) -> list[Path]:
    """Expand file/directory arguments into sorted SVG paths."""
    svgs: list[Path] = []
    for raw in targets:
        p = Path(raw)
        if p.is_file() and p.suffix.lower() == ".svg":
            svgs.append(p)
        elif p.is_dir():
            glob_iter = p.rglob("*.svg") if recursive else p.glob("*.svg")
            svgs.extend(sorted(glob_iter))
    return sorted(set(svgs))


def inspect_svg(svg_path: Path, fix: bool, allow_tspan: bool) -> dict:
    """Optionally normalize fonts in one SVG file and return audit metrics."""
    content = svg_path.read_text(encoding="utf-8")
    subs_made = 0
    if fix:
        normalized, subs_made = normalize_svg_fonts(content)
        if normalized != content:
            svg_path.write_text(normalized, encoding="utf-8")
            content = normalized

    text_count = len(re.findall(r"<text\b.*?</text>", content, re.DOTALL))
    tspan_count = content.count("<tspan")

    fonts = set(re.findall(r"font-family:\s*([^;\"]+)", content))
    fonts.update(re.findall(r'font-family="([^"]+)"', content))
    bad_fonts = sorted(
        f for f in fonts if any(bad.lower() in f.lower() for bad in DISALLOWED_FONT_SUBSTRS)
    )

    issues: list[str] = []
    if not allow_tspan and tspan_count > 0:
        issues.append(f"fragmented <tspan> count={tspan_count} (expected 0)")
    if bad_fonts:
        issues.append(f"disallowed residual fonts={bad_fonts}")

    return {
        "path": svg_path,
        "text_count": text_count,
        "tspan_count": tspan_count,
        "fonts": sorted(fonts),
        "subs_made": subs_made,
        "issues": issues,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit SVG text fragmentation (<tspan>) and optionally normalize residual fonts to Times New Roman."
    )
    parser.add_argument("targets", nargs="+", help="One or more SVG files or directories.")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan subdirectories.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rewrite residual STIXGeneral/DejaVu declarations to Times New Roman in-place.",
    )
    parser.add_argument(
        "--allow-tspan",
        action="store_true",
        help="Report <tspan> count without failing exit code.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if sys.prefix == sys.base_prefix:
        raise RuntimeError(
            "[ENV ERROR] Detected global Python environment! Run with .venv\\Scripts\\python.exe or .venv-linux."
        )
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    svgs = collect_svg_files(args.targets, args.recursive)
    if not svgs:
        print("No SVG files found in specified target(s).", file=sys.stderr)
        return 2

    failures = 0
    for svg_path in svgs:
        res = inspect_svg(svg_path, fix=args.fix, allow_tspan=args.allow_tspan)
        status = "PASS" if not res["issues"] else "FAIL"
        if res["issues"]:
            failures += 1
        print(
            f"[{status}] {res['path'].name} | texts={res['text_count']} "
            f"| tspans={res['tspan_count']} | subs={res['subs_made']} | fonts={res['fonts']}"
        )
        for issue in res["issues"]:
            print(f"   - {issue}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
