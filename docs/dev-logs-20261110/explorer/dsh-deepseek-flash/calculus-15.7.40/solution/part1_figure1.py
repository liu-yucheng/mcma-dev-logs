"""Draw the solid bounded by a parabolic cylinder and three planes.

Panel (a) shows the solid E, its parabolic back face, its planar roof, and one
cross-section at a fixed value of y.  Panel (b) shows that cross-section, a right
triangle in a plane parallel to the xz-plane.
"""

import base64

import matplotlib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the 3d projection)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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

LABEL_BOX = {"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 1.4}

figure = plt.figure(figsize=(9.6, 4.5))
axes_3d = figure.add_subplot(1, 2, 1, projection="3d")
axes_2d = figure.add_subplot(1, 2, 2)

# Grid over the parabolic segment 0 <= z <= 1 - y**2, -1 <= y <= 1.
y_values = np.linspace(-1.0, 1.0, 80)
t_values = np.linspace(0.0, 1.0, 45)
y_grid, t_grid = np.meshgrid(y_values, t_values)
z_grid = t_grid * (1.0 - y_grid**2)

# Roof: the plane x + z = 1, that is, x = 1 - z.
axes_3d.plot_surface(
    1.0 - z_grid, y_grid, z_grid,
    color="#e8d5ab", alpha=0.55, linewidth=0.0, shade=False, antialiased=True,
)

# Back face: the plane x = 0.
axes_3d.plot_surface(
    np.zeros_like(y_grid), y_grid, z_grid,
    color="#b9cfe2", alpha=0.45, linewidth=0.0, shade=False,
)

# Floor: the rectangle 0 <= x <= 1, -1 <= y <= 1 at z = 0.
x_floor, y_floor = np.meshgrid(np.linspace(0.0, 1.0, 14), y_values)
axes_3d.plot_surface(
    x_floor, y_floor, np.zeros_like(x_floor),
    color="#e7edf2", alpha=0.55, linewidth=0.0, shade=False,
)

# Curves that outline the solid.
rim_y = np.linspace(-1.0, 1.0, 240)
axes_3d.plot(rim_y**2, rim_y, 1.0 - rim_y**2, color="#1f3d5c", linewidth=1.9)
axes_3d.plot(np.zeros(240), rim_y, 1.0 - rim_y**2, color="#1f3d5c", linewidth=1.1)
axes_3d.plot(np.ones(240), rim_y, np.zeros(240), color="#8a6d3b", linewidth=1.7)
axes_3d.plot(np.zeros(240), rim_y, np.zeros(240), color="#44546a", linewidth=1.2)
for edge_y in (-1.0, 1.0):
    axes_3d.plot([0.0, 1.0], [edge_y, edge_y], [0.0, 0.0], color="#44546a", linewidth=1.2)
    axes_3d.plot([0.0, 0.0], [edge_y, edge_y], [0.0, 1.0 - edge_y**2], color="#1f3d5c",
                 linewidth=1.1)

# One cross-section at y = -0.55, drawn as a filled right triangle.
section_y = -0.55
section_height = 1.0 - section_y**2
axes_3d.plot([0.0, 1.0, 0.0, 0.0], [section_y] * 4, [0.0, 0.0, section_height, 0.0],
             color="#8a1c1c", linewidth=1.6)
section_face = Poly3DCollection(
    [[(0.0, section_y, 0.0), (1.0, section_y, 0.0), (0.0, section_y, section_height)]],
    facecolor="#d94848", edgecolor="none", alpha=0.42,
)
axes_3d.add_collection3d(section_face)

# One fibre parallel to the x-axis at y = 0.45 and z = 0.3.
fibre_y = 0.45
fibre_z = 0.3
axes_3d.plot([0.0, 1.0 - fibre_z], [fibre_y, fibre_y], [fibre_z, fibre_z],
             color="white", linewidth=4.4, solid_capstyle="round")
axes_3d.plot([0.0, 1.0 - fibre_z], [fibre_y, fibre_y], [fibre_z, fibre_z],
             color="#8a1c1c", linewidth=2.2, solid_capstyle="round")
axes_3d.plot([0.0], [fibre_y], [fibre_z], marker="o", color="#8a1c1c", markersize=5)
axes_3d.plot([1.0 - fibre_z], [fibre_y], [fibre_z], marker="o", color="#8a1c1c", markersize=5)

axes_3d.text(0.70, 0.72, 0.60, r"$x + z = 1$", color="#6b5222", fontsize=10.5,
             bbox=LABEL_BOX)
axes_3d.text(-0.34, -0.30, 0.55, r"$x = 0$", color="#2f4d6b", fontsize=10.5, bbox=LABEL_BOX)
axes_3d.text(0.28, 0.60, 0.97, r"$z = 1 - y^{2}$", color="#1f3d5c", fontsize=10, bbox=LABEL_BOX)
axes_3d.text(0.05, -1.16, 0.05, r"$z = 0$", color="#44546a", fontsize=10.5, bbox=LABEL_BOX)
axes_3d.text(0.30, -0.95, 0.10, r"section $y = -0.55$", color="#8a1c1c", fontsize=9,
             bbox=LABEL_BOX)

axes_3d.set_xlabel(r"$x$", labelpad=6)
axes_3d.set_ylabel(r"$y$", labelpad=6)
axes_3d.set_zlabel(r"$z$", labelpad=6)
axes_3d.set_xlim(0.0, 1.2)
axes_3d.set_ylim(-1.2, 1.2)
axes_3d.set_zlim(0.0, 1.15)
axes_3d.set_box_aspect((1.0, 1.6, 1.0), zoom=1.3)
axes_3d.view_init(elev=20, azim=-68)
axes_3d.set_title("(a) the solid $E$", pad=2)

# Panel (b): the cross-section at y = -0.55, a right triangle in the xz-plane.
x_line = np.linspace(0.0, 1.0, 200)
axes_2d.fill([0.0, 1.0, 0.0], [0.0, 0.0, section_height], color="#d94848", alpha=0.22,
             edgecolor="#8a1c1c", linewidth=1.6)
axes_2d.plot([0.0, 0.0], [0.0, section_height], color="#8a1c1c", linewidth=1.6)
axes_2d.plot(x_line, 1.0 - x_line, color="#6b5222", linewidth=1.8)
axes_2d.plot([0.0, 1.0], [0.0, 0.0], color="#44546a", linewidth=1.5)
axes_2d.annotate("", xy=(1.0, 0.0), xytext=(0.0, 0.0),
                 arrowprops={"arrowstyle": "<->", "color": "#44546a", "linewidth": 1.0})
axes_2d.text(0.45, -0.09, r"$1$", color="#44546a", fontsize=10, ha="center")
axes_2d.annotate("", xy=(0.0, section_height), xytext=(0.0, 0.0),
                 arrowprops={"arrowstyle": "<->", "color": "#44546a", "linewidth": 1.0})
axes_2d.text(-0.07, section_height / 2, r"$1 - y^{2}$", color="#44546a", fontsize=10,
             ha="right", va="center")
axes_2d.text(0.60, 0.56, r"$x + z = 1$", color="#6b5222", fontsize=10.5)
axes_2d.text(0.05, 0.42, r"$x = 0$", color="#8a1c1c", fontsize=10.5)
axes_2d.text(0.30, 0.16, r"$0 \leq x \leq 1 - z$", color="#8a1c1c", fontsize=10)
axes_2d.text(0.02, section_height + 0.05, rf"$z = {section_height:.2f}$", color="#1f3d5c",
             fontsize=10)
axes_2d.set_xlim(-0.25, 1.15)
axes_2d.set_ylim(-0.18, 1.0)
axes_2d.set_aspect("equal")
axes_2d.set_xlabel(r"$x$")
axes_2d.set_ylabel(r"$z$")
axes_2d.set_title(r"(b) the cross-section at fixed $y$", pad=6)
axes_2d.grid(True, color="#e2ded2", linewidth=0.7)
axes_2d.set_axisbelow(True)

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
