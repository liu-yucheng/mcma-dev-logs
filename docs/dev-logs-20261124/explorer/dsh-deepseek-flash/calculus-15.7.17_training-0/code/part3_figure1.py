"""Draw the radius integral that Part 3 evaluates.

The left panel shows the integrand 8*(r - r^5) on 0 <= r <= 1 and the shaded area,
which equals 8/3.  The right panel shows the running integral from 0 to R.  The
running integral increases to 8/3, so the figure shows the value without a formula.

The script writes the figure to code/figures/part3_figure1.png.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

RADIUS_INTEGRAL_VALUE: float = 8.0 / 3.0
"""The value of the radius integral from 0 to 1."""

FIGURE_DPI: int = 200
"""Resolution of the written image in dots per inch."""

COLOR_CURVE: str = "#2f5d8a"
"""Color of the integrand curve."""

COLOR_ACCENT: str = "#c8863c"
"""Color of the shaded area and the limit line."""

FIGURE_PATH: Path = Path(__file__).resolve().parent / "figures" / "part3_figure1.png"
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


def integrand(radius: np.ndarray | float) -> np.ndarray | float:
    """Return the integrand 8*(r - r^5) of the radius integral.

    Args:
        radius: A radius value or an array of radius values in [0, 1].

    Returns:
        The value of 0.5*(16 - 16*r^4)*r.
    """
    return 0.5 * (PLANE_POSITION**2 - (PARABOLOID_COEFFICIENT * np.asarray(radius) ** 2) ** 2) \
        * np.asarray(radius)


def draw_integrand(axes: plt.Axes) -> None:
    """Draw the integrand and its shaded area.

    Args:
        axes: The axes of the left panel.
    """
    radius_values = np.linspace(0.0, 1.0, 400)
    value_values = integrand(radius_values)
    axes.fill_between(radius_values, 0.0, value_values, color=COLOR_ACCENT, alpha=0.28,
                      linewidth=0.0)
    axes.plot(radius_values, value_values, color=COLOR_CURVE, linewidth=2.2)
    peak_index = int(np.argmax(value_values))
    axes.plot([radius_values[peak_index]], [value_values[peak_index]], marker="o",
              markersize=4.0, color=COLOR_CURVE)
    axes.annotate(r"$8(r - r^5)$", xy=(0.86, float(integrand(0.86))), xytext=(0.14, 3.55),
                  color=COLOR_CURVE, fontsize=11,
                  arrowprops={"arrowstyle": "->", "color": COLOR_CURVE, "linewidth": 0.9})
    axes.text(0.33, 0.55, r"area $= \dfrac{8}{3}$", color="#8a5a1c", fontsize=12)
    axes.set_xlim(0.0, 1.0)
    axes.set_ylim(0.0, 4.9)
    axes.set_xlabel(r"$r$")
    axes.set_ylabel("integrand")
    axes.set_title(r"Radius integrand $8r\,(1 - r^4)$ on $0 \leq r \leq 1$", fontsize=10.5)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)


def draw_running_integral(axes: plt.Axes) -> None:
    """Draw the running integral from 0 to R.

    Args:
        axes: The axes of the right panel.
    """
    radius_values = np.linspace(0.0, 1.0, 400)
    running_values = 4.0 * radius_values**2 - (4.0 / 3.0) * radius_values**6
    axes.plot(radius_values, running_values, color=COLOR_CURVE, linewidth=2.2,
              label=r"$G(R) = \int_0^R 8(r - r^5)\,dr$")
    axes.axhline(RADIUS_INTEGRAL_VALUE, color=COLOR_ACCENT, linewidth=1.4, linestyle="--",
                 label=r"$8/3 = 2.6667$")
    axes.plot([1.0], [RADIUS_INTEGRAL_VALUE], marker="o", markersize=5.0, color=COLOR_ACCENT,
              zorder=5)
    axes.annotate(r"$G(1) = 8/3$", xy=(1.0, RADIUS_INTEGRAL_VALUE), xytext=(0.40, 2.05),
                  color="#8a5a1c", fontsize=10.5,
                  arrowprops={"arrowstyle": "->", "color": COLOR_ACCENT, "linewidth": 0.9})
    axes.set_xlim(0.0, 1.12)
    axes.set_ylim(0.0, 3.0)
    axes.set_xlabel(r"$R$")
    axes.set_ylabel("running integral")
    axes.set_title("The running integral increases to the limit", fontsize=10.5)
    axes.legend(loc="lower right", frameon=False, fontsize=8.5)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)


def build_figure() -> plt.Figure:
    """Build the complete figure.

    Returns:
        The figure object that holds the two panels.
    """
    figure, (left_axes, right_axes) = plt.subplots(1, 2, figsize=(9.4, 3.9))
    draw_integrand(left_axes)
    draw_running_integral(right_axes)
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
