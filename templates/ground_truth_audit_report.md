# 《<Paper Title Here>》
## 零幻觉物理溯源与真实数据审计报告 (Ground Truth Audit Report)

**审计基准文献**：<Journal, Year, Volume, Pages, DOI>  
**提取物理原文文件**：`raw_paper_text.txt` (<Character Count> 字符，共 <Page Count> 页)  
**执行规范**：严格遵循 `AGENTS.md` 零幻觉物理溯源铁律（Rule 9/10）与化学式/科学记数法上下标规范（Rule 8）

---

### 一、 核心实验与物性参数逐项物理溯源表

| 序号 | 物理量 / 参数名称 | 论文实测数值 | 物理量单位 | 对应体系 / 样品 | 原文 PDF 物理定位 (页码/段落/图表) | 审计核验状态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 关键性能指标 A | 例如 $1.63 \times 10^{-4}$ | $\mathrm{S\ cm^{-1}}$ | Sample-A (实验组) | Page 1 (Abstract); Page 4 (Sec 2.2); Figure 2b | 完全吻合 |
| 2 | 对照指标 B | 例如 $1.25 \times 10^{-4}$ | $\mathrm{S\ cm^{-1}}$ | Sample-B (对照组) | Page 2 (Intro); Figure 2b | 完全吻合 |
| 3 | 活化能 $E_{\mathrm{a}}$ | 例如 2.11 | $\mathrm{kJ\ mol^{-1}}$ | Sample-A (MD 计算) | Page 4 (Sec 2.2); Figure S9 | 完全吻合 |
| 4 | 循环保持率 | 95.3% (200 圈) | % | Full Cell (2 C) | Page 8 (Sec 2.4); Figure 4b | 完全吻合 |

---

### 二、 图表坐标轴、量纲与图例三度交叉核验

1. **坐标轴极值与物理量单位核准**：
   - 曲线图 X 轴物理量：`[Cycle Number / Capacity / Voltage / Time]`，单位：`[圈 / mAh g^-1 / V / h]`；
   - 曲线图 Y 轴物理量：`[Specific Capacity / Overpotential / Retention]`，单位：`[mAh g^-1 / mV / %]`；
   - *核验结论*：横纵轴量纲与实测曲线完全互锁，无张冠李戴。

2. **图例与颜色曲线严格对应**：
   - 黑色曲线：Sample-A（实验组）；
   - 红色曲线：Sample-B（对照组）；
   - 蓝色虚线：基准空白样；
   - *核验结论*：图文阐述中颜色/样品对应关系 100% 正确。

3. **正文描述与图表标注 100% 互锁**：
   - 正文声明的数值必须在图表曲线或数据表中精准出现；
   - 严禁将全电池库仑效率（如 99.8%）误述为孔隙率，严禁将核磁峰形宽化（broadened）反向写为变窄。

---

### 三、 异常与偏差审计记录 (Findings & Discrepancies)

- **偏差项 1 (若有)**：
  - *原文表述差异*：摘要中标注为 A，正文/图表标注为 B；
  - *原因分析*：例如统计基准不同（第 1 圈 vs 第 5 圈激活后算起）；
  - *汇报采信建议*：在汇报幻灯片中采信图表实测值，并在演播备忘录（Speaker Notes）中注明口头说明。

---

### 四、 审计人签核 (Sign-off)

- **物理文本提取比对状态**：已完成（通过 `pymupdf` 硬提取比对）
- **交付准入结论**：PASS（全部数据可追溯，零幻觉）
