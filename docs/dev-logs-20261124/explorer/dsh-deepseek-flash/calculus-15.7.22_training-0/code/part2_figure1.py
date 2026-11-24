"""Draw the vertical thickness h = 5 - z above the disk.

The figure shows the disk D: x^2 + z^2 <= 4 in the plane of x and z.
The color gives the length of the vertical interval above each point of the disk.
The length is 3 at the point (0, 2) and 7 at the point (0, -2).
"""

from pathlib import Path
from typing import Final

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

RADIUS: Final[float] = 2.0
"""Radius of the disk."""

GRID_POINT_COUNT: Final[int] = 401
"""Number of grid points on each side of the square grid."""

FIGURE_PATH: Final[Path] = Path(__file__).parent / "figures" / "part2_figure1.png"
"""Path of the output file of the figure."""


def main() -> None:
    """Draw the thickness over the disk and save the figure."""
    matplotlib.rcParams["mathtext.fontset"] = "cm"
    axis = np.linspace(-RADIUS, RADIUS, GRID_POINT_COUNT)
    grid_x, grid_z = np.meshgrid(axis, axis)
    thickness = 5.0 - grid_z
    outside = grid_x**2 + grid_z**2 > RADIUS**2
    plotted = np.ma.array(thickness, mask=outside)

    figure, axes = plt.subplots(figsize=(6.6, 5.4))
    mesh = axes.pcolormesh(grid_x, grid_z, plotted, cmap="viridis", shading="auto")
    color_bar = figure.colorbar(mesh, ax=axes)
    color_bar.set_label(r"vertical thickness $h=5-z$")

    circle_angle = np.linspace(0.0, 2.0 * np.pi, 361)
    axes.plot(RADIUS * np.cos(circle_angle), RADIUS * np.sin(circle_angle), color="white",
              linewidth=1.6)
    axes.plot([-2.4, 2.4], [2.0, 2.0], color="white", linewidth=0.9, linestyle=":")
    axes.plot([-2.4, 2.4], [-2.0, -2.0], color="white", linewidth=0.9, linestyle=":")

    axes.annotate(r"$h=3$ at $z=2$", xy=(0.0, 1.99), xytext=(0.55, 2.26), color="black", fontsize=11,
                  arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 1.0})
    axes.annotate(r"$h=7$ at $z=-2$", xy=(0.0, -1.99), xytext=(0.55, -2.26), color="black", fontsize=11,
                  arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 1.0})
    axes.annotate(r"$h=5$", xy=(0.0, 0.0), xytext=(0.35, 0.15), color="white", fontsize=12)
    axes.set_xlim(-2.35, 2.35)
    axes.set_ylim(-2.35, 2.35)
    axes.set_xlabel(r"$x$")
    axes.set_ylabel(r"$z$")
    axes.set_aspect("equal")
    axes.set_title(r"Length of the vertical interval above $(x,z)$: $h=5-z$", fontsize=11)

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=170)
    print(f"saved {FIGURE_PATH}")


if __name__ == "__main__":
    main()
