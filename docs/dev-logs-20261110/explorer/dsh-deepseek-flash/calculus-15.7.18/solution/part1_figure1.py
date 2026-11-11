"""Draw the solid of Exercise 18 as a stack of rectangular slices.

Each slice sits at one value of y.  The slice is the rectangle 0 <= x <= y/3
and 0 <= z <= sqrt(9 - y**2), so the stack shows the volume as an iterated
integral in the order dz dx dy.
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

figure = plt.figure(figsize=(7.6, 5.9))
axes = figure.add_subplot(111, projection="3d")

slice_centers = np.linspace(0.12, 2.88, 11)
half_thickness = 0.07
highlight_index = 5

for index, y_value in enumerate(slice_centers):
    x_edge = y_value / 3.0
    z_edge = float(np.sqrt(max(9.0 - y_value**2, 0.0)))
    x_grid, z_grid = np.meshgrid(np.linspace(0.0, x_edge, 4), np.linspace(0.0, z_edge, 14))
    if index == highlight_index:
        front_color, back_color, edge_color = "#c0392b", "#8a1c1c", "#5c0f0f"
    else:
        front_color, back_color, edge_color = "#e8bd7a", "#c98f3f", "#7a4f14"
    axes.plot_surface(x_grid, np.full_like(x_grid, y_value - half_thickness), z_grid,
                      color=front_color, alpha=1.0, linewidth=0.0, shade=False)
    axes.plot_surface(x_grid, np.full_like(x_grid, y_value + half_thickness), z_grid,
                      color=back_color, alpha=1.0, linewidth=0.0, shade=False)
    axes.plot([0.0, x_edge], [y_value, y_value], [z_edge, z_edge],
              color=edge_color, linewidth=1.0)
    axes.plot([0.0, 0.0], [y_value, y_value], [0.0, z_edge], color=edge_color, linewidth=0.9)
    axes.plot([x_edge, x_edge], [y_value, y_value], [0.0, z_edge], color=edge_color, linewidth=0.9)

# The quarter circle y**2 + z**2 = 9 on the back face x = 0.
rim_angle = np.linspace(0.0, np.pi / 2.0, 200)
axes.plot(np.zeros_like(rim_angle), 3.0 * np.cos(rim_angle), 3.0 * np.sin(rim_angle),
          color="#12304d", linewidth=2.0)

# The edge where the planes y = 3*x and z = 0 meet.
axes.plot([0.0, 1.0], [0.0, 3.0], [0.0, 0.0], color="#2f6b4f", linewidth=1.8)

axes.text(0.50, 2.00, 2.62, r"one slice at fixed $y$", color="#8a1c1c", fontsize=9.5)

axes.text(0.03, 1.35, 3.02, r"$y^{2}+z^{2}=9$", color="#12304d", fontsize=11)
axes.text(0.74, 2.42, 0.12, r"$y=3x$", color="#2f6b4f", fontsize=11)

axes.set_xlabel(r"$x$", labelpad=8)
axes.set_ylabel(r"$y$", labelpad=8)
axes.set_zlabel(r"$z$", labelpad=6)
axes.set_xlim(-0.05, 1.2)
axes.set_ylim(-0.12, 3.3)
axes.set_zlim(0.0, 3.3)
axes.set_xticks([0.0, 0.5, 1.0])
axes.set_yticks([0.0, 1.0, 2.0, 3.0])
axes.set_zticks([0.0, 1.0, 2.0, 3.0])
axes.set_box_aspect((0.9, 2.2, 2.2))
axes.view_init(elev=24, azim=-60)
axes.set_title(r"$E$ divided into slices of thickness $\Delta y$", pad=8)

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
