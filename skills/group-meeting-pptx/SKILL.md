---
name: group-meeting-pptx
description: >-
  Build, revise, audit, and verify lab group-meeting Chinese academic PPTX decks
  from papers or raw reading notes. Use for 组会PPT、组会汇报、文献汇报PPT and
  PPTX QA in <project_root>/presentations; takes precedence over generic slogan-banner
  slide defaults in nature-paper2ppt.
---

# Group Meeting PPTX Workflow

Workspace standard for lab group-meeting presentations in `<project_root>`.
Always verify constraints below before writing code or reporting completion.

## Hard Stop Before Any Write

- **User Final Authority:** If the user states an existing `.pptx` is finalized or instructs not to touch it ("别动我 PPT / 已定稿"), immediately stop all writes to that `.pptx`. Only perform read-only audits or provide independent text notes.

## Resource Map

| Resource | When to Read / Run |
| :--- | :--- |
| [references/house-style-and-layout.md](./references/house-style-and-layout.md) | Slide 1/overview/data/summary/ending geometry, colors, fonts, `add_picture_fit()` |
| [references/visual-fact-audit-checklist.md](./references/visual-fact-audit-checklist.md) | Per-panel axis, NMR, TGA, CV, ToF-SIMS, IR colorbar & hype checks |
| [scripts/verify_group_pptx.py](./scripts/verify_group_pptx.py) | Mandatory exit-`0` programmatic PPTX gate |
| [export_slides.ps1](../../scripts/export_slides.ps1) | PowerPoint COM full-slide PNG export for visual inspection |

## Blocking 5-Step Protocol

### 1. Align Template and House Style First
1. Inspect the latest finalized deck in `<project_root>/presentations\` (e.g., `<latest_finalized_deck>.pptx`) and template `<project_root>/presentations\<house_template_deck>.pptx`.
2. Read [references/house-style-and-layout.md](./references/house-style-and-layout.md) for exact coordinates, layouts, and dual-font helpers.

### 2. Visual Fact Audit Before Authoring Slides
1. Load extracted physical text (`raw_paper_text.txt`, `si_raw_text.txt`) and view **every cropped PNG asset** + paired SI figures before writing text.
2. Never blindly copy numbers from secondary summaries (`ground_truth_audit_report.md`, `paper_xray.md`) without spot-checking primary text and cropped axes.
3. Verify every panel against [references/visual-fact-audit-checklist.md](./references/visual-fact-audit-checklist.md): separate axis ceilings (`800`) from true curve peaks (`~650`), check TGA dashed dividers (`~315–320 °C`), check `⁷Li NMR` direction (`ppm` increase = downfield / 低场), verify CV scan bounds, and confirm chart types (`dual-axis bar` vs `radar`).
4. **Screen vs Speaker Notes Isolation:** On-slide cards strictly describe what is visible on screen; move SI-only figures and deep mechanism details into Speaker Notes.

### 3. Build Lossless Aspect-Ratio Slides Without Slogans
- Save the builder script in `<project_root>/papers/<paper_id>/` or `<project_root>/presentations/`.
- Always embed images with `add_picture_fit()` (`w_px/h_px` aspect ratio locked); retain full axes and subpanel letters during cropping.
- **Data slides omit top `21 pt` proposition banners and `【结论短句】` prefixes.**
- Inside flat pure-white `MSO_SHAPE.RECTANGLE` (`#CFD8DC`, `MSO_ANCHOR.TOP`, `20%–30%` bottom margin), use centered bold `#1F497D` figure-name headings (`图 a：表征/测试名称`) + 1–2 concise factual lines + Unicode subscripts/superscripts (`₀–₉`, `⁰–⁹`, `⁺`, `⁻`, `ₐ`).
- Use screen-direction labels (`左上图 a`), zero `(Figure X)` extraction tags, and zero hype/analogy/unmeasured phrases.

### 4. Dual-Font Pass With Double Slide Exemption
- Enforce `Times New Roman` (`<a:latin>`) + `微软雅黑` (`<a:ea>`) on content slides, **explicitly skipping `s_idx == 0` (Cover) and `s_idx == total - 1` (Ending)**.
- Lock Cover presenter and date strictly centered (`left = (slide_width - width) / 2`).
- Lock Ending slide strictly to centered `THANKS!` (`Arial Bold 58 pt #9C1D22` XML) + presenter/date, with **zero** `"敬请各位老师、师兄师姐批评指正！"`.

### 5. Dual Verification Gate Before Reporting Done
1. Run deterministic PPTX verification (must exit `0`; pass `--check-extraction-tags` and `--extra-banned` when paper-specific traps apply):
   ```text
   .venv\Scripts\python.exe skills/group-meeting-pptx/scripts/verify_group_pptx.py --pptx "<path_to_pptx>" --check-extraction-tags
   ```
2. Export every slide via PowerPoint COM (`BypassSandbox` if host COM blocks sandbox):
   ```text
   powershell -ExecutionPolicy Bypass -File scripts/export_slides.ps1 -PptxPath "<path_to_pptx>"
   ```
3. Visually inspect **every rendered PNG slide** with `read_file` to verify zero overlap, zero text truncation, and intact fonts before concluding.
