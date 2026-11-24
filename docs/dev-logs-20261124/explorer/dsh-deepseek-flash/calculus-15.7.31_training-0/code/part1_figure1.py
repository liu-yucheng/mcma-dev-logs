"""Draw the solid E and its three projections for Stewart 15.7 Exercise 31.

The upper left panel shows the three bounding surfaces of the solid.  Each surface is drawn over the
part of its own domain that belongs to E, so the drawn body is closed.  The three curves where two
surfaces meet are drawn in a dark stroke, because those curves close the body.  A label sits outside
the body at an anchor point that satisfies the equation of the surface that it names.

The other three panels show the projection of E on each coordinate plane.  A projection that drops
the coordinate y lies on the plane y = 0, and each panel title names the plane by the two
coordinates that its points keep.

Run this script with the interpreter of ``code/.venv``.  It writes ``code/figures/part1_figure1.png``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory of the figure files."""

OUTPUT_PATH = FIGURE_DIRECTORY / "part1_figure1.png"
"""Path of the figure of this part."""

WALL_COLOR = "#7aa6c2"
"""Color of the parabolic cylinder y = x squared."""

FLOOR_COLOR = "#c9dae7"
"""Color of the plane z = 0."""

PLANE_COLOR = "#e3b778"
"""Color of the plane y + 2z = 4."""

EDGE_COLOR = "#1f2933"
"""Color of the curves where two surfaces meet."""


def draw_solid(axes: plt.Axes) -> None:
    """Draw the three bounding surfaces of E over the part of each surface that belongs to E.

    Args:
        axes: The three-dimensional axes of the upper left panel.
    """
    parameter_x = np.linspace(-2.0, 2.0, 81)
    parameter_v = np.linspace(0.0, 1.0, 41)
    grid_x, grid_v = np.meshgrid(parameter_x, parameter_v)
    cap = 4.0 - grid_x * grid_x

    axes.plot_surface(grid_x, grid_x * grid_x, grid_v * cap / 2.0, color=WALL_COLOR, alpha=0.55,
                      linewidth=0.0, antialiased=True)
    floor_y = grid_x * grid_x + grid_v * cap
    axes.plot_surface(grid_x, floor_y, np.zeros_like(floor_y), color=FLOOR_COLOR, alpha=0.62,
                      linewidth=0.0, antialiased=True)
    plane_y = grid_x * grid_x + grid_v * cap
    axes.plot_surface(grid_x, plane_y, (4.0 - plane_y) / 2.0, color=PLANE_COLOR, alpha=0.55,
                      linewidth=0.0, antialiased=True)

    curve_x = np.linspace(-2.0, 2.0, 241)
    axes.plot(curve_x, curve_x * curve_x, np.zeros_like(curve_x), color=EDGE_COLOR, linewidth=1.3)
    axes.plot(curve_x, np.full_like(curve_x, 4.0), np.zeros_like(curve_x), color=EDGE_COLOR,
              linewidth=1.3)
    axes.plot(curve_x, curve_x * curve_x, (4.0 - curve_x * curve_x) / 2.0, color=EDGE_COLOR,
              linewidth=1.3)

    axes.set_xlabel("x", fontsize=10, labelpad=-3)
    axes.set_ylabel("y", fontsize=10, labelpad=-3)
    axes.set_zlabel("z", fontsize=10, labelpad=-5)
    axes.set_xlim(-2.0, 2.0)
    axes.set_ylim(0.0, 4.0)
    axes.set_zlim(0.0, 2.0)
    axes.set_xticks([-2, 0, 2])
    axes.set_yticks([0, 2, 4])
    axes.set_zticks([0, 1, 2])
    axes.tick_params(labelsize=8, pad=0)
    axes.grid(False)
    axes.set_box_aspect((4.0, 4.0, 2.4), zoom=1.14)
    axes.view_init(elev=28.0, azim=-52.0)
    axes.set_title("The solid E, closed by three surfaces", fontsize=10, pad=0)

    anchor_points = [(-1.90, 3.61, 0.00), (1.55, 3.20, 0.00), (0.00, 1.20, 1.40)]
    for anchor in anchor_points:
        axes.scatter([anchor[0]], [anchor[1]], [anchor[2]], color=EDGE_COLOR, s=11,
                     depthshade=False, zorder=20)

    legend_handles = [
        Patch(facecolor=WALL_COLOR, alpha=0.75, edgecolor=EDGE_COLOR, label="$y = x^2$"),
        Patch(facecolor=FLOOR_COLOR, alpha=0.85, edgecolor=EDGE_COLOR, label="$z = 0$"),
        Patch(facecolor=PLANE_COLOR, alpha=0.75, edgecolor=EDGE_COLOR, label="$y + 2z = 4$"),
    ]
    axes.legend(handles=legend_handles, loc="upper left", fontsize=8.0, frameon=False,
                handlelength=1.1, borderpad=0.1, labelspacing=0.25)


def draw_projection_z(axes: plt.Axes) -> None:
    """Draw the projection of E on the plane z = 0, which keeps the coordinates x and y.

    Args:
        axes: The axes of the upper right panel.
    """
    x_values = np.linspace(-2.0, 2.0, 400)
    axes.fill_between(x_values, x_values ** 2, 4.0, color=WALL_COLOR, alpha=0.45, linewidth=0.0)
    axes.plot(x_values, x_values ** 2, color=EDGE_COLOR, linewidth=1.4)
    axes.axhline(4.0, color=EDGE_COLOR, linewidth=1.4)
    axes.set_xlim(-2.7, 2.7)
    axes.set_ylim(-0.45, 4.7)
    axes.set_xticks([-2, -1, 0, 1, 2])
    axes.set_yticks([0, 1, 2, 3, 4])
    axes.set_xlabel("x", fontsize=10)
    axes.set_ylabel("y", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Projection on the plane $z = 0$\nkeeps $x$ and $y$", fontsize=9.5, pad=6)
    axes.text(-2.55, 1.35, "$y = x^2$", fontsize=8.5, color=EDGE_COLOR)
    axes.text(1.45, 4.18, "$y = 4$", fontsize=8.5, color=EDGE_COLOR)


def draw_projection_x(axes: plt.Axes) -> None:
    """Draw the projection of E on the plane x = 0, which keeps the coordinates y and z.

    Args:
        axes: The axes of the lower left panel.
    """
    axes.fill([0.0, 4.0, 0.0], [0.0, 0.0, 2.0], color=PLANE_COLOR, alpha=0.5, linewidth=0.0)
    axes.plot([0.0, 4.0, 0.0, 0.0], [0.0, 0.0, 2.0, 0.0], color=EDGE_COLOR, linewidth=1.4)
    axes.set_xlim(-0.45, 4.5)
    axes.set_ylim(-0.35, 2.45)
    axes.set_xticks([0, 1, 2, 3, 4])
    axes.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    axes.set_xlabel("y", fontsize=10)
    axes.set_ylabel("z", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Projection on the plane $x = 0$\nkeeps $y$ and $z$", fontsize=9.5, pad=6)
    axes.text(1.30, 1.72, "$y + 2z = 4$", fontsize=8.5, color=EDGE_COLOR)


def draw_projection_y(axes: plt.Axes) -> None:
    """Draw the projection of E on the plane y = 0, which keeps the coordinates x and z.

    Args:
        axes: The axes of the lower right panel.
    """
    x_values = np.linspace(-2.0, 2.0, 400)
    height = (4.0 - x_values ** 2) / 2.0
    axes.fill_between(x_values, 0.0, height, color="#9dc0a8", alpha=0.5, linewidth=0.0)
    axes.plot(x_values, height, color=EDGE_COLOR, linewidth=1.4)
    axes.axhline(0.0, color=EDGE_COLOR, linewidth=1.4)
    axes.set_xlim(-2.7, 2.7)
    axes.set_ylim(-0.35, 2.45)
    axes.set_xticks([-2, -1, 0, 1, 2])
    axes.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    axes.set_xlabel("x", fontsize=10)
    axes.set_ylabel("z", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Projection on the plane $y = 0$\nkeeps $x$ and $z$", fontsize=9.5, pad=6)
    axes.text(-2.55, 1.80, "$x^2 + 2z = 4$", fontsize=8.5, color=EDGE_COLOR)


def main() -> None:
    """Draw the four panels and write the figure."""
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    figure = plt.figure(figsize=(10.2, 8.6), dpi=170)
    solid_axes = figure.add_subplot(2, 2, 1, projection="3d")
    draw_solid(solid_axes)
    draw_projection_z(figure.add_subplot(2, 2, 2))
    draw_projection_x(figure.add_subplot(2, 2, 3))
    draw_projection_y(figure.add_subplot(2, 2, 4))
    figure.tight_layout(pad=1.5)
    figure.savefig(OUTPUT_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
