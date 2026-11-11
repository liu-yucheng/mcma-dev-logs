"""Draw the solid enclosed by the two paraboloids z = r^2 and z = 5 - r^2.

The picture shows the lower bowl, the upper bowl, and the circle where the two
surfaces meet. The script saves the PNG and its Base64 copy.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part1_figure1"


def main():
    """Render the closed solid and write the two output files."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.7,
        }
    )

    rim = np.sqrt(5.0 / 2.0)
    radius = np.linspace(0.0, rim, 90)
    angle = np.linspace(0.0, 2.0 * np.pi, 160)
    grid_radius, grid_angle = np.meshgrid(radius, angle)
    grid_x = grid_radius * np.cos(grid_angle)
    grid_y = grid_radius * np.sin(grid_angle)

    figure = plt.figure(figsize=(7.4, 5.8))
    axes = figure.add_subplot(111, projection="3d")

    axes.plot_surface(
        grid_x, grid_y, grid_radius**2,
        color="#3f6fa8", alpha=0.80, linewidth=0.0, antialiased=True,
    )
    axes.plot_surface(
        grid_x, grid_y, 5.0 - grid_radius**2,
        color="#c0703f", alpha=0.80, linewidth=0.0, antialiased=True,
    )

    rim_angle = np.linspace(0.0, 2.0 * np.pi, 400)
    axes.plot(
        rim * np.cos(rim_angle), rim * np.sin(rim_angle),
        np.full_like(rim_angle, 2.5), color="#1c1c1e", linewidth=1.5,
        linestyle="--",
    )

    axes.plot([0.0, 0.0], [0.0, 0.0], [0.0, 5.0], color="#1c1c1e", linewidth=0.9)
    axes.text(0.05, 0.05, 5.15, r"$z = 5$", fontsize=9.5)

    axes.text(1.72, 0.55, 2.72, r"rim $z = 2.5$", fontsize=9.0, ha="left")
    axes.text(1.05, -1.62, 0.45, r"$z = x^2 + y^2$", fontsize=9.5, ha="left")
    axes.text(-1.92, 1.30, 4.55, r"$z = 5 - x^2 - y^2$", fontsize=9.5, ha="left")

    limits = 1.95
    axes.set_xlim(-limits, limits)
    axes.set_ylim(-limits, limits)
    axes.set_zlim(0.0, 5.4)
    axes.set_box_aspect((2.0, 2.0, 1.45))
    axes.set_xlabel(r"$x$", labelpad=4)
    axes.set_ylabel(r"$y$", labelpad=4)
    axes.set_zlabel(r"$z$", labelpad=6)
    axes.set_title("The solid between $z = x^{2} + y^{2}$ and $z = 5 - x^{2} - y^{2}$",
                   fontsize=11)
    axes.view_init(elev=22, azim=-58)
    axes.grid(True, linewidth=0.4, alpha=0.5)

    figure.tight_layout()
    output = Path(__file__).with_name(FIGURE_NAME + ".png")
    figure.savefig(output, dpi=170)
    plt.close(figure)

    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    Path(__file__).with_name(FIGURE_NAME + ".b64.txt").write_text(encoded, encoding="ascii")
    print(f"saved {output.name} and {FIGURE_NAME}.b64.txt ({len(encoded)} base64 characters)")


if __name__ == "__main__":
    main()