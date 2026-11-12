---
name: paper-bilingual-reader
description: >-
  Extract physical PDF/SI text and figures, perform source-grounded
  verification, build synchronized paper.md + source_map.json + audit suites,
  and run cross-file error remediation. Use for 论文精读、中英对照、全文翻译、
  paper.md、source_map.json、Paper X-Ray 与审计纠偏闭环.
---

# Paper Bilingual Reader & Audit Suite

Workspace standard for lossless bilingual readers and full-chain source grounding in `<project_root>`.

## Task Scope Routing

- **Single Question or Excerpt:** Inspect only the relevant extracted `raw_paper_text.txt`, `si_raw_text.txt`, and corresponding high-res figure PNGs; verify numerical accuracy against [references/audit-pitfalls-and-errata.md](./references/audit-pitfalls-and-errata.md) without forcing a full rebuild. Even casual or "plain-language" explanations must keep true figure IDs and SI distinctions intact.
- **Full Paper Reader / Translation / Audit:** Always deliver both synchronized `paper.md` and `source_map.json` alongside supporting audit files via all 5 blocking steps below.

## Resource Map

| Resource | Purpose |
| :--- | :--- |
| [references/reader-and-sourcemap-spec.md](./references/reader-and-sourcemap-spec.md) | `paper.md` anchor/pair syntax, `source_map.json` schema, companion reports |
| [references/audit-pitfalls-and-errata.md](./references/audit-pitfalls-and-errata.md) | Unit typos, `Tg`/`Tm` swaps, NMR shifts, axis ceilings, `r"""..."""` rules |
| [scripts/audit_markdown_suite.py](./scripts/audit_markdown_suite.py) | Exit-`0` scanner for control chars, escapes, banned terms, `$`, JSON & images |

## Blocking 5-Step Protocol

### 1. Hard-Extract Physical Text and Visual Assets First
1. Never summarize or reconstruct English quotes from memory. Use `pymupdf` (`fitz`) under `.venv\Scripts\python.exe` to extract main `raw_paper_text.txt` and SI `si_raw_text.txt`.
2. Export every main figure, **every SI figure** (`Fig. S1–SN`), and tables into `<paper_dir>/assets/`.

### 2. Visually Audit Every Figure & Paired SI Panel Before Writing
1. Inspect every main figure PNG **and all paired SI panel PNGs** via `read_file` before writing translations, deep analysis cards, or X-Ray conclusions.
2. When an SI figure spans multiple sub-images (e.g., `Fig. S2a` & `Fig. S2b`), embed **all panel images** together — never only panel 1.
3. Cross-check prose, captions, axes, and SI against [references/audit-pitfalls-and-errata.md](./references/audit-pitfalls-and-errata.md) to flag unit typos (`J mol⁻¹`), transition mislabels (`Tg` vs `Tm`), swapped fit values (`Fig. 4j Peak O/R`), cycle drift (`220` vs `230`), NMR direction (`ppm` increase = downfield), and matrix-background relativity.

### 3. Build Synchronized Dual Deliverables With Raw Strings
1. Any Python generator outputting Markdown/LaTeX **must use raw strings (`r"""..."""`)** so `\t` (`\text`) and `\x07` (`\approx`, `\alpha`) never corrupt source.
2. Produce the synchronized deliverable suite defined in [references/reader-and-sourcemap-spec.md](./references/reader-and-sourcemap-spec.md):
   - `paper.md` (metadata, Terminology Ledger, TOC, unique `<a id="...">` anchors, verbatim `> **Original Text:**` + `**【中文翻译与学术精读】**` covering main + SI + back matter)
   - `source_map.json` (valid JSON indexing metadata, blocks, figures, SI figures/tables, equations)
   - `ground_truth_audit_report.md` (errata ledger, parameter traceability table, peer-review hedging)
   - `translation_notes.md` (terminology rationale + `**E1**..` source errata log)
   - Optional `paper_xray.md`, interactive HTML tour, and paper-specific completeness checker (`validate_reader.py`).

### 4. Dual Programmatic Verification Gate
Run any paper-specific structural validator plus the workspace audit scanner (must exit `0`):
```text
.venv\Scripts\python.exe skills/paper-bilingual-reader/scripts/audit_markdown_suite.py --dir "<paper_dir>" --check-json --check-images --check-math
```
Confirm zero control characters, zero broken LaTeX escapes, zero unexpected hype/unmeasured phrasing, balanced `$`, valid JSON, and 100% disk image existence.

### 5. Full-Chain Closed-Loop Remediation
When an error is spotted in any deliverable, **never stop after apologizing in chat**: update **every** linked file (`ground_truth_audit_report.md`, `paper_xray.md`, `paper.md`, `source_map.json`, `translation_notes.md`, interactive HTML) and re-run Step 4 to exit code `0`.

## Done Checklist
- `raw_paper_text.txt` + `si_raw_text.txt` extracted via `pymupdf`; English quotes match word-for-word
- Every main & paired SI PNG read visually before writing interpretations
- Synchronized `paper.md` + `source_map.json` + `ground_truth_audit_report.md` + `translation_notes.md`
- Both `validate_reader.py` (if present) and `audit_markdown_suite.py` exited `0` after final edit
