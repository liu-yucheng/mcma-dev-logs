"""Check the exact maximum value of Part 4 of the tutorial of Problem 15.7.55.

Part 4 states the closed form of the maximum, its decimal value, and the mean-value
interpretation. The script compares a symbolic route with a rational route and with the
numeric routes of Part 1 and Part 3, so that no comparison holds one expression on both sides.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import support

OUTPUT_PATH = CODE_DIRECTORY / "outputs" / "part4_results.json"
OUTPUTS_DIRECTORY = CODE_DIRECTORY / "outputs"
DECIMAL_PLACES = 6
SIGN_SAMPLE_COUNT = 200000
SIGN_SAMPLE_SEED = 20261123
MIDPOINT_COUNT = 2000
SAMPLE_ERROR_FACTOR = 4.0


def load_part_results(part_number: int) -> dict[str, object]:
    """Return the result file of one earlier part."""
    path = OUTPUTS_DIRECTORY / f"part{part_number}_results.json"
    return json.loads(path.read_text(encoding="utf-8"))


def exact_radial_integral() -> Fraction:
    """Return the radial integral by the exact antiderivative with rational arithmetic."""
    upper = Fraction(1, 3) - Fraction(1, 5)
    lower = Fraction(0, 3) - Fraction(0, 5)
    return upper - lower


def square_of_first_form() -> Fraction:
    """Return the square of $8\\pi/(15\\sqrt{6})$, with the factor $\\pi^{2}$ removed exactly."""
    return Fraction(8, 15) ** 2 / 6


def square_of_second_form() -> Fraction:
    """Return the square of $4\\pi\\sqrt{6}/45$, with the factor $\\pi^{2}$ removed exactly."""
    return Fraction(4, 45) ** 2 * 6


def sign_agreement_count() -> tuple[int, int]:
    """Return the count of sign disagreements between $f$ and $1 - Q$, and the sample count."""
    generator = np.random.default_rng(SIGN_SAMPLE_SEED)
    x = generator.uniform(-1.2, 1.2, SIGN_SAMPLE_COUNT)
    y = generator.uniform(-0.85, 0.85, SIGN_SAMPLE_COUNT)
    z = generator.uniform(-0.7, 0.7, SIGN_SAMPLE_COUNT)
    inside_ellipsoid = support.quadratic_form_array(x, y, z) <= 1.0
    integrand_positive = support.integrand_array(x, y, z) > 0.0
    disagreements = int(np.count_nonzero(inside_ellipsoid != integrand_positive))
    return disagreements, SIGN_SAMPLE_COUNT


def main() -> None:
    """Run the checks of Part 4, print each comparison, and write the result file."""
    ledger = support.CheckLedger("part4")
    part_one = load_part_results(1)
    part_two = load_part_results(2)
    part_three = load_part_results(3)

    radial_exact = exact_radial_integral()
    ledger.add("radial_integral_fraction_against_part3_quadrature",
               float(radial_exact), float(part_three["radial_factor"]), 1.0e-12)

    first_square = square_of_first_form()
    second_square = square_of_second_form()
    print("CHECK squared_forms_carry_one_rational_coefficient")
    print(f"  computed = {first_square.numerator}/{first_square.denominator} from 8pi/(15 sqrt 6)")
    print(f"  expected = {second_square.numerator}/{second_square.denominator} from 4 pi sqrt 6 / 45")
    print(f"  {'PASS' if first_square == second_square else 'FAIL'}")
    if first_square != second_square:
        raise AssertionError("check failed: squared_forms_carry_one_rational_coefficient")
    ledger.records.append(support.CheckRecord(
        "squared_forms_carry_one_rational_coefficient", float(first_square),
        float(second_square), 0.0))

    symbolic_integral = sympy.integrate((1 - sympy.Symbol("r") ** 2) * sympy.Symbol("r") ** 2,
                                        (sympy.Symbol("r"), 0, 1))
    symbolic_value = sympy.simplify(sympy.Rational(1, 1) / sympy.sqrt(6)
                                    * 4 * sympy.pi * symbolic_integral)
    difference = sympy.simplify(symbolic_value
                                - sympy.Rational(8, 15) * sympy.pi / sympy.sqrt(6))
    print("CHECK symbolic_integral_against_closed_form")
    print(f"  computed = {symbolic_integral} from the computer algebra integral")
    print(f"  expected = {sympy.Rational(2, 15)} from 1/3 - 1/5")
    print(f"  simplified difference of the two closed forms = {difference}")
    if symbolic_integral != sympy.Rational(2, 15) or difference != 0:
        raise AssertionError("check failed: symbolic_integral_against_closed_form")
    ledger.records.append(support.CheckRecord(
        "symbolic_integral_against_closed_form", float(symbolic_integral),
        float(Fraction(2, 15)), 0.0))

    exact_value = support.exact_maximum_value()
    ledger.add("closed_form_against_part3_exact_value", exact_value,
               float(part_three["exact_value"]), 1.0e-12)
    ledger.add("rationalized_form_against_closed_form",
               support.exact_maximum_value_rationalized(), exact_value, 1.0e-15)
    ledger.add("closed_form_against_part2_maximum", exact_value,
               float(part_two["maximum_value"]), 1.0e-12)

    mean_value = float(Fraction(2, 5))
    mean_route = mean_value * float(part_one["ellipsoid_volume"])
    ledger.add("mean_value_route_against_closed_form", mean_route, exact_value, 1.0e-12)
    ledger.add("mean_value_against_part3_mean", mean_value,
               float(part_three["mean_value"]), 1.0e-12)

    sample = float(part_three["value_sample"])
    sample_error = float(part_three["value_sample_error"])
    ledger.add_gap("sample_interval_upper_above_exact",
                   sample + SAMPLE_ERROR_FACTOR * sample_error, exact_value, 0.0)
    ledger.add_gap("sample_interval_lower_below_exact",
                   exact_value, sample - SAMPLE_ERROR_FACTOR * sample_error, 0.0)

    radius_grid = np.linspace(0.0, 1.0, MIDPOINT_COUNT + 1)
    midpoint_radius = 0.5 * (radius_grid[:-1] + radius_grid[1:])
    midpoint_value = float(1.0 / MIDPOINT_COUNT
                           * np.sum((1.0 - midpoint_radius ** 2) * midpoint_radius ** 2))
    ledger.add("midpoint_rule_radial_against_closed_form",
               midpoint_value, float(radial_exact), 1.0e-4)
    ledger.add("cartesian_quadrature_against_closed_form",
               float(part_three["value_cartesian"]), exact_value, 1.0e-9)

    decimals = round(exact_value, DECIMAL_PLACES)
    ledger.add("six_decimal_rounding_against_part3_value",
               decimals, round(float(part_three["exact_value"]), DECIMAL_PLACES), 0.0)

    disagreements, sample_count = sign_agreement_count()
    ledger.add("sign_disagreements_against_zero", float(disagreements), 0.0, 0.0)
    print(f"the sign of f agreed with the test Q <= 1 at {sample_count - disagreements}"
          f" of {sample_count} sampled points")

    print(f"the radial integral is {radial_exact} exactly")
    print(f"the maximum value is {exact_value!r}, which rounds to {decimals:.6f}")
    print(f"the mean value of f over P is {mean_value!r}")
    print(f"the sample interval is [{sample - SAMPLE_ERROR_FACTOR * sample_error!r},"
          f" {sample + SAMPLE_ERROR_FACTOR * sample_error!r}]")

    support.write_results(OUTPUT_PATH, {
        "checks": ledger.summary(),
        "exact_value": exact_value,
        "exact_value_rationalized": support.exact_maximum_value_rationalized(),
        "six_decimals": decimals,
        "radial_integral": float(radial_exact),
        "mean_value": mean_value,
        "mean_route": mean_route,
        "sample_lower": sample - SAMPLE_ERROR_FACTOR * sample_error,
        "sample_upper": sample + SAMPLE_ERROR_FACTOR * sample_error,
        "sign_disagreements": disagreements,
        "sign_sample_count": sample_count,
        "squared_coefficient": [first_square.numerator, first_square.denominator],
    })
    print(f"wrote {OUTPUT_PATH} with {ledger.summary()['count']} checks")


if __name__ == "__main__":
    main()
