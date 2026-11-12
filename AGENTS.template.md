# AGENTS.md

This file defines mandatory workspace rules for all AI coding assistants (`Google Antigravity`, `Claude Code`, `Codex`, `Copilot`, `Cursor`) working in `<project_root>`.

## Project Overview & General Guidelines
- **Repository:** `<your_repository_name>` | **Working Directory:** `<project_root>`
- Keep changes focused and modular; preserve existing comments/docstrings outside task scope.
- Never commit secrets, credential tokens, or environment artifacts (`.venv*/`, caches).
- Verify scripts, builds, and visual deliverables before claiming completion.
- **Volume Hard-Cap (`<= 22,000` bytes):** Antigravity caps single rule files at `24,000` bytes and truncates overflow lines. Keep this file **permanently `<= 22,000` bytes** (target `11–15 KB`). Domain templates, plotting specs, schemas, and checklists belong in `.agents/skills/`, never back in `AGENTS.md`.

---

## 第 0 层：跨任务全局高压红线（Rules 1–7）

### Rule 1｜代码、脚本与资产持久化规范（Multi-Agent 透明准则）
- **严禁将业务代码、绘图脚本或构建工具遗留在外部临时目录**（如 AppData 或 `.gemini/antigravity/brain/...`）。
- 所有可执行代码与工作流资产必须持久化保存在 `<project_root>/` 内部并纳入版本控制：
  1. 通用工具脚本 -> `<project_root>/scripts/`（如 `scripts/export_slides.ps1`、`scripts/pub_style.py`）；
  2. 论文专属脚本与产物 -> `<project_root>/papers/<paper_id>/`；
  3. 汇报脚本与成品 -> `<project_root>/presentations/`；
  4. 工作区专属技能 -> `<project_root>/.agents/skills/<skill_name>/`。

### Rule 2｜运行环境、`uv` 隔离与终端执行准则
- **WSL-First 与 Direct Bypass Sandbox**：检测到 WSL 时，日常指令、文件检索与脚本运行首选 WSL（`<wsl_project_root>`）；经用户授权直接采用绕过沙盒模式执行涉及 WSL/宿主的终端命令，禁止无意义的先期沙盒试探。
- **PowerShell 唯一例外**：除调用 Windows 独占接口（如本地 PowerPoint COM 接口执行独立 `.ps1` 导出幻灯片）外，坚决不使用 PowerShell 指令。
- **File-First 独立脚本落地**：严禁在命令行用 `python -c "..."`、`powershell -Command "..."` 或复杂引号拼接运行业务/数据处理逻辑，必须先写入独立 `.py` / `.sh` 文件再执行。
- **编码与跨平台 Git**：Python 文件读写一律显式声明 `encoding='utf-8'`，控制台建议执行 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`；WSL 内配置 `core.filemode false` 与 `core.autocrlf true`，`.gitignore` 永久包含 `.venv*/`。
- **虚拟环境与 `uv` 强隔离**：
  - 唯一合法解释器：Windows 使用 `.venv\Scripts\python.exe`；WSL 使用 `<wsl_project_root>/.venv-linux/bin/python`；**严禁向宿主机全局 Python 安装任何包**。
  - 依赖管理使用 `uv pip install <pkg>` 并同步更新根目录 `requirements.txt`（重建命令：`uv venv --clear --python 3.12 && uv pip install -r requirements.txt`）。
  - 关键脚本应在 `main()` 或入口检查虚拟环境：若 `sys.prefix == sys.base_prefix` 则抛出 `RuntimeError` 阻断运行。

### Rule 3｜学术零幻觉溯源、先图后文与反夸大铁律（Anti-Hallucination & Peer-Review Protocol）
- **物理原文硬提取为第一步**：分析任何文献前，必先使用 `pymupdf`（`fitz`）提取正文 `raw_paper_text.txt` 与支持信息 `si_raw_text.txt`。所有标为原文英文的引文必须能在物理文本中逐字检索命中；严禁凭记忆捏造原话、参数或测试项目。
- **先看裁剪实图、核准标尺再落笔**：引用任何曲线或图像前，必须亲自查看实际图片（含配对 SI 图片），执行三度交叉核验：
  1. **坐标轴与刻度**：分清横/纵轴物理量、单位、虚线分界及**坐标轴顶格刻度 vs 曲线真实峰值**（如轴顶 `800` 不等于峰高 `800`；曲线未到零失重不准编“300 °C 零失重”）；
  2. **化学/物理方向**：准确辨别图型（如双轴柱状图 vs 雷达图）、独立色标边界，以及 **`⁷Li NMR` 位移方向（`ppm` 增大 = 低场 / 去屏蔽，绝非高场位移）**；
  3. **正文与图注互锁**：检出并客观记录原文笔误/矛盾（单位量级错、`Tg`/`Tm` 混淆、`Peak O/R` 图文互反等），科普或口头讲解同样严禁把单张主图多子图拆散冒充其他图号。
- **严禁盲信二级底稿 & 全链路同步纠偏**：复用既有 `ground_truth_audit_report.md`、`paper_xray.md` 或 `paper.md` 制作 PPT/答疑前，必须对照原文与原图抽核关键数字；一旦在任意工件发现事实错误，**严禁仅在对话中口头道歉**，必须同步修正全部关联文件并重跑校验脚本清零。
- **严禁营销夸大、臆造比喻、未测感官与二元极端化**：
  - 禁用商业/夸张词（如“军工级”、“工业级”、“神级”、“颠覆性”、“革命性”、“顶尖”、“第一梯队”、“彻底杜绝”、“彻底终止”、“断崖式”、“白炽”、“暴力”）；
  - 禁用原文无物理依据的类比修辞（如“避雷针效应”、“活塞式”）；
  - 禁用未经仪器实测的感官套话（无声学计禁写“无爆鸣”、无烟气仪禁写“无发烟”、禁臆造“离火即熄/万无一失/零失重/零恶化/零积累”）；
  - 微观表征严守**背底相对论**（被基体强峰压制的解卷积小峰禁称“极其强烈”，需如实说明相对强度并提示结合 ToF-SIMS 等纵深表征）与**连续谱客观性**（3D 点云稀疏/色调变浅禁夸大为“几乎完全透明/彻底清零”）；汇报遵循**屏幕肉眼所见优先于机理诠释**。

### Rule 4｜实验样品命名保真与引文零虚构准则
- **严禁擅自更改用户样品命名**：当原始数据或表格列名为 `Sample 1–4` 等未命名代号时，**绝对只能使用原始代号**；严禁依据行业经验或文献擅自替换为特定化学配方（如 `<Formula-A>`/`<Formula-B>`），仅在用户明确提供映射表后方可更新。
- **学术引文与机理出处零虚构**：凡陈述机理依据或作图惯例来源，所引文献必须 100% 在本地 `papers/` PDF 或实测联网文献中物理存在，并准确标出期刊、年份、DOI 与图号；严禁凭记忆拼凑文献或图号。

### Rule 5｜中西文双字体、严格上下标与脚本转义规范
- **双字体分离**：除封面页（`Slide 0`）与致谢尾页（`Slide -1`）外，正文与图表中的英文字母/数字/公式符号统一使用 `Times New Roman`，中文统一使用 `微软雅黑`（PPTX 底层 XML 显式声明 `<a:latin typeface="Times New Roman"/>` 与 `<a:ea typeface="微软雅黑"/>`；全局字体遍历后处理必须显式豁免 `Slide 0` 与 `Slide -1`）。
- **化学式与物理量上下标零平铺**：所有化学式（$\mathrm{CO_2}$、$\mathrm{Li_3N}$、$\mathrm{Li_2CO_3}$、$\mathrm{LiPF_6}$）、离子电荷（$\mathrm{Li}^+$、$\mathrm{TFSI}^-$）、科学记数法（$10^{-4}$）、反比单位（$\mathrm{cm}^{-1}$、$\mathrm{mAh\ g^{-1}}$）及物理量角标（$E_{\mathrm{a}}$、$t_{\mathrm{Li}^+}$）必须严格标出上下标，交付前执行正则扫描清零。
- **原始字符串防转义损坏**：生成含 LaTeX / 公式的 Markdown 或源代码的 Python 脚本**一律使用原始字符串 `r"""..."""`**，杜绝 `\t`（`\text`）、`\x07`（`\approx` / `\alpha`）导致不可见控制字符或残缺命令。

### Rule 6｜学术汇报 PPTX 通用禁令与用户资产保护
- **用户定稿物理只读红线**：一旦用户表明现有 `.pptx` 已定稿或指示“不要动我的 PPT”，该文件立即降级为物理只读，**严禁调用任何脚本覆写既有版式或内容**，AI 仅可执行只读检查并输出修改建议或独立备忘录。
- **交付前 COM 导出视觉自审**：生成 PPTX 后，必须运行 [`scripts/export_slides.ps1`](scripts/export_slides.ps1) 调用本地 PowerPoint COM 导出全部幻灯片 PNG，并亲自用图片查看工具逐页核验零溢出、零遮挡、零重叠后方可交付。
- **图片原比例锁与防御性卡片**：插图必保真实像素宽高比（禁同时硬定不一致的宽高导致拉伸）；文本卡片优先采用平直纯白矩形（`MSO_SHAPE.RECTANGLE`，微灰边框 `#CFD8DC`）、顶部垂直对齐（`MSO_ANCHOR.TOP`），底部预留 `20%–30%` 呼吸留白。
- **去提取标签与组会小标题体例**：标题、卡片与备注严禁出现 `(Figure 4a-c)` 等内部资产编号；正文导向使用屏幕方位（如“左上图 a”），严禁跨页引用幽灵子图；实验室组会数据页**禁用顶部 `21 pt` 结论横幅与 `【结论短句】`**，右侧统一使用居中加粗 `图 X：表征/测试名称` 小标题 + 精炼短事实行。
- **封面/尾页几何定制与屏幕-备注物理隔离**：封面汇报人及日期须严丝合缝水平居中（`left = (slide_width - width) / 2`, `PP_ALIGN.CENTER`）；致谢尾页仅保留居中 `THANKS!`（`Arial Bold 58 pt #9C1D22`）与汇报人时间，**严禁添加“敬请各位老师、师兄师姐批评指正！”**；PPT 屏幕仅写当前画面可见物理量，未放主图的支持信息（SI）数据与深层机理解析物理隔离至 Speaker Notes。

### Rule 7｜工作区 Skill 强制路由表（Workspace > Built-in）
执行以下三类专项任务前，**必须先读取对应工作区 Skill**，以其阻塞流程、参考细则和退出码门禁脚本为准（优先级高于全局与通用插件默认模板）：

| 任务类型 | 必加载工作区 Skill | 核心门禁脚本 |
| :--- | :--- | :--- |
| **组会 / 文献汇报 PPTX 制作、修改或审计** | [`group-meeting-pptx`](skills/group-meeting-pptx/SKILL.md) | `scripts/verify_group_pptx.py` + `scripts/export_slides.ps1` |
| **科研数据绘图（DSC/FTIR/LSV/长循环/双Y轴）、SVG 导出与 3D 机理图** | [`scientific-plotting-svg`](skills/scientific-plotting-svg/SKILL.md) | `scripts/audit_svg_postprocess.py` |
| **论文物理原文提取、双语对照精读（`paper.md` + `source_map.json`）、X-Ray 与全链路审计纠偏** | [`paper-bilingual-reader`](skills/paper-bilingual-reader/SKILL.md) | `scripts/audit_markdown_suite.py` |
