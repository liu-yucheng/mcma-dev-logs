"""Verification of Part 6: the table of the six orders and their equality.

The script evaluates every order for five test functions. It prints one table row for each
pair of an order and a function, compares each value with the exact rational multiple of pi
from exact_integrals.py, and compares the six values of one function with each other.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exact_integrals import exact_value
from iteration_forms import ORDER_LABELS, integrators

# The five test functions, named by the exponents of x, y, and z.
TEST_FUNCTIONS = ((0, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 0, 2))

# Tolerance of a compared pair of a volume integral.
TOLERANCE = 1.0e-6


def report(name: str, computed: float, reference: float) -> float:
    """Print one compared pair and return the absolute difference.

    Args:
        name: Label of the compared quantity.
        computed: Value from the first method.
        reference: Value from the second method.

    Returns:
        The absolute difference of the two values.
    """
    difference = abs(computed - reference)
    print(f"{name}: computed = {computed:.12f}  reference = {reference:.12f}  "
          f"difference = {difference:.3e}")
    return difference


def main() -> None:
    """Run the table and the equality checks of Part 6."""
    forms = integrators()
    collected: dict[tuple[int, int, int], list[float]] = {case: [] for case in TEST_FUNCTIONS}
    worst_difference = 0.0
    print("--- Section: the value of every order for every test function ---")
    for exponents in TEST_FUNCTIONS:
        exponent_x, exponent_y, exponent_z = exponents
        reference = exact_value(exponent_x, exponent_y, exponent_z)
        print(f"test function f = x^{exponent_x} y^{exponent_y} z^{exponent_z}: "
              f"exact value = {reference:.12f} = ({reference / 3.141592653589793:.9f}) pi")
        for form_name, integrate in forms.items():
            value, error = integrate(
                lambda x, y, z, a=exponent_x, b=exponent_y, c=exponent_z: x**a * y**b * z**c
            )
            difference = report(f"    order {ORDER_LABELS[form_name]}", value, reference)
            assert difference < TOLERANCE, "an order disagrees with the exact value"
            worst_difference = max(worst_difference, difference)
            collected[exponents].append(value)
        spread = max(collected[exponents]) - min(collected[exponents])
        print(f"    spread over the six orders = {spread:.3e}")
        assert spread < TOLERANCE, "the six orders of one function disagree"
    print("--- Section: the summary table ---")
    header = " ".join(f"{name:>16s}" for name in
                      ("volume", "integral of y", "integral of z", "integral of x^2",
                       "integral of z^2"))
    print(f"{'order':10s} {header}")
    for form_name in forms:
        values = [collected[exponents][list(forms).index(form_name)] for exponents in TEST_FUNCTIONS]
        row = " ".join(f"{value:16.9f}" for value in values)
        print(f"{ORDER_LABELS[form_name]:10s} {row}")
    print(f"largest difference over every pair of an order and a function = {worst_difference:.3e}")
    print("Part 6: every compared pair agrees within the stated tolerance.")


if __name__ == "__main__":
    main()
