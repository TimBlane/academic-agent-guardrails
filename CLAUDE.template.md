# CLAUDE.md — Academic AI Pair Programming Protocol

This repository adheres to the **Academic Agent Guardrails** protocol defined in `AGENTS.md`.

## Core Guidelines for Claude Code

1. **Check Virtual Environment**:
   Always execute Python commands using the project's local virtual environment:
   `.venv\Scripts\python.exe <script>` (Windows) or `uv run <script>`.
   Never install dependencies globally.

2. **File-First Execution (Windows)**:
   Do not inline multiline python snippets in terminal commands. Write standalone scripts to `scripts/` or local directories and run them.

3. **Academic PPTX Delivery**:
   - Deliveries are NOT complete until slides are exported to PNG using `scripts/export_slides.ps1` and visually reviewed.
   - Text boxes must use flat rectangles (`MSO_SHAPE.RECTANGLE`) and top-alignment.
   - English/numbers must use **Times New Roman**; Chinese text must use **微软雅黑**.
   - Chemical formulas must have subscripts ($\mathrm{CO_2}$, $\mathrm{Li}^+$).

4. **Zero-Hallucination Literature Analysis**:
   - Extract raw text from original PDFs before analyzing.
   - Deliver `ground_truth_audit_report.md` for any claim or card.
   - Strictly avoid marketing/hyperbolic phrasing ("军工级", "神级表现").

5. **Scientific Figure Standards**:
   - 4-sided box frames (`linewidth = 2.5 ~ 3.0 pt`), inward ticks (`tick.direction: in`), no top/right ticks.
   - Never rename user sample IDs without explicit mapping; zero hallucinated citations.
   - Vector SVG with zero `<tspan>` fragments and Times New Roman fonts.

Refer to `AGENTS.md` for the complete 20 Ironclad Rules.
