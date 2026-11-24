"""Draw the two choices of the inner integral on the disk y^2 + z^2 <= 9.

Panel A cuts the disk into strips of constant y.  Each strip runs in z, so the inner integral
runs over z and the outer integral runs over y.  Panel B cuts the disk into strips of constant z,
so the roles of y and z exchange.  Both panels use the same disk, because the two choices describe
the same solid.

Run this script with the interpreter of `code/.venv`.  It writes
`code/figures/part2_figure1.png`.
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

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part2_figure1.png"
"""Path of the figure file."""

INK = "#1f2933"
"""Color of the outline of a curve."""

ACCENT = "#1f3b57"
"""Color of a labeled strip."""

FILL_COLOR = "#cfe0ee"
"""Color of the filled disk."""


def arrow_axis(axis, horizontal_name: str, vertical_name: str) -> None:
    """Draw one horizontal axis and one vertical axis, each with one arrowhead and one label."""
    reach = 4.3
    axis.annotate("", xy=(reach, 0.0), xytext=(-reach, 0.0),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 0.9})
    axis.annotate("", xy=(0.0, reach), xytext=(0.0, -reach),
                  arrowprops={"arrowstyle": "-|>", "color": INK, "linewidth": 0.9})
    axis.text(reach + 0.12, 0.0, horizontal_name, color=INK, fontsize=11, ha="left",
              va="center", bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.7})
    axis.text(0.0, reach + 0.12, vertical_name, color=INK, fontsize=11, ha="center",
              va="bottom")


def draw_disk(axis) -> None:
    """Fill the disk y^2 + z^2 <= 9 and draw its boundary."""
    angle = np.linspace(0.0, 2.0 * math.pi, 361)
    axis.fill(RADIUS * np.cos(angle), RADIUS * np.sin(angle), color=FILL_COLOR, zorder=1)
    axis.plot(RADIUS * np.cos(angle), RADIUS * np.sin(angle), color=INK, linewidth=1.3,
              zorder=2)


def draw_constant_y_strips(axis) -> None:
    """Draw chords of constant y, which become the inner integral in z."""
    for value in (-2.4, -1.2, 0.0, 1.2, 2.4):
        half = math.sqrt(RADIUS**2 - value**2)
        axis.annotate("", xy=(value, half), xytext=(value, -half),
                      arrowprops={"arrowstyle": "<|-|>", "color": ACCENT, "linewidth": 1.2})
    axis.text(-2.4, math.sqrt(RADIUS**2 - 2.4**2) + 0.18, "$y$ fixed, $z$ runs",
              color=ACCENT, fontsize=10, ha="left", va="bottom")
    axis.set_title("strips of constant $y$:\n$z$ from $-\\sqrt{9-y^2}$ to $\\sqrt{9-y^2}$",
                   fontsize=10, color=INK)


def draw_constant_z_strips(axis) -> None:
    """Draw chords of constant z, which become the inner integral in y."""
    for value in (-2.4, -1.2, 0.0, 1.2, 2.4):
        half = math.sqrt(RADIUS**2 - value**2)
        axis.annotate("", xy=(half, value), xytext=(-half, value),
                      arrowprops={"arrowstyle": "<|-|>", "color": ACCENT, "linewidth": 1.2})
    axis.text(-2.7, 2.35, "$z$ fixed, $y$ runs", color=ACCENT, fontsize=10, ha="left",
              va="bottom")
    axis.set_title("strips of constant $z$:\n$y$ from $-\\sqrt{9-z^2}$ to $\\sqrt{9-z^2}$",
                   fontsize=10, color=INK)


def main() -> None:
    """Draw the two panels and write the figure."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure, panels = plt.subplots(1, 2, figsize=(10.4, 5.0), dpi=200)

    for axis, drawer, pair in ((panels[0], draw_constant_y_strips, ("y", "z")),
                               (panels[1], draw_constant_z_strips, ("z", "y"))):
        draw_disk(axis)
        drawer(axis)
        arrow_axis(axis, pair[0], pair[1])
        axis.set_xlim(-4.6, 4.6)
        axis.set_ylim(-4.6, 4.6)
        axis.set_aspect("equal")
        axis.axis("off")

    figure.tight_layout(pad=0.8)
    figure.savefig(FIGURE_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
