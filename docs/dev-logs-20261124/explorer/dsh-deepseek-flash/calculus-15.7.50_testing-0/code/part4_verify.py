"""Verify the moment of inertia about the z-axis of the solid E of Problem 25.

The integrand is (x^2 + y^2) times the density, that is (x^2 + y^2)^2. The script checks the inner
integral in x, the closed form with the Beta function, a second integration order, and a sample.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import integrate, special

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors
import verification_support as support

OUTPUT_PATH = Path(__file__).resolve().parent / "outputs" / "part4_results.json"
CHECKED_HEIGHTS = (0.6, 1.5, 2.4)


def integrand(x: float, y: float, z: float) -> float:
    """Return (x^2 + y^2)^2, the product of the squared radius and the density."""
    radius_squared = x * x + y * y
    return radius_squared * radius_squared


def inner_formula(y: float) -> float:
    """Return 436 y^5 / 1215, the integral of the integrand over x from 0 to y / 3."""
    return 436.0 * y ** 5 / 1215.0


def inner_direct(y: float) -> float:
    """Return the same integral from the antiderivative x^5/5 + 2 x^3 y^2/3 + x y^4."""
    upper = support.x_upper(y)
    return upper ** 5 / 5.0 + 2.0 * upper ** 3 * y * y / 3.0 + upper * y ** 4


def mass() -> float:
    """Return the mass of E, computed here from the Beta function."""
    return (28.0 / 81.0) * 243.0 * 0.5 * special.beta(2.0, 1.5)


def main() -> None:
    """Run every check of Part 4 and write the JSON result file."""
    print("PART 4: the moment of inertia about the z-axis")
    ledger = support.CheckLedger("part4")
    seed = figure_anchors.MONTE_CARLO_SEED + 4
    inner_rows = []
    for y in CHECKED_HEIGHTS:
        formula = inner_formula(y)
        direct = inner_direct(y)
        gauss, _ = integrate.fixed_quad(lambda x: integrand(x, y, 0.0), 0.0,
                                        support.x_upper(y), n=5)
        print(f"inner integral at y = {y}: formula = {formula:.12f},"
              f" antiderivative = {direct:.12f}, Gauss = {gauss:.12f}")
        ledger.add(f"inner x integral of the inertia at y = {y}",
                   float(formula), float(direct), 1.0e-12)
        inner_rows.append({
            "y": f"{y:.1f}",
            "formula": f"{formula:.9f}",
            "direct": f"{direct:.9f}",
            "gauss": f"{gauss:.9f}",
            "difference": f"{abs(formula - direct):.2e}",
        })

    inertia_closed = (436.0 / 1215.0) * 2187.0 * 0.5 * special.beta(3.0, 1.5)
    inertia_primary = support.integrate_dx_dz_dy(integrand)
    inertia_alternate = support.integrate_dz_dy_dx(integrand)
    inertia_sample, inertia_error = support.monte_carlo(
        integrand, figure_anchors.MONTE_CARLO_SAMPLE_COUNT, seed)
    print(f"inertia by the Beta function = {inertia_closed:.12f}")
    print(f"inertia by dx dz dy = {inertia_primary:.12f}")
    print(f"inertia by dz dy dx = {inertia_alternate:.12f}")
    print(f"inertia by Monte Carlo = {inertia_sample:.12f} +- {inertia_error:.12f}")
    ledger.add("inertia: Beta function against quadrature",
               float(inertia_closed), float(inertia_primary), 1.0e-8)
    ledger.add("inertia: two integration orders",
               float(inertia_primary), float(inertia_alternate), 1.0e-9)
    ledger.add("inertia: quadrature against Monte Carlo",
               float(inertia_primary), float(inertia_sample),
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * inertia_error)

    substitution_integral, _ = integrate.quad(lambda y: y ** 5 * np.sqrt(9.0 - y * y), 0.0, 3.0)
    substitution_factor = 3.0 ** 7 * 0.5 * special.beta(3.0, 1.5)
    print(f"the integral of y^5 sqrt(9 - y^2) by quadrature = {substitution_integral:.12f}")
    print(f"the same integral as 3^7 times B(3, 3/2) / 2 = {substitution_factor:.12f}")
    print(f"the substitution power of 3 = {(substitution_integral / (0.5 * special.beta(3.0, 1.5))):.6f}"
          f" against 3^7 = {3.0 ** 7:.1f}")
    ledger.add("the substitution y = 3 t gives the factor 3^7 = 2187",
               float(substitution_integral), float(substitution_factor), 1.0e-9)

    substitution_ratio = substitution_integral / (0.5 * special.beta(3.0, 1.5))
    substitution_exponent = int(round(np.log(substitution_ratio) / np.log(3.0)))
    print(f"the ratio of the integral to the Beta value = {substitution_ratio:.9f}")
    print(f"the exponent of 3 recovered from the ratio = {substitution_exponent}")
    ledger.add("the exponent of 3 recovered from the integral is an integer power",
               float(3.0 ** substitution_exponent), float(substitution_ratio),
               float(substitution_ratio) * 1.0e-9)

    repeated_mass = support.integrate_dx_dz_dy(lambda x, y, z: x * x + y * y)
    print(f"the integral of the density itself, a second route to the mass ="
          f" {repeated_mass:.12f}")
    ledger.add("the integral of the density is the mass of Part 2",
               float(repeated_mass), float(mass()), 1.0e-9)
    inertia_at_the_cylinder_radius = 9.0 * mass()
    print(f"wrong candidate: every point at the radius 3 gives 9 M ="
          f" {inertia_at_the_cylinder_radius:.6f}")
    support.add_difference(ledger, "the radius of the cylinder overstates the inertia",
                           float(inertia_at_the_cylinder_radius), float(inertia_primary), 1.0)

    mean_square_radius = inertia_primary / mass()
    print(f"mean squared distance from the z-axis = {mean_square_radius:.12f}")
    ledger.add("the mean squared radius is the inertia over the mass",
               float(mean_square_radius * mass()), float(inertia_primary), 1.0e-9)

    results = {
        "iz": f"{inertia_primary:.6f}",
        "iz_3dp": support.rounded_three_decimals(inertia_primary),
        "iz_closed": f"{inertia_closed:.9f}",
        "iz_alternate": f"{inertia_alternate:.9f}",
        "iz_monte_carlo": f"{inertia_sample:.6f}",
        "iz_monte_carlo_error": f"{inertia_error:.6f}",
        "iz_sigma": f"{abs(inertia_sample - inertia_primary) / inertia_error:.3f}",
        "repeated_mass": f"{repeated_mass:.6f}",
        "iz_at_cylinder_radius": f"{inertia_at_the_cylinder_radius:.6f}",
        "mean_square_radius": f"{mean_square_radius:.6f}",
        "substitution_integral": f"{substitution_integral:.6f}",
        "substitution_factor": f"{substitution_factor:.6f}",
        "substitution_power": f"{substitution_ratio:.6f}",
        "substitution_exponent": substitution_exponent,
        "substitution_ratio": f"{substitution_ratio:.0f}",
        "inner_rows": inner_rows,
        "inner_iz_at_0_6": inner_rows[0]["formula"],
        "inner_iz_at_1_5": inner_rows[1]["formula"],
        "inner_iz_at_2_4": inner_rows[2]["formula"],
        "checks": ledger.summary(),
    }
    support.write_results(OUTPUT_PATH, results)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
