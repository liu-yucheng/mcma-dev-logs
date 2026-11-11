"""Draw the ellipsoid x**2 + 2*y**2 + 3*z**2 = 1 with its three semi-axes.

The surface is the boundary of the region that maximizes the integral. The
principal ellipses lie in the three coordinate planes, and the labelled points
are the intercepts with the coordinate axes.
"""

import base64

import matplotlib
import numpy as np
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

semi_axis_x = 1.0
semi_axis_y = 1.0 / np.sqrt(2.0)
semi_axis_z = 1.0 / np.sqrt(3.0)

figure = plt.figure(figsize=(7.0, 5.6))
axes = figure.add_subplot(111, projection="3d")

polar_values = np.linspace(0.0, np.pi, 90)
azimuth_values = np.linspace(0.0, 2.0 * np.pi, 160)
polar_grid, azimuth_grid = np.meshgrid(polar_values, azimuth_values)
x_surface = semi_axis_x * np.sin(polar_grid) * np.cos(azimuth_grid)
y_surface = semi_axis_y * np.sin(polar_grid) * np.sin(azimuth_grid)
z_surface = semi_axis_z * np.cos(polar_grid)

axes.plot_surface(
    x_surface, y_surface, z_surface,
    color="#7fa8c9", linewidth=0.2, edgecolor=(0.12, 0.22, 0.32, 0.18),
    alpha=0.55, rstride=3, cstride=3, antialiased=True, shade=True,
)

# Principal ellipses in the three coordinate planes.
angle = np.linspace(0.0, 2.0 * np.pi, 300)
axes.plot(semi_axis_x * np.cos(angle), semi_axis_y * np.sin(angle), np.zeros_like(angle),
          color="#1f3d5c", linewidth=1.6)
axes.plot(semi_axis_x * np.cos(angle), np.zeros_like(angle), semi_axis_z * np.sin(angle),
          color="#1f3d5c", linewidth=1.6)
axes.plot(np.zeros_like(angle), semi_axis_y * np.cos(angle), semi_axis_z * np.sin(angle),
          color="#1f3d5c", linewidth=1.6)

# Intercepts with the coordinate axes.
intercepts = [
    (semi_axis_x, 0.0, 0.0, 1.12, 0.0, 0.0, r"$a = 1.000$"),
    (0.0, semi_axis_y, 0.0, 0.0, 0.88, 0.0, r"$b = 0.707$"),
    (0.0, 0.0, semi_axis_z, 0.0, 0.0, 0.73, r"$c = 0.577$"),
]
label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 1.5}
for point_x, point_y, point_z, text_x, text_y, text_z, label in intercepts:
    axes.scatter([point_x], [point_y], [point_z], color="#8a1c1c", s=20, depthshade=False)
    axes.text(text_x, text_y, text_z, label, fontsize=10, color="#8a1c1c",
              ha="left", va="center", zorder=20, bbox=label_box)

axes.set_xlabel(r"$x$", labelpad=6)
axes.set_ylabel(r"$y$", labelpad=6)
axes.set_zlabel(r"$z$", labelpad=4)
axes.set_xlim(-1.1, 1.2)
axes.set_ylim(-0.85, 0.85)
axes.set_zlim(-0.7, 0.7)
axes.set_box_aspect((semi_axis_x, semi_axis_y, semi_axis_z))
axes.view_init(elev=22, azim=-64)
axes.set_title(r"The ellipsoid $x^{2} + 2y^{2} + 3z^{2} = 1$", pad=12)

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
