"""Figure 1: the solid, its two surfaces, and the three points that fix its outline.

The script writes code/figures/part1_figure1.png. Run it with the environment
interpreter: code/.venv/Scripts/python.exe code/part1_figure1.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
WALL_ALPHA = 0.55


def main() -> None:
    """Draw the solid and write the figure file."""
    figure = plt.figure(figsize=(7.2, 6.0))
    axes = figure.add_subplot(111, projection="3d")

    axis_x = np.linspace(-1.0, 1.0, 61)
    axis_y = np.linspace(0.0, 1.0, 61)
    grid_x, grid_y = np.meshgrid(axis_x, axis_y)
    top_z = 1.0 - grid_y

    axes.plot_surface(grid_x, grid_y, top_z, color="#b8cbe4", alpha=WALL_ALPHA, linewidth=0.0, shade=False)
    axes.plot_surface(grid_x, grid_y, np.zeros_like(grid_y), color="#d9e2ee", alpha=WALL_ALPHA, linewidth=0.0)

    wall_y = np.linspace(0.0, 1.0, 41)
    wall_x = np.sqrt(wall_y)
    wall_z = np.linspace(0.0, 1.0, 41)
    grid_wall_y, grid_wall_z = np.meshgrid(wall_y, wall_z)
    grid_wall_x = np.sqrt(grid_wall_y)
    axes.plot_surface(grid_wall_x, grid_wall_y, grid_wall_z, color="#9db8d6", alpha=WALL_ALPHA, linewidth=0.0)
    axes.plot_surface(-grid_wall_x, grid_wall_y, grid_wall_z, color="#9db8d6", alpha=WALL_ALPHA, linewidth=0.0)

    rim = np.linspace(-1.0, 1.0, 200)
    axes.plot(rim, rim**2, np.zeros_like(rim), color="#1f3b57", linewidth=1.4)
    axes.plot(rim, rim**2, 1.0 - rim**2, color="#1f3b57", linewidth=1.4)

    corner = figure_anchors.CORNER_POINTS[2]
    axes.plot([corner[0]], [corner[1]], [corner[2]], marker="o", color="#1f3b57", markersize=4)

    cylinder_point = figure_anchors.CYLINDER_LABEL_POINT
    floor_point = figure_anchors.FLOOR_LABEL_POINT
    top_point = figure_anchors.TOP_LABEL_POINT
    axes.text(*cylinder_point, r"$y = x^{2}$", fontsize=11, color="#1f3b57")
    axes.text(*floor_point, r"$z = 0$", fontsize=11, color="#1f3b57")
    axes.text(*top_point, r"$y + z = 1$", fontsize=11, color="#1f3b57")

    axes.set_xlabel(r"$x$", labelpad=6)
    axes.set_ylabel(r"$y$", labelpad=6)
    axes.set_zlabel(r"$z$", labelpad=6)
    axes.set_xlim(-1.0, 1.0)
    axes.set_ylim(0.0, 1.0)
    axes.set_zlim(0.0, 1.0)
    axes.set_xticks([-1.0, 0.0, 1.0])
    axes.set_yticks([0.0, 0.5, 1.0])
    axes.set_zticks([0.0, 0.5, 1.0])
    axes.view_init(elev=22.0, azim=-58.0)
    axes.set_box_aspect((1.0, 1.0, 1.0))

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=170)
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
