"""Verify the angle integral, the radius integral, and the final value of Part 3.

Part 3 evaluates the iterated integral

    integral from 0 to 2*pi, integral from 0 to 1, integral from 4*r^2 to 4 of x * r dx dr dtheta.

The module checks the angle integral 2*pi, the radius integral 8/3, and the product
16*pi/3.  It also evaluates the same integral by two independent numerical methods.

Every check prints the computed value, the expected value, and the verdict.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from scipy import integrate

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

RANDOM_SEED: int = 20261122
"""Seed of the pseudo random generator that this module uses."""


def radius_integrand(radius: float) -> float:
    """Return the integrand 8*(r - r^5) of the radius integral.

    Args:
        radius: The distance r of a point from the x axis.

    Returns:
        The inner integral 8*(1 - r^4) multiplied by the Jacobian factor r.
    """
    return 0.5 * (PLANE_POSITION**2 - (PARABOLOID_COEFFICIENT * radius**2) ** 2) * radius


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


def check_angle_integral() -> bool:
    """Check that the integral of 1 over the full turn is 2*pi.

    Returns:
        True when the quadrature value agrees with 2*pi.
    """
    value, _ = integrate.quad(lambda angle: 1.0, 0.0, 2.0 * math.pi)
    return report("angle integral of 1 over one turn", value, 2.0 * math.pi, 1.0e-12)


def check_radius_integral() -> bool:
    """Check that the radius integral equals 8/3.

    Returns:
        True when the quadrature value agrees with 8/3 within 1e-12.
    """
    value, _ = integrate.quad(radius_integrand, 0.0, 1.0)
    return report("radius integral of 8*(r - r^5) from 0 to 1", value, 8.0 / 3.0, 1.0e-12)


def check_radius_integral_rational() -> bool:
    """Check the radius integral with exact rational arithmetic.

    Returns:
        True when the exact antiderivative value is 8/3.
    """
    exact_value = Fraction(8, 1) * (Fraction(1, 2) - Fraction(1, 6))
    print(f"{'radius integral as an exact rational number':<56} "
          f"computed={float(exact_value): .12f} expected={8.0 / 3.0: .12f} fraction={exact_value}")
    return bool(exact_value == Fraction(8, 3))


def check_product() -> bool:
    """Check the product of the two one dimensional integrals against 16*pi/3.

    Returns:
        True when the product agrees with 16*pi/3 within 1e-12.
    """
    angle_value, _ = integrate.quad(lambda angle: 1.0, 0.0, 2.0 * math.pi)
    radius_value, _ = integrate.quad(radius_integrand, 0.0, 1.0)
    return report("product 2*pi * 8/3", angle_value * radius_value, 16.0 * math.pi / 3.0, 1.0e-12)


def check_full_triple_quadrature() -> bool:
    """Check the full integral by nested adaptive quadrature.

    Returns:
        True when the nested quadrature agrees with 16*pi/3 within 1e-8.
    """
    value, _ = integrate.tplquad(
        lambda x_value, radius, angle: x_value * radius,
        0.0, 2.0 * math.pi,
        lambda angle: 0.0, lambda angle: 1.0,
        lambda angle, radius: PARABOLOID_COEFFICIENT * radius**2,
        lambda angle, radius: PLANE_POSITION,
    )
    return report("nested quadrature over theta, r, x", value, 16.0 * math.pi / 3.0, 1.0e-8)


def check_point_sample_integral() -> bool:
    """Check the integral by a stratified sample of the region E.

    The sample is uniform in the cylinder 0 <= r <= 1, 0 <= theta < 2*pi,
    0 <= x <= 4.  The radius uses the area weight, so the sample is uniform with
    respect to the volume element r dr dtheta dx.  The ratio of accepted points
    estimates the volume of E, and the mean of x over the accepted points
    estimates the mean value of x over E.

    Returns:
        True when the estimate agrees with 16*pi/3 within four standard errors.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = 4000000
    radial_values = np.sqrt(generator.uniform(0.0, 1.0, sample_count))
    angle_values = generator.uniform(0.0, 2.0 * math.pi, sample_count)
    x_values = generator.uniform(0.0, PLANE_POSITION, sample_count)
    lower_bounds = PARABOLOID_COEFFICIENT * radial_values**2
    inside = (lower_bounds <= x_values) & (x_values <= PLANE_POSITION)
    cylinder_volume = math.pi * 1.0**2 * PLANE_POSITION
    weighted_values = np.where(inside, x_values, 0.0)
    estimated_integral = cylinder_volume * float(np.mean(weighted_values))
    standard_error = (cylinder_volume * float(np.std(weighted_values, ddof=1))
                      / math.sqrt(sample_count))
    accepted_count = int(np.count_nonzero(inside))
    estimated_volume = cylinder_volume * accepted_count / sample_count
    mean_x = float(np.mean(x_values[inside]))
    print(f"{'sample estimate of the integral':<56} computed={estimated_integral: .6f} "
          f"expected={16.0 * math.pi / 3.0: .6f} error={standard_error:.6f}")
    print(f"{'sample estimate of the volume':<56} computed={estimated_volume: .6f} "
          f"expected={2.0 * math.pi: .6f}")
    print(f"{'mean of x over the accepted points':<56} computed={mean_x: .6f} "
          f"expected={8.0 / 3.0: .6f}")
    return abs(estimated_integral - 16.0 * math.pi / 3.0) <= 4.0 * standard_error


def main() -> int:
    """Run every check of Part 3.

    Returns:
        The process exit status: 0 when every check passes, and 1 otherwise.
    """
    print("Part 3 verification: angle integral, radius integral, final value")
    print("-" * 110)
    results = [
        check_angle_integral(),
        check_radius_integral(),
        check_radius_integral_rational(),
        check_product(),
        check_full_triple_quadrature(),
        check_point_sample_integral(),
    ]
    print("-" * 110)
    print(f"Final value of the integral: 16*pi/3 = {16.0 * math.pi / 3.0:.9f}")
    print(f"All Part 3 checks passed: {all(results)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
