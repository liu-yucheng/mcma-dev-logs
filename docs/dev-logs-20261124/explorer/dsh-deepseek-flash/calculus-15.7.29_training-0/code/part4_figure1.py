"""Draw figure 1 of Part 4: the shadow of the solid on a plane of constant z.

The figure is a workspace product. At a fixed value z = z0 the solid projects on the plane of
the coordinates x and y onto the region 0 <= y <= 4 - x**2 - 4*z0**2 with |x| <= sqrt(4 - 4*z0**2).
Each panel is one such region. The region is one piece, so the order with the inner integral in
z needs no split.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Path of the figure that this script writes.
FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part4_figure1.png"

# Resolution of the figure in dots per inch.
FIGURE_RESOLUTION = 150

# Values of z of the two panels.
FIXED_Z_VALUES = (0.0, 0.5)

# Count of points along one parabola.
POINT_COUNT = 400


def main() -> None:
    """Draw both panels and write the figure to the figures directory."""
    figure, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    for axis, fixed_z in zip(axes, FIXED_Z_VALUES):
        half_width = math.sqrt(4.0 - 4.0 * fixed_z**2)
        coordinate_x = np.linspace(-half_width, half_width, POINT_COUNT)
        coordinate_y = 4.0 - 4.0 * fixed_z**2 - coordinate_x**2
        axis.fill_between(coordinate_x, 0.0, coordinate_y, color="#4c78a8", alpha=0.35)
        axis.plot(coordinate_x, coordinate_y, color="#1f3b57", linewidth=2.0)
        axis.plot([-half_width, half_width], [0.0, 0.0], color="#8a5a00", linewidth=2.0)
        axis.annotate("", xy=(half_width + 0.45, 0.0), xytext=(0.0, 0.0),
                      arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
        axis.annotate("", xy=(0.0, 4.7), xytext=(0.0, 0.0),
                      arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
        axis.text(half_width + 0.48, 0.06, "$x$", fontsize=13, va="bottom")
        axis.text(0.08, 4.62, "$y$", fontsize=13, va="bottom")
        # The wall label is anchored on the parabola, where its own equation holds.
        anchor_x = 0.55 * half_width
        axis.text(anchor_x, 4.0 - 4.0 * fixed_z**2 - anchor_x**2,
                  "$y = 4 - 4z_0^{2} - x^{2}$", fontsize=10, color="#1f3b57", va="center")
        axis.text(-half_width, -0.22, f"$x = -{half_width:.4f}$", fontsize=9, ha="left")
        axis.text(half_width, -0.22, f"$x = {half_width:.4f}$", fontsize=9, ha="right")
        axis.set_xlim(-2.6, 2.75)
        axis.set_ylim(-0.6, 4.9)
        axis.grid(alpha=0.3)
        axis.set_xlabel("$x$")
        axis.set_ylabel("$y$")
        axis.set_title(f"The shadow at $z_0 = {fixed_z:.1f}$: one region, so no split", fontsize=10)
    figure.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=FIGURE_RESOLUTION, bbox_inches="tight")
    plt.close(figure)
    for fixed_z in FIXED_Z_VALUES:
        print(f"z0 = {fixed_z:.1f}: half width in x = {math.sqrt(4.0 - 4.0 * fixed_z**2):.9f}, "
              f"height = {4.0 - 4.0 * fixed_z**2:.9f}")
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
