# Group-Meeting House Style & Slide Geometry Specification

Reference specification derived from finalized lab decks (`<latest_finalized_deck>.pptx`), template (`<project_root>/presentations\<house_template_deck>.pptx`), and verified production builder (`build_perfect_aspect_pptx.py`).

## 1. Template, Slide Size & Master Layouts
- **Slide Dimensions:** 16:9 widescreen (`13.333 × 7.5 in`).
- **Preserve Cover (`prs.slides[0]`):** Modify in-place; drop template slides `1..len-1` cleanly via relationship + `_sldIdLst` cleanup before appending slides.
- **Content Layout:** `prs.slide_layouts[0]` (`1_节标题` — inherits emblem and footer motto).
- **Ending Layout:** `prs.slide_layouts[2]` (`2_节标题` — inherits burgundy arch corners).

## 2. Color Palette & Typography
- `COLOR_PRIMARY`: `#1F497D` (Deep Navy — slide headings, figure-block subheadings)
- `COLOR_SECONDARY`: `#2E75B6` (Steel Blue)
- `COLOR_BURGUNDY`: `#9C1D22` (Wine Red — `THANKS!`, control-group warning headers)
- `COLOR_ACCENT_GREEN`: `#2E7D32` (Forest Emerald — modified-group positive headers)
- `COLOR_TEXT_MAIN`: `#222222` (Body text) | `COLOR_TEXT_MUTED`: `#555555` (Ending presenter line / cover date)
- `COLOR_CARD_BORDER`: `#CFD8DC` | `COLOR_WHITE`: `#FFFFFF`
- **Dual-Font Split:** English letters, digits, units, symbols -> `Times New Roman` (`<a:latin>`, `<a:cs>`); Chinese text -> `微软雅黑` (`<a:ea>`).
- **Mandatory Double Exemption:** `apply_dual_fonts_to_presentation(prs)` MUST `continue` on `s_idx == 0` and `s_idx == total - 1`.

## 3. Slide-by-Slide Geometry & Styling

### Slide 1 — Cover Page (`prs.slides[0]`)
- `shapes[0]` banner: `"组会汇报"`, `微软雅黑 44 pt Bold #FFFFFF`, centered.
- `shapes[1]` presenter: `center_w = Inches(9.0)`, `left = int((prs.slide_width - center_w) / 2)`, `top = 5755640`, margins `0`, `PP_ALIGN.CENTER`, `微软雅黑 20 pt Bold #222222`.
- `shapes[2]` date: same `left` & `center_w`, `top = 6151245`, margins `0`, `PP_ALIGN.CENTER`, `微软雅黑 17 pt #555555`.

### Intro / Overview / Mechanism / Summary Slides (`21 pt` top title allowed)
- **Top Title Box:** `Inches(0.8, 0.60, 11.8, 0.48)`, `21 pt Bold #1F497D` (e.g., `文献概览`, `研究背景与设计思路`, `对称分子拓扑构筑与机理示意图`, `总结与启示`). Never include `(Figure 1)` or `【】`.
- **Overview Slide:** Header image fits `(1.16, 1.20, 11.0, 2.95)`; bottom flat white card `(1.16, 4.32, 11.0, 2.45)`.
- **Background 2-Column Slide:** Left card `(0.80, 1.30, 5.65, 5.30)` + right card `(6.88, 1.30, 5.65, 5.30)`.
- **Summary 3-Column Slide:** Three equal flat white cards `top=1.25, w=3.75, h=5.50` at `left = 0.80`, `4.79`, `8.78`; section headings `14.0 pt Bold`, body `10.5 pt`.

### Data & Characterization Slides (Clean Banner-Free Layout)
- **No Top `21 pt` Proposition Title Banner and No Bottom Strip.** Let the experimental figure own vertical canvas (`y = 0.88` to `6.90`).
- **Left / Main Figure Zone:** `x = Inches(0.80)`, `y = Inches(0.88)`, `w = Inches(7.45)`, `h = Inches(6.02)` (subpanels can form clean rows/grids inside `x: 0.80–8.25, y: 0.88–6.90`).
- **Right Analysis Card:** Flat `MSO_SHAPE.RECTANGLE` at `(Inches(8.45), Inches(0.88), Inches(4.08), Inches(6.02))`, `#FFFFFF` fill, `#CFD8DC` `1 pt` border, `tf.vertical_anchor = MSO_ANCHOR.TOP`, margins `(0.18, 0.15, 0.18, 0.15) in`. Leave `20%–30%` breathing whitespace at card bottom.
- **Card Typography Format (`add_fig_block`):**
  - Subheading: `PP_ALIGN.CENTER`, Bold `#1F497D`, `12.0–12.8 pt`, strictly Figure Name + Characterization Type (`"图 a：TGA 热重失重曲线"`, `"图 d & 图 e：表面 SEM 形貌与厚度测定"`). **Strictly ban `【...】` conclusion slogans.**
  - Body lines: `PP_ALIGN.CENTER`, Regular `#222222`, `9.6–10.5 pt`, 1–2 crisp factual lines anchored to visible image metrics.

### Ending Slide (`prs.slides[-1]`, `LAYOUT_ENDING`)
- Centered textbox: `Inches(3.22, 2.70, 6.90, 2.0)`.
- Line 1: `"THANKS!"` — `PP_ALIGN.CENTER`, `Arial 58 pt Bold #9C1D22`, XML explicitly locking `<a:latin typeface="Arial"/>`, `<a:cs typeface="Arial"/>`, `<a:ea typeface="微软雅黑"/>`.
- Line 2: `"汇报人：<姓名>   |   <YYYY年MM月DD日>"` — `PP_ALIGN.CENTER`, `16 pt #555555`.
- **Forbidden:** `"敬请各位老师、师兄师姐批评指正！"` or extra decorative boxes.

## 4. Mandatory Helper Patterns

```python
def add_picture_fit(slide, img_path, left, top, max_w, max_h, center_h=True, center_v=True):
    with Image.open(img_path) as img:
        w_px, h_px = img.size
    aspect = w_px / h_px
    if (max_w / max_h) > aspect:
        h = max_h
        w = h * aspect
    else:
        w = max_w
        h = w / aspect
    actual_left = left + (max_w - w) / 2 if center_h else left
    actual_top = top + (max_h - h) / 2 if center_v else top
    return slide.shapes.add_picture(img_path, int(actual_left), int(actual_top), width=int(w), height=int(h))
```

- Maintain a `fix_chemistry()` Unicode subscript/superscript pass (`₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ₐ`) across chemical formulas (`CO₂`, `Li₃N`, `Li₂CO₃`, `LiPF₆`), ions (`Li⁺`, `TFSI⁻`), inverse units (`mS cm⁻¹`, `mAh g⁻¹`, `mA cm⁻²`), exponents (`10⁻⁴`), and descriptors (`Eₐ`, `tLi⁺`).
