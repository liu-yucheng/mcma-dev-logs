"""Draw the two projections that fix the limits of the integral.

The left panel shows the projection of E onto the xy-plane, a triangle bounded
by y = 3*x and y = 3. The right panel shows the quarter disk that the cylinder
cuts from the yz-plane with the z-range of one vertical slab.
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
    "axes.titlesize": 11,
})

figure, (left_axes, right_axes) = plt.subplots(1, 2, figsize=(9.6, 4.1))

# Left panel: the triangle 0 <= y <= 3, 0 <= x <= y/3.
y_values = np.linspace(0.0, 3.0, 200)
left_axes.fill_between(y_values / 3.0, y_values, 0.0, color="#cfdbe8", alpha=0.75,
                       edgecolor="none")
left_axes.plot(y_values / 3.0, y_values, color="#2f4f75", linewidth=2.0,
               label=r"$y=3x$")
left_axes.plot([0.0, 1.0], [3.0, 3.0], color="#8a6d3b", linewidth=2.0,
               label=r"$y=3$")
left_axes.plot([0.0, 0.0], [0.0, 3.0], color="#4d4d4d", linewidth=1.4)
left_axes.annotate("", xy=(0.5, 1.5), xytext=(0.0, 1.5),
                   arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "lw": 1.6})
left_axes.text(0.22, 1.62, r"$0\leq x\leq y/3$", color="#8a1c1c", fontsize=10)
left_axes.text(0.62, 1.05, r"$D_{xy}$", color="#2f4f75", fontsize=12)
left_axes.set_xlim(-0.05, 1.2)
left_axes.set_ylim(-0.1, 3.35)
left_axes.set_xlabel(r"$x$")
left_axes.set_ylabel(r"$y$")
left_axes.set_title(r"Projection of $E$ onto the $xy$-plane")
left_axes.legend(loc="upper right", frameon=False, fontsize=10)
left_axes.grid(color="#e2ded2", linewidth=0.7)
left_axes.set_axisbelow(True)

# Right panel: the quarter disk 0 <= y <= 3, 0 <= z <= sqrt(9 - y**2).
y_grid = np.linspace(0.0, 3.0, 300)
z_top = np.sqrt(np.maximum(9.0 - y_grid**2, 0.0))
right_axes.fill_between(y_grid, z_top, 0.0, color="#cfe0d2", alpha=0.8,
                        edgecolor="none")
right_axes.plot(y_grid, z_top, color="#2f6b4f", linewidth=2.0,
                label=r"$z=\sqrt{9-y^{2}}$")
right_axes.plot([0.0, 3.0], [0.0, 0.0], color="#4d4d4d", linewidth=1.4)
right_axes.plot([0.0, 0.0], [0.0, 3.0], color="#4d4d4d", linewidth=1.4)
right_axes.annotate("", xy=(1.5, np.sqrt(9.0 - 1.5**2)), xytext=(1.5, 0.0),
                    arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "lw": 1.6})
right_axes.text(1.62, 1.05, r"$z=\sqrt{9-y^{2}}$", color="#8a1c1c", fontsize=10)
right_axes.text(1.6, 0.25, r"$0\leq y\leq 3$", color="#2f6b4f", fontsize=10)
right_axes.set_xlim(-0.15, 3.4)
right_axes.set_ylim(-0.15, 3.4)
right_axes.set_aspect("equal")
right_axes.set_xlabel(r"$y$")
right_axes.set_ylabel(r"$z$")
right_axes.set_title(r"Section at fixed $x$: the quarter disk $D_{yz}$")
right_axes.grid(color="#e2ded2", linewidth=0.7)
right_axes.set_axisbelow(True)

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")
