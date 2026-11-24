"""Verify that all six orders give the same number for one nontrivial function.

A general function f has no single value, so this script uses one concrete function that depends
on all three coordinates,

    f(x, y, z) = 1 + x + y^2 + z^2,

and compares the six iterated integrals with the closed form

    volume + integral of x + integral of y^2 + integral of z^2 = 36*pi + 0 + 81*pi + 81*pi.

The closed form is computed from the analytic results of Parts 1, 3, and 4, and each iterated
integral is computed by a separate nested quadrature.  The two routes share no code, so agreement
is evidence that the six limit sets describe the same solid.  The script also compares the six
values with each other and runs one negative control in which the cylinder bound is replaced by
the constant 3.

Run this script with the interpreter of `code/.venv`.  It writes
`code/results/part5_results.json`.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from scipy import integrate

RADIUS = 3.0
"""Radius of the circular cylinder y^2 + z^2 = 9."""

HALF_LENGTH = 2.0
"""Half of the distance between the planes x = -2 and x = 2."""

CYLINDER_LENGTH = 2.0 * HALF_LENGTH
"""Distance between the two planes x = -2 and x = 2."""

EXACT_VOLUME = math.pi * RADIUS**2 * CYLINDER_LENGTH
"""Volume of E, thus 36*pi."""

EXACT_INTEGRAL_OF_Y_SQUARED = 81.0 * math.pi
"""Integral of y^2 over E, computed in Part 3."""

EXACT_INTEGRAL_OF_Z_SQUARED = 81.0 * math.pi
"""Integral of z^2 over E, computed in Part 4."""

EXACT_INTEGRAL_OF_THE_TEST_FUNCTION = (EXACT_VOLUME + EXACT_INTEGRAL_OF_Y_SQUARED
                                      + EXACT_INTEGRAL_OF_Z_SQUARED)
"""Closed form of the integral of 1 + x + y^2 + z^2 over E, thus 198*pi."""

MEAN_DIFFERENCE_TOLERANCE = 1e-6
"""Largest accepted relative difference between an iterated integral and the closed form."""

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "part5_results.json"
"""Path of the machine-readable record of the checks."""


def test_function(x: float, y: float, z: float) -> float:
    """Return the value of the test function 1 + x + y^2 + z^2."""
    return 1.0 + x + y * y + z * z


def integrate_once(integrand, low: float, high: float) -> float:
    """Return the one-dimensional integral of `integrand` between two limits."""
    value, _ = integrate.quad(integrand, low, high, epsabs=1e-12, epsrel=1e-12, limit=200)
    return float(value)


def follow(follow_cylinder: bool, fixed_other: float) -> float:
    """Return the half width of the cylinder opening, or the constant 3 for the control.

    Args:
        follow_cylinder: When True, return sqrt(9 - t^2) for the fixed value of the other
            coordinate.  When False, return the constant 3.
        fixed_other: Fixed value of the other coordinate of the plane y-z.

    Returns:
        The half width of the inner limits.
    """
    if follow_cylinder:
        return math.sqrt(max(RADIUS**2 - fixed_other * fixed_other, 0.0))
    return RADIUS


def order_dz_dy_dx(integrand, follow_cylinder: bool = True) -> float:
    """Return the iterated integral with the order dz dy dx.

    The outer integral runs over x, the middle integral runs over y, and the inner integral
    runs over z between the two halves of the cylinder at the fixed value of y.
    """
    def integral_over_z(fixed_y: float, fixed_x: float) -> float:
        half_width = follow(follow_cylinder, fixed_y)
        return integrate_once(lambda z: integrand(fixed_x, fixed_y, z), -half_width, half_width)

    def integral_over_y(fixed_x: float) -> float:
        return integrate_once(lambda y: integral_over_z(y, fixed_x), -RADIUS, RADIUS)

    return integrate_once(integral_over_y, -HALF_LENGTH, HALF_LENGTH)


def order_dy_dz_dx(integrand) -> float:
    """Return the iterated integral with the order dy dz dx.

    The outer integral runs over x, the middle integral runs over z, and the inner integral
    runs over y between the two halves of the cylinder at the fixed value of z.
    """
    def integral_over_y(fixed_z: float, fixed_x: float) -> float:
        half_width = follow(True, fixed_z)
        return integrate_once(lambda y: integrand(fixed_x, y, fixed_z), -half_width, half_width)

    def integral_over_z(fixed_x: float) -> float:
        return integrate_once(lambda z: integral_over_y(z, fixed_x), -RADIUS, RADIUS)

    return integrate_once(integral_over_z, -HALF_LENGTH, HALF_LENGTH)


def order_dz_dx_dy(integrand) -> float:
    """Return the iterated integral with the order dz dx dy.

    The outer integral runs over y, the middle integral runs over x, and the inner integral
    runs over z between the two halves of the cylinder at the fixed value of y.
    """
    def integral_over_z(fixed_y: float, fixed_x: float) -> float:
        half_width = follow(True, fixed_y)
        return integrate_once(lambda z: integrand(fixed_x, fixed_y, z), -half_width, half_width)

    def integral_over_x(fixed_y: float) -> float:
        return integrate_once(lambda x: integral_over_z(fixed_y, x), -HALF_LENGTH, HALF_LENGTH)

    return integrate_once(integral_over_x, -RADIUS, RADIUS)


def order_dx_dz_dy(integrand) -> float:
    """Return the iterated integral with the order dx dz dy.

    The outer integral runs over y, the middle integral runs over z between the two halves of
    the cylinder at the fixed value of y, and the inner integral runs over x between -2 and 2.
    """
    def integral_over_x(fixed_y: float, fixed_z: float) -> float:
        return integrate_once(lambda x: integrand(x, fixed_y, fixed_z), -HALF_LENGTH, HALF_LENGTH)

    def integral_over_z(fixed_y: float) -> float:
        half_width = follow(True, fixed_y)
        return integrate_once(lambda z: integral_over_x(fixed_y, z), -half_width, half_width)

    return integrate_once(integral_over_z, -RADIUS, RADIUS)


def order_dy_dx_dz(integrand) -> float:
    """Return the iterated integral with the order dy dx dz.

    The outer integral runs over z, the middle integral runs over x, and the inner integral
    runs over y between the two halves of the cylinder at the fixed value of z.
    """
    def integral_over_y(fixed_z: float, fixed_x: float) -> float:
        half_width = follow(True, fixed_z)
        return integrate_once(lambda y: integrand(fixed_x, y, fixed_z), -half_width, half_width)

    def integral_over_x(fixed_z: float) -> float:
        return integrate_once(lambda x: integral_over_y(fixed_z, x), -HALF_LENGTH, HALF_LENGTH)

    return integrate_once(integral_over_x, -RADIUS, RADIUS)


def order_dx_dy_dz(integrand) -> float:
    """Return the iterated integral with the order dx dy dz.

    The outer integral runs over z, the middle integral runs over y between the two halves of
    the cylinder at the fixed value of z, and the inner integral runs over x between -2 and 2.
    """
    def integral_over_x(fixed_z: float, fixed_y: float) -> float:
        return integrate_once(lambda x: integrand(x, fixed_y, fixed_z), -HALF_LENGTH, HALF_LENGTH)

    def integral_over_y(fixed_z: float) -> float:
        half_width = follow(True, fixed_z)
        return integrate_once(lambda y: integral_over_x(fixed_z, y), -half_width, half_width)

    return integrate_once(integral_over_y, -RADIUS, RADIUS)


def record(results: list[dict[str, object]], label: str, computed: float, expected: float,
           tolerance: float) -> None:
    """Append one comparison to the record, print it, and raise when it fails."""
    difference = abs(computed - expected)
    passed = difference <= tolerance
    results.append({
        "label": label,
        "computed": computed,
        "expected": expected,
        "difference": difference,
        "tolerance": tolerance,
        "passed": passed,
    })
    print(f"{label}: computed={computed:.12f} expected={expected:.12f} "
          f"difference={difference:.3e} tolerance={tolerance:.3e}")
    if not passed:
        raise AssertionError(f"{label}: difference {difference:.6e} exceeds {tolerance:.6e}")


def main() -> None:
    """Run every check of Part 5 and write the record."""
    results: list[dict[str, object]] = []
    tolerance = MEAN_DIFFERENCE_TOLERANCE * EXACT_INTEGRAL_OF_THE_TEST_FUNCTION

    orders = {
        "dz dy dx": order_dz_dy_dx,
        "dy dz dx": order_dy_dz_dx,
        "dz dx dy": order_dz_dx_dy,
        "dx dz dy": order_dx_dz_dy,
        "dy dx dz": order_dy_dx_dz,
        "dx dy dz": order_dx_dy_dz,
    }

    values: dict[str, float] = {}
    for name, order in orders.items():
        value = order(test_function)
        values[name] = value
        record(results, f"order {name} against 198*pi", value,
               EXACT_INTEGRAL_OF_THE_TEST_FUNCTION, tolerance)

    names = list(values)
    largest_difference = 0.0
    for first_index in range(len(names)):
        for second_index in range(first_index + 1, len(names)):
            difference = abs(values[names[first_index]] - values[names[second_index]])
            largest_difference = max(largest_difference, difference)
    record(results, "largest pairwise difference of the six orders", largest_difference, 0.0,
           tolerance)

    grouped = {
        "outer x": ("dz dy dx", "dy dz dx"),
        "outer y": ("dz dx dy", "dx dz dy"),
        "outer z": ("dy dx dz", "dx dy dz"),
    }
    for group_name, pair in grouped.items():
        record(results, f"the two orders with {group_name} agree", values[pair[0]], values[pair[1]],
               tolerance)

    control_value = order_dz_dy_dx(test_function, follow_cylinder=False)
    control_expected = CYLINDER_LENGTH * (2.0 * RADIUS) * (2.0 * RADIUS)
    control_expected += 0.0
    control_expected += 2.0 * CYLINDER_LENGTH * (2.0 * RADIUS) * (RADIUS**3 / 3.0)
    control_expected += 2.0 * CYLINDER_LENGTH * (2.0 * RADIUS) * (RADIUS**3 / 3.0)
    print(f"order dz dy dx with the constant bound gives {control_value:.6f}")
    record(results, "negative control: the box bound gives the box integral", control_value,
           control_expected, 1e-3 * control_expected)
    if abs(control_value - EXACT_INTEGRAL_OF_THE_TEST_FUNCTION) < 100.0:
        raise AssertionError("the negative control does not separate the two limit sets")

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
