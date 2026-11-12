#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
install.py — Academic Agent Guardrails v2.0.0 模块化与跨平台定制安装工具
----------------------------------------------------------------------------
功能：
1. 智能检测当前操作系统（Windows / WSL2 / macOS / Linux）与环境依赖；
2. 明确区分必须组件（Layer 0 核心守则）与可选组件（Layer 1 领域子 Skill 与配套工具），
   并针对用户操作系统说明每个可选组件的用处与依赖；
3. 根据用户选择的组件，部署对应 Layer 1 子 Skill（group-meeting-pptx /
   scientific-plotting-svg / paper-bilingual-reader）、pub_style.py 与退出码 0 门禁脚本，
   并动态生成严格满足 <= 22,000 字节上限的定制版 SKILL.md 与 AGENTS(.template).md；
4. 识别并说明协同搭配的 Nature Skills（如 nature-figure, nature-paper2ppt, nature-reader 等），
   支持一键软链/挂载到目标 Agent 技能库。

使用方式：
    # 交互式向导（推荐）：
    python scripts/install.py

    # 命令行指定配置：
    python scripts/install.py --target ~/.gemini/antigravity/skills/academic-agent-guardrails --preset full
    python scripts/install.py --target ./my_project --as-root --modules core,reader,pptx,figures,wsl
    python scripts/install.py --target ./test_dir --preset minimal
"""

import argparse
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SOURCE_SUBSKILLS_DIR = SKILL_ROOT / "skills"
TEMPLATES_DIR = SKILL_ROOT / "templates"
AGENTS_MAX_BYTES = 22_000


# ==================== 1. 系统与依赖检测 ====================

def _detect_windows_powerpoint() -> bool:
    """Checks for installed Microsoft PowerPoint on Windows via registry without launching COM GUI."""
    try:
        import winreg  # type: ignore

        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                with winreg.OpenKey(
                    hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\powerpnt.exe"
                ):
                    return True
            except OSError:
                continue
    except Exception:
        pass
    return bool(shutil.which("powerpnt"))


def detect_system() -> dict:
    os_name = platform.system().lower()
    is_wsl = False
    has_wsl = False

    if os_name == "windows":
        system_type = "windows"
        system_desc = f"Windows ({platform.release()})"
        try:
            wsl_check = subprocess.run(
                ["wsl.exe", "-l", "-q"], capture_output=True, text=True, errors="replace", timeout=3
            )
            has_wsl = wsl_check.returncode == 0 and bool(wsl_check.stdout.strip())
        except Exception:
            has_wsl = False
    elif os_name == "darwin":
        system_type = "macos"
        system_desc = f"macOS ({platform.mac_ver()[0]})"
    else:
        system_type = "linux"
        try:
            proc_ver = Path("/proc/version")
            if proc_ver.exists():
                ver_text = proc_ver.read_text(encoding="utf-8", errors="replace").lower()
                if "microsoft" in ver_text or "wsl" in ver_text:
                    is_wsl = True
        except Exception:
            pass
        system_desc = f"Linux (WSL2: {platform.release()})" if is_wsl else f"Linux ({platform.release()})"

    python_version = platform.python_version()
    in_venv = sys.prefix != sys.base_prefix
    uv_path = shutil.which("uv")
    git_path = shutil.which("git")

    has_powerpoint = _detect_windows_powerpoint() if system_type == "windows" else False
    has_libreoffice = False if system_type == "windows" else bool(
        shutil.which("soffice") or shutil.which("libreoffice")
    )

    installed_pkgs = {}
    for pkg in ["pymupdf", "pptx", "PIL", "matplotlib", "seaborn", "scipy"]:
        found = importlib.util.find_spec(pkg) is not None
        if not found and pkg == "pymupdf":
            found = importlib.util.find_spec("fitz") is not None
        installed_pkgs[pkg] = found

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


# ==================== 2. 组件分级定义与说明 ====================

AVAILABLE_MODULES = {
    "core": {
        "name": "Layer 0 全局高危底线守则 (Core Guardrails)",
        "required": True,
        "description": "持久化目录规范 (Rule 1)、WSL-First/uv 隔离与 File-First (Rule 2)、先图后文零幻觉与反夸大 (Rule 3)、样品命名与引文保真 (Rule 4)、双字体/上下标/r\"\"\"...\"\"\" 原始字符串防护 (Rule 5)、<= 22 KB 体积硬上限防截断。",
        "value": "必须组件。为所有 AI 科研任务建立简洁且绝不被 IDE 截断的核心护栏。",
        "deps": ["pymupdf"],
    },
    "reader": {
        "name": "Layer 1 子技能: 论文双语精读与源码溯源审计 (paper-bilingual-reader)",
        "required": False,
        "subskill": "paper-bilingual-reader",
        "gate": "audit_markdown_suite.py",
        "description": "pymupdf 物理全文/SI 提取、先图后文（7Li NMR 低场方向/背底相对论/3D 连续谱）、paper.md + source_map.json 双语构建、全链路闭环纠偏，以及退出码 0 的 audit_markdown_suite.py 门禁。",
        "value": "文献精读、双语对照翻译、参数核对必备！彻底消除控制字符转义损坏（\\approx -> \\x07pprox）与跨文件事实脱节。",
        "deps": ["pymupdf"],
    },
    "pptx": {
        "name": "Layer 1 子技能: 组会与学术汇报 PPTX 视觉门禁 (group-meeting-pptx)",
        "required": False,
        "subskill": "group-meeting-pptx",
        "gate": "verify_group_pptx.py",
        "description": "16:9 组会版式、无横幅数据页体例（图 X：...，禁用 21 pt 顶部横幅与 【】）、Slide 0 / Slide -1 双字体双重豁免、图片原比例锁、平直微灰框 #CFD8DC、Speaker Notes 物理隔离、COM PNG 自审及退出码 0 的 verify_group_pptx.py 门禁。",
        "value": "制作组会 PPT、文献汇报、答辩演示必备！拦截比例拉伸、字体污染封面尾页、数据页堆砌大字报。",
        "deps": ["python-pptx", "Pillow"],
        "system_notes": {
            "windows": "配合 scripts/export_slides.ps1 调用本地 Microsoft PowerPoint COM 极速导出全页 PNG。",
            "macos": "建议安装 LibreOffice (soffice --headless) 与 poppler (pdftoppm) 进行无头 PNG 视觉自审。",
            "linux": "WSL2 可通过 powershell.exe 桥接宿主 COM 导图；纯 Linux 建议配置 LibreOffice + pdftoppm。",
        },
    },
    "figures": {
        "name": "Layer 1 子技能: 顶刊科研绘图与零 <tspan> SVG (scientific-plotting-svg)",
        "required": False,
        "subskill": "scientific-plotting-svg",
        "gate": "audit_svg_postprocess.py",
        "description": "导入共享样式基线 scripts/pub_style.py；4 面纯黑围框（3.0–4.0 pt）+ 朝内刻度；DSC/FTIR/LSV/Dual-Y CE 气隙与 Li||Li 对称电池放大框规范；独立生成 3D 机理图 Prompt 并以退出码 0 门禁 audit_svg_postprocess.py 确保零 <tspan> 与 Times New Roman。",
        "value": "科研出图必备！保证导出矢量 SVG 可在 Illustrator/CorelDRAW 中单字直编，不再被 mathtext 切碎成几十个 <tspan>。",
        "deps": ["matplotlib", "seaborn", "scipy"],
    },
    "auditor": {
        "name": "独立静态严谨性文本扫描器 (Standalone Rigor Scanner)",
        "required": False,
        "description": "部署轻量单文件脚本 scripts/scan_academic_rigor.py，用于对任意零散 Markdown/讲稿进行去营销词与化学式上下标快速巡检。",
        "value": "无需整套 paper.md + source_map.json 时也能随时随地执行一键文本体检。",
        "deps": [],
    },
    "nature": {
        "name": "Nature Skills 生态深度协同 (Nature Skills Synergy)",
        "required": False,
        "description": "配置本守则与 Nature 系列技能（nature-paper2ppt, nature-figure, nature-reader, nature-paper-xray, nature-writing）的分层协同与优先级规则。",
        "value": "强烈推荐搭配！让通用 Nature 技能负责广度草稿，Layer 1 工作区守则与门禁脚本把控最终交付红线。",
        "deps": [],
    },
    "wsl": {
        "name": "Windows + WSL2 跨系统混合开发防御 (WSL Hybrid Synergy)",
        "required": False,
        "description": "WSL-First 指令准则、双虚拟环境隔离 (.venv vs .venv-linux)、Direct Bypass 沙盒规避 Wsl/E_ACCESSDENIED、Git NTFS 权限锁定 (core.filemode false / core.autocrlf true)。",
        "value": "Windows 宿主与 WSL 混用必备！防止 NTFS 假修改、跨系统二进制混跑与沙盒失败损耗 Token。",
        "deps": [],
    },
}


# ==================== 3. 动态生成 v2.0.0 模块化定制文档 ====================

def _skill_rel_prefix(as_project_root: bool) -> str:
    return ".agents/skills" if as_project_root else "skills"


def generate_custom_skill_md(selected_modules: list[str], sys_info: dict, as_project_root: bool = False) -> str:
    """根据用户选定模块动态构建 Layer 0 + Layer 1 定制版 SKILL.md"""
    prefix = _skill_rel_prefix(as_project_root)
    has_reader = "reader" in selected_modules
    has_pptx = "pptx" in selected_modules
    has_figures = "figures" in selected_modules
    has_auditor = "auditor" in selected_modules
    has_nature = "nature" in selected_modules
    has_wsl = "wsl" in selected_modules or sys_info.get("is_wsl") or sys_info.get("has_wsl")

    active_subskills = [
        AVAILABLE_MODULES[m]["subskill"]
        for m in ("pptx", "figures", "reader")
        if m in selected_modules
    ]

    lines = [
        "---",
        "name: academic-agent-guardrails",
        "description: v2.0.0 modular 2-tier academic research, presentation, scientific plotting, and literature guardrails configured for this workspace.",
        "---",
        "",
        f"# Academic Agent Guardrails v2.0.0 ({sys_info['desc']})",
        "",
        f"Deployed modules: **{', '.join(selected_modules)}** | Layer-1 sub-skills active: **{len(active_subskills)}**.",
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
        "## 📋 Layer 0: Cross-Task High-Voltage Rules (Rules 1–7)",
        "",
        "- **Rule 1｜Code & Asset Persistence**: Persist reusable scripts in `scripts/`, paper assets in `papers/<paper_id>/`, decks in `presentations/`, and local workflows in `.agents/skills/`. Never leave logic in temporary sandboxes.",
    ])

    if has_wsl:
        lines.append(
            "- **Rule 2｜WSL-First, `uv` Isolation & File-First**: Prefer WSL when available (`core.filemode false`, `core.autocrlf true`); reserve PowerShell for Windows COM (`scripts/export_slides.ps1`). Windows uses `.venv/Scripts/python.exe`; WSL uses `.venv-linux/bin/python`. Always write standalone UTF-8 `.py`/`.sh` files (never inline multiline `python -c`)."
        )
    else:
        lines.append(
            "- **Rule 2｜`uv` Environment Isolation & File-First**: Execute Python exclusively via `.venv` (`uv run` or `.venv/Scripts/python.exe` / `.venv/bin/python`). Never pollute global Python. Never inline multiline terminal code; write standalone UTF-8 `.py`/`.sh` scripts first."
        )

    lines.extend([
        r'- **Rule 3｜Source Truth & Anti-Hyperbole**: Hard-extract PDF/SI text via `pymupdf` first; visually inspect cropped panels before writing; obey `7Li NMR` downfield sign (`ppm` up = deshielding), XPS/FTIR matrix relativity, and 3D gradient objectivity; ban marketing hype, ungrounded analogies, and unmeasured sensory claims; fix detected errors across all linked artifacts.',
        "- **Rule 4｜Sample Fidelity & Citation Zero-Fabrication**: Keep raw user sample IDs (`Sample 1–4`) unless given an explicit mapping. Cite only verified DOIs, journals, years, and figures.",
        r'- **Rule 5｜Dual Fonts, Subscripts & Raw Strings**: Apply `Times New Roman` (Latin/digits) + `微软雅黑` (Chinese) while exempting Cover (`Slide 0`) and Ending (`Slide -1`); format chemical stoichiometry/charges ($\mathrm{CO_2}$, $\mathrm{Li}^+$, $\mathrm{cm}^{-1}$); always write LaTeX-bearing Python generators using raw strings `r"""..."""`.',
        "- **Rule 6｜PPTX Safeguards & Notes Separation**: Respect user Read-Only locks on finalized decks; export slide PNGs via COM/LibreOffice and visually audit; lock image aspect ratio; use flat `#CFD8DC` rectangles with `20%–30%` breathing room; remove extraction tags; no `21 pt` top banners/`【】` on data slides (`图 X：...` instead); isolate SI details into Speaker Notes.",
        "",
        "---",
        "",
        "## 🧭 Rule 7: Layer 1 Sub-Skill Routing & Exit-0 Verification Gates",
        "",
    ])

    if active_subskills:
        lines.append("| Task Domain | Mandatory Sub-Skill | Deterministic Exit-0 Gate |")
        lines.append("| :--- | :--- | :--- |")
        if has_pptx:
            lines.append(
                f"| **Group-Meeting / Literature PPTX** | [`{prefix}/group-meeting-pptx/SKILL.md`]({prefix}/group-meeting-pptx/SKILL.md) | `{prefix}/group-meeting-pptx/scripts/verify_group_pptx.py` + `scripts/export_slides.ps1` |"
            )
        if has_figures:
            lines.append(
                f"| **Scientific Plots (DSC/FTIR/LSV/Dual-Y/SVG/3D)** | [`{prefix}/scientific-plotting-svg/SKILL.md`]({prefix}/scientific-plotting-svg/SKILL.md) | `{prefix}/scientific-plotting-svg/scripts/audit_svg_postprocess.py` + `scripts/pub_style.py` |"
            )
        if has_reader:
            lines.append(
                f"| **Paper Extraction, Bilingual Reader & Audit** | [`{prefix}/paper-bilingual-reader/SKILL.md`]({prefix}/paper-bilingual-reader/SKILL.md) | `{prefix}/paper-bilingual-reader/scripts/audit_markdown_suite.py` |"
            )
    else:
        lines.append("_(Minimal core deployment: no Layer 1 domain sub-skills selected. Re-run `scripts/install.py` to add `pptx`, `figures`, or `reader`.)_")

    if has_auditor:
        lines.extend([
            "",
            "### Standalone Rigor Audit",
            "Run `scripts/scan_academic_rigor.py <file.md>` for quick standalone banned-word & chemistry formatting checks.",
        ])

    if has_nature:
        lines.extend([
            "",
            "---",
            "",
            "## 🤝 Nature Skills Ecosystem Synergy",
            "",
            "Pair this guardrail package with `nature-*` skills (precedence rule: workspace Layer 1 sub-skills override generic templates when enabled):",
            "- `nature-paper2ppt` -> enforced by `group-meeting-pptx` (`verify_group_pptx.py` + visual PNG audit).",
            "- `nature-figure` -> enforced by `scientific-plotting-svg` (`scripts/pub_style.py` + `audit_svg_postprocess.py`).",
            "- `nature-reader` / `nature-paper-xray` / `nature-paper-card` -> enforced by `paper-bilingual-reader` (`audit_markdown_suite.py`).",
            "- `nature-writing` / `nature-polishing` -> enforced by Layer 0 Rule 3–5 (anti-hyperbole & chemistry indices).",
        ])

    return "\n".join(lines) + "\n"


def generate_custom_agents_md(selected_modules: list[str], sys_info: dict, as_project_root: bool = False) -> str:
    """生成严格 <= 22,000 字节的定制版 AGENTS.md / AGENTS.template.md"""
    skill_content = generate_custom_skill_md(selected_modules, sys_info, as_project_root=as_project_root)
    body = skill_content.split("---", 2)[-1].strip()
    header = [
        "# AGENTS.md — Academic Agent Guardrails v2.0.0",
        "",
        f"- **Target OS:** `{sys_info['desc']}` | **Active Modules:** `{', '.join(selected_modules)}`",
        f"- **Volume Hard-Cap (`<= {AGENTS_MAX_BYTES:,}` bytes):** Keep core cross-task guardrails in this file and domain templates/checklists inside `{'`.agents/skills/`' if as_project_root else '`skills/`'}`.",
        "",
        "---",
        "",
    ]
    result = "\n".join(header) + body + "\n"
    byte_len = len(result.encode("utf-8"))
    if byte_len > AGENTS_MAX_BYTES:
        raise RuntimeError(f"Generated AGENTS.md exceeds {AGENTS_MAX_BYTES} byte cap ({byte_len} bytes).")
    return result


# ==================== 4. 协同安装 Nature Skills ====================

def scan_and_link_nature_skills(target_skills_dir: Path) -> list[str]:
    """扫描本地已有的 nature-skills 并提供协同挂载"""
    detected_nature = []
    candidate_dirs = [
        Path.cwd() / ".agents" / "skills",
        Path.home() / ".gemini" / "antigravity" / "skills",
        Path.home() / ".agents" / "skills",
        SKILL_ROOT.parent.parent / ".agents" / "skills",
    ]

    found_src_dir = None
    for c in candidate_dirs:
        if c.exists() and any(p.is_dir() and p.name.startswith("nature-") for p in c.iterdir()):
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


def _deploy_subskill(subskill_name: str, dest_root: Path, as_project_root: bool) -> bool:
    src = SOURCE_SUBSKILLS_DIR / subskill_name
    if not src.exists():
        print(f"  ⚠ 未找到源子技能目录: {src}")
        return False

    dst = dest_root / subskill_name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # When deployed to <project>/.agents/skills/<name>/, adjust ../../scripts/ links to ../../../scripts/
    if as_project_root:
        for md_file in dst.rglob("*.md"):
            rel_parts = md_file.relative_to(dst).parts
            text = md_file.read_text(encoding="utf-8")
            if len(rel_parts) == 1:
                text = text.replace("(../../scripts/", "(../../../scripts/")
            elif len(rel_parts) == 2 and rel_parts[0] == "references":
                text = text.replace("(../../../scripts/", "(../../../../scripts/")
            md_file.write_text(text, encoding="utf-8")
    return True


# ==================== 5. 交互式向导流程 ====================

def run_interactive_wizard() -> None:
    sys_info = detect_system()

    print("=================================================================")
    print(" 🛡️  Academic Agent Guardrails v2.0.0 跨平台模块化安装向导")
    print("=================================================================")
    print("\n[1] 宿主操作系统检测:")
    print(f"    • 操作系统: {sys_info['desc']}")
    print(f"    • Python 运行时: {sys_info['python_version']} ({'虚拟环境中' if sys_info['in_venv'] else '系统环境'})")
    print(f"    • uv 包管理器: {'已安装 (' + sys_info['uv'] + ')' if sys_info['uv'] else '❌ 未检测到 (建议安装: https://astral.sh/uv)'}")
    print(f"    • Git 版本控制: {'已安装' if sys_info['git'] else '❌ 未检测到'}")

    print("\n[2] 组件依赖检测:")
    if sys_info["type"] == "windows":
        print(f"    • PowerPoint 本地套件: {'✅ 已安装 (支持 COM 导出 PNG)' if sys_info['has_powerpoint'] else '⚠️ 未检测到 Office PowerPoint'}")
        print(f"    • WSL 子系统检测: {'✅ 已安装 WSL (推荐启用 wsl 模块)' if sys_info['has_wsl'] else '○ 未检测到 WSL'}")
    elif sys_info["is_wsl"]:
        print("    • WSL 运行环境: ✅ 当前正在 WSL2 (Linux) 内部执行 (支持跨系统 COM 桥接)")
    else:
        print(f"    • LibreOffice 引擎: {'✅ 支持 (可用于无头 PPTX 渲染)' if sys_info['has_libreoffice'] else '⚠️ 未检测到 LibreOffice (PPTX 自审建议安装)'}")

    for pkg_name, installed in sys_info["pkgs"].items():
        status = "✅ 已安装" if installed else "○ 未安装 (写入 requirements.txt)"
        print(f"    • Python 模块 [{pkg_name}]: {status}")

    print("\n-----------------------------------------------------------------")
    print(" [3] 组件分级与用处说明 (Layer 0 必须 + Layer 1 可选子技能)")
    print("-----------------------------------------------------------------")
    print(" 【必须组件 (Required Essentials)】:")
    print(f"   • {AVAILABLE_MODULES['core']['name']}")
    print(f"     用处: {AVAILABLE_MODULES['core']['value']}")
    print(f"     覆盖: {AVAILABLE_MODULES['core']['description']}")

    print("\n 【可选组件 (Optional Modules — 按科研场景定制)】:")
    for key, mod in AVAILABLE_MODULES.items():
        if key == "core":
            continue
        print(f"\n   [{key}] {mod['name']}")
        print(f"       • 核心用处: {mod['value']}")
        print(f"       • 涵盖内容: {mod['description']}")
        if "system_notes" in mod and sys_info["type"] in mod["system_notes"]:
            print(f"       • 本系统适配: {mod['system_notes'][sys_info['type']]}")

    print("\n-----------------------------------------------------------------")
    print(" [4] 请选择要激活的可选组件 (逗号分隔，回车默认全选):")
    print("   1. reader  - 论文物理提取、双语精读 (paper-bilingual-reader) + audit_markdown_suite.py")
    print("   2. pptx    - 组会 PPTX 视觉门禁 (group-meeting-pptx) + verify_group_pptx.py")
    print("   3. figures - 顶刊科研绘图与零 <tspan> SVG (scientific-plotting-svg) + pub_style.py")
    print("   4. auditor - 轻量单文件文本合规扫描器 (scan_academic_rigor.py)")
    print("   5. nature  - Nature Skills 生态深度协同 (nature-figure/paper2ppt/reader 等)")
    print("   6. wsl     - Windows + WSL2 混合协作防御套件")
    print("-----------------------------------------------------------------")

    user_choice = input(" 请输入选择 [回车默认全选 / 例如 1,2,3 / 1,2,5,6]: ").strip()
    selected_modules = ["core"]

    mapping = {
        "1": "reader",
        "reader": "reader",
        "2": "pptx",
        "pptx": "pptx",
        "3": "figures",
        "figures": "figures",
        "4": "auditor",
        "auditor": "auditor",
        "5": "nature",
        "nature": "nature",
        "6": "wsl",
        "wsl": "wsl",
    }

    if not user_choice:
        selected_modules.extend(["reader", "pptx", "figures", "auditor", "nature"])
        if sys_info["type"] == "windows" or sys_info["is_wsl"]:
            selected_modules.append("wsl")
    else:
        for part in user_choice.replace("，", ",").split(","):
            part = part.strip().lower()
            if part in mapping and mapping[part] not in selected_modules:
                selected_modules.append(mapping[part])

    print(f"\n✅ 已选模块: {[AVAILABLE_MODULES[m]['name'] for m in selected_modules]}")

    default_target = Path.home() / ".gemini" / "antigravity" / "skills" / "academic-agent-guardrails"
    print("\n[5] 请选择安装目标位置:")
    print(f"   [1] 个人全局 Agent 技能目录 (推荐): {default_target}")
    print("   [2] 当前项目根目录 (部署 AGENTS.md + .agents/skills/)")
    print("   [3] 自定义目录")

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

def install_configured_skill(
    selected_modules: list[str], target_dir: Path, sys_info: dict, as_project_root: bool = False
) -> None:
    print(f"\n🚀 开始构建并部署 v2.0.0 模块化守则至: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. 生成定制版 SKILL.md (全局安装或技能根参考)
    if not as_project_root:
        custom_skill = generate_custom_skill_md(selected_modules, sys_info, as_project_root=False)
        (target_dir / "SKILL.md").write_text(custom_skill, encoding="utf-8")
        print("  ✓ 已生成定制版 SKILL.md (Layer 0 + Layer 1 路由)")

    # 2. 生成定制版 AGENTS.md / AGENTS.template.md (校验 <= 22,000 bytes)
    custom_agents = generate_custom_agents_md(selected_modules, sys_info, as_project_root=as_project_root)
    agents_bytes = len(custom_agents.encode("utf-8"))
    if as_project_root:
        (target_dir / "AGENTS.md").write_text(custom_agents, encoding="utf-8")
        print(f"  ✓ 已生成项目级 AGENTS.md ({agents_bytes} bytes <= {AGENTS_MAX_BYTES})")
    else:
        (target_dir / "AGENTS.template.md").write_text(custom_agents, encoding="utf-8")
        print(f"  ✓ 已生成 AGENTS.template.md ({agents_bytes} bytes <= {AGENTS_MAX_BYTES})")

    # 3. 部署 Layer 1 领域子技能 (skills/ 或 .agents/skills/)
    subskills_dest = (target_dir / ".agents" / "skills") if as_project_root else (target_dir / "skills")
    deployed_subskills: list[str] = []
    for mod_key in ("pptx", "figures", "reader"):
        if mod_key in selected_modules:
            subskill_name = AVAILABLE_MODULES[mod_key]["subskill"]
            if _deploy_subskill(subskill_name, subskills_dest, as_project_root=as_project_root):
                deployed_subskills.append(subskill_name)
                print(f"  ✓ 已部署 Layer 1 子技能: {subskills_dest / subskill_name}")

    # 4. 复制对应的共用工具脚本 scripts/
    target_scripts = target_dir / "scripts"
    target_scripts.mkdir(parents=True, exist_ok=True)

    if (SCRIPT_DIR / "sync_agents_to_opensource.py").exists():
        shutil.copy2(SCRIPT_DIR / "sync_agents_to_opensource.py", target_scripts / "sync_agents_to_opensource.py")

    if "pptx" in selected_modules:
        for fname in ("export_slides.ps1", "apply_dual_fonts.py"):
            if (SCRIPT_DIR / fname).exists():
                shutil.copy2(SCRIPT_DIR / fname, target_scripts / fname)
        print("  ✓ 已部署 PPTX 导出与双字体注入工具 (export_slides.ps1, apply_dual_fonts.py)")

    if "figures" in selected_modules:
        if (SCRIPT_DIR / "pub_style.py").exists():
            shutil.copy2(SCRIPT_DIR / "pub_style.py", target_scripts / "pub_style.py")
        print("  ✓ 已部署科研绘图共享样式基线 (scripts/pub_style.py)")

    if "auditor" in selected_modules:
        if (SCRIPT_DIR / "scan_academic_rigor.py").exists():
            shutil.copy2(SCRIPT_DIR / "scan_academic_rigor.py", target_scripts / "scan_academic_rigor.py")
        print("  ✓ 已部署独立严谨性文本扫描器 (scripts/scan_academic_rigor.py)")

    # 5. 复制模板
    target_templates = target_dir / "templates"
    if TEMPLATES_DIR.exists():
        target_templates.mkdir(parents=True, exist_ok=True)
        for t in TEMPLATES_DIR.iterdir():
            if t.is_file():
                shutil.copy2(t, target_templates / t.name)
        print("  ✓ 已复制文献审计与虚拟环境自检模板 (templates/)")

    # 6. 生成适配依赖清单 requirements.txt
    required_deps: list[str] = ["pymupdf"]
    if "pptx" in selected_modules:
        required_deps.extend(["python-pptx", "Pillow"])
    if "figures" in selected_modules:
        required_deps.extend(["matplotlib", "seaborn", "scipy"])

    # 去重保序
    required_deps = list(dict.fromkeys(required_deps))
    req_file = target_dir / "requirements.txt"
    req_file.write_text("\n".join(required_deps) + "\n", encoding="utf-8")
    print(f"  ✓ 已生成适配依赖清单 requirements.txt ({', '.join(required_deps)})")

    # 7. 处理 Nature Skills 协同挂载
    if "nature" in selected_modules:
        skills_container = (target_dir / ".agents" / "skills") if as_project_root else target_dir.parent
        linked = scan_and_link_nature_skills(skills_container)
        if linked:
            print(f"  ✓ 成功协同挂载 Nature Skills ({len(linked)} 个技能: {', '.join(linked[:5])}...)")
        else:
            print("  ℹ Nature Skills 推荐搭配: 已写入协同路由，后续可将 nature-figure / nature-paper2ppt / nature-reader 放入技能目录联动。")

    # 8. 处理 WSL 混合开发防护
    if "wsl" in selected_modules:
        if as_project_root:
            gitignore_path = target_dir / ".gitignore"
            if gitignore_path.exists():
                gi_content = gitignore_path.read_text(encoding="utf-8", errors="replace")
            else:
                gi_content = ""
            if ".venv*/" not in gi_content and ".venv-linux" not in gi_content:
                new_gi = (gi_content.rstrip() + "\n\n# Dual vEnv (Windows & WSL)\n.venv*/\n").lstrip()
                gitignore_path.write_text(new_gi, encoding="utf-8")
                print("  ✓ 已在 .gitignore 配置 .venv*/ (防止 Windows/WSL 虚拟环境冲突)")
        print("  ✓ 已启用 Windows + WSL2 混合协作防御规范")

    print("\n=================================================================")
    print(" 🎉 Academic Agent Guardrails v2.0.0 安装与定制完成！")
    print(f" 📂 目标路径: {target_dir}")
    if deployed_subskills:
        print(f" 🧩 已激活 Layer 1 子技能: {', '.join(deployed_subskills)}")
    print(" 💡 建议使用现代化 uv 初始化虚拟环境并安装依赖:")
    print(f'    uv venv --python 3.12 && uv pip install -r "{req_file}"')
    if "wsl" in selected_modules:
        print("\n 🐧 WSL2 混合开发配置贴士:")
        print("    • WSL 内部独立虚拟环境: uv venv --python 3.12 .venv-linux && uv pip install -r requirements.txt")
        print("    • 消除 NTFS 假权限修改: git config --global core.filemode false && git config --global core.autocrlf true")
        print("    • WSL 跨系统调用 PowerPoint 导图: powershell.exe -File scripts/export_slides.ps1")
    print("=================================================================\n")


# ==================== 7. 主入口与命令行解析 ====================

def main() -> None:
    parser = argparse.ArgumentParser(description="Academic Agent Guardrails v2.0.0 跨平台模块化定制安装工具")
    parser.add_argument("--target", help="目标安装目录路径 (留空进入交互向导)")
    parser.add_argument("--modules", help="启用的模块列表，逗号分隔 (如 core,reader,pptx,figures,auditor,nature,wsl)")
    parser.add_argument("--preset", choices=["minimal", "paper", "presentation", "full"], help="预设配置组合")
    parser.add_argument("--as-root", action="store_true", help="直接部署为项目根目录 (生成 AGENTS.md 与 .agents/skills/)")

    args = parser.parse_args()

    if not args.target and not args.modules and not args.preset:
        run_interactive_wizard()
        return

    sys_info = detect_system()

    if args.preset == "minimal":
        selected_modules = ["core"]
    elif args.preset == "paper":
        selected_modules = ["core", "reader", "figures", "auditor", "nature"]
    elif args.preset == "presentation":
        selected_modules = ["core", "reader", "pptx", "auditor", "nature"]
    elif args.preset == "full":
        selected_modules = ["core", "reader", "pptx", "figures", "auditor", "nature"]
        if sys_info["type"] == "windows" or sys_info["is_wsl"]:
            selected_modules.append("wsl")
    elif args.modules:
        selected_modules = ["core"]
        for m in args.modules.split(","):
            m = m.strip().lower()
            if m in AVAILABLE_MODULES and m not in selected_modules:
                selected_modules.append(m)
    else:
        selected_modules = ["core", "reader", "pptx", "figures", "auditor", "nature"]

    target_dir = Path(args.target).resolve() if args.target else Path.cwd()
    install_configured_skill(selected_modules, target_dir, sys_info, args.as_root)


if __name__ == "__main__":
    main()
