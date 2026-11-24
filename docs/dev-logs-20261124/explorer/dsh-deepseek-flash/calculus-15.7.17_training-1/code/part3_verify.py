"""Verify the polar evaluation of the double integral over the unit disk.

The script checks the radial integral, the angular integral, and their product 16 pi / 3.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import dblquad, quad

NUMERIC_TOLERANCE = 1.0e-9
"""Absolute tolerance for a one-dimensional quadrature."""

DOUBLE_TOLERANCE = 1.0e-8
"""Absolute tolerance for a two-dimensional quadrature."""

RADIAL_FACTOR = 8.0
"""Coefficient of (1 - r^4) r in the radial integrand."""


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
    """Run the radial and angular checks.

    Returns:
        The number of failed checks.
    """
    failures = 0
    print("Part 3: polar coordinates in the unit disk")
    print("")

    # Step 3.1. The area element r dr d(theta) and the radial integrand 8 (1 - r^4) r.
    radial_value = quad(lambda radius: RADIAL_FACTOR * (1.0 - radius**4) * radius, 0.0, 1.0)[0]
    radial_closed_form = RADIAL_FACTOR * (0.5 - 1.0 / 6.0)
    failures += not check("radial integral", radial_value, radial_closed_form, NUMERIC_TOLERANCE)
    failures += not check("radial integral against 8 / 3", radial_value, 8.0 / 3.0, NUMERIC_TOLERANCE)
    print("")

    # Step 3.2. The angular integral and the product of the two factors.
    print("Step 3.2: the angular integral and the product")
    angular_value = quad(lambda angle: 1.0, 0.0, 2.0 * np.pi)[0]
    failures += not check("angular integral", angular_value, 2.0 * np.pi, NUMERIC_TOLERANCE)

    answer = radial_value * angular_value
    exact_answer = 16.0 * np.pi / 3.0
    failures += not check("product of the two factors", answer, exact_answer, 1.0e-8)

    plane_value = dblquad(
        lambda radius, angle: RADIAL_FACTOR * (1.0 - radius**4) * radius,
        0.0,
        2.0 * np.pi,
        lambda angle: 0.0,
        lambda angle: 1.0,
    )[0]
    failures += not check("two-dimensional quadrature in polar form", plane_value, exact_answer,
                          DOUBLE_TOLERANCE)
    print("")
    print(f"answer 16 pi / 3 = {exact_answer:.17g}")
    print(f"checks failed: {failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
