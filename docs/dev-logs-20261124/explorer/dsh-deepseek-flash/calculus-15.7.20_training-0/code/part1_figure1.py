"""Draw the cross section of the solid in a vertical plane through the vertical axis.

The horizontal axis is the signed distance radius from the vertical axis. The
vertical axis is the height y. The figure shows the two parabolas, the enclosed
cross section, and the meeting point at radius 2 and height 4.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

# The upper surface is y = 8 - radius**2, so its constant term is 8.
UPPER_SURFACE_CONSTANT = 8.0
# The two surfaces meet at radius 2 and at height 4.
MEETING_RADIUS = 2.0
MEETING_HEIGHT = 4.0
# The plotting window of the radius axis.
RADIUS_MINIMUM = -2.6
RADIUS_MAXIMUM = 2.6
# The output file of the figure.
OUTPUT_PATH = "code/figures/part1_figure1.png"


def main() -> None:
    """Draw the cross section and write the figure file."""
    radius = np.linspace(RADIUS_MINIMUM, RADIUS_MAXIMUM, 800)
    lower_height = radius**2
    upper_height = UPPER_SURFACE_CONSTANT - radius**2

    figure, axes = plt.subplots(figsize=(7.2, 4.6))
    axes.plot(radius, lower_height, color="#1f4e79", linewidth=2.0, label=r"$y = x^{2} + z^{2}$")
    axes.plot(radius, upper_height, color="#a33a2a", linewidth=2.0, label=r"$y = 8 - x^{2} - z^{2}$")

    inside = np.abs(radius) <= MEETING_RADIUS
    axes.fill_between(
        radius,
        lower_height,
        upper_height,
        where=inside,
        color="#8fb8d8",
        alpha=0.45,
        label="enclosed cross section",
    )

    axes.plot([MEETING_RADIUS, -MEETING_RADIUS], [MEETING_HEIGHT, MEETING_HEIGHT], "o", color="#222222", markersize=6)
    axes.plot([0.0], [UPPER_SURFACE_CONSTANT], "o", color="#222222", markersize=5)
    axes.annotate(
        r"meeting curve: $r = 2$, $y = 4$",
        xy=(MEETING_RADIUS, MEETING_HEIGHT),
        xytext=(0.55, 6.6),
        fontsize=11,
        arrowprops={"arrowstyle": "->", "color": "#222222"},
    )
    axes.annotate(
        r"top point: $y = 8$",
        xy=(0.0, UPPER_SURFACE_CONSTANT),
        xytext=(-2.5, 7.15),
        fontsize=11,
        arrowprops={"arrowstyle": "->", "color": "#222222"},
    )
    axes.annotate(
        r"bottom point: $y = 0$",
        xy=(0.0, 0.0),
        xytext=(-2.45, 1.55),
        fontsize=11,
        arrowprops={"arrowstyle": "->", "color": "#222222"},
    )
    axes.axvline(MEETING_RADIUS, color="#666666", linestyle=":", linewidth=1.0)
    axes.axvline(-MEETING_RADIUS, color="#666666", linestyle=":", linewidth=1.0)
    axes.set_xlim(RADIUS_MINIMUM, RADIUS_MAXIMUM)
    axes.set_ylim(-0.5, 9.2)
    axes.set_xlabel(r"radius $r$ in the plane $y = \mathrm{constant}$  (with $r^{2} = x^{2} + z^{2}$)")
    axes.set_ylabel(r"height $y$")
    axes.set_title(r"Cross section of the solid: $r^{2} \leq y \leq 8 - r^{2}$")
    axes.grid(True, color="#dddddd", linewidth=0.6)
    axes.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3, fontsize=10,
                frameon=False)
    figure.tight_layout()
    figure.savefig(OUTPUT_PATH, dpi=200)
    plt.close(figure)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
