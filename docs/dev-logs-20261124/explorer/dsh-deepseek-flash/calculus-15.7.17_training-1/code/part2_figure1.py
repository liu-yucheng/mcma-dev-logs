"""Draw one vertical segment of E and the reduced integrand over the disk.

The left panel shows the segment from x = 4 r^2 to x = 4 for two radii. The right panel shows the
value of the inner integral as a function of the point in the disk.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (the backend must be set first)

PARABOLOID_FACTOR = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_X = 4.0
"""Coordinate x of the plane that closes the solid."""

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part2_figure1.png"
"""Output path of the figure."""

MARKED_RADII = (0.45, 0.82)
"""Radii of the two segments that the left panel shows."""

COLORS = ("#1f6f43", "#8a4b08")
"""Colors of the two segments."""


def draw_segments(axes: plt.Axes) -> None:
    """Draw the radius-height section of E with two marked segments.

    Args:
        axes: Target axes of the drawing.
    """
    radius_values = np.linspace(0.0, 1.0, 300)
    axes.fill_between(radius_values, PARABOLOID_FACTOR * radius_values**2, PLANE_X,
                      color="#c9dcf0", alpha=0.8, label=r"$4r^2 \leq x \leq 4$")
    axes.plot(radius_values, PARABOLOID_FACTOR * radius_values**2, color="#1f4e79", linewidth=2.0,
              label=r"$x = 4r^2$")
    axes.plot([0.0, 1.0], [PLANE_X, PLANE_X], color="#a33", linewidth=2.0, label=r"$x = 4$")
    for radius, color in zip(MARKED_RADII, COLORS):
        lower = PARABOLOID_FACTOR * radius**2
        axes.annotate(
            "",
            xy=(radius, PLANE_X),
            xytext=(radius, lower),
            arrowprops={"arrowstyle": "<->", "color": color, "linewidth": 1.8},
        )
        axes.text(radius + 0.10, 0.5 * (lower + PLANE_X), rf"$4-4r^2={PLANE_X - lower:.2f}$",
                  color=color, fontsize=11, rotation=90, va="center", ha="left")
        axes.plot([radius], [lower], "o", color=color, markersize=4)
    axes.set_xlim(-0.03, 1.12)
    axes.set_ylim(-0.25, 4.4)
    axes.set_xlabel(r"$r = \sqrt{y^2 + z^2}$")
    axes.set_ylabel(r"$x$")
    axes.set_title("One segment along $x$ at a fixed $(y, z)$")
    axes.grid(True, alpha=0.3)
    axes.legend(loc="upper left", fontsize=10, framealpha=0.9)


def draw_inner_integral(axes: plt.Axes) -> None:
    """Draw the level curves of the inner integral over the unit disk.

    Args:
        axes: Target axes of the drawing.
    """
    coordinate = np.linspace(-1.0, 1.0, 400)
    y_grid, z_grid = np.meshgrid(coordinate, coordinate)
    radius_squared = y_grid**2 + z_grid**2
    values = 8.0 * (1.0 - radius_squared**2)
    values = np.where(radius_squared <= 1.0, values, np.nan)
    filled = axes.contourf(y_grid, z_grid, values, levels=20, cmap="YlGnBu")
    axes.contour(y_grid, z_grid, np.sqrt(radius_squared), levels=[0.25, 0.5, 0.75, 1.0],
                 colors="#444", linewidths=0.8)
    axes.plot(np.cos(np.linspace(0.0, 2.0 * np.pi, 400)), np.sin(np.linspace(0.0, 2.0 * np.pi, 400)),
              color="#111", linewidth=1.6)
    axes.set_aspect("equal")
    axes.set_xlim(-1.15, 1.15)
    axes.set_ylim(-1.15, 1.15)
    axes.set_xlabel(r"$y$")
    axes.set_ylabel(r"$z$")
    axes.set_title(r"$g(y,z) = 8\left(1 - (y^2 + z^2)^2\right)$ on $D$")
    colorbar = plt.colorbar(filled, ax=axes, shrink=0.85)
    colorbar.set_label("value of the inner integral")


def main() -> None:
    """Build the figure and write it to the figures directory."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 12, "axes.titlesize": 13, "axes.labelsize": 12})
    figure = plt.figure(figsize=(9.6, 4.2), constrained_layout=True)
    segment_axes = figure.add_subplot(1, 2, 1)
    integral_axes = figure.add_subplot(1, 2, 2)
    draw_segments(segment_axes)
    draw_inner_integral(integral_axes)
    figure.savefig(FIGURE_PATH, dpi=190, facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
