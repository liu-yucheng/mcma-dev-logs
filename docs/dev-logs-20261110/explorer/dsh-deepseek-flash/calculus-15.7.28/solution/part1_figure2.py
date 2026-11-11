"""Draw the projection of the solid of exercise 15.7.28 onto the yz-plane."""

import base64

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Cambria", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 11,
})

figure, axes = plt.subplots(figsize=(6.9, 4.3))

triangle_y = np.array([0.0, 2.0, 0.0, 0.0])
triangle_z = np.array([0.0, 0.0, 2.0, 0.0])
axes.fill(triangle_y, triangle_z, color="#a9bccd", alpha=0.45, edgecolor="#2c4a6b",
          linewidth=1.6, zorder=1)

# One cut at a fixed height y shows the z-limits.
cut_y = 0.8
cut_top = 2.0 - cut_y
axes.plot([cut_y, cut_y], [0.0, cut_top], color="#8a1c1c", linewidth=2.8, zorder=3)
axes.annotate("", xy=(cut_y + 0.07, cut_top), xytext=(cut_y + 0.07, 0.0),
              arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "lw": 1.4,
                          "shrinkA": 0.0, "shrinkB": 0.0})

axes.annotate("cut at fixed $y$:" "\n" r"$0 \leq z \leq 2 - y$" "\n"
              r"$0 \leq x \leq 4 - y^{2}$",
              xy=(cut_y, 0.62), xytext=(2.12, 1.02), fontsize=10.5, color="#222222",
              va="center",
              arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 0.9,
                          "connectionstyle": "arc3,rad=0.12"})

axes.text(1.5, 0.34, r"$z = 2 - y$", color="#2c4a6b", fontsize=12, rotation=-33,
          rotation_mode="anchor", ha="left", va="top")

axes.set_xlim(-0.15, 3.15)
axes.set_ylim(-0.18, 2.25)
axes.set_aspect("equal")
axes.set_xlabel(r"$y$")
axes.set_ylabel(r"$z$")
axes.set_title(r"The projection is the triangle $0 \leq y \leq 2$, $0 \leq z \leq 2 - y$",
               pad=10)
axes.grid(alpha=0.22, linewidth=0.6)
axes.spines["top"].set_visible(False)
axes.spines["right"].set_visible(False)

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")