"""Draw the solid of Exercise 15.7.31 in three dimensions.

The figure shows the parabolic wall y = x**2, the floor z = 0, and the
slanted top plane y + 2*z = 4. The viewpoint looks into the open end at
x = -2, so the floor and the wall are both visible under the plane. The
script writes part1_figure1.png and its Base64 copy.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.labelsize": 12,
})

OUT = Path(__file__).resolve().parent


def main():
    """Draw the three boundary surfaces and save the figure."""
    span = np.linspace(-2.0, 2.0, 81)
    depth = np.linspace(0.0, 1.0, 61)
    grid_x, grid_s = np.meshgrid(span, depth)

    wall_y = grid_x**2
    wall_z = grid_s * (2.0 - grid_x**2 / 2.0)

    region_y = grid_x**2 + grid_s * (4.0 - grid_x**2)
    floor_z = np.zeros_like(region_y)
    top_z = 2.0 - region_y / 2.0

    fig = plt.figure(figsize=(8.4, 7.8))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(grid_x, wall_y, wall_z, color="#6fa8c8", alpha=1.0,
                    linewidth=0.3, edgecolor="#2f6285", rcount=13, ccount=21,
                    shade=False)
    ax.plot_surface(grid_x, region_y, floor_z, color="#c6d2d8", alpha=1.0,
                    linewidth=0, rcount=18, ccount=30, shade=False)
    ax.plot_surface(grid_x, region_y, top_z, color="#dfb47c", alpha=0.72,
                    linewidth=0.2, edgecolor="#b08347", rcount=18, ccount=30,
                    shade=False)

    span_curve = np.linspace(-2.0, 2.0, 201)
    ax.plot(span_curve, span_curve**2, np.zeros_like(span_curve), color="#0d2c42", lw=1.8)
    ax.plot([-2.0, 2.0], [4.0, 4.0], [0.0, 0.0], color="#101010", lw=1.8, ls="--")

    ax.set_xlabel(r"$x$", labelpad=10)
    ax.set_ylabel(r"$y$", labelpad=10)
    ax.set_zlabel(r"$z$", labelpad=8)
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(0.0, 4.4)
    ax.set_zlim(0.0, 2.25)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_zticks([0, 1, 2])
    ax.view_init(elev=30, azim=168)
    ax.set_box_aspect((1.05, 1.2, 0.8), zoom=1.12)
    ax.set_title(r"The solid $E$: $y\geq x^{2}$, $z\geq 0$, $y+2z\leq 4$", pad=2,
                 fontsize=13)

    handles = [
        Patch(facecolor="#dfb47c", edgecolor="#b08347", label=r"top plane $y+2z=4$"),
        Patch(facecolor="#6fa8c8", edgecolor="#2f6285", label=r"wall $y=x^{2}$"),
        Patch(facecolor="#c8d4da", edgecolor="#96a7b0", label=r"floor $z=0$"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
               fontsize=10.5, bbox_to_anchor=(0.5, 0.015))

    png_path = OUT / "part1_figure1.png"
    fig.savefig(png_path, dpi=170, bbox_inches="tight", facecolor="white")
    payload = write_base64(png_path)
    print(png_path)
    print(f"base64 length {len(payload)}")
    plt.close(fig)


def write_base64(path):
    """Write the Base64 text of the image and return it."""
    text = base64.b64encode(path.read_bytes()).decode("ascii")
    path.with_suffix(".b64.txt").write_text(text, encoding="ascii")
    return text


if __name__ == "__main__":
    main()