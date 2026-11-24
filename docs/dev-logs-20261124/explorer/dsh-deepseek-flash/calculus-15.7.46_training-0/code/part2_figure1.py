"""Draw Figure 2: the cross section of the cone in the r-z half plane.

The shaded region holds every pair (r, z) of the solid. The vertical segment at a fixed
radius r0 shows the inner limits r0 <= z <= h. The horizontal segment at a fixed height z0
shows the radius 0 <= r <= z0 of one horizontal slice. The script asserts that each text box
lies inside the axes box before it writes the PNG file.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import importlib.metadata
import platform

HEIGHT = 1.0
"""The height h of the cone."""

RADIUS_OF_SEGMENT = 0.45
"""The fixed radius r0 of the vertical segment that shows the inner limits."""

HEIGHT_OF_SLICE = 0.72
"""The fixed height z0 of the horizontal segment that shows the slice radius."""

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part2_figure1.png"
"""The output path of the figure."""


def region_boundary(height: float, samples: int) -> tuple[np.ndarray, np.ndarray]:
    """Return the closed boundary of the region 0 <= r <= z <= height.

    Args:
        height: The height h of the cone.
        samples: The number of points on each straight part of the boundary.

    Returns:
        The arrays r and z that follow the boundary from the apex to the base.
    """
    radius = np.linspace(0.0, height, samples)
    return radius, radius


def region_polygon(height: float) -> tuple[np.ndarray, np.ndarray]:
    """Return the vertices of the triangular region in the order that fills it.

    Args:
        height: The height h of the cone.

    Returns:
        The arrays r and z of the three vertices.
    """
    return np.array([0.0, height, 0.0]), np.array([0.0, height, height])


def inside_axes(axes: plt.Axes, text: plt.Text, renderer: object) -> bool:
    """Return True when the drawn box of a text lies inside the axes box.

    Args:
        axes: The axes that holds the text.
        text: The text object.
        renderer: The renderer of the canvas.

    Returns:
        True when the text box lies fully inside the axes box.
    """
    box = text.get_window_extent(renderer=renderer)
    return bool(
        box.x0 >= axes.bbox.x0
        and box.y0 >= axes.bbox.y0
        and box.x1 <= axes.bbox.x1
        and box.y1 <= axes.bbox.y1
    )


def report_environment() -> None:
    """Print the version of each tool, so that the figure repeats."""
    package_names = ("numpy", "matplotlib")
    versions = ", ".join(
        f"{name} {importlib.metadata.version(name)}" for name in package_names
    )
    print(f"Python {platform.python_version()}, {versions}")


def main() -> None:
    """Draw the figure, check the label positions, and write the PNG file."""
    report_environment()
    figure, axes = plt.subplots(figsize=(6.4, 5.6))
    label_box = {"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "#c8ccd2",
                 "alpha": 0.94}

    radius_line, height_line = region_boundary(HEIGHT, 200)
    polygon_radius, polygon_height = region_polygon(HEIGHT)
    axes.fill(polygon_radius, polygon_height, color="#a9cbe8", alpha=0.55, zorder=1)
    axes.plot(radius_line, height_line, color="#1f4e79", linewidth=1.8, zorder=3,
              label="$z=r$, the wall of the cone")
    axes.plot([0.0, 0.0], [0.0, HEIGHT], color="#1f4e79", linewidth=1.8, zorder=3)
    axes.plot([0.0, HEIGHT], [HEIGHT, HEIGHT], color="#1f4e79", linewidth=1.8, zorder=3,
              label="$z=h$, the base of the cone")

    axes.plot([RADIUS_OF_SEGMENT, RADIUS_OF_SEGMENT], [RADIUS_OF_SEGMENT, HEIGHT],
              color="#8c2f1e", linewidth=2.6, zorder=5,
              label="$r_0\\leq z\\leq h$, the inner limits at $r=r_0$")
    axes.plot([0.0, HEIGHT_OF_SLICE], [HEIGHT_OF_SLICE, HEIGHT_OF_SLICE],
              color="#b5432f", linewidth=2.2, linestyle="--", zorder=4,
              label="$0\\leq r\\leq z_0$, the radius of one slice")
    axes.plot([RADIUS_OF_SEGMENT], [RADIUS_OF_SEGMENT], marker="o", markersize=5.0,
              color="#8c2f1e", zorder=6)
    axes.plot([0.0], [HEIGHT_OF_SLICE], marker="o", markersize=4.0, color="#b5432f", zorder=6)

    axes.set_xlim(0.0, 1.10 * HEIGHT)
    axes.set_ylim(0.0, 1.10 * HEIGHT)
    axes.set_xticks([0.0, RADIUS_OF_SEGMENT, HEIGHT])
    axes.set_yticks([0.0, RADIUS_OF_SEGMENT, HEIGHT_OF_SLICE, HEIGHT])
    axes.set_xticklabels(["$0$", "$r_0$", "$h$"], fontsize=10)
    axes.set_yticklabels(["$0$", "$r_0$", "$z_0$", "$h$"], fontsize=10)
    axes.set_xlabel("$r$, the distance from the $z$ axis", fontsize=11)
    axes.set_ylabel("$z$, the height", fontsize=11)
    axes.set_title("Cross section of the solid cone in the $rz$ plane", fontsize=11.5)
    axes.grid(True, color="#dfe3e8", linewidth=0.7, zorder=0)
    axes.set_axisbelow(True)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)

    axes.plot([0.33, RADIUS_OF_SEGMENT - 0.012], [0.90, 0.88], color="#5a6b7d", linewidth=0.9,
              zorder=9)
    axes.plot([0.755, HEIGHT_OF_SLICE + 0.022], [0.60, HEIGHT_OF_SLICE - 0.008],
              color="#5a6b7d", linewidth=0.9, zorder=9)
    annotations = [
        axes.text(0.20, 0.58, "the solid" "\n" r"$r\leq z\leq h$", fontsize=10.5,
                  color="#1f4e79", ha="center", va="center", bbox=label_box, zorder=10),
        axes.text(0.20, 0.92, "inner limits" "\n" r"at $r=r_0$", fontsize=9.5,
                  color="#8c2f1e", ha="center", va="center", bbox=label_box, zorder=10),
        axes.text(0.80, 0.60, "one slice" "\n" r"$z=z_0$", fontsize=9.5,
                  color="#b5432f", ha="left", va="center", bbox=label_box, zorder=10),
        axes.text(0.10, 0.10, "apex", fontsize=9.5, color="#1f4e79", ha="left", va="center"),
    ]
    axes.legend(loc="lower right", fontsize=8.6, framealpha=0.94,
                bbox_to_anchor=(1.0, 0.02))

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for index, text in enumerate(annotations, start=1):
        inside = inside_axes(axes, text, renderer)
        print(f"annotation {index} inside the axes box: computed = {inside}, expected = True")
        assert inside, f"the annotation {index} leaves the axes box"
    legend_box = axes.get_legend().get_window_extent(renderer=renderer)
    inside_legend = bool(
        legend_box.x0 >= axes.bbox.x0
        and legend_box.y0 >= axes.bbox.y0
        and legend_box.x1 <= axes.bbox.x1
        and legend_box.y1 <= axes.bbox.y1
    )
    print(f"legend inside the axes box: computed = {inside_legend}, expected = True")
    assert inside_legend, "the legend leaves the axes box"

    print(f"vertical segment limits: z from {RADIUS_OF_SEGMENT:.4f} to {HEIGHT:.4f}")
    print(f"horizontal segment limits: r from {0.0:.4f} to {HEIGHT_OF_SLICE:.4f}")

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=200, bbox_inches="tight")
    print(f"figure written: {FIGURE_PATH}")


if __name__ == "__main__":
    main()
