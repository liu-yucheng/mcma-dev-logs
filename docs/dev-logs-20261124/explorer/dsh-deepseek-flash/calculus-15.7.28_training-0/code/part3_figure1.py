"""Draw figure 1 of part 3: the five patches of the boundary, one panel for each patch.

The geometry comes from `part4_verify.py`, which also checks each patch against the inequality
that defines the region.  This script only draws.  Each panel names the corners of its patch.
"""

import numpy as np

import figure_style
from figure_style import BODY_COLOR, EDGE_COLOR, CUT_COLOR, apply_style, save_figure
from part4_verify import VERTICES, build_patches

CORNERS_OF_PATCH = {
    "S1": ("A", "B", "C", "D"),
    "S2": ("A", "D", "T"),
    "S3": ("A", "B", "T"),
    "S4": ("D", "C", "T"),
    "S5": ("B", "C", "T"),
}
"""The corners that each patch carries, as checked by `part3_verify.py`."""

PANEL_LIMITS = (4.4, 2.4, 2.4)
"""The upper bound of the x, the y, and the z axis in every panel."""


def draw_patch(axes, patch):
    """Draw one patch in three dimensions, with its corners and its name.

    Args:
        axes: A three dimensional axes of matplotlib.
        patch: The patch record of `part4_verify.py`.
    """
    grid = patch.grid(24)
    axes.plot_surface(
        grid[:, :, 0],
        grid[:, :, 1],
        grid[:, :, 2],
        color=BODY_COLOR,
        alpha=0.55,
        linewidth=0.0,
        antialiased=True,
        edgecolor="none",
        shade=False,
    )
    boundary_rows = (grid[0, :, :], grid[-1, :, :], grid[:, 0, :], grid[:, -1, :])
    for row in boundary_rows:
        axes.plot(row[:, 0], row[:, 1], row[:, 2], color=EDGE_COLOR, linewidth=1.6)
    for corner in CORNERS_OF_PATCH[patch.name]:
        x, y, z = VERTICES[corner]
        axes.plot([x], [y], [z], marker="o", markersize=5.0, color=CUT_COLOR)
        axes.text(
            x + 0.14,
            y + 0.10,
            z + 0.10,
            f"${corner}$",
            fontsize=12,
            color=CUT_COLOR,
        )
    axes.set_xlim(0.0, PANEL_LIMITS[0])
    axes.set_ylim(0.0, PANEL_LIMITS[1])
    axes.set_zlim(0.0, PANEL_LIMITS[2])
    axes.set_box_aspect(PANEL_LIMITS)
    axes.view_init(elev=24.0, azim=-56.0)
    axes.set_axis_off()
    axes.set_title(f"{patch.name}: ${patch.equation}$", fontsize=12.5, pad=0.0)


def main():
    """Draw figure 1 of part 3 and write it to the figure directory."""
    apply_style()
    patches = build_patches()
    figure = figure_style.plt.figure(figsize=(12.4, 7.6))
    for index, patch in enumerate(patches):
        axes = figure.add_subplot(2, 3, index + 1, projection="3d")
        draw_patch(axes, patch)
    spare = figure.add_subplot(2, 3, 6)
    spare.set_axis_off()
    spare.text(
        0.02,
        0.92,
        "The corners:",
        fontsize=12.5,
        va="top",
        transform=spare.transAxes,
    )
    lines = [
        "$A = (0, 0, 0)$",
        "$B = (4, 0, 0)$",
        "$C = (4, 0, 2)$",
        "$D = (0, 0, 2)$",
        "$T = (0, 2, 0)$",
        "",
        "The five patches close the boundary:",
        "each corner lies on three patches,",
        "except $T$, which lies on four.",
    ]
    spare.text(
        0.02,
        0.84,
        "\n".join(lines),
        fontsize=12.0,
        va="top",
        linespacing=1.7,
        transform=spare.transAxes,
    )
    figure.suptitle("The five patches of the boundary of the solid", fontsize=13.5)
    save_figure(figure, "part3_figure1")


if __name__ == "__main__":
    main()
