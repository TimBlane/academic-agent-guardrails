---
name: academic-agent-guardrails
description: Battle-tested academic research, presentation, and engineering guardrails for AI coding agents (Antigravity, Claude Code, Cursor, Copilot). Prevents hallucinations, token waste, slide clutter, and unverified data claims.
---

# Academic Agent Guardrails (学术科研与多智能体结对攻防守则)

This skill equips AI agents with battle-tested defensive protocols for rigorous scientific research, academic presentation generation, paper digestion, figure plotting, and multi-agent development.

It translates painful lessons learned from AI hallucinations, slide layout breakdowns, token waste, and toolchain pollution into **20 enforceable, ironclad engineering rules**.

---

## 🎯 When to Use This Skill

Activate or apply this skill whenever the user or task involves:
1. **Academic Presentation Generation (PPTX)**: Designing, updating, or reviewing academic slide decks, journal club slides, or defense presentations.
2. **Scientific Literature Reading & Analysis**: Digesting PDFs, extracting claims, comparing experimental groups, or writing reading notes.
3. **Scientific Plotting & Figure Standards**: Generating publication-quality vector figures (Matplotlib/Seaborn/SVG), 4-sided box frames, domain curves (FTIR/DSC/LSV), or 3D conceptual schematics.
4. **Writing Scientific Text**: Drafting papers, proposals, responses, or technical documentation where rigor and tone matter.
5. **Multi-Agent / Cross-IDE Collaboration**: Writing scripts or workflows to be shared across Antigravity, Claude Code, Cursor, or Copilot on Windows/Linux.

---

## 🛡️ The 6 Core Defense Pillars

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ACADEMIC AGENT GUARDRAILS PILLARS                    │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. Persistence     │ 2. Source Truth    │ 3. Presentation Defense      │
│ • File-First       │ • Hard PDF extract │ • Vision self-audit (PNG)    │
│ • Transparent dirs │ • 3-way validation │ • Dual fonts (Times + 雅黑)  │
│ • Zero sandbox loss│ • No sample rename │ • LaTeX/chem sub/superscripts│
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 4. Academic Rigor  │ 5. Scientific Plots│ 6. Toolchain Isolation       │
│ • Anti-hyperbole   │ • 4-sided box frame│ • Strict uv / .venv lockdown │
│ • Zero fake cites  │ • Zero <tspan> SVG │ • Windows quote defense      │
│ • Notes isolation  │ • Decoupled flows  │ • User asset read-only lock  │
└────────────────────┴────────────────────┴──────────────────────────────┘
```

---

## 📋 The 20 Ironclad Rules (Checklist)

Every AI agent operating in this repository MUST comply with the following 20 rules without exception:

### Pillar 1: Multi-Agent Transparency & Code Persistence
- **Rule 1 (Code Organization & Transparency)**: Never save business logic, plotting scripts, or build tools in ephemeral AI sandboxes or temporary scratchpads. All executable code MUST be saved persistently inside the project directory (e.g. `scripts/`, `papers/<paper_id>/`, `presentations/`) so other agents and humans can inspect, debug, and version-control them.

### Pillar 2: Presentation & Visual Quality Control
- **Rule 2 (Pre-Delivery Visual Self-Audit)**: NEVER declare "done" simply because code compiled. After generating or updating PPTX, run the export script (`export_slides.ps1`) to render every slide to high-res PNG, and use visual inspection tools to check for text overflows, overlapping cards, or occluded images with your own eyes before delivering.
- **Rule 3 (100% Figure-Text & Subpanel Consistency)**: Every parameter, number, axis unit, and time duration on the slide MUST strictly match the visual evidence in the figure on that slide. Subpanel letters (e.g. "左上图a", "图b") must refer ONLY to images actually displayed on the current slide—no ghost references.
- **Rule 4 (Removal of Extraction Tags)**: Slide titles must be pure scientific conclusions or propositions. NEVER include internal scraping tags like `(Figure 4a-c)` or `(Fig. S4)` in slide titles. Use audience-intuitive spatial directions ("左上图a", "底图右一") instead.
- **Rule 5 (SVG vs. 3D Model Division of Labor)**:
  - *Data curves (FTIR, XRD, XPS, cycling)*: Plot using Python (Matplotlib/Seaborn) with standard LaTeX syntax (`r'$\mathrm{cm^{-1}}$'`, `mathtext.fontset = 'dejavusans'`) and export crisp vector SVG and PNG.
  - *3D Mechanism & Conceptual Models*: Never use wireframe Matplotlib 3D hacks. Use dedicated diffusion/generative imaging tools (`generate_image`) with high-end cinematic prompts, and persist prompts alongside the paper.
- **Rule 6 (Defensive Slide Layouts)**: Use plain flat rectangular containers (`MSO_SHAPE.RECTANGLE`) with subtle borders (`#CFD8DC`) rather than unpredictable rounded shapes. Always set `tf.vertical_anchor = MSO_ANCHOR.TOP`. Preserve 20%–30% vertical breathing room.

### Pillar 3: Academic Tone & Typesetting Standards
- **Rule 7 (Zero Fluff & Anti-Hyperbole)**: Strictly prohibit marketing, sensationalist, or non-academic jargon (e.g., "军工级", "神级表现", "革命性颠覆"). Use objective, peer-reviewed scientific vocabulary. Every quantitative statement must have direct experimental data backing.
- **Rule 8 (Dual-Font Separation Principle)**:
  - English letters, numbers, variables ($E_a$, $t_{\mathrm{Li}^+}$, $\mathrm{mAh/g}$, $\mathrm{NCM811}$): **Times New Roman**.
  - Chinese characters: **微软雅黑** (Microsoft YaHei) or Source Han Sans.
  - Implement via explicit OpenXML dual-font declaration (`<a:latin typeface="Times New Roman"/>` and `<a:ea typeface="微软雅黑"/>`).
- **Rule 9 (Chemical Formulas & Scientific Indices)**:
  - Chemical stoichiometry must be subscripted ($\mathrm{CO_2}$, $\mathrm{Li_3N}$, $\mathrm{LiNi_{0.8}Co_{0.1}Mn_{0.1}O_2}$). Never write plain `CO2` or `Li3N`.
  - Ion charges must be superscripted ($\mathrm{Li}^+$, $\mathrm{TFSI}^-$).
  - Scientific notation powers ($10^{-4}$) and composite units ($\mathrm{cm}^{-1}$) must be properly formatted.

### Pillar 4: Zero-Hallucination Source Truth & Data Integrity
- **Rule 10 (PDF Physical Hard-Extraction First)**: Before analyzing any literature, physically extract raw text from the original PDF using tools like `pymupdf` (save as `raw_paper_text.txt`). Any quote labeled as `Original` must match verbatim in `raw_paper_text.txt`.
- **Rule 11 (3-Way Cross-Verification)**: Verify:
  1. Coordinate axes extrema & physical units (cycle count vs. capacity, MPa vs. GPa).
  2. Legend and curve color matching (Sample-A vs. Sample-B).
  3. Text claims vs. curve values (100% interlocking).
- **Rule 12 (Mandatory Ground Truth Audit Report)**: For any paper-based presentation or card, generate a companion `ground_truth_audit_report.md` recording exact page, paragraph, and figure numbers for every cited parameter.
- **Rule 13 (No Unsolicited Sample Renaming)**: Never replace anonymous or neutral sample IDs (e.g. `Sample 1`, `Sample 2`, `Control`, `A`, `B`) with assumed chemical formulation names. The user's explicit sample designations are ground truth.
- **Rule 14 (Zero Hallucinated Citations)**: Never guess or synthesize DOIs, authors, journals, years, or figure references. All citations must be 100% verified against local PDFs or verified databases.

### Pillar 5: Publication Figure Standards & Domain Plotting
- **Rule 15 (Four-Sided Box Frame Standards)**: Top, bottom, left, and right spines must all be visible (`linewidth = 2.5 ~ 3.0 pt`, solid black). Top and right axes must NOT have tick marks (`xtick.top = False`, `ytick.right = False`). Bottom and left ticks must point inward (`tick.direction: in`).
- **Rule 16 (Domain-Specific Plotting Rules - DSC/FTIR/LSV)**:
  - *DSC*: Y-axis label `Heat Flow (a.u.)`, hide absolute numerical values. Endo down (troughs) for melting. Directly annotate $T_\mathrm{g}$ and $T_\mathrm{m}$ on curves with dashed arrows. Set large offset ($\ge 1.0\ \mathrm{a.u.}$) to prevent collisions.
  - *FTIR*: Y-axis label `Transmittance (%, Offset)`, hide numbers. Place legends in clean baseline windows ($1800 \sim 2600\ \mathrm{cm^{-1}}$).
  - *LSV*: Annotate onset decomposition potential directly on curve inflection points. Crop axes rationally to highlight turn-up points.
- **Rule 17 (Vector SVG Text Integrity & Zero `<tspan>`)**: Prevent Matplotlib mathtext from fragmenting text into uneditable `<tspan>` tags. Use clean text with Unicode superscripts/subscripts (`°C`, `⁻¹`, `⁺`). Post-process SVGs to replace residual `STIXGeneral`/`DejaVu Sans` with academic standard `Times New Roman`.
- **Rule 18 (Decoupled Iteration Workflow)**: Never recompile an entire multi-panel master figure when fine-tuning a single subpanel. Follow "single plot compilation -> instant visual verification -> final master assembly".

### Pillar 6: User Protection & Operating Environment Defense
- **Rule 19 (User Final Authority & Asset Protection)**: When a user declares a slide or document finalized ("不要改动任何内容"), treat it as physically Read-Only. Never run automated scripts that overwrite manual edits. Preserve personalized layouts (ending slide styling, title alignment constraints).
- **Rule 20 (Windows Terminal File-First & uv Isolation)**:
  - **File-First Principle**: Never run inline multiline code (`python -c "..."`) on Windows consoles. Always write a standalone `.py` or `.ps1` script first to eliminate quote stripping and parser errors.
  - **uv Virtual Environment Isolation**: Run all Python code strictly within `<project_root>/.venv` using `uv run` or `.venv\Scripts\python.exe`. Never install packages to the host global Python environment. Keep `requirements.txt` synced.
  - **Presentation vs. Speaker Notes Isolation**: Slide screens display ONLY figures and concise claims clearly visible to the audience. Supporting information (SI) details and deep mechanism proofs belong in Speaker Notes.

---

## 🚀 Standard Operating Workflows

### 1. Generating an Academic PPTX
```text
[Input Paper / Notes]
       │
       ▼
[Hard PDF Extraction] ──> Save raw_paper_text.txt
       │
       ▼
[Fact Verification]   ──> Audit parameters & dimensions against figure axes
       │
       ▼
[Build PPTX Script]   ──> Apply dual fonts (Times + 微软雅黑), LaTeX formulas, pure rectangles
       │
       ▼
[Render Slides (PNG)] ──> Run scripts/export_slides.ps1 via PowerPoint COM
       │
       ▼
[Visual Self-Audit]   ──> Inspect PNGs for overlapping, clipping, and font alignment
       │
       ▼
[Delivery & Audit Log]──> Deliver PPTX + ground_truth_audit_report.md
```

### 2. Plotting Publication-Ready Scientific Figures
```text
[Raw Experimental Data] ──> Keep original sample IDs (Rule 13)
       │
       ▼
[Box Frame Configuration] ──> 4-sided spines (2.5-3.0 pt), inward ticks (Rule 15)
       │
       ▼
[Domain Calibration] ──> DSC exo up/endo down, FTIR clean baseline legend (Rule 16)
       │
       ▼
[Vector Export & Clean] ──> Export SVG with Zero <tspan>, Times New Roman font (Rule 17)
```

### 3. Checking Academic Rigor on Any Document
Run the automated rigor scanner before finalizing:
```bash
uv run scripts/scan_academic_rigor.py path/to/document.md
```
This scans for:
- Banned hyperbole terms ("碾压", "神级", "军工级", etc.)
- Unformatted chemical formulas (`CO2`, `Li+`, `Zn2+`, etc.)
- Malformed unit exponents

---

## 🛠️ Companion Tooling in `scripts/`

- `export_slides.ps1`: Automated PowerPoint COM exporter rendering 1080p+ PNGs per slide for visual self-audit.
- `apply_dual_fonts.py`: Lossless OpenXML post-processor setting Latin/Digits to Times New Roman and Chinese to 微软雅黑.
- `scan_academic_rigor.py`: Regex auditor for chemical subscripts and academic tone compliance.
- `sync_agents_to_opensource.py`: Automated tool to sanitize private project paths and update open-source rules.

---

## 💡 Adoption Guide for Other Projects

To adopt this defense system in any other repository:
1. Copy `AGENTS.template.md` to your repository root as `AGENTS.md`.
2. Ensure your virtual environment is initialized with `uv venv .venv`.
3. Add `scripts/export_slides.ps1` and `scripts/apply_dual_fonts.py` to your `scripts/` folder.
4. Instruct your AI agent: *"Please follow the rules in AGENTS.md strictly for all tasks."*
