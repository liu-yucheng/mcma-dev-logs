"""Draw the area of the horizontal slice as a function of the height y.

The figure shows the two cases of Part 3.
For -1 <= y <= 2 the slice is the full disk, and its area is 4 pi.
For 2 <= y <= 6 the slice is a circular segment, and its area falls to 0.
The three sample heights 0, 3, and 5 are marked.
"""

import math
from pathlib import Path
from typing import Final

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

RADIUS: Final[float] = 2.0
"""Radius of the disk."""

CUT_CONSTANT: Final[float] = 4.0
"""Right side of the top plane y + z = 4."""

HEIGHT_SAMPLE_COUNT: Final[int] = 1201
"""Number of sample heights of the curve."""

MARKED_HEIGHTS: Final[tuple[float, ...]] = (0.0, 3.0, 5.0)
"""Heights at which the figure marks the area."""

FIGURE_PATH: Final[Path] = Path(__file__).parent / "figures" / "part3_figure1.png"
"""Path of the output file of the figure."""


def slice_area(height: float) -> float:
    """Return the area of the slice at y = height from the circular segment formula."""
    cut_position = CUT_CONSTANT - height
    if cut_position >= RADIUS:
        return math.pi * RADIUS**2
    if cut_position <= -RADIUS:
        return 0.0
    distance = -cut_position
    return RADIUS**2 * math.acos(distance / RADIUS) - distance * math.sqrt(
        RADIUS**2 - distance**2
    )


def main() -> None:
    """Draw the area curve and save the figure."""
    matplotlib.rcParams["mathtext.fontset"] = "cm"
    heights = np.linspace(-1.0, 6.0, HEIGHT_SAMPLE_COUNT)
    areas = np.array([slice_area(float(height)) for height in heights])

    figure, axes = plt.subplots(figsize=(6.8, 4.8))
    axes.plot(heights, areas, color="#2F4C77", linewidth=2.0, label=r"$A(y)$")
    axes.axhline(math.pi * RADIUS**2, color="grey", linewidth=1.0, linestyle="--")
    axes.axvline(CUT_CONSTANT - RADIUS, color="grey", linewidth=1.0, linestyle=":")
    axes.fill_between(heights, areas, color="#9DB4D6", alpha=0.35)

    for height in MARKED_HEIGHTS:
        area = slice_area(height)
        axes.plot([height], [area], marker="o", color="#C44E52", markersize=7)
        axes.annotate(
            f"$({height:.0f},\\,{area:.3f})$",
            xy=(height, area),
            xytext=(height + 0.12, area + 0.9),
            fontsize=10,
            color="#8C2F33",
        )

    axes.annotate(r"$4\pi=12.566$", xy=(-0.9, math.pi * RADIUS**2), xytext=(-0.9, 13.4),
                  fontsize=10, color="#555555")
    axes.annotate(r"$y=2$", xy=(2.0, 1.0), xytext=(2.06, 0.4), fontsize=10, color="#555555")
    axes.set_xlabel(r"height $y$ of the slice")
    axes.set_ylabel(r"area $A(y)$ of the slice")
    axes.set_xlim(-1.0, 6.1)
    axes.set_ylim(-0.4, 14.2)
    axes.grid(alpha=0.25)
    axes.set_title(r"$A(y)=4\pi$ for $y\leq 2$, then a circular segment that falls to 0 at $y=6$",
                   fontsize=10)
    axes.legend(loc="lower left")

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=170)
    print(f"saved {FIGURE_PATH}")


if __name__ == "__main__":
    main()
