"""Draw the integrand of the radius integral and the area that it encloses.

The radius integral is the integral from 0 to 2 of 8 * radius - 2 * radius**3.
The area under the curve is 8, and the angle integral supplies the factor 2 * pi.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

# The projection of the solid is the disk of radius 2.
PROJECTION_RADIUS = 2.0
# The radius integral over 0 to 2 has the value 8.
EXPECTED_RADIUS_INTEGRAL = 8.0
# The output file of the figure.
OUTPUT_PATH = "code/figures/part3_figure1.png"


def radius_integrand(radius: float) -> float:
    """Return the integrand 8 * radius - 2 * radius**3 of the radius integral."""
    return 8.0 * radius - 2.0 * radius**3


def main() -> None:
    """Draw the integrand and write the figure file."""
    radius = np.linspace(0.0, PROJECTION_RADIUS, 500)
    values = radius_integrand(radius)

    figure, axes = plt.subplots(figsize=(7.2, 4.4))
    axes.fill_between(radius, 0.0, values, color="#8fb8d8", alpha=0.45)
    axes.plot(radius, values, color="#1f4e79", linewidth=2.2)
    axes.axhline(0.0, color="#555555", linewidth=0.9)
    axes.plot([PROJECTION_RADIUS], [radius_integrand(PROJECTION_RADIUS)], "o", color="#222222", markersize=6)
    axes.text(0.62, 3.05, r"area $=\int_{0}^{2}\left(8r-2r^{3}\right)dr = 8$", fontsize=12)
    axes.text(0.30, 1.10, r"$r\left(8-2r^{2}\right)$", fontsize=12, color="#1f4e79")
    axes.annotate(
        r"$r = 2$: the integrand returns to $0$",
        xy=(PROJECTION_RADIUS, 0.0),
        xytext=(1.02, 1.45),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "#222222"},
    )
    axes.set_xlim(0.0, 2.25)
    axes.set_ylim(-0.6, 6.6)
    axes.set_xlabel(r"radius $r$")
    axes.set_ylabel(r"integrand $r\left(8 - 2r^{2}\right)$")
    axes.set_title(r"Radius integral: the weight of each polar ring")
    axes.grid(True, color="#dddddd", linewidth=0.6)
    figure.tight_layout()
    figure.savefig(OUTPUT_PATH, dpi=200)
    plt.close(figure)
    print(f"wrote {OUTPUT_PATH}; the radius integral is {EXPECTED_RADIUS_INTEGRAL}")


if __name__ == "__main__":
    main()
