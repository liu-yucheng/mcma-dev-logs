"""Verify the setup of the triple integral for the enclosed volume.

The solid is the set of points with x**2 + z**2 <= y <= 8 - x**2 - z**2.
This script checks four steps of the setup:

1. The inner integral over y gives the vertical thickness 8 - 2 * radius**2.
2. The Cartesian double integral of the thickness over the disk of radius 2
   gives the volume 16 * pi.
3. The polar form of the same double integral, with the Jacobian factor radius,
   gives the same volume.
4. The order of the horizontal integration does not change the volume.

Every check prints the computed value and the expected value.
"""

import math

import numpy as np
from scipy.integrate import dblquad, quad

# The upper surface is y = 8 - radius**2, so its constant term is 8.
UPPER_SURFACE_CONSTANT = 8.0
# The projection of the solid is the disk of radius 2.
PROJECTION_RADIUS = 2.0
# The volume of the solid is 16 * pi.
EXPECTED_VOLUME = 16.0 * math.pi
# The numerical comparisons use this absolute tolerance.
COMPARISON_TOLERANCE = 1.0e-8


def vertical_thickness(squared_radius: float) -> float:
    """Return the vertical thickness of the solid at the given squared radius."""
    return UPPER_SURFACE_CONSTANT - 2.0 * squared_radius


def thickness_at_point(horizontal_x: float, horizontal_z: float) -> float:
    """Return the vertical thickness of the solid above one horizontal point."""
    return vertical_thickness(horizontal_x**2 + horizontal_z**2)


def report(name: str, computed: float, expected: float) -> None:
    """Print one checked value, its expected value, and the absolute difference."""
    difference = abs(computed - expected)
    print(f"{name}: computed = {computed:.12f}, expected = {expected:.12f}, difference = {difference:.3e}")


def main() -> None:
    """Run every check of the integral setup."""
    print("Part 2: setup of the triple integral")

    # Check 1: the inner integral over y must give the vertical thickness.
    sample_radii = np.array([0.0, 0.5, 1.0, 1.5, 1.9])
    worst_gap = 0.0
    for radius in sample_radii:
        inner_integral, _ = quad(lambda height: 1.0, radius**2, UPPER_SURFACE_CONSTANT - radius**2)
        worst_gap = max(worst_gap, abs(inner_integral - vertical_thickness(radius**2)))
        print(f"  inner integral over y at radius {radius:.1f}: computed = {inner_integral:.12f}, "
              f"expected = {vertical_thickness(radius**2):.12f}")
    report("largest gap of the inner integral over y", worst_gap, 0.0)
    assert worst_gap < COMPARISON_TOLERANCE

    # Check 2: the double integral in Cartesian form gives the volume.
    cartesian_volume, _ = dblquad(
        lambda horizontal_z, horizontal_x: thickness_at_point(horizontal_x, horizontal_z),
        -PROJECTION_RADIUS,
        PROJECTION_RADIUS,
        lambda horizontal_x: -math.sqrt(max(PROJECTION_RADIUS**2 - horizontal_x**2, 0.0)),
        lambda horizontal_x: math.sqrt(max(PROJECTION_RADIUS**2 - horizontal_x**2, 0.0)),
    )
    report("volume from the Cartesian double integral", cartesian_volume, EXPECTED_VOLUME)
    assert abs(cartesian_volume - EXPECTED_VOLUME) < COMPARISON_TOLERANCE

    # Check 3: the polar form with the Jacobian factor gives the same volume.
    polar_volume, _ = dblquad(
        lambda angle, radius: vertical_thickness(radius**2) * radius,
        0.0,
        PROJECTION_RADIUS,
        lambda radius: 0.0,
        lambda radius: 2.0 * math.pi,
    )
    report("volume from the polar double integral", polar_volume, EXPECTED_VOLUME)
    assert abs(polar_volume - EXPECTED_VOLUME) < COMPARISON_TOLERANCE

    # Check 4: the reversed order of the horizontal integration gives the same volume.
    reversed_volume, _ = dblquad(
        lambda horizontal_x, horizontal_z: thickness_at_point(horizontal_x, horizontal_z),
        -PROJECTION_RADIUS,
        PROJECTION_RADIUS,
        lambda horizontal_z: -math.sqrt(max(PROJECTION_RADIUS**2 - horizontal_z**2, 0.0)),
        lambda horizontal_z: math.sqrt(max(PROJECTION_RADIUS**2 - horizontal_z**2, 0.0)),
    )
    report("volume from the reversed horizontal order", reversed_volume, EXPECTED_VOLUME)
    assert abs(reversed_volume - EXPECTED_VOLUME) < COMPARISON_TOLERANCE

    # Check 5: the Jacobian factor radius reproduces the area of the disk.
    polar_area, _ = dblquad(lambda angle, radius: radius, 0.0, PROJECTION_RADIUS, lambda radius: 0.0,
                            lambda radius: 2.0 * math.pi)
    report("area of the disk from the polar integral", polar_area, math.pi * PROJECTION_RADIUS**2)
    assert abs(polar_area - math.pi * PROJECTION_RADIUS**2) < COMPARISON_TOLERANCE

    print("Part 2: all checks passed")


if __name__ == "__main__":
    main()
