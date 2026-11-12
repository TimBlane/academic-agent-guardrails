---
name: academic-agent-guardrails
description: v2.0.0 modular 2-tier academic research, presentation, scientific plotting, and literature digestion guardrails for AI coding agents (Antigravity, Claude Code, Cursor, Copilot). Enforces <= 22 KB Layer-0 rules plus 3 domain sub-skills with deterministic exit-0 verification gates.
---

# Academic Agent Guardrails v2.0.0 (两层模块化科研与多智能体攻防架构)

This skill equips AI coding agents with a **2-tier modular defensive architecture** built from real academic research, data visualization, and slide-deck debugging lessons:

- **Layer 0 (`AGENTS.md`, `<= 22,000` bytes, Rules 1–7)**: Compact, non-truncatable cross-task redlines (prevents silent overflow in IDEs with 24 KB context caps) plus **Rule 7 mandatory skill routing**.
- **Layer 1 (`skills/` / `.agents/skills/`, 3 Domain Sub-Skills + Exit-0 Gates)**: Progressive-disclosure reference manuals, shared plotting baseline (`scripts/pub_style.py`), and deterministic verification scripts that must return exit code `0` before delivery.

---

## 🎯 When to Use This Skill

Activate or apply this skill whenever a task involves:
1. **Group Meeting & Journal Club PPTX (`group-meeting-pptx`)**: Building, revising, auditing, or visually verifying Chinese/English academic slide decks.
2. **Publication Figures & 3D Schematics (`scientific-plotting-svg`)**: Plotting DSC, FTIR, LSV, Dual-Y cycling/CE, symmetric-cell zoom insets as `<tspan>`-free editable SVGs via `pub_style.py`, or generating 3D mechanism art.
3. **Bilingual Paper Reading & Audit Suites (`paper-bilingual-reader`)**: Hard-extracting PDF/SI raw text (`pymupdf`), building `paper.md` + `source_map.json`, or running closed-loop cross-file errata fixes.
4. **Cross-IDE Multi-Agent Workflows (Windows + WSL)**: Maintaining clean code persistence, `uv` environment lockdown, and zero-hallucination academic tone.

---

## 🏗️ v2.0.0 Two-Tier Modular Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                   LAYER 0: AGENTS.md (Rules 1–7, <= 22 KB)                  │
│  1. Asset Persistence   2. WSL-First & uv Lockdown   3. Source Truth & Tone │
│  4. Sample/Cite Fidelity 5. Dual Fonts & r"""..."""  6. PPTX Protection     │
│  7. Mandatory Domain Skill Routing Table ──┬──────────────────┬─────────────┤
└────────────────────────────────────────────┼──────────────────┼─────────────┘
                                             ▼                  ▼
┌───────────────────────────┐  ┌─────────────────────────┐  ┌──────────────────────────┐
│  skills/group-meeting-pptx│  │ skills/scientific-      │  │ skills/paper-bilingual-  │
│  • house-style-and-layout │  │         plotting-svg    │  │         reader           │
│  • visual-fact-audit      │  │ • pub_style.py baseline │  │ • reader & sourcemap spec│
│  Gate: verify_group_pptx  │  │ • electrochem & SVG/3D  │  │ • pitfalls & errata log  │
│      + export_slides.ps1  │  │ Gate: audit_svg_post    │  │ Gate: audit_markdown_    │
│        (Exit 0)           │  │        (Exit 0)         │  │        suite (Exit 0)    │
└───────────────────────────┘  └─────────────────────────┘  └──────────────────────────┘
```

---

## 📋 Layer 0 Summary: The 7 Global High-Voltage Rules

1. **Rule 1｜Code, Script & Asset Persistence**: Never leave executable scripts in temporary brain/AppData sandboxes. Persist shared helpers in `scripts/`, paper pipelines in `papers/<paper_id>/`, slide builders in `presentations/`, and local workflows in `.agents/skills/`.
2. **Rule 2｜WSL-First, `uv` Isolation & File-First Execution**:
   - Prefer WSL (`<wsl_project_root>`) when available; reserve PowerShell strictly for Windows-exclusive COM interfaces (`scripts/export_slides.ps1`).
   - **File-First**: Never inline business/data logic via `python -c "..."` or `powershell -Command`; write standalone `.py` / `.sh` files with explicit `encoding='utf-8'`.
   - **Strict `uv` Virtual Environment**: Only run via `.venv\Scripts\python.exe` (Windows) or `.venv-linux/bin/python` (WSL); guard critical scripts against `sys.prefix == sys.base_prefix`.
3. **Rule 3｜Zero-Hallucination Source Truth & Anti-Hyperbole**:
   - Always extract physical text (`raw_paper_text.txt` / `si_raw_text.txt`) via `pymupdf` (`fitz`) first.
   - **Inspect actual cropped images before writing**: Separate axis top ticks from curve peaks; note TGA/CV boundaries; enforce **`7Li NMR` downfield chemistry (`ppm` increase = low field / deshielding)**; enforce matrix-background relativity in XPS/FTIR and contour continuity in 3D ToF-SIMS.
   - Ban hype words ("军工级", "颠覆性", "彻底杜绝", "零恶化"), ungrounded analogies, and unmeasured sensory claims; fix factual errors across *all* linked artifacts in one closed loop.
4. **Rule 4｜Sample Naming Fidelity & Zero Fabricated Citations**: Never overwrite raw sample labels (e.g., `Sample 1–4`) with assumed chemical formulas without an explicit user mapping. Cite only verified DOIs, journals, years, and figure indices present in local PDFs or checked online sources.
5. **Rule 5｜Dual Fonts, Subscripts/Superscripts & Raw Strings**:
   - Body slides and plots: `Times New Roman` (Latin/digits) + `微软雅黑` (Chinese), explicitly preserving `<a:latin/>` + `<a:ea/>`, while **exempting Cover (`Slide 0`) and Ending (`Slide -1`)**.
   - Subscript/superscript all chemical formulas ($\mathrm{CO_2}$, $\mathrm{Li_3N}$), ion charges ($\mathrm{Li}^+$), powers ($10^{-4}$), and units ($\mathrm{cm}^{-1}$).
   - Always use Python raw strings `r"""..."""` when emitting LaTeX strings so `\approx`, `\alpha`, or `\text` never degrade into `\x07` or `\t`.
6. **Rule 6｜Academic PPTX Protection & Screen-vs-Notes Separation**:
   - **Read-Only Lock**: Finalized user `.pptx` decks are strictly read-only.
   - **Visual Audit & Geometry**: Run `scripts/export_slides.ps1`, inspect every rendered PNG, lock image aspect ratios, use flat rectangles (`MSO_SHAPE.RECTANGLE`, `#CFD8DC`, `TOP` anchor, `20%–30%` breathing room), strip extraction tags like `(Figure 4a-c)`, avoid `21 pt` top conclusion banners / `【】` on group-meeting data slides (use `图 X：...`), keep `Slide -1` minimal (`THANKS!` + speaker/date), and isolate deep SI/mechanisms into Speaker Notes.
7. **Rule 7｜Mandatory Domain Skill Routing Table**:

| Task Domain | Route to Sub-Skill | Exit-0 Gate / Tooling |
| :--- | :--- | :--- |
| **Group-meeting / Journal-club PPTX** | [`skills/group-meeting-pptx/SKILL.md`](skills/group-meeting-pptx/SKILL.md) | `skills/group-meeting-pptx/scripts/verify_group_pptx.py` + `scripts/export_slides.ps1` |
| **Scientific Plotting (DSC/FTIR/LSV/Dual-Y/3D)** | [`skills/scientific-plotting-svg/SKILL.md`](skills/scientific-plotting-svg/SKILL.md) | `skills/scientific-plotting-svg/scripts/audit_svg_postprocess.py` + `scripts/pub_style.py` |
| **Paper Extraction, Bilingual Reader & Audit** | [`skills/paper-bilingual-reader/SKILL.md`](skills/paper-bilingual-reader/SKILL.md) | `skills/paper-bilingual-reader/scripts/audit_markdown_suite.py` |

---

## 🛠️ Verification Gates & Companion Tooling

Run these deterministic checks before declaring any deliverable complete:

```bash
# 1. Verify PPTX layout, dual-font exemption, chemistry formatting & banned terms
.venv/Scripts/python.exe skills/group-meeting-pptx/scripts/verify_group_pptx.py --pptx deck.pptx

# 2. Post-process & verify zero-<tspan> Times New Roman SVGs
.venv/Scripts/python.exe skills/scientific-plotting-svg/scripts/audit_svg_postprocess.py fig.svg --fix

# 3. Audit paper.md + source_map.json against raw-string escapes, math balance & disk figures
.venv/Scripts/python.exe skills/paper-bilingual-reader/scripts/audit_markdown_suite.py --dir papers/<paper_id> --check-images --check-math --check-json
```

Additional root utilities in `scripts/`:
- `scripts/pub_style.py`: Shared publication Matplotlib baseline (`set_pub_style()`, `safe_save_clean()`, `annotate_curve_point()`).
- `scripts/export_slides.ps1`: Windows PowerPoint COM exporter rendering slide PNGs for visual inspection.
- `scripts/apply_dual_fonts.py`: Standalone OpenXML dual-font post-processor (preserving Slide 0 and Slide `-1` exemptions when configured).
- `scripts/scan_academic_rigor.py`: Lightweight standalone regex scanner for markdown/text rigor.
- `scripts/install.py`: Cross-platform interactive / CLI installer deploying selected modules and OS/WSL rules.
- `scripts/sync_agents_to_opensource.py`: Workspace-to-OSS sanitizer with `<= 22,000` byte cap enforcement.

---

## 🔗 Recommended Ecosystem Pairings

For end-to-end literature discovery, peer-review simulation, and manuscript drafting alongside these strict engineering guardrails, pair with complementary academic skills (e.g., `nature-academic-search`, `nature-paper-xray`, `nature-figure`, `nature-writing`). Notice that workspace Rule 7 delegates group-meeting PPTX, vector SVG electrochemistry plots, and bilingual `source_map.json` readers with precedence to `skills/*` above.
