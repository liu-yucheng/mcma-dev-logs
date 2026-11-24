"""Verify Part 2: the mass of E.

The script derives the mass in three steps. It checks the inner integral in z at three points
with an independent quadrature. It checks the integral in y at three values of x. It checks the
three standard integrals in x with a quadrature. Finally it compares five independent values of
the mass: a symbolic integration, three nested quadratures, a Monte Carlo sample, and the sum of
the four terms of the linear decomposition of the density. The script writes
`code/results/part2_results.json`.
"""

from __future__ import annotations

import math

import numpy as np
import sympy

import common_region as region

X, Y, Z = sympy.symbols("x y z")
"""Symbols of the Cartesian coordinates."""

RHO = 1 + X + Y + Z
"""The density function of the statement."""


def inner_integral_in_z(x_value: float, y_value: float) -> float:
    """Return the analytic inner integral of rho over z from 0 to y."""
    return (1.0 + x_value) * y_value + 1.5 * y_value**2


def integral_in_y(x_value: float) -> float:
    """Return the analytic integral over the triangle at the given x."""
    outer = region.outer_radius(x_value)
    return (1.0 + x_value) * outer**2 / 2.0 + outer**3 / 2.0


def main() -> None:
    """Run every check of Part 2 and write the result record."""
    checks: list[dict[str, object]] = []
    tables: list[dict[str, object]] = []

    inner_symbolic = sympy.integrate(RHO, (Z, 0, Y))
    inner_symbolic = sympy.expand(inner_symbolic)
    print(f"[exact] inner integral in z: {inner_symbolic}")
    assert sympy.simplify(inner_symbolic - ((1 + X) * Y + sympy.Rational(3, 2) * Y**2)) == 0
    print("[check] the symbolic inner integral equals (1 + x)y + (3/2)y^2")

    rows_inner: list[list[str]] = []
    for x_value, y_value in ((0.0, 0.5), (0.3, 0.8), (0.7, 0.2)):
        from scipy.integrate import quad

        quad_value = quad(lambda z_value: region.density(x_value, y_value, z_value), 0.0, y_value, epsabs=1e-13, epsrel=1e-13)[0]
        formula_value = inner_integral_in_z(x_value, y_value)
        checks.append(
            region.check_close(
                f"inner integral in z at x={x_value:.1f}, y={y_value:.1f}, quadrature against the formula",
                quad_value,
                formula_value,
                1e-13,
            )
        )
        rows_inner.append(
            [
                region.decimal(x_value, 1),
                region.decimal(y_value, 1),
                region.decimal(formula_value, 6),
                region.decimal(quad_value, 6),
            ]
        )
    tables.append(
        {
            "caption": "The inner integral in $z$ of $\\rho$, checked at three points $(x,y)$",
            "columns": ["$x$", "$y$", "$(1+x)y+\\tfrac{3}{2}y^{2}$", "quadrature"],
            "rows": rows_inner,
        }
    )

    integral_symbolic = sympy.integrate(inner_symbolic, (Y, 0, sympy.sqrt(1 - X**2)))
    integral_symbolic = sympy.simplify(integral_symbolic)
    print(f"[exact] integral in y: {integral_symbolic}")
    expected_symbolic = sympy.simplify((1 + X) * (1 - X**2) / 2 + (1 - X**2) ** sympy.Rational(3, 2) / 2)
    assert sympy.simplify(integral_symbolic - expected_symbolic) == 0
    print("[check] the symbolic integral in y equals (1+x)(1-x^2)/2 + (1-x^2)^(3/2)/2")

    rows_section: list[list[str]] = []
    from scipy.integrate import dblquad

    for x_value in (0.0, 0.4, 0.8):
        outer = region.outer_radius(x_value)
        quad_value = dblquad(
            lambda z_value, y_value: region.density(x_value, y_value, z_value),
            0.0,
            outer,
            lambda y_value: 0.0,
            lambda y_value: y_value,
            epsabs=1e-12,
            epsrel=1e-12,
        )[0]
        formula_value = integral_in_y(x_value)
        checks.append(
            region.check_close(
                f"section mass at x={x_value:.1f}, two-dimensional quadrature against the formula",
                quad_value,
                formula_value,
                1e-10,
            )
        )
        rows_section.append(
            [
                region.decimal(x_value, 1),
                region.decimal(outer, 6),
                region.decimal(formula_value, 6),
                region.decimal(quad_value, 6),
            ]
        )
    tables.append(
        {
            "caption": "The mass of the section at a fixed $x$, checked at three values of $x$",
            "columns": ["$x$", "$Y$", "$(1+x)Y^{2}/2+Y^{3}/2$", "quadrature"],
            "rows": rows_section,
        }
    )

    standard_integrals = [
        (
            "$\int_0^1 (1-x^{2})\,dx$",
            sympy.integrate(1 - X**2, (X, 0, 1)),
            sympy.Rational(2, 3),
            lambda x_value: 1.0 - x_value * x_value,
        ),
        (
            "$\int_0^1 x(1-x^{2})\,dx$",
            sympy.integrate(X * (1 - X**2), (X, 0, 1)),
            sympy.Rational(1, 4),
            lambda x_value: x_value * (1.0 - x_value * x_value),
        ),
        (
            "$\int_0^1 (1-x^{2})^{3/2}\,dx$",
            sympy.integrate((1 - X**2) ** sympy.Rational(3, 2), (X, 0, 1)),
            3 * sympy.pi / 16,
            lambda x_value: (1.0 - x_value * x_value) ** 1.5,
        ),
    ]
    rows_standard: list[list[str]] = []
    from scipy.integrate import quad

    for latex_label, symbolic_value, claimed_value, numeric_function in standard_integrals:
        symbolic_value = sympy.simplify(symbolic_value)
        print(f"[exact] {latex_label} = {symbolic_value}")
        checks.append(region.check_close(f"{latex_label} against its closed form", float(symbolic_value), float(claimed_value), 1e-15))
        quad_value = quad(numeric_function, 0.0, 1.0, epsabs=1e-13, epsrel=1e-13)[0]
        checks.append(region.check_close(f"{latex_label}, quadrature against the closed form", quad_value, float(claimed_value), 1e-11))
        rows_standard.append(
            [
                latex_label,
                sympy.latex(symbolic_value),
                region.decimal(float(symbolic_value), 9),
                region.decimal(quad_value, 9),
            ]
        )
    tables.append(
        {
            "caption": "The three standard integrals in $x$",
            "columns": ["integral", "exact value", "decimal", "quadrature"],
            "rows": rows_standard,
        }
    )

    mass_symbolic = sympy.integrate(integral_symbolic, (X, 0, 1))
    mass_symbolic = sympy.simplify(mass_symbolic)
    print(f"[exact] m = {mass_symbolic}")
    claimed_mass = sympy.Rational(11, 24) + 3 * sympy.pi / 32
    assert sympy.simplify(mass_symbolic - claimed_mass) == 0
    print(f"[check] the symbolic mass equals 11/24 + 3pi/32 = {sympy.nsimplify(claimed_mass)}")
    checks.append(region.check_close("m against 11/24 + 3pi/32", float(mass_symbolic), float(claimed_mass), 1e-15))

    quadrature_mass, _ = region.integrate_with_nquad(lambda x_value, y_value, z_value: region.density(x_value, y_value, z_value), order="z_y_x")
    checks.append(region.check_close("m, quadrature in the order dz dy dx against the exact value", quadrature_mass, float(mass_symbolic), 1e-10))
    quadrature_second, _ = region.integrate_with_nquad(lambda x_value, y_value, z_value: region.density(x_value, y_value, z_value), order="y_z_x")
    checks.append(region.check_close("m, quadrature in the order dy dz dx against the exact value", quadrature_second, float(mass_symbolic), 1e-10))

    monte_carlo_mass, monte_carlo_error = region.monte_carlo_integral(
        region.masked_integrand(lambda x_values, y_values, z_values: region.density_array(x_values, y_values, z_values))
    )
    four_errors = 4.0 * monte_carlo_error
    print(
        f"[monte-carlo] m={monte_carlo_mass:.6f} standard_error={monte_carlo_error:.6f} "
        f"four_standard_errors={four_errors:.6f}"
    )
    checks.append(region.check_close("m, Monte Carlo against the exact value within four standard errors", monte_carlo_mass, float(mass_symbolic), four_errors))

    volume_term = sympy.integrate(1, (Z, 0, Y), (Y, 0, sympy.sqrt(1 - X**2)), (X, 0, 1))
    x_term = sympy.integrate(X, (Z, 0, Y), (Y, 0, sympy.sqrt(1 - X**2)), (X, 0, 1))
    y_term = sympy.integrate(Y, (Z, 0, Y), (Y, 0, sympy.sqrt(1 - X**2)), (X, 0, 1))
    z_term = sympy.integrate(Z, (Z, 0, Y), (Y, 0, sympy.sqrt(1 - X**2)), (X, 0, 1))
    linear_sum = sympy.simplify(volume_term + x_term + y_term + z_term)
    print(
        f"[linearity] volume={volume_term} x term={x_term} y term={y_term} z term={z_term} "
        f"sum={linear_sum}"
    )
    checks.append(
        region.check_close(
            "m, sum of the four terms of the linear decomposition against the direct integral",
            float(linear_sum),
            float(mass_symbolic),
            1e-15,
        )
    )
    rows_linear = [
        ["$\\int_E 1\\,dV$", sympy.latex(sympy.simplify(volume_term)), region.decimal(float(volume_term), 6)],
        ["$\\int_E x\\,dV$", sympy.latex(sympy.simplify(x_term)), region.decimal(float(x_term), 6)],
        ["$\\int_E y\\,dV$", sympy.latex(sympy.simplify(y_term)), region.decimal(float(y_term), 6)],
        ["$\\int_E z\\,dV$", sympy.latex(sympy.simplify(z_term)), region.decimal(float(z_term), 6)],
        ["sum", sympy.latex(sympy.simplify(linear_sum)), region.decimal(float(linear_sum), 6)],
    ]
    tables.append(
        {
            "caption": "The four terms of the linear decomposition of the mass",
            "columns": ["term", "exact value", "decimal"],
            "rows": rows_linear,
        }
    )

    largest_difference = max(float(record["difference"]) for record in checks)
    payload = {
        "part": 2,
        "title": "The mass of E",
        "checks": checks,
        "tables": tables,
        "facts": {
            "mass_exact": sympy.latex(claimed_mass),
            "mass_exact_text": "11/24 + 3\\pi/32",
            "mass_common_denominator": sympy.latex((44 + 9 * sympy.pi) / 96),
            "mass_decimal": region.decimal(float(claimed_mass), 6),
            "monte_carlo_mass": monte_carlo_mass,
            "monte_carlo_standard_error": monte_carlo_error,
            "largest_difference": largest_difference,
            "check_count": len(checks),
        },
    }
    region.write_result(2, payload)
    print(f"[summary] {len(checks)} checks, largest difference {largest_difference:.3e}")


if __name__ == "__main__":
    main()
