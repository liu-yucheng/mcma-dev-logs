"""Figure 1 of Part 2: the projection on the plane z = 0 with both families of strips.

The left panel draws the strips of the order dz dx dy, which fixes y and sweeps x. The right
panel draws the strips of the order dz dy dx, which fixes x and sweeps y.

Constants:
    CORNERS: The three corners of the projection, in the order (2,0), (0,2), (2,2).
    HEIGHTS: The heights of the drawn strips in the outer variable.
    STRIP_COLOR: The color of one drawn strip.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import figure_common
import solid

CORNERS = np.array([[2.0, 0.0], [0.0, 2.0], [2.0, 2.0]])
HEIGHTS = (0.4, 1.0, 1.6)
STRIP_COLOR = "#1f5fa8"


def draw_panel(panel, fixed_variable):
    """Draw one family of strips on one panel.

    Args:
        panel: The axes of the panel.
        fixed_variable: "y" when the strip fixes y and sweeps x, "x" otherwise.

    Returns:
        The list of the label artists of the panel.
    """
    panel.set_xlim(-0.35, 2.8)
    panel.set_ylim(-0.35, 2.6)
    panel.set_aspect("equal")
    panel.set_xlabel("$x$", fontsize=12)
    panel.set_ylabel("$y$", fontsize=12)
    panel.set_xticks([0.0, 1.0, 2.0])
    panel.set_yticks([0.0, 1.0, 2.0])
    panel.spines["top"].set_visible(False)
    panel.spines["right"].set_visible(False)
    panel.fill(CORNERS[:, 0], CORNERS[:, 1], color="#d6e4f0", alpha=figure_common.SURFACE_ALPHA)
    panel.plot(
        [2.0, 0.0, 2.0, 2.0],
        [0.0, 2.0, 2.0, 0.0],
        color="black",
        linewidth=1.2,
    )
    labels = []
    for height in HEIGHTS:
        if fixed_variable == "y":
            start = (2.0 - height, height)
            end = (2.0, height)
        else:
            start = (height, 2.0 - height)
            end = (height, 2.0)
        panel.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "-|>", "color": STRIP_COLOR, "linewidth": 1.4, "shrinkA": 0.0, "shrinkB": 4.0})
        if fixed_variable == "y":
            anchor = end
            offset = (9, -3)
            alignment = {"ha": "left", "va": "center"}
        else:
            anchor = end
            offset = (8, 6)
            alignment = {"ha": "left", "va": "bottom"}
        labels.append(
            figure_common.place_label(
                panel,
                plt.gcf(),
                "$%s = %g$" % (fixed_variable, height),
                anchor,
                candidates=[offset],
                fontsize=9.5,
                **alignment
            )
        )
    return labels


def main():
    """Draw both families of strips, check each label, and write the PNG file."""
    figure, panels = plt.subplots(1, 2, figsize=(9.2, 4.4))
    area = solid.shoelace_area([(2.0, 0.0), (0.0, 2.0), (2.0, 2.0)])

    left_labels = draw_panel(panels[0], "y")
    left_labels.append(
        figure_common.place_label(panels[0], figure, "$dz\\,dx\\,dy$: outer $y$", (0.05, -0.24), fontsize=11.0)
    )
    left_labels.append(figure_common.place_label(panels[0], figure, "$x + y = 2$", (0.95, 1.05), fontsize=10.0))

    right_labels = draw_panel(panels[1], "x")
    right_labels.append(
        figure_common.place_label(panels[1], figure, "$dz\\,dy\\,dx$: outer $x$", (0.05, -0.24), fontsize=11.0)
    )
    right_labels.append(figure_common.place_label(panels[1], figure, "$x + y = 2$", (0.95, 1.05), fontsize=10.0))

    figure.suptitle("Projection on the plane $z = 0$: $D_{xy}$ with area $%s$" % area, fontsize=12)

    figure.tight_layout()
    figure.canvas.draw()
    figure_common.assert_inside(panels[0], figure, left_labels, "labels of the left panel")
    figure_common.assert_inside(panels[1], figure, right_labels, "labels of the right panel")
    path = figure_common.save_figure(figure, "part2_figure1.png")
    print("figure written: %s" % path)


if __name__ == "__main__":
    main()
