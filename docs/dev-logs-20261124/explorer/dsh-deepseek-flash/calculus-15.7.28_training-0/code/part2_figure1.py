"""Draw figure 1 of part 2: the horizontal cuts of the solid at five heights.

Each cut is a rectangle in a plane of constant height.  The figure draws the five rectangles in
one common frame, so the reader sees that each cut holds the previous cut.  Each area text sits
inside the rectangle that it measures.
"""

import numpy as np

import figure_style
from figure_style import apply_style, save_figure

HEIGHTS = (0.0, 0.5, 1.0, 1.5, 2.0)
"""The heights at which the figure cuts the solid."""

SHADES = ("#1a365d", "#2b6cb0", "#4a90c4", "#8fb8d8", "#c05621")
"""The color of the cut at each height, from the bottom cut to the top cut."""


def area_of_cut(height):
    """Return the area of the rectangle that the solid cuts at one height.

    The value agrees with the record of `part2_verify.py`, which measures the same area by
    point sampling.

    Args:
        height: The height of the cut.

    Returns:
        The area of the rectangle as a float.
    """
    return (4.0 - height * height) * (2.0 - height)


def draw_cut_frame(axes):
    """Draw the five rectangles in the xz-plane and mark the top point."""
    for height, shade in zip(HEIGHTS, SHADES):
        width = 4.0 - height * height
        depth = 2.0 - height
        if width <= 0.0 or depth <= 0.0:
            continue
        rectangle_x = [0.0, width, width, 0.0, 0.0]
        rectangle_z = [0.0, 0.0, depth, depth, 0.0]
        axes.plot(rectangle_x, rectangle_z, color=shade, linewidth=1.8)
        axes.annotate(
            f"$y = {height:g}$, area ${area_of_cut(height):g}$",
            xy=(width * 0.5, depth),
            xytext=(0.14, depth + 0.06 + 0.02 * height),
            fontsize=11.5,
            color=shade,
        )
    axes.plot([0.0], [0.0], marker="o", markersize=7.0, color=SHADES[-1], zorder=5)
    axes.annotate(
        "$y = 2$, the cut is the point $T$",
        xy=(0.0, 0.0),
        xytext=(0.55, -0.28),
        fontsize=11.5,
        color=SHADES[-1],
        arrowprops={"arrowstyle": "-|>", "color": SHADES[-1], "linewidth": 1.0},
    )
    axes.annotate(
        "",
        xy=(4.6, 0.0),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "-|>", "color": figure_style.AXIS_COLOR, "linewidth": 1.3},
    )
    axes.text(4.66, -0.02, "$x$", fontsize=15, ha="left", va="top", color=figure_style.AXIS_COLOR)
    axes.annotate(
        "",
        xy=(0.0, 2.35),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "-|>", "color": figure_style.AXIS_COLOR, "linewidth": 1.3},
    )
    axes.text(-0.10, 2.40, "$z$", fontsize=15, ha="right", va="bottom", color=figure_style.AXIS_COLOR)
    axes.set_xlim(-0.35, 4.95)
    axes.set_ylim(-0.45, 2.55)
    axes.set_aspect("equal")
    axes.set_axis_off()


def main():
    """Draw figure 1 of part 2 and write it to the figure directory."""
    apply_style()
    figure, axes = figure_style.plt.subplots(figsize=(7.6, 4.9))
    draw_cut_frame(axes)
    axes.set_title("The horizontal cut of the solid at five heights", fontsize=13)
    save_figure(figure, "part2_figure1")


if __name__ == "__main__":
    main()
