# Audit Pitfalls, Source Errata & Anti-Hallucination Reference

Real recurring failure modes cataloged from workspace audits; inspect before drafting or approving any paper reading suite.

## 1. Python Generator Escape Corruption (Silent LaTeX Loss)
- **Failure Mode:** Using ordinary string literals `"""..."""` instead of raw strings `r"""..."""` inside Python file builders causes:
  - `\approx` -> `\x07pprox` (BEL char + `pprox`)
  - `\alpha` -> `\x07lpha` (BEL char + `lpha`)
  - `\text{...}` -> `<TAB>ext{...}`
- **Mandatory Prevention:** Always author multi-line Markdown/LaTeX Python scripts with `r"""..."""` and scan output with `scripts/audit_markdown_suite.py`.

## 2. Primary Source Errata Pattern Catalog (Examples to Catch & Document)
Always verify suspect paper claims physically and record genuine source inconsistencies in `translation_notes.md` (`**E1**..`) and `ground_truth_audit_report.md`:
1. **Unit Order-of-Magnitude Typos:** e.g., bond dissociation energy printed as `312.27 J mol⁻¹` missing `k` (real covalent C–Br energy is `~280–318 kJ mol⁻¹`; `312 J mol⁻¹` is below room-temperature `RT ~ 2.5 kJ mol⁻¹`).
2. **Polymer Transition Confusion:** Authors mislabeling crystalline melting endotherm `Tm` (`141 °C -> 91 °C`) as glass transition `Tg` (`PVDF-HFP` real `Tg` is `-35 to -40 °C`).
3. **Intro Rhetoric vs Measured Control Drift:** Introduction citing baseline `<0.1 mS cm⁻¹` while experimental plot (e.g., Fig. 4g) measures `0.27 mS cm⁻¹` (`2.7x` mismatch).
4. **Text-vs-Figure Value Swaps:** Prose reporting `b` values `oxidation (0.693)` and `reduction (0.602)` while plot legend labels `Peak O = 0.602` and `Peak R = 0.693`.
5. **Cycle-Count / Index / Legend Drift:** Summary citing `230 cycles` vs Results/plot `220 cycles`; swapped figure sub-letters `(c)` vs `(e)`; monomer alias mismatch (`TBBPA` in schematic legend vs `BADBP` in text); cure temp mismatch (`120 °C` main text vs `70 °C / 12 h` in SI).
6. **NMR & Axis Ceiling Traps:** `ppm` shift `-1.01 -> -0.98` is downfield (低场), not upfield; `ToF-SIMS` Y-axis max `800` is frame ceiling while data peaks at `~650`; TGA `~315–320 °C` dashed divider marks end of `20.8%` residual solvent stage, NOT zero mass loss.

## 3. Characterization Rhetoric & Peer-Review Evidence Boundaries
- **Matrix Background Relativity (XPS / FTIR / XRD):** When deconvolved additive/SEI peaks (`LiF`, `LiBr`) are weak next to dominant polymer C–F peaks, describe signal onset/deconvolution relative to control rather than calling them `"极其强烈"`, and reference complementary depth profiling (`ToF-SIMS`).
- **3D Volume / Map Continuity:** Sparser `ToF-SIMS` 3D point clouds or lighter pink regions reflect suppressed degradation, NOT `"几乎完全透明"` or `"彻底清零"`.
- **Forbidden Banned Terms:** Never use `军工级`, `工业级`, `神级`, `颠覆性`, `革命性`, `万无一失`, `无烟无火`, `无声无息`, `断崖式`, `令人瞩目`, `离火自熄`, `离火即刻自熄`, `离火即熄`, `剧烈爆燃`, `火球喷溅`, `毫无冒烟`, `零失重分解`, `几乎完全透明`, `极其强烈`.
- **Structural / Scope Skepticism (Preserve Hedging):**
  - Check whether `"solid polymer electrolyte"` loses `~20 wt%` residual `DMF` in TGA (mechanistically plasticized / quasi-solid GPE).
  - Check missing negative controls (e.g., no asymmetric monomer isomer control -> `"symmetrical topology"` is partially rhetoric alongside crosslinking density + Br functionality).
  - Separate electrode specific capacity (`mAh g⁻¹`, lab pouch `~170 mAh g⁻¹`) from unmeasured commercial Ah-scale capacity.
