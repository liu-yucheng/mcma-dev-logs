"""Draw the solid of Part 1 in three dimensions.

The figure shows the four boundary surfaces, one label per surface at a point that satisfies the
equation of that surface, and the section of the solid at the demonstration height.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from figure_support import save_figure
from geometry_anchors import (
    CYLINDER_RADIUS,
    DEMO_HEIGHT_Y,
    FIGURE_DPI,
    PLANE_SLOPE,
    SURFACE_ALPHA,
    SURFACE_LABEL_POINTS,
)

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory that holds every rendered figure."""

SURFACE_STEPS = 81
"""Number of parameter steps of each curved surface."""

PLANE_ALPHA = 0.45
"""Opacity of the two flat boundary faces of the solid."""

LABEL_FONT_SIZE = 11
"""Font size of every surface label."""


def check_label_points() -> None:
    """Check that each label point satisfies the equation of the surface that it labels."""
    points = SURFACE_LABEL_POINTS
    cylinder_point = points["cylinder"]
    if abs(cylinder_point[1] ** 2 + cylinder_point[2] ** 2 - CYLINDER_RADIUS**2) > 1.0e-12:
        raise AssertionError("the cylinder label point is not on the cylinder")
    if abs(points["plane_x_zero"][0]) > 1.0e-12:
        raise AssertionError("the label point of the plane x = 0 is not on that plane")
    if abs(points["plane_y_three_x"][1] - PLANE_SLOPE * points["plane_y_three_x"][0]) > 1.0e-12:
        raise AssertionError("the label point of the plane y = 3x is not on that plane")
    if abs(points["plane_z_zero"][2]) > 1.0e-12:
        raise AssertionError("the label point of the plane z = 0 is not on that plane")


def draw_cylinder_wall(axes: plt.Axes) -> None:
    """Draw the part of the cylinder that bounds the solid.

    Args:
        axes: Three dimensional axes of the figure.
    """
    angle = np.linspace(0.0, math.pi / 2.0, SURFACE_STEPS)
    depth = np.linspace(0.0, 1.0, 61)
    angle_grid, depth_grid = np.meshgrid(angle, depth)
    wall_y = CYLINDER_RADIUS * np.cos(angle_grid)
    wall_z = CYLINDER_RADIUS * np.sin(angle_grid)
    depth_grid = np.where(depth_grid <= wall_y / PLANE_SLOPE, depth_grid, np.nan)
    axes.plot_surface(
        depth_grid,
        wall_y,
        wall_z,
        color="#4C78A8",
        alpha=SURFACE_ALPHA,
        linewidth=0.0,
        antialiased=True,
    )


def draw_plane_x_zero(axes: plt.Axes) -> None:
    """Draw the quarter disk that the solid has on the plane x = 0.

    Args:
        axes: Three dimensional axes of the figure.
    """
    angle = np.linspace(0.0, math.pi / 2.0, 161)
    vertices = [(0.0, 0.0, 0.0)]
    vertices.extend(
        (0.0, float(CYLINDER_RADIUS * math.cos(value)), float(CYLINDER_RADIUS * math.sin(value)))
        for value in angle
    )
    patch = Poly3DCollection([vertices], facecolor="#F58518", alpha=PLANE_ALPHA, edgecolor="#B8540A")
    axes.add_collection3d(patch)


def draw_plane_z_zero(axes: plt.Axes) -> None:
    """Draw the triangle that the solid has on the plane z = 0.

    Args:
        axes: Three dimensional axes of the figure.
    """
    corners = [(0.0, 0.0, 0.0), (0.0, CYLINDER_RADIUS, 0.0), (1.0, CYLINDER_RADIUS, 0.0)]
    patch = Poly3DCollection([corners], facecolor="#54A24B", alpha=PLANE_ALPHA, edgecolor="#2F6B2A")
    axes.add_collection3d(patch)


def draw_plane_y_three_x(axes: plt.Axes) -> None:
    """Draw the rectangle that the solid has on the plane y = 3x.

    Args:
        axes: Three dimensional axes of the figure.
    """
    x_values = np.linspace(0.0, 1.0, 2)
    z_values = np.linspace(0.0, CYLINDER_RADIUS, 2)
    x_grid, z_grid = np.meshgrid(x_values, z_values)
    axes.plot_surface(
        x_grid,
        PLANE_SLOPE * x_grid,
        z_grid,
        color="#E45756",
        alpha=0.28,
        linewidth=0.0,
    )


def draw_demo_section(axes: plt.Axes) -> None:
    """Draw the rectangle section of the solid at the demonstration height.

    Args:
        axes: Three dimensional axes of the figure.
    """
    half_height = math.sqrt(CYLINDER_RADIUS**2 - DEMO_HEIGHT_Y**2)
    x_values = np.array([0.0, DEMO_HEIGHT_Y / PLANE_SLOPE])
    z_values = np.array([0.0, half_height])
    x_grid, z_grid = np.meshgrid(x_values, z_values)
    axes.plot_surface(
        x_grid,
        np.full_like(x_grid, DEMO_HEIGHT_Y),
        z_grid,
        color="#B279A2",
        alpha=0.55,
        linewidth=0.0,
    )
    axes.plot(
        [0.0, DEMO_HEIGHT_Y / PLANE_SLOPE],
        [DEMO_HEIGHT_Y, DEMO_HEIGHT_Y],
        [half_height, half_height],
        color="#7A3E6E",
        linewidth=1.4,
    )


def main() -> None:
    """Draw the figure and write it to the figure directory."""
    check_label_points()
    figure = plt.figure(figsize=(6.6, 5.6), dpi=FIGURE_DPI)
    axes = figure.add_subplot(projection="3d")
    draw_cylinder_wall(axes)
    draw_plane_x_zero(axes)
    draw_plane_z_zero(axes)
    draw_plane_y_three_x(axes)

    points = SURFACE_LABEL_POINTS
    labels = [
        (r"$y^{2} + z^{2} = 9$", points["cylinder"], (0.00, -0.20, 0.16)),
        (r"$x = 0$", points["plane_x_zero"], (0.10, 0.10, 0.10)),
        (r"$y = 3x$", points["plane_y_three_x"], (0.10, -0.30, 0.18)),
        (r"$z = 0$", points["plane_z_zero"], (0.10, -0.20, 0.12)),
    ]
    texts = []
    for text_value, anchor, offset in labels:
        texts.append(
            axes.text(
                anchor[0] + offset[0],
                anchor[1] + offset[1],
                anchor[2] + offset[2],
                text_value,
                fontsize=LABEL_FONT_SIZE,
                color="#222222",
            )
        )

    axes.set_xlabel(r"$x$", labelpad=8)
    axes.set_ylabel(r"$y$", labelpad=8)
    axes.set_zlabel(r"$z$", labelpad=8)
    axes.set_xlim(-0.05, 1.15)
    axes.set_ylim(0.0, CYLINDER_RADIUS + 0.35)
    axes.set_zlim(0.0, CYLINDER_RADIUS + 0.15)
    axes.view_init(elev=18.0, azim=-62.0)
    axes.set_box_aspect((0.9, 1.0, 1.0))
    axes.grid(False)
    for text, (text_value, anchor, offset) in zip(texts, labels):
        print(f"label {text_value!r} anchored at {anchor} with offset {offset}")
    print(f"the figure carries {len(texts)} text labels")
    figure.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
    save_figure(figure, FIGURE_DIRECTORY / "part1_figure1.png")
    plt.close(figure)


if __name__ == "__main__":
    main()
