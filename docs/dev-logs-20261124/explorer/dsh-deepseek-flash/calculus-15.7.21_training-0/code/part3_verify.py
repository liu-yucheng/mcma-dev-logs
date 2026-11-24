"""Check the shape and the area of the cross-section at a fixed value of x.

The cross-section at x = x0 is the set of points (y, z) that satisfies the
three conditions of the statement with x fixed. The script measures this set
in five independent ways at three abscissas.

1. The set of points equals the closed triangle with three named vertices.
2. The area from a rejection sample of the set.
3. The area from an integral of the vertical extent of the set.
4. The area from the surveyor formula on the three vertices.
5. The area from the closed form (1 - x0^2)^2 / 2 of Part 3.

Run this script with: code/.venv/Scripts/python.exe code/part3_verify.py
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import quad
from scipy.spatial import ConvexHull

RANDOM_SEED = 20261122
"""Seed of the random number generator of this script."""

SAMPLE_COUNT = 2_000_000
"""Number of random points in each rejection sample."""

TRIANGLE_POINT_COUNT = 200_000
"""Number of random points in each shape test."""

ABSCISSAS = (0.0, 0.5, 0.9)
"""Three abscissas where the script measures the cross-section."""

MAXIMUM_AREA = 0.5
"""Largest cross-section area over the solid, at x = 0."""

EXACT_TOLERANCE = 1.0e-12
"""Largest accepted difference between two exact formulas."""


def report(name: str, computed: float, expected: float, tolerance: float) -> None:
    """Print one check line, and stop the script when the check fails.

    Args:
        name: Short name of the check.
        computed: Value that the script measured.
        expected: Value that the derivation predicts.
        tolerance: Largest accepted absolute difference.

    Returns:
        None.
    """
    difference = abs(computed - expected)
    passed = difference <= tolerance
    verdict = "PASS" if passed else "FAIL"
    print(
        f"{name}: computed = {computed:.12g}, expected = {expected:.12g}, "
        f"difference = {difference:.3e}, tolerance = {tolerance:.3e}, {verdict}"
    )
    if not passed:
        raise SystemExit(f"FAILED CHECK: {name}")


def closed_form_area(x_value: float) -> float:
    """Return the area (1 - x^2)^2 / 2 of the cross-section at x.

    Args:
        x_value: Fixed x coordinate.

    Returns:
        The area of the cross-section.
    """
    return (1.0 - x_value * x_value) ** 2 / 2.0


def vertices(x_value: float) -> np.ndarray:
    """Return the three vertices of the cross-section in the (y, z) plane.

    Args:
        x_value: Fixed x coordinate.

    Returns:
        An array of shape (3, 2) with the points (y, z).
    """
    floor_left = (x_value * x_value, 0.0)
    floor_right = (1.0, 0.0)
    roof_left = (x_value * x_value, 1.0 - x_value * x_value)
    return np.array([floor_left, floor_right, roof_left])


def inside_triangle(x_value: float, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return True where (y, z) lies in the closed triangle of three vertices.

    The test uses barycentric coordinates of the three vertices. The test does
    not read the inequalities of the solid.

    Args:
        x_value: Fixed x coordinate.
        y: Array of y coordinates.
        z: Array of z coordinates.

    Returns:
        A Boolean array of the same shape as the input arrays.
    """
    corner = vertices(x_value)
    first_edge = corner[1] - corner[0]
    second_edge = corner[2] - corner[0]
    determinant = first_edge[0] * second_edge[1] - first_edge[1] * second_edge[0]
    offset_y = y - corner[0, 0]
    offset_z = z - corner[0, 1]
    weight_one = (offset_y * second_edge[1] - offset_z * second_edge[0]) / determinant
    weight_two = (first_edge[0] * offset_z - first_edge[1] * offset_y) / determinant
    return (weight_one >= 0.0) & (weight_two >= 0.0) & (weight_one + weight_two <= 1.0)


def inside_solid_section(x_value: float, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return True where (y, z) satisfies the three conditions at fixed x.

    Args:
        x_value: Fixed x coordinate.
        y: Array of y coordinates.
        z: Array of z coordinates.

    Returns:
        A Boolean array of the same shape as the input arrays.
    """
    return (y >= x_value * x_value) & (y <= 1.0) & (z >= 0.0) & (z <= 1.0 - y)


def rejection_area(x_value: float, generator: np.random.Generator) -> float:
    """Return the area of the cross-section from a rejection sample.

    The sample box is [x^2, 1] x [0, 1 - x^2]. The box comes from the
    conditions y <= 1 and 0 <= z <= 1 - y, and from no other source.

    Args:
        x_value: Fixed x coordinate.
        generator: Random number generator.

    Returns:
        The measured area.
    """
    low_y, high_y = x_value * x_value, 1.0
    low_z, high_z = 0.0, 1.0 - x_value * x_value
    box_area = (high_y - low_y) * (high_z - low_z)
    y = generator.uniform(low_y, high_y, SAMPLE_COUNT)
    z = generator.uniform(low_z, high_z, SAMPLE_COUNT)
    hits = np.count_nonzero(inside_solid_section(x_value, y, z))
    return box_area * hits / SAMPLE_COUNT


def rejection_standard_error(x_value: float) -> float:
    """Return the standard error of the rejection area at one abscissa.

    Args:
        x_value: Fixed x coordinate.

    Returns:
        The standard error of the measured area.
    """
    box_area = (1.0 - x_value * x_value) ** 2
    probability = closed_form_area(x_value) / box_area
    return box_area * np.sqrt(probability * (1.0 - probability) / SAMPLE_COUNT)


def integrated_area(x_value: float) -> float:
    """Return the area from the integral of the vertical extent over y.

    The vertical extent at a fixed y is the length of the z interval that the
    conditions admit.

    Args:
        x_value: Fixed x coordinate.

    Returns:
        The area of the cross-section.
    """
    value, _ = quad(lambda y: (1.0 - y) - 0.0, x_value * x_value, 1.0)
    return float(value)


def surveyor_area(x_value: float) -> float:
    """Return the area of the cross-section from the surveyor formula.

    Args:
        x_value: Fixed x coordinate.

    Returns:
        The area of the triangle with the three vertices of the cross-section.
    """
    corner = vertices(x_value)
    total = 0.0
    for index in range(3):
        next_index = (index + 1) % 3
        total += corner[index, 0] * corner[next_index, 1] - corner[next_index, 0] * corner[index, 1]
    return abs(total) / 2.0


def main() -> None:
    """Run every check of Part 3 and print one line for each check."""
    generator = np.random.default_rng(RANDOM_SEED)
    print("shape test: the cross-section equals the closed triangle of three vertices")
    for x_value in ABSCISSAS:
        y = generator.uniform(x_value * x_value - 0.3, 1.3, TRIANGLE_POINT_COUNT)
        z = generator.uniform(-0.3, 1.3, TRIANGLE_POINT_COUNT)
        from_conditions = inside_solid_section(x_value, y, z)
        from_triangle = inside_triangle(x_value, y, z)
        disagreement_count = np.count_nonzero(from_conditions != from_triangle)
        report(f"  disagreements at x = {x_value}", float(disagreement_count), 0.0, 0.0)
        hull = ConvexHull(vertices(x_value))
        report(f"  corner count at x = {x_value}", float(hull.vertices.size), 3.0, 0.0)

    print("")
    print("area of the cross-section at three abscissas")
    for x_value in ABSCISSAS:
        expected = closed_form_area(x_value)
        measured = rejection_area(x_value, generator)
        allowed = 4.0 * rejection_standard_error(x_value)
        report(f"  rejection area at x = {x_value}", measured, expected, allowed)
        standard_error = rejection_standard_error(x_value)
        difference = abs(measured - expected)
        print(f"    standard error = {standard_error:.3e}, difference = {difference:.3e}")
        report(f"  integrated area at x = {x_value}", integrated_area(x_value), expected, EXACT_TOLERANCE)
        report(f"  surveyor area at x = {x_value}", surveyor_area(x_value), expected, EXACT_TOLERANCE)

    print("")
    print("the largest cross-section area over the solid")
    grid = np.linspace(-1.0, 1.0, 200_001)
    values = (1.0 - grid * grid) ** 2 / 2.0
    report("  largest area on the grid", float(values.max()), MAXIMUM_AREA, 1.0e-9)
    report("  abscissa of the largest area", float(grid[int(np.argmax(values))]), 0.0, 1.0e-5)
    print(f"    largest area divided by pi = {MAXIMUM_AREA / np.pi:.12g} (this is not a disc)")

    print("")
    print("the cross-section closes to a point at the two ends of the x range")
    report("  area at x = -1", closed_form_area(-1.0), 0.0, EXACT_TOLERANCE)
    report("  area at x = 1", closed_form_area(1.0), 0.0, EXACT_TOLERANCE)


if __name__ == "__main__":
    main()
