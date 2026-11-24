"""Draw the projection, one cross-section, and the cross-section area function.

Left panel: the projection of the solid on the xy plane, with the strip at
x = 0.5. Middle panel: the cross-section at x = 0.5, which the inequalities
make a right triangle. Right panel: the area A(x) of the cross-section.

The script writes code/figures/part3_figure2.png.

Run this script with: code/.venv/Scripts/python.exe code/part3_figure2.py
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_PATH = pathlib.Path(__file__).resolve().parent / "figures" / "part3_figure2.png"
"""Output path of the figure of Part 3."""

FIXED_X = 0.5
"""Abscissa of the cross-section that the middle panel shows."""

MARKED_ABSCISSAS = (0.0, 0.5, 0.9)
"""Three abscissas where the right panel marks the area."""


def area_of_cross_section(x: np.ndarray | float) -> np.ndarray | float:
    """Return the area (1 - x^2)^2 / 2 of the cross-section at x.

    Args:
        x: One abscissa or an array of abscissas.

    Returns:
        The area of the cross-section at each abscissa.
    """
    return (1.0 - np.asarray(x) ** 2) ** 2 / 2.0


def draw_projection(axes: plt.Axes) -> None:
    """Draw the projection of the solid on the xy plane and the strip at x = 0.5.

    Args:
        axes: Axes of the left panel.

    Returns:
        None.
    """
    x = np.linspace(-1.0, 1.0, 801)
    axes.fill_between(x, x * x, 1.0, color="#cfe0ef", edgecolor="none")
    axes.plot(x, x * x, color="#1f4e79", linewidth=2.2, label="$y = x^2$")
    axes.plot([-1.0, 1.0], [1.0, 1.0], color="#b5651d", linewidth=2.2, label="$y = 1$")
    axes.vlines(FIXED_X, FIXED_X * FIXED_X, 1.0, color="#c0322f", linewidth=2.6, label="$x = 0.5$")
    axes.plot([FIXED_X], [FIXED_X * FIXED_X], "o", color="#c0322f", markersize=5)
    axes.plot([FIXED_X], [1.0], "o", color="#c0322f", markersize=5)
    axes.annotate("$y = x^2$", xy=(0.72, 0.52), xytext=(0.2, 0.62), color="#1f4e79", fontsize=10)
    axes.set_xlim(-1.15, 1.15)
    axes.set_ylim(-0.05, 1.18)
    axes.set_xlabel("$x$")
    axes.set_ylabel("$y$")
    axes.set_title("Projection $D$: $-1 \\leq x \\leq 1$, $x^2 \\leq y \\leq 1$", fontsize=10)
    axes.legend(loc="upper right", fontsize=8.5, frameon=False)
    axes.grid(True, linewidth=0.4, alpha=0.4)


def draw_cross_section(axes: plt.Axes) -> None:
    """Draw the cross-section at x = 0.5 in the yz plane.

    Args:
        axes: Axes of the middle panel.

    Returns:
        None.
    """
    y_low = FIXED_X * FIXED_X
    height = 1.0 - y_low
    vertices_y = np.array([y_low, 1.0, y_low, y_low])
    vertices_z = np.array([0.0, 0.0, height, 0.0])
    axes.fill(vertices_y, vertices_z, color="#f6d5c3", edgecolor="none")
    axes.plot(vertices_y, vertices_z, color="#c0322f", linewidth=2.4)
    axes.annotate("", xy=(1.0, 0.0), xytext=(y_low, 0.0),
                  arrowprops={"arrowstyle": "<->", "color": "black", "lw": 1.2})
    axes.text(0.62, -0.085, f"$1 - x^2 = {height:.2f}$", ha="center", fontsize=9.5)
    axes.annotate("", xy=(y_low, height), xytext=(y_low, 0.0),
                  arrowprops={"arrowstyle": "<->", "color": "black", "lw": 1.2})
    axes.text(y_low + 0.03, height / 2, f"$1 - x^2 = {height:.2f}$", rotation=90,
              va="center", fontsize=9.5)
    axes.text(0.50, 0.10, f"$A = \\frac{{(1-x^2)^2}}{{2}} = {height ** 2 / 2:.5f}$", fontsize=9.5, color="#8b0000")
    axes.set_xlim(0.1, 1.12)
    axes.set_ylim(-0.14, 0.9)
    axes.set_xlabel("$y$")
    axes.set_ylabel("$z$")
    axes.set_title("Cross-section at $x = 0.5$: a right triangle", fontsize=10)
    axes.grid(True, linewidth=0.4, alpha=0.4)


def draw_area_function(axes: plt.Axes) -> None:
    """Draw the cross-section area A(x) over the full x range.

    Args:
        axes: Axes of the right panel.

    Returns:
        None.
    """
    x = np.linspace(-1.0, 1.0, 801)
    values = area_of_cross_section(x)
    axes.plot(x, values, color="#1f4e79", linewidth=2.2)
    axes.fill_between(x, values, 0.0, color="#cfe0ef", alpha=0.9)
    for abscissa in MARKED_ABSCISSAS:
        area = float(area_of_cross_section(abscissa))
        axes.plot([abscissa], [area], "o", color="#c0322f", markersize=5)
        axes.annotate(
            f"{area:.5f}",
            xy=(abscissa, area),
            xytext=(abscissa + 0.05 if abscissa < 0.6 else abscissa - 0.30, area + 0.035),
            fontsize=8.5,
            color="#c0322f",
        )
    axes.set_xlim(-1.05, 1.05)
    axes.set_ylim(0.0, 0.58)
    axes.set_xlabel("$x$")
    axes.set_ylabel("$A(x)$")
    axes.set_title("$A(x) = \\frac{(1-x^2)^2}{2}$, largest value $0.5$ at $x = 0$", fontsize=10)
    axes.grid(True, linewidth=0.4, alpha=0.4)


def main() -> None:
    """Draw the figure of Part 3 and write it to the figures directory."""
    figure, panels = plt.subplots(1, 3, figsize=(14.4, 4.5))
    draw_projection(panels[0])
    draw_cross_section(panels[1])
    draw_area_function(panels[2])
    figure.suptitle("From the projection to the cross-section area", fontsize=12)

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=180)
    plt.close(figure)
    print(f"figure written to {FIGURE_PATH}")


if __name__ == "__main__":
    main()
