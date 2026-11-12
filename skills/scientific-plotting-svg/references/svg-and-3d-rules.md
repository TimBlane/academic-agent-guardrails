# SVG Text Integrity & 3D Conceptual Figure Rules

## 1. Zero-`<tspan>` Editable SVG Standard
- Matplotlib `$...$` Mathtext splits single strings like `$T_g = -18.6\ ^\circ\mathrm{C}$` into fragmented `<tspan>` runs upon SVG export, making text editing in Adobe Illustrator / CorelDraw painful.
- **Required Fix:**
  1. Set `plt.rcParams['svg.fonttype'] = 'none'` and `plt.rcParams['pdf.fonttype'] = 42`.
  2. Write axis labels, legends, and annotations using clean plain text + standard Unicode characters (`°C`, `⁻¹`, `⁻²`, `⁺`, `⁻`, `₂`, `₃`, `ₐ`) instead of `$...$` where vectorized curves do not strictly require nested math layout.
  3. Run `scripts/audit_svg_postprocess.py --fix` on exported SVGs to replace any fallback `STIXGeneral` or `DejaVu` font strings with `'Times New Roman'` and verify `<tspan>` count equals `0`.

## 2. Single-Figure Decoupled Iteration Workflow
- During visual polish (adjusting DSC spacing, LSV cutoffs, legend coordinates, inset clearance), build and verify **one standalone figure script at a time**.
- Never rebuild multi-panel composite figures (`characterization_multipanel` etc.) inside minor single-panel tweak loops; only run assembly scripts once every sub-figure passes individual inspection.

## 3. 3D Mechanism & Conceptual Schematics Protocol
- **Prohibited:** Crude Matplotlib 3D wireframe sticks/spheres (`mpl_toolkits.mplot3d`) for polymer chains, solvation sheaths, ion hopping pathways, or battery stacks.
- **Required:** Invoke `image-generator` (diffusion generation tool) for publication-style 3D scientific illustrations with subsurface scattering, translucent crystal facets, flexible helix networks, and particle lighting.
- **Prompt Persistence:** Save the exact generation prompt, aspect ratio, seed/notes, and iterative adjustments in a Markdown or JSON file inside the same paper/figure folder (e.g., `<project_root>/papers/<paper_id>/3d_prompts.md`) so other collaborators or agents can reproduce or refine renders cleanly.
