"""Figure of Part 2: the three cross sections of the solid.

Every drawn polygon comes from `region_tools.slice_polygon`, so the picture
follows the inequalities. The name and the area in each panel title come from
`region_tools.name_polygon` and `region_tools.polygon_area`, so no label of
the figure is written by hand. Each edge label is attached to the edge whose
own corners satisfy the equation of that label.
"""

from fractions import Fraction

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PolygonPatch

import region_tools as region

SAMPLES: tuple[tuple[str, Fraction], ...] = (
    ("z", Fraction(1, 2)),
    ("x", Fraction(1, 2)),
    ("y", Fraction(1)),
)
"""The slicing variable and the value of each panel."""

COORDINATE_RULE = "coordinate"
"""Rule kind: both corners of the edge hold one coordinate equal to a value."""

LINEAR_RULE = "linear"
"""Rule kind: both corners of the edge satisfy a linear equation of the panel."""

TOLERANCE = 1.0e-9
"""Tolerance of the test that selects the edge of a label."""


def coordinate_rule(label: str, index: int, target) -> tuple:
    """Build a rule that selects the edge with one fixed coordinate."""
    return (label, COORDINATE_RULE, (index, target))


def linear_rule(label: str, coefficients: tuple[float, float], constant: float) -> tuple:
    """Build a rule that selects the edge where a·u + b·v equals a constant."""
    return (label, LINEAR_RULE, (coefficients, constant))


def edge_rules(axis: str, value: Fraction) -> tuple[tuple, ...]:
    """Return the label rules of one panel, with the value of the panel built in."""
    number = float(value)
    if axis == "z":
        return (
            coordinate_rule(r"$1-z$", 1, 0.0),
            coordinate_rule(r"$2-2z$", 0, 0.0),
        )
    if axis == "x":
        return (
            coordinate_rule(r"$1-x$", 1, 0.0),
            coordinate_rule(r"$2x$", 0, 1.0 - number),
            linear_rule(r"$y = 2-2z$", (2.0, 1.0), 2.0),
        )
    return (
        coordinate_rule(r"$1-y/2$", 1, 1.0 - number / 2.0),
        linear_rule(r"$x+z=1$", (1.0, 1.0), 1.0),
    )


FIGURE_PATH = "code/figures/part2_figure1.png"
"""Path of the figure file, relative to the workspace."""


def fraction_text(value: Fraction) -> str:
    """Return a fraction as LaTeX source."""
    if value.denominator == 1:
        return str(value.numerator)
    return rf"\frac{{{value.numerator}}}{{{value.denominator}}}"


def edge_matches(rule: tuple, first: tuple[float, float], second: tuple[float, float]) -> bool:
    """Return True when both corners of an edge satisfy the rule of a label."""
    _, kind, payload = rule
    if kind == COORDINATE_RULE:
        index, target = payload
        return abs(first[index] - target) < TOLERANCE and abs(second[index] - target) < TOLERANCE
    coefficients, constant = payload
    first_value = coefficients[0] * first[0] + coefficients[1] * first[1]
    second_value = coefficients[0] * second[0] + coefficients[1] * second[1]
    return abs(first_value - constant) < TOLERANCE and abs(second_value - constant) < TOLERANCE


def label_edges(axes, axis: str, value: Fraction, points: list[tuple[float, float]]) -> None:
    """Place each edge label on the edge that its own equation selects."""
    count = len(points)
    used: set[int] = set()
    for rule in edge_rules(axis, value):
        for index in range(count):
            if index in used:
                continue
            first = points[index]
            second = points[(index + 1) % count]
            if not edge_matches(rule, first, second):
                continue
            middle = ((first[0] + second[0]) / 2.0, (first[1] + second[1]) / 2.0)
            offset = (0, 9) if abs(first[1] - second[1]) < TOLERANCE else (8, 7)
            axes.annotate(
                rule[0],
                xy=middle,
                xytext=offset,
                textcoords="offset points",
                fontsize=10,
                color="#8a4b00",
                horizontalalignment="center" if offset[0] == 0 else "left",
                verticalalignment="center" if offset[0] != 0 else "bottom",
            )
            used.add(index)
            break
        else:
            raise AssertionError(f"the panel at constant {axis} has no edge for the label {rule[0]}")


def draw_panel(axes, axis: str, value: Fraction) -> None:
    """Draw one cross section with its corners, its edge labels, and its area."""
    polygon = region.slice_polygon(axis, value)
    shape = region.name_polygon(region.describe_polygon(polygon))
    area = region.polygon_area(polygon)
    points = [(float(point[0]), float(point[1])) for point in polygon]
    axes.add_patch(
        PolygonPatch(points, closed=True, facecolor="#cfe3f3", edgecolor="#1f4e79", linewidth=1.8, alpha=0.9)
    )
    for point in points:
        axes.plot(point[0], point[1], marker="o", color="#1f4e79", markersize=4.5, clip_on=False, zorder=5)
    horizontal_axis, vertical_axis = region.PLANE_AXES[axis]
    axes.set_xlabel(rf"${horizontal_axis}$")
    axes.set_ylabel(rf"${vertical_axis}$")
    axes.set_title(
        rf"constant ${axis} = {fraction_text(value)}$: {shape}" "\n" rf"area $= {fraction_text(area)}$",
        fontsize=10.5,
    )
    axes.set_aspect("equal")
    axes.grid(True, linestyle=":", linewidth=0.6, color="#bbbbbb")
    horizontal = [point[0] for point in points]
    vertical = [point[1] for point in points]
    axes.set_xlim(0.0, max(horizontal) * 1.26 + 0.06)
    axes.set_ylim(0.0, max(vertical) * 1.14 + 0.06)
    axes.axhline(0.0, color="#666666", linewidth=0.9)
    axes.axvline(0.0, color="#666666", linewidth=0.9)
    label_edges(axes, axis, value, points)
    axes.tick_params(labelsize=8.5)


def main() -> None:
    """Draw the three panels and write the figure file."""
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Cambria", "DejaVu Serif"]
    plt.rcParams["mathtext.fontset"] = "stix"
    figure, axes_row = plt.subplots(1, 3, figsize=(10.4, 3.9))
    for axes, (axis, value) in zip(axes_row, SAMPLES):
        draw_panel(axes, axis, value)
    figure.suptitle("Cross sections of the solid, clipped from the six limits", fontsize=12)
    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=190, bbox_inches="tight")
    print(f"wrote {FIGURE_PATH}")


if __name__ == "__main__":
    main()
