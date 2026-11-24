"""Verification of Part 3: the two orders with the inner integral in y.

The script checks four facts. First, a random tuple inside the printed limits maps to a point
of the solid. Second, a random point of the solid satisfies the printed limits. Third, the
area of the section at a fixed value of x from a two-dimensional quadrature agrees with the
closed form 2*(4 - x**2)**(3/2)/3 from the by-hand integration. Fourth, the adaptive
quadrature of both orders agrees with the exact rational multiple of pi from
exact_integrals.py.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import dblquad

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exact_integrals import exact_value
from iteration_forms import ORDER_LABELS, evaluate_dy_dx_dz, evaluate_dy_dz_dx, limits_are_met
from solid_geometry import inside_solid

# Random seed of every sampled check in this script.
RANDOM_SEED = 20261122

# Count of random points of each sampled check.
SAMPLE_COUNT = 200_000

# Values of x at which the section area is compared.
SECTION_POSITIONS = (0.0, 1.0, -1.0, 1.5, -1.5, 1.9)

# Tolerance of a compared pair.
TOLERANCE = 1.0e-8


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


def sample_parameter_points(form_name: str, count: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Draw points from the printed limits of one form and return their coordinates.

    The draw is uniform in the outermost variable, then uniform in the middle variable inside
    its printed interval, then uniform in the innermost variable inside its printed interval.

    Args:
        form_name: Name of the form, one of the keys of ORDER_LABELS.
        count: Count of points to draw.

    Returns:
        The three coordinate arrays of the drawn points.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    outer = generator.uniform(-1.0, 1.0, count)
    middle_unit = generator.uniform(-1.0, 1.0, count)
    inner_unit = generator.uniform(0.0, 1.0, count)
    if form_name == "dy_dz_dx":
        x = 2.0 * outer
        half_width_z = np.sqrt(np.maximum(4.0 - x**2, 0.0)) / 2.0
        z = middle_unit * half_width_z
        y = inner_unit * (4.0 - x**2 - 4.0 * z**2)
    elif form_name == "dy_dx_dz":
        z = outer
        half_width_x = 2.0 * np.sqrt(np.maximum(1.0 - z**2, 0.0))
        x = middle_unit * half_width_x
        y = inner_unit * (4.0 - x**2 - 4.0 * z**2)
    else:
        raise ValueError(f"the form {form_name} does not have the inner integral in y")
    return x, y, z


def check_limits_cover_the_solid() -> None:
    """Compare the printed limits of both orders with the defining inequalities of the solid.

    The check runs in two directions. A point drawn from the limits must lie in the solid, and
    a point drawn from the solid must satisfy the limits. One direction alone would accept
    limits that are too small or too large.
    """
    print("--- Section: the printed limits agree with the defining inequalities ---")
    generator = np.random.default_rng(RANDOM_SEED + 1)
    box_x = generator.uniform(-2.4, 2.4, SAMPLE_COUNT)
    box_y = generator.uniform(-0.4, 4.4, SAMPLE_COUNT)
    box_z = generator.uniform(-1.4, 1.4, SAMPLE_COUNT)
    inside = inside_solid(box_x, box_y, box_z)
    print(f"sample count of the box draw = {SAMPLE_COUNT}")
    print(f"points of the box draw inside the solid = {int(np.count_nonzero(inside))}")
    for form_name in ("dy_dz_dx", "dy_dx_dz"):
        admitting = limits_are_met(form_name, box_x, box_y, box_z)
        missing = int(np.count_nonzero(inside & ~admitting))
        extra = int(np.count_nonzero(admitting & ~inside))
        print(f"form {ORDER_LABELS[form_name]}: points of the solid outside the limits = {missing}, "
              f"points of the limits outside the solid = {extra}")
        assert missing == 0, "the printed limits miss a point of the solid"
        assert extra == 0, "the printed limits admit a point outside the solid"
        drawn_x, drawn_y, drawn_z = sample_parameter_points(form_name, SAMPLE_COUNT)
        outside = int(np.count_nonzero(~inside_solid(drawn_x, drawn_y, drawn_z)))
        excess_above_upper = float(np.max(np.maximum(
            drawn_y - (4.0 - drawn_x**2 - 4.0 * drawn_z**2), 0.0
        )))
        excess_below_zero = float(np.max(np.maximum(-drawn_y, 0.0)))
        print(f"form {ORDER_LABELS[form_name]}: points of the drawn set outside the solid = "
              f"{outside}, largest excess above the upper bound = {excess_above_upper:.3e}, "
              f"largest excess below zero = {excess_below_zero:.3e}")
        assert outside == 0, "a point inside the printed limits lies outside the solid"


def check_section_area_at_fixed_x() -> None:
    """Compare the section area at a fixed x from a quadrature with the closed form.

    At a fixed x the section is the set of (y, z) with 0 <= y <= 4 - x**2 - 4*z**2 and
    |z| <= sqrt(4 - x**2)/2. The by-hand integration of the height over z gives
    2*(4 - x**2)**(3/2)/3. The quadrature integrates the same height, so the two methods are
    independent.
    """
    print("--- Section: the area of the section at a fixed value of x ---")
    worst_difference = 0.0
    for position in SECTION_POSITIONS:
        radius_squared = 4.0 - position**2
        half_width = math.sqrt(radius_squared) / 2.0
        area_closed_form = 2.0 * radius_squared * math.sqrt(radius_squared) / 3.0
        area_quadrature, _ = dblquad(
            lambda inner_z, outer_y: 1.0,
            0.0,
            radius_squared,
            lambda outer_y: -math.sqrt(max(radius_squared - outer_y, 0.0)) / 2.0,
            lambda outer_y: math.sqrt(max(radius_squared - outer_y, 0.0)) / 2.0,
        )
        print(f"    half width in z at x = {position:.2f} is {half_width:.9f}")
        difference = report(f"section area at x = {position:.2f}", area_quadrature, area_closed_form)
        worst_difference = max(worst_difference, difference)
    assert worst_difference < TOLERANCE, "a section area disagrees with its closed form"


def check_values_of_both_orders() -> None:
    """Compare the two orders with the exact rational multiple of pi.

    The exact value of the integral of x**a * y**b * z**c over the solid is a rational multiple
    of pi from exact_integrals.py. The adaptive quadrature of each order is a different
    computation.
    """
    print("--- Section: the value of each order for two test functions ---")
    test_cases = ((0, 0, 0), (0, 1, 0))
    worst_difference = 0.0
    for form_name, integrate in (("dy_dz_dx", evaluate_dy_dz_dx), ("dy_dx_dz", evaluate_dy_dx_dz)):
        for exponents in test_cases:
            exponent_x, exponent_y, exponent_z = exponents
            value, error = integrate(
                lambda x, y, z, a=exponent_x, b=exponent_y, c=exponent_z: x**a * y**b * z**c
            )
            reference = exact_value(exponent_x, exponent_y, exponent_z)
            difference = report(
                f"form {ORDER_LABELS[form_name]} of x^{exponent_x} y^{exponent_y} z^{exponent_z}",
                value,
                reference,
            )
            print(f"    estimated absolute error of the quadrature = {error:.3e}")
            worst_difference = max(worst_difference, difference)
            assert difference < 1.0e-6, "an order disagrees with the exact value"
    print(f"largest difference over both orders and both functions = {worst_difference:.3e}")


def main() -> None:
    """Run every check of Part 3 and print the compared values."""
    check_limits_cover_the_solid()
    check_section_area_at_fixed_x()
    check_values_of_both_orders()
    print("Part 3: every compared pair agrees within the stated tolerance.")


if __name__ == "__main__":
    main()
