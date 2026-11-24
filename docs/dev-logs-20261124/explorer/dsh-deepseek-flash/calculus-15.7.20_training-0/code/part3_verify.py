"""Verify the analytic evaluation of the triple integral for the enclosed volume.

The iterated integral is
    V = integral from 0 to 2*pi, integral from 0 to 2,
        integral from radius**2 to 8 - radius**2 of radius dy dradius dangle.
This script checks each stage of the evaluation:

1. The inner integral over y gives 8 - 2 * radius**2.
2. The integrand of the radius integral is 8 * radius - 2 * radius**3.
3. The antiderivative 4 * radius**2 - radius**4 / 2 takes the value 8 at radius 2.
4. The radius integral over 0 to 2 gives 8.
5. The angle integral gives 2 * pi, so the volume is 16 * pi.

Every check prints the computed value and the expected value.
"""

import math

from scipy.integrate import quad, tplquad

# The upper surface is y = 8 - radius**2, so its constant term is 8.
UPPER_SURFACE_CONSTANT = 8.0
# The projection of the solid is the disk of radius 2.
PROJECTION_RADIUS = 2.0
# The radius integral over 0 to 2 has the value 8.
EXPECTED_RADIUS_INTEGRAL = 8.0
# The angle integral over 0 to 2 * pi has the value 2 * pi.
EXPECTED_ANGLE_INTEGRAL = 2.0 * math.pi
# The volume of the solid is 16 * pi.
EXPECTED_VOLUME = 16.0 * math.pi
# The integral without the Jacobian factor of the polar coordinates gives 64 * pi / 3.
EXPECTED_VOLUME_WITHOUT_JACOBIAN = 64.0 * math.pi / 3.0
# The numerical comparisons use this absolute tolerance.
COMPARISON_TOLERANCE = 1.0e-9


def vertical_thickness(radius: float) -> float:
    """Return the vertical thickness of the solid at the given radius."""
    return UPPER_SURFACE_CONSTANT - 2.0 * radius**2


def radius_integrand(radius: float) -> float:
    """Return the integrand of the radius integral, namely radius times the thickness."""
    return UPPER_SURFACE_CONSTANT * radius - 2.0 * radius**3


def thickness_only_integrand(radius: float) -> float:
    """Return the thickness alone, which is the integrand when the Jacobian factor is missing."""
    return vertical_thickness(radius)


def radius_antiderivative(radius: float) -> float:
    """Return the antiderivative 4 * radius**2 - radius**4 / 2 of the radius integrand."""
    return 4.0 * radius**2 - radius**4 / 2.0


def report(name: str, computed: float, expected: float) -> None:
    """Print one checked value, its expected value, and the absolute difference."""
    difference = abs(computed - expected)
    print(f"{name}: computed = {computed:.12f}, expected = {expected:.12f}, difference = {difference:.3e}")


def main() -> None:
    """Run every check of the analytic evaluation."""
    print("Part 3: evaluation of the triple integral")

    # Check 1: the inner integral over y gives the thickness.
    inner_value, _ = quad(lambda height: 1.0, 0.5**2, UPPER_SURFACE_CONSTANT - 0.5**2)
    report("inner integral over y at radius 0.5", inner_value, vertical_thickness(0.5))
    assert abs(inner_value - vertical_thickness(0.5)) < COMPARISON_TOLERANCE

    # Check 2: the antiderivative reproduces the integrand by differentiation.
    sample_radii = [0.1, 0.7, 1.3, 1.9]
    worst_derivative_gap = 0.0
    for radius in sample_radii:
        numerical_derivative, _ = quad(radius_integrand, radius - 1.0e-4, radius + 1.0e-4)
        analytic_derivative = radius_antiderivative(radius + 1.0e-4) - radius_antiderivative(radius - 1.0e-4)
        worst_derivative_gap = max(worst_derivative_gap, abs(numerical_derivative - analytic_derivative))
        print(f"  increment of the integrand on a small interval at radius {radius:.1f}: "
              f"computed = {numerical_derivative:.12f}, expected = {analytic_derivative:.12f}")
    report("largest gap between the integrand and the antiderivative increment", worst_derivative_gap, 0.0)
    assert worst_derivative_gap < COMPARISON_TOLERANCE

    # Check 3: the antiderivative takes the value 8 at radius 2 and 0 at radius 0.
    report("antiderivative at radius 2", radius_antiderivative(PROJECTION_RADIUS), EXPECTED_RADIUS_INTEGRAL)
    report("antiderivative at radius 0", radius_antiderivative(0.0), 0.0)
    assert abs(radius_antiderivative(PROJECTION_RADIUS) - EXPECTED_RADIUS_INTEGRAL) < COMPARISON_TOLERANCE
    assert abs(radius_antiderivative(0.0)) < COMPARISON_TOLERANCE

    # Check 4: the radius integral over 0 to 2 has the value 8.
    radius_value, _ = quad(radius_integrand, 0.0, PROJECTION_RADIUS)
    report("radius integral over 0 to 2", radius_value, EXPECTED_RADIUS_INTEGRAL)
    assert abs(radius_value - EXPECTED_RADIUS_INTEGRAL) < COMPARISON_TOLERANCE
    report("value from the antiderivative", radius_antiderivative(PROJECTION_RADIUS) - radius_antiderivative(0.0),
           EXPECTED_RADIUS_INTEGRAL)
    antiderivative_gain = radius_antiderivative(PROJECTION_RADIUS) - radius_antiderivative(0.0)
    assert abs(antiderivative_gain - EXPECTED_RADIUS_INTEGRAL) < COMPARISON_TOLERANCE

    # Check 5: the full triple integral in cylindrical coordinates gives 16 * pi.
    cylindrical_volume, _ = tplquad(
        lambda height, radius, angle: radius,
        0.0,
        EXPECTED_ANGLE_INTEGRAL,
        lambda angle: 0.0,
        lambda angle: PROJECTION_RADIUS,
        lambda angle, radius: radius**2,
        lambda angle, radius: UPPER_SURFACE_CONSTANT - radius**2,
    )
    report("volume from the cylindrical triple integral", cylindrical_volume, EXPECTED_VOLUME)
    assert abs(cylindrical_volume - EXPECTED_VOLUME) < 1.0e-8

    # Check 6: the product of the two outer integrals gives the volume.
    outer_product = EXPECTED_ANGLE_INTEGRAL * EXPECTED_RADIUS_INTEGRAL
    report("volume from the product of the outer integrals", outer_product, EXPECTED_VOLUME)
    assert abs(outer_product - EXPECTED_VOLUME) < COMPARISON_TOLERANCE

    # Check 7: a missing Jacobian factor gives a value that is too large.
    thickness_integral, _ = quad(thickness_only_integrand, 0.0, PROJECTION_RADIUS)
    volume_without_jacobian = EXPECTED_ANGLE_INTEGRAL * thickness_integral
    report("volume when the Jacobian factor is missing", volume_without_jacobian,
           EXPECTED_VOLUME_WITHOUT_JACOBIAN)
    assert abs(volume_without_jacobian - EXPECTED_VOLUME_WITHOUT_JACOBIAN) < COMPARISON_TOLERANCE
    assert volume_without_jacobian > EXPECTED_VOLUME

    print(f"Part 3: final answer V = 16 * pi = {EXPECTED_VOLUME:.12f}")
    print("Part 3: all checks passed")


if __name__ == "__main__":
    main()
