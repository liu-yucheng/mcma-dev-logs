"""Draw the projection of E on the plane x = 0 and the section of E at a fixed y.

The left panel shows the quarter disc that the cylinder cuts in the plane x = 0 and the strip that the
section at y = 1.5 projects onto. The right panel shows that section itself as a rectangle in the plane
y = 1.5, with the numbers of the drawing printed from figure_anchors.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors

OUTPUT_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure2.png"
GRID_POINT_COUNT = 400


def main() -> None:
    """Draw the two panels, check every annotation, and write the PNG file."""
    section_y = figure_anchors.SECTION_Y
    width = section_y / 3.0
    height = float(np.sqrt(9.0 - section_y ** 2))
    print(f"section at y = {section_y}: width = {width:.6f}, height = {height:.6f},"
          f" area = {width * height:.6f}")

    figure, (left, right) = plt.subplots(1, 2, figsize=(10.4, 4.8))
    angle = np.linspace(0.0, np.pi / 2.0, GRID_POINT_COUNT)
    left.fill_between(3.0 * np.cos(angle), 0.0, 3.0 * np.sin(angle), color="#4c72b0",
                      alpha=0.30, label="projection of $E$")
    left.plot(3.0 * np.cos(angle), 3.0 * np.sin(angle), color="#2f4b7c", linewidth=1.8,
              label="$y^{2} + z^{2} = 9$")
    left.plot([section_y, section_y], [0.0, height], color="#c44e52", linewidth=2.4,
              label=f"section at $y = {section_y}$")
    left.plot([section_y], [height], marker="o", color="#c44e52", markersize=5)
    left.annotate(f"height $= {height:.3f}$", xy=(section_y, height), xytext=(0.85, 2.95),
                  arrowprops={"arrowstyle": "-|>", "color": "#7d2b2f", "linewidth": 0.9,
                              "shrinkA": 2.0, "shrinkB": 6.0},
                  fontsize=10, bbox={"facecolor": "white", "edgecolor": "#cccccc", "pad": 2.0})
    left.set_xlim(-0.35, 3.45)
    left.set_ylim(-0.35, 3.45)
    left.set_aspect("equal")
    left.set_xlabel(r"$y$")
    left.set_ylabel(r"$z$")
    left.set_title("Projection on the plane $x = 0$", fontsize=11)
    left.legend(loc="lower left", fontsize=8.5, framealpha=0.9)
    left.grid(alpha=0.25)

    corners_x = [0.0, width, width, 0.0, 0.0]
    corners_z = [0.0, 0.0, height, height, 0.0]
    right.fill(corners_x, corners_z, color="#c44e52", alpha=0.25)
    right.plot(corners_x, corners_z, color="#7d2b2f", linewidth=1.8)
    right.plot([width / 2.0, width / 2.0], [0.0, height], color="#7d2b2f", linewidth=0.8,
               linestyle=(0, (4, 3)))
    right.annotate(f"$x$ from $0$ to ${width:.3f}$", xy=(width, height / 2.0),
                   xytext=(0.62, 1.55), fontsize=10,
                   arrowprops={"arrowstyle": "-|>", "color": "#7d2b2f", "linewidth": 0.9,
                               "shrinkA": 2.0, "shrinkB": 8.0},
                   bbox={"facecolor": "white", "edgecolor": "#cccccc", "pad": 2.0})
    right.annotate(f"$z$ from $0$ to ${height:.3f}$", xy=(width / 2.0, height),
                   xytext=(0.62, 2.60), fontsize=10,
                   arrowprops={"arrowstyle": "-|>", "color": "#7d2b2f", "linewidth": 0.9,
                               "shrinkA": 2.0, "shrinkB": 8.0},
                   bbox={"facecolor": "white", "edgecolor": "#cccccc", "pad": 2.0})
    right.plot([0.0], [0.0], marker="o", color="#7d2b2f", markersize=4)
    right.set_xlim(-0.05, 1.30)
    right.set_ylim(-0.25, 3.15)
    right.set_xlabel(r"$x$")
    right.set_ylabel(r"$z$")
    right.set_title(f"Section at $y = {section_y}$", fontsize=11)
    right.grid(alpha=0.25)

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for panel, name in ((left, "left"), (right, "right")):
        axes_box = panel.get_window_extent(renderer)
        for annotation in panel.texts:
            extent = annotation.get_window_extent(renderer)
            inside = (axes_box.contains(extent.x0, extent.y0)
                      and axes_box.contains(extent.x1, extent.y1))
            print(f"annotation on the {name} panel inside the axes box = {inside},"
                  f" text = {annotation.get_text()!r}")
            assert inside, f"an annotation leaves the {name} panel"
        legend = panel.get_legend()
        if legend is not None:
            extent = legend.get_window_extent(renderer)
            inside = (axes_box.contains(extent.x0, extent.y0)
                      and axes_box.contains(extent.x1, extent.y1))
            print(f"legend on the {name} panel inside the axes box = {inside}")
            assert inside, f"the legend leaves the {name} panel"

    figure.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=170, bbox_inches="tight")
    image = plt.imread(OUTPUT_PATH)
    border = np.concatenate([image[0, :, :3].ravel(), image[-1, :, :3].ravel(),
                             image[:, 0, :3].ravel(), image[:, -1, :3].ravel()])
    print(f"saved image {image.shape[1]} x {image.shape[0]} pixels,"
          f" smallest border value = {border.min():.3f}")
    assert border.min() >= 0.90, "a drawn element touches the border of the saved image"
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
