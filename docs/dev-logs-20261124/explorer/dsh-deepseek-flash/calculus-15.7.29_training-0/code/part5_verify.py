"""Verification of Part 5: the two orders with the inner integral in x.

The script checks four facts. First, a random tuple inside the printed limits of either order
maps to a point of the solid, and a random point of the solid satisfies the printed limits.
Second, the half width in x at a fixed pair (y, z) from a root find on the upper surface agrees
with the closed form sqrt(4 - y - 4*z**2). Third, each outer region is one interval at every
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
from iteration_forms import ORDER_LABELS, evaluate_dx_dy_dz, evaluate_dx_dz_dy, limits_are_met
from solid_geometry import inside_solid

# Random seed of every sampled check in this script.
RANDOM_SEED = 20261124

# Count of random points of each sampled check.
SAMPLE_COUNT = 200_000

# Count of samples along one line of the contiguity check.
LINE_SAMPLE_COUNT = 4001

# Pairs (y, z) of the root-find check. Each pair satisfies 4 - y - 4*z**2 > 0.
ROOT_FIND_PAIRS = ((0.0, 0.0), (2.0, 0.5), (2.0, -0.5), (3.0, 0.4), (1.0, 0.8), (3.9, 0.1))

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
    """Draw points from the printed limits of one order with the inner integral in x.

    Args:
        form_name: Name of the form, either dx_dz_dy or dx_dy_dz.
        count: Count of points to draw.

    Returns:
        The three coordinate arrays of the drawn points.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    outer = generator.uniform(0.0, 1.0, count)
    middle_unit = generator.uniform(-1.0, 1.0, count)
    inner_unit = generator.uniform(-1.0, 1.0, count)
    if form_name == "dx_dz_dy":
        y = 4.0 * outer
        half_width_z = np.sqrt(np.maximum(4.0 - y, 0.0)) / 2.0
        z = middle_unit * half_width_z
        half_width_x = np.sqrt(np.maximum(4.0 - y - 4.0 * z**2, 0.0))
        x = inner_unit * half_width_x
    elif form_name == "dx_dy_dz":
        z = 2.0 * outer - 1.0
        upper_y = np.maximum(4.0 - 4.0 * z**2, 0.0)
        y = upper_y * (middle_unit + 1.0) / 2.0
        half_width_x = np.sqrt(np.maximum(4.0 - 4.0 * z**2 - y, 0.0))
        x = inner_unit * half_width_x
    else:
        raise ValueError(f"the form {form_name} does not have the inner integral in x")
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
    for form_name in ("dx_dz_dy", "dx_dy_dz"):
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


def check_half_width_in_x() -> None:
    """Compare the half width in x from a root find with the closed form."""
    print("--- Section: the half width in x at a fixed pair (y, z) ---")
    worst_difference = 0.0
    for position_y, position_z in ROOT_FIND_PAIRS:
        radicand = 4.0 - position_y - 4.0 * position_z**2
        print(f"    pair (y, z) = ({position_y:.2f}, {position_z:.2f}) has 4 - y - 4*z**2 = "
              f"{radicand:.6f}")
        assert radicand > 0.0, "the pair lies above the top wall, so it has no root"
        root = brentq(
            lambda value: 4.0 - value**2 - 4.0 * position_z**2 - position_y,
            0.0,
            2.0,
        )
        difference = report(
            f"half width in x at (y, z) = ({position_y:.2f}, {position_z:.2f})",
            root,
            math.sqrt(radicand),
        )
        worst_difference = max(worst_difference, difference)
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
    """Check that each outer region is one interval at every fixed value of its outer variable."""
    print("--- Section: each outer region is one interval, so no order needs a split ---")
    for form_name, outer_positions, line_low, line_high in (
        ("dx_dz_dy", np.linspace(0.001, 3.999, 41), -1.2, 1.2),
        ("dx_dy_dz", np.linspace(-0.999, 0.999, 41), -1.0, 5.0),
    ):
        largest_run_count = 0
        for outer_value in outer_positions:
            line = np.linspace(line_low, line_high, LINE_SAMPLE_COUNT)
            if form_name == "dx_dz_dy":
                mask = limits_are_met(form_name, np.zeros_like(line), outer_value, line)
            else:
                mask = limits_are_met(form_name, np.zeros_like(line), line, outer_value)
            largest_run_count = max(largest_run_count, count_runs(mask))
        print(f"form {ORDER_LABELS[form_name]}: positions tested = {len(outer_positions)}, "
              f"largest count of separate runs = {largest_run_count}")
        assert largest_run_count <= 1, "an outer region has two pieces at one position"


def check_values_of_both_orders() -> None:
    """Compare the two orders with the exact rational multiple of pi."""
    print("--- Section: the value of each order for two test functions ---")
    test_cases = ((0, 0, 0), (0, 0, 2))
    worst_difference = 0.0
    for form_name, integrate in (("dx_dz_dy", evaluate_dx_dz_dy), ("dx_dy_dz", evaluate_dx_dy_dz)):
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
    """Run every check of Part 5 and print the compared values."""
    check_limits_cover_the_solid()
    check_half_width_in_x()
    check_no_split_is_needed()
    check_values_of_both_orders()
    print("Part 5: every compared pair agrees within the stated tolerance.")


if __name__ == "__main__":
    main()
