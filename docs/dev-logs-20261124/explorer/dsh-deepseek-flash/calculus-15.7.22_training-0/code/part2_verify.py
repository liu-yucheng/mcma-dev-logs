"""Verify the triple integral of Part 2 and its value.

The script checks three claims of Part 2.
The first claim is that the inner integral in y equals 5 - z.
The second claim is that the double integral of 5 - z over the disk equals 20 pi.
The third claim is that the evaluation with the half disk area gives the same value.

The inner integral is computed by numerical quadrature.
The thickness is computed by the two plane equations.
The two values are independent.
"""

import math
from typing import Final

import numpy as np
from scipy.integrate import dblquad, quad

SQUARED_RADIUS: Final[float] = 4.0
"""Right side of the cylinder equation x^2 + z^2 = 4."""

QUADRATURE_TOLERANCE: Final[float] = 1.0e-10
"""Absolute tolerance that the script requests from the quadrature."""

HEIGHT_SAMPLE_VALUES: Final[tuple[float, ...]] = (-2.0, -0.5, 1.5, 2.0)
"""Values of z at which the script compares the inner integral with 5 - z."""

EXACT_VOLUME_FACTOR: Final[float] = 20.0
"""Factor of the closed form volume 20 pi."""


def thickness_by_inner_integral(z_value: float) -> float:
    """Return the length of the interval [-1, 4 - z] by numerical integration."""
    value, _ = quad(lambda height: 1.0, -1.0, 4.0 - z_value, epsabs=QUADRATURE_TOLERANCE)
    return value


def thickness_formula(z_value: float) -> float:
    """Return the length of the interval [-1, 4 - z] by the two plane equations."""
    return 5.0 - z_value


def volume_by_double_integral(radius: float) -> float:
    """Return the volume as the double integral of 5 - z over the disk of the given radius."""
    value, _ = dblquad(
        lambda z_value, x_value: 5.0 - z_value,
        -radius,
        radius,
        lambda x_value: -math.sqrt(SQUARED_RADIUS - x_value * x_value),
        lambda x_value: math.sqrt(SQUARED_RADIUS - x_value * x_value),
        epsabs=QUADRATURE_TOLERANCE,
    )
    return value


def upper_half_disk_area(radius: float) -> float:
    """Return the area of the upper half of the disk by numerical integration."""
    value, _ = quad(
        lambda x_value: math.sqrt(SQUARED_RADIUS - x_value * x_value),
        -radius,
        radius,
        epsabs=QUADRATURE_TOLERANCE,
    )
    return value


def main() -> None:
    """Run the three checks of Part 2 and print each computed value with its expected value."""
    radius = float(np.max(np.roots([1.0, 0.0, -SQUARED_RADIUS])))
    exact_volume = EXACT_VOLUME_FACTOR * math.pi

    for z_value in HEIGHT_SAMPLE_VALUES:
        computed = thickness_by_inner_integral(z_value)
        expected = thickness_formula(z_value)
        print(f"check 1 at z = {z_value:5.2f}: integral {computed:.12f}, formula {expected:.12f}")
        assert abs(computed - expected) <= 1.0e-9, "the inner integral differs from 5 - z"

    volume_double = volume_by_double_integral(radius)
    print(f"check 2 double integral: {volume_double:.12f}")
    print(f"check 2 closed form:     {exact_volume:.12f}")
    assert abs(volume_double - exact_volume) <= 1.0e-8, "the double integral is not 20 pi"

    half_area = upper_half_disk_area(radius)
    geometric_half_area = 0.5 * math.pi * radius**2
    volume_half_disk = 10.0 * half_area
    print(f"check 3 half disk area: integral {half_area:.12f}, formula {geometric_half_area:.12f}")
    print(f"check 3 volume:         10 * area {volume_half_disk:.12f}, closed form {exact_volume:.12f}")
    assert abs(half_area - geometric_half_area) <= 1.0e-9, "the half disk area is wrong"
    assert abs(volume_half_disk - exact_volume) <= 1.0e-8, "10 times the half disk area is not 20 pi"
    assert abs(volume_half_disk - volume_double) <= 1.0e-8, "the two volume computations disagree"

    print("part 2: all checks passed")


if __name__ == "__main__":
    main()
