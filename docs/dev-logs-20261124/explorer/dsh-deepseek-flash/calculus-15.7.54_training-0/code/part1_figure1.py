"""Draw Figure 1: the solid E and its projection on the plane z = 0.

The left panel shows the paraboloid cap over the closed unit disk and the floor
of the solid. The right panel shows the projection, which is the closed unit
disk in the plane z = 0. Each surface label sits at a point whose coordinates
satisfy the equation of that surface, and the script proves that fact before it
draws the point.
"""

from __future__ import annotations

import math
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

FIGURE_NAME = "part1_figure1.png"
LABEL_FONT_SIZE = 11
TICK_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
SURFACE_ALPHA = 0.82
FLOOR_ALPHA = 0.66
AXIS_LENGTH = 1.58
LABEL_MARGIN = 0.12
COLOR_SURFACE = "#e0a458"
COLOR_FLOOR = "#7fa8d0"
COLOR_CURVE = "#a02828"
COLOR_AXIS = "#202020"


def paraboloid_height(x_value: float, y_value: float) -> float:
    """Return the height of the paraboloid z = 1 - x^2 - y^2 at one point."""
    return 1.0 - x_value * x_value - y_value * y_value


def draw_axis_arrows(solid_axes: plt.Axes) -> None:
    """Draw the three coordinate axes from the origin with one arrow each."""
    endpoints = ((AXIS_LENGTH, 0.0, 0.0), (0.0, AXIS_LENGTH, 0.0), (0.0, 0.0, AXIS_LENGTH))
    for endpoint in endpoints:
        solid_axes.quiver(
            0.0,
            0.0,
            0.0,
            endpoint[0],
            endpoint[1],
            endpoint[2],
            color=COLOR_AXIS,
            linewidth=1.1,
            arrow_length_ratio=0.11,
            zorder=12,
        )
    for endpoint, letter in zip(endpoints, ("$x$", "$y$", "$z$")):
        solid_axes.text(
            endpoint[0] + LABEL_MARGIN,
            endpoint[1] + LABEL_MARGIN,
            endpoint[2] + LABEL_MARGIN,
            letter,
            fontsize=LABEL_FONT_SIZE,
            color=COLOR_AXIS,
            zorder=12,
        )


def draw_unit_ticks(solid_axes: plt.Axes) -> None:
    """Write the tick value one on the x axis and on the z axis.

    The y extent is read from the ticks of the projection panel, because every
    free position of a third numeral in the solid panel falls on the fill.
    """
    tick_positions = (
        ((1.0, -0.14, -0.10), "1"),
        ((-0.19, -0.10, 1.0), "1"),
    )
    for position, tick_text in tick_positions:
        solid_axes.text(
            position[0],
            position[1],
            position[2],
            tick_text,
            fontsize=TICK_FONT_SIZE,
            color=COLOR_AXIS,
            zorder=12,
        )


def assert_label_inside_data_box(label_point: tuple[float, float, float]) -> None:
    """Raise an error when a label point lies outside the drawn data box."""
    limits = ((-1.30, 1.30), (-1.30, 1.30), (-0.30, 1.30))
    for value, limit_pair in zip(label_point, limits):
        if not limit_pair[0] < value < limit_pair[1]:
            raise ValueError("the label point leaves the data box")


def main() -> None:
    """Build the figure and write it beside the other figures of the session."""
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
    os.makedirs(output_directory, exist_ok=True)

    radius = np.linspace(0.0, 1.0, 80)
    angle = np.linspace(0.0, 2.0 * math.pi, 160)
    radius_grid, angle_grid = np.meshgrid(radius, angle)
    grid_x = radius_grid * np.cos(angle_grid)
    grid_y = radius_grid * np.sin(angle_grid)
    grid_z = 1.0 - radius_grid**2

    figure = plt.figure(figsize=(10.6, 4.9))
    solid_axes = figure.add_subplot(1, 2, 1, projection="3d")
    solid_axes.set_proj_type("ortho")
    solid_axes.computed_zorder = False
    solid_axes.plot_surface(
        grid_x,
        grid_y,
        np.zeros_like(grid_z),
        color=COLOR_FLOOR,
        alpha=FLOOR_ALPHA,
        linewidth=0.0,
        zorder=1,
    )
    solid_axes.plot_surface(
        grid_x,
        grid_y,
        grid_z,
        color=COLOR_SURFACE,
        alpha=SURFACE_ALPHA,
        linewidth=0.0,
        antialiased=True,
        shade=True,
        zorder=2,
    )
    solid_axes.plot(
        np.cos(angle),
        np.sin(angle),
        np.zeros_like(angle),
        color=COLOR_CURVE,
        linewidth=2.4,
        zorder=6,
    )

    surface_label_point = (-0.60, 0.46, paraboloid_height(-0.60, 0.46))
    floor_label_point = (0.46, -0.62, 0.0)
    if abs(surface_label_point[2] - paraboloid_height(-0.60, 0.46)) > 1.0e-12:
        raise ValueError("the surface label point does not satisfy the surface equation")
    if floor_label_point[2] != 0.0:
        raise ValueError("the floor label point does not satisfy the floor equation")
    if surface_label_point[0] ** 2 + surface_label_point[1] ** 2 > 1.0:
        raise ValueError("the surface label point lies outside the base disk")
    if floor_label_point[0] ** 2 + floor_label_point[1] ** 2 > 1.0:
        raise ValueError("the floor label point lies outside the base disk")
    for point in (surface_label_point, floor_label_point):
        assert_label_inside_data_box(point)

    solid_axes.text(
        surface_label_point[0],
        surface_label_point[1],
        surface_label_point[2] + 0.26,
        "$z = 1 - x^2 - y^2$",
        fontsize=LABEL_FONT_SIZE,
        color="#6d3f0c",
        zorder=12,
        horizontalalignment="center",
    )
    solid_axes.text(
        floor_label_point[0],
        floor_label_point[1],
        floor_label_point[2] - 0.20,
        "$z = 0$",
        fontsize=LABEL_FONT_SIZE,
        color="#20456b",
        zorder=12,
        horizontalalignment="center",
    )
    draw_axis_arrows(solid_axes)
    draw_unit_ticks(solid_axes)
    solid_axes.set_xlim(-1.30, 1.30)
    solid_axes.set_ylim(-1.30, 1.30)
    solid_axes.set_zlim(-0.30, 1.30)
    solid_axes.set_box_aspect((1.0, 1.0, 1.0))
    solid_axes.view_init(elev=18.0, azim=-64.0)
    solid_axes.set_axis_off()
    solid_axes.set_title("the solid $E$", fontsize=TITLE_FONT_SIZE, pad=-4.0)

    projection_axes = figure.add_subplot(1, 2, 2)
    projection_axes.add_patch(
        Circle((0.0, 0.0), 1.0, facecolor=COLOR_FLOOR, edgecolor=COLOR_CURVE, linewidth=2.4, alpha=0.72)
    )
    projection_axes.annotate(
        "",
        xy=(1.46, 0.0),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "-|>", "color": COLOR_AXIS, "linewidth": 1.1},
    )
    projection_axes.annotate(
        "",
        xy=(0.0, 1.46),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "-|>", "color": COLOR_AXIS, "linewidth": 1.1},
    )
    projection_axes.text(1.52, -0.20, "$x$", fontsize=LABEL_FONT_SIZE, color=COLOR_AXIS, horizontalalignment="right", verticalalignment="center")
    projection_axes.text(-0.18, 1.36, "$y$", fontsize=LABEL_FONT_SIZE, color=COLOR_AXIS, horizontalalignment="right", verticalalignment="center")
    projection_axes.text(0.12, 0.58, "$D$", fontsize=LABEL_FONT_SIZE + 1, color="#173a5c")
    projection_axes.text(
        0.0,
        -1.36,
        "$x^2 + y^2 \\leq 1$, area $\\pi$",
        fontsize=LABEL_FONT_SIZE,
        color="#173a5c",
        horizontalalignment="center",
    )
    projection_axes.set_xlim(-1.60, 1.60)
    projection_axes.set_ylim(-1.56, 1.52)
    projection_axes.set_aspect("equal")
    projection_axes.set_xticks([-1.0, 0.0, 1.0])
    projection_axes.set_yticks([-1.0, 0.0, 1.0])
    projection_axes.tick_params(labelsize=TICK_FONT_SIZE, length=3.0)
    projection_axes.set_title("the projection on the plane $z = 0$", fontsize=TITLE_FONT_SIZE, pad=8.0)
    for spine_name in ("top", "right"):
        projection_axes.spines[spine_name].set_visible(False)

    figure.tight_layout(pad=1.0)
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    axes_box = projection_axes.get_window_extent(renderer)
    for label in projection_axes.texts:
        extent = label.get_window_extent(renderer)
        if not (
            extent.x0 >= axes_box.x0
            and extent.x1 <= axes_box.x1
            and extent.y0 >= axes_box.y0
            and extent.y1 <= axes_box.y1
        ):
            raise ValueError(f"the label {label.get_text()!r} leaves the axes box")

    output_path = os.path.join(output_directory, FIGURE_NAME)
    figure.savefig(output_path, dpi=200)
    plt.close(figure)
    print("wrote", output_path)


if __name__ == "__main__":
    main()
