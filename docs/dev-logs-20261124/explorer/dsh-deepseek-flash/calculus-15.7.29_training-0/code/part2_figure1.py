"""Draw figure 1 of Part 2: the projection on the plane y = 0 and the sections at fixed y.

The figure is a workspace product. The left panel shows the projection D of the solid on the
plane y = 0, which keeps the coordinates x and z. The right panel shows three sections at
fixed heights. Each label sits at a point that its own equation satisfies.
"""

from __future__ import annotations

import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Path of the figure that this script writes.
from pathlib import Path

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part2_figure1.png"

# Resolution of the figure in dots per inch.
FIGURE_RESOLUTION = 150

# Count of points along one ellipse.
POINT_COUNT = 400

# Heights of the three sections of the right panel.
SECTION_HEIGHTS = (0.0, 2.0, 3.9)

# Colors of the three sections, from the base to the apex.
SECTION_COLORS = ("#1f3b57", "#4c78a8", "#9ecae1")


def draw_projection_panel(axis) -> None:
    """Draw the projection D with its semi-axes and its area.

    Args:
        axis: The two-dimensional axis of the figure.
    """
    angle = np.linspace(0.0, 2.0 * np.pi, POINT_COUNT)
    coordinate_x = 2.0 * np.cos(angle)
    coordinate_z = np.sin(angle)
    axis.fill(coordinate_x, coordinate_z, color="#4c78a8", alpha=0.35)
    axis.plot(coordinate_x, coordinate_z, color="#1f3b57", linewidth=2.0)
    axis.annotate("", xy=(2.45, 0.0), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
    axis.annotate("", xy=(0.0, 1.45), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
    axis.text(2.50, 0.04, "$x$", fontsize=13, va="bottom")
    axis.text(0.07, 1.40, "$z$", fontsize=13, va="bottom")
    axis.annotate("", xy=(2.0, 0.0), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="<|-|>", color="#8a5a00", linewidth=1.0))
    axis.annotate("", xy=(0.0, 1.0), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="<|-|>", color="#8a5a00", linewidth=1.0))
    # The semi-axis labels sit on the axes, where their own equations hold.
    axis.text(1.0, -0.11, "2", color="#8a5a00", fontsize=11, ha="center")
    axis.text(0.08, 0.50, "1", color="#8a5a00", fontsize=11, va="center")
    # The curve label is anchored at an angle of 135 degrees, which satisfies x**2 + 4z**2 = 4.
    axis.text(2.0 * math.cos(2.356), 2.0 * math.sin(2.356) * 0.5 + 0.12,
              "$x^{2} + 4z^{2} = 4$", fontsize=11, color="#1f3b57", ha="center")
    axis.set_xlim(-2.7, 2.85)
    axis.set_ylim(-1.65, 1.75)
    axis.set_aspect("equal")
    axis.set_xticks([-2, -1, 0, 1, 2])
    axis.set_yticks([-1, 0, 1])
    axis.grid(alpha=0.3)
    axis.set_title("(a) the projection D on the plane $y = 0$, area $2\\pi$", fontsize=10)


def draw_section_panel(axis) -> None:
    """Draw three sections at fixed heights, nested in the plane of the coordinates x and z.

    Args:
        axis: The two-dimensional axis of the figure.
    """
    angle = np.linspace(0.0, 2.0 * np.pi, POINT_COUNT)
    for height, color in zip(SECTION_HEIGHTS, SECTION_COLORS):
        radius = math.sqrt(4.0 - height)
        coordinate_x = radius * np.cos(angle)
        coordinate_z = radius / 2.0 * np.sin(angle)
        axis.fill(coordinate_x, coordinate_z, color=color, alpha=0.25)
        area = math.pi * (4.0 - height) / 2.0
        radius_text = radius / 2.0 + 0.06
        axis.plot(coordinate_x, coordinate_z, color=color, linewidth=2.0,
                  label=f"$y = {height:.1f}$: area ${area:.4f}$")
    axis.annotate("", xy=(2.45, 0.0), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
    axis.annotate("", xy=(0.0, 1.45), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
    axis.text(2.50, 0.04, "$x$", fontsize=13, va="bottom")
    axis.text(0.07, 1.40, "$z$", fontsize=13, va="bottom")
    axis.set_xlim(-2.7, 2.85)
    axis.set_ylim(-1.65, 1.75)
    axis.set_aspect("equal")
    axis.set_xticks([-2, -1, 0, 1, 2])
    axis.set_yticks([-1, 0, 1])
    axis.grid(alpha=0.3)
    axis.legend(loc="lower center", fontsize=9, frameon=False)
    axis.set_title("(b) the sections at $y = 0$, $2$, and $3.9$", fontsize=10)


def main() -> None:
    """Draw both panels and write the figure to the figures directory."""
    figure, (left_axis, right_axis) = plt.subplots(1, 2, figsize=(10.2, 4.4))
    draw_projection_panel(left_axis)
    draw_section_panel(right_axis)
    figure.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=FIGURE_RESOLUTION, bbox_inches="tight")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")
    print(f"area of the projection = {2.0 * math.pi:.9f}")


if __name__ == "__main__":
    main()
