#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_dual_fonts.py
-------------------
Losslessly applies dual fonts to an existing PPTX presentation via OpenXML.
Preserves 100% of text positions, formatting, colors, and layout geometry.

Standard academic mapping:
- Latin alphabet & Arabic numbers: Times New Roman
- East Asian (Chinese characters): 微软雅黑 (Microsoft YaHei)

Usage:
    python apply_dual_fonts.py input.pptx [output.pptx]
    uv run scripts/apply_dual_fonts.py input.pptx --latin "Times New Roman" --ea "微软雅黑"
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import pptx
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls
except ImportError:
    print("[ERROR] python-pptx is required. Install via: uv pip install python-pptx")
    sys.exit(1)

# Ensure UTF-8 output on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def set_dual_font_on_run(run, latin_font="Times New Roman", ea_font="微软雅黑"):
    run.font.name = latin_font
    rPr = run._r.get_or_add_rPr()
    for child in list(rPr):
        if child.tag.endswith('ea') or child.tag.endswith('cs'):
            rPr.remove(child)
    ns = nsdecls("a")
    ea = parse_xml(f'<a:ea {ns} typeface="{ea_font}"/>')
    cs = parse_xml(f'<a:cs {ns} typeface="{latin_font}"/>')
    rPr.append(ea)
    rPr.append(cs)


def process_shape(shape, latin_font="Times New Roman", ea_font="微软雅黑"):
    count = 0
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                set_dual_font_on_run(r, latin_font, ea_font)
                count += 1
    if shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                for p in cell.text_frame.paragraphs:
                    for r in p.runs:
                        set_dual_font_on_run(r, latin_font, ea_font)
                        count += 1
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
        for child in shape.shapes:
            count += process_shape(child, latin_font, ea_font)
    return count


def apply_dual_fonts(pptx_path, out_path=None, latin_font="Times New Roman", ea_font="微软雅黑"):
    pptx_path = Path(pptx_path)
    if not pptx_path.exists():
        print(f"[ERROR] PPTX file not found: {pptx_path}")
        return False

    if out_path is None:
        out_path = pptx_path

    prs = pptx.Presentation(str(pptx_path))
    total_runs = 0
    for slide_idx, slide in enumerate(prs.slides, 1):
        slide_runs = 0
        for shape in slide.shapes:
            slide_runs += process_shape(shape, latin_font, ea_font)
        total_runs += slide_runs

    prs.save(str(out_path))
    print(f"[SUCCESS] Applied dual fonts to {len(prs.slides)} slides ({total_runs} text runs updated).")
    print(f"  Latin/Digits -> {latin_font}")
    print(f"  East Asian   -> {ea_font}")
    print(f"  Saved to     -> {out_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Losslessly inject Times New Roman + 微软雅黑 into PPTX slides.")
    parser.add_argument("input_pptx", help="Path to target PPTX presentation")
    parser.add_argument("-o", "--output", help="Output PPTX path (defaults to in-place overwrite)", default=None)
    parser.add_argument("--latin", default="Times New Roman", help="Font for Latin & numbers (default: Times New Roman)")
    parser.add_argument("--ea", default="微软雅黑", help="Font for East Asian characters (default: 微软雅黑)")

    args = parser.parse_args()
    apply_dual_fonts(args.input_pptx, args.output, args.latin, args.ea)


if __name__ == "__main__":
    main()
