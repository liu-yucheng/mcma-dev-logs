"""Draw the projection triangle and the horizontal slices of the pyramid.

The left panel shows the projection T of the solid onto the xz-plane. The right panel
shows the rectangle that the solid cuts from the plane z = constant. The script writes a
PNG file with its Base64 copy.
"""

import base64

import matplotlib
from matplotlib.patches import Polygon, Rectangle

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "axes.labelsize": 12,
})

figure, (left, right) = plt.subplots(1, 2, figsize=(9.8, 4.6))

triangle = Polygon([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], closed=True,
                   facecolor="#cfbf9a", edgecolor="#5b4a2e", linewidth=1.6, alpha=0.75)
left.add_patch(triangle)
left.plot([0.0, 1.0], [1.0, 0.0], color="#8c2f1e", linewidth=1.8)
left.annotate(r"$z = 1 - x$", xy=(0.55, 0.45), xytext=(0.62, 0.72), fontsize=11,
              arrowprops={"arrowstyle": "-", "color": "#8c2f1e", "linewidth": 1.0}, color="#8c2f1e")
left.text(0.30, 0.26, r"$T$", fontsize=17, color="#4a3a1e")
left.text(0.32, 0.11, r"area $= \frac{1}{2}$", fontsize=11, color="#4a3a1e")
left.set_xlim(-0.06, 1.12)
left.set_ylim(-0.06, 1.12)
left.set_aspect("equal")
left.set_xlabel(r"$x$")
left.set_ylabel(r"$z$")
left.set_title("(a) projection $T$ onto the $xz$-plane")
left.grid(color="0.88", linewidth=0.7)

height_colors = ["#a8c6d8", "#9dbb85", "#d79a72", "#b09ec9"]
for index, height in enumerate([0.0, 0.25, 0.5, 0.75]):
    width = 1.0 - height
    depth = 2.0 - 2.0 * height
    right.add_patch(Rectangle((0.0, 0.0), width, depth, facecolor=height_colors[index],
                              edgecolor="#2f3a44", linewidth=1.5, alpha=0.30))
    right.text(width + 0.03, depth - 0.09, f"$z = {height:g}$", fontsize=10.5,
               color="#1f2a33", va="top")
right.plot([0.0], [0.0], marker="o", markersize=5.0, color="#8c2f1e", zorder=5)
right.text(0.03, -0.05, r"$z = 1$: one point", fontsize=9.5, color="#8c2f1e", va="top")

right.set_xlim(-0.08, 1.45)
right.set_ylim(-0.28, 2.30)
right.set_aspect("equal")
right.set_xlabel(r"$x$")
right.set_ylabel(r"$y$")
right.set_title(r"(b) slice at height $z$: width $1 - z$, length $2 - 2z$", fontsize=11.5)
right.grid(color="0.88", linewidth=0.7)

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", pad_inches=0.06, facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")
