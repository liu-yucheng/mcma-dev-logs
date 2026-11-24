"""Draw figure 1 of part 4: the assembled solid, with the labels of its five surfaces.

Each surface label hangs from a point that its own equation satisfies.  The coordinates come
from `part4_verify.py`, which checks each point against its own surface and against the other
four surfaces.  The axes use an explicit drawing order, so a label is never hidden behind a
translucent face.
"""

import numpy as np

from figure_style import AXIS_COLOR, EDGE_COLOR, apply_style, plt, save_figure
from part4_verify import LABEL_POINTS, VERTICES, grid_back, grid_bottom, grid_floor
from part4_verify import grid_slope, grid_wall

SUBDIVISION = 44
"""Count of the subdivisions of the parametric directions of the drawing."""

FACE_STYLE = {
    "S1": ("#c2d2e2", 0.30, 2),
    "S2": ("#9db6cd", 0.55, 3),
    "S3": ("#7ba1c6", 0.55, 4),
    "S5": ("#26578c", 0.58, 5),
    "S4": ("#4478ad", 0.56, 6),
}
"""The fill color, the opacity, and the drawing order of each patch.

The patch y = 0 keeps an opacity below one half, because it is the near face of the body and it
would hide the interior.  The other four patches stay above one half, so the body reads as a
closed body.
"""

EQUATIONS = {
    "S2": "$x = 0$",
    "S3": "$z = 0$",
    "S4": "$y + z = 2$",
    "S5": "$x = 4 - y^2$",
}
"""The equation that each patch satisfies."""

LEADER_DIRECTION = {
    "S2": (0.0, 0.75, 0.65),
    "S3": (0.10, 0.95, -0.30),
    "S4": (0.0, 0.75, 0.75),
    "S5": (0.55, 0.85, 0.0),
}
"""The direction of the leader line of each label, as an unnormalized vector."""

EDGE_ZORDER = 8.0
"""Drawing order of the outline of a patch."""

LABEL_ZORDER = 10.0
"""Drawing order of a label and of its dot."""

AXIS_ZORDER = 9.0
"""Drawing order of a coordinate arrow."""


def draw_patch(axes, name, grid):
    """Draw one patch with an explicit drawing order and its outline.

    Args:
        axes: A three dimensional axes of matplotlib.
        name: The short name of the patch.
        grid: A function of the subdivision count that returns the point grid.
    """
    color, alpha, order = FACE_STYLE[name]
    points = grid(SUBDIVISION)
    axes.plot_surface(
        points[:, :, 0],
        points[:, :, 1],
        points[:, :, 2],
        color=color,
        alpha=alpha,
        linewidth=0.0,
        antialiased=True,
        edgecolor="none",
        shade=False,
        zorder=order,
    )
    for row in (points[0, :, :], points[-1, :, :], points[:, 0, :], points[:, -1, :]):
        axes.plot(
            row[:, 0],
            row[:, 1],
            row[:, 2],
            color=EDGE_COLOR,
            linewidth=1.7,
            zorder=EDGE_ZORDER,
        )


def draw_surface_label(axes, name):
    """Write the equation of one patch at a point that the equation satisfies.

    Args:
        axes: A three dimensional axes of matplotlib.
        name: The short name of the patch.
    """
    anchor = np.array(LABEL_POINTS[name])
    direction = np.array(LEADER_DIRECTION[name])
    tip = anchor + 0.62 * direction / np.linalg.norm(direction)
    axes.plot(
        [anchor[0], tip[0]],
        [anchor[1], tip[1]],
        [anchor[2], tip[2]],
        color=EDGE_COLOR,
        linewidth=1.0,
        zorder=EDGE_ZORDER,
    )
    axes.plot(
        [anchor[0]],
        [anchor[1]],
        [anchor[2]],
        marker="o",
        markersize=4.5,
        color=EDGE_COLOR,
        zorder=LABEL_ZORDER,
    )
    axes.text(
        tip[0],
        tip[1],
        tip[2],
        EQUATIONS[name],
        fontsize=11.5,
        color=EDGE_COLOR,
        ha="center",
        va="center",
        zorder=LABEL_ZORDER,
    )


def draw_corners(axes):
    """Mark the five corners with one letter each.

    Args:
        axes: A three dimensional axes of matplotlib.
    """
    offsets = {
        "A": (-0.22, -0.14, 0.02),
        "B": (-0.12, 0.22, 0.16),
        "C": (0.14, 0.14, 0.18),
        "D": (-0.20, -0.14, 0.16),
        "T": (0.08, -0.26, 0.22),
    }
    for name, point in VERTICES.items():
        axes.plot(
            [point[0]],
            [point[1]],
            [point[2]],
            marker="o",
            markersize=5.5,
            color=EDGE_COLOR,
            zorder=LABEL_ZORDER,
        )
        offset = offsets[name]
        axes.text(
            point[0] + offset[0],
            point[1] + offset[1],
            point[2] + offset[2],
            f"${name}$",
            fontsize=13.0,
            color=EDGE_COLOR,
            ha="center",
            va="center",
            zorder=LABEL_ZORDER,
        )


def draw_axis_marks(axes, lengths):
    """Draw the three coordinate directions with one arrow and one letter each.

    Args:
        axes: A three dimensional axes of matplotlib.
        lengths: The length of the arrow of the x, the y, and the z direction.
    """
    letters = ("x", "y", "z")
    for index, letter in enumerate(letters):
        tip = np.zeros(3)
        tip[index] = lengths[index]
        axes.quiver(
            0.0,
            0.0,
            0.0,
            tip[0],
            tip[1],
            tip[2],
            color=AXIS_COLOR,
            linewidth=1.3,
            arrow_length_ratio=0.10,
            zorder=AXIS_ZORDER,
        )
        label_position = tip * 1.08
        axes.text(
            label_position[0],
            label_position[1],
            label_position[2],
            f"${letter}$",
            color=AXIS_COLOR,
            fontsize=15.0,
            ha="center",
            va="center",
            zorder=LABEL_ZORDER,
        )


def main():
    """Draw figure 1 of part 4 and write it to the figure directory."""
    apply_style()
    figure = plt.figure(figsize=(9.6, 5.8))
    axes = figure.add_subplot(1, 1, 1, projection="3d")
    axes.computed_zorder = False
    grid_of = {
        "S1": grid_bottom,
        "S2": grid_back,
        "S3": grid_floor,
        "S4": grid_slope,
        "S5": grid_wall,
    }
    for name in ("S1", "S2", "S3", "S5", "S4"):
        draw_patch(axes, name, grid_of[name])
    for name in EQUATIONS:
        draw_surface_label(axes, name)
    draw_corners(axes)
    draw_axis_marks(axes, (4.85, 2.80, 2.80))
    axes.set_xlim(0.0, 5.05)
    axes.set_ylim(-0.25, 3.05)
    axes.set_zlim(-0.20, 3.05)
    axes.set_box_aspect((5.05, 3.30, 3.25))
    axes.view_init(elev=22.0, azim=50.0)
    axes.set_axis_off()
    axes.set_title("The solid that the limits describe", fontsize=13.5)
    save_figure(figure, "part4_figure1")


if __name__ == "__main__":
    main()
