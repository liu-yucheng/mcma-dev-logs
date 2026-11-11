"""Draw the vertical cross-section of the cap in the plane y = 0.

The slice shows the parabolic boundary z = 1 - x**2, the floor z = 0, the two
rim points x = -1 and x = 1, and one vertical fibre of length 1 - r**2.
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
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
})

figure, axes = plt.subplots(figsize=(7.0, 4.2))

x_values = np.linspace(-1.0, 1.0, 400)
upper_values = 1.0 - x_values**2

axes.fill_between(x_values, 0.0, upper_values, color="#cfe0ef", alpha=0.85,
                  label="the solid $E$")
axes.plot(x_values, upper_values, color="#1f3d5c", linewidth=2.0,
          label=r"$z = 1 - x^{2}$")
axes.plot([-1.05, 1.05], [0.0, 0.0], color="#8a6d3b", linewidth=1.6,
          label=r"$z = 0$")

fibre_x = 0.55
fibre_height = 1.0 - fibre_x**2
axes.annotate(
    "", xy=(fibre_x, fibre_height), xytext=(fibre_x, 0.0),
    arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "linewidth": 1.8},
)
axes.plot([fibre_x], [fibre_height], marker="o", color="#8a1c1c", markersize=4)
axes.annotate(
    r"$1 - r^{2} = " + f"{fibre_height:.3f}" + r"$",
    xy=(fibre_x - 0.02, 0.33), xytext=(0.09, 0.12),
    color="#8a1c1c", fontsize=11,
    arrowprops={"arrowstyle": "-", "color": "#8a1c1c", "linewidth": 1.0},
)

axes.plot([-1.0, 1.0], [0.0, 0.0], linestyle="none", marker="o", color="#8a6d3b",
          markersize=5)
axes.text(-0.98, -0.10, r"$x = -1$", color="#6b5222", fontsize=10)
axes.text(0.86, -0.10, r"$x = 1$", color="#6b5222", fontsize=10)

axes.set_xlim(-1.12, 1.12)
axes.set_ylim(-0.16, 1.10)
axes.set_xlabel(r"$x$   (in the plane $y = 0$ the distance from the axis is $r = |x|$)")
axes.set_ylabel(r"$z$")
axes.set_title(r"Vertical cross-section of $E$ in the plane $y = 0$", pad=10)
axes.legend(loc="upper left", frameon=False, fontsize=10)
axes.grid(True, linewidth=0.4, alpha=0.35)
figure.tight_layout()

output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")
