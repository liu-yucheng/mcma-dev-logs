"""Draw Figure 2 of Part 1: the horizontal section of $P$ at the fixed height $z = 0.4$.

The section is taken from the inequality $x^2 + 2y^2 \leq 1 - 3z^2$, so its two semi-axes are
$\\sqrt{1 - 3z^2}$ and $\\sqrt{(1 - 3z^2)/2}$. The script measures each label and each reference
line against the rendered curve before the export.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import figure_anchors as anchors
import support

FIGURE_PATH = CODE_DIRECTORY / "figures" / "part1_figure2.png"
FILL_COLOUR = "#e08a3c"
EDGE_COLOUR = "#a33d1f"
CLEARANCE = 6.0
SAMPLE_COUNT = 720


def main() -> None:
    """Draw the section, check each label, and write the PNG."""
    height = anchors.SECTION_HEIGHT
    semi_x, semi_y = anchors.section_semi_axes()
    angles = np.linspace(0.0, 2.0 * math.pi, SAMPLE_COUNT)
    boundary_x = semi_x * np.cos(angles)
    boundary_y = semi_y * np.sin(angles)

    figure, axes = plt.subplots(figsize=(6.0, 4.4))
    axes.fill(boundary_x, boundary_y, color=FILL_COLOUR, alpha=0.55, linewidth=0.0)
    axes.plot(boundary_x, boundary_y, color=EDGE_COLOUR, linewidth=1.9)

    reach = 1.05 * semi_x
    arrow = {"arrowstyle": "-|>", "color": "#8a8a8a", "linewidth": 1.0,
             "shrinkA": 0.0, "shrinkB": 0.0, "mutation_scale": 10.0}
    axes.annotate("", xy=(reach, 0.0), xytext=(-reach, 0.0), arrowprops=arrow)
    axes.annotate("", xy=(0.0, 1.05 * semi_y), xytext=(0.0, -1.05 * semi_y), arrowprops=arrow)
    axes.text(reach, 0.0, "$x$", fontsize=11, color="#4a4a4a", ha="left", va="center")
    axes.text(0.0, 1.05 * semi_y, "$y$", fontsize=11, color="#4a4a4a", ha="center", va="bottom")

    axes.plot([0.0, semi_x], [0.0, 0.0], color="#1f1f1f", linewidth=1.3, linestyle=(0, (5, 3)))
    axes.plot([0.0, 0.0], [0.0, semi_y], color="#1f1f1f", linewidth=1.3, linestyle=(0, (5, 3)))
    axes.plot(0.0, 0.0, marker="o", color="#333333", markersize=3.0)

    labels = []
    labels.append(axes.text(semi_x * 0.58, -0.075, rf"$a={semi_x:.4f}$", fontsize=10.5,
                            ha="center", va="top"))
    labels.append(axes.text(0.045, semi_y * 0.58, rf"$b={semi_y:.4f}$", fontsize=10.5,
                            ha="left", va="center"))
    labels.append(axes.text(0.0, -0.60 * semi_y,
                            r"$x^2+2y^2=1-3z^2$", fontsize=10.5, ha="center", va="center"))

    axes.set_xlim(-1.22 * semi_x, 1.42 * semi_x)
    axes.set_ylim(-1.28 * semi_y, 1.30 * semi_y)
    axes.set_aspect("equal")
    axes.set_axis_off()
    axes.set_title(rf"Section of $P$ at $z={height}$: semi-axes $a$ and $b$", fontsize=11.5,
                   pad=6.0)

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    curve = axes.transData.transform(np.column_stack([boundary_x, boundary_y]))
    box_axes = axes.get_window_extent(renderer)
    for text in labels:
        box = text.get_window_extent(renderer)
        if (box.x0 < box_axes.x0 or box.x1 > box_axes.x1
                or box.y0 < box_axes.y0 or box.y1 > box_axes.y1):
            raise AssertionError(f"label {text.get_text()!r} left the axes box")
        corners = np.array([[box.x0, box.y0], [box.x1, box.y0],
                            [box.x0, box.y1], [box.x1, box.y1]])
        distance = float(np.min(np.linalg.norm(corners[:, None, :] - curve[None, :, :], axis=2)))
        if distance < CLEARANCE:
            raise AssertionError(f"label {text.get_text()!r} touches the curve: {distance:.1f} px")

    print(f"the section at z = {height} has semi-axes {semi_x!r} and {semi_y!r}")
    print(f"the area of the section is {support.cross_section_area_formula(height)!r}")
    print(f"the ratio of the axes is {semi_x / semi_y!r}, the square root of two")
    if abs(semi_x / semi_y - math.sqrt(2.0)) > 1.0e-12:
        raise AssertionError("the axis ratio is not the square root of two")

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=200, bbox_inches="tight", pad_inches=0.04)
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
