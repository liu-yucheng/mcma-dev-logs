"""Draw figure 1 of Part 1: the solid between the paraboloid and the plane y = 0.

The figure is a workspace product. It is not a copy of the source image, which holds no
figure. The left panel shows the body in space. The right panel shows the section at z = 0,
which is the parabola y = 4 - x**2 over the interval -2 <= x <= 2. Each axis carries one arrow
with one letter, and each curve label sits at a point that its own equation satisfies.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from solid_geometry import APEX_HEIGHT, BASE_SEMI_AXIS_X, BASE_SEMI_AXIS_Z

# Path of the figure that this script writes.
FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"

# Resolution of the figure in dots per inch.
FIGURE_RESOLUTION = 150

# Count of grid points along the scaled radius and along the angle.
RADIAL_COUNT = 60
ANGULAR_COUNT = 90

# Opacity of the wall and of the base. A value above 0.5 makes the solid read as a closed body.
WALL_OPACITY = 0.62
BASE_OPACITY = 0.62

# Limits of the section panel.
SECTION_X_LIMITS = (-2.55, 2.95)
SECTION_Y_LIMITS = (-0.75, 5.25)


def draw_space_axes(axis) -> None:
    """Draw one arrow with one letter for each axis of the space panel.

    Args:
        axis: The three-dimensional axis of the figure.
    """
    arrow_lengths = (BASE_SEMI_AXIS_X + 0.9, APEX_HEIGHT + 0.7, BASE_SEMI_AXIS_Z + 0.8)
    directions = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    letters = ("$x$", "$y$", "$z$")
    for length, direction, letter in zip(arrow_lengths, directions, letters):
        tip = tuple(length * component for component in direction)
        axis.quiver(0.0, 0.0, 0.0, tip[0], tip[1], tip[2], color="black",
                    arrow_length_ratio=0.06, linewidth=1.2)
        axis.text(tip[0], tip[1], tip[2], letter, fontsize=14, color="black")


def draw_solid_panel(axis) -> None:
    """Draw the wall surface, the base disk, and the space axes.

    Args:
        axis: The three-dimensional axis of the figure.
    """
    scaled_radius = np.linspace(0.0, 1.0, RADIAL_COUNT)
    angle = np.linspace(0.0, 2.0 * np.pi, ANGULAR_COUNT)
    radius_grid, angle_grid = np.meshgrid(scaled_radius, angle)
    coordinate_x = BASE_SEMI_AXIS_X * radius_grid * np.cos(angle_grid)
    coordinate_z = BASE_SEMI_AXIS_Z * radius_grid * np.sin(angle_grid)
    coordinate_y = APEX_HEIGHT * (1.0 - radius_grid**2)
    axis.plot_surface(coordinate_x, coordinate_y, coordinate_z, color="#4c78a8",
                      alpha=WALL_OPACITY, linewidth=0.0, antialiased=True, shade=True)
    base_x = coordinate_x
    base_z = coordinate_z
    base_y = np.zeros_like(base_x)
    axis.plot_surface(base_x, base_y, base_z, color="#f2a541", alpha=BASE_OPACITY, linewidth=0.0,
                      antialiased=True, shade=False)
    axis.plot(coordinate_x[-1], coordinate_y[-1], coordinate_z[-1], color="#1f3b57",
              linewidth=2.0)
    draw_space_axes(axis)
    axis.set_xlim(-2.9, 2.9)
    axis.set_ylim(-0.2, 4.9)
    axis.set_zlim(-1.8, 1.8)
    axis.set_xticklabels([])
    axis.set_yticklabels([])
    axis.set_zticklabels([])
    axis.set_box_aspect((2.9, 4.9, 1.8))
    axis.view_init(elev=16.0, azim=-66.0)
    axis.set_title("(a) the body between the wall and the base", fontsize=10)


def draw_section_panel(axis) -> None:
    """Draw the section at z = 0 with its parabola and its labels.

    Args:
        axis: The two-dimensional axis of the figure.
    """
    coordinate_x = np.linspace(-BASE_SEMI_AXIS_X, BASE_SEMI_AXIS_X, 400)
    coordinate_y = APEX_HEIGHT - coordinate_x**2
    axis.fill_between(coordinate_x, 0.0, coordinate_y, color="#4c78a8", alpha=0.35)
    axis.plot(coordinate_x, coordinate_y, color="#1f3b57", linewidth=2.0)
    axis.plot([-BASE_SEMI_AXIS_X, BASE_SEMI_AXIS_X], [0.0, 0.0], color="#8a5a00", linewidth=2.0)
    axis.annotate("", xy=(2.45, 0.0), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.2))
    axis.annotate("", xy=(0.0, 4.95), xytext=(0.0, 0.0),
                  arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.2))
    axis.text(2.50, 0.06, "$x$", fontsize=13, va="bottom")
    axis.text(0.07, 4.90, "$y$", fontsize=13, ha="left", va="bottom")
    # The wall label is anchored at (1.30, 2.31), which satisfies y = 4 - x**2.
    axis.text(1.30, APEX_HEIGHT - 1.30**2, "$y = 4 - x^{2}$", fontsize=11, color="#1f3b57",
              ha="left", va="bottom")
    # The base label is anchored at (-1.60, 0.00), which satisfies y = 0.
    axis.text(-1.60, 0.0, "$y = 0$", fontsize=11, color="#8a5a00", ha="center", va="top")
    axis.plot([0.0], [APEX_HEIGHT], marker="o", color="#1f3b57", markersize=5)
    axis.text(0.12, APEX_HEIGHT - 0.12, "apex $(0, 4, 0)$", fontsize=10, ha="left", va="top")
    axis.plot([-BASE_SEMI_AXIS_X, BASE_SEMI_AXIS_X], [0.0, 0.0], marker="o", color="#8a5a00",
              markersize=4, linestyle="none")
    axis.text(-2.02, -0.12, "$(-2, 0, 0)$", fontsize=9, ha="right", va="top")
    axis.text(2.02, -0.12, "$(2, 0, 0)$", fontsize=9, ha="left", va="top")
    axis.set_xlim(*SECTION_X_LIMITS)
    axis.set_ylim(*SECTION_Y_LIMITS)
    axis.set_xticks([-2, -1, 0, 1, 2])
    axis.set_yticks([0, 1, 2, 3, 4])
    axis.set_xlabel("$x$")
    axis.set_ylabel("$y$")
    axis.grid(alpha=0.3)
    axis.set_title("(b) the section at $z = 0$", fontsize=10)


def main() -> None:
    """Draw both panels and write the figure to the figures directory."""
    figure = plt.figure(figsize=(10.4, 4.6))
    space_axis = figure.add_subplot(1, 2, 1, projection="3d")
    section_axis = figure.add_subplot(1, 2, 2)
    draw_solid_panel(space_axis)
    draw_section_panel(section_axis)
    figure.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=FIGURE_RESOLUTION, bbox_inches="tight")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")
    print(f"base semi-axes = ({BASE_SEMI_AXIS_X}, {BASE_SEMI_AXIS_Z}), "
          f"apex height = {APEX_HEIGHT}")
    print(f"section area under the parabola = {2.0 * (2.0 * APEX_HEIGHT - 8.0 / 3.0) / 2.0:.9f}")


if __name__ == "__main__":
    main()
