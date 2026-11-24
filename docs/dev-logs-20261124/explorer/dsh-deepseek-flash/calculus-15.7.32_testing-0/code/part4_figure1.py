"""Figure 1 of Part 4: the projection that drops x, drawn in the yz-plane.

The projection lies on the plane x = 0. The left panel draws the strips of the order
dx dy dz, which fixes z and sweeps y. The right panel draws the strips of the order
dx dz dy, which fixes y and sweeps z.

Constants:
    CORNERS: The three corners of the projection on the plane x = 0.
    HEIGHTS: The drawn values of the outer variable.
    STRIP_COLOR: The color of one drawn strip.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import figure_common
import solid

CORNERS = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 1.0]])
HEIGHTS = (0.2, 0.5, 0.8)
STRIP_COLOR = "#a8561f"


def draw_panel(panel, figure, fixed_variable, order_text):
    """Draw one family of strips on one panel.

    Args:
        panel: The axes of the panel.
        figure: The figure that holds the panel.
        fixed_variable: "z" when the strip fixes z and sweeps y, "y" otherwise.
        order_text: The text that names the order of the panel.

    Returns:
        The list of the label artists of the panel.
    """
    panel.set_xlim(-0.35, 2.8)
    panel.set_ylim(-0.35, 1.65)
    panel.set_aspect("equal")
    panel.set_xlabel("$y$", fontsize=12)
    panel.set_ylabel("$z$", fontsize=12)
    panel.set_xticks([0.0, 1.0, 2.0])
    panel.set_yticks([0.0, 0.5, 1.0])
    panel.spines["top"].set_visible(False)
    panel.spines["right"].set_visible(False)

    panel.fill(CORNERS[:, 0], CORNERS[:, 1], color="#f4e0d0", alpha=figure_common.SURFACE_ALPHA)
    panel.plot([0.0, 2.0, 2.0, 0.0], [0.0, 0.0, 1.0, 0.0], color="black", linewidth=1.2)

    labels = [figure_common.place_label(panel, figure, order_text, (0.05, -0.2), candidates=[(0, 0)], fontsize=11.0)]
    for height in HEIGHTS:
        if fixed_variable == "z":
            start = (2.0 * height, height)
            end = (2.0, height)
            offset = (9, -3)
            alignment = {"ha": "left", "va": "center"}
        else:
            start = (height, 0.0)
            end = (height, height / 2.0)
            offset = (0, 7)
            alignment = {"ha": "center", "va": "bottom"}
        panel.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={"arrowstyle": "-|>", "color": STRIP_COLOR, "linewidth": 1.4, "shrinkA": 0.0, "shrinkB": 4.0},
        )
        labels.append(
            figure_common.place_label(
                panel,
                figure,
                "$%s = %g$" % (fixed_variable, height),
                end,
                candidates=[offset],
                fontsize=9.5,
                **alignment,
            )
        )
    return labels


def main():
    """Draw both families of strips, check each label, and write the PNG file."""
    figure, panels = plt.subplots(1, 2, figsize=(9.2, 3.6))
    area = solid.shoelace_area([(0.0, 0.0), (2.0, 0.0), (2.0, 1.0)])

    left_labels = draw_panel(panels[0], figure, "z", "$dx\\,dy\\,dz$: outer $z$")
    left_labels.append(
        figure_common.place_label(panels[0], figure, "$y = 2z$", (1.1, 0.55), candidates=[(-44, 6)], fontsize=10.0)
    )

    right_labels = draw_panel(panels[1], figure, "y", "$dx\\,dz\\,dy$: outer $y$")
    right_labels.append(
        figure_common.place_label(panels[1], figure, "$z = y/2$", (1.45, 0.725), candidates=[(0, -16)], fontsize=10.0)
    )

    figure.suptitle("Projection on the plane $x = 0$: $D_{yz}$ with area $%s$" % area, fontsize=12)
    figure.tight_layout()
    figure.canvas.draw()
    figure_common.assert_inside(panels[0], figure, left_labels, "labels of the left panel")
    figure_common.assert_inside(panels[1], figure, right_labels, "labels of the right panel")
    path = figure_common.save_figure(figure, "part4_figure1.png")
    print("figure written: %s" % path)


if __name__ == "__main__":
    main()
