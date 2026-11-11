"""Draw the bumpy sphere rho = 1 + sin(6 theta) sin(5 phi) / 5.

The surface is colored by its distance from the origin, so the six bumps on the
equator and the five rings of bumps are easy to see.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize

FIGURE_NAME = "part1_figure1"


def main():
    """Render the bumpy surface and write the two output files."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 11.0,
        }
    )

    azimuth = np.linspace(0.0, 2.0 * np.pi, 361)
    polar = np.linspace(0.0, np.pi, 241)
    grid_azimuth, grid_polar = np.meshgrid(azimuth, polar)
    radius = 1.0 + 0.2 * np.sin(6.0 * grid_azimuth) * np.sin(5.0 * grid_polar)

    surface_x = radius * np.sin(grid_polar) * np.cos(grid_azimuth)
    surface_y = radius * np.sin(grid_polar) * np.sin(grid_azimuth)
    surface_z = radius * np.cos(grid_polar)

    figure = plt.figure(figsize=(6.6, 5.9))
    axes = figure.add_subplot(111, projection="3d")
    norm = Normalize(vmin=float(radius.min()), vmax=float(radius.max()))
    colors = cm.viridis(norm(radius))[..., :3] * 0.55 + 0.45

    axes.plot_surface(surface_x, surface_y, surface_z, facecolors=colors,
                      linewidth=0.0, antialiased=True, shade=False, rstride=2, cstride=2)


    axes.set_xlim(-1.3, 1.3)
    axes.set_ylim(-1.3, 1.3)
    axes.set_zlim(-1.3, 1.3)
    axes.set_box_aspect((1.0, 1.0, 1.0))
    axes.set_xticks([-1.0, 0.0, 1.0])
    axes.set_yticks([-1.0, 0.0, 1.0])
    axes.set_zticks([-1.0, 0.0, 1.0])
    axes.tick_params(labelsize=9.0)
    axes.set_xlabel(r"$x$", labelpad=2)
    axes.set_ylabel(r"$y$", labelpad=2)
    axes.set_zlabel(r"$z$", labelpad=4)
    axes.set_title("The bumpy sphere $\\rho = 1 + \\frac{1}{5}\\sin 6\\theta\\,\\sin 5\\phi$",
                   fontsize=11.0)
    axes.view_init(elev=18, azim=-58)

    figure.tight_layout()
    output = Path(__file__).with_name(FIGURE_NAME + ".png")
    figure.savefig(output, dpi=170)
    plt.close(figure)

    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    Path(__file__).with_name(FIGURE_NAME + ".b64.txt").write_text(encoded, encoding="ascii")
    print(f"saved {output.name} and {FIGURE_NAME}.b64.txt ({len(encoded)} base64 characters)")


if __name__ == "__main__":
    main()