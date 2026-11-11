"""Draw the silo: a cylinder of radius 3 and height 10 with a hemispherical roof.

The figure has two panels. The left panel shows the solid in space. The right
panel is a side elevation with the three governing dimensions marked.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part1_figure1"
RADIUS = 3.0
WALL_HEIGHT = 10.0


def draw_solid(axes):
    """Draw the three-dimensional silo on the given axes."""
    angle = np.linspace(0.0, 2.0 * np.pi, 160)
    height = np.linspace(0.0, WALL_HEIGHT, 60)
    grid_angle, grid_height = np.meshgrid(angle, height)
    wall_x = RADIUS * np.cos(grid_angle)
    wall_y = RADIUS * np.sin(grid_angle)

    polar = np.linspace(0.0, np.pi / 2.0, 40)
    grid_polar, grid_angle_dome = np.meshgrid(polar, angle)
    dome_radius = RADIUS * np.sin(grid_polar)
    dome_x = dome_radius * np.cos(grid_angle_dome)
    dome_y = dome_radius * np.sin(grid_angle_dome)
    dome_z = WALL_HEIGHT + RADIUS * np.cos(grid_polar)

    axes.plot_surface(wall_x, wall_y, grid_height, color="#b7c9d9", alpha=1.0,
                      linewidth=0.0, antialiased=True)
    axes.plot_surface(dome_x, dome_y, dome_z, color="#d8c3a5", alpha=1.0,
                      linewidth=0.0, antialiased=True)

    base_angle = np.linspace(0.0, 2.0 * np.pi, 200)
    axes.plot(RADIUS * np.cos(base_angle), RADIUS * np.sin(base_angle),
              np.zeros_like(base_angle), color="#33414d", linewidth=1.2)
    axes.plot(RADIUS * np.cos(base_angle), RADIUS * np.sin(base_angle),
              np.full_like(base_angle, WALL_HEIGHT), color="#6b5330",
              linewidth=0.9, linestyle="--")

    axes.set_xlim(-4.0, 4.0)
    axes.set_ylim(-4.0, 4.0)
    axes.set_zlim(0.0, 14.2)
    axes.set_box_aspect((1.0, 1.0, 1.6))
    axes.set_xlabel(r"$x$", labelpad=2)
    axes.set_ylabel(r"$y$", labelpad=2)
    axes.set_zlabel(r"$z$", labelpad=8)
    axes.set_title("(a) the solid", fontsize=12.0)
    axes.view_init(elev=16, azim=-62)
    axes.grid(True, linewidth=0.4, alpha=0.4)


def draw_elevation(axes):
    """Draw the side elevation with its dimensions."""
    half = RADIUS
    axes.plot([-half, half], [0.0, 0.0], color="#33414d", linewidth=1.4)
    axes.plot([-half, -half], [0.0, WALL_HEIGHT], color="#33414d", linewidth=1.4)
    axes.plot([half, half], [0.0, WALL_HEIGHT], color="#33414d", linewidth=1.4)
    roof_angle = np.linspace(0.0, np.pi, 200)
    axes.plot(half * np.cos(roof_angle), WALL_HEIGHT + half * np.sin(roof_angle),
              color="#8a5b33", linewidth=1.4)
    axes.fill_between([-half, half], [0.0, 0.0], [WALL_HEIGHT, WALL_HEIGHT],
                      color="#dce6ef", zorder=0)
    axes.fill(np.append(half * np.cos(roof_angle), [-half, half]),
              np.append(WALL_HEIGHT + half * np.sin(roof_angle),
                        [WALL_HEIGHT, WALL_HEIGHT]),
              color="#ead9c2", zorder=0)
    axes.plot([0.0, 0.0], [0.0, WALL_HEIGHT + half], color="#8c8c8c",
              linewidth=0.8, linestyle=":")

    axes.annotate("", xy=(3.85, WALL_HEIGHT), xytext=(3.85, 0.0),
                  arrowprops={"arrowstyle": "<->", "linewidth": 0.9, "color": "#1c1c1e"})
    axes.text(4.0, WALL_HEIGHT / 2.0, r"$10$", fontsize=10, va="center")
    axes.annotate("", xy=(3.85, WALL_HEIGHT + half), xytext=(3.85, WALL_HEIGHT),
                  arrowprops={"arrowstyle": "<->", "linewidth": 0.9, "color": "#8a5b33"})
    axes.text(4.0, WALL_HEIGHT + half / 2.0, r"$3$", fontsize=10, va="center",
              color="#8a5b33")
    axes.annotate("", xy=(half, -0.9), xytext=(0.0, -0.9),
                  arrowprops={"arrowstyle": "<->", "linewidth": 0.9, "color": "#1c1c1e"})
    axes.text(half / 2.0, -1.55, r"$3$", fontsize=10, ha="center")

    axes.set_xlim(-4.6, 5.2)
    axes.set_ylim(-2.2, 14.2)
    axes.set_aspect("equal")
    axes.set_xlabel(r"$x$")
    axes.set_ylabel(r"$z$")
    axes.set_title("(b) side elevation with dimensions", fontsize=12.0)
    axes.grid(True, linewidth=0.4, alpha=0.35)


def main():
    """Render the two panels and write the two output files."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.7,
            "font.size": 12.5,
            "axes.titlesize": 12.5,
            "axes.labelsize": 12.0,
            "xtick.labelsize": 11.0,
            "ytick.labelsize": 11.0,
        }
    )

    figure = plt.figure(figsize=(8.0, 4.2))
    grid = figure.add_gridspec(1, 2, width_ratios=[1.02, 1.0], wspace=0.18)
    solid_axes = figure.add_subplot(grid[0, 0], projection="3d")
    elevation_axes = figure.add_subplot(grid[0, 1])

    draw_solid(solid_axes)
    draw_elevation(elevation_axes)

    figure.suptitle("A silo: cylinder $r = 3$, height $10$, with a hemispherical roof",
                    fontsize=12.5, y=0.975)
    figure.subplots_adjust(left=0.015, right=0.995, top=0.80, bottom=0.13, wspace=0.16)
    output = Path(__file__).with_name(FIGURE_NAME + ".png")
    figure.savefig(output, dpi=170)
    plt.close(figure)

    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    Path(__file__).with_name(FIGURE_NAME + ".b64.txt").write_text(encoded, encoding="ascii")
    print(f"saved {output.name} and {FIGURE_NAME}.b64.txt ({len(encoded)} base64 characters)")


if __name__ == "__main__":
    main()