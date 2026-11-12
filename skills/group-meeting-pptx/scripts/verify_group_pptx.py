#!/usr/bin/env python3
"""Deterministic verification gate for group-meeting PPTX presentations."""

import argparse
import io
import re
import sys
from pathlib import Path

from PIL import Image
import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Pt

DEFAULT_BANNED_TERMS = [
    "避雷针",
    "活塞式",
    "工业级",
    "军工级",
    "神级",
    "颠覆性",
    "革命性",
    "白炽",
    "暴力",
    "顶尖",
    "第一梯队",
    "彻底杜绝",
    "彻底终止",
    "断崖式",
    "令人瞩目",
    "万无一失",
    "无烟无火",
    "无声无息",
    "毫无冒烟",
    "离火即熄",
    "离火自熄",
    "离火即刻自熄",
    "剧烈爆燃",
    "火球喷溅",
    "零失重",
    "零恶化",
    "零积累",
    "不燃不爆",
    "几乎完全透明",
    "极其强烈",
    "批评指正",
]

UNSUBSCRIPTED_PATTERNS = [
    r"(?<![A-Za-z0-9_])cm-1(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9_])cm-2(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9_])g-1(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9_])s-1(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9_])min-1(?![A-Za-z0-9])",
    r"(?<![A-Za-z0-9_])ps-1(?![A-Za-z0-9])",
    r"10\^-?\d+",
    r"(?<![A-Za-z])CO2(?![A-Za-z0-9])",
    r"(?<![A-Za-z])Li3N(?![A-Za-z0-9])",
    r"(?<![A-Za-z])Li2O(?![A-Za-z0-9])",
    r"(?<![A-Za-z])Li2CO3(?![A-Za-z0-9])",
    r"(?<![A-Za-z])LiPF6(?![A-Za-z0-9])",
    r"(?<![A-Za-z])H2CO3(?![A-Za-z0-9])",
    r"(?<![A-Za-z])H2O(?![A-Za-z0-9])",
]

EXTRACTION_TAG_RE = re.compile(r"\(\s*(?:Figure|Fig\.?)\s*S?\d+[a-zA-Z0-9,\-\s]*\)")


def check_slide_pictures(slide, slide_num: int, max_aspect_diff: float) -> list[str]:
    """Ensure every embedded picture preserves its natural pixel aspect ratio."""
    failures: list[str] = []
    for s_idx, shape in enumerate(slide.shapes):
        if shape.shape_type != MSO_SHAPE_TYPE.PICTURE or shape.height == 0:
            continue
        with Image.open(io.BytesIO(shape.image.blob)) as im:
            nat_ratio = im.width / im.height
        disp_ratio = shape.width / shape.height
        diff = abs(nat_ratio - disp_ratio)
        if diff > max_aspect_diff:
            failures.append(
                f"Slide {slide_num} pic {s_idx}: aspect diff {diff:.4f} "
                f"(nat={nat_ratio:.3f}, disp={disp_ratio:.3f})"
            )
    return failures


def check_text_strings(
    txt: str,
    location: str,
    banned_terms: list[str],
    allow_brackets: bool,
    check_tags: bool,
    check_subscripts: bool = True,
) -> list[str]:
    """Scan a slide shape or notes string for banned tokens, formatting, and brackets."""
    failures: list[str] = []
    if not allow_brackets and ("【" in txt or "】" in txt):
        failures.append(f"{location} contains '【/】': {txt[:80]!r}")
    if check_tags:
        m_tag = EXTRACTION_TAG_RE.search(txt)
        if m_tag:
            failures.append(f"{location} contains internal extraction tag {m_tag.group(0)!r}")
    for term in banned_terms:
        if term in txt:
            failures.append(f"{location} contains banned term {term!r}: {txt[:80]!r}")
    if check_subscripts:
        for pat in UNSUBSCRIPTED_PATTERNS:
            m = re.search(pat, txt)
            if m:
                failures.append(f"{location} unsubscripted {m.group(0)!r}: {txt[:80]!r}")
    return failures


def check_ending_thanks(slide) -> list[str]:
    """Verify final slide THANKS! preserves Arial Bold 58 pt styling."""
    for shape in slide.shapes:
        if shape.has_text_frame and "THANKS!" in shape.text_frame.text:
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    if "THANKS!" in r.text:
                        ok = (
                            r.font.name == "Arial"
                            and bool(r.font.bold)
                            and r.font.size == Pt(58)
                        )
                        if ok:
                            return []
                        return [
                            "Last slide THANKS! font check failed "
                            f"(name={r.font.name!r}, bold={r.font.bold}, size={r.font.size})"
                        ]
    return ["Last slide missing 'THANKS!' run"]


def verify_pptx(
    pptx_path: Path,
    extra_banned: list[str],
    max_aspect_diff: float,
    check_tags: bool,
    check_notes_subscripts: bool = False,
) -> list[str]:
    """Run all automated quality gates on target presentation and return failures."""
    prs = pptx.Presentation(str(pptx_path))
    print(f"Inspecting PPTX: {pptx_path} ({len(prs.slides)} slides)")
    banned_terms = DEFAULT_BANNED_TERMS + [t for t in extra_banned if t]
    failures: list[str] = []

    for idx, slide in enumerate(prs.slides, start=1):
        failures.extend(check_slide_pictures(slide, idx, max_aspect_diff))
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            txt = shape.text_frame.text
            failures.extend(
                check_text_strings(
                    txt,
                    location=f"Slide {idx} shape",
                    banned_terms=banned_terms,
                    allow_brackets=(idx == 1),
                    check_tags=check_tags,
                    check_subscripts=True,
                )
            )
        if slide.has_notes_slide:
            nt = slide.notes_slide.notes_text_frame.text
            failures.extend(
                check_text_strings(
                    nt,
                    location=f"Slide {idx} notes",
                    banned_terms=banned_terms,
                    allow_brackets=True,
                    check_tags=check_tags,
                    check_subscripts=check_notes_subscripts,
                )
            )

    if len(prs.slides) > 0:
        failures.extend(check_ending_thanks(prs.slides[-1]))
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify group-meeting PPTX compliance with house style and anti-hallucination gates."
    )
    parser.add_argument("--pptx", required=True, help="Absolute or relative path to target .pptx file.")
    parser.add_argument(
        "--extra-banned",
        default="",
        help="Comma-separated paper-specific banned terms (e.g. '高场位移,雷达图,560 cm').",
    )
    parser.add_argument(
        "--max-aspect-diff",
        type=float,
        default=0.015,
        help="Maximum allowed |nat_ratio - disp_ratio| per embedded picture (default: 0.015).",
    )
    parser.add_argument(
        "--check-extraction-tags",
        action="store_true",
        help="Also flag internal extraction tags such as '(Figure 4a-c)' in text shapes.",
    )
    parser.add_argument(
        "--check-notes-subscripts",
        action="store_true",
        help="Also enforce Unicode subscript/superscript formatting inside Speaker Notes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if sys.prefix == sys.base_prefix:
        raise RuntimeError(
            "[ENV ERROR] Detected global Python environment! Run with .venv\\Scripts\\python.exe or .venv-linux."
        )
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    pptx_path = Path(args.pptx).resolve()
    if not pptx_path.exists():
        print(f"ERROR: File not found: {pptx_path}", file=sys.stderr)
        return 2

    extra = [s.strip() for s in args.extra_banned.split(",") if s.strip()]
    failures = verify_pptx(
        pptx_path=pptx_path,
        extra_banned=extra,
        max_aspect_diff=args.max_aspect_diff,
        check_tags=args.check_extraction_tags,
        check_notes_subscripts=args.check_notes_subscripts,
    )
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for item in failures:
            print(" -", item)
        return 1

    print("ALL CHECKS PASSED: 0 failures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
