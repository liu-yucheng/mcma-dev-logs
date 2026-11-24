"""Verify the section at a fixed x and the two orders with x as the outer variable.

For a fixed value of x the two remaining conditions are y^2 + z^2 <= 9, so the section is the
full disk of radius 3 at every x in [-2, 2].  This script checks four claims.

1.  The section at a fixed x is the disk y^2 + z^2 <= 9, whatever the value of x in [-2, 2].
2.  At a fixed pair (x, y) the third coordinate z fills the chord [-sqrt(9 - y^2), sqrt(9 - y^2)].
3.  The order dz dy dx and the order dy dz dx both give the volume 36*pi, and both give
    117*pi for the function 1 + x + y^2.  A separate route computes those two exact values.
4.  A wrong set of inner limits gives a different number, so the check of Item 3 can fail.

Run this script with the interpreter of `code/.venv`.  It writes
`code/results/part2_results.json`.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import integrate

RADIUS = 3.0
"""Radius of the circular cylinder y^2 + z^2 = 9."""

HALF_LENGTH = 2.0
"""Half of the distance between the planes x = -2 and x = 2."""

CYLINDER_LENGTH = 2.0 * HALF_LENGTH
"""Distance between the two planes x = -2 and x = 2."""

EXACT_VOLUME = math.pi * RADIUS**2 * CYLINDER_LENGTH
"""Volume of E, thus 36*pi."""

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "part2_results.json"
"""Path of the machine-readable record of the checks."""


def constant_integrand(x: float, y: float, z: float) -> float:
    """Return 1, the integrand of the volume."""
    del x, y, z
    return 1.0


def quadratic_integrand(x: float, y: float, z: float) -> float:
    """Return 1 + x + y^2, an integrand with a known exact integral over E."""
    return 1.0 + x + y * y


def exact_integral_of_y_squared() -> float:
    """Return the integral of y^2 over E by polar coordinates in the (y, z) plane.

    The integral is length times the disk integral of y^2.  In polar coordinates the disk
    integral is the double integral of r^3 sin(theta)^2 over r in [0, 3] and theta in [0, 2*pi].
    """
    radial_part, _ = integrate.quad(lambda r: r**3, 0.0, RADIUS, limit=400)
    angular_part, _ = integrate.quad(lambda theta: math.sin(theta) ** 2, 0.0, 2.0 * math.pi,
                                     limit=400)
    return CYLINDER_LENGTH * radial_part * angular_part


def exact_integral_of_quadratic() -> float:
    """Return the exact integral of 1 + x + y^2 over E.

    The integral of x is zero, because E is symmetric about the plane x = 0 and x is odd.
    """
    first_moment_of_x = 0.0
    return EXACT_VOLUME + first_moment_of_x + exact_integral_of_y_squared()


def order_dz_dy_dx(integrand, follow_cylinder: bool = True) -> float:
    """Return the iterated integral with the order dz dy dx.

    Args:
        integrand: Function of (x, y, z).
        follow_cylinder: When True, the inner limits are the two halves of the cylinder.
            When False, the inner limits are the constants -3 and 3.  The second setting is a
            negative control that must give a different number.

    Returns:
        The value of the iterated integral.
    """
    def lower_for_z(x: float, y: float) -> float:
        del x
        if not follow_cylinder:
            return -RADIUS
        return -math.sqrt(max(RADIUS**2 - y * y, 0.0))

    def upper_for_z(x: float, y: float) -> float:
        del x
        if not follow_cylinder:
            return RADIUS
        return math.sqrt(max(RADIUS**2 - y * y, 0.0))

    value, _ = integrate.tplquad(
        lambda z, y, x: integrand(x, y, z),
        -HALF_LENGTH, HALF_LENGTH,
        lambda x: -RADIUS, lambda x: RADIUS,
        lower_for_z, upper_for_z,
        epsabs=1e-11, epsrel=1e-11,
    )
    return float(value)


def order_dy_dz_dx(integrand) -> float:
    """Return the iterated integral with the order dy dz dx.

    Args:
        integrand: Function of (x, y, z).

    Returns:
        The value of the iterated integral.
    """
    def lower_for_y(x: float, z: float) -> float:
        del x
        return -math.sqrt(max(RADIUS**2 - z * z, 0.0))

    def upper_for_y(x: float, z: float) -> float:
        del x
        return math.sqrt(max(RADIUS**2 - z * z, 0.0))

    value, _ = integrate.tplquad(
        lambda y, z, x: integrand(x, y, z),
        -HALF_LENGTH, HALF_LENGTH,
        lambda x: -RADIUS, lambda x: RADIUS,
        lower_for_y, upper_for_y,
        epsabs=1e-11, epsrel=1e-11,
    )
    return float(value)


def chord_of_section(fixed_y: float) -> tuple[float, float]:
    """Return the two ends of the z interval at the fixed value y.

    Args:
        fixed_y: Value of y at which the chord is measured.

    Returns:
        The lower end and the upper end of the chord.
    """
    half_chord = math.sqrt(max(RADIUS**2 - fixed_y * fixed_y, 0.0))
    return -half_chord, half_chord


def chord_membership_scan(fixed_y: float, step: float = 1e-4) -> tuple[float, float]:
    """Return the first and the last accepted z on a fine scan at the fixed value y.

    The scan uses the membership test |x| <= 2 and y^2 + z^2 <= 9 with x = 0.

    Args:
        fixed_y: Value of y at which the chord is scanned.
        step: Distance between two scanned values of z.

    Returns:
        The first and the last scanned z that lies in E.
    """
    accepted = [value for value in np.arange(-RADIUS - 0.01, RADIUS + 0.01, step)
                if abs(value) <= RADIUS and value * value + fixed_y * fixed_y <= RADIUS * RADIUS]
    return float(min(accepted)), float(max(accepted))


def inner_disk_integral(fixed_x: float) -> float:
    """Return the integral of 1 + x + y^2 over the disk of the section at x = fixed_x.

    Args:
        fixed_x: Value of x at which the inner double integral is measured.

    Returns:
        The value of the inner double integral.
    """
    value, _ = integrate.dblquad(
        lambda y, z: 1.0 + fixed_x + y * y,
        -RADIUS, RADIUS,
        lambda z: -math.sqrt(max(RADIUS**2 - z * z, 0.0)),
        lambda z: math.sqrt(max(RADIUS**2 - z * z, 0.0)),
        epsabs=1e-11, epsrel=1e-11,
    )
    return float(value)


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
    """Run every check of Part 2 and write the record."""
    results: list[dict[str, object]] = []

    exact_quadratic = exact_integral_of_quadratic()
    print(f"exact integral of y^2 over E = {exact_integral_of_y_squared():.12f}")
    print(f"exact integral of 1 + x + y^2 over E = {exact_quadratic:.12f}")

    volume_dz_dy_dx = order_dz_dy_dx(constant_integrand)
    volume_dy_dz_dx = order_dy_dz_dx(constant_integrand)
    record(results, "order dz dy dx against 36*pi for f = 1", volume_dz_dy_dx, EXACT_VOLUME, 1e-6)
    record(results, "order dy dz dx against 36*pi for f = 1", volume_dy_dz_dx, EXACT_VOLUME, 1e-6)
    record(results, "the two orders with x outer agree for f = 1",
           volume_dz_dy_dx, volume_dy_dz_dx, 1e-8)

    value_dz_dy_dx = order_dz_dy_dx(quadratic_integrand)
    value_dy_dz_dx = order_dy_dz_dx(quadratic_integrand)
    record(results, "order dz dy dx against 117*pi for f = 1 + x + y^2",
           value_dz_dy_dx, exact_quadratic, 1e-6 * exact_quadratic)
    record(results, "order dy dz dx against 117*pi for f = 1 + x + y^2",
           value_dy_dz_dx, exact_quadratic, 1e-6 * exact_quadratic)
    record(results, "the two orders with x outer agree for f = 1 + x + y^2",
           value_dz_dy_dx, value_dy_dz_dx, 1e-6 * exact_quadratic)

    wrong_limits_value = order_dz_dy_dx(constant_integrand, follow_cylinder=False)
    box_volume = CYLINDER_LENGTH * (2.0 * RADIUS) * (2.0 * RADIUS)
    print(f"order dz dy dx with z from -3 to 3 gives {wrong_limits_value:.6f}")
    print(f"the box [-2, 2] x [-3, 3] x [-3, 3] has volume {box_volume:.6f}")
    difference_to_volume = abs(wrong_limits_value - EXACT_VOLUME)
    print(f"distance of the wrong value to 36*pi = {difference_to_volume:.6f}")
    if difference_to_volume < 20.0:
        raise AssertionError("the negative control does not separate the two limit sets")
    results.append({
        "label": "negative control: z from -3 to 3 is not the cylinder bound",
        "computed": wrong_limits_value,
        "expected": box_volume,
        "difference": abs(wrong_limits_value - box_volume),
        "tolerance": 1e-6,
        "passed": abs(wrong_limits_value - box_volume) <= 1e-6,
    })

    for fixed_y in (-2.0, -0.5, 0.0, 2.0):
        low, high = chord_of_section(fixed_y)
        scanned_low, scanned_high = chord_membership_scan(fixed_y)
        print(f"y = {fixed_y:+.1f}: closed chord [{low:.9f}, {high:.9f}], "
              f"scanned chord [{scanned_low:.6f}, {scanned_high:.6f}]")
        record(results, f"lower end of the chord at y = {fixed_y:+.1f}",
               scanned_low, low, 2e-4)
        record(results, f"upper end of the chord at y = {fixed_y:+.1f}",
               scanned_high, high, 2e-4)
        record(results, f"chord length at y = {fixed_y:+.1f} against 2*sqrt(9 - y^2)",
               scanned_high - scanned_low, high - low, 4e-4)

    inner_at_zero = inner_disk_integral(0.0)
    inner_at_one = inner_disk_integral(1.0)
    print(f"inner disk integral at x = 0: {inner_at_zero:.12f}")
    print(f"inner disk integral at x = 1: {inner_at_one:.12f}")
    record(results, "change of the inner disk integral from x = 0 to x = 1 against 9*pi",
           inner_at_one - inner_at_zero, math.pi * RADIUS**2, 1e-6)
    record(results, "inner disk integral at x = 0 against the integral of 1 + y^2 over the disk",
           inner_at_zero, math.pi * RADIUS**2 + exact_integral_of_y_squared() / CYLINDER_LENGTH,
           1e-6)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
