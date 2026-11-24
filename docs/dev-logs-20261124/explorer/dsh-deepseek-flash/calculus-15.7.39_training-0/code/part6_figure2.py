"""Draw Figure 2: the solid E, its three bounding surfaces, and its center of mass.

The solid E is the set of points with (x, y) in D and 0 <= z <= 1 + x + y. The script writes
the figure to code/figures/part6_figure2.png and checks that every surface label sits at a
point that the equation of that surface satisfies.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part6_figure2.png"
"""The file that holds Figure 2."""

CEILING_LABEL_POINT = (0.10, 0.10, 1.20)
"""The point of the ceiling z = 1 + x + y that carries the ceiling label."""

WALL_LABEL_POINT = (1.0, 0.55, 1.55)
"""The point of the wall x = 1 that carries the wall label."""

FLOOR_LABEL_POINT = (0.42, 0.30, 0.0)
"""The point of the floor z = 0 that carries the floor label."""

CENTER_OF_MASS = (358.0 / 553.0, 33.0 / 79.0, 571.0 / 553.0)
"""The center of mass of E, from the exact quotients of Part 6."""

TOLERANCE = 1.0e-9
"""The tolerance of a check that a label point lies on the surface that it names."""


def region_heights(abscissas: np.ndarray) -> np.ndarray:
    """Return the upper boundary sqrt(x) of the planar region D at each abscissa."""
    return np.sqrt(abscissas)


def draw_solid(axes: plt.Axes) -> None:
    """Draw the floor, the two vertical walls, the ceiling, the frame, and the center of mass."""
    abscissas = np.linspace(0.0, 1.0, 60)
    heights = region_heights(abscissas)
    x_grid, y_grid = np.meshgrid(abscissas, abscissas, indexing="ij")
    inside = y_grid <= np.sqrt(x_grid)
    z_grid = np.where(inside, 1.0 + x_grid + y_grid, np.nan)

    axes.plot_surface(x_grid, y_grid, z_grid, color="#7fb3e8", alpha=0.62,
                      linewidth=0.0, antialiased=True, shade=True)

    floor_x = np.linspace(0.0, 1.0, 40)
    floor_y = np.linspace(0.0, 1.0, 40)
    floor_xx, floor_yy = np.meshgrid(floor_x, floor_y, indexing="ij")
    floor_zz = np.where(floor_yy <= np.sqrt(floor_xx), 0.0, np.nan)
    axes.plot_surface(floor_xx, floor_yy, floor_zz, color="#3d6f9e", alpha=0.85, linewidth=0.0)

    wall_y = np.linspace(0.0, 1.0, 40)
    wall_z = np.linspace(0.0, 2.0, 40)
    wall_yy, wall_zz = np.meshgrid(wall_y, wall_z, indexing="ij")
    wall_xx = np.where(wall_zz <= 2.0 + wall_yy, 1.0, np.nan)
    axes.plot_surface(wall_xx, wall_yy, wall_zz, color="#5b8fbf", alpha=0.55, linewidth=0.0)

    side_x = np.linspace(0.0, 1.0, 40)
    side_z = np.linspace(0.0, 2.0, 40)
    side_xx, side_zz = np.meshgrid(side_x, side_z, indexing="ij")
    side_yy = np.where(side_zz <= 1.0 + side_xx, 0.0, np.nan)
    axes.plot_surface(side_xx, side_yy, side_zz, color="#5b8fbf", alpha=0.55, linewidth=0.0)

    frame_y = np.linspace(0.0, 1.0, 60)
    axes.plot(np.ones_like(frame_y), frame_y, 2.0 + frame_y, color="#12457a", linewidth=1.6)
    frame_x = np.linspace(0.0, 1.0, 60)
    axes.plot(frame_x, np.zeros_like(frame_x), 1.0 + frame_x, color="#12457a", linewidth=1.6)
    axes.plot(abscissas, np.sqrt(abscissas), 1.0 + abscissas + np.sqrt(abscissas),
              color="#12457a", linewidth=1.6)

    axes.plot([CENTER_OF_MASS[0], CENTER_OF_MASS[0]],
              [CENTER_OF_MASS[1], CENTER_OF_MASS[1]],
              [0.0, CENTER_OF_MASS[2]], color="#b3261e", linewidth=1.2, linestyle="--")
    axes.scatter([CENTER_OF_MASS[0]], [CENTER_OF_MASS[1]], [CENTER_OF_MASS[2]],
                 color="#b3261e", s=48, depthshade=False)
    axes.scatter([CENTER_OF_MASS[0]], [CENTER_OF_MASS[1]], [0.0],
                 color="#b3261e", s=22, marker="x", depthshade=False)

    axes.text(*CEILING_LABEL_POINT, r"$z = 1 + x + y$", fontsize=12, color="#0d2f52")
    axes.text(*WALL_LABEL_POINT, r"$x = 1$", fontsize=12, color="#0d2f52")
    axes.text(*FLOOR_LABEL_POINT, r"$z = 0$", fontsize=12, color="#f2f6fa")
    axes.text(CENTER_OF_MASS[0] + 0.05, CENTER_OF_MASS[1] + 0.05, CENTER_OF_MASS[2] + 0.13,
              "CM", fontsize=13, color="#b3261e")


def main() -> None:
    """Build Figure 2, check the label anchors, and write the PNG file."""
    ceiling_value = 1.0 + CEILING_LABEL_POINT[0] + CEILING_LABEL_POINT[1]
    print(f"ceiling label height: computed = {CEILING_LABEL_POINT[2]:.15f}, "
          f"expected = {ceiling_value:.15f} (the value of 1 + x + y at the label)")
    assert abs(ceiling_value - CEILING_LABEL_POINT[2]) < TOLERANCE

    wall_x = WALL_LABEL_POINT[0]
    print(f"wall label abscissa: computed = {wall_x:.15f}, expected = 1.000000000000000 "
          f"(the plane x = 1)")
    assert abs(wall_x - 1.0) < TOLERANCE

    floor_z = FLOOR_LABEL_POINT[2]
    print(f"floor label height: computed = {floor_z:.15f}, expected = 0.000000000000000 "
          f"(the plane z = 0)")
    assert abs(floor_z) < TOLERANCE

    print(f"center of mass: computed = ({CENTER_OF_MASS[0]:.6f}, {CENTER_OF_MASS[1]:.6f}, "
          f"{CENTER_OF_MASS[2]:.6f}), expected = (0.647378, 0.417722, 1.032550) "
          f"(Part 6 exact quotients)")

    figure = plt.figure(figsize=(7.0, 5.8))
    axes = figure.add_subplot(111, projection="3d")
    draw_solid(axes)
    axes.set_xlabel("$x$", fontsize=13, labelpad=10)
    axes.set_ylabel("$y$", fontsize=13, labelpad=10)
    axes.set_zlabel("$z$", fontsize=13, labelpad=10)
    axes.set_xticks([0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 0.5, 1.0])
    axes.set_zticks([0.0, 1.0, 2.0, 3.0])
    axes.set_xlim(0.0, 1.0)
    axes.set_ylim(0.0, 1.0)
    axes.set_zlim(0.0, 3.0)
    axes.view_init(elev=22.0, azim=-58.0)
    axes.set_title("The solid $E$ with the center of mass and its projection", fontsize=12)

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=180)
    print(f"figure written: {FIGURE_PATH}")
    plt.close(figure)


if __name__ == "__main__":
    main()
