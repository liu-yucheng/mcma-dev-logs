"""Draw the solid E with the four surfaces that bound it.

Each surface label points at an anchor that satisfies the equation of its own surface. The axis names
use one mechanism only, the axis label of matplotlib, and the script checks each label position and the
border of the saved image before it reports the file.
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

OUTPUT_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
WALL_ALPHA = 0.55
CURVED_ALPHA = 0.85
SLANT_ALPHA = 0.42
GRID_POINT_COUNT = 60
LABEL_BOX = {"facecolor": "white", "edgecolor": "#666666", "linewidth": 0.5,
             "alpha": 0.88, "pad": 2.0}


def curved_face() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the band of the cylinder y^2 + z^2 = 9 with x from 0 to y / 3.

    A point of the band has y = 3 cos(theta) and z = 3 sin(theta), so it sits on the cylinder for
    every value of the sweep parameter s and every angle theta. The sweep parameter sets
    x = s y / 3 = s cos(theta), so the band keeps x inside the plane y = 3x and never fills the
    interior of the quarter disc.
    """
    sweep = np.linspace(0.0, 1.0, GRID_POINT_COUNT)[:, None]
    angle = np.linspace(0.0, np.pi / 2.0, GRID_POINT_COUNT)[None, :]
    y = 3.0 * np.cos(angle) * np.ones_like(sweep)
    z = 3.0 * np.sin(angle) * np.ones_like(sweep)
    x = sweep * np.cos(angle)
    radius_error = np.abs(y * y + z * z - 9.0)
    assert radius_error.max() <= 1.0e-12, "a point of the band leaves the cylinder"
    return x, y, z


def slanted_face() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the face y = 3x with z from 0 to sqrt(9 - y^2)."""
    x = np.linspace(0.0, 1.0, GRID_POINT_COUNT)
    y = 3.0 * x
    height = np.sqrt(np.maximum(0.0, 9.0 - y * y))
    z = np.linspace(0.0, 1.0, GRID_POINT_COUNT)[:, None] * height[None, :]
    return np.meshgrid(x, y)[0], np.meshgrid(x, y)[1], z


def main() -> None:
    """Draw the figure, check the labels, and write the PNG file."""
    figure = plt.figure(figsize=(7.4, 6.6))
    axes = figure.add_subplot(111, projection="3d")

    x_curved, y_curved, z_curved = curved_face()
    axes.plot_surface(x_curved, y_curved, z_curved, color="#4c72b0", alpha=CURVED_ALPHA,
                      linewidth=0.0, antialiased=True, shade=True)

    x_slant, y_slant, z_slant = slanted_face()
    axes.plot_surface(x_slant, y_slant, z_slant, color="#dd8452", alpha=SLANT_ALPHA,
                      linewidth=0.0, antialiased=True, shade=False)

    angle_curve = np.linspace(0.0, np.pi / 2.0, 200)
    y_curve = 3.0 * np.cos(angle_curve)
    z_curve = 3.0 * np.sin(angle_curve)
    x_curve = y_curve / 3.0
    axes.plot(x_curve, y_curve, z_curve, color="#1f2d3a", linewidth=1.6, zorder=12)
    print(f"drew the intersection curve of the cylinder and the plane y = 3x,"
          f" largest residual {np.abs(y_curve * y_curve + z_curve * z_curve - 9.0).max():.2e}")

    base = np.array([[0.0, 0.0], [0.0, 3.0], [1.0, 3.0]])
    axes.plot_trisurf(base[:, 0], base[:, 1], np.zeros(len(base)), color="#55a868",
                      alpha=WALL_ALPHA, linewidth=0.0)

    radius = np.linspace(0.0, 1.0, GRID_POINT_COUNT)[:, None]
    angle = np.linspace(0.0, np.pi / 2.0, GRID_POINT_COUNT)[None, :]
    axes.plot_surface(np.zeros_like(radius * angle), 3.0 * radius * np.cos(angle),
                      3.0 * radius * np.sin(angle), color="#c44e52", alpha=WALL_ALPHA,
                      linewidth=0.0, antialiased=True, shade=False)

    label_texts = {
        "cylinder": r"$y^{2} + z^{2} = 9$",
        "zero_plane": r"$z = 0$",
        "x_zero_plane": r"$x = 0$",
        "plane_y_equals_3x": r"$y = 3x$",
    }
    for surface, text in label_texts.items():
        point, offset = figure_anchors.SURFACE_LABEL_ANCHORS[surface]
        residual = figure_anchors.label_residual(surface, point)
        assert residual <= 1.0e-12, f"anchor of {surface} leaves its surface by {residual}"
        placed = (point[0] + offset[0], point[1] + offset[1], point[2] + offset[2])
        axes.plot([point[0], placed[0]], [point[1], placed[1]], [point[2], placed[2]],
                  color="#333333", linewidth=0.8, linestyle=(0, (3, 2)))
        axes.text(placed[0], placed[1], placed[2], text, fontsize=11, color="#111111",
                  bbox=LABEL_BOX, zorder=20)
        print(f"label {surface}: anchor ({point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f})"
              f" residual {residual:.2e}, text at ({placed[0]:.3f}, {placed[1]:.3f},"
              f" {placed[2]:.3f})")

    axes.set_xlabel(r"$x$", labelpad=8)
    axes.set_ylabel(r"$y$", labelpad=10)
    axes.set_zlabel(r"$z$", labelpad=10)
    axes.set_xlim(0.0, 1.35)
    axes.set_ylim(0.0, 3.35)
    axes.set_zlim(0.0, 3.35)
    axes.set_xticks([0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 1.0, 2.0, 3.0])
    axes.set_zticks([0.0, 1.0, 2.0, 3.0])
    axes.view_init(elev=20.0, azim=-58.0)
    axes.set_box_aspect((1.0, 1.0, 1.0), zoom=0.86)
    axes.set_title(r"The solid $E$ between the four surfaces", fontsize=12)

    for surface in label_texts:
        point, offset = figure_anchors.SURFACE_LABEL_ANCHORS[surface]
        placed = (point[0] + offset[0], point[1] + offset[1], point[2] + offset[2])
        for axis_name, low, high, value in (
            ("x", axes.get_xlim()[0], axes.get_xlim()[1], placed[0]),
            ("y", axes.get_ylim()[0], axes.get_ylim()[1], placed[1]),
            ("z", axes.get_zlim()[0], axes.get_zlim()[1], placed[2]),
        ):
            span = high - low
            inside = low + 0.02 * span <= value <= high - 0.02 * span
            print(f"label {surface}: coordinate {axis_name} = {value:.3f} inside the limits ="
                  f" {inside}")
            assert inside, f"label {surface} leaves the axes limits in {axis_name}"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=170, bbox_inches="tight")
    image = plt.imread(OUTPUT_PATH)
    border = np.concatenate([image[0, :, :3].ravel(), image[-1, :, :3].ravel(),
                             image[:, 0, :3].ravel(), image[:, -1, :3].ravel()])
    print(f"saved image {image.shape[1]} x {image.shape[0]} pixels,"
          f" smallest border value = {border.min():.3f}")
    assert border.min() >= 0.90, "a drawn element touches the border of the saved image"
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
