"""Check every numerical claim of Part 3 of the tutorial of Problem 15.7.55.

Part 3 evaluates the integral over $P$ by a change of variable to the unit ball and by spherical
coordinates. The script checks the Jacobian, the transformed integrand, the two factors of the
spherical integral, and the final value against three independent numerical routes.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import support

OUTPUT_PATH = CODE_DIRECTORY / "outputs" / "part3_results.json"
SETTING = (0.11, -0.27, 0.42)
SAMPLE_OFFSETS = ((0.3, -0.2, 0.5), (-0.6, 0.1, 0.2), (0.05, 0.33, -0.4),
                  (0.7, -0.05, -0.1), (-0.15, -0.35, 0.25))
GAUSS_ORDER = 80
MONTE_CARLO_COUNT = 3000000
MONTE_CARLO_SEED = 20261123
CUMULATIVE_RADII = (0.25, 0.5, 0.75, 1.0)


def transformed_point(x: float, y: float, z: float) -> tuple[float, float, float]:
    """Return $(u, v, w) = (x, \\sqrt{2} y, \\sqrt{3} z)$."""
    return (math.sqrt(support.COEFFICIENT_X_SQUARED) * x,
            math.sqrt(support.COEFFICIENT_Y_SQUARED) * y,
            math.sqrt(support.COEFFICIENT_Z_SQUARED) * z)


def main() -> None:
    """Run the checks of Part 3, print each comparison, and write the result file."""
    ledger = support.CheckLedger("part3")
    determinant = support.offset_matrix_determinant()
    ledger.add("jacobian_determinant_against_closed_form", determinant,
               1.0 / support.SQUARE_ROOT_OF_SIX, 1.0e-12)

    worst_mismatch = 0.0
    for offset in SAMPLE_OFFSETS:
        point = tuple(setting + step for setting, step in zip(SETTING, offset))
        u, v, w = transformed_point(*point)
        worst_mismatch = max(worst_mismatch, abs(support.integrand(*point)
                                                 - support.transformed_integrand(u, v, w)))
    ledger.add("pointwise_transformation_mismatch", worst_mismatch, 0.0, 1.0e-12)

    generator = np.random.default_rng(20261123)
    directions = generator.normal(size=(5000, 3))
    directions /= np.linalg.norm(directions, axis=1)[:, None]
    first, second, third = support.ellipsoid_semi_axes()
    points = np.column_stack([first * directions[:, 0], second * directions[:, 1],
                              third * directions[:, 2]])
    residuals = support.quadratic_form_array(points[:, 0], points[:, 1], points[:, 2]) - 1.0
    ledger.add("unit_sphere_maps_to_boundary_of_P", float(np.max(np.abs(residuals))), 0.0,
               1.0e-12)

    angular = support.spherical_angular_integral()
    ledger.add("angular_integral_against_four_pi", angular, 4.0 * math.pi, 1.0e-9)
    radial = support.radial_integral_quadrature()
    ledger.add("radial_integral_antiderivative_against_quadrature",
               support.radial_integral_exact(), radial, 1.0e-12)

    route_substitution = (1.0 / support.SQUARE_ROOT_OF_SIX) * angular * radial
    route_rationalized = support.exact_maximum_value_rationalized()
    ledger.add("substitution_route_against_rationalized_route", route_substitution,
               route_rationalized, 1.0e-12)

    cartesian = support.integrate_cartesian(support.integrand)
    ledger.add("cartesian_quadrature_against_exact_value", cartesian, route_substitution, 1.0e-9)
    gauss = support.integrate_gauss_legendre_scaled(support.integrand, GAUSS_ORDER)
    ledger.add("gauss_rule_against_exact_value", gauss, route_substitution, 1.0e-6)
    sample, sample_error = support.monte_carlo_ellipsoid(support.integrand, MONTE_CARLO_COUNT,
                                                         MONTE_CARLO_SEED)
    ledger.add("sample_against_exact_value", sample, route_substitution,
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * sample_error)

    volume = support.ellipsoid_volume_closed_form()
    mean_closed = route_substitution / volume
    ledger.add("mean_value_against_two_fifths", mean_closed, 0.4, 1.0e-12)
    mean_sample, mean_error = support.monte_carlo_ellipsoid_mean(support.integrand, 400000,
                                                                 MONTE_CARLO_SEED + 1)
    ledger.add("mean_sample_against_closed_mean", mean_sample, mean_closed,
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * mean_error)

    cumulative = support.cumulative_radial_integral(CUMULATIVE_RADII)
    ledger.add("cumulative_radial_at_one", cumulative[-1], radial, 1.0e-12)
    ledger.add_gap("cumulative_radial_increases", cumulative[1], cumulative[0], 0.01)
    ledger.add_gap("cumulative_radial_increases_again", cumulative[2], cumulative[1], 0.01)

    print(f"the Jacobian determinant is {determinant!r}")
    print(f"the angular factor is {angular!r} and the radial factor is {radial!r}")
    print(f"the exact value is {route_substitution!r} and {route_rationalized!r}")
    print(f"the Cartesian quadrature gives {cartesian!r}")
    print(f"the Gauss rule gives {gauss!r} at order {GAUSS_ORDER}")
    print(f"the sample gives {sample!r} with error {sample_error!r}")
    print(f"the mean value is {mean_closed!r}")
    print(f"the cumulative radial integral at {CUMULATIVE_RADII!r} is {cumulative!r}")

    support.write_results(OUTPUT_PATH, {
        "jacobian": determinant,
        "angular_factor": angular,
        "radial_factor": radial,
        "exact_value": route_substitution,
        "exact_value_rationalized": route_rationalized,
        "value_cartesian": cartesian,
        "value_gauss": gauss,
        "value_sample": sample,
        "value_sample_error": sample_error,
        "mean_value": mean_closed,
        "mean_sample": mean_sample,
        "mean_sample_error": mean_error,
        "cumulative_radii": list(CUMULATIVE_RADII),
        "cumulative_values": cumulative,
        "checks": ledger.summary(),
    })
    print(f"wrote {OUTPUT_PATH} with {ledger.summary()['count']} checks")


if __name__ == "__main__":
    main()
