"""Draw the disk y**2 + z**2 <= 9 and the two families of slices.

A vertical slice at a fixed y gives the z-interval of the inner integral with
respect to z. A horizontal slice at a fixed z gives the y-interval of the
inner integral with respect to y.
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

figure, axes = plt.subplots(figsize=(5.4, 4.9))
theta = np.linspace(0.0, 2.0 * np.pi, 400)
axes.fill(3.0 * np.cos(theta), 3.0 * np.sin(theta), color="#eef3f8", edgecolor="#4d6a8a",
          linewidth=1.4, zorder=1)

# Vertical slice at y = 1.2, where z runs from -sqrt(9 - y^2) to sqrt(9 - y^2).
fixed_y = 1.2
half_height = np.sqrt(9.0 - fixed_y**2)
axes.plot([fixed_y, fixed_y], [-half_height, half_height], color="#8a1c1c", linewidth=2.2,
          zorder=3)
axes.plot([fixed_y, fixed_y], [half_height, half_height + 0.35], color="#8a1c1c",
          linewidth=0.9, linestyle=":", zorder=3)
axes.annotate(r"$z=\pm\sqrt{9-y^{2}}$ at fixed $y$", xy=(fixed_y, half_height),
              xytext=(0.15, 3.45), color="#8a1c1c", fontsize=10,
              arrowprops={"arrowstyle": "->", "color": "#8a1c1c", "lw": 0.9})

# Horizontal slice at z = -1.6, where y runs from -sqrt(9 - z^2) to sqrt(9 - z^2).
fixed_z = -1.6
half_width = np.sqrt(9.0 - fixed_z**2)
axes.plot([-half_width, half_width], [fixed_z, fixed_z], color="#3f6b34", linewidth=2.2,
          zorder=3)
axes.plot([-half_width - 0.35, -half_width], [fixed_z, fixed_z], color="#3f6b34",
          linewidth=0.9, linestyle=":", zorder=3)
axes.annotate(r"$y=\pm\sqrt{9-z^{2}}$ at fixed $z$", xy=(-half_width, fixed_z),
              xytext=(-3.70, -3.55), color="#3f6b34", fontsize=10, ha="left",
              arrowprops={"arrowstyle": "->", "color": "#3f6b34", "lw": 0.9})

axes.axhline(0.0, color="#9a9a9a", linewidth=0.8, zorder=0)
axes.axvline(0.0, color="#9a9a9a", linewidth=0.8, zorder=0)
axes.set_xlim(-4.0, 4.2)
axes.set_ylim(-4.3, 4.0)
axes.set_aspect("equal")
axes.set_xlabel(r"$y$")
axes.set_ylabel(r"$z$")
axes.set_title(r"The disk $D$: $y^{2}+z^{2} \leq 9$ and its slices", pad=8)
axes.grid(True, color="#e3e0d8", linewidth=0.6)
axes.set_axisbelow(True)

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")