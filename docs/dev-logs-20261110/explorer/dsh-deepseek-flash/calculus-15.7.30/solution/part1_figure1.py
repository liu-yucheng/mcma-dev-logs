"""Draw the cylinder y**2 + z**2 = 9 between the planes x = -2 and x = 2.

The figure shows the cylindrical side, the two circular end disks, and the
x-axis that is the axis of the cylinder.
"""

import base64

import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the 3d projection)

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
})

figure = plt.figure(figsize=(7.2, 5.1))
axes = figure.add_subplot(111, projection="3d")

angle = np.linspace(0.0, 2.0 * np.pi, 160)
along = np.linspace(-2.0, 2.0, 60)
angle_grid, along_grid = np.meshgrid(angle, along)
side = axes.plot_surface(
    along_grid,
    3.0 * np.cos(angle_grid),
    3.0 * np.sin(angle_grid),
    cmap=cm.YlGnBu_r,
    alpha=0.55,
    linewidth=0.15,
    edgecolor=(0.25, 0.3, 0.35, 0.25),
    rstride=2,
    cstride=2,
    antialiased=True,
)

radial = np.linspace(0.0, 3.0, 30)
radial_grid, disk_angle = np.meshgrid(radial, angle)
for plane_x, shade in ((2.0, "#d8cdb8"), (-2.0, "#e6ded0")):
    axes.plot_surface(
        np.full_like(radial_grid, plane_x),
        radial_grid * np.cos(disk_angle),
        radial_grid * np.sin(disk_angle),
        color=shade,
        alpha=0.92,
        linewidth=0.0,
        shade=False,
    )
    axes.plot(
        np.full(200, plane_x),
        3.0 * np.cos(np.linspace(0.0, 2.0 * np.pi, 200)),
        3.0 * np.sin(np.linspace(0.0, 2.0 * np.pi, 200)),
        color="#8a6d3b",
        linewidth=1.3,
    )

axes.plot([-2.0, 2.0], [0.0, 0.0], [0.0, 0.0], color="#5d6168", linewidth=1.1, linestyle="--")

axes.set_xlabel(r"$x$", labelpad=6)
axes.set_ylabel(r"$y$", labelpad=6)
axes.set_zlabel(r"$z$", labelpad=6)
axes.set_xlim(-3.2, 3.2)
axes.set_ylim(-3.4, 3.4)
axes.set_zlim(-3.4, 3.4)
axes.set_box_aspect((1.25, 1.0, 1.0))
axes.view_init(elev=22, azim=-62)
axes.set_title(r"The solid $E$: $y^{2}+z^{2} \leq 9$, $-2 \leq x \leq 2$", pad=10)

color_bar = figure.colorbar(side, ax=axes, shrink=0.6, pad=0.09)
color_bar.set_label(r"$x$")

legend_handles = [
    Patch(facecolor="#9fb6cc", edgecolor="#4d6a8a", alpha=0.7, label=r"cylinder $y^{2}+z^{2}=9$"),
    Patch(facecolor="#d8cdb8", edgecolor="#8a6d3b", label=r"plane $x=2$"),
    Patch(facecolor="#e6ded0", edgecolor="#8a6d3b", label=r"plane $x=-2$"),
]
figure.legend(handles=legend_handles, loc="lower center", ncol=3, frameon=False, fontsize=10)
figure.tight_layout(rect=(0.0, 0.05, 1.0, 1.0))
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")