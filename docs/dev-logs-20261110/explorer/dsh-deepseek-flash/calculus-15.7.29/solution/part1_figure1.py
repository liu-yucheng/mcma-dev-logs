"""Draw the elliptic paraboloid cap y = 4 - x^2 - 4z^2 above the plane y = 0.

The surface, the base, one horizontal cross-section, and one fibre in the y-direction are
drawn in one 3-D view.  The script writes part1_figure1.png and part1_figure1.b64.txt.

Usage:
    python part1_figure1.py
"""

import base64
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "stix",
    "axes.labelsize": 13,
    "font.size": 11,
})


def save(figure: plt.Figure, name: str) -> None:
    """Write the PNG file and its Base64 sidecar file.

    Args:
        figure: The matplotlib figure to save.
        name: The file name without extension.
    """
    png = Path(name + ".png")
    figure.savefig(png, dpi=170, bbox_inches="tight")
    text = base64.b64encode(png.read_bytes()).decode("ascii")
    Path(name + ".b64.txt").write_text(text, encoding="ascii")
    print(f"{png}: {png.stat().st_size} bytes, base64 length {len(text)}")


def main() -> None:
    """Build the figure and save it."""
    theta = np.linspace(0.0, 2.0 * np.pi, 160)
    radial = np.linspace(0.0, 1.0, 70)
    radius, angle = np.meshgrid(radial, theta)
    x_surface = 2.0 * radius * np.cos(angle)
    z_surface = radius * np.sin(angle)
    y_surface = 4.0 * (1.0 - radius**2)

    figure = plt.figure(figsize=(7.6, 6.2))
    axes = figure.add_subplot(111, projection="3d")

    axes.plot_surface(x_surface, z_surface, y_surface, color="#9dc3d4", alpha=0.30,
                      rstride=2, cstride=2, linewidth=0.20, edgecolor="0.52", antialiased=True)
    axes.plot_surface(x_surface, z_surface, np.zeros_like(y_surface), color="#c9cfd8", alpha=0.85,
                      linewidth=0, antialiased=True)

    half = np.sqrt(2.0)
    slice_x = half * np.cos(theta)
    slice_z = 0.5 * half * np.sin(theta)
    axes.plot_surface(np.array([slice_x]), np.array([slice_z]), np.full((1, theta.size), 2.0),
                      color="#f3c88b", alpha=0.55, linewidth=0, antialiased=True)

    axes.plot(2.0 * np.cos(theta), np.sin(theta), np.zeros_like(theta), color="#22303c", linewidth=2.0)
    axes.plot(slice_x, slice_z, np.full_like(theta, 2.0), color="#b9770e", linewidth=2.4)

    axes.plot([0.6, 0.6], [0.4, 0.4], [0.0, 3.0], color="#a93226", linestyle="-", linewidth=2.6)
    axes.scatter([0.6], [0.4], [0.0], color="#a93226", s=30, depthshade=False)
    axes.scatter([0.6], [0.4], [3.0], color="#a93226", s=30, depthshade=False)

    axes.set_xlabel(r"$x$", labelpad=6)
    axes.set_ylabel(r"$z$", labelpad=6)
    axes.set_zlabel(r"$y$", labelpad=8)
    axes.set_xlim(-2.4, 2.4)
    axes.set_ylim(-1.5, 1.5)
    axes.set_zlim(0.0, 4.6)
    axes.set_xticks([-2, -1, 0, 1, 2])
    axes.set_yticks([-1, 0, 1])
    axes.set_zticks([0, 1, 2, 3, 4])
    axes.view_init(elev=19, azim=-62)
    axes.set_box_aspect((1.50, 0.98, 0.92))

    handles = [
        Patch(facecolor="#9dc3d4", alpha=0.45, label=r"$y = 4 - x^{2} - 4z^{2}$"),
        Patch(facecolor="#c9cfd8", alpha=0.95, label=r"base $y = 0$"),
        Line2D([], [], color="#22303c", linewidth=2.0, label=r"rim $x^{2} + 4z^{2} = 4$"),
        Patch(facecolor="#f3c88b", alpha=0.85, label=r"slice $y = 2$"),
        Line2D([], [], color="#a93226", linewidth=2.6, label="fibre in $y$"),
    ]
    axes.legend(handles=handles, loc="upper left", fontsize=9, framealpha=0.93)

    axes.set_title(r"$y = 4 - x^{2} - 4z^{2}$ above $x^{2} + 4z^{2} \leq 4$", fontsize=12.5, pad=4)

    save(figure, "part1_figure1")
    plt.close(figure)


if __name__ == "__main__":
    main()
