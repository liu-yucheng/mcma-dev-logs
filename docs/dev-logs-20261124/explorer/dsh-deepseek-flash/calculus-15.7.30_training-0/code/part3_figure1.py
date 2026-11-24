"""Draw the section at a fixed value of y.

Panel A is the plane of constant y, with x horizontal and z vertical.  The section is the
rectangle [-2, 2] x [-sqrt(9 - y^2), sqrt(9 - y^2)].  The three rectangles of the panel show how
the rectangle shrinks when |y| grows, and the rectangle collapses to the segment [-2, 2] at
|y| = 3.  Panel B is the disk in the plane x = 0: the chord at the fixed value of y is the
opening of the same rectangle, so the height of the rectangle is the length of the chord.

Run this script with the interpreter of `code/.venv`.  It writes
`code/figures/part3_figure1.png`.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt

RADIUS = 3.0
"""Radius of the circular cylinder y^2 + z^2 = 9."""

HALF_LENGTH = 2.0
"""Half of the distance between the planes x = -2 and x = 2."""

MEASURED_VALUES = (0.0, 1.5, 2.5)
"""Values of y that the two panels show."""

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part3_figure1.png"
"""Path of the figure file."""

INK = "#1f2933"
"""Color of the outline of a curve."""

ACCENT = "#1f3b57"
"""Color of a labeled item."""

FILL_COLOR = "#cfe0ee"
"""Color of a filled region."""


def arrow_axis(axis, horizontal_name: str, vertical_name: str) -> None:
    """Draw one horizontal axis and one vertical axis, each with one arrowhead and one label."""
    reach = 4.0
    axis.annotate("", xy=(reach, 0.0), xytext=(-reach, 0.0),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 0.9})
    axis.annotate("", xy=(0.0, reach), xytext=(0.0, -reach),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 0.9})
    axis.text(reach + 0.12, 0.0, horizontal_name, color=INK, fontsize=11, ha="left",
              va="center", bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.7})
    axis.text(0.0, reach + 0.12, vertical_name, color=INK, fontsize=11, ha="center",
              va="bottom")


def draw_rectangles(axis) -> None:
    """Draw the three rectangles of the section at y = 0, y = 1.5, and y = 2.5."""
    shades = ("#dbe8f3", "#c2d8ea", "#a7c6dd")
    for shade, value in zip(shades, MEASURED_VALUES):
        half = math.sqrt(RADIUS**2 - value**2)
        axis.add_patch(plt.Rectangle((-HALF_LENGTH, -half), 2.0 * HALF_LENGTH, 2.0 * half,
                                     facecolor=shade, edgecolor=INK, linewidth=1.2, zorder=2))
        axis.text(HALF_LENGTH + 0.15, half - 0.1, "$y={:g}$".format(value),
                  color=ACCENT, fontsize=9.5, ha="left", va="top", zorder=3)
    axis.text(0.0, -3.15, "$|y|=3$: the segment $-2\\leq x\\leq 2$", color=ACCENT,
              fontsize=9.5, ha="center", va="top")
    axis.set_title("section in the plane $x$-$z$ at fixed $y$:\n"
                   "$-2\\leq x\\leq 2$, $|z|\\leq\\sqrt{9-y^2}$", fontsize=10, color=INK, pad=12.0)


def draw_disk_with_chords(axis) -> None:
    """Draw the disk in the plane x = 0 and the chords that the section uses."""
    angle = np.linspace(0.0, 2.0 * math.pi, 361)
    axis.fill(RADIUS * np.cos(angle), RADIUS * np.sin(angle), color=FILL_COLOR, zorder=1)
    axis.plot(RADIUS * np.cos(angle), RADIUS * np.sin(angle), color=INK, linewidth=1.3,
              zorder=2)
    for value in MEASURED_VALUES:
        half = math.sqrt(RADIUS**2 - value**2)
        axis.plot([-half, half], [value, value], color=ACCENT, linewidth=1.6, zorder=3)
        axis.text(-half - 0.12, value, "$y={:g}$".format(value), color=ACCENT,
                  fontsize=9.5, ha="right", va="center", zorder=3)
    axis.set_title("the chord at fixed $y$ gives the height\nof the rectangle: "
                   "$|z|\\leq\\sqrt{9-y^2}$", fontsize=10, color=INK)


def main() -> None:
    """Draw the two panels and write the figure."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure, panels = plt.subplots(1, 2, figsize=(10.8, 5.0), dpi=200)

    draw_rectangles(panels[0])
    arrow_axis(panels[0], "$x$", "$z$")
    panels[0].set_xlim(-4.6, 4.6)
    panels[0].set_ylim(-4.6, 4.6)
    panels[0].set_aspect("equal")
    panels[0].axis("off")

    draw_disk_with_chords(panels[1])
    arrow_axis(panels[1], "$y$", "$z$")
    panels[1].set_xlim(-4.6, 4.9)
    panels[1].set_ylim(-4.6, 4.6)
    panels[1].set_aspect("equal")
    panels[1].axis("off")

    figure.tight_layout(pad=0.8)
    figure.savefig(FIGURE_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
