"""Verify Part 4: the moment of inertia of E about the z axis.

The script computes I_z = integral of (x^2 + y^2) rho over E in five independent ways: one
direct exact integral, one exact split into the two second moments, one exact split into eight
monomial integrals, one exact integral in polar coordinates, and three numerical routes (two
Cartesian orders, one polar quadrature, one Monte Carlo sample). It then checks two bounds that
follow from 1 <= rho <= 1 + sqrt(5) on E. The script writes `code/results/part4_results.json`.
"""

from __future__ import annotations

import math

import numpy as np
import sympy

import common_region as region

X, Y, Z = sympy.symbols("x y z")
"""Symbols of the Cartesian coordinates."""

R, THETA = sympy.symbols("r theta", positive=True)
"""Symbols of the polar coordinates of the disk x^2 + y^2 <= 1."""

RHO = 1 + X + Y + Z
"""The density function of the statement."""

OUTER = sympy.sqrt(1 - X**2)
"""The largest y of E at a fixed x."""

DISTANCE_SQUARED = X**2 + Y**2
"""The square of the distance from a point to the z axis."""

I_Z_TEXT = r"\frac{17}{60}+\frac{\pi}{16}"
"""The LaTeX source of the exact moment of inertia about the z axis."""

MAXIMUM_DENSITY = 1.0 + math.sqrt(5.0)
"""The largest value of rho on E, which the point (1/sqrt(5), 2/sqrt(5), 2/sqrt(5)) attains."""


def integrate_over_region(expression: sympy.Expr) -> sympy.Expr:
    """Return the exact integral of one expression over E in the order dz dy dx."""
    return sympy.simplify(sympy.integrate(expression, (Z, 0, Y), (Y, 0, OUTER), (X, 0, 1)))


def integrate_in_polar(expression: sympy.Expr) -> sympy.Expr:
    """Return the exact integral of one Cartesian expression over E in polar coordinates.

    The substitution x = r cos(theta), y = r sin(theta) turns the disk x^2 + y^2 <= 1 into the
    rectangle 0 <= r <= 1, 0 <= theta <= pi/2, and it turns z <= y into z <= r sin(theta). The
    area element dx dy becomes r dr dtheta, so the volume element is r dz dr dtheta.
    """
    polar = expression.subs({X: R * sympy.cos(THETA), Y: R * sympy.sin(THETA)}, simultaneous=True)
    value = sympy.integrate(polar * R, (Z, 0, R * sympy.sin(THETA)), (R, 0, 1), (THETA, 0, sympy.pi / 2))
    return sympy.simplify(value)


def integrate_in_polar_numeric() -> float:
    """Return the integral of (x^2 + y^2) rho over E with a numerical polar quadrature."""
    from scipy.integrate import quad

    options = {"epsabs": 1e-13, "epsrel": 1e-13, "limit": 200}

    def after_theta(theta_value: float) -> float:
        """Integrate over r for one angle, then over z for one radius and that angle."""

        def after_radius(radius: float) -> float:
            """Integrate over z for one radius and one angle, with the Jacobian r."""
            return quad(
                lambda z_value: (radius**3)
                * (1.0 + radius * math.cos(theta_value) + radius * math.sin(theta_value) + z_value),
                0.0,
                radius * math.sin(theta_value),
                **options,
            )[0]

        return quad(after_radius, 0.0, 1.0, **options)[0]

    value, _ = quad(after_theta, 0.0, math.pi / 2.0, **options)
    return float(value)


def main() -> None:
    """Run every check of Part 4 and write the result record."""
    checks: list[dict[str, object]] = []
    bounds: list[dict[str, object]] = []
    tables: list[dict[str, object]] = []

    product = DISTANCE_SQUARED * RHO
    moment_of_inertia = integrate_over_region(product)
    print(f"[exact] I_z={moment_of_inertia} = {float(moment_of_inertia):.12f}")

    second_moment_x = integrate_over_region(X**2 * RHO)
    second_moment_y = integrate_over_region(Y**2 * RHO)
    print(f"[split] S_xx={second_moment_x} S_yy={second_moment_y} sum={second_moment_x + second_moment_y}")
    checks.append(
        region.check_close(
            "I_z, the sum of the two second moments against the direct integral",
            float(second_moment_x + second_moment_y),
            float(moment_of_inertia),
            1e-14,
        )
    )

    monomials = [X**2, Y**2, X**3, X**2 * Y, X**2 * Z, Y**3, X * Y**2, Y**2 * Z]
    monomial_values = [integrate_over_region(monomial) for monomial in monomials]
    monomial_sum = sympy.simplify(sum(monomial_values))
    print(f"[split] eight monomial terms={[str(value) for value in monomial_values]} sum={monomial_sum}")
    checks.append(
        region.check_close(
            "I_z, the sum of its eight monomial terms against the direct integral",
            float(monomial_sum),
            float(moment_of_inertia),
            1e-14,
        )
    )

    polar_exact = integrate_in_polar(product)
    print(f"[polar] exact value={polar_exact}")
    checks.append(
        region.check_close(
            "I_z, the exact polar integral against the direct integral",
            float(polar_exact),
            float(moment_of_inertia),
            1e-14,
        )
    )

    quadrature_order_z_y_x, _ = region.integrate_with_nquad(
        lambda x_value, y_value, z_value: (x_value**2 + y_value**2) * (1.0 + x_value + y_value + z_value),
        "z_y_x",
    )
    checks.append(
        region.check_close(
            "I_z, quadrature in the order dz dy dx against the exact value",
            quadrature_order_z_y_x,
            float(moment_of_inertia),
            1e-10,
        )
    )

    quadrature_order_x_z_y, _ = region.integrate_with_nquad(
        lambda x_value, y_value, z_value: (x_value**2 + y_value**2) * (1.0 + x_value + y_value + z_value),
        "x_z_y",
    )
    checks.append(
        region.check_close(
            "I_z, quadrature in the order dx dz dy against the exact value",
            quadrature_order_x_z_y,
            float(moment_of_inertia),
            1e-10,
        )
    )

    polar_numeric = integrate_in_polar_numeric()
    checks.append(
        region.check_close(
            "I_z, numerical polar quadrature against the exact value",
            polar_numeric,
            float(moment_of_inertia),
            1e-10,
        )
    )

    monte_carlo_value, monte_carlo_error = region.monte_carlo_integral(
        region.masked_integrand(
            lambda x_values, y_values, z_values: (x_values**2 + y_values**2)
            * region.density_array(x_values, y_values, z_values)
        )
    )
    print(f"[monte-carlo] I_z={monte_carlo_value:.6f}+-{monte_carlo_error:.6f}")
    checks.append(
        region.check_close(
            "I_z, Monte Carlo estimate within four standard errors",
            monte_carlo_value,
            float(moment_of_inertia),
            4.0 * monte_carlo_error,
        )
    )

    plain_moment = integrate_over_region(DISTANCE_SQUARED)
    plain_numeric, _ = region.integrate_with_nquad(lambda x_value, y_value, z_value: x_value**2 + y_value**2, "z_y_x")
    print(f"[bound] plain moment={plain_moment}={float(plain_moment):.12f}")
    checks.append(
        region.check_close(
            "the moment of the plain distance weight, quadrature against the exact value",
            plain_numeric,
            float(plain_moment),
            1e-10,
        )
    )
    print(
        f"[bound] 1 <= rho <= {MAXIMUM_DENSITY:.12f} on E, so the plain moment is a lower bound "
        f"and {MAXIMUM_DENSITY:.12f} times the plain moment is an upper bound"
    )
    if not float(plain_moment) < float(moment_of_inertia):
        raise AssertionError("The plain moment is not smaller than I_z, so the lower bound fails.")
    upper_bound = MAXIMUM_DENSITY * plain_numeric
    if not float(moment_of_inertia) < upper_bound:
        raise AssertionError("I_z is not smaller than the upper bound of the sandwich.")
    print(
        f"[check] lower bound {float(plain_moment):.12f} < I_z {float(moment_of_inertia):.12f} "
        f"< upper bound {upper_bound:.12f}"
    )
    bounds.append(
        {
            "label": "I_z inside the sandwich [plain moment, maximum density times plain moment]",
            "computed": float(moment_of_inertia),
            "expected": float(plain_moment),
            "difference": float(moment_of_inertia) - float(plain_moment),
            "tolerance": upper_bound - float(plain_moment),
        }
    )

    mass = integrate_over_region(RHO)
    if not float(moment_of_inertia) < float(mass):
        raise AssertionError("I_z is not smaller than the mass, although x^2 + y^2 <= 1 on E.")
    print(f"[check] I_z {float(moment_of_inertia):.12f} < m {float(mass):.12f} because x^2 + y^2 <= 1 on E")
    bounds.append(
        {
            "label": "I_z smaller than the mass, because the distance squared is at most one",
            "computed": float(moment_of_inertia),
            "expected": float(mass),
            "difference": float(mass) - float(moment_of_inertia),
            "tolerance": float(mass),
        }
    )

    generator = np.random.default_rng(region.RANDOM_SEED + 4)
    sample = generator.random((region.MONTE_CARLO_SAMPLE_COUNT, 3))
    inside = region.membership_mask(sample[:, 0], sample[:, 1], sample[:, 2])
    sampled_density = region.density_array(sample[:, 0], sample[:, 1], sample[:, 2])[inside]
    largest_sampled_density = float(sampled_density.max())
    print(f"[check] largest sampled density {largest_sampled_density:.6f} <= {MAXIMUM_DENSITY:.6f}")
    if not largest_sampled_density <= MAXIMUM_DENSITY:
        raise AssertionError("A sampled point of E has a density above the stated maximum.")
    checks.append(
        {
            "label": "largest sampled density at or below the maximum density",
            "computed": largest_sampled_density,
            "expected": MAXIMUM_DENSITY,
            "difference": MAXIMUM_DENSITY - largest_sampled_density,
            "tolerance": MAXIMUM_DENSITY - 1.0,
        }
    )

    mean_distance_squared = float(moment_of_inertia) / float(mass)
    numeric_mean = quadrature_order_z_y_x / float(region.integrate_with_nquad(
        lambda x_value, y_value, z_value: 1.0 + x_value + y_value + z_value, "z_y_x"
    )[0])
    checks.append(
        region.check_close(
            "the density-weighted mean of x^2 + y^2, exact quotient against the quadrature quotient",
            numeric_mean,
            mean_distance_squared,
            1e-10,
        )
    )
    if not 0.0 < mean_distance_squared < 1.0:
        raise AssertionError("The mean of x^2 + y^2 is outside the interval (0, 1).")

    rows_terms = [
        [f"${sympy.latex(monomial)}$", sympy.latex(value), region.decimal(float(value), 6)]
        for monomial, value in zip(monomials, monomial_values)
    ]
    payload = {
        "part": 4,
        "title": "The moment of inertia of E about the z axis",
        "checks": checks,
        "bounds": bounds,
        "tables": [
            {
                "caption": "The eight monomial integrals of the moment of inertia",
                "columns": ["term", "exact integral", "decimal"],
                "rows": rows_terms,
            },
            {
                "caption": "The moment of inertia and its two second moments",
                "columns": ["quantity", "exact value", "decimal"],
                "rows": [
                    ["$I_z$", I_Z_TEXT, region.decimal(float(moment_of_inertia), 6)],
                    [r"$\int_E x^2\rho\,dV$", sympy.latex(second_moment_x), region.decimal(float(second_moment_x), 6)],
                    [r"$\int_E y^2\rho\,dV$", sympy.latex(second_moment_y), region.decimal(float(second_moment_y), 6)],
                    [r"$\int_E (x^2+y^2)\,dV$", sympy.latex(plain_moment), region.decimal(float(plain_moment), 6)],
                ],
            },
        ],
        "facts": {
            "moment_of_inertia_exact": I_Z_TEXT,
            "moment_of_inertia_decimal": region.decimal(float(moment_of_inertia), 6),
            "second_moment_x_exact": sympy.latex(second_moment_x),
            "second_moment_y_exact": sympy.latex(second_moment_y),
            "second_moment_x_decimal": region.decimal(float(second_moment_x), 6),
            "second_moment_y_decimal": region.decimal(float(second_moment_y), 6),
            "plain_moment_exact": sympy.latex(plain_moment),
            "plain_moment_decimal": region.decimal(float(plain_moment), 6),
            "polar_exact": sympy.latex(polar_exact),
            "maximum_density_decimal": region.decimal(MAXIMUM_DENSITY, 6),
            "upper_bound_decimal": region.decimal(MAXIMUM_DENSITY * float(plain_moment), 6),
            "mean_distance_squared_decimal": region.decimal(mean_distance_squared, 6),
            "monte_carlo_value": region.decimal(monte_carlo_value, 6),
            "monte_carlo_error": region.decimal(monte_carlo_error, 6),
            "largest_difference": max(float(record["difference"]) for record in checks),
            "check_count": len(checks),
        },
    }
    region.write_result(4, payload)
    largest_difference = max(float(record["difference"]) for record in checks)
    print(f"[summary] {len(checks)} checks, largest difference {largest_difference:.3e}")


if __name__ == "__main__":
    main()
