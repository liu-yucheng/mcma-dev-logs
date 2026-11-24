"""Draw figure 2 of part 4: the three projections of the solid on the coordinate planes.

The panel of the xz-plane shows the filled projection.  The same panel shows a disk of radius 2
with a dashed line, so the reader sees that the projection is not that disk.  The areas of the
three projections come from the limits and not from the drawing.
"""

import numpy as np

from figure_style import AXIS_COLOR, BODY_COLOR, CUT_COLOR, EDGE_COLOR, apply_style, plt, save_figure

CURVE_COUNT = 400
"""Count of the points of a curve of one panel."""


def draw_axes(axes, horizontal_length, vertical_length, horizontal_letter, vertical_letter):
    """Draw two coordinate arrows with one letter at each tip.

    Args:
        axes: A two dimensional axes of matplotlib.
        horizontal_length: The length of the horizontal arrow.
        vertical_length: The length of the vertical arrow.
        horizontal_letter: The letter of the horizontal direction.
        vertical_letter: The letter of the vertical direction.
    """
    axes.annotate(
        "",
        xy=(horizontal_length, 0.0),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "-|>", "color": AXIS_COLOR, "linewidth": 1.2},
    )
    axes.text(
        horizontal_length * 1.02,
        -0.045 * vertical_length,
        f"${horizontal_letter}$",
        fontsize=14.0,
        color=AXIS_COLOR,
        ha="left",
        va="top",
    )
    axes.annotate(
        "",
        xy=(0.0, vertical_length),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "-|>", "color": AXIS_COLOR, "linewidth": 1.2},
    )
    axes.text(
        -0.045 * horizontal_length,
        vertical_length * 1.02,
        f"${vertical_letter}$",
        fontsize=14.0,
        color=AXIS_COLOR,
        ha="right",
        va="bottom",
    )


def draw_xz_panel(axes):
    """Draw the projection of the solid on the plane y = 0, and the disk for contrast."""
    axes.fill(
        [0.0, 4.0, 4.0, 0.0],
        [0.0, 0.0, 2.0, 2.0],
        color=BODY_COLOR,
        alpha=0.32,
        linewidth=0.0,
    )
    axes.plot([0.0, 4.0, 4.0, 0.0, 0.0], [0.0, 0.0, 2.0, 2.0, 0.0], color=EDGE_COLOR, linewidth=1.9)
    angle = np.linspace(0.0, 2.0 * np.pi, CURVE_COUNT)
    axes.plot(2.0 * np.cos(angle), 2.0 * np.sin(angle), color=CUT_COLOR, linewidth=1.5, linestyle="--")
    axes.text(2.55, 2.28, "the disk $x^2 + z^2 \\leq 4$", fontsize=11.0, color=CUT_COLOR, ha="center")
    axes.text(2.55, 0.42, "the projection, area $8$", fontsize=11.5, color=EDGE_COLOR, ha="center")
    draw_axes(axes, 4.6, 2.5, "x", "z")
    axes.set_xlim(-0.45, 4.95)
    axes.set_ylim(-0.35, 2.6)
    axes.set_aspect("equal")
    axes.set_axis_off()
    axes.set_title("on the plane $y = 0$", fontsize=12.5)


def draw_xy_panel(axes):
    """Draw the projection of the solid on the plane z = 0."""
    height = np.linspace(0.0, 2.0, CURVE_COUNT)
    reach = 4.0 - height * height
    axes.fill(
        np.concatenate([reach, np.zeros_like(height)]),
        np.concatenate([height, height[::-1]]),
        color=BODY_COLOR,
        alpha=0.32,
        linewidth=0.0,
    )
    axes.plot(reach, height, color=EDGE_COLOR, linewidth=1.9)
    axes.plot([0.0, 4.0], [0.0, 0.0], color=EDGE_COLOR, linewidth=1.9)
    axes.plot([0.0, 0.0], [0.0, 2.0], color=EDGE_COLOR, linewidth=1.9)
    axes.text(1.35, 0.62, "area $\\dfrac{16}{3}$", fontsize=11.5, color=EDGE_COLOR, ha="center")
    draw_axes(axes, 4.6, 2.5, "x", "y")
    axes.set_xlim(-0.45, 4.95)
    axes.set_ylim(-0.35, 2.6)
    axes.set_aspect("equal")
    axes.set_axis_off()
    axes.set_title("on the plane $z = 0$", fontsize=12.5)


def draw_yz_panel(axes):
    """Draw the projection of the solid on the plane x = 0."""
    height = np.linspace(0.0, 2.0, CURVE_COUNT)
    axes.fill(
        np.concatenate([height, height[::-1]]),
        np.concatenate([2.0 - height, np.zeros_like(height)]),
        color=BODY_COLOR,
        alpha=0.32,
        linewidth=0.0,
    )
    axes.plot(height, 2.0 - height, color=EDGE_COLOR, linewidth=1.9)
    axes.plot([0.0, 0.0, 2.0], [2.0, 0.0, 0.0], color=EDGE_COLOR, linewidth=1.9)
    axes.text(0.72, 0.62, "area $2$", fontsize=11.5, color=EDGE_COLOR, ha="center")
    draw_axes(axes, 2.6, 2.5, "y", "z")
    axes.set_xlim(-0.35, 2.95)
    axes.set_ylim(-0.35, 2.6)
    axes.set_aspect("equal")
    axes.set_axis_off()
    axes.set_title("on the plane $x = 0$", fontsize=12.5)


def main():
    """Draw figure 2 of part 4 and write it to the figure directory."""
    apply_style()
    figure, panels = plt.subplots(1, 3, figsize=(12.6, 4.2))
    draw_yz_panel(panels[0])
    draw_xz_panel(panels[1])
    draw_xy_panel(panels[2])
    figure.suptitle("The three projections of the solid", fontsize=13.5)
    save_figure(figure, "part4_figure2")


if __name__ == "__main__":
    main()
