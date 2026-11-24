"""Verify the center of mass of the solid E of Problem 25.

Each numerator uses a closed form, two nested quadratures in different orders, and one rejection
sample. Every coordinate is compared with a value from the sample route, and the standard error of
that route sets the tolerance. The script also prints three wrong candidates that a shortcut gives.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import special

sys.path.insert(0, str(Path(__file__).resolve().parent))

import figure_anchors
import verification_support as support

OUTPUT_PATH = Path(__file__).resolve().parent / "outputs" / "part3_results.json"
SAMPLE_COUNT = 1_500_000


def density(x: float, y: float, z: float) -> float:
    """Return the density rho(x, y, z) = x^2 + y^2."""
    return x * x + y * y


def first_numerator(x: float, y: float, z: float) -> float:
    """Return x times the density."""
    return x * density(x, y, z)


def second_numerator(x: float, y: float, z: float) -> float:
    """Return y times the density."""
    return y * density(x, y, z)


def third_numerator(x: float, y: float, z: float) -> float:
    """Return z times the density."""
    return z * density(x, y, z)


def beta_weight() -> float:
    """Return the integral of y^4 sqrt(9 - y^2) from 0 to 3, that is 729 B(5/2, 3/2) / 2."""
    return 729.0 * 0.5 * special.beta(2.5, 1.5)


def main() -> None:
    """Run every check of Part 3 and write the JSON result file."""
    print("PART 3: the center of mass of E")
    ledger = support.CheckLedger("part3")
    seed = figure_anchors.MONTE_CARLO_SEED + 3

    closed_forms = {
        "x rho": (19.0 / 324.0) * beta_weight(),
        "y rho": (28.0 / 81.0) * beta_weight(),
        "z rho": (14.0 / 81.0) * (9.0 * 81.0 / 4.0 - 729.0 / 6.0),
    }
    functions = {
        "x rho": first_numerator,
        "y rho": second_numerator,
        "z rho": third_numerator,
    }
    mass_closed = (28.0 / 81.0) * 243.0 * 0.5 * special.beta(2.0, 1.5)
    mass_exact = Fraction(28, 81) * Fraction(243, 1) * Fraction(2, 15)
    mass_exact_float = float(mass_exact)
    print(f"mass from the Beta function = {mass_closed:.12f}")
    print(f"mass from exact fractions = {mass_exact} = {mass_exact_float:.12f}")
    ledger.add("mass: Beta function against exact fractions",
               float(mass_closed), mass_exact_float, 1.0e-12)
    ledger.add("the Beta weight 2 / 15 against scipy.special.beta",
               float(special.beta(2.0, 1.5) / 2.0), float(Fraction(2, 15)), 1.0e-15)

    mass_estimate, mass_error = support.monte_carlo(density, SAMPLE_COUNT, seed - 1)
    values: dict[str, float] = {}
    errors: dict[str, float] = {}
    route_values: dict[str, list[float]] = {}
    numerator_rows = []
    for name, function in functions.items():
        closed_form = closed_forms[name]
        primary = support.integrate_dx_dz_dy(function)
        alternate = support.integrate_dz_dy_dx(function)
        estimate, error = support.monte_carlo(function, SAMPLE_COUNT, seed)
        print(f"numerator of {name}: closed form = {closed_form:.12f},"
              f" dx dz dy = {primary:.12f}, dz dy dx = {alternate:.12f},"
              f" Monte Carlo = {estimate:.12f} +- {error:.12f}")
        ledger.add(f"numerator of {name}: closed form against dx dz dy",
                   float(closed_form), float(primary), 1.0e-9)
        ledger.add(f"numerator of {name}: two integration orders",
                   float(primary), float(alternate), 1.0e-9)
        values[name] = primary
        errors[name] = error
        route_values[name] = [float(closed_form), float(primary), float(alternate)]
        numerator_rows.append({
            "name": name,
            "closed_form": f"{closed_form:.6f}",
            "primary": f"{primary:.6f}",
            "alternate": f"{alternate:.6f}",
            "monte_carlo": f"{estimate:.6f}",
            "error": f"{error:.6f}",
            "sigma": f"{abs(estimate - primary) / error:.3f}",
        })

    exact_third = Fraction(14, 81) * (Fraction(729, 4) - Fraction(243, 2))
    print(f"numerator of z rho from exact fractions = {exact_third} = {float(exact_third):.12f}")
    ledger.add("numerator of z rho: exact fractions against the floating closed form",
               float(exact_third), float(values["z rho"]), 1.0e-12)

    z_routes = route_values["z rho"] + [float(exact_third)]
    numerator_z_max_difference = max(z_routes) - min(z_routes)
    print(f"the spread of the four routes of numerator z rho = {numerator_z_max_difference:.6e}")
    ledger.add("numerator of z rho: the spread of the four routes",
               float(max(z_routes)), float(min(z_routes)), 1.0e-9)

    coordinate_names = {"x": "x rho", "y": "y rho", "z": "z rho"}
    coordinates: dict[str, float] = {}
    for axis, name in coordinate_names.items():
        closed_coordinate = values[name] / mass_closed
        sample_coordinate = (values[name] + 0.0) / mass_closed
        print(f"coordinate {axis} from the closed route = {closed_coordinate:.12f}")
        coordinates[axis] = closed_coordinate
    coordinate_sigmas: dict[str, float] = {}
    sample_coordinates = {}
    for axis, name in coordinate_names.items():
        estimate = float(numerator_rows[list(functions).index(name)]["monte_carlo"])
        sample_value = estimate / mass_estimate
        relative_error = math.hypot(errors[name] / values[name], mass_error / mass_estimate)
        sigma = abs(sample_value) * relative_error
        print(f"coordinate {axis} from the sample route = {sample_value:.12f} +- {sigma:.12f}")
        sample_coordinates[axis] = sample_value
        coordinate_sigmas[axis] = abs(sample_value - coordinates[axis]) / sigma
        ledger.add(f"coordinate {axis}: closed route against the sample route",
                   float(coordinates[axis]), float(sample_value),
                   support.MONTE_CARLO_STANDARD_ERROR_FACTOR * sigma)

    volume_value = support.integrate_dx_dz_dy(lambda x, y, z: 1.0)
    wrong_x_with_volume = values["x rho"] / volume_value
    uniform_x = support.integrate_dx_dz_dy(lambda x, y, z: x) / volume_value
    wrong_z_disc_centroid = 4.0 * 3.0 / (3.0 * math.pi)
    print(f"wrong candidate: numerator of x rho divided by the volume ="
          f" {wrong_x_with_volume:.6f}")
    print(f"comparison: coordinate x with a uniform density = {uniform_x:.6f}")
    print(f"wrong candidate: centroid height of the quarter disc = {wrong_z_disc_centroid:.6f}")
    support.add_difference(ledger, "the shortcut that divides by the volume misses x bar",
                           float(wrong_x_with_volume), float(coordinates["x"]), 0.1)
    support.add_difference(ledger, "the centroid of the projection misses z bar",
                           float(wrong_z_disc_centroid), float(coordinates["z"]), 0.1)

    inside = (
        3.0 * coordinates["x"] <= coordinates["y"] + 1.0e-12
        and coordinates["y"] ** 2 + coordinates["z"] ** 2 <= 9.0 + 1.0e-12
        and coordinates["x"] >= 0.0 and coordinates["y"] >= 0.0 and coordinates["z"] >= 0.0
    )
    print(f"the center of mass lies inside E: {inside}")
    ledger.add_text("the center of mass lies inside E", str(inside), "True")

    z_bar_exact = exact_third / mass_exact
    print(f"coordinate z from exact fractions = {z_bar_exact} = {float(z_bar_exact):.12f}")
    ledger.add("coordinate z: exact fractions against the floating closed route",
               float(z_bar_exact), float(coordinates["z"]), 1.0e-12)

    results = {
        "numerator_x": f"{values['x rho']:.6f}",
        "numerator_y": f"{values['y rho']:.6f}",
        "numerator_z": f"{values['z rho']:.6f}",
        "mass": f"{mass_closed:.6f}",
        "mass_exact": f"{mass_exact}",
        "volume": f"{volume_value:.6f}",
        "x_bar": f"{coordinates['x']:.6f}",
        "y_bar": f"{coordinates['y']:.6f}",
        "z_bar": f"{coordinates['z']:.6f}",
        "x_bar_3dp": support.rounded_three_decimals(coordinates["x"]),
        "y_bar_3dp": support.rounded_three_decimals(coordinates["y"]),
        "z_bar_3dp": support.exact_three_decimals(z_bar_exact.numerator, z_bar_exact.denominator),
        "z_bar_exact": f"{z_bar_exact}",
        "x_bar_uniform": f"{uniform_x:.6f}",
        "wrong_x_with_volume": f"{wrong_x_with_volume:.6f}",
        "wrong_z_disc_centroid": f"{wrong_z_disc_centroid:.6f}",
        "numerator_rows": numerator_rows,
        "numerator_z_max_difference": f"{numerator_z_max_difference:.2e}",
        "numerator_z_max_difference_latex": support.scientific_latex(numerator_z_max_difference),
        "coordinate_sigma_max": f"{max(coordinate_sigmas.values()):.3f}",
        "checks": ledger.summary(),
    }
    support.write_results(OUTPUT_PATH, results)
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
