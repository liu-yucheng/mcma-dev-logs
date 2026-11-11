"""Draw the solid between the paraboloids y = r**2 and y = 8 - r**2.

The figure shows the lower bowl, the upper bowl, the circle where they meet,
the cross-section in the plane z = 0, the projection disk in the plane y = 0,
and one vertical fibre that measures the height at a fixed radius.
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
    "axes.titlesize": 12,
})

figure = plt.figure(figsize=(7.8, 6.0))
axes = figure.add_subplot(111, projection="3d")

radius_values = np.linspace(0.0, 2.0, 40)
angle_values = np.linspace(0.0, 2.0 * np.pi, 140)
radius_grid, angle_grid = np.meshgrid(radius_values, angle_values)
x_grid = radius_grid * np.cos(angle_grid)
z_grid = radius_grid * np.sin(angle_grid)

# The lower bowl y = x**2 + z**2 and the upper bowl y = 8 - x**2 - z**2.
axes.plot_surface(x_grid, z_grid, radius_grid**2, color="#e0a35c", alpha=0.72,
                  linewidth=0.0, shade=False)
axes.plot_surface(x_grid, z_grid, 8.0 - radius_grid**2, color="#6f9ec4", alpha=0.38,
                  linewidth=0.0, shade=False)

# The circle x**2 + z**2 = 4 at y = 4 where the bowls meet.
rim_angle = np.linspace(0.0, 2.0 * np.pi, 300)
axes.plot(2.0 * np.cos(rim_angle), 2.0 * np.sin(rim_angle), np.full_like(rim_angle, 4.0),
          color="#12304d", linewidth=2.0)

# Cross-sections in the plane z = 0: the profiles y = x**2 and y = 8 - x**2.
profile_x = np.linspace(-2.0, 2.0, 200)
axes.plot(profile_x, np.zeros_like(profile_x), profile_x**2, color="#9a6420", linewidth=2.0)
axes.plot(profile_x, np.zeros_like(profile_x), 8.0 - profile_x**2, color="#2c5b80",
          linewidth=2.0)

# The projection disk in the plane y = 0.
axes.plot_surface(x_grid, z_grid, np.zeros_like(x_grid), color="#cfd8e0", alpha=0.55,
                  linewidth=0.0, shade=False)
axes.plot(2.0 * np.cos(rim_angle), 2.0 * np.sin(rim_angle), np.zeros_like(rim_angle),
          color="#12304d", linewidth=1.4)

# One vertical fibre at x = 1, z = 0, from y = 1 to y = 7.
axes.plot([1.0, 1.0], [0.0, 0.0], [1.0, 7.0], color="#8a1c1c", linewidth=2.4)

axes.text(1.40, 0.55, 0.95, r"$y = x^{2}+z^{2}$", color="#8a5a1a", fontsize=10)
axes.text(1.25, 0.15, 7.45, r"$y = 8-x^{2}-z^{2}$", color="#2c5b80", fontsize=10)


axes.set_xlabel(r"$x$", labelpad=8)
axes.set_ylabel(r"$z$", labelpad=8)
axes.set_zlabel(r"$y$", labelpad=6)
axes.set_xlim(-2.4, 2.4)
axes.set_ylim(-2.4, 2.4)
axes.set_zlim(0.0, 9.0)
axes.set_xticks([-2.0, 0.0, 2.0])
axes.set_yticks([-2.0, 0.0, 2.0])
axes.set_zticks([0.0, 2.0, 4.0, 6.0, 8.0])
axes.set_box_aspect((2.0, 2.0, 3.1))
axes.view_init(elev=14, azim=-64)
axes.set_title(r"The solid between $y = x^{2}+z^{2}$ and $y = 8-x^{2}-z^{2}$", pad=8)

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
