"""Verification of Part 4: the two orders with the inner integral in z.

The script checks four facts. First, a random tuple inside the printed limits of either order
maps to a point of the solid, and a random point of the solid satisfies the printed limits.
Second, the half width in z at a fixed pair (x, y) from a root find on the upper surface agrees
with the closed form sqrt(4 - x**2 - y)/2. Third, each outer region is one interval at every
fixed value of its outer variable, so the order needs no split. Fourth, the adaptive quadrature
of both orders agrees with the exact rational multiple of pi from exact_integrals.py.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exact_integrals import exact_value
from iteration_forms import ORDER_LABELS, evaluate_dz_dx_dy, evaluate_dz_dy_dx, limits_are_met
from solid_geometry import inside_solid

# Random seed of every sampled check in this script.
RANDOM_SEED = 20261123

# Count of random points of each sampled check.
SAMPLE_COUNT = 200_000

# Count of samples along one line of the contiguity check.
LINE_SAMPLE_COUNT = 4001

# Pairs (x, y) of the root-find check. Each pair satisfies 4 - x**2 - y > 0.
ROOT_FIND_PAIRS = ((0.0, 0.0), (1.0, 1.0), (-1.5, 1.5), (1.9, 0.2), (0.5, 3.0))

# Tolerance of a compared pair.
TOLERANCE = 1.0e-9


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
    """Draw points from the printed limits of one order with the inner integral in z.

    Args:
        form_name: Name of the form, either dz_dy_dx or dz_dx_dy.
        count: Count of points to draw.

    Returns:
        The three coordinate arrays of the drawn points.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    outer = generator.uniform(-1.0, 1.0, count)
    middle_unit = generator.uniform(-1.0, 1.0, count)
    inner_unit = generator.uniform(-1.0, 1.0, count)
    if form_name == "dz_dy_dx":
        x = 2.0 * outer
        y = (4.0 - x**2) * (middle_unit + 1.0) / 2.0
        half_width_z = np.sqrt(np.maximum(4.0 - x**2 - y, 0.0)) / 2.0
        z = inner_unit * half_width_z
    elif form_name == "dz_dx_dy":
        y = 2.0 * (outer + 1.0)
        half_width_x = np.sqrt(np.maximum(4.0 - y, 0.0))
        x = middle_unit * half_width_x
        half_width_z = np.sqrt(np.maximum(4.0 - y - x**2, 0.0)) / 2.0
        z = inner_unit * half_width_z
    else:
        raise ValueError(f"the form {form_name} does not have the inner integral in z")
    return x, y, z


def check_limits_cover_the_solid() -> None:
    """Compare the printed limits of both orders with the defining inequalities of the solid."""
    print("--- Section: the printed limits agree with the defining inequalities ---")
    generator = np.random.default_rng(RANDOM_SEED + 1)
    box_x = generator.uniform(-2.4, 2.4, SAMPLE_COUNT)
    box_y = generator.uniform(-0.4, 4.4, SAMPLE_COUNT)
    box_z = generator.uniform(-1.4, 1.4, SAMPLE_COUNT)
    inside = inside_solid(box_x, box_y, box_z)
    print(f"sample count of the box draw = {SAMPLE_COUNT}")
    print(f"points of the box draw inside the solid = {int(np.count_nonzero(inside))}")
    for form_name in ("dz_dy_dx", "dz_dx_dy"):
        admitting = limits_are_met(form_name, box_x, box_y, box_z)
        missing = int(np.count_nonzero(inside & ~admitting))
        extra = int(np.count_nonzero(admitting & ~inside))
        print(f"form {ORDER_LABELS[form_name]}: points of the solid outside the limits = {missing}, "
              f"points of the limits outside the solid = {extra}")
        assert missing == 0, "the printed limits miss a point of the solid"
        assert extra == 0, "the printed limits admit a point outside the solid"
        drawn_x, drawn_y, drawn_z = sample_parameter_points(form_name, SAMPLE_COUNT)
        outside = int(np.count_nonzero(~inside_solid(drawn_x, drawn_y, drawn_z)))
        excess = float(np.max(np.maximum(drawn_y - (4.0 - drawn_x**2 - 4.0 * drawn_z**2), 0.0)))
        print(f"form {ORDER_LABELS[form_name]}: points of the drawn set outside the solid = "
              f"{outside}, largest excess above the upper bound = {excess:.3e}")
        assert outside == 0, "a point inside the printed limits lies outside the solid"


def check_half_width_in_z() -> None:
    """Compare the half width in z from a root find with the closed form.

    At a fixed pair (x, y) the top wall of the solid meets the plane y = const where
    4 - x**2 - 4*z**2 = y. A root find on that equation gives the half width. The closed form
    sqrt(4 - x**2 - y)/2 solves the same equation by hand.
    """
    print("--- Section: the half width in z at a fixed pair (x, y) ---")
    worst_difference = 0.0
    for position_x, position_y in ROOT_FIND_PAIRS:
        radicand = 4.0 - position_x**2 - position_y
        print(f"    pair (x, y) = ({position_x:.2f}, {position_y:.2f}) has 4 - x**2 - y = "
              f"{radicand:.6f}")
        assert radicand > 0.0, "the pair lies above the top wall, so it has no root"
        root = brentq(lambda value: 4.0 - position_x**2 - 4.0 * value**2 - position_y, 0.0, 1.0)
        closed_form = math.sqrt(4.0 - position_x**2 - position_y) / 2.0
        difference = report(
            f"half width in z at (x, y) = ({position_x:.2f}, {position_y:.2f})",
            root,
            closed_form,
        )
        worst_difference = max(worst_difference, difference)
        full_width = 2.0 * closed_form
        print(f"    full width in z = {full_width:.12f}, which is sqrt(4 - x**2 - y) = "
              f"{math.sqrt(4.0 - position_x**2 - position_y):.12f}")
    assert worst_difference < TOLERANCE, "a half width disagrees with its closed form"


def count_runs(admissible: np.ndarray) -> int:
    """Return the count of separate runs of True values along a Boolean array.

    Args:
        admissible: Boolean array of the membership along one line.

    Returns:
        The count of maximal runs of True values.
    """
    padded = np.concatenate(([False], np.asarray(admissible, dtype=bool), [False]))
    transitions = np.diff(padded.astype(np.int8))
    return int(np.count_nonzero(transitions == 1))


def check_no_split_is_needed() -> None:
    """Check that each outer region is one interval at every fixed value of the outer variable.

    A split of an iterated integral is necessary only when the outer region has two separate
    pieces at one value of the outer variable. The check walks a line across the outer region
    and counts the runs of admissible samples. A count above one at any position would require
    a split.
    """
    print("--- Section: each outer region is one interval, so no order needs a split ---")
    for form_name, outer_positions in (
        ("dz_dy_dx", np.linspace(-1.999, 1.999, 41)),
        ("dz_dx_dy", np.linspace(0.001, 3.999, 41)),
    ):
        largest_run_count = 0
        for outer_value in outer_positions:
            if form_name == "dz_dy_dx":
                line = np.linspace(-1.0, 5.0, LINE_SAMPLE_COUNT)
                mask = limits_are_met(form_name, outer_value, line, np.zeros_like(line))
            else:
                line = np.linspace(-2.2, 2.2, LINE_SAMPLE_COUNT)
                mask = limits_are_met(form_name, line, outer_value, np.zeros_like(line))
            largest_run_count = max(largest_run_count, count_runs(mask))
        print(f"form {ORDER_LABELS[form_name]}: positions tested = {len(outer_positions)}, "
              f"largest count of separate runs = {largest_run_count}")
        assert largest_run_count <= 1, "an outer region has two pieces at one position"


def check_values_of_both_orders() -> None:
    """Compare the two orders with the exact rational multiple of pi."""
    print("--- Section: the value of each order for two test functions ---")
    test_cases = ((0, 0, 0), (2, 0, 0))
    worst_difference = 0.0
    for form_name, integrate in (("dz_dy_dx", evaluate_dz_dy_dx), ("dz_dx_dy", evaluate_dz_dx_dy)):
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
    """Run every check of Part 4 and print the compared values."""
    check_limits_cover_the_solid()
    check_half_width_in_z()
    check_no_split_is_needed()
    check_values_of_both_orders()
    print("Part 4: every compared pair agrees within the stated tolerance.")


if __name__ == "__main__":
    main()
