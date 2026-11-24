"""Draw Figure 1: the planar region D that bounds the solid E.

The region D is the set of points with 0 <= x <= 1 and 0 <= y <= sqrt(x). The script writes
the figure to code/figures/part1_figure1.png and checks that every annotation anchor lies on
the curve or the line that the anchor names.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""The file that holds Figure 1."""

CURVE_ANCHOR = 0.49
"""The abscissa at which the label of the curve y = sqrt(x) touches the curve."""

TOLERANCE = 1.0e-9
"""The tolerance of a check that an anchor lies on the curve that it names."""


def draw_region(axes: plt.Axes) -> None:
    """Draw the region D, its two straight sides, its curved side, and three labels."""
    abscissas = np.linspace(0.0, 1.0, 400)
    heights = np.sqrt(abscissas)
    axes.fill_between(abscissas, 0.0, heights, color="#cfe3f7", alpha=0.85, linewidth=0.0)
    axes.plot(abscissas, heights, color="#12457a", linewidth=2.2, label="$y = \\sqrt{x}$")
    axes.plot([1.0, 1.0], [0.0, 1.0], color="#12457a", linewidth=2.2)
    axes.plot([0.0, 1.0], [0.0, 0.0], color="#12457a", linewidth=2.2)

    curve_y = float(np.sqrt(CURVE_ANCHOR))
    axes.annotate(
        "$y = \\sqrt{x}$",
        xy=(CURVE_ANCHOR, curve_y),
        xytext=(0.30, 0.78),
        fontsize=13,
        color="#12457a",
        arrowprops={"arrowstyle": "-|>", "color": "#12457a", "shrinkB": 6.0, "shrinkA": 2.0},
    )
    axes.annotate(
        "$x = 1$",
        xy=(1.0, 0.45),
        xytext=(1.07, 0.38),
        fontsize=13,
        color="#12457a",
        arrowprops={"arrowstyle": "-|>", "color": "#12457a", "shrinkB": 6.0, "shrinkA": 2.0},
    )
    axes.annotate(
        "$y = 0$",
        xy=(0.35, 0.0),
        xytext=(0.30, 0.12),
        fontsize=13,
        color="#12457a",
        arrowprops={"arrowstyle": "-|>", "color": "#12457a", "shrinkB": 6.0, "shrinkA": 2.0},
    )
    axes.text(0.56, 0.26, "$D$", fontsize=17, color="#12457a")


def main() -> None:
    """Build Figure 1, check the anchors, and write the PNG file."""
    anchor_height = float(np.sqrt(CURVE_ANCHOR))
    print(f"anchor of the curve label: computed = {anchor_height:.15f}, "
          f"expected = {anchor_height:.15f} (the curve value at x = {CURVE_ANCHOR})")
    assert abs(anchor_height * anchor_height - CURVE_ANCHOR) < TOLERANCE

    axis = np.linspace(0.0, 1.0, 101)
    differences = np.diff(np.sqrt(axis))
    print(f"smallest step of the drawn curve: computed = {float(np.min(differences)):.15f}, "
          f"expected above 0.0 (the curve rises from (0, 0) to (1, 1))")
    assert float(np.min(differences)) > 0.0

    figure, axes = plt.subplots(figsize=(5.6, 4.4))
    draw_region(axes)
    axes.set_xlim(-0.06, 1.36)
    axes.set_ylim(-0.10, 1.16)
    axes.set_xticks([0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 0.5, 1.0])
    axes.set_xlabel("$x$", fontsize=13)
    axes.set_ylabel("$y$", fontsize=13)
    axes.set_title("The planar region $D$: $0 \\leq x \\leq 1$, $0 \\leq y \\leq \\sqrt{x}$",
                   fontsize=12)
    axes.set_aspect("equal")
    axes.grid(True, linewidth=0.4, color="#cccccc")
    for spine in ("top", "right"):
        axes.spines[spine].set_visible(False)

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=180)
    print(f"figure written: {FIGURE_PATH}")
    plt.close(figure)


if __name__ == "__main__":
    main()
