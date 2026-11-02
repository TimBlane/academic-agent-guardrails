# 支柱六：顶刊科研图表坐标系与材料物性绘图规范

## 痛点背景
大语言模型在生成科研数据图表（Matplotlib/Seaborn/SVG）时，经常表现出缺乏顶刊（Nature / Science / Advanced Materials / ACS / Wiley）排版直觉的问题：
1. **坐标系粗糙**：默认使用仅左下两条脊线的半开框，刻度朝外，线宽单薄，毫无顶刊分量感；
2. **擅自脑补样品配方**：将用户原始数据中的 `Sample 1, Sample 2, Control` 擅自脑补替换为推测的化学配方名称，造成灾难性篡改；
3. **专业图谱反向绘制**：将高分子结晶熔融（DSC）吸热峰画成尖锐向上的凸峰（违反 Exo Up 惯例），或红外（FTIR）图例盖住官能团特征峰；
4. **SVG 文本碎片化**：导出 SVG 时因 LaTeX `$...$` 公式导致单个词汇被拆散为数十个零碎的 `<tspan>` 标签，无法在 Adobe Illustrator 中二次编辑；
5. **低效反复重绘**：微调一个子图时全量重新编译整个多面板大图，极度浪费等待时间与 Token。

---

## 核心科研绘图规范

### 1. 顶刊四面全封闭框线规范（Four-Sided Box Frame Standards）
- **全封闭四面框线**：顶部（Top）、底部（Bottom）、左侧（Left）、右侧（Right）四面坐标轴脊线必须全部显式开启（`axes.spines.top/right/bottom/left = True`），线宽统一采用 $2.5 \sim 3.0\ \mathrm{pt}$ 纯黑粗线；
- **上右无标尺，纯线包围（No Ticks on Top & Right）**：
  - 上框线与右框线仅保留边框线，**绝不添加标尺刻度线**（显式设置 `xtick.top = False`, `ytick.right = False` 及 `ax.tick_params(top=False, right=False)`）；
- **下左朝内刻度（Inward Ticks）**：
  - 刻度线严格仅保留在底部（X 轴）与左侧（Y 轴），方向一律**朝内（`tick.direction: in`）**，主刻度线宽 $2.5 \sim 3.0\ \mathrm{pt}$、长度 $8 \sim 9\ \mathrm{pt}$，严禁朝外散开。

### 2. 实验样品命名“严禁臆造与强加”（No Unsolicited Sample Renaming）
- 当用户提供原始数据（如 Excel 表格列名为 `Sample 1`, `Sample 2`, `Control`, `A`, `B`）时，**绝对只能使用用户原始指定的代号**；
- 坚决杜绝根据经验泛化擅自更改样品名称；只有用户明确提供映射表时方可替换。

### 3. 学术引文与机理出处“零虚构”物理查证（Zero Hallucinated Citations）
- 严禁语言模型凭记忆捏造 DOI、作者、期刊名、卷期年份；
- 所有文献出处必须在本地物理 PDF 或真实数据库中 100% 验证，并标明精确图表编号（例如：*Adv. Energy Mater.* 2024, 14, 2303527, Figure 2f）。

### 4. 专业领域图谱规范（DSC / FTIR / LSV）
- **差示扫描量热（DSC）**：
  - Y 轴标签标准化为 **`Heat Flow (a.u.)`**，隐藏无物理意义的绝对数字刻度；
  - 遵循放热朝上（Exo Up）学术惯例，高分子熔融吸热表现为**向下凹陷的波谷（Troughs）**；
  - $T_\mathrm{g}$ 与 $T_\mathrm{m}$ 在曲线上直接通过同色虚线短箭头引出标注（如 `Tg = -18.6 °C`, `Tm = 56.6 °C`）；
  - 多曲线堆叠必须设置足够大的基线偏移（Offset $\ge 1.0\ \mathrm{a.u.}$），防止曲线重叠碰撞。
- **红外光谱（FTIR）**：
  - Y 轴隐去刻度数值，仅保留 `Transmittance (%, Offset)`；
  - 图例放置在 $1800 \sim 2600\ \mathrm{cm^{-1}}$ 的纯净基线空白窗口，特征吸收峰上方标注规范化学式（如 $\mathrm{TFSI}^-$、$\mathrm{C=O}$）。
- **线性扫描伏安（LSV）**：
  - 在起翘拐点处通过虚线箭头标出氧化分解电位（如 `4.15 V`）；合理截取坐标轴，裁剪掉极化异常假象。

### 5. 矢量图 SVG 文本完整性与零 `<tspan>`（Zero `<tspan>` Protocol）
- 优先使用干净纯文本与通用 Unicode 符号（如 `°C`, `⁻¹`, `⁺`, `₂`），保证 SVG 中每个标注为单一独立的 `<text>` 标签，`<tspan>` 数量严格为 0；
- 导出后对 SVG 执行正则置换，将任何残留的 `STIXGeneral`、`DejaVu Sans` 规范化为学术标准 `Times New Roman`。

### 6. 解耦分流迭代原则（Decoupled Iteration Workflow）
- 单图独立编译、极速反馈验证、最终定稿再组装，严禁微调单图时全量重新跑大型组合图。
