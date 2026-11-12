# Visual Fact Audit Checklist (Anti-Hallucination Defense)

Run this panel-by-panel audit on cropped PNG images + `raw_paper_text.txt` / `si_raw_text.txt` **before** authoring card text or Speaker Notes. Real recurring mistakes prevented by this checklist are listed explicitly below.

## 1. Axis Limits vs Actual Data Values
- **Y-Axis Top Tick != Data Peak:** Never read the axis ceiling as the peak signal (e.g., ToF-SIMS `LiF₂⁻` Y-axis upper tick `800` vs actual curve peak `~650`, or decay tail ending at `~250 s` vs total axis).
- **Dashed Inflection Divider Meaning (TGA):** Read what happens *before* and *after* vertical dashed guide lines. Never hallucinate `"300 °C 零失重分解"` when `~20.8 wt%` mass loss already occurred before the `~315–320 °C` dashed divider (e.g., residual DMF evaporation stage).
- **X/Y Unit Separation:** Verify units (`MPa` vs `GPa`, `mAh g⁻¹` vs `mAh`, `cm⁻¹`, `cycles`, `s`, `h`). Never read a capacity value (`mAh g⁻¹`) as cycle count (`cycles`), or coulombic efficiency (`99.8%`) as porosity.

## 2. Spectroscopy, NMR & Electrochemical Conventions
- **NMR Chemical Shift Direction:** Higher / less-negative `ppm` (`-1.01 ppm -> -0.98 ppm`) is **downfield / deshielded (低场位移 / 去屏蔽)**; more negative `ppm` is **upfield / shielded (高场位移)**. Do not invert this under any circumstance.
- **Matrix Background Relativity (XPS / FTIR / XRD):** When deconvolved additive/SEI peaks (`LiF`, `LiBr`) are smaller than dominant polymer matrix peaks (`C–F`), never call them `"极其强烈"` or `"主峰"`. State the deconvolved binding energy/change objectively and note depth-profiling complementarity (`ToF-SIMS`) when relevant.
- **3D Volume & Contour Continuity (ToF-SIMS / COMSOL):** Never exaggerate sparser point clouds or lighter pink shading into binary claims (`"几乎完全透明"`, `"彻底清零"`). Describe the visible sparsity/attenuation first, then explain suppressed decomposition.
- **Scan-Rate CV & `b`-Value Audits:** Read exact scan-rate legends (e.g., `0.1–1.0 mV s⁻¹`; never invent phantom bounds like `560 cm`). Check printed figure legend assignments (`Peak O` vs `Peak R`) against body prose and log any text-figure swap errata in Speaker Notes.

## 3. Chart Type, Colorbar & Microscopy Checks
- **Chart Type Exactness:** Visually confirm whether a multi-metric comparison is a **dual-axis grouped bar chart** (`cycles` + `temperature`/`rate`) or a radar/spider chart; never guess the chart type from topic similarity.
- **Independent Colorbars (Infrared Thermography / AFM):** Verify whether paired panels share one unified colorbar or carry independent `min–max` scales. If scales differ across panels, describe qualitative core thermal distribution and relative contrast honestly instead of forging invalid cross-panel subtractions.
- **Surface vs Cross-Section SEM:** Check what the screen image actually shows (`top-view` / `surface SEM` vs `cross-section thickness SEM` in SI `Fig. S10`). If cross-section thickness numbers come from SI while only surface SEM is on screen, cite SI cleanly inside **Speaker Notes**, not as an on-screen image label.

## 4. Forbidden Phrasing & Peer-Review Evidence Boundaries
- **Banned Hype / Marketing:** `军工级`, `工业级`, `神级`, `颠覆性`, `革命性`, `顶尖`, `第一梯队`, `彻底杜绝`, `彻底终止`, `断崖式`, `令人瞩目`, `白炽`, `暴力`.
- **Banned Invented Analogies (unless verbatim in source text):** `避雷针效应`, `活塞式`, `分子手术刀` etc.
- **Banned Unmeasured Sensory Claims:** `无爆鸣` (no acoustic mic), `无发烟` / `无烟无火` / `毫无冒烟` (no gas/smoke analyzer), `离火即熄` / `离火自熄`, `万无一失`, `不燃不爆`, `零失重`, `零恶化`, `零积累`. Describe only instrumented observables (`IR thermography`, `LED continuity under folding/nail/cutting`, `ARC TOER/TTR`).
- **Secondary Audit Rule:** Never treat a pre-existing `ground_truth_audit_report.md` as infallible. Cross-check key numbers, axis readings, and figure assignments against primary `raw_paper_text.txt` + actual cropped figures before building slides.
