"""Draw figure 1 of part 1: the two laws that bound the region, one in each vertical plane.

The left panel is the plane z = 0.  The right panel is the plane x = 0.  Each panel shades the
region that its own plane cuts from the solid, and each label sits on the curve that it names.
"""

import numpy as np

import figure_style
from figure_style import CUT_COLOR, EDGE_COLOR, apply_style, save_figure


def draw_plane_arrows(axes, horizontal_length, vertical_length, horizontal_letter, vertical_letter):
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
        arrowprops={"arrowstyle": "-|>", "color": figure_style.AXIS_COLOR, "linewidth": 1.3},
    )
    axes.text(
        horizontal_length * 1.03,
        -0.04 * vertical_length,
        f"${horizontal_letter}$",
        fontsize=15,
        ha="left",
        va="top",
        color=figure_style.AXIS_COLOR,
    )
    axes.annotate(
        "",
        xy=(0.0, vertical_length),
        xytext=(0.0, 0.0),
        arrowprops={"arrowstyle": "-|>", "color": figure_style.AXIS_COLOR, "linewidth": 1.3},
    )
    axes.text(
        -0.06 * horizontal_length,
        vertical_length * 1.02,
        f"${vertical_letter}$",
        fontsize=15,
        ha="right",
        va="bottom",
        color=figure_style.AXIS_COLOR,
    )


def draw_floor_panel(axes):
    """Draw the cut of the solid by the plane z = 0 in the xy-plane."""
    height = np.linspace(0.0, 2.0, 400)
    reach = 4.0 - height * height
    polygon_x = np.concatenate([reach, np.zeros_like(height)])
    polygon_y = np.concatenate([height, height[::-1]])
    axes.fill(polygon_x, polygon_y, color=figure_style.BODY_COLOR, alpha=0.28, linewidth=0.0)
    axes.plot(reach, height, color=EDGE_COLOR, linewidth=1.8)
    axes.plot([0.0, 0.0], [0.0, 2.0], color=EDGE_COLOR, linewidth=1.8)
    axes.plot([0.0, 4.0], [0.0, 0.0], color=EDGE_COLOR, linewidth=1.8)
    axes.annotate(
        "$x = 4 - y^2$",
        xy=(4.0 - 1.2**2, 1.2),
        xytext=(1.15, 1.72),
        fontsize=14,
        color=CUT_COLOR,
        arrowprops={"arrowstyle": "-", "color": CUT_COLOR, "linewidth": 1.0},
    )
    axes.plot([0.0], [2.0], marker="o", markersize=6.0, color=CUT_COLOR)
    axes.annotate(
        "$T$",
        xy=(0.0, 2.0),
        xytext=(0.16, 2.14),
        fontsize=14,
        color=CUT_COLOR,
    )
    axes.text(1.30, 0.30, "the floor $z = 0$", fontsize=12, color="0.35")
    draw_plane_arrows(axes, 4.75, 2.55, "x", "y")
    axes.set_xlim(-0.6, 5.0)
    axes.set_ylim(-0.3, 2.6)
    axes.set_aspect("equal")
    axes.set_axis_off()


def draw_back_panel(axes):
    """Draw the cut of the solid by the plane x = 0 in the yz-plane."""
    height = np.linspace(0.0, 2.0, 400)
    top = 2.0 - height
    polygon_y = np.concatenate([height, height[::-1]])
    polygon_z = np.concatenate([top, np.zeros_like(height)])
    axes.fill(polygon_y, polygon_z, color=figure_style.BODY_COLOR, alpha=0.28, linewidth=0.0)
    axes.plot(height, top, color=EDGE_COLOR, linewidth=1.8)
    axes.plot([0.0, 2.0], [0.0, 0.0], color=EDGE_COLOR, linewidth=1.8)
    axes.plot([0.0, 0.0], [0.0, 2.0], color=EDGE_COLOR, linewidth=1.8)
    axes.annotate(
        "$z = 2 - y$",
        xy=(1.2, 0.8),
        xytext=(0.42, 1.62),
        fontsize=14,
        color=CUT_COLOR,
        arrowprops={"arrowstyle": "-", "color": CUT_COLOR, "linewidth": 1.0},
    )
    axes.plot([2.0], [0.0], marker="o", markersize=6.0, color=CUT_COLOR)
    axes.annotate("$T$", xy=(2.0, 0.0), xytext=(2.10, 0.12), fontsize=14, color=CUT_COLOR)
    axes.text(0.20, 0.22, "the back $x = 0$", fontsize=12, color="0.35")
    draw_plane_arrows(axes, 2.65, 2.55, "y", "z")
    axes.set_xlim(-0.3, 2.9)
    axes.set_ylim(-0.3, 2.6)
    axes.set_aspect("equal")
    axes.set_axis_off()


def main():
    """Draw figure 1 of part 1 and write it to the figure directory."""
    apply_style()
    figure, panel = figure_style.plt.subplots(1, 2, figsize=(9.6, 4.2))
    draw_floor_panel(panel[0])
    draw_back_panel(panel[1])
    panel[0].set_title("the plane $z = 0$", fontsize=13)
    panel[1].set_title("the plane $x = 0$", fontsize=13)
    save_figure(figure, "part1_figure1")


if __name__ == "__main__":
    main()
