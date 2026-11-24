"""Draw the solid E: one cross-section and the three-dimensional view.

The left panel shows the section in the plane z = 0. The right panel shows the paraboloid cap
between x = 4 y^2 + 4 z^2 and the plane x = 4.
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

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""Output path of the figure."""


def draw_cross_section(axes: plt.Axes) -> None:
    """Draw the section of E in the plane z = 0.

    Args:
        axes: Target axes of the drawing.
    """
    y_values = np.linspace(-1.08, 1.08, 400)
    x_paraboloid = PARABOLOID_FACTOR * y_values**2
    axes.fill_between(
        y_values,
        x_paraboloid,
        PLANE_X,
        where=x_paraboloid <= PLANE_X,
        color="#c9dcf0",
        alpha=0.85,
        label="section of $E$",
    )
    axes.plot(y_values, x_paraboloid, color="#1f4e79", linewidth=2.0,
              label=r"$x = 4y^2 + 4z^2$")
    axes.plot(y_values, np.full_like(y_values, PLANE_X), color="#a33", linewidth=2.0,
              label=r"$x = 4$")
    axes.plot([1.0, 1.0], [0.0, PLANE_X], color="#555", linestyle=":", linewidth=1.2)
    axes.annotate(r"$y^2 + z^2 = 1$", xy=(1.0, 2.9), xytext=(1.12, 2.55),
                  fontsize=12, color="#333")
    axes.set_xlim(-1.25, 1.35)
    axes.set_ylim(-0.5, 4.6)
    axes.set_xlabel(r"$y$  (at $z = 0$)")
    axes.set_ylabel(r"$x$")
    axes.set_title("Section at $z = 0$")
    axes.grid(True, alpha=0.3)
    axes.legend(loc="upper center", fontsize=11, framealpha=0.9)


def draw_solid(axes: plt.Axes) -> None:
    """Draw the paraboloid cap and its top disk in three dimensions.

    Args:
        axes: Target three-dimensional axes of the drawing.
    """
    radius = np.linspace(0.0, 1.0, 60)
    angle = np.linspace(0.0, 2.0 * np.pi, 90)
    radius_grid, angle_grid = np.meshgrid(radius, angle)
    x_grid = PARABOLOID_FACTOR * radius_grid**2
    y_grid = radius_grid * np.cos(angle_grid)
    z_grid = radius_grid * np.sin(angle_grid)
    axes.plot_surface(x_grid, y_grid, z_grid, cmap="Blues", alpha=0.75, linewidth=0,
                      antialiased=True, edgecolor="none")

    cap_radius = np.linspace(0.0, 1.0, 20)
    cap_angle = np.linspace(0.0, 2.0 * np.pi, 80)
    cap_radius_grid, cap_angle_grid = np.meshgrid(cap_radius, cap_angle)
    axes.plot_surface(
        np.full_like(cap_radius_grid, PLANE_X),
        cap_radius_grid * np.cos(cap_angle_grid),
        cap_radius_grid * np.sin(cap_angle_grid),
        color="#f2b8b8",
        alpha=0.55,
        linewidth=0,
    )
    rim_angle = np.linspace(0.0, 2.0 * np.pi, 200)
    axes.plot(np.full_like(rim_angle, PLANE_X), np.cos(rim_angle), np.sin(rim_angle),
              color="#a33", linewidth=2.0)
    axes.set_xlabel(r"$x$")
    axes.set_ylabel(r"$y$")
    axes.set_zlabel(r"$z$")
    axes.set_title(r"$E$: $4y^2 + 4z^2 \leq x \leq 4$")
    axes.view_init(elev=18.0, azim=-64.0)
    axes.set_box_aspect((1.2, 1.0, 1.0))
    axes.set_xticks([0.0, 2.0, 4.0])
    axes.set_yticks([-1.0, 0.0, 1.0])
    axes.set_zticks([-1.0, 0.0, 1.0])
    axes.tick_params(labelsize=10, pad=1.5)
    axes.set_xlim(0.0, 4.4)
    axes.set_ylim(-1.1, 1.1)
    axes.set_zlim(-1.1, 1.1)


def main() -> None:
    """Build the figure and write it to the figures directory."""
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 12, "axes.titlesize": 13, "axes.labelsize": 12})
    figure = plt.figure(figsize=(9.6, 4.2), constrained_layout=True)
    section_axes = figure.add_subplot(1, 2, 1)
    solid_axes = figure.add_subplot(1, 2, 2, projection="3d")
    draw_cross_section(section_axes)
    draw_solid(solid_axes)
    figure.savefig(FIGURE_PATH, dpi=190, facecolor="white")
    plt.close(figure)
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
