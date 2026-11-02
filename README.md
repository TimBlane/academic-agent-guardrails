# Academic Agent Guardrails 🛡️
### 学术科研与多智能体结对攻防守则 (Open Source Edition)

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Toolchain: uv](https://img.shields.io/badge/Toolchain-uv-purple.svg)](https://github.com/astral-sh/uv)
[![AI Agents: Antigravity | Claude Code | Cursor | Copilot](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Claude%20%7C%20Cursor-orange.svg)](#)

> **"让 AI 成为真正严谨的科研搭子，而不是满嘴跑火车的测试员。"**
> 
> 本项目是一套经过高强度真实科研、学术文献精读与组会 PPTX 汇报实战打磨沉淀的 **AI 智能体行为准则、防御协议与自动化工具包**。适用于 **Google Antigravity**、**Claude Code**、**Cursor**、**GitHub Copilot** 等现代编程与科研智能体。

---

## 📖 痛点与开源背景 (Why This Project?)

大语言模型（LLM）与代码智能体（Coding Agents）极大提升了学术研究与幻灯片制作的生产力，但在没有深度工程防御约束的情况下，AI 在真实科研场景中极易频繁触发以下“灾难性”故障：

1. **幻觉与张冠李戴**：阅读 PDF 文献时凭模糊印象概括，甚至捏造数据；将横坐标圈数与纵坐标容量混淆，子图标号乱写。
2. **汇报版式翻车**：PPT 代码编译通过后就宣布“完成”，交付给用户时到处是文本框重叠、文字溢出卡片、图文遮挡。
3. **语言营销化**：在严肃学术报告或论文草稿中凭空臆造“军工级防护”、“神级表现”、“革命性颠覆”等非学术词汇。
4. **字体与排版粗糙**：混用单一中文字体渲染英文与数字，导致 Times New Roman 与中文字体混杂失序；化学式平铺直写（如 `CO2`、`Li+` 未做上下标）。
5. **沙盒黑洞与环境污染**：代码随手写在临时沙盒中导致会话结束后丢失；直接向宿主机全局 Python 安装依赖，污染系统环境。
6. **Windows 控制台 Token 浪费**：在命令行中内联长篇代码，因引号转义与控制台解析错误引发死循环重试。

本项目将从成百上千次人机协作返工中总结出的血泪教训，凝炼为 **6 大防御支柱、20 条铁律** 与 **配套自动化工具链**，帮助科研人员与开发者构建一个**零幻觉、防翻车、可追溯**的高可用科研工作流。

---

## 🏛️ 六大核心防御支柱 (The 6 Defense Pillars)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ACADEMIC AGENT GUARDRAILS PILLARS                    │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. 代码持久化透明   │ 2. 零幻觉物理溯源   │ 3. 学术汇报视觉自审          │
│ • File-First 原则   │ • PDF 原文硬提取   │ • 交付前真机视觉肉眼自审     │
│ • 杜绝沙盒文件丢失 │ • 严禁擅改样品名称 │ • 双字体分离 (Times + 雅黑)  │
│ • Git 纳入全量追踪 │ • 文献零虚构物理查证│ • 化学式/科学记数法规范上下标│
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 4. 严谨学术范式与表达│ 5. 顶刊科研绘图标准│ 6. 现代环境与执行防御        │
│ • 严禁非学术修饰性夸大│ • 四面框线与内向标尺│ • uv 虚拟环境严格锁定 (.venv)│
│ • 坐标轴与量纲硬互锁│ • DSC/FTIR/LSV 惯例│ • Windows 终端脚本落盘执行   │
│ • 备忘录与正文物理隔离│ • 矢量图零 <tspan> │ • 用户定稿绝对只读保护       │
└────────────────────┴────────────────────┴──────────────────────────────┘
```

---

## 📦 项目目录结构 (Directory Structure)

```text
Open Source/
├── SKILL.md                          # 标准 Agent Skill 声明与行为引导定义 (20条铁律)
├── README.md                         # 本开源项目完整文档与使用指南
├── LICENSE                           # Apache-2.0 开源许可证
├── NOTICE                            # 著作权归属与强制署名声明文件 (Attribution)
├── AGENTS.template.md                # 即拷即用的通用 AGENTS.md 规范模板 (20条完整规则)
├── CLAUDE.template.md                # 兼容 Claude Code 的轻量化指引模板
├── docs/                             # 深度原理解析与各模块实战指南
│   ├── 01_multi_agent_persistence.md # 支柱一：多 Agent 代码持久化与透明共享
│   ├── 02_source_truth_protocol.md   # 支柱二：零幻觉物理文本溯源与数据互锁
│   ├── 03_presentation_guardrails.md # 支柱三：学术 PPTX 视觉自审与双字体排版
│   ├── 04_academic_rigor.md          # 支柱四：严谨学术语言范式与去营销化
│   ├── 05_toolchain_isolation.md     # 支柱五：现代化 uv 隔离与 Windows 防御
│   ├── 06_scientific_figure_standards.md # 支柱六：顶刊科研图表坐标系与材料物性绘图规范
│   └── 07_wsl_hybrid_architecture.md # 支柱七：Windows 宿主与 WSL 跨系统混合协作攻防指南
├── scripts/                          # 经过安全脱敏的即用型自动化工具链
│   ├── install.py                    # 跨平台智能安装、组件分级与动态定制向导
│   ├── export_slides.ps1             # PowerPoint COM 接口高分辨率逐页 PNG 导出脚本
│   ├── apply_dual_fonts.py           # PPTX OpenXML 双字体无损注入器 (Times + 雅黑)
│   ├── scan_academic_rigor.py        # 文本化学式/上下标/夸大词自动化合规审查器
│   └── sync_agents_to_opensource.py  # 自动同步并脱敏工作区 AGENTS.md 的持续集成脚本
└── templates/                        # 真实学术交付模板
    ├── ground_truth_audit_report.md  # 物理文献事实核查与数据溯源审计模板
    └── env_guard_snippet.py          # 防误入全局 Python 环境的运行时断言代码
```

---

## 🛠️ 组件清单与跨平台系统适配 (Component Matrix)

本项目采用**模块化与系统感知设计**，组件划分为**必须组件**与**可选组件**：

| 组件类别 | 模块代号 | 核心用处与价值 | 适用平台与依赖 |
| :--- | :--- | :--- | :--- |
| **必须组件** | `core` | **底层学术真实性与环境防污染底线**：硬提取 PDF 原文、事实审计报告、去商业营销词汇、化学式上下标、现代 `uv` 隔离。 | 跨平台通用 (Win/macOS/Linux)<br>依赖: `pymupdf`, `uv`, `git` |
| **可选组件** | `pptx` | **学术汇报 PPTX 视觉自审与双字体**：组会/答辩 PPT 生成后，自动逐页导出高清 PNG，Agent 自身肉眼复核卡片重叠与文字溢出；自动注入 Times New Roman + 微软雅黑；正文与备忘录物理隔离。 | **Windows**: 本地 MS PowerPoint (COM)<br>**macOS**: LibreOffice / Keynote CLI<br>**Linux**: `libreoffice` + `pdftoppm`<br>Python 库: `python-pptx` |
| **可选组件** | `figures` | **顶刊科研图表坐标系与材料物性标准**：绘制实验数据曲线时，强制 4 面全包围沉稳黑框（无上右刻度、朝内刻度）；保护用户样品代号；规范 DSC/FTIR/LSV 专有图谱；导出 Illustrator 友好型零 `<tspan>` 矢量 SVG。 | 跨平台通用<br>依赖: `matplotlib`, `seaborn`, `scipy` |
| **可选组件** | `auditor` | **学术严谨度与文本合规自动化审查**：自动扫描 Markdown / 论文稿件 / 讲稿中未标上下标的化学式（如 `CO2`, `Li+`）及商业夸大词。 | 跨平台通用 (轻量内置正则扫描) |
| **可选组件** | `nature` | **Nature Skills 深度协同路由**：与 Nature 系列技能联动，作为前置输入拦截与后置交付审核网关。 | 跨平台通用 (搭配 `.agents/skills`) |
| **可选组件** | `wsl` | **Windows + WSL 跨系统混合协作套件**：消除双系统二进制冲突；双虚拟环境隔离 (`.venv` vs `.venv-linux`)；Git NTFS 权限防污染 (`core.filemode false`)；Direct Bypass 沙盒准则；WSL 终端跨系统调起 Windows 办公导图。 | Windows 宿主 + WSL (Ubuntu/Debian) |

---

## 🚀 智能安装与动态定制向导 (Dynamic Installation)

你可以通过内置的 `install.py` 脚本，根据你的操作系统和科研需求**动态裁剪并生成专属的 Skill 内容**：

### 1. 交互式向导（推荐）
```bash
python scripts/install.py
```
向导会自动检测你的操作系统（Windows / macOS / Linux）与本地软件（PowerPoint / LibreOffice / uv / Python 环境），列出必须与可选组件，让你自由勾选需要的功能。

### 2. 预设快速安装 (Presets)
根据你的典型科研场景一键生成定制守则：
```bash
# 全功能完整版 (包含 PPTX 自审 + 顶刊绘图 + 严谨审查 + Nature Skills)
python scripts/install.py --target ~/.gemini/antigravity/skills/academic-agent-guardrails --preset full

# 纯论文精读与写作版 (去除 PPTX 组件，保留文献提取与绘图标准)
python scripts/install.py --target ./my_paper_project --preset paper --as-root

# 极简核心版 (仅保留零幻觉物理文本溯源与环境隔离底线)
python scripts/install.py --target ./my_code_project --preset minimal --as-root
```

---

## 🤝 搭配技能生态：与 Nature Skills 强强联合

本项目作为**防御与品质护栏（“刹车与底盘”）**，与主打学术生成生产力的 **Nature Skills 系列（“发动机与油门”）** 具备天然的互补协同能力：

| 协同技能 | Nature 技能功能 | Guardrails 安全护栏赋能 (防翻车增益) |
| :--- | :--- | :--- |
| **`nature-paper2ppt`** | 论文/精读笔记一键生成组会汇报 PPTX | 强制执行真机视觉自审（导出 PNG 肉眼审核）、双字体分离（Times + 雅黑）、去提取代号、SI 补充数据物理隔离至演播备忘录。 |
| **`nature-figure`** | 生成多面板科研数据图与机理图 | 强制执行四面全包围粗黑框、内向标尺、零 `<tspan>` 碎片化矢量 SVG、严禁擅自改动用户样品名称、DSC/FTIR 惯例修正。 |
| **`nature-reader`** / **`nature-paper-card`** | 论文双语对照精读、生成精读卡片 | 强制执行原版 PDF 文本物理硬提取比对，杜绝模型幻觉脑补，强制交付三度交叉事实审计报告 (`ground_truth_audit_report.md`)。 |
| **`nature-writing`** / **`nature-polishing`** | 学术论文写作、润色与段落精炼 | 强制过滤非学术商业营销词汇（“军工级”、“神级表现”等），严格规范化学式与离子电荷上下标。 |
| **`nature-reviewer`** / **`nature-response`** | 模拟同行评审、返修意见逐点回复 | 确保所有反驳观点与修改数据 100% 具备本地实验与文献实测证据支撑，严禁虚构引文。 |

安装本守则时选择 `nature` 模块，即可自动关联已安装的 Nature Skills，形成闭环科研生产力！

---

## 🔄 越用越好用：动态进化与脱敏同步机制

本项目的设计理念是：**规则伴随实际科研使用持续迭代与进化**。

当您在日常科研中遇到新的翻车案例、总结出新的防御铁律（如 Rule 15、Rule 16）并写入工作区的 `AGENTS.md` 后，只需运行脱敏同步脚本：

```bash
uv run scripts/sync_agents_to_opensource.py
```

该脚本会自动执行：
- 扫描私有路径（如本地磁盘绝对路径、用户家目录等），并自动替换为 `<project_root>`；
- 脱敏具体私人课题代码、论文 ID、学生/导师姓名与特定机构信息；
- 执行敏感词安全审计；
- 幂等刷新 `academic-agent-guardrails/AGENTS.template.md`，让开源版本始终与您的最佳实践保持同步！

---

## 📄 许可证与署名引用规范 (License & Citation)

本项目采用 **[Apache-2.0 许可证](LICENSE)** 开源。

Apache-2.0 是一项具备**强制署名保护、专利交叉反制与商标品牌防护**的严密开源协议。根据协议条款（Section 4）与学术同行评审规范，使用本项目需严格恪守以下条件：

1. **强制保留署名与来源出处 (Attribution Required)**：
   - 任何二次分发、修改、衍生开发或在您团队/个人项目中复用本守则时，**必须在显著位置保留原作者版权声明（Copyright Notice）与项目出处链接**：`https://github.com/TimBlane/academic-agent-guardrails`；
   - 必须随附本项目的 [LICENSE](LICENSE) 副本及 [NOTICE](NOTICE) 归属说明文件；
   - 严禁抹去原作者署名或将本守则伪称为第三方或个人独立原创。
2. **显式修改声明 (State Changes)**：
   - 对本守则、规则模板或工具脚本进行任何实质性修改的文件，必须包含醒目的修改声明，严禁甩锅或混淆原作者设计。
3. **学术与科研引用规范 (How to Cite)**：
   - 如果您的学术论文、学位论文、汇报 PPTX、预印本（arXiv/bioRxiv）或科研工程受益于本项目的攻防守则与工具链，请按如下 BibTeX 格式规范引用以支持开源原作者：

```bibtex
@software{academic_agent_guardrails_2026,
  author = {Alex (TimBlane)},
  title = {Academic Agent Guardrails: Battle-tested academic research, presentation, and engineering guardrails for AI coding agents},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/TimBlane/academic-agent-guardrails}}
}
```
