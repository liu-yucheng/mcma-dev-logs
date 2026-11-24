"""Draw Figure 1 of Part 1: the solid ellipsoid $P$ with one horizontal section.

The label of the boundary stands at a point that satisfies the equation of the surface. The
script measures every label against the rendered body and the axes box before the export.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from matplotlib.transforms import Bbox
from mpl_toolkits.mplot3d import proj3d

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import figure_anchors as anchors
import support

FIGURE_PATH = CODE_DIRECTORY / "figures" / "part1_figure1.png"
SURFACE_ALPHA = 0.62
SECTION_ALPHA = 0.9
SURFACE_COLOUR = "#8fb4d9"
SECTION_COLOUR = "#e08a3c"
AXIS_LENGTH = 1.26
LABEL_CLEARANCE_PIXELS = 8.0
GRID_SIZE = 61
FONT_SIZE = 10.5


def ellipsoid_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the coordinates of the surface $x^2 + 2y^2 + 3z^2 = 1$ on a parameter grid."""
    polar, azimuth = np.meshgrid(np.linspace(0.0, math.pi, GRID_SIZE),
                                 np.linspace(0.0, 2.0 * math.pi, GRID_SIZE))
    first, second, third = support.ellipsoid_semi_axes()
    return (first * np.sin(polar) * np.cos(azimuth),
            second * np.sin(polar) * np.sin(azimuth),
            third * np.cos(polar))


def project(axes: plt.Axes, points: np.ndarray) -> np.ndarray:
    """Return the display coordinates of an array of three-dimensional points."""
    matrix = axes.get_proj()
    flat_x, flat_y, _ = proj3d.proj_transform(points[:, 0], points[:, 1], points[:, 2], matrix)
    return axes.transData.transform(np.column_stack([flat_x, flat_y]))


def display_box(text: str, point: np.ndarray, renderer, axes: plt.Axes,
                horizontal: str, vertical: str) -> Bbox:
    """Return the display box of one label that stands at one three-dimensional point."""
    anchor = project(axes, np.array([point]))[0]
    width, height, _ = renderer.get_text_width_height_descent(
        text, plt.matplotlib.font_manager.FontProperties(size=FONT_SIZE), ismath=True)
    left = anchor[0] - (width if horizontal == "right" else 0.5 * width if horizontal == "center"
                        else 0.0)
    bottom = anchor[1] - (height if vertical == "top" else 0.5 * height
                          if vertical == "center" else 0.0)
    return Bbox.from_bounds(left, bottom, width, height)


def trim_white_margin(path: Path, margin: int = 12) -> None:
    """Crop the uniform white border of a rendered figure and keep a small margin.

    Args:
        path: The path of the PNG file.
        margin: The number of pixels to keep around the content.
    """
    image = Image.open(path).convert("RGB")
    grey = image.convert("L")
    box = grey.point(lambda value: 0 if value >= 250 else 255).getbbox()
    if box is None:
        raise AssertionError("the figure is empty")
    left = max(box[0] - margin, 0)
    upper = max(box[1] - margin, 0)
    right = min(box[2] + margin, image.width)
    lower = min(box[3] + margin, image.height)
    image.crop((left, upper, right, lower)).save(path)
    print(f"the trimmed figure box is {right - left} by {lower - upper} pixels")


def main() -> None:
    """Draw the figure, check every label, and write the PNG."""
    first, second, third = support.ellipsoid_semi_axes()
    surface_x, surface_y, surface_z = ellipsoid_grid()
    height = anchors.SECTION_HEIGHT
    semi_x, semi_y = anchors.section_semi_axes()

    figure = plt.figure(figsize=(4.4, 4.2))
    axes = figure.add_subplot(111, projection="3d")
    axes.plot_surface(surface_x, surface_y, surface_z, color=SURFACE_COLOUR,
                      alpha=SURFACE_ALPHA, linewidth=0.0, antialiased=True)
    angles = np.linspace(0.0, 2.0 * math.pi, 240)
    axes.plot(semi_x * np.cos(angles), semi_y * np.sin(angles),
              np.full_like(angles, height), color="#a33d1f", linewidth=1.6, zorder=8)
    axes.plot_trisurf(semi_x * np.cos(angles), semi_y * np.sin(angles),
                      np.full_like(angles, height), color=SECTION_COLOUR,
                      alpha=SECTION_ALPHA, linewidth=0.0, zorder=7)

    arrow_colour = "#222222"
    axes.quiver(0.0, 0.0, 0.0, AXIS_LENGTH, 0.0, 0.0, color=arrow_colour,
                arrow_length_ratio=0.06, linewidth=1.0)
    axes.quiver(0.0, 0.0, 0.0, 0.0, AXIS_LENGTH, 0.0, color=arrow_colour,
                arrow_length_ratio=0.06, linewidth=1.0)
    axes.quiver(0.0, 0.0, 0.0, 0.0, 0.0, AXIS_LENGTH, color=arrow_colour,
                arrow_length_ratio=0.06, linewidth=1.0)

    surface_point = np.array([anchors.SURFACE_LABEL_POINT[0], anchors.SURFACE_LABEL_POINT[1],
                              anchors.surface_label_height()])
    label_point = np.array([1.42, 0.25, 1.20])

    labels = [
        (np.array([AXIS_LENGTH, 0.0, 0.0]), "$x$", "left", "center"),
        (np.array([0.0, AXIS_LENGTH, 0.0]), "$y$", "left", "center"),
        (np.array([0.0, 0.0, AXIS_LENGTH]), "$z$", "left", "bottom"),
    ]
    for point, text, horizontal, vertical in labels:
        axes.text(point[0], point[1], point[2], text, fontsize=FONT_SIZE, color="#111111",
                  ha=horizontal, va=vertical)

    limit = 1.38
    axes.set_xlim(-limit, limit)
    axes.set_ylim(-limit, limit)
    axes.set_zlim(-limit, limit)
    axes.set_box_aspect((1.0, 1.0, 1.0))
    axes.view_init(elev=22.0, azim=-42.0)
    axes.set_axis_off()

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    body = project(axes, np.column_stack([surface_x.ravel(), surface_y.ravel(),
                                          surface_z.ravel()]))
    ring = project(axes, np.column_stack([semi_x * np.cos(angles), semi_y * np.sin(angles),
                                          np.full_like(angles, height)]))
    axes_box = axes.get_window_extent(renderer)
    for point, text, horizontal, vertical in labels:
        box = display_box(text, point, renderer, axes, horizontal, vertical)
        if (box.x0 < axes_box.x0 or box.x1 > axes_box.x1
                or box.y0 < axes_box.y0 or box.y1 > axes_box.y1):
            raise AssertionError(f"label {text!r} left the axes box at {box.bounds}")
    letter_clearance = float(np.min(np.linalg.norm(
        project(axes, np.array([[AXIS_LENGTH, 0.0, 0.0], [0.0, AXIS_LENGTH, 0.0],
                                [0.0, 0.0, AXIS_LENGTH]]))[:, None, :]
        - project(axes, np.column_stack([surface_x.ravel(), surface_y.ravel(),
                                         surface_z.ravel()]))[None, :, :], axis=2)))

    residual = support.quadratic_form(*surface_point) - 1.0
    if abs(residual) > 1.0e-12:
        raise AssertionError("the surface label does not stand on the surface")
    print(f"the surface label stands at {tuple(round(value, 6) for value in surface_point)}"
          f" with residual {residual:.3e}")
    print(f"the drawn section has semi-axes {semi_x!r} and {semi_y!r} at z = {height}")
    print(f"the smallest axis-letter distance to the body is {letter_clearance:.1f} pixels")

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=430, bbox_inches="tight", pad_inches=0.05)
    plt.close(figure)
    trim_white_margin(FIGURE_PATH)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
