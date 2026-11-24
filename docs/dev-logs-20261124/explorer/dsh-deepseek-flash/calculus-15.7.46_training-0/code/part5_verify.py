"""Check the mass of the cone, the standard cone formula, and the scaling law.

The script compares the mass from a symbolic triple integral with the mass from
the disk stack and with a Monte Carlo estimate. It then shows that the result
pi*k*h**5/10 equals (3/10)*M*h**2 and that a change of h to 2*h multiplies the
moment of inertia by 32.
"""

from __future__ import annotations

import numpy as np
import sympy
from scipy import integrate
import importlib.metadata
import platform

HEIGHT_ONE = 1.0
"""The first height h that the checks use."""

HEIGHT_SCALED = 2.0
"""The height 2*h that the scaling check uses."""

DENSITY = 2.3
"""The density k that the comparison of two forms of the answer uses."""

HEIGHT_DENSITY = 1.7
"""The height h that the comparison of two forms of the answer uses."""

RANDOM_SEED = 20261123
"""The seed of the random number generator, so that a result repeats."""

SAMPLE_COUNT = 2_000_000
"""The number of points of the Monte Carlo estimate."""


def numeric_moment(height: float, density: float) -> float:
    """Return the triple quadrature value of the moment of inertia about the z axis.

    Args:
        height: The height h of the cone.
        density: The constant density k.

    Returns:
        The value of the triple integral of density * r**2 over the cone.
    """
    value, _ = integrate.tplquad(
        lambda z_value, radius_value, angle_value: density * radius_value ** 3,
        0.0,
        2.0 * np.pi,
        lambda angle_value: 0.0,
        lambda angle_value: height,
        lambda angle_value, radius_value: radius_value,
        lambda angle_value, radius_value: height,
    )
    return float(value)


def monte_carlo_mass(count: int, height: float, density: float,
                     generator: np.random.Generator) -> tuple[float, float]:
    """Return the Monte Carlo mass of the cone and its standard error.

    Args:
        count: The number of sampled points.
        height: The height h of the cone.
        density: The constant density k.
        generator: The random number generator.

    Returns:
        The estimated mass and the standard error of the estimate.
    """
    x = generator.uniform(-height, height, count)
    y = generator.uniform(-height, height, count)
    z = generator.uniform(0.0, height, count)
    inside = (x * x + y * y <= z * z) & (z <= height)
    indicator = inside.astype(float)
    box_volume = (2.0 * height) ** 2 * height
    fraction = float(np.mean(indicator))
    estimate = box_volume * density * fraction
    standard_error = box_volume * density * float(np.sqrt(fraction * (1.0 - fraction) / count))
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
    """Run the checks of Part 5 and print each computed value beside its expected value."""
    symbol_k, symbol_h, symbol_r, symbol_z, symbol_angle = sympy.symbols("k h r z theta")

    mass_symbolic = sympy.simplify(
        sympy.integrate(
            sympy.integrate(
                sympy.integrate(symbol_k * symbol_r, (symbol_z, symbol_r, symbol_h)),
                (symbol_r, 0, symbol_h),
            ),
            (symbol_angle, 0, 2 * sympy.pi),
        )
    )
    mass_stack = integrate.quad(lambda value: np.pi * value ** 2, 0.0, HEIGHT_ONE)[0]
    print(f"mass at k = 1, h = 1: symbolic = {mass_symbolic}, "
          f"disk stack = {mass_stack:.9f}, formula pi*k*h**3/3 = {np.pi / 3.0:.9f}")
    assert sympy.simplify(mass_symbolic - sympy.pi * symbol_k * symbol_h ** 3 / 3) == 0, \
        "the symbolic mass is not pi*k*h**3/3"
    assert abs(mass_stack - np.pi / 3.0) <= 1.0e-9, "the disk stack mass is off"

    generator = np.random.default_rng(RANDOM_SEED)
    mass_mc, mass_error = monte_carlo_mass(SAMPLE_COUNT, HEIGHT_ONE, 1.0, generator)
    print(f"mass by Monte Carlo: computed = {mass_mc:.6f} +- {mass_error:.6f}, "
          f"expected = {np.pi / 3.0:.6f}, gap in standard errors = "
          f"{abs(mass_mc - np.pi / 3.0) / mass_error:.3f}")
    assert abs(mass_mc - np.pi / 3.0) <= 4.0 * mass_error, "the Monte Carlo mass is off"

    moment_symbolic = sympy.pi * symbol_k * symbol_h ** 5 / 10
    standard_form = sympy.Rational(3, 10) * (sympy.pi * symbol_k * symbol_h ** 3 / 3) * symbol_h ** 2
    print(f"standard cone form (3/10)*M*h**2: computed = {sympy.simplify(standard_form)}, "
          f"expected = {moment_symbolic}")
    assert sympy.simplify(standard_form - moment_symbolic) == 0, \
        "the standard cone form does not equal pi*k*h**5/10"

    moment_formula = float(moment_symbolic.subs({symbol_k: DENSITY, symbol_h: HEIGHT_DENSITY}))
    moment_numeric = numeric_moment(HEIGHT_DENSITY, DENSITY)
    print(f"at k = {DENSITY}, h = {HEIGHT_DENSITY}: formula = {moment_formula:.10f}, "
          f"triple quadrature = {moment_numeric:.10f}")
    assert abs(moment_formula - moment_numeric) <= 1.0e-9, "the formula and the quadrature disagree"

    moment_small = numeric_moment(HEIGHT_ONE, DENSITY)
    moment_large = numeric_moment(HEIGHT_SCALED, DENSITY)
    ratio = moment_large / moment_small
    print(f"scaling ratio I(2h)/I(h): computed = {ratio:.10f}, expected = 32.0")
    assert abs(ratio - 32.0) <= 1.0e-8, "the moment of inertia does not scale with h**5"

    ratio_formula = float(
        moment_symbolic.subs({symbol_k: DENSITY, symbol_h: 2 * HEIGHT_ONE})
        / moment_symbolic.subs({symbol_k: DENSITY, symbol_h: HEIGHT_ONE})
    )
    print(f"scaling ratio from the formula: computed = {ratio_formula:.10f}, expected = 32.0")
    assert abs(ratio_formula - 32.0) <= 1.0e-12, "the formula does not scale with h**5"

    print(f"answer: computed = pi*k*h**5/10, expected = pi*k*h**5/10; "
          f"value at k = {DENSITY}, h = {HEIGHT_DENSITY} is {moment_formula:.10f}")


if __name__ == "__main__":
    main()
