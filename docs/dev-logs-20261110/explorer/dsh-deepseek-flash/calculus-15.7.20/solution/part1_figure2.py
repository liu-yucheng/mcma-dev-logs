"""Draw the cross-section and the section radii of the solid.

The left panel is the cross-section in the plane z = 0 with r >= 0. The right
panel shows the same cross-section with r from -2 to 2 and marks the chords
that give the radii of the horizontal sections at y = 1, 4, and 7.
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

figure, (left_axes, right_axes) = plt.subplots(1, 2, figsize=(10.6, 5.2))

# Left panel: the cross-section in the plane z = 0 with r >= 0.
radius = np.linspace(0.0, 2.0, 200)
left_axes.fill_between(radius, radius**2, 8.0 - radius**2, color="#e8e1cd", alpha=0.85)
left_axes.plot(radius, radius**2, color="#9a6420", linewidth=2.0, label=r"$y = r^{2}$")
left_axes.plot(radius, 8.0 - radius**2, color="#2c5b80", linewidth=2.0,
               label=r"$y = 8 - r^{2}$")
left_axes.plot([2.0, 2.0], [0.0, 4.0], color="#12304d", linewidth=1.2, linestyle=(0, (4, 3)))
left_axes.plot([2.0], [4.0], marker="o", color="#12304d", markersize=5)
left_axes.annotate("", xy=(1.0, 7.0), xytext=(1.0, 1.0),
                   arrowprops={"arrowstyle": "<->", "color": "#8a1c1c", "linewidth": 1.6})
left_axes.text(1.12, 3.6, r"$8 - 2r^{2}$", color="#8a1c1c", fontsize=10)
left_axes.text(2.08, 2.0, r"$r = 2$", color="#12304d", fontsize=10)
left_axes.text(2.08, 4.3, r"$y = 4$", color="#12304d", fontsize=10)
left_axes.set_xlim(0.0, 2.9)
left_axes.set_ylim(0.0, 9.0)
left_axes.set_xlabel(r"$r$")
left_axes.set_ylabel(r"$y$")
left_axes.set_title("Cross-section in the plane $z = 0$")
left_axes.grid(True, color="#e2dfd4", linewidth=0.8)
left_axes.legend(loc="upper right", frameon=False, fontsize=11)

# Right panel: chords that give the radii of the horizontal sections.
chord_radius = np.linspace(-2.0, 2.0, 300)
right_axes.fill_between(chord_radius, chord_radius**2, 8.0 - chord_radius**2,
                        color="#e8e1cd", alpha=0.85)
right_axes.plot(chord_radius, chord_radius**2, color="#9a6420", linewidth=1.6)
right_axes.plot(chord_radius, 8.0 - chord_radius**2, color="#2c5b80", linewidth=1.6)

for height_value, chord_color, label_text, label_shift in (
    (1.0, "#c0392b", r"$r = \sqrt{y}$", -0.42),
    (4.0, "#12304d", r"$r = 2$", 0.10),
    (7.0, "#2c5b80", r"$r = \sqrt{8-y}$", 0.10),
):
    half_width = float(np.sqrt(min(height_value, 8.0 - height_value)))
    right_axes.plot([-half_width, half_width], [height_value, height_value],
                    color=chord_color, linewidth=2.6, solid_capstyle="round")
    right_axes.text(-(half_width + 0.10), height_value + label_shift, label_text,
                    color=chord_color, fontsize=11, ha="right")

right_axes.text(-2.50, 8.45, "each section is a disk of this radius", color="#4a4a4a",
                fontsize=10.5)
right_axes.set_xlim(-2.6, 2.6)
right_axes.set_ylim(0.0, 9.0)
right_axes.set_xlabel(r"$x$ or $z$")
right_axes.set_ylabel(r"$y$")
right_axes.set_title(r"Horizontal sections have area $A(y) = \pi r^{2}$")
right_axes.grid(True, color="#e2dfd4", linewidth=0.8)

figure.tight_layout()
output_path = "part1_figure2.png"
figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
with open(output_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("ascii")
with open("part1_figure2.b64.txt", "w", encoding="ascii") as text_file:
    text_file.write(encoded)
print(f"saved {output_path} and part1_figure2.b64.txt ({len(encoded)} base64 characters)")
