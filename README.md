# Academic Agent Guardrails 🛡️ (v2.0.0)
### 学术科研与多智能体两层模块化攻防架构 (Open Source Edition)

[![Release: v2.0.0](https://img.shields.io/badge/Architecture-v2.0.0%202--Tier%20Modular-brightgreen.svg)](#)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Toolchain: uv](https://img.shields.io/badge/Toolchain-uv-purple.svg)](https://github.com/astral-sh/uv)
[![AI Agents: Antigravity | Claude Code | Cursor | Copilot](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Claude%20%7C%20Cursor-orange.svg)](#)

> **"让 AI 成为真正严谨的科研搭子，而不是满嘴跑火车的测试员。"**
>
> 本项目是一套从高强度真实科研、文献精读、顶刊矢量出图与组会 PPTX 汇报实战中沉淀出来的 **两层模块化 AI 智能体攻防架构、领域子技能库与确定性退出码 `0` 门禁套件**。原生适配 **Google Antigravity**、**Claude Code**、**Cursor**、**GitHub Copilot**（覆盖 Windows / WSL2 / macOS / Linux）。

---

## 📖 痛点与 v2.0.0 架构重构背景 (Why v2.0.0 Modular Guardrails?)

早期单文件规则堆砌极易突破 IDE 单规则文件体积上限（如 Antigravity 的 `24 KB` 截断阈值），导致尾部核心铁律被静默丢弃；同时仅有“文字禁止性规范”不足以拦住大模型在化学上下标、矢量图 `<tspan>` 碎片、Markdown 控制字符转义或 PPTX 图片拉伸比例上的失误。

因此在 **v2.0.0** 中，我们将整套防御系统升级为 **Layer 0 + Layer 1 两层渐进式架构**：
1. **Layer 0 (`AGENTS.md`, `<= 22,000` 字节硬上限)**：仅承载跨任务高频高压红线（Rules 1–7）与路由表，确保永不截断；
2. **Layer 1 (`skills/`, 3 大独立领域子 Skill + 退出码 `0` 门禁)**：按任务领域精准按需加载细则，并以共享基线 `scripts/pub_style.py` 与自动化校验脚本提供**确定性物理拦截（Exit Code = 0）**。

---

## 🏗️ 两层模块化防御架构 (v2.0.0 Two-Tier Architecture)

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                 LAYER 0: AGENTS.md (Rules 1–7, Hard-Cap <= 22,000 B)             │
│  1. 代码与资产持久化  2. WSL-First / uv / File-First  3. 先图后文与反夸大         │
│  4. 样品与引文零虚构  5. 双字体 / 上下标 / r"""..."""  6. 组会PPT保护与备注隔离   │
│  7. 强制技能路由表 (Workspace > Built-in) ──┬────────────────────┬───────────────┤
└─────────────────────────────────────────────┼────────────────────┼───────────────┘
                                              ▼                    ▼
┌────────────────────────────┐  ┌──────────────────────────┐  ┌───────────────────────────┐
│  skills/group-meeting-pptx │  │ skills/scientific-       │  │ skills/paper-bilingual-   │
│  • 组会无横幅体例 (图X：…)│  │        plotting-svg      │  │        reader             │
│  • 首尾页字体双重豁免      │  │ • 导入 pub_style.py 基线 │  │ • pymupdf PDF/SI 硬提取   │
│  • 视觉实图核验清单        │  │ • 4面黑框 / 朝内刻度     │  │ • ⁷Li NMR低场/背底相对论  │
│  Gate: verify_group_pptx.py│  │ • Dual-Y CE气隙 / 对称窗 │  │ • paper.md+source_map     │
│      + export_slides.ps1   │  │ Gate: audit_svg_         │  │ Gate: audit_markdown_     │
│         (Exit 0)           │  │   postprocess.py (Exit 0)│  │   suite.py (Exit 0)       │
└────────────────────────────┘  └──────────────────────────┘  └───────────────────────────┘
```

---

## 🚦 确定性退出码 `0` 门禁矩阵 (Deterministic Exit-0 Gates)

除文字规范与人工看图复核外，每个 Layer 1 子技能均配有独立验证脚本，**未返回 Exit `0` 前禁止交付**：

| 领域子技能 | 门禁脚本路径 | 核心物理检查项 |
| :--- | :--- | :--- |
| **`group-meeting-pptx`** | `skills/group-meeting-pptx/scripts/verify_group_pptx.py` | 校验图片像素真实宽高比误差（`<= 0.015`）、禁用 `【/】` 与 `(Figure 4a-c)` 刮削标签、化学式未上下标、夸张禁用词、尾页极简 `THANKS!` 格式 |
| **`scientific-plotting-svg`** | `skills/scientific-plotting-svg/scripts/audit_svg_postprocess.py` | 自动将残留 `STIXGeneral` / `DejaVu` 规范化为 `Times New Roman`（`--fix`），严格检验矢量 `<tspan>` 数量为 `0` |
| **`paper-bilingual-reader`** | `skills/paper-bilingual-reader/scripts/audit_markdown_suite.py` | 扫描 `r"""..."""` 漏用导致的控制字符（`\x07` / `\t`）与 LaTeX 残缺、禁用夸大词、磁盘图片存在性（`--check-images`）、`$` 平衡（`--check-math`）及 `source_map.json` 完整性（`--check-json`） |

---

## 📦 项目目录结构 (Directory Structure)

```text
academic-agent-guardrails/
├── SKILL.md                                    # v2.0.0 两层模块化总控引导
├── README.md                                   # 本开源项目完整文档与使用指南
├── LICENSE                                     # Apache-2.0 开源许可证
├── NOTICE                                      # 著作权归属与强制署名声明文件 (Attribution)
├── AGENTS.template.md                          # Layer 0 通用规范模板 (严格 <= 22,000 字节)
├── CLAUDE.template.md                          # 兼容 Claude Code 的 v2.0.0 轻量化指引模板
├── skills/                                     # Layer 1 三大领域子技能与门禁套件
│   ├── group-meeting-pptx/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── house-style-and-layout.md       # 16:9 组会板式、无横幅数据页、首尾页双字体豁免
│   │   │   └── visual-fact-audit-checklist.md  # 顶格!=峰值、⁷Li NMR 低场、XPS相对论、3D渐变
│   │   └── scripts/verify_group_pptx.py        # PPTX 退出码 0 门禁脚本
│   ├── scientific-plotting-svg/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── matplotlib-electrochem-specs.md # 3.0-4.0pt黑框、DSC/FTIR/LSV/Dual-Y CE/Li||Li
│   │   │   └── svg-and-3d-rules.md             # 零 <tspan> Unicode 与 3D 扩散 Prompt 持久化
│   │   └── scripts/audit_svg_postprocess.py    # SVG 字体替换与零 <tspan> 门禁脚本
│   └── paper-bilingual-reader/
│       ├── SKILL.md
│       ├── references/
│       │   ├── audit-pitfalls-and-errata.md    # raw-string 转义损坏与常见原文勘误库
│       │   └── reader-and-sourcemap-spec.md    # paper.md + source_map.json 同步规范
│       └── scripts/audit_markdown_suite.py     # Markdown/JSON 退出码 0 全检门禁
├── docs/                                       # 支柱理论深度解析 (01 ~ 07)
├── scripts/                                    # 共享样式基线与跨平台自动化工具链
│   ├── pub_style.py                            # 顶刊科研绘图共享样式基线 (set_pub_style / safe_save_clean)
│   ├── install.py                              # v2.0.0 跨平台智能安装、组件分级与子技能部署向导
│   ├── export_slides.ps1                       # PowerPoint COM 接口高分辨率逐页 PNG 导出脚本
│   ├── apply_dual_fonts.py                     # PPTX OpenXML 双字体无损注入器 (Times + 微软雅黑)
│   ├── scan_academic_rigor.py                  # 轻量单文件 Markdown/讲稿严谨性扫描器
│   └── sync_agents_to_opensource.py            # 工作区 AGENTS.md + skills -> 开源版脱敏同步脚本
└── templates/                                  # 真实学术交付模板 (audit report / env guard)
```

---

## 🛠️ 组件清单与跨平台系统适配 (Component Matrix)

本项目采用**模块化与系统感知设计**，运行 `install.py` 时根据宿主环境与科研场景自由勾选：

| 组件类别 | 模块代号 | 核心用处与部署产物 | 适用平台与依赖 |
| :--- | :--- | :--- | :--- |
| **必须组件** | `core` | **Layer 0 全局守则与防截断底线**：生成 `<= 22 KB` 定制版 `AGENTS.md` / `SKILL.md`、持久化原则、`uv` 隔离与 `r"""..."""` 规范。 | 跨平台通用 (Win/WSL/macOS/Linux)<br>依赖: `pymupdf`, `uv`, `git` |
| **可选组件** | `reader` | **部署 `skills/paper-bilingual-reader/`**：`pymupdf` 全文/SI 硬提取、`paper.md` + `source_map.json` 规范与 `audit_markdown_suite.py` 门禁。 | 跨平台通用<br>依赖: `pymupdf` |
| **可选组件** | `pptx` | **部署 `skills/group-meeting-pptx/` + 导图脚本**：组会版式、无横幅数据页、首尾页双字体豁免、`verify_group_pptx.py`、`export_slides.ps1`、`apply_dual_fonts.py`。 | **Windows**: 本地 PowerPoint COM<br>**WSL**: `powershell.exe` 跨系统桥接<br>**macOS/Linux**: `libreoffice` + `pdftoppm`<br>库: `python-pptx`, `Pillow` |
| **可选组件** | `figures` | **部署 `skills/scientific-plotting-svg/` + `scripts/pub_style.py`**：四面围框、DSC/FTIR/LSV/Dual-Y CE 气隙、`Li||Li` 放大窗与零 `<tspan>` 门禁 `audit_svg_postprocess.py`。 | 跨平台通用<br>依赖: `matplotlib`, `seaborn`, `scipy` |
| **可选组件** | `auditor` | **独立文本严谨性扫描器**：部署 `scripts/scan_academic_rigor.py` 用于日常散篇 Markdown 快速检查。 | 跨平台通用 |
| **可选组件** | `nature` | **Nature Skills 深度协同**：自动检测/挂载本地 `nature-*` 技能，配置生成-审核双驱优先级。 | 跨平台通用 (搭配 `.agents/skills`) |
| **可选组件** | `wsl` | **Windows + WSL2 混合协作防御**：WSL-First、`.venv` 与 `.venv-linux` 双隔离、`core.filemode false` 与 Direct Bypass 准则。 | Windows 宿主 + WSL2 |

---

## 🚀 智能安装与动态定制向导 (Dynamic Installation)

通过 `install.py` 一键部署定制版 Layer 0 规范、选定 Layer 1 子技能与 `pub_style.py`：

### 1. 交互式向导（推荐）
```bash
python scripts/install.py
```
向导会自动检测你的操作系统（Windows / WSL2 / macOS / Linux）与本地软件（PowerPoint / LibreOffice / uv / Python 环境），列出必须与可选组件，并针对所选模块动态生成不超过 `22 KB` 的 `AGENTS.md` / `SKILL.md`。

### 2. 预设与项目级根目录一键部署
```bash
# 全功能完整版 (部署全部 3 个 Layer 1 子技能 + pub_style.py + 全部门禁脚本)
python scripts/install.py --target ~/.gemini/antigravity/skills/academic-agent-guardrails --preset full

# 直接部署为任意科研项目根目录 (生成 AGENTS.md + .agents/skills/ + scripts/pub_style.py)
python scripts/install.py --target /path/to/your_project --as-root --preset full

# 论文精读与出图版 (reader + figures + auditor + nature，不含 PPTX)
python scripts/install.py --target ./my_paper_project --as-root --preset paper

# 极简核心版 (仅 Layer 0 防线 <= 22 KB，不展开领域子技能)
python scripts/install.py --target ./my_code_project --as-root --preset minimal
```

---

## 🤝 搭配技能生态：与 Nature Skills 强强联合

本项目作为**防御与门禁底座（“底盘、刹车与质检线”）**，与主打高效率内容生成的 **Nature Skills 系列（“发动机”）** 形成强强互补：

| 协同技能 | Nature 技能功能 | Guardrails v2.0.0 安全护栏与门禁增益 |
| :--- | :--- | :--- |
| **`nature-paper2ppt`** | 论文/精读笔记生成汇报 PPTX | 优先由 `group-meeting-pptx` 接管组会体例：去顶部结论横幅、首尾页双字体豁免、真实比例锁、`verify_group_pptx.py` + PNG 视觉自审。 |
| **`nature-figure`** | 生成多面板科研数据图与机理图 | 由 `scientific-plotting-svg` 与 `pub_style.py` 锁定四面黑框、内向标尺、Dual-Y CE 气隙、`Li||Li` 放大窗、`audit_svg_postprocess.py` 零 `<tspan>` 检验与样品原名锁定。 |
| **`nature-reader`** / **`nature-paper-card`** / **`nature-paper-xray`** | 论文精读、双语读者与卡片拆解 | 由 `paper-bilingual-reader` 执行 `pymupdf` 原文硬提取、先图后文三度核验（含 `⁷Li NMR` 方向与相对峰强）、`source_map.json` 映射与 `audit_markdown_suite.py` 门禁。 |
| **`nature-writing`** / **`nature-polishing`** | 学术论文写作、润色与精简 | 严格过滤营销夸大词、未测感官词与无依据类比，确保化学式与科学记数法全量规范上下标。 |

---

## 🔄 持续进化与脱敏同步机制

当工作区根目录的 `AGENTS.md` 或 `.agents/skills/*` 迭代新经验后，只需运行脱敏同步脚本：

```bash
uv run scripts/sync_agents_to_opensource.py
```

脚本会自动执行：
- 将工作区 `AGENTS.md`（校验 `<= 22,000` 字节）、3 个 `.agents/skills/` 子技能目录与 `scripts/pub_style.py` 同步至开源目录；
- 对私有盘符路径、WSL 挂载路径、内部论文代号、个人姓名与特定配方名称执行脱敏替换；
- 基于 `.private_terms.txt` 与敏感正则执行全量泄露零容忍审计，任一告警即以非零状态码阻断。

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
