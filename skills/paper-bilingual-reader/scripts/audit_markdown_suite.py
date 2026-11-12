#!/usr/bin/env python3
"""Deterministic quality, LaTeX-escape, banned-term, and link auditor for paper reader suites."""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_TARGET_FILES = [
    "paper.md",
    "paper_xray.md",
    "ground_truth_audit_report.md",
    "translation_notes.md",
]

CTRL_RE = re.compile(r"[\x00-\x09\x0b-\x1f\x7f]")
BROKEN_LATEX_RE = re.compile(r"(?<![\\A-Za-z])(?:pprox|lpha|ext\{|au_)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
IMG_REF_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
NEGATION_HEDGE_RE = re.compile(r"(?:尚未|未开展|未测试|未达到|未进行|缺乏|非|绝非|不属|并非).{0,10}工业级")

DEFAULT_BANNED_TERMS = [
    "军工级",
    "工业级",
    "神级",
    "颠覆性",
    "革命性",
    "万无一失",
    "无烟无火",
    "无声无息",
    "断崖式",
    "令人瞩目",
    "离火自熄",
    "离火即刻自熄",
    "离火即熄",
    "剧烈爆燃",
    "火球喷溅",
    "毫无冒烟",
    "零失重分解",
    "几乎完全透明",
    "极其强烈",
]


def strip_inline_code(line: str) -> str:
    """Remove backtick inline-code spans so regex/math examples do not self-flag."""
    return INLINE_CODE_RE.sub("", line)


def scan_markdown_file(
    path: Path,
    base_dir: Path,
    banned_re: re.Pattern,
    check_images: bool,
    check_math: bool,
) -> tuple[dict, bool]:
    """Scan a single Markdown file for escapes, banned terms, missing images, and $ balance."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    ctrl_hits = []
    broken_hits = []
    banned_hits = []
    missing_images = []
    dollar_mismatches = []
    has_failure = False

    in_fenced_code = False
    in_display_math = False

    for lineno, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_fenced_code = not in_fenced_code
            continue

        if CTRL_RE.search(raw_line):
            ctrl_hits.append((lineno, repr(raw_line[:100])))

        if not in_fenced_code:
            prose = strip_inline_code(raw_line)
            for m in BROKEN_LATEX_RE.finditer(prose):
                broken_hits.append((lineno, m.group(0), stripped[:100]))
            for m in banned_re.finditer(prose):
                banned_hits.append((lineno, m.group(0), stripped[:120]))

            if check_math:
                if stripped == "$$" or (stripped.startswith("$$") and not stripped.endswith("$$")):
                    in_display_math = not in_display_math
                elif stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 2:
                    pass
                elif not in_display_math:
                    clean_math = re.sub(r"\\\$", "", prose)
                    clean_math = clean_math.replace("$$", "")
                    if clean_math.count("$") % 2 != 0:
                        dollar_mismatches.append((lineno, stripped[:80]))

    if check_images:
        for ref in IMG_REF_RE.findall(text):
            rel = ref.strip().split()[0].strip("<>")
            if rel.startswith(("http://", "https://", "data:", "#")):
                continue
            if not ((path.parent / rel).exists() or (base_dir / rel).exists()):
                missing_images.append(rel)

    unexpected_banned = 0
    classified_hits = []
    for lineno, term, line in banned_hits:
        is_neg_audit = path.name == "ground_truth_audit_report.md" and "确证无任何" in line
        is_neg_hedge = term == "工业级" and bool(NEGATION_HEDGE_RE.search(line))
        if is_neg_audit:
            tag = "ALLOWED_NEGATIVE_AUDIT"
        elif is_neg_hedge:
            tag = "ALLOWED_NEGATIVE_HEDGE"
        else:
            tag = "UNEXPECTED"
            unexpected_banned += 1
        classified_hits.append((lineno, term, line, tag))

    if ctrl_hits or broken_hits or unexpected_banned or missing_images or dollar_mismatches:
        has_failure = True

    return (
        {
            "name": path.name,
            "lines": len(lines),
            "chars": len(text),
            "ctrl_hits": ctrl_hits,
            "broken_hits": broken_hits,
            "banned_hits": classified_hits,
            "missing_images": missing_images,
            "dollar_mismatches": dollar_mismatches,
        },
        has_failure,
    )


def validate_source_map_json(json_path: Path) -> list[str]:
    """Validate JSON syntax and required top-level keys in source_map.json."""
    if not json_path.exists():
        return [f"Missing {json_path.name}"]
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in {json_path.name}: {exc}"]
    required = ["paper_metadata", "blocks", "figures", "supplementary_figures", "equations"]
    missing = [k for k in required if k not in data]
    if missing:
        return [f"{json_path.name} missing required keys: {missing}"]
    print(
        f"=== {json_path.name} === blocks={len(data['blocks'])}, "
        f"figs={len(data['figures'])}, si_figs={len(data['supplementary_figures'])}, "
        f"eqs={len(data['equations'])}"
    )
    return []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit paper bilingual reader Markdown & JSON suite for escapes, banned terms, images, and math balance."
    )
    parser.add_argument("--dir", default=".", help="Target paper directory path.")
    parser.add_argument(
        "--files",
        default="",
        help="Comma-separated filenames inside --dir (defaults to standard 4 deliverables that exist).",
    )
    parser.add_argument(
        "--extra-banned",
        default="",
        help="Comma-separated additional banned terms to flag.",
    )
    parser.add_argument("--check-json", action="store_true", help="Validate source_map.json structure.")
    parser.add_argument("--check-images", action="store_true", help="Verify local Markdown image links exist on disk.")
    parser.add_argument("--check-math", action="store_true", help="Check inline $ math pairing outside code blocks.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if sys.prefix == sys.base_prefix:
        raise RuntimeError(
            "[ENV ERROR] Detected global Python environment! Run with .venv\\Scripts\\python.exe or .venv-linux."
        )
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    base_dir = Path(args.dir).resolve()
    if not base_dir.is_dir():
        print(f"ERROR: Directory not found: {base_dir}", file=sys.stderr)
        return 2

    names = (
        [n.strip() for n in args.files.split(",") if n.strip()]
        if args.files
        else [n for n in DEFAULT_TARGET_FILES if (base_dir / n).exists()]
    )
    if not names:
        print(f"ERROR: No target Markdown files found under {base_dir}", file=sys.stderr)
        return 2

    extra = [s.strip() for s in args.extra_banned.split(",") if s.strip()]
    banned_re = re.compile("|".join(re.escape(t) for t in DEFAULT_BANNED_TERMS + extra))

    any_failure = False
    for name in names:
        fpath = base_dir / name
        if not fpath.exists():
            print(f"ERROR: Missing file {fpath}", file=sys.stderr)
            any_failure = True
            continue
        res, failed = scan_markdown_file(
            fpath, base_dir, banned_re, args.check_images, args.check_math
        )
        if failed:
            any_failure = True
        print(f"=== {res['name']} ({res['lines']} lines, {res['chars']} chars) ===")
        print(
            f"  ctrl_chars={len(res['ctrl_hits'])} | broken_latex={len(res['broken_hits'])} "
            f"| banned_hits={len(res['banned_hits'])} | missing_imgs={len(res['missing_images'])} "
            f"| unmatched_$={len(res['dollar_mismatches'])}"
        )
        for item in res["ctrl_hits"]:
            print(f"    [CTRL] L{item[0]}: {item[1]}")
        for item in res["broken_hits"]:
            print(f"    [BROKEN_LATEX] L{item[0]} [{item[1]}]: {item[2]}")
        for lineno, term, line, tag in res["banned_hits"]:
            print(f"    [BANNED:{tag}] L{lineno} [{term}]: {line}")
        for img in res["missing_images"]:
            print(f"    [MISSING_IMAGE] {img}")
        for item in res["dollar_mismatches"]:
            print(f"    [MATH_$] L{item[0]}: {item[1]}")

    if args.check_json:
        json_errors = validate_source_map_json(base_dir / "source_map.json")
        for err in json_errors:
            any_failure = True
            print(f"  [JSON_ERROR] {err}")

    return 1 if any_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
