# Reader, Source Map & Audit Suite Specification

Canonical workspace format rules extracted from former Rule 21 and verified production builds under `<project_root>/papers/`.

## 1. Required Deliverables per Analyzed Paper (`<paper_dir>/`)
1. `raw_paper_text.txt` & `si_raw_text.txt` — physical text extracted directly via `pymupdf`.
2. `assets/` — extracted high-resolution PNG figures (all main figures `fig_1..` and all SI figures `fig_s1..`).
3. `paper.md` — full-coverage bilingual academic reader (Main Text + Methods + Supporting Information + Back Matter; never truncated or degraded into a summary).
4. `source_map.json` — synchronized machine-readable index for downstream HTML tours, search, and verification.
5. `ground_truth_audit_report.md` — three-way cross-verified quantitative audit table (`value`, `page/line`, `figure/table`, `status`), errata section, and peer-review hedging boundaries.
6. `translation_notes.md` — terminology localization choices + enumerated `**E1**, **E2**, ...` source errata ledger.
7. Optional: `paper_xray.md` (mechanics/claims/load-bearing vs decoration/worked micro-examples) and `validate_reader.py`.

## 2. `paper.md` Structure & Formatting Contract
- **Header & Terminology Ledger:** Paper EN/ZH titles, journal, DOI, authors with affiliations/corresponding markers, plus a Markdown table (`英文专业术语 | 标准中文翻译 | 化学式/缩写 | 物理意义`).
- **Complete Table of Contents:** Hierarchical links to every `#section-*`, `#Sxxx`, `#Fxxx`, `#FSxxx`, `#Exxx`, `#TSxxx`.
- **Standard Anchors:**
  - Title/authors: `<a id="S001_TITLE"></a>`
  - Text blocks: `<a id="S001"></a>` ... `<a id="Sxxx"></a>`
  - Main figures: `<a id="F001"></a>` ...; Supplementary figures: `<a id="FS001"></a>` ...
  - Equations: `<a id="E001"></a>` ...; Tables: `<a id="TS001"></a>` ...
- **Paired Bilingual Block Pattern:**
  - Every paragraph starts verbatim with `> **Original Text:**` matching `raw_paper_text.txt` word-for-word, followed by `**【中文翻译与学术精读】**`.
- **Paired Figure Cards:** Embed high-res `assets/` image(s) (embed **all** panels of multi-part SI figures together), bilingual caption, and `💡 顶刊深度导读与数据核验`.
- **Equations & Notation:** Standalone numbered block equations in `$$...$$`; chemistry and units cleanly rendered in LaTeX (`$t_{\mathrm{Li}^+}$`, `$\mathrm{mS\ cm^{-1}}$`), honoring `Times New Roman` (Latin/digits) & `微软雅黑` (Chinese) separation where styled.

## 3. `source_map.json` Schema Contract
Validate via `json.load()`. Required top-level keys:
```json
{
  "paper_metadata": {
    "title_en": "...",
    "title_zh": "...",
    "journal": "...",
    "volume_issue": "...",
    "doi": "...",
    "published_online": "YYYY-MM-DD",
    "authors": [{"name": "...", "affiliation": "...", "role": "..."}]
  },
  "blocks": {
    "S001_TITLE": {"page": 1, "type": "heading", "refs": [], "original_excerpt": "..."},
    "S001": {"page": 1, "type": "paragraph", "refs": [], "original_excerpt": "..."}
  },
  "figures": {"F001": {"page": 1, "image_path": "assets/...", "caption_en": "...", "caption_zh": "...", "analysis": "..."}},
  "supplementary_figures": {"FS001": {"page": 1, "image_path": "assets/...", "caption_en": "...", "caption_zh": "..."}},
  "supplementary_tables": {"TS001": {"page": 1, "title_en": "...", "title_zh": "..."}},
  "equations": {"E001": {"page": 1, "latex": "...", "meaning_en": "...", "meaning_zh": "..."}}
}
```
*(When one SI figure contains multiple images, store `"image_paths": [...]` alongside or instead of a single `"image_path"` so every sub-image stays indexed.)*
