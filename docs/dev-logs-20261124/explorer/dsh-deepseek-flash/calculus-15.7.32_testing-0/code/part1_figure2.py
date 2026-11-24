"""Figure 1 of Part 1: the three projections of E on the three coordinate planes.

Each panel draws one projection as a filled triangle, names the two axes that the panel
keeps, and names the two edges that bound the fill.

Constants:
    PROJECTIONS: The three projections, each with its kept axes, its corners, and its name.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import figure_common
import solid

PROJECTIONS = [
    ([2.0, 0.0, 2.0], [0.0, 2.0, 2.0], "$x$", "$y$", "on the plane $z = 0$", "$D_{xy}$"),
    ([0.0, 2.0, 2.0], [0.0, 0.0, 1.0], "$x$", "$z$", "on the plane $y = 0$", "$D_{xz}$"),
    ([0.0, 2.0, 2.0], [0.0, 0.0, 1.0], "$y$", "$z$", "on the plane $x = 0$", "$D_{yz}$"),
]


def main():
    """Draw the three projections, check each label, and write the PNG file."""
    figure, panels = plt.subplots(1, 3, figsize=(11.0, 3.9))
    for panel, (first, second, horizontal, vertical, plane_text, name) in zip(panels, PROJECTIONS):
        corners = np.column_stack([first, second])
        panel.fill(corners[:, 0], corners[:, 1], color="#9dc3e6", alpha=figure_common.SURFACE_ALPHA)
        panel.plot(
            [corners[0, 0], corners[1, 0], corners[2, 0], corners[0, 0]],
            [corners[0, 1], corners[1, 1], corners[2, 1], corners[0, 1]],
            color="black",
            linewidth=1.2,
        )
        panel.scatter(corners[:, 0], corners[:, 1], color="black", s=16, zorder=5)
        panel.set_xlim(-0.35, 2.75)
        panel.set_ylim(-0.35, 2.35)
        panel.set_aspect("equal")
        panel.set_xlabel(horizontal, fontsize=12)
        panel.set_ylabel(vertical, fontsize=12)
        panel.set_xticks([0.0, 1.0, 2.0])
        panel.set_yticks([0.0, 1.0, 2.0] if max(second) > 1.01 else [0.0, 0.5, 1.0])
        panel.spines["top"].set_visible(False)
        panel.spines["right"].set_visible(False)

        area = solid.shoelace_area(list(zip(first, second)))
        middle = corners.mean(axis=0)
        labels = [
            figure_common.place_label(panel, figure, plane_text, (float(middle[0]), float(middle[1]) + 0.42), fontsize=10.5),
            figure_common.place_label(panel, figure, "%s, area $%s$" % (name, area), (0.06, 1.95), fontsize=11.0),
        ]
        for corner_index in range(3):
            point = (float(corners[corner_index, 0]), float(corners[corner_index, 1]))
            labels.append(
                figure_common.place_label(
                    panel,
                    figure,
                    "$(%g, %g)$" % point,
                    point,
                    candidates=[(8, 8), (8, -16), (-52, 8), (-52, -16), (6, 20), (-46, 20)],
                    fontsize=8.5,
                )
            )
        figure.canvas.draw()
        figure_common.assert_inside(panel, figure, labels, "labels of %s" % name)

    figure.tight_layout()
    path = figure_common.save_figure(figure, "part1_figure2.png")
    print("figure written: %s" % path)


if __name__ == "__main__":
    main()
