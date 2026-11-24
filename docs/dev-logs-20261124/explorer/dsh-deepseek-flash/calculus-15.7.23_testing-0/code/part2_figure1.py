"""Figure 1 of Part 2: the quarter disk in the plane x = 0 and one slice of it.

The left panel shows the region of the pair (y, z) that the inequalities allow at x = 0.  The
right panel shows the slice at the height z = 0.50 in the plane of the pair (x, y).  Each label
is checked against the axes box before the file is written.
"""

from __future__ import annotations

import math

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import mcma_support as support  # noqa: E402

HEIGHT = 0.5
"""Height of the drawn slice."""


def assert_inside(axes, text) -> None:
    """Raise an error when a text object leaves its axes box."""
    renderer = axes.figure.canvas.get_renderer()
    box = text.get_window_extent(renderer=renderer)
    frame = axes.get_window_extent(renderer=renderer)
    if box.x0 < frame.x0 or box.x1 > frame.x1 or box.y0 < frame.y0 or box.y1 > frame.y1:
        raise AssertionError(f"text leaves its axes box: {text.get_text()}")


def main() -> None:
    """Draw the two panels and write the figure."""
    figure, (left, right) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=150)

    radius = np.linspace(0.0, 1.0, 400)
    left.fill_between(radius, 0.0, np.sqrt(np.maximum(0.0, 1.0 - radius ** 2)),
                      color="#cfe0ee", alpha=0.9, linewidth=0)
    left.plot(radius, np.sqrt(np.maximum(0.0, 1.0 - radius ** 2)), color="#2f5d82", linewidth=2,
              label="arc $y^{2}+z^{2}=1$")
    width = support.slice_length_at_height(HEIGHT)
    left.fill_between([0.0, width], HEIGHT - 0.03, HEIGHT + 0.03, color="#e8b04b", alpha=0.95,
                      linewidth=0, label=f"slice at $z={HEIGHT:.2f}$")
    left.set_xlabel("$y$")
    left.set_ylabel("$z$")
    left.set_xlim(0.0, 1.05)
    left.set_ylim(0.0, 1.10)
    left.set_title(f"Plane $x=0$: quarter disk, slice length ${width:.4f}$", fontsize=9)
    left.legend(fontsize=8, loc="upper right", frameon=False)
    left.set_aspect("equal")

    height = support.slice_length_at_height(HEIGHT)
    area = support.slice_area_exact(HEIGHT)
    right.fill([0.0, height, height], [0.0, 0.0, height], color="#cfe0ee", alpha=0.9,
               linewidth=0)
    right.plot([0.0, height], [0.0, height], color="#8a5a10", linewidth=2,
               label="wall $y=x$")
    right.plot([height, height], [0.0, height], color="#4a6b3c", linewidth=2,
               label=f"side $y={height:.4f}$")
    right.set_xlabel("$x$")
    right.set_ylabel("$y$")
    right.set_xlim(-0.03, 0.98)
    right.set_ylim(-0.03, 0.98)
    right.set_title(f"Slice at $z={HEIGHT:.2f}$: area ${area:.4f}$", fontsize=9)
    right.legend(fontsize=8, loc="upper left", frameon=False)
    right.set_aspect("equal")

    figure.canvas.draw()
    for axes in (left, right):
        for text in axes.texts:
            assert_inside(axes, text)
        legend = axes.get_legend()
        if legend is not None:
            renderer = figure.canvas.get_renderer()
            box = legend.get_window_extent(renderer=renderer)
            frame = axes.get_window_extent(renderer=renderer)
            if box.x0 < frame.x0 or box.x1 > frame.x1 or box.y0 < frame.y0 or box.y1 > frame.y1:
                raise AssertionError("legend leaves its axes box")
    area_slice = support.slice_area_exact(HEIGHT)
    print(f"drawn slice: z = {HEIGHT:.2f}, side {height:.9f}, area {area_slice:.9f}, "
          f"triangle half of {height ** 2:.9f}")

    support.FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(support.FIGURE_DIRECTORY / "part2_figure1.png", bbox_inches="tight")
    print("wrote part2_figure1.png")


if __name__ == "__main__":
    main()
