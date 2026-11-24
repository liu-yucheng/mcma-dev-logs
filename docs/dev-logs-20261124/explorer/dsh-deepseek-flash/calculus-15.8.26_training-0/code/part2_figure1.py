"""Draw figure 2: the footprint of the solid and one vertical segment of it.

The left panel shows the disk $r \le a\cos\theta$ together with one polar cell. The
right panel shows the plane that holds one ray of angle $\theta$ and the vertical
segment of the solid above that ray.

Run with ``code/.venv/Scripts/python.exe code/part2_figure1.py``.
"""

from __future__ import annotations

import math

import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Polygon

import figure_anchors as anchors
import figure_helpers as helpers

RADIUS = 1.0


def footprint_boundary(sample_count: int = 400) -> tuple[np.ndarray, np.ndarray]:
    """Return the boundary of the footprint as a closed curve.

    Args:
        sample_count: Number of samples of the angle.

    Returns:
        The arrays of the horizontal and the vertical coordinate.
    """
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, sample_count)
    radial = RADIUS * np.cos(angles)
    return radial * np.cos(angles), radial * np.sin(angles)


def cell_outline(sample_count: int = 40) -> np.ndarray:
    """Return the corner points of one polar cell of the footprint.

    Args:
        sample_count: Number of samples along each radial edge.

    Returns:
        The array of the corner points, in order around the cell.
    """
    inner_angles = np.linspace(anchors.CELL_ANGLE_START, anchors.CELL_ANGLE_END, sample_count)
    outer_angles = inner_angles[::-1]
    inner_x = anchors.CELL_INNER_RADIUS * np.cos(inner_angles)
    inner_y = anchors.CELL_INNER_RADIUS * np.sin(inner_angles)
    outer_x = anchors.CELL_OUTER_RADIUS * np.cos(outer_angles)
    outer_y = anchors.CELL_OUTER_RADIUS * np.sin(outer_angles)
    return np.column_stack([np.concatenate([inner_x, outer_x]), np.concatenate([inner_y, outer_y])])


def draw_footprint_panel(axes: Axes) -> list[helpers.Text]:
    """Draw the left panel of the figure.

    Args:
        axes: Panel that receives the drawing.

    Returns:
        The text objects of the panel.
    """
    x_values, y_values = footprint_boundary()
    axes.fill(x_values, y_values, color=helpers.SPHERE_FILL, alpha=0.22, zorder=2)
    axes.plot(x_values, y_values, color=helpers.INK, linewidth=1.8, zorder=6)

    axes.add_patch(
        Polygon(cell_outline(), closed=True, facecolor=helpers.CELL_FILL, alpha=0.30, edgecolor="none", zorder=4)
    )
    for angle_value in (anchors.CELL_ANGLE_START, anchors.CELL_ANGLE_END):
        axes.plot(
            [anchors.CELL_INNER_RADIUS * math.cos(angle_value), anchors.CELL_OUTER_RADIUS * math.cos(angle_value)],
            [anchors.CELL_INNER_RADIUS * math.sin(angle_value), anchors.CELL_OUTER_RADIUS * math.sin(angle_value)],
            color=helpers.CELL_FILL,
            linewidth=1.2,
            zorder=8,
        )
    for radius_value in (anchors.CELL_INNER_RADIUS, anchors.CELL_OUTER_RADIUS):
        arc = np.linspace(anchors.CELL_ANGLE_START, anchors.CELL_ANGLE_END, 40)
        axes.plot(
            radius_value * np.cos(arc),
            radius_value * np.sin(arc),
            color=helpers.CELL_FILL,
            linewidth=1.2,
            zorder=8,
        )

    helpers.draw_axis(axes, (-0.22, 0.0), (0.78, 0.0))
    helpers.draw_axis(axes, (0.0, -0.62), (0.0, 0.62))
    texts = [
        helpers.axis_letter(axes, "$x$", (0.72, -0.11)),
        helpers.axis_letter(axes, "$y$", (-0.11, 0.56)),
    ]

    end_x = RADIUS * math.cos(anchors.SIDE_VIEW_ANGLE) ** 2
    end_y = RADIUS * math.cos(anchors.SIDE_VIEW_ANGLE) * math.sin(anchors.SIDE_VIEW_ANGLE)
    axes.plot([0.0, end_x], [0.0, end_y], color=helpers.CURVE_COLOR, linewidth=1.6, zorder=12)

    texts.append(helpers.draw_note(axes, (0.20, -0.34), r"footprint $D$"))
    texts.append(helpers.draw_note(axes, (0.50, 0.16), r"cell"))
    texts.append(helpers.draw_note(axes, (-0.05, -0.10), r"$O$", "right"))
    return texts


def draw_side_panel(axes: Axes) -> list[helpers.Text]:
    """Draw the right panel of the figure.

    Args:
        axes: Panel that receives the drawing.

    Returns:
        The text objects of the panel.
    """
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, 400)
    axes.plot(RADIUS * np.cos(angles), RADIUS * np.sin(angles), color=helpers.INK, linewidth=1.8, zorder=6)

    radial_position = RADIUS * math.cos(anchors.SIDE_VIEW_ANGLE)
    height = RADIUS * math.sin(anchors.SIDE_VIEW_ANGLE)
    axes.plot(
        [radial_position, radial_position],
        [-height, height],
        color=helpers.CURVE_COLOR,
        linewidth=2.6,
        zorder=12,
    )
    helpers.draw_dot(axes, (radial_position, height), size=3.4)
    helpers.draw_dot(axes, (radial_position, -height), size=3.4)
    axes.plot([0.0, radial_position], [0.0, 0.0], color=helpers.GUIDE, linewidth=0.9, zorder=4)

    helpers.draw_axis(axes, (-0.14, 0.0), (1.26, 0.0))
    helpers.draw_axis(axes, (0.0, -0.72), (0.0, 0.72))
    texts = [
        helpers.axis_letter(axes, "$r$", (1.20, -0.12)),
        helpers.axis_letter(axes, "$z$", (-0.12, 0.66)),
        helpers.draw_tick(axes, (radial_position, 0.0), (0.0, -0.035), r"$a\cos\theta$"),
        helpers.draw_tick(axes, (RADIUS, 0.0), (0.0, -0.10), r"$a$"),
    ]

    texts.append(
        axes.text(
            radial_position - 0.06,
            0.30,
            r"$z = \pm\sqrt{a^{2} - r^{2}}$",
            fontsize=9.5,
            color=helpers.CURVE_COLOR,
            ha="right",
            va="center",
            zorder=29,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.4},
        )
    )
    texts.append(helpers.draw_note(axes, (0.44, 0.64), r"$r^{2} + z^{2} = a^{2}$"))
    return texts


def main() -> None:
    """Draw both panels and check where the labels sit."""
    figure = helpers.create_figure(8.6, 3.6)
    left_axes = figure.add_axes((0.03, 0.06, 0.46, 0.86))
    right_axes = figure.add_axes((0.53, 0.06, 0.44, 0.86))
    for panel, x_limits, y_limits in (
        (left_axes, (-0.28, 1.10), (-0.66, 0.66)),
        (right_axes, (-0.16, 1.28), (-0.80, 0.80)),
    ):
        panel.set_xlim(*x_limits)
        panel.set_ylim(*y_limits)
        panel.set_aspect("equal", adjustable="box")
        for spine in panel.spines.values():
            spine.set_visible(False)
        panel.set_xticks([])
        panel.set_yticks([])

    left_texts = draw_footprint_panel(left_axes)
    right_texts = draw_side_panel(right_axes)

    left_margins = helpers.measure_texts(figure, left_axes, left_texts)
    right_margins = helpers.measure_texts(figure, right_axes, right_texts)
    smallest = min(min(left_margins), min(right_margins))
    assert smallest > 2.0, f"a label crosses a panel edge by {2.0 - smallest:.1f} pixels"
    helpers.save_figure(figure, "part2_figure1.png")
    print(f"CHECK figure2_labels_inside_panels min_margin={smallest:.1f} pixels")


if __name__ == "__main__":
    main()
