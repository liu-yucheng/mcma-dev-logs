"""Verify Part 3: the center of mass of E.

The script computes the three first moments twice. The first method integrates each product of
two factors directly. The second method splits each product into four terms and adds the four
integrals. It then compares each exact coordinate with a nested quadrature, with a Monte Carlo
ratio, and with the difference ȳ - z̄ that the integrand (y - z) rho gives. The script writes
`code/results/part3_results.json`.
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

OUTER = sympy.sqrt(1 - X**2)
"""The largest y of E at a fixed x."""

X_BAR_TEXT = r"\frac{28}{44+9\pi}"
"""The LaTeX source of the exact x coordinate of the center of mass."""

Y_BAR_TEXT = r"\frac{2(15\pi+64)}{5(44+9\pi)}"
"""The LaTeX source of the exact y coordinate of the center of mass."""

Z_BAR_TEXT = r"\frac{45\pi+208}{15(44+9\pi)}"
"""The LaTeX source of the exact z coordinate of the center of mass."""


def integrate_over_region(expression: sympy.Expr) -> sympy.Expr:
    """Return the exact integral of one expression over E in the order dz dy dx."""
    value = sympy.integrate(expression, (Z, 0, Y), (Y, 0, OUTER), (X, 0, 1))
    return sympy.simplify(value)


def main() -> None:
    """Run every check of Part 3 and write the result record."""
    checks: list[dict[str, object]] = []
    tables: list[dict[str, object]] = []

    mass = integrate_over_region(RHO)
    moment_yz = integrate_over_region(X * RHO)
    moment_xz = integrate_over_region(Y * RHO)
    moment_xy = integrate_over_region(Z * RHO)
    print(f"[exact] m={mass} M_yz={moment_yz} M_xz={moment_xz} M_xy={moment_xy}")

    split_terms = {
        "M_yz": [X, X**2, X * Y, X * Z],
        "M_xz": [Y, X * Y, Y**2, Y * Z],
        "M_xy": [Z, X * Z, Y * Z, Z**2],
    }
    direct_values = {"M_yz": moment_yz, "M_xz": moment_xz, "M_xy": moment_xy}
    split_sums: dict[str, sympy.Expr] = {}
    rows_split: list[list[str]] = []
    for name, terms in split_terms.items():
        term_values = [integrate_over_region(term) for term in terms]
        total = sympy.simplify(sum(term_values))
        split_sums[name] = total
        print(f"[split] {name}: terms={term_values} sum={total} direct={direct_values[name]}")
        checks.append(
            region.check_close(
                f"{name}, sum of its four terms against the direct integral",
                float(total),
                float(direct_values[name]),
                1e-15,
            )
        )
        rows_split.append(
            [
                f"${name}$",
                " $+$ ".join(sympy.latex(sympy.simplify(value)) for value in term_values),
                sympy.latex(direct_values[name]),
            ]
        )
    tables.append(
        {
            "caption": "Each first moment, split into the four terms that the product of two factors gives",
            "columns": ["moment", "four terms", "direct value"],
            "rows": rows_split,
        }
    )

    for name, moment_expression, integrand in (
        ("M_yz", moment_yz, lambda x_value, y_value, z_value: x_value * region.density(x_value, y_value, z_value)),
        ("M_xz", moment_xz, lambda x_value, y_value, z_value: y_value * region.density(x_value, y_value, z_value)),
        ("M_xy", moment_xy, lambda x_value, y_value, z_value: z_value * region.density(x_value, y_value, z_value)),
    ):
        quadrature_value, _ = region.integrate_with_nquad(integrand, order="z_y_x")
        checks.append(
            region.check_close(
                f"{name}, quadrature in the order dz dy dx against the exact value",
                quadrature_value,
                float(moment_expression),
                1e-10,
            )
        )
        quadrature_second, _ = region.integrate_with_nquad(integrand, order="x_z_y")
        checks.append(
            region.check_close(
                f"{name}, quadrature in the order dx dz dy against the exact value",
                quadrature_second,
                float(moment_expression),
                1e-10,
            )
        )

    x_bar = sympy.simplify(moment_yz / mass)
    y_bar = sympy.simplify(moment_xz / mass)
    z_bar = sympy.simplify(moment_xy / mass)
    claimed_x = 28 / (44 + 9 * sympy.pi)
    claimed_y = (30 * sympy.pi + 128) / (220 + 45 * sympy.pi)
    claimed_z = (45 * sympy.pi + 208) / (15 * (44 + 9 * sympy.pi))
    print(f"[exact] x_bar={x_bar} = {sympy.nsimplify(x_bar)}")
    print(f"[exact] y_bar={y_bar} = {sympy.nsimplify(y_bar)}")
    print(f"[exact] z_bar={z_bar} = {sympy.nsimplify(z_bar)}")
    checks.append(region.check_close("x_bar against 28/(44+9pi)", float(x_bar), float(claimed_x), 1e-15))
    checks.append(region.check_close("y_bar against (30pi+128)/(220+45pi)", float(y_bar), float(claimed_y), 1e-15))
    checks.append(region.check_close("z_bar against (45pi+208)/(15(44+9pi))", float(z_bar), float(claimed_z), 1e-15))

    quadrature_mass, _ = region.integrate_with_nquad(lambda x_value, y_value, z_value: region.density(x_value, y_value, z_value), order="z_y_x")
    quadrature_yz, _ = region.integrate_with_nquad(lambda x_value, y_value, z_value: x_value * region.density(x_value, y_value, z_value), order="z_y_x")
    ratio_x = quadrature_yz / quadrature_mass
    checks.append(region.check_close("x_bar, ratio of two quadratures against the exact value", ratio_x, float(x_bar), 1e-10))

    monte_carlo_x, error_x = region.monte_carlo_ratio(
        region.masked_integrand(lambda x_values, y_values, z_values: x_values * region.density_array(x_values, y_values, z_values)),
        region.masked_integrand(lambda x_values, y_values, z_values: region.density_array(x_values, y_values, z_values)),
    )
    monte_carlo_y, error_y = region.monte_carlo_ratio(
        region.masked_integrand(lambda x_values, y_values, z_values: y_values * region.density_array(x_values, y_values, z_values)),
        region.masked_integrand(lambda x_values, y_values, z_values: region.density_array(x_values, y_values, z_values)),
    )
    monte_carlo_z, error_z = region.monte_carlo_ratio(
        region.masked_integrand(lambda x_values, y_values, z_values: z_values * region.density_array(x_values, y_values, z_values)),
        region.masked_integrand(lambda x_values, y_values, z_values: region.density_array(x_values, y_values, z_values)),
    )
    print(
        f"[monte-carlo] x_bar={monte_carlo_x:.6f}+-{error_x:.6f} y_bar={monte_carlo_y:.6f}+-{error_y:.6f} "
        f"z_bar={monte_carlo_z:.6f}+-{error_z:.6f}"
    )
    checks.append(region.check_close("x_bar, Monte Carlo ratio within four standard errors", monte_carlo_x, float(x_bar), 4.0 * error_x))
    checks.append(region.check_close("y_bar, Monte Carlo ratio within four standard errors", monte_carlo_y, float(y_bar), 4.0 * error_y))
    checks.append(region.check_close("z_bar, Monte Carlo ratio within four standard errors", monte_carlo_z, float(z_bar), 4.0 * error_z))

    difference_moment = integrate_over_region((Y - Z) * RHO)
    direct_difference, _ = region.integrate_with_nquad(
        lambda x_value, y_value, z_value: (y_value - z_value) * region.density(x_value, y_value, z_value),
        order="z_y_x",
    )
    checks.append(
        region.check_close(
            "M_xz - M_xy against the integral of (y - z) rho",
            float(moment_xz - moment_xy),
            float(difference_moment),
            1e-15,
        )
    )
    checks.append(
        region.check_close(
            "y_bar - z_bar against the quadrature of (y - z) rho divided by m",
            float(y_bar - z_bar),
            direct_difference / quadrature_mass,
            1e-10,
        )
    )

    inside = region.membership_mask(
        np.array([float(x_bar)]), np.array([float(y_bar)]), np.array([float(z_bar)])
    )[0]
    print(f"[center] the center of mass lies inside E: {bool(inside)}")
    assert bool(inside), "the center of mass lies outside E"
    print("[check] the center of mass satisfies the five defining inequalities")

    for label, value in (("x_bar", x_bar), ("y_bar", y_bar), ("z_bar", z_bar)):
        assert 0.0 < float(value) < 1.0, f"{label} lies outside the unit interval"
        print(f"[check] 0 < {label} < 1: {float(value):.6f}")

    largest_difference = max(float(record["difference"]) for record in checks)
    payload = {
        "part": 3,
        "title": "The center of mass of E",
        "checks": checks,
        "tables": tables,
        "facts": {
            "mass_exact": sympy.latex(mass),
            "moment_yz_exact": sympy.latex(moment_yz),
            "moment_xz_exact": sympy.latex(moment_xz),
            "moment_xy_exact": sympy.latex(moment_xy),
            "moment_yz_decimal": region.decimal(float(moment_yz), 6),
            "moment_xz_decimal": region.decimal(float(moment_xz), 6),
            "moment_xy_decimal": region.decimal(float(moment_xy), 6),
            "x_bar_exact": X_BAR_TEXT,
            "y_bar_exact": Y_BAR_TEXT,
            "z_bar_exact": Z_BAR_TEXT,
            "x_bar_decimal": region.decimal(float(x_bar), 6),
            "y_bar_decimal": region.decimal(float(y_bar), 6),
            "z_bar_decimal": region.decimal(float(z_bar), 6),
            "largest_difference": largest_difference,
            "check_count": len(checks),
        },
    }

    rows_moments: list[list[str]] = []
    for name, expression, decimal_value, integrand_check in (
        ("M_{yz}=\\int_E x\\rho\\,dV", moment_yz, None, None),
        ("M_{xz}=\\int_E y\\rho\\,dV", moment_xz, None, None),
        ("M_{xy}=\\int_E z\\rho\\,dV", moment_xy, None, None),
    ):
        rows_moments.append([f"${name}$", sympy.latex(expression), region.decimal(float(expression), 6)])
    payload["tables"] = payload["tables"] + [
        {
            "caption": "The three first moments of E",
            "columns": ["moment", "exact value", "decimal"],
            "rows": rows_moments,
        },
        {
            "caption": "The center of mass of E",
            "columns": ["coordinate", "exact value", "decimal"],
            "rows": [
                ["$\\bar{x}$", X_BAR_TEXT, region.decimal(float(x_bar), 6)],
                ["$\\bar{y}$", Y_BAR_TEXT, region.decimal(float(y_bar), 6)],
                ["$\\bar{z}$", Z_BAR_TEXT, region.decimal(float(z_bar), 6)],
            ],
        },
    ]
    region.write_result(3, payload)
    print(f"[summary] {len(checks)} checks, largest difference {largest_difference:.3e}")


if __name__ == "__main__":
    main()
