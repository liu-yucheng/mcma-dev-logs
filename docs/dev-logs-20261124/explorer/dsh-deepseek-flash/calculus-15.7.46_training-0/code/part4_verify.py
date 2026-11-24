"""Check the moment of inertia of the cone about the z axis.

The script computes the same value by four routes: the symbolic triple integral,
the adaptive triple quadrature, the stack of horizontal slices, and a Monte Carlo
estimate over a box. It also checks the second moment of one slice at three
heights, once in polar coordinates and once in Cartesian coordinates.
"""

from __future__ import annotations

import numpy as np
import sympy
from scipy import integrate
import importlib.metadata
import platform

HEIGHT = 1.0
"""The height h of the cone that the numeric checks use."""

DENSITY = 1.0
"""The constant density k that the numeric checks use."""

RANDOM_SEED = 20261123
"""The seed of the random number generator, so that a result repeats."""

SAMPLE_COUNT = 3_000_000
"""The number of points of the Monte Carlo estimate."""

EXACT_VALUE = np.pi * DENSITY * HEIGHT ** 5 / 10.0
"""The value pi*k*h**5/10 at the numeric values of h and k."""

TOLERANCE = 1.0e-9
"""The absolute tolerance of the adaptive quadrature checks."""


def slice_second_moment_polar(height_of_slice: float) -> float:
    """Return the second moment of one horizontal disk, integrated in polar coordinates.

    Args:
        height_of_slice: The value z0 of the slice, which is also its radius.

    Returns:
        The integral of x**2 + y**2 over the disk of radius z0.
    """
    value, _ = integrate.dblquad(
        lambda radius_value, angle_value: radius_value ** 3,
        0.0,
        2.0 * np.pi,
        lambda angle_value: 0.0,
        lambda angle_value: height_of_slice,
    )
    return float(value)


def slice_second_moment_cartesian(height_of_slice: float) -> float:
    """Return the second moment of one horizontal disk, integrated in Cartesian coordinates.

    Args:
        height_of_slice: The value z0 of the slice, which is also its radius.

    Returns:
        The integral of x**2 + y**2 over the disk of radius z0.
    """
    value, _ = integrate.dblquad(
        lambda y_value, x_value: x_value ** 2 + y_value ** 2,
        -height_of_slice,
        height_of_slice,
        lambda x_value: -np.sqrt(max(height_of_slice ** 2 - x_value ** 2, 0.0)),
        lambda x_value: np.sqrt(max(height_of_slice ** 2 - x_value ** 2, 0.0)),
    )
    return float(value)


def monte_carlo_moment(count: int, generator: np.random.Generator) -> tuple[float, float]:
    """Return the Monte Carlo moment of inertia and its standard error.

    Args:
        count: The number of sampled points.
        generator: The random number generator.

    Returns:
        The estimated moment of inertia and the standard error of the estimate.
    """
    x = generator.uniform(-HEIGHT, HEIGHT, count)
    y = generator.uniform(-HEIGHT, HEIGHT, count)
    z = generator.uniform(0.0, HEIGHT, count)
    inside = (x * x + y * y <= z * z) & (z <= HEIGHT)
    weight = np.where(inside, DENSITY * (x * x + y * y), 0.0)
    box_volume = (2.0 * HEIGHT) ** 2 * HEIGHT
    estimate = box_volume * float(np.mean(weight))
    standard_error = box_volume * float(np.std(weight, ddof=1)) / np.sqrt(count)
    return estimate, standard_error


def print_environment() -> None:
    """Print the version of each tool and the seed, so that a reported result repeats."""
    package_names = ("numpy", "scipy", "sympy", "matplotlib")
    versions = ", ".join(
        f"{name} {importlib.metadata.version(name)}" for name in package_names
    )
    seed = globals().get("RANDOM_SEED", "not used")
    print(f"Python {platform.python_version()}, {versions}, random seed {seed}")
    print()


def main() -> None:
    print_environment()
    """Run the checks of Part 4 and print each computed value beside its expected value."""
    symbol_k, symbol_h, symbol_r, symbol_z, symbol_angle = sympy.symbols("k h r z theta")
    symbolic_value = sympy.integrate(
        sympy.integrate(
            sympy.integrate(symbol_k * symbol_r ** 3, (symbol_z, symbol_r, symbol_h)),
            (symbol_r, 0, symbol_h),
        ),
        (symbol_angle, 0, 2 * sympy.pi),
    )
    symbolic_value = sympy.simplify(symbolic_value)
    print(f"symbolic triple integral: computed = {symbolic_value}, expected = pi*k*h**5/10")
    assert sympy.simplify(symbolic_value - sympy.pi * symbol_k * symbol_h ** 5 / 10) == 0, \
        "the symbolic triple integral is not pi*k*h**5/10"

    triple_value, _ = integrate.tplquad(
        lambda z_value, radius_value, angle_value: DENSITY * radius_value ** 3,
        0.0,
        2.0 * np.pi,
        lambda angle_value: 0.0,
        lambda angle_value: HEIGHT,
        lambda angle_value, radius_value: radius_value,
        lambda angle_value, radius_value: HEIGHT,
    )
    print(f"triple quadrature: computed = {triple_value:.12f}, expected = {EXACT_VALUE:.12f}")
    assert abs(triple_value - EXACT_VALUE) <= TOLERANCE, "the triple quadrature value is off"

    gap_polar = 0.0
    gap_cartesian = 0.0
    for height_of_slice in (0.25 * HEIGHT, 0.50 * HEIGHT, 0.75 * HEIGHT):
        polar_value = slice_second_moment_polar(height_of_slice)
        cartesian_value = slice_second_moment_cartesian(height_of_slice)
        formula_value = np.pi * height_of_slice ** 4 / 2.0
        gap_polar = max(gap_polar, abs(polar_value - formula_value))
        gap_cartesian = max(gap_cartesian, abs(cartesian_value - formula_value))
        print(f"slice z = {height_of_slice:.2f}: polar = {polar_value:.9f}, "
              f"Cartesian = {cartesian_value:.9f}, formula pi*z**4/2 = {formula_value:.9f}")
        assert abs(polar_value - cartesian_value) <= 1.0e-8, "the two slice integrals disagree"
    print(f"largest gap of the polar slice value: computed = {gap_polar:.3e}, expected = 0.0")
    assert gap_polar <= 1.0e-8 and gap_cartesian <= 1.0e-8, "a slice second moment is off"

    stack_value, _ = integrate.quad(
        lambda value: DENSITY * np.pi * value ** 4 / 2.0, 0.0, HEIGHT
    )
    print(f"slice stack: computed = {stack_value:.12f}, expected = {EXACT_VALUE:.12f}")
    assert abs(stack_value - EXACT_VALUE) <= TOLERANCE, "the slice stack value is off"

    generator = np.random.default_rng(RANDOM_SEED)
    moment_mc, error_mc = monte_carlo_moment(SAMPLE_COUNT, generator)
    print(f"Monte Carlo: computed = {moment_mc:.6f} +- {error_mc:.6f}, "
          f"expected = {EXACT_VALUE:.6f}, gap in standard errors = "
          f"{abs(moment_mc - EXACT_VALUE) / error_mc:.3f}")
    assert abs(moment_mc - EXACT_VALUE) <= 4.0 * error_mc, "the Monte Carlo moment is off"

    print(f"final value: computed = {EXACT_VALUE:.12f}, expected = pi*k*h**5/10 "
          f"with k = {DENSITY} and h = {HEIGHT}")


if __name__ == "__main__":
    main()
