"""Draw the solid of Exercise 15.7.49 as a see-through surface sketch.

The solid is the part of the quarter cylinder x**2 + y**2 <= 1 that lies between
the planes z = 0 and z = y. The base z = 0 is filled. The slanted top z = y is
drawn as a ruled grid, the curved wall x**2 + y**2 = 1 as vertical ribs, and one
red segment marks a typical range 0 <= z <= y.
"""

from base64 import b64encode
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import pyplot as plt


def main():
    """Draw the solid of Exercise 15.7.49 and save the figure with its Base64 text."""
    matplotlib.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "mathtext.fontset": "stix",
        "figure.dpi": 170,
    })

    figure = plt.figure(figsize=(7.4, 6.6), dpi=170)
    axes = figure.add_subplot(projection="3d")

    angle = np.linspace(0.0, np.pi / 2, 240)

    angle_grid, radial_grid = np.meshgrid(angle, np.linspace(0.0, 1.0, 80))
    disc_x = radial_grid * np.cos(angle_grid)
    disc_y = radial_grid * np.sin(angle_grid)
    axes.plot_surface(disc_x, disc_y, np.zeros_like(disc_x), color="#b3c69c", alpha=1.0,
                      linewidth=0.0, shade=False)

    for radius in np.linspace(0.25, 0.75, 3):
        axes.plot(radius * np.cos(angle), radius * np.sin(angle), np.zeros_like(angle),
                  color="#7d9163", linewidth=0.7, alpha=0.75)
    for ray_angle in np.linspace(0.0, np.pi / 2, 7):
        axes.plot([0.0, np.cos(ray_angle)], [0.0, np.sin(ray_angle)], [0.0, 0.0],
                  color="#7d9163", linewidth=0.7, alpha=0.75)

    for fraction in np.linspace(0.2, 0.92, 5):
        axes.plot(fraction * np.cos(angle), fraction * np.sin(angle), fraction * np.sin(angle),
                  color="#b4702c", linewidth=1.0)
    for ray_angle in np.linspace(0.0, np.pi / 2, 9):
        axes.plot([0.0, np.cos(ray_angle)], [0.0, np.sin(ray_angle)],
                  [0.0, np.sin(ray_angle)], color="#b4702c", linewidth=1.0)

    for ray_angle in np.linspace(0.0, np.pi / 2, 9):
        axes.plot([np.cos(ray_angle), np.cos(ray_angle)],
                  [np.sin(ray_angle), np.sin(ray_angle)],
                  [0.0, np.sin(ray_angle)], color="#7f97b3", linewidth=1.0)

    axes.plot(np.cos(angle), np.sin(angle), np.sin(angle), color="#1f3752", linewidth=1.8)
    axes.plot(np.cos(angle), np.sin(angle), np.zeros_like(angle), color="#1f3752", linewidth=1.8)
    axes.plot(np.zeros_like(angle), np.sin(angle), np.sin(angle), color="#8a5a28", linewidth=1.6)
    axes.plot(np.linspace(0.0, 1.0, 2), np.zeros(2), np.zeros(2), color="#1f3752", linewidth=1.6)
    axes.plot(np.zeros(2), np.linspace(0.0, 1.0, 2), np.zeros(2), color="#1f3752", linewidth=1.6)
    axes.plot(np.zeros(2), np.linspace(0.0, 1.0, 2), np.linspace(0.0, 1.0, 2),
              color="#8a5a28", linewidth=1.6)

    sample_x, sample_y = 0.40, 0.58
    axes.plot([sample_x, sample_x], [sample_y, sample_y], [0.0, sample_y],
              color="#a4231f", linewidth=3.0, solid_capstyle="round")
    axes.scatter([sample_x], [sample_y], [0.0], color="#a4231f", s=26, depthshade=False)
    axes.scatter([sample_x], [sample_y], [sample_y], color="#a4231f", s=26, depthshade=False)

    axes.text(-0.10, 0.74, 0.80, r"$z = y$", color="#8a4b14", fontsize=17, ha="right")
    axes.text(1.00, 0.30, 0.66, r"$x^2 + y^2 = 1$", color="#2f4b68", fontsize=15)
    axes.text(0.05, 0.74, 0.36, r"$0 \leq z \leq y$", color="#a4231f", fontsize=14)

    axes.set_xlabel(r"$x$", fontsize=15, labelpad=8)
    axes.set_ylabel(r"$y$", fontsize=15, labelpad=8)
    axes.set_zlabel(r"$z$", fontsize=15, labelpad=8)
    axes.set_xlim(0.0, 1.08)
    axes.set_ylim(0.0, 1.08)
    axes.set_zlim(0.0, 1.08)
    axes.set_box_aspect((1.0, 1.0, 1.0))
    axes.view_init(elev=26, azim=-60)
    axes.set_xticks([0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 0.5, 1.0])
    axes.set_zticks([0.0, 0.5, 1.0])
    axes.tick_params(labelsize=11)
    axes.grid(True)

    figure.tight_layout()
    output_path = Path(__file__).with_name("part1_figure1.png")
    figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
    print(output_path.resolve())

    encoded = b64encode(output_path.read_bytes()).decode("ascii")
    text_path = output_path.with_name("part1_figure1.b64.txt")
    text_path.write_text(encoded, encoding="ascii")
    print(text_path.resolve())
    print(f"base64 length: {len(encoded)}")


if __name__ == "__main__":
    main()
