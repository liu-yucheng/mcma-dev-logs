"""Check every numerical claim of Part 2 of the tutorial of Problem 15.7.55.

Part 2 proves that the ellipsoid $P$ is the maximizing region. The script compares the integral of
$f$ over $P$ with the integral over four other regions, splits one region into its parts inside and
outside $P$, and checks the derivative of the scaled family of ellipsoids.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import support

OUTPUT_PATH = CODE_DIRECTORY / "outputs" / "part2_results.json"
GAUSS_ORDER = 80
FINE_GAUSS_ORDER = 160
MONTE_CARLO_COUNT = 2000000
MONTE_CARLO_SEED = 20261123
REMOVED_BALL_RADIUS = 0.1


def integrate_over_box_of_positive_part(order: int) -> float:
    """Return $\\int_{box} \\max(f, 0)\\,dV$ by a tensor Gauss-Legendre rule on the box."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    total = 0.0
    for node_x, weight_x in zip(nodes, weights):
        for node_y, weight_y in zip(nodes, weights):
            values = np.maximum(0.0, support.integrand_array(
                np.full(order, node_x), np.full(order, node_y), nodes))
            total += weight_x * weight_y * float(np.dot(weights, values))
    return total


def integrate_ball_parts(radius: float) -> tuple[float, float]:
    """Return the integral over the part of a ball inside $P$ and over the part outside $P$."""
    def inner_inside(x: float, y: float) -> float:
        height_ball = math.sqrt(max(0.0, radius * radius - x * x - y * y))
        height_ellipsoid = math.sqrt(max(0.0, (1.0 - x * x - 2.0 * y * y) / 3.0))
        height = min(height_ball, height_ellipsoid)
        if height <= 0.0:
            return 0.0
        value, _ = integrate.quad(lambda z: support.integrand(x, y, z), -height, height,
                                  epsabs=1.0e-12, epsrel=1.0e-12)
        return value

    def inner_outside(x: float, y: float) -> float:
        height_ball = math.sqrt(max(0.0, radius * radius - x * x - y * y))
        height_ellipsoid = math.sqrt(max(0.0, (1.0 - x * x - 2.0 * y * y) / 3.0))
        if height_ball <= height_ellipsoid:
            return 0.0
        outer, _ = integrate.quad(lambda z: support.integrand(x, y, z),
                                  height_ellipsoid, height_ball, epsabs=1.0e-12, epsrel=1.0e-12)
        inner, _ = integrate.quad(lambda z: support.integrand(x, y, z),
                                  -height_ball, -height_ellipsoid, epsabs=1.0e-12,
                                  epsrel=1.0e-12)
        return outer + inner

    def middle(function, x: float) -> float:
        half_width = math.sqrt(max(0.0, radius * radius - x * x))
        value, _ = integrate.quad(lambda y: function(x, y), -half_width, half_width,
                                  epsabs=1.0e-12, epsrel=1.0e-12)
        return value

    inside, _ = integrate.quad(lambda x: middle(inner_inside, x), -radius, radius,
                               epsabs=1.0e-12, epsrel=1.0e-12)
    outside, _ = integrate.quad(lambda x: middle(inner_outside, x), -radius, radius,
                                epsabs=1.0e-12, epsrel=1.0e-12)
    return inside, outside


def monte_carlo_without_ball(radius: float, sample_count: int, seed: int) -> tuple[float, float]:
    """Estimate the integral of $f$ over $P$ without the ball of that radius."""
    generator = np.random.default_rng(seed)
    x = generator.uniform(-1.0, 1.0, sample_count)
    y = generator.uniform(-1.0, 1.0, sample_count)
    z = generator.uniform(-1.0, 1.0, sample_count)
    inside = support.quadratic_form_array(x, y, z) <= 1.0
    inner = x * x + y * y + z * z <= radius * radius
    weight = np.where(inside & ~inner, support.integrand_array(x, y, z), 0.0)
    estimate = 8.0 * float(np.mean(weight))
    error = 8.0 * float(np.std(weight, ddof=1)) / math.sqrt(sample_count)
    return estimate, error


def main() -> None:
    """Run the checks of Part 2, print each comparison, and write the result file."""
    ledger = support.CheckLedger("part2")
    maximum = support.exact_maximum_value()
    volume = support.ellipsoid_volume_closed_form()
    moment = support.exact_quadratic_form_moment()

    rows: list[dict[str, object]] = []
    candidate_specs = (
        ("ellipsoid P", maximum, support.integrate_gauss_legendre_scaled(support.integrand,
                                                                         GAUSS_ORDER)),
        ("unit ball", support.ball_integral_closed_form(1.0),
         support.ball_integral_quadrature(1.0)),
        ("unit cube", support.cube_integral_closed_form(0.5),
         support.cube_integral_quadrature(0.5)),
    )
    for name, closed_form, quadrature in candidate_specs:
        ledger.add(f"candidate_{name.replace(' ', '_')}_closed_form_against_quadrature",
                   quadrature, closed_form, 1.0e-7 * max(1.0, abs(closed_form)))
        rows.append({"name": name, "value": closed_form, "quadrature": quadrature,
                     "gap": maximum - closed_form})

    for scale in (0.8, 1.25):
        closed_form = support.scaled_ellipsoid_integral_closed_form(scale)
        quadrature = support.integrate_gauss_legendre_scaled(
            lambda x, y, z: scale ** 3 * support.integrand(scale * x, scale * y, scale * z),
            GAUSS_ORDER)
        name = f"scaled {scale:.2f}"
        ledger.add(f"candidate_scaled_{scale:.2f}_closed_form_against_quadrature",
                   quadrature, closed_form, 1.0e-5 * max(1.0, abs(closed_form)))
        rows.append({"name": name, "value": closed_form, "quadrature": quadrature,
                     "gap": maximum - closed_form})
        ledger.add_gap(f"candidate_scaled_{scale:.2f}_below_maximum", maximum, closed_form, 0.05)

    for row in rows:
        if row["name"] != "ellipsoid P":
            ledger.add_gap(f"candidate_{str(row['name']).replace(' ', '_')}_below_maximum",
                           maximum, float(row["value"]), 0.05)

    inside_ball, outside_ball = integrate_ball_parts(1.0)
    direct_ball = support.ball_integral_quadrature(1.0)
    ledger.add("ball_split_sum_against_direct_quadrature", inside_ball + outside_ball,
               direct_ball, 1.0e-8)
    ledger.add_gap("ball_part_outside_P_is_negative", 0.0, outside_ball, 0.5)

    positive_part = integrate_over_box_of_positive_part(FINE_GAUSS_ORDER)
    ledger.add("positive_part_over_box_against_maximum", positive_part, maximum, 2.0e-3)

    without_ball, without_ball_error = monte_carlo_without_ball(
        REMOVED_BALL_RADIUS, MONTE_CARLO_COUNT, MONTE_CARLO_SEED)
    gap_closed = support.ball_integral_closed_form(REMOVED_BALL_RADIUS)
    ledger.add("removed_ball_gap_against_closed_form", maximum - without_ball, gap_closed,
               support.MONTE_CARLO_STANDARD_ERROR_FACTOR * without_ball_error + 1.0e-6)

    trim = 1.0e-5
    derivative = (support.scaled_ellipsoid_integral_closed_form(1.0 + trim)
                  - support.scaled_ellipsoid_integral_closed_form(1.0 - trim)) / (2.0 * trim)
    ledger.add("scaled_family_derivative_at_one", derivative, 0.0, 1.0e-6)

    moment_quadrature = support.integrate_gauss_legendre_scaled(support.quadratic_form,
                                                                GAUSS_ORDER)
    ledger.add("quadratic_moment_against_closed_form", moment_quadrature, moment, 1.0e-5)
    ledger.add("stationarity_three_volume_against_five_moment", 5.0 * moment_quadrature,
               3.0 * volume, 1.0e-4)

    print(f"the maximum value is {maximum!r}")
    for row in rows:
        print(f"{row['name']}: value {row['value']!r}, gap to the maximum {row['gap']!r}")
    print(f"the ball splits into {inside_ball!r} inside P and {outside_ball!r} outside P")
    print(f"the derivative of the scaled family at one is {derivative!r}")

    support.write_results(OUTPUT_PATH, {
        "maximum_value": maximum,
        "candidate_rows": rows,
        "ball_inside": inside_ball,
        "ball_outside": outside_ball,
        "positive_part_over_box": positive_part,
        "removed_ball_gap": maximum - without_ball,
        "removed_ball_gap_error": without_ball_error,
        "scaled_derivative": derivative,
        "quadratic_moment": moment_quadrature,
        "checks": ledger.summary(),
    })
    print(f"wrote {OUTPUT_PATH} with {ledger.summary()['count']} checks")


if __name__ == "__main__":
    main()
