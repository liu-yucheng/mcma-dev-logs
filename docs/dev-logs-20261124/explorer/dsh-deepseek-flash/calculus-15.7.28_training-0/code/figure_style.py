"""Shared drawing setup for the figures of the tutorial.

Every figure uses the same font, the same line widths, and the same set of axis marks.  One
axis mark mechanism draws the three coordinate directions: an arrow along each axis and one
letter at its tip.  No figure sets an axis label in a second way.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  the backend must be set before pyplot is imported

FIGURE_DIRECTORY = Path(__file__).with_name("figures")
"""Directory that receives every drawn figure."""

AXIS_COLOR = "0.25"
"""Color of the coordinate arrows."""

BODY_COLOR = "#2b6cb0"
"""Fill color of the solid."""

EDGE_COLOR = "#1a365d"
"""Color of the edges of the solid."""

CUT_COLOR = "#c05621"
"""Color of a boundary curve or a cut plane."""

FIGURE_SIZE = (7.2, 5.4)
"""Size of a single panel figure in inches."""

OUTPUT_DPI = 200
"""Resolution of a saved figure in dots per inch."""


def apply_style():
    """Set the font and the line style of every figure of the tutorial."""
    plt.rcParams.update(
        {
            "font.family": "STIXGeneral",
            "mathtext.fontset": "stix",
            "font.size": 13,
            "axes.linewidth": 1.0,
            "axes.edgecolor": "0.3",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "legend.frameon": False,
        }
    )


def save_figure(figure, name):
    """Write one figure to the figure directory and report the path.

    Args:
        figure: The matplotlib figure to write.
        name: The file name without a suffix.

    Returns:
        The path of the written file.
    """
    FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DIRECTORY / f"{name}.png"
    figure.savefig(path, dpi=OUTPUT_DPI, bbox_inches="tight", pad_inches=0.08)
    plt.close(figure)
    print(f"figure written to {path}")
    return path


def draw_axis_marks(axes, lengths):
    """Draw the three coordinate directions with one arrow and one letter each.

    Args:
        axes: A three dimensional axes of matplotlib.
        lengths: The length of the arrow of the x, the y, and the z direction.
    """
    origin = np.zeros(3)
    directions = np.eye(3)
    letters = ("x", "y", "z")
    for index, letter in enumerate(letters):
        tip = origin + lengths[index] * directions[index]
        axes.quiver(
            origin[0],
            origin[1],
            origin[2],
            tip[0],
            tip[1],
            tip[2],
            color=AXIS_COLOR,
            linewidth=1.3,
            arrow_length_ratio=0.10,
        )
        axes.text(
            tip[0] * 1.06,
            tip[1] * 1.06,
            tip[2] * 1.06,
            f"${letter}$",
            color=AXIS_COLOR,
            fontsize=15,
            ha="center",
            va="center",
        )


def set_equal_view(axes, limits):
    """Set the range of the three axes to the same box and a readable point of view.

    Args:
        axes: A three dimensional axes of matplotlib.
        limits: The upper bound of the x, the y, and the z axis.
    """
    axes.set_xlim(0.0, limits[0])
    axes.set_ylim(0.0, limits[1])
    axes.set_zlim(0.0, limits[2])
    axes.set_box_aspect((limits[0], limits[1], limits[2]))
    axes.view_init(elev=22.0, azim=-58.0)
    axes.set_axis_off()
