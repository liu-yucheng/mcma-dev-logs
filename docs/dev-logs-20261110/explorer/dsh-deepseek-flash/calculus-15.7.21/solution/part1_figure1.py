"""Draw the solid bounded by y = x^2, z = 0, and y + z = 1 as a stack of slices.

Each slice sits at a fixed value of x. Its shape is the triangle x^2 <= y <= 1,
0 <= z <= 1 - y, so the slices shrink to a point at x = -1 and at x = 1.
"""

import base64

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.labelsize": 11,
})

figure = plt.figure(figsize=(8.2, 6.8))
axes = figure.add_subplot(1, 1, 1, projection="3d")

slice_count = 11
half_thickness = 0.05
slice_centers = np.linspace(-0.88, 0.88, slice_count)
highlight_index = slice_count // 2

for index, center in enumerate(slice_centers):
    lower_edge = center**2
    height = 1.0 - lower_edge
    left_x = center - half_thickness
    right_x = center + half_thickness
    front_face = [(left_x, lower_edge, 0.0), (left_x, 1.0, 0.0), (left_x, lower_edge, height)]
    back_face = [(right_x, lower_edge, 0.0), (right_x, 1.0, 0.0), (right_x, lower_edge, height)]
    faces = [front_face, back_face]
    for first, second in ((0, 1), (1, 2), (2, 0)):
        faces.append([front_face[first], front_face[second], back_face[second], back_face[first]])
    face_color = "#c0392b" if index == highlight_index else "#e8bd7a"
    edge_color = "#8a1c1c" if index == highlight_index else "#a9762c"
    collection = Poly3DCollection(faces, facecolor=face_color, edgecolor=edge_color,
                                  linewidths=0.6, alpha=0.96)
    axes.add_collection3d(collection)

# Straight lines of the slanted roof z = 1 - y, from the wall up to the ridge y = 1.
for ruling_x in (-0.8, -0.45, 0.0, 0.45, 0.8):
    axes.plot([ruling_x, ruling_x], [ruling_x**2, 1.0], [1.0 - ruling_x**2, 0.0],
              color="#2c5b80", linewidth=0.9, linestyle=(0, (3, 2)))

curve_x = np.linspace(-1.0, 1.0, 300)
axes.plot(curve_x, curve_x**2, np.zeros_like(curve_x), color="#12304d", linewidth=2.2)
axes.plot(curve_x, curve_x**2, 1.0 - curve_x**2, color="#12304d", linewidth=2.2)
axes.plot(curve_x, np.ones_like(curve_x), np.zeros_like(curve_x), color="#2f6b4f", linewidth=2.2)

axes.text(0.06, 0.06, 1.03, "one slice at fixed $x$", color="#8a1c1c", fontsize=10)

axes.set_xlim(-1.12, 1.12)
axes.set_ylim(-0.05, 1.12)
axes.set_zlim(0.0, 1.12)
axes.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
axes.set_yticks([0.0, 0.5, 1.0])
axes.set_zticks([0.0, 0.5, 1.0])
axes.set_xlabel("$x$")
axes.set_ylabel("$y$")
axes.set_zlabel("$z$")
axes.set_box_aspect((2.1, 1.0, 1.0))
axes.view_init(elev=26, azim=-76)
axes.set_title(r"The solid: $y \geq x^{2}$, $z \geq 0$, $y + z \leq 1$", pad=2)

figure.tight_layout()
output_path = "part1_figure1.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure1.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure1.b64.txt ({len(encoded)} base64 characters)")
