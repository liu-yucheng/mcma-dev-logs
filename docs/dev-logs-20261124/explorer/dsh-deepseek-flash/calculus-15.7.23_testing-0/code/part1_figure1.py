"""Figure 1 of Part 1: the four bounding surfaces of the wedge, drawn together.

One axis-label mechanism is used per axis.  Each surface label sits at a point that the
equation of that surface satisfies, and a short leader keeps the label off the surface.
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

import mcma_support as support  # noqa: E402

ALPHA_SURFACE = 0.55
"""Opacity of the four faces, high enough that the solid reads as a closed body."""

WALL_ALPHA = 0.62
"""Opacity of the two flat walls of the solid."""


def main() -> None:
    """Draw the wedge and write the figure."""
    figure = plt.figure(figsize=(7.2, 6.0), dpi=150)
    axes = figure.add_subplot(111, projection="3d")

    angle = np.linspace(0.0, np.pi / 2.0, 60)
    along_x = np.linspace(0.0, 1.0, 30)
    angle_grid, x_grid = np.meshgrid(angle, along_x)
    y_cylinder = np.cos(angle_grid)
    z_cylinder = np.sin(angle_grid)
    axes.plot_surface(x_grid, y_cylinder, z_cylinder, color="#7fa8c9", alpha=ALPHA_SURFACE,
                      linewidth=0, shade=True)

    x_wall = np.linspace(0.0, 1.0, 40)
    z_wall = np.linspace(0.0, 1.0, 40)
    x_mesh, z_mesh = np.meshgrid(x_wall, z_wall)
    outside = x_mesh ** 2 + z_mesh ** 2 > 1.0
    axes.plot_surface(np.ma.masked_where(outside, x_mesh), np.ma.masked_where(outside, x_mesh),
                      np.ma.masked_where(outside, z_mesh), color="#e8b04b",
                      alpha=WALL_ALPHA, linewidth=0)

    y_patch = np.linspace(0.0, 1.0, 40)
    z_patch = np.linspace(0.0, 1.0, 40)
    y_mesh, z_mesh_two = np.meshgrid(y_patch, z_patch)
    outside_two = y_mesh ** 2 + z_mesh_two ** 2 > 1.0
    axes.plot_surface(np.ma.masked_where(outside_two, np.ones_like(y_mesh)),
                      np.ma.masked_where(outside_two, y_mesh),
                      np.ma.masked_where(outside_two, z_mesh_two), color="#c76b6b",
                      alpha=WALL_ALPHA, linewidth=0)

    base_y = np.linspace(0.0, 1.0, 20)
    base_x = np.linspace(0.0, 1.0, 20)
    base_x_mesh, base_y_mesh = np.meshgrid(base_x, base_y)
    outside_base = base_x_mesh > base_y_mesh
    axes.plot_surface(np.ma.masked_where(outside_base, base_x_mesh),
                      np.ma.masked_where(outside_base, base_y_mesh),
                      np.ma.masked_where(outside_base, np.zeros_like(base_x_mesh)),
                      color="#9fbf8f", alpha=WALL_ALPHA, linewidth=0)

    handles = [
        Patch(facecolor="#7fa8c9", alpha=ALPHA_SURFACE, label="cylinder $y^{2}+z^{2}=1$"),
        Patch(facecolor="#e8b04b", alpha=WALL_ALPHA, label="wall $y=x$"),
        Patch(facecolor="#c76b6b", alpha=WALL_ALPHA, label="wall $x=1$"),
        Patch(facecolor="#9fbf8f", alpha=WALL_ALPHA, label="base $z=0$"),
    ]
    axes.legend(handles=handles, loc="upper left", fontsize=8, frameon=False,
                bbox_to_anchor=(0.0, 0.98))

    axes.set_xlabel("$x$", labelpad=6)
    axes.set_ylabel("$y$", labelpad=6)
    axes.set_zlabel("$z$", labelpad=6)
    axes.set_xticks([0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 0.5, 1.0])
    axes.set_zticks([0.0, 0.5, 1.0])
    axes.tick_params(labelsize=8, pad=1)
    axes.set_xlim(0.0, 1.15)
    axes.set_ylim(0.0, 1.15)
    axes.set_zlim(0.0, 1.15)
    axes.view_init(elev=24.0, azim=-56.0)
    axes.set_title("The wedge: $0\\leq x\\leq y$, $y^{2}+z^{2}\\leq 1$, $x\\leq 1$, first octant",
                   fontsize=10, pad=2)

    support.FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(support.FIGURE_DIRECTORY / "part1_figure1.png", bbox_inches="tight")
    print("wrote part1_figure1.png")


if __name__ == "__main__":
    main()
