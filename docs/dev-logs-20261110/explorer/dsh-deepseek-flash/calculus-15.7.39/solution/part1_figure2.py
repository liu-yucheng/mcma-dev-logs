"""Draw the plane region D bounded by y = sqrt(x), y = 0, and x = 1.

A vertical slice and a horizontal slice of D are marked. They give the two
descriptions of D that the page uses for the two orders of integration.
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
})

figure, axes = plt.subplots(figsize=(6.4, 5.0))

curve_x = np.linspace(0.0, 1.0, 400)
curve_y = np.sqrt(curve_x)

axes.fill_between(curve_x, np.zeros_like(curve_x), curve_y, color="#a9c4de", alpha=0.70,
                  label=r"$D$")
axes.plot(curve_x, curve_y, color="#8a1c1c", linewidth=2.4, label=r"$y = \sqrt{x}$")
axes.plot([0.0, 1.0], [0.0, 0.0], color="#333333", linewidth=1.6, label=r"$y = 0$")
axes.plot([1.0, 1.0], [0.0, 1.0], color="#33506b", linewidth=1.6, label=r"$x = 1$")

box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 1.2}

slice_x = 0.55
slice_top = np.sqrt(slice_x)
axes.plot([slice_x, slice_x], [0.0, slice_top], color="#1f6b3a", linewidth=2.0)
axes.text(slice_x + 0.035, 0.36, r"$0 \leq y \leq \sqrt{x}$", color="#1f6b3a",
          fontsize=9.5, ha="left", va="center", bbox=box)

level_y = 0.55
level_left = level_y ** 2
axes.plot([level_left, 1.0], [level_y, level_y], color="#8a5a12", linewidth=2.0)
axes.text(0.62, level_y - 0.045, r"$y^2 \leq x \leq 1$", color="#8a5a12",
          fontsize=9.5, ha="left", va="top", bbox=box)

axes.text(0.83, 0.20, r"$D$", color="#16405e", fontsize=15, ha="center")
axes.set_xlabel(r"$x$")
axes.set_ylabel(r"$y$")
axes.set_xlim(0.0, 1.12)
axes.set_ylim(0.0, 1.12)
axes.set_aspect("equal")
axes.grid(True, color="#e2e2e2", linewidth=0.8)
axes.set_axisbelow(True)
axes.legend(loc="upper left", fontsize=10, frameon=True, framealpha=0.95,
            edgecolor="#cccccc")

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")
