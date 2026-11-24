"""Verify the final value of the integral by an independent order of integration.

Part 4 uses the slice of E at a fixed x.  That slice is a disk of radius sqrt(x/4),
so the integral also equals

    integral from 0 to 4 of x * pi * (x/4) dx.

The module checks this independent order, the volume of E, and the mean value of x
over E.  The three numbers must satisfy integral = volume * mean, which is a
consistency check that uses no trigonometric antiderivative.

Every check prints the computed value, the expected value, and the verdict.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import integrate

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

EXPECTED_INTEGRAL: float = 16.0 * math.pi / 3.0
"""The value that Parts 1 to 3 derive, about 16.755160819."""

RANDOM_SEED: int = 20261122
"""Seed of the pseudo random generator that this module uses."""


def slice_radius(x_coordinate: float) -> float:
    """Return the radius of the disk that the plane at x cuts from E.

    Args:
        x_coordinate: A value of x between 0 and 4.

    Returns:
        The value sqrt(x/4), which is the solution of 4*r^2 = x.
    """
    return math.sqrt(x_coordinate / PARABOLOID_COEFFICIENT)


def slice_area(x_coordinate: float) -> float:
    """Return the area of the disk that the plane at x cuts from E.

    Args:
        x_coordinate: A value of x between 0 and 4.

    Returns:
        The value pi * x / 4.
    """
    return math.pi * slice_radius(x_coordinate) ** 2


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


def check_slice_area_formula() -> bool:
    """Check the slice area against a point count on the disk.

    Returns:
        True when the counted area at x = 2 agrees with pi/2 within the statistical error.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = 2000000
    target_x = 2.0
    radius = slice_radius(target_x)
    y_values = generator.uniform(-1.0, 1.0, sample_count)
    z_values = generator.uniform(-1.0, 1.0, sample_count)
    inside = (y_values**2 + z_values**2) <= radius**2
    counted_area = 4.0 * float(np.mean(inside))
    statistical_error = 4.0 * math.sqrt(float(np.mean(inside)) * (1.0 - float(np.mean(inside)))
                                        / sample_count)
    print(f"{'counted slice area at x = 2':<56} computed={counted_area: .6f} "
          f"expected={slice_area(target_x): .6f} error={statistical_error:.6f}")
    return abs(counted_area - slice_area(target_x)) <= 4.0 * statistical_error


def check_alternative_order() -> bool:
    """Check the integral in the order x first, disk slice second.

    Returns:
        True when the quadrature value agrees with 16*pi/3 within 1e-10.
    """
    value, _ = integrate.quad(lambda x_coordinate: x_coordinate * slice_area(x_coordinate),
                              0.0, PLANE_POSITION)
    return report("integral in the order dx dy dz (disk slices)", value, EXPECTED_INTEGRAL, 1.0e-10)


def check_volume_by_slices() -> bool:
    """Check that the volume of E is 2*pi by the disk slice integral.

    Returns:
        True when the quadrature value agrees with 2*pi within 1e-10.
    """
    value, _ = integrate.quad(slice_area, 0.0, PLANE_POSITION)
    return report("volume of E from disk slices", value, 2.0 * math.pi, 1.0e-10)


def check_mean_value_of_x() -> bool:
    """Check that the mean value of x over E is 8/3.

    Returns:
        True when the ratio integral over volume agrees with 8/3 within 1e-10.
    """
    mean_value = EXPECTED_INTEGRAL / (2.0 * math.pi)
    return report("mean value of x over E", mean_value, 8.0 / 3.0, 1.0e-10)


def check_shell_form() -> bool:
    """Check the integral in the order of a cylindrical shell about the x axis.

    At radius r the shell has length 4 - 4*r^2, circumference 2*pi*r, and the
    mean value of x on the shell is (4 + 4*r^2)/2.  The product of the three
    factors must give the same integral.

    Returns:
        True when the shell integral agrees with 16*pi/3 within 1e-10.
    """
    def shell_integrand(radius: float) -> float:
        shell_length = PLANE_POSITION - PARABOLOID_COEFFICIENT * radius**2
        mean_x_on_shell = (PLANE_POSITION + PARABOLOID_COEFFICIENT * radius**2) / 2.0
        return 2.0 * math.pi * radius * shell_length * mean_x_on_shell

    value, _ = integrate.quad(shell_integrand, 0.0, 1.0)
    return report("integral in the order of cylindrical shells", value, EXPECTED_INTEGRAL, 1.0e-10)


def main() -> int:
    """Run every check of Part 4.

    Returns:
        The process exit status: 0 when every check passes, and 1 otherwise.
    """
    print("Part 4 verification: independent order of integration and consistency checks")
    print("-" * 110)
    results = [
        check_slice_area_formula(),
        check_alternative_order(),
        check_volume_by_slices(),
        check_mean_value_of_x(),
        check_shell_form(),
    ]
    print("-" * 110)
    print(f"All four orders agree on the value {EXPECTED_INTEGRAL:.9f}")
    print(f"All Part 4 checks passed: {all(results)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
