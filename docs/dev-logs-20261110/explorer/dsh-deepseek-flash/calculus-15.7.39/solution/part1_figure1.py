"""Draw the solid under z = 1 + x + y above the plane region bounded by y = sqrt(x), y = 0, x = 1.

The roof plane is translucent and covers the base region exactly. Three walls join
the base to the roof, and three vertical fibres show the gap between them.
"""

import base64

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.labelsize": 11,
})

figure = plt.figure(figsize=(7.4, 5.9))
axes = figure.add_subplot(111, projection="3d")

# The base region: x = u, y = v*sqrt(u) maps the unit square onto D.
u = np.linspace(0.0, 1.0, 100)
v = np.linspace(0.0, 1.0, 70)
grid_u, grid_v = np.meshgrid(u, v)
grid_x = grid_u
grid_y = grid_v * np.sqrt(grid_u)

axes.plot_surface(grid_x, grid_y, np.zeros_like(grid_x), color="#8fb0cc",
                  alpha=0.95, linewidth=0.0, shade=False)

# The roof covers the same base region, so its boundary is the curved edge y = sqrt(x).
axes.plot_surface(grid_x, grid_y, 1.0 + grid_x + grid_y, color="#e8a33d",
                  alpha=0.42, linewidth=0.0, shade=False)

# The three walls of E: one flat wall at y = 0, one at x = 1, and one curved wall.
wall_color = "#9fb2c4"
wall_a, wall_t = np.meshgrid(np.linspace(0.0, 1.0, 60), np.linspace(0.0, 1.0, 40))
axes.plot_surface(wall_a, np.zeros_like(wall_a), wall_t * (1.0 + wall_a),
                  color=wall_color, alpha=0.15, linewidth=0.0, shade=False)
axes.plot_surface(np.ones_like(wall_a), wall_a, wall_t * (2.0 + wall_a),
                  color=wall_color, alpha=0.15, linewidth=0.0, shade=False)
curved_u, curved_t = np.meshgrid(u, np.linspace(0.0, 1.0, 40))
axes.plot_surface(curved_u, np.sqrt(curved_u),
                  curved_t * (1.0 + curved_u + np.sqrt(curved_u)),
                  color=wall_color, alpha=0.15, linewidth=0.0, shade=False)

# Boundary curves of the base and of the roof.
edge_color = "#4a4a4a"
axes.plot(u, np.zeros_like(u), 1.0 + u, color=edge_color, linewidth=1.3)
axes.plot(np.ones_like(u), u, 2.0 + u, color=edge_color, linewidth=1.3)
axes.plot(u, np.sqrt(u), 1.0 + u + np.sqrt(u), color="#8a1c1c", linewidth=1.9)
axes.plot(u, np.zeros_like(u), np.zeros_like(u), color=edge_color, linewidth=1.2)
axes.plot(np.ones_like(u), u, np.zeros_like(u), color=edge_color, linewidth=1.2)
axes.plot(u, np.sqrt(u), np.zeros_like(u), color="#8a1c1c", linewidth=1.5)
axes.plot([0.0, 0.0], [0.0, 0.0], [1.0, 1.0], color=edge_color, linewidth=1.0)

for fibre_x, fibre_y in ((0.18, 0.20), (0.52, 0.42), (0.86, 0.55)):
    axes.plot([fibre_x, fibre_x], [fibre_y, fibre_y], [0.0, 1.0 + fibre_x + fibre_y],
              color="#8a1c1c", linewidth=1.8, zorder=10)
    axes.scatter([fibre_x], [fibre_y], [1.0 + fibre_x + fibre_y],
                 color="#8a1c1c", s=14, depthshade=False)

# A short vertical leader ties the roof label to the roof surface.
axes.plot([0.12, 0.12], [0.06, 0.06], [1.19, 2.42], color="#a9812f", linewidth=0.9)
box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 1.2}
axes.text(0.12, 0.06, 2.48, r"$z = 1 + x + y$", color="#8a5a12", fontsize=10,
          ha="left", va="bottom", bbox=box)
axes.text(0.78, 0.99, 0.03, r"$y = \sqrt{x}$", color="#8a1c1c", fontsize=10,
          ha="center", va="center", bbox=box)
axes.text2D(0.815, 0.345, r"$x = 1$", transform=axes.transAxes, color="#2d4a63",
             fontsize=10, ha="center", va="center", bbox=box)
axes.text(0.32, 0.10, 0.06, r"$D$", color="#123a56", fontsize=13, zorder=40,
          ha="center", va="center", bbox=box)

axes.set_xlabel(r"$x$", labelpad=8)
axes.set_ylabel(r"$y$", labelpad=8)
axes.set_zlabel(r"$z$", labelpad=8)
axes.set_xlim(0.0, 1.15)
axes.set_ylim(0.0, 1.15)
axes.set_zlim(0.0, 3.1)
axes.set_xticks([0.0, 0.5, 1.0])
axes.set_yticks([0.0, 0.5, 1.0])
axes.set_zticks([0.0, 1.0, 2.0, 3.0])
axes.set_box_aspect((1.0, 1.0, 1.0))
axes.view_init(elev=26, azim=-46)
for pane in (axes.xaxis.pane, axes.yaxis.pane, axes.zaxis.pane):
    pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
    pane.set_edgecolor("#c8c8c8")

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
