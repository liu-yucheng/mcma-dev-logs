"""Draw how the inner integral of two orders reads the section at a fixed value of z.

The section of E at a fixed value of z keeps the coordinates x and y, and its boundaries follow from
``x**2 <= y <= 4 - 2 * z``.  The left panel draws the inner integral of the order dy dx dz: at a fixed
value of x, y runs from x**2 to 4 - 2 * z, so the inner piece is a vertical segment.  The right panel
draws the inner integral of the order dx dy dz: at a fixed value of y, x runs from -sqrt(y) to sqrt(y),
so the inner piece is a horizontal segment.

Run this script with the interpreter of ``code/.venv``.  It writes ``code/figures/part5_figure4.png``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"
"""Directory of the figure files."""

OUTPUT_PATH = FIGURE_DIRECTORY / "part5_figure4.png"
"""Path of the figure of this part."""

EDGE_COLOR = "#1f2933"
"""Color of the boundary of the section."""

FILL_COLOR = "#9dc0a8"
"""Color of the section."""

STRIP_COLOR = "#b5446e"
"""Color of the drawn inner piece."""

FIXED_Z = 0.5
"""The fixed value of z that both panels use."""

UPPER_Y = 4.0 - 2.0 * FIXED_Z
"""The largest value of y in the section."""


def draw_inner_y(axes: plt.Axes) -> None:
    """Draw the inner piece of the order dy dx dz, which is a vertical segment.

    Args:
        axes: The axes of the left panel.
    """
    x_values = np.linspace(-np.sqrt(UPPER_Y), np.sqrt(UPPER_Y), 400)
    axes.fill_between(x_values, x_values ** 2, UPPER_Y, color=FILL_COLOR, alpha=0.45,
                      linewidth=0.0)
    axes.plot(x_values, x_values ** 2, color=EDGE_COLOR, linewidth=1.5)
    axes.plot([-np.sqrt(UPPER_Y), np.sqrt(UPPER_Y)], [UPPER_Y, UPPER_Y], color=EDGE_COLOR,
              linewidth=1.5)

    for x_value in (-1.0, 0.0, 1.0):
        axes.annotate("", xy=(x_value, UPPER_Y), xytext=(x_value, x_value ** 2),
                      arrowprops={"arrowstyle": "-|>", "color": STRIP_COLOR, "linewidth": 1.4,
                                  "shrinkA": 0.0, "shrinkB": 5.0})
        axes.text(x_value - 0.11, (x_value ** 2 + UPPER_Y) / 2.0, f"$y: {x_value ** 2:.1f} \\to {UPPER_Y:.1f}$",
                  fontsize=7.6, color=STRIP_COLOR, rotation=90.0, va="center", ha="right")

    axes.set_xlim(-2.05, 2.05)
    axes.set_ylim(-0.30, 3.45)
    axes.set_xticks([-2, -1, 0, 1, 2])
    axes.set_yticks([0, 1, 2, 3])
    axes.set_xlabel("x", fontsize=10)
    axes.set_ylabel("y", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Inner integral in $y$: fix $x$, then $x^2 \\leq y \\leq 4 - 2z$", fontsize=9.0,
                   pad=6)


def draw_inner_x(axes: plt.Axes) -> None:
    """Draw the inner piece of the order dx dy dz, which is a horizontal segment.

    Args:
        axes: The axes of the right panel.
    """
    x_values = np.linspace(-np.sqrt(UPPER_Y), np.sqrt(UPPER_Y), 400)
    axes.fill_between(x_values, x_values ** 2, UPPER_Y, color=FILL_COLOR, alpha=0.45,
                      linewidth=0.0)
    axes.plot(x_values, x_values ** 2, color=EDGE_COLOR, linewidth=1.5)
    axes.plot([-np.sqrt(UPPER_Y), np.sqrt(UPPER_Y)], [UPPER_Y, UPPER_Y], color=EDGE_COLOR,
              linewidth=1.5)

    for y_value in (0.5, 1.5, 2.5):
        half_width = np.sqrt(y_value)
        axes.annotate("", xy=(half_width, y_value), xytext=(-half_width, y_value),
                      arrowprops={"arrowstyle": "-|>", "color": STRIP_COLOR, "linewidth": 1.4,
                                  "shrinkA": 0.0, "shrinkB": 5.0})
        axes.text(0.0, y_value + 0.10,
                  f"$x: -{half_width:.2f} \\to {half_width:.2f}$", fontsize=7.6,
                  color=STRIP_COLOR, ha="center")

    axes.set_xlim(-2.05, 2.05)
    axes.set_ylim(-0.30, 3.45)
    axes.set_xticks([-2, -1, 0, 1, 2])
    axes.set_yticks([0, 1, 2, 3])
    axes.set_xlabel("x", fontsize=10)
    axes.set_ylabel("y", fontsize=10)
    axes.tick_params(labelsize=8)
    axes.set_title("Inner integral in $x$: fix $y$, then $-\\sqrt{y} \\leq x \\leq \\sqrt{y}$",
                   fontsize=9.0, pad=6)


def main() -> None:
    """Draw the two panels and write the figure."""
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    figure, panel_pair = plt.subplots(1, 2, figsize=(10.4, 4.3), dpi=170)
    draw_inner_y(panel_pair[0])
    draw_inner_x(panel_pair[1])
    figure.tight_layout(pad=1.6)
    figure.savefig(OUTPUT_PATH, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"wrote {OUTPUT_PATH}")
    print(f"section at z = {FIXED_Z} keeps |x| <= {np.sqrt(UPPER_Y):.6f} and x^2 <= y <= {UPPER_Y}")
    for y_value in (0.5, 1.5, 2.5):
        print(f"  inner x range at y = {y_value}: [{-np.sqrt(y_value):.6f}, {np.sqrt(y_value):.6f}]")


if __name__ == "__main__":
    main()
