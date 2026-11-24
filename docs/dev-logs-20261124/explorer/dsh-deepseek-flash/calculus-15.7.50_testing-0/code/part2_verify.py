"""Verify the mass of the solid E of Problem 25.

The script checks the inner integral in x, the step that removes the z integral, and the final value
of the mass. The closed form uses the Beta function, the second route uses nested quadrature, and the
third route uses rejection sampling.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, special

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors
import verification_support as support

OUTPUT_PATH = Path(__file__).resolve().parent / "outputs" / "part2_results.json"
CHECKED_HEIGHTS = (0.6, 1.5, 2.4)


def density(x: float, y: float, z: float) -> float:
    """Return the density rho(x, y, z) = x^2 + y^2."""
    return x * x + y * y


def inner_integral_formula(y: float) -> float:
    """Return 28 y^3 / 81, the value of the integral of the density over x from 0 to y / 3."""
    return 28.0 * y ** 3 / 81.0


def inner_integral_direct(y: float) -> float:
    """Return the same integral from the antiderivative x^3 / 3 + x y^2, without simplification."""
    upper = support.x_upper(y)
    return upper ** 3 / 3.0 + upper * y * y


def inner_integral_gauss(y: float) -> float:
    """Return the same integral from a five point Gauss rule on the interval of x."""
    value, _ = integrate.fixed_quad(
        lambda x: density(x, y, 0.0), 0.0, support.x_upper(y), n=5)
    return value


def mass_closed_form() -> float:
    """Return the mass from the Beta function: (28 / 81) * 243 * B(2, 3 / 2) / 2."""
    return (28.0 / 81.0) * 243.0 * 0.5 * special.beta(2.0, 1.5)


def mass_without_the_plane() -> float:
    """Return the mass of the region that keeps x <= 1 instead of x <= y / 3."""
    inner = lambda y, z: integrate.quad(  # noqa: E731
        lambda x: density(x, y, z), 0.0, 1.0,
        epsabs=support.QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=support.QUADRATURE_RELATIVE_TOLERANCE)[0]
    middle = lambda y: integrate.quad(  # noqa: E731
        lambda z: inner(y, z), 0.0, support.cylinder_height(y),
        epsabs=support.QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=support.QUADRATURE_RELATIVE_TOLERANCE)[0]
    return integrate.quad(
        middle, 0.0, 3.0,
        epsabs=support.QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=support.QUADRATURE_RELATIVE_TOLERANCE)[0]


def mass_without_the_z_integral() -> float:
    """Return the value of the double integral over the yz projection, which drops the height."""
    return integrate.quad(
        lambda y: inner_integral_formula(y), 0.0, 3.0,
        epsabs=support.QUADRATURE_ABSOLUTE_TOLERANCE,
        epsrel=support.QUADRATURE_RELATIVE_TOLERANCE)[0]


def main() -> None:
    """Run every check of Part 2 and write the JSON result file."""
    print("PART 2: the mass M = the integral of x^2 + y^2 over E")
    ledger = support.CheckLedger("part2")
    inner_rows = []
    for y in CHECKED_HEIGHTS:
        formula = inner_integral_formula(y)
        direct = inner_integral_direct(y)
        gauss = inner_integral_gauss(y)
        print(f"inner integral at y = {y}: formula = {formula:.15f},"
              f" direct antiderivative = {direct:.15f}, Gauss = {gauss:.15f}")
        ledger.add(f"inner x integral at y = {y}", formula, direct, 1.0e-12)
        inner_rows.append({
            "y": f"{y:.1f}",
            "formula": f"{formula:.9f}",
            "direct": f"{direct:.9f}",
            "gauss": f"{gauss:.9f}",
            "difference": f"{abs(formula - direct):.2e}",
        })

    mass_beta = mass_closed_form()
    mass_quadrature = support.integrate_dx_dz_dy(density)
    mass_alternate = support.integrate_dz_dy_dx(density)
    mass_monte_carlo, mass_error = support.monte_carlo(
        density, figure_anchors.MONTE_CARLO_SAMPLE_COUNT, figure_anchors.MONTE_CARLO_SEED + 2)
    print(f"mass by the Beta function = {mass_beta:.12f}")
    print(f"mass by dx dz dy = {mass_quadrature:.12f}")
    print(f"mass by dz dy dx = {mass_alternate:.12f}")
    print(f"mass by Monte Carlo = {mass_monte_carlo:.12f} +- {mass_error:.12f}")
    ledger.add("mass: Beta function against quadrature",
               float(mass_beta), float(mass_quadrature), 1.0e-9)
    ledger.add("mass: two integration orders", mass_quadrature, mass_alternate, 1.0e-9)
    ledger.add("mass: quadrature against Monte Carlo", mass_quadrature, mass_monte_carlo,
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * mass_error)

    mass_without_plane = mass_without_the_plane()
    mass_without_z = mass_without_the_z_integral()
    print(f"mass with x <= 1 instead of x <= y / 3 = {mass_without_plane:.6f}")
    print(f"mass of the double integral over the projection = {mass_without_z:.6f}")
    print(f"mass against the mass with x <= 1 differ by"
          f" {abs(mass_without_plane - mass_quadrature):.6f}")

    results = {
        "mass": f"{mass_quadrature:.6f}",
        "mass_3dp": f"{mass_quadrature:.3f}",
        "mass_beta": f"{mass_beta:.9f}",
        "mass_quadrature": f"{mass_quadrature:.9f}",
        "mass_alternate": f"{mass_alternate:.9f}",
        "mass_monte_carlo": f"{mass_monte_carlo:.6f}",
        "mass_monte_carlo_error": f"{mass_error:.6f}",
        "mass_sigma_deviation": f"{abs(mass_monte_carlo - mass_quadrature) / mass_error:.3f}",
        "inner_rows": inner_rows,
        "inner_x_at_0_6": inner_rows[0]["formula"],
        "inner_x_at_1_5": inner_rows[1]["formula"],
        "inner_x_at_2_4": inner_rows[2]["formula"],
        "middle_integral_at_1_5": f"{inner_integral_formula(1.5) * float(np.sqrt(9.0 - 1.5 ** 2)):.6f}",
        "mass_without_plane": f"{mass_without_plane:.6f}",
        "mass_without_plane_3dp": f"{mass_without_plane:.3f}",
        "mass_without_z": f"{mass_without_z:.6f}",
        "mass_without_z_3dp": f"{mass_without_z:.3f}",
        "mean_density": f"{mass_quadrature / support.integrate_dx_dz_dy(lambda x, y, z: 1.0):.6f}",
        "checks": ledger.summary(),
    }
    support.write_results(OUTPUT_PATH, results)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
