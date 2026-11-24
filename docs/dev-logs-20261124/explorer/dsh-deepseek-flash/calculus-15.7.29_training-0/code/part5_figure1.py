"""Draw figure 1 of Part 5: the shadow of the solid on a plane of constant x.

The figure is a workspace product. At a fixed value x = x0 the solid projects on the plane of
the coordinates z and y onto the region 0 <= y <= 4 - x0**2 - 4*z**2 with
|z| <= sqrt(4 - x0**2)/2. Each panel is one such region. The region is one piece, so the order
with the inner integral in x needs no split.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Path of the figure that this script writes.
FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part5_figure1.png"

# Resolution of the figure in dots per inch.
FIGURE_RESOLUTION = 150

# Values of x of the two panels.
FIXED_X_VALUES = (0.0, 1.5)

# Count of points along one parabola.
POINT_COUNT = 400


def main() -> None:
    """Draw both panels and write the figure to the figures directory."""
    figure, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    for axis, fixed_x in zip(axes, FIXED_X_VALUES):
        half_width = math.sqrt(4.0 - fixed_x**2) / 2.0
        coordinate_z = np.linspace(-half_width, half_width, POINT_COUNT)
        coordinate_y = 4.0 - fixed_x**2 - 4.0 * coordinate_z**2
        axis.fill_between(coordinate_z, 0.0, coordinate_y, color="#4c78a8", alpha=0.35)
        axis.plot(coordinate_z, coordinate_y, color="#1f3b57", linewidth=2.0)
        axis.plot([-half_width, half_width], [0.0, 0.0], color="#8a5a00", linewidth=2.0)
        axis.annotate("", xy=(half_width + 0.55, 0.0), xytext=(0.0, 0.0),
                      arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
        axis.annotate("", xy=(0.0, 4.9), xytext=(0.0, 0.0),
                      arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.1))
        axis.text(half_width + 0.58, 0.06, "$z$", fontsize=13, va="bottom")
        axis.text(0.03, 4.82, "$y$", fontsize=13, va="bottom")
        anchor_z = 0.55 * half_width
        axis.text(anchor_z, 4.0 - fixed_x**2 - 4.0 * anchor_z**2,
                  "$y = 4 - x_0^{2} - 4z^{2}$", fontsize=10, color="#1f3b57", va="center")
        axis.text(-half_width, -0.28, f"$z = -{half_width:.4f}$", fontsize=9, ha="left")
        axis.text(half_width, -0.28, f"$z = {half_width:.4f}$", fontsize=9, ha="right")
        axis.set_xlim(-1.9, 1.95)
        axis.set_ylim(-0.75, 5.1)
        axis.grid(alpha=0.3)
        axis.set_xlabel("$z$")
        axis.set_ylabel("$y$")
        axis.set_title(f"The shadow at $x_0 = {fixed_x:.1f}$: one region, so no split", fontsize=10)
    figure.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=FIGURE_RESOLUTION, bbox_inches="tight")
    plt.close(figure)
    for fixed_x in FIXED_X_VALUES:
        print(f"x0 = {fixed_x:.1f}: half width in z = {math.sqrt(4.0 - fixed_x**2) / 2.0:.9f}, "
              f"height = {4.0 - fixed_x**2:.9f}")
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
