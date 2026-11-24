"""Draw the solid E with its four bounding surfaces and one horizontal section.

The script draws the parabolic cylinder z = 1 - y^2, the inclined plane x + z = 1, the wall x = 0 and the base
z = 0. It names each surface in one legend entry, and it marks the section at z = 0.5 in a second panel. The
script asserts the equation residual of every label anchor before it writes the file.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

import figure_anchors  # noqa: E402
import problem_model  # noqa: E402

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""The path of the figure file."""

SECTION_HEIGHT = 0.5
"""The height of the highlighted section."""

WALL_ALPHA = 0.55
"""The opacity of a bounding surface, high enough that the solid reads as a closed body."""

CYLINDER_COLOR = "#4c72b0"
INCLINED_COLOR = "#55a868"
WALL_COLOR = "#dd8452"
BASE_COLOR = "#8c8c8c"
SECTION_COLOR = "#c44e52"


def build_surfaces() -> list[tuple[np.ndarray, np.ndarray, np.ndarray, str, str]]:
    """Return the four bounding surfaces as coordinate meshes.

    Returns:
        A list of mesh triples with a colour and a legend label for each surface.
    """
    count = 48
    coordinate_x = np.linspace(0.0, 1.0, count)
    coordinate_y = np.linspace(-1.0, 1.0, count)
    coordinate_z = np.linspace(0.0, 1.0, count)

    x_grid, y_grid = np.meshgrid(coordinate_x, coordinate_y)
    cylinder = (x_grid, y_grid, 1.0 - y_grid**2)

    z_grid, fraction_y = np.meshgrid(coordinate_z, np.linspace(-1.0, 1.0, count))
    half_width = np.sqrt(np.clip(1.0 - z_grid, 0.0, None))
    inclined = (1.0 - z_grid, fraction_y * half_width, z_grid)

    y_grid_wall, z_grid_wall = np.meshgrid(coordinate_y, coordinate_z)
    wall = (np.zeros_like(y_grid_wall), y_grid_wall, z_grid_wall * (1.0 - y_grid_wall**2))

    x_grid_base, y_grid_base = np.meshgrid(coordinate_x, coordinate_y)
    base = (x_grid_base, y_grid_base, np.zeros_like(x_grid_base))

    return [
        (cylinder[0], cylinder[1], cylinder[2], CYLINDER_COLOR, r"cylinder $z = 1 - y^{2}$"),
        (inclined[0], inclined[1], inclined[2], INCLINED_COLOR, r"plane $x + z = 1$"),
        (wall[0], wall[1], wall[2], WALL_COLOR, r"wall $x = 0$"),
        (base[0], base[1], base[2], BASE_COLOR, r"base $z = 0$"),
    ]


def section_outline() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the outline of the section at the fixed height.

    Returns:
        Three coordinate arrays of the closed outline.
    """
    corners = problem_model.corners_at_z(SECTION_HEIGHT)
    points = np.array([[corner[0], corner[1], corner[2]] for corner in corners])
    closed = np.vstack((points, points[0]))
    return closed[:, 0], closed[:, 1], closed[:, 2]


def assert_labels_hold() -> None:
    """Raise an error when a label anchor does not satisfy the equation of its surface."""
    for label in figure_anchors.SURFACE_LABELS:
        point = label.anchor_point
        if "cylinder" in label.surface_name:
            residual = abs(figure_anchors.cylinder_residual(point))
        elif "x + z" in label.surface_name:
            residual = abs(figure_anchors.inclined_plane_residual(point))
        elif label.surface_name.endswith("x = 0"):
            residual = abs(point[0])
        else:
            residual = abs(point[2])
        if residual > 1.0e-12:
            raise ValueError(f"label {label.surface_name} sits off its surface by {residual:.3e}")


def main() -> None:
    """Draw the figure and write it to the figures directory."""
    assert_labels_hold()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure = plt.figure(figsize=(10.4, 6.0))
    solid_axes = figure.add_subplot(1, 2, 1, projection="3d")
    section_axes = figure.add_subplot(1, 2, 2)

    handles: list[Patch] = []
    for first, second, third, color, label in build_surfaces():
        solid_axes.plot_surface(first, second, third, color=color, alpha=WALL_ALPHA, linewidth=0.0,
                                antialiased=True, shade=True)
        handles.append(Patch(facecolor=color, alpha=WALL_ALPHA, label=label))

    section_x, section_y, section_z = section_outline()
    solid_axes.plot(section_x, section_y, section_z, color=SECTION_COLOR, linewidth=2.2)
    solid_axes.set_xlim(0.0, 1.0)
    solid_axes.set_ylim(-1.0, 1.0)
    solid_axes.set_zlim(0.0, 1.0)
    solid_axes.set_xlabel(r"$x$", fontsize=11, labelpad=4)
    solid_axes.set_ylabel(r"$y$", fontsize=11, labelpad=6)
    solid_axes.set_zlabel(r"$z$", fontsize=11, labelpad=4)
    solid_axes.set_xticks([0.0, 0.5, 1.0])
    solid_axes.set_yticks([-1.0, 0.0, 1.0])
    solid_axes.set_zticks([0.0, 0.5, 1.0])
    solid_axes.tick_params(labelsize=8, pad=1)
    solid_axes.set_box_aspect((1.1, 2.0, 1.0))
    solid_axes.view_init(elev=20.0, azim=-60.0)
    solid_axes.set_title("the solid $E$ with the red section at $z = 0.5$", fontsize=10.5, pad=0)
    solid_axes.grid(False)
    for pane in (solid_axes.xaxis.pane, solid_axes.yaxis.pane, solid_axes.zaxis.pane):
        pane.set_visible(False)
    figure.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.30, 0.055),
        ncol=2,
        fontsize=9,
        frameon=False,
        handlelength=1.6,
        columnspacing=1.4,
    )

    corners = np.array([[corner[0], corner[1]] for corner in problem_model.corners_at_z(SECTION_HEIGHT)])
    section_axes.fill(corners[:, 0], corners[:, 1], color=SECTION_COLOR, alpha=0.28)
    section_axes.plot(
        np.append(corners[:, 0], corners[0, 0]),
        np.append(corners[:, 1], corners[0, 1]),
        color=SECTION_COLOR,
        linewidth=2.2,
    )
    width = 2.0 * np.sqrt(1.0 - SECTION_HEIGHT)
    depth = 1.0 - SECTION_HEIGHT
    section_axes.annotate(
        "",
        xy=(depth, -width / 2.0),
        xytext=(0.0, -width / 2.0),
        arrowprops={"arrowstyle": "<->", "color": "#333333", "linewidth": 1.0},
    )
    section_axes.text(
        depth / 2.0,
        -width / 2.0 - 0.10,
        rf"$1 - z = {depth:.2f}$",
        ha="center",
        va="top",
        fontsize=10,
    )
    section_axes.annotate(
        "",
        xy=(depth + 0.07, width / 2.0),
        xytext=(depth + 0.07, -width / 2.0),
        arrowprops={"arrowstyle": "<->", "color": "#333333", "linewidth": 1.0},
    )
    section_axes.text(
        depth + 0.11,
        0.0,
        rf"$2\sqrt{{1 - z}} = {width:.4f}$",
        ha="left",
        va="center",
        fontsize=10,
    )
    section_axes.set_xlim(-0.08, 0.86)
    section_axes.set_ylim(-0.92, 0.86)
    section_axes.set_xlabel(r"$x$", fontsize=11)
    section_axes.set_ylabel(r"$y$", fontsize=11)
    section_axes.set_aspect("equal")
    section_axes.grid(True, color="#dde1e7", linewidth=0.6)
    section_axes.set_title(
        rf"section at $z = 0.5$: {depth:.2f} by {width:.4f}, area ${depth * width:.4f}$", fontsize=10.5, pad=8
    )

    figure.tight_layout(rect=(0.0, 0.10, 1.0, 1.0))
    figure.savefig(FIGURE_PATH, dpi=165, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"FIGURE written: {FIGURE_PATH}")
    print(f"section width {width:.6f}, depth {depth:.6f}, area {depth * width:.6f}")


if __name__ == "__main__":
    main()
