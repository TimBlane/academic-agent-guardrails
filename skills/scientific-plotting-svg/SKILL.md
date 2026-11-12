---
name: scientific-plotting-svg
description: >-
  Generate, refine, and audit publication-grade data figures (DSC, FTIR, LSV,
  electrochemical cycling, dual-Y, symmetric cell insets) as unfragmented SVGs
  and 3D diffusion-model schematics. Use for 科研绘图、Matplotlib 曲线、SVG
  后处理、矢量图表规范与 3D 机理图生成.
---

# Scientific Plotting & Clean SVG Workflow

Workspace plotting protocol for publication-ready electrochemistry and materials figures in `<project_root>`.

## Hard Guardrails Before Plotting

1. **Preserve Original Sample Names:** Never rename user sample codes (e.g., do **not** replace `Sample 1–4` with `<Formula-A>`/`<Formula-B>`) unless the user explicitly provides the formula mapping.
2. **Route Quantitative vs 3D Schematics Strictly:**
   - **Data Curves & Spectra:** Use Python (`Matplotlib` / `Seaborn`) with real extracted data only.
   - **3D Mechanism & Network Illustrations:** Never draw crude Matplotlib 3D wireframes (`mpl_toolkits.mplot3d`). Invoke `image-generator` (diffusion tool) for publication-style 3D renders and save complete prompts beside the target paper/figure folder.
3. **Single-Figure Decoupled Iteration:** During visual refinement, compile and inspect each standalone subplot individually before regenerating any multi-panel composite sheet.

## Resource Map

| Resource | Purpose |
| :--- | :--- |
| [pub_style.py](../../scripts/pub_style.py) | Shared Matplotlib `set_pub_style()` + `safe_save_clean()` baseline |
| [references/matplotlib-electrochem-specs.md](./references/matplotlib-electrochem-specs.md) | Box frames, inward ticks, DSC, FTIR, LSV, Dual-Y CE, Li\|\|Li insets |
| [references/svg-and-3d-rules.md](./references/svg-and-3d-rules.md) | Zero-`<tspan>` editable SVG standard, prompt logging, decoupled flow |
| [scripts/audit_svg_postprocess.py](./scripts/audit_svg_postprocess.py) | Font sanitizer + `<tspan>` exit-`0` verification gate |

## Blocking 5-Step Protocol

### 1. Load Shared Styling Base & Frame Rules
- Import `set_pub_style` from `scripts/pub_style.py` (add `<project_root>/scripts` to `sys.path` or replicate cleanly).
- Verify four-sided closed black box spines (`2.5–3.0 pt`), `xtick.top = False`, `ytick.right = False`, and inward bottom/left major ticks (`8–9 pt`).

### 2. Apply Domain-Specific Plot Specifications
Read [references/matplotlib-electrochem-specs.md](./references/matplotlib-electrochem-specs.md) matching your characterization type:
- **DSC:** `Heat Flow (a.u.)` hidden Y numbers, Exo-Up downward troughs, bare sample legends, dashed-arrow `Tg`/`Tm` callouts on traces, vertical offset `>= 2x` trough depth.
- **FTIR:** `Transmittance (%, Offset)` hidden Y numbers, band callouts, legend inside quiet `1800–2600 cm⁻¹` baseline window.
- **LSV:** Same-color onset potential dashed-arrow callouts (`e.g. 4.15 V`), trimmed polarization tail.
- **Full-Cell Dual-Y Cycling:** Attribute champion CE (`#C53030` open markers) vs multi-group neutral Slate Gray (`#64748B`), keeping `>= 20–25 mAh g⁻¹` air gap below CE scatter (`50%–105%` right axis).
- **Symmetric-Cell Inset:** `10–20 h` (`~5–10` cycles) flat square waves in quiet white region with `>= 0.05 V` clearance.

### 3. Enforce Zero-`<tspan>` Editable SVG Labels
Read [references/svg-and-3d-rules.md](./references/svg-and-3d-rules.md): keep `svg.fonttype = 'none'` and use clean Unicode symbols (`°C`, `⁻¹`, `⁺`, `⁻`, `₂`) instead of `$...$` Mathtext for text annotations so Illustrator/CorelDraw opens intact single `<text>` nodes.

### 4. Normalize Residual Fonts & Audit SVG Integrity
Run the post-process cleaner and SVG integrity auditor (must exit `0`):
```text
.venv\Scripts\python.exe skills/scientific-plotting-svg/scripts/audit_svg_postprocess.py "<svg_or_dir>" --fix
```
Confirm zero fragmented `<tspan>` tags and pure `Times New Roman` font declarations.

### 5. Pixel-Inspect Paired PNG Before Delivery
1. Save a `300 dpi` PNG alongside each SVG (`characterization_multipanel.png` only after individual subplots pass).
2. Inspect via `read_file` for label overlaps, truncated axes, dual-Y air gap (`20–25 mAh g⁻¹`), and `Li||Li` inset boundaries.
3. For 3D renders, persist exact prompts and parameters in `<paper_dir>/3d_prompts.md` or `<figure_dir>/`.

## Done Checklist
- Original user sample names preserved (`Sample 1–4` untouched unless mapped by user)
- Standalone subplot compiled and visually inspected before composite assembly
- `audit_svg_postprocess.py` exited `0` (`0` `<tspan>`, `Times New Roman` only)
