"""Draw the solid cone and the cylindrical shell used for its moment of inertia.

Panel (a) shows the cone sqrt(x^2 + y^2) <= z <= h with h = 1, cut open along two
half-planes so that one shell of radius r and height h - r is visible.  Panel (b) shows
the cross-section in a plane that contains the z-axis, where the shell becomes a
vertical strip of width dr.
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
HEIGHT = 1.0
SHELL_RADIUS = 0.55
CUT_START = np.deg2rad(55.0)
CUT_END = np.deg2rad(305.0)

figure = plt.figure(figsize=(9.6, 4.5))
axes_3d = figure.add_subplot(1, 2, 1, projection="3d")
axes_2d = figure.add_subplot(1, 2, 2)

angle_cut = np.linspace(CUT_START, CUT_END, 121)
angle_full = np.linspace(0.0, 2.0 * np.pi, 241)

# Lateral surface of the cone z = r, cut open along two half-planes.
radius_values = np.linspace(0.0, HEIGHT, 60)
angle_grid, radius_grid = np.meshgrid(angle_cut, radius_values)
axes_3d.plot_surface(
    radius_grid * np.cos(angle_grid), radius_grid * np.sin(angle_grid), radius_grid,
    color="#b9cfe2", alpha=0.55, linewidth=0.0, shade=False, antialiased=True,
)

# Base sector at z = h.
base_radius, base_angle = np.meshgrid(np.linspace(0.0, HEIGHT, 20), angle_cut)
axes_3d.plot_surface(
    base_radius * np.cos(base_angle), base_radius * np.sin(base_angle),
    np.full_like(base_radius, HEIGHT), color="#e8d5ab", alpha=0.6, linewidth=0.0, shade=False,
)

# The two cut faces are right triangles through the z-axis.
for cut_angle in (CUT_START, CUT_END):
    cut_face = Poly3DCollection(
        [[(0.0, 0.0, 0.0),
          (HEIGHT * np.cos(cut_angle), HEIGHT * np.sin(cut_angle), HEIGHT),
          (0.0, 0.0, HEIGHT)]],
        facecolor="#8fa9c4", edgecolor="#1f3d5c", linewidth=1.0, alpha=0.30,
    )
    axes_3d.add_collection3d(cut_face)

# Rim of the base and the axis.
axes_3d.plot(HEIGHT * np.cos(angle_full), HEIGHT * np.sin(angle_full),
             np.full_like(angle_full, HEIGHT), color="#1f3d5c", linewidth=1.6)
axes_3d.plot([0.0, 0.0], [0.0, 0.0], [0.0, HEIGHT + 0.18], color="#44546a", linewidth=1.1,
             linestyle=(0, (5, 3)))

# One shell of radius r: the part of the cylinder wall between z = r and z = h.
shell_angle = np.linspace(CUT_START, CUT_END, 121)
shell_z_values = np.linspace(SHELL_RADIUS, HEIGHT, 12)
shell_angle_grid, shell_z_grid = np.meshgrid(shell_angle, shell_z_values)
axes_3d.plot_surface(
    SHELL_RADIUS * np.cos(shell_angle_grid), SHELL_RADIUS * np.sin(shell_angle_grid), shell_z_grid,
    color="#d94848", alpha=0.35, linewidth=0.0, shade=False,
)
# Front generator of the shell, marked with its height h - r.
axes_3d.plot([SHELL_RADIUS, SHELL_RADIUS], [0.0, 0.0], [SHELL_RADIUS, HEIGHT],
             color="white", linewidth=4.6, solid_capstyle="round")
axes_3d.plot([SHELL_RADIUS, SHELL_RADIUS], [0.0, 0.0], [SHELL_RADIUS, HEIGHT],
             color="#8a1c1c", linewidth=2.4, solid_capstyle="round")
# Radius of the shell, drawn on the base plane.
axes_3d.plot([0.0, SHELL_RADIUS], [0.0, 0.0], [HEIGHT, HEIGHT], color="white", linewidth=4.0)
axes_3d.plot([0.0, SHELL_RADIUS], [0.0, 0.0], [HEIGHT, HEIGHT], color="#8a1c1c", linewidth=1.8)

axes_3d.text(-0.95, -0.55, 0.42, r"$z = \sqrt{x^{2} + y^{2}}$", color="#1f3d5c", fontsize=9.5,
             bbox=LABEL_BOX)
axes_3d.text(0.66, 0.02, 0.60, r"$h - r$", color="#8a1c1c", fontsize=10.5, bbox=LABEL_BOX)
axes_3d.text(-0.95, -0.75, 1.06, r"$z = h$", color="#6b5222", fontsize=10, bbox=LABEL_BOX)

axes_3d.set_xlabel(r"$x$", labelpad=6)
axes_3d.set_ylabel(r"$y$", labelpad=6)
axes_3d.set_zlabel(r"$z$", labelpad=6)
axes_3d.set_xlim(-1.15, 1.15)
axes_3d.set_ylim(-1.15, 1.15)
axes_3d.set_zlim(0.0, 1.25)
axes_3d.set_box_aspect((1.0, 1.0, 1.0), zoom=1.25)
axes_3d.view_init(elev=18, azim=-62)
axes_3d.set_title("(a) the cone and one shell", pad=2)

# Panel (b): the r z cross-section, 0 <= r <= h and r <= z <= h.
r_line = np.linspace(0.0, HEIGHT, 200)
axes_2d.fill([0.0, HEIGHT, 0.0], [0.0, HEIGHT, HEIGHT], color="#b9cfe2", alpha=0.45,
             edgecolor="#1f3d5c", linewidth=1.6)
axes_2d.plot(r_line, r_line, color="#1f3d5c", linewidth=1.8)
axes_2d.plot([0.0, HEIGHT], [HEIGHT, HEIGHT], color="#6b5222", linewidth=1.8)
axes_2d.plot([0.0, 0.0], [0.0, HEIGHT], color="#44546a", linewidth=1.4)

strip_width = 0.09
axes_2d.add_patch(plt.Rectangle((SHELL_RADIUS - strip_width / 2, SHELL_RADIUS), strip_width,
                                HEIGHT - SHELL_RADIUS, facecolor="#d94848", alpha=0.55,
                                edgecolor="#8a1c1c", linewidth=1.2))
axes_2d.annotate("", xy=(SHELL_RADIUS, HEIGHT), xytext=(SHELL_RADIUS, SHELL_RADIUS),
                 arrowprops={"arrowstyle": "<->", "color": "#4a0d0d", "linewidth": 1.1})
axes_2d.text(SHELL_RADIUS - 0.06, 0.76, r"$h - r$", color="#8a1c1c", fontsize=10.5,
             rotation=90, va="center", ha="center")
axes_2d.annotate("", xy=(SHELL_RADIUS + strip_width / 2, HEIGHT + 0.06),
                 xytext=(SHELL_RADIUS - strip_width / 2, HEIGHT + 0.06),
                 arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "linewidth": 1.0})
axes_2d.text(SHELL_RADIUS, HEIGHT + 0.10, r"$dr$", color="#8a1c1c", fontsize=10, ha="center")
axes_2d.text(0.66, 0.78, r"$z = r$", color="#1f3d5c", fontsize=10.5)
axes_2d.text(0.20, 1.03, r"$z = h$", color="#6b5222", fontsize=10.5)
axes_2d.annotate("", xy=(HEIGHT, HEIGHT), xytext=(0.0, HEIGHT),
                 arrowprops={"arrowstyle": "<->", "color": "#6b5222", "linewidth": 1.0})

axes_2d.set_xlim(-0.18, 1.15)
axes_2d.set_ylim(-0.22, 1.20)
axes_2d.set_aspect("equal")
axes_2d.set_xlabel(r"$r$")
axes_2d.set_ylabel(r"$z$")
axes_2d.set_title(r"(b) the cross-section at fixed $\theta$", pad=6)
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
