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

Refer to `AGENTS.md` for the complete 14 Ironclad Rules.
