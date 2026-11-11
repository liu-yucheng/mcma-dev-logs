"""Draw the solid described by 0 <= x <= 4 - y**2, 0 <= z <= 2 - y, 0 <= y <= 2."""

import base64

import matplotlib
import numpy as np
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the 3d projection)
from matplotlib.lines import Line2D

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

figure = plt.figure(figsize=(7.0, 5.4))
axes = figure.add_subplot(111, projection="3d")
axes.set_proj_type("ortho")

# Curved face: the parabolic cylinder x = 4 - y**2 between z = 0 and z = 2 - y.
height_values = np.linspace(0.0, 2.0, 70)
depth_values = np.linspace(0.0, 1.0, 40)
height_grid, depth_grid = np.meshgrid(height_values, depth_values)
curved_x = 4.0 - height_grid**2
curved_z = depth_grid * (2.0 - height_grid)
axes.plot_surface(
    curved_x, height_grid, curved_z,
    color="#4a7fb5", linewidth=0.25, edgecolor=(0.16, 0.28, 0.42, 0.35),
    alpha=0.55, rstride=2, cstride=2, antialiased=True,
)

# Top face: the plane z = 2 - y over the same footprint.
stretch_values = np.linspace(0.0, 1.0, 40)
stretch_grid, height_grid = np.meshgrid(stretch_values, height_values)
top_x = stretch_grid * (4.0 - height_grid**2)
axes.plot_surface(top_x, height_grid, 2.0 - height_grid, color="#d9c49a", alpha=0.5,
                  linewidth=0.0, shade=False)

# Bottom face: the plane z = 0.
axes.plot_surface(top_x, height_grid, np.zeros_like(top_x), color="#a9bccd", alpha=0.35,
                  linewidth=0.0, shade=False)

# Back face: the plane x = 0, a triangle in the yz-plane.
axes.plot_trisurf(
    np.zeros(3), np.array([0.0, 0.0, 2.0]), np.array([0.0, 2.0, 0.0]),
    triangles=[[0, 1, 2]], color="#8fae8b", alpha=0.45, linewidth=0.0, shade=False,
)

# Front face: the rectangle y = 0, 0 <= x <= 4, 0 <= z <= 2.
axes.plot_trisurf(
    np.array([0.0, 4.0, 4.0, 0.0]), np.zeros(4), np.array([0.0, 0.0, 2.0, 2.0]),
    triangles=[[0, 1, 2], [0, 2, 3]], color="#c9b9a6", alpha=0.22, linewidth=0.0,
    shade=False,
)

# Boundary curves: the two parabola rims and the back edge.
parabola_y = np.linspace(0.0, 2.0, 200)
axes.plot(4.0 - parabola_y**2, parabola_y, np.zeros_like(parabola_y),
          color="#2c4a6b", linewidth=1.6)
axes.plot(4.0 - parabola_y**2, parabola_y, 2.0 - parabola_y, color="#8a6d3b", linewidth=1.6)
axes.plot(np.zeros_like(parabola_y), parabola_y, 2.0 - parabola_y,
          color="#4f6b4a", linewidth=1.4)
axes.plot(np.zeros_like(parabola_y), parabola_y, np.zeros_like(parabola_y),
          color="#4f6b4a", linewidth=1.1, linestyle="--")
axes.plot([4.0, 0.0], [0.0, 2.0], [0.0, 0.0], color="#2c4a6b", linewidth=1.0, linestyle="--")

# One representative fibre in the x-direction at y = 1.4, z = 0.3.
axes.plot([0.0, 4.0 - 1.4**2], [1.4, 1.4], [0.3, 0.3], color="#8a1c1c", linewidth=2.0,
          linestyle=(0, (4, 2)), marker="o", markersize=3.5, markerfacecolor="#8a1c1c")

axes.set_xlabel(r"$x$", labelpad=7)
axes.set_ylabel(r"$y$", labelpad=7)
axes.set_zlabel(r"$z$", labelpad=7)
axes.set_xlim(0.0, 4.4)
axes.set_ylim(0.0, 2.2)
axes.set_zlim(0.0, 2.15)
axes.set_xticks([0, 1, 2, 3, 4])
axes.set_yticks([0, 1, 2])
axes.set_zticks([0, 1, 2])
axes.set_box_aspect((1.8, 1.0, 0.95))
axes.view_init(elev=22, azim=32)

handles = [
    Patch(facecolor="#4a7fb5", edgecolor="#2c4a6b", alpha=0.7, label=r"$x = 4 - y^{2}$"),
    Patch(facecolor="#d9c49a", edgecolor="#8a6d3b", alpha=0.8, label=r"$z = 2 - y$"),
    Patch(facecolor="#a9bccd", edgecolor="#38546b", alpha=0.8, label=r"$z = 0$"),
    Patch(facecolor="#8fae8b", edgecolor="#3d5a37", alpha=0.8, label=r"$x = 0$"),
    Line2D([0], [0], color="#8a1c1c", linewidth=1.8, linestyle=(0, (4, 2)),
           label=r"typical fibre in $x$"),
]
axes.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize=9,
            framealpha=0.92)
axes.set_title(r"The solid $E$ and one fibre in the $x$-direction", pad=8)

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")