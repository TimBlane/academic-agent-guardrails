# 专题指南：Windows 宿主与 WSL 跨系统混合协作攻防指南

## 痛点背景
在科研与深度开发中，很多开发者采用 **Windows 宿主 + WSL (Windows Subsystem for Linux)** 混合架构：
- **Windows 宿主优势**：拥有原生 Microsoft Office (PowerPoint COM 接口自动化)、Adobe Illustrator 矢量查看器、各种专业科研仪器上位机软件与原生图形界面；
- **WSL Linux 优势**：原生 POSIX 终端环境、无缝使用 Linux 版学术工具链（如各类生物信息学、计算材料学、强化学习 Python 库），避免在 Windows 下痛苦配置复杂的 C++ 编译环境。

然而，在 AI 编程助手（Antigravity、Claude Code、Cursor、Copilot）跨越 Windows 与 WSL 协作时，极易踩入以下 **4 大灾难性天坑**：

1. **虚拟环境二进制冲突**：在 WSL 里误激活 Windows 的 `.venv`，导致 ELF 与 PE 格式二进制冲突崩溃；
2. **NTFS 权限污染致使 Git 全量爆炸**：在 WSL 中执行 `git status`，因 NTFS 缺乏 Linux 权限位导致成千上万个文件全部被标记为权限变更（`0644 -> 0755`）；
3. **安全沙盒隔离报错死循环**：在 Windows 沙盒内直接调用 `wsl` 进程，因权限隔离令牌冲突报 `CreateProcessSecurityEnvironment: Access is denied` 或 `Wsl/E_ACCESSDENIED`；
4. **命令行长篇内联引号转义**：在 Windows 控制台或跨环境执行拼接长篇 `python -c "..."` 代码，导致引号剥离与 Token 严重浪费。

---

## 五大核心 WSL 混合协作铁律

### 1. 双虚拟环境物理隔离铁律 (Dual-vEnv Isolation)
* **宿主与子系统环境严禁混用**：
  * **Windows 宿主虚拟环境**：`<project_root>/.venv`（由 `.venv\Scripts\python.exe` 驱动）；
  * **WSL Linux 虚拟环境**：`<wsl_project_root>/.venv-linux`（由 `.venv-linux/bin/python` 驱动）。
* **依赖跨系统一秒同步**：
  * 两者共享项目根目录唯一的 `requirements.txt`；
  * 项目 `.gitignore` 必须永久声明：
    ```gitignore
    .venv*/
    ```
    严禁任何系统的虚拟环境入库！
* **运行时双环境防呆断言**：
  在关键自动化脚本入口处添加跨环境防护代码：
  ```python
  import sys
  if sys.prefix == sys.base_prefix:
      raise RuntimeError("[ENV ERROR] 检测到全局 Python 环境！必须使用 .venv (Windows) 或 .venv-linux (WSL) 虚拟环境执行。")
  ```

---

### 2. WSL-First 原则与终端职责明确分工
* **日常指令首选 WSL**：
  通用文件检索（`grep`/`find`/`sed`/`awk`）、多命令管道（`&&`/`||`）、Git 版本审查、高负荷 Python 算法运算，直接调用 WSL 执行（默认挂载路径 `/mnt/<drive>/<project_root>`）；
* **PowerShell 专属保留（COM 自动化独占）**：
  涉及 Windows 原生独占的 COM 接口调用（如调用本地 PowerPoint COM 自动将 PPTX 幻灯片渲染为 PNG 图片进行视觉自审），**必须且只能通过独立的 `.ps1` 文件由 Windows PowerShell 执行**。
* **WSL 跨系统调起 Windows 导图**：
  如果在 WSL 终端内需要触发幻灯片真机自审导出，可使用 Windows 跨系统调用：
  ```bash
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/export_slides.ps1 -PptxPath "presentations/my_slide.pptx"
  ```

---

### 3. 沙盒试探防 Token 浪费准则 (Direct Bypass Sandbox Protocol)
* **报错根源**：在 Windows 安全沙盒内调度 WSL 虚拟机进程时，外层安全沙盒机制必然因底层隔离令牌冲突报错（`CreateProcessSecurityEnvironment: Access is denied` 或 `Wsl/E_ACCESSDENIED`）；
* **防御铁律**：经用户授权后，所有涉及 WSL 终端调度的操作，**一律直接采用绕过沙盒（Bypass Sandbox）模式执行**，严禁进行必然失败的先期沙盒试探，彻底消除无效重试开销与往返延迟。

---

### 4. 跨系统 Git 权限防污染配置 (Git Sanitization)
当 WSL 访问 Windows NTFS 挂载目录（如 `/mnt/c/...`）时，WSL 内部必须全局开启以下配置，消除因文件系统权限位缺失造成的假修改：
```bash
# 在 WSL 终端内执行：
git config --global core.filemode false
git config --global core.autocrlf true
```

---

### 5. 独立脚本落地优先 (File-First 原则)
* **严禁命令行长篇内联**：
  绝不允许通过 `python -c "..."` 或长篇内嵌 bash 拼接带有复杂双引号、单引号嵌套的代码；
* **必须先落盘为独立文件**：
  凡涉及文件抽取、正则清洗、批量重命名、数据分析等逻辑，**必须先持久化写入独立的 `.py` 或 `.sh` 文件再调用执行**，从源头消灭 Windows / WSL 引号转义报错。
