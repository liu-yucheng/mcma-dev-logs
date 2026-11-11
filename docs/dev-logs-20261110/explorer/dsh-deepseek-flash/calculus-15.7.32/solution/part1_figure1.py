"""Draw the tetrahedron bounded by x = 2, y = 2, z = 0, and x + y - 2*z = 2.

Each of the four faces is a translucent panel with bold edges. A legend names
the four planes, and one vertical fibre shows the inner z-limits of the order
dz dy dx.
"""

import base64

import matplotlib
import numpy as np
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.labelsize": 11,
})

vertex_a = np.array([2.0, 0.0, 0.0])
vertex_b = np.array([0.0, 2.0, 0.0])
vertex_c = np.array([2.0, 2.0, 0.0])
vertex_d = np.array([2.0, 2.0, 1.0])

figure = plt.figure(figsize=(7.4, 5.6))
axes = figure.add_subplot(111, projection="3d")

legend_handles = []
faces = [
    ([vertex_a, vertex_b, vertex_c], "#8fb0cc", 0.42, r"$z = 0$"),
    ([vertex_a, vertex_c, vertex_d], "#e3cfa6", 0.36, r"$x = 2$"),
    ([vertex_b, vertex_c, vertex_d], "#bdd3b6", 0.36, r"$y = 2$"),
    ([vertex_a, vertex_b, vertex_d], "#e9b3a2", 0.42, r"$x+y-2z = 2$"),
]
for corners, color, alpha, name in faces:
    panel = Poly3DCollection([corners], facecolor=color, edgecolor="none", alpha=alpha)
    axes.add_collection3d(panel)
    legend_handles.append(Patch(facecolor=color, edgecolor="#555555", alpha=0.75, label=name))

edges = [
    (vertex_a, vertex_b), (vertex_b, vertex_c), (vertex_c, vertex_a),
    (vertex_a, vertex_d), (vertex_b, vertex_d), (vertex_c, vertex_d),
]
for start, end in edges:
    axes.plot(*zip(start, end), color="#222222", linewidth=1.5)

fibre_x, fibre_y = 1.45, 1.75
fibre_top = (fibre_x + fibre_y - 2.0) / 2.0
axes.plot([fibre_x, fibre_x], [fibre_y, fibre_y], [0.0, fibre_top],
          color="#8a1c1c", linewidth=2.2, zorder=10)
axes.scatter([fibre_x], [fibre_y], [fibre_top], color="#8a1c1c", s=20, depthshade=False)

label_style = {"fontsize": 11, "fontweight": "bold", "color": "#1c1c1e", "ha": "center"}
axes.text(2.16, -0.16, -0.06, "A", **label_style)
axes.text(-0.18, 2.18, -0.04, "B", **label_style)
axes.text(2.20, 2.22, 1.10, "D", **label_style)

fibre_handle = plt.Line2D([], [], color="#8a1c1c", linewidth=2.2, label="typical fibre of $E$")
axes.legend(handles=legend_handles + [fibre_handle], loc="upper left", fontsize=9,
            frameon=True, framealpha=0.95, edgecolor="#cccccc", handlelength=1.4)

axes.set_xlabel(r"$x$", labelpad=8)
axes.set_ylabel(r"$y$", labelpad=8)
axes.set_zlabel(r"$z$", labelpad=8)
axes.set_xlim(-0.05, 2.55)
axes.set_ylim(-0.05, 2.55)
axes.set_zlim(-0.22, 1.25)
axes.set_xticks([0.0, 1.0, 2.0])
axes.set_yticks([0.0, 1.0, 2.0])
axes.set_zticks([0.0, 0.5, 1.0])
axes.set_box_aspect((1.0, 1.0, 0.55))
axes.view_init(elev=26, azim=-138)
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
