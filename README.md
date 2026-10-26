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
├── AGENTS.template.md                # 即拷即用的通用 AGENTS.md 规范模板 (20条完整规则)
├── CLAUDE.template.md                # 兼容 Claude Code 的轻量化指引模板
├── docs/                             # 深度原理解析与各模块实战指南
│   ├── 01_multi_agent_persistence.md # 支柱一：多 Agent 代码持久化与透明共享
│   ├── 02_source_truth_protocol.md   # 支柱二：零幻觉物理文本溯源与数据互锁
│   ├── 03_presentation_guardrails.md # 支柱三：学术 PPTX 视觉自审与双字体排版
│   ├── 04_academic_rigor.md          # 支柱四：严谨学术语言范式与去营销化
│   ├── 05_toolchain_isolation.md     # 支柱五：现代化 uv 隔离与 Windows 防御
│   └── 06_scientific_figure_standards.md # 支柱六：顶刊科研图表坐标系与材料物性绘图规范
├── scripts/                          # 经过安全脱敏的即用型自动化工具链
│   ├── export_slides.ps1             # PowerPoint COM 接口高分辨率逐页 PNG 导出脚本
│   ├── apply_dual_fonts.py           # PPTX OpenXML 双字体无损注入器 (Times + 雅黑)
│   ├── scan_academic_rigor.py        # 文本化学式/上下标/夸大词自动化合规审查器
│   └── sync_agents_to_opensource.py  # 自动同步并脱敏工作区 AGENTS.md 的持续集成脚本
└── templates/                        # 真实学术交付模板
    ├── ground_truth_audit_report.md  # 物理文献事实核查与数据溯源审计模板
    └── env_guard_snippet.py          # 防误入全局 Python 环境的运行时断言代码
```

---

## 🚀 快速上手 (Quick Start)

### 模式 A：作为 Agent Skill 使用（推荐）
如果您使用的是支持 Skills 机制的 AI 编程助手（如 Antigravity、Claude Code、Cursor 等）：
1. 将本项目目录复制到您的 agent 技能目录中：
   ```bash
   cp -r "academic-agent-guardrails" ~/.gemini/antigravity/skills/academic-agent-guardrails
   # 或复制到项目局部 skills 目录：
   # cp -r "academic-agent-guardrails" .agents/skills/academic-agent-guardrails
   ```
2. AI 助手将自动加载 `SKILL.md`，并在处理学术汇报、文献精读、图表绘制时自动启用守则约束。

### 模式 B：作为项目根目录行为准则
1. 复制模板至您的目标仓库根目录：
   ```bash
   cp "academic-agent-guardrails/AGENTS.template.md" "/path/to/your/repo/AGENTS.md"
   ```
2. 在该仓库中唤醒 AI 助手时，AI 会将 `AGENTS.md` 作为第一优先法则执行。

### 模式 C：使用自动化工具链
1. **PPTX 逐页导出视觉自审**（Windows PowerShell）：
   ```powershell
   powershell -File scripts/export_slides.ps1 -PptxPath "presentations/my_slide.pptx"
   ```
2. **一键注入学术标准双字体**（英数 Times New Roman + 中文 微软雅黑）：
   ```bash
   uv run scripts/apply_dual_fonts.py "presentations/my_slide.pptx"
   ```
3. **学术用词与化学式规范性扫描**：
   ```bash
   uv run scripts/scan_academic_rigor.py "papers/my_paper/paper.md"
   ```

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

## 📄 许可证 (License)

本项目采用 [Apache-2.0 许可证](LICENSE) 开源。欢迎学术界与工业界同行自由引用、复用、提 PR 与二次定制。
