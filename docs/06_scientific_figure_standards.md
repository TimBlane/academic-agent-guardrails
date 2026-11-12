# 支柱六：顶刊科研绘图、共享样式基线与零 `<tspan>` SVG 规范 (`scientific-plotting-svg`)

## 痛点背景
LLM 生成科研图表时常见五大顽疾：半开放细框朝外刻度、擅自把 `Sample 1–4` 猜改成具体配方、Dual-Y 柱状/折线互相压盖导致 CE 标签撞车、Matplotlib mathtext 把单位切碎成几十个 `<tspan>` 导致 AI/CorelDRAW 无法编辑，以及改一张子图却全量重绘整张组图。

---

## 核心绘图与矢量导出规范

### 1. 共享基线 `scripts/pub_style.py` 与四面全封闭框线
所有数据绘图脚本必须导入共享工具 [`scripts/pub_style.py`](../scripts/pub_style.py)（提供 `set_pub_style()`、`safe_save_clean()`、`annotate_curve_point()`）：
- **四面纯黑全封闭框线**：顶部、底部、左侧、右侧 Spine 全部显式开启，线宽加粗至 **`3.0–4.0 pt`**（或按刊物统一 `2.5–3.0 pt`）纯黑实线；
- **上右无标尺、下左朝内刻度**：严格关闭顶部与右侧刻度线（`xtick.top = False`, `ytick.right = False`），底部与左侧主刻度朝内（`tick.direction: in`）。

### 2. 电化学与热分析领域专有规范
- **DSC（差示扫描量热）**：Y 轴 `Heat Flow (a.u.)`，隐藏无意义数字刻度；遵循 **Exo Up（吸热波谷向下）**；虚线短箭头标注 $T_{\mathrm{g}}$ / $T_{\mathrm{m}}$，多曲线设置大基线偏移（`>= 1.0 a.u.`）避免碰撞；
- **FTIR（红外光谱）**：Y 轴 `Transmittance (%, Offset)` 且隐去数字刻度；图例置入 `1800–2600 cm⁻¹` 无特征峰空白基线窗，特征峰上方标注规范化学式；
- **LSV（线性扫描伏安）**：拐点虚线箭头直接标出分解电位，裁剪极化异常区间；
- **Full-Cell 双 Y 轴与 CE 解耦策略**：
  - *场景 A（突出单一优胜样，如 Champion-Sample）*：在主容量区突出显示优胜样红色高对比曲线（`#C53030`）；
  - *场景 B（平行对照全库仑效率）*：弱化非核心曲线为 Slate Gray（`#64748B`），避免彩线混战；
  - 始终在左 Y 轴容量上限与右 Y 轴库仑效率（`98%–101%`）之间保留 **`>= 20–25 mAh g⁻¹` 垂直气隙（Air Gap）**，禁止双轴曲线交缠撞字；
- **对称电池（`Li||Li`）局部放大插图（Inset）**：
  - 截取 **`10–20 h`** 稳态局部时间窗口放大；在主曲线上界与放大框之间保留 **`>= 0.05 V` 垂直安全间距**，避免框线压字。

### 3. 零 `<tspan>` 矢量 SVG 与退出码 `0` 门禁
- 全局配置 `svg.fonttype = 'none'` 与 `pdf.fonttype = 42`；优先使用洁净 Unicode（`°C`、`⁻¹`、`⁺`、`₂`）替代复杂 `$...$`，保证输出矢量文字为独立可编辑 `<text>`，**`<tspan>` 数量严格等于 0**；
- 导出后运行后处理门禁脚本，自动把残留 `STIXGeneral` / `DejaVu` 替换为 `Times New Roman` 并校验零 `<tspan>`（退出码 `0`）：
  ```bash
  .venv/Scripts/python.exe skills/scientific-plotting-svg/scripts/audit_svg_postprocess.py figure.svg --fix
  ```

### 4. 解耦单图迭代 & 数据图 vs. 3D 机理图分工
- **单图独立构建**：绝不在调参时重跑整张组合大图；单图验证达标后再组版；
- **数据图 vs. 3D 示意图**：实验数据图必须采用真实数据坐标绘图；3D 核壳/溶剂化/机制示意图使用专业扩散或 3D 工具生成，并持久化保存所用 Prompt 至 `papers/<paper_id>/3d_prompts.md`。
