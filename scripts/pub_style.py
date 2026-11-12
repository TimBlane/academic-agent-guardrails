"""
Publication Plotting Style & Post-Processing Guardrail:
Encapsulates top-tier journal standards established in AGENTS.md (Rules 15-20):
- 4-sided closed box frame (top, bottom, left, right 3.0 pt black spines)
- Top & right axes have NO tick marks (xtick.top=False, ytick.right=False)
- Inward ticks on bottom & left (tick.direction='in')
- Times New Roman Bold across all text and numbers
- Zero <tspan> clean SVG export with automatic font post-processing
"""

import os
import re
import sys
import time
import tempfile
import matplotlib as mpl
import matplotlib.pyplot as plt

os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'matplotlib_pub')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def set_pub_style(extra_params=None):
    """Configures matplotlib rcParams according to top-tier journal standards."""
    params = {
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
        'font.weight': 'bold',
        'axes.labelweight': 'bold',
        'axes.titleweight': 'bold',
        'figure.titleweight': 'bold',
        'mathtext.fontset': 'custom',
        'mathtext.rm': 'Times New Roman:bold',
        'mathtext.it': 'Times New Roman:bold:italic',
        'mathtext.bf': 'Times New Roman:bold',
        'font.size': 28.0,
        'axes.labelsize': 36.0,
        'xtick.labelsize': 28.0,
        'ytick.labelsize': 28.0,
        'legend.fontsize': 22.0,
        'axes.linewidth': 3.0,          # 3 pt bounding box spine
        'axes.spines.top': True,         # 4-sided full box frame
        'axes.spines.right': True,
        'axes.spines.bottom': True,
        'axes.spines.left': True,
        'xtick.direction': 'in',         # Inward ticks
        'ytick.direction': 'in',
        'xtick.top': False,              # NO ticks on top spine (line only)
        'ytick.right': False,            # NO ticks on right spine (line only)
        'xtick.major.size': 9.0,
        'xtick.major.width': 3.0,
        'ytick.major.size': 9.0,
        'ytick.major.width': 3.0,
        'xtick.major.pad': 10.0,
        'ytick.major.pad': 10.0,
        'xtick.minor.size': 5.0,
        'xtick.minor.width': 2.0,
        'ytick.minor.size': 5.0,
        'ytick.minor.width': 2.0,
        'xtick.minor.visible': True,
        'ytick.minor.visible': True,
        'svg.fonttype': 'none',          # Editable vector text in SVG
        'pdf.fonttype': 42,              # Editable TrueType fonts in PDF
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.15,
    }
    if extra_params:
        params.update(extra_params)
    mpl.rcParams.update(params)


def safe_save_clean(fig, filepath, **kwargs):
    """
    Saves figure with file-lock retry, and post-processes SVGs to remove
    fragmented font families and enforce pure Times New Roman.
    """
    for attempt in range(6):
        try:
            fig.savefig(filepath, **kwargs)
            break
        except OSError:
            time.sleep(0.4)

    if filepath.endswith('.svg') and os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            content = re.sub(r"font-family:\s*['\"][^'\"]*STIXGeneral[^'\"]*['\"]", "font-family: 'Times New Roman'", content)
            content = re.sub(r"font-family:\s*['\"][^'\"]*DejaVu[^'\"]*['\"]", "font-family: 'Times New Roman'", content)
            content = re.sub(r"font-family:\s*'Times New Roman',\s*'DejaVu Serif',\s*serif", "font-family: 'Times New Roman'", content)
            content = re.sub(r'font-family="STIXGeneral"', 'font-family="Times New Roman"', content)
            content = re.sub(r'font-family="DejaVu Sans"', 'font-family="Times New Roman"', content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Warning cleaning SVG {filepath}: {e}")


def annotate_curve_point(ax, text, xy, xytext, color, arrowstyle='->', ls='--', lw=2.0, fontsize=18):
    """
    Adds a standardized dashed arrow annotation pointing to a specific curve feature
    (e.g., onset voltage, Tg transition, or Tm melting trough).
    """
    ax.annotate(text, xy=xy, xytext=xytext,
                arrowprops=dict(arrowstyle=arrowstyle, color=color, lw=lw, ls=ls),
                fontsize=fontsize, fontweight='bold', fontfamily='Times New Roman', color=color)
