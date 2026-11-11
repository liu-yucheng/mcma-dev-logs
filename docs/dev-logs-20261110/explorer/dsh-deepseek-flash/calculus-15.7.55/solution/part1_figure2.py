"""Show where the integrand is positive and where it is negative.

Panel (a) maps the level curves of g(x, y, 0) = 1 - x**2 - 2*y**2 in the plane
z = 0. Panel (b) plots g along the three coordinate axes, so the reader sees the
three intercepts of the ellipsoid.
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
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
})

figure, (map_axes, axis_axes) = plt.subplots(1, 2, figsize=(9.6, 4.3))

grid_values = np.linspace(-1.35, 1.35, 401)
x_grid, y_grid = np.meshgrid(grid_values, grid_values)
level_values = 1.0 - x_grid**2 - 2.0 * y_grid**2

map_axes.contourf(x_grid, y_grid, level_values, levels=[-5.0, 0.0], colors=["#f3d9d5"])
map_axes.contourf(x_grid, y_grid, level_values, levels=[0.0, 1.2], colors=["#dce9f5"])
map_axes.contour(x_grid, y_grid, level_values, levels=[-4.0, -3.0, -2.0, -1.0, 0.25, 0.5, 0.75],
                 colors="#7c93a8", linewidths=0.8)
map_axes.contour(x_grid, y_grid, level_values, levels=[0.0], colors="#1f3d5c", linewidths=2.2)

map_axes.plot([1.0, -1.0], [0.0, 0.0], linestyle="none", marker="o", color="#8a1c1c", markersize=4)
map_axes.plot([0.0, 0.0], [0.7071, -0.7071], linestyle="none", marker="o", color="#8a1c1c", markersize=4)
map_axes.text(0.0, 0.30, r"$g > 0$", ha="center", fontsize=11, color="#1f3d5c")
map_axes.text(1.05, 0.98, r"$g < 0$", ha="center", fontsize=11, color="#8a1c1c")
map_axes.annotate(r"$x = 1$", xy=(1.0, 0.0), xytext=(0.58, -0.46),
                  fontsize=10, arrowprops={"arrowstyle": "-", "color": "#555555", "lw": 0.7})
map_axes.annotate(r"$y = 0.707$", xy=(0.0, 0.7071), xytext=(-1.30, 0.90),
                  fontsize=10, arrowprops={"arrowstyle": "-", "color": "#555555", "lw": 0.7})
map_axes.set_xlim(-1.35, 1.35)
map_axes.set_ylim(-1.15, 1.15)
map_axes.set_xlabel(r"$x$")
map_axes.set_ylabel(r"$y$")
map_axes.set_aspect("equal")
map_axes.set_title(r"Level curves of $g$ in the plane $z = 0$")

distance = np.linspace(0.0, 1.45, 400)
axis_axes.axhline(0.0, color="#333333", linewidth=1.0)
axis_axes.plot(distance, 1.0 - distance**2, color="#1f4e79", linewidth=1.8, label=r"along $x$: $1 - t^{2}$")
axis_axes.plot(distance, 1.0 - 2.0 * distance**2, color="#b5651d", linewidth=1.8,
               label=r"along $y$: $1 - 2t^{2}$")
axis_axes.plot(distance, 1.0 - 3.0 * distance**2, color="#4c7a34", linewidth=1.8,
               label=r"along $z$: $1 - 3t^{2}$")
for root in (1.0, 0.7071, 0.5774):
    axis_axes.plot([root], [0.0], marker="o", markersize=5, color="#8a1c1c", zorder=5)
axis_axes.axvspan(0.0, 1.0, color="#dce9f5", alpha=0.55, zorder=0)
axis_axes.text(0.42, -0.42, r"$g > 0$", fontsize=11, color="#1f3d5c")
axis_axes.text(1.16, 0.16, r"$g < 0$", fontsize=11, color="#8a1c1c")
axis_axes.set_xlim(0.0, 1.45)
axis_axes.set_ylim(-1.6, 1.25)
axis_axes.set_xlabel(r"distance $t$ from the origin along the axis")
axis_axes.set_ylabel(r"$g$")
axis_axes.legend(loc="lower left", fontsize=10, frameon=False)
axis_axes.set_title(r"$g$ on the three coordinate axes")
axis_axes.text(0.02, 0.96, "(b)", transform=axis_axes.transAxes, va="top", fontsize=10)
map_axes.text(0.02, 0.96, "(a)", transform=map_axes.transAxes, va="top", fontsize=10)

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")
