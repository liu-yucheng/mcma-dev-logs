"""Verify the inner integration over x and the volume element of Part 2.

Part 2 fixes a point (y, z) of the unit disk and integrates the function x along
the x segment 4*(y^2 + z^2) <= x <= 4.  This module checks three facts:

1. the inner integral equals 8*(1 - r^4) for r = sqrt(y^2 + z^2);
2. the cylindrical substitution (y, z) = (r*cos(theta), r*sin(theta)) has Jacobian r,
   which the module checks by a change of variables on the volume of E;
3. the inner integrand does not depend on the angle theta.

Every check prints the computed value, the expected value, and the verdict.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy import integrate

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

RANDOM_SEED: int = 20261122
"""Seed of the pseudo random generator that this module uses."""


def inner_integral_exact(radius: float) -> float:
    """Return the closed form 8*(1 - r^4) of the inner integral.

    Args:
        radius: The distance r of the point (y, z) from the x axis.

    Returns:
        The value of the integral of x from 4*r^2 to 4.
    """
    return 0.5 * (PLANE_POSITION**2 - (PARABOLOID_COEFFICIENT * radius**2) ** 2)


def inner_integral_quadrature(radius: float) -> float:
    """Return the inner integral of x from 4*r^2 to 4 by numerical quadrature.

    Args:
        radius: The distance r of the point (y, z) from the x axis.

    Returns:
        The value that scipy.integrate.quad reports for the same integral.
    """
    lower_bound = PARABOLOID_COEFFICIENT * radius**2
    value, _ = integrate.quad(lambda x_value: x_value, lower_bound, PLANE_POSITION)
    return value


def report(check_name: str, computed_value: float, expected_value: float, tolerance: float) -> bool:
    """Print one comparison and return its verdict.

    Args:
        check_name: A short name of the checked fact.
        computed_value: The value that the computation produced.
        expected_value: The value that the tutorial states.
        tolerance: The largest accepted absolute difference.

    Returns:
        True when the difference is within the tolerance, and False otherwise.
    """
    difference = abs(computed_value - expected_value)
    verdict = "PASS" if difference <= tolerance else "FAIL"
    print(f"{check_name:<56} computed={computed_value: .12f} expected={expected_value: .12f} "
          f"difference={difference:.3e} {verdict}")
    return verdict == "PASS"


def check_inner_integral_values() -> bool:
    """Compare the closed form with quadrature at five radii.

    Returns:
        True when every radius agrees within 1e-10.
    """
    all_passed = True
    for radius in (0.0, 0.25, 0.5, 0.75, 1.0):
        all_passed &= report(
            f"inner integral at r = {radius:.2f}",
            inner_integral_quadrature(radius),
            inner_integral_exact(radius),
            1.0e-10,
        )
    return all_passed


def check_inner_integral_rational_value() -> bool:
    """Check the inner integral at r = 1/2 against an exact rational number.

    Returns:
        True when the exact value 15/2 agrees with the closed form.
    """
    radius = Fraction(1, 2)
    lower_bound = PARABOLOID_COEFFICIENT * radius**2
    exact_value = (Fraction(PLANE_POSITION) ** 2 - lower_bound**2) / 2
    closed_form = (Fraction(PLANE_POSITION) ** 2 -
                   (Fraction(PARABOLOID_COEFFICIENT) * radius**2) ** 2) / 2
    print(f"{'inner integral at r = 1/2 as a rational number':<56} "
          f"computed={float(exact_value): .6f} expected={float(Fraction(15, 2)): .6f} "
          f"fraction={exact_value}")
    return bool(exact_value == Fraction(15, 2) == closed_form)


def check_volume_element() -> bool:
    """Check that the cylindrical substitution carries the factor r.

    The volume of E is 2*pi.  The module computes the volume with the factor r and
    without the factor r.  Only the version with r gives 2*pi.

    Returns:
        True when the version with the factor r agrees with 2*pi.
    """
    volume_with_factor, _ = integrate.tplquad(
        lambda x_value, radius, angle: radius,
        0.0, 2.0 * np.pi,
        lambda angle: 0.0, lambda angle: 1.0,
        lambda angle, radius: PARABOLOID_COEFFICIENT * radius**2,
        lambda angle, radius: PLANE_POSITION,
    )
    volume_without_factor, _ = integrate.tplquad(
        lambda x_value, radius, angle: 1.0,
        0.0, 2.0 * np.pi,
        lambda angle: 0.0, lambda angle: 1.0,
        lambda angle, radius: PARABOLOID_COEFFICIENT * radius**2,
        lambda angle, radius: PLANE_POSITION,
    )
    passed_with = report("volume of E with the Jacobian factor r", volume_with_factor,
                         2.0 * np.pi, 1.0e-9)
    print(f"{'volume of E without the Jacobian factor r':<56} "
          f"computed={volume_without_factor: .12f} expected={2.0 * np.pi: .12f} "
          f"{'PASS' if abs(volume_without_factor - 2.0 * np.pi) > 1.0e-3 else 'FAIL'}")
    return passed_with and abs(volume_without_factor - 2.0 * np.pi) > 1.0e-3


def check_angle_independence() -> bool:
    """Check that the inner integral has the same value at every angle.

    Returns:
        True when the spread of the inner integral over the angle is negligible.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    angle_values = generator.uniform(0.0, 2.0 * np.pi, 20000)
    radius_values = generator.uniform(0.0, 1.0, 20000)
    y_values = radius_values * np.cos(angle_values)
    z_values = radius_values * np.sin(angle_values)
    direct_values = 0.5 * (PLANE_POSITION**2 -
                           (PARABOLOID_COEFFICIENT * (y_values**2 + z_values**2)) ** 2)
    reference_values = np.array([inner_integral_exact(radius) for radius in radius_values])
    largest_difference = float(np.max(np.abs(direct_values - reference_values)))
    return report("inner integral from (y, z) equals the form in r", largest_difference, 0.0, 1.0e-12)


def main() -> int:
    """Run every check of Part 2.

    Returns:
        The process exit status: 0 when every check passes, and 1 otherwise.
    """
    print("Part 2 verification: inner integral over x and the volume element")
    print("-" * 110)
    results = [
        check_inner_integral_values(),
        check_inner_integral_rational_value(),
        check_volume_element(),
        check_angle_independence(),
    ]
    print("-" * 110)
    print(f"All Part 2 checks passed: {all(results)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
