"""Draw the solid region E of the problem in three dimensions.

The figure shows the paraboloid x = 4*(y^2 + z^2), the plane x = 4, and the circle
where the two surfaces meet.  The shaded surface is the paraboloid.  The flat disk
is the part of the plane x = 4 that closes the solid.

The script writes the figure to code/figures/part1_figure1.png.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

FIGURE_DPI: int = 200
"""Resolution of the written image in dots per inch."""

COLOR_SURFACE: str = "#2f5d8a"
"""Fill color of the paraboloid."""

COLOR_PLANE: str = "#c8863c"
"""Fill color of the flat cap."""

COLOR_RIM: str = "#7a2f2f"
"""Color of the intersection circle."""

FIGURE_PATH: Path = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""Output path of the figure."""


def apply_style() -> None:
    """Set a consistent style for the figure."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Cambria", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.linewidth": 0.8,
        "figure.facecolor": "white",
    })


def draw_paraboloid(axes: plt.Axes) -> None:
    """Draw the paraboloid surface.

    Args:
        axes: The three dimensional axes of the figure.
    """
    radial_values = np.linspace(0.0, 1.0, 120)
    angle_values = np.linspace(0.0, 2.0 * math.pi, 160)
    radius_grid, angle_grid = np.meshgrid(radial_values, angle_values)
    x_grid = PARABOLOID_COEFFICIENT * radius_grid**2
    y_grid = radius_grid * np.cos(angle_grid)
    z_grid = radius_grid * np.sin(angle_grid)
    axes.plot_surface(x_grid, y_grid, z_grid, color=COLOR_SURFACE, alpha=0.45,
                      linewidth=0.0, antialiased=True, shade=True)
    for radius in (0.4, 0.7, 1.0):
        ring_angle = np.linspace(0.0, 2.0 * math.pi, 200)
        axes.plot(np.full_like(ring_angle, PARABOLOID_COEFFICIENT * radius**2),
                  radius * np.cos(ring_angle), radius * np.sin(ring_angle),
                  color=COLOR_SURFACE, linewidth=0.7, alpha=0.8)


def draw_cap(axes: plt.Axes) -> None:
    """Draw the flat disk of the plane x = 4.

    Args:
        axes: The three dimensional axes of the figure.
    """
    radial_values = np.linspace(0.0, 1.0, 40)
    angle_values = np.linspace(0.0, 2.0 * math.pi, 120)
    radius_grid, angle_grid = np.meshgrid(radial_values, angle_values)
    x_grid = np.full_like(radius_grid, PLANE_POSITION)
    y_grid = radius_grid * np.cos(angle_grid)
    z_grid = radius_grid * np.sin(angle_grid)
    axes.plot_surface(x_grid, y_grid, z_grid, color=COLOR_PLANE, alpha=0.30,
                      linewidth=0.0, antialiased=True, shade=False)
    ring_angle = np.linspace(0.0, 2.0 * math.pi, 300)
    axes.plot(np.full_like(ring_angle, PLANE_POSITION), np.cos(ring_angle), np.sin(ring_angle),
              color=COLOR_PLANE, linewidth=1.4)


def draw_intersection_circle(axes: plt.Axes) -> None:
    """Draw the circle where the paraboloid meets the plane.

    Args:
        axes: The three dimensional axes of the figure.
    """
    ring_angle = np.linspace(0.0, 2.0 * math.pi, 400)
    axes.plot(np.full_like(ring_angle, PLANE_POSITION), np.cos(ring_angle), np.sin(ring_angle),
              color=COLOR_RIM, linewidth=2.0)


def draw_guide_lines(axes: plt.Axes) -> None:
    """Draw the x axis and the two marked positions.

    Args:
        axes: The three dimensional axes of the figure.
    """
    axes.plot([0.0, 4.6], [0.0, 0.0], [0.0, 0.0], color="#333333", linewidth=1.0)
    axes.scatter([0.0], [0.0], [0.0], color="#333333", s=14, zorder=10)
    axes.text(0.02, -0.12, 0.12, r"$O$", fontsize=10)


def build_figure() -> plt.Figure:
    """Build the complete figure.

    Returns:
        The figure object that holds the panels.
    """
    figure = plt.figure(figsize=(6.4, 5.0))
    axes = figure.add_subplot(111, projection="3d")
    draw_paraboloid(axes)
    draw_cap(axes)
    draw_intersection_circle(axes)
    draw_guide_lines(axes)
    axes.set_xlabel(r"$x$", labelpad=6)
    axes.set_ylabel(r"$y$", labelpad=6)
    axes.set_zlabel(r"$z$", labelpad=6)
    axes.set_xlim(0.0, 4.6)
    axes.set_ylim(-1.25, 1.25)
    axes.set_zlim(-1.25, 1.25)
    axes.set_box_aspect((1.9, 1.0, 1.0))
    axes.view_init(elev=18.0, azim=-58.0)
    axes.set_xticks([0, 2, 4])
    axes.set_yticks([-1, 0, 1])
    axes.set_zticks([-1, 0, 1])
    axes.grid(False)
    for axis in (axes.xaxis, axes.yaxis, axes.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((0.85, 0.85, 0.85, 0.6))
    axes.text(1.35, 0.95, 0.95, r"$x = 4y^2 + 4z^2$", color=COLOR_SURFACE, fontsize=11)
    axes.text(4.05, -0.95, 0.75, r"$x = 4$", color="#8a5a1c", fontsize=11)
    axes.text(3.35, 0.55, -1.05, r"$y^2 + z^2 = 1$", color=COLOR_RIM, fontsize=9.5)
    figure.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
    return figure


def main() -> int:
    """Draw the figure and write it to the figures directory.

    Returns:
        The process exit status: 0 on success.
    """
    apply_style()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure = build_figure()
    figure.savefig(FIGURE_PATH, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
