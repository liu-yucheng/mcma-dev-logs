"""Verify the inner integral along x and the volume of the solid E.

The script checks the antiderivative of x on one vertical segment, the reduced integrand
8 (1 - r^4), and the volume of the solid.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import dblquad, quad

PARABOLOID_FACTOR = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_X = 4.0
"""Coordinate x of the plane that closes the solid."""

SAMPLE_RADII = (0.0, 0.25, 0.5, 0.75, 1.0)
"""Radii at which the inner integral is compared with its closed form."""

NUMERIC_TOLERANCE = 1.0e-9
"""Absolute tolerance for a one-dimensional quadrature."""


def check(name: str, computed: float, expected: float, tolerance: float) -> bool:
    """Print one checked value and its expected value.

    Args:
        name: Short name of the checked fact.
        computed: Value that the script computed.
        expected: Value that the reasoning predicts.
        tolerance: Largest accepted absolute difference.

    Returns:
        True when the absolute difference is at most the tolerance.
    """
    difference = abs(computed - expected)
    passed = difference <= tolerance
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    print(f"       computed   = {computed!r}")
    print(f"       expected   = {expected!r}")
    print(f"       difference = {difference:.3e}   tolerance = {tolerance:.1e}")
    return passed


def main() -> int:
    """Run the checks of the inner integral and of the volume.

    Returns:
        The number of failed checks.
    """
    failures = 0
    print("Part 2: the inner integral along x")
    print("")

    # Step 2.1. For a fixed point (y, z) the variable x runs from 4 r^2 to 4.
    for radius in SAMPLE_RADII:
        lower_limit = PARABOLOID_FACTOR * radius**2
        numeric_value = quad(lambda x: x, lower_limit, PLANE_X)[0]
        closed_form = 0.5 * (PLANE_X**2 - lower_limit**2)
        simplified_form = 8.0 * (1.0 - radius**4)
        print(f"radius r = {radius:.2f}, segment [{lower_limit:.4f}, {PLANE_X:.4f}]")
        failures += not check(
            "  integral of x along the segment", numeric_value, closed_form, NUMERIC_TOLERANCE
        )
        failures += not check(
            "  form 8 (1 - r^4)", closed_form, simplified_form, NUMERIC_TOLERANCE
        )
    print("")

    # Step 2.2. The double integral of the reduced integrand over the unit disk.
    print("Step 2.2: the reduced double integral and the volume")
    reduced_integral = dblquad(
        lambda radius, angle: 8.0 * (1.0 - radius**4) * radius,
        0.0,
        2.0 * np.pi,
        lambda angle: 0.0,
        lambda angle: 1.0,
    )[0]
    failures += not check(
        "double integral of 8 (1 - r^4)", reduced_integral, 16.0 * np.pi / 3.0, 1.0e-8
    )

    volume_numeric = dblquad(
        lambda radius, angle: (PLANE_X - PARABOLOID_FACTOR * radius**2) * radius,
        0.0,
        2.0 * np.pi,
        lambda angle: 0.0,
        lambda angle: 1.0,
    )[0]
    volume_half_cylinder = 0.5 * np.pi * 1.0**2 * PLANE_X
    failures += not check("volume of E", volume_numeric, 2.0 * np.pi, 1.0e-8)
    failures += not check(
        "volume against half of the cylinder", volume_numeric, volume_half_cylinder, 1.0e-8
    )
    radial_volume_factor = quad(lambda radius: (PLANE_X - PARABOLOID_FACTOR * radius**2) * radius,
                                0.0, 1.0)[0]
    failures += not check("radial factor of the volume", radial_volume_factor, 1.0, NUMERIC_TOLERANCE)
    print("")

    print(f"checks failed: {failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
