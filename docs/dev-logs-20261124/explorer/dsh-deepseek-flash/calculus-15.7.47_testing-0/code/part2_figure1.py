"""Figure 1 of Part 2: the two families of sections and the projection on the plane y = 0.

The script writes code/figures/part2_figure1.png and asserts that every label lies
inside its axes box before the export. Run it with the environment interpreter:
code/.venv/Scripts/python.exe code/part2_figure1.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part2_figure1.png"


def assert_inside(axes, artist, name: str) -> None:
    """Raise when one artist lies outside the axes box of its panel.

    Args:
        axes: The axes that holds the artist.
        artist: The text artist to measure.
        name: The label of the artist, for the error message.
    """
    figure = axes.figure
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    box = artist.get_window_extent(renderer=renderer)
    axes_box = axes.get_window_extent(renderer=renderer)
    if (
        box.x0 < axes_box.x0 - 0.5
        or box.x1 > axes_box.x1 + 0.5
        or box.y0 < axes_box.y0 - 0.5
        or box.y1 > axes_box.y1 + 0.5
    ):
        raise AssertionError(f"label {name} lies outside its axes box")


def main() -> None:
    """Draw the three panels and write the figure file."""
    figure, panels = plt.subplots(1, 3, figsize=(12.6, 4.2))
    labels: list[tuple[object, object, str]] = []

    left = panels[0]
    axis_x = np.linspace(-1.0, 1.0, 401)
    left.fill_between(axis_x, axis_x**2, 1.0, color="#dfe7f0")
    for z in figure_anchors.Z_SLICES:
        left.plot(axis_x, np.maximum(axis_x**2, 0.0), color="#8fa6bf", linewidth=0.6, linestyle=":")
        left.fill_between(axis_x, axis_x**2, 1.0 - z, color="#8fa6bf", alpha=0.35)
        left.plot([-1.0, 1.0], [1.0 - z, 1.0 - z], color="#1f3b57", linewidth=1.2)
    left.plot(axis_x, axis_x**2, color="#1f3b57", linewidth=1.6)
    left.set_xlim(-1.15, 1.15)
    left.set_ylim(-0.02, 1.12)
    left.set_xlabel(r"$x$")
    left.set_ylabel(r"$y$")
    left.set_title("level sets of the section at fixed $z$, drawn in the $xy$-plane", fontsize=10)
    labels.append((left, left.text(0.58, 0.93, "upper rim", fontsize=10), "left top"))
    labels.append((left, left.text(-0.95, 0.10, r"$y = x^{2}$", fontsize=10), "left floor"))

    middle = panels[1]
    middle.fill_between(axis_x, 0.0, 1.0 - axis_x**2, color="#dfe7f0")
    middle.plot(axis_x, 1.0 - axis_x**2, color="#1f3b57", linewidth=1.6)
    for y in figure_anchors.Y_SLICES:
        half_width = np.sqrt(y)
        middle.add_patch(
            plt.Rectangle(
                (-half_width, 0.0),
                2.0 * half_width,
                1.0 - y,
                facecolor="#8fa6bf",
                edgecolor="#1f3b57",
                alpha=0.45,
                linewidth=1.0,
            )
        )
    middle.set_xlim(-1.15, 1.15)
    middle.set_ylim(-0.02, 1.12)
    middle.set_xlabel(r"$x$")
    middle.set_ylabel(r"$z$")
    middle.set_title("sections at fixed $y$: rectangles in planes parallel to the $xz$-plane", fontsize=10)
    labels.append((middle, middle.text(0.26, 0.60, r"$z = 1 - x^{2}$", fontsize=10), "middle curve"))
    labels.append((middle, middle.text(-0.95, 0.06, r"$y = 0.25$", fontsize=10), "middle floor"))

    right = panels[2]
    axis_y = np.linspace(0.0, 1.0, 201)
    right.fill_between(axis_y, 0.0, 1.0 - axis_y, color="#dfe7f0")
    right.plot(axis_y, 1.0 - axis_y, color="#1f3b57", linewidth=1.6)
    right.plot([0.0, 1.0], [0.0, 0.0], color="#1f3b57", linewidth=1.6)
    right.plot([0.0, 0.0], [0.0, 1.0], color="#1f3b57", linewidth=1.6)
    right.set_xlim(-0.08, 1.12)
    right.set_ylim(-0.08, 1.12)
    right.set_xlabel(r"$y$")
    right.set_ylabel(r"$z$")
    right.set_title("projection on the plane $x = 0$: a triangle", fontsize=10)
    labels.append((right, right.text(0.42, 0.72, r"$y + z = 1$", fontsize=10), "right slope"))
    labels.append((right, right.text(0.72, 0.06, r"$y = 1$", fontsize=10), "right floor"))

    figure.tight_layout()
    for axes, artist, name in labels:
        assert_inside(axes, artist, name)

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=170)
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
