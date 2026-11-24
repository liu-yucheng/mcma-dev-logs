r"""Draw Figure 3: the solid that answers the problem, with one scale on each axis.

The left panel shows the closed body that the two paraboloids enclose.  The right
panel shows the same body cut by the plane $y = 0$, so that the lens shape and the
two meeting points are visible without the perspective.  Every text is checked
against its axes box before the image is written.
"""

from __future__ import annotations

import math
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from drawing_frame import (
    annotate_surface_point,
    assert_annotations_do_not_overlap,
    assert_annotation_inside_axes,
    draw_coordinate_frame,
)
from solid_geometry import (
    AXIS_LIMIT,
    RIM_SQUARED_RADIUS,
    TOP_HEIGHT,
    build_label_anchors,
    build_meeting_circle,
    build_surface_meshes,
)

FIGURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "part4_figure1.png")
LOWER_COLOR = "#3f74a8"
UPPER_COLOR = "#c1703c"
CIRCLE_COLOR = "#101010"
HORIZONTAL_TICKS = (1.0, 2.0)
VERTICAL_TICKS = (1.0, 3.0, 5.0)
LABEL_OFFSET_POINTS = {
    "lower": (-72.0, -52.0),
    "upper": (-118.0, 34.0),
    "circle": (76.0, 46.0),
}


def draw_body(axes: plt.Axes) -> list:
    """Draw the closed body with its frame and return the text annotations."""
    meshes = build_surface_meshes()
    circle = build_meeting_circle()
    axes.plot_surface(
        meshes["x"], meshes["y"], meshes["lower"],
        color=LOWER_COLOR, alpha=0.66, linewidth=0.15, edgecolor="#2b557f",
        rstride=2, cstride=4, shade=True,
    )
    axes.plot_surface(
        meshes["x"], meshes["y"], meshes["upper"],
        color=UPPER_COLOR, alpha=0.66, linewidth=0.15, edgecolor="#8d4d24",
        rstride=2, cstride=4, shade=True,
    )
    axes.plot(circle["x"], circle["y"], circle["z"], color=CIRCLE_COLOR, linewidth=2.4, zorder=12)
    axes.set_xlim(-2.30, 3.30)
    axes.set_ylim(-2.30, 2.70)
    axes.set_zlim(0.0, 6.05)
    axes.set_box_aspect((1.0, 1.0, 0.94))
    axes.view_init(elev=24.0, azim=-52.0)
    annotations = draw_coordinate_frame(axes, AXIS_LIMIT, TOP_HEIGHT, HORIZONTAL_TICKS, VERTICAL_TICKS)
    for anchor in build_label_anchors():
        key = str(anchor["key"])
        position = (float(anchor["x"]), float(anchor["y"]), float(anchor["z"]))
        annotations.append(
            annotate_surface_point(axes, str(anchor["text"]), position, LABEL_OFFSET_POINTS[key])
        )
    return annotations


def draw_cross_section(axes: plt.Axes) -> None:
    """Draw the cut of the body by the plane y = 0, with one scale on each axis."""
    rim_radius = math.sqrt(RIM_SQUARED_RADIUS)
    x_values = np.linspace(-rim_radius, rim_radius, 401)
    axes.fill_between(x_values, x_values**2, TOP_HEIGHT - x_values**2, color="#9ec1e0", alpha=0.75)
    axes.plot(x_values, x_values**2, color=LOWER_COLOR, linewidth=1.8)
    axes.plot(x_values, TOP_HEIGHT - x_values**2, color=UPPER_COLOR, linewidth=1.8)
    for sign in (-1.0, 1.0):
        axes.plot(
            [sign * rim_radius, sign * rim_radius], [0.0, RIM_SQUARED_RADIUS],
            color="#4a4a4a", linewidth=0.9, linestyle=":",
        )
        axes.plot([sign * rim_radius], [RIM_SQUARED_RADIUS], marker="o", markersize=5.0, color=CIRCLE_COLOR)
    axes.axhline(0.0, color="#333333", linewidth=1.0)
    axes.axvline(0.0, color="#333333", linewidth=1.0)
    axes.set_xlim(-2.6, 2.6)
    axes.set_ylim(-0.35, 5.5)
    axes.set_xticks([-2.0, -1.0, 1.0, 2.0])
    axes.set_yticks([1.0, 3.0, 5.0])
    axes.set_xlabel("$x$")
    axes.set_ylabel("$z$")
    axes.set_title("The same body cut by the plane $y = 0$", fontsize=10.5)
    axes.grid(True, color="#e2e2e2", linewidth=0.6)
    meeting_annotation = axes.annotate(
        r"$x^{2} = \frac{5}{2}$, $z = \frac{5}{2}$",
        xy=(rim_radius, RIM_SQUARED_RADIUS),
        xytext=(-128.0, 26.0),
        textcoords="offset points",
        fontsize=9.0,
        arrowprops={"arrowstyle": "-", "color": "#4a4a4a", "linewidth": 0.9, "shrinkB": 2.0},
    )
    assert_annotation_inside_axes(axes.figure, axes, meeting_annotation)


def draw_figure() -> plt.Figure:
    """Build the answer drawing and return the figure."""
    figure = plt.figure(figsize=(11.6, 5.4), dpi=170)
    body_axes = figure.add_axes((0.005, 0.02, 0.50, 0.90), projection="3d")
    section_axes = figure.add_axes((0.56, 0.12, 0.40, 0.76))
    annotations = draw_body(body_axes)
    body_axes.set_title("The closed body, drawn", fontsize=10.5, pad=2.0)
    draw_cross_section(section_axes)
    assert_annotations_do_not_overlap(figure, annotations)
    return figure


def main() -> None:
    """Write Figure 3 to the figures directory."""
    os.makedirs(os.path.dirname(FIGURE_PATH), exist_ok=True)
    figure = draw_figure()
    figure.savefig(FIGURE_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
