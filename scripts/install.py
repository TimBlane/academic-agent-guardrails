#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install.py — Academic Agent Guardrails 模块化与跨平台定制安装工具
----------------------------------------------------------------------
功能：
1. 智能检测当前操作系统（Windows / macOS / Linux）与环境依赖；
2. 明确呈现必须组件（Required）与可选组件（Optional），并讲明可选组件的用处；
3. 根据用户选择的可选组件，动态裁剪并定制生成专属于该环境的 SKILL.md 与 AGENTS.md；
4. 识别并说明协同搭配的 Nature Skills（如 nature-figure, nature-paper2ppt, nature-reader 等），
   支持一键软链/安装到目标 Agent 技能库中。

使用方式：
    # 交互式向导（推荐）：
    python scripts/install.py

    # 命令行指定配置（适合 CI / 自动化）：
    python scripts/install.py --target ~/.gemini/antigravity/skills/academic-agent-guardrails --modules core,pptx,figures,nature
    python scripts/install.py --target ./my_project --preset minimal
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Windows UTF-8 控制台防御
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_ROOT / "templates"
DOCS_DIR = SKILL_ROOT / "docs"

# ==================== 1. 系统与依赖检测 ====================

def detect_system():
    os_name = platform.system().lower()
    is_wsl = False
    has_wsl = False

    if os_name == "windows":
        system_type = "windows"
        system_desc = f"Windows ({platform.release()})"
        try:
            wsl_check = subprocess.run(["wsl.exe", "-l", "-q"], capture_output=True, text=True, errors="replace")
            has_wsl = wsl_check.returncode == 0 and bool(wsl_check.stdout.strip())
        except Exception:
            has_wsl = False
    elif os_name == "darwin":
        system_type = "macos"
        system_desc = f"macOS ({platform.mac_ver()[0]})"
    else:
        system_type = "linux"
        try:
            if Path("/proc/version").exists():
                ver_text = Path("/proc/version").read_text(encoding="utf-8", errors="replace").lower()
                if "microsoft" in ver_text or "wsl" in ver_text:
                    is_wsl = True
        except Exception:
            pass
        system_desc = f"Linux (WSL2: {platform.release()})" if is_wsl else f"Linux ({platform.release()})"

    # 检测 Python 与虚拟环境
    python_version = platform.python_version()
    in_venv = sys.prefix != sys.base_prefix

    # 检测 uv
    uv_path = shutil.which("uv")
    # 检测 git
    git_path = shutil.which("git")

    # 检测 PPTX 渲染环境
    has_powerpoint = False
    has_libreoffice = False
    if system_type == "windows":
        try:
            import win32com.client
            has_powerpoint = True
        except ImportError:
            try:
                ps_check = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "New-Object -ComObject PowerPoint.Application | Out-Null; $?"],
                    capture_output=True, text=True, errors="replace"
                )
                has_powerpoint = ps_check.returncode == 0
            except Exception:
                has_powerpoint = False
    else:
        has_libreoffice = bool(shutil.which("soffice") or shutil.which("libreoffice"))

    # 检测已安装的 Python 库
    installed_pkgs = {}
    for pkg in ["pymupdf", "pptx", "matplotlib", "seaborn", "scipy"]:
        try:
            __import__(pkg)
            installed_pkgs[pkg] = True
        except ImportError:
            # 兼容老版 fitz 别名
            if pkg == "pymupdf":
                try:
                    __import__("fitz")
                    installed_pkgs[pkg] = True
                    continue
                except ImportError:
                    pass
            installed_pkgs[pkg] = False

    return {
        "type": system_type,
        "desc": system_desc,
        "is_wsl": is_wsl,
        "has_wsl": has_wsl,
        "python_version": python_version,
        "in_venv": in_venv,
        "uv": uv_path,
        "git": git_path,
        "has_powerpoint": has_powerpoint,
        "has_libreoffice": has_libreoffice,
        "pkgs": installed_pkgs,
    }


# ==================== 2. 可选组件定义与说明 ====================

AVAILABLE_MODULES = {
    "core": {
        "name": "基础学术防御核心 (Core Guardrails)",
        "required": True,
        "description": "零幻觉 PDF 原文硬提取 (Rule 10)、事实审计报告 (Rule 12)、学术去营销化 (Rule 7)、化学式上下标 (Rule 9)、现代化 uv/环境隔离与 File-First 原则 (Rule 1, 20)。",
        "value": "必须组件。为所有 AI 科研任务提供底层真实性与环境防污染安全底线。",
        "deps": ["pymupdf"],
    },
    "pptx": {
        "name": "PPTX 汇报真机视觉自审与双字体排版 (Presentation Defense)",
        "required": False,
        "description": "交付前调用本地办公套件逐页导出高清 PNG，智能体自身肉眼核验卡片重叠与文字溢出 (Rule 2)；Times New Roman + 微软雅黑双字体自动映射 (Rule 8)；幻灯片去提取标签 (Rule 4)；正文与演播备忘录物理隔离 (Rule 20)。",
        "value": "做组会汇报、论文汇报、答辩 PPT 必备！彻底杜绝代码编译通过但排版视觉车祸、文字被图片遮挡的问题。",
        "deps": ["python-pptx"],
        "system_notes": {
            "windows": "基于本地 Microsoft PowerPoint COM 自动化（开箱即用，极速渲染）。",
            "macos": "基于 LibreOffice 或 Keynote CLI 渲染高清导图。",
            "linux": "基于 LibreOffice (soffice --headless) + poppler-utils (pdftoppm) 导出 PNG。",
        }
    },
    "figures": {
        "name": "顶刊科研图表与材料物性绘图标准 (Publication Figures)",
        "required": False,
        "description": "顶刊四面全包围框线与内向标尺 (Rule 15)；实验样品代号严禁臆造更替 (Rule 13)；引文零虚构物理查证 (Rule 14)；DSC（Exo Up 熔融凹陷）/FTIR/LSV 专有图谱规整 (Rule 16)；矢量图零 <tspan> 碎片化与字体统一 (Rule 17)；解耦独立迭代 (Rule 18)。",
        "value": "绘制论文配图、多面板图、实验表征曲线必备！保证输出符合 CNS / Advanced Materials 顶刊审美品味，且矢量图可在 Illustrator 中二次编辑。",
        "deps": ["matplotlib", "seaborn", "scipy"],
    },
    "auditor": {
        "name": "学术严谨度与化学式自动化审计工具 (Automated Rigor Scanner)",
        "required": False,
        "description": "自动化文本扫描脚本 `scan_academic_rigor.py`，正则扫描 Markdown / 论文稿件 / 讲稿中未标上下标的化学式（如 CO2, Li+）和违规营销词汇。",
        "value": "交付前自动化静态检查，防止低级格式错误溜进汇报或论文手稿。",
        "deps": [],
    },
    "nature": {
        "name": "Nature Skills 深度协同路由 (Nature Skills Synergy)",
        "required": False,
        "description": "将本守则作为安全护栏，与 Nature 系列技能（nature-figure, nature-paper2ppt, nature-reader, nature-writing, nature-paper-card 等）形成“生成+审核”双轮驱动闭环。",
        "value": "极大提升整套 AI 科研工作流的上限！Nature Skills 负责高质量生成，Guardrails 负责严谨审查，强强联合。",
        "deps": [],
    },
    "wsl": {
        "name": "Windows + WSL 混合开发防御套件 (WSL Hybrid Synergy)",
        "required": False,
        "description": "跨系统协作防护：WSL-First 日常操作、双虚拟环境隔离 (.venv vs .venv-linux)、Git NTFS 权限防污染 (core.filemode false)、Direct Bypass 沙盒准则与跨系统 COM 办公桥接。",
        "value": "在 Windows 宿主与 WSL 跨系统结对开发必备！彻底消除跨系统二进制冲突与 Git 全量假修改报错。",
        "deps": [],
    }
}

# ==================== 3. 动态组装 SKILL.md 与 AGENTS.md ====================

def generate_custom_skill_md(selected_modules: list[str], sys_info: dict) -> str:
    """根据选择的模块动态生成定制版 SKILL.md"""
    has_pptx = "pptx" in selected_modules
    has_figures = "figures" in selected_modules
    has_nature = "nature" in selected_modules
    has_auditor = "auditor" in selected_modules
    has_wsl = "wsl" in selected_modules or sys_info.get("is_wsl") or sys_info.get("has_wsl")

    rules_count = 8
    if has_pptx:
        rules_count += 6
    if has_figures:
        rules_count += 6

    lines = [
        "---",
        "name: academic-agent-guardrails",
        "description: Battle-tested academic research, presentation, and engineering guardrails for AI coding agents. Prevents hallucinations, token waste, slide clutter, and unverified data claims.",
        "---",
        "",
        "# Academic Agent Guardrails (学术科研与多智能体结对攻防守则)",
        "",
        f"This skill equips AI agents with battle-tested defensive protocols tailored for **{sys_info['desc']}**.",
        f"Configured with **{len(selected_modules)} active modules** ({rules_count} enforced engineering rules).",
        "",
        "---",
        "",
        "## 🎯 Active Modules in This Deployment",
        "",
    ]

    for mod_key in selected_modules:
        m = AVAILABLE_MODULES[mod_key]
        lines.append(f"- **{m['name']}**: {m['value']}")

    lines.extend([
        "",
        "---",
        "",
        "## 📋 Enforced Rules & Defense Protocols",
        "",
        "### Pillar 1: Code Persistence & Multi-Agent Transparency",
        "- **Rule 1 (Code Persistence)**: Never save executable code, plotting scripts, or data tools in temporary sandboxes. Save persistently in project directories (`scripts/`, `papers/<id>/`, `presentations/`).",
        "",
        "### Pillar 2: Academic Rigor & Tone Defense",
        "- **Rule 2 (Anti-Hyperbole)**: Strictly prohibit marketing buzzwords (e.g., '军工级', '神级表现', '革命性颠覆'). Quantitative claims must have experimental backing.",
        r"- **Rule 3 (Chemical Formulas & Indices)**: Chemical formulas must be subscripted ($\mathrm{CO_2}$, $\mathrm{Li_3N}$); ions superscripted ($\mathrm{Li}^+$, $\mathrm{TFSI}^-$); scientific notation exponents properly formatted.",
        "",
        "### Pillar 3: Zero-Hallucination Source Truth Protocol",
        "- **Rule 4 (PDF Physical Extraction First)**: Physically extract original PDF text (`raw_paper_text.txt`) using pymupdf before analyzing any paper. Labeling text as 'Original' requires verbatim matching.",
        "- **Rule 5 (3-Way Cross-Verification)**: Verify axis extrema/units, curve colors/legends, and textual claims against data curves without discrepancies.",
        "- **Rule 6 (Mandatory Ground Truth Audit Report)**: For literature analysis or PPT creation, deliver a companion `ground_truth_audit_report.md` documenting exact page/paragraph/figure numbers.",
        "- **Rule 7 (Zero Hallucinated Citations)**: Never guess or synthesize DOIs, author names, journal titles, or figure references.",
    ])

    if has_pptx:
        lines.extend([
            "",
            "### Pillar 4: Academic Presentation & Visual Defense (Module: pptx)",
            "- **Rule 8 (Pre-Delivery Visual Self-Audit)**: NEVER declare 'done' simply because code compiled. Automatically export slides to high-res PNGs and visually inspect for text overflow, card collisions, and occluded figures before delivery.",
            "- **Rule 9 (100% Figure-Text Consistency)**: Numbers, units, durations, and subpanel letters on slides must strictly match what is visibly displayed on screen. No ghost subpanel references.",
            "- **Rule 10 (Removal of Extraction Tags)**: Slide titles must be pure scientific conclusions. Never include scraping tags like `(Figure 4a-c)` in titles.",
            "- **Rule 11 (Dual-Font Separation)**: English letters and digits must use **Times New Roman**; Chinese text must use **微软雅黑** via explicit OpenXML declaration.",
            "- **Rule 12 (Defensive Slide Layouts)**: Use flat white rectangular containers (`MSO_SHAPE.RECTANGLE`) with subtle borders; vertical top-alignment; 20%-30% vertical breathing room.",
            "- **Rule 13 (Speaker Notes vs. Screen Isolation)**: Slide screens display ONLY figures and concise claims visible to the audience. Supporting information (SI) details and deep mechanism proofs belong in Speaker Notes.",
        ])

    if has_figures:
        lines.extend([
            "",
            "### Pillar 5: Scientific Figure Standards & Domain Plotting (Module: figures)",
            "- **Rule 14 (No Unsolicited Sample Renaming)**: Never rename anonymous user sample IDs (e.g. `Sample 1`, `Control`, `A`) to assumed chemical formulations. Explicit user mappings are ground truth.",
            "- **Rule 15 (Four-Sided Box Frame Standards)**: 4-sided visible black spines (`linewidth = 2.5 ~ 3.0 pt`), top and right axes pure frame without ticks, bottom and left ticks point inward (`tick.direction: in`).",
            "- **Rule 16 (Domain-Specific Plotting Rules - DSC/FTIR/LSV)**:",
            r"  - *DSC*: Y-axis `Heat Flow (a.u.)`, hide numbers, Exo Up (melting as troughs), directly annotate $T_\mathrm{g}$ and $T_\mathrm{m}$ with dashed arrows, large baseline offset ($\ge 1.0\ \mathrm{a.u.}$).",
            r"  - *FTIR*: Y-axis `Transmittance (%, Offset)`, legends in baseline windows ($1800 \sim 2600\ \mathrm{cm^{-1}}$).",
            "  - *LSV*: Annotate onset decomposition potential directly on curve turn-up points.",
            "- **Rule 17 (Vector SVG Text Integrity & Zero `<tspan>`)**: Use clean Unicode symbols to avoid Matplotlib math splitting text into fragmented `<tspan>` tags. Normalize fonts to Times New Roman.",
            "- **Rule 18 (Decoupled Iteration Workflow)**: Never recompile an entire multi-panel master figure when fine-tuning a single subpanel.",
            "- **Rule 19 (SVG vs. 3D Model Division)**: Python curves for data; dedicated diffusion models for 3D conceptual mechanisms (never wireframe 3D hacks).",
        ])

    lines.extend([
        "",
        "### Pillar 6: Environment Defense & User Protection",
        "- **Rule 20 (Virtual Environment & File-First Execution)**:",
        "  - Always execute inside the dedicated virtual environment (`.venv` on Windows, `.venv-linux` on WSL) using `uv run` or isolated interpreter paths.",
        "  - On Windows, always write logic into standalone `.py` or `.ps1` files first instead of multiline terminal inline strings.",
        "  - User-finalized slides and files are strictly Read-Only.",
    ])

    if has_wsl:
        lines.extend([
            "",
            "### Pillar 7: Windows Host & WSL Hybrid Synergy (Module: wsl)",
            "- **Rule 21 (Dual-vEnv Physical Isolation)**: Windows host MUST use `<project_root>/.venv` (`.venv\\Scripts\\python.exe`); WSL Linux MUST use `<wsl_project_root>/.venv-linux` (`.venv-linux/bin/python`). Both share root `requirements.txt`. `.gitignore` must ignore `.venv*/`.",
            "- **Rule 22 (WSL-First & Zero-PowerShell Policy)**: Default to WSL Linux for file search, Git, batch scripts, and heavy Python computation. PowerShell is strictly reserved for Windows-exclusive PowerPoint COM automation.",
            "- **Rule 23 (Direct Bypass Sandbox for WSL)**: When spawning WSL processes on Windows, always bypass sandbox directly to eliminate token waste from `Wsl/E_ACCESSDENIED` or `CreateProcessSecurityEnvironment` failures.",
            "- **Rule 24 (Git NTFS Permission Sanitization)**: Inside WSL, execute `git config --global core.filemode false` and `core.autocrlf true` to prevent false 0755 permission modifications on NTFS mount points.",
        ])

    if has_nature:
        lines.extend([
            "",
            "---",
            "",
            "## 🤝 Nature Skills Synergy Workflow",
            "",
            "When used alongside the **Nature Skills suite**, this skill acts as the **Executive Quality & Defense Gate**:",
            "- **With `nature-paper2ppt`**: Guardrails enforces PNG visual self-audit, Times New Roman + 微软雅黑 dual-font injection, and SI speaker notes isolation.",
            "- **With `nature-figure`**: Guardrails enforces 4-sided box frames, zero `<tspan>` SVG text integrity, sample ID immutability, and DSC/FTIR conventions.",
            "- **With `nature-reader` / `nature-paper-card` / `nature-paper-xray`**: Guardrails enforces raw PDF hard text extraction, zero hallucinated citations, and companion ground truth audit reports.",
            "- **With `nature-writing` / `nature-polishing`**: Guardrails enforces anti-hyperbole vocabulary bans and chemical formula subscript formatting.",
        ])

    return "\n".join(lines) + "\n"


def generate_custom_agents_md(selected_modules: list[str], sys_info: dict) -> str:
    """根据选择的模块动态生成定制版 AGENTS.md"""
    # 直接基于已定制的 SKILL 规则生成可直接放置在项目根目录的 AGENTS.md
    skill_content = generate_custom_skill_md(selected_modules, sys_info)
    header = [
        "# AGENTS.md — Academic AI Pair Programming Protocol",
        "",
        f"This file provides context and ironclad guidelines for AI coding assistants working on this repository.",
        f"Target OS: {sys_info['desc']} | Active Modules: {', '.join(selected_modules)}",
        "",
        "---",
        "",
    ]
    # 去除 yaml frontmatter
    body = skill_content.split("---", 2)[-1].strip()
    return "\n".join(header) + body + "\n"


# ==================== 4. 协同安装 Nature Skills ====================

def scan_and_link_nature_skills(target_skills_dir: Path) -> list[str]:
    """扫描本地已有的 nature-skills 并提供协同挂载"""
    detected_nature = []
    # 候选位置 (跨平台通用路径)
    candidate_dirs = [
        Path.cwd() / ".agents" / "skills",
        Path.home() / ".gemini" / "antigravity" / "skills",
        Path.home() / ".agents" / "skills",
        SKILL_ROOT.parent.parent / ".agents" / "skills",
    ]
    
    found_src_dir = None
    for c in candidate_dirs:
        if c.exists() and any("nature-" in p.name for p in c.iterdir() if p.is_dir()):
            found_src_dir = c
            break

    if not found_src_dir:
        return []

    target_skills_dir.mkdir(parents=True, exist_ok=True)
    for skill_path in found_src_dir.iterdir():
        if skill_path.is_dir() and skill_path.name.startswith("nature-"):
            dest = target_skills_dir / skill_path.name
            if not dest.exists():
                try:
                    # 优先符号链接，若无权限则目录复制
                    if hasattr(os, "symlink"):
                        try:
                            os.symlink(skill_path, dest, target_is_directory=True)
                        except (OSError, NotImplementedError):
                            shutil.copytree(skill_path, dest)
                    else:
                        shutil.copytree(skill_path, dest)
                    detected_nature.append(skill_path.name)
                except Exception:
                    pass
            else:
                detected_nature.append(skill_path.name)

    return detected_nature


# ==================== 5. 交互式向导流程 ====================

def run_interactive_wizard():
    sys_info = detect_system()

    print("=================================================================")
    print(" 🛡️  Academic Agent Guardrails (AAG) 跨平台智能安装与定制向导")
    print("=================================================================")
    print(f"\n[1] 宿主操作系统检测:")
    print(f"    • 操作系统: {sys_info['desc']}")
    print(f"    • Python 运行时: {sys_info['python_version']} ({'虚拟环境中' if sys_info['in_venv'] else '系统环境'})")
    print(f"    • uv 包管理器: {'已安装 (' + sys_info['uv'] + ')' if sys_info['uv'] else '❌ 未检测到 (强烈建议安装: https://astral-sh/uv)'}")
    print(f"    • Git 版本控制: {'已安装' if sys_info['git'] else '❌ 未检测到'}")

    print(f"\n[2] 组件依赖检测:")
    if sys_info['type'] == "windows":
        print(f"    • PowerPoint COM 接口: {'✅ 支持 (可直接进行真机视觉自审)' if sys_info['has_powerpoint'] else '⚠️ 未检测到 Office PowerPoint'}")
        print(f"    • WSL 子系统检测: {'✅ 检测到已安装 WSL (支持 Windows + WSL 混合开发模式)' if sys_info['has_wsl'] else '○ 未检测到 WSL'}")
    elif sys_info['is_wsl']:
        print(f"    • WSL 运行环境: ✅ 当前正在 WSL2 (Linux) 内部执行 (支持跨系统 COM 调用)")
    else:
        print(f"    • LibreOffice 引擎: {'✅ 支持 (可用于无头 PPTX 渲染)' if sys_info['has_libreoffice'] else '⚠️ 未检测到 LibreOffice (如需视觉自审建议安装)'}")

    for pkg_name, installed in sys_info['pkgs'].items():
        status = "✅ 已安装" if installed else "○ 未安装 (按需自动安装)"
        print(f"    • Python 模块 [{pkg_name}]: {status}")

    print("\n-----------------------------------------------------------------")
    print(" [3] 组件分级与用处说明 (Component Breakdown)")
    print("-----------------------------------------------------------------")
    print(" 【必须组件 (Required Essentials)】:")
    print(f"   • {AVAILABLE_MODULES['core']['name']}")
    print(f"     用处: {AVAILABLE_MODULES['core']['value']}")
    print(f"     内容: {AVAILABLE_MODULES['core']['description']}")

    print("\n 【可选组件 (Optional Modules - 可根据科研需求自由定制)】:")
    for key, mod in AVAILABLE_MODULES.items():
        if key == "core":
            continue
        print(f"\n   [{key}] {mod['name']}")
        print(f"       • 核心用处: {mod['value']}")
        print(f"       • 规则覆盖: {mod['description']}")
        if "system_notes" in mod and sys_info['type'] in mod["system_notes"]:
            print(f"       • 本系统适配: {mod['system_notes'][sys_info['type']]}")

    print("\n-----------------------------------------------------------------")
    print(" [4] 请选择您要激活的可选组件 (多选用逗号分隔，默认全选 1,2,3,4,5):")
    print("   1. pptx    - PPTX 汇报真机视觉自审与双字体排版")
    print("   2. figures - 顶刊科研图表坐标系与材料物性绘图标准")
    print("   3. auditor - 学术严谨度与化学式自动化扫描器")
    print("   4. nature  - Nature Skills 深度协同路由 (搭配 nature-skills 套件)")
    print("   5. wsl     - Windows + WSL 跨系统混合协作套件 (双虚拟环境+Git防污染)")
    print("-----------------------------------------------------------------")

    user_choice = input(" 请输入选择 [回车默认全选 / 1,2 / 1,2,5 等]: ").strip()
    selected_modules = ["core"]

    mapping = {
        "1": "pptx",
        "pptx": "pptx",
        "2": "figures",
        "figures": "figures",
        "3": "auditor",
        "auditor": "auditor",
        "4": "nature",
        "nature": "nature",
        "5": "wsl",
        "wsl": "wsl",
    }

    if not user_choice:
        selected_modules.extend(["pptx", "figures", "auditor", "nature"])
        if sys_info['type'] == "windows" or sys_info['is_wsl']:
            selected_modules.append("wsl")
    else:
        for part in user_choice.replace("，", ",").split(","):
            part = part.strip()
            if part in mapping:
                mod_name = mapping[part]
                if mod_name not in selected_modules:
                    selected_modules.append(mod_name)

    print(f"\n✅ 您已选择激活模块: {[AVAILABLE_MODULES[m]['name'] for m in selected_modules]}")

    # 询问安装目标路径
    default_target = Path.home() / ".gemini" / "antigravity" / "skills" / "academic-agent-guardrails"
    print(f"\n[5] 请选择安装目标位置:")
    print(f"   [1] 个人全局 Agent 技能目录 (推荐): {default_target}")
    print(f"   [2] 当前项目根目录 (作为项目级守则 AGENTS.md)")
    print(f"   [3] 自定义目录")

    target_choice = input(" 请输入选择 [1/2/3, 默认 1]: ").strip()
    if target_choice == "2":
        install_target = Path.cwd()
        as_project_root = True
    elif target_choice == "3":
        custom_p = input(" 请输入自定义目标路径: ").strip()
        install_target = Path(custom_p).resolve()
        as_project_root = False
    else:
        install_target = default_target
        as_project_root = False

    install_configured_skill(selected_modules, install_target, sys_info, as_project_root)


# ==================== 6. 执行安装与交付 ====================

def install_configured_skill(selected_modules: list[str], target_dir: Path, sys_info: dict, as_project_root: bool = False):
    print(f"\n🚀 开始构建并安装定制版守则至: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. 生成定制版 SKILL.md
    custom_skill = generate_custom_skill_md(selected_modules, sys_info)
    (target_dir / "SKILL.md").write_text(custom_skill, encoding="utf-8")
    print("  ✓ 已生成定制版 SKILL.md (根据所选模块裁剪)")

    # 2. 生成定制版 AGENTS.md (或 template)
    custom_agents = generate_custom_agents_md(selected_modules, sys_info)
    if as_project_root:
        (target_dir / "AGENTS.md").write_text(custom_agents, encoding="utf-8")
        print("  ✓ 已生成项目级 AGENTS.md")
    else:
        (target_dir / "AGENTS.template.md").write_text(custom_agents, encoding="utf-8")
        print("  ✓ 已生成 AGENTS.template.md")

    # 3. 复制对应的支撑脚本
    target_scripts = target_dir / "scripts"
    target_scripts.mkdir(parents=True, exist_ok=True)

    # 基础脚本
    if (SCRIPT_DIR / "sync_agents_to_opensource.py").exists():
        shutil.copy2(SCRIPT_DIR / "sync_agents_to_opensource.py", target_scripts / "sync_agents_to_opensource.py")

    if "pptx" in selected_modules:
        if (SCRIPT_DIR / "export_slides.ps1").exists():
            shutil.copy2(SCRIPT_DIR / "export_slides.ps1", target_scripts / "export_slides.ps1")
        if (SCRIPT_DIR / "apply_dual_fonts.py").exists():
            shutil.copy2(SCRIPT_DIR / "apply_dual_fonts.py", target_scripts / "apply_dual_fonts.py")
        print("  ✓ 已部署 PPTX 视觉自审与双字体注入工具")

    if "auditor" in selected_modules:
        if (SCRIPT_DIR / "scan_academic_rigor.py").exists():
            shutil.copy2(SCRIPT_DIR / "scan_academic_rigor.py", target_scripts / "scan_academic_rigor.py")
        print("  ✓ 已部署学术严谨性与格式合规审查器")

    # 4. 复制模板
    target_templates = target_dir / "templates"
    if TEMPLATES_DIR.exists():
        target_templates.mkdir(parents=True, exist_ok=True)
        for t in TEMPLATES_DIR.iterdir():
            shutil.copy2(t, target_templates / t.name)
        print("  ✓ 已复制文献事实审计与环境防御模板")

    # 5. 生成依赖清单
    required_deps = ["pymupdf"]
    if "pptx" in selected_modules:
        required_deps.append("python-pptx")
    if "figures" in selected_modules:
        required_deps.extend(["matplotlib", "seaborn", "scipy"])

    req_file = target_dir / "requirements.txt"
    req_file.write_text("\n".join(required_deps) + "\n", encoding="utf-8")
    print(f"  ✓ 已生成适配依赖清单 requirements.txt ({', '.join(required_deps)})")

    # 6. 处理 Nature Skills 协同挂载
    if "nature" in selected_modules:
        skills_container = target_dir.parent if not as_project_root else target_dir / ".agents" / "skills"
        linked = scan_and_link_nature_skills(skills_container)
        if linked:
            print(f"  ✓ 成功关联协同 Nature Skills ({len(linked)} 个技能: {', '.join(linked[:5])}...)")
        else:
            print("  ℹ Nature Skills: 可选生态。已在守则中配置协同路由，后续放入 .agents/skills 即可直接协同生效。")

    # 7. 处理 WSL 混合开发防护
    if "wsl" in selected_modules:
        if as_project_root:
            gitignore_path = target_dir / ".gitignore"
            if gitignore_path.exists():
                gi_content = gitignore_path.read_text(encoding="utf-8", errors="replace")
                if ".venv*/" not in gi_content and ".venv-linux" not in gi_content:
                    gitignore_path.write_text(gi_content.rstrip() + "\n\n# Dual vEnv (Windows & WSL)\n.venv*/\n", encoding="utf-8")
                    print("  ✓ 已在 .gitignore 中配置 .venv*/ (防止 Windows/WSL 虚拟环境混淆入库)")
        print("  ✓ 已启用 Windows + WSL 跨系统混合协作防御规则 (Rule 21-24)")

    print("\n=================================================================")
    print(" 🎉 Academic Agent Guardrails 安装与定制完成！")
    print(f" 📂 目标路径: {target_dir}")
    print(" 💡 建议执行依赖安装 (现代化 uv 极速安装):")
    print(f"    uv pip install -r \"{req_file}\"")
    if "wsl" in selected_modules:
        print("\n 🐧 WSL 跨系统混合开发配置贴士:")
        print("    • WSL 内部创建独立虚拟环境: uv venv --python 3.12 .venv-linux && uv pip install -r requirements.txt")
        print("    • WSL 内部消除 NTFS 权限假修改: git config --global core.filemode false")
        print("    • WSL 跨系统调用 PowerPoint 导图: powershell.exe -File scripts/export_slides.ps1")
    print("=================================================================\n")


# ==================== 7. 主入口与命令行解析 ====================

def main():
    parser = argparse.ArgumentParser(description="Academic Agent Guardrails 跨平台定制安装工具")
    parser.add_argument("--target", help="目标安装目录路径 (留空进入交互向导)")
    parser.add_argument("--modules", help="启用的模块列表，逗号分隔 (如 core,pptx,figures,nature)")
    parser.add_argument("--preset", choices=["minimal", "paper", "presentation", "full"], help="预设配置组合")
    parser.add_argument("--as-root", action="store_true", help="直接作为项目根目录部署 AGENTS.md")

    args = parser.parse_args()

    if not args.target and not args.modules and not args.preset:
        run_interactive_wizard()
        return

    sys_info = detect_system()

    if args.preset == "minimal":
        selected_modules = ["core"]
    elif args.preset == "paper":
        selected_modules = ["core", "figures", "auditor", "nature"]
    elif args.preset == "presentation":
        selected_modules = ["core", "pptx", "auditor", "nature"]
    elif args.preset == "full":
        selected_modules = ["core", "pptx", "figures", "auditor", "nature"]
        if sys_info['type'] == "windows" or sys_info['is_wsl']:
            selected_modules.append("wsl")
    elif args.modules:
        selected_modules = ["core"]
        for m in args.modules.split(","):
            m = m.strip().lower()
            if m in AVAILABLE_MODULES and m not in selected_modules:
                selected_modules.append(m)
    else:
        selected_modules = ["core", "pptx", "figures", "auditor", "nature"]

    target_dir = Path(args.target).resolve() if args.target else Path.cwd()
    install_configured_skill(selected_modules, target_dir, sys_info, args.as_root)


if __name__ == "__main__":
    main()
