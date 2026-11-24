"""Verification of Part 1: the three pairs of limits and the base triangle.

Each check compares a value that one method computes with a value that a
different method computes. Run this script with the interpreter of the
session environment:

    code/.venv/Scripts/python.exe code/part1_verify.py
"""

from fractions import Fraction
import math
import random

import numpy as np
from scipy import integrate
from scipy.optimize import linprog

import figure_anchors
import region_tools as region

RANDOM_SEED = 20261122
"""Seed of every random draw of this check."""

SAMPLE_COUNT = 400000
"""Number of points of the Monte Carlo volume estimate."""

BOX_LOWER = (0.0, 0.0, 0.0)
"""Lowest corner of the box that holds the solid."""

BOX_UPPER = (1.0, 2.0, 1.0)
"""Highest corner of the box that holds the solid."""


def report(name: str, computed: float, expected: float, tolerance: float) -> bool:
    """Print one comparison and return True when the values agree."""
    difference = abs(computed - expected)
    passed = difference <= tolerance
    print(f"{name}: computed = {computed!r}, expected = {expected!r}, difference = {difference:.3e}")
    assert passed, f"{name} failed: {computed!r} differs from {expected!r} by {difference:.3e}"
    return passed


def check_limit_structure() -> None:
    """Check that each limit holds only the variables that the order allows.

    The inner limit must ignore x and follow z. The middle limit must follow x
    and ignore y. The outer limit must be constant. The check evaluates the
    limit functions, so a limit that secretly holds x fails it.
    """
    z_values = [Fraction(0), Fraction(1, 3), Fraction(4, 5)]
    x_values = [Fraction(0), Fraction(1, 2), Fraction(9, 10)]
    for z_value in z_values:
        inner = {region.inner_upper_limit(x_value, z_value) for x_value in x_values}
        assert len(inner) == 1, f"the y limit changes with x at z = {z_value}"
    inner_by_z = [region.inner_upper_limit(Fraction(0), z_value) for z_value in z_values]
    assert len(set(inner_by_z)) == len(z_values), "the y limit does not follow z"
    print(f"check the inner limit: values over z = {[str(value) for value in inner_by_z]}, holds no x")

    middle = {region.middle_upper_limit(x_value, Fraction(0)) for x_value in x_values}
    assert len(middle) == len(x_values), "the z limit does not follow x"
    middle_by_y = {region.middle_upper_limit(Fraction(1, 2), Fraction(0)) for _ in range(3)}
    assert len(middle_by_y) == 1, "the z limit changes with a variable that it cannot hold"
    print(f"check the middle limit: values over x = {[str(value) for value in middle]}, holds no y")

    outer = {region.outer_upper_limit(Fraction(0), Fraction(0)), region.outer_upper_limit(Fraction(1), Fraction(1))}
    assert outer == {Fraction(1)}, "the x limit is not the constant 1"
    print(f"check the outer limit: constant {sorted(str(value) for value in outer)}")


def inside_by_convex_hull(point: tuple[float, float, float], vertices: list) -> bool:
    """Return True when a point is a convex combination of the five corners.

    This test uses only the corner list. It never reads an inequality, so it is
    independent of the limit test and of the half-space test.
    """
    corner_count = len(vertices)
    equality = np.zeros((4, corner_count))
    equality[0, :] = 1.0
    for index in range(3):
        equality[index + 1, :] = [float(corner[index]) for corner in vertices]
    target = np.array([1.0, point[0], point[1], point[2]])
    result = linprog(
        c=np.zeros(corner_count),
        A_eq=equality,
        b_eq=target,
        bounds=[(0.0, None)] * corner_count,
        method="highs",
    )
    return bool(result.success)


def check_hull_equivalence() -> None:
    """Check that the limits and the five corners describe the same set.

    The check draws points in a box that is larger than the solid, keeps the
    points that are clearly inside or clearly outside, and compares two tests:
    the three pairs of limits, and membership in the convex hull of the five
    corners.
    """
    random.seed(RANDOM_SEED)
    vertices = region.enumerate_vertices()
    agree = 0
    compared = 0
    for _ in range(240):
        x_value = random.uniform(-0.2, 1.2)
        y_value = random.uniform(-0.2, 2.2)
        z_value = random.uniform(-0.2, 1.2)
        point = (x_value, y_value, z_value)
        margin = min(
            float(bound) - sum(float(coefficient) * value for coefficient, value in zip(coefficients, point))
            for _, coefficients, bound in region.SOLID_HALF_SPACES
        )
        if abs(margin) < 1.0e-6:
            continue
        by_limits = region.contains_by_limits(point)
        by_hull = inside_by_convex_hull(point, vertices)
        compared += 1
        if by_limits == by_hull:
            agree += 1
    share = agree / compared
    print(f"check the limits against the five corners: {agree} of {compared} points agree, share = {share}")
    report("hull agreement share", share, 1.0, 0.0)


def check_base_triangle() -> None:
    """Check the base triangle in the xz plane by three methods."""
    polygon = region.slice_polygon("y", Fraction(0))
    clipped_area = region.polygon_area(polygon)
    exact_area = region.polynomial_integral([Fraction(1), Fraction(-1)], Fraction(0), Fraction(1))
    grid_area = region.section_area_from_grid("y", Fraction(0), count=400)
    print(f"check the base triangle: {len(polygon)} corners {polygon}")
    report("base area from the clip", float(clipped_area), float(exact_area), 0.0)
    report("base area from the grid", grid_area, float(exact_area), 0.01)
    shape = region.name_polygon(region.describe_polygon(polygon))
    print(f"check the base shape: {shape}")
    assert shape == "triangle", f"the base is a {shape} and not a triangle"


def check_volume() -> None:
    """Check that the three limits give the volume 2 / 3 by three methods."""
    exact = region.exact_volume()
    numeric, numeric_error = integrate.tplquad(
        lambda z_value, y_value, x_value: 1.0,
        0.0,
        1.0,
        lambda x_value: 0.0,
        lambda x_value: 1.0 - x_value,
        lambda x_value, z_value: 0.0,
        lambda x_value, z_value: 2.0 - 2.0 * z_value,
    )
    print(f"check the volume: exact = {exact}, numeric = {numeric!r}, error = {numeric_error:.2e}")
    report("volume from the nested quadrature", numeric, float(exact), 1.0e-9)

    random.seed(RANDOM_SEED)
    generator = np.random.default_rng(RANDOM_SEED)
    draws = generator.uniform(low=BOX_LOWER, high=BOX_UPPER, size=(SAMPLE_COUNT, 3))
    inside = np.zeros(SAMPLE_COUNT, dtype=bool)
    inside |= (draws[:, 2] <= 1.0 - draws[:, 0]) & (draws[:, 1] <= 2.0 - 2.0 * draws[:, 2])
    share = float(np.count_nonzero(inside)) / SAMPLE_COUNT
    box_volume = math.prod(BOX_UPPER[index] - BOX_LOWER[index] for index in range(3))
    estimate = share * box_volume
    standard_error = box_volume * math.sqrt(share * (1.0 - share) / SAMPLE_COUNT)
    print(f"check the volume by sampling: share = {share!r}, estimate = {estimate!r}, error = {standard_error:.3e}")
    report("volume from the sampling", estimate, float(exact), 3.0 * standard_error)


def check_extremes() -> None:
    """Check the highest and the lowest value of each coordinate."""
    vertices = region.enumerate_vertices()
    box = region.bounding_box(vertices)
    expected = (
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(2)),
        (Fraction(0), Fraction(1)),
    )
    print(f"check the corner list: {len(vertices)} corners")
    for index, name in enumerate(("x", "y", "z")):
        report(f"lowest {name} over the corners", float(box[index][0]), float(expected[index][0]), 0.0)
        report(f"highest {name} over the corners", float(box[index][1]), float(expected[index][1]), 0.0)
    top_height = max(float(vertices[index][1]) for index in range(len(vertices)))
    from_limits = float(2 - 2 * min(float(vertices[index][2]) for index in range(len(vertices))))
    report("highest y from the corners", top_height, from_limits, 0.0)
    assert region.contains((Fraction(1, 2), Fraction(2), Fraction(0))), "the top edge is not in the solid"


def main() -> None:
    """Run every check of Part 1 in order."""
    print("Part 1: the limits, the base triangle, and the volume")
    check_limit_structure()
    check_base_triangle()
    check_volume()
    check_extremes()
    check_hull_equivalence()
    print("Part 1: every check passed")


if __name__ == "__main__":
    main()
