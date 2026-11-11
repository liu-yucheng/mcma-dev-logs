"""Draw the solid of Exercise 15.7.50 as a see-through surface sketch.

The solid is the part of the quarter cylinder y**2 + z**2 <= 9 that lies between
the planes x = 0 and y = 3x, above z = 0. The triangular base z = 0 is filled, the
flat end x = 0 is drawn as concentric quarter arcs, the plane y = 3x carries
vertical ribs, and one red segment marks a typical range 0 <= z <= sqrt(9 - y**2).
"""

from base64 import b64encode
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

HEIGHT = 3.0
ANGLE = np.linspace(0.0, np.pi / 2, 240)


def draw_base(axes):
    """Fill the triangular base z = 0 and mark its straight edges."""
    floor_y, floor_fraction = np.meshgrid(np.linspace(0.0, HEIGHT, 60), np.linspace(0.0, 1.0, 30))
    axes.plot_surface(floor_fraction * floor_y / 3.0, floor_y, np.zeros_like(floor_y),
                      color="#b3c69c", alpha=1.0, linewidth=0.0, shade=False)
    for sample_y in np.linspace(0.4, HEIGHT, 6):
        axes.plot([0.0, sample_y / 3.0], [sample_y, sample_y], [0.0, 0.0],
                  color="#7d9163", linewidth=0.8, alpha=0.9)
    axes.plot([0.0, 1.0], [0.0, 3.0], [0.0, 0.0], color="#1f3752", linewidth=1.8)
    axes.plot([1.0, 0.0], [3.0, 3.0], [0.0, 0.0], color="#1f3752", linewidth=1.8)


def draw_end_face(axes):
    """Draw the quarter disk in the plane x = 0 as concentric arcs."""
    for fraction in np.linspace(0.2, 1.0, 5):
        axes.plot(np.zeros_like(ANGLE), fraction * HEIGHT * np.sin(ANGLE),
                  fraction * HEIGHT * np.cos(ANGLE), color="#6d86a3", linewidth=0.9)
    axes.plot(np.zeros_like(ANGLE), HEIGHT * np.sin(ANGLE), HEIGHT * np.cos(ANGLE),
              color="#1f3752", linewidth=1.8)


def draw_slanted_plane(axes):
    """Draw the plane y = 3x with vertical ribs and its curved upper edge."""
    for sample_y in np.linspace(0.2, 2.9, 7):
        top_height = np.sqrt(max(HEIGHT**2 - sample_y**2, 0.0))
        axes.plot([sample_y / 3.0, sample_y / 3.0], [sample_y, sample_y], [0.0, top_height],
                  color="#b4702c", linewidth=1.1)
    axes.plot(HEIGHT * np.sin(ANGLE) / 3.0, HEIGHT * np.sin(ANGLE), HEIGHT * np.cos(ANGLE),
              color="#8a5a28", linewidth=1.8)


def draw_probe_segment(axes):
    """Mark a vertical segment 0 <= z <= sqrt(9 - y**2) at one interior point."""
    sample_x, sample_y = 0.25, 1.50
    top_height = np.sqrt(HEIGHT**2 - sample_y**2)
    axes.plot([sample_x, sample_x], [sample_y, sample_y], [0.0, top_height],
              color="#a4231f", linewidth=3.0, solid_capstyle="round")
    axes.scatter([sample_x, sample_x], [sample_y, sample_y], [0.0, top_height],
                 color="#a4231f", s=26, depthshade=False)


def main():
    """Draw the solid of Exercise 15.7.50 and save the figure with its Base64 text."""
    matplotlib.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "mathtext.fontset": "stix",
        "figure.dpi": 170,
    })

    figure = plt.figure(figsize=(7.6, 6.8), dpi=170)
    axes = figure.add_subplot(projection="3d")

    draw_base(axes)
    draw_end_face(axes)
    draw_slanted_plane(axes)
    draw_probe_segment(axes)

    label_box = {"boxstyle": "round,pad=0.18", "facecolor": "white", "alpha": 0.82, "edgecolor": "none"}
    axes.text(0.02, 0.25, 2.62, r"$x = 0$", color="#2f4b68", fontsize=14, bbox=label_box)
    axes.text(0.50, 2.45, 2.62, r"$y = 3x$", color="#8a4b14", fontsize=14, bbox=label_box)
    axes.text(0.55, 2.75, 0.62, r"$y^2 + z^2 = 9$", color="#2f4b68", fontsize=13, bbox=label_box)
    axes.text(-0.48, 1.30, 1.35, r"$\sqrt{9-y^2}$", color="#a4231f", fontsize=13, bbox=label_box)

    axes.set_xlabel(r"$x$", fontsize=15, labelpad=8)
    axes.set_ylabel(r"$y$", fontsize=15, labelpad=8)
    axes.set_zlabel(r"$z$", fontsize=15, labelpad=8)
    axes.set_xlim(0.0, 1.05)
    axes.set_ylim(0.0, 3.1)
    axes.set_zlim(0.0, 3.1)
    axes.set_box_aspect((0.55, 1.6, 1.6))
    axes.view_init(elev=22, azim=-60)
    axes.set_xticks([0.0, 0.5, 1.0])
    axes.set_yticks([0.0, 1.0, 2.0, 3.0])
    axes.set_zticks([0.0, 1.0, 2.0, 3.0])
    axes.tick_params(labelsize=10)

    figure.tight_layout()
    output_path = Path(__file__).with_name("part1_figure1.png")
    figure.savefig(output_path, dpi=170, bbox_inches="tight", facecolor="white")
    print(output_path.resolve())

    encoded = b64encode(output_path.read_bytes()).decode("ascii")
    text_path = output_path.with_name("part1_figure1.b64.txt")
    text_path.write_text(encoded, encoding="ascii")
    print(text_path.resolve())
    print(f"base64 length: {len(encoded)}")


if __name__ == "__main__":
    main()
