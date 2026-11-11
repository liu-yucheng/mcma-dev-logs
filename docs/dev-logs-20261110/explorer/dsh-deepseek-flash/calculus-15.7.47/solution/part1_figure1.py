"""Draw the solid enclosed by a parabolic cylinder, a floor, and a sloping roof.

Panel (a) shows the solid cut open at x = 0.55: the wall y = x^2, the floor z = 0, the roof
y + z = 1, and the red triangular cross-section that the cut exposes.  Panel (b) shows the base
region in the xy-plane, where a strip of width dx runs from the parabola up to the line y = 1.
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

LABEL_BOX = {"facecolor": "white", "edgecolor": "none", "alpha": 1.0, "pad": 1.4}

figure = plt.figure(figsize=(9.6, 4.5))
axes_3d = figure.add_subplot(1, 2, 1, projection="3d")
axes_2d = figure.add_subplot(1, 2, 2)

cut_x = 0.55
x_values = np.linspace(-1.0, cut_x, 60)
s_values = np.linspace(0.0, 1.0, 30)
x_grid, s_grid = np.meshgrid(x_values, s_values)

# Base region: y runs from x^2 to 1.
y_base = x_grid**2 + s_grid * (1.0 - x_grid**2)

# Floor z = 0 over the base region.
axes_3d.plot_surface(x_grid, y_base, np.zeros_like(x_grid), color="#e7edf2", alpha=0.85,
                     linewidth=0.0, shade=False)

# Roof y + z = 1, that is, z = 1 - y.
axes_3d.plot_surface(x_grid, y_base, 1.0 - y_base, color="#e8d5ab", alpha=0.85,
                     linewidth=0.0, shade=False)

# Wall y = x^2, from the floor up to the roof.
z_wall = s_grid * (1.0 - x_grid**2)
axes_3d.plot_surface(x_grid, x_grid**2, z_wall, color="#9dbcd8", alpha=0.9,
                     linewidth=0.0, shade=False)

# Ridge where the roof meets the wall, and the foot of the wall on the floor.
axes_3d.plot(x_values, x_values**2, 1.0 - x_values**2, color="#1f3d5c", linewidth=2.0)
axes_3d.plot(x_values, x_values**2, np.zeros_like(x_values), color="#1f3d5c", linewidth=1.1)
axes_3d.plot(x_values, np.ones_like(x_values), np.zeros_like(x_values), color="#8a6d3b",
             linewidth=1.6)

# Red triangle exposed by the cut: y from cut_x^2 to 1, z from 0 to 1 - y.
cut_face = [[(cut_x, cut_x**2, 0.0), (cut_x, 1.0, 0.0), (cut_x, cut_x**2, 1.0 - cut_x**2)]]
axes_3d.add_collection3d(Poly3DCollection(cut_face, facecolor="#c85a5a", edgecolor="#8a1c1c",
                                          linewidth=1.3, alpha=0.85))

axes_3d.text(-0.55, 0.30, 0.98, r"$y + z = 1$", color="#6b5222", fontsize=10.5, bbox=LABEL_BOX,
             zorder=60)
axes_3d.text(-0.98, 0.70, 0.30, r"$y = x^{2}$", color="#2f4d6b", fontsize=10.5, bbox=LABEL_BOX,
             zorder=60)
# The floor needs no label: the caption names it and the light surface is visible at the front.
axes_3d.text(cut_x + 0.12, 0.72, 0.80, r"cut at $x = 0.55$", color="#8a1c1c", fontsize=9.5,
             bbox=LABEL_BOX, zorder=60)
axes_3d.plot([cut_x, cut_x + 0.10], [0.80, 0.76], [0.60, 0.78], color="#8a1c1c", linewidth=0.9,
             linestyle=(0, (3, 2)))

axes_3d.set_xlabel(r"$x$", labelpad=6)
axes_3d.set_ylabel(r"$y$", labelpad=6)
axes_3d.set_zlabel(r"$z$", labelpad=6)
axes_3d.set_xlim(-1.1, 1.0)
axes_3d.set_ylim(0.0, 1.15)
axes_3d.set_zlim(0.0, 1.15)
axes_3d.set_box_aspect((1.5, 1.0, 1.0), zoom=1.25)
axes_3d.view_init(elev=20, azim=-35)
axes_3d.set_title("(a) the solid, cut at $x = 0.55$", pad=2)

# Panel (b): the base region x^2 <= y <= 1.
panel_x = np.linspace(-1.0, 1.0, 300)
axes_2d.fill_between(panel_x, panel_x**2, 1.0, color="#b9cfe2", alpha=0.45, edgecolor="none")
axes_2d.plot(panel_x, panel_x**2, color="#1f3d5c", linewidth=1.9)
axes_2d.plot([-1.0, 1.0], [1.0, 1.0], color="#6b5222", linewidth=1.8)
axes_2d.plot([-1.0, -1.0], [0.0, 1.05], color="#44546a", linewidth=1.1, linestyle=(0, (4, 3)))
axes_2d.plot([1.0, 1.0], [0.0, 1.05], color="#44546a", linewidth=1.1, linestyle=(0, (4, 3)))

strip_x = -0.45
strip_width = 0.06
axes_2d.add_patch(plt.Rectangle((strip_x - strip_width / 2, strip_x**2), strip_width,
                                1.0 - strip_x**2, facecolor="#d94848", alpha=0.55,
                                edgecolor="#8a1c1c", linewidth=1.2))
axes_2d.annotate("", xy=(strip_x + 0.10, 1.0), xytext=(strip_x + 0.10, strip_x**2),
                 arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "linewidth": 1.1})
axes_2d.text(strip_x + 0.13, (1.0 + strip_x**2) / 2, r"$x^{2} \leq y \leq 1$", color="#8a1c1c",
             fontsize=10, va="center")
axes_2d.text(strip_x, -0.12, r"$dx$", color="#8a1c1c", fontsize=10, ha="center")
axes_2d.text(0.55, 0.66, r"$y = x^{2}$", color="#1f3d5c", fontsize=10.5)
axes_2d.text(-0.42, 1.05, r"$y = 1$", color="#6b5222", fontsize=10.5)
axes_2d.text(0.95, -0.15, r"$x$", color="#33475b", fontsize=11)
axes_2d.text(-1.25, 0.55, r"$y$", color="#33475b", fontsize=11)

axes_2d.set_xlim(-1.32, 1.18)
axes_2d.set_ylim(-0.22, 1.15)
axes_2d.set_aspect("equal")
axes_2d.set_title("(b) the base region", pad=6)
axes_2d.grid(True, color="#e2ded2", linewidth=0.7)
axes_2d.set_axisbelow(True)
axes_2d.set_xticks([])
axes_2d.set_yticks([])

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
