# AGENTS.md

This file provides context and guidelines for AI coding assistants (Google Antigravity, Codex, Copilot, etc.) working on this repository.

## Project Overview
- Repository: <your_repository_name>
- Working Directory: `<project_root>`

## General Guidelines
- Keep responses and changes focused and modular.
- Avoid committing sensitive data, secrets, or credential tokens.
- Follow modern best practices for code styling, documentation, and error handling.
- Verify changes with relevant tests or build steps before finalizing.

## 📂 代码与脚本组织规范（多 Agent 协作透明与持久化准则）
- **严禁将业务代码、绘图脚本、构建工具保存在外部临时沙盒中**（如 AppData 或 `.gemini/antigravity/brain/...`）。会话结束后此类目录不可见，其他 AI 助手（Claude Code、Copilot、Cursor 等）无法读取或修改。
- **所有生成的可执行代码必须持久化保存在 `<project_root>` 项目目录内部**：
  1. **通用工具脚本**：存放于 `<project_root>/scripts/`（如 `scripts/export_slides.ps1` 批量渲染工具等）；
  2. **论文专属绘图与分析脚本**：就近存放在对应论文目录下（如 `<project_root>/papers/<paper_id>/generate_ftir_svg.py`、`build_group_pptx.py`）；
  3. **汇报生成脚本**：就近保存在 `<project_root>/presentations/` 或对应课题目录下。
- **保证所有 Agent 均可透明感知、读取、调试和二次迭代**，并纳入 Git 版本控制。

---

## 🛑 学术汇报 PPTX 与科研绘图铁律规范（吸取深刻返工教训沉淀）

### 1. 交付前真机视觉自审原则（严禁将用户当测试员）
- **绝不允许代码编译通过就直接宣布“完成”**。
- 生成 PPTX 后，必须先调用本地 PowerPoint COM 接口或渲染脚本将每一页导出为高清 PNG 图片。
- Agent 自身必须调用图片查看工具对每一页进行**像素级肉眼复核**，确认无任何文本溢出、无任何卡片重叠、无任何图文遮挡后，方可向用户汇报交付。

### 2. 图文数据与子图字母 100% 对应原则
- 幻灯片上出现的每一个物理量、参数数值、时间范围、单位：
  - **必须以屏幕配图中的真实标记为最高准则**，严禁脱离配图凭泛化印象书写；
  - 严禁出现“图上标 Ea = 0.74 eV，文字写 0.38 eV”或“图上是 1500h 循环，文字写 600h”等前后割裂低级错误。
- 正文中引用的子图编号（如“左上图a”、“左中图b”），必须与当前页面展示的实际图片完全一致，严禁出现跨页引用的“幽灵子图”（如当前页只有 3D 模型，文字却写“图e、图f”）。

### 3. 学术汇报“去提取标签”原则
- **幻灯片标题绝不允许包含论文内部提取代号**：严禁出现 `(Figure 4a-c)`、`(Figure 2 & Fig. S4)`、`(Figure 1)` 等内部资产标签。
- 幻灯片标题必须是纯粹、专业的**科学命题或研究结论**（如“物相结构演化、多重氢键网络与力学性能表征”）。
- 正文与演播备忘录中的指引一律使用观众视角能够立即领会的**屏幕方位**（如“左上图a”、“右上图b”、“底图右一”）。

### 4. 科研矢量图（SVG）与 3D 概念机理图分工铁律
- **数据与表征曲线类（FTIR, XRD, DSC, XPS, 电化学循环等）**：
  - 必须使用 Python (Matplotlib / Seaborn) 基于真实数据绘制，严格使用标准 LaTeX 数学语法（`r'$\mathrm{cm^{-1}}$'`、`$\rightarrow$`、`$E_a$` 等），统一配置 `mathtext.fontset = 'dejavusans'`。
  - 导出时默认提供可编辑文本版与高保真矢量路径版 SVG，严禁生僻 Unicode 符号导致的乱码。
- **3D 科学机理与概念模型图（分子动力学、聚合物网络、离子跳跃、器件三维结构等）**：
  - **严禁使用简陋的 Matplotlib 3D 线框拼接**（效果粗糙且缺乏材质感）。
  - **一律使用系统高品质扩散生成工具（`generate_image`）** 直接渲染頂刊级（Nature/AENM 水准）影视光影 3D 科学图（包含真实的次表面散射、晶体透明材质、柔性螺旋链与光晕粒子）。
  - 必须将调用的完整提示词（Prompt）和参数就近持久化记录在对应论文目录下，确保其他 Agent 可以复用或迭代提示词重新生成。

### 5. 防御性版式排版规范
- 文本容器优先采用标准的平直纯白矩形（`MSO_SHAPE.RECTANGLE`），边框统一微灰（`#CFD8DC`），严禁使用边界难以预测的圆角矩形。
- 文本框必须显式声明垂直顶部对齐（`tf.vertical_anchor = MSO_ANCHOR.TOP`），防止多行文字上下对称发散导致挤占图片。
- 容器必须保留至少 20%~30% 的纵向白边呼吸感，严禁文字填满卡片底部。

### 6. 科研写作与学术表述“严禁修饰性夸大与凭空创造”铁律（事实与学界公认最高准则）
- **严禁使用非学术、商业营销或修辞夸张词汇**：坚决杜绝在学术汇报、论文手稿、机理解读中凭空臆造如“军工级”、“革命性颠覆”、“神级表现”等未经验证、无学术界明确定义的通俗公关词汇。
- **事实与实验数据 100% 溯源**：每一句定性或定量描述（如安全性能、结构强度、电化学稳定性），必须在实验方法（具体标准测试如针刺、剪角、热箱等）和实测数据中有直接、确凿的证据支撑。
- **恪守同行评审（Peer Review）公认的严谨科学范式**：一律使用严谨、客观、克制的学术语言（如“展现出卓越的抗机械穿刺破坏与本征安全防护特性”，绝不写“军工级安全防护”）。在后续所有课题调研、论文撰写（CNS / Wiley / ACS / Elsevier 标准）与组会汇报中，无条件严格执行。

### 7. 学术汇报与图文排版字体规范（中西文双字体分离准则）
- **英文与数字一律采用 Times New Roman**：在 PPTX 幻灯片、图表标注、论文材料中，所有英文字母（专业术语、单位、化学式、缩写、变量符号如 $E_a$、$t_{\mathrm{Li}^+}$、$\mathrm{mAh/g}$、$\mathrm{S/cm}$、$\mathrm{NCM811}$ 等）及所有阿拉伯数字，一律统一使用学术界标准衬线字体 **Times New Roman**。
- **中文字体统一采用高辨识度黑体**：正文与标题汉字统一采用 **微软雅黑**（或思源黑体），确保学术汇报远距离投影清晰易读。
- **双字体独立映射机制**：生成 PPTX 时底层文本属性必须显式声明 `<a:latin typeface="Times New Roman"/>` 与 `<a:ea typeface="微软雅黑"/>`，保证英文字母与数字自动调用 Times New Roman、汉字自动调用微软雅黑，杜绝全篇混用单一中文字体渲染英文数字的不规范现象。

### 8. 科研汇报化学式与科学记数法上下标规范（严禁平铺直写）
- **化学式分子式下标必须规范**：所有化学式（如 $\mathrm{CO_2}$、$\mathrm{H_2CO_3}$、$\mathrm{Li_3N}$、$\mathrm{Li_2CO_3}$、$\mathrm{LiNi_{0.8}Co_{0.1}Mn_{0.1}O_2}$ 等）中的原子计量数必须严格使用下标（如 $\mathrm{CO_2}$ 绝不可写作 `CO2`，$\mathrm{H_2CO_3}$ 绝不可写作 `H2CO3`）。
- **离子带电荷数与上角标必须规范**：所有离子符号（如 $\mathrm{Li}^+$、$\mathrm{TFSI}^-$、$\mathrm{PF_6}^-$ 等）的电荷符号必须严格使用上标（如 $\mathrm{Li}^+$ 绝不可写作 `Li+`，$\mathrm{TFSI}^-$ 绝不可写作 `TFSI-`）。
- **物理量、科学记数法与复合单位指数必须规范**：
  - 数量级幂次：$10^{-4}$ 绝不可写作 `10^-4` 或 `10-4`；
  - 复合单位反比指数：$\mathrm{cm}^{-1}$ 绝不可写作 `cm-1` 或 `cm^-1`；
  - 物理量角标：活化能 $E_{\mathrm{a}}$ 下标 $a$、锂离子迁移数 $t_{\mathrm{Li}^+}$ 等必须准确标出下标与上标。
- **交付前专项检查**：PPT 生成或脚本编写完成后，必须执行专项目视自查或正则扫描，杜绝任何未标上下标的化学式流入最终交付材料。

### 9. 文献研读与数据采信“零幻觉物理溯源”铁律（Source Truth & Anti-Hallucination Protocol）
- **PDF 物理原文物理级硬提取为第一步**：
  - 在分析任何文献前，必须使用代码工具（如 `pymupdf`/`fitz`）将原版 PDF 全文及支持信息提取为物理文本（如 `raw_paper_text.txt`）；
  - 严禁任何语言模型凭记忆、泛化印象或“概括理解”来伪造标有 `Original` 的英文段落；所有标为原话的引文，必须能在 `raw_paper_text.txt` 中逐字精准检索命中。
- **图表数据“三度交叉核验”法则（严禁张冠李戴）**：
  1. **坐标轴极值与物理量单位核准**：引用曲线图时，必须首先核准横纵坐标轴的物理量名称、单位与坐标范围（例如：横坐标是 Cycle 还是 Capacity？终点是 50 还是 150？纵轴是 MPa 还是 GPa？单位是 $\mathrm{mAh/g}$ 还是 $\mathrm{mA/cm^2}$？）；严禁将纵坐标数值看串行为横坐标循环圈数；
  2. **图例与颜色曲线严格对应**：必须逐一对应实验组与对照组（如 Sample-A vs Sample-B（实验组 vs 对照组））在各个倍率、各个循环节点的实测数值，严禁凭经验混淆；
  3. **正文描述与图表标注 100% 互锁**：正文中的每一个定量陈述（如保持率、衰减率、初始容量），必须与图表真实曲线严格吻合；严禁将全电池库仑效率（如 99.8%）误植为气凝胶孔隙率，严禁将核磁峰形宽化（broadened）反向写为变窄。
- **数据留痕与强制交付审计报告**：
  - 任何针对论文生成的 PPTX、分析报告或卡片，必须同步在论文目录下生成 `ground_truth_audit_report.md`，列明汇报中出现的每一个关键参数在原文 PDF 中的具体页码、段落与图表编号；
  - 严禁在未经原文字对字核验的情况下向用户宣布“完成”。

### 10. 用户个性化版式定制永久保护原则（严禁脚本回滚覆盖用户设计）
- **致谢页（Ending Slide）规范**：遵循用户既定风格（如大写英文致谢、特定主题色）与汇报人/时间居中排版，**严禁私自添加非预设的冗余客套话**（如“敬请批评指正”等）。
- **封面页（Title Slide）居中几何约束**：汇报人姓名与汇报时间文本框必须显式设置水平居中几何约束（`left = (slide_width - width) / 2`，`alignment = PP_ALIGN.CENTER`），严禁继承模板中未对齐的偏差坐标，确保姓名与时间严丝合缝居中对齐。

### 11. 终端执行与代码运行防 Token 浪费准则（Windows 平台专属规范）
- **平台适用条件**：**本规范仅在 Windows 宿主平台下严格生效**（Linux / macOS 原生 POSIX 终端与全系统 UTF-8 环境直接使用系统默认 Bash 即可，不受此条款限制）。
- **独立脚本落地优先（File-First 原则）**：
  - **严禁**在命令行中通过 `python -c "..."` 或 `powershell -Command "..."` 内联拼接长篇、多行或带有复杂引号嵌套的代码；
  - 凡涉及文件抽取、正则处理、批量重命名、数据分析等逻辑，**必须先持久化写入独立的 `.py` 文件再调用执行**，从根源上杜绝 Windows 控制台因引号转义剥离、脚本块解析失败（`ParserError`）导致的重试与 Token 浪费。
- **Shell 工具职责明确分工**：
  - **Git Bash 优先（日常高频操作）**：通用文件检索（`grep`/`find`/`awk`/`sed`）、多命令串联（`&&`/`||`）、Git 版本控制、复杂文本管道流等，在 Windows 下优先调用 Git Bash（如 `bash -c "..."` 或运行 `.sh`），避开 Windows 原生 PowerShell 的别名劫持（如 `curl`、`cat`）与语法报错；
  - **PowerShell 专属保留（Windows COM 自动化）**：涉及 Windows 原生 COM 组件调用（如 `export_slides.ps1` 中的 PowerPoint COM 高清导图进行视觉自审）、系统底层接口交互，**必须且只能通过独立的 `.ps1` 文件由 PowerShell 执行**。
- **Python 编码与输出防御规范**：
  - 代码中所有文件 I/O 必须显式声明 UTF-8 编码：`open(..., encoding='utf-8')`；
  - 关键控制台输出建议在脚本开头配置防御性重定向：`sys.stdout.reconfigure(encoding='utf-8', errors='replace')`，确保即使遇到罕见生僻字符也以占位符平滑降级，绝不因 `UnicodeEncodeError` 中断核心执行流程。

---

### 12. 口头讲解与通俗科普“严禁泛化脑补”及“全链路闭环交付”铁律（深刻吸取真实学术汇报严重返工教训）
- **“讲通俗”绝不等于“胡编乱造”**：
  - 在向用户进行通俗、零基础科普或口头总结时，AI 助手极易退行回“泛化印象自由发挥”的恶习；
  - **严禁凭模糊记忆捏造图解归属**：绝不允许为了迁就通俗叙事，将一张主图的十几个子图拆散冒充其他图号（如把 Figure 4a-j 拆成图 3、4、5，把真正的图 3 和图 5 抹杀），绝不允许凭空臆造未在配图中出现的测试（如臆造图 1 有 TGA/原位质谱）；
  - 所有口头讲解涉及到的图片序号、子图字母、坐标轴物理量，必须像对待正式学术手稿一样，以提取好的物理文本（`raw_paper_text.txt`）和实际图片为唯一真理。
- **纠偏整改“全链路闭环”原则（严禁半吊子糊弄）**：
  - 当用户指出图解对不上或发现数据差错时，**绝不允许仅在对话框里发长篇道歉与口头辩解**；
  - 必须第一时间对所有交付工件执行全链路同步整改：包括正文 Markdown Reader（`paper.md`）、物理审计报告（`ground_truth_audit_report.md`）、交互导览网页（`interactive_paper_tour.html`）、结构映射文件（`source_map.json`）；
  - 必须重新运行本地验证工具（如 `validate_reader_math.py --strict`）确保零错误后，方可向用户汇报。
### 13. Python 虚拟环境与现代化 uv 工具链隔离铁律 (Virtual Environment & uv Protocol)
- **唯一合法解释器与包管理器**：
  - 本项目已全面升级为现代化的 `uv` 工具链管理；
  - 虚拟环境标准路径：`<project_root>/.venv`（基于独立的纯净 Python 3.12+，通过 `.gitignore` 严禁同步至版本库）；
  - Windows 环境下执行脚本显式调用解释器路径：`.venv\Scripts\python.exe` 或使用 `uv run`；
  - 依赖安装优先使用极速包管理：`uv pip install <package>`（亦完全兼容 `.venv\Scripts\pip.exe install`，严禁直接调用全局未隔离的 `pip`）。
- **零全局包污染红线**：
  - **严禁**将任何第三方库安装至宿主机用户全局 Python 目录（如 `AppData\Local\Python\...`）；
  - 任何 Agent（Google Antigravity、Claude Code、Codex、Copilot、Cursor）在执行命令时，必须确保执行上下文处于 `.venv`。
- **跨设备一秒恢复与依赖追踪准则**：
  - 一旦引入新的第三方依赖，**必须同步更新根目录 `requirements.txt`**（通过 `uv pip freeze > requirements.txt` 或显式追加）；
  - 换设备或新环境时，仅需执行 `uv venv --clear --python 3.12 && uv pip install -r requirements.txt`，即可在数秒内快速幂等重建环境。
- **脚本入口防呆与运行时自检**：
  - 关键自动化脚本建议在入口处加入防御断言：
    ```python
    import sys
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("[ENV ERROR] 检测到全局 Python 环境！必须使用 <project_root>/.venv 虚拟环境执行。")
    ```

---

### 14. 学术汇报防御性铁律：用户资产保护、量纲硬互锁与演播备忘录隔离规范 (Presentation & Audit Defense Protocol)
- **用户定稿绝对保护红线（User Final Authority Protocol）**：
  - 一旦用户声明“PPT 我已经做好了/不要改动任何内容”，该 PPTX 文件的写权限立即物理降级为只读（Read-Only）；
  - **严禁**调用任何自动化生成脚本对用户的既有版式、Logo 徽标、字体层级进行二次全量覆写；AI 仅保留只读审查、对比建议及独立备忘录输出权。
- **图表数据与坐标轴量纲硬互锁法则（Coordinate & Dimension Hard-Locking）**：
  - 引用任何曲线或图表时，必须先核准原图横纵坐标轴物理量与单位（横轴是圈数 Cycle 还是容量？纵轴是放电比容量 $\mathrm{mAh\ g^{-1}}$ 还是绝对容量 $\mathrm{mAh}$？）；
  - **严禁**凭模糊经验或行业套话脑补未在原文出现的物理量（如捏造 500 mAh 绝对容量、张冠李戴 30 °C 测试温度）；未在当前图表中明确展示的数据，绝不能在幻灯片对应图注中凭空写出。
- **屏幕正文与演播备忘录（Speaker Notes）物理隔离机制**：
  - **PPT 屏幕画面**：100% 只能展示当前屏幕配图中肉眼可见的物理量与精炼论断，文字简洁利落，保障投影仪大字距清晰可读，杜绝密密麻麻照着念；
  - **支持信息（SI）与机理延伸**（如 Supporting Information 中补充机理测试（如溶剂挥发热重、DFT 理论吸附能计算等））：**严禁在未放配图的情况下作为主图标号直接贴在 PPT 屏幕上**；必须物理隔离至 PPT 下方的演播备忘录（Speaker Notes）或独立口述讲稿中，作为答辩时口头展开的高阶亮点。

