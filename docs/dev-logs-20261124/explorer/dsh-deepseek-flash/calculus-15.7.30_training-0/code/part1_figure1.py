"""Draw the solid E and its two projections.

Panel A shows the solid itself: the part of the circular cylinder y^2 + z^2 = 9 that lies between
the planes x = -2 and x = 2.  Each surface label sits at a point that satisfies the equation of
that surface.  Panel B shows the section x = 0, which is the disk y^2 + z^2 <= 9 in the plane
x = 0.  Panel C shows the projection onto the plane z = 0, which is the rectangle
[-2, 2] x [-3, 3].

Run this script with the interpreter of `code/.venv`.  It writes
`code/figures/part1_figure1.png`.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt

RADIUS = 3.0
"""Radius of the circular cylinder y^2 + z^2 = 9."""

HALF_LENGTH = 2.0
"""Half of the distance between the planes x = -2 and x = 2."""

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""Path of the figure file."""

INK = "#1f2933"
"""Color of the outline of a curve."""

ACCENT = "#1f3b57"
"""Color of a labeled surface."""

SURFACE_COLOR = "#7fa6c9"
"""Color of a wall of the solid."""

FILL_COLOR = "#cfe0ee"
"""Color of a filled section."""


def axis_arrows(axis) -> None:
    """Draw one axis line per coordinate axis, with one arrowhead and one label per axis.

    The line runs through the solid, and the arrowhead marks the positive direction.  The label
    sits at the tip of the arrowhead, so each axis carries exactly one label.

    Args:
        axis: The three-dimensional axes of the figure.
    """
    reach = 4.6
    axis.plot([-reach, reach], [0.0, 0.0], [0.0, 0.0], color=INK, linewidth=0.9, zorder=6)
    axis.plot([0.0, 0.0], [-reach, reach], [0.0, 0.0], color=INK, linewidth=0.9, zorder=6)
    axis.plot([0.0, 0.0], [0.0, 0.0], [-reach, reach], color=INK, linewidth=0.9, zorder=6)
    axis.quiver(0.0, 0.0, 0.0, reach, 0.0, 0.0, color=INK, linewidth=0.9,
                arrow_length_ratio=0.07, zorder=7)
    axis.quiver(0.0, 0.0, 0.0, 0.0, reach, 0.0, color=INK, linewidth=0.9,
                arrow_length_ratio=0.07, zorder=7)
    axis.quiver(0.0, 0.0, 0.0, 0.0, 0.0, reach, color=INK, linewidth=0.9,
                arrow_length_ratio=0.07, zorder=7)
    box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.72, "pad": 1.5}
    axis.text(reach + 0.1, 0.0, 0.0, "x", color=INK, fontsize=11, ha="left", va="center",
              zorder=10, bbox=box)
    axis.text(0.0, reach + 0.1, 0.0, "y", color=INK, fontsize=11, ha="left", va="bottom",
              zorder=10, bbox=box)
    axis.text(0.0, 0.0, reach + 0.1, "z", color=INK, fontsize=11, ha="center", va="bottom",
              zorder=10, bbox=box)


def draw_solid(axis) -> None:
    """Draw the wall of the cylinder, the two end disks, and the surface labels."""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    angle = np.linspace(0.0, 2.0 * math.pi, 181)
    station = np.array([-HALF_LENGTH, HALF_LENGTH])
    angle_grid, station_grid = np.meshgrid(angle, station)
    axis.plot_surface(station_grid, RADIUS * np.cos(angle_grid), RADIUS * np.sin(angle_grid),
                      color=SURFACE_COLOR, alpha=0.55, linewidth=0.0, shade=True, zorder=1)

    ring = np.column_stack([RADIUS * np.cos(angle), RADIUS * np.sin(angle)])
    for station_value in (-HALF_LENGTH, HALF_LENGTH):
        corners = np.column_stack([np.full(angle.size, station_value), ring])
        disk = Poly3DCollection([corners], facecolor=FILL_COLOR, edgecolor=INK, linewidth=1.2,
                                alpha=0.92, zorder=3)
        axis.add_collection3d(disk)
        axis.plot(np.full(angle.size, station_value), ring[:, 0], ring[:, 1], color=INK,
                  linewidth=1.2, zorder=4)

    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.72, "pad": 1.5}
    axis.text(-1.15, 0.0, RADIUS, "$y^2+z^2=9$", color=ACCENT, fontsize=10,
              ha="center", va="bottom", zorder=10, bbox=label_box)
    axis.text(HALF_LENGTH, -0.9, -RADIUS, "$x=2$", color=ACCENT, fontsize=10,
              ha="center", va="top", zorder=10, bbox=label_box)
    axis.text(-HALF_LENGTH, -0.9, -RADIUS, "$x=-2$", color=ACCENT, fontsize=10,
              ha="center", va="top", zorder=10, bbox=label_box)

    axis.set_xlim(-4.8, 4.8)
    axis.set_ylim(-4.8, 4.8)
    axis.set_zlim(-4.8, 4.8)
    axis.set_box_aspect((1.0, 1.0, 1.0))
    axis.computed_zorder = False
    axis.set_axis_off()
    axis.view_init(elev=22.0, azim=-58.0)


def draw_section(axis) -> None:
    """Draw the disk y^2 + z^2 <= 9 in the plane x = 0."""
    angle = np.linspace(0.0, 2.0 * math.pi, 361)
    axis.fill(RADIUS * np.cos(angle), RADIUS * np.sin(angle), color=FILL_COLOR,
              edgecolor=INK, linewidth=1.4)
    axis.plot([0.0], [0.0], marker="o", color=INK, markersize=4.0)
    axis.text(0.0, -RADIUS - 0.55, "$y^2+z^2\\leq 9$", color=ACCENT, fontsize=10,
              ha="center", va="top")
    axis.text(RADIUS + 0.15, 0.0, "$y$", color=INK, fontsize=10, ha="left", va="center")
    axis.text(0.0, RADIUS + 0.15, "$z$", color=INK, fontsize=10, ha="center", va="bottom")
    axis.annotate("", xy=(RADIUS + 0.15, 0.0), xytext=(0.0, 0.0),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 1.0})
    axis.annotate("", xy=(0.0, RADIUS + 0.15), xytext=(0.0, 0.0),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 1.0})
    axis.set_xlim(-3.7, 3.9)
    axis.set_ylim(-3.9, 3.7)
    axis.set_aspect("equal")
    axis.set_title("section at $x=0$: a disk in the plane $x=0$", fontsize=10, color=INK,
                   pad=10.0)
    axis.axis("off")


def draw_projection(axis) -> None:
    """Draw the projection onto the plane z = 0, which is the rectangle [-2, 2] x [-3, 3]."""
    axis.add_patch(plt.Rectangle((-HALF_LENGTH, -RADIUS), 2.0 * HALF_LENGTH, 2.0 * RADIUS,
                                 facecolor=FILL_COLOR, edgecolor=INK, linewidth=1.4))
    axis.text(0.0, -RADIUS - 0.55, "$-3\\leq y\\leq 3$, $-2\\leq x\\leq 2$", color=ACCENT,
              fontsize=10, ha="center", va="top")
    axis.text(HALF_LENGTH + 0.15, 0.0, "$x$", color=INK, fontsize=10, ha="left", va="center")
    axis.text(0.0, RADIUS + 0.15, "$y$", color=INK, fontsize=10, ha="center", va="bottom")
    axis.annotate("", xy=(HALF_LENGTH + 0.15, 0.0), xytext=(0.0, 0.0),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 1.0})
    axis.annotate("", xy=(0.0, RADIUS + 0.15), xytext=(0.0, 0.0),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 1.0})
    axis.set_xlim(-3.4, 3.4)
    axis.set_ylim(-3.9, 3.5)
    axis.set_aspect("equal")
    axis.set_title("projection on the plane $z=0$: a rectangle", fontsize=10, color=INK,
                   pad=10.0)
    axis.axis("off")


def main() -> None:
    """Draw the three panels and write the figure."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure = plt.figure(figsize=(14.0, 5.2), dpi=200)
    grid = figure.add_gridspec(1, 3, width_ratios=(1.25, 1.0, 1.0))
    solid_axis = figure.add_subplot(grid[0, 0], projection="3d")
    section_axis = figure.add_subplot(grid[0, 1])
    projection_axis = figure.add_subplot(grid[0, 2])

    draw_solid(solid_axis)
    axis_arrows(solid_axis)
    solid_axis.set_title("solid $E$: $|x|\\leq 2$ and $y^2+z^2\\leq 9$", fontsize=10,
                         color=INK, pad=-2.0)
    draw_section(section_axis)
    draw_projection(projection_axis)

    figure.tight_layout(pad=0.6)
    figure.savefig(FIGURE_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
