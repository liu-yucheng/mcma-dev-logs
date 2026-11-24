"""Draw the slice view of Part 4 and the comparison of the four orders.

The left panel shows the disk that the plane at x cuts from E.  Its radius is
sqrt(x)/2 and its area is pi*x/4, so the integral in the order dx dy dz is a single
integral of x*pi*x/4 over 0 <= x <= 4.

The right panel lists the value that each independent method reports.  Every method
must agree with 16*pi/3.

The script writes the figure to code/figures/part4_figure1.png.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

EXPECTED_VALUE: float = 16.0 * math.pi / 3.0
"""The value that the tutorial derives, about 16.755160819."""

FIGURE_DPI: int = 200
"""Resolution of the written image in dots per inch."""

COLOR_CURVE: str = "#2f5d8a"
"""Color of the radius curve."""

COLOR_ACCENT: str = "#c8863c"
"""Color of the exact value line and the highlighted bar."""

METHOD_NAMES: tuple[str, ...] = (
    "cylindrical\n(3 quadratures)",
    "disk slices\n(1 quadrature)",
    "cylindrical\nshells",
    "point sample\n(4 million)",
)
"""Labels of the four methods in the right panel."""

METHOD_VALUES: tuple[float, ...] = (
    16.755160819145562,
    16.755160819145562,
    16.755160819145562,
    16.772078,
)
"""Values that the four methods report, taken from the verification scripts."""

FIGURE_PATH: Path = Path(__file__).resolve().parent / "figures" / "part4_figure1.png"
"""Output path of the figure."""


def apply_style() -> None:
    """Set a consistent style for the figure."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Cambria", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#333333",
        "figure.facecolor": "white",
    })


def draw_slice_radius(axes: plt.Axes) -> None:
    """Draw the radius of the slice as a function of x.

    Args:
        axes: The axes of the left panel.
    """
    x_values = np.linspace(0.0, PLANE_POSITION, 400)
    radius_values = np.sqrt(x_values / PARABOLOID_COEFFICIENT)
    axes.fill_between(x_values, 0.0, radius_values, color=COLOR_CURVE, alpha=0.18,
                      linewidth=0.0)
    axes.plot(x_values, radius_values, color=COLOR_CURVE, linewidth=2.2)
    axes.plot([2.0], [math.sqrt(2.0) / 2.0], marker="o", markersize=5.0, color=COLOR_ACCENT,
              zorder=5)
    axes.annotate(r"$r = \dfrac{\sqrt{x}}{2}$", xy=(2.0, math.sqrt(2.0) / 2.0),
                  xytext=(0.55, 0.82), color=COLOR_CURVE, fontsize=11.5,
                  arrowprops={"arrowstyle": "->", "color": COLOR_CURVE, "linewidth": 0.9})
    axes.annotate(r"area $= \pi x / 4$", xy=(2.6, 0.30), fontsize=11, color="#8a5a1c")
    axes.set_xlim(0.0, PLANE_POSITION)
    axes.set_ylim(0.0, 1.12)
    axes.set_xlabel(r"$x$")
    axes.set_ylabel(r"radius of the slice $r(x)$")
    axes.set_title(r"Slice area $\pi x/4$ grows linearly in $x$", fontsize=10.5)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)


def draw_method_comparison(axes: plt.Axes) -> None:
    """Draw the value of each method next to the expected value.

    The point sample carries its standard error from the verification script.

    Args:
        axes: The axes of the right panel.
    """
    positions = np.arange(len(METHOD_NAMES))[::-1]
    for position, name, value in zip(positions, METHOD_NAMES, METHOD_VALUES):
        axes.plot([EXPECTED_VALUE, value], [position, position], color=COLOR_CURVE,
                  linewidth=1.0, alpha=0.55, zorder=2)
        axes.plot([value], [position], marker="o", markersize=8.0, color=COLOR_CURVE, zorder=3)
    axes.errorbar([METHOD_VALUES[3]], [positions[3]], xerr=[0.009369], fmt="none",
                  ecolor=COLOR_ACCENT, elinewidth=1.4, capsize=4.0, zorder=4)
    axes.axvline(EXPECTED_VALUE, color=COLOR_ACCENT, linewidth=1.6, linestyle="--", zorder=1,
                 label=r"$16\pi/3 = 16.755160819$")
    axes.set_yticks(positions)
    axes.set_yticklabels(METHOD_NAMES, fontsize=8.5)
    axes.set_xlim(16.70, 16.82)
    axes.set_ylim(-0.7, len(METHOD_NAMES) - 0.3)
    axes.set_xlabel(r"computed value of $\iiint_E x\,dV$")
    axes.set_title("Four independent orders agree", fontsize=10.5)
    axes.legend(loc="lower right", frameon=False, fontsize=8.0)
    axes.grid(axis="x", color="#dddddd", linewidth=0.6, zorder=0)
    axes.set_axisbelow(True)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)


def build_figure() -> plt.Figure:
    """Build the complete figure.

    Returns:
        The figure object that holds the two panels.
    """
    figure, (left_axes, right_axes) = plt.subplots(1, 2, figsize=(9.6, 3.9),
                                                   gridspec_kw={"width_ratios": [1.0, 1.25]})
    draw_slice_radius(left_axes)
    draw_method_comparison(right_axes)
    figure.tight_layout(pad=1.2)
    return figure


def main() -> int:
    """Draw the figure and write it to the figures directory.

    Returns:
        The process exit status: 0 on success.
    """
    apply_style()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure = build_figure()
    figure.savefig(FIGURE_PATH, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
