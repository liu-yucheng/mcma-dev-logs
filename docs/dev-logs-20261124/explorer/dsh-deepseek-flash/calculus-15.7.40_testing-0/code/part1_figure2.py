"""Draw the three sections of E at a fixed value of each coordinate.

One panel shows the section at a fixed height, one panel the section at a fixed y, and one panel the section at a
fixed x. Every drawn outline takes its corners from problem_model, and the printed area comes from the same module.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

import problem_model  # noqa: E402

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure2.png"
"""The path of the figure file."""

FIXED_HEIGHT = 0.5
"""The height of the section of the first panel."""

FIXED_Y = 0.5
"""The y value of the section of the second panel."""

FIXED_X = 0.25
"""The x value of the section of the third panel."""

FILL_COLOR = "#4c72b0"
EDGE_COLOR = "#1f3d63"


def assert_titles_inside(figure: plt.Figure, panels: list[plt.Axes]) -> None:
    """Raise an error when a title leaves the figure.

    Args:
        figure: The figure that holds the panels.
        panels: The three panels.
    """
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


def main() -> None:
    """Draw the figure and write it to the figures directory."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure, panels = plt.subplots(1, 3, figsize=(13.2, 4.6))

    height_corners = np.array([[corner[0], corner[1]] for corner in problem_model.corners_at_z(FIXED_HEIGHT)])
    height_area = float(problem_model.cross_section_area_at_z(FIXED_HEIGHT))
    panels[0].fill(height_corners[:, 0], height_corners[:, 1], color=FILL_COLOR, alpha=0.55)
    panels[0].plot(
        np.append(height_corners[:, 0], height_corners[0, 0]),
        np.append(height_corners[:, 1], height_corners[0, 1]),
        color=EDGE_COLOR,
        linewidth=2.0,
    )
    panels[0].set_xlabel("$x$", fontsize=12)
    panels[0].set_ylabel("$y$", fontsize=12)
    panels[0].set_title(
        f"plane $z = {FIXED_HEIGHT}$ keeps $x$ and $y$\nrectangle, area $= {height_area:.4f}$", fontsize=11
    )

    y_corners = np.array([[corner[0], corner[2]] for corner in problem_model.corners_at_y(FIXED_Y)])
    y_area = float(problem_model.cross_section_area_at_y(FIXED_Y))
    panels[1].fill(y_corners[:, 0], y_corners[:, 1], color=FILL_COLOR, alpha=0.55)
    panels[1].plot(
        np.append(y_corners[:, 0], y_corners[0, 0]),
        np.append(y_corners[:, 1], y_corners[0, 1]),
        color=EDGE_COLOR,
        linewidth=2.0,
    )
    panels[1].set_xlabel("$x$", fontsize=12)
    panels[1].set_ylabel("$z$", fontsize=12)
    panels[1].set_title(
        f"plane $y = {FIXED_Y}$ keeps $x$ and $z$\ntrapezoid, area $= {y_area:.4f}$", fontsize=11
    )

    coordinate_z = np.linspace(0.0, 1.0 - FIXED_X, 240)
    half_width = np.sqrt(1.0 - coordinate_z)
    panels[2].fill_betweenx(coordinate_z, -half_width, half_width, color=FILL_COLOR, alpha=0.55)
    panels[2].plot(half_width, coordinate_z, color=EDGE_COLOR, linewidth=2.0)
    panels[2].plot(-half_width, coordinate_z, color=EDGE_COLOR, linewidth=2.0)
    x_area = float(problem_model.cross_section_area_at_x(FIXED_X))
    panels[2].set_xlabel("$y$", fontsize=12)
    panels[2].set_ylabel("$z$", fontsize=12)
    panels[2].set_title(
        f"plane $x = {FIXED_X}$ keeps $y$ and $z$\ncurved region, area $= {x_area:.4f}$", fontsize=11
    )

    for panel in panels:
        panel.set_aspect("equal", adjustable="box")
        panel.grid(alpha=0.25, linewidth=0.6)
        panel.tick_params(labelsize=9)

    assert_titles_inside(figure, list(panels))
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"FIGURE written: {FIGURE_PATH}")
    print(f"section areas: {height_area:.6f}, {y_area:.6f}, {x_area:.6f}")


if __name__ == "__main__":
    main()
