"""Draw figure 2 of Part 2: the corner list of each section, which decides its shape.

The figure is a workspace product. It draws the four extreme points of the section at the
heights y = 0, y = 2, and y = 4 in the plane of the coordinates x and z. The printed corner
list gives four distinct positions at y = 0 and at y = 2, and one position at y = 4.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Path of the figure that this script writes.
FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part2_figure2.png"

# Resolution of the figure in dots per inch.
FIGURE_RESOLUTION = 150

# Count of points along one ellipse.
POINT_COUNT = 400

# Heights of the three sections, with the color of each section.
SECTION_HEIGHTS = (0.0, 2.0, 4.0)
SECTION_COLORS = ("#1f3b57", "#4c78a8", "#d1495b")


def corner_list(height: float) -> list[tuple[float, float]]:
    """Return the four extreme points of the section at one height.

    Args:
        height: Height of the section.

    Returns:
        The four corner positions in the coordinates x and z.
    """
    radius_squared = 4.0 - height
    half_width_x = math.sqrt(max(radius_squared, 0.0))
    half_width_z = math.sqrt(max(radius_squared, 0.0)) / 2.0
    return [(half_width_x, 0.0), (-half_width_x, 0.0), (0.0, half_width_z), (0.0, -half_width_z)]


def main() -> None:
    """Draw the three sections with their corners and write the figure."""
    figure, axis = plt.subplots(figsize=(6.4, 5.0))
    angle = np.linspace(0.0, 2.0 * np.pi, POINT_COUNT)
    for height, color in zip(SECTION_HEIGHTS, SECTION_COLORS):
        radius_squared = 4.0 - height
        radius = math.sqrt(max(radius_squared, 0.0))
        coordinate_x = radius * np.cos(angle)
        coordinate_z = radius / 2.0 * np.sin(angle)
        axis.plot(coordinate_x, coordinate_z, color=color, linewidth=2.0)
        corners = corner_list(height)
        distinct = sorted({(round(position, 12), round(other, 12))
                           for position, other in corners})
        axis.plot([position for position, _ in corners], [other for _, other in corners],
                  marker="o", color=color, linestyle="none", markersize=5)
        annotation = f"$y = {height:.0f}$: {len(distinct)} distinct corner" + \
                     ("s" if len(distinct) > 1 else "")
        axis.text(0.0, -radius / 2.0 - 0.10, annotation, fontsize=9, ha="center", color=color)
    axis.annotate("", xy=(2.45, 0.0), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
    axis.annotate("", xy=(0.0, 1.45), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
    axis.text(2.50, 0.04, "$x$", fontsize=13, va="bottom")
    axis.text(0.07, 1.40, "$z$", fontsize=13, va="bottom")
    axis.text(2.06, 0.16, "$(2, 0, 0)$", fontsize=8, ha="left")
    axis.text(1.45, -0.62, "$(\\sqrt{2}, 0, \\sqrt{2}/2)$", fontsize=8, ha="center")
    axis.set_xlim(-2.7, 2.85)
    axis.set_ylim(-1.75, 1.75)
    axis.set_aspect("equal")
    axis.grid(alpha=0.3)
    axis.set_xlabel("$x$")
    axis.set_ylabel("$z$")
    axis.set_title("The corner list of each section, in the plane of $x$ and $z$", fontsize=10)
    figure.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=FIGURE_RESOLUTION, bbox_inches="tight")
    plt.close(figure)
    for height in SECTION_HEIGHTS:
        print(f"height y = {height:.1f}: corners = {corner_list(height)}")
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
