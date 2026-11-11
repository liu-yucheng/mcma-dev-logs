"""Draw the solid bounded by x = 4*y**2 + 4*z**2 and x = 4.

The figure shows the parabolic bowl, the cutting plane x = 4, the circular
projection on the yz-plane, and one representative vertical fibre.
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

figure = plt.figure(figsize=(7.0, 5.4))
axes = figure.add_subplot(111, projection="3d")

radial_values = np.linspace(0.0, 1.0, 60)
angle_values = np.linspace(0.0, 2.0 * np.pi, 120)
radius_grid, angle_grid = np.meshgrid(radial_values, angle_values)
x_surface = 4.0 * radius_grid**2
y_surface = radius_grid * np.cos(angle_grid)
z_surface = radius_grid * np.sin(angle_grid)

surface = axes.plot_surface(
    x_surface, y_surface, z_surface,
    cmap=cm.YlGnBu_r, linewidth=0.2, edgecolor=(0.25, 0.3, 0.35, 0.25),
    alpha=0.85, rstride=2, cstride=2, antialiased=True,
)

# Cutting plane x = 4, drawn as the disk y**2 + z**2 <= 1.
disk_radius = np.linspace(0.0, 1.0, 30)
disk_angle = np.linspace(0.0, 2.0 * np.pi, 100)
disk_r, disk_t = np.meshgrid(disk_radius, disk_angle)
axes.plot_surface(
    np.full_like(disk_r, 4.0), disk_r * np.cos(disk_t), disk_r * np.sin(disk_t),
    color="#d8cdb8", alpha=0.55, linewidth=0.0, shade=False,
)
axes.plot(np.full(200, 4.0), np.cos(np.linspace(0, 2 * np.pi, 200)),
          np.sin(np.linspace(0, 2 * np.pi, 200)), color="#8a6d3b", linewidth=1.4)

# Circular projection on the plane x = 0, drawn as a translucent disk.
axes.plot_surface(
    np.zeros_like(disk_r), disk_r * np.cos(disk_t), disk_r * np.sin(disk_t),
    color="#9fb6cc", alpha=0.32, linewidth=0.0, shade=False,
)
axes.plot(np.zeros(200), np.cos(np.linspace(0, 2 * np.pi, 200)),
          np.sin(np.linspace(0, 2 * np.pi, 200)), color="#4d6a8a", linewidth=1.1,
          linestyle="--")


axes.text(1.2, 0.0, -1.45, r"$x = 4y^2 + 4z^2$", color="#1f3d5c", fontsize=11)
axes.text(4.15, 0.55, 0.95, r"$x = 4$", color="#6b5222", fontsize=11)

axes.set_xlabel(r"$x$", labelpad=6)
axes.set_ylabel(r"$y$", labelpad=6)
axes.set_zlabel(r"$z$", labelpad=6)
axes.set_xlim(0.0, 5.0)
axes.set_ylim(-1.3, 1.3)
axes.set_zlim(-1.3, 1.3)
axes.set_box_aspect((1.35, 1.0, 1.0))
axes.view_init(elev=20, azim=-62)
axes.set_title(r"The solid $E$: $4y^2 + 4z^2 \leq x \leq 4$", pad=12)

color_bar = figure.colorbar(surface, ax=axes, shrink=0.62, pad=0.08)
color_bar.set_label(r"$x$")

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")