"""Check the two inner integrals of the moment of inertia.

The script computes the inner integral over z and the middle integral over r
with four methods: exact rational arithmetic on the hand antiderivative, the
symbolic integrator of SymPy, adaptive quadrature, and the composite Simpson
rule. Each pair of values is asserted against the tolerance of the method.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import sympy
from scipy import integrate
import importlib.metadata
import platform

RADIUS = 0.3
"""The radius r of the inner integral, in units of h."""

HEIGHT_ONE = 1.0
"""The first height h that the checks use."""

HEIGHT_TWO = 1.7
"""The second height h that the checks use."""

SAMPLE_COUNT = 20001
"""The number of points of the composite Simpson rule."""


def inner_integral_exact(radius: Fraction, height: Fraction) -> Fraction:
    """Return the exact value of the integral of r**3 over z from r to h.

    Args:
        radius: The radius r as an exact fraction.
        height: The height h as an exact fraction.

    Returns:
        The exact value r**3 * (h - r).
    """
    return radius ** 3 * (height - radius)


def middle_integral_exact(height: Fraction) -> Fraction:
    """Return the exact value of the integral of r**3 * (h - r) over r from 0 to h.

    Args:
        height: The height h as an exact fraction.

    Returns:
        The exact value h**5 / 20.
    """
    return height ** 5 / 20


def simpson_rule(values: np.ndarray, step: float) -> float:
    """Return the composite Simpson estimate of an integral on a uniform grid.

    Args:
        values: The sampled integrand on the uniform grid.
        step: The distance between two neighbouring grid points.

    Returns:
        The composite Simpson estimate of the integral.
    """
    weight = np.ones(values.size)
    weight[1:-1:2] = 4.0
    weight[2:-1:2] = 2.0
    return float(step / 3.0 * np.dot(weight, values))


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
    """Run the checks of Part 3 and print each computed value beside its expected value."""
    symbol_height, symbol_radius, symbol_z = sympy.symbols("h r z")

    symbolic_inner = sympy.integrate(symbol_radius ** 3, (symbol_z, symbol_radius, symbol_height))
    inner_value = sympy.simplify(symbolic_inner.subs({symbol_radius: sympy.Rational(3, 10),
                                                     symbol_height: 1}))
    inner_exact = inner_integral_exact(Fraction(3, 10), Fraction(1, 1))
    inner_quad, _ = integrate.quad(lambda value: RADIUS ** 3, RADIUS, HEIGHT_ONE)
    print(f"inner integral at r = {RADIUS}, h = 1: symbolic = {inner_value}, "
          f"exact arithmetic = {inner_exact} = {float(inner_exact):.8f}, "
          f"quad = {inner_quad:.8f}")
    assert sympy.simplify(symbolic_inner - symbol_radius ** 3 * (symbol_height - symbol_radius)) == 0
    assert inner_exact == Fraction(int(inner_value.p), int(inner_value.q)), \
        "the exact rational value and the symbolic value differ"
    assert abs(inner_quad - float(inner_exact)) <= 1.0e-12, "the quad value of the inner integral is off"

    symbolic_middle = sympy.integrate(symbol_radius ** 3 * (symbol_height - symbol_radius),
                                      (symbol_radius, 0, symbol_height))
    symbolic_middle = sympy.simplify(symbolic_middle)
    middle_exact = middle_integral_exact(Fraction(1, 1))

    grid_one = np.linspace(0.0, HEIGHT_ONE, SAMPLE_COUNT)
    values_one = grid_one ** 3 * (HEIGHT_ONE - grid_one)
    middle_quad_one, _ = integrate.quad(
        lambda value: value ** 3 * (HEIGHT_ONE - value), 0.0, HEIGHT_ONE
    )
    middle_simpson_one = simpson_rule(values_one, grid_one[1] - grid_one[0])
    print(f"middle integral, h = 1: symbolic = {symbolic_middle.subs(symbol_height, 1)}, "
          f"exact arithmetic = {middle_exact} = {float(middle_exact):.8f}, "
          f"quad = {middle_quad_one:.8f}, Simpson = {middle_simpson_one:.8f}")
    assert sympy.simplify(symbolic_middle - symbol_height ** 5 / 20) == 0, \
        "the symbolic middle integral is not h**5/20"
    assert middle_exact == Fraction(1, 20), "the exact rational middle integral is not 1/20"
    assert abs(middle_quad_one - float(middle_exact)) <= 1.0e-12, "the quad value of the middle integral is off"
    assert abs(middle_simpson_one - float(middle_exact)) <= 1.0e-12, "the Simpson value is off"

    grid_two = np.linspace(0.0, HEIGHT_TWO, SAMPLE_COUNT)
    values_two = grid_two ** 3 * (HEIGHT_TWO - grid_two)
    middle_quad_two, _ = integrate.quad(
        lambda value: value ** 3 * (HEIGHT_TWO - value), 0.0, HEIGHT_TWO
    )
    middle_simpson_two = simpson_rule(values_two, grid_two[1] - grid_two[0])
    formula_two = symbolic_middle.subs(symbol_height, sympy.Rational(17, 10)).evalf()
    print(f"middle integral, h = 1.7: formula h**5/20 = {float(formula_two):.10f}, "
          f"quad = {middle_quad_two:.10f}, Simpson = {middle_simpson_two:.10f}")
    assert abs(middle_quad_two - float(formula_two)) <= 1.0e-9, "the quad value at h = 1.7 is off"
    assert abs(middle_simpson_two - float(formula_two)) <= 1.0e-9, "the Simpson value at h = 1.7 is off"

    moment_from_middle = 2.0 * math.pi * float(middle_exact)
    moment_from_formula = math.pi / 10.0
    print(f"moment from 2*pi*h**5/20 at k = 1, h = 1: computed = {moment_from_middle:.10f}, "
          f"formula pi*k*h**5/10 = {moment_from_formula:.10f}")
    assert abs(moment_from_middle - moment_from_formula) <= 1.0e-15,         "the two forms of the moment of inertia disagree"


if __name__ == "__main__":
    main()
