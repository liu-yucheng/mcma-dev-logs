"""Draw the sphere, the cylinder r = cos(theta), and their intersection.

The unit sphere and the cylinder are drawn together, and the two closed curves
where they meet are drawn in dark red. The script writes the PNG and its Base64
copy.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part1_figure1"


def main():
    """Render the two surfaces and their intersection."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.7,
            "font.size": 11.5,
        }
    )

    figure = plt.figure(figsize=(7.0, 5.9))
    axes = figure.add_subplot(111, projection="3d")

    azimuth = np.linspace(0.0, 2.0 * np.pi, 150)
    polar = np.linspace(0.0, np.pi, 90)
    grid_azimuth, grid_polar = np.meshgrid(azimuth, polar)
    sphere_x = np.sin(grid_polar) * np.cos(grid_azimuth)
    sphere_y = np.sin(grid_polar) * np.sin(grid_azimuth)
    sphere_z = np.cos(grid_polar)

    axes.plot_surface(sphere_x, sphere_y, sphere_z, color="#7fa8cc", alpha=0.30,
                      linewidth=0.0, antialiased=True, shade=False)

    angle = np.linspace(0.0, 2.0 * np.pi, 150)
    height = np.linspace(-1.0, 1.0, 40)
    grid_angle, grid_height = np.meshgrid(angle, height)
    cylinder_x = 0.5 + 0.5 * np.cos(grid_angle)
    cylinder_y = 0.5 * np.sin(grid_angle)

    axes.plot_surface(cylinder_x, cylinder_y, grid_height, color="#7fae7a", alpha=0.42,
                      linewidth=0.0, antialiased=True, shade=False)

    for sign in (1.0, -1.0):
        axes.plot(0.5 + 0.5 * np.cos(angle), 0.5 * np.sin(angle),
                  sign * np.abs(np.sin(angle / 2.0)), color="#8a1c1c", linewidth=2.0)


    axes.set_xlim(-1.1, 1.1)
    axes.set_ylim(-1.1, 1.1)
    axes.set_zlim(-1.1, 1.1)
    axes.set_box_aspect((1.0, 1.0, 1.0))
    axes.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    axes.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    axes.set_zticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    axes.tick_params(labelsize=9.5)
    axes.set_xlabel(r"$x$", labelpad=3)
    axes.set_ylabel(r"$y$", labelpad=3)
    axes.set_zlabel(r"$z$", labelpad=5)
    axes.set_title("The sphere $x^{2}+y^{2}+z^{2}=a^{2}$ and the cylinder "
                   "$x^{2}+y^{2}=ax$", fontsize=11.5)
    axes.view_init(elev=20, azim=-56)
    axes.grid(True, linewidth=0.4, alpha=0.4)

    figure.tight_layout()
    output = Path(__file__).with_name(FIGURE_NAME + ".png")
    figure.savefig(output, dpi=170)
    plt.close(figure)

    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    Path(__file__).with_name(FIGURE_NAME + ".b64.txt").write_text(encoded, encoding="ascii")
    print(f"saved {output.name} and {FIGURE_NAME}.b64.txt ({len(encoded)} base64 characters)")


if __name__ == "__main__":
    main()