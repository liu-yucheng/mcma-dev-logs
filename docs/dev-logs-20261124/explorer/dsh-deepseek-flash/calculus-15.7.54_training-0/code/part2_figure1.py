"""Draw Figure 2: the vertical section of the solid at y = 0.

The section is the plane region between the parabola z = 1 - x^2 and the line
z = 0. The horizontal chord at height z is the diameter of the horizontal
section of the solid, so the area of that section is pi (1 - z) and not the area
of an annulus. The script proves the two chord endpoints before it draws them.
"""

from __future__ import annotations

import math
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part2_figure1.png"
LABEL_FONT_SIZE = 11
TICK_FONT_SIZE = 10
TITLE_FONT_SIZE = 12
COLOR_SECTION = "#e0a458"
COLOR_CHORD = "#1f5f8b"
COLOR_AXIS = "#202020"
COLOR_PARABOLA = "#a0522d"
HEIGHT_VALUES = (0.25, 0.5, 0.75)


def paraboloid_height(x_value: float) -> float:
    """Return the height z = 1 - x^2 of the section curve at y = 0."""
    return 1.0 - x_value * x_value


def chord_half_width(height_value: float) -> float:
    """Return the half width of the horizontal chord at one height."""
    return math.sqrt(1.0 - height_value)


def main() -> None:
    """Build the figure and write it beside the other figures of the session."""
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
    os.makedirs(output_directory, exist_ok=True)

    horizontal_values = np.linspace(-1.0, 1.0, 400)
    height_values = paraboloid_height(horizontal_values)

    figure, axes = plt.subplots(figsize=(7.6, 4.9))
    axes.fill_between(horizontal_values, 0.0, height_values, color=COLOR_SECTION, alpha=0.55)
    axes.plot(horizontal_values, height_values, color=COLOR_PARABOLA, linewidth=2.4)
    axes.plot([-1.0, 1.0], [0.0, 0.0], color=COLOR_AXIS, linewidth=1.4)

    for height_value in HEIGHT_VALUES:
        half_width = chord_half_width(height_value)
        if abs(paraboloid_height(half_width) - height_value) > 1.0e-12:
            raise ValueError("the chord endpoint does not satisfy the section curve")
        if abs(paraboloid_height(-half_width) - height_value) > 1.0e-12:
            raise ValueError("the chord endpoint does not satisfy the section curve")
        axes.plot([-half_width, half_width], [height_value, height_value], color=COLOR_CHORD, linewidth=1.3)

    main_height = 0.5
    main_half_width = chord_half_width(main_height)
    axes.plot(
        [main_half_width, main_half_width],
        [0.0, main_height],
        color=COLOR_CHORD,
        linewidth=1.0,
        linestyle=(0, (4, 3)),
    )
    axes.plot(
        [-main_half_width, -main_half_width],
        [0.0, main_height],
        color=COLOR_CHORD,
        linewidth=1.0,
        linestyle=(0, (4, 3)),
    )
    axes.annotate(
        "$\\sqrt{1 - z}$",
        xy=(main_half_width / 2.0, 0.0),
        xytext=(main_half_width / 2.0, -0.20),
        fontsize=LABEL_FONT_SIZE,
        color=COLOR_CHORD,
        ha="center",
        arrowprops={"arrowstyle": "-|>", "color": COLOR_CHORD, "linewidth": 1.0},
    )
    axes.text(
        0.02,
        main_height - 0.09,
        "chord at $z = 0.5$",
        fontsize=LABEL_FONT_SIZE,
        color=COLOR_CHORD,
        ha="center",
    )
    axes.annotate(
        "$z = 1 - x^2$",
        xy=(-0.60, paraboloid_height(-0.60)),
        xytext=(-1.00, 0.94),
        fontsize=LABEL_FONT_SIZE,
        color="#6d3f0c",
        arrowprops={"arrowstyle": "-", "color": "#6d3f0c", "linewidth": 0.9},
    )
    axes.text(
        0.52,
        0.11,
        "section of $E$",
        fontsize=LABEL_FONT_SIZE,
        color="#6d3f0c",
    )
    axes.text(
        0.0,
        -0.30,
        "every horizontal chord is a diameter, so each horizontal section is a disk",
        fontsize=LABEL_FONT_SIZE - 1,
        color="#333333",
        ha="center",
    )

    axes.set_xlim(-1.35, 1.35)
    axes.set_ylim(-0.40, 1.22)
    axes.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 0.5, 1.0])
    axes.tick_params(labelsize=TICK_FONT_SIZE)
    axes.set_xlabel("$x$", fontsize=LABEL_FONT_SIZE, color=COLOR_AXIS)
    axes.set_ylabel("$z$", fontsize=LABEL_FONT_SIZE, color=COLOR_AXIS)
    axes.set_title("the section of $E$ at $y = 0$", fontsize=TITLE_FONT_SIZE, pad=8.0)
    for spine_name in ("top", "right"):
        axes.spines[spine_name].set_visible(False)

    figure.tight_layout(pad=0.8)
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    axes_box = axes.get_window_extent(renderer)
    for label in axes.texts:
        extent = label.get_window_extent(renderer)
        inside = (
            extent.x0 >= axes_box.x0
            and extent.x1 <= axes_box.x1
            and extent.y0 >= axes_box.y0
            and extent.y1 <= axes_box.y1
        )
        if not inside:
            raise ValueError(f"the label {label.get_text()!r} leaves the axes box")

    output_path = os.path.join(output_directory, FIGURE_NAME)
    figure.savefig(output_path, dpi=200)
    plt.close(figure)
    print("wrote", output_path)


if __name__ == "__main__":
    main()
