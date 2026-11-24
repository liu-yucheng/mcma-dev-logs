"""Draw how the inner integral of two orders reads the section at a fixed value of x.

The section of E at a fixed value of x keeps the coordinates y and z, and its boundaries follow from
``x**2 <= y <= 4`` and ``0 <= z <= (4 - y) / 2``.  The left panel draws the inner integral of the order
dz dy dx: at a fixed value of y, z runs from 0 to (4 - y) / 2, so the inner piece is a vertical
segment.  The right panel draws the inner integral of the order dy dz dx: at a fixed value of z, y runs
from x**2 to 4 - 2 * z, so the inner piece is a horizontal segment.

Run this script with the interpreter of ``code/.venv``.  It writes ``code/figures/part3_figure1.png``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory of the figure files."""

OUTPUT_PATH = FIGURE_DIRECTORY / "part3_figure1.png"
"""Path of the figure of this part."""

EDGE_COLOR = "#1f2933"
"""Color of the boundary of the section."""

FILL_COLOR = "#7aa6c2"
"""Color of the section."""

STRIP_COLOR = "#b5446e"
"""Color of the drawn inner piece."""

FIXED_X = 1.0
"""The fixed value of x that both panels use."""


def height_at(y_value: float) -> float:
    """Return the upper limit of z at a fixed value of y.

    Args:
        y_value: The fixed value of y.

    Returns:
        The upper limit (4 - y_value) / 2.
    """
    return (4.0 - y_value) / 2.0


def draw_inner_z(axes: plt.Axes) -> None:
    """Draw the inner piece of the order dz dy dx, which is a vertical segment.

    Args:
        axes: The axes of the left panel.
    """
    y_values = np.linspace(FIXED_X ** 2, 4.0, 300)
    axes.fill_between(y_values, 0.0, [height_at(value) for value in y_values],
                      color=FILL_COLOR, alpha=0.35, linewidth=0.0)
    axes.plot([FIXED_X ** 2, 4.0, FIXED_X ** 2, FIXED_X ** 2],
              [0.0, 0.0, height_at(FIXED_X ** 2), 0.0], color=EDGE_COLOR, linewidth=1.5)

    for y_value in (1.6, 2.4, 3.2):
        top = height_at(y_value)
        axes.annotate("", xy=(y_value, top), xytext=(y_value, 0.0),
                      arrowprops={"arrowstyle": "-|>", "color": STRIP_COLOR, "linewidth": 1.4,
                                  "shrinkA": 0.0, "shrinkB": 5.0})
        axes.text(y_value + 0.06, top / 2.0, f"$z: 0 \\to {top:.2f}$", fontsize=8.0,
                  color=STRIP_COLOR, rotation=90.0, va="center")

    axes.set_xlim(0.55, 4.55)
    axes.set_ylim(-0.30, 1.85)
    axes.set_xticks([1, 2, 3, 4])
    axes.set_yticks([0, 0.5, 1.0, 1.5])
    axes.set_xlabel("y", fontsize=10)
    axes.set_ylabel("z", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Inner integral in $z$: fix $y$, then $0 \\leq z \\leq (4 - y)/2$", fontsize=9.0,
                   pad=6)


def draw_inner_y(axes: plt.Axes) -> None:
    """Draw the inner piece of the order dy dz dx, which is a horizontal segment.

    Args:
        axes: The axes of the right panel.
    """
    y_values = np.linspace(FIXED_X ** 2, 4.0, 300)
    axes.fill_between(y_values, 0.0, [height_at(value) for value in y_values],
                      color=FILL_COLOR, alpha=0.35, linewidth=0.0)
    axes.plot([FIXED_X ** 2, 4.0, FIXED_X ** 2, FIXED_X ** 2],
              [0.0, 0.0, height_at(FIXED_X ** 2), 0.0], color=EDGE_COLOR, linewidth=1.5)

    for z_value in (0.30, 0.60, 0.90):
        right = 4.0 - 2.0 * z_value
        axes.annotate("", xy=(right, z_value), xytext=(FIXED_X ** 2, z_value),
                      arrowprops={"arrowstyle": "-|>", "color": STRIP_COLOR, "linewidth": 1.4,
                                  "shrinkA": 0.0, "shrinkB": 5.0})
        axes.text((FIXED_X ** 2 + right) / 2.0, z_value + 0.075,
                  f"$y: 1 \\to {right:.1f}$", fontsize=8.0, color=STRIP_COLOR, ha="center")

    axes.set_xlim(0.55, 4.55)
    axes.set_ylim(-0.30, 1.85)
    axes.set_xticks([1, 2, 3, 4])
    axes.set_yticks([0, 0.5, 1.0, 1.5])
    axes.set_xlabel("y", fontsize=10)
    axes.set_ylabel("z", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Inner integral in $y$: fix $z$, then $x^2 \\leq y \\leq 4 - 2z$", fontsize=9.0,
                   pad=6)


def main() -> None:
    """Draw the two panels and write the figure."""
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    figure, panel_pair = plt.subplots(1, 2, figsize=(10.4, 4.3), dpi=170)
    draw_inner_z(panel_pair[0])
    draw_inner_y(panel_pair[1])
    figure.tight_layout(pad=1.6)
    figure.savefig(OUTPUT_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {OUTPUT_PATH}")
    print(f"section at x = {FIXED_X}: corners ({FIXED_X ** 2}, 0), (4, 0), ({FIXED_X ** 2}, "
          f"{height_at(FIXED_X ** 2)})")
    for y_value in (1.6, 2.4, 3.2):
        print(f"  inner z range at y = {y_value}: [0, {height_at(y_value):.6f}]")
    for z_value in (0.30, 0.60, 0.90):
        print(f"  inner y range at z = {z_value}: [{FIXED_X ** 2}, {4.0 - 2.0 * z_value:.6f}]")


if __name__ == "__main__":
    main()
