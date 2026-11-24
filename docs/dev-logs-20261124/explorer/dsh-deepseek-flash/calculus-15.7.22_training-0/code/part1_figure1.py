"""Draw the solid of the exercise.

The figure shows the three surfaces that bound the solid.
The wall is the part of the cylinder x^2 + z^2 = 4 between y = -1 and y = 4 - z.
The bottom is the disk at y = -1.
The top is the part of the plane y + z = 4 above the disk.
"""

from pathlib import Path
from typing import Final

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

RADIUS: Final[float] = 2.0
"""Radius of the cylinder."""

ANGLE_POINT_COUNT: Final[int] = 121
"""Number of sample angles on the wall."""

HEIGHT_POINT_COUNT: Final[int] = 41
"""Number of sample points along each vertical line of the wall."""

RADIAL_POINT_COUNT: Final[int] = 41
"""Number of sample radii of the bottom and of the top."""

FIGURE_PATH: Final[Path] = Path(__file__).parent / "figures" / "part1_figure1.png"
"""Path of the output file of the figure."""


def main() -> None:
    """Draw the three surfaces of the solid and save the figure."""
    matplotlib.rcParams["mathtext.fontset"] = "cm"
    figure = plt.figure(figsize=(7.2, 6.4))
    axes = figure.add_subplot(111, projection="3d")

    angles = np.linspace(0.0, 2.0 * np.pi, ANGLE_POINT_COUNT)
    fractions = np.linspace(0.0, 1.0, HEIGHT_POINT_COUNT)
    angle_grid, fraction_grid = np.meshgrid(angles, fractions)
    wall_x = RADIUS * np.cos(angle_grid)
    wall_z = RADIUS * np.sin(angle_grid)
    wall_y = -1.0 + fraction_grid * (5.0 - wall_z)
    axes.plot_surface(wall_x, wall_y, wall_z, color="#4C72B0", alpha=0.34, linewidth=0.0)

    radii = np.linspace(0.0, RADIUS, RADIAL_POINT_COUNT)
    radial_grid, angle_grid = np.meshgrid(radii, angles)
    disk_x = radial_grid * np.cos(angle_grid)
    disk_z = radial_grid * np.sin(angle_grid)
    axes.plot_surface(disk_x, np.full_like(disk_x, -1.0), disk_z, color="#DD8452", alpha=0.80,
                      linewidth=0.0)
    axes.plot_surface(disk_x, 4.0 - disk_z, disk_z, color="#55A868", alpha=0.80, linewidth=0.0)

    axes.plot([0.0, 2.6], [0.0, 0.0], [0.0, 0.0], color="black", linewidth=1.2)
    axes.plot([0.0, 0.0], [0.0, 6.6], [0.0, 0.0], color="black", linewidth=1.2)
    axes.plot([0.0, 0.0], [0.0, 0.0], [0.0, 2.6], color="black", linewidth=1.2)
    axes.text(2.7, 0.0, 0.0, r"$x$", fontsize=13)
    axes.text(0.0, 6.8, 0.0, r"$y$", fontsize=13)
    axes.text(0.0, 0.0, 2.7, r"$z$", fontsize=13)
    axes.text(0.0, -1.3, -2.6, r"$y=-1$", fontsize=11, color="#8C4A21")
    axes.text(0.0, 5.6, 2.4, r"$y+z=4$", fontsize=11, color="#2F6B3C")
    axes.text(2.1, 2.4, 1.6, r"$x^2+z^2=4$", fontsize=11, color="#2F4C77")

    axes.set_xlim(-2.6, 2.6)
    axes.set_ylim(-1.6, 6.9)
    axes.set_zlim(-2.4, 2.6)
    axes.set_box_aspect((1.0, 1.65, 1.0))
    axes.view_init(elev=16.0, azim=-58.0)
    axes.set_xlabel(r"$x$", labelpad=8)
    axes.set_ylabel(r"$y$", labelpad=8)
    axes.set_zlabel(r"$z$", labelpad=8)
    axes.set_title("The solid: cylinder wall, bottom disk at $y=-1$, top $y=4-z$", fontsize=11)

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=170)
    print(f"saved {FIGURE_PATH}")


if __name__ == "__main__":
    main()
