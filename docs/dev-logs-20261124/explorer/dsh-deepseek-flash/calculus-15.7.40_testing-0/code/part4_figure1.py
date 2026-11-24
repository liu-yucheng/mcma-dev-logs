"""Draw the shadow of E on the plane z = 0 and the projection of E on the plane y = 0.

The left panel shows the rectangle [0, 1] x [-1, 1] on the plane z = 0. The right panel shows the triangle with the
corners (0, 0), (1, 0) and (0, 1) on the plane y = 0, together with the center of mass and the centroid.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

import figure_anchors  # noqa: E402
import problem_model  # noqa: E402

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part4_figure1.png"
"""The path of the figure file."""

FILL_COLOR = "#4c72b0"
EDGE_COLOR = "#1f3d63"
POINT_COLOR = "#c44e52"
CENTROID_COLOR = "#55a868"


def main() -> None:
    """Draw the figure and write it to the figures directory."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure, panels = plt.subplots(1, 2, figsize=(9.0, 4.9), gridspec_kw={"width_ratios": [1.5, 1.0]})

    shadow = np.array([[0.0, -1.0], [1.0, -1.0], [1.0, 1.0], [0.0, 1.0]])
    shadow_area = problem_model.polygon_area(np.column_stack((shadow, np.zeros(4))), 0, 1)
    panels[0].fill(shadow[:, 0], shadow[:, 1], color=FILL_COLOR, alpha=0.45)
    panels[0].plot(
        np.append(shadow[:, 0], shadow[0, 0]),
        np.append(shadow[:, 1], shadow[0, 1]),
        color=EDGE_COLOR,
        linewidth=2.0,
    )
    panels[0].set_xlabel("$x$", fontsize=12)
    panels[0].set_ylabel("$y$", fontsize=12)
    panels[0].set_title(
        f"shadow on the plane $z = 0$ keeps $x$ and $y$\nrectangle, area $= {shadow_area:.4f}$", fontsize=11
    )

    triangle = figure_anchors.projection_polygon()
    triangle_area = problem_model.polygon_area(np.column_stack((triangle, np.zeros(3))), 0, 1)
    panels[1].fill(triangle[:, 0], triangle[:, 1], color=FILL_COLOR, alpha=0.45)
    panels[1].plot(
        np.append(triangle[:, 0], triangle[0, 0]),
        np.append(triangle[:, 1], triangle[0, 1]),
        color=EDGE_COLOR,
        linewidth=2.0,
    )
    center = figure_anchors.CENTER_OF_MASS_POINT
    centroid = figure_anchors.TRIANGLE_CENTROID_POINT
    panels[1].plot([center[0]], [center[1]], marker="o", markersize=8, color=POINT_COLOR, linestyle="none")
    panels[1].plot([centroid[0]], [centroid[1]], marker="s", markersize=7, color=CENTROID_COLOR, linestyle="none")
    panels[1].legend(
        handles=[
            Line2D([], [], marker="o", markersize=8, color=POINT_COLOR, linestyle="none",
                   label="center of mass $(5/14, 2/7)$"),
            Line2D([], [], marker="s", markersize=7, color=CENTROID_COLOR, linestyle="none",
                   label="centroid $(1/3, 1/3)$"),
        ],
        loc="lower left",
        fontsize=8.5,
        frameon=True,
        framealpha=0.95,
        borderpad=0.5,
    )
    panels[1].set_xlabel("$x$", fontsize=12)
    panels[1].set_ylabel("$z$", fontsize=12)
    panels[1].set_title(
        f"projection on the plane $y = 0$ keeps $x$ and $z$\ntriangle, area $= {triangle_area:.4f}$", fontsize=11
    )

    for panel in panels:
        panel.set_aspect("equal", adjustable="box")
        panel.grid(alpha=0.25, linewidth=0.6)
        panel.tick_params(labelsize=9)
        panel.set_xlim(-0.18, 1.22)
        panel.set_ylim(-1.22, 1.22)

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    figure_box = figure.get_window_extent(renderer)
    for panel in panels:
        extent = panel.title.get_window_extent(renderer)
        if not (
            figure_box.x0 <= extent.x0
            and extent.x1 <= figure_box.x1
            and figure_box.y0 <= extent.y0
            and extent.y1 <= figure_box.y1
        ):
            raise ValueError(f"title {panel.get_title()!r} leaves the figure")

    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"FIGURE written: {FIGURE_PATH}")
    print(f"shadow area: {shadow_area:.6f}; projection area: {triangle_area:.6f}")
    print(f"center of mass in the projection: ({center[0]:.6f}, {center[1]:.6f})")
    print(f"centroid of the triangle: ({centroid[0]:.6f}, {centroid[1]:.6f})")


if __name__ == "__main__":
    main()
