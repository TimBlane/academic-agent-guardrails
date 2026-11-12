# 支柱一：多 Agent 代码持久化与透明共享规范

## 痛点背景
现代 AI 编程辅助工具（如 Google Antigravity、Claude Code、Cursor、Copilot 等）往往在不同的执行环境或临时会话目录中运行：
- 部分智能体在会话中默认将代码写入内部沙盒（例如 `AppData/.../brain/scratch/...` 或临时沙盒目录）；
- 会话结束后，这些临时文件对人类开发者和其他智能体完全不可见；
- 当切换到另一个智能体（例如从 Antigravity 切换到 Claude Code 或 Cursor）继续工作时，另一个智能体无法感知先前的改动，导致重复编码甚至严重的功能回滚。

---

## 核心法则：File-First 与项目目录持久化

### 1. 物理保存在项目工作区
所有业务代码、数据分析脚本、PPTX 构建脚本、绘图程序，**必须直接落盘保存在项目根目录的既定子目录下**：
- **通用工具脚本**：存放于 `<project_root>/scripts/`（如 `export_slides.ps1`、`apply_dual_fonts.py`）；
- **论文与课题专属代码**：就近存放在对应论文目录下（如 `<project_root>/papers/<paper_id>/`）；
- **汇报与演示脚本**：存放在 `<project_root>/presentations/` 或对应课题目录下。

### 2. 纳入 Git 版本控制
所有持久化脚本均应纳入版本控制追踪，杜绝“隐形代码”与“口头交付”。

### 3. 多智能体跨工具无缝接力
无论下一个打开项目的是 Claude Code、Antigravity 还是人类工程师，只需 `git pull` 或查看本地对应目录，即可立即基于现有代码继续迭代，形成闭环协作。
