"""Check the volume of the solid in six independent ways.

1. Exact rational arithmetic on the antiderivative of the cross-section area.
2. One dimensional quadrature of the cross-section area over x.
3. Two dimensional quadrature over the projection.
4. A trapezoid rule on a fine grid over x.
5. A rejection sample of the bounding box.
6. A second order of integration, which slices the solid at a fixed y.

The script also checks two bounds that the volume must obey, and it measures
the area of three slices at fixed y.

Run this script with: code/.venv/Scripts/python.exe code/part4_verify.py
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.integrate import dblquad, quad

RANDOM_SEED = 20261122
"""Seed of the random number generator of this script."""

SAMPLE_COUNT = 4_000_000
"""Number of random points in the rejection sample of the bounding box."""

SLICE_SAMPLE_COUNT = 2_000_000
"""Number of random points in each slice measurement."""

VOLUME_EXACT = Fraction(8, 15)
"""Exact volume of the solid in cubic units."""

VOLUME_FLOAT = float(VOLUME_EXACT)
"""Volume of the solid as a floating point number."""

QUADRATURE_TOLERANCE = 1.0e-12
"""Largest accepted difference between the exact value and a quadrature."""

GRID_TOLERANCE = 1.0e-9
"""Largest accepted difference between the exact value and the trapezoid rule."""


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
        f"{name}: computed = {computed:.15g}, expected = {expected:.15g}, "
        f"difference = {difference:.3e}, tolerance = {tolerance:.3e}, {verdict}"
    )
    if not passed:
        raise SystemExit(f"FAILED CHECK: {name}")


def report_lower_bound(name: str, computed: float, bound: float) -> None:
    """Print one lower bound check, and stop the script when the check fails.

    Args:
        name: Short name of the check.
        computed: Value that the script measured.
        bound: Value that the computed value must exceed.

    Returns:
        None.
    """
    passed = computed > bound
    verdict = "PASS" if passed else "FAIL"
    print(f"{name}: computed = {computed:.15g}, bound = {bound:.15g}, margin = {computed - bound:.3e}, {verdict}")
    if not passed:
        raise SystemExit(f"FAILED CHECK: {name}")


def report_upper_bound(name: str, computed: float, bound: float) -> None:
    """Print one upper bound check, and stop the script when the check fails.

    Args:
        name: Short name of the check.
        computed: Value that the script measured.
        bound: Value that must exceed the computed value.

    Returns:
        None.
    """
    passed = computed < bound
    verdict = "PASS" if passed else "FAIL"
    print(f"{name}: computed = {computed:.15g}, bound = {bound:.15g}, margin = {bound - computed:.3e}, {verdict}")
    if not passed:
        raise SystemExit(f"FAILED CHECK: {name}")


def cross_section_area(x: float) -> float:
    """Return the area of the cross-section at a fixed x.

    Args:
        x: Fixed x coordinate.

    Returns:
        The area (1 - x^2)^2 / 2.
    """
    return (1.0 - x * x) ** 2 / 2.0


def exact_volume_from_antiderivative() -> Fraction:
    """Return the volume from exact arithmetic on the antiderivative.

    The integrand is the polynomial 1/2 - x^2 + x^4/2. Its antiderivative is
    x/2 - x^3/3 + x^5/10. The script evaluates this function at both end points.

    Returns:
        The exact volume.
    """
    def antiderivative(x_value: Fraction) -> Fraction:
        """Return x/2 - x^3/3 + x^5/10 at an exact value."""
        return x_value / 2 - x_value ** 3 / 3 + x_value ** 5 / 10

    return antiderivative(Fraction(1)) - antiderivative(Fraction(-1))


def exact_volume_from_y_slices() -> Fraction:
    """Return the volume from exact arithmetic on the slices at a fixed y.

    The slice at a fixed y is the rectangle sqrt(y) wide on each side and 1 - y
    tall, so its area is 2 sqrt(y) (1 - y). The integral of this area over y is
    4/3 - 4/5.

    Returns:
        The exact volume.
    """
    first_term = Fraction(4, 3)
    second_term = Fraction(4, 5)
    return first_term - second_term


def slice_area(y: float) -> float:
    """Return the area of the slice at a fixed y.

    Args:
        y: Fixed y coordinate.

    Returns:
        The area 2 sqrt(y) (1 - y).
    """
    return 2.0 * np.sqrt(y) * (1.0 - y)


def rejection_area_at_fixed_y(y_value: float, generator: np.random.Generator) -> float:
    """Return the area of the slice at a fixed y from a rejection sample.

    The sample box is [-1, 1] x [0, 1] in the (x, z) plane. The box is larger
    than the slice, so the measured area is a fraction of the box area and not
    the box area itself.

    Args:
        y_value: Fixed y coordinate.
        generator: Random number generator.

    Returns:
        The measured area of the slice in the (x, z) plane.
    """
    box_area = 2.0
    x = generator.uniform(-1.0, 1.0, SLICE_SAMPLE_COUNT)
    z = generator.uniform(0.0, 1.0, SLICE_SAMPLE_COUNT)
    hits = np.count_nonzero(
        (np.abs(x) <= np.sqrt(y_value)) & (z >= 0.0) & (z <= 1.0 - y_value)
    )
    return box_area * hits / SLICE_SAMPLE_COUNT


def main() -> None:
    """Run every check of Part 4 and print one line for each check."""
    generator = np.random.default_rng(RANDOM_SEED)
    print("the exact value")
    print(f"  volume = {VOLUME_EXACT} = {VOLUME_FLOAT:.15g} cubic units")

    print("")
    print("independent evaluations of the volume")
    report("antiderivative, exact rational arithmetic", float(exact_volume_from_antiderivative()), VOLUME_FLOAT, 0.0)
    report("quadrature of the cross-section area over x",
           float(quad(cross_section_area, -1.0, 1.0)[0]), VOLUME_FLOAT, QUADRATURE_TOLERANCE)
    report("two dimensional quadrature over the projection",
           float(dblquad(lambda y, x: 1.0 - y, -1.0, 1.0, lambda x: x * x, lambda x: 1.0)[0]),
           VOLUME_FLOAT, QUADRATURE_TOLERANCE)
    report("quadrature of the slices at a fixed y",
           float(quad(slice_area, 0.0, 1.0)[0]), VOLUME_FLOAT, QUADRATURE_TOLERANCE)
    report("exact arithmetic on the slices at a fixed y", float(exact_volume_from_y_slices()), VOLUME_FLOAT, 0.0)

    grid = np.linspace(-1.0, 1.0, 1_600_001)
    trapezoid_value = float(np.trapezoid(cross_section_area(grid), grid))
    report("trapezoid rule with 1600000 intervals", trapezoid_value, VOLUME_FLOAT, GRID_TOLERANCE)

    box_volume = 2.0
    points = generator.uniform((-1.0, 0.0, 0.0), (1.0, 1.0, 1.0), size=(SAMPLE_COUNT, 3))
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    hits = np.count_nonzero((y >= x * x) & (z >= 0.0) & (y + z <= 1.0))
    estimate = box_volume * hits / SAMPLE_COUNT
    probability = VOLUME_FLOAT / box_volume
    standard_error = box_volume * np.sqrt(probability * (1.0 - probability) / SAMPLE_COUNT)
    report("rejection sample of the bounding box", estimate, VOLUME_FLOAT, 4.0 * standard_error)
    print(f"    standard error = {standard_error:.3e}, difference = {abs(estimate - VOLUME_FLOAT):.3e}")

    print("")
    print("bounds that the volume must obey")
    report_lower_bound("volume is larger than zero", VOLUME_FLOAT, 0.0)
    inner_corner = np.array([-0.5, 0.25, 0.0])
    inner_size = np.array([1.0, 0.25, 0.5])
    inner_volume = float(np.prod(inner_size))
    inner_corners = np.array([[sx, sy, sz]
                              for sx in (0.0, 1.0) for sy in (0.0, 1.0) for sz in (0.0, 1.0)])
    inner_points = inner_corner + inner_corners * inner_size
    inner_inside = np.all((inner_points[:, 1] >= inner_points[:, 0] ** 2)
                          & (inner_points[:, 2] >= 0.0)
                          & (inner_points[:, 1] + inner_points[:, 2] <= 1.0))
    report("all eight corners of the inner box are members of the solid", float(inner_inside), 1.0, 0.0)
    report("volume of the inner box", inner_volume, 0.125, 0.0)
    report_lower_bound("volume is larger than the inner box", VOLUME_FLOAT, inner_volume)
    report_upper_bound("volume is smaller than the bounding box", VOLUME_FLOAT, box_volume)
    projection_area = float(quad(lambda x_value: 1.0 - x_value * x_value, -1.0, 1.0)[0])
    report("area of the projection in the xy plane", projection_area, 4.0 / 3.0, QUADRATURE_TOLERANCE)
    report_upper_bound("volume is smaller than projection area times tallest height",
                       VOLUME_FLOAT, projection_area * 1.0)

    print("")
    print("the slice area at three fixed values of y")
    for y_value in (0.25, 0.5, 0.75):
        expected = slice_area(y_value)
        probability = expected / 2.0
        standard_error_slice = 2.0 * np.sqrt(probability * (1.0 - probability) / SLICE_SAMPLE_COUNT)
        measured = rejection_area_at_fixed_y(y_value, generator)
        report(f"  slice area at y = {y_value}", measured, expected, 4.0 * standard_error_slice)
        print(f"    standard error = {standard_error_slice:.3e}, difference = {abs(measured - expected):.3e}")


if __name__ == "__main__":
    main()
