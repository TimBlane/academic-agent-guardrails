# 支柱五：现代化 uv 隔离与 Windows 终端防御准则

## 痛点背景
在跨平台或 Windows 宿主环境下与 AI 结对开发时，有两个高频导致失败的根源：
1. **全局 Python 环境污染**：AI 随手调用宿主机的全局 `pip install`，导致依赖版本冲突，换一台设备后完全无法复现环境；
2. **Windows 终端引号转义与 Token 浪费**：AI 喜欢在命令行中使用 `python -c "import ...; for ...; print(...)"` 拼接几十行带有双引号、单引号的代码，导致 Windows PowerShell 报 `ParserError`，进而陷入多轮报错与重试，白白消耗大量 Token。

---

## 防御性工程准则

### 1. 现代化 uv 工具链与虚拟环境硬锁定
- **纯净虚拟环境**：项目必须采用本地独立的纯净虚拟环境（`<project_root>/.venv`，基于 Python 3.12+）；
- **唯一合法解释器与包管理**：
  - Windows 执行显式指定解释器：`.venv\Scripts\python.exe` 或使用 `uv run`；
  - 依赖安装优先使用极速包管理：`uv pip install <package>`；
- **零全局污染红线**：严禁向宿主机用户全局 Python 目录（如 `AppData\Local\Python\...`）安装任何依赖；
- **跨设备一秒恢复机制**：
  - 一旦引入新依赖，必须同步更新根目录 `requirements.txt`；
  - 新设备仅需执行：
    ```bash
    uv venv --clear --python 3.12 && uv pip install -r requirements.txt
    ```
    即可在数秒内幂等完成全量环境重建。

### 2. Windows 平台独立脚本落地优先（File-First 原则）
- **严禁内联长篇代码**：严禁在命令行中通过 `python -c "..."` 或 `powershell -Command "..."` 拼接长篇、多行或带有复杂嵌套引号的代码；
- **先落盘再调用**：凡涉及数据抽取、正则清洗、批量更名、分析计算，必须先持久化写入独立的 `.py` 脚本，然后直接调用该脚本；
- **终端分工清晰**：
  - 日常文本管道与 Git 操作优先使用 Git Bash；
  - 原生 Windows COM 组件（如 PowerPoint COM 导出 PNG）必须由独立 `.ps1` 文件交由 PowerShell 执行。
