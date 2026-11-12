# CLAUDE.md — Academic AI Pair Programming Protocol (v2.0.0)

This repository follows the **Academic Agent Guardrails v2.0.0** 2-tier modular protocol defined in `AGENTS.md` (Layer 0, capped `<= 22,000` bytes) and `.agents/skills/` (or `skills/`).

## Layer 0 Essentials for Claude Code

1. **Virtual Environment & File-First Execution**:
   - Run Python strictly via `.venv/Scripts/python.exe <script>` (Windows), `.venv-linux/bin/python <script>` (WSL), or `uv run <script>`. Never install packages globally.
   - Never run inline multiline logic (`python -c "..."`, `powershell -Command`). Always write standalone `.py` / `.sh` files with explicit `encoding='utf-8'`.
   - Use WSL (`<wsl_project_root>`) when available; reserve PowerShell exclusively for Windows PowerPoint COM automation (`scripts/export_slides.ps1`).

2. **Zero-Hallucination Literature & Data Integrity**:
   - Extract raw PDF/SI text via `pymupdf` (`fitz`) before analysis; visually inspect cropped panels before writing prose.
   - Respect `7Li NMR` downfield convention (`ppm` increase = deshielding), matrix-background relativity (XPS/FTIR), and never rename user sample IDs without explicit mapping.
   - Write LaTeX strings with Python raw strings `r"""..."""` to avoid `\x07` / `\t` escape corruption, and eliminate banned hype terms or unsubscripted chemical formulas.

3. **Mandatory Layer 1 Sub-Skill Routing & Exit-0 Verification Gates**:
   - **Group-Meeting PPTX** -> Read `skills/group-meeting-pptx/SKILL.md` & `references/*`; validate with `verify_group_pptx.py` + COM export `scripts/export_slides.ps1` PNG review. Preserve Slide 0 / Slide `-1` font exemptions, flat `#CFD8DC` cards, bannerless `图 X：...` headings, and Read-Only finalized decks.
   - **Scientific Plotting (SVG / 3D)** -> Read `skills/scientific-plotting-svg/SKILL.md` & `references/*`; build on `scripts/pub_style.py` (`3.0–4.0 pt` 4-sided spines, inward ticks, Dual-Y CE air gaps, `10–20 h` symmetric zoom insets) and pass `audit_svg_postprocess.py --fix` (zero `<tspan>`, Times New Roman).
   - **Bilingual Paper Reader & Audit** -> Read `skills/paper-bilingual-reader/SKILL.md` & `references/*`; pass `audit_markdown_suite.py --check-images --check-math --check-json` cleanly with full closed-loop fixes across all linked artifacts.

Refer to `AGENTS.md` for all Rules 1–7 and exact routing paths.
