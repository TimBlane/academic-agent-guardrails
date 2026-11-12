# 支柱五：WSL-First、uv 强隔离与 Windows 终端防御准则

## 痛点背景
在 Windows 宿主机与 WSL 共存的科研协作环境中，AI 助手极易因环境混用和命令行转义踩坑：
1. **全局 Python 污染**：直接向宿主机全局安装依赖，或误用权限受限的系统 Python 别名，导致项目无法跨机复现；
2. **多行命令行引号崩坏**：在 PowerShell / CMD 中使用 `python -c "..."` 或 `powershell -Command "..."` 拼接含正则/LaTeX 的多行脚本，引发 `ParserError` 与转义损坏；
3. **AGENTS.md 体积膨胀截断**：单文件规则无节制堆砌超过 `24,000` 字节后，被 IDE 静默截断尾部规范，导致关键红线失效。

---

## 模块化与隔离工程准则

### 1. 两层架构与 `<= 22,000` 字节硬上限
- **Layer 0 (`AGENTS.md`)**：仅保留跨任务高频高压红线（Rules 1–7）与技能路由表，**文件体积永久控制在 `<= 22,000` 字节（建议 `11–15 KB`）**，远离 IDE `24 KB` 截断风险；
- **Layer 1 (`.agents/skills/` 或 `skills/`)**：详细领域排版规范、电化学绘图模板、文献审计细则与退出码门禁脚本全部下沉至按需加载的子 Skill。

### 2. WSL-First 与 PowerShell 唯一例外原则
- 检测到 WSL 环境时，日常文本管道、Git 操作与跨平台脚本运行**首选 WSL**（`<wsl_project_root>`）；
- **PowerShell 唯一例外**：仅在调用 Windows 独占接口（如通过本地 PowerPoint COM 接口运行 `scripts/export_slides.ps1` 导出 PPTX 幻灯片 PNG）时使用独立 `.ps1` 脚本，日常坚决不用 PowerShell 拼指令；
- **编码与换行**：Python 文件读写显式声明 `encoding='utf-8'`，Windows 控制台入口执行 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`；WSL 内配置 `core.filemode false` 与 `core.autocrlf true`。

### 3. `uv` 虚拟环境强隔离与入口自检
- **唯一合法解释器**：Windows 下为 `<project_root>/.venv/Scripts/python.exe`，WSL 下为 `<wsl_project_root>/.venv-linux/bin/python`；**严禁向宿主机全局 Python 安装任何包**；
- **依赖管理与重建**：使用 `uv pip install <pkg>` 并同步更新 `requirements.txt`（一键重建：`uv venv --clear --python 3.12 && uv pip install -r requirements.txt`）；
- **环境防误触护栏**：关键脚本应在 `main()` 入口检测 `sys.prefix == sys.base_prefix`，若未激活 `.venv` 则抛出 `RuntimeError` 阻断运行。

### 4. File-First 独立脚本与持久化规范
- **严禁内联长代码**：凡业务、数据解析、正则清洗与绘图逻辑，一律先持久化写入独立 `.py` / `.sh` 脚本，禁止用 `python -c` 或 `powershell -Command`；
- **资产持久化**：严禁将可复用脚本遗留在临时沙盒或 AppData 目录，按职责落盘于 `scripts/`、`papers/<paper_id>/`、`presentations/` 与 `.agents/skills/`。
