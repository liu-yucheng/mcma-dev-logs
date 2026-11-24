"""Draw the coordinate frame of a three dimensional figure and check the placement of its text.

The frame uses one mechanism for each axis: one arrow, one name at the tip of the
arrow, and one tick mark with one number at each value that the reader must read.
No letter is written twice.  Every text is an annotation of the projected point,
so the layout check can compare the pixel box of each text with the box of every
other text and with the box of the axes.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.text import Annotation
from mpl_toolkits.mplot3d import Axes3D, proj3d

ARROW_COLOR = "#111111"
AXIS_COLOR = "#111111"
HALO_STYLE = {"facecolor": "white", "edgecolor": "none", "alpha": 0.70, "pad": 0.22}
TICK_LENGTH = 0.10
TICK_FONT_SIZE = 10
AXIS_FONT_SIZE = 13
TICK_OFFSET_POINTS = (-8.0, -12.0)
AXIS_NAME_OFFSET_POINTS = {"x": (14.0, -2.0), "y": (14.0, 4.0), "z": (0.0, 14.0)}


def project_point(axes: Axes3D, x_value: float, y_value: float, z_value: float) -> tuple[float, float]:
    """Return the two projected coordinates of one three dimensional point.

    The projection uses the current view of the axes, so the caller must set the
    limits and the view before it asks for a projected point.
    """
    projected_x, projected_y, _ = proj3d.proj_transform(x_value, y_value, z_value, axes.get_proj())
    return float(projected_x), float(projected_y)


def draw_coordinate_frame(
    axes: Axes3D,
    axis_limit: float,
    top_height: float,
    horizontal_ticks: Sequence[float],
    vertical_ticks: Sequence[float],
) -> list[Annotation]:
    """Draw three arrows with one name each and one tick mark at each listed value.

    The two horizontal arrows run along the positive x axis and the positive y
    axis.  The vertical arrow runs along the positive z axis.  Each arrow carries
    its name at the tip, and each tick value carries one short mark and one
    number.  The function returns every text as an annotation of its projected
    point, so that the caller can check the layout.
    """
    axes.set_axis_off()
    arrow_length_ratio = 0.12
    axes.quiver(
        0.0, 0.0, 0.0, axis_limit + 0.55, 0.0, 0.0,
        color=ARROW_COLOR, linewidth=1.1, arrow_length_ratio=arrow_length_ratio, pivot="tail", zorder=15,
    )
    axes.quiver(
        0.0, 0.0, 0.0, 0.0, axis_limit + 0.55, 0.0,
        color=ARROW_COLOR, linewidth=1.1, arrow_length_ratio=arrow_length_ratio, pivot="tail", zorder=15,
    )
    axes.quiver(
        0.0, 0.0, 0.0, 0.0, 0.0, top_height + 0.60,
        color=ARROW_COLOR, linewidth=1.1, arrow_length_ratio=arrow_length_ratio, pivot="tail", zorder=15,
    )

    annotations: list[Annotation] = []
    for name, position in (
        (r"$x$", (axis_limit + 0.80, 0.0, 0.0)),
        (r"$y$", (0.0, axis_limit + 0.80, 0.0)),
        (r"$z$", (0.0, 0.0, top_height + 0.85)),
    ):
        annotations.append(
            _annotate(axes, name, position, AXIS_NAME_OFFSET_POINTS[name[1]], AXIS_FONT_SIZE, bold=True)
        )

    for tick_value in horizontal_ticks:
        axes.plot(
            [tick_value, tick_value], [0.0, -TICK_LENGTH], [0.0, 0.0],
            color=ARROW_COLOR, linewidth=0.9, zorder=15,
        )
        axes.plot(
            [0.0, -TICK_LENGTH], [tick_value, tick_value], [0.0, 0.0],
            color=ARROW_COLOR, linewidth=0.9, zorder=15,
        )
        annotations.append(
            _annotate(
                axes, f"{tick_value:g}", (tick_value, 0.0, 0.0), TICK_OFFSET_POINTS, TICK_FONT_SIZE,
            )
        )
        annotations.append(
            _annotate(
                axes, f"{tick_value:g}", (0.0, tick_value, 0.0), (-16.0, 4.0), TICK_FONT_SIZE,
            )
        )
    for tick_value in vertical_ticks:
        axes.plot(
            [0.0, TICK_LENGTH], [0.0, 0.0], [tick_value, tick_value],
            color=ARROW_COLOR, linewidth=0.9, zorder=15,
        )
        annotations.append(
            _annotate(
                axes, f"{tick_value:g}", (0.0, 0.0, tick_value), (20.0, 0.0), TICK_FONT_SIZE,
            )
        )
    return annotations


def annotate_surface_point(
    axes: Axes3D,
    text: str,
    position: tuple[float, float, float],
    offset_points: tuple[float, float],
) -> Annotation:
    """Label one surface at a point of that surface, with a leader and a halo.

    The caller gives a point that the equation of the surface satisfies.  The
    text sits at ``offset_points`` from the projected point and a thin leader
    joins the text to the point, so that no label floats away from its surface.
    """
    axes.plot(
        [position[0]], [position[1]], [position[2]],
        marker="o", markersize=3.6, color=AXIS_COLOR, zorder=18,
    )
    projected_x, projected_y = project_point(axes, *position)
    return axes.annotate(
        text,
        xy=(projected_x, projected_y),
        xytext=offset_points,
        textcoords="offset points",
        fontsize=10.0,
        color="#101010",
        ha="center",
        va="center",
        bbox=HALO_STYLE,
        arrowprops={"arrowstyle": "-", "color": AXIS_COLOR, "linewidth": 0.8, "shrinkA": 6.0, "shrinkB": 2.0},
        zorder=25,
    )


def _annotate(
    axes: Axes3D,
    text: str,
    position: tuple[float, float, float],
    offset_points: tuple[float, float],
    font_size: float,
    bold: bool = False,
) -> Annotation:
    """Place one text at an offset in points from the projected point of ``position``."""
    projected_x, projected_y = project_point(axes, *position)
    return axes.annotate(
        text,
        xy=(projected_x, projected_y),
        xytext=offset_points,
        textcoords="offset points",
        fontsize=font_size,
        fontweight="bold" if bold else "normal",
        color=AXIS_COLOR,
        ha="center",
        va="center",
        bbox=HALO_STYLE,
        zorder=26,
    )


def assert_annotations_do_not_overlap(figure: plt.Figure, annotations: Iterable[Annotation]) -> None:
    """Assert that no two text boxes overlap and that each box lies inside the axes.

    The check draws the figure first, because a pixel box exists only after the
    draw.  A pair of overlapping boxes hides a number or a name from the reader,
    so the check stops the script.
    """
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    labelled_boxes = [(annotation.get_text(), annotation.get_window_extent(renderer=renderer))
                      for annotation in annotations]
    axes_box = figure.axes[0].bbox
    for label, box in labelled_boxes:
        if box.x0 < axes_box.x0 - 2.0 or box.x1 > axes_box.x1 + 2.0:
            raise AssertionError(
                f"the text {label!r} leaves the axes box in x: {box.x0:.0f} to {box.x1:.0f} "
                f"against {axes_box.x0:.0f} to {axes_box.x1:.0f}"
            )
        if box.y0 < axes_box.y0 - 2.0 or box.y1 > axes_box.y1 + 2.0:
            raise AssertionError(
                f"the text {label!r} leaves the axes box in y: {box.y0:.0f} to {box.y1:.0f} "
                f"against {axes_box.y0:.0f} to {axes_box.y1:.0f}"
            )
    for first_index in range(len(labelled_boxes)):
        for second_index in range(first_index + 1, len(labelled_boxes)):
            first_label, first_box = labelled_boxes[first_index]
            second_label, second_box = labelled_boxes[second_index]
            if first_box.overlaps(second_box):
                raise AssertionError(
                    f"the texts {first_label!r} and {second_label!r} overlap: "
                    f"{first_box.x0:.0f},{first_box.y0:.0f} against {second_box.x0:.0f},{second_box.y0:.0f}"
                )
    print(f"text boxes checked for overlap and for the axes box: {len(labelled_boxes)}")


def assert_legend_inside_axes(figure: plt.Figure, axes: plt.Axes, legend: Legend) -> None:
    """Assert that the box of a legend lies inside the axes box of its figure."""
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    legend_box = legend.get_window_extent(renderer=renderer)
    axes_box = axes.bbox
    inside = (
        legend_box.x0 >= axes_box.x0
        and legend_box.x1 <= axes_box.x1
        and legend_box.y0 >= axes_box.y0
        and legend_box.y1 <= axes_box.y1
    )
    if not inside:
        raise AssertionError(
            f"the legend leaves the axes box: x {legend_box.x0:.0f} to {legend_box.x1:.0f}, "
            f"y {legend_box.y0:.0f} to {legend_box.y1:.0f}, "
            f"box {axes_box.x0:.0f} to {axes_box.x1:.0f} by {axes_box.y0:.0f} to {axes_box.y1:.0f}"
        )


def assert_annotation_inside_axes(figure: plt.Figure, axes: plt.Axes, text: plt.Text) -> None:
    """Assert that the box of an annotation lies inside the axes box of its figure."""
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    text_box = text.get_window_extent(renderer=renderer)
    axes_box = axes.bbox
    inside = (
        text_box.x0 >= axes_box.x0
        and text_box.x1 <= axes_box.x1
        and text_box.y0 >= axes_box.y0
        and text_box.y1 <= axes_box.y1
    )
    if not inside:
        raise AssertionError(
            f"the annotation {text.get_text()!r} leaves the axes box: "
            f"x {text_box.x0:.0f} to {text_box.x1:.0f}, y {text_box.y0:.0f} to {text_box.y1:.0f}, "
            f"box {axes_box.x0:.0f} to {axes_box.x1:.0f} by {axes_box.y0:.0f} to {axes_box.y1:.0f}"
        )
