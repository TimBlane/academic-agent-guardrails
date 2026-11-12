# 支柱二：零幻觉物理文本溯源与“先图后文”协议 (Source Truth Protocol)

## 痛点背景
大语言模型在阅读英文论文或提取实验数据时，极容易出现**幻觉性泛化**：
- 凭借模糊印象或概率预测脑补参数（如把轴顶刻度当成峰高，或编造“300 °C 零失重”）；
- 伪造带 `Original` 引号的英文段落；
- 搞反 `⁷Li NMR` 化学位移方向，或把主图多子图拆散冒充其他图号；
- 修改了一处错误后，只在对话里道歉而未同步修正 `paper.md`、`source_map.json` 与 PPT。

---

## 零幻觉闭环工作流 (`paper-bilingual-reader`)

### 第一步：物理原文硬提取 (Physical Extraction)
- 在分析任何文献前，必须使用 `pymupdf`（`fitz`）将原版 PDF 正文与 Supporting Information（SI）提取为 `raw_paper_text.txt` 与 `si_raw_text.txt`；
- **原话检验红线**：所有标注为原文英文的引述，必须能在物理提取文本中逐字检索命中（Exact Match）。未命中一律视为幻觉；
- **Raw-String 转义保护**：Python 脚本生成含 LaTeX / 公式的 Markdown 时**一律使用原始字符串 `r"""..."""`**，防止 `\approx`、`\alpha`、`\text` 退化为控制字符 `\x07` 或 `\t`。

### 第二步：先看裁剪实图、再落笔“三度交叉核验”
引用任何曲线或微观图像前，必须先查看实际图片（含配对 SI 子图）：
1. **坐标轴与物理方向核准**：
   - 分清横/纵轴物理量、单位、虚线分界，严格区分**坐标轴顶格刻度 vs 曲线真实峰值**（顶格 `800` 不等于峰高 `800`；曲线未到零失重不准编造“零失重”）；
   - **⁷Li NMR 化学/物理方向**：`ppm` 增大 = **低场位移 / 去屏蔽（Downfield / Deshielding）**，绝对禁止反向误判为高场位移；
   - 分清双轴柱状图 vs 雷达图、独立红外热成像色标边界、CV 扫描区间端点与表面/截面 SEM 视角。
2. **背底相对论与连续谱客观性**：
   - **XPS / FTIR 信号强弱**：被基体极强峰压制的解卷积小峰禁称“极其强烈”，需如实说明相对强度并提示结合 ToF-SIMS 等纵深表征；
   - **3D 成像与点云密度**：如 ToF-SIMS 三维分布仅能反映密度分布或连续渐变（梯度变化），严禁夸大为“几乎完全透明 / 彻底清零”。
3. **正文与图注互锁纠偏**：
   - 客观检出并记录原文常见勘误（如热力学焓变单位量级错、$T_{\mathrm{g}}$/$T_{\mathrm{m}}$ 互换、Peak O/R 图文互反）；
   - 一旦在任意工件检出错误，必须**全链路闭环同步修正**关联的 `paper.md`、`source_map.json` 与汇报 PPTX。

### 第三步：门禁审计与交付 (`audit_markdown_suite.py`)
- 对精读套件（含 `ground_truth_audit_report.md`、`paper.md`、`source_map.json`）执行自动化门禁校验，确认**退出码为 0** 后方可交付：
  ```bash
  .venv/Scripts/python.exe skills/paper-bilingual-reader/scripts/audit_markdown_suite.py \
    --dir papers/<paper_id> --check-images --check-math --check-json
  ```
