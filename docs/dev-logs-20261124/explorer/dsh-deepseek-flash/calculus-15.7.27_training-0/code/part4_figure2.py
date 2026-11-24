"""Figure of Part 3: the base of the solid, seen from above.

The panel shows the base triangle in the xz-plane, the three walls as the three
edges of the triangle, the level line at a constant value of z, and the point
where the height bar of Figure 1 stands. Every drawn triangle comes from
`region_tools.slice_polygon("y", 0)`.
"""

from fractions import Fraction

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PolygonPatch

import figure_anchors
import region_tools as region

FIGURE_PATH = "code/figures/part4_figure2.png"
"""Path of the figure file, relative to the workspace."""

LEVEL = figure_anchors.HEIGHT_SAMPLE_Z
"""The value of z that the dashed level line holds."""

LEVEL_UPPER = Fraction(1) - LEVEL
"""The value of x where the level line meets the wall x + z = 1."""

POINT = (figure_anchors.HEIGHT_SAMPLE_X, LEVEL)
"""The point of the base where the height bar stands, in the xz-plane."""


def fraction_text(value: Fraction) -> str:
    """Return a fraction as LaTeX source."""
    if value.denominator == 1:
        return str(value.numerator)
    return rf"\frac{{{value.numerator}}}{{{value.denominator}}}"


def main() -> None:
    """Draw the projection panel and write the figure file."""
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Cambria", "DejaVu Serif"]
    plt.rcParams["mathtext.fontset"] = "stix"
    figure, axes = plt.subplots(figsize=(6.4, 5.4))
    triangle = region.slice_polygon("y", Fraction(0))
    points = [(float(point[0]), float(point[1])) for point in triangle]
    axes.add_patch(
        PolygonPatch(points, closed=True, facecolor="#9ecbe8", edgecolor="#17324a", linewidth=1.9, alpha=0.85)
    )
    for point in points:
        axes.plot(point[0], point[1], marker="o", color="#17324a", markersize=5, clip_on=False, zorder=5)
    names = {point: name for name, point in figure_anchors.VERTEX_NAMES}
    corner_offsets = {
        "P0": (-16, -14),
        "P1": (8, -14),
        "P2": (-18, 6),
    }
    for point in points:
        corner = (Fraction(point[0]).limit_denominator(8), Fraction(0), Fraction(point[1]).limit_denominator(8))
        name = names[corner]
        axes.annotate(
            name,
            xy=point,
            xytext=corner_offsets[name],
            textcoords="offset points",
            fontsize=10,
            color="#17324a",
        )
    level_start = (0.0, float(LEVEL))
    level_end = (float(LEVEL_UPPER), float(LEVEL))
    axes.plot(
        [level_start[0], level_end[0]],
        [level_start[1], level_end[1]],
        color="#9c2f1c",
        linewidth=1.4,
        linestyle=(0, (5, 3)),
    )
    axes.annotate(
        r"width $1-z$",
        xy=((level_start[0] + level_end[0]) / 2.0, float(LEVEL)),
        xytext=(0, 8),
        textcoords="offset points",
        fontsize=10,
        color="#9c2f1c",
        horizontalalignment="center",
    )
    axes.plot(POINT[0], float(POINT[1]), marker="o", color="#9c2f1c", markersize=7, zorder=6)
    axes.annotate(
        r"height $2-2z$",
        xy=(float(POINT[0]), float(POINT[1])),
        xytext=(10, -14),
        textcoords="offset points",
        fontsize=10,
        color="#9c2f1c",
    )
    axes.annotate(
        r"$x+z=1$",
        xy=(0.72, 0.28),
        xytext=(8, 4),
        textcoords="offset points",
        fontsize=10.5,
        color="#17324a",
    )
    axes.annotate(
        r"$z=0$",
        xy=(0.5, 0.0),
        xytext=(0, -14),
        textcoords="offset points",
        fontsize=10.5,
        color="#17324a",
        horizontalalignment="center",
    )
    axes.annotate(
        r"$x=0$",
        xy=(0.0, 0.62),
        xytext=(-10, 0),
        textcoords="offset points",
        fontsize=10.5,
        color="#17324a",
        horizontalalignment="right",
    )
    axes.set_xlabel(r"$x$")
    axes.set_ylabel(r"$z$")
    title = "The base triangle in the plane $y=0$, and the level line $z = " + fraction_text(LEVEL) + "$"
    axes.set_title(title, fontsize=10.5)
    axes.set_aspect("equal")
    axes.set_xlim(-0.16, 1.20)
    axes.set_ylim(-0.16, 1.16)
    axes.grid(True, linestyle=":", linewidth=0.6, color="#bbbbbb")
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=190, bbox_inches="tight")
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
