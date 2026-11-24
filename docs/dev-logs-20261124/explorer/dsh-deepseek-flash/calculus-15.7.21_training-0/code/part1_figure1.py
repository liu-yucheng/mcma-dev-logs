"""Draw the solid that the cylinder y = x^2 and the planes z = 0 and y + z = 1 enclose.

The figure uses ruled lines, because a ruled line drawing has no hidden face
that a shaded face would produce. The blue lines are the rulings of the
parabolic cylinder. The orange lines are the grid of the plane y + z = 1.
The three thick black curves are the edges of the solid. The red triangle is
the cross-section at x = 0.5.

The script writes code/figures/part1_figure1.png.

Run this script with: code/.venv/Scripts/python.exe code/part1_figure1.py
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_PATH = pathlib.Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""Output path of the figure of Part 1."""

WALL_COLOR = "#2f6690"
"""Color of the rulings of the parabolic cylinder."""

ROOF_COLOR = "#b5651d"
"""Color of the grid of the plane y + z = 1."""

FLOOR_COLOR = "#8a8a8a"
"""Color of the grid of the plane z = 0."""

SECTION_COLOR = "#c0322f"
"""Color of the cross-section at x = 0.5."""

ABSCISSA = np.linspace(-1.0, 1.0, 400)
"""Dense abscissas for the three edge curves."""


def draw_wall(axes: plt.Axes) -> None:
    """Draw the rulings and the horizontal parabolas of the cylinder y = x^2.

    Args:
        axes: Three dimensional axes of the figure.

    Returns:
        None.
    """
    for abscissa in np.linspace(-1.0, 1.0, 25):
        axes.plot(
            [abscissa, abscissa],
            [abscissa * abscissa, abscissa * abscissa],
            [0.0, 1.0 - abscissa * abscissa],
            color=WALL_COLOR,
            linewidth=0.8,
            alpha=0.85,
        )
    for height in np.linspace(0.0, 1.0, 9):
        visible = height <= 1.0 - ABSCISSA * ABSCISSA
        axes.plot(
            ABSCISSA[visible],
            ABSCISSA[visible] ** 2,
            np.full(int(np.count_nonzero(visible)), height),
            color=WALL_COLOR,
            linewidth=0.8,
            alpha=0.85,
        )


def draw_roof(axes: plt.Axes) -> None:
    """Draw the grid of the plane z = 1 - y over the projection.

    Args:
        axes: Three dimensional axes of the figure.

    Returns:
        None.
    """
    for ordinate in np.linspace(0.0, 1.0, 11):
        half_width = np.sqrt(ordinate)
        axes.plot(
            [-half_width, half_width],
            [ordinate, ordinate],
            [1.0 - ordinate, 1.0 - ordinate],
            color=ROOF_COLOR,
            linewidth=1.0,
            alpha=0.95,
        )
    for abscissa in np.linspace(-1.0, 1.0, 11):
        ordinates = np.linspace(abscissa * abscissa, 1.0, 100)
        axes.plot(
            np.full_like(ordinates, abscissa),
            ordinates,
            1.0 - ordinates,
            color=ROOF_COLOR,
            linewidth=0.6,
            alpha=0.55,
        )


def draw_floor(axes: plt.Axes) -> None:
    """Draw the grid of the plane z = 0 over the projection.

    Args:
        axes: Three dimensional axes of the figure.

    Returns:
        None.
    """
    for ordinate in np.linspace(0.0, 1.0, 6):
        half_width = np.sqrt(ordinate)
        axes.plot([-half_width, half_width], [ordinate, ordinate], [0.0, 0.0],
                  color=FLOOR_COLOR, linewidth=0.7, alpha=0.5)


def draw_edge_curves(axes: plt.Axes) -> None:
    """Draw the three curves where two faces of the solid meet.

    Args:
        axes: Three dimensional axes of the figure.

    Returns:
        None.
    """
    axes.plot(ABSCISSA, ABSCISSA ** 2, np.zeros_like(ABSCISSA), color="black", linewidth=2.2)
    axes.plot(ABSCISSA, ABSCISSA ** 2, 1.0 - ABSCISSA ** 2, color="black", linewidth=2.2)
    axes.plot(ABSCISSA, np.ones_like(ABSCISSA), np.zeros_like(ABSCISSA),
              color="black", linewidth=2.2, linestyle="--")


def draw_cross_section(axes: plt.Axes, abscissa: float) -> None:
    """Draw the cross-section at one fixed value of x.

    Args:
        axes: Three dimensional axes of the figure.
        abscissa: Fixed x coordinate.

    Returns:
        None.
    """
    ordinate_low = abscissa * abscissa
    height = 1.0 - ordinate_low
    section_ordinate = np.array([ordinate_low, 1.0, ordinate_low, ordinate_low])
    section_height = np.array([0.0, 0.0, height, 0.0])
    section_abscissa = np.full_like(section_ordinate, abscissa)
    axes.plot(section_abscissa, section_ordinate, section_height, color=SECTION_COLOR, linewidth=2.6)
    axes.text(abscissa + 0.04, 0.68, 0.50, "cross-section\nat $x=0.5$",
              color=SECTION_COLOR, fontsize=10)


def main() -> None:
    """Draw the figure of Part 1 and write it to the figures directory."""
    figure = plt.figure(figsize=(8.8, 6.0))
    axes = figure.add_subplot(111, projection="3d")
    draw_floor(axes)
    draw_wall(axes)
    draw_roof(axes)
    draw_edge_curves(axes)
    draw_cross_section(axes, 0.5)

    axes.set_xlim(-1.05, 1.05)
    axes.set_ylim(-0.05, 1.05)
    axes.set_zlim(-0.05, 1.05)
    axes.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    axes.set_zticks([0.0, 0.25, 0.5, 0.75, 1.0])
    axes.set_xlabel("$x$", labelpad=6)
    axes.set_ylabel("$y$", labelpad=6)
    axes.set_zlabel("$z$", labelpad=6)
    axes.set_box_aspect((2.0, 1.05, 1.0))
    axes.set_proj_type("ortho")
    axes.view_init(elev=24.0, azim=-58.0)
    axes.set_title("The solid between $y=x^2$, $z=0$, and $y+z=1$", fontsize=13, pad=6)

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.subplots_adjust(left=0.0, right=0.98, bottom=0.0, top=0.93)
    figure.savefig(FIGURE_PATH, dpi=190)
    plt.close(figure)
    print(f"figure written to {FIGURE_PATH}")


if __name__ == "__main__":
    main()
