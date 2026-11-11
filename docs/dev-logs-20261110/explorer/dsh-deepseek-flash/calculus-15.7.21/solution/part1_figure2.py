"""Draw the projection of the solid and one section at a fixed x.

The left panel is the projection D in the xy-plane, bounded by the parabola
y = x**2 and the line y = 1. The right panel is the section at x = 0.5, a
triangle with vertices (0.25, 0), (1, 0), and (0.25, 0.75).
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
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 12.5,
})

figure, (left_axes, right_axes) = plt.subplots(1, 2, figsize=(10.6, 4.9))

# Left panel: the projection D in the xy-plane.
coordinate_x = np.linspace(-1.0, 1.0, 300)
left_axes.fill_between(coordinate_x, coordinate_x**2, 1.0, color="#cfd8e0", alpha=0.55)
left_axes.plot(coordinate_x, coordinate_x**2, color="#9a6420", linewidth=2.2, label=r"$y = x^{2}$")
left_axes.plot([-1.25, 1.25], [1.0, 1.0], color="#2c5b80", linewidth=2.2, label=r"$y = 1$")
for boundary_x in (-1.0, 1.0):
    left_axes.plot([boundary_x, boundary_x], [0.0, 1.0], color="#12304d", linewidth=1.2,
                   linestyle=(0, (4, 3)))
left_axes.annotate("", xy=(0.0, 1.0), xytext=(0.0, 0.0),
                   arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "linewidth": 1.6})
left_axes.text(0.06, 0.52, r"$x^{2} \leq y \leq 1$", color="#8a1c1c", fontsize=11.5)
left_axes.text(-0.62, 0.72, r"$D_{xy}$", color="#12304d", fontsize=13)
left_axes.text(-1.22, 1.05, r"$x = -1$", color="#12304d", fontsize=10.5)
left_axes.text(0.72, 1.05, r"$x = 1$", color="#12304d", fontsize=10.5)
left_axes.set_xlim(-1.35, 1.35)
left_axes.set_ylim(0.0, 1.18)
left_axes.set_xlabel(r"$x$")
left_axes.set_ylabel(r"$y$")
left_axes.set_title("The projection in the $xy$-plane")
left_axes.grid(True, color="#e2dfd4", linewidth=0.8)
left_axes.legend(loc="lower right", frameon=False, fontsize=11)

# Right panel: the section at x = 0.5.
triangle_y = [0.25, 1.0, 0.25, 0.25]
triangle_z = [0.0, 0.0, 0.75, 0.0]
right_axes.fill(triangle_y, triangle_z, color="#e8e1cd", alpha=0.9)
right_axes.plot(triangle_y, triangle_z, color="#6b5222", linewidth=1.6)
right_axes.plot([0.25, 1.0], [0.75, 0.0], color="#2c5b80", linewidth=2.4)
right_axes.plot([0.25, 0.25], [0.0, 0.75], color="#9a6420", linewidth=2.4)
right_axes.annotate("", xy=(1.0, 0.12), xytext=(0.25, 0.12),
                    arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "linewidth": 1.6})
right_axes.text(0.30, 0.17, r"$x^{2} = 0.25 \leq y \leq 1$", color="#8a1c1c", fontsize=11)
right_axes.annotate("", xy=(0.38, 0.62), xytext=(0.38, 0.0),
                    arrowprops={"arrowstyle": "<->", "color": "#2f6b4f", "linewidth": 1.6})
right_axes.text(0.42, 0.26, r"$0 \leq z \leq 1 - y$", color="#2f6b4f", fontsize=11)
right_axes.text(0.60, 0.46, r"$z = 1 - y$", color="#2c5b80", fontsize=11.5)
right_axes.text(0.18, 0.66, r"$0.75$", color="#9a6420", fontsize=10.5, ha="right")
right_axes.text(0.22, -0.06, r"$0.25$", color="#9a6420", fontsize=10.5, ha="right")
right_axes.set_xlim(0.10, 1.15)
right_axes.set_ylim(-0.10, 0.92)
right_axes.set_xlabel(r"$y$")
right_axes.set_ylabel(r"$z$")
right_axes.set_title("The section at $x = 0.5$")
right_axes.grid(True, color="#e2dfd4", linewidth=0.8)

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")
