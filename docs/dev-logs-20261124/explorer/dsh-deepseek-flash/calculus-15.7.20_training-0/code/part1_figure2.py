"""Draw both paraboloids and the circle where they meet.

The vertical axis is y. The two horizontal axes are x and z. The figure shows
the lower paraboloid, the upper paraboloid, and the meeting circle of radius 2
at the height 4.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# The upper surface is y = 8 - radius**2, so its constant term is 8.
UPPER_SURFACE_CONSTANT = 8.0
# The two surfaces meet at radius 2 and at height 4.
MEETING_RADIUS = 2.0
MEETING_HEIGHT = 4.0
# The surfaces are drawn on a disk that is slightly wider than the solid.
DRAWING_RADIUS = 2.0
# The output file of the figure.
OUTPUT_PATH = "code/figures/part1_figure2.png"


def main() -> None:
    """Draw the two surfaces and write the figure file."""
    radius = np.linspace(0.0, DRAWING_RADIUS, 80)
    angle = np.linspace(0.0, 2.0 * np.pi, 120)
    radius_grid, angle_grid = np.meshgrid(radius, angle)
    horizontal_x = radius_grid * np.cos(angle_grid)
    horizontal_z = radius_grid * np.sin(angle_grid)
    lower_grid = radius_grid**2
    upper_grid = UPPER_SURFACE_CONSTANT - radius_grid**2

    figure = plt.figure(figsize=(8.0, 6.6))
    axes = figure.add_subplot(111, projection="3d")
    axes.plot_surface(horizontal_x, horizontal_z, lower_grid, color="#1f4e79", alpha=0.55,
                      linewidth=0.0, antialiased=True)
    axes.plot_surface(horizontal_x, horizontal_z, upper_grid, color="#a33a2a", alpha=0.35,
                      linewidth=0.0, antialiased=True)

    circle_angle = np.linspace(0.0, 2.0 * np.pi, 240)
    axes.plot(
        MEETING_RADIUS * np.cos(circle_angle),
        MEETING_RADIUS * np.sin(circle_angle),
        np.full_like(circle_angle, MEETING_HEIGHT),
        color="#111111",
        linewidth=2.4,
    )
    axes.plot([0.0], [0.0], [MEETING_HEIGHT], "o", color="#111111", markersize=5)
    axes.plot([0.0], [0.0], [UPPER_SURFACE_CONSTANT], "o", color="#111111", markersize=4)
    axes.plot([0.0], [0.0], [0.0], "o", color="#111111", markersize=4)

    surface_legend = [
        Patch(facecolor="#1f4e79", alpha=0.55, label=r"lower surface $y = x^{2} + z^{2}$"),
        Patch(facecolor="#a33a2a", alpha=0.40, label=r"upper surface $y = 8 - x^{2} - z^{2}$"),
        Line2D([0.0], [0.0], color="#111111", linewidth=2.4, label=r"meeting circle $r = 2$, $y = 4$"),
    ]
    axes.legend(handles=surface_legend, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=1, fontsize=9,
                frameon=False)
    axes.set_xlabel(r"$x$", fontsize=11)
    axes.set_ylabel(r"$z$", fontsize=11)
    axes.set_zlabel(r"$y$", fontsize=11)
    axes.set_xlim(-2.35, 2.35)
    axes.set_ylim(-2.35, 2.35)
    axes.set_zlim(0.0, 8.6)
    axes.set_title(r"The solid between $y = x^{2} + z^{2}$ and $y = 8 - x^{2} - z^{2}$", fontsize=12)
    axes.view_init(elev=18.0, azim=-62.0)
    axes.set_box_aspect((1.0, 1.0, 1.25))
    figure.tight_layout()
    figure.savefig(OUTPUT_PATH, dpi=200)
    plt.close(figure)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
