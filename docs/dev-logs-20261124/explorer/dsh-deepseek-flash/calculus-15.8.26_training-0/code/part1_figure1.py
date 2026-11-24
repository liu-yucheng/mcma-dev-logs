"""Draw figure 1: the trace of the cylinder in the plane $z = 0$.

The trace is the circle $r = a\cos\theta$. The figure marks its center, its tangency
point at the origin, one radial segment of length $a\cos\theta$, and the diameter
of length $a$.

Run with ``code/.venv/Scripts/python.exe code/part1_figure1.py``.
"""

from __future__ import annotations

import math

import numpy as np
from matplotlib.axes import Axes

import figure_anchors as anchors
import figure_helpers as helpers

RADIUS = 1.0


def circle_points(sample_count: int = 400) -> tuple[np.ndarray, np.ndarray]:
    """Return the trace of the cylinder, sampled from its polar form.

    Args:
        sample_count: Number of samples of the angle.

    Returns:
        The arrays of the horizontal and the vertical coordinate.
    """
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, sample_count)
    radial = RADIUS * np.cos(angles)
    return radial * np.cos(angles), radial * np.sin(angles)


def dimension_arrow(axes: Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    """Draw a double arrow that names one length.

    Args:
        axes: Panel that receives the arrow.
        start: Coordinates of the first end.
        end: Coordinates of the second end.
    """
    axes.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "<|-|>",
            "color": helpers.MUTED,
            "linewidth": 0.95,
            "mutation_scale": 7.0,
            "shrinkA": 0.0,
            "shrinkB": 0.0,
        },
        zorder=18,
    )


def main() -> None:
    """Draw the figure and check where its labels sit."""
    figure = helpers.create_figure(6.6, 4.3)
    axes = helpers.make_panel(figure, (1, 1, 1), (-0.50, 1.56), (-1.04, 0.76))
    figure.subplots_adjust(left=0.02, right=0.98, bottom=0.03, top=0.97)

    x_values, y_values = circle_points()
    axes.fill(x_values, y_values, color=helpers.SPHERE_FILL, alpha=0.22, zorder=2)
    axes.plot(x_values, y_values, color=helpers.INK, linewidth=1.9, zorder=6)

    helpers.draw_axis(axes, (-0.46, 0.0), (1.44, 0.0))
    helpers.draw_axis(axes, (0.0, -0.80), (0.0, 0.66))

    texts = [
        helpers.axis_letter(axes, "$x$", (1.38, -0.13)),
        helpers.axis_letter(axes, "$y$", (-0.14, 0.60)),
    ]

    end_x = RADIUS * math.cos(anchors.RADIAL_ANGLE) ** 2
    end_y = RADIUS * math.cos(anchors.RADIAL_ANGLE) * math.sin(anchors.RADIAL_ANGLE)
    axes.plot([0.0, end_x], [0.0, end_y], color=helpers.CURVE_COLOR, linewidth=2.0, zorder=12)
    helpers.draw_dot(axes, (end_x, end_y))
    texts.append(helpers.draw_note(axes, (end_x + 0.06, end_y + 0.06), r"$P$", "left"))

    angle_arc = np.linspace(0.0, anchors.RADIAL_ANGLE, 60)
    axes.plot(0.30 * np.cos(angle_arc), 0.30 * np.sin(angle_arc), color=helpers.MUTED, linewidth=1.0)
    texts.append(helpers.draw_note(axes, (0.42, 0.12), r"$\theta$"))

    texts.append(
        axes.text(
            0.60,
            0.34,
            r"$r = a\cos\theta$",
            fontsize=10.5,
            color=helpers.CURVE_COLOR,
            ha="left",
            va="center",
            zorder=29,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.6},
        )
    )

    helpers.draw_dot(axes, (RADIUS / 2.0, 0.0), size=3.2)
    helpers.draw_dot(axes, (0.0, 0.0), size=3.2)
    texts.append(helpers.draw_note(axes, (RADIUS / 2.0, -0.16), r"$C = (a/2,\,0)$"))
    texts.append(helpers.draw_note(axes, (-0.04, -0.14), r"$O$", "right"))

    radius_x = RADIUS / 2.0 + 0.30 * math.cos(0.15)
    radius_y = 0.30 * math.sin(0.15)
    axes.plot([RADIUS / 2.0, radius_x], [0.0, radius_y], color=helpers.MUTED, linewidth=1.0, zorder=15)
    texts.append(helpers.draw_note(axes, (0.72, 0.13), r"$a/2$"))

    dimension_arrow(axes, (0.0, -0.66), (RADIUS, -0.66))
    texts.append(helpers.draw_note(axes, (0.50, -0.78), r"diameter $a$"))
    texts.append(
        helpers.draw_note(axes, (0.30, -0.38), r"angle range $-\pi/2 \leq \theta \leq \pi/2$")
    )

    margins = helpers.measure_texts(figure, axes, texts)
    assert min(margins) > 2.0, f"a label crosses the panel edge by {2.0 - min(margins):.1f} pixels"
    helpers.save_figure(figure, "part1_figure1.png")
    print(f"CHECK figure1_labels_inside_panel min_margin={min(margins):.1f} pixels")


if __name__ == "__main__":
    main()
