"""Draw the base region of the solid cut from the sphere by the cylinder.

The inequality r <= a cos(theta) describes a disk of radius a/2 centred at
(a/2, 0). The figure shows that disk, the polar curve r = a cos(theta), and the
point where the angle theta is measured.
"""

import base64
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

FIGURE_NAME = "part1_figure2"


def main():
    """Render the base region and write the two output files."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Cambria", "STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.7,
            "font.size": 11.5,
        }
    )

    full_angle = np.linspace(0.0, np.pi, 400)
    curve_x = np.cos(full_angle) ** 2
    curve_y = np.cos(full_angle) * np.sin(full_angle)

    figure, axes = plt.subplots(figsize=(5.6, 4.9))
    axes.fill(np.append(curve_x, 0.0), np.append(curve_y, 0.0), color="#cfddea", zorder=0)
    axes.plot(curve_x, curve_y, color="#3f6fa8", linewidth=2.0)

    axes.plot([0.0, 1.0], [0.0, 0.0], color="#1c1c1e", linewidth=0.8)
    point_angle = np.pi / 3.0
    point_x = np.cos(point_angle) ** 2
    point_y = np.cos(point_angle) * np.sin(point_angle)
    axes.plot([0.0, point_x], [0.0, point_y], color="#8a1c1c", linewidth=1.2)
    axes.plot([point_x], [point_y], marker="o", color="#8a1c1c", markersize=5)
    axes.annotate(r"$\theta$", xy=(0.18, 0.06), fontsize=12)
    axes.annotate(r"$r = a\cos\theta$", xy=(0.93, 0.26), xytext=(0.56, 0.50),
                  fontsize=10.5, color="#3f6fa8",
                  arrowprops={"arrowstyle": "->", "linewidth": 0.8, "color": "#3f6fa8"})
    axes.text(0.16, -0.42, r"the disk $r \leq a\cos\theta$", fontsize=10.5, color="#33506f")
    axes.annotate(r"$a/2$", xy=(0.5, 0.0), xytext=(0.5, -0.13), fontsize=10,
                  ha="center")
    axes.plot([0.5], [0.0], marker="+", color="#1c1c1e", markersize=6)
    axes.annotate(r"$a$", xy=(1.0, 0.0), xytext=(1.0, -0.13), fontsize=10, ha="center")

    axes.set_aspect("equal")
    axes.set_xlim(-0.12, 1.15)
    axes.set_ylim(-0.62, 0.62)
    axes.set_xlabel(r"$x/a$")
    axes.set_ylabel(r"$y/a$")
    axes.set_title("The base of the solid: the disk $r \\leq a\\cos\\theta$", fontsize=11.5)
    axes.grid(True, linewidth=0.4, alpha=0.45)

    figure.tight_layout()
    output = Path(__file__).with_name(FIGURE_NAME + ".png")
    figure.savefig(output, dpi=170)
    plt.close(figure)

    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    Path(__file__).with_name(FIGURE_NAME + ".b64.txt").write_text(encoded, encoding="ascii")
    print(f"saved {output.name} and {FIGURE_NAME}.b64.txt ({len(encoded)} base64 characters)")


if __name__ == "__main__":
    main()