"""Draw Figure 1: the two paraboloids and the circle where the two surfaces meet.

The figure is the instrument of Part 1.  It shows each surface over the disk of
squared radius 5/2, the circle where the surfaces meet, one name at each axis,
one tick at each value that the reader must read, and one label at a point of
each surface that the equation of that surface satisfies.  The script checks the
layout of every text before it writes the image.
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from drawing_frame import (
    annotate_surface_point,
    assert_annotations_do_not_overlap,
    draw_coordinate_frame,
)
from solid_geometry import (
    AXIS_LIMIT,
    TOP_HEIGHT,
    build_label_anchors,
    build_meeting_circle,
    build_surface_meshes,
)

FIGURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "part1_figure1.png")
LOWER_COLOR = "#3f74a8"
UPPER_COLOR = "#c1703c"
CIRCLE_COLOR = "#101010"
HORIZONTAL_TICKS = (1.0, 2.0)
VERTICAL_TICKS = (1.0, 3.0, 5.0)
LABEL_OFFSET_POINTS = {
    "lower": (-92.0, -58.0),
    "upper": (-132.0, 20.0),
    "circle": (96.0, 44.0),
}


def draw_figure() -> plt.Figure:
    """Build the figure of the two paraboloids and return it."""
    meshes = build_surface_meshes()
    circle = build_meeting_circle()
    figure = plt.figure(figsize=(7.2, 6.2), dpi=170)
    axes = figure.add_axes((0.01, 0.01, 0.98, 0.90), projection="3d")
    axes.plot_surface(
        meshes["x"], meshes["y"], meshes["lower"],
        color=LOWER_COLOR, alpha=0.62, linewidth=0.15, edgecolor="#2b557f",
        rstride=2, cstride=4, shade=True,
    )
    axes.plot_surface(
        meshes["x"], meshes["y"], meshes["upper"],
        color=UPPER_COLOR, alpha=0.62, linewidth=0.15, edgecolor="#8d4d24",
        rstride=2, cstride=4, shade=True,
    )
    axes.plot(circle["x"], circle["y"], circle["z"], color=CIRCLE_COLOR, linewidth=2.2, zorder=12)
    axes.set_xlim(-2.30, 3.30)
    axes.set_ylim(-2.30, 2.70)
    axes.set_zlim(0.0, 6.05)
    axes.set_box_aspect((1.0, 1.0, 0.94))
    axes.view_init(elev=24.0, azim=-52.0)
    axes.set_title(
        "The two paraboloids and the circle where they meet",
        fontsize=11.5, color="#1b2836", pad=4.0,
    )
    annotations = draw_coordinate_frame(
        axes, AXIS_LIMIT, TOP_HEIGHT, HORIZONTAL_TICKS, VERTICAL_TICKS,
    )
    for anchor in build_label_anchors():
        key = str(anchor["key"])
        position = (float(anchor["x"]), float(anchor["y"]), float(anchor["z"]))
        annotations.append(
            annotate_surface_point(axes, str(anchor["text"]), position, LABEL_OFFSET_POINTS[key])
        )
    assert_annotations_do_not_overlap(figure, annotations)
    return figure


def main() -> None:
    """Write the figure to the figures directory."""
    os.makedirs(os.path.dirname(FIGURE_PATH), exist_ok=True)
    figure = draw_figure()
    figure.savefig(FIGURE_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
