"""Draw the paraboloid cap and its circular shadow on the plane z = 0.

The figure shows the surface z = 1 - x**2 - y**2 over the unit disk, the floor
z = 0, and the rim where the paraboloid meets the floor.
"""

import base64

import matplotlib
import numpy as np
from matplotlib import cm
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

figure = plt.figure(figsize=(7.0, 5.6))
axes = figure.add_subplot(111, projection="3d")

radial_values = np.linspace(0.0, 1.0, 70)
angle_values = np.linspace(0.0, 2.0 * np.pi, 160)
radius_grid, angle_grid = np.meshgrid(radial_values, angle_values)
x_surface = radius_grid * np.cos(angle_grid)
y_surface = radius_grid * np.sin(angle_grid)
z_surface = 1.0 - radius_grid**2

surface = axes.plot_surface(
    x_surface, y_surface, z_surface,
    cmap=cm.viridis, linewidth=0.15, edgecolor=(0.15, 0.2, 0.25, 0.22),
    alpha=0.92, rstride=2, cstride=2, antialiased=True,
)

# Floor of the solid, the unit disk in the plane z = 0.
disk_radius = np.linspace(0.0, 1.0, 26)
disk_angle = np.linspace(0.0, 2.0 * np.pi, 120)
disk_r, disk_t = np.meshgrid(disk_radius, disk_angle)
axes.plot_surface(
    disk_r * np.cos(disk_t), disk_r * np.sin(disk_t), np.zeros_like(disk_r),
    color="#d8cdb8", alpha=0.6, linewidth=0.0, shade=False,
)

# Rim of the projection, the circle x**2 + y**2 = 1 at z = 0.
rim_angle = np.linspace(0.0, 2.0 * np.pi, 240)
axes.plot(np.cos(rim_angle), np.sin(rim_angle), np.zeros_like(rim_angle),
          color="#8a6d3b", linewidth=1.6)

axes.set_xlabel(r"$x$", labelpad=6)
axes.set_ylabel(r"$y$", labelpad=6)
axes.set_zlabel(r"$z$", labelpad=4)
axes.set_xlim(-1.15, 1.15)
axes.set_ylim(-1.15, 1.15)
axes.set_zlim(0.0, 1.2)
axes.set_box_aspect((1.0, 1.0, 0.95))
axes.view_init(elev=26, azim=-58)
axes.set_title(r"The solid $E$: $0 \leq z \leq 1 - x^{2} - y^{2}$", pad=12)

color_bar = figure.colorbar(surface, ax=axes, shrink=0.6, pad=0.09)
color_bar.set_label(r"$z$")

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
