# Matplotlib & Electrochemistry Domain Specifications

Derived from workspace top-tier publication standards (former Rules 17, 18, 22) and aligned with [pub_style.py](../../../scripts/pub_style.py).

## 1. Universal Coordinate Frame & Typography
- **Four-Sided Closed Box Frame:** Enable all four spines (`axes.spines.top/right/bottom/left = True`), pure black `#000000`, `2.5–3.0 pt` linewidth.
- **No Ticks on Top & Right:** Top and right spines are solid lines only (`xtick.top = False`, `ytick.right = False`, `ax.tick_params(top=False, right=False)`).
- **Inward Left & Bottom Ticks:** `tick.direction = 'in'`, major tick width `2.5–3.0 pt`, length `8–9 pt` (minor ticks `5 pt` length, `2.0 pt` width).
- **Fonts:** Bold `Times New Roman` for Latin text, numbers, units, and labels.

## 2. Thermal, Spectroscopy & Electrochemical Voltammetry Plots

### Differential Scanning Calorimetry (DSC)
- **Y-Axis:** Title `Heat Flow (a.u.)`; **hide Y tick marks and numeric values**.
- **Exo-Up Endothermic Orientation:** Polymer melting endotherms point **downward as troughs**. Negate raw positive heat-flow values if exported with endothermic-up sign.
- **Pure Legends & Direct Curve Callouts:** Legend lists only bare sample names (never `(Tm = 56.6 °C)`). Annotate `Tg` inflection and `Tm` trough directly on curves with matching-color dashed arrows (`Tg = -18.6 °C`, `Tm = 56.6 °C`).
- **Vertical Stacking Gap:** Offset stacked thermograms by `>= 2x` melting trough depth (e.g., `Delta >= 1.0 a.u.`) and reserve top margin for the legend so troughs never collide with adjacent traces.

### Fourier-Transform Infrared Spectroscopy (FTIR)
- **Y-Axis:** Title `Transmittance (%, Offset)` with **all numeric Y ticks hidden**.
- **Peak Bands & Clean Legend Window:** Shade characteristic bands with chemical group callouts (`C-H₂`, `TFSI⁻`, `C=O`, `O-H`); place legend inside the quiet `1800–2600 cm⁻¹` baseline window away from intense peaks.

### Linear Sweep Voltammetry (LSV)
- **Onset Annotations:** Label each curve's electrochemical oxidation inflection with a matching-color dashed arrow (`4.15 V`, `4.76 V`, `5.10 V`).
- **Axis Cropping:** Trim high-polarization artificial plateaus/drops (e.g., keep `3.0–5.5 V` and `-0.08–0.35 mA`) to emphasize oxidative stability breakdown.

## 3. Full-Cell Dual-Y Cycling & Symmetric Cell Insets

### Dual-Y Capacity Retention + Coulombic Efficiency (CE)
- **Scenario A (Single Champion CE):** When showing one CE trace specifically attributed to the champion cell (e.g., `<Formula-B>`), match the champion sample's hue (e.g., Ruby Red `#C53030`) with open markers (`mfc='none'`) and match right Y-axis ticks/label color to signal ownership.
- **Scenario B (Multi-Sample / Neutral Baseline):** When CE represents a neutral reference or palette density is already high, use low-saturation Slate Gray (`#64748B`); avoid unrelated clashing bright colors.
- **Scenario C (User Override):** User-specified palette and marker assignments always take highest priority.
- **Vertical Spatial Decoupling:** Expand the right CE Y-axis (e.g., `50%–105%` or `40%–105%`) so `98%–100%` CE scatter points sit high in the upper headroom (`>180 mAh g⁻¹` left-axis level), maintaining **`>= 20–25 mAh g⁻¹` clear vertical whitespace** above capacity curves (`90–160 mAh g⁻¹`).

### Symmetric Cell (`Li||Li`) Zoom-In Inset
- **Window Width:** Show `10–20 h` (`~5–10` complete charge/discharge square-wave cycles) at `1.0–1.2 pt` linewidth to clearly resolve flat plateaus without solid-block ink merging.
- **Placement:** Anchor inside quiet white space after curve termination (e.g., `600–1250 h`) with explicit top/bottom `0.05 V` clearance from main traces and outer spines.
