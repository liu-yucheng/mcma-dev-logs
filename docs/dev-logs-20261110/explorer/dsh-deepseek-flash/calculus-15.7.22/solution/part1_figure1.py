"""Draw the solid enclosed by x**2 + z**2 = 4, y = -1, and y + z = 4.

The figure shows the cylindrical wall, the flat bottom disk, the oblique top face,
and the two rim curves. The wall is opaque so that the silhouette of the solid is clear.
"""

import base64

import matplotlib
import numpy as np
from matplotlib.patches import Patch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "axes.labelsize": 12,
})

figure = plt.figure(figsize=(7.4, 5.4))
axes = figure.add_axes([0.02, 0.02, 0.96, 0.92], projection="3d")
axes.computed_zorder = False

angle_values = np.linspace(0.0, 2.0 * np.pi, 160)
height_fraction = np.linspace(0.0, 1.0, 50)
angle_grid, fraction_grid = np.meshgrid(angle_values, height_fraction)
x_wall = 2.0 * np.cos(angle_grid)
z_wall = 2.0 * np.sin(angle_grid)
y_wall = -1.0 + fraction_grid * (5.0 - z_wall)

axes.plot_surface(
    x_wall, y_wall, z_wall,
    color="#a8c6d8", alpha=1.0, linewidth=0.0, antialiased=False,
    rstride=1, cstride=2, shade=True, zorder=1,
)

radial_values = np.linspace(0.0, 2.0, 30)
radial_grid, angle_grid = np.meshgrid(radial_values, angle_values)
disk_x = radial_grid * np.cos(angle_grid)
disk_z = radial_grid * np.sin(angle_grid)

axes.plot_surface(
    disk_x, np.full_like(disk_x, -1.0), disk_z,
    color="#d3bd97", alpha=1.0, linewidth=0.0, shade=False, antialiased=False, zorder=2,
)
axes.plot_surface(
    disk_x, 4.0 - disk_z, disk_z,
    color="#b6cfa8", alpha=1.0, linewidth=0.0, shade=False, antialiased=False, zorder=3,
)

# Heavy outlines of both rim curves.
axes.plot(2.0 * np.cos(angle_values), np.full_like(angle_values, -1.0), 2.0 * np.sin(angle_values),
          color="#7a5c2e", linewidth=1.5, zorder=4)
axes.plot(2.0 * np.cos(angle_values), 4.0 - 2.0 * np.sin(angle_values), 2.0 * np.sin(angle_values),
          color="#3d5c2c", linewidth=1.5, zorder=4)

label_box = {"facecolor": "white", "alpha": 0.88, "edgecolor": "none", "pad": 2.0}
axes.text(-0.10, -1.03, -0.95, r"$y=-1$", color="#6b5222", fontsize=12, ha="center",
          bbox=label_box, zorder=10)
axes.text(-0.35, 4.03, 0.55, r"$y+z=4$", color="#3d5c2c", fontsize=12, ha="center",
          bbox=label_box, zorder=10)

axes.set_xlabel(r"$x$", labelpad=2)
axes.set_ylabel(r"$y$", labelpad=2)
axes.set_zlabel(r"$z$", labelpad=0)
axes.set_xlim(-2.6, 2.6)
axes.set_ylim(-1.0, 6.4)
axes.set_zlim(-2.6, 2.6)
axes.set_box_aspect((1.0, 1.75, 1.0))
axes.view_init(elev=24, azim=-62)

axes.legend(
    handles=[Patch(facecolor="#a8c6d8", edgecolor="#5b7f94", label=r"cylinder $x^2+z^2=4$")],
    loc="upper left", framealpha=0.95, handlelength=1.4, borderpad=0.45,
)

for axis in (axes.xaxis, axes.yaxis, axes.zaxis):
    axis.set_pane_color((0.97, 0.97, 0.95, 1.0))
    axis._axinfo["grid"]["color"] = (0.80, 0.80, 0.78, 1.0)

output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", pad_inches=0.06, facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
